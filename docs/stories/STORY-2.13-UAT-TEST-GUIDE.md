# Story 2.13: Audit Trail & Compliance - UAT Test Guide

## Prerequisites

1. Backend server running: `cd backend && python -m uvicorn main:app --reload`
2. Frontend server running: `cd frontend && npm run dev`
3. Logged in as Company Admin or System Admin

## Test Case 1: Full Lifecycle Audit

**Objective:** Verify complete audit trail for form lifecycle

### Steps:
1. Log in as a Company Admin
2. Create a new Form with cost > $100
3. Edit the Form (change description)
4. Submit for approval (or request external approval)
5. Approve the form
6. Navigate to Form Detail View
7. Click "View Compliance Report" button

### Expected Results:
- ✅ Compliance Report opens in modal
- ✅ "Overview" tab shows form metadata (creator, dates, status)
- ✅ "Timeline" tab shows all 5 actions in chronological order:
  - Form Created
  - Form Updated
  - Submitted for Approval
  - Approved
  - Form Published
- ✅ Each entry shows correct user attribution

---

## Test Case 2: External Approval Traceability (AC-2.13.2)

**Objective:** Verify external approver email and token ID in audit logs

### Steps:
1. Create a Form with cost > $100
2. Request external approval (enter external email)
3. Complete approval via external link (or verify via backend)
4. View Compliance Report for the form

### Expected Results:
- ✅ "Approvals" tab shows:
  - External Approver badge
  - External email address visible
  - Token ID visible (e.g., "Token #123")
  - Decision (Approved/Rejected)
  - Decision timestamp
- ✅ "Timeline" shows "Approved (External)" with external email

---

## Test Case 3: Access Control Audit

**Objective:** Verify access grant/revoke actions are logged

### Steps:
1. Open a Form
2. Click "Manage Access"
3. Grant access to a new user (VIEW or EDIT)
4. View Compliance Report
5. Revoke access from the user
6. Refresh Compliance Report

### Expected Results:
- ✅ "Access" tab shows current access list
- ✅ "Timeline" shows:
  - "Access Granted" entry with user email
  - "Access Revoked" entry with user email

---

## Test Case 4: Activity Log Dashboard (AC-2.13.4)

**Objective:** Verify Admin Dashboard Activity Log tab

### Steps:
1. Log in as Company Admin
2. Navigate to Admin Dashboard
3. Click "Activity Log" tab
4. Use filters (Entity Type, Action)
5. Navigate through pages

### Expected Results:
- ✅ Activity Log table displays
- ✅ Filters work (Form, Event, etc.)
- ✅ Pagination controls work
- ✅ External actions show "External" badge
- ✅ Token IDs shown where applicable

---

## Test Case 5: Security Check (AC-2.13.5)

**Objective:** Verify RBAC enforcement on audit endpoints

### Steps:
1. Log in as a regular user (company_user role)
2. Try to access: `GET /api/audit/form/{form_id}`
3. Try to access: `GET /api/audit/company/activity`

### Expected Results:
- ✅ 403 Forbidden response
- ✅ Error message: "Only Company Admins and System Admins can access audit reports"

### Alternative Test (Frontend):
1. Log in as regular user
2. Navigate to Form Detail View
3. "View Compliance Report" button should NOT be visible

---

## API Testing (Direct)

### Form Audit Report
```bash
curl -X GET "http://localhost:8000/api/audit/form/32" \
  -H "Authorization: Bearer <admin_token>"
```

### Event Audit Report
```bash
curl -X GET "http://localhost:8000/api/audit/event/20" \
  -H "Authorization: Bearer <admin_token>"
```

### Company Activity Log
```bash
curl -X GET "http://localhost:8000/api/audit/company/activity?page=1&page_size=10" \
  -H "Authorization: Bearer <admin_token>"
```

### Security Test (Non-Admin)
```bash
curl -X GET "http://localhost:8000/api/audit/form/32" \
  -H "Authorization: Bearer <regular_user_token>"
# Expected: 403 Forbidden
```

---

## Test Results

| Test Case | Status | Notes |
|-----------|--------|-------|
| 1. Full Lifecycle Audit | ✅ PASS | Tested 27-Nov-2025: Full workflow verified - Form Created, Updated, Status change (Draft→Under Review), External Approval, Form Published (auto), and subsequent updates. All entries show correct user format and human-readable values. |
| 2. External Traceability | ✅ PASS | Tested 27-Nov-2025: External approval by peter@nottest.com shows "External" badge, Token ID: 5, and `form.published` action logged separately with 🚀 icon. |
| 3. Access Control Audit | ✅ PASS | Tested 27-Nov-2025: Access grant/revoke events logged correctly in Timeline. |
| 4. Activity Log Dashboard | ✅ **FIXED** | System Admin initially saw "No activity found" - Fixed by allowing System Admin to see all company activity when no company_id is set |
| 5. Security Check | ✅ PASS | Tested 27-Nov-2025: Company User could NOT see "View Compliance Report" button. Company Admin COULD see and access report. |

---

## Implementation Improvements Made During Testing

### Issues Found and Fixed:
1. **ID Translation** - Status IDs (1, 2, 3) were displayed instead of names (Draft, Under Review, Published)
   - Fixed: Backend now translates `form_status_id` → "Status: Name"
   
2. **User Display Format** - Users requested `email (FirstName LastName)` format
   - Fixed: All user references now display in this format
   
3. **Table Format for Updates** - Change entries needed 3-column table (Field | Original | New Value)
   - Fixed: Frontend parses old_value/new_value and displays in table format with visual highlighting
   
4. **Blank Update Entries** - Some updates logged with no actual changes
   - Fixed: Backend only logs updates when actual field changes are detected

5. **Auto-Publish Audit Gap** - Auto-publish after approval was not explicitly logged
   - Fixed: Added `form.published` action logged separately when approval triggers auto-publish
   - Affects: Internal approval (approve_form) and External approval (decide_via_token)

6. **System Admin Activity Log Empty** - System Admin could not see Activity Log (showed "No activity found")
   - Root Cause: Endpoint required `company_id` but System Admin may not have one set
   - Fixed: System Admin now sees ALL activity across all companies when no company_id is specified
   - Added optional `company_id_filter` query parameter for System Admin to filter by specific company

### Test Data Created:
- Form: "Audit Test Form 2.13" (FormID: 34)
- Event: CeBIT Australia 2025
- Users: User1@test.com (Company User), user2@test.com (Company Admin)

---

*UAT Test Guide for Story 2.13*
*Created: 2025-11-27*
*Last Updated: 2025-11-27*
*Status: ✅ ALL 5 TEST CASES PASSED*
