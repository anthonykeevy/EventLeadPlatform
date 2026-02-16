# Story 5.6 UAT Results — Publish Request Workflow

**Story:** 5.6  
**Epic:** 5 - Form Builder Readiness + Review & Publishing  
**Status:** Implementation complete; human verification required  
**Created:** 2026-02-16  

---

## UAT Summary Table

| Test ID | Description | Command/Action | Result | Evidence |
|---------|-------------|----------------|--------|----------|
| DC1 | RequirePublishApproval config; Company User sees Request Publish | Manual / API | Human verification required | Enable via PUT /api/forms/company-test-config; login as Company User |
| DC2 | FormPublishRequest created; form status Pending Review | API / DB | Human verification required | POST /api/forms/{id}/publish-request; check FormPublishRequest + Form.FormStatusID |
| DC3 | Request Publish modal; select admin, message; success | Manual | Human verification required | Builder or Form Detail → Request Publish → modal → submit |
| DC4 | Admin queue visible; deep link works | Manual | Human verification required | Dashboard → Pending Publish Requests card → Review & Publish |
| DC5 | Duplicate request handled | API / Manual | Human verification required | Second POST for same form returns existing (idempotent) |
| Build/lint | Backend + frontend | pytest; npm run lint | Partial | See notes below |

---

## Implementation Delivered

### Backend
- **Migration 042**: RequirePublishApproval column on CompanyFormTestConfig; FormPublishRequest table; PENDING_REVIEW in ref.FormStatus
- **API GET/PUT** `/api/forms/company-test-config` — includes `requirePublishApproval`
- **API POST** `/api/forms/{form_id}/publish-request` — create request; validate readiness; set form status to PENDING_REVIEW; idempotent for duplicates
- **API GET** `/api/forms/publish-requests/pending` — admin-only; returns pending requests for company

### Frontend
- **RequestPublishModal** — message input; calls createPublishRequest
- **FormDetailView** — Request Publish button when Company User + requirePublishApproval + readiness met
- **BuilderLayout** — headerAction slot; **BuilderPublishAction** shows Request Publish when applicable
- **PendingPublishRequestsCard** — admin dashboard; pending requests with deep link to `/forms/{formId}/review`
- **FormReviewPage** — placeholder for Review & Publish (full UI in Story 5.7)

### Role Gating
- Company Admin: Publish directly (existing flow); sees pending queue
- Company User + requirePublishApproval: Request Publish (modal)
- Company User + !requirePublishApproval: Publish (subject to test threshold)

---

## Migration Command (Human)

```
cd backend
alembic upgrade head
```

---

## Pre-UAT Checklist

- [ ] Run migration: `alembic upgrade head`
- [ ] Enable RequirePublishApproval for test company (PUT /api/forms/company-test-config)
- [ ] Ensure at least one Company User and one Company Admin in the company
- [ ] Create a form in Draft with readiness met (or threshold disabled)

---

*Story 5.6 implementation complete; UAT to be executed by human.*
