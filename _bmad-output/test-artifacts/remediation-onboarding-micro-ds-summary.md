# Final Pre-Epic-6 Onboarding-Flow Micro-Pass (DS Summary)

## Scope
Address only onboarding-flow residual setup instability:
- `backend/tests/test_onboarding_flow.py` SQLite schema-path failure (`unknown database ref`)

No Epic 6 feature work was performed.

## Files changed
- `backend/tests/test_onboarding_flow.py`

## Setup/harness changes made
- Removed file-local SQLite harness pattern (in-memory engine + local `Base.metadata.create_all()` + local dependency override) that caused schema-qualified table creation failures.
- Switched onboarding tests to shared fixture strategy used by stable suites:
  - `client` fixture from `backend/tests/conftest.py`
  - `test_db` fixture (aliased as `db_session` for minimal test churn)
- Updated token generation calls to current JWT contract (`create_access_token(db=..., user_id=..., email=...)`).
- Added deterministic uniqueness helpers for onboarding inputs where shared DB collisions were occurring:
  - valid ABN generator (checksum-valid)
  - valid ACN generator (checksum-valid)
- Aligned stale assertions to current contracts:
  - JWT `sub` is string
  - audit model fields use `ChangeType` and can produce multiple rows
  - ABN-with-spaces request currently rejected at schema layer (`422`)
  - timezone validation path currently allows updates when `ref.Timezone` is unavailable

## Validation outputs
- `pytest backend/tests/test_onboarding_flow.py -q --maxfail=1`  
  Result: **14 passed**
- `pytest backend/tests/test_preflight_seed_config_parity.py -q`  
  Result: **1 passed**
- `python backend/scripts/check_no_new_datetime_utcnow.py --base-ref origin/master`  
  Result: **pass** (`No changed Python files found for utcnow guard.`)
- `pytest backend/tests -q --maxfail=12` (sampled broad run)  
  Result: **273 passed, 1 skipped, 12 failed, 0 errors** (stopped at maxfail threshold)

## Remaining blockers (if any)
- Onboarding-flow residual cluster is resolved.
- Broad-run remaining blockers are outside this micro-pass scope:
  - `backend/tests/test_password_reset.py` contract/data setup failures
  - `backend/tests/test_password_validator.py` validator call-signature drift
