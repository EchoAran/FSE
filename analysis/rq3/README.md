# RQ3 downstream implementation analysis

RQ3 uses one two-panel figure and one four-method table to report observable requirement scale, cross-run judgment agreement, and complete five-run outcomes. Five selected Cases each have four interview-derived specifications and five independent implementations, giving 100 coding runs.

## Reproduce

From the repository root, using Python with matplotlib:

```powershell
python analysis/rq3/analyze_rq3.py
```

Read a different complete artifact directory with the same five-Case/four-method/five-run design:

```powershell
python analysis/rq3/analyze_rq3.py --artifacts-root <artifacts-directory>
```

The script reads `evolution/rq3/cases.jsonl` and each Case/method's `srs/reviewed_srs.json`, `srs/scenarios.csv`, and `evaluations/reviewed_judgments.json`. It runs locally from saved data and writes only to this analysis directory. The imported reviewed judgments are the analysis source.

## Scope and measures

The paper analyzes requirements assigned `evaluation_scope=required` and classified as functional requirements (FR), business rules and constraints (BR), or exception boundaries (EX). The figure separates FR from BR+EX; the table pools all three. The source matrix retains all 1,301 evaluable requirements and their 6,505 run judgments. The main behavioral scope contains 1,102 requirements; the other 199 quality/interface requirements remain available in the `all_evaluable` summaries.

An evaluable observation has status `observed_satisfied`, `observed_partial`, or `observed_unsatisfied`. Each Case/method/requirement is counted once, using its five run judgments.

| Measure | Definition |
| --- | --- |
| N | Number of requirements in scope |
| O | Requirements with at least one evaluable observation |
| R | Requirements with at least two evaluable observations |
| S | Judgment-consistent requirements: requirements in R whose observed judgments agree across runs |
| A | Conditional judgment agreement, S/R |
| R5 | Requirements observed in all five runs |
| S5 | Requirements with five identical observed judgments |
| P5 | Requirements satisfied in all five runs |

S is decomposed into consistently satisfied, consistently partially satisfied, and consistently unsatisfied requirements. R-S counts varying judgments. Unobserved runs do not enter the judgment comparison. A rate with a zero denominator is left blank in the source CSV.

## Analysis and paper presentation

Counts are summed across the five Cases. Conditional agreement is the pooled S divided by pooled R. Case-level paired differences for O and S are summarized by mean, median, range, and higher/equal/lower Case counts, keeping the Case as the comparison unit. RQ3 uses descriptive statistics and complete five-run observation analysis. Overall behavioral comparisons and BR+EX comparisons are reported within their respective scopes.

The main figure is a quantitative comparison grid with two panels: functional requirements and rules/boundaries. Each bar contains repeatedly observed requirements, partitioned into three consistent statuses and varying labels. Bar-top labels show S/R. The two panels use separate count scales. The table reports N, O, R, S (A), and R5/S5/P5. The result text proceeds from overall scale, to functional/boundary composition, to complete five-run outcomes. The overall Case-paired comparison belongs with the overall behavioral results.

The figure inherits the RQ1/RQ2 Times New Roman typography and 6.6-inch width, with a shared status palette rather than method colors. Figure dimensions are 6.6 × 2.8 inches; table preview dimensions are 6.6 × 1.6 inches. SVG/PDF retain editable text, and PNG is exported at 600 dpi.

## Outputs

| File | Contents |
| --- | --- |
| `analyze_rq3.py` | Complete analysis and rendering script |
| `requirements.csv` | 1,301 requirements, five original labels each, derived observation and agreement fields |
| `case_summary.csv` | 80 Case/method/scope summaries, including all-evaluable, behavioral, functional, and boundary scopes |
| `method_summary.csv` | 16 pooled method/scope summaries, including unrounded rates |
| `paired_comparisons.csv` | 24 descriptive Case-paired O/S comparisons against the three baselines |
| `source_manifest.json` | Case/method/run scope and SHA-256 hashes of all 60 input artifacts |
| `rq3_implementation_outcomes.png`, `.svg`, `.pdf` | The two-panel paper figure |
| `table_rq3_summary.md`, `.tex`, `.png`, `.svg`, `.pdf` | The four-row paper table and previews |
| `results.md` | Generated numerical results, English Results paragraphs, and figure caption |
| `answer_rq3.md` | Chinese narrative roles and proposed Answer to RQ3 |
| `qa.md` | Numerical, reproducibility, and rendered-output verification |

The LaTeX table is a `table*` fragment requiring `booktabs`; it inherits the manuscript font. Its caption defines all symbols. The generated PDF is a matplotlib preview, not a compilation of the LaTeX fragment.
