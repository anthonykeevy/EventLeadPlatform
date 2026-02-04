# Task T01 Completion Note: Submission Contracts + Foundations

**Story:** 3.11 - Dynamic Submission (Outbox)  
**Task ID:** T01  
**Branch:** `task/3.11/T01-submission-contracts-and-foundation`  
**Date:** 2026-02-03  

## Summary
Defined the canonical **public submission** and **validation telemetry** contracts (TypeScript + Pydantic), plus the **public outbox record** contract and foundational helpers for **client identity** + **privacy-safe value diagnostics**.

## Scope / Forbidden Zones Check
- **No DB migrations** were created or modified (`backend/migrations/` untouched).
- **No Builder changes** (`frontend/src/features/builder/` untouched).
- **No Auth changes** (`frontend/src/features/auth/` untouched).

## Files Changed
### Created
- `frontend/src/features/renderer/types/publicSubmission.types.ts`
- `frontend/src/features/renderer/types/telemetry.types.ts`
- `frontend/src/features/renderer/utils/clientIdentity.ts`
- `frontend/src/features/renderer/utils/valueDiagnostics.ts`
- `frontend/src/features/renderer/utils/valueDiagnostics.test.ts`
- `backend/modules/forms/public_submission_schemas.py`

### Modified
- `docs/tasks/3.11/LESSONS-LEARNED.md`

## Acceptance Criteria Verification

### AC1: Submission contract is defined (FE + BE)
**Result:** ✅ Contract defined; ⚠️ full “TS builds” verification is **blocked** by pre-existing TypeScript errors in the repo.

**Evidence (contract match):**
- Frontend types: `frontend/src/features/renderer/types/publicSubmission.types.ts`
  - `PublicFormSubmissionRequest`: `idempotencyKey`, `submittedAtClient`, `answersByComponentId`, `context`
  - `PublicSubmissionContext`: `clientDeviceId`, `clientSessionId`, `submitAttemptId`, plus optional client context fields
  - `PublicFormSubmissionResponse`: `submissionId`, `status`
- Backend Pydantic: `backend/modules/forms/public_submission_schemas.py`
  - `PublicFormSubmissionRequest` / `PublicFormSubmissionResponse` use **field aliases** to match the TS contract (camelCase in JSON).

**Evidence (frontend build attempt):**

```text
Command:
  cd frontend; npm run build

Result:
  FAILED (pre-existing tsc errors unrelated to renderer submission contracts)

Example errors (excerpt):
  src/features/forms/pages/FormsPage.tsx(23,10): error TS6133: 'formApprovalStatuses' is declared but its value is never read.
  ...
  src/features/renderer/components/PublicFormArtboard.tsx(177,9): error TS2345: Argument of type '{ dateFormat: string | undefined; }' is not assignable to parameter of type 'ValidationContext'.
```

➡️ **Route/Blocker:** A separate build-stabilization task is needed to restore `npm run build` to green before this AC can be fully satisfied.

### AC2: Outbox item contract is defined
**Result:** ✅ Contract defined.

**Evidence:**
- `frontend/src/features/renderer/types/publicSubmission.types.ts` defines:
  - `PublicOutboxStatus`: `'pending' | 'uploading' | 'failed' | 'success'`
  - `PublicOutboxItem`: `outboxItemId`, `token`, `linkType?`, `request`, `status`, `retryCount`, `lastError?`, `createdAt`, `lastTriedAt?`
- File includes a comment explicitly tying this contract to **T04**.

### AC3: Client identity contract is defined
**Result:** ✅ Contract defined.

**Evidence:**
- `frontend/src/features/renderer/utils/clientIdentity.ts` exports:
  - `getOrCreateClientDeviceId(): string` (stable random UUID persisted in localStorage; no fingerprinting)
  - `createNewClientSessionId(): string` (documented to rotate on page load + kiosk reset)
  - `createSubmitAttemptId(): string` (per submit click)

### AC4: Value diagnostics exist (no raw values)
**Result:** ✅ Implemented + verified.

**Evidence (unit test):**

```text
Command:
  cd frontend; npm run test:run -- src/features/renderer/utils/valueDiagnostics.test.ts

Result:
  PASS (2 tests)
```

The test asserts `getValueDiagnostics("  test  ")` returns lengths/flags and that the serialized diagnostics do **not** contain `"test"`.

## Test / Verification Evidence

### Frontend
- **Build (required by task spec):** `cd frontend; npm run build` → **FAILED** due to pre-existing TypeScript errors (see AC1).
- **Unit test (AC4 evidence):** `cd frontend; npm run test:run -- src/features/renderer/utils/valueDiagnostics.test.ts` → **PASS**.

### Backend
Run from `backend/` to match module import expectations:

```text
Commands:
  cd backend
  python -c "from main import app; print('main import ok')"
  python -c "from modules.forms.public_submission_schemas import PublicFormSubmissionRequest; print('public_submission_schemas import ok')"

Result:
  PASS (imports succeed)
```

## Manual UAT Steps (quick)
1. Compare the FE/BE submission payload fields:
   - `frontend/src/features/renderer/types/publicSubmission.types.ts`
   - `backend/modules/forms/public_submission_schemas.py` (aliases)
2. Confirm client identity helper docs describe session rotation (kiosk-safe) in `frontend/src/features/renderer/utils/clientIdentity.ts`.
3. Confirm telemetry contract excludes raw values:
   - `frontend/src/features/renderer/types/telemetry.types.ts` references `ValueDiagnostics` only
4. Run `cd frontend; npm run test:run -- src/features/renderer/utils/valueDiagnostics.test.ts` and confirm ✅ pass.

## Known Limitations / Out of Scope
- ⚠️ **Blocked:** `npm run build` currently fails due to unrelated, pre-existing TS errors across the repo. Fixing those is **out of scope for T01**.
- No public submission endpoint wiring (T03).
- No IndexedDB outbox implementation (T04).
- No renderer submit behavior changes (T05+).
- No DB migration work (T02).

## Recommended Next Step
**Blocked - needs ralf-sm attention**: create a small task to restore a green frontend build (`cd frontend; npm run build`) so AC1/AC2 can be fully verified on CI and locally.

