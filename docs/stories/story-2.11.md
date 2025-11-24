# Story 2.11: Approval Workflow Extensions

Status: **📋 DRAFT** - Ready for Implementation

## Story Scope & Domain Context

**Key Requirements (Based on Epic 2 Status & Domain Analysis):**

1.  **Cost-Based Approval Triggers:**
    *   Implement logic to automatically transition a form to `PENDING_APPROVAL` if its `DeploymentCost` exceeds a configured threshold (e.g., $100).
    *   Allow company-level configuration of this threshold (optional, default to system standard first).

2.  **Workflow State Machine:**
    *   Define clear transitions: `DRAFT` -> `PENDING_APPROVAL` -> `APPROVED` / `REJECTED`.
    *   Ensure `APPROVED` forms can be `PUBLISHED`.
    *   Ensure `REJECTED` forms return to `DRAFT` (or a specific `REJECTED` state allowing edits).

3.  **Notification Logic:**
    *   Trigger email notifications to Company Admins when a form requires approval.
    *   Trigger email notifications to Form Owners when their form is Approved or Rejected.
    *   Leverage existing `EmailService` from Epic 1.

4.  **Approval UI Extensions:**
    *   Add "Submit for Approval" action in Form Detail/Edit views (replacing direct "Publish" for costly forms).
    *   Add "Approve/Reject" actions for Company Admins on the Form Detail view.
    *   Display approval history/comments (using Audit Trail or a new lightweight comment system).

## Story

As a Company Admin,
I want high-cost forms to require my approval before they can be published,
so that I can control deployment costs and ensure quality standards are met before forms go live.

## Context

**Background:**
*   **Story 2.8** established `FormStatus` (`Draft`, `Published`) and `FormApprovalStatus` (`No Approval`, `Pending`, `Approved`) fields.
*   **Story 2.4** established basic Event workflow patterns.
*   **Domain 4 Focus:** This is the first story of the "Approval Workflows" domain, adding logic to the static status fields.

**Technical Foundation:**
*   `Form` table has `FormStatusID`, `FormApprovalStatusID`, and `DeploymentCost`.
*   `EmailService` exists for sending notifications.
*   `UserCompanyRole` permissions (`CanManageForms`) determine who can approve.

## Acceptance Criteria

1.  **AC-2.11.1:** Approval Trigger Logic: Saving a form with `DeploymentCost > Threshold` sets `FormApprovalStatus` to `PENDING` (if currently `NO_APPROVAL`).
2.  **AC-2.11.2:** Submit for Approval Action: User can explicitly "Submit" a form, transitioning it to `PENDING_APPROVAL` state.
3.  **AC-2.11.3:** Admin Approval Action: Company Admins can "Approve" a pending form, transitioning it to `APPROVED`.
4.  **AC-2.11.4:** Admin Rejection Action: Company Admins can "Reject" a pending form, transitioning it to `REJECTED` (with optional comment).
5.  **AC-2.11.5:** Publish Guard: Forms requiring approval cannot be set to `PUBLISHED` status until `FormApprovalStatus` is `APPROVED`.
6.  **AC-2.11.6:** Notification (Request): Company Admins receive an email when a form is submitted for approval.
7.  **AC-2.11.7:** Notification (Decision): Form Owner receives an email when their form is Approved or Rejected.
8.  **AC-2.11.8:** UI Feedback: Form Detail view clearly shows current approval status and blocks restricted actions (e.g., Publish button disabled if pending).
9.  **AC-2.11.9:** Comprehensive UAT tests covering the approval lifecycle.

## Tasks / Subtasks

### **Phase 1: Backend Workflow Logic**
- [ ] **Task 1: Approval Service Layer**
    - [ ] Create `ApprovalService` (or extend `FormService`).
    - [ ] Implement `submit_for_approval(form_id)` method.
    - [ ] Implement `approve_form(form_id, approver_id)` method.
    - [ ] Implement `reject_form(form_id, rejector_id, reason)` method.
    - [ ] Implement cost-check logic (Threshold default: $100).

- [ ] **Task 2: Publish Guard Update**
    - [ ] Update `update_form` (specifically status changes) to check `FormApprovalStatus` before allowing transition to `PUBLISHED`.

- [ ] **Task 3: Notification Integration**
    - [ ] Update `ApprovalService` to call `EmailService`.
    - [ ] Create email templates for "Approval Request" and "Approval Decision".

### **Phase 2: Frontend Approval UI**
- [ ] **Task 4: Approval Status Indicators**
    - [ ] Update `FormStatusBadge` to be more prominent for Pending/Rejected states.
    - [ ] Add banner/alert in `FormDetailView` explaining why Publish is disabled (if applicable).

- [ ] **Task 5: Approval Actions (Owner)**
    - [ ] Add "Submit for Approval" button in `FormDetailView` (visible when Draft + Cost > Threshold).

- [ ] **Task 6: Approval Actions (Admin)**
    - [ ] Add "Review Request" panel for Admins on Pending forms.
    - [ ] Implement Approve/Reject buttons with confirmation modals (Reject requires reason).

### **Phase 3: Integration & Testing**
- [ ] **Task 7: Backend API Endpoints**
    - [ ] `POST /api/forms/{id}/submit`
    - [ ] `POST /api/forms/{id}/approve`
    - [ ] `POST /api/forms/{id}/reject`

- [ ] **Task 8: UAT Scenarios**
    - [ ] **Trigger:** Create costly form -> Verify "Submit" required.
    - [ ] **Flow:** Submit -> Admin Approve -> Owner Publish.
    - [ ] **Rejection:** Submit -> Admin Reject -> Owner Edit -> Resubmit.
    - [ ] **Guard:** Try to Publish pending form via API -> Verify 403/400.

## UAT Test Requirements

### **Category 1: Workflow Triggers**
1.  **Cost Trigger:** Create form with Cost=$0. Verify Publish allowed. Create form with Cost=$500. Verify Publish blocked, "Submit for Approval" shown.
2.  **Explicit Submit:** User clicks "Submit". Verify status changes to `PENDING`.

### **Category 2: Admin Decisions**
3.  **Approve:** Admin approves pending form. Verify status `APPROVED`. Verify Publish now enabled.
4.  **Reject:** Admin rejects pending form. Verify status `REJECTED`. Verify Publish blocked.

### **Category 3: Notifications**
5.  **Admin Alert:** Verify mocked email sent to Admin on submission.
6.  **Owner Alert:** Verify mocked email sent to Owner on decision.

---

*Story 2.11 - Approval Workflow Extensions*
*Status: 📋 DRAFT*

