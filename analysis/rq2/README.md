# RQ2 aggregate analysis

The figure compares four methods on the three flow-quality dimensions using three aligned panels. Each bar shows the overall four-rater mean score across 69 Cases, with a Case-bootstrap 95% confidence interval and a numerical mean label. The figure has no overall heading, footer, or agreement annotations. Numerical paired contrasts are reported in the accompanying table. The bar axis starts at zero; individual ratings range from one to five.

The style follows the existing RQ1 figures: Times New Roman throughout, plain left-aligned panel headings, light horizontal grids, horizontal method labels and a consistent blue/teal/gold/berry palette. Bars have lightly tinted fills and method-colored outlines. Only the final figure and table exports are retained.

## Reproduce

From the repository root:

```powershell
python analysis/rq2/analyze_rq2.py
```

Build the compact paper table from the existing Case means and paired-comparison CSVs, including exact paired sign tests and Holm correction:

```powershell
python analysis/rq2/make_tables.py
```

The paper uses one figure and one table to answer RQ2. The figure shows the absolute scores of four methods. The table has three baseline rows and three dimension columns, showing paired mean gains (ElicitMind minus baseline) [95% CI] to three decimal places. It has no footnotes. Overall four-rater agreement belongs in the evaluation text; significance across all nine comparisons can be reported in one Results sentence. Complete win/tie/loss counts and exact p values remain in CSV. `answer_rq2.md` records this evidence chain and a proposed Answer to RQ2.

Inputs are the four current rating CSVs under `evolution/rq2/artifacts/ratings`. An alternative complete rating directory can be supplied with `--ratings-dir`. The random seed defaults to 31017 and bootstrap repeats to 10000, matching the current RQ2 statistics configuration; both can be supplied as command-line arguments. The script leaves the evaluation pipeline and input scores unchanged.

## Statistical unit and aggregation

For each Case, method and dimension, first average the two LLM and two human ratings with equal weights. Average those transcript-level scores across the 69 Cases with equal Case weights. All 3,312 original scores contribute. Four ratings of a transcript do not create four independent Cases. High inter-rater agreement supports consistency; it does not by itself establish rating validity.

For each of the three baselines and three dimensions, calculate the Case-level difference between the ElicitMind and the baseline after rater aggregation. Generate 10,000 bootstrap samples of 69 complete Cases with replacement. Each draw retains the Case's complete method-by-dimension matrix. Use the same draws for all means and contrasts. Recompute average differences for each draw and take the 2.5th and 97.5th percentiles for the pointwise 95% confidence interval. The four evaluators are held fixed; uncertainty reflects variation over Cases. Original per-rater confidence-interval endpoints are not averaged.

Following RQ1, use two-sided exact paired sign tests on these Case-level differences. Exclude ties and test whether wins and losses have equal probability among non-tied Cases, using `scipy.stats.binomtest` with probability 0.5. This tests directional consistency across Cases, not whether the population mean difference is zero. Apply Holm correction jointly to the nine ElicitMind-versus-baseline tests (three baselines by three dimensions). The confidence intervals remain pointwise 95% intervals; correcting the p values does not make these simultaneous intervals. All nine Holm-adjusted p values are below 0.05; the largest is 2.4021645783633976e-09. Agreement estimates are reported with confidence intervals without additional hypothesis tests.

## Outputs

| File | Contents |
| --- | --- |
| `rq2_mean_scores.png` | Rendered figure preview, 600 dpi |
| `rq2_mean_scores.svg`, `rq2_mean_scores.pdf` | Editable vector figure, 6.6 × 2.75 inches, matching the RQ1 design width |
| `case_means.csv` | 276 transcript-level three-dimensional four-rater means |
| `score_summary.csv` | 12 aggregate means, Case-level median/quartiles and newly calculated mean CIs |
| `paired_comparisons.csv` | Nine aggregate paired contrasts, new CIs and higher/equal/lower counts |
| `agreement.csv` | Nine ordinal agreement estimates and CIs for LLM, human and all-four rater groups; copied unchanged from the evaluation report |
| `results.md` | Compact manuscript-facing mean and paired-contrast tables |
| `tables/paired_sign_tests.csv` | Nine exact paired sign tests: Case counts, wins/ties/losses, raw p values and Holm-adjusted p values |
| `tables/table1_summary.csv` | Full-precision gains, confidence intervals and p values for three baselines by three dimensions |
| `tables/table1_summary.md`, `.tex` | Compact paired-gain table, three rows by three dimensions |
| `tables/table1_summary.png`, `.svg`, `.pdf` | Times New Roman comparison table preview, 6.6 × 1.6 inches; statistic definition belongs in the table caption |
| `answer_rq2.md` | Manuscript evidence roles, necessary reporting and proposed Answer to RQ2 |

The figure is a quantitative comparison grid with shared scoring axes. SVG/PDF retain editable text. PNG is the raster preview; TIFF is not part of this vector delivery. The Python backend generates all graphics. All original scores contribute to the displayed aggregate means and confidence intervals.

## Verification

All 12 aggregate means were checked against the four original rater-level report means, allowing only the original report's rounding precision. All nine paired intervals were independently reproduced by directly resampling the saved Case-level differences, with agreement within 1e-12. Higher/equal/lower counts sum to 69 for every contrast. The style revision retains byte-identical Case means, score summaries and paired-comparison CSVs. The generic Nature preflight does not recognize the explicitly requested Times New Roman font and flags the RQ1-style 6.6-inch width. These are intentional style choices, verified in the rendered files. Other chart warnings concern the intentionally omitted TIFF and the bootstrap random-number generator: the generator resamples observed Cases and does not simulate score data. The rendered chart was inspected for scale, colors and axis-label visibility. The table PDF retains Times New Roman text with all text bounds inside the page. The table layout revision preserves all original paired-gain estimates, intervals and sign-test p values.

The RQ1 and RQ2 analysis guides and retained outputs are tracked as part of the experiment artifact. Reproduction uses the saved ratings and Case-level data.

## Table integration

The LaTeX fragment requires `\usepackage{booktabs}` in the manuscript preamble and can be included with `\input{analysis/rq2/tables/table1_summary.tex}` when compiling from the repository root. It follows the RQ1 table conventions and inherits the manuscript's font. Its float label is `tab:rq2-results`. The PNG/PDF/SVG preview uses Times New Roman; it is rendered by Python, not by compiling the LaTeX fragment. The fragment has not been compiled in the manuscript template.

All nine displayed gains and their 18 interval endpoints are copied from the existing paired-comparison artifact. The table script additionally computes the nine sign tests from `case_means.csv` and applies Holm correction; raw and adjusted p values are retained in the full-precision table CSV. Exact binomial probabilities were independently verified using integer binomial coefficients, and Holm-adjusted values were verified with a separate sorted cumulative-maximum calculation. Wins/ties/losses match the original paired-comparison CSV for all nine contrasts. The table uses 69 matched Case pairs; complete Cases are the bootstrap resampling unit.

`agreement.csv` is a retained copy of `evolution/rq2/artifacts/reports/agreement.csv`. Agreement calculation belongs to the existing evaluation reporting code in `evolution/rq2/report.py`; the two local scripts reproduce the final mean-score figure, paired-gain table and sign tests from the original ratings.

## Suggested figure caption

Full-transcript flow-quality scores for four interview methods on Local Coherence, Transition Quality and Contingent Responsiveness. Each bar shows the mean across 69 Cases after averaging the two LLM and two human evaluator scores for each transcript. Capped error bars show pointwise 95% percentile Case-bootstrap confidence intervals (10,000 draws). Labels show the overall mean to two decimal places. Paired differences and their confidence intervals are reported in the accompanying table.
