# Story 6.1 Single-Session Dev Prompt

**Purpose:** Copy this entire prompt into a new chat for Story 6.1 implementation.  
**Agent:** `@bmad-agent-bmm-dev`  
**Workspace:** Open story worktree in Cursor: `C:\wt\elp\story-epic6-6.1-ai-foundation-static-validator`

---

## Copy everything below this line into a new chat

```markdown
@bmad-agent-bmm-dev Implement Story 6.1: AI Foundation - Static Validator in a single session.

Treat these as source of truth:
- `docs/stories/story-6.1.md`
- `docs/stories/story-context-6.1.xml`
- `docs/stories/STORY-6.1-UAT-TEST-GUIDE.md`
- `docs/stories/EPIC-6-WORKFLOW-GUIDE.md`

---

## Git discipline (MANDATORY)

- Work only in story worktree: `C:\wt\elp\story-epic6-6.1-ai-foundation-static-validator`
- Branch must be: `story/epic6-6.1-ai-foundation-static-validator`
- Do not work on `master`
- No task branches for this story
- Use PowerShell syntax (`;` not `&&`)

### Worktree and branch preflight (DO FIRST, NO EXCEPTIONS)

1. Run and report output:
   - `Get-Location`
   - `git branch --show-current`
   - `git status -sb`
2. If current folder is not `C:\wt\elp\story-epic6-6.1-ai-foundation-static-validator` or branch is not `story/epic6-6.1-ai-foundation-static-validator`, STOP.
3. When stopped, provide the exact instruction: "Open `C:\wt\elp\story-epic6-6.1-ai-foundation-static-validator` in Cursor and rerun this prompt."
4. Do not implement anything until preflight passes.

---

## Scope (Story 6.1 only)

Implement backend static validator endpoint:
- `POST /api/form-validate`
- Input: `DefinitionJSON`
- Output: machine-readable validation result with:
  - `valid`
  - `schemaErrors`
  - `boundaryViolations`
  - `collisions`
  - `summary`

Validation must include:
1. Schema validation
2. Canvas boundary checks
3. Component collision checks
4. Deterministic behavior for same input

Do not implement:
- AI model integration
- Builder chat UI integration
- Stripe/payment features

---

## Green CI/CD Rule (MANDATORY)

The quality gate is strict. TEA baseline is 94/100 and must be preserved.

Before closeout commit, you MUST run:
- Frontend touched: `npm run lint`; `npm run test:unit -- --watch=false`
- Backend touched: `python -m pytest --tb=short`

### Anti-hallucination protocol
- Read exact test/lint output.
- If output is truncated, timed out, or missing final summary, treat as FAILED.
- Re-run until final summary is visible and passing.
- Do not claim success without explicit final pass summary.

### Zero-tolerance closeout condition
- Do not close story while touched-scope lint/tests are failing.
- Fix issues first, then re-run checks.

---

## Story Evidence Contract (MANDATORY)

Before handing to human UAT, provide:
1. Commands run (exact command + working directory)
2. Final summaries copied from terminal output
3. Pass/fail table (frontend/backend)
4. Checks not run, with reason
5. Manual-only checks recommended for human

If any evidence item is missing, story is NOT READY for UAT.

---

## Agent-Owned UAT Policy (Story 6.1)

- Execute all tests in `docs/stories/STORY-6.1-UAT-TEST-GUIDE.md` directly as the dev agent.
- Do not ask the human to run API/backend UAT steps.
- Produce `docs/stories/STORY-6.1-UAT-RESULTS.md` with pass/fail outcomes and evidence.
- Proceed to closeout workflow when tests pass and Green CI/CD is satisfied.

### Escalate only for true human-only blockers

Escalation is allowed only when blocked by constraints the agent cannot resolve, such as:
- missing credentials/secrets requiring human entry,
- unavailable protected environment access,
- external system/network controls outside agent permissions.

When escalating, include:
1. Exact step attempted
2. Command/output evidence
3. Why this cannot be solved agent-side
4. Minimal human action required

Without this evidence, continue execution and do not escalate.

---

## Delivery checklist

1. Implement endpoint and validation logic.
2. Add/adjust tests for valid, schema-invalid, boundary-invalid, collision-invalid, determinism.
3. Update relevant docs/comments where needed.
4. Produce:
   - implementation summary,
   - Green CI/CD evidence section,
   - any residual risks.
5. Commit and push changes on story branch.

---

## Human handoff (only if needed)

Default path for Story 6.1:
- Agent completes implementation, Green CI/CD, and UAT evidence autonomously.
- Human acts as final reviewer/merger only.

Escalation path:
- If and only if true human-only blocker exists, request the minimal human action, then continue to completion.
```

---

*Prompt created for Story 6.1 single-session implementation*  
*Last Updated: 2026-02-26*
