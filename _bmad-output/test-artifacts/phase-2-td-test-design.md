# Phase 2 TEA Test Design (TD) - Next Implementation Cycle

Date: 2026-02-26  
Author: TEA (Test Architect)  
Status: Draft - Ready for ATDD follow-on

---

## 1) Scope and assumptions

### Scope target
- **Primary target:** `Epic 6 / Story 6.1 - AI Foundation: Static Validator`
- **Design focus:** Backend validation API (`POST /api/form-validate`) that accepts `DefinitionJSON` and returns schema + collision/boundary feedback without DOM dependency.

### Assumption (ambiguity resolved)
- The "next epic/story set" is treated as **Epic 6 Story 6.1**, based on:
  - `docs/stories/EPIC-6-WORKFLOW-GUIDE.md` explicitly marking **Current Focus: Story 6.1**
  - `docs/stories/EPIC-6-STATUS.md` roadmap positioning 6.1 as the first delivery item in Epic 6
  - Phase 1 auth-token stabilization now complete and positioned as a quality baseline, not the active feature stream.

### Explicit constraints carried from Phase 1 RV
- Must include and track:
  - **Reference seed parity checks** (for deterministic integration behavior)
  - **Explicit `pytest-asyncio` loop-scope configuration** to avoid future behavior drift
  - **`datetime.utcnow()` warning debt reduction plan** (timezone-aware UTC migration path)

### Out of scope for this TD
- Implementation code and endpoint coding details
- Full Epic 6.2+ UX/agent-loop implementation details
- Stripe billing/connect stories (6.3+)

---

## 2) Risk matrix (probability x impact, ranked)

| Rank | Risk ID | Category | Risk Description | Probability (1-3) | Impact (1-3) | Score | Mitigation Direction | Owner |
|---|---|---|---|---:|---:|---:|---|---|
| 1 | R-001 | TECH | Static collision/boundary validator diverges from builder runtime behavior, producing false pass/fail outputs | 3 | 3 | 9 | Shared collision rules + golden parity tests against canonical layouts | Backend + QA |
| 2 | R-002 | DATA | `DefinitionJSON` schema contract drift between backend validator and form builder payload versions | 3 | 2 | 6 | Contract tests + versioned schema fixtures + strict backward-compat checks | Backend |
| 3 | R-003 | OPS | Environment seed parity issues reintroduce non-deterministic failures in integration tests | 2 | 3 | 6 | Preflight seed parity gate in CI and local test bootstrap | QA + DevOps |
| 4 | R-004 | OPS | Warning debt (`datetime.utcnow`, async loop-scope) masks regressions and degrades signal quality | 3 | 2 | 6 | Enforce warning budget + migrate to aware UTC + set loop scope explicitly | Backend |
| 5 | R-005 | PERF | Large/complex form payloads cause validator latency spikes | 2 | 3 | 6 | Payload-size test bins + perf budget checks in nightly suite | Backend |
| 6 | R-006 | SEC | Validation endpoint error messages leak internal details (schema internals/stack traces) | 2 | 3 | 6 | Error-shaping tests + safe, structured failure responses | Backend |
| 7 | R-007 | BUS | AI loop receives low-quality feedback schema, reducing auto-correction success | 2 | 2 | 4 | Stable machine-readable error taxonomy and deterministic ordering | Product + Backend |
| 8 | R-008 | TECH | Existing auth middleware baseline regresses while implementing new validator surfaces | 1 | 3 | 3 | Keep focused auth regression set in PR gate | QA |

---

## 3) Priority map (P0/P1/P2/P3 by requirement area)

| Requirement Area | Priority | Why |
|---|---|---|
| Validator correctness: schema validation and deterministic collision/boundary outcomes | P0 | Core story value; blocker if incorrect |
| Error contract quality: stable machine-readable `schemaErrors/collisions/boundaryViolations` | P0 | Needed for reliable AI retry loop |
| Negative/edge payload handling (malformed JSON, missing fields, invalid coordinates/types) | P0 | Prevents brittle runtime behavior |
| Endpoint security and safe error response shape | P1 | High-impact if leaked internals |
| Performance envelope (payload size/component count buckets) | P1 | Critical for practical usage, not day-1 blocker if guarded |
| Compatibility with existing schema endpoint and form builder assumptions | P1 | Avoid downstream integration breakage |
| Observability/logging quality for validation failures | P2 | Operability improvement |
| UX-level AI prompt quality and iterative refinement effectiveness | P2 | Story 6.2+ optimization path |
| Experimental/adversarial fuzzing and long-run soak scenarios | P3 | Valuable but not DS-blocking |

---

## 4) Test level strategy (unit/integration/e2e split with rationale)

### Strategy split
- **Unit (~55%)**
  - Pure validators: field/schema guards, collision geometry helpers, boundary checks, deterministic error ordering.
  - Rationale: fastest feedback and best defect localization for algorithmic logic.
- **Integration/API (~40%)**
  - Endpoint contract tests for `POST /api/form-validate`, auth expectations, payload classes, and response shape invariants.
  - Includes seed parity preflight + warning-budget checks from Phase 1 concerns.
  - Rationale: validates service wiring and real request/response behavior.
- **E2E (~5%)**
  - Thin smoke only (if story 6.1 is backend-only, keep this minimal): schema retrieval + validator endpoint round-trip through API boundary.
  - Rationale: avoid overinvesting in UI/E2E before 6.2 integration.

### Anti-duplication rule
- E2E checks flow integrity only; correctness assertions stay at unit/API levels.

---

## 5) Critical path scenarios (minimum P0 set required before DS)

| Test ID | Scenario | Level | Risk Link | DS Blocker? |
|---|---|---|---|---|
| TD-6.1-P0-001 | Valid minimal `DefinitionJSON` returns `valid=true` with empty violation arrays | API | R-001/R-002 | Yes |
| TD-6.1-P0-002 | Overlapping components return deterministic `collisions[]` with stable component IDs | Unit + API | R-001 | Yes |
| TD-6.1-P0-003 | Out-of-canvas placement returns deterministic `boundaryViolations[]` with directional flags | Unit + API | R-001 | Yes |
| TD-6.1-P0-004 | Schema-invalid payload returns normalized `schemaErrors[]` (no internal trace leakage) | API | R-002/R-006 | Yes |
| TD-6.1-P0-005 | Same payload + same config always yields same ordered response (determinism test) | Unit | R-001/R-007 | Yes |
| TD-6.1-P0-006 | CI preflight fails fast when required reference seed rows/config are missing | Integration | R-003 | Yes |
| TD-6.1-P0-007 | Test environment has explicit async loop-scope config and zero related deprecation warnings in touched scope | Integration | R-004 | Yes |
| TD-6.1-P0-008 | Touched validator/auth code path has no newly introduced `datetime.utcnow()` usage | Unit/Static + API | R-004 | Yes |

**Minimum P0 pass condition before DS:** all `TD-6.1-P0-*` pass at 100%.

---

## 6) Data/fixture strategy

### Fixture principles
- Use deterministic, versioned JSON fixtures for:
  - Valid baseline forms
  - Collision-heavy layouts
  - Boundary-only violation cases
  - Mixed schema + geometry failure payloads
- Maintain fixture catalog by complexity tier:
  - Tier A: 1-3 components
  - Tier B: 10-20 components
  - Tier C: stress/perf payloads

### Seed/config parity controls (mandatory from Phase 1)
- Add a test preflight asserting required reference rows/config records exist before integration tests run.
- Fail fast with actionable error output when parity is missing.

### Async + time handling controls (mandatory from Phase 1)
- Set explicit `asyncio_default_fixture_loop_scope` in pytest config (target: `function`, unless test architecture requires broader scope).
- Introduce a warning budget policy for touched files:
  - No new `datetime.utcnow()` usage
  - Migration path to aware UTC (`datetime.now(datetime.UTC)`) in validator-adjacent code.

### Test data hygiene
- Unique IDs/emails/tokens for mutable entities to avoid collision across runs.
- No hidden dependencies on machine-local DB state.

---

## 7) CI execution strategy (what must run per PR vs nightly)

### Per PR (required)
- Validator/unit suite for Story 6.1 scope
- Validator API integration suite
- Phase 1 baseline protection set:
  - `backend/tests/test_jwt_service.py`
  - `backend/tests/test_auth_middleware.py`
  - `backend/tests/test_team_invitations.py`
- Seed parity preflight check
- Warning policy checks for touched files:
  - async loop-scope configuration present
  - no newly introduced `datetime.utcnow()` in touched scope

### Nightly (required)
- Extended payload/performance tiers (large forms, worst-case collision maps)
- Broader auth-adjacent regression matrix
- Flakiness burn-in repeat runs for validator deterministic responses

### Weekly (recommended)
- Stress and adversarial malformed payload suite
- Extended compatibility drift checks against latest builder JSON schema snapshots

---

## 8) Gate criteria (PASS / CONCERNS / FAIL thresholds)

### PASS
- 100% pass on P0 scenarios (`TD-6.1-P0-*`)
- No unresolved risk with score `9`
- P1 pass rate >=95%
- Seed parity preflight green
- Async loop-scope explicitly configured
- No newly introduced `datetime.utcnow()` usage in touched scope
- No security leakage in validation error responses

### CONCERNS
- P0 pass is 100%, but one or more score-6 risks remain with approved mitigation plans and owners
- P1 pass rate between 90% and 94%
- Non-blocking warning debt remains but is trending down with explicit action plan

### FAIL
- Any P0 failure
- Any unresolved score-9 risk
- Seed parity preflight missing/failing
- Missing async loop-scope config in active test path
- New warning debt introduced in touched scope (`datetime.utcnow` or equivalent) without waiver
- Validation response leaks sensitive/internal error detail

---

## 9) Traceability anchors (requirement -> planned test IDs)

| Requirement Anchor | Planned Test IDs | Priority |
|---|---|---|
| REQ-6.1-API-001: Provide `POST /api/form-validate` endpoint | TD-6.1-P0-001, TD-6.1-P0-004 | P0 |
| REQ-6.1-SCHEMA-002: Validate `DefinitionJSON` contract | TD-6.1-P0-001, TD-6.1-P0-004, TD-6.1-P1-009 | P0/P1 |
| REQ-6.1-COLLISION-003: Detect component overlaps deterministically | TD-6.1-P0-002, TD-6.1-P0-005, TD-6.1-P1-010 | P0/P1 |
| REQ-6.1-BOUNDARY-004: Detect out-of-canvas violations | TD-6.1-P0-003, TD-6.1-P1-011 | P0/P1 |
| REQ-6.1-CONTRACT-005: Return machine-readable feedback for AI loop | TD-6.1-P0-004, TD-6.1-P1-012 | P0/P1 |
| REQ-6.1-OPS-006: Deterministic CI/test environment setup | TD-6.1-P0-006, TD-6.1-P0-007 | P0 |
| REQ-6.1-TECHDEBT-007: Prevent warning debt regression | TD-6.1-P0-008, TD-6.1-P2-013 | P0/P2 |
| REQ-6.1-PERF-008: Maintain acceptable validator latency | TD-6.1-P1-014, TD-6.1-P3-015 | P1/P3 |

---

## ATDD handoff readiness

- This TD is intentionally design-first and code-free, suitable for immediate ATDD breakdown of `TD-6.1-P0-*` scenarios.
- Recommended next step: generate failing acceptance tests from P0 anchors before implementation begins.
