# Retro: Story 5.6 — Publish Request Workflow

**Story:** 5.6 - Publish Request Workflow  
**Date:** 2026-02-16  

---

## What went well

- **Backend API complete:** FormPublishRequest, RequirePublishApproval, publish-request and pending endpoints delivered
- **Request Publish UX:** Modal in Form Detail and Builder; Company User flow clear
- **Admin queue:** PendingPublishRequestsCard with deep link to Review & Publish
- **Idempotent duplicates:** Second request for same form returns existing (no duplicate)
- **Role gating:** Company Admin vs Company User behavior correct; RequirePublishApproval respected

---

## What could improve

- **No Company Admin UI for config:** RequirePublishApproval, TestThresholdEnabled, TestThresholdValue are only settable via `PUT /api/forms/company-test-config`. No UI exists.
- **Cost threshold hardcoded in prompts:** $100 appears in confirm dialogs; should come from config
- **Terminology:** "Demo" vs "Preview" used inconsistently; need platform-wide alignment (Demo = Preview)

---

## Action: Build Form Workflow Thresholds Page (Next Story)

**Routed to next story:** Form Workflow Thresholds (Company Settings)

Company Admins need a rich UI to control form governance. The **Company Settings** area is where we give customers these controls. Add a **Form Workflow Thresholds** page under Company Settings with:

1. **Demo test threshold enabled** — checkbox
2. **Demo test runs required** — number (0–100)
3. **Require publish approval** — checkbox
4. **Approval cost threshold** — per-company override (new column on `CompanyFormTestConfig`; today only platform-level)

All values stored in `CompanyFormTestConfig`; platform is database-driven. Include platform defaults on the page so Admins understand fallback behavior.

See: `docs/stories/STORY-5.6-FORM-WORKFLOW-THRESHOLDS.md`

---

## Final Retrospective (Post-UAT — 2026-02-17)

### UAT Fixes Applied

| Issue | Fix | Outcome |
|-------|-----|---------|
| **422 on GET /api/forms/company-test-config** | Route ordering: register `forms_readiness_router` before `forms_router` in `main.py` so `company-test-config` is not matched as `form_id` | Config API works; Request Publish visibility correct |
| **Request Publish hidden when threshold not met** | Show button disabled with tooltip (e.g. "1 more test run(s) needed") instead of hiding | User understands why they cannot request; UX aligned with "blocked until ready" |
| **"Record test run" vs "Open in preview"** | For Manage users, link opens preview in new tab so user can submit real test; Edit-only users keep one-click "Record test run" | Readiness count increases correctly; threshold can be met |
| **Form Review page placeholder** | Replaced "Open in Builder" with full UI: "Open in preview" (preview link), "Approve & Publish", "Reject" (with optional comment/reason) | Admin can review and approve/reject in one place |
| **Approval terminology confusion** | Clarified: "Approval Status" (high-cost) vs "Publish approval" (RequirePublishApproval); documented in UAT guide | Less confusion during manual testing |

### Delivery

- **Backend:** `POST /api/forms/{formId}/publish-request/approve` and `/reject` endpoints added
- **Frontend:** FormReviewPage fully implemented — preview link, approve/reject actions, optional comments
- **UAT:** All phases (A–D) passed; DC1–DC5 verified

### Lessons for future

- **Route ordering matters:** When adding new top-level paths under a parametric route (e.g. `/forms/company-test-config` vs `/forms/{form_id}`), register the specific router first
- **UX expectations:** "Record test run" (one-click) vs "Open in preview" (real test) — align behaviour with what users expect for "increasing test count"
- When adding company-level config, plan Company Settings UI in same or follow-on story so Admins can use it
- Terminology (Demo vs Preview) should be agreed and applied consistently before UI copy is finalised

---

*Story 5.6 Retro — 2026-02-16; Final retro 2026-02-17*
