# Form AI Eval Diff Report

## Runs

- Baseline: `story-6.4.2-post-cleanup-baseline`
- Variant: `story-6.4.4-live-h4-operational-trim`

## Structural Summary

- Matched rows: 10
- Missing in variant: 0
- Extra in variant: 0

## Blocking Decision

- Blocked: `False`
- Reasons: none

## Advisory Metric Deltas

| Metric | Baseline Mean | Variant Mean | Delta |
|---|---:|---:|---:|
| component_count | 16.0 | 14.9 | -1.0999999999999996 |
| collision_count | 0.0 | 0.0 | 0.0 |
| attempt_count | 1.2 | 1.5 | 0.30000000000000004 |
| duration_ms | 65881.6 | 54531.2 | -11350.400000000009 |
| input_tokens | 0.0 | 0.0 | 0.0 |
| output_tokens | 0.0 | 0.0 | 0.0 |
| total_cost_usd | 0.0 | 0.0 | 0.0 |

## Judge Metric Deltas

| Metric | Baseline Mean | Variant Mean | p-value | Action |
|---|---:|---:|---:|---|
| field_coverage_recall | 5.0 | 5.0 | None | rerun-at-n15 |
| field_label_f1 | 5.0 | 5.0 | None | rerun-at-n15 |
| validation_intent_accuracy | 4.85 | 4.8 | 0.7146985496690503 | rerun-at-n15 |
| row_group_agreement | 4.7 | 4.55 | 0.13814824935597148 | rerun-at-n15 |
| locale_fidelity | 5.0 | 5.0 | None | rerun-at-n15 |
| copy_quality_score | 4.95 | 5.0 | 0.3434363961348613 | rerun-at-n15 |

## Limitations

- Non-blocking deltas are advisory and require PM/SM review.
- Small or statistically inconclusive Category B samples should be rerun at n=15.
