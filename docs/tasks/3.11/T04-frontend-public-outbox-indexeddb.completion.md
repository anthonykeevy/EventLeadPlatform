# Task Completion: T04

**Story:** 3.11  
**Task:** Frontend - Public Outbox (IndexedDB) + Client IDs  
**Completed:** 2026-02-04  
**Status:** Complete (implementation)  

---

## Summary of Changes

Implemented an auth-free public outbox backed by IndexedDB, with deterministic retry/backoff and a minimal public submission API helper. Updated task plan/status docs for Story 3.11.

## Files Changed

| File | Change | Reason |
|------|--------|--------|
| `frontend/src/features/renderer/outbox/publicOutboxRetry.ts` | Created | Deterministic backoff helpers |
| `frontend/src/features/renderer/outbox/publicOutbox.ts` | Created | IndexedDB outbox + processor |
| `frontend/src/features/renderer/api/publicSubmissionApi.ts` | Created | Auth-free submission POST helper |
| `docs/tasks/3.11/T04-frontend-public-outbox-indexeddb.md` | Modified | Mark task complete |
| `docs/tasks/3.11/TASK-PLAN.md` | Modified | Mark T04 complete |
| `docs/tasks/3.11/STATUS.md` | Created | Story task status snapshot |

## Acceptance Criteria Verification

### AC1: IndexedDB outbox persists items across reload
- **Status:** PARTIAL (implemented; manual verification pending)
- **Evidence:** `publicOutbox.ts` initializes `eventlead_public_outbox` and supports enqueue/list on `publicOutbox` store.

### AC2: Status + retry fields update correctly
- **Status:** PASS (code-level)
- **Evidence:** `processPublicOutbox()` sets `uploading`, and on failure sets `failed`, increments `retryCount`, sets `lastError` + `lastTriedAt`, and on success sets `success`.

### AC3: Processor auto-runs when online and respects backoff
- **Status:** PARTIAL (implemented; manual verification pending)
- **Evidence:** `registerPublicOutboxOnlineHandler()` hooks `window.online` and `shouldAttemptOutboxItem()` enforces backoff.

### AC4: Auth-free implementation
- **Status:** PASS (code-level)
- **Evidence:** `submitPublicFormSubmission()` uses only `fetch` with JSON body and no auth headers.

## Test Evidence

### Automated Tests
```bash
cd frontend
npm run lint
npm run build
```

Output (errors pre-existing in repo):
- ESLint failed: no ESLint config found in `frontend/` path.
- `npm run build` failed with numerous TypeScript errors in existing files (builder/auth/dashboard/etc.).

## Manual UAT Steps

For human verification:

1. [ ] Run frontend dev server.
2. [ ] In DevTools Console, run:
   - `await import('/src/features/renderer/outbox/publicOutbox.ts')` and call `enqueuePublicOutboxItem(...)`
   - Verify: `eventlead_public_outbox` DB and `publicOutbox` store exist.
3. [ ] Refresh the page and call `listPublicOutboxItems()` from the imported module.
   - Verify: previously enqueued items persist across reload.
4. [ ] Toggle DevTools Network Offline/Online.
   - Verify: `processPublicOutbox()` runs on `online`, and items respect backoff timing.

## Known Limitations / Out-of-Scope Items

- Lint/build failures exist in unrelated areas of the repo (see Test Evidence). Not addressed in this task.
- Renderer submit wiring is handled in T05.

## Recommended Next Step

Blocked - repo-wide lint/build failures need baseline clarification or fixes before full verification.
