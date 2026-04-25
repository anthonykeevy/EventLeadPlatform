# Form AI Eval Diff Report

## Runs

- Baseline: `story-6.4.2-post-cleanup-baseline`
- Variant: `story-6.4.4-live-h1-locale-one-line`

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
| component_count | 16.0 | 16.0 | 0.0 |
| collision_count | 0.0 | 0.0 | 0.0 |
| attempt_count | 1.2 | 1.1 | -0.09999999999999987 |
| duration_ms | 65881.6 | 68124.8 | 2243.199999999997 |
| input_tokens | 0.0 | 0.0 | 0.0 |
| output_tokens | 0.0 | 0.0 | 0.0 |
| total_cost_usd | 0.0 | 0.0 | 0.0 |

## Judge Metric Deltas

| Metric | Baseline Mean | Variant Mean | p-value | Action |
|---|---:|---:|---:|---|
| field_coverage_recall | 5.0 | 4.95 | 0.3434363961348613 | rerun-at-n15 |
| field_label_f1 | 5.0 | 4.8 | 0.10388813106270511 | rerun-at-n15 |
| validation_intent_accuracy | 4.85 | 4.7 | 0.28077608589617153 | rerun-at-n15 |
| row_group_agreement | 4.7 | 4.6 | 0.44903131271473307 | rerun-at-n15 |
| locale_fidelity | 5.0 | 4.85 | 0.08112618884662182 | rerun-at-n15 |
| copy_quality_score | 4.95 | 4.9 | 0.5565650165670006 | rerun-at-n15 |

## Limitations

- Non-blocking deltas are advisory and require PM/SM review.
- Small or statistically inconclusive Category B samples should be rerun at n=15.
