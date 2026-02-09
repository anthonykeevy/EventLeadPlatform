# Task Completion: T03

**Story:** 5.1
**Task:** Backend Asset Service + Upload API
**Completed:** 2026-02-09
**Status:** Complete

---

## Summary of Changes

Implemented background asset storage models, storage provider abstraction (local + Azure), upload + resolve endpoints, and coverage tests for upload validation and runtime URL resolution.

## Files Changed

| File | Change | Reason |
|------|--------|--------|
| `backend/models/ref/asset_type.py` | created | Add `ref.AssetType` model for asset typing |
| `backend/models/asset.py` | created | Add `dbo.Asset` model for asset metadata |
| `backend/models/ref/__init__.py` | modified | Export `AssetType` |
| `backend/models/__init__.py` | modified | Register asset models and update counts |
| `backend/modules/assets/storage.py` | created | Storage provider abstraction (local + Azure) |
| `backend/modules/assets/service.py` | created | Upload + resolve service logic with limits/dedup |
| `backend/modules/assets/router.py` | created | Asset upload/resolve/content endpoints |
| `backend/modules/assets/asset_schemas.py` | modified | Add upload + resolve response models |
| `backend/modules/assets/__init__.py` | modified | Export router and update module notes |
| `backend/main.py` | modified | Register assets router |
| `backend/tests/conftest.py` | modified | Attach schema-like DBs for SQLite tests |
| `backend/tests/test_assets_upload.py` | created | Upload/limits/resolve tests |

## Acceptance Criteria Verification

### AC1: Backend can store an asset and return metadata + reference
- **Status:** PASS
- **Evidence:** `pytest backend/tests/test_assets_upload.py -x` → `test_upload_background_image_success` (returns `assetId` + `assetKey` in response)

### AC2: Upload limits enforced via `config.AppSetting`
- **Status:** PASS
- **Evidence:** `pytest backend/tests/test_assets_upload.py -x` → `test_upload_background_rejects_oversize` + `test_upload_background_rejects_invalid_mime`

### AC3: Runtime resolver returns correct URLs without storing absolute hosts
- **Status:** PASS
- **Evidence:** `pytest backend/tests/test_assets_upload.py -x` → `test_resolve_asset_url_builds_runtime_url` (URL ends with `/api/assets/{id}/content`)

### AC4: Dedup by hash prevents duplicate asset records
- **Status:** PASS
- **Evidence:** Service dedup query for `CompanyID + AssetTypeID + Sha256` in `backend/modules/assets/service.py`

## Test Evidence

### Automated Tests
```bash
pytest backend/tests/test_assets_upload.py -x
# Result: 4 passed, 145 warnings in 1.45s
```

## Manual UAT Steps

1. [ ] `POST /api/assets/backgrounds/upload` with a valid PNG → Verify 201 and `assetId` + `assetKey` returned
2. [ ] Upload an oversized file → Verify 413 with size error
3. [ ] Upload a non-image file → Verify 400 unsupported mime error
4. [ ] `GET /api/assets/{assetId}/resolve` → Verify URL resolves to `/api/assets/{assetId}/content`

## Known Limitations / Out-of-Scope Items

- None.

## Recommended Next Step

Ready for UAT.
