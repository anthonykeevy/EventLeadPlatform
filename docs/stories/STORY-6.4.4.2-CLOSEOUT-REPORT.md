# Story 6.4.4.2 Closeout Report

## Summary

H2 and H4 were re-evaluated under the AC10 `prompts-v1.1` / `rubric_v2` baseline as separate single-variable ablations. Both variants completed structural generation, judge review, ingest, and diff/stat comparison.

Neither candidate clears the ship bar. Both have no structural blockers, but both show material semantic regressions across multiple Category B metrics. The closeout is measured/no-change: do not ship H2-only or H4-only, and keep current `master` runtime behavior unchanged for now.

## Final Prompt State

| Candidate | Verdict | Final state |
|---|---|---|
| H2 consent/legal decision table | No-change | Do not ship H2-only |
| H4 operational-notes trim | No-change | Do not ship H4-only |
| Accepted H2+H4 subset | N/A | Not run because neither individual candidate passed |

## Evidence

See:

- `STORY-6.4.4.2-HYPOTHESIS-EVIDENCE.md`
- `STORY-6.4.4.2-GATE-EVIDENCE.md`
- `STORY-6.4.4.2-UAT-RESULTS.md`

Green gate: focused eval/judge tests passed (`31 passed`) and backend regression passed (`805 passed, 26 skipped`). Frontend checks were not applicable because no frontend files changed. Stale-field audit passed with PR #79 open against `master` and no unintended stale status placeholders remaining.

## Carry-Forward Backlog

- No H2/H4 accepted-subset run required.
- No prompt-shrink winner from this ablation study.
- Current `master` prompt behavior remains unchanged for now.
- Keep Story 6.4.5 as the next prompt-shrink candidate story.
- If PM/SM want to revisit H2/H4 later, treat it as a new prompt design rather than shipping these candidates.

## Recommended Next Story

Story 6.4.5 — Component Property Cheat Sheet H3.

