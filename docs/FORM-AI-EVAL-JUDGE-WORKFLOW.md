# Form AI Eval Judge Workflow

Story 6.4.3b adds the manual judge layer on top of the 6.4.3a eval harness. It does not call judge model APIs. Anthony runs the judge chats in Cursor, saves JSON files, and the ingest tool validates and aggregates them.

## Inputs

- Eval run folder: `_bmad-output/eval-runs/<run-id>/`
- Preferred current input: `_bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline/`
- Rubric: `backend/tests/form_ai_eval/rubric_v1.md`
- Package generator: `backend/tests/form_ai_eval/judge_pack.py`
- Ingest tool: `backend/tests/form_ai_eval/judge_ingest.py`

The 6.4.3a local metrics artifact stores `GenerationRunID` but not full generated definitions. For real live runs, use `--use-db` so the package can load `final-definition` artifacts from `dbo.GenerationArtifact`.

## Generate A Judge Package

From the worktree root:

```powershell
python -m backend.tests.form_ai_eval.judge_pack _bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline --use-db
```

Expected output:

```text
_bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline/judge-package/
├── rubric_v1.md
├── judge-input-batch.md
├── judge-output-template.json
├── judge-package-metadata.json
└── results/
```

If DB access is unavailable, the generator still creates the package and marks generated definitions as unavailable. That path is useful for plumbing tests, but semantic judging needs generated definition content.

For Story 6.4.4.1 AC-10, six locale-sliced runs are combined into one judge package with `--inputs`:

```powershell
python -m backend.tests.form_ai_eval.judge_pack `
  _bmad-output/eval-runs/story-6.4.4.1-ac10-baseline `
  --inputs story-6.4.4.1-ac10-baseline-AU,story-6.4.4.1-ac10-baseline-NZ,story-6.4.4.1-ac10-baseline-UK,story-6.4.4.1-ac10-baseline-US,story-6.4.4.1-ac10-baseline-INTL_ONLINE,story-6.4.4.1-ac10-baseline-EU `
  --use-db
```

The package includes `judge-prompt-claude.md`, `judge-prompt-grok.md`, and `judge-prompt-gpt5mini.md`. Each prompt embeds the exact `results/judge-output-*.json` path the Cursor judge must write.

For Story 6.4.6 AU diagnostic runs, generate the package with the AU prompt set:

```powershell
python -m backend.tests.form_ai_eval.judge_pack `
  _bmad-output/eval-runs/story-6.4.6-au-baseline-current `
  --prompts-path backend/tests/form_ai_eval/prompts_au_v1.yaml `
  --use-db
```

The AU package includes `shared-context-bundle.json` and row-level references to prompt/context section IDs, deterministic AU findings, expected AU signals, and generated definitions.

For Story 6.4.6, the judge input/output surface is:

- Model input prompt: `_bmad-output/eval-runs/<run-id>/metrics.jsonl` field `user_prompt`
- Model assembled context references: `_bmad-output/eval-runs/<run-id>/shared-context-bundle.json`, with per-row section refs in `metrics.jsonl` field `prompt_context_section_refs`
- Model output: `_bmad-output/eval-runs/<run-id>/metrics.jsonl` field `generated_definition`
- Scrubbed judge-facing bundle: `_bmad-output/eval-runs/<run-id>/judge-package/judge-input-batch.md`
- Judge shared context copy: `_bmad-output/eval-runs/<run-id>/judge-package/shared-context-bundle.json`
- Judge JSON destination: `_bmad-output/eval-runs/<run-id>/judge-package/results/judge-output-<model>.json`

## Experiment-Aware Judge Context

For Story 6.4.7 Analyst iterations, judge packages should include experiment metadata in addition to the generated form output:

- `experiment_id`
- `baseline_run_id`
- candidate `variant_label`
- `improvement_goal`
- `target_metrics`
- changed prompt/context section name
- changed prompt/context text or a scrubbed excerpt
- Analyst hypothesis and expected metric movement

Judges must score each row absolutely against `rubric_v2` before using the experiment goal for feedback. The score should be based on the visible user prompt, expected signals, generated definition, and rubric anchors only. Do not inflate or deflate any metric because a candidate was intended to improve it.

When experiment metadata is present, ask judges to:

- score every Category B metric normally before writing targeted feedback,
- keep the primary rationale evidence-based and tied to the rubric,
- use the listed `target_metrics` only to make the post-score feedback more useful,
- identify whether the generated definition shows the intended improvement after scoring,
- call out regressions in non-target metrics,
- use `suggested_correction` to recommend a prompt/context adjustment tied to the changed section where possible.

If a package contains multiple candidate arms, the row scores remain absolute per row. Candidate selection should be made by ingest/diff tooling and Tony/SM review, not by asking a judge to choose a winner informally.

## Run The Three Cursor Judge Chats

Create three separate Cursor chats. In each chat, provide:

1. `rubric_v1.md`
2. `judge-input-batch.md`
3. `judge-output-template.json`

Use these model roles:

- GPT-5 mini: control judge, saved as `results/judge-output-gpt5mini.json`
- Claude: primary judge, saved as `results/judge-output-claude.json`
- Gemini: primary judge, saved as `results/judge-output-gemini.json`

Ask each judge to return only valid JSON matching the template. Do not ask judges to compare against each other.

For `rubric_v2`, each row must also include diagnostic fields:

- `conflicting_data_exists`
- `conflict_description`
- `likely_responsible_section_ids`
- `suggested_correction`
- `confidence`

## Ingest Judge Results

After saving the three JSON files:

```powershell
python -m backend.tests.form_ai_eval.judge_ingest _bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline/judge-package
```

This writes:

- `judge-ingest-summary.json`
- `judge-ingest-summary.csv`

To update nullable judge fields on `log.FormAiEvalRun`:

```powershell
python -m backend.tests.form_ai_eval.judge_ingest _bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline/judge-package --persist-db
```

The ingest updates:

- `JudgeRubricVersion`
- `JudgeAgreementScore`
- `BiasDeltaJSON`

## Validation Rules

Ingest fails before writing DB updates when any judge file has:

- missing rows,
- duplicate rows,
- unknown row IDs,
- malformed metric keys,
- non-numeric scores,
- scores outside `0..5`,
- a wrong `rubric_version`,
- a `judge_model` that does not match the result filename.

Claude and Gemini are required because their mean is the primary score. GPT-5 mini is a control; its bias deltas are recorded when present.

## Disagreement Handling

The ingest computes `JudgeAgreementScore` per row from Claude/Gemini distance. Low agreement does not choose a winner in 6.4.3b. It flags rows for Anthony/SM review and for the 6.4.3c statistics/diff layer.

Recommended handling:

- Agreement near `1.0`: judges are aligned.
- Agreement around `0.6`: inspect rationales before using the row as decisive evidence.
- Agreement below `0.5`: treat the row as ambiguous and carry it into 6.4.3c review notes.

## PII-Adjacent Handling

Generated definitions can contain realistic synthetic contact values. The package generator scrubs obvious emails, phone numbers, date-like values, and common synthetic full names. Field labels such as "First name" are preserved so semantic judging remains possible.

Do not paste raw DB artifacts into chat. Use `judge-input-batch.md`, which is the scrubbed judge input surface.

## Out Of Scope Until 6.4.3c

- Welch/Fisher statistical tests.
- Diff reports.
- PR comment automation.
- Declaring a prompt variant winner.
- Live judge API clients or new model secrets.
