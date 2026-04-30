# Story 6.4.6 Single-Session Dev Prompt

You are implementing **Story 6.4.6 - AU-Only Diagnostic Evaluation Framework + Baseline**.

**Worktree:** `C:\wt\elp\story-epic6-6.4.6-au-diagnostic-eval-framework`  
**Branch:** `story/epic6-6.4.6-au-diagnostic-eval-framework`  
**PR:** [#82](https://github.com/anthonykeevy/EventLeadPlatform/pull/82) - Draft PR to `master`  
**Base:** `master` at or after PR #81 merge commit `93bfceb`

---

## Mission

Build the AU-only diagnostic evaluation framework and produce the first current-state AU baseline.

This is not a prompt-improvement story. Do not apply candidate prompt/context changes. The output of this story is a clean diagnostic framework, baseline artifacts, and a filled `AU-000` row for the Analyst loop in Story 6.4.7.

---

## Read First

1. `docs/stories/story-6.4.6.md`
2. `docs/stories/story-context-6.4.6.xml`
3. `docs/stories/STORY-6-AU-EVAL-ANALYST-LOOP.md`
4. `docs/stories/STORY-6-AU-EVAL-ITERATION-TRACKING.md`
5. `docs/stories/STORY-6.4.5-CLOSEOUT-REPORT.md`
6. `docs/FORM-AI-EVAL-HARNESS.md`
7. `docs/FORM-AI-EVAL-JUDGE-WORKFLOW.md`
8. `docs/FORM-AI-EVAL-DIFF-STATS.md`
9. `backend/tests/form_ai_eval/run.py`
10. `backend/tests/form_ai_eval/prompts.yaml`
11. `backend/tests/form_ai_eval/judge_pack.py`
12. `backend/tests/form_ai_eval/judge_ingest.py`
13. `backend/modules/form_ai/service.py`

---

## Step 0 - Preflight

Run:

```powershell
.\scripts\workflow\preflight-story.ps1 `
  -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.4.6-au-diagnostic-eval-framework" `
  -ExpectedBranch "story/epic6-6.4.6-au-diagnostic-eval-framework" `
  -ReportFile "docs/stories/STORY-6.4.6-PREFLIGHT.md"
```

Verify:

- PR #82 exists and targets `master`.
- PR #81 is merged.
- You are not in the Story 6.4.5 worktree.
- `docs/stories/STORY-6-AU-EVAL-ANALYST-LOOP.md` and `docs/stories/STORY-6-AU-EVAL-ITERATION-TRACKING.md` exist.

If any precondition fails, stop and report it.

---

## Step 1 - AU Prompt Set

Create an AU-only benchmark prompt set for launch diagnostics.

Expected outcome:

- A version-managed AU prompt file, for example `backend/tests/form_ai_eval/prompts_au_v1.yaml`.
- A benchmark version such as `prompts-au-v1`.
- Stable prompt IDs and metadata that support row-level comparison in Story 6.4.7.
- Explicit metadata for adversarial source-market adaptation rows, if any.

Rules:

- Rewrite or replace non-AU market rows rather than carrying six-locale noise forward.
- Keep form-type variety.
- Remove accidental foreign-market cues such as NHS, UK GDPR, NZ regions, ZIP/+1, +44/+64, EU lawful basis, and CCPA-only privacy wording unless the row is explicitly adversarial.
- Keep the file JSON-shaped YAML if the current loader remains dependency-free.

Update loader/tests so the AU prompt set can run without weakening existing `prompts-v1.1` tests.

---

## Step 2 - AU Locale Contract

Create a version-managed AU locale contract from existing DB/config facts plus the approved story text.

The contract must include:

- +61 phone guidance.
- DD/MM/YYYY dates.
- Suburb, State, Postcode.
- AUD.
- Privacy Act 1988.
- Spam Act 2003.
- Australian English.
- Practical/plain-English tone.

Record the artifact path and any source/assumption notes in `STORY-6.4.6-AU-BASELINE-EVIDENCE.md`.

---

## Step 3 - Complete Prompt Context Sections

Add framework support to assemble the complete LLM prompt context into stable sections before generation.

Required shared sections:

- `system_prompt_output_contract`
- `au_locale_block`
- `brand_posture_block`
- `component_capability_block`
- `component_property_cheat_sheet` if active
- `consent_legal_guidance`
- `context_pack_excerpt`
- `candidate_prompt_block` if active

Each section needs:

- Stable section ID.
- Human-readable label.
- Content hash.
- Content used for the eval row.

Prefer extracting/reusing existing prompt assembly helpers so the diagnostic view matches what the LLM receives. Do not create a production API surface unless there is no safer eval-only path.

---

## Step 4 - Context Consistency Preflight/Linter

Add a deterministic preflight/linter that checks the complete prompt context before generation.

It must detect and report at least:

- ZIP where Postcode is expected.
- +1, +44, or +64 where +61 or neutral AU guidance is expected.
- MM/DD/YYYY where DD/MM/YYYY is expected.
- GDPR/CCPA-only privacy wording where AU privacy wording is expected.
- NHS, NZ-region, or other foreign-market leakage unless explicitly tagged as intentional.

The linter should write artifacts under the eval run folder, such as:

- `prompt-context-lint.json`
- `prompt-context-lint.md`
- `au-deterministic-checks.json`
- `au-deterministic-checks.md`

If the preflight finds blocking conflicts in a non-adversarial row, fail fast or require an explicit override that is recorded in metadata.

---

## Step 5 - Eval Runner Artifacts

Update the eval runner so AU baseline runs include:

- Run metadata that identifies the AU benchmark version.
- Shared context bundle artifact, for example `shared-context-bundle.json`.
- Per-case references from metric rows or companion artifacts to shared context section IDs/hashes.
- Deterministic AU check results.
- Complete generated definitions as currently supported by the runner.

Current-state baseline run label:

```text
story-6.4.6-au-baseline-current
```

Do not enable any candidate prompt improvement flags.

---

## Step 6 - Judge Package Diagnostics

Update `judge_pack.py`, judge prompts, `judge-output-template.json`, and `judge_ingest.py` so the judge package includes:

- Shared context bundle references.
- Per-case user prompt, output, expected AU signals, deterministic AU findings, and section references.
- Diagnostic output fields for:
  - `conflicting_data_exists`
  - `conflict_description`
  - `likely_responsible_section_ids`
  - `suggested_correction`
  - `confidence`

Keep existing metric score/rationale validation. Add tests that fail if the diagnostic fields are missing.

---

## Step 7 - Focused Tests

Run focused tests before the live baseline. Adjust the exact file list to match implementation, but include all touched eval/judge paths:

```powershell
python -m pytest `
  backend/tests/test_form_ai_eval_harness.py `
  backend/tests/test_form_ai_eval_locale_filter.py `
  backend/tests/test_judge_pack.py `
  backend/tests/test_judge_ingest.py `
  backend/tests/test_eval_diff.py `
  --tb=short
```

Record exact summaries in `STORY-6.4.6-GATE-EVIDENCE.md`.

---

## Step 8 - AU Baseline Run

Run the current-state AU baseline. Use the final prompt file path and CLI flags from your implementation.

Expected shape:

```powershell
python -m backend.tests.form_ai_eval.run `
  --prompts-path backend/tests/form_ai_eval/prompts_au_v1.yaml `
  --variant baseline `
  --hypothesis-code baseline `
  --variant-label story-6.4.6-au-baseline-current `
  --run-id story-6.4.6-au-baseline-current
```

If the run must be sliced or resumed, keep the final aggregate run ID traceable and document every source run.

---

## Step 9 - Judge Package + Tony Judge Sessions

Generate the judge package:

```powershell
python -m backend.tests.form_ai_eval.judge_pack `
  _bmad-output/eval-runs/story-6.4.6-au-baseline-current `
  --use-db
```

Confirm the package includes:

- `shared-context-bundle.json`
- `judge-input-batch.md`
- `judge-output-template.json`
- `judge-package-metadata.json`
- `judge-prompt-claude.md`
- `judge-prompt-grok.md`
- `judge-prompt-gpt5mini.md`
- `results/`

Send Tony the three judge prompt paths. After Tony saves the outputs to the embedded paths, ingest:

```powershell
python -m backend.tests.form_ai_eval.judge_ingest `
  _bmad-output/eval-runs/story-6.4.6-au-baseline-current/judge-package
```

Record output paths and diagnostic summaries in `STORY-6.4.6-AU-BASELINE-EVIDENCE.md`.

---

## Step 10 - Tracking Sheet

Update `docs/stories/STORY-6-AU-EVAL-ITERATION-TRACKING.md` row `AU-000`.

For baseline:

- `Baseline run ID` = `story-6.4.6-au-baseline-current`.
- `Candidate run ID` = `N/A`.
- `Prompt/context section changed` = `N/A`.
- `Decision` = `baseline`.
- Include judge conflict findings, deterministic AU failures, and evidence links.

Do not add candidate prompt changes.

---

## Step 11 - Green Gate

Run focused and backend regression gates:

```powershell
python -m pytest `
  backend/tests/test_form_ai_eval_harness.py `
  backend/tests/test_form_ai_eval_locale_filter.py `
  backend/tests/test_judge_pack.py `
  backend/tests/test_judge_ingest.py `
  backend/tests/test_eval_diff.py `
  --tb=short

python -m pytest backend/tests --tb=short
```

Frontend checks are required only if frontend files are touched:

```powershell
cd frontend
npm run lint
npm run test:unit -- --watch=false
```

Record exact final summaries in `STORY-6.4.6-GATE-EVIDENCE.md`.

---

## Step 12 - Closeout

Before merge:

1. Fill `STORY-6.4.6-AU-BASELINE-EVIDENCE.md`.
2. Fill `STORY-6.4.6-GATE-EVIDENCE.md`.
3. Fill `STORY-6.4.6-UAT-RESULTS.md`.
4. Fill `STORY-6.4.6-CLOSEOUT-REPORT.md`.
5. Update `story-6.4.6.md`, `EPIC-6-STATUS.md`, and `EPIC-6-WORKFLOW-GUIDE.md`.
6. Run the SM stale-field audit before merge.

Expected next-story routing:

- Clean framework + baseline closeout -> Story 6.4.7 Analyst loop.
- Framework blocker -> smallest Dev-owned fix story before 6.4.7.
