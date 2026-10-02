# RQ3 results

| Method | N | O | R | S (A) | R5 / S5 / P5 |
| --- | ---: | ---: | ---: | ---: | ---: |
| LLMREI-long | 115 | 71 | 48 | 32 (66.7%) | 11 / 7 / 6 |
| Hashimoto | 139 | 91 | 71 | 55 (77.5%) | 16 / 14 / 12 |
| SparkMe | 405 | 162 | 112 | 82 (73.2%) | 28 / 16 / 11 |
| ElicitMind | 443 | 213 | 143 | 101 (70.6%) | 48 / 28 / 13 |

## Results text

After a common SRS conversion, each method's interview results were used for five independent implementations. ElicitMind produced 213 behavioral requirements with at least one evaluable observation, 143 with repeated observations, and 101 with consistent judgments across observed runs, giving a conditional judgment agreement rate of 70.6%. Its observable and judgment-consistent counts exceeded those of the three baselines. Within the overall behavioral scope, observable counts were higher in 5, 4, and 3 Cases, and judgment-consistent counts in 5, 4, and 2 Cases, relative to LLMREI-long, Hashimoto, and SparkMe.

The judgment-consistent requirements comprised 81 functional requirements and 20 business rules or exception boundaries. Within the rules and boundaries scope, 45 requirements had at least one evaluable observation and 26 had repeated observations. Observable and judgment-consistent counts exceeded those of the three baselines, extending the validation scope to conditions, constraints, and exception handling.

With complete observation across all five runs, 48 behavioral requirements were evaluable in every run, 28 had identical judgments, and 13 were satisfied in every implementation. All three counts exceeded those of the three baselines.

## Figure caption

Cross-run implementation outcomes for (a) functional requirements and (b) business rules and exception boundaries across five Cases, with five independent implementations per Case and method. Bars include requirements with at least two evaluable observations. Segments distinguish consistently satisfied, consistently partially satisfied, consistently unsatisfied, and varying judgment labels. Labels above bars show consistent/repeatedly observed requirement counts. The two panels use separate count scales.
