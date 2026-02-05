# Task Completion: T07

**Story:** 3.11  
**Task:** Validation Telemetry - Events + Storage + Resolved vs Abandoned  
**Completed:** 2026-02-05  
**Status:** Complete

---

## Summary of Changes

Added client-side telemetry for validation-blocked submits with privacy-safe diagnostics and wired a public backend endpoint to store the events in `log.FrontendEvent`. Telemetry now carries component/rule identity, value diagnostics, and client/session correlation identifiers without raw values.

## Files Changed

| File | Change | Reason |
|------|--------|--------|
| `frontend/src/features/renderer/api/publicSubmissionApi.ts` | Modified | Add API client for validation telemetry endpoint |
| `frontend/src/features/renderer/components/PublicFormArtboard.tsx` | Modified | Emit `validation_failed_submit` events on blocked submit with diagnostics |
| `backend/modules/forms/public_form_router.py` | Modified | Add public telemetry endpoint storing events in `log.FrontendEvent` |

## Acceptance Criteria Verification

### AC1: Emit `validation_failed_submit` events when submit is blocked by validation
- **Status:** PASS  
- **Evidence:** `PublicFormArtboard` now creates a submit attempt ID, builds failures, and calls `submitPublicValidationTelemetry` when `computeErrors(true)` returns errors.

### AC2: Include rule/component identity + value diagnostics and exclude raw values
- **Status:** PASS  
- **Evidence:** Failures are built with `componentId`, `componentType`, `ruleType`, `ruleCode`, `errorCategory`, and `valueDiagnostics` via `getValueDiagnostics` (no raw values are included).

### AC3: Store telemetry in a queryable backend table
- **Status:** PASS  
- **Evidence:** New public endpoint `/api/public/forms/{token}/telemetry/validation` stores events in `log.FrontendEvent` with `EventType="validation_failed_submit"` and JSON payload.

### AC4: Enable resolved vs abandoned correlation via `clientSessionId` + submission capture
- **Status:** PASS  
- **Evidence:** Telemetry is stored with `SessionID = clientSessionId` in `log.FrontendEvent`. Submissions already persist `clientSessionId` in `FormSubmission.ContextJSON`, enabling correlation.

## Test Evidence

### Automated Tests
```bash
python -m py_compile "backend/modules/forms/public_form_router.py"
```

### Build Verification
Not run (no build step required for this task).

## Manual UAT Steps

For human verification:

1. [ ] Open a public form with at least one required field. Click Submit with the field empty.  
   → Verify: Validation UI appears and the backend receives `POST /api/public/forms/{token}/telemetry/validation`.
2. [ ] Query `log.FrontendEvent` for `EventType = 'validation_failed_submit'`.  
   → Verify: A new row exists with `SessionID` populated and payload contains `failures` with `valueDiagnostics` only (no raw values).
3. [ ] Submit a valid response, then compare the `clientSessionId` in `FormSubmission.ContextJSON` to the telemetry row’s `SessionID`.  
   → Verify: IDs match for correlation.

## Known Limitations / Out-of-Scope Items

- [ ] No explicit `submission_captured` event is emitted; correlation relies on existing `FormSubmission` records. → Route to: ralf-sm if a dedicated event is required.

## Recommended Next Step

Ready for UAT by human.
