# Story 6.4.4.2 — Re-evaluate H2/H4 under rubric_v2

**Epic:** 6 — AI Generation & Monetization Engine  
**Story ID:** 6.4.4.2  
**Title:** Re-evaluate H2/H4 under rubric_v2  
**Status:** Draft / story worktree opened  
**Branch:** `story/epic6-6.4.4.2-h2-h4-rubric-v2-rerun`  
**PR:** [#79](https://github.com/anthonykeevy/EventLeadPlatform/pull/79) — Draft  
**Created:** 2026-04-28  
**Depends On:** Story 6.4.4.1-ac10 ([PR #77](https://github.com/anthonykeevy/EventLeadPlatform/pull/77)) and AC10 post-merge stamp ([PR #78](https://github.com/anthonykeevy/EventLeadPlatform/pull/78)) merged.  
**Unblocks:** Story 6.4.5 and later additive AI capability stories.

---

## 1) Goal

Re-run the two plausible prompt-shrink candidates from Story 6.4.4 — **H2 consent/legal decision table** and **H4 operational-notes trim** — against the now-valid `prompts-v1.1` / `rubric_v2` baseline from Story 6.4.4.1-ac10.

This story exists because AC10 passed with real judge variance. That makes the v2 judge panel usable for deciding whether H2 and/or H4 are safe to ship. This is a measured decision story, not a broad prompt refactor.

Success means:

- H2 and H4 are each tested as single-variable variants against the AC10 v2 baseline.
- Each candidate has structural, judge, ingest, and diff/stat evidence.
- Only evidence-backed winners are retained.
- If neither candidate clears the bar, close the story as measured/no-change and move to Story 6.4.5.

---

## 2) In Scope

### 2.1 Baseline reuse

Use the regenerated AC10 baseline package as the control:

- `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-v2/`
- `prompts-v1.1`
- `rubric_v2`
- Judge panel: Claude 4.7 + Grok 4 primary, GPT-5 mini control.

Do not compare rubric_v1 and rubric_v2 scores.

### 2.2 H2 consent/legal decision table

Re-apply the compact consent/legal guidance from Story 6.4.4 as a single-variable variant. Preserve:

- `terms` component selection when the user asks for terms/legal acknowledgement,
- checkbox fallback behavior,
- company-managed terms behavior,
- required acknowledgement behavior,
- no invented legal URLs/content unless requested.

Variant run label: `story-6.4.4.2-h2-consent-v2`.

### 2.3 H4 operational-notes trim

Re-apply the operational-notes/context-pack trim from Story 6.4.4 as a single-variable variant. Preserve:

- collision recovery,
- row grouping,
- tab order,
- supported catalog compliance,
- existing validation contract behavior.

Variant run label: `story-6.4.4.2-h4-operational-trim-v2`.

### 2.4 Optional accepted-subset final run

If H2 and H4 both pass individually, run a final accepted-subset variant with H2+H4 together to catch interaction effects. Do not include H1.

Variant run label: `story-6.4.4.2-h2-h4-accepted-v2`.

### 2.5 Evidence and decision artifacts

Required artifacts:

- `STORY-6.4.4.2-HYPOTHESIS-EVIDENCE.md`
- `STORY-6.4.4.2-GATE-EVIDENCE.md`
- `STORY-6.4.4.2-UAT-RESULTS.md`
- `STORY-6.4.4.2-CLOSEOUT-REPORT.md`

Evidence must include:

- commands run,
- run IDs,
- prompt-size deltas,
- structural metrics,
- judge output paths,
- ingest summaries,
- diff/statistics outputs,
- final ship/revert/no-change verdict for H2 and H4.

---

## 3) Out of Scope

| Item | Reason / future home |
|---|---|
| H1 locale one-line shrink | Rejected/suspect after combined locale-fidelity regression; superseded by Story 6.4.4.1 locale architecture. |
| Combined H1+H2+H4 | Explicitly rejected by Story 6.4.4 evidence due significant locale-fidelity regression. |
| H3 Component Property Cheat Sheet | Story 6.4.5. |
| H5 Style Intent resolver | Later style story. |
| H6 Google Fonts directive | Conditional later story. |
| Image-to-Form | Later 6.5b-vision story. |
| Rubric v3 or judge-panel redesign | AC10 passed; rubric_v2 remains authoritative. |
| New migrations or public API changes | This story should only touch prompt/service/eval/docs code paths. |

---

## 4) Acceptance Criteria

1. **AC-1 Baseline control pinned:** Story references and verifies the AC10 regenerated v2 baseline (`story-6.4.4.1-ac10-baseline-v2`) as the control for comparisons.
2. **AC-2 H2 variant re-applied and measured:** H2 consent/legal decision table is applied as a single-variable variant and run against `prompts-v1.1` / `rubric_v2`.
3. **AC-3 H4 variant re-applied and measured:** H4 operational-notes trim is applied as a single-variable variant and run against `prompts-v1.1` / `rubric_v2`.
4. **AC-4 Judge packages generated:** Each measured variant has a judge package using rubric_v2 with explicit output paths for Claude, Grok, and GPT-5 mini.
5. **AC-5 Cursor judge outputs ingested:** Judge JSONs are present, valid, and ingested into summary JSON/CSV for each variant.
6. **AC-6 Diff/statistics outputs recorded:** Each variant has diff/stat outputs against the AC10 baseline, including p-values/effect sizes where applicable.
7. **AC-7 Final verdict recorded:** H2 and H4 each have a clear ship/revert/no-change verdict in `STORY-6.4.4.2-HYPOTHESIS-EVIDENCE.md`.
8. **AC-8 Revert losers:** Any failing or inconclusive prompt change is reverted before merge unless Tonyk/PM explicitly accepts it with the evidence recorded.
9. **AC-9 Accepted-subset interaction checked:** If both H2 and H4 pass individually, the accepted H2+H4 subset is run once and checked for interaction regressions.
10. **AC-10 No unrelated AI capability work:** No H1, H3, H5, H6, image-to-form, or frontend feature work leaks into this story.
11. **AC-11 Green gate evidence recorded:** Focused prompt/eval tests and backend regression evidence are recorded in `STORY-6.4.4.2-GATE-EVIDENCE.md`; frontend checks are run only if frontend files are touched, otherwise explicitly marked not applicable.
12. **AC-12 Closeout complete:** Closeout report records shipped changes, reverted changes, carry-forward items, and the next recommended story.

---

## 5) Definition of Done

- All ACs are mapped to gate evidence or UAT results.
- Story branch is pushed and Draft PR #79 remains the review surface.
- No untracked scratch artifacts are committed.
- Any retained prompt changes are backed by v2 evidence.
- Stale-field audit passes before merge.
- Workflow guide Current Focus advances to the next story at closeout.

