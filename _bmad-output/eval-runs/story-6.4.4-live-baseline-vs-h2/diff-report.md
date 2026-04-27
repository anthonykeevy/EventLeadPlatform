# Form AI Eval Diff Report

## Runs

- Baseline: `story-6.4.2-post-cleanup-baseline`
- Variant: `story-6.4.4-live-h2-consent-decision-table`

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
| component_count | 16.0 | 15.2 | -0.8000000000000007 |
| collision_count | 0.0 | 0.0 | 0.0 |
| attempt_count | 1.2 | 1.1 | -0.09999999999999987 |
| duration_ms | 65881.6 | 89252.4 | 23370.79999999999 |
| input_tokens | 0.0 | 0.0 | 0.0 |
| output_tokens | 0.0 | 0.0 | 0.0 |
| total_cost_usd | 0.0 | 0.0 | 0.0 |

## Judge Metric Deltas

| Metric | Baseline Mean | Variant Mean | p-value | Action |
|---|---:|---:|---:|---|
| field_coverage_recall | 5.0 | 4.95 | 0.3434363961348613 | rerun-at-n15 |
| field_label_f1 | 5.0 | 5.0 | None | rerun-at-n15 |
| validation_intent_accuracy | 4.85 | 4.6 | 0.10808851642508543 | rerun-at-n15 |
| row_group_agreement | 4.7 | 4.75 | 0.673322036950413 | rerun-at-n15 |
| locale_fidelity | 5.0 | 5.0 | None | rerun-at-n15 |
| copy_quality_score | 4.95 | 5.0 | 0.3434363961348613 | rerun-at-n15 |

## Limitations

- Non-blocking deltas are advisory and require PM/SM review.
- Small or statistically inconclusive Category B samples should be rerun at n=15.
