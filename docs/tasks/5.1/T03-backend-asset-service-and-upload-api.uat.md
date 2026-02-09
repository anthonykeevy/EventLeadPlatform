# UAT Checklist: T03

**Story:** 5.1
**Task:** Backend Asset Service + Upload API
**Generated:** 2026-02-09

---

## Pre-conditions

- [ ] Backend server is running
- [ ] Valid JWT access token is available
- [ ] Storage provider configured (`ASSET_STORAGE_PROVIDER=local` or `azure`)

## Test Steps

### AC1: Backend can store an asset and return metadata + reference

- [ ] Step 1: `POST /api/assets/backgrounds/upload` with a valid PNG file → Verify: 201 response with `asset.assetId` and `asset.assetKey`
- [ ] Step 2: Confirm response includes `mimeType`, `byteSize`, and dimensions → Verify: values match uploaded file

### AC2: Upload limits enforced via `config.AppSetting`

- [ ] Step 1: Upload a file larger than the configured max bytes → Verify: 413 error with size message
- [ ] Step 2: Upload a non-image file → Verify: 400 error for unsupported/invalid image

### AC3: Runtime resolver returns correct URLs without storing absolute hosts

- [ ] Step 1: `GET /api/assets/{assetId}/resolve` → Verify: URL ends with `/api/assets/{assetId}/content` (local) or valid Azure blob URL (azure)

### AC4: Dedup by hash prevents duplicate asset records

- [ ] Step 1: Upload the same file twice → Verify: second response returns same `assetId` and `isDuplicate=true`

## Regression Check

- [ ] Verify existing authenticated endpoints still work (e.g., `/api/auth/me`)
- [ ] No new backend errors in logs

## Post-conditions

- [ ] Uploaded file remains accessible via `/api/assets/{assetId}/content`

---

**Instructions for Human Tester:**
1. Execute each step in order
2. Mark ✅ or ❌ for each item
3. Add notes for any failures
4. When complete, run `@ralf-uat *record-uat` with your results
