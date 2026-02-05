# UAT Checklist: T05

**Story:** 3.11  
**Task:** Renderer Integration - Submit → Upload/Queue + Clear-after-capture  
**Generated:** 2026-02-04

---

## Pre-conditions

- [ ] Backend server running with T03 endpoint available
- [ ] Frontend running
- [ ] Valid public form token exists
- [ ] Form has at least one required field

## Test Steps

### AC1: Renderer submit validates before capture

- [ ] Step 1: Open public form link → Leave required field empty → Click Submit → Verify: validation errors shown and no submission occurs.

### AC2: Online submit uploads immediately with success UX

- [ ] Step 1: Ensure browser is online → Fill valid inputs → Click Submit → Verify: success notice appears and inputs clear.
- [ ] Step 2: Verify backend received submission (DB row exists) and no outbox item remains pending.

### AC3: Offline/failure enqueues with queued UX

- [ ] Step 1: Set DevTools network to Offline → Fill valid inputs → Click Submit → Verify: queued notice appears and inputs clear.
- [ ] Step 2: Inspect IndexedDB `eventlead_public_outbox` → Verify: new pending item exists with same idempotencyKey.

### AC4: Clear values after capture (upload or queue)

- [ ] Step 1: After online submit → Verify: all inputs cleared and session reset.
- [ ] Step 2: After offline submit → Verify: all inputs cleared and session reset.

### AC5: Idempotency key generated once per capture

- [ ] Step 1: Capture submission (online or offline) → Inspect request/outbox → Verify: single idempotencyKey per capture.
- [ ] Step 2: If queued, retry upload → Verify: same idempotencyKey is used.

## Regression Check

- [ ] Preview helper (validate/reset) still works for embed mode
- [ ] No new console errors during submit flow

## Post-conditions

- [ ] Outbox pending items (if any) eventually transition to success once online

## Edge Cases

- [ ] Double-click submit → Verify: only one submission is captured

---

**Instructions for Human Tester:**
1. Execute each step in order
2. Mark ✅ or ❌ for each item
3. Add notes for any failures
4. When complete, run `@ralf-uat *record-uat` with your results
