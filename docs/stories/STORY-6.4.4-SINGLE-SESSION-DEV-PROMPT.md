# Story 6.4.4 Single-Session Dev Prompt

You are implementing **Story 6.4.4 — Prompt Shrink Sweeps H1/H2/H4**.

**Worktree:** `C:\wt\elp\story-epic6-6.4.4-prompt-shrink-sweeps`  
**Branch:** `story/epic6-6.4.4-prompt-shrink-sweeps`  
**PR:** [#72](https://github.com/anthonykeevy/EventLeadPlatform/pull/72) — Draft PR to `master`  

---

## Mission

Run measured prompt shrink experiments for H1, H2, H4, and combined H1+H2+H4. Ship only evidence-backed winners. Revert losers before merge.

---

## Read First

1. `docs/stories/story-6.4.4.md`
2. `docs/stories/story-context-6.4.4.xml`
3. `docs/FORM-AI-EVAL-HARNESS.md`
4. `docs/FORM-AI-EVAL-JUDGE-WORKFLOW.md`
5. `docs/FORM-AI-EVAL-DIFF-STATS.md`
6. `backend/modules/form_ai/service.py`

---

## Step 0 — Preflight

Run:

```powershell
python scripts/agent/preflight.py `
  -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.4.4-prompt-shrink-sweeps" `
  -ExpectedBranch "story/epic6-6.4.4-prompt-shrink-sweeps" `
  -Story "6.4.4"
```

Record output in `docs/stories/STORY-6.4.4-PREFLIGHT.md`.

---

## Step 1 — Establish Baseline

Use the frozen benchmark set and existing harness. Prefer the latest stable post-6.4.2/6.4.3c baseline if valid; otherwise run a fresh control.

Record:

- run ID,
- command,
- artifact path,
- model/provider,
- repetitions,
- cost/cap settings,
- any checkpoint/resume behavior.

Update `STORY-6.4.4-HYPOTHESIS-EVIDENCE.md`.

---

## Step 2 — H1 Locale Shrink

Change only the AU/NZ locale prompt block to:

```text
Form audience: Australia/New Zealand. Use AU/NZ spelling, address, phone, date conventions.
```

Run the eval harness with a clear variant label such as `h1-locale-one-line`.

Generate diff outputs against baseline and update the evidence file.

Revert H1 if locale behavior regresses.

---

## Step 3 — H2 Consent/Legal Shrink

Change only `_CONSENT_GUIDANCE_BLOCK` to a compact decision table that preserves:

- `terms` component selection,
- checkbox fallback behavior,
- company-managed terms behavior,
- required acknowledgement behavior,
- no invented legal URLs/content unless requested.

Run the eval harness with a clear variant label such as `h2-consent-decision-table`.

Generate diff outputs and update evidence.

Revert H2 if terms/checkbox selection regresses.

---

## Step 4 — H4 Operational Notes Trim

Trim only duplicated operational notes/context-pack guidance already covered by the active prompt contract.

Run the eval harness with a clear variant label such as `h4-operational-trim`.

Generate diff outputs and update evidence.

Revert H4 if collision handling, row grouping, tab order, or supported catalog compliance regresses.

---

## Step 5 — Combined Variant

Apply H1+H2+H4 together from a known state and run `h1-h2-h4-combined`.

Generate diff outputs and update evidence.

If combined fails, ship only the individually accepted subset.

---

## Step 6 — Judge Evidence

For variants needing Category B semantic confidence:

1. Generate judge package(s).
2. Ask Anthony to run Cursor judges if required.
3. Ingest judge JSON outputs.
4. Re-run diff/statistics reports using the judge summaries.

Document any missing manual judge evidence as a UAT gap, not as a silent pass.

---

## Step 7 — Gates

Run focused checks for touched prompt/eval code. At minimum:

```powershell
cd backend
python -m pytest tests/test_form_ai_service.py --tb=short
python -m pytest tests/test_eval_diff.py tests/test_eval_stats.py --tb=short
```

Run the broader backend gate unless a clear exception is agreed:

```powershell
cd backend
python -m pytest --tb=short
```

Record results in `docs/stories/STORY-6.4.4-GATE-EVIDENCE.md`.

---

## Step 8 — Closeout

Complete:

- `docs/stories/STORY-6.4.4-HYPOTHESIS-EVIDENCE.md`
- `docs/stories/STORY-6.4.4-GATE-EVIDENCE.md`
- `docs/stories/STORY-6.4.4-CLOSEOUT-REPORT.md`

Update `docs/stories/story-6.4.4.md` with implementation notes and final status.

Before asking for review, run:

```powershell
gh pr view 72 --json state,isDraft,mergedAt,headRefName,baseRefName,url
rg -n "Ready for UAT|Ready for UAT/SM review|Keep PR .* open|Current Focus" docs/stories/story-6.4.4.md docs/stories/STORY-6.4.4-CLOSEOUT-REPORT.md docs/stories/EPIC-6-STATUS.md docs/stories/EPIC-6-WORKFLOW-GUIDE.md
```

`Draft` is expected while PR #72 is still a Draft PR.

---

## Non-Negotiables

- Do not mutate `prompts.yaml`.
- Do not mutate `rubric_v1.md`.
- Do not implement H3/H5/H6/Image-to-Form.
- Do not keep structural-blocker regressions.
- Do not hide inconclusive variants in the final diff.
- Do not run Alembic.
