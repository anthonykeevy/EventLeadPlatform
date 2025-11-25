# Story 2.11: Approval Workflow Extensions

Status: **COMPLETE**

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

## Completion Report

### 1. Implementation Summary
Story 2.11 successfully implemented a cost-based approval workflow for form publishing. The system now automatically intercepts publishing attempts for high-cost forms (>$100), requiring approval from Company Admins. Key features include a robust state machine, automated email notifications, and role-based UI actions.

### 2. APIs Created/Modified
- **New Endpoints:**
    - `POST /api/forms/{id}/submit`: Triggers the approval workflow.
    - `POST /api/forms/{id}/approve`: Admin action to approve (with auto-publish logic).
    - `POST /api/forms/{id}/reject`: Admin action to reject (with reason).
- **Modified Endpoints:**
    - `PUT /api/forms/{id}`: Updated to include a "Publish Guard" that prevents direct status changes to `PUBLISHED` if requirements aren't met.

### 3. Database Changes
- **Configuration:** Added default cost threshold setting (`forms.approval.default_cost_threshold`).
- **Schema:** No new tables, but enhanced usage of `FormApprovalStatus` and `ActivityLog` for tracking workflow events.

### 4. Frontend Components
- **FormDetailView:** Implemented "Smart Publish" button logic, Admin decision buttons (Approve/Reject/Pre-Approve), and role-based visibility.
- **EditFormModal:** Added "Admin Bypass" for direct publishing and blocked "Published" option for standard users if cost is high.
- **FormStatusBadge:** Unified display logic to show the most relevant status (e.g., hiding "Draft" if "Pending Approval" is active).

### 5. Testing Results
- **UAT Status:** ✅ **Passed (6/6 Scenarios)**
    - Scenario 1: Low Cost Flow (Auto-Publish) - PASS
    - Scenario 2: High Cost Flow (Interception & Request) - PASS
    - Scenario 3: Governance Flow (Admin Approval) - PASS
    - Scenario 4: Proactive Flow (Pre-Approval & Admin Bypass) - PASS
    - Scenario 5: System Admin Override - PASS
    - Scenario 6: Restricted Flow (Viewer Access) - PASS

### 6. Issues Resolved
- **Middleware Crash:** Fixed a critical stability issue where `JWTAuthMiddleware` was raising exceptions instead of returning JSON responses, causing the backend worker to crash on auth failures.
- **Email Notifications:** Corrected role code lookup (`admin` vs `company_admin`) ensuring notifications reach the right users.
- **Self-Spam:** Suppressed "Form Approved" email notifications when the approver is also the form owner.

### 7. Lessons Learned
- **Smart Defaults:** Merging "Submit" and "Publish" into a single "Smart Publish" action significantly reduced user confusion compared to separate buttons.
- **Role Context:** "Admin as Creator" is a unique persona that requires specific "Bypass" logic to avoid friction in testing/demo creation.
- **Middleware Stability:** Always return `JSONResponse` in ASGI middleware; never raise `HTTPException` directly to ensure server stability.

### 8. What Could Be Improved
- **Configurable Thresholds:** Currently, the threshold is a system-wide default ($100). Moving this to a Company Setting would allow per-tenant customization.
- **Email Customization:** Emails use a hardcoded template. Implementing a template editor would allow companies to brand their approval emails.
- **Audit Trail Visibility:** While logged in the database, the approval history (who approved when) is only partially visible in the UI. A dedicated "Approval History" tab would improve transparency.

---

*Story 2.11 - Approval Workflow Extensions*
*Status: ✅ COMPLETE*
