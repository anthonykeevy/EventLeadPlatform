# Story 6.1 UAT Test Guide - AI Foundation Static Validator

**Story:** 6.1  
**Epic:** 6 - AI Generation and Monetization Engine  
**Updated:** 2026-02-26  
**UAT Status:** Pending

---

## Objective

Validate that `POST /api/form-validate` correctly returns deterministic, machine-readable validation results for schema, boundary, and collision checks.

This story uses an **agent-first UAT execution model**:
- Dev agent executes all backend/API UAT cases in this guide.
- Human testing is skipped by default for Story 6.1.
- Escalate to human only for true human-only blockers (credentials/access/env/network controls that the agent cannot resolve).

---

## Execution Ownership (Mandatory)

| Test Type | Owner | Rule |
|-----------|-------|------|
| API/backend UAT (T1-T7) | Dev agent | Must execute fully and record evidence |
| Frontend visual/manual UX | Human | Only when story includes frontend behavior |
| Blocked tests | Dev agent -> Human escalation | Escalate only with explicit blocker evidence |

For Story 6.1 specifically, T1-T7 are API/backend checks and are **agent-owned**.

---

## Prerequisites

1. Backend service running locally.
2. API docs available (Swagger/OpenAPI) or agent-driven HTTP test path available.
3. Test payloads prepared:
   - one valid `DefinitionJSON`,
   - one schema-invalid payload,
   - one boundary-invalid payload,
   - one collision-invalid payload.
4. Story branch/worktree is active for Story 6.1.

---

## Test Cases

## T1 - Endpoint availability

| Step | Action | Expected |
|------|--------|----------|
| 1 | Open Swagger or Postman | API surface available |
| 2 | Locate `POST /api/form-validate` | Endpoint documented |
| 3 | Send minimal valid request body | HTTP 200 response |

---

## T2 - Valid payload

| Step | Action | Expected |
|------|--------|----------|
| 1 | Submit known valid `DefinitionJSON` | HTTP 200 |
| 2 | Inspect response | `valid=true` |
| 3 | Check error arrays | `schemaErrors`, `boundaryViolations`, `collisions` are empty |

---

## T3 - Schema validation failure

| Step | Action | Expected |
|------|--------|----------|
| 1 | Submit schema-invalid payload (missing required field/type mismatch) | HTTP 200 or defined validation status |
| 2 | Inspect response | `valid=false` |
| 3 | Inspect `schemaErrors` | Contains structured, parseable entries |

---

## T4 - Boundary validation failure

| Step | Action | Expected |
|------|--------|----------|
| 1 | Submit payload with out-of-canvas component position/sizing | Response received |
| 2 | Inspect response | `valid=false` |
| 3 | Inspect `boundaryViolations` | Contains component-level boundary flags/details |

---

## T5 - Collision validation failure

| Step | Action | Expected |
|------|--------|----------|
| 1 | Submit payload with overlapping components | Response received |
| 2 | Inspect response | `valid=false` |
| 3 | Inspect `collisions` | Contains component relationships useful for correction |

---

## T6 - Determinism check

| Step | Action | Expected |
|------|--------|----------|
| 1 | Submit same invalid payload twice | Two responses returned |
| 2 | Compare relevant response fields | Error classification/details consistent across calls |

---

## T7 - Non-crash handling

| Step | Action | Expected |
|------|--------|----------|
| 1 | Submit malformed but JSON-parseable payload | Controlled validation response |
| 2 | Verify backend behavior | No server crash/500 stack trace |

---

## Evidence Capture

For each test case, record:
- Request payload identifier
- HTTP status
- Key response snippet
- Pass/Fail verdict

Record results in `docs/stories/STORY-6.1-UAT-RESULTS.md`.

### Escalation Protocol (only if blocked)

If a test cannot be executed by the agent, the UAT results must include:
1. Exact command/action attempted
2. Failure output (error text)
3. Why this is human-only (not just inconvenient)
4. Exact human action requested

Without this evidence, "blocked" is invalid and the agent must continue execution.

---

## UAT Result Summary Table (to complete)

| Test ID | Description | Result | Evidence |
|---------|-------------|--------|----------|
| T1 | Endpoint availability | ⬜ Pending | |
| T2 | Valid payload | ⬜ Pending | |
| T3 | Schema failure | ⬜ Pending | |
| T4 | Boundary failure | ⬜ Pending | |
| T5 | Collision failure | ⬜ Pending | |
| T6 | Determinism | ⬜ Pending | |
| T7 | Non-crash handling | ⬜ Pending | |

---

*Story 6.1 UAT Guide*  
*Last Updated: 2026-02-26*
