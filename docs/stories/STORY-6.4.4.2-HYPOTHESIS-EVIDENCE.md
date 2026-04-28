# Story 6.4.4.2 Hypothesis Evidence

## Summary

This file records the `rubric_v2` re-evaluation of the two plausible prompt-shrink candidates carried forward from Story 6.4.4:

- H2 — consent/legal decision table.
- H4 — operational-notes trim.

Control baseline: `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-v2/`.

## Baseline Control

| Field | Value |
|---|---|
| Run id | `story-6.4.4.1-ac10-baseline-v2` |
| Benchmark | `prompts-v1.1` |
| Rubric | `rubric_v2` |
| Rows | 270 |
| Generated definitions | 270/270 |
| Judge ingest summary | `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-v2/judge-package/judge-ingest-summary.json` |
| Claude mean | TBD |
| Grok mean | TBD |
| GPT-5 mini mean | TBD |

## Prompt Size Deltas

| Candidate | Before chars | After chars | Delta | Notes |
|---|---:|---:|---:|---|
| H2 consent/legal decision table | TBD | TBD | TBD | From Story 6.4.4 candidate. |
| H4 operational-notes trim | TBD | TBD | TBD | From Story 6.4.4 candidate. |
| Accepted H2+H4 subset | TBD | TBD | TBD | Only if both individual candidates pass. |

## Variant Evidence

| Candidate | Run id | Judge package | Judge ingest | Diff/stat output | Verdict |
|---|---|---|---|---|---|
| H2 | `story-6.4.4.2-h2-consent-v2` | TBD | TBD | TBD | TBD |
| H4 | `story-6.4.4.2-h4-operational-trim-v2` | TBD | TBD | TBD | TBD |
| H2+H4 accepted subset | `story-6.4.4.2-h2-h4-accepted-v2` | TBD | TBD | TBD | TBD / N/A |

## Decision Notes

- H1 is excluded from this story because the Story 6.4.4 combined run showed significant locale-fidelity regression and H1 was the locale-specific shrink.
- Combined H1+H2+H4 is excluded.
- A measured/no-change result is acceptable if H2/H4 do not clear the evidence bar.

## Final Verdict

TBD.

