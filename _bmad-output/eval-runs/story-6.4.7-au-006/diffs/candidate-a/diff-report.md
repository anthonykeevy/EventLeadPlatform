# Form AI Eval Diff Report

## Runs

- Baseline: `story-6.4.6-au-baseline-current`
- Variant: `story-6.4.7-au-006-candidate-a`

## Structural Summary

- Matched rows: 45
- Missing in variant: 0
- Extra in variant: 0

## Blocking Decision

- Blocked: `False`
- Reasons: none

## Advisory Metric Deltas

| Metric | Baseline Mean | Variant Mean | Delta |
|---|---:|---:|---:|
| component_count | 12.28888888888889 | 12.222222222222221 | -0.0666666666666682 |
| collision_count | 0.0 | 0.0 | 0.0 |
| attempt_count | 1.0222222222222221 | 1.0888888888888888 | 0.06666666666666665 |
| duration_ms | 69570.37777777777 | 50325.555555555555 | -19244.822222222218 |
| input_tokens | 0.0 | 4338.488888888889 | 4338.488888888889 |
| output_tokens | 0.0 | 4526.422222222222 | 4526.422222222222 |
| total_cost_usd | 0.0 | 0.0 | 0.0 |

## Judge Metric Deltas

| Metric | Baseline Mean | Variant Mean | p-value | Action |
|---|---:|---:|---:|---|
| field_coverage_recall | 4.433333333333334 | 4.544444444444444 | 0.13449078022095573 | rerun-at-n15 |
| field_label_f1 | 4.044444444444444 | 3.966666666666667 | 0.3769433628162794 | rerun-at-n15 |
| validation_intent_accuracy | 3.7666666666666666 | 3.433333333333333 | 0.00016034297103162398 | human-review |
| row_group_agreement | 4.355555555555555 | 4.2555555555555555 | 0.2137404903499549 | rerun-at-n15 |
| locale_fidelity | 3.3444444444444446 | 4.655555555555556 | 1.0768169134145467e-08 | human-review |
| policy_compliance | 3.7888888888888888 | 3.566666666666667 | 0.004692593320904326 | human-review |
| cultural_register | 3.9 | 4.411111111111111 | 9.852232374374381e-08 | human-review |
| cross_locale_leakage | 3.522222222222222 | 4.866666666666666 | 1.338708606524186e-06 | human-review |
| format_pattern_accuracy | 3.3444444444444446 | 4.566666666666666 | 5.440141964685452e-07 | human-review |
| copy_quality_score | 4.122222222222222 | 3.8777777777777778 | 0.00017940575816588478 | human-review |

## Limitations

- Non-blocking deltas are advisory and require PM/SM review.
- Small or statistically inconclusive Category B samples should be rerun at n=15.
