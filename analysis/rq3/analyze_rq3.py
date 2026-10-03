"""Describe reviewed RQ3 requirement outcomes and export one figure and one table."""

import argparse
import csv
import hashlib
import json
from pathlib import Path
from statistics import mean, median

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = Path(__file__).resolve().parent
METHODS = ("llmrei-long", "hashimoto", "sparkme", "proposed_method")
LABELS = ("LLMREI-long", "Hashimoto", "SparkMe", "ElicitMind")
FUNCTIONAL = {"functional_requirement"}
BOUNDARY = {"business_rule_constraint", "exception_boundary"}
SCOPES = {"all_evaluable": None, "behavioral": FUNCTIONAL | BOUNDARY,
          "functional": FUNCTIONAL, "boundary": BOUNDARY}
OBSERVED = ("observed_satisfied", "observed_partial", "observed_unsatisfied")
COLORS = ("#3B6FB6", "#75AFA8", "#B9BEC7", "#D9A441")
HATCHES = (None, None, "..", "//")
CAPTION = (
    "Cross-run implementation outcomes for (a) functional requirements and (b) business rules "
    "and exception boundaries across five Cases, with five independent implementations per "
    "Case and method. Bars include requirements with at least two evaluable observations. "
    "Segments distinguish consistently satisfied, consistently partially satisfied, consistently "
    "unsatisfied, and varying judgment labels. Labels above bars show consistent/repeatedly "
    "observed requirement counts. The two panels use separate count scales."
)


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def load_requirements(artifacts_root, cases):
    rows, sources = [], []
    for case in cases:
        for method in METHODS:
            directory = artifacts_root / "cases" / case / method
            paths = [directory / "srs/reviewed_srs.json", directory / "srs/scenarios.csv",
                     directory / "evaluations/reviewed_judgments.json"]
            sources.extend({"path": path.relative_to(artifacts_root).as_posix(),
                            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()} for path in paths)
            srs = json.loads(paths[0].read_text(encoding="utf-8"))
            with paths[1].open(encoding="utf-8-sig", newline="") as handle:
                scenarios = list(csv.DictReader(handle))
            required = {row["requirement_id"] for row in scenarios if row["evaluation_scope"] == "required"}
            judgments = json.loads(paths[2].read_text(encoding="utf-8"))
            index = {(row["requirement_id"], row["run_index"]): row["status"] for row in judgments}
            for item in srs["items"]:
                requirement = item["requirement_id"]
                if requirement not in required:
                    continue
                statuses = [index[requirement, run] for run in range(1, 6)]
                observed = [status for status in statuses if status in OBSERVED]
                repeated = len(observed) >= 2
                consistent = repeated and len(set(observed)) == 1
                rows.append({
                    "case_id": case, "method_id": method, "requirement_id": requirement,
                    "type": item["type"], "statement": item["statement"],
                    **{f"run_{run}": status for run, status in enumerate(statuses, 1)},
                    "observed_runs": len(observed), "repeated": int(repeated),
                    "consistent": int(consistent), "consistent_status": observed[0] if consistent else "",
                    "fully_observed": int(len(observed) == 5),
                    "fully_consistent": int(len(observed) == 5 and consistent),
                    "fully_satisfied": int(len(observed) == 5 and set(observed) == {OBSERVED[0]}),
                })
    return rows, sources


def summarize(rows):
    result = {"N": len(rows), "O": sum(row["observed_runs"] > 0 for row in rows),
              "R": sum(row["repeated"] for row in rows), "S": sum(row["consistent"] for row in rows)}
    for name, status in zip(("satisfied", "partial", "unsatisfied"), OBSERVED):
        result[name] = sum(row["consistent_status"] == status for row in rows)
    result.update({"varying": result["R"] - result["S"],
                   "R5": sum(row["fully_observed"] for row in rows),
                   "S5": sum(row["fully_consistent"] for row in rows),
                   "P5": sum(row["fully_satisfied"] for row in rows)})
    result["observability_rate"] = result["O"] / result["N"] if result["N"] else ""
    result["agreement_rate"] = result["S"] / result["R"] if result["R"] else ""
    result["full_agreement_rate"] = result["S5"] / result["R5"] if result["R5"] else ""
    return result


def save_figure(fig, prefix):
    fig.savefig(OUTPUT / f"{prefix}.svg", facecolor="white")
    fig.savefig(OUTPUT / f"{prefix}.pdf", facecolor="white")
    fig.savefig(OUTPUT / f"{prefix}.png", dpi=600, facecolor="white")
    plt.close(fig)


def plot_outcomes(summary):
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.8))
    fig.subplots_adjust(left=0.08, right=0.99, bottom=0.26, top=0.86, wspace=0.23)
    for ax, scope, title, limit, ticks in zip(
        axes, ("functional", "boundary"),
        ("(a) Functional requirements", "(b) Business rules and exception boundaries"),
        (125, 30), (range(0, 126, 25), range(0, 31, 5)),
    ):
        for m, method in enumerate(METHODS):
            row = summary[method, scope]
            bottom = 0
            for name, color, hatch in zip(("satisfied", "partial", "unsatisfied", "varying"), COLORS, HATCHES):
                height = row[name]
                ax.bar(m, height, bottom=bottom, width=0.58, color=color,
                       edgecolor="white", linewidth=0.6, hatch=hatch, zorder=3)
                if height >= limit * 0.06:
                    ax.text(m, bottom + height / 2, str(height), ha="center", va="center",
                            fontsize=8, color="white" if name == "satisfied" else "#202020")
                bottom += height
            ax.text(m, row["R"] + limit * 0.025, f'{row["S"]}/{row["R"]}',
                    ha="center", va="bottom", fontsize=8.5)
        ax.set(xlim=(-0.5, 3.5), ylim=(0, limit))
        ax.set_yticks(ticks)
        ax.set_xticks(range(4), ("LLMREI-\nlong", "Hashimoto", "SparkMe", "ElicitMind"))
        ax.tick_params(axis="x", labelsize=8, pad=4, length=3)
        ax.tick_params(axis="y", labelsize=9, length=3)
        ax.grid(axis="y", color="#E7E7E7", linewidth=0.5, zorder=0)
        ax.text(0, 1.06, title, transform=ax.transAxes, ha="left", va="bottom",
                fontsize=9.5, fontweight="bold")
    axes[0].set_ylabel("Requirements with repeated observations", fontsize=9)
    handles = [Patch(facecolor=color, edgecolor="white", hatch=hatch, label=label)
               for color, hatch, label in zip(COLORS, HATCHES,
                   ("Consistently satisfied", "Consistently partially satisfied", "Consistently not satisfied", "Varying verdicts"))]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, 0.02),
               ncol=4, fontsize=7.5, handlelength=1.5, columnspacing=1.2)
    save_figure(fig, "rq3_implementation_outcomes")


def make_table(summary):
    markdown = ["| Method | N | O | R | S (A) | R5 / S5 / P5 |",
                "| --- | ---: | ---: | ---: | ---: | ---: |"]
    latex = [r"\begin{table*}[t]", r"\centering",
             r"\caption{Downstream outcomes of behavioral requirements (FR, BR, and EX) across five Cases. "
             r"$N$: evaluated requirements; $O$: at least one evaluable observation; $R$: at least two; "
             r"$S$: unchanged labels among $R$, with $A=S/R$. $R_5$: all five runs observed; "
             r"$S_5$: all five labels identical; $P_5$: all five satisfied.}",
             r"\label{tab:rq3-results}", r"\small", r"\setlength{\tabcolsep}{4pt}",
             r"\begin{tabular*}{\linewidth}{@{\extracolsep{\fill}}lrrrrc@{}}", r"\toprule",
             r"Method & $N$ & $O$ & $R$ & $S$ ($A$) & $R_5 / S_5 / P_5$ \\", r"\midrule"]
    fig, ax = plt.subplots(figsize=(6.6, 1.6))
    fig.subplots_adjust(left=0.025, right=0.975, bottom=0.04, top=0.98)
    ax.set(xlim=(0, 1), ylim=(0, 5.25))
    ax.axis("off")
    columns = (0.015, 0.30, 0.42, 0.54, 0.72, 0.92)
    for x, label in zip(columns, ("Method", "N", "O", "R", "S (A)", "R₅ / S₅ / P₅")):
        ax.text(x, 4.55, label, ha="left" if x == columns[0] else "center",
                va="center", fontsize=9, fontweight="bold")
    ax.hlines((5.0, 4.05, 0.35), 0, 1, colors="#202020", linewidths=(0.9, 0.5, 0.9))
    for m, (method, label) in enumerate(zip(METHODS, LABELS)):
        row = summary[method, "behavioral"]
        cells = [label, str(row["N"]), str(row["O"]), str(row["R"]),
                 f'{row["S"]} ({100 * row["agreement_rate"]:.1f}%)',
                 f'{row["R5"]} / {row["S5"]} / {row["P5"]}']
        markdown.append("| " + " | ".join(cells) + " |")
        latex.append(" & ".join(cell.replace("%", r"\%") for cell in cells) + r" \\")
        for x, value in zip(columns, cells):
            ax.text(x, 3.55 - m * 0.9, value, ha="left" if x == columns[0] else "center",
                    va="center", fontsize=8.5, fontweight="bold" if m == 3 else "normal")
    latex.extend([r"\bottomrule", r"\end{tabular*}", r"\end{table*}"])
    (OUTPUT / "table_rq3_summary.md").write_text("\n".join(markdown) + "\n", encoding="utf-8")
    (OUTPUT / "table_rq3_summary.tex").write_text("\n".join(latex) + "\n", encoding="utf-8")
    save_figure(fig, "table_rq3_summary")
    return markdown


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts-root", type=Path, default=ROOT / "evolution/rq3/artifacts")
    args = parser.parse_args()
    cases_file = ROOT / "evolution/rq3/cases.jsonl"
    cases = [json.loads(line)["case_id"] for line in cases_file.read_text(encoding="utf-8").splitlines() if line.strip()]
    requirements, sources = load_requirements(args.artifacts_root, cases)
    write_csv(OUTPUT / "requirements.csv", requirements)
    case_rows, method_rows = [], []
    for scope, types in SCOPES.items():
        selected = [row for row in requirements if types is None or row["type"] in types]
        for method in METHODS:
            subset = [row for row in selected if row["method_id"] == method]
            method_rows.append({"method_id": method, "scope": scope, **summarize(subset)})
            for case in cases:
                case_rows.append({"case_id": case, "method_id": method, "scope": scope,
                                  **summarize([row for row in subset if row["case_id"] == case])})
    write_csv(OUTPUT / "case_summary.csv", case_rows)
    write_csv(OUTPUT / "method_summary.csv", method_rows)
    case_index = {(row["case_id"], row["method_id"], row["scope"]): row for row in case_rows}
    pairs = []
    for scope in SCOPES:
        for metric in ("O", "S"):
            for baseline in METHODS[:-1]:
                differences = [case_index[case, METHODS[-1], scope][metric] - case_index[case, baseline, scope][metric]
                               for case in cases]
                pairs.append({"baseline": baseline, "scope": scope, "metric": metric, "n_cases": len(cases),
                              "mean_difference": mean(differences), "median_difference": median(differences),
                              "min_difference": min(differences), "max_difference": max(differences),
                              "wins": sum(value > 0 for value in differences),
                              "ties": differences.count(0), "losses": sum(value < 0 for value in differences)})
    write_csv(OUTPUT / "paired_comparisons.csv", pairs)
    manifest = {"cases": cases, "methods": METHODS, "runs_per_srs": 5,
                "cases_sha256": hashlib.sha256(cases_file.read_bytes()).hexdigest(), "sources": sources,
                "evaluable_requirements": len(requirements),
                "behavioral_requirements": sum(row["type"] in FUNCTIONAL | BOUNDARY for row in requirements)}
    (OUTPUT / "source_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman"],
                         "font.size": 9.5, "svg.fonttype": "none", "pdf.fonttype": 42,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "axes.linewidth": 0.65, "legend.frameon": False})
    summary = {(row["method_id"], row["scope"]): row for row in method_rows}
    plot_outcomes(summary)
    table = make_table(summary)
    ours = summary[METHODS[-1], "behavioral"]
    ratios = ", ".join(f'{ours["S"] / summary[method, "behavioral"]["S"]:.2f}×' for method in METHODS[:-1])
    pair_index = {(row["baseline"], row["scope"], row["metric"]): row for row in pairs}
    wins = {metric: ", ".join(str(pair_index[method, "behavioral", metric]["wins"]) for method in METHODS[:-1])
            for metric in ("O", "S")}
    results = ["# RQ3 results", "", *table, "", "## Results text", "",
               f'ElicitMind yielded {ours["O"]} behavioral requirements with at least one evaluable observation, '
               f'{ours["R"]} with repeated observations, and {ours["S"]} with unchanged labels. '
               f'The consistent requirement counts were {ratios} those of LLMREI-long, Hashimoto, and SparkMe, '
               f'respectively, with a conditional agreement rate of {100 * ours["agreement_rate"]:.1f}%.', "",
               f'The consistent outcomes comprised {summary[METHODS[-1], "functional"]["S"]} functional '
               f'requirements and {summary[METHODS[-1], "boundary"]["S"]} business rules or exception boundaries. '
               f'The latter included {summary[METHODS[-1], "boundary"]["O"]} requirements with at least one '
               f'observation and {summary[METHODS[-1], "boundary"]["R"]} with repeated observations. '
               f'ElicitMind had higher observable counts in {wins["O"]} Cases and higher consistent counts '
               f'in {wins["S"]} Cases against the three baselines, respectively.', "",
               f'Under complete observation across all five runs, {ours["R5"]} behavioral requirements were '
               f'evaluable in every run, {ours["S5"]} had identical labels, and {ours["P5"]} were satisfied '
               'in all five implementations.', "", "## Figure caption", "", CAPTION, ""]
    (OUTPUT / "results.md").write_text("\n".join(results), encoding="utf-8")
    print(f'Analyzed {len(cases)} Cases, {len(METHODS)} methods, {len(requirements)} evaluable requirements; '
          f'{manifest["behavioral_requirements"]} behavioral requirements. Exported one figure and one table.')


if __name__ == "__main__":
    main()
