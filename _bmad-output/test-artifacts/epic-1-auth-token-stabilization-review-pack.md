# Epic 1 Auth Token Stabilization Review Pack

Date: 2026-02-26  
Scope: Epic 1 auth/token reliability (JWT generation, auth middleware, auth-adjacent integration tests)

## Findings (ordered by severity)

1. **P0 - JWT unit suite is testing a superseded token contract**
   - `backend/tests/test_jwt_service.py` fails against current implementation (13 failed, 2 passed).
   - Current service intentionally encodes `sub` as `str` per JWT spec, while tests assert `int`.
   - Current service requires DB-backed signatures, while several tests still call legacy positional signatures without `db`.
   - Access-token TTL is now config-driven (default 15 min), while one test still expects 60 min.

2. **P0 - Auth token factory usage is inconsistent across Epic 1+ tests**
   - Multiple tests still call legacy token signatures (no `db`) and will fail as soon as executed.
   - Drift is not isolated to one file; it appears in invitations/onboarding and other auth-adjacent suites.

3. **P0 - Team invitation tests bypass shared fixture architecture and fail before auth logic**
   - `backend/tests/test_team_invitations.py` builds its own SQLite engine and fails with `unknown database ref` because schema-qualified models expect attached schemas.
   - This causes false negatives in auth/token work by failing at DB setup before endpoint behavior is tested.

4. **P1 - Auth middleware suite is healthy but masks broader drift**
   - `backend/tests/test_auth_middleware.py` passes (25/25), confirming runtime JWT/middleware behavior is currently sound.
   - This indicates production auth core is likely fine; instability is mainly test harness and contract alignment.

5. **P2 - Time/deprecation warnings increase future brittleness**
   - Widespread `datetime.utcnow()` warnings and async fixture loop-scope warnings add noise and future risk.
   - Not the current blocker, but should be cleaned after P0 stabilization.

---

## Evidence Snapshot

- `pytest backend/tests/test_jwt_service.py -q` -> **13 failed, 2 passed**
- `pytest backend/tests/test_auth_middleware.py -q --maxfail=1 -vv` -> **25 passed**
- `pytest backend/tests/test_team_invitations.py -q --maxfail=1 -vv` -> **ERROR at setup** (`sqlite3.OperationalError: unknown database ref`)

---

## High-Risk Contract Mismatches (exact)

### A) JWT `sub` type mismatch

`jwt_service` behavior:

```56:60:backend/modules/auth/jwt_service.py
    payload: Dict[str, Any] = {
        "sub": str(user_id),  # JWT spec requires 'sub' to be a string
        "email": email,
        "type": "access",
```

Stale test assertion:

```34:37:backend/tests/test_jwt_service.py
        # Decode and verify
        payload = decode_token(token)
        assert payload["sub"] == 123
```

### B) Legacy function signature calls in tests

Current signature requires `db`:

```20:24:backend/modules/auth/jwt_service.py
def create_access_token(
    db: Session,
    user_id: int,
    email: str,
```

Stale test call:

```119:119:backend/tests/test_jwt_service.py
        token = create_access_token(123, "test@example.com")
```

### C) Stale TTL assumption

Current config path (DB-backed, default 15 min):

```35:45:backend/config/jwt.py
    def get_access_token_expire_minutes(self, db: Session) -> int:
        """
        Get JWT access token expiry from database (ConfigurationService).
        ...
        Returns:
            Access token expiry in minutes (default: 15)
```

Stale test expectation:

```67:69:backend/tests/test_jwt_service.py
        # Should be approximately 1 hour (3600 seconds)
        time_diff = (exp - iat).total_seconds()
        assert 3550 <= time_diff <= 3650  # Allow 50 second tolerance
```

### D) Isolated DB harness in invitation tests

```35:38:backend/tests/test_team_invitations.py
# Test database setup
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
```

This bypasses shared schema-attach logic in `backend/tests/conftest.py`, causing setup failures for schema-qualified tables.

---

## Epic 1 Stabilization Plan (execution order)

1. **Lock token contract in tests (P0)**
   - Update `backend/tests/test_jwt_service.py` to:
     - assert `payload["sub"] == str(user_id)` (or `extract_user_id(payload) == user_id` for business behavior)
     - pass `test_db` to all token factory calls
     - compute expected TTL from `get_access_token_expire_minutes(test_db)` and `get_refresh_token_expire_days(test_db)` (no hardcoded 1h/7d assumptions)

2. **Unify token creation pattern across auth-adjacent tests (P0)**
   - Replace direct legacy calls with one consistent helper (`create_test_token` from `conftest.py`) or direct `create_access_token(db=..., ...)`.
   - Priority files:
     - `backend/tests/test_team_invitations.py`
     - `backend/tests/test_onboarding_flow.py`
     - any remaining legacy call sites from grep results

3. **Move invitation tests onto shared fixtures (P0)**
   - Refactor `test_team_invitations.py` to use `test_db`/`client` from `conftest.py` instead of custom engine/session.
   - Remove file-local DB setup to prevent schema mismatch (`unknown database ref`).

4. **Add a contract guard test (P1)**
   - Add one explicit regression test that validates:
     - JWT `sub` is encoded string
     - `extract_user_id` returns `int`
     - token TTL equals current DB-config values

5. **Noise cleanup pass (P2)**
   - Standardize timezone-aware datetime usage and set `asyncio_default_fixture_loop_scope` in `pytest.ini`.

---

## Proposed Done Criteria for Epic 1 Token Stabilization

- `backend/tests/test_jwt_service.py` green.
- `backend/tests/test_auth_middleware.py` remains green.
- `backend/tests/test_auth_login.py` smoke-green for non-rate-limiting assertions.
- `backend/tests/test_team_invitations.py` no setup error; auth assertions execute.
- Zero remaining legacy token signature calls in `backend/tests` (`create_access_token(` / `create_refresh_token(` without DB context).

---

## Suggested Validation Commands

```powershell
pytest backend/tests/test_jwt_service.py -q
pytest backend/tests/test_auth_middleware.py -q
pytest backend/tests/test_auth_login.py -q --maxfail=1
pytest backend/tests/test_team_invitations.py -q --maxfail=1
```

---

## Recommendation

Treat this as **test contract migration**, not a platform-auth bug fix. The platform behavior (middleware path) is currently healthy; the suite is failing because parts of the test layer still assert a pre-Story-1.13 token model and bypass the shared test infrastructure.
