# Task Retrospective: T03-form-builder-init-api

**Story:** 5.2 - Company Form Defaults (Brand System)  
**Task:** T03 - Form Builder Init API (Single Payload)  
**Final Status:** ✅ HumanDone  
**Date:** 2026-02-14  

---

## What Went Well

| What Went Well | Evidence |
|----------------|----------|
| T02 resolver reuse | `service.py` uses `resolve_merged_defaults` directly; no duplication (T03-form-builder-init-api.md scope) |
| Raw SQL for FormBuilderComponent | No ORM model; `sqlalchemy.text()` with parameterized query worked cleanly; pragmatic choice |
| CountryID resolution | Event.CountryID → Company.CountryID fallback implemented per design |
| Scope filtering | Component query (Global ∪ Country ∪ Company) and defaultGridLayoutsByComponent filtering by allowed components as specified |
| Clear acceptance criteria | All 5 ACs passed on human UAT; spec was unambiguous |
| Auth enforced | POST without token returns 401; verified in UAT |

---

## What Went Wrong

| Issue | Root Cause | Evidence |
|-------|------------|----------|
| Agent UAT initially got 404 | Backend running from worktree without form_builder module (e.g. T04 worktree branched before T03) | uat-results.md: "form-builder init 404 — backend needs to run from T03 or story worktree" |
| Automated tests deferred | TestClient with app middleware (anyio) caused ExceptionGroup | T03 retro: "Test isolation: TestClient with app middleware caused ExceptionGroup; deferred automated tests" |

---

## Prevention Actions

| Issue | Prevention Action | Owner |
|-------|-------------------|-------|
| Agent UAT 404 (wrong worktree backend) | Add note to UAT checklist: "Backend must be started from worktree containing this task's code" | ralf-uat |
| Automated tests deferred | Add integration test in future task: POST /api/form-builder/init returns 200 for seeded companyId/eventId | ralf-dev / ralf-sm |

---

## Test Improvements

### Automated Tests to Add

| Test Type | Description | Location | Command |
|-----------|-------------|----------|---------|
| integration | POST /api/form-builder/init returns 200 with schemaVersion, context, defaults, components, definitionJSON for valid companyId/eventId | backend/tests/ | `pytest backend/tests/...` |
| integration | 401 when no Authorization header | backend/tests/ | `pytest backend/tests/...` |
| integration | 400/404 for invalid companyId or eventId | backend/tests/ | `pytest backend/tests/...` |

### UAT Automation Candidates

- **Login + form-builder init flow**: Repeated across form-defaults and form-builder tasks. PowerShell script in uat-results already provides template; could be scripted in CI with seeded DB.

---

## Process Improvements

### For ralf-sm (Decomposition)
- Backend API tasks: Include explicit "Backend startup path" note when worktrees are used.
- Consider AC for "integration test returns 200" when endpoint behavior is core.

### For ralf-dev (Execution)
- Before marking complete: Run backend from *this* worktree and verify endpoint responds (smoke test).
- Document any middleware/test harness issues that block automated tests in completion note.

### For ralf-uat (Validation)
- Add prerequisite to UAT checklist: "Backend started from worktree containing task code".
- Use Agent Logging Guide script for quick verification; human validates AC details.

---

## Scope Creep Discovered

| Item | Classification | Routing |
|------|----------------|---------|
| None | — | — |

---

## If We Ran This Again

1. **Smoke test before completion**: Run the PowerShell UAT script from the T03 worktree before marking dev complete; would have caught 404 earlier.
2. **Integrate before deferring tests**: Attempt integration test setup earlier; if TestClient/anyio blocks, document and add manual UAT as mandatory.
3. **UAT checklist prerequisite**: Add "Backend running from worktree with form_builder module" to prerequisites to avoid confusion.

---

*Ralf-Retro — Retrospective complete*
