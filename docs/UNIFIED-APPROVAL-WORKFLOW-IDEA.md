# Unified Form Approval Workflow

**Status:** ✅ Implemented (2026-02-20)  
**Created:** 2026-02-20  
**Source:** User feedback during Story 5.8 UAT  

---

## 1. Prior Gaps (Resolved)

| Gap | Description |
|-----|-------------|
| **Request Publish visibility** | Button appears only for **Company User** (not Admin), in Builder header, Edit Form footer, Form Detail footer. Admins never see it (by design). Form card on Dashboard has no Request Publish. |
| **Form Cost Threshold** | Hardcoded $100 in EditFormModal, FormDetailView, FormDetailView handleSubmitForApproval. Not configurable at company level. |
| **Separate approval flows** | Two distinct flows: (1) **Publish approval** (RequirePublishApproval → Request Publish → FormReviewPage); (2) **High-cost approval** (FormApprovalStatus: NO_APPROVAL, PENDING, APPROVED when cost > 100). These feel like separate workflows. |
| **Form Approval Workflow page** | Has: Enforce demo test requirement, Require publish approval. Missing: Form Cost Threshold. |

---

## 2. Vision: Single Approval Workflow, Multiple Gates

**Proposal:** One unified approval workflow with **multiple entry gates**. When any gate triggers, the form goes through the same flow: Request Publish → Admin reviews on FormReviewPage → Approve only / Approve & Publish.

| Gate | When it triggers | Current behaviour | Desired behaviour |
|------|------------------|-------------------|-------------------|
| **RequirePublishApproval** | Company setting enabled | Request Publish for Company User | Same — gate to approval flow |
| **EnforceDemoTestRequirement** | Test runs < threshold | Blocks publish (readiness) | Same — blocks until met, then flows to approval if other gates apply |
| **FormCostThreshold** | Deployment cost > company threshold | Triggers separate FormApprovalStatus (high-cost) flow | **Unify:** Trigger same Request Publish flow; no separate FormApprovalStatus path |

**Result:** All gates feed into one approval queue. Admin sees one FormReviewPage; one Pending Publish Requests card. No separate "high-cost approval" vs "publish approval" — it's all publish approval.

---

## 3. Implementation Sketch

1. **Add FormCostThreshold to CompanyFormTestConfig**
   - Migration: `FormCostThreshold` (DECIMAL or INT, nullable, default 100)
   - When null: treat as "disabled" (cost never triggers approval)
   - When set: forms with cost > threshold require approval (same flow as RequirePublishApproval)

2. **Form Approval Workflow page**
   - Add "Form cost threshold ($)" — optional; when set, forms exceeding this cost require admin approval before publish
   - Help text: "When set, forms with deployment cost above this value must go through the approval flow before publishing."

3. **Unify logic**
   - "Needs approval" = RequirePublishApproval **OR** (FormCostThreshold set AND form.DeploymentCost > threshold)
   - When Company User and needs approval: show Request Publish (not direct Publish)
   - Deprecate or repurpose FormApprovalStatus for high-cost — route to Request Publish instead

4. **Request Publish discoverability**
   - Add Request Publish link/button on form card (Dashboard) when: Company User + needs approval + form Draft
   - Consider: brief help text for Admins ("Company Users see Request Publish when approval is required")

---

## 4. References

- CompanyFormTestConfig: `backend/models/company_form_test_config.py`
- Form Approval Workflow page: `frontend/src/features/dashboard/pages/FormApprovalWorkflowPage.tsx`
- Hardcoded threshold: `EditFormModal.tsx` (line 45), `FormDetailView.tsx` (lines 118, 247, 278)
- EPIC-5-STATUS.md backlog

---

## 5. Implementation Summary (2026-02-20)

| Change | Location |
|--------|----------|
| **Unified needsApproval** | `needsApproval = RequirePublishApproval OR (FormCostThreshold set AND formCost > threshold)` |
| **Backend createPublishRequest** | `publish_request_router.py` — allows request when needs_approval (either gate) |
| **Backend review-context** | Retroactive FormPublishRequest when form is PENDING_REVIEW with no request + needs_approval |
| **FormDetailView** | uses needsApproval for Request Publish, Direct Publish, PublishWorkflowStatus |
| **EditFormModal** | uses needsApproval for Request Publish / Direct Publish buttons |
| **BuilderPublishAction** | uses needsApproval including deploymentCost from getForm |
| **CompanyContainer** | Form card Request Publish when needsApproval (both gates) |
| **PendingPublishRequestsCard** | Shown when requirePublishApproval OR formCostThreshold set |
| **Approval Status display** | FormDetailView shows "Required (publish approval or cost gate)" when needsApproval |

---

## 6. Full Review: Form Status vs Form Approval Status (UAT Phase 1.2f)

**Status:** ⚠️ Gaps identified — implementation pending  
**Context:** UAT Phase 1.2f failed. After Admin clicks "Approve only", the form still shows "Pending Admin Review" and has no URL. Expected: form shows "Approved" or "Ready to Publish" and Admin can publish later with one click.

### 6.1 Reference Tables (Complete)

#### ref.FormStatus

| FormStatusID | StatusCode | StatusName | StatusDescription | StatusColor | When used |
|--------------|------------|------------|--------------------|-------------|-----------|
| 1 | DRAFT | Draft | Form is being created and edited | #FFA500 | Default for new forms |
| 2 | REVIEW | Under Review | Form submitted for approval | #17A2B8 | Legacy; may overlap with PENDING_REVIEW |
| 3 | PUBLISHED | Published | Form is live and accepting submissions | #28A745 | After publish |
| 4 | PAUSED | Paused | Form is temporarily paused | #FFC107 | Future use |
| 5 | ARCHIVED | Archived | Form has been archived | #6C757D | Future use |
| 6 | DELETED | Deleted | Form has been deleted | #DC3545 | Soft-delete |
| 7 | PENDING_REVIEW | Pending Admin Review | Form requested for publish; awaiting admin review | #17A2B8 | Request Publish flow (approval enabled) |
| 9 | UNPUBLISHED | Unpublished | Form was published; now taken offline | #6C757D | After unpublish |
| — | **APPROVED_FOR_PUBLISH** (proposed) | Approved for Publish | Form approved; Admin can publish with one click | #059669 | After Approve only (approval enabled) |

#### ref.FormApprovalStatus

| FormApprovalStatusID | ApprovalStatusCode | ApprovalStatusName | ApprovalStatusDescription | IsRequiresApproval | When used |
|----------------------|--------------------|--------------------|---------------------------|--------------------|-----------|
| 1 | NO_APPROVAL | No Approval Required | Form does not require approval | 0 | Default when approval disabled |
| 2 | PENDING | Pending Approval | Form is waiting for approval | 1 | Request Publish created |
| 3 | APPROVED | Approved | Form has been approved | 0 | After Admin approves |
| 4 | REJECTED | Rejected | Form has been rejected | 0 | After Admin rejects |
| 5 | CANCELLED | Cancelled | Form approval was cancelled | 0 | If request cancelled |
| 6 | EXPIRED | Expired | Form approval has expired | 0 | If approval window expires |

---

### 6.2 Workflows: Statuses by Context

**Principle:** Only show statuses when the user needs them. Avoid clutter for single-user orgs; expose approval statuses only when approval is enabled.

| Context | Form Statuses to show | Form Approval Statuses to show |
|---------|------------------------|--------------------------------|
| **No approval** (single user, or approval disabled) | DRAFT, PUBLISHED, UNPUBLISHED | — (hide approval badge; stays NO_APPROVAL) |
| **Approval enabled** (Company User) | DRAFT, PENDING_REVIEW, PUBLISHED, UNPUBLISHED | PENDING, APPROVED, REJECTED (when ≠ NO_APPROVAL) |
| **Approval enabled** (Admin) | Same + PENDING_REVIEW for review queue | Same |

#### A. Single User / No Approval (RequirePublishApproval = false, no cost gate)

One user publishes directly. No approval workflow.

| Step | Form Status | Form Approval Status | What user sees |
|------|-------------|----------------------|----------------|
| Create form | DRAFT | NO_APPROVAL | **Draft** |
| Complete test runs, Publish | PUBLISHED | NO_APPROVAL | **Published** |
| Unpublish | UNPUBLISHED | NO_APPROVAL | **Unpublished** |
| Re-publish | PUBLISHED | NO_APPROVAL | **Published** |

**Statuses used:** DRAFT → PUBLISHED → UNPUBLISHED (and back). Approval status stays NO_APPROVAL; approval badges hidden.

---

#### B. Corporation with Form Approval Enabled (RequirePublishApproval = true OR cost gate)

Company User requests publish; Admin approves or rejects.

**Design decisions:**

1. **Create form:** When approval is enabled, set Form Approval Status = **PENDING** from creation. This prevents admins from bypassing the workflow by manually changing Form Status to PUBLISHED — we restrict allowed Form Statuses when Approval Status = PENDING (e.g. only DRAFT, PENDING_REVIEW, APPROVED_FOR_PUBLISH; not PUBLISHED until approved).

2. **Approve only:** Use a distinct Form Status (e.g. **APPROVED_FOR_PUBLISH**) instead of PENDING_REVIEW. Keeping PENDING_REVIEW after approve is misleading — Company User would still see "Pending Admin Review". Suggested names: `APPROVED_FOR_PUBLISH`, `READY_TO_PUBLISH`, or `APPROVED_PENDING_PUBLISH`. Requires new ref.FormStatus row and migration.

| Step | Form Status | Form Approval Status | Company User sees | Admin sees |
|------|-------------|----------------------|-------------------|------------|
| Create form | DRAFT | **PENDING** (when approval enabled) | Draft | Draft |
| Request Publish | PENDING_REVIEW | PENDING | **Pending Admin Review** | Pending Publish Requests |
| Approve only | **APPROVED_FOR_PUBLISH** (new) | APPROVED | **Ready to Publish** / Approved | Ready to publish (can publish) |
| Approve & Publish | PUBLISHED | APPROVED | **Published** | Published |
| Reject | DRAFT | REJECTED | **Rejected** / Draft | — |
| Unpublish | UNPUBLISHED | APPROVED | **Unpublished** | Unpublished |
| Direct publish (Admin, no request) | PUBLISHED | NO_APPROVAL | **Published** | Published |

**Status restriction when Approval Status = PENDING:** Limit admin's allowed Form Status transitions so they cannot set Form Status = PUBLISHED directly. Allowed transitions only via approval flow (Approve only → APPROVED_FOR_PUBLISH; Approve & Publish → PUBLISHED).

**Statuses used:** DRAFT, PENDING_REVIEW, APPROVED_FOR_PUBLISH (new), PUBLISHED, UNPUBLISHED (Form Status) + PENDING, APPROVED, REJECTED (Form Approval Status when approval enabled).

**Optional (future):** CANCELLED, EXPIRED if approval windows or cancellations are implemented.

---

#### C. Statuses not used in current Story 5.6/5.8 flow

| Status | Table | Notes |
|-------|-------|-------|
| REVIEW | FormStatus | Legacy; PENDING_REVIEW used for Request Publish |
| PAUSED | FormStatus | Future: pause live form |
| ARCHIVED | FormStatus | Future: archive form |
| DELETED | FormStatus | Soft-delete; rarely shown in UI |
| CANCELLED | FormApprovalStatus | Future: cancel request before review |
| EXPIRED | FormApprovalStatus | Future: request expires |

---

### 6.3 Two Status Systems (Summary)

| System | Purpose |
|--------|---------|
| **Form Status** | Lifecycle stages: DRAFT → PENDING_REVIEW (if approval) → PUBLISHED → UNPUBLISHED |
| **Form Approval Status** | Approval state when approval required: NO_APPROVAL, PENDING, APPROVED, REJECTED (+ CANCELLED, EXPIRED for future) |

### 6.4 Current Behaviour by Workflow (Implementation)

#### A. Request Publish Flow (Story 5.6 / 5.8 — RequirePublishApproval or cost gate)

| Step | Form Status | Form Approval Status | FormPublishRequest | UI Display |
|------|-------------|----------------------|--------------------|------------|
| Create publish request | PENDING_REVIEW | **unchanged** (NO_APPROVAL) | pending | "Pending Admin Review" |
| Approve only | PENDING_REVIEW | **unchanged** (NO_APPROVAL) | approved | **"Pending Admin Review"** ← bug |
| Approve & Publish | PUBLISHED | **unchanged** | approved | "Published" + URL |
| Reject | DRAFT | **unchanged** | declined | "Draft" |
| Direct publish (Admin) | PUBLISHED | **unchanged** | N/A | "Published" + URL |

**Root cause:** The Request Publish flow never updates `Form.FormApprovalStatusID`. It only updates `FormPublishRequest` and `Form.FormStatusID`.

#### B. High-Cost Approval Flow (Story 2.11 / 2.12 — approval_service)

| Step | Form Status | Form Approval Status |
|------|-------------|----------------------|
| Submit for approval | unchanged | PENDING |
| Approve (internal) | PUBLISHED (optional) | APPROVED |
| Reject (internal) | unchanged | REJECTED |
| External approve via token | PUBLISHED | APPROVED |

This flow correctly updates `FormApprovalStatusID`. It is a separate path from Request Publish.

### 6.5 Frontend Display Logic (Current)

| Component | Logic | Result after "Approve only" |
|-----------|-------|-----------------------------|
| **CompanyContainer** (form card) | Form Status always shown; Approval Status only when ≠ NO_APPROVAL | Shows "Pending Admin Review" (Form Status) — Approval badge hidden |
| **FormStatusBadge** | APPROVED + DRAFT → "Ready to Publish"; else Form Status | Form has PENDING_REVIEW + NO_APPROVAL → shows "Pending Admin Review" |
| **FormReviewPage** | hasApprovedRequest + PENDING_REVIEW → "Ready to publish" | Works for Admin; Company User sees FormDetailView, not FormReviewPage |
| **PublishWorkflowStatus** (Company User) | PENDING_REVIEW → "Pending Admin Review" | No distinction for approved-but-not-published |

### 6.6 Gaps for Phase 1.2f (Approve Only)

| # | Gap | Location | Fix |
|---|-----|----------|-----|
| 1 | **Form.FormApprovalStatusID not set on Approve only** | `publish_request_router.py` ~306 | Set `Form.FormApprovalStatusID = APPROVED` when `do_publish=False` |
| 2 | **Form.FormApprovalStatusID not set on create_publish_request** | `publish_request_router.py` ~149 | When `needs_approval`, set `Form.FormApprovalStatusID = PENDING` |
| 3 | **Form.FormApprovalStatusID not set on reject** | `publish_request_router.py` ~585 | Set `Form.FormApprovalStatusID = REJECTED` |
| 4 | **Form card shows Form Status only** | `CompanyContainer.tsx` ~914 | When Form Status = PENDING_REVIEW and Approval Status = APPROVED → show "Ready to Publish" as primary (or prioritize Approval Status) |
| 5 | **FormStatusBadge: APPROVED + PENDING_REVIEW** | `FormStatusBadge.tsx` ~61 | Extend: APPROVED + (DRAFT or PENDING_REVIEW) → "Ready to Publish" |
| 6 | **PublishWorkflowStatus: approved-but-not-published** | `PublishWorkflowStatus.tsx` | Company User with approved request: show "Approved — Admin will publish when ready" instead of "Pending Admin Review" (needs hasApprovedRequest in FormDetailView) |
| 7 | **publish_form: clear Approval Status after publish** | `publish_service.py` | Optionally set `Form.FormApprovalStatusID = NO_APPROVAL` after successful publish (or leave APPROVED for audit) |

### 6.7 Desired Behaviour When Form Approval Is Enabled

- **Request Publish created** → Form Status = PENDING_REVIEW, Form Approval Status = PENDING  
- **Approve only** → Form Status = PENDING_REVIEW, Form Approval Status = APPROVED → UI: "Ready to Publish"  
- **Approve & Publish** → Form Status = PUBLISHED, Form Approval Status = APPROVED (or cleared) → UI: "Published" + URL  
- **Reject** → Form Status = DRAFT, Form Approval Status = REJECTED → UI: "Rejected" / "Draft"  
- **Direct publish (Admin)** → Form Status = PUBLISHED, Form Approval Status unchanged (NO_APPROVAL) → Admin skips approval when disabled  

### 6.8 When Form Approval Is Disabled

- Admin can publish directly (no Request Publish).
- Form Approval Status can stay NO_APPROVAL.
- Form goes DRAFT → (test threshold) → Published via direct publish.

### 6.9 Recommended Implementation Order

1. **Backend:** Update `Form.FormApprovalStatusID` in Request Publish flow (create, approve only, approve & publish, reject).
2. **Migration:** Add ref.FormStatus `APPROVED_FOR_PUBLISH` for Approve-only step.
3. **Backend:** On Approve only, set Form Status = APPROVED_FOR_PUBLISH (not PENDING_REVIEW).
4. **Backend:** On form create (approval enabled), set Form Approval Status = PENDING; restrict Form Status transitions when PENDING.
5. **Frontend form card:** Show "Ready to Publish" when Form Status = APPROVED_FOR_PUBLISH.
6. **FormDetailView / PublishWorkflowStatus:** Pass `hasApprovedRequest` (or equivalent) so Company User sees correct message.

---

### 6.10 Audit Trail Gaps (Platform Compliance)

**Finding:** The Request Publish flow (`publish_request_router.py`) does **not** log to `audit.ActivityLog`. The user sees `form.created` but not:
- Form Status change to Pending Review
- Publish request approval (step 1.2e)

**Root cause:** `publish_request_router.py` has no `ActivityLog` calls. The high-cost approval flow (`approval_service.py`) uses `_log_activity()` for submit/approve/reject; the Request Publish flow does not.

**Required audit events:**

| Event | Action string | When |
|-------|---------------|------|
| Publish request created | `form.publish_requested` | post_publish_request — Form Status → PENDING_REVIEW, Form Approval → PENDING |
| Publish request approved (only) | `form.publish_request_approved` | approve_publish_request with `publish=false` |
| Publish request approved & published | `form.publish_request_approved`, `form.published` | approve_publish_request with `publish=true` |
| Publish request rejected | `form.publish_request_rejected` | reject_publish_request |
| Direct publish | `form.published` | direct_publish, publish_form |
| Unpublish | `form.unpublished` | unpublish endpoint |

**Fix:** Add `_log_activity()` helper and calls in `publish_request_router.py` (mirror pattern from `approval_service.py`). Include in NewValue: form_id, form_name, request_id (if applicable), old/new status, user email.

**Implemented (2026-02-20):** Audit logging added to `publish_request_router.py` for: `form.publish_requested`, `form.publish_request_approved`, `form.published`, `form.publish_request_rejected`, `form.unpublished`.

### 6.11 Pending Publish Requests: Exclude Deleted/Archived Forms

**Issue:** Deleted forms still appear in Pending Publish Requests.

**Option 1 (implemented):** Filter `get_pending_publish_requests` to exclude forms where `Form.IsDeleted == True` or `Form.FormStatusID` in (ARCHIVED, DELETED).

**Option 2 (backlog):** On Form delete/archive, cascade to related records (FormPublishRequest, etc.). Reusable pattern for Form, Event, Company domains.
