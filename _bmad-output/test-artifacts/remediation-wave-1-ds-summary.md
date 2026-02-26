# Pre-Epic-6 Remediation Wave 1 - DS Summary

Date: 2026-02-26  
Scope: P0 testing/framework guardrails only (no Epic 6 feature implementation)

## Files changed
- `backend/pytest.ini`
- `backend/tests/test_preflight_seed_config_parity.py`
- `backend/scripts/check_no_new_datetime_utcnow.py`

## Exact guardrails added

1. **Seed/config parity preflight (hard gate)**
- Added deterministic preflight test:
  - `backend/tests/test_preflight_seed_config_parity.py`
- Gate verifies required integration dependencies exist in active DB session:
  - `ref.UserStatus(active)`
  - `ref.Country(AU)`
  - `ref.UserCompanyRole(company_admin, company_user)`
  - `ref.UserCompanyStatus(active)`
  - `ref.JoinedVia(signup)`
  - `ref.UserInvitationStatus(pending)`
  - `ref.SettingCategory(authentication)`
  - `ref.SettingType(integer)`
  - `config.AppSetting(ACCESS_TOKEN_EXPIRY_MINUTES, REFRESH_TOKEN_EXPIRY_DAYS)` active/non-deleted
- Fails fast with actionable missing-item diagnostics.
- Runnable locally and in CI:
  - `pytest backend/tests/test_preflight_seed_config_parity.py -q`

2. **Async loop-scope enforcement (hard gate)**
- Updated pytest config to explicitly set loop scope:
  - `backend/pytest.ini`
  - `asyncio_default_fixture_loop_scope = function`
- Also corrected pytest config section header to be active (`[pytest]`) so setting is enforced.
- Runtime verification confirms:
  - `asyncio: mode=Mode.AUTO, asyncio_default_fixture_loop_scope=function`
  - deprecation warning path for loop-scope unset is removed for touched scope.

3. **No-new datetime.utcnow guard (hard gate)**
- Added local/CI guard script:
  - `backend/scripts/check_no_new_datetime_utcnow.py`
- Behavior:
  - scans changed Python files (or explicit file list) from git diff
  - fails if new added lines contain `datetime.utcnow(`
  - allows legacy existing usage (Wave 1 is enforcement-only, no full migration)
- Runnable locally and in CI:
  - `python backend/scripts/check_no_new_datetime_utcnow.py --base-ref origin/master`

## Validation command results

- `pytest backend/tests/test_preflight_seed_config_parity.py -q`  
  **PASS** (1 passed)

- `python backend/scripts/check_no_new_datetime_utcnow.py --base-ref origin/master --files backend/tests/test_preflight_seed_config_parity.py backend/scripts/check_no_new_datetime_utcnow.py backend/pytest.ini`  
  **PASS** (`No newly introduced datetime.utcnow() usage detected.`)

- `pytest backend/tests/test_jwt_service.py -q`  
  **PASS** (15 passed)

- `pytest backend/tests/test_auth_middleware.py -q`  
  **PASS** (25 passed)

- `pytest backend/tests/test_team_invitations.py -q --maxfail=1`  
  **PASS** (12 passed)

## Residual blockers for Wave 2
- Legacy `datetime.utcnow()` usage still exists across broader codebase/tests (guard now blocks new usage only).
- High warning volume remains (non-blocking for Wave 1 but should be reduced in Wave 2 hardening).
- CI pipeline wiring for these new guard commands may need explicit insertion in your repo’s active pipeline definition if not already templated.

## Urgent login regression micro-fix

### Files changed
- `backend/middleware/auth.py`
- `backend/tests/test_auth_middleware.py`
- `backend/tests/test_auth_login.py`

### Exact behavior restored
- Public auth routes are no longer blocked by stale/invalid bearer token validation.
- Middleware now treats public paths as non-blocking for missing/invalid/malformed tokens while preserving optional valid-token parsing when present.
- Protected routes retain strict behavior (invalid bearer on protected endpoint still returns `401`).

### Test results
- `pytest backend/tests/test_auth_middleware.py -q`  
  **PASS** (26 passed)
- `pytest backend/tests/test_auth_login.py -q --maxfail=1`  
  **PASS** (14 passed, 1 skipped)
- Direct login regression check:  
  `pytest backend/tests/test_auth_login.py -q -k "login_public_route_ignores_stale_bearer_token"`  
  **PASS** (1 passed; request reached `/api/auth/login` and returned endpoint-level `401` for invalid credentials, not middleware token-signature rejection)

### Regression resolution confirmation
- Login-blocking regression reproduced by requirement and now resolved: stale/invalid bearer no longer causes middleware `401 Invalid token signature` on `/api/auth/login`.
