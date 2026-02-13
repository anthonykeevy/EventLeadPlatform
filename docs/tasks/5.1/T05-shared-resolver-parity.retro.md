# Task Retrospective: T05 Shared Resolver Parity

**Story:** 5.1 - Background Asset Management  
**Task:** T05 - Shared Resolver Parity (Builder + Renderer)  
**Final Status:** ✅ HumanDone  
**Date:** 2026-02-11

---

## What Went Well

| What Went Well | Evidence |
|----------------|----------|
| ACs passed on first UAT | UAT Results: AC1 Passed, AC2 Passed (`T05-shared-resolver-parity.uat-results.md`) |
| Shared resolver pattern applied cleanly | Single `backgroundAssetResolver.ts` + `useBackgroundImageUrl` hook; both FormBuilderCanvas and PublicFormArtboard use it (Completion Note) |
| Automated verification ran before UAT | Lint, build, pytest all passed (Completion Note § Test Evidence) |
| Pre-approved scope prevented re-confirm loops | Task Spec status, workflow guide (EPIC-5-WORKFLOW-GUIDE) |
| Diagnostic logging clarified 404 noise | `enhanced_diagnostic_logs.py --path-filter assets` showed orphaned asset metadata; documented in session as data/storage issue, not T05 bug |
| Public renderer gap fixed | Previously no background image; now uses same resolver (Completion Note § Summary) |

---

## What Went Wrong

| Issue | Root Cause | Evidence |
|-------|------------|----------|
| Initial build failed (libphonenumber-js) | Package API changed: path `mobile/examples/examples.mobile.json` no longer valid | Dep scan error in terminal; fix: `libphonenumber-js/examples.mobile.json` |
| Initial build failed (objectFit) | `BackgroundDefinition.imageSize` allows `'tile'|'auto'` but CSS `objectFit` does not | T05 FormBuilderCanvas.tsx, PublicFormArtboard.tsx – TS2322 |
| Initial build failed (lib/index) | T05 worktree missing `lib/auth.ts` – branch divergence from main | lib/index.ts imports `./auth` which does not exist |
| Initial build failed (formatFileSize) | Dead code in AssetLibrary; TS6133 unused variable | AssetLibrary.tsx:172 |
| JSX structure error | Added wrapper `<div z-10>` but misplaced closing tag | PublicFormArtboard.tsx – TS17008 "div has no corresponding closing tag" |
| Regression check "Not explicitly reported" | UAT results template does not require explicit pass/fail per regression item | T05-shared-resolver-parity.uat-results.md § Regression Check |

---

## Prevention Actions

| Issue | Prevention Action | Owner |
|-------|-------------------|-------|
| External dep API drift | Run `npm run build` (incl. dep scan) after first implementation pass | ralf-dev |
| objectFit / type mismatch | Add AC or spec note: "Valid CSS objectFit values only" when exposing imageSize to DOM | ralf-sm |
| Branch divergence (missing lib/auth) | Merge master into story branch early when master has parallel changes (EPIC-5-WORKFLOW-GUIDE) | Human / ralf-sm |
| Dead code | ESLint `no-unused-vars` or run lint before completion | ralf-dev |
| JSX structural errors | Run build after each significant JSX/component change | ralf-dev |
| Regression check not explicit | UAT results template: require Pass/Fail/N/A for each regression item | ralf-uat |

---

## Test Improvements

### Automated Tests to Add

| Test Type | Description | Location | Command |
|-----------|-------------|----------|---------|
| Unit | `resolveAssetContentUrl` returns `{base}/api/assets/{id}/content` | `backgroundAssetResolver.ts` | `npm test backgroundAssetResolver` |
| Integration | Form with asset background: builder canvas and PublicFormArtboard both receive same resolved URL | Renderer/builder integration | `npm run test:int` (if configured) |
| E2E | Upload asset → set as background → verify builder and public view show same image | Story 5.1 E2E | `npm run test:e2e` (if configured) |

### UAT Automation Candidates

- **Console check:** `list_console_messages` for asset-related errors (already in AGENT-LOGGING-GUIDE)
- **Network check:** Verify `/api/assets/*/content` returns 200 for referenced assets (diagnostic script exists)

---

## Process Improvements

### For ralf-sm (Decomposition)
- For "resolver parity" tasks: include explicit type/contract verification in AC (e.g. "URL format matches backend contract")
- Clarify scope for build fixes: pre-existing errors that block verification – fix inline vs. separate task

### For ralf-dev (Execution)
- Run `npm run build` after first implementation pass, not only at final verification
- When adding wrapper divs in JSX: verify nesting/closure count matches before moving on
- Document build blockers (lib auth, formatFileSize) in completion as "scope expansion: build fixes"

### For ralf-uat (Validation)
- UAT results: require explicit Pass/Fail/N/A for each regression checklist item
- When asset 404s appear in logs: distinguish "orphan metadata" (data) from "wrong URL/resolver" (defect)

---

## Scope Creep Discovered

| Item | Classification | Routing |
|------|----------------|---------|
| Orphan asset 404s (metadata exists, files missing) | DATA_HYGIENE | Backlog; consider `listBackgrounds` filter or orphan cleanup script |
| Anonymous public form asset load (401) | KNOWN_LIMITATION | Documented in completion; future: signed URLs (T07+) |

---

## If We Ran This Again

1. **Run build after first pass** – Catch libphonenumber, objectFit, lib/auth, formatFileSize before completion.
2. **Explicit regression pass/fail** – UAT results should require Pass/Fail per regression item.
3. **Resolver AC + contract check** – Spec could include "Verify URL format: `{base}/api/assets/{id}/content`" to catch mismatches early.

---

*Retro completed 2026-02-11*
