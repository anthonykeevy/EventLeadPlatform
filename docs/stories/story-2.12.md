# Story 2.12: External Approver Support

Status: **✅ COMPLETE**

## Story Scope & Domain Context

**Key Requirements (Based on Epic 2 Status & Domain Analysis):**

1.  **External Approval Request:**
    *   Allow Form Owners to request approval from an email address outside the organization.
    *   Support for "Client Approval" or "Partner Sign-off" workflows.
    *   **Fraud Prevention:** Prevent self-approval bypass (External Email != Owner Email).

2.  **External User Management (New Requirement):**
    *   **Persist External Approvers:** Store external approvers as "Lightweight Users" (`IsExternal=1`) in the `User` table or a dedicated `ExternalUser` table to retain history.
    *   **Reuse:** If `client@example.com` is used again, link to the existing record.
    *   **Transition Support:** If `client@example.com` later signs up for a full account, merge/link their historical approvals to their new User ID.

3.  **Secure Access Mechanism:**
    *   Generate secure, time-limited access tokens.
    *   No *password* or *platform login* required for external approvers (Token-based access).
    *   Public-facing (but token-protected) "Approval View".

4.  **Clear Communication & Decision Support:**
    *   **Email Content:** Comprehensive context (Name, Event, Cost, Description).
    *   **Rejection Reasoning:** Mandatory text reason.
    *   **Urgency Highlighting:** Highlight urgent requests.
    *   **Admin Transparency:** Notify Admins of all external requests.

5.  **Audit & Security:**
    *   Log actions against the persistent `ExternalUser` record (or placeholder ID).
    *   Audit Flag for external requests.

## Story

As a **Form Owner**,
I want to **send an approval request to an external client**,
so that **I can get official sign-off, and if they later join the platform, their approval history is preserved**.

## Context

**Background:**
*   **Story 2.11** established the internal approval workflow.
*   **Refinement:** User requested persistent history for external approvers to support future onboarding transition.

**Technical Foundation:**
*   `User` table exists.
*   `ApprovalService` exists.

## Acceptance Criteria

1.  **AC-2.12.1:** **External User Persistence:** When an external email is used:
    *   Check if `User` exists with that email.
    *   If YES (Full User): Treat as internal user (if in same company) or external user (if different company).
    *   If NO: Create a "Shadow User" record (e.g., `UserStatus='EXTERNAL'`, `PasswordHash=NULL`).
2.  **AC-2.12.2:** **Reuse:** Subsequent requests to the same email reuse the existing `UserID`.
3.  **AC-2.12.3:** **Transition Logic:** If an External User signs up:
    *   Detect existing `EXTERNAL` record by email.
    *   Update record to `ACTIVE` (or `PENDING_VERIFICATION`).
    *   Set Password and other profile fields.
    *   **Retain** `UserID` so all historical audit logs (Approvals) remain linked.
4.  **AC-2.12.4:** Request Interface: Submit modal allows external email input.
5.  **AC-2.12.5:** Fraud Guard: Block self-approval.
6.  **AC-2.12.6:** Token Logic: Generate token linked to `UserID` (the external/shadow user) and `FormID`.
7.  **AC-2.12.7:** Public Review Page: Access via token.
8.  **AC-2.12.8:** Audit Trail: Log `UserID` correctly (pointing to the Shadow User).

## Tasks / Subtasks

### **Phase 1: Backend Infrastructure**
- [x] **Task 1: User Schema Update**
    *   Add `UserStatus` 'EXTERNAL' (if not exists).
    *   Ensure `PasswordHash` can be nullable (or handle via dummy hash for external).
    *   Migration: `028_add_external_user_support`.
- [x] **Task 2: External User Service**
    *   Implement `get_or_create_external_user(email, first_name, last_name)`.
    *   Implement `convert_external_to_full_user(user_id, password, details)`.
- [x] **Task 3: Approval Service Update**
    *   Update `request_approval` to use `get_or_create_external_user`.
    *   Link `FormApprovalToken` to `UserID`.

### **Phase 2: Public API & UI**
- [x] **Task 4: Public Endpoints**
    *   `GET /api/public/approval/{token}`.
    *   `POST /api/public/approval/{token}/decide`.
- [x] **Task 5: Public UI Page**
    *   `ExternalApprovalPage.tsx` with Urgency/Reject logic.

### **Phase 3: Integration**
- [x] **Task 6: Signup Flow Update**
    *   Update `auth/router.py` `signup` to check for existing 'EXTERNAL' user and "Claim/Upgrade" the account instead of creating new.

### **Phase 4: Testing**
- [x] **Task 7: UAT Scenarios**
    *   External Request -> Creates Shadow User.
    *   Repeat Request -> Reuses Shadow User.
    *   Signup with Shadow Email -> Upgrades User -> Verifies History Retained.

## UAT Test Requirements

### **Test Cases**
1.  **Shadow User Creation:** Submit approval to `new-client@test.com`. Verify new `User` record created with `Status='EXTERNAL'`. (PASSED)
2.  **Approval History:** Approve the request. Verify `ActivityLog` shows `UserID` of the shadow user. (PASSED)
3.  **User Conversion:** Sign up as `new-client@test.com`. Verify account creation succeeds (upgrades existing record). (PASSED)
4.  **History Verification:** Log in as the new user. Check "My Approvals" (if visible) or Audit Log. Verify the previous approval is linked to this account. (PASSED)

## Implementation Summary
- **Architecture:** Adopted "Shadow User" pattern. External users are created as full DB entities with a special 'EXTERNAL' status.
- **Security:** Token-based access via `FormApprovalToken` table (7-day expiry). Fraud checks prevent self-approval.
- **Frontend:** Added `ExternalApprovalPage.tsx` (public route) and `ApprovalRequestModal.tsx` (request UI).
- **Transition:** Signup flow enhanced to detect 'EXTERNAL' status and upgrade account in-place, preserving ID and history.
- **Smart Onboarding:** Implemented logic to auto-join users to companies where they have a prior trusted approval history.

## ✅ Completion Report

**Completion Date:** 2025-11-27
**Status:** Complete
**UAT Status:** 5/5 Scenarios Passed

### APIs Created/Modified
*   `POST /api/forms/{form_id}/request-external-approval`: New endpoint to initiate external approval.
*   `GET /api/public/approval/{token}`: New public endpoint to retrieve form details for approval.
*   `POST /api/public/approval/{token}/decide`: New public endpoint to submit approval/rejection.
*   `POST /api/auth/signup`: Modified to support upgrading 'EXTERNAL' users to 'ACTIVE'.
*   `GET /api/users/me/companies`: Enhanced with robust error handling.
*   `GET /api/users/me/suggested-company`: New endpoint to suggest company during onboarding based on approval history.
*   `POST /api/companies`: Modified to support "Smart Auto-Join" for trusted external approvers.

### Database Changes
*   **New Table:** `FormApprovalToken` (Token, FormID, UserID, Expiry, IsUsed).
*   **Schema Update:** Added `JoinedVia` reference data `approval_trust`.
*   **Migrations:**
    *   `028_external_approval_support.py`
    *   `029_add_approval_trust_joined_via.py`

### Frontend Components
*   `ExternalApprovalPage.tsx`: Public-facing page for external approvers.
*   `ApprovalRequestModal.tsx`: Updated to support external email input.
*   `OnboardingStep2.tsx`: Updated to pre-fill company details from suggestion API.

### Testing Results
*   **Scenario 1 (Busy CFO):** Passed. External user created, token generated, approval successful.
*   **Scenario 2 (Agency Client):** Passed. External domain approval/rejection works.
*   **Scenario 3 (Self-Approval Fraud):** Passed. System blocks self-approval attempts.
*   **Scenario 4 (Upgrade Flow):** Passed. Signup converts EXTERNAL user to ACTIVE, retaining history.
*   **Scenario 5 (Unauthorized Internal User):** Passed. Blocks requests to internal non-admin users.

### Issues Resolved
*   **Circular Dependency:** Resolved `CircularDependencyError` in SQLAlchemy models by reordering imports.
*   **SQL Syntax Error:** Fixed boolean comparison syntax for SQL Server in `event_company_service.py`.
*   **Form Ownership:** Fixed logic where forms created by Participants were incorrectly assigned to Event Owners.
*   **Onboarding Friction:** Resolved "Company Already Exists" hard stop by implementing "Smart Auto-Join".

### Lessons Learned
*   **SQLAlchemy Relationships:** Importance of import order in `__init__.py` to avoid circular dependencies.
*   **SQL Server Compatibility:** Need to be explicit with boolean comparisons (`is_(True)`) for SQL Server dialects.
*   **User Experience:** Onboarding flows for converted users need careful design to avoid friction (e.g., auto-joining existing companies).

### What Could Be Improved
*   **Email Templates:** Enhance HTML email designs for approval requests.
*   **Expiration Handling:** Add UI for resending expired tokens.
