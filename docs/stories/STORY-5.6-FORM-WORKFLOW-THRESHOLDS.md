# Story 5.6 Follow-on: Form Workflow Thresholds (Company Settings)

**Epic:** Epic 5 - Form Builder Readiness + Review & Publishing  
**Domain:** Company Settings, Form Workflow  
**Status:** Ready for refinement  
**Priority:** High (enables Company Admins to control form governance)  
**Created:** 2026-02-16  
**Follows:** Story 5.6 - Publish Request Workflow  

---

## 📖 User Story

**As a** Company Admin,  
**I want** a Form Workflow Thresholds page under Company Settings where I can configure test requirements, publish approval, and cost thresholds for my company,  
**So that** I can tailor form governance to our business without relying on platform defaults or API calls.

**Context & entry point:**  
- Story 5.6 delivered publish request workflow, but Company Admins have **no UI** to set `RequirePublishApproval`, `TestThresholdEnabled`, or `TestThresholdValue`.  
- Budget/cost threshold is platform-level only (`config.AppSetting`); companies cannot override.  
- The platform is database-driven; `CompanyFormTestConfig` stores per-company values and should be the single source of truth for form workflow settings.

---

## 🧭 Scope Boundary

### In scope

- **Company Settings: Form Workflow Thresholds page**
  - Location: Company Settings (or Team panel when company selected)
  - Company Admin only
  - Section: "Form Workflow Thresholds" (or equivalent)
- **Settings to configure**
  1. **Demo test threshold enabled** (checkbox) — when ON, forms must meet demo test count before publish/request publish
  2. **Demo test runs required** (number, 0–100) — default 3; shown when enabled
  3. **Require publish approval** (checkbox) — when ON, Company Users must request publish; when OFF, they can publish directly
  4. **Approval cost threshold** (optional; new) — per-company override of platform default ($100). Forms with Deployment Cost > threshold require high-cost approval flow. NULL = use platform default
- **Defaults**
  - Display platform defaults on the page (e.g. "Platform default: $100 for cost threshold")
  - When no company config row exists, use defaults; creating/saving creates the row
- **Terminology consistency**
  - Use **"Demo"** consistently for preview/test submissions across the platform (Demo = Preview; same meaning)
  - Audit and align wording in: readiness badge, PublishWorkflowStatus, Form Detail, Builder, any "preview" vs "demo" references

### Out of scope

- Changing how test runs are counted (Story 5.5 logic)
- Changing publish request or high-cost approval backend logic
- Email notifications for publish requests

---

## 🗃️ Data Model

### CompanyFormTestConfig (extend)

| Column | Type | Notes |
|--------|------|-------|
| TestThresholdEnabled | BIT | Existing |
| TestThresholdValue | INT | Existing; 0–100 |
| RequirePublishApproval | BIT | Existing |
| **ApprovalCostThreshold** | DECIMAL(10,2) NULL | **New** — per-company override. NULL = use platform default |

**Migration:** Add `ApprovalCostThreshold` to `CompanyFormTestConfig`. Backend/approval logic: if company has override, use it; else use `forms.approval.default_cost_threshold`.

---

## 🎯 Done Criteria

- [ ] **DC1:** Form Workflow Thresholds page exists under Company Settings; Company Admin can access.
- [ ] **DC2:** Page allows editing: Demo test threshold enabled, Demo test runs required (0–100), Require publish approval. Changes persist via `PUT /api/forms/company-test-config`.
- [ ] **DC3:** Approval cost threshold: add to `CompanyFormTestConfig`; API supports get/set; UI shows field with platform default as placeholder/hint.
- [ ] **DC4:** Backend approval/cost logic uses company override when present; falls back to platform default when NULL.
- [ ] **DC5:** Terminology: "Demo" used consistently for preview/test submissions; no conflicting "Preview" wording in form workflow context.
- [ ] **DC6:** UAT guide executed and marked PASSED.
- [ ] **DC7:** Story PR merged to `master`.

---

## 📐 API (existing + extension)

**Existing**
- `GET /api/forms/company-test-config` — returns `testThresholdEnabled`, `testThresholdValue`, `requirePublishApproval`
- `PUT /api/forms/company-test-config` — updates config; requires company admin

**Extension**
- Add `approvalCostThreshold` (number | null) to request/response
- Backend: read/write `CompanyFormTestConfig.ApprovalCostThreshold`
- Approval service: `get_approval_cost_threshold(company_id)` → company override or platform default

---

## 📐 UI Design Notes

- Form Workflow Thresholds as a subsection of Company Settings
- Clear labels and help text for each setting
- Defaults visible: "If not set, platform default applies (e.g. $100 for cost threshold)"
- Save/Cancel; success/error feedback

---

## 📚 References

- Story 5.5: test threshold, readiness
- Story 5.6: publish request, RequirePublishApproval
- Story 2.11: approval cost threshold (`forms.approval.default_cost_threshold`)
- `backend/models/company_form_test_config.py`
- `backend/modules/forms/readiness_router.py`
- `backend/common/config_service.py` — `get_approval_cost_threshold()`

---

*Story 5.6 Follow-on: Form Workflow Thresholds*  
*Last Updated: 2026-02-16*
