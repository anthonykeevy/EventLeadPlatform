# Form AI Eval Harness

Story 6.4.4.1 bumps the harness to `prompts-v1.1` for locale-registry validation. It freezes 270 cells (15 prompt scenarios x 6 audience locales x 3 prompt variants), runs baseline generations through the existing Form AI service path, captures Category A structural metrics, writes local artifacts, and can optionally persist rows to `log.FormAiEvalRun` after Anthony applies the migration.

Story 6.4.6 adds an AU-only diagnostic benchmark, `prompts-au-v1`, at `backend/tests/form_ai_eval/prompts_au_v1.yaml`. AU runs write shared prompt-context and deterministic AU diagnostic artifacts alongside the existing metrics.

## Architecture And Data Flow

```text
backend/tests/form_ai_eval/prompts.yaml
  -> backend/tests/form_ai_eval/run.py
  -> modules.form_ai.service.generate_form_definition(...)
  -> Category A metrics extraction
  -> _bmad-output/eval-runs/<run-id>/{metrics.jsonl,summary.csv,run-metadata.json}
  -> optional log.FormAiEvalRun row per prompt x repetition
```

The runner calls `modules.form_ai.service.generate_form_definition(...)` directly. That preserves the current generation stack, including prompt assembly, capability filtering, deterministic compiler validation, and `dbo.GenerationRun` persistence when a DB session is supplied. No new production API or duplicated generation logic is introduced.

`prompts.yaml` is intentionally JSON-shaped YAML so it remains dependency-free in the backend test environment. The loader validates `prompts-v1.1`, exactly 270 prompt rows, stable IDs, `audience_locale`, prompt variant metadata, frozen `runtimeContext.canvas`, `runtimeContext.termsDefaults`, `runtimeContext.audienceLocale`, `runtimeContext.capabilitySnapshot.version`, `expected_signals`, and `llm_judge_focus`.

`prompts_au_v1.yaml` follows the same JSON-shaped YAML convention. It contains AU-only rows and adds diagnostic metadata for source-market adaptation tracking.

## Analyst Iteration Model

Story 6.4.6 builds the harness and captures the current-state baseline. Story 6.4.7 uses the same harness as the Analyst's prompt-improvement loop. In that loop, the Analyst should not need to change code or run bespoke tools; the Analyst supplies the hypothesis and candidate prompt/context changes, while the harness executes repeatable runs, packages judge inputs, and preserves evidence.

Keep these concepts separate:

- **Frozen baseline:** immutable run against the agreed benchmark rows, current production prompt/context state, fixed rubric, and fixed scoring method.
- **Scenario set:** stable prompt rows such as `p01` through `p15`; these are the row keys used for baseline-to-candidate comparison.
- **Experiment variant:** a candidate prompt/context change being tested, such as `candidate-a`, `candidate-b`, or `candidate-c`.
- **Locale stress variant:** rows such as `neutral`, `ambiguous`, and `adversarial`; these are useful when the improvement target is locale robustness, but they are not the only valid experiment dimension.

For Analyst iterations, prefer this flow:

1. Select the improvement target and primary metrics, for example `field_coverage_recall`, `validation_intent_accuracy`, `row_group_agreement`, or `copy_quality_score`.
2. Choose a stable scenario slice. Use all 15 base scenarios for a formal candidate check, or a smaller representative slice for low-cost exploration.
3. Define up to three candidate prompt/context changes. Change one experiment dimension at a time.
4. Run each candidate against the same scenario slice and compare it to the frozen baseline row-by-row.
5. Promote a candidate to the new baseline only at an explicit gate after deterministic checks, judge scoring, and Tony/SM review.

The `variant` and `variant_label` fields identify the experiment arm for the run; they should not be overloaded to mean "the baseline changed." Baseline runs remain stable controls, while candidate variants are temporary trial arms.

Recommended labels:

```text
baseline run:   story-6.4.6-au-baseline-current
experiment id:  story-6.4.7-validation-intent-r1
candidate runs: story-6.4.7-validation-intent-r1-candidate-a
                story-6.4.7-validation-intent-r1-candidate-b
                story-6.4.7-validation-intent-r1-candidate-c
variant labels: candidate-a | candidate-b | candidate-c
hypothesis:     improve-validation-intent
```

## Analyst Experiment Runner

The harness supports Analyst-authored prompt experiments through a JSON-shaped config, without requiring the Analyst to edit Python or production service code. The config captures:

- `experiment_id`
- `baseline_run_id`
- `improvement_goal`
- `target_metrics`
- selected `prompt_id` rows or named scenario slice
- candidate labels and hypotheses
- the prompt/context section being changed
- the exact candidate prompt/context text or file path
- expected metric movement and known risk metrics

Run an experiment with:

```powershell
python -m backend.tests.form_ai_eval.experiment docs/stories/examples/analyst-experiment.example.json
```

Example config shape:

```json
{
  "experiment_id": "story-6.4.7-validation-intent-r1",
  "baseline_run_id": "story-6.4.6-au-baseline-current",
  "improvement_goal": "improve-validation-intent",
  "target_metrics": ["validation_intent_accuracy", "field_coverage_recall"],
  "prompts_path": "backend/tests/form_ai_eval/prompts_au_v1.yaml",
  "scenario_slice": "au-neutral",
  "concurrency": 4,
  "candidates": [
    {
      "label": "candidate-a",
      "hypothesis": "Make validation intent explicit.",
      "changed_section_id": "candidate_prompt_block",
      "system_prompt_addendum": "Eval-only candidate text..."
    },
    {
      "label": "candidate-b",
      "hypothesis": "Make required-field rules explicit.",
      "changed_section_id": "candidate_prompt_block",
      "system_prompt_addendum_file": "docs/stories/experiments/candidate-b.md"
    }
  ]
}
```

Each candidate run records the effective experiment metadata in `run-metadata.json`, includes the changed prompt/context section in `shared-context-bundle.json`, and preserves hashes so a judge can see what changed. Candidate overlays are passed as `system_prompt_addendum` and are eval-only; they do not mutate production prompt state.

Use either explicit `prompt_ids` or a named `scenario_slice`. Supported slices are `all`, `au-all`, `au-neutral`, `au-ambiguous`, and `au-adversarial`; explicit `prompt_ids` take precedence.

The experiment runner produces, for each experiment:

- one immutable run folder per candidate arm,
- deterministic structural/runtime metrics,
- AU deterministic findings when using the AU benchmark,
- one judge package and `judge-input-batch.md` per candidate arm,
- judge packages with experiment goal and changed-section context,
- diff/comparison artifacts against the frozen baseline,
- a tracking-row payload suitable for `docs/stories/STORY-6-AU-EVAL-ITERATION-TRACKING.md`.

Default output structure:

```text
_bmad-output/eval-runs/<experiment_id>/
  experiment-summary.json
  tracking-row-payload.json
  tracking-row-payload.md
  candidate-a/
    metrics.jsonl
    summary.csv
    run-metadata.json
    shared-context-bundle.json
    judge-package/
      judge-input-batch.md
      judge-output-template.json
      results/
  candidate-b/
    ...
  diffs/
    candidate-a/
      diff-summary.json
      diff-details.csv
      diff-report.md
```

## AU Diagnostic Baseline

Smoke the framework without live LLM calls:

```powershell
python -m backend.tests.form_ai_eval.run `
  --prompts-path backend/tests/form_ai_eval/prompts_au_v1.yaml `
  --variant baseline `
  --hypothesis-code baseline `
  --variant-label story-6.4.6-au-baseline-current-smoke `
  --run-id story-6.4.6-au-baseline-current-smoke `
  --mock
```

Run the live current-state AU baseline only after cost/environment approval:

```powershell
python -m backend.tests.form_ai_eval.run `
  --prompts-path backend/tests/form_ai_eval/prompts_au_v1.yaml `
  --variant baseline `
  --hypothesis-code baseline `
  --variant-label story-6.4.6-au-baseline-current `
  --run-id story-6.4.6-au-baseline-current `
  --concurrency 4
```

AU runs produce:

- `shared-context-bundle.json`
- `prompt-context-lint.json` / `prompt-context-lint.md`
- `au-deterministic-checks.json` / `au-deterministic-checks.md`

## Smoke Baseline

Use the deterministic mock path when live LLM access is unavailable or when only harness plumbing needs verification:

```powershell
python -m backend.tests.form_ai_eval.run --variant baseline --hypothesis-code baseline --repetitions 1 --max-cost-usd 1 --mock
```

This writes the same artifact shape as a live run but uses local synthetic responses. It does not prove prompt quality.

## Formal Baseline

After environment access and cost approval are confirmed, run the live service path:

```powershell
python -m backend.tests.form_ai_eval.run --variant baseline --hypothesis-code baseline --variant-label current-master-baseline --repetitions 5 --max-cost-usd 1
```

`prompts-v1.1` rows carry locale and prompt variant dimensions inside the prompt file. Use `--prompt-id` to run a narrow cell, or omit it for the full 270-cell pass.

## Prompt Selection

Run a subset by repeating `--prompt-id`:

```powershell
python -m backend.tests.form_ai_eval.run --variant baseline --hypothesis-code baseline --prompt-id p-03-survey-nps --repetitions 1 --max-cost-usd 1 --mock
```

Unknown prompt IDs fail fast.

Run a locale slice with `--locale-filter`. This is the AC-10 path for parallel baseline execution; each locale writes a non-overlapping run folder:

```powershell
python -m backend.tests.form_ai_eval.run `
  --locale-filter AU `
  --variant rubric-v2-baseline-AU `
  --run-id story-6.4.4.1-ac10-baseline-AU
```

When `--locale-filter` is set and `--run-id` is omitted, the runner uses the locale-suffixed variant as the run id.

## Checkpoint And Resume

The runner writes `_bmad-output/eval-runs/<run-id>/checkpoint.json` when it halts because of a cost cap or error. Resume by pointing at that checkpoint:

```powershell
python -m backend.tests.form_ai_eval.run --variant baseline --hypothesis-code baseline --run-id <same-run-id> --resume _bmad-output/eval-runs/<same-run-id>/checkpoint.json
```

Completed prompt/repetition keys are skipped on resume.

The runner is durable at prompt/repetition granularity. After each completed generation it rewrites `metrics.jsonl`, `summary.csv`, `run-metadata.json`, and `checkpoint.json`. If `--persist-db` is enabled, it also commits that `log.FormAiEvalRun` row immediately. If prompt 7 fails, rows 1-6 remain on disk and committed, and the checkpoint records the completed keys.

The runner refuses to write to a non-empty run folder unless `--resume` is supplied or `--overwrite-existing` is passed explicitly. Use a new immutable `--run-id` for every analyst iteration.

## Concurrency And Progress

`--concurrency` is native runner concurrency, capped at 4. The runner uses an in-process thread pool, submits up to the requested number of pending rows, and logs row submission/completion progress to stderr. Each `metrics.jsonl` row includes `started_at_utc`, `completed_at_utc`, and `eval_sequence`, so wall-clock overlap can be audited without relying on folder timestamps.

When `--persist-db` is enabled, the runner intentionally uses serial execution because the generation service DB session is not thread-safe. `run-metadata.json` records both `concurrency_cap` and `concurrency_effective`.

## Cost Cap And Retry

`--max-cost-usd` halts the sweep once accumulated captured cost reaches the cap and records a checkpoint. The Form AI service now surfaces OpenAI usage metadata in `FormAiGenerateResponse.meta.provider_usage` when the provider returns it, and the runner maps that into `input_tokens` and `output_tokens`. OpenAI does not return cost, so `total_cost_usd` remains `0` unless an explicit pricing layer is added later; `run-metadata.json` records `token_cost_status`.

Provider 429/5xx exceptions are retried with jitter up to 3 retries.

## DB Persistence

The migration `backend/migrations/versions/062_story_643a_form_ai_eval_run.py` creates `log.FormAiEvalRun`. The runner inserts one row per prompt x repetition when `--persist-db` is supplied and the migration has been applied by Anthony:

```powershell
python -m backend.tests.form_ai_eval.run --variant baseline --hypothesis-code baseline --repetitions 1 --max-cost-usd 1 --persist-db
```

The table stores `MetricsJSON` as a structured blob with `category_a`, `category_b`, and `category_c` slots. Category B/C remain `null` in this story. `GenerationRunID` maps to the current `dbo.GenerationRun.GenerationRunID` table; no `form_ai.GenerationRun` schema exists in the current migration chain. Rows are committed after each completed prompt/repetition so late-run failures do not roll back earlier eval evidence.

Anthony applies the migration; agents must not run Alembic upgrade/downgrade/revision commands.

## PII-Adjacent Handling

The prompt rows use synthetic contexts and example URLs only, but generated definitions can contain realistic names, emails, dates, or contact fields. Treat eval artifacts as PII-adjacent:

- Keep raw outputs in `_bmad-output/eval-runs/`.
- Do not paste raw generated definitions into chat or external systems.
- Share summaries and aggregate metrics by default.

## Future Extension Points

Judge packages use `rubric_v2.md` and require Claude + Grok primary outputs plus optional GPT-5 mini control output. Each judge JSON must include `judge_model_version`; ingest computes the primary mean from Claude + Grok and records GPT-5 mini bias deltas when present.

Story 6.4.3c adds diff/statistics tooling, including Welch/Fisher tests and comparison reports.

Prompt shrink and capability snapshot experiments must run through this harness after the baseline is captured.

## Harness Readiness Status

The Analyst prompt-improvement loop is implemented for eval-only prompt/context overlays through `backend.tests.form_ai_eval.experiment`.

Acceptance checks now covered by automated tests:

- A mock experiment can run candidate A/B against a small prompt slice without live LLM calls.
- Candidate run metadata distinguishes baseline, experiment id, candidate label, target metrics, changed section, and overlay hash.
- `shared-context-bundle.json` includes an active `candidate_prompt_block` for candidate overlays.
- Each candidate arm gets its own `judge-package/judge-input-batch.md`.
- Candidate diff outputs are generated against the frozen baseline when the baseline folder is available.
- A tracking-row payload is written for `docs/stories/STORY-6-AU-EVAL-ITERATION-TRACKING.md`.
