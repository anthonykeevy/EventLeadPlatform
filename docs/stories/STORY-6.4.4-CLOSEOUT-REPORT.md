# Story 6.4.4 Closeout Report

**Story:** 6.4.4 - Prompt Shrink Sweeps H1/H2/H4  
**Branch:** `story/epic6-6.4.4-prompt-shrink-sweeps`  
**PR:** [#72](https://github.com/anthonykeevy/EventLeadPlatform/pull/72)  
**Closeout disposition:** Evidence complete; PM/SM ship decision required before merge.

## 1) Summary

Story 6.4.4 implemented and measured the prompt-shrink candidates:

- H1: AU/NZ locale guidance reduced to one line.
- H2: consent/legal guidance reduced to a compact decision table.
- H4: prompt assembly trims non-generation `## Operational Notes`.
- Combined: H1+H2+H4 together.

The story is closed from a development/evidence perspective. It is not cleanly merge-ready as a shipped prompt change because the live judge evidence found a statistically significant locale regression in the combined variant, and each individual variant remained inconclusive at the current n=10 sample size.

## 2) Findings

| Hypothesis | Final evidence finding | Recommendation |
|---|---|---|
| H1 | No structural blockers. Category B inconclusive; `locale_fidelity` dropped from 5.0 to 4.85 (`p=0.0811`). | Treat as suspect; rerun at n=15 or revert before shipping. |
| H2 | No structural blockers. Category B inconclusive; no significant semantic regression. | Candidate for PM/SM acceptance or n=15 rerun. |
| H4 | No structural blockers. Category B inconclusive; strongest semantic stability of the individual variants. | Candidate for PM/SM acceptance or n=15 rerun. |
| Combined | No structural blockers, but `locale_fidelity` regressed from 5.0 to 4.6 (`p=0.000202`, effect size 2.68). | Do not ship combined as-is. |

## 3) Acceptance Criteria

| AC | Status | Evidence |
|---|---|---|
| AC-1 H1 variant implemented and measured | Complete | `STORY-6.4.4-HYPOTHESIS-EVIDENCE.md` |
| AC-2 H2 variant implemented and measured | Complete | `STORY-6.4.4-HYPOTHESIS-EVIDENCE.md` |
| AC-3 H4 variant implemented and measured | Complete | `STORY-6.4.4-HYPOTHESIS-EVIDENCE.md` |
| AC-4 Combined variant measured | Complete | `STORY-6.4.4-HYPOTHESIS-EVIDENCE.md` |
| AC-5 Structural gates pass for shipped changes | Complete for measured candidates | live diff reports |
| AC-6 Semantic evidence recorded | Complete | 15 judge outputs ingested and diffed |
| AC-7 Statistical outputs recorded | Complete | live diff summaries |
| AC-8 Revert losers | PM/SM decision pending | combined should not ship as-is; individual variants need accept/rerun/revert decision |
| AC-9 Prompt size delta documented | Complete | `STORY-6.4.4-HYPOTHESIS-EVIDENCE.md` |
| AC-10 Hypothesis evidence complete | Complete | `STORY-6.4.4-HYPOTHESIS-EVIDENCE.md` |
| AC-11 No unrelated capability work | Complete | no H3/H5/H6/Image-to-Form changes |
| AC-12 Closeout complete | Complete | this report |

## 4) Test Gates

| Gate | Result |
|---|---|
| Preflight | Attempted; script missing in worktree. Recorded in `STORY-6.4.4-PREFLIGHT.md`. |
| Focused prompt/eval tests | 31 passed. |
| Backend regression | 784 passed, 26 skipped. |
| Eval harness runs | Mock and live baseline/H1/H2/H4/combined completed. |
| Judge ingest | Baseline plus H1/H2/H4/combined each ingested from 3 judges. |
| Diff/stat reports | Live diff reports generated for all variants. |
| Lints | No IDE lint errors in touched files after implementation pass. |

## 5) Evidence Artifacts

| Artifact | Path |
|---|---|
| Hypothesis evidence | `docs/stories/STORY-6.4.4-HYPOTHESIS-EVIDENCE.md` |
| Gate evidence | `docs/stories/STORY-6.4.4-GATE-EVIDENCE.md` |
| Judge prompts | `docs/stories/STORY-6.4.4-JUDGE-PROMPTS.md` |
| H1 live diff | `_bmad-output/eval-runs/story-6.4.4-live-baseline-vs-h1/` |
| H2 live diff | `_bmad-output/eval-runs/story-6.4.4-live-baseline-vs-h2/` |
| H4 live diff | `_bmad-output/eval-runs/story-6.4.4-live-baseline-vs-h4/` |
| Combined live diff | `_bmad-output/eval-runs/story-6.4.4-live-baseline-vs-combined/` |

The source live run folders and judge packages were generated under `_bmad-output/eval-runs/` in the active evaluation workspace.

## 6) Architecture Notes

The implementation is intentionally narrow:

- prompt constants changed only in `backend/modules/form_ai/service.py`,
- prompt assembly trims context-pack operational notes without mutating the source context pack,
- eval harness parsing now accepts Story 6.4.4 candidate labels,
- tests cover the new prompt contracts and harness variant parsing,
- no benchmark prompt or rubric changes were made,
- no database migrations or schema changes were made.

## 7) Carry-Forward

| Item | Owner | Reason |
|---|---|---|
| Decide final ship/revert subset | PM/SM + Anthony | Combined is a clear no-ship; individual variants are inconclusive. |
| Rerun selected candidates at n=15 | Dev/QA if requested | Diff tool recommends `rerun-at-n15` for inconclusive Category B metrics. |
| Consider H2/H4-only combined run | PM/SM decision | Combined failure appears locale-specific, so an H2+H4 run may isolate safer shrink value. |
| Update PR before final merge | Dev | Revert unaccepted prompt changes or document explicit PM/SM acceptance. |

## 8) Closeout Decision

Development and evidence gathering are complete. The current PR should remain unmerged until PM/SM chooses the final ship strategy. The conservative merge-ready path is to revert H1 and the combined state, then either accept only explicitly approved H2/H4 changes or carry all prompt shrinks forward for a larger n=15 evaluation.
