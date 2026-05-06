# Form AI Eval Diff Report

## Runs

- Baseline: `story-6.4.6-au-baseline-current`
- Variant: `story-6.4.7-au-002-candidate-a`

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
| component_count | 12.28888888888889 | 12.666666666666666 | 0.37777777777777644 |
| collision_count | 0.0 | 0.0 | 0.0 |
| attempt_count | 1.0222222222222221 | 1.0222222222222221 | 0.0 |
| duration_ms | 69570.37777777777 | 38147.177777777775 | -31423.199999999997 |
| input_tokens | 0.0 | 3438.0 | 3438.0 |
| output_tokens | 0.0 | 4044.7555555555555 | 4044.7555555555555 |
| total_cost_usd | 0.0 | 0.0 | 0.0 |

## Judge Metric Deltas

| Metric | Baseline Mean | Variant Mean | p-value | Action |
|---|---:|---:|---:|---|
| field_coverage_recall | 4.433333333333334 | 4.677777777777778 | 0.00013740016092045337 | human-review |
| field_label_f1 | 4.044444444444444 | 3.566666666666667 | 7.586173793938666e-05 | human-review |
| validation_intent_accuracy | 3.7666666666666666 | 3.7222222222222223 | 0.5349515657779276 | rerun-at-n15 |
| row_group_agreement | 4.355555555555555 | 3.8666666666666667 | 4.59522198070772e-10 | human-review |
| locale_fidelity | 3.3444444444444446 | 3.988888888888889 | 0.007548230842383652 | human-review |
| policy_compliance | 3.7888888888888888 | 4.066666666666666 | 0.0014102424065595143 | human-review |
| cultural_register | 3.9 | 3.7222222222222223 | 0.045036230796944854 | human-review |
| cross_locale_leakage | 3.522222222222222 | 3.8555555555555556 | 0.2652071547031203 | rerun-at-n15 |
| format_pattern_accuracy | 3.3444444444444446 | 3.9555555555555557 | 0.025130174973442387 | human-review |
| copy_quality_score | 4.122222222222222 | 3.7222222222222223 | 1.7928363182928564e-07 | human-review |

## Limitations

- Non-blocking deltas are advisory and require PM/SM review.
- Small or statistically inconclusive Category B samples should be rerun at n=15.
