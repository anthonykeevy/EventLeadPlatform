# Story 6.4.3b — UAT Test Guide

**Story:** 6.4.3b — Eval Judge Package + Rubric ADR  
**Owner:** Anthony (Human UAT)  
**Prep:** Dev provides gate evidence, generated 10-row judge package, completed rubric ADR, and judge workflow doc  
**Protocol:** Manual judge execution is optional for this story; required UAT verifies package readiness, workflow clarity, and automated ingest coverage.

---

## Environment

- Branch: `story/epic6-6.4.3b-eval-judge-package-rubric`
- Worktree: `C:\wt\elp\story-epic6-6.4.3b-eval-judge-package-rubric`
- Input run: a 6.4.3a/6.4.2 eval run folder, preferably `_bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline/`
- Generated package: `_bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline/judge-package/`
- DB: required only if regenerating the real package with generated definitions via `--use-db`; local ingest tests do not require DB
- Models: Cursor chats only if Anthony chooses to do a live judge dry-run

---

## §1 — Automated Gates Witness

| Step | Action | Expected |
|------|--------|----------|
| 1.1 | Open `STORY-6.4.3b-GATE-EVIDENCE.md` | Focused tests and backend gate summaries recorded. |
| 1.2 | Review `backend/tests/test_judge_pack.py` result | Pass; no live model calls. |
| 1.3 | Review `backend/tests/test_judge_ingest.py` result | Pass; no live model calls. |
| 1.4 | Confirm stale-field audit | Story/status/workflow fields agree before merge. |
| 1.5 | Optional witness rerun | From worktree root, run `.\scripts\workflow\run-green-gate.ps1 -StoryId "6.4.3b" -FocusedTestCommand "python -m pytest tests/test_judge_pack.py tests/test_judge_ingest.py --tb=short" -BackendGateCommand "python -m pytest --tb=short" -EvidenceFile "docs/stories/STORY-6.4.3b-GATE-EVIDENCE.md"`; expected focused `7 passed`, backend green. |

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
| 3.1 | Confirm existing generated package | `_bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline/judge-package/` exists. |
| 3.2 | Optional: regenerate package | From worktree root, run `python -m backend.tests.form_ai_eval.judge_pack _bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline --use-db`; expected row count is 10. |
| 3.3 | Inspect package files | Contains `rubric_v1.md`, `judge-input-batch.md`, `judge-output-template.json`, `judge-package-metadata.json`, and `results/`. |
| 3.4 | Inspect row ordering | `judge-package-metadata.json` rows follow prompt order with stable `row_id` values ending `__r01`. |
| 3.5 | Inspect DB enrichment | Each row has `generated_definition_available: true`, `generated_definition_source: "dbo.GenerationArtifact"`, and `eval_run_id` populated. |
| 3.6 | Inspect anonymisation note | Metadata documents email/phone/date/name scrubbing limitations; generated judge input is the approved scrubbed surface. |

---

## §4 — Cursor Judge Workflow Dry-Run

| Step | Action | Expected |
|------|--------|----------|
| 4.1 | Open `docs/FORM-AI-EVAL-JUDGE-WORKFLOW.md` | Clear step-by-step instructions for Anthony. |
| 4.2 | Confirm model list | GPT-5 mini control, Claude, Gemini. |
| 4.3 | Confirm save paths | Uses `results/judge-output-gpt5mini.json`, `results/judge-output-claude.json`, `results/judge-output-gemini.json`. |
| 4.4 | Optional: run the three judge chats | Save outputs to `results/judge-output-gpt5mini.json`, `results/judge-output-claude.json`, and `results/judge-output-gemini.json`. This is not required for Dev sign-off. |

---

## §5 — Judge Ingest

| Step | Action | Expected |
|------|--------|----------|
| 5.1 | Review automated ingest coverage | `STORY-6.4.3b-GATE-EVIDENCE.md` shows focused ingest tests passed. |
| 5.2 | Optional: run ingest after saving real judge files | `python -m backend.tests.form_ai_eval.judge_ingest _bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline/judge-package`; expected `judge-ingest-summary.json` and `.csv`. |
| 5.3 | Optional: DB update after successful real ingest | Add `--persist-db`; expected nullable judge fields update on `log.FormAiEvalRun`. |
| 5.4 | Validation behavior | Missing rows, duplicate rows, unknown rows, malformed score keys, and out-of-range scores are covered by automated tests; do not hand-edit real judge files just to prove failures unless you want extra witness evidence. |

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
- generated 10-row judge package exists and maps to eval rows,
- package generation and ingest validation are covered by passing automated gates,
- workflow doc is clear enough for Anthony to run three Cursor chats,
- no 6.4.3c/statistics scope leaked in.

No extra automated tests are required from Anthony unless you want to witness the gate locally. The only manual UAT decision is whether to run the optional three Cursor judge chats now or defer live judge scoring until the first prompt sweep needs it.
