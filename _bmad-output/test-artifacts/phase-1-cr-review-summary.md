# Phase 1 CR Review Summary (Auth-Token Stabilization)

Date: 2026-02-26  
Scope reviewed:
- `backend/tests/test_jwt_service.py`
- `backend/tests/test_team_invitations.py`
- Immediate fixture/helper context in `backend/tests/conftest.py`

## Findings by severity

### Critical
- None.

### High
- None.

### Medium
1. **Reference-data dependency is environment-sensitive in invitation tests**
   - `test_team_invitations.py` now intentionally relies on existing SQL Server reference rows (`active`, `company_admin`, `company_user`, `pending`, `AU`, etc.) via `seed_reference_data()`.
   - This is correct for production-like integration behavior, but it means environments with incomplete reference seed data will fail fast at runtime.
   - Risk: portability/reproducibility drift across developer machines and CI environments if DB seed parity is not enforced.

### Low
1. **`test_token_uniqueness` no longer verifies uniqueness semantics**
   - In `test_jwt_service.py`, the test now validates repeated token generation is valid, but no longer asserts uniqueness.
   - This avoids false failures due same-second token issuance, but also drops explicit coverage for `jti`-style uniqueness behavior (if that behavior is desired in future).

2. **Minor maintainability wording drift**
   - Some JWT test docstrings/comments still mention old fixed TTL language while assertions are now config-driven.
   - No behavior risk; slight readability debt.

## Required fixes vs optional improvements

### Required fixes (before Phase 1 closeout)
- None.

### Optional improvements (recommended)
1. Add/maintain a DB-seed preflight check in CI to guarantee required reference rows for invitation integration tests.
2. If token uniqueness is a product requirement, add a deterministic uniqueness claim (e.g., `jti`) and assert on that; otherwise rename the test to reflect current intent.
3. Refresh stale test docstrings/comments to match config-driven TTL behavior.

## Go/No-Go recommendation
- **Recommendation: GO**
- Rationale:
  - No Critical/High defects found in Phase 1 reviewed scope.
  - Contract alignment with current JWT behavior is correct (`sub` handling, `db` token factory signatures, config-driven TTL assertions).
  - Invitation integration suite is now stable and passing on production-like fixture flow.
  - Remaining items are non-blocking maintainability/operational hardening tasks.
