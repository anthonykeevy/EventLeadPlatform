# Story 5.6: Publish Request Workflow

**Epic:** Epic 5 - Form Builder Readiness + Review & Publishing  
**Domain:** Form Builder, Dashboard, Publish Workflow  
**Status:** ⏳ Ready  
**Priority:** High (enables Company User → Admin separation of duties)  
**Created:** 2026-02-16  
**Owner:** Developer Agent  

---

## 📖 User Story

**As a** Company User,  
**I want** to request that a Company Admin publish my form when I cannot publish directly,  
**So that** I can build and test forms while an admin controls publishing and payment.

**As a** Company Admin,  
**I want** to see pending publish requests in a queue with a direct link to review each form,  
**So that** I can efficiently approve or request changes without hunting through forms.

**Context & entry point:**  
- Stories 5.1–5.5 are complete: assets, company defaults, schema, shared resolver parity, preview/production governance, readiness badges.  
- Company Users today have no way to request publish when their role cannot publish directly.  
- Epic Phase B requires: publish request flow (optional per company), admin review queue, deep link to "Review and Publish".

---

## 🧭 Scope Boundary

### In scope (Story 5.6)

- **Company-level publish approval toggle**
  - Optional per company: `RequirePublishApproval` (or equivalent). When enabled: Company Users must request publish; when disabled: Company Users may publish directly (subject to test threshold).
  - Stored in company settings or `CompanyFormTestConfig` (extend) or new `CompanyFormPublishConfig`. Migration if needed.
- **Publish request entity**
  - Table/entity: `FormPublishRequest` (FormID, RequestedBy, RequestedAt, Message, Status: pending/approved/declined/changes_requested). Audit: who, when, optional message.
  - Handle duplicate requests for same form (idempotent or "already pending" response).
- **Request Publish UX (Company User)**
  - Builder: When approval required and user is Company User, CTA shows "Request Publish" (not "Publish").
  - Modal: "Only Company Admins can publish forms." Select admin(s) from company; optional message.
  - API: `POST /api/forms/{form_id}/publish-request` — creates request; validates readiness (test threshold); sets form status to Pending Admin Review.
  - Success: Builder shows "Pending Admin Review"; Event Dashboard badge "Pending Review".
- **Admin review queue**
  - Dashboard: List of pending publish requests (form name, requester, requested date). Can be embedded in Event Dashboard or separate "Review Queue" view.
  - API: `GET /api/forms/publish-requests/pending` — returns pending requests for current user's company (admin-only).
  - Deep link: Each row links to "Review and Publish" entry point (Story 5.7 will implement the review screen; 5.6 provides the link/route).
- **Form status**
  - Add or use `PENDING_REVIEW` (or equivalent) in `ref.FormStatus`; form transitions to this when publish request is created.
- **Role-aware gating**
  - Company Admin: sees Publish (subject to test threshold from 5.5).
  - Company User + approval required: sees Request Publish; modal flow.
  - Company User + approval disabled: sees Publish (subject to test threshold).

### Out of scope (Story 5.6)

- Admin Review & Publish screen (review form, approve/decline/request changes) — Story 5.7.
- Actual publish/unpublish actions from review — Story 5.7.
- Stable public URL/token generation, activation windows — Story 5.7.
- Email notifications for publish requested — optional; in-app queue is MVP.
- Payment/Stripe integration — Epic 6.

---

## 🎯 Done Criteria

- [ ] **DC1:** Company-level `RequirePublishApproval` config; when enabled, Company Users see "Request Publish" instead of "Publish".
- [ ] **DC2:** `FormPublishRequest` table and API: create request; validate readiness before creating; form status → Pending Review.
- [ ] **DC3:** Request Publish modal in Builder: select admin(s), optional message; success shows "Pending Admin Review".
- [ ] **DC4:** Admin Dashboard: pending publish requests queue; each row has deep link to Review and Publish (route/page; review UI in 5.7).
- [ ] **DC5:** Duplicate requests handled (idempotent or clear "already pending" message).
- [ ] **DC6:** UAT guide executed and marked PASSED.
- [ ] **DC7:** Story PR merged to `master`.

---

## 📐 References

- Epic scope: `docs/stories/EPIC-5-STATUS.md` (Phase B: Publish request + review flow)
- PRD: `docs/prd.md` (Create Form & Request Publish — User Flow 3.4)
- UX spec: `docs/ux-specification.md` (User Flow 4)
- Epic UX ideation: `docs/stories/EPIC-5-UX-IDEATION.md` (Journey 1, Journey 2)
- Story 5.5: readiness badges, test threshold, publish block
- Git workflow: `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`

---

*Story 5.6 - Publish Request Workflow*  
*Last Updated: 2026-02-16*
