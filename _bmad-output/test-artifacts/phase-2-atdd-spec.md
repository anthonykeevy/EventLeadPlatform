# Phase 2 ATDD Spec - Epic 6 Story 6.1 (Red Phase)

Date: 2026-02-26  
Author: TEA (Test Architect)  
Input Blueprint: `_bmad-output/test-artifacts/phase-2-td-test-design.md`

---

## 1) Story scope + assumptions

### Story scope
- Story target: `Epic 6 / Story 6.1 - AI Foundation: Static Validator`
- Delivery scope for ATDD red phase:
  - Generate acceptance scenarios for `TD-6.1-P0-001` through `TD-6.1-P0-008`
  - Define failing expectations before DS implementation starts
  - Specify contracts, determinism constraints, and DS-ready traceability.

### Assumptions
- `POST /api/form-validate` is the canonical validation endpoint for Story 6.1.
- Validation response is machine-readable and structured around:
  - `valid`
  - `schemaErrors[]`
  - `collisions[]`
  - `boundaryViolations[]`
- Story 6.1 is backend-first; UI/agent-loop behavior is deferred to later stories.
- Phase 1 residual constraints are mandatory in this story:
  - seed parity preflight
  - explicit async loop-scope config
  - no newly introduced `datetime.utcnow()` in touched scope.

---

## 2) Acceptance scenarios mapped to test IDs

| ATDD Scenario ID | TD ID | Scenario Title | Priority |
|---|---|---|---|
| ATDD-6.1-P0-001 | TD-6.1-P0-001 | Minimal valid definition returns clean success contract | P0 |
| ATDD-6.1-P0-002 | TD-6.1-P0-002 | Overlap detection returns deterministic collision list | P0 |
| ATDD-6.1-P0-003 | TD-6.1-P0-003 | Out-of-canvas placement returns directional boundary violations | P0 |
| ATDD-6.1-P0-004 | TD-6.1-P0-004 | Schema-invalid payload returns normalized schema errors only | P0 |
| ATDD-6.1-P0-005 | TD-6.1-P0-005 | Same payload/config yields stable, repeatable ordered output | P0 |
| ATDD-6.1-P0-006 | TD-6.1-P0-006 | Seed/config preflight fails fast on missing required rows/settings | P0 |
| ATDD-6.1-P0-007 | TD-6.1-P0-007 | Async loop-scope config is explicit and enforced in test runtime | P0 |
| ATDD-6.1-P0-008 | TD-6.1-P0-008 | Guardrail blocks new `datetime.utcnow()` usage in touched scope | P0 |

---

## 3) Given/When/Then definitions for each P0 case

### ATDD-6.1-P0-001 (TD-6.1-P0-001)
- **Given** a minimal valid `DefinitionJSON` fixture with no overlap and in-bounds coordinates
- **When** client calls `POST /api/form-validate`
- **Then**
  - response status is success (2xx)
  - `valid=true`
  - `schemaErrors`, `collisions`, `boundaryViolations` are present and empty arrays.

### ATDD-6.1-P0-002 (TD-6.1-P0-002)
- **Given** a fixture with two components intentionally overlapping
- **When** client calls `POST /api/form-validate`
- **Then**
  - `valid=false`
  - `collisions[]` contains deterministic entries with stable `componentId` links
  - repeated execution returns identical collision pairing and ordering.

### ATDD-6.1-P0-003 (TD-6.1-P0-003)
- **Given** a fixture with components violating left/right/top/bottom canvas constraints
- **When** client calls `POST /api/form-validate`
- **Then**
  - `valid=false`
  - `boundaryViolations[]` includes directional flags (`left/right/top/bottom`) per violating component
  - direction flags are deterministic across repeated runs.

### ATDD-6.1-P0-004 (TD-6.1-P0-004)
- **Given** malformed or schema-invalid `DefinitionJSON` (missing required fields / wrong types)
- **When** client calls `POST /api/form-validate`
- **Then**
  - failure response is normalized to `schemaErrors[]`
  - no internal stack trace, SQL detail, or framework internals leak in payload
  - collision/boundary outputs are either empty or omitted by documented contract rules.

### ATDD-6.1-P0-005 (TD-6.1-P0-005)
- **Given** a fixed payload and fixed environment config
- **When** validation is executed multiple times
- **Then**
  - full response body is stable in semantic content and deterministic ordering
  - no random IDs/order drift between runs.

### ATDD-6.1-P0-006 (TD-6.1-P0-006)
- **Given** test preflight with required seed/config rows intentionally missing
- **When** preflight suite executes before integration tests
- **Then**
  - suite fails fast with actionable missing-key/missing-row diagnostics
  - downstream validator tests are blocked until parity is restored.

### ATDD-6.1-P0-007 (TD-6.1-P0-007)
- **Given** pytest runtime configuration under Story 6.1 test scope
- **When** configuration validation runs
- **Then**
  - `asyncio_default_fixture_loop_scope` is explicitly set
  - async loop-scope deprecation warning path is not triggered in touched scope.

### ATDD-6.1-P0-008 (TD-6.1-P0-008)
- **Given** static guard/lint-style check over touched Story 6.1 scope
- **When** check runs in CI and local verification
- **Then**
  - no newly added `datetime.utcnow()` usage is allowed
  - violations fail the pipeline with file/symbol-level diagnostics.

---

## 4) Expected API contracts (request/response/error shape)

### Request contract (`POST /api/form-validate`)
- **Content-Type:** `application/json`
- **Body (minimum conceptual shape):**
  - `definition` (object): Story 6.1 `DefinitionJSON` payload
  - optional `options` (object): deterministic validation options (if implemented).

### Success response contract
- **Status:** `200`
- **Body shape:**
  - `valid` (boolean)
  - `schemaErrors` (array)
  - `collisions` (array)
  - `boundaryViolations` (array)
  - optional `meta` (object) for version/context.

### Validation-failure response contract
- **Status:** `200` preferred for analyzable validation results, or `4xx` only for malformed transport-level input (implementation decision must be explicit)
- **Body invariants:**
  - deterministic error structures
  - no internal trace leakage
  - stable keys and deterministic ordering.

### Transport/system error contract
- **Status:** `4xx/5xx` per platform standard
- **Body:** safe, sanitized error format with no stack traces/internal DB details.

---

## 5) Determinism expectations (ordering, stable IDs, repeatability)

- Collision and boundary arrays must be deterministically ordered (documented ordering rule, for example by `componentId` then violation type).
- Component identifiers in violations must map to stable IDs from payload; no runtime-generated random IDs.
- Re-running the same fixture/config yields semantically identical output payloads.
- Preflight checks must produce deterministic missing-item lists (sorted output).

---

## 6) Explicit fail conditions (what should fail now in red phase)

The following are expected to fail in RED phase until DS implements Story 6.1 behavior:

1. `ATDD-6.1-P0-001`: endpoint/contract not fully present or returns non-conforming success payload.
2. `ATDD-6.1-P0-002`: collision list absent, non-deterministic, or missing stable ID mapping.
3. `ATDD-6.1-P0-003`: boundary direction flags incomplete/non-deterministic.
4. `ATDD-6.1-P0-004`: schema error format not normalized or leaks internal details.
5. `ATDD-6.1-P0-005`: repeated runs produce drift in order/content.
6. `ATDD-6.1-P0-006`: no seed/config preflight gate or non-actionable parity diagnostics.
7. `ATDD-6.1-P0-007`: async loop-scope config missing/implicit.
8. `ATDD-6.1-P0-008`: no guard to prevent new `datetime.utcnow()` in touched scope.

Red-phase pass criteria for ATDD generation:
- All eight P0 scenarios are defined and intentionally failing against current non-implemented Story 6.1 behavior.

---

## 7) Traceability table (REQ -> TD ID -> ATDD scenario ID)

| Requirement | TD ID | ATDD Scenario ID |
|---|---|---|
| REQ-6.1-API-001 (`POST /api/form-validate`) | TD-6.1-P0-001, TD-6.1-P0-004 | ATDD-6.1-P0-001, ATDD-6.1-P0-004 |
| REQ-6.1-SCHEMA-002 (schema validity) | TD-6.1-P0-001, TD-6.1-P0-004 | ATDD-6.1-P0-001, ATDD-6.1-P0-004 |
| REQ-6.1-COLLISION-003 (overlap detection) | TD-6.1-P0-002, TD-6.1-P0-005 | ATDD-6.1-P0-002, ATDD-6.1-P0-005 |
| REQ-6.1-BOUNDARY-004 (canvas constraints) | TD-6.1-P0-003 | ATDD-6.1-P0-003 |
| REQ-6.1-CONTRACT-005 (machine-readable feedback) | TD-6.1-P0-004, TD-6.1-P0-005 | ATDD-6.1-P0-004, ATDD-6.1-P0-005 |
| REQ-6.1-OPS-006 (deterministic environment) | TD-6.1-P0-006, TD-6.1-P0-007 | ATDD-6.1-P0-006, ATDD-6.1-P0-007 |
| REQ-6.1-TECHDEBT-007 (warning debt controls) | TD-6.1-P0-008 | ATDD-6.1-P0-008 |

---

## Notes for DS handoff

- P1 anchors are intentionally excluded from this ATDD pack because P0 scope is prioritized and fully specified.
- This document contains no implementation code by design.
