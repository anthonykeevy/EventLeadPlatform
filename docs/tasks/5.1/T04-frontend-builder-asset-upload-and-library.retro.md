# Task Retrospective: T04

**Story:** 5.1  
**Task:** Frontend Builder Asset Upload + Library + Reference Wiring  
**Final Status:** ✅ HumanDone  
**Date:** 2026-02-10

---

## What Went Well

| What Went Well | Evidence |
|----------------|----------|
| UAT passed (AC1–AC3, regression, post, edge) | `T04-frontend-builder-asset-upload-and-library.uat-results.md` |
| Asset upload + library + ref wiring implemented and stable | Builder stores asset refs; no Data URLs in DefinitionJSON |
| Background Style (Image ↔ Colour) persistence added | `colorValue` + type-only switch; both branches retained |
| Upload failure logging and dimension hint added | Backend `asset_upload_*` logs; frontend helper text with max dimensions |

## What Went Wrong

| Issue | Root Cause | Evidence |
|-------|------------|----------|
| Logger.info(msg=...) caused TypeError | Python logging has no `msg=` kwarg; first positional is message | Backend upload 500; fixed in service.py |
| LogRecord KeyError on "filename" | Reserved attribute in logging.LogRecord | Backend upload 500; fixed with asset_* prefix in extra |
| JPG "Invalid file type" (empty file.type) | Some browsers send empty MIME for .jpg (e.g. OneDrive path) | Frontend relaxed to allow by extension; backend normalizes image/jpg→jpeg |

## Prevention Actions

| Issue | Prevention Action | Owner |
|-------|-------------------|-------|
| Logger API misuse | Use only (msg, *args, extra=) for stdlib logging; never pass reserved keys in extra | ralf-dev |
| MIME/extension mismatch | Document: allow image by extension when file.type empty; normalize image/jpg server-side | ralf-dev |

## Test Improvements

### Automated Tests to Add

| Test Type | Description | Location | Command |
|-----------|-------------|----------|---------|
| unit | Frontend: looksLikeImageFile('file.jpg') when file.type === '' returns true | AssetLibrary or assetsApi test | `npm run test` |
| integration | Backend: upload with Content-Type image/jpg returns 201 and stored as image/jpeg | test_assets_upload.py | `pytest backend/tests/test_assets_upload.py` |

### UAT Automation Candidates

- Asset upload E2E (with auth fixture) for AC2.
- DefinitionJSON shape check (no data: URL) for AC1.

## Process Improvements

### For ralf-sm (Decomposition)
- When task touches logging, add AC or note: "Use stdlib logging correctly (no msg=, no reserved extra keys)."

### For ralf-dev (Execution)
- Preflight: check logging calls use (format, *args, extra=) and extra keys avoid LogRecord attributes (filename, message, etc.).

### For ralf-uat (Validation)
- Include "Background Style switch (Image ↔ Colour) retains both settings" in regression or edge cases.

## Scope Creep Discovered

| Item | Classification | Routing |
|------|----------------|---------|
| Background colour/image persistence when switching style | In-scope UX fix | Delivered in T04 |
| Upload failure logging + dimension hint | In-scope clarity | Delivered in T04 |

## If We Ran This Again

1. Use correct logging signature and safe extra keys from the start.
2. Add image/jpg→jpeg normalization and extension-based client check in initial implementation.
3. Add colorValue + type-only switch when implementing Background Style toggle.
