# Form AI Eval Diff Report

## Runs

- Baseline: `story-6.4.6-au-baseline-current`
- Variant: `story-6.4.7-au-003-candidate-a`

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
| component_count | 12.28888888888889 | 12.488888888888889 | 0.1999999999999993 |
| collision_count | 0.0 | 0.0 | 0.0 |
| attempt_count | 1.0222222222222221 | 1.0444444444444445 | 0.022222222222222365 |
| duration_ms | 69570.37777777777 | 53919.97777777778 | -15650.399999999994 |
| input_tokens | 0.0 | 3706.4 | 3706.4 |
| output_tokens | 0.0 | 4382.444444444444 | 4382.444444444444 |
| total_cost_usd | 0.0 | 0.0 | 0.0 |

## Judge Metric Deltas

| Metric | Baseline Mean | Variant Mean | p-value | Action |
|---|---:|---:|---:|---|
| field_coverage_recall | 4.433333333333334 | 4.466666666666667 | 0.655837434811094 | rerun-at-n15 |
| field_label_f1 | 4.044444444444444 | 4.0 | 0.5982596859625049 | rerun-at-n15 |
| validation_intent_accuracy | 3.7666666666666666 | 3.9444444444444446 | 0.006325339905666194 | human-review |
| row_group_agreement | 4.355555555555555 | 4.011111111111111 | 1.685130559536674e-07 | human-review |
| locale_fidelity | 3.3444444444444446 | 4.9 | 1.0666745264842348e-10 | human-review |
| policy_compliance | 3.7888888888888888 | 4.444444444444445 | 5.821565451924471e-12 | human-review |
| cultural_register | 3.9 | 3.977777777777778 | 0.3074881297657509 | rerun-at-n15 |
| cross_locale_leakage | 3.522222222222222 | 4.888888888888889 | 1.0221982140734553e-06 | human-review |
| format_pattern_accuracy | 3.3444444444444446 | 4.888888888888889 | 1.8664031431470107e-09 | human-review |
| copy_quality_score | 4.122222222222222 | 3.922222222222222 | 0.0012744743316753793 | human-review |

## Limitations

- Non-blocking deltas are advisory and require PM/SM review.
- Small or statistically inconclusive Category B samples should be rerun at n=15.
