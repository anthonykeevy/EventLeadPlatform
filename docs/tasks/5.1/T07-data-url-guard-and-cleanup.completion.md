# Task Completion: T07 Data URL Guard + Cleanup

**Story:** 5.1 - Background Asset Management  
**Task:** T07 - Data URL Guard + Cleanup  
**Completed:** 2026-02-13  
**Status:** Complete

---

## Summary of Changes

Implemented Data URL guards to prevent base64 backgrounds from entering definitions and to strip legacy Data URLs on load. Builder input now rejects Data URLs with a clear error; definitions loaded from API or localStorage strip Data URLs from page backgrounds; save path continues to strip any remaining Data URLs.

---

## Files Changed

| File | Change | Reason |
|------|--------|--------|
| `frontend/src/features/builder/utils/dataUrlGuard.ts` | Created | Shared `isDataUrl`, `stripDataUrlFromBackground`, `DATA_URL_ERROR_MESSAGE` |
| `frontend/src/features/builder/utils/__tests__/dataUrlGuard.test.ts` | Created | Unit tests for dataUrlGuard |
| `frontend/src/features/builder/stores/useBuilderStore.ts` | Modified | Added `normalizeDefinitionForLoad`; call it on API and localStorage load; refactored save to use `stripDataUrlFromBackground` |
| `frontend/src/features/builder/components/properties/BackgroundPropertiesPanel.tsx` | Modified | Input guard: reject Data URL in URL field; show `DATA_URL_ERROR_MESSAGE`; clear error on asset select/remove |
| `docs/tasks/5.1/T07-data-url-guard-and-cleanup.uat.md` | Created | UAT checklist |
| `docs/tasks/5.1/T07-data-url-guard-and-cleanup.uat-results.md` | Created | UAT results |

---

## Acceptance Criteria Verification

### AC1: Data URL backgrounds are rejected at input with clear errors
- **Status:** PASS (implementation)
- **Evidence:** BackgroundPropertiesPanel checks `isDataUrl(value)` in URL field onChange; when true, sets `dataUrlError` to `DATA_URL_ERROR_MESSAGE` and does not call `onBackgroundChange`. Error displayed in amber alert below input.

### AC2: Strip/normalize Data URL background on definition load
- **Status:** PASS
- **Evidence:** `normalizeDefinitionForLoad` strips Data URLs from all page backgrounds; called before `withSafeDefaults` when loading from API (`preferred.definition`) and from localStorage fallback. Uses `stripDataUrlFromBackground` for each page.

### AC3: No base64 blobs remain in DefinitionJSON after save
- **Status:** PASS
- **Evidence:** `normalizeDefinitionForSave` uses `stripDataUrlFromBackground` for each page background. Data URLs without asset ref → background removed; Data URLs with asset ref → value cleared, asset kept.

---

## Test Evidence

### Lint
```
No ESLint errors on: dataUrlGuard.ts, useBuilderStore.ts, BackgroundPropertiesPanel.tsx
```

### Unit Tests
```
dataUrlGuard.test.ts: 8 tests (isDataUrl, stripDataUrlFromBackground, DATA_URL_ERROR_MESSAGE)
Run: npx vitest run src/features/builder/utils/__tests__/dataUrlGuard.test.ts
```

### Build
- Pre-existing TS error in phoneValidation.ts (libphonenumber-js); unrelated to T07.
- Touched files compile; no new TS errors.

---

## Manual UAT Steps

See `T07-data-url-guard-and-cleanup.uat.md`. Human verification recommended for AC1–AC3 and regression.

---

## Known Limitations / Out-of-Scope

- None for this task.

---

## Recommended Next Step

Ready for human UAT. Merge after human verification passes.
