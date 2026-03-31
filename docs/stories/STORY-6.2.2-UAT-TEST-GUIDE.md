# Story 6.2.2 — UAT Test Guide

**Story:** 6.2.2 — File Upload Component (Full Stack)  
**Worktree:** `C:\wt\elp\story-epic6-6.2.2-file-upload-full-stack`  
**Branch:** `story/epic6-6.2.2-file-upload-full-stack`

### UAT execution record (2026-03-31)

| Section | Scope | Result |
|---------|--------|--------|
| **§1** | Builder — toolbox, canvas, properties, form-validate | **PASS** |
| **§2** | Runtime — upload, submit, DB bind | **PASS** |
| **§3** | Negative cases (size, types, foreign session / fake id) | **PASS** |
| **§4** | Company download (product UX) | **DEFERRED** → **Epic 8** |
| **§5** | Regression sniff | **PASS** |

Detailed matrix and sign-off: **`STORY-6.2.2-UAT-RESULTS.md`**.  
Automated lint, unit tests, and Story 622 pytest module: **`STORY-6.2.2-GATE-EVIDENCE.md`**.

---

## 0) Preconditions

| Step | Action |
|------|--------|
| 0.1 | `git pull` story branch; DB migrated per Dev closeout (Anthony ran Alembic upgrade). |
| 0.2 | Backend + frontend running per usual dev docs. |
| 0.3 | A **published** form with public link token (prod or preview per test case). |

Record environment (URLs, form id, token suffix) in `STORY-6.2.2-UAT-RESULTS.md`.

**Published definition vs builder changes:** A **production** public link always loads the form version that is **`IsActive`** (last successful **publish**). Edits in the builder usually live on a **DRAFT** version until you publish again—upload rules like “allowed types” come from that JSON, so **changes made after publish are not visible on production until you republish** the version that contains them. A **preview** link, by contrast, resolves the **highest version number** for the form (often the latest draft), so behaviour can differ from production until draft and active versions match.

---

## 1) Builder — toolbox & canvas

| ID | Steps | Expected |
|----|-------|----------|
| 1.1 | Open builder → toolbox | **File upload** appears under Input (or agreed category). |
| 1.2 | Drag onto canvas | Component renders with label + upload affordance + validation region. |
| 1.3 | Properties: set accept to `.pdf`, max size small (e.g. 1MB), single file | Values persist after save/reload. |
| 1.4 | Save definition; run `POST /api/form-validate` (Swagger/Postman) with `file-upload` | **200** / valid. |

---

## 2) Runtime — upload & submit (happy path)

| ID | Steps | Expected |
|----|-------|----------|
| 2.1 | Open public URL with token | Form renders; file control works. |
| 2.2 | Choose valid file (within type/size) | Upload completes; UI shows file name; DevTools shows attachment id response. |
| 2.3 | Submit form | **ACCEPTED**; submission id returned. |
| 2.4 | DB or admin UI (if available) | `FormSubmission` row exists; attachment row(s) have **same** `FormSubmissionID` (not null). |

---

## 3) Negative & abuse (sampling)

| ID | Steps | Expected |
|----|-------|----------|
| 3.1 | Upload file over max size | Clear error; no orphan or orphaned row documented. |
| 3.2 | **First** set **Allowed file types** to a narrow rule (e.g. `.pdf` only). **Then** upload a file that does not match (e.g. `.txt` or `.png`). | Rejected with a clear error. (**Note:** if allowed types is **left blank**, any type is allowed—only max size applies, so this test needs an explicit restriction.) |
| 3.3 | Craft submit payload referencing **foreign** attachment id (from another session or fake uuid) | **Rejected** or validation error (per AC-3). |

**Automated coverage (backend):** After migration 051, from `backend`: `python -m pytest tests/test_story_622_file_upload.py -v -k "reject_fake or reject_cross"` exercises a **fake UUID** on submit (`422`) and an attachment uploaded in **session A** submitted with **session B** (`422`). Full file also runs happy path, dedupe, and download.

**Manual 3.3 (optional):** In DevTools, copy the JSON body your browser would send for submit; replace the file-upload answer value with a random GUID that was never returned from `POST .../attachments`, or with an `attachmentId` from another browser tab’s session. Expect submit to fail with a validation-style error (`422`).

---

## 4) Company download

**UAT for this section is deferred to Epic 8** (in-app / customer-grade attachment retrieval). Story 6.2.2 delivers the authenticated download **API**; Epic 8 should own the UX and gate evidence for end-user download.

| ID | Steps | Expected (Epic 8) |
|----|-------|-------------------|
| 4.1 | Company user opens submission / lead and downloads attachment(s) | Correct file + filename from product UI. |
| 4.2 | User **without** access | 403/404. |

### Appendix — API-only check (optional, pre–Epic 8)

Supporting engineering verification (not the customer path):

1. **Confirm the submission**  
   After a successful public submit (step 2.3), locate the `FormSubmission` row. In **`AnswersJSON`**, the file-upload component’s value is the **`attachmentPublicId`** (GUID, or array of GUIDs if multi-file).

2. **Call the download endpoint**  
   `GET /api/forms/{formId}/attachments/{attachmentPublicId}/content` with `Authorization: Bearer <token>` for a user with access to that form.

3. **Verify**  
   **HTTP 200**, body matches uploaded bytes, `Content-Disposition` includes original filename.

4. **Swagger**  
   Authorize, then try the GET with the same ids.

5. **Errors**  
   Invalid/unbound id → **404**; no permission → **403** (see Epic 8 for product messaging).

---

## 5) Regression sniff

| ID | Steps | Expected |
|----|-------|----------|
| 5.1 | Form with **only** text + submit | Still submits. |
| 5.2 | Existing url/rating/paragraph fields | Unchanged behaviour. |

---

## 6) Evidence

- **UAT matrix and sign-off:** `docs/stories/STORY-6.2.2-UAT-RESULTS.md`  
- **Automated gates (lint, unit tests, Story 622 pytest):** `docs/stories/STORY-6.2.2-GATE-EVIDENCE.md`  
- Optional: screenshots or HTTP logs appended under §6 in `STORY-6.2.2-UAT-RESULTS.md`.
