# Story 5.6 Single-Session Dev Prompt

**Purpose:** Copy this entire prompt into a **new chat** to implement Story 5.6 in one session (skip Ralf-SM decomposition and task cycle).  
**Agent:** @dev (BMAD Developer Agent)  
**Workspace:** Open the Story worktree in Cursor: `C:\wt\elp\story-epic5-5.6-publish-request-workflow`

---

## Copy everything below this line into a new chat

```markdown
@dev Implement Story 5.6: Publish Request Workflow in a single session. Skip Ralf; no task decomposition. Treat story-5.6.md and story-context-5.6.xml as the sole source of truth.

---

## Git discipline (MANDATORY)

- **Work only in the Story worktree:** `C:\wt\elp\story-epic5-5.6-publish-request-workflow`
- **Branch:** `story/epic5-5.6-publish-request-workflow` (confirm you are on this branch; do NOT work on master)
- **No task branches:** All implementation goes directly on the story branch
- **Commit discipline (from Epic 5 lessons):**
  1. **Implementation commits FIRST** — before any closeout. Run `git status`; if backend/ or frontend/ code is modified, commit it with `feat(5.6): <description>`. Do NOT leave implementation uncommitted.
  2. **Closeout commit = docs only** — UAT results, status updates, completion notes go in a separate commit after implementation is committed.
  3. **Verify clean tree before push** — run `git status`; working tree must be clean (or only intentionally untracked)
- **PowerShell:** Do NOT use `&&`; use `;` for command chaining
- **Migrations:** I (human) will run Alembic commands; you create migration files and provide the exact command. Never run `alembic upgrade` yourself

---

## Story inputs (READ THESE)

- **Story:** `docs/stories/story-5.6.md`
- **Context:** `docs/stories/story-context-5.6.xml`
- **UAT guide:** `docs/stories/STORY-5.6-UAT-TEST-GUIDE.md`
- **Epic scope:** `docs/stories/EPIC-5-STATUS.md` (Phase B)
- **Existing:** Form model (FormStatusID); ref.FormStatus; CompanyFormTestConfig; readiness_service; RBAC (Company User vs Company Admin)

---

## Implementation order

1. **Company-level RequirePublishApproval** — Add to company config (extend CompanyFormTestConfig or new CompanyFormPublishConfig). Migration if needed. API to GET/PUT.
2. **FormPublishRequest table** — FormID, RequestedBy, RequestedAt, Message, Status (pending/approved/declined/changes_requested). Migration.
3. ** ref.FormStatus PENDING_REVIEW** — Add if missing; migration to seed.
4. **POST /api/forms/{form_id}/publish-request** — Create request; validate readiness (reuse check_publish_readiness); validate role (Company User only when approval required); set form status to Pending Review; handle duplicates.
5. **GET /api/forms/publish-requests/pending** — Admin-only; return pending requests for company.
6. **Request Publish modal (Builder)** — When Company User + approval required: CTA "Request Publish"; modal with admin selector, optional message; call API; show "Pending Admin Review" on success.
7. **Admin Dashboard queue** — List pending requests; deep link to Review and Publish route (placeholder page ok; full UI in 5.7).
8. **UAT** — Run checks; record evidence in STORY-5.6-UAT-RESULTS.md.

---

## UAT (maximize automation — show evidence for EACH test)

Create `docs/stories/STORY-5.6-UAT-RESULTS.md` with a table:

| Test ID | Description | Command/Action | Result | Evidence |
|---------|-------------|----------------|--------|----------|
| DC1 | RequirePublishApproval config; Company User sees Request Publish | Manual / API | PASS/FAIL | (snippet) |
| DC2 | FormPublishRequest created; form status Pending Review | API / DB | — | — |
| DC3 | Request Publish modal; select admin, message; success | Manual | — | — |
| DC4 | Admin queue visible; deep link works | Manual | — | — |
| DC5 | Duplicate request handled | API / Manual | — | — |
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

1. Company-level RequirePublishApproval config
2. FormPublishRequest table + create/list APIs
3. Request Publish modal in Builder; role-aware CTA
4. Admin Dashboard: pending requests queue + deep link
5. Duplicate request handling
6. `docs/stories/STORY-5.6-UAT-RESULTS.md` with evidence table
7. All implementation committed and pushed; working tree clean

---

## Human handoff

After you complete: I will run the migration (you provide command), run manual UAT, then merge the Story PR to master.
```

---

*Prompt created for Story 5.6 single-session implementation*  
*SM-activated; scope from EPIC-5-STATUS Phase B*  
*Last Updated: 2026-02-16*
