# Story 6.4.2 — UAT Test Guide

**Story:** 6.4.2 — Capability Snapshot Prompt Cleanup  
**Owner:** Anthony (Human UAT)  
**Prep:** Dev provides gate evidence, completed capability audit, ADR, and post-cleanup baseline summary  
**Protocol:** Harness-backed structural UAT. Human review focuses on audit quality, scope boundaries, and baseline comparison.

---

## Environment

- Branch: `story/epic6-6.4.2-capability-snapshot-prompt-cleanup`
- Worktree: `C:\wt\elp\story-epic6-6.4.2-capability-snapshot-prompt-cleanup`
- Prior baseline: `docs/stories/STORY-6.4.3a-BENCHMARK-BASELINE.md`
- Harness: `python -m backend.tests.form_ai_eval.run`
- Migrations: none expected unless audit finds a snapshot repair; Anthony applies any migration.

---

## §1 — Automated Gates Witness

| Step | Command | Expected |
|------|---------|----------|
| 1.1 | Preflight script from the story worktree | Pass; branch/worktree and DB resolution captured. |
| 1.2 | Focused backend prompt/capability tests | Pass; orphan import deleted, active prompt path covered. |
| 1.3 | Focused `FormSemanticPlan` compatibility tests | Pass; ADR behavior covered. |
| 1.4 | Backend green gate | Pass or explicit CI-backed gap recorded. |
| 1.5 | Stale-field audit from workflow guide | No unintended `Draft`, `Ready for UAT`, or stale next-focus language before merge sign-off. |

---

## §2 — Capability Parity Audit Review

| Step | Action | Expected |
|------|--------|----------|
| 2.1 | Open `STORY-6.4.2-CAPABILITY-PARITY-AUDIT.md` | Completed, not a blank template. |
| 2.2 | Review component matrix | Each active backend snapshot type is classified against frontend registry, renderer, runtime footprint, compiler/validator. |
| 2.3 | Check for `missing-renderer` or unresolved `backend-only` types | None remain without explicit SM-approved blocker. |
| 2.4 | Review findings table | P0/P1 findings are fixed or escalated; P2/P3 have clear follow-up homes. |

---

## §3 — Prompt Cleanup Verification

| Step | Action | Expected |
|------|--------|----------|
| 3.1 | Search for `SYSTEM_PROMPT_SECTIONS_1_TO_6` | No matches. |
| 3.2 | Confirm `backend/modules/form_ai/system_prompt_sections_1_6.py` is deleted | File absent. |
| 3.3 | Review prompt tests | Tests assert active `_build_initial_messages()` / capability helper behavior. |
| 3.4 | Review active prompt output fixture/test | Snapshot present produces `ALLOWED COMPONENT TYPES`; snapshot absent legacy fallback does not crash. |

---

## §4 — Backward-Compat ADR Review

| Step | Action | Expected |
|------|--------|----------|
| 4.1 | Open `STORY-6.4.2-FORMSEMANTICPLAN-BACKWARD-COMPAT-ADR.md` | ADR completed with decision, rationale, consequences, tests, and retirement trigger. |
| 4.2 | Review test evidence | Version normalization, aliases, extra root keys, and unknown component rejection are covered. |
| 4.3 | Confirm scope | No new `FormSemanticPlan` fields were added unless explicitly justified by test failure. |

---

## §5 — Post-Cleanup Baseline

| Step | Action | Expected |
|------|--------|----------|
| 5.1 | Review harness command in closeout | Uses `prompts-v1.0`, `baseline`, and distinct variant label such as `post-642-capability-cleanup`. |
| 5.2 | Review output folder | `_bmad-output/eval-runs/<post-642-run-id>/` exists with metrics and summary. |
| 5.3 | Compare to 6.4.3a baseline | No `schema_valid` regression, no boundary violations, no unresolved collisions. |
| 5.4 | Confirm DB persistence if enabled | Rows inserted into `log.FormAiEvalRun` and linked to run metadata. |

---

## §6 — Scope Boundary

| Step | Action | Expected |
|------|--------|----------|
| 6.1 | Review PR diff for H1/H2/H4 prompt edits | None. |
| 6.2 | Review PR diff for judge/rubric/stats files | None. |
| 6.3 | Review `prompts.yaml` | Unchanged unless a separate ADR exists. |
| 6.4 | Review migrations | None expected. If present, Anthony applied it and rationale is recorded. |

---

## Sign-Off

UAT passes when:

- audit and ADR are complete,
- active prompt path tests are green,
- post-cleanup baseline is structurally green,
- scope boundaries are clean,
- stale-field audit passes before merge.
