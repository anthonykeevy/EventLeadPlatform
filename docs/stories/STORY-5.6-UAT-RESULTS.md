# Story 5.6 UAT Results — Publish Request Workflow

**Story:** 5.6  
**Epic:** 5 - Form Builder Readiness + Review & Publishing  
**Status:** ✅ UAT PASSED  
**Created:** 2026-02-16  
**UAT Completed:** 2026-02-17  

---

## UAT Summary Table

| Test ID | Description | Command/Action | Result | Evidence |
|---------|-------------|----------------|--------|----------|
| DC1 | RequirePublishApproval config; Company User sees Request Publish | Manual / API | PASS | Config set; Company User sees "Request Publish" and "Publish approval: Required" |
| DC2 | FormPublishRequest created; form status Pending Review | API / DB | PASS | POST creates request; FormPublishRequest row; Form status = PENDING_REVIEW |
| DC3 | Request Publish modal; message; success | Manual | PASS | Modal with optional message; submit → "Pending Admin Review" |
| DC4 | Admin queue visible; deep link works | Manual | PASS | Pending Publish Requests card; Review & Publish → Form Review page |
| DC5 | Duplicate request handled | API / Manual | PASS | Second request idempotent; no duplicate row |
| Phase A | Threshold blocking (Request Publish disabled, Admin blocked) | Manual | PASS | 2/3 tests; button disabled with tooltip; Admin publish blocked |
| Phase B | Full flow: Request → Admin Review → Approve | Manual | PASS | Open in preview → test → Approve & Publish → form published |
| Phase C | Duplicate request idempotent | Manual | PASS | No error; existing request returned |
| Phase D | RequirePublishApproval off → Publish direct | Manual | PASS | Company User sees Publish (not Request Publish) |
| Build/lint | Backend + frontend | pytest; npm run lint | PASS | Pre-UAT verification |

---

## Implementation Delivered

### Backend
- **Migration 042**: RequirePublishApproval on CompanyFormTestConfig; FormPublishRequest table; PENDING_REVIEW in ref.FormStatus
- **API GET/PUT** `/api/forms/company-test-config` — includes `requirePublishApproval`
- **API POST** `/api/forms/{form_id}/publish-request` — create request; validate readiness; set form status to PENDING_REVIEW; idempotent for duplicates
- **API GET** `/api/forms/publish-requests/pending` — admin-only; returns pending requests for company
- **Readiness route order fix:** `/company-test-config` defined before `/{form_id}/...` to avoid 422

### Frontend
- **RequestPublishModal** — message input; calls createPublishRequest
- **FormDetailView** — Request Publish button; PublishWorkflowStatus callout; Approval Status vs Publish approval clarification
- **EditFormModal** — Request Publish in footer when Company User + requirePublishApproval
- **BuilderLayout** — BuilderPublishAction shows Request Publish when applicable; BuilderFormStatusBadge shows actual form status
- **PendingPublishRequestsCard** — admin dashboard; pending requests with deep link to `/forms/{formId}/review`
- **FormReviewPage** — full UI: Open in preview, Approve & Publish, Reject (with optional comment/reason)

### Role Gating
- Company Admin: Publish directly; sees pending queue
- Company User + requirePublishApproval: Request Publish
- Company User + !requirePublishApproval: Publish (subject to test threshold)

---

## Migration Command (Human)

```
cd backend
alembic upgrade head
```

---

## Pre-UAT Checklist

- [x] Run migration: `alembic upgrade head`
- [x] Enable RequirePublishApproval for test company (PUT /api/forms/company-test-config with `requirePublishApproval: true`)
- [x] Ensure at least one Company User and one Company Admin in the company
- [x] Create a form in Draft with readiness met (or test threshold disabled)

---

## Retro & Follow-on

- **Retro:** `docs/stories/STORY-5.6-RETRO.md`
- **Follow-on story:** Form Workflow Thresholds page in Company Settings — `docs/stories/STORY-5.6-FORM-WORKFLOW-THRESHOLDS.md`

---

*Story 5.6 UAT PASSED — 2026-02-17*
