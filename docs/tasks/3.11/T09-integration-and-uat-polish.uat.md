# UAT Checklist: T09

**Story:** 3.11  
**Task:** Integration + UAT Polish (Scenarios 1–10)  
**Generated:** 2026-02-05

---

## Pre-conditions

- [ ] Backend server running locally
- [ ] Frontend running locally
- [ ] Form exists with required fields + Submit button
- [ ] Valid public form token available (`/forms/:token`)

## Test data (recommended)

- First Name (required)
- Last Name (required)
- Email (required)
- Submit button

---

## Scenarios (1–10)

### Scenario 1 — Online submit uploads immediately

- [ ] Step 1: Network online → Open `/forms/:token` → Fill required fields → Submit → Verify: success UI shown.
- [ ] Step 2: Verify public submission request sent; no "queued offline" notice; pending queue count stays 0.

### Scenario 2 — Offline submit is queued to IndexedDB

- [ ] Step 1: DevTools → Network → Offline → Reload `/forms/:token`.
- [ ] Step 2: Fill required fields → Submit → Verify: queued/offline confirmation shown.
- [ ] Step 3: Verify pending queue count increases by 1; no crash or lost input state.

### Scenario 3 — Queue survives reload

- [ ] Step 1: While offline, reload the page → Verify: queued submission still pending (count unchanged).

### Scenario 4 — Reconnect triggers auto-sync

- [ ] Step 1: Network online → wait up to 10s → Verify: syncing → success confirmation.
- [ ] Step 2: Verify pending queue count returns to 0 (or item marked success then cleaned).

### Scenario 5 — Backend down while “online” queues and later syncs

- [ ] Step 1: Keep network online; stop backend server.
- [ ] Step 2: Open `/forms/:token` → Submit valid form → Verify: submission queued on failure.
- [ ] Step 3: Start backend → wait up to 10s (or toggle offline/online) → Verify: queued item syncs.

### Scenario 6 — Idempotency (no duplicates on retry)

- [ ] Step 1: Go offline → Submit once (queue 1 item).
- [ ] Step 2: Go online → allow sync; toggle offline/online a few times during sync.
- [ ] Step 3: Verify server treats retries as safe; only one submission record per idempotency key.

### Scenario 7 — Invalid/expired token behavior

- [ ] Step 1: Use invalid or expired token → Attempt submit.
- [ ] Step 2: Verify UI shows clear error; submission not marked success.
- [ ] Step 3: If queued, it remains failed/pending with actionable error reason.

### Scenario 8 — Shared-device safety (values cleared after capture)

- [ ] Step 1 (online): Submit valid form → Verify: success UI and all fields cleared.
- [ ] Step 2 (offline): Network offline → Submit valid form → Verify: queued UI and all fields cleared.
- [ ] Optional: If kiosk reset enabled, verify countdown and clean state after delay.

### Scenario 9 — Validation-blocked telemetry (no raw values)

- [ ] Step 1: Leave required field empty (or invalid email) → Submit.
- [ ] Step 2: Verify validation errors shown; no submission queued.
- [ ] Step 3: Verify validation telemetry generated without raw values (network or DB log).

### Scenario 10 — Kiosk session rotation (optional)

- [ ] Step 1: Submit once successfully.
- [ ] Step 2: Start next submission cycle (auto-reset or New submission) → Submit again.
- [ ] Step 3: Verify second submission has different `clientSessionId` (same `clientDeviceId`).

---

## Pass/Fail Recording

- [ ] Scenario 1: ✅ / ❌
- [ ] Scenario 2: ✅ / ❌
- [ ] Scenario 3: ✅ / ❌
- [ ] Scenario 4: ✅ / ❌
- [ ] Scenario 5: ✅ / ❌
- [ ] Scenario 6: ✅ / ❌
- [ ] Scenario 7: ✅ / ❌
- [ ] Scenario 8: ✅ / ❌
- [ ] Scenario 9: ✅ / ❌
- [ ] Scenario 10: ✅ / ❌

---

## Notes / Issues Found

- 

---

**Instructions for Human Tester:**
1. Execute each scenario in order
2. Mark ✅ or ❌ for each step
3. Add notes for any failures
4. When complete, run `@ralf-uat *record-uat` with your results
