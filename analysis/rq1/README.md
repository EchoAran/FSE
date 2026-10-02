# RQ1 analysis and figures

This directory contains a standalone, read-only analysis of the existing Case artifacts. It does not invoke a model, change the evaluation pipeline, or modify source results.

## Run

From the repository root, use a Python environment containing NumPy, SciPy, Matplotlib, and the Times New Roman font:

```powershell
python analysis/rq1/plot_rq1.py
```

The current Anaconda Python environment has these packages; the project `.venv` does not currently contain Matplotlib. No project dependency files were changed.

Optional input and output locations:

```powershell
python analysis/rq1/plot_rq1.py --artifacts evolution/rq1/artifacts --output analysis/rq1
```

Rerunning replaces the named analysis outputs. It does not delete directories or invalidate evaluation checkpoints.

## Outputs

- `figures/fig1_yield_breadth.pdf`, `.svg`, `.png`: two panels of raw Yield and Breadth distributions. Boxes show median/IQR; all Case observations remain visible.
- `figures/fig2_depth_retention.pdf`, `.svg`, `.png`: the Case-equal depth retention curve displayed over depths 1--8, with distinct markers, straight connecting lines, and pointwise bootstrap intervals. All methods start at 100% at depth 1. Full depth 1--18 data remain in the CSV outputs. There is no depth-count heatmap and no MeanDepth scalar.
- `tables/table1_summary.csv`, `.md`, `.tex`: four-method descriptive summaries and baseline-versus-Ours adjusted significance values.
- `tables/paired_sign_tests.csv`: all 12 pairwise tests, including ties and effective sample sizes. Holm correction is applied to the entire 12-test family.
- `tables/omnibus_tests.csv`: Friedman tests for Yield and Breadth, with a separate two-test Holm family.
- `tables/depth_retention.csv`: method-level curve values and pointwise 95% intervals.
- `source_data/`: raw Case metrics, complete exact-depth counts, and Case-level retention fractions.
- `analysis.md`: analysis definitions, results, interpretation boundaries, and ready-to-use English captions.
- `QA.md`: numerical checks, export checks, visual inspection, and target-specific preflight exceptions.

## Statistical scope

The independent analysis unit is the Case; four methods are matched within each Case. Pairwise significance uses two-sided exact sign tests, not a displayed difference or ratio metric. Ties are excluded from the tests and explicitly counted. All raw p values retain numerical precision.

Depth retention is computed within each transcript before averaging Cases with equal weights. Confidence intervals use 10,000 Case bootstrap resamples with seed 31017, keeping the four methods together in each resample. They are pointwise intervals, not simultaneous bands or tests of Depth superiority.

The figures describe complete-interview information outcomes, not equal-budget efficiency. One interview per method/Case does not identify run-to-run variation. Manual RIU quality review remains a separate requirement.

## Manuscript integration

The figures use an English, serif, compact FSE-style layout with consistent colors, editable SVG text, embedded TrueType PDF fonts, and 600 dpi PNGs. The table uses `booktabs`, which must be loaded in the manuscript preamble. Figure 2 should be labeled `fig:rq1-depth` if the table's cross-reference is retained.

Include each PDF with `width=\linewidth` and inspect the actual manuscript size. The explicit design canvas is 6.6 inches wide; it is not a claim that FSE requires a double-column layout.
