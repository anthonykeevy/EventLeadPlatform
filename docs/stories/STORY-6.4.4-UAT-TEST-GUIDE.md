# Story 6.4.4 UAT Test Guide

**Story:** 6.4.4 — Prompt Shrink Sweeps H1/H2/H4  
**Branch:** `story/epic6-6.4.4-prompt-shrink-sweeps`  
**PR:** [#72](https://github.com/anthonykeevy/EventLeadPlatform/pull/72) — Draft  
**Audience:** Anthony / SM  
**Prep:** Dev completes gate evidence, hypothesis evidence, and closeout report.

---

## 1) UAT Goal

Confirm that every prompt shrink decision is evidence-backed:

- H1 locale shrink,
- H2 consent/legal shrink,
- H4 operational notes trim,
- combined H1+H2+H4 interaction.

UAT is mostly evidence review unless Dev requests Anthony to run Cursor judge scoring.

---

## 2) Required Evidence

Review these files:

- `docs/stories/STORY-6.4.4-HYPOTHESIS-EVIDENCE.md`
- `docs/stories/STORY-6.4.4-GATE-EVIDENCE.md`
- `docs/stories/STORY-6.4.4-CLOSEOUT-REPORT.md`
- `_bmad-output/eval-runs/<story-6.4.4-run>/`

Expected evidence:

- baseline and variant run IDs,
- diff reports for H1, H2, H4, and combined,
- prompt size deltas,
- structural blockers/advisory deltas,
- judge ingest summaries where semantic scoring was performed,
- final ship/revert verdicts.

---

## 3) Review Checklist

| Step | Check | Expected |
|------|-------|----------|
| 3.1 | Open hypothesis evidence | All H1/H2/H4/combined rows are complete. |
| 3.2 | Inspect baseline and variant paths | Run artifacts exist and have clear names. |
| 3.3 | Open each diff report | Reports are readable and compare against the same baseline. |
| 3.4 | Check structural blockers | Shipped changes have no schema regression or boundary violations. |
| 3.5 | Check semantic evidence | Judge gaps are explicit; inconclusive results are not silently shipped. |
| 3.6 | Check final code diff | Only accepted prompt changes remain. |
| 3.7 | Check out-of-scope guard | No H3/H5/H6/Image-to-Form work appears. |

---

## 4) Optional Cursor Judge Flow

If Dev needs Category B scoring:

1. Open the generated judge package from `_bmad-output/eval-runs/.../judge-package/`.
2. Follow `docs/FORM-AI-EVAL-JUDGE-WORKFLOW.md`.
3. Save judge JSON outputs in the requested artifact directory.
4. Ask Dev to ingest the judge outputs and regenerate the diff/stat evidence.

Do not paste sensitive credentials or production secrets into judge prompts.

---

## 5) Approval Decision

Approve only when:

- every retained prompt shrink has PASS evidence,
- losers or inconclusive variants are reverted or clearly deferred,
- closeout lists the exact final shipped changes,
- backend/focused gates pass or exceptions are explicitly justified.

Reject or send back if:

- combined variant passes but individual variants were not evaluated,
- evidence does not identify run IDs and artifact paths,
- a prompt change is retained despite structural blockers,
- the story includes unrelated prompt/capability changes.

---

## 6) UAT Sign-Off

| Field | Value |
|-------|-------|
| UAT reviewer | Anthony |
| Date | TBD |
| Decision | TBD |
| Notes | TBD |
