# Story 3.11 UAT Test Guide — Dynamic Submission (Outbox / Offline Queue + Sync)

**Story:** 3.11  
**Scope:** Public form submission transport + offline outbox + sync  
**Status:** ✅ PASSED (executed 2026-02-05)  

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

### Scenario 8 - Shared-device safety (values cleared after capture)

Goal: Ensure previous attendee data is not left on screen after submit.

Steps (online):
1. Ensure network is online.
2. Open /forms/:token.
3. Enter realistic values in all fields.
4. Click Submit.

Expected:
- Submission is uploaded successfully (success UI).
- All form fields are cleared (no previous attendee values remain visible).

Steps (offline queue):
1. Set DevTools -> Network -> Offline.
2. Reload /forms/:token.
3. Enter values.
4. Click Submit.

Expected:
- Submission is queued (offline confirmation UI).
- All form fields are cleared after the queue capture.

Optional (if kiosk auto-reset is enabled for this form/link):
- A visible countdown is shown and the form returns to a clean state after the configured delay.

---

### Scenario 9 - Validation-blocked telemetry (no raw values)

Goal: Validate that validation failures are observable and don't create fake submissions.

Steps:
1. Ensure network is online.
2. Open /forms/:token.
3. Leave at least one required field empty (or enter an invalid email format).
4. Click Submit.

Expected:
- UI shows validation errors and submission is blocked.
- No submission is queued (pending queue count does not increase).
- Validation telemetry is generated (componentId + rule/category + value diagnostics), without raw values.

How to verify telemetry (implementation-dependent):
- Inspect Network requests for a validation event call, OR
- Inspect DB log table (e.g. log.FormValidationEvent) for an inserted event.

---

### Scenario 10 - Kiosk session rotation (optional)

Goal: In kiosk usage, multiple attendees on one device should not share a single session id.

Steps (if kiosk reset/new submission is enabled):
1. Submit once successfully.
2. Start the next submission cycle (auto-reset or New submission).
3. Submit again.

Expected:
- The second submission has a different clientSessionId than the first (same clientDeviceId).

---

## Pass/Fail Recording

Mark each scenario:
- [x] Scenario 1: ✅ PASS
- [x] Scenario 2: ✅ PASS
- [x] Scenario 3: ✅ PASS
- [x] Scenario 4: ✅ PASS
- [x] Scenario 5: ✅ PASS
- [x] Scenario 6: ✅ PASS
- [x] Scenario 7: ✅ PASS
- [x] Scenario 8: ✅ PASS
- [x] Scenario 9: ✅ PASS
- [x] Scenario 10: ✅ PASS

---

## Notes / Issues Found

- None.
- Evidence highlights:
  - Idempotency: `POST /api/public/forms/{token}/submissions` returned `{ status: "DUPLICATE" }` for replay attempts with the same idempotency key.
  - Validation telemetry: Network request observed to `/api/public/forms/{token}/telemetry/validation`.
  - Kiosk rotation: same `clientDeviceId` with different `clientSessionId` across two submissions.

