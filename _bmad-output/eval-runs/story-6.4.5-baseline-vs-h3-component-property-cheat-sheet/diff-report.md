# Form AI Eval Diff Report

## Runs

- Baseline: `story-6.4.4.1-ac10-baseline-v2`
- Variant: `story-6.4.5-h3-component-property-cheat-sheet`

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
| component_count | 11.877777777777778 | 11.84074074074074 | -0.03703703703703809 |
| collision_count | 0.0 | 0.0 | 0.0 |
| attempt_count | 1.0407407407407407 | 1.0148148148148148 | -0.025925925925925908 |
| duration_ms | 42376.433333333334 | 43128.95925925926 | 752.5259259259255 |
| input_tokens | 0.0 | 0.0 | 0.0 |
| output_tokens | 0.0 | 0.0 | 0.0 |
| total_cost_usd | 0.0 | 0.0 | 0.0 |

## Judge Metric Deltas

| Metric | Baseline Mean | Variant Mean | p-value | Action |
|---|---:|---:|---:|---|
| field_coverage_recall | 4.409259259259259 | 4.857407407407408 | 0.0 | human-review |
| field_label_f1 | 4.985185185185185 | 4.061111111111111 | 1.326716514427062e-13 | human-review |
| validation_intent_accuracy | 4.409259259259259 | 4.027777777777778 | 2.6434410216324977e-13 | human-review |
| row_group_agreement | 4.801851851851852 | 4.657407407407407 | 1.9121149108514146e-11 | human-review |
| locale_fidelity | 3.7888888888888888 | 4.225925925925926 | 2.0921279741958898e-07 | human-review |
| policy_compliance | 3.9518518518518517 | 4.516666666666667 | 0.0 | human-review |
| cultural_register | 4.088888888888889 | 4.372222222222222 | 5.940803404769213e-13 | human-review |
| cross_locale_leakage | 3.935185185185185 | 4.155555555555556 | 0.05454147208582816 | rerun-at-n15 |
| format_pattern_accuracy | 3.9092592592592594 | 4.2518518518518515 | 2.6929675578934997e-05 | human-review |
| copy_quality_score | 4.357407407407408 | 4.442592592592592 | 0.005668280812225479 | human-review |

## Limitations

- Non-blocking deltas are advisory and require PM/SM review.
- Small or statistically inconclusive Category B samples should be rerun at n=15.
