# Story 6.4.3b — UAT Test Guide

**Story:** 6.4.3b — Eval Judge Package + Rubric ADR  
**Owner:** Anthony (Human UAT)  
**Prep:** Dev provides gate evidence, generated judge package fixture, completed rubric ADR, and judge workflow doc  
**Protocol:** Manual judge execution is optional for this story; the required UAT verifies package generation, workflow clarity, and ingest validation.

---

## Environment

- Branch: `story/epic6-6.4.3b-eval-judge-package-rubric`
- Worktree: `C:\wt\elp\story-epic6-6.4.3b-eval-judge-package-rubric`
- Input run: a 6.4.3a/6.4.2 eval run folder, preferably `_bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline/`
- DB: optional for ingest UAT; local summary artifacts must work without DB
- Models: Cursor chats only if Anthony chooses to do a live judge dry-run

---

## §1 — Automated Gates Witness

| Step | Action | Expected |
|------|--------|----------|
| 1.1 | Open `STORY-6.4.3b-GATE-EVIDENCE.md` | Focused tests and backend gate summaries recorded. |
| 1.2 | Review `backend/tests/test_judge_pack.py` result | Pass; no live model calls. |
| 1.3 | Review `backend/tests/test_judge_ingest.py` result | Pass; no live model calls. |
| 1.4 | Confirm stale-field audit | Story/status/workflow fields agree before merge. |

---

## §2 — Rubric Review

| Step | Action | Expected |
|------|--------|----------|
| 2.1 | Open `backend/tests/form_ai_eval/rubric_v1.md` | Defines Category B metrics, score ranges, anchors, JSON shape, and judge instructions. |
| 2.2 | Open `STORY-6.4.3b-RUBRIC-ADR.md` | ADR is completed, not a template. |
| 2.3 | Check governance | ADR states when `rubric_v2.md` is required and that baseline re-scoring is needed after rubric changes. |
| 2.4 | Check scope | Rubric does not require style scoring except clearly marked future placeholders. |

---

## §3 — Judge Package Generation

| Step | Action | Expected |
|------|--------|----------|
| 3.1 | Run documented `judge_pack.py` command on a known eval run folder | Creates `judge-package/`. |
| 3.2 | Inspect package files | Contains `rubric_v1.md`, `judge-input-batch.md`, `judge-output-template.json`, and `results/`. |
| 3.3 | Inspect row ordering | Stable prompt/repetition order; row IDs map back to eval rows. |
| 3.4 | Re-run generator | Output row order and row IDs are unchanged. |
| 3.5 | Inspect anonymisation | Obvious email/phone/date/name-like synthetic values are scrubbed or limitations are documented. |

---

## §4 — Cursor Judge Workflow Dry-Run

| Step | Action | Expected |
|------|--------|----------|
| 4.1 | Open `docs/FORM-AI-EVAL-JUDGE-WORKFLOW.md` | Clear step-by-step instructions for Anthony. |
| 4.2 | Confirm model list | GPT-5 mini control, Claude, Gemini. |
| 4.3 | Confirm save paths | Uses `results/judge-output-gpt5mini.json`, `results/judge-output-claude.json`, `results/judge-output-gemini.json`. |
| 4.4 | Optional: run one judge chat on a tiny fixture | Output matches template and can be ingested. |

---

## §5 — Judge Ingest

| Step | Action | Expected |
|------|--------|----------|
| 5.1 | Run ingest with valid fixture outputs | Summary artifact created; aggregates computed. |
| 5.2 | Remove one row from a fixture output | Ingest fails with clear missing-row error. |
| 5.3 | Duplicate a row ID | Ingest fails with clear duplicate-row error. |
| 5.4 | Set an out-of-range score | Ingest fails with clear range error. |
| 5.5 | Run DB-disabled mode | Local summary still emitted and DB gap recorded. |
| 5.6 | Run DB-enabled mode if available | `log.FormAiEvalRun` judge fields update as documented. |

---

## §6 — Scope Boundary

| Step | Action | Expected |
|------|--------|----------|
| 6.1 | Review PR diff | No Welch/Fisher stats module, diff CLI, or PR-comment CI. |
| 6.2 | Review PR diff | No prompt shrink changes. |
| 6.3 | Review PR diff | No live judge API client or new secrets. |
| 6.4 | Review `prompts.yaml` | Unchanged. |

---

## Sign-Off

UAT passes when:

- rubric and ADR are complete,
- package generation is deterministic,
- ingest validation rejects bad judge files,
- workflow doc is clear enough for Anthony to run three Cursor chats,
- no 6.4.3c/statistics scope leaked in.
