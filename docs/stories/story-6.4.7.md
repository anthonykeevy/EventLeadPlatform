# Story 6.4.7 - AU Baseline Analysis And Iterative Prompt Improvement Loop

**Epic:** 6 - AI Generation & Monetization Engine  
**Story ID:** 6.4.7  
**Title:** AU Baseline Analysis And Iterative Prompt Improvement Loop  
**Status:** Complete / Closed  
**Branch:** `story/epic6-6.4.7-au-baseline-analyst-loop`  
**PR:** [#84](https://github.com/anthonykeevy/EventLeadPlatform/pull/84) - Merged 2026-05-06  
**Created:** 2026-05-05  
**Depends On:** Story 6.4.6 ([PR #82](https://github.com/anthonykeevy/EventLeadPlatform/pull/82)) merged and `AU-000` baseline captured.  
**Unblocks:** First AU prompt/context improvement decision against the frozen Story 6.4.6 baseline.

---

## 1) Goal

Run the BMAD Analyst-owned AU prompt improvement loop against the frozen Story 6.4.6 baseline.

This story should convert the `AU-000` evidence into one approved, controlled prompt/context experiment, execute it through the Story 6.4.6 Analyst harness, ingest judge results, update the iteration tracking sheet, and stop for Tony's keep / reject / revise / continue decision.

Success is not "highest aggregate score." Success is causal evidence about whether one controlled prompt/context change set improves AU launch quality without introducing material regressions.

---

## 2) In Scope

### 2.1 Baseline analysis

Review the frozen baseline and related evidence:

- `docs/stories/STORY-6-AU-EVAL-ANALYST-LOOP.md`
- `docs/stories/STORY-6-AU-EVAL-ITERATION-TRACKING.md`
- `docs/stories/STORY-6.4.6-AU-BASELINE-EVIDENCE.md`
- `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/`
- `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/judge-package/judge-ingest-summary.json`
- `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/au-deterministic-checks.json`

The Analyst must inspect row-level failures, judge conflict findings, deterministic AU failures, judge disagreement, and likely responsible prompt/context sections before proposing changes.

### 2.2 Top 5 candidate improvements

Present Tony with the top 5 candidate prompt/context improvements before editing anything.

For each candidate, include:

- Target prompt/context section.
- Failure evidence from `AU-000`.
- Expected metric movement.
- Known risk / possible regression.
- Whether it can safely be bundled with another candidate without obscuring causality.

The Analyst recommends one controlled change set and then stops for Tony approval.

### 2.3 One approved controlled experiment

After Tony approval, create one experiment configuration and any eval-only prompt/context overlay files needed to run it.

Rules:

- Use version-managed prompt/context or docs/story experiment artifacts only.
- Prefer `candidate_prompt_block` / eval-only overlay text unless Tony approves a direct prompt/context artifact change.
- Use one controlled change set only.
- Keep the baseline run folder immutable.
- Use a new immutable candidate run ID.

### 2.4 Eval and judge execution

Run the approved candidate through the Analyst experiment harness:

- Use `backend.tests.form_ai_eval.experiment`.
- Use `backend/tests/form_ai_eval/prompts_au_v1.yaml`.
- Compare against `story-6.4.6-au-baseline-current`.
- Produce candidate run artifacts, judge package, diff outputs, and tracking payload.
- Run or coordinate three Cursor judge sessions for Claude, Grok, and GPT-5 mini.
- Ingest judge outputs with `backend.tests.form_ai_eval.judge_ingest`.

### 2.5 Decision and tracking

Update `docs/stories/STORY-6-AU-EVAL-ITERATION-TRACKING.md` with a new row, expected to start at `AU-001`.

The row must record:

- Baseline run ID.
- Candidate run ID.
- Prompt/context section changed.
- Exact change tested.
- Hypothesis and expected movement.
- Actual movement.
- Improved/regressed metrics.
- Improved/regressed rows.
- Judge conflict findings.
- Deterministic AU findings.
- Decision: keep / reject / revise / pending Tony decision.
- Evidence links.

The story must stop after Tony's decision. Do not start a second loop inside this story unless Tony explicitly asks and the story scope is updated.

---

## 3) Out of Scope

| Item | Reason / future home |
|---|---|
| Backend, frontend, application, harness, judge-ingest, or migration code changes | Story 6.4.7 is Analyst-owned. If code changes are needed, stop and raise the smallest Dev-owned framework fix story. |
| Alembic commands | No DB migration is expected; agents must not run Alembic commands. |
| More than one uncontrolled prompt experiment | Causal clarity is the point of this reset. |
| Six-locale prompt sweeps | Explicitly paused by the AU-first reset. |
| Declaring a permanent prompt winner without Tony/SM review | Candidate promotion requires explicit decision after evidence review. |
| Customer-discovery hardening work | Tracked separately under Epic 6 Phase D / discovery docs. |

---

## 4) Acceptance Criteria

1. **AC-1 Baseline evidence reviewed:** Analyst reviews `AU-000`, deterministic AU findings, judge ingest, row-level weak spots, and likely responsible prompt/context sections before proposing changes.
2. **AC-2 Top 5 candidates presented:** Analyst presents five candidate improvements with target section, evidence, expected movement, risk, and bundleability guidance.
3. **AC-3 Tony approval recorded:** No prompt/context edits or experiment run starts until Tony approves one controlled change set.
4. **AC-4 Scope boundary preserved:** No application, backend, frontend, harness, judge-ingest, or migration code is modified.
5. **AC-5 Experiment config created:** The approved experiment is represented by a version-managed config and any eval-only overlay file(s), with stable run IDs and hypothesis metadata.
6. **AC-6 Candidate eval run complete:** Candidate run artifacts are produced under a new immutable run folder without overwriting `story-6.4.6-au-baseline-current`.
7. **AC-7 Judge packages complete:** Candidate judge packages include experiment metadata, changed-section context, shared context bundle, and model-specific judge prompts.
8. **AC-8 Judge outputs ingested:** Claude, Grok, and GPT-5 mini outputs are saved, validated, ingested, and summarized.
9. **AC-9 Diff/evidence reviewed:** Candidate results are compared to the frozen baseline using deterministic checks, judge metrics, row-level movement, and diff artifacts.
10. **AC-10 Tracking row updated:** `STORY-6-AU-EVAL-ITERATION-TRACKING.md` has a complete `AU-001` row with decision and evidence links.
11. **AC-11 Stop/continue gate honored:** Story stops after Tony's keep / reject / revise / continue decision.
12. **AC-12 Green gates recorded:** Focused Analyst harness tests are run and recorded; frontend checks are not required unless frontend files are touched, which should not happen in this story.

---

## 5) Definition of Done

- Draft PR #84 exists and targets `master`.
- Story artifacts are present:
  - `docs/stories/story-6.4.7.md`
  - `docs/stories/story-context-6.4.7.xml`
  - `docs/stories/STORY-6.4.7-UAT-TEST-GUIDE.md`
  - `docs/stories/STORY-6.4.7-SINGLE-SESSION-DEV-PROMPT.md`
- Top 5 candidate improvements are captured in story evidence or the PR discussion before any experiment edit.
- One approved controlled experiment has been executed.
- Judge outputs are ingested.
- `AU-001` is updated in the tracking sheet.
- Tony's decision is recorded.
- No code changes are included unless the story is stopped and replaced by a Dev-owned fix story.

---

## 6) Closeout

Story 6.4.7 is closed as an Analyst-owned evaluation and decision story.

- Closeout report: `docs/stories/STORY-6.4.7-CLOSEOUT-REPORT.md`
- Top performer: `AU-005` at `4.471 / 5` (`89.4%`)
- Production recommendation: create a follow-up implementation story to promote AU-005's strict AU + publish-ready prompt improvements into production prompt/context sections, using AU-006's lint-clean wording lessons without repeating AU-006's policy, validation, and copy-quality regressions.
