# Form AI Eval Harness

Story 6.4.4.1 bumps the harness to `prompts-v1.1` for locale-registry validation. It freezes 270 cells (15 prompt scenarios x 6 audience locales x 3 prompt variants), runs baseline generations through the existing Form AI service path, captures Category A structural metrics, writes local artifacts, and can optionally persist rows to `log.FormAiEvalRun` after Anthony applies the migration.

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

The runner is durable at prompt/repetition granularity. After each completed generation it rewrites `metrics.jsonl`, `summary.csv`, and `run-metadata.json`. If `--persist-db` is enabled, it also commits that `log.FormAiEvalRun` row immediately. If prompt 7 fails, rows 1-6 remain on disk and committed, and the checkpoint records the completed keys.

## Cost Cap And Retry

`--max-cost-usd` halts the sweep once accumulated captured cost reaches the cap and records a checkpoint. Story 6.4.3a currently records token and cost fields as `0` when the existing service response does not expose provider usage. The fields are present so later stories can enrich them without changing the artifact or DB schema.

Provider 429/5xx exceptions are retried with jitter up to 3 retries. The CLI enforces a concurrency cap of 4 via `--concurrency` validation; this story runs the baseline loop conservatively while preserving the cap in metadata.

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
