# Form AI Eval Diff Report

## Runs

- Baseline: `story-6.4.6-au-baseline-current`
- Variant: `story-6.4.7-au-004-candidate-a`

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
| component_count | 12.28888888888889 | 12.6 | 0.31111111111111 |
| collision_count | 0.0 | 0.0 | 0.0 |
| attempt_count | 1.0222222222222221 | 1.0666666666666667 | 0.04444444444444451 |
| duration_ms | 69570.37777777777 | 49939.77777777778 | -19630.59999999999 |
| input_tokens | 0.0 | 3809.311111111111 | 3809.311111111111 |
| output_tokens | 0.0 | 4408.266666666666 | 4408.266666666666 |
| total_cost_usd | 0.0 | 0.0 | 0.0 |

## Judge Metric Deltas

| Metric | Baseline Mean | Variant Mean | p-value | Action |
|---|---:|---:|---:|---|
| field_coverage_recall | 4.433333333333334 | 4.055555555555555 | 1.0860224641806582e-07 | human-review |
| field_label_f1 | 4.044444444444444 | 4.011111111111111 | 0.7419599689684855 | rerun-at-n15 |
| validation_intent_accuracy | 3.7666666666666666 | 3.577777777777778 | 0.01416982332456651 | human-review |
| row_group_agreement | 4.355555555555555 | 3.9444444444444446 | 4.993586988355503e-09 | human-review |
| locale_fidelity | 3.3444444444444446 | 4.6 | 4.483015769718435e-08 | human-review |
| policy_compliance | 3.7888888888888888 | 3.966666666666667 | 0.03376010711390964 | human-review |
| cultural_register | 3.9 | 3.7666666666666666 | 0.14308909962200145 | rerun-at-n15 |
| cross_locale_leakage | 3.522222222222222 | 4.5 | 0.0004917465920318831 | human-review |
| format_pattern_accuracy | 3.3444444444444446 | 4.477777777777778 | 2.3675800159272953e-06 | human-review |
| copy_quality_score | 4.122222222222222 | 4.044444444444444 | 0.3575145104964149 | rerun-at-n15 |

## Limitations

- Non-blocking deltas are advisory and require PM/SM review.
- Small or statistically inconclusive Category B samples should be rerun at n=15.
