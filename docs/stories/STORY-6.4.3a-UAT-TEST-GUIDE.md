# Story 6.4.3a — UAT Test Guide

**Story:** 6.4.3a — AI Eval Harness Bones  
**Owner:** Anthony (Human UAT)  
**Prep:** Dev provides `STORY-6.4.3a-GATE-EVIDENCE.md`, completed `STORY-6.4.3a-BENCHMARK-BASELINE.md`, and Draft PR link  
**Protocol:** Harness validation replaces prompt-quality UAT for this story. Semantic judging begins in 6.4.3b.

---

## Environment

- Branch: `story/epic6-6.4.3a-ai-eval-harness-bones`
- Worktree: `C:\wt\elp\story-epic6-6.4.3a-ai-eval-harness-bones`
- Backend: local API/DB as usual
- Migrations: Anthony applies the `log.FormAiEvalRun` migration before DB-persistence UAT
- LLM: optional for smoke baseline; unit tests must not require live LLM calls

---

## §1 — Automated Gates Witness

| Step | Command | Expected |
|------|---------|----------|
| 1.1 | From repo root: `.\scripts\workflow\preflight-story.ps1 -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.4.3a-ai-eval-harness-bones" -ExpectedBranch "story/epic6-6.4.3a-ai-eval-harness-bones" -ReportFile "docs/stories/STORY-6.4.3a-PREFLIGHT.md"` | Pass; branch/worktree and DB resolution evidence captured. |
| 1.2 | Focused backend tests, exact command chosen by Dev | Pass; includes prompt YAML loading, CLI parsing, checkpoint/resume, metrics shape, DB mapping. |
| 1.3 | Backend gate via `.\scripts\workflow\run-green-gate.ps1` or documented equivalent | Pass or explicit CI-backed gap recorded in gate evidence. |
| 1.4 | Migration file inspection | One reversible migration creates `log.FormAiEvalRun`; no Alembic command was run by the agent. |

Record final command summaries in `STORY-6.4.3a-GATE-EVIDENCE.md`.

---

## §2 — Benchmark Set Verification

| Step | Action | Expected |
|------|--------|----------|
| 2.1 | Open `backend/tests/form_ai_eval/prompts.yaml` | Exactly 10 prompt rows exist. |
| 2.2 | Inspect each row | Stable `prompt_id`, prompt text, metadata, and frozen `runtimeContext` exist. |
| 2.3 | Confirm benchmark version | Harness and docs use `prompts-v1.0`. |
| 2.4 | Run the prompt-loader test | Test fails if a required field is removed. |

---

## §3 — Runner Smoke Verification

| Step | Action | Expected |
|------|--------|----------|
| 3.1 | Run the documented smoke command with `--repetitions 1` and a low `--max-cost-usd` | Runner starts, selects baseline variant, and writes output under `_bmad-output/eval-runs/<run-id>/`. |
| 3.2 | Run with `--prompt-id` for one benchmark row | Only that prompt row runs. |
| 3.3 | Force or simulate a checkpoint halt | Checkpoint file is written and contains enough state to resume. |
| 3.4 | Resume from checkpoint | Already completed rows are skipped; remaining rows continue. |
| 3.5 | Inspect summary output | JSONL/CSV contains Category A metrics fields: `schema_valid`, `component_count`, `collision_count`, `boundary_violation_count`, `attempt_count`, `terminal_reason`, `failure_class`, `duration_ms`, tokens/cost, and `retry_count`. |

---

## §4 — DB Persistence Verification

Anthony applies the migration before this section. The agent must not run Alembic.

| Step | Action | Expected |
|------|--------|----------|
| 4.1 | Inspect DB schema for `log.FormAiEvalRun` | Table exists with required columns and index `(HypothesisCode, VariantLabel, PromptID)`. |
| 4.2 | Run a one-prompt, one-repetition baseline with DB persistence enabled | One row is inserted. |
| 4.3 | Inspect inserted row | `BenchmarkSetVersion = "prompts-v1.0"`, `HypothesisCode = "baseline"`, `VariantLabel` is populated, `PromptID` matches YAML, `MetricsJSON` has Category A fields. |
| 4.4 | Inspect baseline expiry | `BaselineExpiresAt` is 30 days after creation for baseline rows. |
| 4.5 | Confirm judge fields | `JudgeRubricVersion`, `JudgeAgreementScore`, and `BiasDeltaJSON` are nullable/empty in this story. |

---

## §5 — Baseline Artifact Verification

| Step | Action | Expected |
|------|--------|----------|
| 5.1 | Open `docs/stories/STORY-6.4.3a-BENCHMARK-BASELINE.md` | Completed, not just a blank template. |
| 5.2 | Verify run metadata | Includes command, git SHA, benchmark version, prompt IDs, repetitions, model/config snapshot, output folder, and DB persistence status. |
| 5.3 | Verify structural summary | Includes schema validity, component/collision/boundary metrics, attempts/failures, duration, token/cost summary. |
| 5.4 | Verify limitations | States that semantic judging, judge packages, and statistical diffing are deferred to 6.4.3b/6.4.3c. |

---

## §6 — Scope Boundary Check

| Step | Action | Expected |
|------|--------|----------|
| 6.1 | Review PR diff for prompt-production files | No H1/H2/H4 prompt shrink changes. |
| 6.2 | Review PR diff for capability snapshot behavior | No always-pass snapshot flip; that belongs to 6.4.2. |
| 6.3 | Review PR diff for judge/stat files | No rubric, judge package generator, judge ingest, stats module, or PR-comment CI wiring. |
| 6.4 | Confirm docs exist | `docs/FORM-AI-EVAL-HARNESS.md` and `STORY-6.4.3a-CLOSEOUT-REPORT.md` exist. |

---

## Sign-Off

UAT is considered PASS when:

- Automated gate summaries are recorded.
- The migration has been applied by Anthony for DB-persistence UAT.
- A smoke baseline produces run artifacts.
- At least one DB-persisted eval row is verified.
- Baseline artifact is complete.
- Scope boundary check passes.
