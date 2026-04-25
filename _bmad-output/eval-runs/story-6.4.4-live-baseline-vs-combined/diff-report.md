# Form AI Eval Diff Report

## Runs

- Baseline: `story-6.4.2-post-cleanup-baseline`
- Variant: `story-6.4.4-live-h1-h2-h4-combined`

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
| component_count | 16.0 | 15.0 | -1.0 |
| collision_count | 0.0 | 0.0 | 0.0 |
| attempt_count | 1.2 | 1.2 | 0.0 |
| duration_ms | 65881.6 | 45426.5 | -20455.100000000006 |
| input_tokens | 0.0 | 0.0 | 0.0 |
| output_tokens | 0.0 | 0.0 | 0.0 |
| total_cost_usd | 0.0 | 0.0 | 0.0 |

## Judge Metric Deltas

| Metric | Baseline Mean | Variant Mean | p-value | Action |
|---|---:|---:|---:|---|
| field_coverage_recall | 5.0 | 4.95 | 0.3434363961348613 | rerun-at-n15 |
| field_label_f1 | 5.0 | 4.95 | 0.3434363961348613 | rerun-at-n15 |
| validation_intent_accuracy | 4.85 | 4.8 | 0.7146985496690503 | rerun-at-n15 |
| row_group_agreement | 4.7 | 4.65 | 0.6600791471797829 | rerun-at-n15 |
| locale_fidelity | 5.0 | 4.6 | 0.00020249932207194732 | human-review |
| copy_quality_score | 4.95 | 5.0 | 0.3434363961348613 | rerun-at-n15 |

## Limitations

- Non-blocking deltas are advisory and require PM/SM review.
- Small or statistically inconclusive Category B samples should be rerun at n=15.
