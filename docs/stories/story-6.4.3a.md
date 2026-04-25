# Story 6.4.3a — AI Eval Harness Bones

**Epic:** 6 — AI Generation & Monetization Engine  
**Story ID:** 6.4.3a  
**Title:** AI Eval Harness Bones  
**Status:** Draft — ready for Dev  
**Branch:** `story/epic6-6.4.3a-ai-eval-harness-bones`  
**PR:** [#68](https://github.com/anthonykeevy/EventLeadPlatform/pull/68) — Draft  
**Created:** 2026-04-25  
**Depends On:** Story 6.4 complete; Epic 6 prompt engineering ideation brief v2 approved  
**Unblocks:** 6.4.2, 6.4.3b, 6.4.3c, 6.4.4 prompt shrink sweeps

---

## 1) Goal

Create the minimum reliable evaluation harness foundation for Form AI prompt experiments before any prompt shrink or capability mutation work begins.

This story does **not** judge semantic quality yet. It freezes the benchmark rows, captures repeatable structural baseline runs, stores run metrics in `log.FormAiEvalRun`, and gives Dev/SM/Human a concrete baseline artifact that later stories can compare against.

Story 6.4.3a exists because 6.4.2 must prove "zero behavioural change" after orphan prompt deletion and always-pass capability snapshot changes. The harness must therefore land first.

---

## 2) In Scope

### 2.1 Frozen benchmark prompt set

Create `backend/tests/form_ai_eval/prompts.yaml` with exactly 10 canonical benchmark rows:

1. Event registration / conference
2. Lead-gen / SaaS demo request
3. Survey / NPS + open comment
4. Waiver / gym membership
5. RSVP / wedding
6. Feedback / post-event
7. Booking / consultation
8. Onboarding / new employee
9. Application / scholarship
10. Donation / charity

Each row must include:

- stable `prompt_id`
- category/richness metadata
- prompt text
- frozen `runtimeContext` fixture data: canvas size, terms defaults, capability snapshot version/input
- expected deterministic structural checks to report, not to force-fit

Mutation rule: changing `prompts.yaml` after this story requires an ADR or an explicit future-story artifact. The initial benchmark version is `prompts-v1.0`.

### 2.2 CLI runner

Create `backend/tests/form_ai_eval/run.py` as a local/dev harness runner that can:

- select all prompts or a subset by `--prompt-id`
- run `--variant baseline` for this story
- run `--hypothesis-code baseline`
- control repetitions with `--repetitions` (default 1 for smoke; documented 5/10 for formal sweeps)
- cap concurrency at 4
- accept `--max-cost-usd`
- retry 429/5xx with jitter, max 3 retries
- write a checkpoint file when halted by cost/error
- resume from checkpoint
- emit JSONL/CSV summary files under `_bmad-output/eval-runs/<run-id>/`
- optionally persist run rows to `log.FormAiEvalRun`

The runner should call the existing Form AI service path as directly as practical, without creating a second production API. If a direct service call would over-couple to runtime dependencies, Dev may use the existing API client path, but must document the choice in `docs/FORM-AI-EVAL-HARNESS.md`.

### 2.3 Eval storage migration

Add a migration for `log.FormAiEvalRun` as the first-class eval run table, separate from `log.ApiRequest`.

Required logical schema:

| Column | Requirement |
|--------|-------------|
| `EvalRunID` | BigInt identity primary key |
| `BenchmarkSetVersion` | `"prompts-v1.0"` for this story |
| `HypothesisCode` | `"baseline"` for this story |
| `VariantLabel` | e.g. `"current-master-baseline"` |
| `PromptID` | matches `prompts.yaml` |
| `RepetitionIndex` | 1-based |
| `GenerationRunID` | nullable FK to `form_ai.GenerationRun` if available in current schema |
| `MetricsJSON` | structured metrics blob |
| `JudgeRubricVersion` | nullable; unused until 6.4.3b |
| `JudgeAgreementScore` | nullable; unused until 6.4.3b |
| `BiasDeltaJSON` | nullable; unused until 6.4.3b |
| `BaselineExpiresAt` | 30 days after creation for baseline drift awareness |
| `CreatedDate` | UTC default |

Required index: `(HypothesisCode, VariantLabel, PromptID)`.

Do **not** run Alembic from the agent shell. Anthony applies migrations.

### 2.4 Structural metrics

For each generation, capture Category A metrics:

- `schema_valid`
- `component_count`
- `collision_count`
- `boundary_violation_count`
- `attempt_count`
- `terminal_reason`
- `failure_class`
- `duration_ms`
- `input_tokens`
- `output_tokens`
- `total_cost_usd`
- `retry_count`

Category B/C judge-scored metrics are placeholders only in this story. The JSON shape should tolerate later enrichment by 6.4.3b/6.4.3c without a schema migration.

### 2.5 Baseline snapshot artifact

Create `docs/stories/STORY-6.4.3a-BENCHMARK-BASELINE.md` as the required baseline artifact.

It must document:

- command(s) used
- benchmark version
- git SHA
- model/config snapshot used for generation
- prompt IDs included
- repetition count
- output folder
- DB persistence status
- summary of structural metrics
- known limitations before judge scoring exists

### 2.6 Harness docs and tests

Create `docs/FORM-AI-EVAL-HARNESS.md` covering:

- architecture and data flow
- how to run a smoke baseline
- how to run a formal baseline
- how checkpoint/resume works
- cost-cap behavior
- PII-adjacent data handling
- how later stories add judge packages and diff/statistics

Add focused backend tests, expected home `backend/tests/test_form_ai_eval_harness.py`, covering:

- prompt YAML loading and required fields
- runtimeContext freeze shape
- CLI argument parsing
- checkpoint write/resume behavior
- metrics JSON shape
- DB persistence mapping for `FormAiEvalRun` where practical without requiring live LLM calls

---

## 3) Out of Scope

| Item | Reason |
|------|--------|
| Prompt shrink changes H1/H2/H4 | Story 6.4.4 after harness + 6.4.2/6.4.3b/6.4.3c land |
| Orphan prompt deletion / always-pass capability snapshot | Story 6.4.2 |
| Judge package generation | Story 6.4.3b |
| Rubric, judge JSON ingest, cross-model scoring | Story 6.4.3b |
| Welch/Fisher statistics and diff tool | Story 6.4.3c |
| CI PR-comment integration | Future story after diff output exists |
| Human semantic UAT for prompt quality | Not meaningful until 6.4.3b judge workflow exists |

---

## 4) Acceptance Criteria

1. **AC-1 Benchmark YAML exists:** `backend/tests/form_ai_eval/prompts.yaml` contains exactly 10 canonical prompt rows from the ideation brief, with stable IDs, metadata, prompt text, and frozen `runtimeContext` data. Tests fail if required fields are missing.
2. **AC-2 Benchmark version is explicit:** The harness reports `BenchmarkSetVersion = "prompts-v1.0"` for every 6.4.3a run. The docs state that prompt-row mutation requires ADR/future-story approval.
3. **AC-3 CLI runner smoke path works:** `python -m backend.tests.form_ai_eval.run --variant baseline --hypothesis-code baseline --repetitions 1 --max-cost-usd 1` or the documented equivalent runs a smoke baseline or a deterministic mocked test path without requiring judge artifacts.
4. **AC-4 Production-safety controls exist:** The runner enforces concurrency cap 4, retry-with-jitter max 3 retries, `--max-cost-usd`, checkpoint-on-halt, and resume from checkpoint.
5. **AC-5 Metrics shape captured:** Every completed run emits Category A metrics with the fields listed in §2.4 and stores them in output JSONL/CSV summary files.
6. **AC-6 Eval table migration prepared:** A reversible migration creates `log.FormAiEvalRun` with required columns and index. Migration is not executed by the agent.
7. **AC-7 DB persistence path works:** When persistence is enabled and migration has been applied by Anthony, the runner inserts one `log.FormAiEvalRun` row per prompt × repetition with `BaselineExpiresAt = CreatedDate + 30 days` for baseline runs.
8. **AC-8 Baseline artifact exists:** `STORY-6.4.3a-BENCHMARK-BASELINE.md` is completed with run command, SHA, output folder, structural summary, and limitations.
9. **AC-9 Harness documentation exists:** `docs/FORM-AI-EVAL-HARNESS.md` explains smoke/formal runs, checkpoint/resume, cost caps, PII-adjacent handling, and later extension points.
10. **AC-10 Automated tests cover the harness bones:** Focused tests cover YAML loading, CLI parsing, checkpoint/resume, metrics shape, and DB mapping. No live LLM call is required in unit tests.
11. **AC-11 No judge scope leaks:** No rubric, judge package generator, Cursor judge workflow, semantic scoring, or statistics module is implemented in this story except nullable placeholders needed for later persistence.
12. **AC-12 Required story pack artifacts exist:** `story-context-6.4.3a.xml`, `STORY-6.4.3a-UAT-TEST-GUIDE.md`, `STORY-6.4.3a-SINGLE-SESSION-DEV-PROMPT.md`, `STORY-6.4.3a-BENCHMARK-BASELINE.md`, and `STORY-6.4.3a-CLOSEOUT-REPORT.md` exist.

---

## 5) Definition of Done

- All ACs have evidence in `STORY-6.4.3a-GATE-EVIDENCE.md`.
- Backend focused tests pass.
- Full backend test gate is run unless Dev records a clear risk-based reason and CI covers the remainder.
- Migration file is prepared but not applied by the agent; Anthony runs migration before DB-backed UAT.
- Draft PR remains scoped to harness bones.
- `STORY-6.4.3a-CLOSEOUT-REPORT.md` is completed before merge because this story ships a schema migration and defers judge/statistics scope.
