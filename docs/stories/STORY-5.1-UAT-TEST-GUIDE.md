# Story 5.1 UAT Test Guide — Background Asset Management

**Story:** 5.1  
**Scope:** Background image assets (no base64 in `DefinitionJSON`)  
**Status:** ⏳ Not Executed  

---

## Preconditions

- Backend is running locally
- Frontend is running locally
- You have access to a form in the builder
- Asset limits exist in `config.AppSetting` (or safe defaults are provided in dev)

**Test credentials (local dev):** user2@test.com / `JChMom7KYLfL88&!` (Company Admin). See `docs/AGENT-LOGGING-GUIDE.md` § UAT test credentials.

---

## Test assets (recommended)

Prepare these images:
- Small PNG (under size limits)
- Large JPG (over size limits)
- Invalid MIME type (e.g., GIF if disallowed)

---

## Scenarios

### Scenario 1 — Upload and apply a background asset

**Goal:** Validate asset upload and use in the builder.

Steps:
1. Open the builder for a form.
2. Upload a valid image within size and dimension limits.
3. Apply it as the background image.

Expected:
- Upload succeeds and the background renders.
- The definition stores an **asset reference**, not a Data URL.

---

### Scenario 2 — Reload builder preserves background via asset reference

Steps:
1. Save the form.
2. Reload the builder.

Expected:
- Background image renders correctly.
- No base64 data appears in `DefinitionJSON`.

---

### Scenario 3 — Renderer parity (preview/public)

Steps:
1. Open the preview/public renderer for the form.

Expected:
- The same background image renders in the renderer.
- No asset host URL is stored in `DefinitionJSON`.

---

### Scenario 4 — Off-canvas intersection rule

Steps:
1. Move the background image completely off-canvas (if supported).

Expected:
- The background is removed from the canvas.
- The asset remains available in the asset library.

---

### Scenario 5 — Upload limit enforcement

Steps:
1. Try to upload an oversized image (bytes or dimensions).
2. Try to upload a disallowed MIME type.

Expected:
- Both uploads are blocked with clear errors.
- Limits are enforced via config-backed settings (not hard-coded).

---

### Scenario 6 — Dedup behavior

Steps:
1. Upload the same image twice.

Expected:
- The system deduplicates by hash (no duplicate asset records).

---

### Scenario 7 — Soft-delete safety (if UI exists)

Steps:
1. Soft-delete a background asset.
2. Open a form that references the asset.

Expected:
- The form handles the missing asset gracefully (clear error or placeholder).
- No crash or broken UI.

---

## Pass/Fail Recording

Mark each scenario:
- [ ] Scenario 1: ⬜ PASS / ⬜ FAIL  
- [ ] Scenario 2: ⬜ PASS / ⬜ FAIL  
- [ ] Scenario 3: ⬜ PASS / ⬜ FAIL  
- [ ] Scenario 4: ⬜ PASS / ⬜ FAIL  
- [ ] Scenario 5: ⬜ PASS / ⬜ FAIL  
- [ ] Scenario 6: ⬜ PASS / ⬜ FAIL  
- [ ] Scenario 7: ⬜ PASS / ⬜ FAIL  

---

## Notes / Issues Found

- TBD

# Story 5.1 UAT Test Guide — Background Asset Management

**Story:** 5.1  
**Scope:** Background image assets (no embedded base64 Data URLs), storage provider abstraction, config-backed limits  
**Status:** 📝 Draft (not yet executed)  

---

## Preconditions

- Backend is running locally
- Frontend is running locally
- You can access the Builder and edit a form
- Asset limits are present in `config.AppSetting` and are being loaded by `ConfigurationService`
  - At minimum: `forms.assets.images.max_upload_bytes`, `forms.assets.images.allowed_mime_types`
- Storage provider is configured (default expected for local dev: `forms.assets.storage.provider = "local"`)

---

## Test data (recommended)

- **Valid small image**: PNG/JPEG/WebP under `max_upload_bytes`, within max dimensions
- **Too-large image**: file exceeding `forms.assets.images.max_upload_bytes`
- **Disallowed type**: e.g. GIF/SVG or any mime not in `forms.assets.images.allowed_mime_types`
- **Oversized dimensions**: image exceeding `max_width_px` or `max_height_px`

---

## Evidence capture (minimal)

Capture at least one of:
- Screenshot of builder canvas showing background applied
- Network/API evidence showing the saved form definition contains an **asset reference** and does **not** contain `data:image/`
- Optional: SQL evidence showing DefinitionJSON contains no `data:image/` substring for the saved version

---

## Scenarios

### Scenario 1 — Upload background image and apply to the form

**Goal:** Validate that the builder uploads an asset and stores a reference (not bytes) in the form definition.

Steps:
1. Open an existing draft form (or create a new one).
2. Add/apply a background image via the builder UI.
3. Save the form (trigger a version save if the system versions on save/publish).

Expected:
- Background renders on the canvas immediately after upload.
- Save succeeds.
- The saved definition includes an **asset reference** (e.g. `assetId`) and placement metadata.
- The saved definition does **not** include a `data:image/*` Data URL.

---

### Scenario 2 — Reload the form; background persists and renders

Steps:
1. Hard refresh the page or navigate away and back to the same form/version.

Expected:
- Background loads and renders correctly after reload (no broken image).

---

### Scenario 3 — Verify `DefinitionJSON` does not contain embedded base64

**Goal:** Prove we removed base64 from persistence.

Verification options (implementation-dependent):

Option A (API/network):
1. Inspect the response payload for the form version definition.
2. Search for `data:image/`.

Option B (database):
1. Query the relevant FormVersion row.
2. Confirm `DefinitionJSON` does not contain `data:image/`.

Expected:
- No `data:image/` substring exists in the persisted definition JSON.

---

### Scenario 4 — Upload limit: max bytes enforced (config-backed)

Steps:
1. Attempt to upload an image larger than `forms.assets.images.max_upload_bytes`.

Expected:
- Upload is rejected with a clear error message.
- Backend enforcement matches the configured AppSetting value (not hard-coded).

---

### Scenario 5 — Upload limit: allowed mime types enforced (config-backed)

Steps:
1. Attempt to upload a disallowed file type (mime not present in `forms.assets.images.allowed_mime_types`).

Expected:
- Upload is rejected with a clear error message.

---

### Scenario 6 — Upload limit: max dimensions enforced (config-backed)

Steps:
1. Attempt to upload an image exceeding `forms.assets.images.max_width_px` or `forms.assets.images.max_height_px`.

Expected:
- Upload is rejected with a clear error message (or the UI prevents selection with a clear reason).

---

### Scenario 7 — Renderer parity: public runtime resolves background asset

**Goal:** The public renderer can load the asset using the runtime resolver (not a builder-only path).

Steps:
1. Generate/open a public preview or production link for the form.
2. Load the public renderer page.

Expected:
- The background image renders in the public runtime.
- No CORS/auth errors prevent loading.

---

### Scenario 8 — Defensive guard: embedded Data URL payload is blocked or stripped

**Goal:** Confirm we handle legacy/malicious embedded base64 payloads safely.

Steps (implementation-dependent; choose one):

Option A (Builder):
1. Load a form that contains an embedded Data URL background (dev seed / crafted draft).
2. Attempt to save.

Option B (API):
1. Call the form save/update endpoint with a definition containing `data:image/*`.

Expected:
- System blocks or strips the embedded Data URL deterministically.
- A clear error/warning is surfaced (no silent acceptance of base64 into persistence).

---

### Scenario 9 — Provider swap smoke test (optional)

If Azure storage is configured in the target environment:
1. Switch `forms.assets.storage.provider` to `"azure_blob"`.
2. Repeat Scenario 1.

Expected:
- Upload + render works using the Azure provider without schema/definition changes.

---

## Pass/Fail Recording

Mark each scenario:
- [ ] Scenario 1: ✅ PASS / ❌ FAIL
- [ ] Scenario 2: ✅ PASS / ❌ FAIL
- [ ] Scenario 3: ✅ PASS / ❌ FAIL
- [ ] Scenario 4: ✅ PASS / ❌ FAIL
- [ ] Scenario 5: ✅ PASS / ❌ FAIL
- [ ] Scenario 6: ✅ PASS / ❌ FAIL
- [ ] Scenario 7: ✅ PASS / ❌ FAIL
- [ ] Scenario 8: ✅ PASS / ❌ FAIL
- [ ] Scenario 9: ✅ PASS / ❌ FAIL / ⏭️ SKIP

---

## Notes / Issues Found

- (Record any failures, screenshots, and logs here.)

