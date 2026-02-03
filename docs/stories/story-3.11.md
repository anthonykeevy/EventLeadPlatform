# Story 3.11: Dynamic Submission (Outbox / Offline Queue + Sync)

**Epic:** Epic 3 - Form Builder & Logic Engine  
**Domain:** Rendering & Submission  
**Status:** 📋 Planned  
**Priority:** Critical (Hero feature: no lost leads)  
**Created:** 2026-02-02  
**Owner:** Developer Agent  

---

## 📖 User Story

**As a** form respondent (event attendee),  
**I want to** submit the public form even when the device is offline or the network is unreliable,  
**So that** leads are not lost at events and submissions reliably sync to the backend when connectivity returns.

**Context & entry point:**  
- Story 3.8 is complete: Public renderer loads and renders from stored `FormVersion.DefinitionJSON`.  
- Story 3.9 is complete: Builder preview uses token flow (`/forms/:token`) and stored definitions.  
- Story 3.8 currently performs client-side validation and produces an in-memory submission payload; **transport/outbox is deferred to this story**.

---

## 🧭 Scope Boundary (CRITICAL)

### In scope (Story 3.11)

- **Public submission transport** for `/forms/:token`:
  - On submit, run existing client-side validation and then **attempt network submission**.
  - If offline (or network fails), **queue submission locally** and confirm to the user.
- **Outbox (offline-first) queue**:
  - Store queued submissions in **IndexedDB** (not localStorage).
  - Support retry + safe queue processing when network restores.
  - Queue includes required metadata (token/formId/linkType, timestamp, idempotency key).
- **Sync behavior**:
  - When the browser fires `online`, automatically attempt to upload pending submissions.
  - Visible UI feedback: “Queued offline”, “Syncing…”, “Uploaded”.
- **Backend acceptance endpoint (minimal but real)**:
  - Add an unauthenticated public endpoint that accepts a submission payload **validated by token**.
  - Persist the submission in the database (minimal storage is acceptable: JSON payload + metadata).
  - Return a stable response that allows the client to mark an outbox item as synced.
- **Idempotency / duplicate protection (minimal)**:
  - Client supplies an idempotency key per submission.
  - Server treats repeated submits with same idempotency key as safe (no duplicate records).
- **Instrumentation / evidence support**:
  - Add/extend high-signal logging for: enqueue, sync attempt, success/failure reasons, and counts.
  - Keep logs safe (no PII in logs).

### Out of scope (Story 3.11)

- Advanced conflict resolution workflows (multi-device sync, merge UI, editing submissions).
- Admin/back-office workflows for reviewing submissions.
- Analytics dashboards for submission funnel and sync success rates.
- CRM integrations / exports.
- Full “lead domain” enrichment or dedupe logic beyond basic idempotency key protection.

---

## 🎯 Functional Requirements (High Level)

### FR-1: Public submission endpoint exists and is token-gated
- A public API endpoint exists that accepts submissions for a public form token.
- Token rules:
  - Invalid/expired token → safe 404/410-style response.
  - PREVIEW vs PRODUCTION linkType is preserved in submission metadata.
- Response includes a stable `submissionId` (or equivalent) to confirm sync success.

### FR-2: Client submits immediately when online
- When `navigator.onLine === true`, clicking submit triggers:
  - required validation (existing)
  - network `POST` attempt
  - success UI on `2xx`

### FR-3: Client queues when offline or network fails
- When offline (or fetch fails), submission is stored in IndexedDB with:
  - token + formId
  - answers payload
  - submittedAtClient timestamp
  - idempotency key
  - retryCount + lastError (for visibility)
- UI confirms “Saved offline. Will upload when online.”

### FR-4: Sync on reconnect (automatic) with retries
- When the device comes online:
  - outbox processes pending items (oldest-first).
  - items update status (pending → uploading → success/failed).
- Retry behavior is deterministic and bounded (max retries + backoff).

### FR-5: UX feedback is clear and non-blocking
- Submit button provides clear result:
  - Uploaded now (online)
  - Queued offline (offline/failure)
- Show pending count somewhere visible on public form experience (lightweight banner is sufficient).

### FR-6: Safety & resilience
- No crashes on submission failure.
- Queue survives refresh/reload.
- No PII leaked in logs.

### FR-7: Shared-device safety (clear-after-capture + optional kiosk auto-reset)
- After a submission is **uploaded** or **queued offline**, the form must **clear all field values immediately** so the next attendee does not see the previous attendee’s data.
- Post-submit UX should be **organiser-controlled** (per form/link setting), because some customers want kiosk behavior and others don’t.
- Two supported modes:
  - **Standard mode (default):** Show a confirmation state (“Uploaded” / “Saved offline”). Values are already cleared.
  - **Kiosk mode (optional):** Auto-reset back to a blank form after a customer-configured delay.
    - `autoResetSeconds` is configurable per form/link (no hard-coded “one size fits all”).
    - Show a visible countdown (“Resetting in 15s…”) so staff can verify capture before reset.
    - Optional secondary action: “New submission” (immediate reset) — keep subtle so it doesn’t confuse respondents.

### FR-8: Validation-blocked attempt telemetry (privacy-safe diagnostics)
- When a user clicks Submit but validation fails, record a **validation failure event** for diagnostics/analysis.
- Include:
  - token/linkType, clientDeviceId
  - `clientSessionId` + `submitAttemptId` so we can measure “resolved vs abandoned” (see below)
  - componentId + componentType
  - validation rule id/code/type (including customer-supplied rules), and error category (required/min/max/pattern/range/etc)
  - **value diagnostics (no raw value):** value type, length/trimmed length, and small “shape” flags (e.g., contains whitespace, contains plus, digit count bucket) so we can understand why rules are blocking
- Exclude:
  - raw field values (avoid persisting partial PII just because someone couldn’t submit)
- Optional future enhancement (explicit opt-in + retention policy): store a redacted/encrypted sample to help customers debug misconfigured custom rules.

**Resolved vs “could not resolve”**
- You can’t know intent directly, but you can infer outcomes:
  - **Resolved:** one or more `validation_failed_submit` events followed by a successful `submission_captured` (queued or uploaded) for the same `clientSessionId` (or within a short time window on the same `clientDeviceId`).
  - **Abandoned/unresolved:** validation failures with no subsequent `submission_captured` within a defined window, optionally confirmed by a `session_end` (page unload) event.
  - Track both: “validation failures” and “validation failures that lead to abandonment” (this is the metric you want for diagnosing bad custom rules).

**Kiosk nuance**
- In kiosk mode, multiple attendees can use the same open tab for hours. To avoid mixing analytics across attendees, `clientSessionId` must rotate on each reset/new submission cycle.

---

## ✅ Acceptance Criteria

1) **Immediate submit (online)**
- [ ] Submitting a valid form while online sends a network request and shows a success confirmation.
- [ ] The outbox remains empty after successful upload.

2) **Offline submit queues**
- [ ] Submitting while offline does not crash and stores the submission in IndexedDB.
- [ ] UI confirms the submission is queued offline.

3) **Auto-sync on reconnect**
- [ ] When network is restored, queued submissions are uploaded automatically.
- [ ] Successful uploads are removed from the pending queue (or marked success then cleaned up).

4) **Idempotency**
- [ ] Re-trying the same submission (same idempotency key) does not create duplicates server-side.

5) **Token validation**
- [ ] Invalid/expired token submissions are rejected safely and remain queued (or fail with clear status).

6) **Shared device safety**
- [ ] After a submission is queued or uploaded, the form values are cleared (no previous attendee data remains on screen).
- [ ] If kiosk mode is enabled, the form auto-resets after the configured delay and shows a countdown.

7) **Validation-blocked telemetry**
- [ ] Validation failures on submit generate telemetry that identifies the failing component/rule and includes value diagnostics (type/length/shape) without storing raw field values.

---

## 🔧 Technical Notes (Guidance)

### Reference architecture
- `docs/technical-guides/OFFLINE-LEAD-CAPTURE-ARCHITECTURE.md`

### Existing related implementation (do not re-invent)
- Public token resolution endpoint: `backend/modules/forms/public_form_router.py` (`GET /api/public/forms/{token}`)
- Public renderer entry: `frontend/src/features/renderer/pages/PublicFormRendererPage.tsx`
- Public runtime rendering + submit stub: `frontend/src/features/renderer/components/PublicFormArtboard.tsx`

### Important constraint
The existing `frontend/src/utils/offlineQueue.ts` is currently designed for **authenticated** users (requires `userId` from auth token). Public forms are **auth-free**, so Story 3.11 must either:
- Implement a dedicated **public outbox** queue (recommended), OR
- Extend `offlineQueue` to support an unauthenticated public mode without weakening security for authenticated queues.

---

## 🗄️ Response storage model (Database)

`docs/database-schema.md` currently has `dbo.Form` counters like `TotalSubmissions` and `LastSubmissionDate`, but it does **not** define a table to store individual form responses/submissions. For Story 3.11 to deliver “sync” (not just “queue”), we need a real persistence table.

### Recommended approach for dynamic component values

- **Store submissions as JSON** in a new `dbo.FormSubmission` table.
- **The form definition is the schema**: `FormVersion.DefinitionJSON` already describes each component’s `id`, `type`, and validation rules, so the backend can interpret the stored JSON later.
- This avoids a brittle “one column per field” design (impossible for a dynamic form builder).

### Proposed minimal table (Story 3.11 scope)

Create `dbo.FormSubmission` with (at minimum):
- `FormSubmissionID` (PK, BIGINT)
- `FormID` (FK → `dbo.Form`)
- `FormVersionID` (FK → `dbo.FormVersion`) — critical to interpret answers even if the form changes later
- `FormPublicLinkID` (FK → `dbo.FormPublicLink`) or `Token` (if we don’t want the FK)
- `LinkType` (`PREVIEW` / `PRODUCTION`)
- `IdempotencyKey` (NVARCHAR, **unique**) — prevents duplicates on retries / flaky networks
- `SubmittedAtClient` (DATETIME2)
- `ReceivedAtServer` (DATETIME2, default `GETUTCDATE()`)
- `AnswersJSON` (NVARCHAR(MAX), JSON) — the dynamic answer payload

Optional (keep lightweight for now):
- `ClientSubmissionID` (NVARCHAR) — stable client-side UUID for debugging
- `ContextJSON` (NVARCHAR(MAX)) — device/browser hints, without leaking PII into logs

**Database naming + standards (mandatory):**
- All new DB objects for this story must follow: `docs/database-naming-rules.md`
  - PascalCase tables/columns, `NVARCHAR` for text, standard audit columns, correct constraint/index naming.
  - Avoid enum/check-constraint “magic values” patterns; follow existing schema conventions.

### What does `AnswersJSON` look like?

Store a single JSON object keyed by **componentId** (the renderer already uses `Record<string, unknown>`):
- Text/email: JSON string
- Dropdown/radio: JSON string (selected option id/value)
- Checkbox: JSON array of strings
- Terms: JSON boolean
- Date: JSON object (current UI shape is `{ year, month, day }`), optionally also store a normalized ISO string for convenience
- Layout-only components (divider, submit button): not included

Example shape (illustrative):

```json
{
  "cmp_firstName": "Alice",
  "cmp_optIn": true,
  "cmp_interests": ["a", "c"],
  "cmp_birthDate": { "year": "2026", "month": "02", "day": "02" }
}
```

---

## 🛰️ Client context + device identification (observability)

Yes — we should include **client context** in Story 3.11 so we can:
- Identify **which laptop/device** produced which submissions
- Diagnose “one of 4 devices isn’t uploading” (by correlating failures/retries to a device)
- Detect likely “out-of-country” submissions (best-effort) for an AU-targeted form

### What to capture (recommended, privacy-safe)

**Client-generated (sent with submission):**
- `clientDeviceId` (UUID) — generated once per browser install and stored locally (IndexedDB/localStorage). **Do not fingerprint.**
- `clientSessionId` (UUID) — **per respondent session** (rotates on page load and on kiosk “reset/new submission” so multiple attendees on one device don’t share a session id)
- `clientTimezone` (e.g. `Australia/Sydney`)
- `clientLocale` (e.g. `en-AU`)
- `clientUserAgent` (string) + (if available) `userAgentData` brands/platform
- `clientScreen` (w×h, DPR) and `clientViewport` (w×h)
- `clientOnlineAtSubmit` (bool) + `effectiveConnectionType` (if available)
- `appVersion/buildSha` (from frontend build env) for “which version had the bug”

**Compatibility + UX signals (optional, still non-fingerprinting):**
- `clientPlatform` / `clientBrowser` / `clientBrowserVersion` (derived server-side from UA; store raw UA string)
- `clientDeviceClass` (desktop/tablet/mobile) (derived from UA + viewport)
- `clientOrientation` + `maxTouchPoints` (helps explain “works on laptop, broken on iPad”)
- `prefersColorScheme` / `prefersReducedMotion` (helps explain styling/accessibility differences)
- `deviceMemoryGb` / `hardwareConcurrency` (helps explain performance issues on low-end devices)
- `supportsIndexedDB` / `supportsServiceWorker` / `storageQuotaMb` (helps explain offline queue failures)
- `renderCanvasWidth` / `renderCanvasHeight` / `renderScaleAtSubmit` (helps diagnose “designed for Desktop but used on iPad”)

**Server-captured (derived at receipt time):**
- `receivedAtServer` (already part of submission)
- `requestIp` (optional; consider retention policy / hashing) and/or `ipCountryCode` (preferred)

> Note on “other countries”: timezone/locale are only **signals**. If you truly need “country”, the backend should derive and store **`ipCountryCode`** using IP geolocation (or store IP for later offline analysis). This is personal data in many jurisdictions, so we should keep it minimal and document retention.

### How this helps the “4 laptops” case

- Every submission row includes `clientDeviceId`, so you can group submissions by device.
- If one laptop is failing to sync, its submissions will show repeated retries/late upload times tied to that deviceId.
- Optional extension (still small): add a **device heartbeat** endpoint that pings `clientDeviceId + token + outboxPendingCount` when online, so you can see “Device A last seen 2 days ago with 12 pending”.

---

## 🧩 Deferred UI wiring (future stories)

These features are enabled by Story 3.11 telemetry/persistence, but the **UI surfacing** can be delivered incrementally in later stories:

- **Telemetry storage (so the dashboard can query it)**
  - Store validation-failure events in a **queryable table** (recommended: `log.FormValidationEvent` or reuse an existing `log.FrontendEvent` table if present).
  - Minimum columns for fast dashboard queries: `FormID`, `OccurredAtServer`, `EventType`, `LinkType`, `ClientDeviceId`, plus `EventPayloadJSON` for details.
  - Index recommendation: `(FormID, OccurredAtServer)` and `(FormID, EventType, OccurredAtServer)`.
  - Retention: keep raw events for a bounded window (e.g., 30–180 days). If longer-term trends are needed, add a roll-up table later.

- **Form dashboard card**
  - Show **validation-blocked count** (e.g., last 24h / 7d) and top failing fields/rules
  - Distinguish **resolved vs abandoned** validation failures (derived from `validation_failed_submit` → `submission_captured` correlations)
  - Show submission health: uploaded vs queued vs failed retries
- **Form settings (organiser)**
  - Kiosk mode toggle + `autoResetSeconds` configuration + countdown enable/disable
  - Optional “diagnostics mode” toggle (only if we later decide to persist richer validation samples with explicit consent + retention policy)
- **Compatibility insights**
  - Breakdown submissions by browser/OS/viewport/deviceClass to inform canvas/profile choices
  - Flag high-error combos (e.g., a spike on Safari iPad) for support + product fixes

## 🔗 Dependencies

### Upstream
- Story 3.8: Public renderer (✅ Complete)
- Story 3.9: Builder persistence + token preview flow (✅ Complete)

### Downstream
- Future epics: Lead processing, analytics, reporting, CRM/export

---

## ✅ Done Criteria

Story 3.11 is complete when:
- [ ] All Acceptance Criteria pass.
- [ ] `docs/stories/STORY-3.11-UAT-TEST-GUIDE.md` is executed and marked ✅ PASSED.
- [ ] Submission UX is reliable offline-first (no lost submissions during UAT scenarios).
- [ ] Implementation is committed to a Story branch with a PR and merged cleanly to `master`.

---

## 🧪 UAT Test Guide (TBD)

See: `docs/stories/STORY-3.11-UAT-TEST-GUIDE.md`

---

## 📝 Completion Report (TBD)

To be filled when Story 3.11 is completed (evidence, files changed, and UAT results).

---

*Story created by Scrum Master Agent (with Git discipline enforced)*  
*Last Updated: 2026-02-02*

