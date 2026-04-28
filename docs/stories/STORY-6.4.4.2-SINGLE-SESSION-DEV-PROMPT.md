# Story 6.4.4.2 Single-Session Dev Prompt

You are implementing **Story 6.4.4.2 — Re-evaluate H2/H4 under rubric_v2**.

**Worktree:** `C:\wt\elp\story-epic6-6.4.4.2-h2-h4-rubric-v2-rerun`  
**Branch:** `story/epic6-6.4.4.2-h2-h4-rubric-v2-rerun`  
**PR:** [#79](https://github.com/anthonykeevy/EventLeadPlatform/pull/79) — Draft PR to `master`  
**Base:** `master` at or after PR #78 (`fd66b17`)

---

## Mission

Use the valid AC10 `rubric_v2` baseline to decide whether the two plausible prompt-shrink candidates from Story 6.4.4 can ship:

- **H2:** compact consent/legal decision table.
- **H4:** operational-notes/context-pack trim.

Keep the story evidence-first. H1 is out. Combined H1+H2+H4 is out. A no-change closeout is acceptable if H2/H4 do not clear the bar.

---

## Read First

1. `docs/stories/story-6.4.4.2.md`
2. `docs/stories/story-context-6.4.4.2.xml`
3. `docs/stories/STORY-6.4.4-HYPOTHESIS-EVIDENCE.md`
4. `docs/stories/STORY-6.4.4.1-AC10-CLOSEOUT-REPORT.md`
5. `docs/stories/STORY-6.4.4.1-AC10-GATE-EVIDENCE.md`
6. `docs/stories/STORY-6.4.4.1-RUBRIC-V2-ADR.md`
7. `docs/FORM-AI-EVAL-HARNESS.md`
8. `docs/FORM-AI-EVAL-JUDGE-WORKFLOW.md`
9. `docs/FORM-AI-EVAL-DIFF-STATS.md`
10. `backend/modules/form_ai/service.py`
11. `backend/tests/form_ai_eval/run.py`
12. `backend/tests/form_ai_eval/judge_pack.py`
13. `backend/tests/form_ai_eval/judge_ingest.py`

---

## Step 0 — Preflight

Run:

```powershell
.\scripts\workflow\preflight-story.ps1 `
  -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.4.4.2-h2-h4-rubric-v2-rerun" `
  -ExpectedBranch "story/epic6-6.4.4.2-h2-h4-rubric-v2-rerun" `
  -ReportFile "docs/stories/STORY-6.4.4.2-PREFLIGHT.md"
```

Verify:

- PR #79 exists and targets `master`.
- `gh pr view 77 --json state,mergedAt` shows `MERGED`.
- `gh pr view 78 --json state,mergedAt` shows `MERGED`.
- AC10 baseline exists at `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-v2/`.
- `judge-ingest-summary.json` exists in that baseline package and includes Claude, Grok, and GPT-5 mini.
- `backend/tests/form_ai_eval/prompts.yaml` is `prompts-v1.1`.
- `backend/tests/form_ai_eval/rubric_v2.md` exists.

If any precondition fails, stop and report it.

---

## Step 1 — Pin Baseline Control

Record the baseline control in `STORY-6.4.4.2-HYPOTHESIS-EVIDENCE.md`:

- run id: `story-6.4.4.1-ac10-baseline-v2`
- package path,
- judge ingest summary path,
- primary means and control mean,
- row count and generated-definition availability.

Do not re-run the baseline unless an artifact is missing or invalid.

---

## Step 2 — H2 Single-Variable Variant

Re-apply only the H2 consent/legal shrink from Story 6.4.4.

Expected intent:

- Replace the large consent/legal guidance with a compact decision table.
- Preserve `terms` component selection.
- Preserve checkbox fallback behavior.
- Preserve company-managed terms behavior.
- Preserve required acknowledgement behavior.
- Do not invent legal URLs/content unless requested.

Run the eval harness with a clear variant label:

```powershell
python -m backend.tests.form_ai_eval.run `
  --benchmark prompts-v1.1 `
  --variant story-6.4.4.2-h2-consent-v2
```

Generate the judge package and verify the emitted prompts include exact output paths.

---

## Step 3 — H4 Single-Variable Variant

Return to a clean baseline state, then re-apply only the H4 operational-notes trim from Story 6.4.4.

Expected intent:

- Trim duplicated operational/context-pack notes already covered elsewhere.
- Preserve collision recovery.
- Preserve row grouping.
- Preserve tab order.
- Preserve supported catalog compliance.

Run:

```powershell
python -m backend.tests.form_ai_eval.run `
  --benchmark prompts-v1.1 `
  --variant story-6.4.4.2-h4-operational-trim-v2
```

Generate the judge package and verify explicit output paths.

---

## Step 4 — Judge Flow

For each variant that reaches judge review:

1. Post the three ready-to-paste prompt paths in chat:
   - `judge-prompt-claude.md`
   - `judge-prompt-grok.md`
   - `judge-prompt-gpt5mini.md`
2. Tonyk runs three Cursor judge sessions and saves outputs to the paths embedded in the prompts.
3. After the outputs exist, run ingest:

```powershell
python -m backend.tests.form_ai_eval.judge_ingest _bmad-output/eval-runs/<variant-run-id>/judge-package
```

Record each summary path and key metrics in `STORY-6.4.4.2-HYPOTHESIS-EVIDENCE.md`.

---

## Step 5 — Diff/Stats

Compare each variant against the AC10 v2 baseline using the existing diff/statistics tooling. Use the documented commands in `docs/FORM-AI-EVAL-DIFF-STATS.md`.

Record:

- output folder,
- significant regressions,
- inconclusive metrics,
- effect sizes,
- advisory runtime/component-count deltas.

---

## Step 6 — Decision Rule

For each candidate:

- **Ship:** no structural blockers, no material semantic regression, and PM/SM/Tonyk accept the v2 evidence.
- **Revert:** structural blocker, material semantic regression, or evidence remains inconclusive and no explicit acceptance is given.
- **Measured/no-change:** no candidate clears the bar; close the story without prompt changes and move to Story 6.4.5.

If both H2 and H4 pass individually, run one accepted-subset interaction check:

```powershell
python -m backend.tests.form_ai_eval.run `
  --benchmark prompts-v1.1 `
  --variant story-6.4.4.2-h2-h4-accepted-v2
```

Only retain the subset if the interaction check does not regress.

---

## Step 7 — Green Gate

At minimum, run focused tests covering any prompt/service/eval code touched. Then run the backend regression gate unless there is a documented CI-backed exception:

```powershell
python -m pytest backend/tests --tb=short
```

Frontend checks are required only if frontend files are touched:

```powershell
cd frontend
npm run lint
npm run test:unit -- --watch=false
```

Record exact final summaries in `STORY-6.4.4.2-GATE-EVIDENCE.md`. If output is truncated before a final summary, treat it as failed.

---

## Step 8 — Closeout

Before marking complete:

1. Fill `STORY-6.4.4.2-HYPOTHESIS-EVIDENCE.md`.
2. Fill `STORY-6.4.4.2-GATE-EVIDENCE.md`.
3. Fill `STORY-6.4.4.2-UAT-RESULTS.md`.
4. Fill `STORY-6.4.4.2-CLOSEOUT-REPORT.md`.
5. Update `story-6.4.4.2.md`, `EPIC-6-STATUS.md`, and `EPIC-6-WORKFLOW-GUIDE.md`.
6. Run the SM stale-field audit before merge.

Next-story routing:

- If H2/H4 decision closes cleanly, recommend Story 6.4.5.
- If judge/eval tooling blocks the decision, register a carry-forward with severity and recommend the smallest fix story before 6.4.5.

