# Story 5.8: Admin Review & Publish + Activation

**Epic:** Epic 5 - Form Builder Readiness + Review & Publishing  
**Domain:** Form Builder, Dashboard, Publish Workflow, Public Runtime  
**Status:** In Progress 
**Priority:** High (completes publish lifecycle; stable URLs)  
**Created:** 2026-02-18  
**Owner:** Developer Agent  
**Prerequisite:** Story 5.6 (Publish Request Workflow) complete  
**PM Decisions:** `docs/stories/STORY-5.8-PM-DECISIONS.md`  
**Context:** `docs/stories/story-context-5.8.xml`  
**UAT Guide:** `docs/stories/STORY-5.8-UAT-TEST-GUIDE.md`  

---

## 📖 User Story

**As a** Company Admin,  
**I want** to publish and unpublish forms with stable public URLs, and see those links on the dashboard,  
**So that** I can reliably share forms with customers and take them offline when needed.

**As a** Company Admin,  
**I want** to optionally control when a form is active (e.g. event date range),  
**So that** forms can go live or show "event ended" based on event timing.

---

## Context & Entry Point

- Story 5.6 delivered: publish request flow, FormReviewPage (approve/reject), admin queue, deep link to review.
- On approve: form is set to PUBLISHED, FormPublishRequest marked approved.
- **Gap:** Approve does not create a stable public URL (FormPublicLink). Public resolver requires FormPublicLink + FormVersion.IsActive. Today, links are created manually via public-links API.
- **Gap:** No unpublish action — reject returns form to Draft; no way to take a published form offline.
- **Gap:** Dashboard does not show copy-link for published forms.
- FormPublicLink, FormVersion.IsActive, and public resolver exist (Story 3.8). ref.FormStatus has DRAFT, PENDING_REVIEW, PUBLISHED. UNPUBLISHED status may need adding.

---

## 🧭 Scope Boundary

### In scope (Story 5.8)

- **Approval options (FormReviewPage)**
  - **Approve only:** Approve the publish request without publishing. Form stays in "Ready to publish" state; Admin can publish later with one click.
  - **Approve and publish:** Approve and publish immediately (current behaviour). Creates FormPublicLink, sets FormVersion.IsActive.
- **Stable public URL on publish**
  - When admin approves-and-publishes (or publishes directly): auto-create FormPublicLink (LinkType=PRODUCTION) if none exists; ensure FormVersion.IsActive is set for the published version.
  - Token is stable (persists; not regenerated on re-publish). One PRODUCTION link per form.
- **Unpublish modes (three options)**
  - **Manually:** Form stays published until Company Admin manually unpublishes. No auto-unpublish.
  - **Event end date:** Form auto-unpublishes when the event ends. Use Event.EndDate; show that date in UI.
  - **Schedule:** Date picker — Admin sets a specific unpublish date. Form auto-unpublishes on that date.
  - Add Form.UnpublishMode (MANUAL | EVENT_END | SCHEDULED) and Form.ScheduledUnpublishDate (nullable).
- **Unpublish action**
  - Admin can manually unpublish: form status → UNPUBLISHED; deactivate FormPublicLink (IsActive=false).
- **Unpublished form — public URL (no 404)**
  - When a visitor opens a production URL for an unpublished form: serve a dedicated **"Form unpublished"** page (not 404). Message: form is no longer active. CTA: "If this form should still be available, request the administrator to publish it again." On click → in-app notification to all Company Admins: "Someone visited an unpublished form and requested it be published. [Form name] is still being advertised. Publish again?" Admins can act from notification or Dashboard.
  - Add ref.FormStatus UNPUBLISHED if not present (migration).
  - Unpublish action available from: FormReviewPage (when form is published), Event Dashboard form card, and/or form detail.
- **Unpublish reminders (in-app only for MVP)**
  - Dashboard: Show notice when form has scheduled/event-end unpublish: "Form [X] will unpublish on [date]".
  - In-app queue (if available): Items 7 days before, 1 day before, and when unpublished. Email reminders deferred to Communication/preference-center workstream.
- **Published link visibility**
  - Event Dashboard: for published forms, show production URL with copy button.
  - FormReviewPage (when reviewing published form): show production link + copy.
  - API: return public URL/token when form is published (e.g. in form detail response or dedicated endpoint).
- **Activation windows**
  - Event-based: form is "active" when event is within activation window (Event.StartDate–EndDate).
  - Public resolver: when form/event is outside window, return "event ended" or similar message instead of form.
  - Config: link Form to Event (or use existing relationship); use Event dates for window.
- **Hide approval workflows when company does not need them**
  - When `RequirePublishApproval` is false (CompanyFormTestConfig): hide publish-request UI — PendingPublishRequestsCard, Request Publish flow, links to FormReviewPage/review queue. Company Users and Admins publish directly (subject to test threshold). Form Approval Workflow page in Company Settings remains (it's where the setting is configured).
- **Direct publish (admin, no request)**
  - Company Admin can publish directly from builder/dashboard when no approval workflow (subject to test threshold). Ensure same flow: create FormPublicLink, set FormVersion.IsActive.

### Out of scope (Story 5.8)

- Email notifications for publish/unpublish/unpublish reminders — deferred to Communication/preference-center workstream. In-app only for MVP (research: 73% unsubscribe due to notification fatigue; preference center best practice).
- Multiple production links per form — one stable link per form.
- Custom expiry on production links — production links do not expire by default; activation windows are event-based.
- Payment/Stripe gate before publish — Epic 6.

---

## 🎯 Done Criteria

- [ ] **DC1:** FormReviewPage: two approval options — "Approve only" (approve request, don't publish) and "Approve & Publish" (approve + publish immediately).
- [ ] **DC2:** On approve-and-publish (and direct publish): auto-create FormPublicLink PRODUCTION if none; ensure FormVersion.IsActive. Public URL works.
- [ ] **DC3:** Unpublish modes: Manual, Event end date, Schedule (date picker). Form.UnpublishMode + ScheduledUnpublishDate; EVENT_END derives from Event.EndDate.
- [ ] **DC4:** Manual unpublish: form → UNPUBLISHED; deactivate link. Public URL for unpublished form: dedicated page (no 404) with message + "Request admin to publish again" CTA; CTA sends in-app notification to all Company Admins.
- [ ] **DC5:** Event Dashboard: published forms show production URL with copy button; show "Will unpublish on [date]" when scheduled/event-end.
- [ ] **DC6:** FormReviewPage: when form is published, show production link + copy; show Unpublish button; show unpublish mode and date if set.
- [ ] **DC7:** Direct publish (admin, no request) uses same publish flow as approve-and-publish.
- [ ] **DC8:** In-app reminders for scheduled unpublish (Dashboard notice; queue items if available). Email deferred.
- [ ] **DC9:** Activation windows: event-based active/inactive; public resolver shows "event ended" when outside window. Use Event.StartDate–EndDate for window.
- [ ] **DC10:** When RequirePublishApproval=false: hide PendingPublishRequestsCard, Request Publish flow, and review-queue links; all users publish directly.
- [ ] **DC11:** UAT guide executed and marked PASSED.
- [ ] **DC12:** Story PR merged to `master`.

---

## 📐 Data Model Notes

- **ref.FormStatus:** Add UNPUBLISHED if not present. Statuses: DRAFT, PENDING_REVIEW, PUBLISHED, UNPUBLISHED.
- **Form:** Add UnpublishMode (MANUAL | EVENT_END | SCHEDULED), ScheduledUnpublishDate (nullable). EVENT_END derives from Event.EndDate.
- **FormPublicLink:** One PRODUCTION link per form; create on first publish; deactivate (IsActive=false) on unpublish. Public resolver serves "Form unpublished" page (not 404) when link is deactivated; CTA triggers re-publish request notification to Company Admins.
- **FormVersion.IsActive:** Set when publishing; clear previous active when publishing new version.
- **FormPublishRequest:** "Approve only" keeps request approved; form needs "Ready to publish" state or equivalent so Admin can publish later without re-request.
- **Form–Event:** Use existing relationship for EVENT_END unpublish mode and activation window.

---

## 📚 References

- **PM decisions:** `docs/stories/STORY-5.8-PM-DECISIONS.md`
- **Context:** `docs/stories/story-context-5.8.xml`
- **UAT guide:** `docs/stories/STORY-5.8-UAT-TEST-GUIDE.md`
- **SM review:** `docs/stories/STORY-5.8-SM-REVIEW-SUGGESTIONS.md` — incorporate suggestions before Dev prompt
- Epic scope: `docs/stories/EPIC-5-STATUS.md`
- Story 5.6: `docs/stories/story-5.6.md` (publish request, FormReviewPage, approve/reject)
- UX ideation: `docs/stories/EPIC-5-UX-IDEATION.md` (Journey 1, Journey 2; published link visibility)
- Public resolver: `backend/modules/forms/public_form_router.py`, `public_links_router.py`
- Form model: `backend/models/form.py`, `form_public_link.py`, `form_version.py`

---

*Story 5.8 - Admin Review & Publish + Activation*  
*Last Updated: 2026-02-18*
