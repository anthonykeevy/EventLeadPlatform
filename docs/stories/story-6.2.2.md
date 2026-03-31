# Story 6.2.2 — File Upload Component (Full Stack)

**Epic:** 6 — AI Generation & Monetization Engine  
**Story ID:** 6.2.2  
**Title:** File Upload Component (Full Stack)  
**Status:** 🔄 Phase 1 complete — ready for Dev implementation  
**Branch:** `story/epic6-6.2.2-file-upload-full-stack`  
**PR:** [#55](https://github.com/anthonykeevy/EventLeadPlatform/pull/55) (Draft)  
**Depends On:** Story 6.2.1 (✅ Complete)  
**Blocks:** Story 6.3 (AI Context Uplift & Benchmark Baseline)  
**Created:** 2026-03-30  
**Sources:** `EPIC-6-STATUS.md`, `story-6.2.1.md` (deferred file-upload), `STORY-6.2-BENCHMARK-FORMS.md`

---

## 1) Goal

Deliver a first-class **`file-upload`** component across the **builder**, **public runtime**, and **backend**: anonymous end-users can upload files under a published form token, submissions reference **submission-scoped** attachment IDs (no cross-submission or cross-form leakage), and **company-authenticated** users can **securely download** attachments for leads they are allowed to see.

---

## 2) In Scope

### 2.1 Builder (frontend)

| Area | Requirement |
|------|-------------|
| **Type** | Add `'file-upload'` to `ComponentType` and backend `ComponentType` enum (`file-upload` string value, consistent with kebab-case types). |
| **Registry** | Full `ComponentDefinition`: toolbox, structure defaults, drag preview, canvas preview, runtime renderer. |
| **Properties** | `accept` / `acceptedFileTypes` (MIME or extension list), `maxFileSizeBytes` (or MB prop + normalize), **`allowMultiple`** (default **`false`**), **`maxFiles`** when multiple is on, labels/help. |
| **Validation** | Required / min-max files at submit time; client-side pre-checks (size/type) before upload. |
| **Product note** | **Default single file per component** keeps simple forms simple; authors enable **multiple** for “résumé + cover letter” style flows (common in general-purpose builders: JotForm-style `allowMultiple` + cap). Extra files can always be gathered by **adding another** `file-upload` component. |

### 2.2 Public runtime (frontend)

| Area | Requirement |
|------|-------------|
| **UX** | Upload control(s) matching builder props; show file name + remove; handle errors (type/size/network). |
| **Flow** | **Two-phase**: (1) upload file(s) via **token-scoped** public API → receive **attachment ID(s)**; (2) include those IDs in `answersByComponentId` when posting `POST .../submissions`. |

### 2.3 Public API (backend)

| Area | Requirement |
|------|-------------|
| **Upload** | New authenticated-by-token endpoint(s) under existing public forms router, e.g. `POST /api/public/forms/{token}/attachments` (multipart). Validates link + optional preview/prod rules mirroring submission. |
| **Constraints** | Enforce max size, allowed MIME/extension, rate/size totals per link or per client session as reasonable MVP (document limits). |
| **Storage (physical)** | **Reuse the same storage stack as company background assets** — `modules/assets/storage.py` (`load_storage_config`, `AssetStorageProvider`: **local** under `ASSET_STORAGE_LOCAL_DIR` or **Azure** when configured). Use a **distinct object key prefix** for submission files (e.g. `submissions/{formPublicLinkId}/{opaqueId}.{ext}`). **Do not** persist anonymous public uploads as **`dbo.Asset`** rows; metadata lives in **`SubmissionAttachment`** only. |
| **Checksum** | Store **SHA-256** on each `SubmissionAttachment` row; enables integrity checks and **optional scoped dedupe** (§2.4.1). |
| **Submission** | Extend submission handler to accept attachment reference shape in answers; bind attachments to **created `FormSubmissionID`** when submission succeeds (see lifecycle below). |

### 2.4 Data model (backend + DB)

| Entity | Purpose |
|--------|---------|
| **`SubmissionAttachment`** (or `FormSubmissionAttachment`) | **Canonical list of all submission-scoped files** for support, audit, download ACL, and cleanup. Columns (minimum): FK `FormPublicLink`, nullable FK `FormSubmission`, **public attachment id** (UUID), `OriginalFileName`, `ContentType`, `SizeBytes`, **`Sha256`**, `StorageProvider`, `StorageKey`, `CreatedAt`, optional `ClientUploadSessionKey` / context fields for binding, optional `ExpiresAt` for orphans. |

### 2.4.1 Duplicate uploads & deduplication

| Scenario | Expected behaviour |
|----------|-------------------|
| **User uploads the same bytes twice** (same link + same browser session / upload batch, per context fields) | **Optional MVP:** if an existing **pending** row (`FormSubmissionID` NULL) matches **same `FormPublicLinkID` + scoped session + `Sha256`**, API may return the **existing** public attachment id and **not** write a second blob (document in closeout). **Do not** dedupe across unrelated respondents or arbitrary cross-link reuse — keeps privacy and audit clear. |
| **User selects a new file after already selecting one** (`allowMultiple: false`) | Replace pending attachment reference in UI; prior pending row may stay until TTL/orphan cleanup or be soft-invalidated per implementation. |
| **Multiple files in one control** (`allowMultiple: true`, within `maxFiles`) | One answer value holds **array of attachment ids**; each id maps to its own `SubmissionAttachment` row. |

**Tests:** at least one automated case for “second upload same hash same session returns stable id or second row” **as implemented**, and **reject** reusing another session’s attachment id on submit (per AC-3).

**Lifecycle (submission-scoped):**

1. After upload: row exists with `FormSubmissionID = NULL`, scoped by `FormPublicLinkID` + client context (e.g. idempotency / session fields—see context XML).
2. On successful submit: link rows to new `FormSubmissionID`; answer JSON stores **only** attachment public IDs (not filesystem paths).
3. Failed/abandoned uploads: orphan rows may be cleaned by TTL job later; MVP may document manual/periodic cleanup.

**Alembic:** New migration under `backend/migrations/versions/` revising current head (`050` at story bootstrap—verify with `alembic heads` before authoring). **Anthony runs Alembic upgrade** in each environment; Dev must not run upgrade/downgrade commands in automation.

### 2.5 Secure download (company)

| Area | Requirement |
|------|-------------|
| **Endpoint** | Authenticated API to download attachment bytes (e.g. by `attachmentId` + submission id or form id), enforcing **company/event access** same as lead/submission list APIs. |
| **Audit** | Log or reuse existing patterns for sensitive access (lightweight OK for MVP). |

### 2.6 Validation & docs

- `POST /api/form-validate` accepts definitions containing `type: "file-upload"`.
- Update **`docs/COMPONENT-FRAMEWORK-GUIDE.md`** inventory + behaviour for `file-upload`.
- Update **`docs/stories/STORY-6.2-AI-CONTEXT-PACK.md`**: `file-upload` **available** (remove “planned 6.2.2 only” wording once implemented).
- **`docs/COMPONENT-FRAMEWORK-REFERENCE.md`**: touch only if needed for upload/submission contracts.

---

## 3) Out of Scope

| Item | Reason |
| Virus scanning | Future hardening |
| New third-party blob product | Use existing **local + Azure** asset storage only |
| AI generation of forms with uploads | Story 6.3 may consume catalogue update; generation prompts separate |
| Email delivery of attachments | Not required |
| Chunked/resumable uploads | Simple multipart POST is sufficient for MVP |

---

## 4) Acceptance Criteria

### AC-1: Builder file-upload

- **Given** the builder is open  
- **When** the user adds **File upload** from the toolbox  
- **Then** it appears on canvas with configured label/help  
- **And** Properties Panel controls **accept**, **max size**, **multiple**  
- **And** `POST /api/form-validate` accepts `type: "file-upload"`

### AC-2: Public upload + submit

- **Given** a published form with a file-upload field  
- **When** an anonymous user selects valid file(s) and uploads  
- **Then** the client receives **stable attachment ID(s)** from the public API  
- **And** on submit, submission is **ACCEPTED** and answers reference those IDs  
- **And** DB rows link attachments to the **same** `FormSubmissionID`

### AC-3: Cross-contamination denied

- **Given** two different submit attempts (different idempotency keys or sessions)  
- **When** attempt B tries to reference attachment IDs created under attempt A  
- **Then** submission fails validation or attachment is rejected (document exact behaviour in closeout)

### AC-4: Company download

- **Given** a company user with access to the submission’s form/event  
- **When** they request download by attachment id  
- **Then** they receive correct bytes and filename  
- **And** users **without** access receive 403/404

### AC-5: Green CI/CD

- `npm run lint` — 0 errors, 0 warnings (touched surfaces)  
- `npm run test:unit -- --watch=false` — pass  
- `python -m pytest --tb=short` — pass, including **new** tests for upload, submit binding, and access control

### AC-6: Storage & registry alignment

- **Given** implementation is complete  
- **Then** submission files are written via **`AssetStorageProvider`** (same config as `modules/assets`) with submission-specific keys  
- **And** **`SubmissionAttachment`** is the system-of-record table listing attachments (not `dbo.Asset` for anonymous uploads)  
- **And** deduplication behaviour matches §2.4.1 and is covered by tests described there  

---

## 5) Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Disk fill / large files | Hard max size; configurable cap; reject with clear error |
| Orphan files on disk | DB metadata + optional expiry; document cleanup |
| Token abuse | Size limits + basic rate limiting if already present in middleware |

---

## 6) Definition of Done

- All ACs satisfied; gate evidence in `STORY-6.2.2-GATE-EVIDENCE.md`  
- UAT results in `STORY-6.2.2-UAT-RESULTS.md` (human + automation sections)  
- Closeout report; Draft PR #55 ready for review/merge  
- `EPIC-6-STATUS.md`: 6.2.2 → Complete with merge date (on merge PR)

---

## 7) Dev Agent Record

_(Filled by Dev during implementation)_

| Field | Value |
|------|-------|
| Migration revision id | |
| Public upload route(s) | |
| Storage | `AssetStorageProvider` + key prefix; env vars documented |
| Dedup policy (§2.4.1) implemented as | |
| Closeout / merge notes | |
