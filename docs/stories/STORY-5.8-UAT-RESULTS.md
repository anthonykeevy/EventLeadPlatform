# Story 5.8 UAT Results — Admin Review & Publish + Activation

**Story:** 5.8  
**Epic:** 5 - Form Builder Readiness + Review & Publishing  
**Date:** 2026-02-20  
**Status:** Ready for human UAT  

---

## UAT Evidence Table

| Test ID | Description | Command/Action | Result | Evidence |
|---------|-------------|----------------|--------|----------|
| DC1 | Approval options (Approve only, Approve & Publish) | Manual | Pending | Human: FormReviewPage; two options; approve-only vs approve-and-publish |
| DC2 | Public URL on publish; stable token | Manual | Pending | Human: Publish form; open production URL; re-publish; same URL |
| DC3 | Unpublish modes (Manual, Event end, Schedule) | Manual | Pending | Human: DirectPublishModal / FormReviewPage; select mode; EVENT_END disabled when no event |
| DC4 | Unpublished form page; re-publish CTA; notification | Manual | Pending | Human: Unpublish; visit URL; "Form unpublished" page; CTA; request-republish API |
| DC5 | Dashboard: published URL + copy; "Will unpublish on" badge | Manual | Pending | Human: CompanyContainer; production URL; copy; badge when SCHEDULED/EVENT_END |
| DC6 | FormReviewPage (published): link + copy; Unpublish | Manual | Pending | Human: FormReviewPage for published form; link; Unpublish button |
| DC7 | Direct publish when RequirePublishApproval=false | Manual | Pending | Human: EditFormModal, FormDetailView, BuilderPublishAction; Publish button; DirectPublishModal |
| DC8 | In-app reminders (Will unpublish on [date]) | Manual | Pending | Human: Dashboard notice; queue items if available |
| DC9 | Activation windows (event ended when outside) | Manual | Pending | Human: Event outside StartDateTime–EndDateTime; "event ended" page |
| DC10 | Hide approval UI when RequirePublishApproval=false | Manual | Pending | Human: PendingPublishRequestsCard hidden; no Request Publish; direct Publish |
| Build/lint | Backend + frontend | pytest; npm run lint | Pending | Human: Run `cd backend; python -m pytest` and `cd frontend; npm run lint` |

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

## Human Handoff

1. Run migration: `cd backend; alembic upgrade head`
2. Run manual UAT per `docs/stories/STORY-5.8-UAT-TEST-GUIDE.md`
3. Update this table with PASS/FAIL and evidence
4. Merge Story PR to master

---

*UAT results — human verification required. Implementation complete 2026-02-20.*
