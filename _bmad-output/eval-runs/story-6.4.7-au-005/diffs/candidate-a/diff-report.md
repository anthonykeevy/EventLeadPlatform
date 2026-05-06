# Form AI Eval Diff Report

## Runs

- Baseline: `story-6.4.6-au-baseline-current`
- Variant: `story-6.4.7-au-005-candidate-a`

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
| component_count | 12.28888888888889 | 12.777777777777779 | 0.48888888888888893 |
| collision_count | 0.0 | 0.0 | 0.0 |
| attempt_count | 1.0222222222222221 | 1.0444444444444445 | 0.022222222222222365 |
| duration_ms | 69570.37777777777 | 52246.77777777778 | -17323.59999999999 |
| input_tokens | 0.0 | 3887.8 | 3887.8 |
| output_tokens | 0.0 | 4538.333333333333 | 4538.333333333333 |
| total_cost_usd | 0.0 | 0.0 | 0.0 |

## Judge Metric Deltas

| Metric | Baseline Mean | Variant Mean | p-value | Action |
|---|---:|---:|---:|---|
| field_coverage_recall | 4.433333333333334 | 4.833333333333333 | 2.096400908424556e-08 | human-review |
| field_label_f1 | 4.044444444444444 | 3.911111111111111 | 0.166796531867201 | rerun-at-n15 |
| validation_intent_accuracy | 3.7666666666666666 | 4.2444444444444445 | 4.273226550388642e-09 | human-review |
| row_group_agreement | 4.355555555555555 | 4.533333333333333 | 0.012096297338526685 | human-review |
| locale_fidelity | 3.3444444444444446 | 4.733333333333333 | 4.1825468644063335e-09 | human-review |
| policy_compliance | 3.7888888888888888 | 4.388888888888889 | 1.4522573810182848e-08 | human-review |
| cultural_register | 3.9 | 4.3 | 3.4230961746595234e-05 | human-review |
| cross_locale_leakage | 3.522222222222222 | 4.7444444444444445 | 1.2931265093496513e-05 | human-review |
| format_pattern_accuracy | 3.3444444444444446 | 4.677777777777778 | 1.131147762123419e-07 | human-review |
| copy_quality_score | 4.122222222222222 | 4.344444444444444 | 0.005380364616249689 | human-review |

## Limitations

- Non-blocking deltas are advisory and require PM/SM review.
- Small or statistically inconclusive Category B samples should be rerun at n=15.
