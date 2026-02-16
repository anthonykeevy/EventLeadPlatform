# Story 5.3 Lessons Learned

**Story:** 5.3 - Schema + Validation Alignment  
**Mode:** Single-session (no task decomposition)  
**Date:** 2026-02-16  

---

## Single-Session Workflow

Story 5.3 was the first Epic 5 story delivered without Ralf-SM task decomposition. Dev implemented the full story in one chat using `STORY-5.3-SINGLE-SESSION-DEV-PROMPT.md`.

### What Worked

- **Prompt with implementation order** — Explicit order (schema → invariants → versioning → migration → API → tests) kept the agent on track.
- **UAT evidence table** — Requiring a table with Test ID, Command, Result, Evidence made UAT auditable and reduced "did it pass?" ambiguity.
- **Git discipline in prompt** — Implementation commits first, closeout docs separately; prevented uncommitted code (T04 lesson applied).
- **Migration handoff** — Agent creates migration; human runs Alembic; no session crash from DB operations.

### What to Improve

- **Scope gate** — For single-session, keep scope tight. Story 5.3 was backend-heavy; frontend changes were minimal. If scope grows, consider reverting to task decomposition.
- **Evidence cap** — Long pytest/build output can crash sessions. Prompt already says cap output; enforce in future prompts.

---

## Reusable Patterns

| Pattern | When to Use |
|---------|-------------|
| **Single-session prompt** | Backend-heavy stories with clear DCs; schema/API/tests; limited or no frontend |
| **UAT evidence table** | All stories (task or single-session); format: Test ID, Description, Command, Result, Evidence |
| **Implementation order** | Include in prompt for multi-step work; reduces backtracking |

---

## Test Improvements

- **Compatibility tests** — `test_form_definition_schema_5_3.py` provides regression protection for DefinitionJSON structure. Run in CI.
- **Schema-from-DB API** — Curl or pytest for GET /api/form-schema/{version}; 200 for known, 404 for unknown.

---

*Append-only. Do not delete lessons.*
