# Phase 2 ATDD Implementation Checklist - Epic 6 Story 6.1

Date: 2026-02-26  
Author: TEA (Test Architect)  
Scope: DS execution checklist aligned to P0 ATDD scenarios only

---

## 1) Ordered implementation tasks for DS

1. **Contract-first scaffolding**
   - Finalize Story 6.1 API contract for `POST /api/form-validate` (keys, ordering guarantees, error normalization).
   - Lock deterministic ordering rules for `collisions[]` and `boundaryViolations[]`.

2. **Preflight guardrails before feature logic**
   - Add seed/config parity preflight for required rows/settings.
   - Enforce explicit async loop-scope configuration check.
   - Enforce no-new-`datetime.utcnow()` static guard on touched scope.

3. **Schema validation layer**
   - Implement schema validation pathway that emits normalized `schemaErrors[]`.
   - Ensure transport/system errors remain sanitized.

4. **Static collision validation layer**
   - Implement overlap detection with stable ID mapping and deterministic ordering.

5. **Boundary validation layer**
   - Implement directional boundary checks with stable directional flags.

6. **Response shaping + determinism hardening**
   - Ensure stable key set and ordering behavior across repeated runs.
   - Add deterministic sorting for violations and preflight diagnostics.

7. **Regression protection integration**
   - Keep Phase 1 auth/token baseline suites in PR gate.
   - Verify new Story 6.1 checks do not regress auth middleware/jwt/invitation baselines.

---

## 2) Test-first sequence (failing tests to enable first)

Recommended red->green enablement order (strict):

1. `ATDD-6.1-P0-006` (seed parity preflight)
2. `ATDD-6.1-P0-007` (async loop-scope explicit config)
3. `ATDD-6.1-P0-008` (no-new-`datetime.utcnow` guard)
4. `ATDD-6.1-P0-001` (minimal valid success contract)
5. `ATDD-6.1-P0-004` (schema-invalid normalized errors)
6. `ATDD-6.1-P0-002` (collision determinism)
7. `ATDD-6.1-P0-003` (boundary directional determinism)
8. `ATDD-6.1-P0-005` (repeatability/stable ordering full determinism)

Rationale:
- Environment and policy guardrails first prevent false-green outcomes and noisy regressions.
- Core contract and schema behavior before geometry logic.
- Determinism lock last, once all violation classes are present.

---

## 3) Data/fixture prerequisites

### Required fixture packs
- `fixtures/definitionjson/minimal-valid.json`
- `fixtures/definitionjson/overlap-two-components.json`
- `fixtures/definitionjson/boundary-violations-all-directions.json`
- `fixtures/definitionjson/schema-invalid-missing-required.json`
- `fixtures/definitionjson/schema-invalid-type-mismatch.json`
- `fixtures/definitionjson/repeatability-baseline.json`

### Required preflight datasets
- Reference rows/settings needed by Story 6.1 integration scope:
  - status/role/config keys used by shared test harness and validator entry path
  - any validator-specific config defaults (if required by contract).

### Determinism data rules
- Stable component IDs in fixtures (no random generation within tests).
- Sorted expected outputs for deterministic assertions.

### Mandatory platform constraints from TD
- Explicit `asyncio_default_fixture_loop_scope` is set and validated.
- No newly introduced `datetime.utcnow()` in touched Story 6.1 scope.
- Seed parity preflight must execute before integration suites.

---

## 4) CI gates required before merge

## Required PR gates
- P0 ATDD scenario suite: 100% pass
- Seed parity preflight: pass
- Async loop-scope config check: pass
- No-new-`datetime.utcnow()` guard: pass
- Story 6.1 unit/API test suites: pass
- Phase 1 baseline protection suites:
  - `backend/tests/test_jwt_service.py`
  - `backend/tests/test_auth_middleware.py`
  - `backend/tests/test_team_invitations.py`

## Required nightly gates
- Extended payload complexity tiers
- Determinism repeat-run burn-in for collision/boundary outputs
- Broader auth-adjacent regression matrix

## Merge stop conditions
- Any P0 scenario failure
- Missing/disabled preflight guardrail checks
- New warning debt introduced in touched scope without approved waiver.

---

## 5) Risk controls tied to R-001, R-002, R-003

### R-001 (validator/runtime divergence, score 9)
- Controls:
  - Golden parity fixtures mapped to known builder collision/boundary semantics
  - Deterministic ordering assertions for every violation class
  - Repeatability test (`ATDD-6.1-P0-005`) as release blocker.
- Evidence required:
  - Stable outputs across repeated runs on same payload/config
  - No mismatch against accepted parity fixtures.

### R-002 (schema contract drift, score 6)
- Controls:
  - Explicit request/response contract assertions in `ATDD-6.1-P0-001` and `ATDD-6.1-P0-004`
  - Schema-invalid fixture matrix (missing required, wrong type)
  - Error normalization checks to prevent contract erosion.
- Evidence required:
  - Contract tests green in PR
  - No undocumented response key drift.

### R-003 (seed parity nondeterminism, score 6)
- Controls:
  - Mandatory preflight test (`ATDD-6.1-P0-006`) gating all integration runs
  - Sorted, actionable missing-item diagnostics
  - CI fail-fast on missing reference/config prerequisites.
- Evidence required:
  - Preflight green in PR
  - Deterministic failure output when parity intentionally broken.

---

## DS readiness decision

- **Ready for DS:** Yes, after all eight P0 red-phase scenarios are instantiated as failing tests and wired into PR gating.
- **P1 carry-over:** Deferred until P0 implementation is complete and stable.
