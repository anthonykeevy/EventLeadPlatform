# Task Retrospective: T07 - Data URL Guard + Cleanup

**Story:** 5.1 - Background Asset Management  
**Task:** T07 - Data URL Guard + Cleanup  
**Final Status:** Complete (human UAT pending)  
**Date:** 2026-02-13

---

## What Went Well

| What Went Well | Evidence |
|----------------|----------|
| Shared utility pattern (`dataUrlGuard.ts`) for reuse across input, load, save paths | `dataUrlGuard.ts`: `isDataUrl`, `stripDataUrlFromBackground`, `DATA_URL_ERROR_MESSAGE` |
| Unit tests added for guard logic | `dataUrlGuard.test.ts`: 8 tests covering isDataUrl, stripDataUrlFromBackground, error message |
| Three defense layers implemented | Input (BackgroundPropertiesPanel rejects + shows error); Load (normalizeDefinitionForLoad on API + localStorage); Save (normalizeDefinitionForSave via stripDataUrlFromBackground) |
| Clear user-facing error message | `DATA_URL_ERROR_MESSAGE` constant; displayed in amber alert below URL field |
| Refactored T04 save logic to use shared util | `useBuilderStore.ts` now uses `stripDataUrlFromBackground` instead of inline logic |
| Lint clean on all touched files | No ESLint errors on dataUrlGuard.ts, useBuilderStore.ts, BackgroundPropertiesPanel.tsx |

---

## What Went Wrong

| Issue | Root Cause | Evidence |
|-------|------------|----------|
| Human UAT not executed by agent | Requires authenticated session + builder navigation; no test credentials in scope | `T07-data-url-guard-and-cleanup.uat-results.md` — "Agent did not execute" for AC1–AC3, regression |
| Unit tests not run in session | Task worktree may lack `npm install`; path restrictions in sandbox | Build/vitest runs targeted main workspace |
| Pre-existing build failure | phoneValidation.ts (libphonenumber-js) unrelated to T07 | Build output shows TS2307 on phoneValidation |

---

## Prevention Actions

| Issue | Prevention Action | Owner |
|-------|-------------------|-------|
| Human UAT deferred | Single-prompt full cycle: commit + push; human runs UAT then merge | ralf-dev, workflow |
| Guard logic tasks | Add unit tests for pure functions (isDataUrl, strip*) before integration | ralf-dev |
| Multi-path cleanup tasks | Document all entry points (input, load, save) in task spec | ralf-sm |

---

## Test Improvements

### Automated Tests Added

| Test Type | Description | Location |
|-----------|-------------|----------|
| Unit | `isDataUrl` — data: vs https vs empty | `dataUrlGuard.test.ts` |
| Unit | `stripDataUrlFromBackground` — no asset, with asset, external URL, undefined | `dataUrlGuard.test.ts` |
| Unit | `DATA_URL_ERROR_MESSAGE` non-empty | `dataUrlGuard.test.ts` |

### UAT Automation Candidates

- **AC1:** Browser automation: paste Data URL into URL field → assert error message visible, `onBackgroundChange` not called.
- **AC3:** After save, parse response/definition JSON, assert no `"data:"` in any `page.background.value`.

---

## Process Improvements

### For ralf-sm (Decomposition)
- Guard/cleanup tasks: list all entry points (input, load path(s), save path) in scope.

### For ralf-dev (Execution)
- For pure guard/utils: add unit tests first or alongside implementation.
- Run `npm run test:run` for touched-area tests before completion note.

### For ralf-uat (Validation)
- AC1 (paste Data URL → blocked) is automatable with browser MCP + login.

---

## Scope Creep Discovered

| Item | Classification | Routing |
|------|----------------|---------|
| None | — | — |

---

## If We Ran This Again

1. **Unit tests first** — `isDataUrl` and `stripDataUrlFromBackground` are trivial; tests could have been added before wiring into components.
2. **Explicit entry-point checklist** — Task spec could list: "Input: BackgroundPropertiesPanel URL field; Load: API + localStorage; Save: normalizeDefinitionForSave."
3. **UAT automation** — AC1 (paste Data URL) is a good candidate for browser automation once login is scripted.

---

*Retro completed 2026-02-13*
