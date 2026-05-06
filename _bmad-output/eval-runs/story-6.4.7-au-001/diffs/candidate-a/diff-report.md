# Form AI Eval Diff Report

## Runs

- Baseline: `story-6.4.6-au-baseline-current`
- Variant: `story-6.4.7-au-001-candidate-a`

## Structural Summary

- Matched rows: 45
- Missing in variant: 0
- Extra in variant: 0

## Blocking Decision

- Blocked: `True`
- Reasons: schema_valid_regression

## Advisory Metric Deltas

| Metric | Baseline Mean | Variant Mean | Delta |
|---|---:|---:|---:|
| component_count | 12.28888888888889 | 11.977777777777778 | -0.3111111111111118 |
| collision_count | 0.0 | 0.0 | 0.0 |
| attempt_count | 1.0222222222222221 | 1.0222222222222221 | 0.0 |
| duration_ms | 69570.37777777777 | 39178.08888888889 | -30392.288888888885 |
| input_tokens | 0.0 | 3306.866666666667 | 3306.866666666667 |
| output_tokens | 0.0 | 4157.288888888889 | 4157.288888888889 |
| total_cost_usd | 0.0 | 0.0 | 0.0 |

## Judge Metric Deltas

| Metric | Baseline Mean | Variant Mean | p-value | Action |
|---|---:|---:|---:|---|
| field_coverage_recall | 4.433333333333334 | 4.066666666666666 | 7.196479645532605e-08 | human-review |
| field_label_f1 | 4.044444444444444 | 4.0777777777777775 | 0.715248642374555 | rerun-at-n15 |
| validation_intent_accuracy | 3.7666666666666666 | 3.488888888888889 | 7.434475328804702e-06 | human-review |
| row_group_agreement | 4.355555555555555 | 4.477777777777778 | 0.034777189995228164 | human-review |
| locale_fidelity | 3.3444444444444446 | 4.677777777777778 | 7.137712310090194e-09 | human-review |
| policy_compliance | 3.7888888888888888 | 4.588888888888889 | 0.0 | human-review |
| cultural_register | 3.9 | 3.911111111111111 | 0.8985663907262627 | rerun-at-n15 |
| cross_locale_leakage | 3.522222222222222 | 4.711111111111111 | 1.4132679081346744e-05 | human-review |
| format_pattern_accuracy | 3.3444444444444446 | 4.688888888888889 | 6.093773130544378e-08 | human-review |
| copy_quality_score | 4.122222222222222 | 3.9555555555555557 | 0.003615436237180414 | human-review |

## Limitations

- Non-blocking deltas are advisory and require PM/SM review.
- Small or statistically inconclusive Category B samples should be rerun at n=15.
