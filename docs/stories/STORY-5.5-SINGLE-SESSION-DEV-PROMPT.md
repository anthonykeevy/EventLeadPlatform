# Story 5.5 Single-Session Dev Prompt

**Purpose:** Copy this entire prompt into a **new chat** to implement Story 5.5 in one session (skip Ralf-SM decomposition and task cycle).  
**Agent:** @dev (BMAD Developer Agent)  
**Workspace:** Open the Story worktree in Cursor: `C:\wt\elp\story-epic5-5.5-preview-production-governance`

---

## Copy everything below this line into a new chat

```markdown
@dev Implement Story 5.5: Preview/Production Governance Foundations in a single session. Skip Ralf; no task decomposition. Treat story-5.5.md and story-context-5.5.xml as the sole source of truth.

---

## Git discipline (MANDATORY)

- **Work only in the Story worktree:** `C:\wt\elp\story-epic5-5.5-preview-production-governance`
- **Branch:** `story/epic5-5.5-preview-production-governance` (confirm you are on this branch; do NOT work on master)
- **No task branches:** All implementation goes directly on the story branch
- **Commit discipline (from Epic 5 lessons):**
  1. **Implementation commits FIRST** — before any closeout. Run `git status`; if backend/ or frontend/ code is modified, commit it with `feat(5.5): <description>`. Do NOT leave implementation uncommitted.
  2. **Closeout commit = docs only** — UAT results, status updates, completion notes go in a separate commit after implementation is committed.
  3. **Verify clean tree before push** — run `git status`; working tree must be clean (or only intentionally untracked)
- **PowerShell:** Do NOT use `&&`; use `;` for command chaining
- **Migrations:** I (human) will run Alembic commands; you create migration files and provide the exact command. Never run `alembic upgrade` yourself

---

## Story inputs (READ THESE)

- **Story:** `docs/stories/story-5.5.md`
- **Context:** `docs/stories/story-context-5.5.xml`
- **UAT guide:** `docs/stories/STORY-5.5-UAT-TEST-GUIDE.md`
- **Epic scope:** `docs/stories/EPIC-5-STATUS.md` (Phase B)
- **Existing:** Submissions table/schema; FormPublicLink; public form router

---

## Implementation order

1. **Submissions: preview flag** — Add `IsPreview` (or equivalent) to submissions; ensure public form router and submission API set/read it based on link type or request context. Migration if needed.
2. **Test threshold config** — Store per-company: enabled/disabled, threshold value. Use `config.AppSetting` or company-level table. Migration if needed.
3. **Test run counting + audit** — Track test runs (preview submission or "Record test run"); store who, when, form version. Increment count per company/form.
4. **Publish block logic** — When threshold enabled and count below threshold: block publish (or equivalent action); return clear message. UI shows "X more test runs needed".
5. **Readiness badge** — Builder or Dashboard shows readiness: "Ready to publish" when threshold met (or disabled), "X more test runs needed" when not.
6. **UAT** — Run automated checks; record evidence in STORY-5.5-UAT-RESULTS.md.

---

## UAT (maximize automation — show evidence for EACH test)

Create `docs/stories/STORY-5.5-UAT-RESULTS.md` with a table:

| Test ID | Description | Command/Action | Result | Evidence |
|---------|-------------|----------------|--------|----------|
| DC1 | Submissions have preview flag | Query DB or API | PASS/FAIL | (snippet) |
| DC2 | Test threshold stored | — | — | — |
| DC3 | Test runs counted/audited | — | — | — |
| DC4 | Publish blocked when not met | Manual or API | — | — |
| DC5 | Readiness badge visible | Manual | — | — |
| Build/lint | Backend + frontend | pytest; npm run lint | PASS/FAIL | (snippet) |

**Cap long output** — use `Select-Object -First 50` or redirect to file; report pass/fail + first/last lines.

---

## Workflow lessons (from Epic 5)

- **Cap long output** — pytest, npm run build can crash sessions. Limit output.
- **Implementation commits first** — never leave code uncommitted before closeout.
- **Migrations** — create migration files; human runs `alembic upgrade head`.
- **Single session** — Proceed: implement → verify → UAT → record → commit (impl first, then docs) → push.

---

## Deliverables

1. Submissions with preview/production flag; API filtering support
2. Test threshold config (per company); test run counting + audit
3. Publish block when threshold not met; clear UI message
4. Readiness badge in Builder or Dashboard
5. `docs/stories/STORY-5.5-UAT-RESULTS.md` with evidence table
6. All implementation committed and pushed; working tree clean

---

## Human handoff

After you complete: I will run the migration (you provide command), run manual UAT, then merge the Story PR to master.
```

---

*Prompt created for Story 5.5 single-session implementation*  
*SM-activated; scope from EPIC-5-STATUS Phase B*  
*Last Updated: 2026-02-16*
