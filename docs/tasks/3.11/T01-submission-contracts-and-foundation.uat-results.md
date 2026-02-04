# UAT Results: T01 - Submission Contracts + Foundations

**Story:** 3.11 - Dynamic Submission (Outbox)  
**Task:** T01 - Submission Contracts + Foundations  
**Tester:** Anthony Keevy  
**Date:** 2026-02-03  
**Overall Result:** ❌ FAIL  

---

## Summary
AC2, AC3, and AC4 passed. AC1 step 3 failed because `cd frontend; npm run build` produced many TypeScript errors, blocking the “TS builds” verification step.

---

## Step Results

| AC | Step | Result | Evidence |
|----|------|--------|----------|
| AC1 | Step 1 | ✅ PASS | Verified `PublicFormSubmissionRequest` fields in `frontend/src/features/renderer/types/publicSubmission.types.ts` |
| AC1 | Step 2 | ✅ PASS | Verified Pydantic aliases match contract in `backend/modules/forms/public_submission_schemas.py` |
| AC1 | Step 3 | ❌ FAIL | `cd frontend; npm run build` failed with many TS errors (see excerpt below) |
| AC2 | Step 1–2 | ✅ PASS | Verified `PublicOutboxItem` contract + T04 reference comment in `frontend/src/features/renderer/types/publicSubmission.types.ts` |
| AC3 | Step 1–2 | ✅ PASS | Verified `getOrCreateClientDeviceId`, `createNewClientSessionId`, `createSubmitAttemptId` in `frontend/src/features/renderer/utils/clientIdentity.ts` |
| AC4 | Step 1–2 | ✅ PASS | Verified `cd frontend; npm run test:run -- src/features/renderer/utils/valueDiagnostics.test.ts` passes and confirms no raw values are emitted |

---

## Defects (Acceptance Criteria Violations)

| ID | Type | AC | Description | Severity | Status |
|----|------|----|-------------|----------|--------|
| D1 | DEFECT | AC1 | Frontend `npm run build` fails with TypeScript errors, preventing AC1 step 3 verification. | Blocker | Open |

### Evidence (D1)

Command:
```powershell
cd frontend
npm run build
```

Observed result: build fails with many TypeScript errors (excerpt):
```text
src/features/forms/pages/FormsPage.tsx(23,10): error TS6133: 'formApprovalStatuses' is declared but its value is never read.
src/features/forms/pages/FormsPage.tsx(44,11): error TS2339: Property 'showToast' does not exist on type '{ success: ... }'.
src/features/forms/pages/FormsPage.tsx(229,29): error TS2322: Type '"large"' is not assignable to type '"sm" | "md" | "lg" | "xl" | undefined'.
src/features/renderer/components/PublicFormArtboard.tsx(177,9): error TS2345: Argument of type '{ dateFormat: string | undefined; }' is not assignable to parameter of type 'ValidationContext'.
Object literal may only specify known properties, and 'dateFormat' does not exist in type 'ValidationContext'.
```

Notes:
- This appears to be a **pre-existing build health issue** (not necessarily caused by T01 changes), but it still blocks the required verification step for this task.

---

## Out-of-Scope / Enhancements
None recorded during this UAT.

---

## Automation Opportunities
- Add/restore a CI gate (or a local preflight script) that ensures `cd frontend; npm run build` is green before any task requiring “TS builds” can be marked ✅ HumanDone.

---

## Handoff
Since UAT is **❌ FAIL**, route back to **Ralf-Dev** to address defect D1 (restore frontend build health) and then re-run this UAT.

