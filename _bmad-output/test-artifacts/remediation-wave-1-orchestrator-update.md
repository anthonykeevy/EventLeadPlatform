# Remediation Wave 1 - Orchestrator Update

WAVE_1_STATUS: complete

## Checklist
- seed parity preflight: **pass**
- async loop-scope enforcement: **pass**
- no-new datetime.utcnow guard: **pass**

## Notes
- Guardrails implemented as test/config/script-level controls only.
- No Epic 6 feature work implemented.
- No alembic commands were run.

## Recommended next step
- Start **Pre-Epic-6 Remediation Wave 2** focused on:
  1. targeted `datetime.utcnow()` migration in highest-signal modules,
  2. warning-budget reduction,
  3. explicit CI pipeline integration of:
     - `pytest backend/tests/test_preflight_seed_config_parity.py -q`
     - `python backend/scripts/check_no_new_datetime_utcnow.py --base-ref origin/master`

## Urgent login regression micro-fix

### Files changed
- `backend/middleware/auth.py`
- `backend/tests/test_auth_middleware.py`
- `backend/tests/test_auth_login.py`

### Exact behavior restored
- Public auth endpoints (including `/api/auth/login`) are no longer blocked by JWT signature validation when a stale/invalid bearer token header is present.
- Protected endpoint behavior remains strict and unchanged for invalid bearer tokens (`401` preserved).

### Test results
- `pytest backend/tests/test_auth_middleware.py -q`: **pass** (26 passed)
- `pytest backend/tests/test_auth_login.py -q --maxfail=1`: **pass** (14 passed, 1 skipped)
- Direct login check with stale bearer header: **pass**  
  `pytest backend/tests/test_auth_login.py -q -k "login_public_route_ignores_stale_bearer_token"`

### Confirmation
- Login-blocking middleware regression is resolved.
