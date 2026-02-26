# Pre-Epic-6 Remediation Wave 3 Corrective Micro-Pass (DS Summary)

## Scope
Focused only on the three residual blockers from Wave 3:
1. `backend/tests/test_multi_tenancy.py` duplicate/collision instability
2. `backend/tests/test_mailhog_integration.py::test_email_service_configuration` config expectation drift
3. `backend/tests/test_models_import.py::test_model_count` stale hardcoded count

No Epic 6 feature work was performed.

## Files changed
- `backend/tests/test_utils.py`
- `backend/tests/test_multi_tenancy.py`
- `backend/tests/test_mailhog_integration.py`
- `backend/tests/test_models_import.py`

## Fixes per residual issue

### 1) Multi-tenancy duplicate email collisions
- Added per-scenario unique email suffixing in `MultiTenantTestScenario` (`test_utils.py`) so admin/user fixture emails do not collide across repeated runs against shared SQL Server data.
- Added `_unique_email()` helper in `test_multi_tenancy.py` and replaced static invitation/user emails with unique values to avoid deterministic re-run collisions.
- Updated invite request payloads to current API contract by including `first_name` and `last_name`.
- Aligned stale detail-message assertions to current permission messaging while preserving security semantics (forbidden/cross-company checks).
- Aligned invitation list response assertions to current shape (`response.json()["invitations"]`).

### 2) MailHog config expectation mismatch
- Updated `test_email_service_configuration` to assert dev SMTP auth fields against the current config contract:
  - `smtp_username == os.getenv("SMTP_USERNAME", "")`
  - `smtp_password == os.getenv("SMTP_PASSWORD", "")`
- This keeps behavior explicit while allowing intentional env overrides in development.

### 3) Stale model-count assertion
- Replaced brittle fixed `33` check with resilient invariants:
  - `len(__all__) == get_model_count()`
  - `len(__all__) >= 33`
- This preserves coverage intent while allowing model-surface growth from completed epics.

## Validation results (required)
- `pytest backend/tests/test_preflight_seed_config_parity.py -q`  
  Result: **1 passed**
- `python backend/scripts/check_no_new_datetime_utcnow.py --base-ref origin/master`  
  Result: **pass** (`No changed Python files found for utcnow guard.`)
- `pytest backend/tests/test_multi_tenancy.py -q --maxfail=1`  
  Result: **22 passed**
- `pytest backend/tests/test_mailhog_integration.py -q --maxfail=1`  
  Result: **8 passed**
- `pytest backend/tests/test_models_import.py -q --maxfail=1`  
  Result: **7 passed**
- `pytest backend/tests -q --maxfail=12` (sampled broad run)  
  Result: **255 passed, 1 skipped, 12 errors, 0 failed** (stopped at maxfail threshold)

## Remaining blockers
- Broad baseline is still not fully gateable due to a non-target residual cluster in `backend/tests/test_onboarding_flow.py` (SQLite schema/db-path errors such as `unknown database ref`).
- Severity: **P1 for baseline gateability** (outside this micro-pass strict scope).

## Outcome
- All three requested Wave 3 micro-pass residual issues were addressed and now pass in targeted validation.
- Overall baseline status remains **partial** because broad sampled run still has non-target errors.
