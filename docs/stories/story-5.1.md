# Story 5.1: Background Asset Management

**Epic:** Epic 5 - Form Builder Readiness + Review & Publishing  
**Domain:** Builder Foundations / Asset Management  
**Status:** 🟡 Draft  
**Priority:** Critical (foundation for Epic 5)  
**Created:** 2026-02-09  
**Owner:** Developer Agent  

---

## 📖 User Story

**As a** Company User or Admin building forms,  
**I want** background images managed as reusable assets (not embedded in JSON),  
**So that** form definitions stay lightweight, assets can be reused, and preview/production rendering stays consistent.

---

## 🧭 Scope Boundary (CRITICAL)

### In scope (Story 5.1)

- **Asset-based backgrounds (no base64 in `DefinitionJSON`)**
  - Upload/store background images as assets.
  - Form definitions store **asset references** (IDs/keys), not Data URLs.
- **Storage provider abstraction**
  - Local dev storage now; Azure Blob ready via config.
  - Runtime URL generation (no absolute hosts stored in definitions).
- **Background placement + cropping**
  - Store placement in canvas coordinates (allow negative offsets).
  - **Intersection rule:** if fully off-canvas, auto-remove from the canvas (asset remains in library).
- **Asset lifecycle basics**
  - Dedup by hash.
  - Soft-delete (keep references safe).
  - Rename support (`displayName` separate from original filename).
- **Config-backed limits (mandatory)**
  - Limits must live in `config.AppSetting` (loaded via `ConfigurationService`).
  - Proposed keys (draft, finalize during decomposition):
    - `forms.assets.images.max_upload_bytes`
    - `forms.assets.images.max_width_px`
    - `forms.assets.images.max_height_px`
    - `forms.assets.images.allowed_mime_types` (JSON array)
    - (Later) `forms.assets.images.max_total_bytes_per_company`
    - (Later) `forms.assets.images.max_count_per_company`
- **Defensive guard against embedded Data URLs**
  - If a background image is detected as a Data URL, reject or strip and surface a clear error.

### Out of scope (Story 5.1)

- Company-level defaults (Story 5.2)
- Schema + validation alignment (Story 5.3)
- Preview/production governance (Story 5.5+)
- Publish workflow, admin review, activation windows (Story 5.6+)
- Payments, invoicing, analytics (Epic 6/7)

---

## 🎯 Functional Requirements (High Level)

### FR-1: Background images are stored as assets
- Builder uploads images and receives a stored asset reference.
- `FormVersion.DefinitionJSON` stores a reference, not raw image data.

### FR-2: Storage provider abstraction exists
- Local filesystem in dev, Azure Blob in prod (config-driven).
- Definitions never store absolute host URLs.

### FR-3: Runtime URL resolution is shared
- Builder preview and public renderer resolve assets the same way.

### FR-4: Placement + cropping is reliable
- Supports negative offsets.
- Fully off-canvas images are auto-removed from the canvas (asset remains available).

### FR-5: Limits enforced via `config.AppSetting`
- Upload and runtime limits enforced using config-backed keys.

### FR-6: Asset lifecycle and dedup
- Uploading an identical image returns the existing asset (dedup via hash).
- Soft-delete and rename operations are supported.

### FR-7: Data URL guard
- If a Data URL background is found, it is rejected/stripped with a clear error to avoid bloated JSON.

---

## ✅ Acceptance Criteria

1) Background images are stored as assets, not embedded in `DefinitionJSON`.  
2) Builder + renderer both resolve background images from asset references (parity).  
3) Upload limits (bytes/size/mime) are enforced using `config.AppSetting`.  
4) Asset URLs are generated at runtime (no absolute host persisted).  
5) Negative offsets are supported; fully off-canvas backgrounds auto-remove from the canvas.  
6) Duplicate uploads dedupe via hash (no duplicate asset records).  
7) Soft-delete and rename are supported without breaking existing forms.  
8) Any embedded Data URL background is blocked/stripped with a clear error.  

---

## 🔧 Technical Notes (Guidance)

- Current builder stores background images via `readAsDataURL`, which bloats `DefinitionJSON`.  
- Replace Data URL storage with asset references and shared resolver logic.  
- Ensure all limits are loaded via `ConfigurationService` (config-backed).  
- Storage provider should be swappable without schema changes (Local ↔ Azure Blob).  

---

## 🔗 Dependencies

### Upstream
- Epic 3 complete (builder + renderer baseline).

### Downstream
- Story 5.2 (Company defaults)
- Story 5.3 (Schema alignment)
- Story 5.4 (Shared resolver parity hardening)
- Story 5.5+ (Preview/production governance)

---

## ✅ Done Criteria

Story 5.1 is complete when:
- All acceptance criteria pass.
- `docs/stories/STORY-5.1-UAT-TEST-GUIDE.md` is executed and marked ✅ PASSED.
- Implementation is merged via Story/Task PRs (no direct work on `master`).

---

## 🧪 UAT Test Guide

See: `docs/stories/STORY-5.1-UAT-TEST-GUIDE.md`

---

## 📝 Completion Report

**Completed:** TBD  
**Evidence:** TBD  

---

*Story created using Epic 5 workflow guide*  
# Story 5.1: Background Asset Management (No base64 Data URLs in `DefinitionJSON`)

**Epic:** Epic 5 - Form Builder Readiness + Review & Publishing  
**Domain:** Form Builder Readiness (Assets)  
**Status:** 📝 Draft (Ready for decomposition)  
**Priority:** High (Foundation / “no rework” constraint)  
**Created:** 2026-02-08  
**Owner:** Developer Agent  

---

## 📖 User Story

**As a** form builder user (Company User/Admin),  
**I want to** upload and reuse background images as managed **assets** (not embedded base64 in the form JSON),  
**So that** forms save/load fast, version history stays small, and the builder + renderer resolve backgrounds consistently.

---

## 🧭 Context (Why this story exists)

Current risk (Epic 5 readiness blocker):
- Background images are currently embedded as **base64 Data URLs** in the form definition JSON (via browser `FileReader.readAsDataURL` style flows).
- This bloats `FormVersion.DefinitionJSON` (NVARCHAR MAX), increases save/load time, inflates version history, and makes asset lifecycle (limits, dedupe, delete, provider swap) impossible.

Epic 5 goal sequencing:
- Epic 3 is complete (builder + renderer + submission/outbox).
- Epic 5 begins with **builder readiness** (assets + defaults + schema parity) before governance (preview/production + publish workflow).

---

## ✅ Scope Boundary (Story 5.1)

### In scope

- **Replace embedded base64 Data URLs with asset references** in form definitions.
  - Form definitions must store **references** (e.g. `assetId`) + placement metadata, not image bytes.
  - A defensive guard must block (or sanitize + warn) embedded Data URLs.
- **Backend persistence model for assets**:
  - DB records for asset metadata + lifecycle state (active/soft-deleted) + tenant scope.
  - Storage provider abstraction for binary content (Local dev → Azure Blob prod) with a config-based switch.
  - Dedup by content hash (optional but preferred) to avoid repeated uploads of identical backgrounds.
- **Builder + renderer parity plan**:
  - Builder preview and public renderer must resolve background assets consistently.
  - Do not persist absolute hostnames in definitions (custom domains later); runtime should generate URLs at request time.
- **Config-backed limits (mandatory)**:
  - Any upload/runtime limits must be stored in `config.AppSetting` and loaded via `ConfigurationService`.
  - Proposed `SettingKey` list is included below (draft; finalize during decomposition).

### Out of scope (explicit deferrals)

- Company-level defaults / brand system → **Story 5.2**
- Schema + validation alignment (builder ↔ backend parity) → **Story 5.3**
- Review/publish governance (preview/prod + publish request + admin review) → **Story 5.5+**
- Payments/invoicing → **Epic 6**

---

## 🎯 Functional Requirements (High Level)

### FR-1: Form definition stores background as an asset reference

- Background image bytes are **never** stored in `FormVersion.DefinitionJSON`.
- Background image in a definition is represented as:
  - An **asset reference** (e.g. `assetId`)
  - **Placement** metadata for canvas positioning/cropping (supports negative offsets)
  - (Optional) render hints: opacity, scale mode, etc. (finalize during decomposition)

### FR-2: Asset upload + metadata persistence exists (tenant-scoped)

- Uploading a background creates (or reuses, if deduped) a persisted asset record:
  - `companyId` scope (tenant-bound)
  - `createdByUserId`
  - original filename + display name
  - content hash (sha256 recommended), mime type, size bytes
  - image width/height
  - storage provider key + storage path/blob key
- Asset records support soft-delete; binary cleanup policy is defined (can be deferred to a later task if needed, but lifecycle fields must exist).

### FR-3: Storage provider abstraction (local ↔ Azure) is swappable via config

- A single storage interface is used by backend services (no direct file-system vs blob branching in feature code).
- Provider selection is configuration-driven and **does not require schema redesign**.
- Local dev provider writes to a predictable local path; Azure provider uses blob storage in production.

### FR-4: Builder + renderer resolve assets consistently

- Background asset resolution must work in:
  - Builder editor + preview
  - Public renderer runtime (token-gated)
- URL generation must be runtime-based (avoid persisting hostnames) so custom domains can be introduced later without rewriting stored definitions.

### FR-5: Upload/runtime limits are enforced via `config.AppSetting`

- Backend enforces:
  - maximum upload bytes
  - allowed mime types
  - maximum image dimensions (px)
- Builder enforces (best-effort UX) the same constraints to prevent “upload then reject”.

### FR-6: Defensive guard against embedded Data URLs (no migration expected)

- As of 2026-02-07, background images were not functional/used in existing customer forms; **no migration is expected**.
- Despite that, we must guard against:
  - Old drafts / dev data
  - Malicious or accidental payloads
- Guard behavior (finalize during decomposition):
  - Backend rejects save with a clear error (preferred), **or**
  - Backend strips the embedded data URL, preserves non-binary placement metadata, and returns a warning.

---

## ⚙️ Proposed `config.AppSetting` keys (Draft; finalize during decomposition)

All keys are stored in `config.AppSetting.SettingKey` and loaded via `ConfigurationService`.

### Limits (mandatory)

- `forms.assets.images.max_upload_bytes` (int, default: 5242880 / 5MB)
- `forms.assets.images.allowed_mime_types` (json array of strings, default: `["image/png","image/jpeg","image/webp"]`)
- `forms.assets.images.max_width_px` (int, default: 4096)
- `forms.assets.images.max_height_px` (int, default: 4096)
- `forms.assets.images.max_pixels` (int, optional; default: 16777216 / 16MP)

### Storage provider selection (required for painless swap)

- `forms.assets.storage.provider` (string enum, default: `"local"`; values: `"local"`, `"azure_blob"`)
- `forms.assets.storage.public_url_mode` (string enum, default: `"api"`; values: `"api"`, `"signed_url"`)
- `forms.assets.storage.signed_url_ttl_seconds` (int, default: 900)  
  (Only used when `public_url_mode = "signed_url"`)

### Quotas (explicitly deferred but reserve keys)

- `forms.assets.images.max_total_bytes_per_company` (int, default: null / disabled)
- `forms.assets.images.max_count_per_company` (int, default: null / disabled)

> Note: Azure credentials/connection strings should be treated as secrets (env/managed secrets). AppSetting should select provider + non-secret behavior knobs.

---

## 🗄️ Draft Data Model (Guidance)

Model must support:

- **Asset table** (tenant-scoped): `dbo.Asset`
  - `AssetID` (PK, GUID recommended)
  - `CompanyID` (FK)
  - `AssetTypeID` (FK → `ref.AssetType`) — enum-backed reference
  - `MimeType`, `SizeBytes`, `WidthPx`, `HeightPx`, `Sha256`
  - `StorageProvider`, `StorageKey` (path/blob key)
  - `OriginalFilename`, `DisplayName`
  - `CreatedByUserID`, `CreatedAt`, `DeletedAt` (soft delete)
- **Asset type enum** (reference table): `ref.AssetType`
  - `AssetTypeID` (PK)
  - `TypeCode` (unique, e.g. `IMAGE`)
  - (Optional) `DisplayName`, `SortOrder`, audit fields (per naming rules)
- **Reference from definitions**:
  - Store only `assetId` + placement metadata in JSON.
  - No bytes/base64; no absolute hostnames.

---

## 🔌 Draft API Surface (Guidance)

Exact routes finalized during decomposition, but the capabilities must exist:

- Authenticated upload/list/delete endpoints for assets (company-scoped)
- Runtime resolution endpoint(s) usable by:
  - Builder (authenticated)
  - Public renderer (token-gated)  

API contract constraints:
- All JSON responses are **camelCase** (per `docs/solution-architecture.md` contract).

---

## ✅ Acceptance Criteria

1) **No base64 in definitions**
- [ ] Saving a form with a background image results in `FormVersion.DefinitionJSON` containing an asset reference (e.g. `assetId`) and **no embedded** `data:image/*` Data URLs.

2) **Asset persistence**
- [ ] Uploading a background image creates a persisted asset record with metadata (mime, size, dimensions) and stored binary content in the configured provider.

3) **Builder + renderer parity**
- [ ] The builder canvas and the public renderer both display the background image reliably for the same form version.

4) **Config-backed limits enforced**
- [ ] Upload rejects files that violate size/mime/dimension limits using values from `config.AppSetting` (not hard-coded).

5) **Provider swap is painless**
- [ ] Switching `forms.assets.storage.provider` changes the storage provider without requiring schema changes or definition rewrites.

6) **Defensive guard**
- [ ] If a form definition contains an embedded `data:image/*` Data URL background, the system blocks or strips it deterministically with a clear error/warning.

---

## 🧪 UAT Test Guide

See: `docs/stories/STORY-5.1-UAT-TEST-GUIDE.md`

---

## ✅ Done Criteria

Story 5.1 is complete when:
- [ ] All Acceptance Criteria pass.
- [ ] Story UAT guide is executed and marked ✅ PASSED.
- [ ] Draft PR exists for the Story branch → `master`, and the story is ready for `@ralf-sm` decomposition into tasks.

