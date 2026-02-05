# Task Completion: T09

**Story:** 3.11  
**Task:** Integration + UAT Polish (Scenarios 1–10)  
**Completed:** 2026-02-05  
**Status:** In Progress (Scenario 3 blocked)

---

## Summary of Changes

Bootstrapped T09 with status updates and a scenario-mapped UAT checklist, created the task PR, ran required automated checks, and executed scenarios 1–10 locally with one exception (Scenario 3 blocked by offline reload emulation timing).

## Files Changed

| File | Change | Reason |
|------|--------|--------|
| `docs/tasks/3.11/T09-integration-and-uat-polish.uat.md` | Added | Scenario 1–10 checklist mapped to story UAT guide |
| `docs/tasks/3.11/T09-integration-and-uat-polish.md` | Modified | Mark task in progress |
| `docs/tasks/3.11/STATUS.md` | Modified | Set current task and T09 status |
| `docs/tasks/3.11/TASK-PLAN.md` | Modified | Mark T09 in progress |

## PR

- https://github.com/anthonykeevy/EventLeadPlatform/pull/16

## Acceptance Criteria Verification

### AC1: Execute Scenarios 1–10 (local)
- **Status:** PARTIAL  
- **Result:** Scenarios 1, 2, 4, 5, 6, 7, 8, 9, 10 passed; Scenario 3 blocked.

### AC2: Fix integration defects blocking scenarios
- **Status:** NOT STARTED  
- **Reason:** Only Scenario 3 remains blocked (offline reload emulation timing).

## Test Evidence

### Automated Tests
```bash
python -m py_compile "backend/modules/forms/public_form_router.py"
```
Result: PASS

### Build Verification
```bash
cd frontend
npm run lint
npm run build
```
Result: FAIL (pre-existing frontend lint/TypeScript errors across multiple files; see command output).

## Manual UAT Results (Scenario Summary)

- **Scenario 1 (online submit):** PASS — success banner shown, fields cleared.
- **Scenario 2 (offline queue):** PASS — offline banner shown; outbox count increased (pending=1).
- **Scenario 3 (queue survives reload):** BLOCKED — reload occurs online before offline emulation patch applies, auto-syncs queued item.
- **Scenario 4 (reconnect auto-sync):** PASS — pending item processed after online event; outbox pending count returned to 0.
- **Scenario 5 (backend down while online):** PASS — simulated upload failure queued item; restored fetch synced to success.
- **Scenario 6 (idempotency):** PASS — replay of latest submission returned `status: "DUPLICATE"` with same `submissionId`.
- **Scenario 7 (invalid token):** PASS — UI shows “Unable to open form / Invalid form link.”
- **Scenario 8 (shared-device safety):** PASS — fields cleared after online and offline captures.
- **Scenario 9 (validation telemetry):** PASS — validation errors shown; telemetry POST observed; no outbox item created.
- **Scenario 10 (kiosk session rotation):** PASS — same `clientDeviceId`, different `clientSessionId` across two kiosk submissions.

## Evidence Notes

- **Idempotency check:** `POST /api/public/forms/{token}/submissions` returned `{ status: "DUPLICATE" }`.
- **Validation telemetry:** Network request observed to `/api/public/forms/{token}/telemetry/validation`.
- **Kiosk rotation:** Last two outbox items show same device ID with different session IDs.

## Known Limitations / Out-of-Scope Items

- Scenario 3 requires true offline reload; current automation uses runtime fetch/online patch which applies after reload and allows auto-sync.

## Recommended Next Step

1. Re-run Scenario 3 using real DevTools offline mode (before reload) to confirm queue persistence.
2. Update UAT results file with final Scenario 3 outcome and mark T09 done if all scenarios pass.
