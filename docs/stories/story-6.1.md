# Story 6.1: AI Foundation - Static Validator

**Epic:** Epic 6 - AI Generation & Monetization Engine  
**Domain:** Backend Validation API, Builder Contract Validation, Quality Gate Enforcement  
**Status:** Ready  
**Priority:** High (foundational dependency for AI form generation loop)  
**Created:** 2026-02-26  
**Owner:** Scrum Master Agent  
**Prerequisite:** Epic 5 publish and workflow baseline is stable  
**Context:** `docs/stories/story-context-6.1.xml`  
**UAT Guide:** `docs/stories/STORY-6.1-UAT-TEST-GUIDE.md`  
**Dev Prompt:** `docs/stories/STORY-6.1-SINGLE-SESSION-DEV-PROMPT.md`

---

## User Story

**As a** platform system,  
**I want** a static validator endpoint that checks `DefinitionJSON` for schema, boundary, and collision issues without rendering in a browser,  
**So that** AI-generated forms can be validated in a deterministic loop before loading into the Builder.

**As a** Product and Engineering team,  
**I want** strict per-story Green CI/CD evidence,  
**So that** high error volume never becomes normalized and quality stays enforceable after every story.

---

## Context & Entry Point

- Epic 6 starts with a backend-first validator to support later AI loop and UI integration (Stories 6.2+).
- Existing collision and geometry concepts already exist in frontend utilities and should be reused logically (not duplicated with drift).
- Existing schema contracts for form definition exist in backend schema modules.
- TEA baseline is 94/100 and this story must preserve that quality gate behavior.

---

## Scope Boundary

### In scope (Story 6.1)

- Add `POST /api/form-validate` endpoint.
- Accept `DefinitionJSON` payload and validate:
  - schema structure and required fields,
  - component boundary constraints against canvas dimensions,
  - component overlap/collision.
- Return a machine-readable validation response suitable for iterative AI correction.
- Keep validator deterministic and side-effect free (no DB writes needed for validation result).
- Add unit/integration tests for valid and invalid payload scenarios.
- Document request/response contract in story artifacts and UAT guide.
- Enforce Green CI/CD evidence in story closeout workflow.

### Out of scope (Story 6.1)

- AI model integration and retry orchestration loop.
- Builder chat UI and generated form insertion UX.
- Multi-page AI generation behavior optimization.
- Stripe direct/connect billing features.
- Analytics and reporting enhancements.

---

## API Contract (Initial)

### Endpoint

- `POST /api/form-validate`

### Request (high-level)

- JSON body containing `DefinitionJSON` (single form definition payload).

### Response (high-level)

- `valid: boolean`
- `schemaErrors: []`
- `boundaryViolations: []`
- `collisions: []`
- `summary: { errorCount, warningCount }`

Notes:
- Error objects must be stable and parseable by an AI loop.
- Include component identifiers where possible for targeted fixes.

---

## Done Criteria

- [ ] **DC1:** Endpoint `POST /api/form-validate` implemented and reachable.
- [ ] **DC2:** Valid payload returns `valid=true` with empty error lists.
- [ ] **DC3:** Invalid schema returns `valid=false` with structured schema error details.
- [ ] **DC4:** Boundary violations return component-level structured violations.
- [ ] **DC5:** Collisions return component-level overlap details.
- [ ] **DC6:** Validator is deterministic for same input (no random/non-repeatable output).
- [ ] **DC7:** Backend automated tests added and passing for happy path + failure paths.
- [ ] **DC8:** UAT guide executed and results recorded.
- [ ] **DC9:** Green CI/CD evidence captured in story closeout (anti-hallucination protocol respected).
- [ ] **DC10:** Story PR merged to `master`.

---

## Engineering Notes

- Prefer reusing existing schema and collision logic concepts instead of introducing parallel rule definitions.
- Keep the response shape concise and machine-friendly for future AI retry loops.
- If migration is unexpectedly required, agent prepares migration and exact command, but human runs DB migration commands.

---

## References

- Epic roadmap: `docs/stories/EPIC-6-STATUS.md`
- Epic workflow: `docs/stories/EPIC-6-WORKFLOW-GUIDE.md`
- AI concept: `docs/AI-FORM-BUILDING-IDEA.md`
- Existing form schema: `backend/schemas/form_definition.py`
- Existing collision concepts: `frontend/src/features/builder/utils/collisionDetection.ts`

---

*Story 6.1 - AI Foundation: Static Validator*  
*Last Updated: 2026-02-26*
