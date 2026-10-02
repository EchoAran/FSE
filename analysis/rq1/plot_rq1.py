"""Build the RQ1 distribution figures and significance table from Case artifacts."""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import logging
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy
from matplotlib.colors import to_rgba
from scipy.stats import binomtest, friedmanchisquare


METHODS = ("hashimoto", "llmrei-long", "sparkme", "proposed_method")
LABELS = ("Hashimoto", "LLMREI-long", "SparkMe", "Ours")
COLORS = ("#3B6FB6", "#2A9D8F", "#D9A441", "#B84A62")
LINESTYLES = ("--", "-.", ":", "-")
MARKERS = ("o", "s", "^", "*")
MARKER_SIZES = (4.0, 4.0, 4.8, 6.5)
SEED = 31017
BOOTSTRAP_REPEATS = 10000
ROOT = Path(__file__).resolve().parents[2]
LOG = logging.getLogger("rq1-analysis")


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream]


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def load_inputs(artifacts: Path) -> tuple[list[str], list[dict], dict]:
    cases = sorted(path.name for path in (artifacts / "cases").iterdir() if path.is_dir())
    rows, histograms = [], {}
    for case in cases:
        folder = artifacts / "cases" / case
        metrics = read_jsonl(folder / "elaboration" / "transcript_metrics.jsonl")
        transcripts = read_jsonl(folder / "ingestion" / "transcripts.jsonl")
        answers = read_jsonl(folder / "ingestion" / "responses.jsonl")
        unique_rius = read_jsonl(folder / "riu" / "unique_rius.jsonl")
        with (folder / "elaboration" / "cluster_depths.csv").open(encoding="utf-8-sig") as stream:
            cluster_depths = list(csv.DictReader(stream))
        if len(metrics) != len(METHODS) or {r["method_id"] for r in metrics} != set(METHODS):
            raise ValueError(f"Incomplete or duplicated method inventory: {case}")
        by_method = {r["method_id"]: r for r in metrics}
        transcript_map = {r["method_id"]: r for r in transcripts}
        for method in METHODS:
            metric = by_method[method]
            transcript = transcript_map[method]
            transcript_id = f"{case}::{method}"
            if metric["case_id"] != case or metric["transcript_id"] != transcript_id:
                raise ValueError(f"Metric identity mismatch: {transcript_id}")
            depths = {int(d): count for d, count in metric["depth_counts"].items()}
            observed = Counter(
                int(r["depth"]) for r in cluster_depths if r["transcript_id"] == transcript_id
            )
            if depths != observed or sum(depths.values()) != metric["breadth"]:
                raise ValueError(f"DAG depth histogram mismatch: {transcript_id}")
            response_count = sum(r["transcript_id"] == transcript_id for r in answers)
            yield_count = sum(r["transcript_id"] == transcript_id for r in unique_rius)
            if response_count != transcript["completed_turns"] or yield_count != metric["yield"]:
                raise ValueError(f"Response or unique RIU count mismatch: {transcript_id}")
            if metric["breadth"] <= 0:
                raise ValueError(f"Conditional depth retention is undefined: {transcript_id}")
            rows.append(dict(case_id=case, method_id=method, transcript_id=transcript_id,
                             yield_count=metric["yield"], breadth=metric["breadth"],
                             response_count=response_count))
            histograms[case, method] = depths
    return cases, rows, histograms


def holm(p_values: list[float]) -> np.ndarray:
    order = np.argsort(p_values)
    adjusted = np.empty(len(order))
    adjusted[order] = np.minimum(1, np.maximum.accumulate(
        np.asarray(p_values)[order] * np.arange(len(order), 0, -1)
    ))
    return adjusted


def significance(matrices: dict[str, np.ndarray]) -> tuple[list[dict], list[dict]]:
    comparisons, omnibus = [], []
    for metric, matrix in matrices.items():
        overall = friedmanchisquare(*matrix.T)
        omnibus.append(dict(metric=metric, n_cases=len(matrix), statistic=float(overall.statistic),
                            p_raw=float(overall.pvalue)))
        for a, b in itertools.combinations(range(len(METHODS)), 2):
            wins = int(np.count_nonzero(matrix[:, b] > matrix[:, a]))
            losses = int(np.count_nonzero(matrix[:, b] < matrix[:, a]))
            ties = len(matrix) - wins - losses
            p_value = float(binomtest(wins, wins + losses, alternative="two-sided").pvalue)
            comparisons.append(dict(metric=metric, method_a=METHODS[a], method_b=METHODS[b],
                                    n_cases=len(matrix), b_wins=wins, ties=ties, b_losses=losses,
                                    n_non_ties=wins + losses, p_raw=p_value))
    for record, adjusted in zip(comparisons, holm([r["p_raw"] for r in comparisons])):
        record["p_holm_12"] = float(adjusted)
    for record, adjusted in zip(omnibus, holm([r["p_raw"] for r in omnibus])):
        record["p_holm_2"] = float(adjusted)
    return comparisons, omnibus


def depth_retention(cases: list[str], histograms: dict) -> tuple[np.ndarray, list[dict], list[dict], list[dict]]:
    max_depth = max(d for counts in histograms.values() for d in counts)
    retention = np.empty((len(cases), len(METHODS), max_depth))
    counts_rows, case_rows = [], []
    for i, case in enumerate(cases):
        for j, method in enumerate(METHODS):
            counts = histograms[case, method]
            breadth = sum(counts.values())
            for d in range(1, max_depth + 1):
                value = sum(count for depth, count in counts.items() if depth >= d) / breadth
                retention[i, j, d - 1] = value
                counts_rows.append(dict(case_id=case, method_id=method, depth=d,
                                        dag_count=counts.get(d, 0)))
                case_rows.append(dict(case_id=case, method_id=method, minimum_depth=d,
                                      breadth=breadth, retained_fraction=value))
    indices = np.random.default_rng(SEED).integers(len(cases), size=(BOOTSTRAP_REPEATS, len(cases)))
    summary = []
    for j, method in enumerate(METHODS):
        bootstrap = retention[indices, j, :].mean(axis=1)
        low, high = np.percentile(bootstrap, [2.5, 97.5], axis=0)
        for d in range(1, max_depth + 1):
            summary.append(dict(method_id=method, minimum_depth=d, n_cases=len(cases),
                                mean_case_fraction=float(retention[:, j, d - 1].mean()),
                                ci95_low=float(low[d - 1]), ci95_high=float(high[d - 1])))
    return retention, counts_rows, case_rows, summary


def configure_style() -> None:
    plt.rcParams.update({
        "font.family": "serif", "font.serif": ["Times New Roman"],
        "font.size": 9.5, "mathtext.fontset": "custom",
        "mathtext.rm": "Times New Roman", "mathtext.it": "Times New Roman:italic",
        "mathtext.bf": "Times New Roman:bold", "mathtext.fallback": None,
        "axes.labelsize": 10, "axes.labelweight": "bold", "axes.linewidth": 0.65,
        "axes.spines.top": False, "axes.spines.right": False,
        "xtick.labelsize": 9, "ytick.labelsize": 9,
        "xtick.major.width": 0.65, "ytick.major.width": 0.65,
        "legend.fontsize": 9, "legend.frameon": False,
        "svg.fonttype": "none", "pdf.fonttype": 42,
        "figure.facecolor": "white", "axes.facecolor": "white",
        "savefig.dpi": 600,
    })


def save_figure(fig: plt.Figure, path: Path) -> None:
    fig.savefig(path.with_suffix(".pdf"), dpi=600)
    fig.savefig(path.with_suffix(".svg"), dpi=600)
    fig.savefig(path.with_suffix(".png"), dpi=600)
    plt.close(fig)


def plot_distributions(matrices: dict, folder: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 3.0))
    rng = np.random.default_rng(SEED)
    for ax, (metric, matrix), letter in zip(axes, matrices.items(), ("a", "b")):
        boxes = ax.boxplot(matrix, positions=np.arange(4), widths=0.52, patch_artist=True,
                           showfliers=False, whis=1.5,
                           medianprops=dict(color="#303030", linewidth=1.2),
                           whiskerprops=dict(color="#555555", linewidth=0.75),
                           capprops=dict(color="#555555", linewidth=0.75))
        for j, color in enumerate(COLORS):
            boxes["boxes"][j].set(facecolor=to_rgba(color, 0.18), edgecolor=color, linewidth=1.0)
            jitter = rng.permutation(np.linspace(-0.16, 0.16, len(matrix)))
            ax.scatter(j + jitter, matrix[:, j], s=9, color=color, alpha=0.72,
                       edgecolors="white", linewidths=0.25, zorder=3)
        ax.set_xticks(np.arange(4), ("Hashimoto", "LLMREI-\nlong", "SparkMe", "Ours"))
        ax.set_ylabel("Unique RIUs" if metric == "yield" else "Covered clusters")
        ax.set_ylim(bottom=0, top=float(matrix.max()) * 1.08)
        ax.set_xlim(-0.6, 3.6)
        ax.grid(axis="y", color="#E7E7E7", linewidth=0.5)
        ax.set_axisbelow(True)
        ax.text(0, 1.035, f"({letter}) {metric.capitalize()}", transform=ax.transAxes,
                fontsize=10, fontweight="bold")
    fig.subplots_adjust(left=0.085, right=0.995, bottom=0.15, top=0.915, wspace=0.25)
    save_figure(fig, folder / "fig1_yield_breadth")


def plot_depth(summary: list[dict], folder: Path) -> None:
    fig, ax = plt.subplots(figsize=(6.6, 2.75))
    for method, label, color, linestyle, marker, size in zip(
        METHODS, LABELS, COLORS, LINESTYLES, MARKERS, MARKER_SIZES
    ):
        records = [r for r in summary if r["method_id"] == method and r["minimum_depth"] <= 8]
        depths = [r["minimum_depth"] for r in records]
        percentages = [100 * r["mean_case_fraction"] for r in records]
        ax.fill_between(depths, [100 * r["ci95_low"] for r in records],
                        [100 * r["ci95_high"] for r in records], color=color, alpha=0.09)
        ax.plot(depths, percentages, label=label, color=color, linestyle=linestyle,
                linewidth=1.4, marker=marker, markersize=size, markerfacecolor="white",
                markeredgecolor=color, markeredgewidth=0.9)
    ax.set_xlabel(r"Minimum elaboration depth $d$")
    ax.set_ylabel(r"Covered clusters with depth $\geq d$ (%)")
    ax.set_xlim(0.75, max(depths) + 0.25)
    ax.set_xticks(range(1, 9))
    ax.set_ylim(-2, 103)
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.grid(axis="y", color="#E7E7E7", linewidth=0.5)
    ax.set_axisbelow(True)
    fig.legend(*ax.get_legend_handles_labels(), loc="upper center", bbox_to_anchor=(0.55, 1.0),
               ncol=4, columnspacing=1.5, handlelength=2.5)
    fig.subplots_adjust(left=0.11, right=0.995, bottom=0.17, top=0.87)
    save_figure(fig, folder / "fig2_depth_retention")


def format_p(value: float) -> str:
    return f"{value:.3g}"


def format_quartiles(values: np.ndarray) -> str:
    q1, median, q3 = np.percentile(values, [25, 50, 75])
    return f"{median:g} [{q1:g}, {q3:g}]"


def build_table(matrices: dict, responses: np.ndarray, comparisons: list[dict], folder: Path) -> str:
    p_map = {(r["method_a"], r["metric"]): r["p_holm_12"] for r in comparisons
             if r["method_b"] == "proposed_method"}
    header = ["Method", "Yield: median [Q1, Q3]", "p (Holm)",
              "Breadth: median [Q1, Q3]", "p (Holm)", "Responses: median [Q1, Q3]"]
    markdown = ["| " + " | ".join(header) + " |", "|:--|--:|--:|--:|--:|--:|"]
    csv_rows, latex_rows = [], []
    for j, (method, label) in enumerate(zip(METHODS, LABELS)):
        p_yield = p_map[method, "yield"] if method != "proposed_method" else ""
        p_breadth = p_map[method, "breadth"] if method != "proposed_method" else ""
        values = [label, format_quartiles(matrices["yield"][:, j]),
                  format_p(p_yield) if p_yield != "" else "—",
                  format_quartiles(matrices["breadth"][:, j]),
                  format_p(p_breadth) if p_breadth != "" else "—",
                  format_quartiles(responses[:, j])]
        markdown.append("| " + " | ".join(values) + " |")
        latex_values = values.copy()
        for k in (2, 4):
            if values[k] == "—":
                latex_values[k] = "--"
            elif "e" in values[k]:
                mantissa, exponent = values[k].split("e")
                latex_values[k] = f"${mantissa}\\times10^{{{int(exponent)}}}$"
        if method == "proposed_method":
            latex_values = [f"\\textbf{{{value}}}" for value in latex_values]
        latex_rows.append(" & ".join(latex_values) + r" \\")
        record = dict(method_id=method, n_cases=len(responses))
        for name, matrix in [*matrices.items(), ("response_count", responses)]:
            q1, median, q3 = np.percentile(matrix[:, j], [25, 50, 75])
            record.update({f"{name}_median": float(median), f"{name}_q1": float(q1), f"{name}_q3": float(q3)})
        record.update(p_yield_holm_vs_ours=p_yield, p_breadth_holm_vs_ours=p_breadth)
        csv_rows.append(record)
    table = "\n".join(markdown)
    (folder / "table1_summary.md").write_text(table + "\n", encoding="utf-8")
    write_csv(folder / "table1_summary.csv", csv_rows)
    latex = r"""\begin{table}[t]
\centering
\caption{Requirement-information outcomes across 69 matched Cases. Values are medians [Q1, Q3].}
\label{tab:rq1-results}
\small
\setlength{\tabcolsep}{4pt}
\begin{tabular}{lrrrrr}
\toprule
 & \multicolumn{2}{c}{Yield} & \multicolumn{2}{c}{Breadth} & Responses \\
\cmidrule(lr){2-3}\cmidrule(lr){4-5}
Method & Median [Q1, Q3] & $p_{\mathrm{Holm}}$ & Median [Q1, Q3] & $p_{\mathrm{Holm}}$ & Median [Q1, Q3] \\
\midrule
""" + "\n".join(latex_rows) + r"""
\bottomrule
\end{tabular}
\par\smallskip
\begin{minipage}{\linewidth}\footnotesize
The $p$ values compare each baseline with Ours using two-sided exact paired sign tests.
Ties are omitted from each test. Holm adjustment covers all 12 pairwise tests across
the four methods and the two outcomes, including baseline--baseline comparisons.
Depth is reported as a distribution in Figure~\ref{fig:rq1-depth}, not as a scalar endpoint.
\end{minipage}
\end{table}
"""
    (folder / "table1_summary.tex").write_text(latex, encoding="utf-8")
    return table


def write_report(output: Path, cases: list[str], rows: list[dict], table: str, retention: list[dict]) -> None:
    curve = {(r["method_id"], r["minimum_depth"]): r for r in retention}
    ours2 = 100 * curve["proposed_method", 2]["mean_case_fraction"]
    spark2 = 100 * curve["sparkme", 2]["mean_case_fraction"]
    ours3 = 100 * curve["proposed_method", 3]["mean_case_fraction"]
    spark3 = 100 * curve["sparkme", 3]["mean_case_fraction"]
    response_medians = {
        method: float(np.median([r["response_count"] for r in rows if r["method_id"] == method]))
        for method in METHODS
    }
    report = f"""# RQ1 statistical analysis and visualization

## Dataset and outcome definitions

All {len(cases)} Cases, {len(rows)} transcripts, and {sum(r['response_count'] for r in rows):,} responses were included.
The four methods are matched within each Case, with one complete interview per Case/method.
The analysis unit is the Case, not an RIU, response, or DAG.
Yield is the within-transcript unique RIU count; Breadth is the covered shared-cluster count.
Input checks confirmed unique RIU counts, response counts, and agreement between cluster_depths.csv and depth_counts.
No model calls, outlier exclusions, or Case subsampling were performed.

## Table 1: raw outcomes and significance

{table}

Quartiles use NumPy's linear interpolation convention. Both p columns report two-sided exact sign tests against Ours.
The null hypothesis is equal win/loss probability among non-tied Cases. Ties are excluded from each test and explicitly counted in paired_sign_tests.csv.
Holm adjustment covers all six method pairs across two outcomes, forming one family of 12 comparisons; comparisons were not selected by significance.
These tests assess consistency of the within-Case win direction, not the magnitude of a difference between marginal medians.
Friedman omnibus results are provided separately in omnibus_tests.csv, with a distinct two-test Holm family. They do not replace pairwise comparisons.

## Figure 1: Yield and Breadth distributions

![Yield and Breadth distributions](figures/fig1_yield_breadth.png)

Boxes span Q1--Q3, center lines indicate medians, and whiskers reach the most extreme observations within 1.5 IQR.
Each point is an observed Case/method outcome. All observations, including points beyond the whiskers, are retained.
Horizontal jitter changes display positions only. There are no mean bars, paired-difference plots, or ratio plots.
Ours has higher marginal medians than all three baselines, but distributions overlap, especially with SparkMe.
This pattern must not be described as Ours winning on every Case.

## Figure 2: Case-equal depth retention (option B)

![Case-equal depth retention](figures/fig2_depth_retention.png)

Let N(c,m,k) count the DAGs at exact depth k for Case c and method m.
S(c,m,d) = sum(k >= d) N(c,m,k) / Breadth(c,m). Each curve is the arithmetic mean of these Case-specific fractions, with equal Case weights.
Exact DAG-depth counts remain available in source_data/depth_counts.csv; they were not reduced to MeanDepth.
Shading shows pointwise 95% percentile intervals from {BOOTSTRAP_REPEATS:,} Case bootstrap resamples, with seed {SEED}.
Every resample uses the same Case indices for the four methods. These are not simultaneous bands, and interval overlap is not a significance test.
All transcripts have positive Breadth, so no conditional fractions were missing or excluded.
Figure 2 displays depths 1--8 to avoid compressing the main pattern with a sparse tail.
The complete depth 1--{max(r['minimum_depth'] for r in retention)} data remain in the exported CSV files; depths above 8 still contribute to cumulative fractions at the displayed thresholds.

At depth at least 2, the Case-equal fractions are {ours2:.2f}% for Ours and {spark2:.2f}% for SparkMe; at depth at least 3, they are {ours3:.2f}% and {spark3:.2f}%, respectively.
These are reading aids for the full curve, not independently selected significance endpoints.
The distribution of longer elaboration chains can be described, but this analysis does not establish statistically significant Depth superiority over SparkMe.

## Interpretation boundaries

Median response counts are Ours {response_medians['proposed_method']:g}, SparkMe {response_medians['sparkme']:g}, LLMREI-long {response_medians['llmrei-long']:g}, and Hashimoto {response_medians['hashimoto']:g}.
Table 1 measures complete-interview total outcomes, not equal-turn, equal-token, or equal-API-cost performance; it does not establish an efficiency advantage.
Curve intervals reflect empirical uncertainty in Case composition, not repeated-interview or LLM-pipeline variability within a Case.
Tests and resampling assume approximately independent Cases. Potential source-level dependencies were not audited here; conclusions are bounded to this benchmark and current run.
Crossing curves should not be described as uniform Depth superiority. No scalar Depth endpoint or per-depth significance tests were created.
The default artifact root currently lacks a manual-review summary. No quality pass rates were fabricated; automatic-outcome statistics do not replace the single reviewer's four quality checks.
This plan was specified after results were visible; it is not a preregistered analysis.

## Manuscript-ready captions and statistical description

**Figure 1. Distributions of requirement-information outcomes across 69 matched Cases.**
(a) Within-transcript unique RIU counts (Yield). (b) Shared-cluster coverage counts (Breadth).
Boxes show the interquartile range, center lines indicate medians, and whiskers extend to the most extreme observations within 1.5 IQR.
All 69 observations per method are shown, including observations beyond the whiskers. Horizontal jitter affects display positions only.

**Figure 2. Case-equal elaboration-depth retention.**
At each integer depth d, the retained fraction is the proportion of a transcript's covered clusters with DAG depth at least d.
Lines show the mean of the Case-specific fractions, giving all 69 Cases equal weight.
Distinct markers identify the evaluated integer depths; straight connecting lines and shading between depths are visual guides, not estimates at fractional depths.
All four methods start at 100% at depth 1 because every covered cluster has depth at least 1.
Shading indicates pointwise 95% percentile confidence intervals from 10,000 paired Case bootstrap resamples (seed 31017), not simultaneous confidence bands or significance tests.
No transcript had zero Breadth. Display is restricted to depths 1--8; the full depth distribution remains available in the source data.

**Statistical analysis.** Yield and Breadth were summarized using medians and first and third quartiles across 69 matched Cases.
Pairwise comparisons used two-sided exact sign tests, excluding ties, with Holm adjustment across all 12 comparisons involving four methods and two outcomes.
The tests assess the balance of within-Case wins and losses rather than the magnitude of a difference between marginal medians.
Depth was analyzed as a complete distribution using Case-equal retention curves and paired Case bootstrap intervals.
Each method was run once per Case; resampling Cases does not quantify within-Case run-to-run variability.

## Style and reproducibility

Serif typography, light axes, and compact panels follow the supplied reference's visual style.
Both figures use a coordinated blue, teal, gold, and berry palette. Figure 2 distinguishes methods with circles, squares, triangles, and stars, as well as different line styles.
The reference's statistical logic, logarithmic axes, radar charts, and result wording were not copied.
Published FSE figure and table layouts informed the compact panels and booktabs table. Method colors and English labels remain consistent.
The design width is 6.6 inches; use LaTeX width=\\linewidth to fit the current FSE/PACMSE single-column manuscript rather than assuming a universal double-column format.
PDFs embed TrueType fonts, SVGs retain text, and PNGs are exported at 600 dpi. Check label size after manuscript scaling.
All new scripts and outputs are under analysis/rq1. Evaluation code, original results, and reference files remain unchanged.

Style context: [FSE 2024 multi-panel distributions](https://cabird.com/pdfs/_FSE_24__Replicating_Software_Engineering_Research_with_LLMs.pdf),
[FSE 2024 Distinguished Paper table layout](https://arxiv.org/abs/2402.02063).
Layout reference: [FSE 2026 Research Papers formatting instructions](https://conf.researchr.org/track/fse-2026/fse-2026-research-papers).
Statistical references: [Benavoli et al., pairwise comparisons across datasets](https://jmlr.org/papers/volume17/benavoli16a/benavoli16a.pdf),
[Demsar, comparisons over multiple datasets](https://www.jmlr.org/papers/v7/demsar06a.html).
These references inform matched-Case comparisons; they are not evidence about the present methods' performance.

Software: Python, NumPy {np.__version__}, SciPy {scipy.__version__}, Matplotlib {matplotlib.__version__}.
"""
    (output / "analysis.md").write_text(report, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path, default=ROOT / "evolution/rq1/artifacts")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(message)s")
    LOG.setLevel(logging.INFO)
    cases, rows, histograms = load_inputs(args.artifacts.resolve())
    LOG.info("Loaded %d Cases, %d transcripts, %d responses", len(cases), len(rows),
             sum(r["response_count"] for r in rows))
    matrices = {name: np.array([r[key] for r in rows]).reshape(len(cases), 4)
                for name, key in [("yield", "yield_count"), ("breadth", "breadth")]}
    responses = np.array([r["response_count"] for r in rows]).reshape(len(cases), 4)
    output = args.output.resolve()
    for name in ("figures", "tables", "source_data"):
        (output / name).mkdir(parents=True, exist_ok=True)
    write_csv(output / "source_data/case_metrics.csv", rows)
    comparisons, omnibus = significance(matrices)
    write_csv(output / "tables/paired_sign_tests.csv", comparisons)
    write_csv(output / "tables/omnibus_tests.csv", omnibus)
    table = build_table(matrices, responses, comparisons, output / "tables")
    LOG.info("Calculated all 12 pairwise sign tests with global Holm adjustment")
    _, counts_rows, case_rows, retention = depth_retention(cases, histograms)
    write_csv(output / "source_data/depth_counts.csv", counts_rows)
    write_csv(output / "source_data/case_depth_retention.csv", case_rows)
    write_csv(output / "tables/depth_retention.csv", retention)
    LOG.info("Calculated full depth retention and %d paired Case bootstrap resamples", BOOTSTRAP_REPEATS)
    configure_style()
    plot_distributions(matrices, output / "figures")
    plot_depth(retention, output / "figures")
    write_report(output, cases, rows, table, retention)
    LOG.info("Exported both figures as PDF/SVG/PNG and the significance table as CSV/Markdown/LaTeX")
    LOG.info("Analysis written to %s", output / "analysis.md")


if __name__ == "__main__":
    main()
