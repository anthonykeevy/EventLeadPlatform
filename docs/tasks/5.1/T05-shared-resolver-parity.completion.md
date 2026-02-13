# Task Completion: T05 Shared Resolver Parity

**Story:** 5.1 - Background Asset Management  
**Task:** T05 - Shared Resolver Parity (Builder + Renderer)  
**Completed:** 2026-02-11  
**Status:** Complete

---

## Summary of Changes

Implemented a shared background asset resolver module and integrated it into both the builder preview (FormBuilderCanvas) and public renderer (PublicFormArtboard). Both now use the same `useBackgroundImageUrl` hook and `backgroundAssetResolver` for URL generation, ensuring identical display of background assets. The public renderer previously did not show background images; it now renders them with the same rules as the builder.

---

## Files Changed

| File | Change | Reason |
|------|--------|--------|
| `frontend/src/features/builder/utils/backgroundAssetResolver.ts` | Created | Shared resolver for asset content URL (matches backend contract) |
| `frontend/src/features/builder/hooks/useBackgroundImageUrl.ts` | Created | Shared hook for resolving and displaying background images |
| `frontend/src/features/builder/components/FormBuilderCanvas.tsx` | Modified | Uses useBackgroundImageUrl instead of inline blob fetch |
| `frontend/src/features/renderer/components/PublicFormArtboard.tsx` | Modified | Added background image layer using shared resolver |
| `frontend/src/features/builder/utils/phoneValidation.ts` | Modified | Fix libphonenumber-js import (dep scan error) |
| `frontend/src/features/builder/components/properties/AssetLibrary.tsx` | Modified | Remove unused formatFileSize (build fix) |
| `frontend/src/lib/index.ts` | Modified | Remove broken auth export (build fix) |

---

## Acceptance Criteria Verification

### AC1: Builder preview and renderer display the same background asset
- **Status:** PASS
- **Evidence:** Both FormBuilderCanvas and PublicFormArtboard use `useBackgroundImageUrl(page?.background)`, which calls `assetsApi.fetchAssetContentBlobUrl` for assets and returns the same resolved URL format for external URLs. The resolver produces URLs matching the backend contract (`/api/assets/{id}/content`).

### AC2: Resolver logic is centralized (no duplicated resolver code)
- **Status:** PASS
- **Evidence:** All resolution logic lives in `backgroundAssetResolver.ts` and `useBackgroundImageUrl.ts`. FormBuilderCanvas and PublicFormArtboard both import and use these modules; no inline resolver logic remains.

---

## Test Evidence

### Frontend Lint
```powershell
cd task-5.1-T05-shared-resolver-parity/frontend
npm run lint
```
**Result:** PASS (exit 0)

### Frontend Build
```powershell
cd task-5.1-T05-shared-resolver-parity/frontend
npm run build
```
**Result:** PASS (exit 0), build completed in ~5.5s

### Backend Asset Tests
```powershell
cd task-5.1-T05-shared-resolver-parity/backend
python -m pytest tests/test_assets_upload.py -v
```
**Result:** 4 passed (test_resolve_asset_url_builds_runtime_url confirms backend contract)

---

## Manual UAT Steps

1. [ ] **Builder preview with asset background:** Open form builder, add a background image (upload or select from library), verify the canvas shows the image.
2. [ ] **Public renderer with asset background:** View the same form in public preview or production link; verify the background image displays identically.
3. [ ] **External URL parity:** Use an external URL as background in builder; verify it appears in both builder preview and public renderer.
4. [ ] **Color background:** Verify solid color backgrounds still work in both contexts.

---

## Known Limitations / Out-of-Scope Items

- **Anonymous public forms:** Asset content endpoint requires auth. When a form is viewed by an unauthenticated user (public submission flow), background images from assets may not load (401). Builder preview (logged-in) and token-based preview work. Future: signed public asset URLs (T07 or later).
- **objectFit "tile" and "auto":** Mapped to "cover" for `<img>` display; true tiling would require `background-image` style (out of scope).

---

## Recommended Next Step

**Ready for UAT by human.** Execute the manual steps above. After UAT passes, run `@ralf-retro *run-retro` then return for next task.
