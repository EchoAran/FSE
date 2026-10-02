# Verification notes

## Numerical checks

- All 69 Cases contain all four methods: 276 metric rows and 7,454 responses.
- Unique RIU counts and response counts agree with the formal upstream artifacts.
- Exact-depth histograms agree with the upstream cluster-depth records and sum to each transcript's Breadth.
- All 4,968 Case-level retention fractions were independently recomputed from the exported exact-depth counts. The 72 method-level means agree with their equally weighted Case fractions.
- Exported retention curves start at 1, are non-increasing, and retain depths 1 through 18. Bootstrap interval bounds are ordered and within [0, 1]. Figure 2 displays only depths 1 through 8.
- All 12 sign-test probabilities were independently checked using binomial coefficients; the full-family Holm adjustments were checked separately.
- All summary-table medians and quartiles were checked against the exported Case metrics.
- The Breadth sensitivity table was recomputed from the per-Case `clustering/threshold_sensitivity.csv` files for both alternative cutoffs, and the primary-cutoff row was checked against the Yield/Breadth descriptives. All 18 cutoff-level sign tests were independently checked, and each cutoff's six Holm adjustments were verified as a separate family. Every baseline-versus-ElicitMind comparison is significant after adjustment (largest adjusted p = 6.74e-05), and ElicitMind has the highest median Breadth at all three cutoffs.

These are deterministic data and statistical checks, not a manual assessment of LLM extraction or judgment quality. No scratch test code was added to the repository.

After the palette and marker revision, all nine table and source-data files were compared with their previous contents and remained byte-for-byte identical. No outcomes, confidence intervals, or significance results changed.

## Figure and language checks

Figures 1 and 2 were visually inspected. Figure 1's method labels are separated, all observations are retained, and neither panel uses a truncated lower axis. Both figures use the same blue, teal, gold, and berry method colors. Figure 2 displays depths 1--8, starting at 100% at depth 1, with circles, squares, triangles, and stars plus distinct line styles. Straight lines and interpolated shading are display guides between evaluated integer depths, not a smoothing model. Figure 3 was visually inspected: the four method curves are separated at every cutoff, the middle x tick is marked as the primary cutoff, the legend and axis labels stay inside the canvas, and each curve lies inside its shaded bootstrap band.

The user requested a display cutoff at depth 8. Of the 72 method/threshold summaries, 32 are displayed and 40 at depths 9--18 are hidden from the figure only. All 69 Cases and all clusters remain in the analysis. Clusters deeper than 8 still contribute to cumulative fractions at displayed thresholds. No separate 1% value filter is applied within depths 1--8; complete values and intervals remain in the CSV outputs.

All three PDFs have one page, selectable text, and embedded Times New Roman fonts. All three SVGs contain editable text and vector drawing elements rather than embedded raster images. PNG exports are 600 dpi: 3,960 by 1,800 pixels for Figure 1, and 3,960 by 1,650 pixels for Figures 2 and 3.

The compact layout retains the 6.6-inch width and all font sizes. Figure 1 is 3.0 inches high, with reduced outer margins, panel spacing, title offsets, and upper-axis headroom; its axes occupy approximately 62% of the canvas, compared with 51% before the layout revision. Figures 2 and 3 are 2.75 inches high, with reduced margins and legend-to-axes spacing. Renderer checks confirmed that axes text and legends lie within the canvas and neighboring method labels do not overlap. The nine table and source-data files from that revision remain unchanged; the threshold-sensitivity files are additions.

All newly created Python, Markdown, CSV, LaTeX, SVG, and extracted PDF text were checked for Chinese characters; none were found. The Python source compiles and has no trailing whitespace.

The LaTeX table was inspected as source, but was not compiled because no LaTeX executable was available. Check table width, figure label sizes, and cross-references in the actual manuscript template before submission.

## Automated preflight interpretation

The generic Nature-oriented figure validator reports 10 passes, three warnings, and one failure. It does not report an unconditional pass. The target-specific findings were reviewed as follows:

- **Font failure:** the validator recognizes a limited sans-serif list and does not recognize Times New Roman. Times New Roman is intentionally used to follow the supplied reference's serif style. The actual PDFs contain embedded font data; the style was not changed merely to satisfy this checker.
- **Width warning:** the 6.6-inch canvas is intentional for a compact FSE/PACMSE-style layout, not the validator's Nature-oriented 89/183 mm presets. Include the figure at `width=\linewidth` and verify the final manuscript layout.
- **Raster warning:** PDF and SVG are the vector deliverables; a 600 dpi PNG is also supplied. TIFF was not requested and was not generated.
- **Simulated-data warning:** the random generator resamples observed Cases for bootstrap intervals and permutes horizontal jitter positions. It does not generate synthetic outcome values.

The unresolved manuscript-level checks are final scaling and LaTeX compilation, not numerical integrity of the exported analysis.
