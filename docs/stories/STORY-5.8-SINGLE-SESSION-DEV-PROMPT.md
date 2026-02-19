# Story 5.8 Single-Session Dev Prompt

**Purpose:** Copy this entire prompt into a **new chat** to implement Story 5.8 in one session (BMAD method; no task decomposition).  
**Agent:** @dev (BMAD Developer Agent)  
**Workspace:** Open the Story worktree in Cursor: `C:\wt\elp\story-epic5-5.8-admin-review-publish-activation`

---

## Copy everything below this line into a new chat

```markdown
@dev Implement Story 5.8: Admin Review & Publish + Activation in a single session. Treat story-5.8.md, story-context-5.8.xml, and STORY-5.8-PM-DECISIONS.md as the sole source of truth.

---

## Git discipline (MANDATORY)

- **Work only in the Story worktree:** `C:\wt\elp\story-epic5-5.8-admin-review-publish-activation`
- **Branch:** `story/epic5-5.8-admin-review-publish-activation` (confirm you are on this branch; do NOT work on master)
- **No task branches:** All implementation goes directly on the story branch
- **Commit discipline (from Epic 5 lessons):**
  1. **Implementation commits FIRST** — before any closeout. Run `git status`; if backend/ or frontend/ code is modified, commit it with `feat(5.8): <description>`. Do NOT leave implementation uncommitted.
  2. **Closeout commit = docs only** — UAT results, status updates, completion notes go in a separate commit after implementation is committed.
  3. **Verify clean tree before push** — run `git status`; working tree must be clean (or only intentionally untracked)
- **PowerShell:** Do NOT use `&&`; use `;` for command chaining
- **Migrations:** I (human) will run Alembic commands; you create migration files and provide the exact command. Never run `alembic upgrade` yourself

---

## Story inputs (READ THESE)

- **Story:** `docs/stories/story-5.8.md`
- **Context:** `docs/stories/story-context-5.8.xml`
- **PM Decisions:** `docs/stories/STORY-5.8-PM-DECISIONS.md` — source of truth
- **UAT guide:** `docs/stories/STORY-5.8-UAT-TEST-GUIDE.md`
- **SM suggestions:** `docs/stories/STORY-5.8-SM-REVIEW-SUGGESTIONS.md` — incorporate where reasonable
- **Existing:** FormReviewPage.tsx, PendingPublishRequestsCard.tsx, FormDetailView, EditFormModal, public_form_router.py, public_links_router.py, Form model, FormPublicLink, FormVersion, FormPublishRequest, Event model, CompanyFormTestConfig

---

## Implementation order (phased)

### Phase 1: Data model + Approval options
1. **Migration:** Add ref.FormStatus UNPUBLISHED if not present; Form.UnpublishMode (MANUAL | EVENT_END | SCHEDULED), Form.ScheduledUnpublishDate (nullable). Provide exact `alembic upgrade head` command for human.
2. **FormReviewPage:** Add "Approve only" and "Approve & Publish" options. Approve only → form stays Ready to publish; Approve & Publish → publish immediately.
3. **Approve only flow:** Form state "Ready to publish"; Admin can publish with one click from FormReviewPage or Dashboard (no re-request).
4. **Publish flow:** On approve-and-publish (and direct publish): auto-create FormPublicLink PRODUCTION if none; set FormVersion.IsActive; stable token.

### Phase 2: Unpublish
5. **Unpublish action:** FormReviewPage, Event Dashboard form card — Unpublish button. Form → UNPUBLISHED; FormPublicLink.IsActive=false.
6. **Unpublish modes UI:** On publish (or form/event settings): Manual, Event end date, Schedule. When EVENT_END: show Event.EndDate. When SCHEDULED: date picker.
7. **Default unpublish mode:** MANUAL when publishing (user may change).
8. **Form without Event:** Disable EVENT_END; activation window: treat as "no window" (form always served if published, or use form-only logic).

### Phase 3: Unpublished form page (no 404)
9. **Public resolver:** When FormPublicLink.IsActive=false or Form.Status=UNPUBLISHED, serve dedicated "Form unpublished" page (not 404).
10. **Page content:** Message: "This form is no longer active. It has been unpublished." CTA: "If this form should still be available, you can request the administrator to publish it again."
11. **Re-publish request API:** POST endpoint (e.g. `/api/forms/{formId}/request-republish`) — anonymous or with token. Creates record; triggers in-app notification to all Company Admins for that form's company.
12. **Notification:** "Someone visited an unpublished form and requested it be published. [Form name] is still being advertised. Would you like to publish it?" Link to FormReviewPage or Dashboard. (If in-app notification system exists; else document as manual/queue placeholder.)

### Phase 4: Dashboard + visibility
13. **Event Dashboard:** Published forms show production URL with copy button. Show "Will unpublish on [date]" badge when SCHEDULED or EVENT_END.
14. **FormReviewPage (published):** Show production link + copy; Unpublish button; unpublish mode and date if set.
15. **API:** Return public URL/token when form is published (form detail or dedicated endpoint).

### Phase 5: Activation windows + Hide approval UI
16. **Activation window:** Public resolver checks Event.StartDate–EndDate. When outside window: serve "event ended" (or similar) page instead of form.
17. **Hide approval workflows:** When RequirePublishApproval=false: hide PendingPublishRequestsCard; hide Request Publish flow; show direct Publish for Company Users and Admins. Form Approval Workflow Settings page remains.
18. **Direct publish:** Admin/User can publish directly (no request) when RequirePublishApproval=false; same flow as approve-and-publish; subject to test threshold.

### Phase 6: Auto-unpublish (if in scope)
19. **Background job / cron:** For SCHEDULED and EVENT_END, auto-unpublish when date passes. (Document: may need scheduler; defer if complex; manual reminder for MVP.)

### Phase 7: In-app reminders
20. **Dashboard notice:** "Form [X] will unpublish on [date]" when SCHEDULED or EVENT_END.
21. **Queue items (if available):** 7 days before, 1 day before, when unpublished. Email deferred.

---

## UAT (maximize automation — show evidence for EACH test)

Create `docs/stories/STORY-5.8-UAT-RESULTS.md` with a table:

| Test ID | Description | Command/Action | Result | Evidence |
|---------|-------------|----------------|--------|----------|
| DC1 | Approval options | Manual | — | — |
| DC2 | Public URL on publish | Manual | — | — |
| DC3 | Unpublish modes | Manual | — | — |
| DC4 | Unpublished page + CTA + notification | Manual | — | — |
| DC5 | Dashboard URL + copy; unpublish badge | Manual | — | — |
| DC6 | FormReviewPage published | Manual | — | — |
| DC7 | Direct publish | Manual | — | — |
| DC8 | In-app reminders | Manual | — | — |
| DC9 | Activation windows | Manual | — | — |
| DC10 | Hide approval UI | Manual | — | — |
| Build/lint | Backend + frontend | pytest; npm run lint | PASS/FAIL | (snippet) |

**Cap long output** — use `Select-Object -First 50` or redirect to file.

---

## Workflow lessons (from Epic 5)

- **Cap long output** — pytest, npm run build can crash sessions. Limit output.
- **Implementation commits first** — never leave code uncommitted before closeout.
- **Migrations** — create migration files; human runs `alembic upgrade head`.
- **SM suggestions** — see STORY-5.8-SM-REVIEW-SUGGESTIONS.md; implement where feasible.

---

## Deliverables

1. FormReviewPage: Approve only + Approve & Publish
2. FormPublicLink auto-creation on publish; stable token; FormVersion.IsActive
3. Unpublish modes: Manual, Event end, Schedule; Form.UnpublishMode + ScheduledUnpublishDate
4. Manual unpublish; Unpublished form page (no 404) with re-publish CTA; notification to Company Admins
5. Dashboard: published URL + copy; "Will unpublish on [date]" badge
6. FormReviewPage (published): link + copy; Unpublish button; mode/date
7. Direct publish when RequirePublishApproval=false
8. Activation windows: "event ended" when outside Event.StartDate–EndDate
9. Hide approval UI when RequirePublishApproval=false
10. ref.FormStatus UNPUBLISHED; migration provided
11. `docs/stories/STORY-5.8-UAT-RESULTS.md` with evidence table
12. All implementation committed and pushed; working tree clean

---

## Human handoff

After you complete: I will run the migration (you provide command), run manual UAT per STORY-5.8-UAT-TEST-GUIDE.md, then merge the Story PR to master.
```

---

*Prompt created for Story 5.8 single-session implementation*  
*PM decisions from STORY-5.8-PM-DECISIONS.md*  
*Last Updated: 2026-02-18*
