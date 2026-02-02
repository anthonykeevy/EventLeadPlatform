# Story 3.11 UAT Test Guide — Dynamic Submission (Outbox / Offline Queue + Sync)

**Story:** 3.11  
**Scope:** Public form submission transport + offline outbox + sync  
**Status:** 📋 Planned (to be executed during Story 3.11)  

---

## Preconditions

- Backend is running locally
- Frontend is running locally
- You have at least one form with:
  - A Submit button component
  - At least one required field
- You can generate a **public token** for the form (PREVIEW or PRODUCTION) and open:
  - `/forms/:token`

---

## Test data (recommended)

Use a small form:
- First Name (required)
- Last Name (required)
- Email (required)
- Submit button

---

## Evidence capture (agent-owned; minimal for human)

If the agent asks for evidence:
- Download the Builder “Dev Logs” JSON bundle (if enabled) and attach it.
- Provide a screenshot of the success/offline banner (if requested).

---

## Scenarios

### Scenario 1 — Online submit uploads immediately

**Goal:** Validate direct upload path when online.

Steps:
1. Ensure network is online.
2. Open `/forms/:token`.
3. Fill required fields with valid values.
4. Click Submit.

Expected:
- UI shows a success confirmation.
- Network request is sent to the public submission endpoint.
- No “queued offline” message is shown.
- Pending queue count remains 0.

---

### Scenario 2 — Offline submit is queued to IndexedDB

**Goal:** Validate offline-first behavior.

Steps:
1. Open Chrome DevTools → Network → set **Offline**.
2. Reload `/forms/:token`.
3. Fill required fields with valid values.
4. Click Submit.

Expected:
- UI confirms submission was saved offline / queued.
- Pending queue count increases by 1.
- No crash / no lost input state.

---

### Scenario 3 — Queue survives reload

Steps:
1. While still offline, reload the page.

Expected:
- The queued submission is still pending (count unchanged).

---

### Scenario 4 — Reconnect triggers auto-sync

Steps:
1. Turn network back **Online**.
2. Wait up to 10 seconds.

Expected:
- UI shows syncing state and then success confirmation.
- Pending queue count decreases to 0 (or item is marked success then cleaned up).

---

### Scenario 5 — Backend down while “online” queues and later syncs

Steps:
1. Keep network online, but stop the backend server.
2. Open `/forms/:token`.
3. Submit a valid form.
4. Start the backend server again.
5. Wait up to 10 seconds or toggle offline/online once.

Expected:
- Submission is queued when upload fails.
- Once backend is available, queued item syncs successfully.

---

### Scenario 6 — Idempotency (no duplicates on retry)

**Goal:** Ensure retries do not create multiple server records.

Steps:
1. Go offline.
2. Submit once (queues 1 item).
3. Go online and allow sync.
4. Repeat “online/offline” toggling a few times during sync (simulate flaky network).

Expected:
- The server treats repeated attempts with the same idempotency key as safe.
- Only one submission record exists per idempotency key.

---

### Scenario 7 — Invalid/expired token behavior

Steps:
1. Use an invalid token (or revoke/expire a token).
2. Attempt to submit.

Expected:
- The UI shows a clear error.
- Submission is not silently marked as success.
- If queued, it remains failed/pending with an actionable error reason.

---

## Pass/Fail Recording

Mark each scenario:
- [ ] Scenario 1: ✅ / ❌
- [ ] Scenario 2: ✅ / ❌
- [ ] Scenario 3: ✅ / ❌
- [ ] Scenario 4: ✅ / ❌
- [ ] Scenario 5: ✅ / ❌
- [ ] Scenario 6: ✅ / ❌
- [ ] Scenario 7: ✅ / ❌

---

## Notes / Issues Found

- 

