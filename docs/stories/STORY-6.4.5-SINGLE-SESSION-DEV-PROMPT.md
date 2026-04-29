# Story 6.4.5 Single-Session Dev Prompt

You are implementing **Story 6.4.5 — Component Property Cheat Sheet H3**.

**Worktree:** `C:\wt\elp\story-epic6-6.4.5-component-property-cheat-sheet`  
**Branch:** `story/epic6-6.4.5-component-property-cheat-sheet`  
**PR:** [#81](https://github.com/anthonykeevy/EventLeadPlatform/pull/81) — Draft PR to `master`  
**Base:** `master` at or after PR #80 (`d67337d`)

---

## Mission

Implement and measure H3: a concise component-property cheat sheet in the Form AI prompt path. It should help the model use the right semantic properties for existing component types without inventing unsupported properties.

Ship H3 only if `prompts-v1.1` / `rubric_v2` evidence clears the bar. A measured/no-change closeout is valid.

---

## Read First

1. `docs/stories/story-6.4.5.md`
2. `docs/stories/story-context-6.4.5.xml`
3. `docs/stories/STORY-6.4.4.2-CLOSEOUT-REPORT.md`
4. `docs/stories/STORY-6.4.4.1-AC10-GATE-EVIDENCE.md`
5. `docs/stories/STORY-6.4.4.1-RUBRIC-V2-ADR.md`
6. `docs/FORM-AI-EVAL-HARNESS.md`
7. `docs/FORM-AI-EVAL-JUDGE-WORKFLOW.md`
8. `docs/FORM-AI-EVAL-DIFF-STATS.md`
9. `backend/modules/form_ai/service.py`
10. `backend/tests/test_form_ai_prompt_capabilities.py`
11. `backend/tests/form_ai_eval/run.py`
12. `backend/tests/form_ai_eval/judge_pack.py`
13. `backend/tests/form_ai_eval/judge_ingest.py`

---

## Step 0 — Preflight

Run:

```powershell
.\scripts\workflow\preflight-story.ps1 `
  -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.4.5-component-property-cheat-sheet" `
  -ExpectedBranch "story/epic6-6.4.5-component-property-cheat-sheet" `
  -ReportFile "docs/stories/STORY-6.4.5-PREFLIGHT.md"
```

Verify:

- PR #81 exists and targets `master`.
- PR #79 and PR #80 are merged.
- AC10 baseline v2 artifacts exist.
- `backend/tests/form_ai_eval/prompts.yaml` is `prompts-v1.1`.
- `backend/tests/form_ai_eval/rubric_v2.md` exists.

If any precondition fails, stop and report it.

---

## Step 1 — Implement H3 Prompt Block

In `backend/modules/form_ai/service.py`, add a helper near `_build_capability_prompt_block` that renders a short component-property cheat sheet filtered to the active capability snapshot.

Preferred implementation:

- Small static map keyed by component type.
- Filter map entries to `components[].type` from the capability snapshot.
- Omit the whole block when there is no valid snapshot.
- Keep wording short and semantic-plan oriented.
- Do not mention future/unsupported components.

Suggested content shape:

```text
COMPONENT PROPERTY CHEAT SHEET (use only these semantic properties):
  - text/email/phone/url: label, placeholder, helpText, validationIntent, widthIntent
  - textarea: label, placeholder, helpText, validationIntent, widthIntent=full for long responses
  - dropdown/radio/checkbox: label, options[{label,value}], validationIntent.required, widthIntent
  - terms: label, validationIntent.required, leave legal URLs/content empty unless user provided them
  - header/paragraph/divider: display copy only; no validationIntent
  - submit-button: label/action copy, widthIntent compact/half, no validationIntent
```

Thread it into `_build_initial_messages` close to the allowed-component block.

---

## Step 2 — Focused Tests

Add tests in `backend/tests/test_form_ai_prompt_capabilities.py`:

- H3 block renders only when a capability snapshot exists.
- H3 block filters to snapshot types.
- H3 block excludes unsupported/future components.
- `_build_initial_messages` includes H3 when snapshot exists.

Run:

```powershell
python -m pytest backend/tests/test_form_ai_prompt_capabilities.py --tb=short
```

Must be green before eval work.

---

## Step 3 — H3 Eval Run

Run the H3 variant over `prompts-v1.1`.

Use variant label:

```text
story-6.4.5-h3-component-property-cheat-sheet
```

Recommended command:

```powershell
python -m backend.tests.form_ai_eval.run `
  --benchmark prompts-v1.1 `
  --variant story-6.4.5-h3-component-property-cheat-sheet
```

If wall-clock is high, use the existing locale slicing/aggregation workflow from AC10/6.4.4.2. Keep the final aggregate run id exactly traceable.

---

## Step 4 — Judge Package + Cursor Judge Flow

Generate a rubric_v2 judge package for the H3 run. Verify the three emitted prompt files include exact output paths:

- `judge-prompt-claude.md`
- `judge-prompt-grok.md`
- `judge-prompt-gpt5mini.md`

Post the three prompt paths to Tonyk. After judge outputs are saved, run:

```powershell
python -m backend.tests.form_ai_eval.judge_ingest _bmad-output/eval-runs/story-6.4.5-h3-component-property-cheat-sheet/judge-package
```

Record summary paths and key metrics in `STORY-6.4.5-HYPOTHESIS-EVIDENCE.md`.

---

## Step 5 — Diff/Stats

Compare H3 against the AC10 baseline:

- Control: `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-v2/`
- Variant: `_bmad-output/eval-runs/story-6.4.5-h3-component-property-cheat-sheet/`

Use `docs/FORM-AI-EVAL-DIFF-STATS.md` for exact commands. Record output paths, significant regressions, wins, inconclusive metrics, and advisory runtime/cost deltas.

---

## Step 6 — Decision Rule

Ship H3 only if:

- no structural blockers,
- no material Category B regression,
- evidence shows a useful improvement or at least a safe neutral result that Tonyk/PM explicitly accept,
- focused/backend gates are green.

If H3 fails or remains inconclusive, revert the prompt code and close measured/no-change.

---

## Step 7 — Green Gate

Run focused tests and backend regression:

```powershell
python -m pytest backend/tests/test_form_ai_prompt_capabilities.py backend/tests/test_form_ai_eval_harness.py backend/tests/test_judge_pack.py --tb=short
python -m pytest backend/tests --tb=short
```

Frontend checks are required only if frontend files are touched:

```powershell
cd frontend
npm run lint
npm run test:unit -- --watch=false
```

Record exact final summaries in `STORY-6.4.5-GATE-EVIDENCE.md`.

---

## Step 8 — Closeout

Before merge:

1. Fill `STORY-6.4.5-HYPOTHESIS-EVIDENCE.md`.
2. Fill `STORY-6.4.5-GATE-EVIDENCE.md`.
3. Fill `STORY-6.4.5-UAT-RESULTS.md`.
4. Fill `STORY-6.4.5-CLOSEOUT-REPORT.md`.
5. Update `story-6.4.5.md`, `EPIC-6-STATUS.md`, and `EPIC-6-WORKFLOW-GUIDE.md`.
6. Run the SM stale-field audit before merge.

Expected next-story routing:

- Clean H3 closeout -> Story 6.5a clarification questions.
- H3 tooling blocker -> smallest fix story before 6.5a.

