# Completion Note: T06 - Placement + Intersection + Cropping

**Story:** 5.1 - Background Asset Management  
**Task:** T06  
**Completed:** 2026-02-11

---

## Summary

Implemented background placement metadata (position, size, crop), cropping behavior, and the off-canvas intersection rule. When a background image is fully off-canvas, it is auto-removed from the page (asset remains in library).

---

## Changes

| File | Action |
|------|--------|
| `frontend/src/features/builder/utils/backgroundPlacementUtils.ts` | Created | `isBackgroundFullyOffCanvas`, `createDefaultPlacement` |
| `frontend/src/features/builder/components/properties/BackgroundPropertiesPanel.tsx` | Modified | Placement X/Y/Width/Height inputs; init placement on asset select; off-canvas auto-remove |
| `frontend/src/features/builder/components/PropertiesPanel.tsx` | Modified | Pass canvasWidth, canvasHeight to BackgroundPropertiesPanel |
| `frontend/src/features/builder/components/FormBuilderCanvas.tsx` | Modified | Apply placement/crop when rendering; hide when off-canvas |
| `frontend/src/features/renderer/components/PublicFormArtboard.tsx` | Modified | Apply placement/crop when rendering; hide when off-canvas |

---

## Acceptance Criteria

- **AC1:** Background placement is persisted and applied correctly — Placement (position, size) stored in `background.placement`; rendered in builder and public form.
- **AC2:** Fully off-canvas backgrounds are removed from canvas — On placement update, if fully off-canvas, `handleRemoveAsset()` clears the background from the page.
- **AC3:** Asset remains in the library after auto-removal — We clear `page.background.asset`; we do not call any asset-delete API.

---

## Test Evidence

- **Lint:** N/A (project lint config in different workspace)
- **Build:** `npm run build` passed (T06 worktree frontend)
- **Scope:** Frontend-only (no backend changes)

---

## Out-of-scope / Notes

- Crop UI not added (crop can be set programmatically; BackgroundDefinition.placement.crop is supported in rendering)
- Legacy imageSize/imagePosition retained for forms without placement
