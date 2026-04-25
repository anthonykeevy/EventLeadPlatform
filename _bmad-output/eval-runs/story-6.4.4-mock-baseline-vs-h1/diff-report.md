# Form AI Eval Diff Report

## Runs

- Baseline: `story-6.4.4-mock-baseline`
- Variant: `story-6.4.4-mock-h1-locale-one-line`

## Structural Summary

- Matched rows: 50
- Missing in variant: 0
- Extra in variant: 0

## Blocking Decision

- Blocked: `False`
- Reasons: none

## Advisory Metric Deltas

| Metric | Baseline Mean | Variant Mean | Delta |
|---|---:|---:|---:|
| component_count | 4.0 | 4.0 | 0.0 |
| collision_count | 0.0 | 0.0 | 0.0 |
| attempt_count | 1.0 | 1.0 | 0.0 |
| duration_ms | 0.0 | 0.0 | 0.0 |
| input_tokens | 0.0 | 0.0 | 0.0 |
| output_tokens | 0.0 | 0.0 | 0.0 |
| total_cost_usd | 0.0 | 0.0 | 0.0 |

## Judge Metric Deltas

| Metric | Baseline Mean | Variant Mean | p-value | Action |
|---|---:|---:|---:|---|

## Limitations

- Non-blocking deltas are advisory and require PM/SM review.
- Small or statistically inconclusive Category B samples should be rerun at n=15.
