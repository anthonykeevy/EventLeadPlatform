# Story 6.4.2 — Capability Snapshot Prompt Cleanup

**Epic:** 6 — AI Generation & Monetization Engine  
**Story ID:** 6.4.2  
**Title:** Capability Snapshot Prompt Cleanup  
**Status:** Draft — ready for Dev  
**Branch:** `story/epic6-6.4.2-capability-snapshot-prompt-cleanup`  
**PR:** [#69](https://github.com/anthonykeevy/EventLeadPlatform/pull/69) — Draft  
**Created:** 2026-04-25  
**Depends On:** Story 6.4.3a ✅ Complete (PR #68) — eval harness + full 10-row live baseline  
**Unblocks:** Story 6.4.3b, Story 6.4.3c, Story 6.4.4 prompt shrink sweeps

---

## 1) Goal

Clean up the active Form AI prompt path before any prompt-size experiments begin.

This story removes the orphaned static prompt bundle, verifies frontend/backend capability parity, locks the capability snapshot as an always-present prompt constraint where the active generation path supports it, documents the intentional `FormSemanticPlan` backward-compatibility behavior, and re-captures the 6.4.3a baseline after the cleanup.

Success means Story 6.4.4 can change prompt content with confidence that:

- the prompt source of truth is not split across dead files,
- the LLM receives the component capability palette consistently,
- `FormSemanticPlan` compatibility is deliberate rather than accidental,
- the 10-row structural baseline remains green after cleanup.

---

## 2) In Scope

### 2.1 Delete orphaned prompt bundle

Delete `backend/modules/form_ai/system_prompt_sections_1_6.py`.

Current evidence: it is imported by `backend/tests/test_form_ai_prompt_capabilities.py`, but the active prompt assembly path is `_build_initial_messages()` in `backend/modules/form_ai/service.py`.

Required work:

- remove the orphan file,
- update tests so they assert against the active prompt path or active helper functions,
- ensure no production or test import of `SYSTEM_PROMPT_SECTIONS_1_TO_6` remains,
- document the deletion in closeout so future agents do not resurrect it.

### 2.2 Capability Parity Audit

Complete `docs/stories/STORY-6.4.2-CAPABILITY-PARITY-AUDIT.md` before changing capability prompt behavior.

The audit must compare:

- active backend `config.ComponentCapabilitySnapshot` component types and width classes,
- frontend `ComponentRegistry` / toolbox component types,
- runtime footprint coverage from `buildAiRuntimeFootprints.ts`,
- compiler/semantic-validator accepted component types,
- known intentional substitutions, if any.

The audit must classify every discrepancy as:

- `match`,
- `intentional-substitution`,
- `frontend-only`,
- `backend-only`,
- `missing-renderer`,
- `requires-follow-up`.

If the audit finds a capability snapshot type without a matching renderer, Dev must not close the story until it is removed from the active snapshot or explicitly deferred with SM approval and a blocking carry-forward item.

### 2.3 Always-pass capability snapshot prompt block

The active prompt path already has `_build_capability_prompt_block(capability_snapshot_json)`. This story must make the behavior explicit and regression-tested:

- every production Form AI generation path that resolves active governance must pass the active `componentCapabilitySnapshotJson` into `_build_initial_messages()`,
- the system prompt contains `ALLOWED COMPONENT TYPES` when a snapshot exists,
- runtime `componentFootprints` are filtered to the same capability set before reaching the prompt,
- missing/empty snapshot remains a safe legacy fallback, not the normal configured path,
- tests cover both "snapshot present" and "snapshot absent legacy fallback" cases.

If Dev confirms the behavior already exists, lock it with tests and document that no production code change was required beyond cleanup/tests/docs.

### 2.4 `FormSemanticPlan` backward-compat ADR

Create `docs/stories/STORY-6.4.2-FORMSEMANTICPLAN-BACKWARD-COMPAT-ADR.md`.

The ADR must document the current compatibility choices in `backend/modules/form_ai/schemas.py`, including:

- non-`"1.0"` or missing `semanticPlanVersion` normalizes to `"1.0"`,
- `fields` / `items` / `elements` may be accepted as aliases for `components`,
- extra root keys are ignored,
- why this tolerance exists for LLM drift and replayability,
- what is **not** promised as compatibility for future public APIs,
- the retirement trigger if a future schema version is introduced.

No schema expansion is required in this story unless tests reveal the documented behavior is not covered.

### 2.5 Post-cleanup baseline re-capture

Re-run the 6.4.3a harness after cleanup.

Minimum required:

- one full 10-row baseline using `prompts-v1.0`,
- `HypothesisCode = "baseline"`,
- a distinct `VariantLabel`, e.g. `post-642-capability-cleanup`,
- persisted `log.FormAiEvalRun` rows if Anthony has applied the 6.4.3a migration locally,
- update the 6.4.2 closeout report with before/after structural comparison against `STORY-6.4.3a-BENCHMARK-BASELINE.md`.

Blocking rule for this story:

- `schema_valid` must not regress,
- `boundary_violation_count` must remain 0,
- any `collision_count > 0` must be investigated before UAT sign-off.

---

## 3) Out of Scope

| Item | Reason |
|------|--------|
| H1/H2/H4 prompt shrink edits | Story 6.4.4 after judge/diff layers exist |
| Judge packages, rubric, JSON ingest | Story 6.4.3b |
| Welch/Fisher statistics and diff CLI | Story 6.4.3c |
| Changing benchmark prompts | Frozen by 6.4.3a; mutation requires ADR |
| Adding new component capabilities | This story audits parity; new capability work needs its own story/migration |
| Changing `FormSemanticPlan` public schema shape | This story documents current compatibility, not new semantics |
| Image-to-Form / Style Intent / PII layers | Later AI track stories |

---

## 4) Acceptance Criteria

1. **AC-1 Orphan prompt file removed:** `backend/modules/form_ai/system_prompt_sections_1_6.py` is deleted and no import/reference to `SYSTEM_PROMPT_SECTIONS_1_TO_6` remains.
2. **AC-2 Tests target active prompt path:** `backend/tests/test_form_ai_prompt_capabilities.py` or replacement tests assert against `_build_initial_messages()`, `_build_capability_prompt_block()`, and active prompt helper behavior, not the deleted orphan bundle.
3. **AC-3 Capability Parity Audit complete:** `STORY-6.4.2-CAPABILITY-PARITY-AUDIT.md` lists frontend registry/toolbox/runtime footprint types vs backend active snapshot/compiler types, classifies all discrepancies, and records a decision for each.
4. **AC-4 No missing-renderer active capability:** The active capability snapshot contains no component type lacking a frontend renderer/toolbox/runtime surface. Any exception requires explicit SM sign-off and a blocking carry-forward item.
5. **AC-5 Capability block always present when snapshot exists:** A test proves active generation prompt assembly includes `ALLOWED COMPONENT TYPES` and registered component types when governance returns `componentCapabilitySnapshotJson`.
6. **AC-6 Legacy fallback preserved:** A test proves missing/empty snapshot does not crash prompt assembly or semantic validation; fallback is documented as legacy/permissive, not normal configured operation.
7. **AC-7 Runtime context filtered to snapshot:** Tests prove `componentFootprints` entries not present in the active snapshot are filtered before prompt assembly.
8. **AC-8 `FormSemanticPlan` ADR exists:** `STORY-6.4.2-FORMSEMANTICPLAN-BACKWARD-COMPAT-ADR.md` documents the compatibility contract and retirement trigger.
9. **AC-9 Backward-compat behavior covered:** Tests cover version normalization, alias keys (`fields` / `items` / `elements`), and extra root key tolerance for `FormSemanticPlan`.
10. **AC-10 Post-cleanup baseline captured:** The 6.4.3a harness is re-run after cleanup with a distinct variant label and results are recorded in `STORY-6.4.2-CLOSEOUT-REPORT.md`.
11. **AC-11 Structural baseline does not regress:** Compared with the 6.4.3a baseline, post-cleanup run has no `schema_valid` regression, no boundary violations, and no unresolved collisions.
12. **AC-12 Story closeout complete:** `STORY-6.4.2-CLOSEOUT-REPORT.md` contains AC matrix, parity audit summary, baseline comparison, carry-forward items, and green gate evidence.

---

## 5) Definition of Done

- All ACs are mapped to evidence in `STORY-6.4.2-GATE-EVIDENCE.md`.
- Capability audit and ADR artifacts exist and are reviewed.
- Focused backend tests pass.
- Full backend gate is run unless a clear CI-backed exception is recorded.
- Harness re-run evidence is captured.
- No Alembic command is run by the agent.
- PR remains scoped to cleanup, audit, compatibility docs/tests, and baseline recapture.
