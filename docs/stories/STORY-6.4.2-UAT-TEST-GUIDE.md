# Story 6.4.2 — UAT Test Guide

**Story:** 6.4.2 — Capability Snapshot Prompt Cleanup  
**Owner:** Anthony (Human UAT)  
**Prep:** Dev has provided gate evidence, completed capability audit, ADR, closeout report, and post-cleanup baseline summary  
**Protocol:** Evidence-backed structural UAT. Human review focuses on audit quality, scope boundaries, baseline comparison, and merge readiness.

---

## Environment

- Branch: `story/epic6-6.4.2-capability-snapshot-prompt-cleanup`
- Worktree: `C:\wt\elp\story-epic6-6.4.2-capability-snapshot-prompt-cleanup`
- Prior baseline: `docs/stories/STORY-6.4.3a-BENCHMARK-BASELINE.md`
- Post-cleanup baseline: `_bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline/`
- Harness: `python -m backend.tests.form_ai_eval.run`
- Migrations: none created or expected for this story.
- PR: #69, open Draft PR to `master`

---

## §1 — Automated Gates Witness

| Step | Command | Expected |
|------|---------|----------|
| 1.1 | Open `STORY-6.4.2-PREFLIGHT.md` | PASS for expected worktree, branch, backend path, Python DB preflight, runtime DB, and env/runtime parity. |
| 1.2 | Open `STORY-6.4.2-GATE-EVIDENCE.md` | Focused command shows `30 passed`; backend gate shows `766 passed, 26 skipped`. |
| 1.3 | Open `STORY-6.4.2-CLOSEOUT-REPORT.md` §7 | Gates table matches evidence file and includes baseline recapture. |
| 1.4 | Review stale-field audit result in closeout | PR #69 is intentionally still Draft and story/status fields intentionally show Ready for UAT / SM review. |

---

## §2 — Capability Parity Audit Review

| Step | Action | Expected |
|------|--------|----------|
| 2.1 | Open `STORY-6.4.2-CAPABILITY-PARITY-AUDIT.md` | Status is complete; active snapshot is `cf-6.3.1-v4`. |
| 2.2 | Review component matrix | All 19 active snapshot component types are classified `match`. |
| 2.3 | Check for `missing-renderer`, active `backend-only`, or `requires-follow-up` | None for active snapshot capabilities. |
| 2.4 | Review findings table | Only non-blocking P3 notes remain; no P0/P1/P2 blocker is open. |
| 2.5 | Sanity-check business decision | It is acceptable that prompt now treats the active snapshot as authoritative. |

---

## §3 — Prompt Cleanup Verification

| Step | Action | Expected |
|------|--------|----------|
| 3.1 | Search production/test code for `SYSTEM_PROMPT_SECTIONS_1_TO_6` or `system_prompt_sections_1_6` | No production/test references. Story/planning docs may intentionally mention the deleted file. |
| 3.2 | Confirm `backend/modules/form_ai/system_prompt_sections_1_6.py` is deleted | File absent. |
| 3.3 | Review prompt tests | Tests assert active `_build_initial_messages()` / capability helper behavior. |
| 3.4 | Review active prompt output fixture/test | Snapshot present produces `ALLOWED COMPONENT TYPES`; snapshot absent legacy fallback does not crash. |
| 3.5 | Review `backend/modules/form_ai/service.py` change | Only stale fallback examples changed; no H1/H2/H4 prompt shrink work was introduced. |

---

## §4 — Backward-Compat ADR Review

| Step | Action | Expected |
|------|--------|----------|
| 4.1 | Open `STORY-6.4.2-FORMSEMANTICPLAN-BACKWARD-COMPAT-ADR.md` | Status is Accepted; decision, rationale, consequences, tests, and retirement trigger are present. |
| 4.2 | Review test evidence | Version normalization, aliases, extra root keys, and unknown component rejection are covered. |
| 4.3 | Confirm scope | No new `FormSemanticPlan` fields were added. |
| 4.4 | Confirm compatibility boundary | ADR says this is internal LLM/replay tolerance, not a public API compatibility guarantee. |

---

## §5 — Post-Cleanup Baseline

| Step | Action | Expected |
|------|--------|----------|
| 5.1 | Review harness command in closeout | Uses `prompts-v1.0`, `baseline`, `--variant-label post-642-capability-cleanup`, `--persist-db`, and run id `story-6.4.2-post-cleanup-baseline`. |
| 5.2 | Review output folder | `_bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline/` exists with `metrics.jsonl`, `summary.csv`, and `run-metadata.json`. |
| 5.3 | Compare to 6.4.3a baseline | 10/10 completed, 0 `schema_valid` failures, 0 boundary violations, 0 collisions. |
| 5.4 | Confirm DB persistence if desired | Closeout records `log.FormAiEvalRun` rows `13..22` and `GenerationRunID=107..116`. |
| 5.5 | Review aggregate drift | Mean component count changed from 14.1 to 16.0; accept as structurally green because validity, boundary, and collision metrics did not regress. |

---

## §6 — Scope Boundary

| Step | Action | Expected |
|------|--------|----------|
| 6.1 | Review PR diff for H1/H2/H4 prompt shrink edits | None. |
| 6.2 | Review PR diff for judge/rubric/stats files | None. |
| 6.3 | Review `backend/tests/form_ai_eval/prompts.yaml` | Unchanged. |
| 6.4 | Review migrations | None. |
| 6.5 | Review frontend files | No frontend behavior changes; frontend files were read for audit only. |

---

## §7 — Human Verification Needed

No additional automated test needs to be run manually unless you want an independent witness run. Dev already ran:

- `python -m pytest tests/test_form_ai_prompt_capabilities.py tests/test_story_631_semantic_validator.py --tb=short`
- `python -m pytest --tb=short`
- `python -m backend.tests.form_ai_eval.run --variant baseline --hypothesis-code baseline --variant-label post-642-capability-cleanup --repetitions 1 --max-cost-usd 1 --persist-db --run-id story-6.4.2-post-cleanup-baseline`

Please verify these human-only items:

| Check | What Anthony Should Decide |
|-------|----------------------------|
| Audit quality | The parity audit classifications and `safe` decision are credible. |
| ADR boundary | The documented `FormSemanticPlan` tolerance is acceptable as internal LLM/replay compatibility. |
| Baseline acceptance | The post-cleanup structural baseline is acceptable despite mean component count moving from 14.1 to 16.0. |
| Scope | The PR stayed within cleanup/audit/tests/docs/baseline recapture and did not start prompt-shrink or judge/statistics work. |
| Merge readiness | PR #69 can remain Draft until SM review completes; then mark ready/merge per Epic 6 workflow. |

---

## Sign-Off

UAT passes when:

- audit and ADR are complete,
- active prompt path tests are green,
- post-cleanup baseline is structurally green,
- scope boundaries are clean,
- stale-field audit passes before merge.
