# Task Retrospective: T03

**Story:** 5.1  
**Task:** Backend Asset Service + Upload API  
**Final Status:** ✅ HumanDone  
**Date:** 2026-02-09

---

## What Went Well

| What Went Well | Evidence |
|----------------|----------|
| Upload + validation behavior covered by automated tests | `backend/tests/test_assets_upload.py`, `T03-backend-asset-service-and-upload-api.completion.md` |
| UAT passed with no defects | `T03-backend-asset-service-and-upload-api.uat-results.md` |

## What Went Wrong

| Issue | Root Cause | Evidence |
|-------|------------|----------|
| SQLite schema defaults required workarounds | Local test harness didn’t emulate SQL Server schemas/functions | `backend/tests/conftest.py`, `backend/modules/assets/service.py` |

## Prevention Actions

| Issue | Prevention Action | Owner |
|-------|-------------------|-------|
| SQLite schema defaults | Add schema-attach helper + explicit IDs for SQLite tests when schemas are used | ralf-dev |

## Test Improvements

### Automated Tests to Add

| Test Type | Description | Location | Command |
|-----------|-------------|----------|---------|
| integration | Upload same file twice and assert `isDuplicate=true` + same `assetId` | `backend/tests/test_assets_upload.py` | `pytest backend/tests/test_assets_upload.py -x` |

### UAT Automation Candidates

- Automate dedup verification (upload same file twice) since it is deterministic and repeated.

## Process Improvements

### For ralf-sm (Decomposition)
- Add explicit verification method for resolver URLs (local vs azure) in AC text.

### For ralf-dev (Execution)
- Preflight: ensure SQLite schema attach is in place when writing tests for schema-qualified models.

### For ralf-uat (Validation)
- Include storage-provider-specific expected URL patterns in UAT checklist.

## Scope Creep Discovered

| Item | Classification | Routing |
|------|----------------|---------|
| None | - | - |

## If We Ran This Again

1. Add dedup test case up front.
2. Preflight SQLite schema attach before adding DB-backed tests.
3. Document storage provider env keys in the task spec for faster UAT setup.
