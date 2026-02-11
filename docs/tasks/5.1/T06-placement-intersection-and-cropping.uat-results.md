# UAT Results: T06 - Placement + Intersection + Cropping

**Story:** 5.1 - Background Asset Management  
**Task:** T06  
**Tester:** Agent (automatable checks)  
**Date:** 2026-02-11  
**Status:** ⏳ Pending Human Verification

---

## Summary

| Area | Result |
|------|--------|
| AC1: Placement persisted and applied | Human verification: manual UI flow required |
| AC2: Off-canvas auto-remove | Human verification: manual UI flow required |
| AC3: Asset stays in library | Human verification: manual UI flow required |
| Regression Check | Human verification: manual flow required |

---

## Automatable Evidence

- **Build:** Passed (`npm run build` in T06 worktree frontend)
- **Placement utils:** `backgroundPlacementUtils.ts` exists with `isBackgroundFullyOffCanvas`, `createDefaultPlacement`
- **FormBuilderCanvas:** Uses placement when present; off-canvas returns null
- **PublicFormArtboard:** Same placement/crop logic
- **BackgroundPropertiesPanel:** Placement X/Y/W/H inputs; off-canvas triggers `handleRemoveAsset`

---

## Human Verification Required

1. Run backend + frontend; log in
2. Open form builder; add image background from library
3. Adjust X, Y, Width, Height; verify canvas updates
4. Set X to -2000 (or similar); verify background clears
5. Open asset library; verify asset still present
6. Switch to public preview; verify placement matches

---

## Conclusion

Implementation complete. Human UAT required per checklist.
