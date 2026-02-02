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

