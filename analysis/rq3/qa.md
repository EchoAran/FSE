# RQ3 analysis verification

Verified on 2026-10-03 using the five selected Cases, four methods, and five runs per specification.

## Numerical verification

- All 6,505 labels in the 1,301-row source matrix match the imported reviewed judgments, compared independently by Case/method/requirement/run.
- A separate vectorized calculation reproduces all 16 method/scope and 80 Case/method/scope summaries, including N, O, R, S, the three consistent statuses, varying labels, R5, S5, and P5.
- All observability and agreement rates reproduce the saved numerator/denominator; undefined rates remain blank.
- All 24 Case-paired comparisons reproduce the means, medians, ranges, and higher/equal/lower counts.
- The main scope contains all 1,102 required FR/BR/EX items. The 199 other evaluable items remain in the source matrix and all-evaluable summaries.
- Bar components sum to R, and the three consistent components sum to S. The pooled main counts reproduce 32/55/82/101 consistent requirements and 7/14/16/28 complete-five-run consistent requirements.
- All 60 input artifact hashes match the source manifest and their pre-analysis snapshots.
- A complete rerun produces byte-identical requirement, Case, method, and paired CSVs, source manifest, Markdown/LaTeX table, and Results text (eight outputs).

## Figure contract and rendering

The figure supports the conclusion that ElicitMind produces a larger repeatedly observable requirement set, with consistent results across both functional and boundary requirements. Its two panels form a quantitative comparison grid. Figure data come directly from the functional and boundary rows in `method_summary.csv`; table data come from its behavioral rows. No error bars or significance markers are used.

The figure is 6.6 × 2.8 inches (475.2 × 201.6 PDF points); the table preview is 6.6 × 1.6 inches (475.2 × 115.2 points). PNG dimensions are 3,960 × 1,680 and 3,960 × 960 pixels, with 600-dpi metadata. Both PDFs embed Times New Roman regular and bold fonts. Minimum extracted text sizes are 7.5 pt for the figure and 8.5 pt for the table. All extracted text bounds are inside their PDF pages, and both SVGs contain editable text.

The rendered figure and table were inspected for panel alignment, bar labels, status distinctions, legend fit, horizontal method labels, and table column alignment. Labels inside small segments are omitted when they would not fit; all segment counts remain in the source data. Bar-top S/R annotations cover every method, including the 0/1 boundary result.

The generic Nature source preflight passes syntax, size, palette, editable-text, vector-export, resolution, data-integrity, and Python-only checks. Its font rule accepts only sans-serif families; the inherited RQ1/RQ2 Times New Roman choice is verified directly in both rendered PDFs. Its 183-mm width and TIFF recommendations differ from the agreed 6.6-inch PDF/SVG plus PNG delivery. These format findings are resolved against the repository's figure contract rather than changing the paper's existing style.

The LaTeX artifact is a booktabs `table*` fragment. It has not been compiled in the manuscript template; the delivered table preview is rendered by matplotlib.

## Documentation

The narrative chain, repository README, RQ3 workflow README, infrastructure index, and evidence/evaluation interface document use the same FR/BR/EX scope and N/O/R/S/A/R5/S5/P5 definitions. Existing experiment artifacts are unchanged, and documentation edits are confined to RQ3 text. The paper plan contains one figure and one table, with Case-paired directions summarized in text.
