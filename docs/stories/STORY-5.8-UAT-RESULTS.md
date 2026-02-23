# Story 5.8 UAT Results — Admin Review & Publish + Activation

**Story:** 5.8  
**Epic:** 5 - Form Builder Readiness + Review & Publishing  
**Date:** 2026-02-20  
**Status:** UAT PASSED (Phases 0–5)  

---

## UAT Evidence Table

| Test ID | Description | Command/Action | Result | Evidence |
|---------|-------------|----------------|--------|----------|
| DC1 | Approval options (Approve only, Approve & Publish) | Manual | **PASS** | FormReviewPage; two options; approve-only vs approve-and-publish |
| DC2 | Public URL on publish; stable token | Manual | **PASS** | Publish form; open production URL; re-publish; same URL; form fills viewport |
| DC3 | Unpublish modes (Manual, Event end, Schedule) | Manual | **PASS** | DirectPublishModal / FormReviewPage; select mode; EVENT_END disabled when no event |
| DC4 | Unpublished form page; re-publish CTA; notification | Manual | **PASS** | Unpublish; visit URL; "Form unpublished" page; CTA; request-republish API |
| DC5 | Dashboard: published URL + copy; "Will unpublish on" badge | Manual | **PASS** | CompanyContainer; production URL; copy; badge when SCHEDULED/EVENT_END |
| DC6 | FormReviewPage (published): link + copy; Unpublish | Manual | **PASS** | FormReviewPage for published form; link; Unpublish button |
| DC7 | Direct publish when RequirePublishApproval=false | Manual | **PASS** | EditFormModal, FormDetailView, BuilderPublishAction; Publish button; DirectPublishModal |
| DC8 | In-app reminders (Will unpublish on [date]) | Manual | **PASS** | Dashboard notice; "Will unpublish on" badge |
| DC9 | Activation windows (event ended when outside) | Manual | **PASS** | Event outside StartDateTime–EndDateTime; "event ended" page |
| DC10 | Hide approval UI when RequirePublishApproval=false | Manual | **PASS** | PendingPublishRequestsCard hidden; no Request Publish; direct Publish |
| Build/lint | Backend + frontend | pytest; npm run lint | **PASS** | Backend pytest; frontend lint |

---

## Build Verification Commands

**Backend (pytest):**
```powershell
cd backend; python -m pytest -x -q 2>&1 | Select-Object -First 50
```

**Frontend (lint):**
```powershell
cd frontend; npm run lint
```

**Migration (human runs):**
```powershell
cd backend; alembic upgrade head
```
Migration file: `backend/migrations/versions/048_story_58_admin_review_publish_activation.py`

---

## Implementation Summary

### Phase 1: Data Model + Approval Options ✅
- Migration 048: ref.FormStatus UNPUBLISHED; Form.UnpublishMode (MANUAL | EVENT_END | SCHEDULED); Form.ScheduledUnpublishDate; FormRepublishRequest
- FormReviewPage: Approve only, Approve & Publish, Reject; unpublish modes on approve-and-publish
- Publish flow: FormPublicLink PRODUCTION auto-created; FormVersion.IsActive; stable token

### Phase 2: Unpublish ✅
- Unpublish action: FormReviewPage, Dashboard form card
- Unpublish modes UI: DirectPublishModal, FormReviewPage; Manual, Event end (disabled when no event), Schedule
- Default: MANUAL

### Phase 3: Unpublished Form Page ✅
- Public resolver: UNPUBLISHED / EVENT_ENDED → dedicated page (no 404)
- UnpublishedFormPage: message + CTA "Request admin to publish again"
- POST /forms/{token}/request-republish → FormRepublishRequest
- Notification: documented; in-app queue placeholder

### Phase 4: Dashboard + Visibility ✅
- CompanyContainer: production URL + copy; "Will unpublish on [date]" badge; Unpublish button
- FormReviewPage (published): link + copy; Unpublish; mode/date
- API: getFormPublicUrl, getFormReviewContext

### Phase 5: Activation Windows + Hide Approval UI ✅
- Public resolver: Event.StartDateTime–EndDateTime; outside window → "event ended"
- PendingPublishRequestsCard: hidden when RequirePublishApproval=false
- BuilderPublishAction, EditFormModal, FormDetailView: direct Publish when RequirePublishApproval=false or Admin; DirectPublishModal

### Phase 6–7: Auto-unpublish + Reminders ✅
- STORY-5.8-AUTO-UNPUBLISH-NOTE.md: deferred auto-unpublish; MVP manual reminder
- Dashboard notice: "Will unpublish on [date]" badge

---

## UAT Fixes Applied During Testing

| Phase | Issue | Fix |
|-------|-------|-----|
| 1.1g | Request Publish button stayed disabled after completing tests in preview tab | Added `visibilitychange` listener to refetch readiness when returning to Builder/Form Detail |
| 1.2b | Pending Publish Requests not showing after Request Publish | Fixed `scalars().all()` handling in `get_pending_publish_requests` |
| 1.2e | After Approve Only, page showed unpublish/Publish confusingly | Navigate to dashboard after Approve Only instead of staying on review page |
| 1.3 | Production link showed header; form had black borders | Removed header for PRODUCTION; added cover scaling so form fills viewport |
| 1.3 | Form View required full refresh to see updated response count | FormDetailView fetches form on open; refetches on visibilitychange |
| 4 | No way to change unpublish method for published forms | Added Unpublish fields to Edit Form (unpublishMode, scheduledUnpublishDate) |
| — | Dark theme: text not visible in modals and public link input | Theme-aware colors (--color-card-foreground, etc.) in DirectPublishModal, RequestPublishModal, FormReviewPage, EditFormModal, CompanyContainer |
| — | Production link: React hooks error | Moved fullscreen useEffect before early returns |

---

## Human Handoff

1. ~~Run migration: `cd backend; alembic upgrade head`~~ Done
2. ~~Run manual UAT per `docs/stories/STORY-5.8-UAT-TEST-GUIDE.md`~~ All phases passed
3. ~~Update this table with PASS/FAIL and evidence~~ Complete
4. Merge Story PR to master

---

*UAT PASSED — 2026-02-20. All phases (0–5) executed successfully.*
