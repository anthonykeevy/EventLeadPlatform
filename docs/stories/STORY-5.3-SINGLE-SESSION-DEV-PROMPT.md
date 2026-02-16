# Story 5.3 Single-Session Dev Prompt

**Purpose:** Copy this entire prompt into a **new chat** to implement Story 5.3 in one session (skip Ralf-SM decomposition and task cycle).  
**Agent:** @dev (BMAD Developer Agent)  
**Workspace:** Open the Story worktree in Cursor: `C:\wt\elp\story-epic5-5.3-schema-validation-alignment`

---

## Copy everything below this line into a new chat

```markdown
@dev Implement Story 5.3: Schema + Validation Alignment in a single session. Skip Ralf; no task decomposition. Treat story-5.3.md and story-context-5.3.xml as the sole source of truth.

---

## Git discipline (MANDATORY)

- **Work only in the Story worktree:** `C:\wt\elp\story-epic5-5.3-schema-validation-alignment`
- **Branch:** `story/epic5-5.3-schema-validation-alignment` (confirm you are on this branch; do NOT work on master)
- **No task branches:** All implementation goes directly on the story branch
- **Commit discipline (from Epic 5 lessons):**
  1. **Implementation commits FIRST** — before any closeout. Run `git status`; if backend/ or frontend/ code is modified, commit it with `feat(5.3): <description>`. Do NOT leave implementation uncommitted.
  2. **Closeout commit = docs only** — UAT results, status updates, completion notes go in a separate commit after implementation is committed.
  3. **Verify clean tree before push** — run `git status`; working tree must be clean (or only intentionally untracked)
- **PowerShell:** Do NOT use `&&`; use `;` for command chaining
- **Migrations:** I (human) will run Alembic commands; you create migration files and provide the exact command. Never run `alembic upgrade` yourself

---

## Story inputs (READ THESE)

- **Story:** `docs/stories/story-5.3.md`
- **Context:** `docs/stories/story-context-5.3.xml`
- **UAT guide:** `docs/stories/STORY-5.3-UAT-TEST-GUIDE.md`
- **Builder types:** `frontend/src/features/builder/types/builder.types.ts`
- **Current schema:** `backend/schemas/form_definition.py`
- **Story 5.2 schema:** `ref.FormDefaultsSchemaVersion` (see `backend/models/ref/form_defaults_schema_version.py`, `docs/stories/STORY-5.2-DATA-SCHEMA.md`)

---

## Implementation order

1. **Schema expansion** — Expand `backend/schemas/form_definition.py` to model full DefinitionJSON: globalStyles, canvasSettings, FormPage.background, desktopPages/tabletPages/mobilePages, full component structure. Align to `builder.types.ts`. Use `extra="forbid"` or explicit unknown-key handling.
2. **Key invariants** — Enforce: unique component IDs across all pages; logic rule `sourceComponentId ≠ targetComponentId`.
3. **Schema versioning** — Validate `schemaVersion` ("1.0"); document compatibility strategy in `docs/stories/STORY-5.3-SCHEMA-VERSIONING.md`.
4. **SchemaDocument in DB** — Create migration to add `SchemaVersionString` (NVARCHAR(20), e.g. "1.0") to `ref.FormDefaultsSchemaVersion` if needed for API contract; populate `SchemaDocument` with DefinitionJSON JSON Schema (from Pydantic or hand-crafted). Provide migration file; I will run `alembic upgrade head`.
5. **GET /api/form-schema/{version}** — New endpoint: returns JSON Schema from `SchemaDocument` for version (support "1.0" or "1"). 404 for unknown version.
6. **Compatibility tests** — Create pytest tests: builder output fixtures pass validation; invalid structures (missing formId, duplicate IDs, source===target) raise; regression protection.
7. **Integration** — Ensure form save/load endpoints use the expanded schema; Form Builder save flow still works.

---

## UAT (maximize automation — show evidence for EACH test)

Run as many UAT checks as you can automate. For **every** check, record:

- **Test ID** (e.g. DC1-valid, DC4-duplicate-ids)
- **Command or action** (exact command, working dir)
- **Result** (PASS / FAIL)
- **Evidence** (relevant output snippet, truncated if long — cap at ~20 lines to avoid session issues)

Create `docs/stories/STORY-5.3-UAT-RESULTS.md` with a table like:

| Test ID | Description | Command/Action | Result | Evidence |
|---------|-------------|----------------|--------|----------|
| DC1-valid | Valid DefinitionJSON passes | `pytest tests/... -k ...` | PASS | (snippet) |
| ... | ... | ... | ... | ... |

**UAT checks to execute (automate what you can):**

- **DC1:** Valid DefinitionJSON (globalStyles, canvasSettings, background, desktopPages) passes validation — run pytest or inline validation
- **DC1:** Invalid (missing formId) → validation error — pytest or inline
- **DC2:** schemaVersion "1.0" accepted; SchemaDocument populated — query DB or run migration check
- **DC3:** Compatibility tests pass — `python -m pytest backend/tests/...`
- **DC4:** Duplicate component IDs rejected — pytest
- **DC4:** Logic rule source===target rejected — pytest
- **DC5:** GET /api/form-schema/1.0 returns 200 + JSON Schema — curl or pytest
- **DC5:** GET /api/form-schema/99 returns 404 — curl or pytest
- **Build/lint:** `cd backend; python -m pytest` (cap output); `cd frontend; npm run lint` (cap output)

**Manual-only (record as "Human verification required"):** Form Builder save/load in browser; migration execution.

---

## Workflow lessons (from Epic 5)

- **Cap long output** — `npm run build`, `pytest` etc. can crash sessions. Use `Select-Object -First 50` or redirect to file and report pass/fail + first/last lines.
- **Scope boundary** — If backend changes are needed beyond "schema only," document why and commit both.
- **Pre-UAT automated verification** — Run lint/build/tests for touched areas before declaring UAT; record evidence.
- **Single session** — Do not stop for approval. Proceed: implement → verify → UAT → record results → commit (impl first, then docs) → push. Only halt for: migration (I run it), or explicit blocker.

---

## Deliverables

1. Expanded `backend/schemas/form_definition.py`
2. Migration file(s) for SchemaVersionString + SchemaDocument seed (I run migrations)
3. `GET /api/form-schema/{version}` endpoint
4. Compatibility tests in `backend/tests/`
5. `docs/stories/STORY-5.3-SCHEMA-VERSIONING.md`
6. `docs/stories/STORY-5.3-UAT-RESULTS.md` with evidence table
7. All implementation committed and pushed; working tree clean

---

## Human handoff

After you complete: I will run the migration (you provide command), re-verify Form Builder save/load manually, then merge the Story PR to master.
```

---

*Prompt created for Story 5.3 single-session implementation*  
*Last Updated: 2026-02-16*
