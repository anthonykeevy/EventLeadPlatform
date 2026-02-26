# Final Pre-Epic-6 Story-Contract Alignment Wave — DS Summary

Date: 2026-02-26
Scope: Contract alignment for remaining deterministic failures in:
- `backend/tests/test_story_1_11_switching.py`
- `backend/tests/test_story_1_12_validation.py`
- `backend/tests/test_story_1_13_config_service.py`

## Files changed
- `backend/tests/test_story_1_11_switching.py`
- `backend/tests/test_story_1_12_validation.py`
- `backend/tests/test_story_1_13_config_service.py`
- `backend/middleware/auth.py`

## Fixes per cluster

### A) Story 1.11 switching (2 failures)
- Updated stale primary-company assertions to match current switch-service semantics (`switch_company()` updates JWT context only; it does **not** mutate `IsPrimaryCompany` persistence).
- Kept core guarantees intact:
  - switched company reflected in returned context
  - unauthorized/non-member switching still rejected
  - only one persisted primary membership remains.

**Test update vs runtime fix rationale**
- **Test updates only** for this cluster.
- Reason: runtime behavior is explicit and documented in service code (`switch_company` vs `set_default_company`), so failures were stale test assumptions, not regression.

### B) Story 1.12 validation (7 failures)
- Aligned stale direct calls to current engine signatures:
  - `_validate_phone_number(value, rule, country_id)`
  - `_apply_rule_validation(rule, value, country_id)`
- Updated stale response/shape expectation for `GET /api/countries/{id}/validation-rules/{rule_type}` from list-style assertions to current aggregated metadata dict contract.
- Updated ABN valid-vectors set to current algorithm-verified values (removed stale invalid vector).
- Added explicit mock fields (`DisplayFormat`, `SpacingPattern`, `StripPrefix`, etc.) in rule mocks to avoid pydantic type errors from implicit `Mock` attributes.
- Aligned no-rules behavior expectation to current intentional contract: unknown type without rules returns explicit invalid result.

**Test update vs runtime fix rationale**
- **Test updates only** for this cluster.
- Reason: validator runtime reflects current intended API contracts/signatures; failures were drift in test internals and expected shapes.

### C) Story 1.13 config service (3 failures)
- Restored public endpoint accessibility by adding `/api/config` to JWT middleware `PUBLIC_PATHS`.
- Updated admin endpoint tests to current auth boundary behavior (unauthenticated requests return `401` for `/api/admin/settings/*`).
- Preserved secret non-exposure checks on public config response.

**Test update vs runtime fix rationale**
- **Mixed fix**:
  - **Runtime fix**: `/api/config` was intended public contract but blocked by middleware path omission.
  - **Test updates**: admin endpoint tests previously assumed unauthenticated access (`200`) and were stale against current auth boundary.

## Validation results (required)
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
  - **10 failed, 505 passed, 5 skipped** (completed with aggregate counts)

## Remaining blockers (if any)
- Remaining broad-run failures moved outside this wave’s scope:
  - `backend/tests/test_story_1_9_integration.py` (duplicate deterministic test email usage)
  - `backend/tests/test_validators.py` (ACN vector/expectation drift and security-edge expectation drift)

