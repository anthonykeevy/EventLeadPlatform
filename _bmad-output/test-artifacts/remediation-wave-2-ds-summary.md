# Pre-Epic-6 Remediation Wave 2 - DS Summary

Date: 2026-02-26  
Scope: Stabilization + regression protection only (no Epic 6 feature implementation)

## Files changed
- `backend/pytest.ini`
- `backend/tests/test_exception_handler.py`
- `backend/tests/test_database_connection.py`
- `backend/tests/test_invitation_acceptance.py`

## Stabilization fixes applied
1. **Broad-suite collection gate fix**
- Registered missing strict marker in `pytest.ini`:
  - `story_1_4`
- Outcome: broad runs no longer stop at collection with unknown marker error.

2. **High-signal failing suite alignment**
- `test_exception_handler.py`
  - Updated patch targets from `backend.middleware...` to `middleware...` (actual import path in test runtime).
  - Updated response-shape assertions to current exception handler contract (`detail`, `requestId`).
- `test_database_connection.py`
  - Fixed brittle SQLAlchemy session cleanup assertion to validate post-close transaction state (`in_transaction() is False`) instead of deprecated/semantic mismatch on `is_active`.
- `test_invitation_acceptance.py`
  - Updated stale ORM field usage to current models (`CustomDisplayName`, `IsEmailVerified`, `StatusID`).
  - Added required `CountryID` and invitee `FirstName`/`LastName` fixture fields for schema compliance.
  - Added deterministic uniqueness for seeded user/invitation emails to reduce DB collision instability.
  - Updated JWT token factory calls to pass `db` argument (current contract).

## Public auth-route regression fix status
- **Status: PASS / retained**
- Middleware regression protection remains active from micro-fix:
  - public `/api/auth/login` is not blocked by stale/invalid bearer header
  - protected routes still reject invalid bearer tokens with `401`
- Validation evidence:
  - `pytest backend/tests/test_auth_middleware.py -q` -> **26 passed**
  - Regression case `test_public_login_not_blocked_by_invalid_bearer` passes.

## Validation outputs
- `pytest backend/tests/test_preflight_seed_config_parity.py -q`  
  **PASS** (1 passed)
- `python backend/scripts/check_no_new_datetime_utcnow.py --base-ref origin/master`  
  **PASS** (`No changed Python files found for utcnow guard.`)
- `pytest backend/tests/test_jwt_service.py -q`  
  **PASS** (15 passed)
- `pytest backend/tests/test_auth_middleware.py -q`  
  **PASS** (26 passed)
- `pytest backend/tests/test_team_invitations.py -q --maxfail=1`  
  **PASS** (12 passed)

## One broader backend test run sample
- Command (baseline pre-fix):  
  `pytest backend/tests -q --maxfail=12`  
  Result: **blocked at collection** (`1 error`, unknown marker `story_1_4`)

- Command (pre-stabilization sampled execution):  
  `pytest backend/tests -q --maxfail=12 --ignore=backend/tests/test_api_form_publishing.py --ignore=backend/tests/test_api_lead_collection.py`  
  Result: **9 failed, 130 passed, 1 skipped, 3 errors**

- Command (post-stabilization sampled execution):  
  `pytest backend/tests -q --maxfail=12 --ignore=backend/tests/test_api_form_publishing.py --ignore=backend/tests/test_api_lead_collection.py`  
  Result: **12 failed, 181 passed, 1 skipped, 0 errors**

Interpretation:
- Systemic hard-stop collection error removed.
- Setup/runtime **errors reduced from 3 to 0** in sampled run.
- Useful pass signal increased before fail cutoff (**130 -> 181**).
- Remaining instability is now primarily assertion/contract drift in legacy suites rather than collection/setup crashes.

## Warning-budget reduction (targeted)
- Marker warning path reduced in touched scope by explicit marker registration under strict markers.
- Wave 1 `no-new datetime.utcnow` enforcement preserved and re-validated.

## CI/local gate integration status
- Wave 1 guardrails are now part of practical Wave 2 validation flow:
  - `pytest backend/tests/test_preflight_seed_config_parity.py -q`
  - `python backend/scripts/check_no_new_datetime_utcnow.py --base-ref origin/master`
- Auth-token critical suites continue as stable gate set:
  - `test_jwt_service.py`
  - `test_auth_middleware.py`
  - `test_team_invitations.py`

## Remaining blockers for Wave 3
- `test_invitation_acceptance.py` still has multiple API-contract expectation mismatches (response shapes/messages/status assumptions) and one backend defect exposure (`modules.invitations.router` token minting path missing `db` argument).
- `test_log_filters.py::test_sanitize_dict_nested` failing due sanitize return-shape mismatch.
- `test_logging_integration.py` has stale response-shape expectations and fixture FK assumptions (`UserID`/`CompanyID` existence).
- Two broad suites (`test_api_form_publishing.py`, `test_api_lead_collection.py`) exhibit long-running/hang behavior and need deterministic fixture/service isolation.
