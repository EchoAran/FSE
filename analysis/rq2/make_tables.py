"""Create the RQ2 paper table of paired mean-score gains."""

import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binomtest


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = Path(__file__).resolve().parent / "tables"
DIMENSIONS = ("local_coherence", "transition_quality", "contingent_responsiveness")
BASELINES = (("hashimoto", "Hashimoto"), ("llmrei-long", "LLMREI-long"), ("sparkme", "SparkMe"))


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def format_cell(estimate, low, high, signed=False):
    point = f"{estimate:+.3f}" if signed else f"{estimate:.3f}"
    return f"{point} [{low:.3f}, {high:.3f}]"


def paired_sign_tests():
    case_scores = {(row["case_id"], row["method_id"]): row
                   for row in read_csv(ROOT / "analysis/rq2/case_means.csv")}
    cases = sorted({case for case, method in case_scores})
    tests = []
    for baseline, label in BASELINES:
        for dimension in DIMENSIONS:
            differences = np.array([float(case_scores[case, "proposed_method"][dimension])
                                    - float(case_scores[case, baseline][dimension]) for case in cases])
            wins, losses = int(np.sum(differences > 0)), int(np.sum(differences < 0))
            tests.append({"baseline": baseline, "dimension": dimension, "n_cases": len(cases),
                          "wins": wins, "ties": int(np.sum(differences == 0)), "losses": losses,
                          "n_non_ties": wins + losses,
                          "p_raw": float(binomtest(wins, wins + losses, alternative="two-sided").pvalue)})
    order = np.argsort([row["p_raw"] for row in tests])
    adjusted = np.minimum(1, np.maximum.accumulate(
        np.array([tests[i]["p_raw"] for i in order]) * np.arange(len(tests), 0, -1)))
    for i, value in zip(order, adjusted):
        tests[i]["p_holm_9"] = float(value)
    with (OUTPUT / "paired_sign_tests.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(tests[0]))
        writer.writeheader()
        writer.writerows(tests)
    return {(row["baseline"], row["dimension"]): row for row in tests}


def main():
    OUTPUT.mkdir(exist_ok=True)
    paired = {(row["method_b"], row["dimension"]): row
              for row in read_csv(ROOT / "analysis/rq2/paired_comparisons.csv")}
    tests = paired_sign_tests()
    records = []
    for baseline, label in BASELINES:
        record = {"baseline": baseline, "label": label, "n_cases": 69}
        for dimension in DIMENSIONS:
            row = paired[baseline, dimension]
            record.update({f"{dimension}_estimate": float(row["mean_difference"]),
                           f"{dimension}_ci_low": float(row["ci_low"]),
                           f"{dimension}_ci_high": float(row["ci_high"]),
                           f"{dimension}_p_raw": tests[baseline, dimension]["p_raw"],
                           f"{dimension}_p_holm_9": tests[baseline, dimension]["p_holm_9"]})
        records.append(record)
    with (OUTPUT / "table1_summary.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)

    plt.rcParams.update({
        "font.family": "serif", "font.serif": ["Times New Roman"], "font.size": 9,
        "svg.fonttype": "none", "pdf.fonttype": 42,
    })
    columns = (0.015, 0.42, 0.66, 0.90)
    fig, ax = plt.subplots(figsize=(6.6, 1.6))
    fig.subplots_adjust(left=0.025, right=0.975, bottom=0.04, top=0.98)
    ax.set(xlim=(0, 1), ylim=(0, 4.95))
    ax.axis("off")
    headers = ("Baseline", "Local\nCoherence", "Transition\nQuality", "Contingent\nResponsiveness")
    for x, header in zip(columns, headers):
        ax.text(x, 4.15, header, ha="left" if x == columns[0] else "center",
                va="center", fontsize=9, fontweight="bold", linespacing=1.05)
    ax.hlines((4.75, 3.4, 0.25), 0, 1, colors="#202020", linewidths=(0.9, 0.5, 0.9))
    markdown = ["| Baseline | Local Coherence | Transition Quality | Contingent Responsiveness |",
                "|:--|:--:|:--:|:--:|"]
    latex = [r"\begin{table}[t]", r"\centering",
             r"\caption{Paired mean score gains of ElicitMind over baselines [95\% CI] across 69 Cases.}",
             r"\label{tab:rq2-results}", r"\small", r"\setlength{\tabcolsep}{3pt}",
             r"\begin{tabular*}{\linewidth}{@{\extracolsep{\fill}}lccc@{}}", r"\toprule",
             r"Baseline & \shortstack{Local\\Coherence} & \shortstack{Transition\\Quality} & \shortstack{Contingent\\Responsiveness} \\", r"\midrule"]
    for (baseline, label), y in zip(BASELINES, (2.65, 1.65, 0.65)):
        cells = []
        for dimension in DIMENSIONS:
            row = paired[baseline, dimension]
            cells.append(format_cell(float(row["mean_difference"]), float(row["ci_low"]),
                                     float(row["ci_high"]), signed=True))
        for x, value in zip(columns, (label, *cells)):
            ax.text(x, y, value, ha="left" if x == columns[0] else "center", va="center", fontsize=8.5)
        markdown.append("| " + " | ".join([label, *cells]) + " |")
        latex.append(" & ".join([label, *[f"${cell}$" for cell in cells]]) + r" \\")
    latex.extend([r"\bottomrule", r"\end{tabular*}", r"\end{table}"])
    (OUTPUT / "table1_summary.md").write_text("\n".join(markdown) + "\n", encoding="utf-8")
    (OUTPUT / "table1_summary.tex").write_text("\n".join(latex) + "\n", encoding="utf-8")
    save_table(fig, "table1_summary")
    print("Created the compact RQ2 paired-gain table; full sign tests remain in CSV.")

def save_table(fig, name):
    fig.savefig(OUTPUT / f"{name}.svg", facecolor="white")
    fig.savefig(OUTPUT / f"{name}.pdf", facecolor="white")
    fig.savefig(OUTPUT / f"{name}.png", dpi=600, facecolor="white")
    plt.close(fig)

if __name__ == "__main__":
    main()
