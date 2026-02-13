# Task Completion: T06

**Story:** 3.11  
**Task:** Kiosk Mode (Optional) - Auto-reset + Countdown + Session Rotation  
**Completed:** 2026-02-04  
**Status:** Complete (UAT Passed)

---

## Summary of Changes

Implemented kiosk-mode query params in the public renderer and added inactivity-based reset with visible countdown, including session rotation on kiosk/manual reset.

## Files Changed

| File | Change | Reason |
|------|--------|--------|
| `frontend/src/features/renderer/pages/PublicFormRendererPage.tsx` | Modified | Parse kiosk params and pass to artboard |
| `frontend/src/features/renderer/components/PublicFormArtboard.tsx` | Modified | Kiosk timers, countdown banner, reset behavior |
| `frontend/src/features/renderer/pages/PublicFormPreviewShellPage.tsx` | Modified | Forward kiosk params through preview shell |

## Acceptance Criteria Verification

### AC1: When `kiosk=1` and the user is inactive for `autoResetSeconds`, the form clears and validation state resets.
- **Status:** PASS
- **Evidence:** UAT results recorded in `docs/tasks/3.11/T06-kiosk-mode-auto-reset.uat-results.md`

### AC2: A visible countdown appears during the final `countdownSeconds` before reset.
- **Status:** PASS
- **Evidence:** UAT results recorded in `docs/tasks/3.11/T06-kiosk-mode-auto-reset.uat-results.md`

### AC3: `clientSessionId` changes on kiosk reset (and on manual reset when kiosk mode enabled).
- **Status:** PASS
- **Evidence:** UAT results recorded in `docs/tasks/3.11/T06-kiosk-mode-auto-reset.uat-results.md`

### AC4: When kiosk mode is disabled, existing behavior is unchanged.
- **Status:** PASS
- **Evidence:** UAT results recorded in `docs/tasks/3.11/T06-kiosk-mode-auto-reset.uat-results.md`

## Test Evidence

### Automated Tests
```powershell
cd frontend
npm run lint
# ERROR: 'eslint' is not recognized as an internal or external command.

npm run build
# ERROR: 'tsc' is not recognized as an internal or external command.
```

### Build Verification
Not completed due to missing frontend dependencies (eslint/tsc not available).

## Manual UAT Steps

For human verification:

1. [ ] Open a public link with `?kiosk=1&autoResetSeconds=10&countdownSeconds=5`  
   -> Verify countdown appears and form clears after timeout.
2. [ ] Interact with a field, wait <10s, then interact again  
   -> Verify timer resets and countdown restarts.
3. [ ] Click manual Reset while kiosk mode enabled  
   -> Verify form clears and session rotates.
4. [ ] Open the same public link without `kiosk=1`  
   -> Verify existing behavior unchanged.

## Known Limitations / Out-of-Scope Items

- [ ] Dashboard/builder UI for kiosk configuration -> Route to: ralf-sm
- [ ] Advanced session analytics -> Route to: ralf-sm

## Recommended Next Step

**Ready for handoff** — automated lint/build still need dependencies installed to run.
