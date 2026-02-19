# Story 5.8 UAT Test Guide — Admin Review & Publish + Activation

**Story:** 5.8  
**Epic:** 5 - Form Builder Readiness + Review & Publishing  
**Status:** Skeleton — expand per implementation  
**Created:** 2026-02-18  
**PM Decisions:** `docs/stories/STORY-5.8-PM-DECISIONS.md`  

---

## Scope (UAT Coverage)

Story 5.8 UAT verifies:

1. **DC1:** FormReviewPage — Approve only and Approve & Publish options
2. **DC2:** Stable public URL on publish (FormPublicLink, FormVersion.IsActive)
3. **DC3:** Unpublish modes (Manual, Event end date, Schedule)
4. **DC4:** Manual unpublish — form UNPUBLISHED; public URL returns 404/unavailable
5. **DC5:** Dashboard — published URL + copy; "Will unpublish on [date]" badge
6. **DC6:** FormReviewPage (published) — link + copy; Unpublish button; mode/date
7. **DC7:** Direct publish (admin, no request) uses same flow
8. **DC8:** In-app reminders for scheduled unpublish
9. **DC9:** Activation windows — "event ended" when outside window
10. **DC10:** When RequirePublishApproval=false — hide approval UI; direct publish

---

## Pre-conditions

- Stories 5.6, 5.7 complete
- Backend running; Form, FormVersion, FormPublicLink, FormPublishRequest, Event APIs
- ref.FormStatus includes UNPUBLISHED
- Test company with Company Admin and Company User
- Company has RequirePublishApproval=true (for DC1–DC9); DC10 uses RequirePublishApproval=false
- Form linked to Event (for EVENT_END unpublish and activation window)

---

## UAT Steps

### DC1: Approval Options (FormReviewPage)

| Step | Action | Expected |
|------|--------|----------|
| 1.1 | As Company User, request publish on a Draft form | Form → PENDING_REVIEW |
| 1.2 | As Company Admin, open FormReviewPage (pending request) | Two options visible: "Approve only" and "Approve & Publish" |
| 1.3 | Click "Approve only" | Request approved; form stays in Ready-to-publish state; FormPublicLink NOT created yet |
| 1.4 | As Admin, publish the approved form (one click) | Form → PUBLISHED; FormPublicLink created |
| 1.5 | (New request) Click "Approve & Publish" | Request approved; form published immediately; FormPublicLink created |

---

### DC2: Stable Public URL on Publish

| Step | Action | Expected |
|------|--------|----------|
| 2.1 | Publish a form (approve-and-publish or direct publish) | FormPublicLink PRODUCTION created |
| 2.2 | Open production URL in new tab | Form loads (public render) |
| 2.3 | Re-publish same form (e.g. new version) | Same token/URL; no regeneration |
| 2.4 | Submit a response via public URL | Submission recorded |

---

### DC3: Unpublish Modes

| Step | Action | Expected |
|------|--------|----------|
| 3.1 | On publish flow, select unpublish mode: Manual | No additional fields; form stays published until manual unpublish |
| 3.2 | Select Event end date | Event.EndDate shown (read-only or link to edit); form auto-unpublishes at event end |
| 3.3 | Select Schedule | Date picker shown; set unpublish date; form auto-unpublishes on that date |
| 3.4 | Save publish with each mode | Mode persisted; correct behaviour for each |

---

### DC4: Manual Unpublish + Unpublished Form Page

| Step | Action | Expected |
|------|--------|----------|
| 4.1 | Have a published form | Public URL works |
| 4.2 | As Admin, click Unpublish (FormReviewPage or Dashboard) | Form → UNPUBLISHED; FormPublicLink.IsActive=false |
| 4.3 | Open same production URL (as visitor) | Dedicated "Form unpublished" page (no 404); message that form is no longer active |
| 4.4 | Verify "Request admin to publish again" CTA on page | CTA visible |
| 4.5 | Click CTA (as visitor) | In-app notification sent to all Company Admins: form still being advertised; option to publish |
| 4.6 | As Company Admin, check notification | Notification received; can act to publish or dismiss |
| 4.7 | Re-publish form | Public URL works again; same token |

---

### DC5: Dashboard — Published Link & Unpublish Notice

| Step | Action | Expected |
|------|--------|----------|
| 5.1 | View Event Dashboard with published form | Production URL visible with copy button |
| 5.2 | Click copy | URL copied to clipboard |
| 5.3 | Form with EVENT_END or SCHEDULED unpublish | Badge/notice: "Form [X] will unpublish on [date]" |
| 5.4 | Form with MANUAL unpublish | No unpublish-date notice |

---

### DC6: FormReviewPage — Published Form

| Step | Action | Expected |
|------|--------|----------|
| 6.1 | Open FormReviewPage for a published form | Production link visible with copy |
| 6.2 | Unpublish mode and date (if set) | Displayed |
| 6.3 | Unpublish button | Visible; click unpublishes |

---

### DC7: Direct Publish (No Approval Workflow)

| Step | Action | Expected |
|------|--------|----------|
| 7.1 | Set RequirePublishApproval=false in Company Settings | Saved |
| 7.2 | As Company Admin, publish Draft form directly (builder or dashboard) | Same flow as approve-and-publish; FormPublicLink created |
| 7.3 | As Company User, publish Draft form directly | Same flow (subject to test threshold) |
| 7.4 | No "Request Publish" flow | Direct Publish only |

---

### DC8: In-App Reminders (Scheduled Unpublish)

| Step | Action | Expected |
|------|--------|----------|
| 8.1 | Form with SCHEDULED or EVENT_END unpublish | Dashboard shows "Will unpublish on [date]" |
| 8.2 | (If in-app queue exists) Verify queue items | 7 days before, 1 day before, when unpublished — or note N/A |

---

### DC9: Activation Windows

| Step | Action | Expected |
|------|--------|----------|
| 9.1 | Form linked to Event; Event.StartDate–EndDate in future | Public URL serves form |
| 9.2 | Edit Event so EndDate is in the past (event ended) | Public URL returns "event ended" or similar (no form) |
| 9.3 | Edit Event so StartDate is in the future (event not started) | Public URL returns "event ended" or "not yet active" |
| 9.4 | Event within window again | Form served |

---

### DC10: Hide Approval Workflows When Not Needed

| Step | Action | Expected |
|------|--------|----------|
| 10.1 | Set RequirePublishApproval=false in Company Settings | Saved |
| 10.2 | As Company Admin, view Dashboard | PendingPublishRequestsCard NOT visible |
| 10.3 | As Company User, view form in Draft | No "Request Publish" — direct "Publish" only |
| 10.4 | Navigate to FormReviewPage URL directly (if applicable) | Redirect or "not applicable" — no queue to show |
| 10.5 | Form Approval Workflow page in Company Settings | Still visible; setting can be changed |

---

## Pass Criteria

- [ ] All DC1–DC10 manual checks pass
- [ ] Approve only vs Approve & Publish both work; form state correct
- [ ] Public URL stable across re-publish; unpublished page (no 404) with re-publish CTA; notification to Admins
- [ ] Unpublish modes: Manual, Event end, Schedule — all behave correctly
- [ ] Activation window: form served when in window; "event ended" when outside
- [ ] RequirePublishApproval=false: PendingPublishRequestsCard, Request Publish hidden; direct Publish works

---

## References

- Story: `docs/stories/story-5.8.md`
- PM decisions: `docs/stories/STORY-5.8-PM-DECISIONS.md`
- Story 5.6: `docs/stories/story-5.6.md`
- Public resolver: `backend/modules/forms/public_form_router.py`

---

*Refine during implementation. UAT results feed into final PASS/FAIL.*
