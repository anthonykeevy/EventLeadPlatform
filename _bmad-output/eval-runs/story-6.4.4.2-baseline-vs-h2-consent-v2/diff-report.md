# Form AI Eval Diff Report

## Runs

- Baseline: `story-6.4.4.1-ac10-baseline-v2`
- Variant: `story-6.4.4.2-h2-consent-v2`

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
| component_count | 11.877777777777778 | 11.959259259259259 | 0.0814814814814806 |
| collision_count | 0.0 | 0.0 | 0.0 |
| attempt_count | 1.0407407407407407 | 1.0148148148148148 | -0.025925925925925908 |
| duration_ms | 42376.433333333334 | 57982.95185185185 | 15606.518518518518 |
| input_tokens | 0.0 | 0.0 | 0.0 |
| output_tokens | 0.0 | 0.0 | 0.0 |
| total_cost_usd | 0.0 | 0.0 | 0.0 |

## Judge Metric Deltas

| Metric | Baseline Mean | Variant Mean | p-value | Action |
|---|---:|---:|---:|---|
| field_coverage_recall | 4.409259259259259 | 3.890740740740741 | 0.0 | human-review |
| field_label_f1 | 4.985185185185185 | 3.685185185185185 | 0.0 | human-review |
| validation_intent_accuracy | 4.409259259259259 | 4.212962962962963 | 0.0 | human-review |
| row_group_agreement | 4.801851851851852 | 3.6481481481481484 | 0.0 | human-review |
| locale_fidelity | 3.7888888888888888 | 4.103703703703704 | 5.1006934335684484e-05 | human-review |
| policy_compliance | 3.9518518518518517 | 4.04074074074074 | 0.018861935554921883 | human-review |
| cultural_register | 4.088888888888889 | 4.225925925925926 | 4.886889225508284e-07 | human-review |
| cross_locale_leakage | 3.935185185185185 | 4.307407407407408 | 0.0008259171600523141 | human-review |
| format_pattern_accuracy | 3.9092592592592594 | 3.4 | 3.302926820936136e-10 | human-review |
| copy_quality_score | 4.357407407407408 | 3.588888888888889 | 0.0 | human-review |

## Limitations

- Non-blocking deltas are advisory and require PM/SM review.
- Small or statistically inconclusive Category B samples should be rerun at n=15.
