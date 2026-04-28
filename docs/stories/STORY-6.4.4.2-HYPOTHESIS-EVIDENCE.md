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
| Claude mean | 4.2607 |
| Grok mean | 4.2667 |
| GPT-5 mini mean | 4.2978 |

## Prompt Size Deltas

| Candidate | Before chars | After chars | Delta | Notes |
|---|---:|---:|---:|---|
| H2 consent/legal decision table | 1960 | 748 | -1212 | Re-run as `prompt_shrink_mode=h2`: compact consent table enabled; H4 operational trim disabled. |
| H4 operational-notes trim | 6595 | 6355 | -240 | Re-run as `prompt_shrink_mode=h4`: operational-notes trim enabled; compact H2 consent table disabled. |
| Accepted H2+H4 subset | N/A | N/A | N/A | Not run because neither individual candidate passed. |

## Variant Evidence

| Candidate | Run id | Judge package | Judge ingest | Diff/stat output | Verdict |
|---|---|---|---|---|---|
| H2 | `story-6.4.4.2-h2-consent-v2` | `_bmad-output/eval-runs/story-6.4.4.2-h2-consent-v2/judge-package/` | `_bmad-output/eval-runs/story-6.4.4.2-h2-consent-v2/judge-package/judge-ingest-summary.json` | `_bmad-output/eval-runs/story-6.4.4.2-baseline-vs-h2-consent-v2/` | Revert / no-change: material Category B regressions |
| H4 | `story-6.4.4.2-h4-operational-trim-v2` | `_bmad-output/eval-runs/story-6.4.4.2-h4-operational-trim-v2/judge-package/` | `_bmad-output/eval-runs/story-6.4.4.2-h4-operational-trim-v2/judge-package/judge-ingest-summary.json` | `_bmad-output/eval-runs/story-6.4.4.2-baseline-vs-h4-operational-trim-v2/` | Revert / no-change: material Category B regressions |
| H2+H4 accepted subset | `story-6.4.4.2-h2-h4-accepted-v2` | N/A | N/A | N/A | Not run: neither individual candidate cleared the evidence bar |

## H2 Judge Prompt Paths

- Claude: `_bmad-output/eval-runs/story-6.4.4.2-h2-consent-v2/judge-package/judge-prompt-claude.md`
- Grok: `_bmad-output/eval-runs/story-6.4.4.2-h2-consent-v2/judge-package/judge-prompt-grok.md`
- GPT-5 mini: `_bmad-output/eval-runs/story-6.4.4.2-h2-consent-v2/judge-package/judge-prompt-gpt5mini.md`

H2 package verification:

- Locale slices completed: AU, NZ, UK, US, INTL_ONLINE, EU.
- Total generated rows: 270.
- Judge package row count: 270.
- Generated definitions: 270/270 from `metrics.jsonl`.
- Prompt scope: Story 6.4.4.2 H2 consent/legal `rubric_v2` re-evaluation.

## H4 Judge Prompt Paths

- Claude: `_bmad-output/eval-runs/story-6.4.4.2-h4-operational-trim-v2/judge-package/judge-prompt-claude.md`
- Grok: `_bmad-output/eval-runs/story-6.4.4.2-h4-operational-trim-v2/judge-package/judge-prompt-grok.md`
- GPT-5 mini: `_bmad-output/eval-runs/story-6.4.4.2-h4-operational-trim-v2/judge-package/judge-prompt-gpt5mini.md`

H4 package verification:

- Locale slices completed: AU, NZ, UK, US, INTL_ONLINE, EU.
- Total generated rows: 270.
- Judge package row count: 270.
- Generated definitions: 270/270 from `metrics.jsonl`.
- Prompt scope: Story 6.4.4.2 H4 operational-notes `rubric_v2` re-evaluation.

## Diff / Statistics Summary

H2 diff output: `_bmad-output/eval-runs/story-6.4.4.2-baseline-vs-h2-consent-v2/`.

- Structural blockers: none.
- Matched rows: 270/270.
- Material regressions: `field_coverage_recall`, `field_label_f1`, `validation_intent_accuracy`, `row_group_agreement`, `format_pattern_accuracy`, `copy_quality_score`.
- Wins/advisory improvements: `locale_fidelity`, `cultural_register`, `cross_locale_leakage`, `policy_compliance`.
- Advisory runtime delta: mean duration increased from 42.4s to 58.0s.

H4 diff output: `_bmad-output/eval-runs/story-6.4.4.2-baseline-vs-h4-operational-trim-v2/`.

- Structural blockers: none.
- Matched rows: 270/270.
- Material regressions: `field_coverage_recall`, `field_label_f1`, `validation_intent_accuracy`, `row_group_agreement`, `cultural_register`, `format_pattern_accuracy`.
- Wins/advisory improvements: `policy_compliance`, `locale_fidelity`.
- Inconclusive semantic metrics: `copy_quality_score`, `cross_locale_leakage`.
- Advisory runtime delta: mean duration decreased from 42.4s to 35.5s.

## Decision Notes

- H1 is excluded from this story because the Story 6.4.4 combined run showed significant locale-fidelity regression and H1 was the locale-specific shrink.
- Combined H1+H2+H4 is excluded.
- A measured/no-change result is acceptable if H2/H4 do not clear the evidence bar.

## Final Verdict

Both candidates fail the ship bar under `rubric_v2`.

- H2: no structural blockers, but material semantic regressions across multiple Category B metrics. Do not ship H2-only.
- H4: no structural blockers, but material semantic regressions across multiple Category B metrics. Do not ship H4-only.
- H2+H4 accepted-subset check: not run, because neither individual candidate passed.
- Current `master` runtime behavior remains unchanged for now.

Recommended closeout: measured/no-change; move to Story 6.4.5 after final gate and closeout housekeeping.

