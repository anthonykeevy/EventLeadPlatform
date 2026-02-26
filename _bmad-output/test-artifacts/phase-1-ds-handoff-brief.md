# Phase 1 DS Handoff Brief (Epic 1 Auth Token Stabilization)

Owner workflow: **BMM Dev Story (DS)**  
Execution agent: **💻 Amelia (Developer Agent)**  
Orchestrator chat: **this current chat**

---

## How to run in a new chat

1. Load Amelia:
   - `/bmad:all precision.:agent:dev`
2. Start DS workflow:
   - `/bmad-bmm-dev-story`
3. Paste the full brief below as the task context.

---

## DS Task Context (paste into Amelia chat)

You are implementing **Phase 1: Epic 1 Auth Token Stabilization** for EventLeadPlatform.

Primary reference:
- `_bmad-output/test-artifacts/epic-1-auth-token-stabilization-review-pack.md`

### Objective
Stabilize auth/token tests by aligning test contracts with current JWT implementation and shared fixture architecture.

### Scope (Phase 1 only)
1. **Fix JWT contract drift in `backend/tests/test_jwt_service.py`**
   - Align expectations with current JWT behavior:
     - `sub` encoded as string in payload.
     - `extract_user_id()` returns int.
   - Update all token creation calls to current signatures requiring `db`.
   - Remove hardcoded token TTL assumptions; assert against config-driven values.

2. **Fix test harness drift in `backend/tests/test_team_invitations.py`**
   - Eliminate stale local DB harness that causes setup failure (`unknown database ref`).
   - Use shared test fixtures/patterns compatible with current backend schema setup.
   - Update legacy token creation calls to current signature (`db` included).

3. **Do not broaden scope**
   - No large refactors outside these two files unless required for compilation/test execution.
   - No changes to production auth logic unless a test reveals a genuine defect.

### Acceptance Criteria
- `backend/tests/test_jwt_service.py` passes.
- `backend/tests/test_auth_middleware.py` remains passing.
- `backend/tests/test_team_invitations.py` no longer fails at DB setup and executes auth-related assertions.
- No remaining legacy `create_access_token(...)` or `create_refresh_token(...)` usage in edited files.

### Validation Commands
Run and include results:

```powershell
pytest backend/tests/test_jwt_service.py -q
pytest backend/tests/test_auth_middleware.py -q
pytest backend/tests/test_team_invitations.py -q --maxfail=1
```

### Required DS Output (must provide)
At the end, produce a concise implementation summary with:
1. Files changed
2. Exact contract changes made
3. Test results (pass/fail counts)
4. Known risks or unresolved failures
5. Recommended next step (if blocked)

Also save this summary to:
- `_bmad-output/test-artifacts/phase-1-ds-implementation-summary.md`

---

## Orchestrator Loop (back in this chat)

After DS run completes, return here with:
- DS summary content (or file path),
- test outputs,
- any blockers.

Orchestrator will then:
1. Review DS output and risks,
2. Adjust plan if issues emerged,
3. Route next step (CR, TEA review, or corrective DS iteration).

---

## If problems occur outside workflow

If DS hits unexpected blockers (fixture architecture, schema behavior, hidden dependencies):
- Pause broad code changes.
- Capture blocker details in the DS summary file.
- Return control to orchestrator chat for replanning before continuing.

