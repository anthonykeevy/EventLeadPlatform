# Form AI Eval Diff Report

## Runs

- Baseline: `story-6.4.3c-sample-baseline`
- Variant: `story-6.4.3c-sample-variant`

## Structural Summary

- Matched rows: 3
- Missing in variant: 0
- Extra in variant: 0

## Blocking Decision

- Blocked: `False`
- Reasons: none

## Advisory Metric Deltas

| Metric | Baseline Mean | Variant Mean | Delta |
|---|---:|---:|---:|
| component_count | 5.0 | 5.333333333333333 | 0.33333333333333304 |
| collision_count | 0.0 | 0.0 | 0.0 |
| attempt_count | 1.0 | 1.0 | 0.0 |
| duration_ms | 120.0 | 130.0 | 10.0 |
| input_tokens | 11.0 | 10.0 | -1.0 |
| output_tokens | 21.0 | 19.0 | -2.0 |
| total_cost_usd | 0.01 | 0.009 | -0.0010000000000000009 |

## Judge Metric Deltas

| Metric | Baseline Mean | Variant Mean | p-value | Action |
|---|---:|---:|---:|---|
| field_coverage_recall | 4.0 | 4.0 | 1.0 | rerun-at-n15 |
| field_label_f1 | 4.0 | 4.0 | 1.0 | rerun-at-n15 |
| validation_intent_accuracy | 4.0 | 4.0 | 1.0 | rerun-at-n15 |
| row_group_agreement | 4.0 | 4.0 | 1.0 | rerun-at-n15 |
| locale_fidelity | 4.0 | 4.0 | 1.0 | rerun-at-n15 |
| copy_quality_score | 4.0 | 4.0 | 1.0 | rerun-at-n15 |

## Limitations

- Non-blocking deltas are advisory and require PM/SM review.
- Small or statistically inconclusive Category B samples should be rerun at n=15.
