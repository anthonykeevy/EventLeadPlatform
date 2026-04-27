# Story 6.4.4.1-ac10 UAT Results

## Status

Initial baseline generation completed, but the first aggregate judge package lacked generated definitions. The regenerated v2 package is valid, all three judge outputs are consolidated, and AC-10 passed.

## Round Summary

| Round | Trigger | Single Variable | Result | Notes |
|---|---|---|---|---|
| 1 | Initial `rubric_v2` baseline re-judge | None; baseline execution only | Invalid package | Six locale slices completed, but aggregate judge package had `generated_definition_available = 0 / 270`; judge outputs are invalid for AC-10. |
| 2 | 10-row smoke with generated definitions captured | Harness artifact fix: persist `generated_definition` in `metrics.jsonl` | Pass | Smoke run `story-6.4.4.1-ac10-smoke10-with-definitions` produced 10/10 generated definitions in the judge package and 0 unavailable-definition warnings. |
| 3 | Full regenerated baseline with generated definitions captured | Same harness artifact fix, full 270-row run | Pass | Regenerated `story-6.4.4.1-ac10-baseline-v2` produced 270/270 generated definitions in the judge package and 0 unavailable-definition warnings. Claude, Grok, and GPT-5 mini validated and ingested. |

## Cursor Judge Session Completion

| Judge | Output Path | Tonyk Confirmed Saved At |
|---|---|---|
| Claude 4.7 | `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline/judge-package/results/judge-output-claude.json` | Invalidated: package lacked generated definitions |
| Grok 4 | `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline/judge-package/results/judge-output-grok.json` | Invalidated: package lacked generated definitions |
| GPT-5 mini | `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline/judge-package/results/judge-output-gpt5mini.json` | Invalidated: package lacked generated definitions |
| Claude 4.7 | `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-v2/judge-package/results/judge-output-claude.json` | Verified 2026-04-28 08:00 local |
| Grok 4 | `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-v2/judge-package/results/judge-output-grok.json` | Verified 2026-04-28 07:51 local |
| GPT-5 mini | `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-v2/judge-package/results/judge-output-gpt5mini.json` | Verified 2026-04-28 08:24 local |

## RequestID Lineage

No calibration round invoked yet.
