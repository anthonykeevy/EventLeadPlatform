# Final Pre-Epic-6 Residual Closeout Micro-Pass — DS Summary

Date: 2026-02-26
Scope: strictly limited to:
- `backend/tests/test_story_1_9_integration.py`
- `backend/tests/test_validators.py`

## Files changed
- `backend/tests/test_story_1_9_integration.py`
- `backend/tests/test_validators.py`

## Fixes per cluster

### A) `test_story_1_9_integration.py`
- Added deterministic per-run identity generation via `_unique_email(...)`.
- Replaced reused/static emails in signup/login/error/transaction tests with unique values.
- Kept duplicate-email behavior test intent intact by reusing the same generated email inside that test only.
- Added explicit `int(...)` cast for `generate_verification_token(..., user_id, ...)` argument to align typing contract.

#### Test-update vs runtime-fix rationale
- **Test update only**.
- Root issue was deterministic data collisions against SQL Server unique index (`UX_User_Email`) from static fixture identities, not a production regression.

### B) `test_validators.py`
- Aligned ACN vectors to current checksum contract:
  - Replaced stale invalid “valid” vector (`123456782`) with known valid `004085616`.
  - Updated combined ABN/ACN tests to the same valid ACN vector.
- Aligned security-edge expectations to current validator behavior:
  - Validators are pure format/checksum functions that sanitize to digits; they do not execute SQL.
  - Updated malicious/unicode assertions to ensure deterministic boolean outcomes and no bypass on ACN paths, without changing runtime semantics.

#### Test-update vs runtime-fix rationale
- **Test update only**.
- No proven runtime regression: validator implementation is internally consistent with current normalization/checksum contract.

## Validation results (required)
- `pytest backend/tests/test_story_1_9_integration.py -q --maxfail=1`
  - **7 passed, 0 failed**
- `pytest backend/tests/test_validators.py -q --maxfail=1`
  - **25 passed, 0 failed**
- `pytest backend/tests/test_story_1_11_switching.py -q --maxfail=1`
  - **10 passed, 0 failed**
- `pytest backend/tests/test_story_1_12_validation.py -q --maxfail=1`
  - **22 passed, 0 failed**
- `pytest backend/tests/test_story_1_13_config_service.py -q --maxfail=1`
  - **21 passed, 0 failed**
- `pytest backend/tests/test_story_1_11_integration.py -q --maxfail=1`
  - **9 passed, 0 failed**
- `pytest backend/tests/test_request_logging.py -q --maxfail=1`
  - **10 passed, 0 failed**
- `pytest backend/tests/test_security.py -q --maxfail=1`
  - **17 passed, 0 failed**
- `pytest backend/tests/test_preflight_seed_config_parity.py -q`
  - **1 passed, 0 failed**
- `python backend/scripts/check_no_new_datetime_utcnow.py --base-ref origin/master`
  - **pass** (`No changed Python files found for utcnow guard.`)
- `pytest backend/tests -q --maxfail=12`
  - **515 passed, 5 skipped, 0 failed** (completed with aggregate counts)

## Remaining blockers
- None found in this closeout scope.

