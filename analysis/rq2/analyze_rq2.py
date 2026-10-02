"""Aggregate four RQ2 raters and bootstrap complete Cases for paired contrasts."""

import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
import numpy as np


DIMENSIONS = ("local_coherence", "transition_quality", "contingent_responsiveness")
RATERS = ("llm_expert_1", "llm_expert_2", "human_expert_1", "human_expert_2")
METHODS = ("hashimoto", "llmrei-long", "sparkme", "proposed_method")
LABELS = ("Hashimoto", "LLMREI-long", "SparkMe", "Proposed method")
COLORS = ("#3B6FB6", "#2A9D8F", "#D9A441", "#B84A62")


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    root = Path(__file__).resolve().parents[2]
    output_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ratings-dir", type=Path, default=root / "evolution/rq2/artifacts/ratings")
    parser.add_argument("--seed", type=int, default=31017)
    parser.add_argument("--bootstrap-repeats", type=int, default=10000)
    args = parser.parse_args()

    ratings = {}
    for rater in RATERS:
        with (args.ratings_dir / f"{rater}.csv").open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        for row in rows:
            assert row["status"] == "scored" and row["rater_id"] == rater
            key = (row["case_id"], row["method_id"], row["dimension"], rater)
            assert key not in ratings
            ratings[key] = int(row["score"])

    cases = sorted({key[0] for key in ratings})
    assert len(ratings) == len(cases) * len(METHODS) * len(DIMENSIONS) * len(RATERS)
    case_means = np.array([
        [[np.mean([ratings[(case, method, dimension, rater)] for rater in RATERS])
          for dimension in DIMENSIONS] for method in METHODS] for case in cases
    ])
    n_cases = len(cases)
    means = case_means.mean(axis=0)
    rng = np.random.default_rng(args.seed)
    case_indices = rng.integers(0, n_cases, size=(args.bootstrap_repeats, n_cases))
    bootstrap_means = case_means[case_indices].mean(axis=1)
    mean_intervals = np.percentile(bootstrap_means, [2.5, 97.5], axis=0)

    case_rows = [
        {"case_id": case, "method_id": method,
         **{dimension: case_means[c, m, d] for d, dimension in enumerate(DIMENSIONS)}}
        for c, case in enumerate(cases) for m, method in enumerate(METHODS)
    ]
    summary_rows = [
        {"method_id": method, "dimension": dimension, "n_cases": n_cases, "n_raters": len(RATERS),
         "mean": means[m, d], "median": np.median(case_means[:, m, d]),
         "q1": np.quantile(case_means[:, m, d], 0.25, method="linear"),
         "q3": np.quantile(case_means[:, m, d], 0.75, method="linear"),
         "ci_low": mean_intervals[0, m, d], "ci_high": mean_intervals[1, m, d],
         "bootstrap_repeats": args.bootstrap_repeats, "random_seed": args.seed}
        for m, method in enumerate(METHODS) for d, dimension in enumerate(DIMENSIONS)
    ]
    paired_rows = []
    for m, baseline in enumerate(METHODS[:-1]):
        differences = case_means[:, -1, :] - case_means[:, m, :]
        bootstrap_differences = bootstrap_means[:, -1, :] - bootstrap_means[:, m, :]
        intervals = np.percentile(bootstrap_differences, [2.5, 97.5], axis=0)
        for d, dimension in enumerate(DIMENSIONS):
            paired_rows.append({
                "method_a": METHODS[-1], "method_b": baseline, "dimension": dimension,
                "n_pairs": n_cases, "mean_difference": differences[:, d].mean(),
                "median_difference": np.median(differences[:, d]),
                "n_a_higher": int(np.sum(differences[:, d] > 0)),
                "n_equal": int(np.sum(differences[:, d] == 0)),
                "n_b_higher": int(np.sum(differences[:, d] < 0)),
                "ci_low": intervals[0, d], "ci_high": intervals[1, d],
                "bootstrap_repeats": args.bootstrap_repeats, "random_seed": args.seed,
            })
    write_csv(output_dir / "case_means.csv", case_rows)
    write_csv(output_dir / "score_summary.csv", summary_rows)
    write_csv(output_dir / "paired_comparisons.csv", paired_rows)

    table = [
        "# RQ2 four-rater aggregate results", "",
        f"Each of the {n_cases} Cases contributes one four-rater mean per method and dimension.", "",
        "## Method means", "",
        "| Method | Local Coherence | Transition Quality | Contingent Responsiveness |",
        "| --- | ---: | ---: | ---: |",
    ]
    for m, label in enumerate(LABELS):
        table.append(f"| {label} | " + " | ".join(f"{value:.3f}" for value in means[m]) + " |")
    table.extend([
        "", "## Paired mean differences [95% CI]", "",
        "All contrasts are Proposed method minus baseline, paired within Case.", "",
        "| Baseline | Local Coherence | Transition Quality | Contingent Responsiveness |",
        "| --- | ---: | ---: | ---: |",
    ])
    for m, label in enumerate(LABELS[:-1]):
        rows = paired_rows[m * len(DIMENSIONS):(m + 1) * len(DIMENSIONS)]
        table.append(f"| {label} | " + " | ".join(
            f"{row['mean_difference']:.3f} [{row['ci_low']:.3f}, {row['ci_high']:.3f}]"
            for row in rows) + " |")
    table.extend([
        "", f"Percentile bootstrap: {args.bootstrap_repeats:,} draws; random seed {args.seed}.",
        "Each draw samples complete Cases with replacement, preserving all methods and dimensions.",
        "The four raters have equal fixed weights; rater scores and interval endpoints are not resampled separately.",
        "Intervals are pointwise 95% intervals, without a multiple-comparison adjustment. Exact paired sign-test p values and Holm correction are produced separately by make_tables.py.",
    ])
    (output_dir / "results.md").write_text("\n".join(table) + "\n", encoding="utf-8")

    plt.rcParams.update({
        "font.family": "serif", "font.serif": ["Times New Roman"],
        "font.size": 9.5, "svg.fonttype": "none", "pdf.fonttype": 42,
        "axes.labelsize": 10, "axes.labelweight": "bold",
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.linewidth": 0.65, "legend.frameon": False,
    })
    fig, axes = plt.subplots(1, 3, figsize=(6.6, 2.75), sharey=True)
    fig.subplots_adjust(left=0.07, right=0.99, bottom=0.17, top=0.90, wspace=0.13)
    titles = ("(a) Local Coherence", "(b) Transition Quality", "(c) Contingent Responsiveness")
    for d, ax in enumerate(axes):
        for m, label in enumerate(LABELS):
            mean = means[m, d]
            ax.bar(m, mean, width=0.58, color=to_rgba(COLORS[m], 0.18), edgecolor=COLORS[m],
                   linewidth=1.0, zorder=3)
            ax.errorbar(m, mean, yerr=np.array([[mean - mean_intervals[0, m, d]],
                                              [mean_intervals[1, m, d] - mean]]),
                        fmt="none", color="#555555", elinewidth=0.75, capsize=3, capthick=0.75, zorder=5)
            ax.text(m, mean_intervals[1, m, d] + 0.12, f"{mean:.2f}", ha="center", va="bottom", fontsize=8.5,
                    color="#303030")
        ax.set(xlim=(-0.46, 3.46), ylim=(0, 5))
        ax.set_yticks(range(6))
        ax.set_xticks(range(4), ["Hashimoto", "LLMREI-\nlong", "SparkMe", "Ours"])
        ax.tick_params(axis="x", length=3, width=0.65, pad=5, labelsize=7)
        ax.tick_params(axis="y", length=3, width=0.65, labelsize=9)
        ax.grid(axis="y", color="#E7E7E7", lw=0.5, zorder=0)
        ax.text(0, 1.035, titles[d], transform=ax.transAxes, ha="left", va="bottom",
                fontsize=9.5, fontweight="bold")
    axes[0].set_ylabel("Four-rater mean score")
    fig.savefig(output_dir / "rq2_mean_scores.svg", facecolor="white")
    fig.savefig(output_dir / "rq2_mean_scores.pdf", facecolor="white")
    fig.savefig(output_dir / "rq2_mean_scores.png", dpi=600, facecolor="white")
    plt.close(fig)
    print(f"Used {len(ratings)} ratings across {n_cases} Cases; exported 12 means and 9 paired contrasts.")


if __name__ == "__main__":
    main()
