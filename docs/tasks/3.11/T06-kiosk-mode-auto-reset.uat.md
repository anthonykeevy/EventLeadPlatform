# UAT Checklist: T06

**Story:** 3.11  
**Task:** Kiosk Mode (Optional) - Auto-reset + Countdown + Session Rotation  
**Generated:** 2026-02-04

---

## Pre-conditions

- [ ] Backend server is running
- [ ] Frontend is running
- [ ] Public renderer link is available

## Test Steps

### AC1: When `kiosk=1` and the user is inactive for `autoResetSeconds`, the form clears and validation state resets.
- [ ] Step 1: Open public link with `?kiosk=1&autoResetSeconds=10&countdownSeconds=5`  
  -> Verify: form clears after 10s of inactivity and validation UI resets.
- [ ] Step 2: Interact with a field, wait <10s, interact again  
  -> Verify: reset timer restarts (no reset at the original deadline).

### AC2: A visible countdown appears during the final `countdownSeconds` before reset.
- [ ] Step 1: Stop interacting after initial input  
  -> Verify: banner appears showing "Resetting in 5s…" (counts down).

### AC3: `clientSessionId` changes on kiosk reset (and on manual reset when kiosk mode enabled).
- [ ] Step 1: With kiosk enabled, trigger a reset (timeout or manual Reset)  
  -> Verify: submission context shows a new `clientSessionId` on the next interaction/submission.

### AC4: When kiosk mode is disabled, existing behavior is unchanged.
- [ ] Step 1: Open same public link without `kiosk=1`  
  -> Verify: no countdown banner, no auto-reset behavior.

## Regression Check

- [ ] Submit flow still works (success/queued notice appears)
- [ ] No console errors in browser
- [ ] No new backend errors in logs

## Post-conditions

- [ ] Form remains usable after reset and accepts new input

## Edge Cases (if applicable)

- [ ] If `countdownSeconds` > `autoResetSeconds`, countdown still caps to auto-reset window.

---

**Instructions for Human Tester:**
1. Execute each step in order
2. Mark ✅ or ❌ for each item
3. Add notes for any failures
4. When complete, run `@ralf-uat *record-uat` with your results
