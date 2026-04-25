# Story 6.4.3c — UAT Test Guide

**Story:** 6.4.3c — Eval Diff + Statistics Tooling  
**Owner:** Anthony (Human UAT)  
**Prep:** Dev provides gate evidence, sample diff report, and completed diff/statistics docs  
**Protocol:** Harness/tooling UAT. No live LLM generation required.

---

## Environment

- Branch: `story/epic6-6.4.3c-eval-diff-statistics`
- Worktree: `C:\wt\elp\story-epic6-6.4.3c-eval-diff-statistics`
- Input runs:
  - `_bmad-output/eval-runs/story-6.4.3a-live-full-10row-baseline/`
  - `_bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline/`
- Judge summary input if needed:
  - `_bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline/judge-package/judge-ingest-summary.json`

---

## §1 — Automated Gates Witness

| Step | Action | Expected |
|------|--------|----------|
| 1.1 | Open `STORY-6.4.3c-GATE-EVIDENCE.md` | Focused tests and backend gate summaries recorded. |
| 1.2 | Review `backend/tests/test_eval_stats.py` result | Pass. |
| 1.3 | Review `backend/tests/test_eval_diff.py` result | Pass. |
| 1.4 | Confirm no live model calls | Tests use fixtures only. |

---

## §2 — Statistics Review

| Step | Action | Expected |
|------|--------|----------|
| 2.1 | Inspect `backend/tests/form_ai_eval/stats.py` | Welch t-test, Cohen's d, Fisher exact, and verdict helpers exist. |
| 2.2 | Review tests for known outputs | Tests cover typical continuous and binary comparisons. |
| 2.3 | Review tiny/degenerate samples | Zero variance/tiny sample paths return safe/inconclusive outputs, not crashes. |
| 2.4 | Review auto-rerun logic | Category B inconclusive results can recommend rerun at n=15. |

---

## §3 — Diff Tool Review

| Step | Action | Expected |
|------|--------|----------|
| 3.1 | Run documented diff command on fixture/sample runs | Markdown, CSV, and JSON outputs are written. |
| 3.2 | Inspect report metadata | Both input runs and versions are identified. |
| 3.3 | Inspect row alignment | Rows align by prompt id + repetition; missing/extra rows are visible. |
| 3.4 | Inspect blocker section | `schema_valid` regression and boundary violations are clearly blocking. |
| 3.5 | Inspect advisory section | Component count, attempts, duration, tokens/cost, collisions, and judge deltas are advisory unless blocking rules apply. |
| 3.6 | Inspect judge metric section | Category B metrics appear when judge summaries exist. |

---

## §4 — Docs Review

| Step | Action | Expected |
|------|--------|----------|
| 4.1 | Open `docs/FORM-AI-EVAL-DIFF-STATS.md` | Explains usage, interpretation, blocking/advisory distinction, and 6.4.4 handoff. |
| 4.2 | Confirm statistical definitions | Welch/Fisher/Cohen's d explained at practical level. |
| 4.3 | Confirm CI scope | PR-comment automation explicitly deferred. |

---

## §5 — Scope Boundary

| Step | Action | Expected |
|------|--------|----------|
| 5.1 | Review PR diff for prompt content changes | None. |
| 5.2 | Review `prompts.yaml` | Unchanged. |
| 5.3 | Review PR diff for sweep artifacts | No H1/H2/H4 formal sweep output. |
| 5.4 | Review dependencies | No new heavyweight dependency unless explicitly approved. |

---

## Sign-Off

UAT passes when:

- focused tests and backend gate pass,
- diff report is readable and actionable,
- blockers/advisory outputs match Epic 6 rules,
- docs are sufficient for Story 6.4.4,
- no prompt/sweep scope leaked in.
