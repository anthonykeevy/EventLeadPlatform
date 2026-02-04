## UAT Checklist: T01 - Submission Contracts + Foundations

### Environment Setup
- [ ] Checkout branch `task/3.11/T01-submission-contracts-and-foundation`
- [ ] Ensure Node dependencies are installed: `cd frontend; npm install`
- [ ] Ensure Python env can run from `backend/` folder

### Verification Steps

- [ ] **AC1: Submission contract is defined (FE + BE)**
  - Step 1: Open `frontend/src/features/renderer/types/publicSubmission.types.ts` and verify `PublicFormSubmissionRequest` fields:
    - `idempotencyKey`, `submittedAtClient`, `answersByComponentId`, `context`
  - Step 2: Open `backend/modules/forms/public_submission_schemas.py` and verify `PublicFormSubmissionRequest` defines matching fields via aliases:
    - `idempotencyKey`, `submittedAtClient`, `answersByComponentId`, `context`
  - Step 3: Run `cd frontend; npm run build` -> Verify: build completes successfully (tsc + vite build).

- [ ] **AC2: Outbox item contract is defined**
  - Step 1: In `frontend/src/features/renderer/types/publicSubmission.types.ts`, verify `PublicOutboxItem` includes:
    - `outboxItemId`, `token`, `request`, `status`, `retryCount`, `createdAt`
    - Optional: `linkType`, `lastError`, `lastTriedAt`
  - Step 2: Verify the file comment explicitly references T04 as the IndexedDB implementation consumer.

- [ ] **AC3: Client identity contract is defined**
  - Step 1: Open `frontend/src/features/renderer/utils/clientIdentity.ts` and verify exports exist:
    - `getOrCreateClientDeviceId()`, `createNewClientSessionId()`, `createSubmitAttemptId()`
  - Step 2: Verify the doc comment states:
    - `clientDeviceId` is random UUID persisted locally (no fingerprinting)
    - `clientSessionId` rotates on page load and kiosk reset/new submission
    - `submitAttemptId` is per submit click

- [ ] **AC4: Value diagnostics exist (no raw values)**
  - Step 1: Run `cd frontend; npm run test:run -- src/features/renderer/utils/valueDiagnostics.test.ts`
    -> Verify: tests pass.
  - Step 2: Confirm `getValueDiagnostics("  test  ")` output includes only `type/length/trimmedLength/flags` and does **not** include the raw value.

### Regression Check
- [ ] Run `git diff --name-only origin/story/epic3-3.11-dynamic-submission...HEAD`
  -> Verify: no changes under:
  - `backend/migrations/`
  - `frontend/src/features/builder/`
  - `frontend/src/features/auth/`

### Cleanup
- [ ] None

