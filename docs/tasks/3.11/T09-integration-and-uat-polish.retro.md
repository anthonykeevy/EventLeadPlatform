# Task Retrospective: T09

**Story:** 3.11  
**Task:** Integration + UAT Polish (Scenarios 1–10)  
**Final Status:** ✅ Done  
**Date:** 2026-02-05

---

## What Went Well

| What Went Well | Evidence |
|---|---|
| End-to-end outbox flow works across online/offline/reconnect. | `docs/tasks/3.11/T09-integration-and-uat-polish.uat-results.md` |
| Idempotency behavior validated (duplicate detection on replay). | `docs/tasks/3.11/T09-integration-and-uat-polish.uat-results.md` |
| Shared-device safety validated (fields cleared after capture). | `docs/tasks/3.11/T09-integration-and-uat-polish.uat-results.md` |
| Validation telemetry verified (submit blocked; telemetry emitted; no outbox item). | `docs/tasks/3.11/T09-integration-and-uat-polish.uat-results.md` |

## What Went Wrong

| Issue | Root Cause | Evidence |
|---|---|---|
| Frontend lint/build verification failed due to pre-existing TS/lint errors. | Baseline issues outside Story 3.11 scope. | `docs/tasks/3.11/T09-integration-and-uat-polish.completion.md` |

## Prevention Actions

| Issue | Prevention Action | Owner |
|---|---|---|
| Baseline build failures block verification. | Keep recording baseline failures explicitly in completion notes; schedule a dedicated “build stabilization” task when needed. | ralf-dev / PM |

## Test Improvements

### Automated Tests to Add

| Test Type | Description | Location | Command |
|---|---|---|---|
| integration | Public submission endpoint smoke test (200/409) to prevent “wrong backend worktree” false failures. | `backend/tests/` | `pytest -k public_submission_endpoint_exists` |
| integration | Validation resolved-flow test (invalid telemetry then success) to validate correlation logic. | `backend/tests/` | `pytest -k validation_resolved_flow` |

## Process Improvements

### For ralf-uat (Validation)
- Add a quick Swagger/curl endpoint preflight before scenario execution to confirm the backend worktree includes required routes.

### For ralf-sm (Next task / status hygiene)
- Ensure `docs/tasks/<story>/STATUS.md` stays consistent with `TASK-PLAN.md` + task headers when tasks are merged.

## Scope Creep Discovered

| Item | Classification | Routing |
|---|---|---|
| None | N/A | N/A |

## If We Ran This Again

1. Ensure story UAT guide pass/fail section includes **all** scenarios (1–10) from day 1.
2. Preflight the backend endpoint in Swagger before running UI scenarios.
3. Keep “baseline build errors” explicitly documented to avoid ambiguous verification failures.

