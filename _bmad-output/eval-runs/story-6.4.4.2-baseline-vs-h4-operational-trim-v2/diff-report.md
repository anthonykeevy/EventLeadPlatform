# Form AI Eval Diff Report

## Runs

- Baseline: `story-6.4.4.1-ac10-baseline-v2`
- Variant: `story-6.4.4.2-h4-operational-trim-v2`

## Structural Summary

- Matched rows: 270
- Missing in variant: 0
- Extra in variant: 0

## Blocking Decision

- Blocked: `False`
- Reasons: none

## Advisory Metric Deltas

| Metric | Baseline Mean | Variant Mean | Delta |
|---|---:|---:|---:|
| component_count | 11.877777777777778 | 11.977777777777778 | 0.09999999999999964 |
| collision_count | 0.0 | 0.0 | 0.0 |
| attempt_count | 1.0407407407407407 | 1.048148148148148 | 0.007407407407407307 |
| duration_ms | 42376.433333333334 | 35508.83703703704 | -6867.596296296295 |
| input_tokens | 0.0 | 0.0 | 0.0 |
| output_tokens | 0.0 | 0.0 | 0.0 |
| total_cost_usd | 0.0 | 0.0 | 0.0 |

## Judge Metric Deltas

| Metric | Baseline Mean | Variant Mean | p-value | Action |
|---|---:|---:|---:|---|
| field_coverage_recall | 4.409259259259259 | 4.351851851851852 | 0.007841262651682168 | human-review |
| field_label_f1 | 4.985185185185185 | 3.762962962962963 | 0.0 | human-review |
| validation_intent_accuracy | 4.409259259259259 | 3.912962962962963 | 0.0 | human-review |
| row_group_agreement | 4.801851851851852 | 4.32037037037037 | 2.1049828546892968e-13 | human-review |
| locale_fidelity | 3.7888888888888888 | 4.05 | 0.0009140681187326249 | human-review |
| policy_compliance | 3.9518518518518517 | 4.385185185185185 | 3.049782648645305e-13 | human-review |
| cultural_register | 4.088888888888889 | 3.725925925925926 | 8.570921750106208e-14 | human-review |
| cross_locale_leakage | 3.935185185185185 | 3.9444444444444446 | 0.9324350519101304 | rerun-at-n15 |
| format_pattern_accuracy | 3.9092592592592594 | 3.640740740740741 | 0.0006201954855824532 | human-review |
| copy_quality_score | 4.357407407407408 | 4.357407407407408 | 1.0 | rerun-at-n15 |

## Limitations

- Non-blocking deltas are advisory and require PM/SM review.
- Small or statistically inconclusive Category B samples should be rerun at n=15.
