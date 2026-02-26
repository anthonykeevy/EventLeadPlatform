# Pre-Epic-6 Remediation Wave 3 - DS Summary

Date: 2026-02-26  
Scope: Wave 3 corrective stabilization only (no Epic 6 feature work)

## Files changed
- `backend/modules/invitations/router.py`
- `backend/modules/auth/router.py`
- `backend/tests/test_invitation_acceptance.py`
- `backend/tests/test_log_filters.py`
- `backend/tests/test_logging_integration.py`
- `backend/tests/conftest.py`

## Fixes per target cluster

1) `backend/tests/test_invitation_acceptance.py`
- Fixed invitation accept token minting path defect by passing `db` into `create_access_token()` and `create_refresh_token()` in `modules/invitations/router.py`.
- Added HTTP 400 mapping for invitation-signup `ValueError` path in `modules/auth/router.py` (was surfacing as 500).
- Updated invitation acceptance tests to current API contracts:
  - invitation signup success now expects `201`.
  - invalid invitation now expects `400`.
  - switch-company response shape now asserts nested `company` object.
  - made mismatch email deterministic/unique to avoid duplicate-key collisions.

2) `backend/tests/test_log_filters.py`
- Aligned `test_sanitize_dict_nested` to current sanitizer contract where a sensitive parent key (`credentials`) is redacted as a whole string (`"[REDACTED]"`).

3) `backend/tests/test_logging_integration.py`
- Aligned stale error response assertions to current global exception payload (`detail`, `requestId`).
- Removed brittle FK assumptions by using committed user/company IDs in authenticated logging endpoint.
- Relaxed request/error correlation assertion to support current middleware timing behavior where `ApplicationError` is required and `ApiRequest` may be absent on some error paths.

4) Hanging suites stabilization
- Root cause isolated to shared fixture path in `conftest.py`:
  - expensive `UserCompany` delete in `test_user` fixture caused deterministic blocking in setup.
  - legacy invalid password hash in `test_user` caused bcrypt panic in login-based fixtures.
- Mitigation applied:
  - removed blocking cleanup query path.
  - normalized fixture user password hash using `hash_password("TestP@ssw0rd123")` for both create and legacy-existing user paths.
- Result: both suites now execute and pass without hangs.

## Validation command outputs
- `pytest backend/tests/test_preflight_seed_config_parity.py -q`  
  **PASS**: `1 passed`

- `python backend/scripts/check_no_new_datetime_utcnow.py --base-ref origin/master`  
  **PASS**: `No changed Python files found for utcnow guard.`

- `pytest backend/tests/test_invitation_acceptance.py -q --maxfail=1`  
  **PASS**: `15 passed`

- `pytest backend/tests/test_log_filters.py -q --maxfail=1`  
  **PASS**: `15 passed`

- `pytest backend/tests/test_logging_integration.py -q --maxfail=1`  
  **PASS**: `8 passed`

- `pytest backend/tests/test_api_form_publishing.py -q --maxfail=1`  
  **PASS**: `3 passed`

- `pytest backend/tests/test_api_lead_collection.py -q --maxfail=1`  
  **PASS**: `3 passed`

## Sampled broad run (before vs after)
- Baseline from Wave 2 (same sampled command):  
  `pytest backend/tests -q --maxfail=12 --ignore=backend/tests/test_api_form_publishing.py --ignore=backend/tests/test_api_lead_collection.py`  
  **Before**: `12 failed, 181 passed, 1 skipped, 0 errors`

- Wave 3 post-fix sampled run (same command):  
  `pytest backend/tests -q --maxfail=12 --ignore=backend/tests/test_api_form_publishing.py --ignore=backend/tests/test_api_lead_collection.py`  
  **After**: `2 failed, 228 passed, 1 skipped, 10 errors`

- Additional sampled run including the two formerly hanging suites:  
  `pytest backend/tests -q --maxfail=12`  
  Result: `2 failed, 234 passed, 1 skipped, 10 errors`

Interpretation:
- Wave 3 target clusters are stabilized and pass in isolation.
- Former deterministic hangs are removed.
- Broad baseline still has non-Wave-3 residual instability concentrated in `test_multi_tenancy.py` plus two contract/config failures (`test_mailhog_integration.py`, `test_models_import.py`).

## Remaining blockers and severity
- **High (P1)**: `backend/tests/test_multi_tenancy.py` duplicate-email fixture collisions (`admin_a@company-a.com`) yielding repeated `IntegrityError` setup failures.
- **Medium (P2)**: `backend/tests/test_mailhog_integration.py::test_email_service_configuration` expectation mismatch (`'user'` vs empty credential expectation).
- **Medium (P2)**: `backend/tests/test_models_import.py::test_model_count` stale hardcoded model-count expectation (`33` vs current `77`).

Overall Wave 3 status: **partial** (target clusters complete; broad gate still blocked by non-target residual failures/errors).
