# Task Retrospective: T05

**Story:** 3.11  
**Task:** Renderer Integration - Submit → Upload/Queue + Clear-after-capture  
**Final Status:** ✅ Passed  
**Date:** 2026-02-04

---

## What Went Well

| What Went Well | Evidence |
|----------------|----------|
| All ACs passed in UAT, including offline queue and reset behavior | `docs/tasks/3.11/T05-renderer-submit-integration.uat-results.md` |
| Submit flow integrated with outbox + idempotency and clear-after-capture | `docs/tasks/3.11/T05-renderer-submit-integration.completion.md` |

## What Went Wrong

| Issue | Root Cause | Evidence |
|-------|------------|----------|
| Online submit initially failed with 404 when backend ran from the local story worktree | Backend was started from a **stale local story worktree** (behind `origin/story`), so it did not include the T03 public submissions endpoint | `docs/tasks/3.11/T05-renderer-submit-integration.uat-results.md` |
| TypeScript check failed due to missing local dependency | Environment setup missing `npm install` before running `npx tsc` | `docs/tasks/3.11/T05-renderer-submit-integration.completion.md` |

## Prevention Actions

| Issue | Prevention Action | Owner |
|-------|-------------------|-------|
| Backend endpoint missing at runtime | Add a precondition check: verify `POST /api/public/forms/{token}/submissions` exists in Swagger before AC2 | ralf-uat |
| Backend worktree mismatch | Require UAT to note backend branch/worktree and confirm it includes T03 | ralf-sm / ralf-uat |
| Missing frontend deps for tests | Add “run `npm install`” to dev verification checklist before TypeScript checks | ralf-dev |

## Test Improvements

### Automated Tests to Add

| Test Type | Description | Location | Command |
|-----------|-------------|----------|---------|
| integration | Smoke test for `POST /api/public/forms/{token}/submissions` returns 200 with valid token | `backend/tests/test_public_submissions.py` | `pytest -k public_submissions` |
| unit | Frontend API helper uses `VITE_API_BASE_URL` for public submissions | `frontend/src/features/renderer/api/__tests__/publicSubmissionApi.test.ts` | `npm test -- --testPathPattern=publicSubmissionApi` |

### UAT Automation Candidates

- Automate preflight check that verifies the public submissions endpoint exists before running AC2–AC5.

## Process Improvements

### For ralf-sm (Decomposition)
- Add explicit backend-branch requirement to T05 preconditions when endpoints are introduced in prior tasks.

### For ralf-dev (Execution)
- Verify backend route availability (Swagger or curl) before declaring “online submit” ready.

### For ralf-uat (Validation)
- Add a required UAT step: check `POST /api/public/forms/{token}/submissions` exists in Swagger before AC2.

## Scope Creep Discovered

| Item | Classification | Routing |
|------|----------------|---------|
| None | - | - |

## If We Ran This Again

Top 3 changes:
1. Add a preflight API endpoint check before UAT submission tests.
2. Require backend branch/worktree verification for public submissions.
3. Run `npm install` before any TypeScript checks.
