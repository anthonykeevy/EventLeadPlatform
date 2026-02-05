# UAT Checklist: T04

**Story:** 3.11  
**Task:** Frontend - Public Outbox (IndexedDB) + Client IDs  
**Generated:** 2026-02-04  

---

## Pre-conditions

- [ ] Frontend dev server is running
- [ ] Browser DevTools is open (Application + Console tabs)

## Test Steps

### AC1: IndexedDB outbox persists items across reload

- [ ] Step 1: In DevTools Console, run `await import('/src/features/renderer/outbox/publicOutbox.ts')` and call `enqueuePublicOutboxItem(...)`.
  - Verify: `eventlead_public_outbox` database exists with `publicOutbox` store.
- [ ] Step 2: Reload the page and call `listPublicOutboxItems()` from the imported module.
  - Verify: queued items still exist after reload.

### AC2: Status + retry fields update correctly

- [ ] Step 1: Force submission failure (e.g., invalid token) via `processPublicOutbox()`.
  - Verify: item transitions to `uploading` then `failed`, `retryCount` increments, `lastError` and `lastTriedAt` are set.
- [ ] Step 2: Provide a valid token and re-run `processPublicOutbox()`.
  - Verify: item transitions to `success`.

### AC3: Processor auto-runs when online and respects backoff

- [ ] Step 1: Call `registerPublicOutboxOnlineHandler()`; set DevTools Network to Offline.
  - Verify: processor does not run while offline.
- [ ] Step 2: Toggle back to Online.
  - Verify: processor runs on `online` and skips items until backoff elapses.

### AC4: Auth-free implementation

- [ ] Step 1: Inspect network request to `/api/public/forms/{token}/submissions`.
  - Verify: no auth headers or access tokens are attached.

## Regression Check

- [ ] No new console errors after loading public renderer pages.

## Post-conditions

- [ ] IndexedDB contains only expected outbox records (no unexpected writes).

## Edge Cases (if applicable)

- [ ] Multiple queued items process sequentially without concurrent runs.

---

**Instructions for Human Tester:**
1. Execute each step in order
2. Mark ✅ or ❌ for each item
3. Add notes for any failures
4. When complete, run `@ralf-uat *record-uat` with your results
