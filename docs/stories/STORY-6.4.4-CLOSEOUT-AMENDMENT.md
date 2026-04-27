# Story 6.4.4 — Closeout Amendment

**Document type:** Closeout amendment (supersedes the "PM/SM ship decision" section of `STORY-6.4.4-CLOSEOUT-REPORT.md` only)
**SM:** Bob
**PM:** John
**Decision-maker:** Tonyk (final disposition)
**Date:** 2026-04-27
**Branch:** `docs/epic6-story-6.4.4-closeout-amendment` (this PR)
**Story branch under review:** `story/epic6-6.4.4-prompt-shrink-sweeps` ([PR #72](https://github.com/anthonykeevy/EventLeadPlatform/pull/72) — Draft)
**Successor story:** [Story 6.4.4.1](./story-6.4.4.1.md) — Locale Architecture: Wire the Registry (drafted concurrently with this amendment)

---

## 1. Why this amendment exists

`STORY-6.4.4-CLOSEOUT-REPORT.md` left PR #72 with a "PM/SM ship decision required before merge" hold because:

- The combined H1+H2+H4 variant produced a statistically significant `locale_fidelity` regression (`p=0.000202`, effect size 2.68) under the rubric_v1 judge architecture.
- The individual H1 / H2 / H4 variants were Category-B inconclusive at `n=10`.
- The original closeout proposed three options: (1) ship measured winners only, (2) rerun at `n=15`, (3) revert prompt changes and mark as measured-only learning.

PM/Tonyk review surfaced three findings that change the basis for this decision and remove the value of any of the three original options taken at face value. Those findings are documented in the [Story 6.4.4.1 SM Handoff Brief](../../_bmad-output/planning-artifacts/STORY-6.4.4.1-SM-HANDOFF-BRIEF.md) and the four [locale-strategy research memos](../../_bmad-output/research/locale-strategy/). Summarised:

1. **The judging method is structurally broken at the rubric_v1 level.** Across 5 runs × 60 cells per judge × 3 judges = 900 cells, **Gemini 2.5 Flash and GPT-5 mini both gave 60/60 perfect 5/5 scores in every variant**. Claude was the only judge that moved. The Claude+Gemini "primary mean" is therefore Gemini-flatline-dominated; every Claude-detected regression is exactly halved by averaging with Gemini's constant 5.0. "Rerun-at-n=15" cannot fix this — Gemini's variance is structurally zero.
2. **The `locale_fidelity` metric has no ground truth in `prompts-v1.0`.** No benchmark prompt specifies a target locale; the judge package contains no locale anchor. Claude inferred AU strictness from output context clues (`+61`, "organisation") and applied its own model-internal AU-pedantry. Tonyk's lived AU experience confirmed several of Claude's locale downscores were false positives ("First name / Last name" is fine in AU; mandatory `+61` prefix on a domestic AU form is over-specification, not a locale fidelity bonus).
3. **The product needs an internationalisation architecture, not just a bigger AU block.** The combined regression evidence will be made obsolete by Story 6.4.4.1, which deletes `_LOCALE_PROMPT_BLOCKS["AU"]` entirely and replaces it with a registry-rendered locale block per `audienceLocale`.

Under those three findings, **none of the three original disposition options is well-supported.** This amendment overrides the original closeout's "PM/SM decide later" hold with an explicit accept-with-caveats disposition.

---

## 2. Disposition (overrides the original closeout's hold)

**Disposition: Accept-with-caveats. PR #72 merges to `master` as-is**, plus the audit-trail and ADR-footer additions in §3 below. No code reverts.

| What | Why |
|---|---|
| **Accept H1 (AU/NZ shrink to one line) — keep merged.** | H1's master state is moot: Story 6.4.4.1 deletes `_LOCALE_PROMPT_BLOCKS` entirely and renders the locale block from `config.PromptTemplateLocaleBlock` joined to `ref.Country`. Whether master holds the long block or the short block when 6.4.4.1 starts is irrelevant to the eventual outcome. |
| **Accept H2 (consent decision-table) — keep merged.** | Orthogonal to the locale architecture. The new format/policy/tone sub-block split in 6.4.4.1 puts per-locale consent text inside the policy sub-block per country; H2's compact decision table operates at the global system-prompt level (component selection guidance). They coexist. The v1 evidence was Category-B inconclusive — neither a proven win nor a proven regression. |
| **Accept H4 (operational-trim) — keep merged.** | Fully orthogonal. Trims duplicated context-pack guidance already covered by the active prompt contract. Strongest semantic stability of the three individual variants under v1 judging; no architecture conflict. |
| **Accept the combined p=0.000202 locale regression as a reliability artefact, not a blocker.** | (a) The v1 rubric had no locale ground truth (finding 2); (b) Gemini-flatline-dominated mean structurally distorts the effect size (finding 1); (c) the H1 code that produced the regression is being deleted in 6.4.4.1 (finding 3). Re-evaluating the combined state under rubric_v2 is meaningless because the code state will not exist after 6.4.4.1 ships. |
| **Mark as measured-only-learning at the rubric_v1 level.** | The harness/test/judge-prompt scaffolding from 6.4.4 is real engineering value and stays. The numerical claims about H1/H2/H4 ship/revert decisions are explicitly deferred to rubric_v2 evaluation in the optional Story 6.4.4.2 (§5 below), conditional on the architecture in 6.4.4.1 not already superseding the hypothesis. |

The original closeout's "Option 3 — revert prompt changes" path is rejected because (a) the v1 evidence is too noisy to justify a revert as a precaution, (b) H1 is being replaced wholesale anyway, and (c) H2 and H4 do not conflict with the architecture and have no statistically grounded reason to revert under any rubric.

---

## 3. Required additions to PR #72 before merge

These three items are **mandatory pre-merge steps for PR #72**. They do not require changes outside `story/epic6-6.4.4-prompt-shrink-sweeps`.

### 3.1 Live judge JSONs committed to the audit trail

Currently only diff reports are tracked in git. The raw judge outputs from the live evaluation runs live in the Tonyk OneDrive master folder and must be committed to PR #72 before merge so the audit trail is replayable from `master` alone. Files to add (paths under `_bmad-output/eval-runs/`):

| Run | Judge files (3 each) |
|---|---|
| `story-6.4.4-live-baseline-vs-h1` | `judge-output-claude.json`, `judge-output-gemini.json`, `judge-output-gpt5mini.json` |
| `story-6.4.4-live-baseline-vs-h2` | `judge-output-claude.json`, `judge-output-gemini.json`, `judge-output-gpt5mini.json` |
| `story-6.4.4-live-baseline-vs-h4` | `judge-output-claude.json`, `judge-output-gemini.json`, `judge-output-gpt5mini.json` |
| `story-6.4.4-live-baseline-vs-combined` | `judge-output-claude.json`, `judge-output-gemini.json`, `judge-output-gpt5mini.json` |

Owner: Dev/Human on the 6.4.4 branch. Reference: `docs/FORM-AI-EVAL-JUDGE-WORKFLOW.md` for the directory shape.

### 3.2 Rubric v1 ADR footer

`docs/stories/STORY-6.4.3b-RUBRIC-ADR.md` gains a "Supersession status" footer (added in the same PR as this amendment) noting:

- rubric_v1 is being superseded by rubric_v2 in Story 6.4.4.1;
- rubric_v1 judge outputs (including 6.4.4's) remain valid only for rubric_v1 comparisons;
- rubric_v1 → rubric_v2 cross-comparison is explicitly disallowed (per the ADR's existing baseline-re-snapshot policy).

### 3.3 No code reverts

To be explicit: no `service.py`, `prompts.yaml`, `rubric_v1.md`, harness, test, or judge prompt code is reverted. The branch ships in its current state.

---

## 4. What is preserved as input to future work

| Artefact | Future use |
|---|---|
| `STORY-6.4.4-HYPOTHESIS-EVIDENCE.md` | Input to Story 6.4.4.2 (conditional v2 re-run) for H2/H4 only; H1 will not be re-evaluated because its code is deleted by 6.4.4.1. |
| `STORY-6.4.4-JUDGE-PROMPTS.md` | Replaced by `STORY-6.4.4.1-JUDGE-PROMPTS.md` (Claude 4.7 + Grok 4 + GPT-5 mini, with calibration nudge). The 6.4.4 version is preserved as the rubric_v1 historical record. |
| Live judge JSONs (per §3.1) | Forensic comparison input only. Will not be cross-compared to rubric_v2 outputs. |
| Eval harness updates in `backend/tests/form_ai_eval/run.py` (variant-label parsing) | Carried into Story 6.4.4.1 unchanged. |
| Prompt-engineering judge prompts pattern | Pattern carries forward; concrete prompts are rewritten for v2 in 6.4.4.1. |

---

## 5. Carry-forward (post-merge)

| Item | Suggested home | Notes |
|---|---|---|
| Locale architecture wiring (registry + format/policy/tone split + brand posture parameter) | **Story 6.4.4.1** | This story replaces the AU/NZ Python constant with registry-rendered blocks; concurrent draft of the SM pack is the companion to this amendment. |
| Conditional rubric_v2 re-run of H2/H4 (not H1, not combined) | **Story 6.4.4.2 (conditional)** | Decision point: after 6.4.4.1 ships and v2-rubric baseline numbers exist, hold a 30-min review with Tonyk to decide whether 6.4.4.2 is worth running or whether we skip directly to Story 6.4.5 (H3 component cheat sheet). |
| `judge_model_version` field on judge outputs + ingest validation | **Story 6.4.4.1 (AC-9 / AC-8)** | Reproducibility requirement from Memo 0 §5 / Memo 3. |
| Judge architecture re-investigation (escape hatch) | **Story 6.4.4.1 carry-forward** | If after rubric_v2 + "name one weakness" calibration nudge all three judges still ceiling-lock, Story 6.4.4.1's AC-10 escape clause routes the question to a follow-up rather than blocking the architecture work. |

---

## 6. Acceptance criteria for this amendment

| AC | Description | Owner |
|---|---|---|
| AM-AC-1 | This amendment file checked in on `docs/epic6-story-6.4.4-closeout-amendment` and merged to `master`. | SM (Bob) |
| AM-AC-2 | `STORY-6.4.3b-RUBRIC-ADR.md` rubric_v1 supersession footer added in the same PR. | SM (Bob) |
| AM-AC-3 | All twelve live judge JSONs (4 runs × 3 judges) committed to `story/epic6-6.4.4-prompt-shrink-sweeps` before that branch merges. | Dev / Human on PR #72 |
| AM-AC-4 | PR #72 merged to `master` with no code reverts in `backend/modules/form_ai/service.py`, `prompts.yaml`, `rubric_v1.md`, harness, tests, or judge prompts. | Dev / Human on PR #72 |
| AM-AC-5 | `EPIC-6-STATUS.md` Story 6.4.4 row updated post-merge to reflect "Complete (measured-only learning under rubric_v1; H1 deletion-in-progress via 6.4.4.1)". | SM at Story 6.4.4 closeout audit |
| AM-AC-6 | Story 6.4.4.1 SM pack referenced from this amendment exists and is opened as its own Draft PR. | SM (Bob) — separate PR (deliverable B of the SM handoff) |

AM-AC-3 and AM-AC-4 are pre-conditions for PR #72 merge. AM-AC-5 is a post-merge stamp. AM-AC-1, AM-AC-2, AM-AC-6 are this PR's exit criteria.

---

## 7. Sequencing summary

```
[NOW]
  this PR (docs/epic6-story-6.4.4-closeout-amendment)
    ├── adds STORY-6.4.4-CLOSEOUT-AMENDMENT.md            (this file)
    └── adds rubric_v1 ADR supersession footer
  ↓ merges to master
[NEXT]
  PR #72 (story/epic6-6.4.4-prompt-shrink-sweeps)
    ├── adds 12 live judge JSONs (audit trail)
    └── (no code reverts)
  ↓ merges to master
[THEN]
  Story 6.4.4.1 PR (drafted concurrently with this amendment by SM)
    └── locale architecture wire-up + rubric_v2 + prompts-v1.1 + judge swap
[CONDITIONAL]
  Story 6.4.4.2 — H2/H4 re-evaluation under rubric_v2 if still useful after 6.4.4.1
```

---

## 8. References

- Authoritative brief: [`_bmad-output/planning-artifacts/STORY-6.4.4.1-SM-HANDOFF-BRIEF.md`](../../_bmad-output/planning-artifacts/STORY-6.4.4.1-SM-HANDOFF-BRIEF.md)
- Consolidated PM recommendation: [`_bmad-output/research/locale-strategy/00-CONSOLIDATED-RECOMMENDATION.md`](../../_bmad-output/research/locale-strategy/00-CONSOLIDATED-RECOMMENDATION.md)
- Original closeout: [`docs/stories/STORY-6.4.4-CLOSEOUT-REPORT.md`](./STORY-6.4.4-CLOSEOUT-REPORT.md) (on PR #72 branch — reachable via `gh pr view 72`)
- Hypothesis evidence: [`docs/stories/STORY-6.4.4-HYPOTHESIS-EVIDENCE.md`](./STORY-6.4.4-HYPOTHESIS-EVIDENCE.md) (on PR #72 branch)
- Diff reports: `_bmad-output/eval-runs/story-6.4.4-live-baseline-vs-{h1,h2,h4,combined}/diff-report.md` (on PR #72 branch)
- v1 ADR with new supersession footer: [`docs/stories/STORY-6.4.3b-RUBRIC-ADR.md`](./STORY-6.4.3b-RUBRIC-ADR.md)
- Successor story pack: [`docs/stories/story-6.4.4.1.md`](./story-6.4.4.1.md) (drafted concurrently in a separate PR)

---

*End of amendment. This file changes only the disposition section of the original closeout. Evidence sections in the original closeout (§1–7 of `STORY-6.4.4-CLOSEOUT-REPORT.md`) remain authoritative and are not superseded.*
