# UAT Test Guide - Story 2.11: Approval Workflows

## 📋 Test Information
- **Story:** 2.11 Approval Workflow Extensions
- **Tester:** Tony
- **Date:** 25 November 2025
- **Status:** Passed

## 🛠️ Pre-requisites
1.  **Browser:** Chrome/Edge.
2.  **Configuration:** Cost Threshold is set to **$100.00**.
3.  **Users & Roles:**
    *   **User A (Creator):** `company_user` (Standard rights). Can create/edit.
    *   **User B (Admin):** `company_admin` (Full rights). Can approve/reject.
    *   **User C (Viewer):** `company_viewer` (Read-only).
    *   **User D (SysAdmin):** `system_admin` (Global override).

---

## 🧪 Test Scenarios

### Scenario 1: The "Standard" Flow (Low Cost)
*Goal: Verify seamless publishing for low-risk forms.*

| Step | User Role | Action | Expected Result | Pass/Fail |
|------|-----------|--------|-----------------|-----------|
| 1.1 | **Company User** | Create Form "Standard Form". Cost: **$50.00**. | Form created. Status: `Draft`. | **PASS** |
| 1.2 | **Company User** | Open Detail View. | Verify **"Publish"** button is visible. No approval badges. | **PASS** |
| 1.3 | **Company User** | Click **"Publish"**. | System checks cost ($50 < Threshold). Form becomes `Published`. | **PASS** |

### Scenario 2: The "Blocked" Flow (High Cost)
*Goal: Verify automated interception of high-cost publishes.*

| Step | User Role | Action | Expected Result | Pass/Fail |
|------|-----------|--------|-----------------|-----------|
| 2.1 | **Company User** | Create Form "Expensive Form". Cost: **$500.00**. | Form created. Status: `Draft`. | **PASS** |
| 2.2 | **Company User** | Click **"Publish"**. | **Interception Modal**: "Form requires approval based on your company's threshold and will be sent to Company Admins." | **PASS** |
| 2.3 | **Company User** | Confirm "Send Request". | Form Status remains `Draft`. Approval Status becomes `Pending`. Dashboard badge: "Pending Approval". | **PASS** |
| 2.4 | **Company User** | Check Dashboard. | Form card shows "Pending Approval". "Publish" button is now disabled/hidden. | **PASS** |

### Scenario 3: The "Governance" Flow (Admin Intervention)
*Goal: Verify Admin visibility and auto-publish action.*

| Step | User Role | Action | Expected Result | Pass/Fail |
|------|-----------|--------|-----------------|-----------|
| 3.1 | **Company Admin** | Log in. View Dashboard. | Sees "Expensive Form" with **"Pending Approval"** badge. | **PASS** |
| 3.2 | **Company Admin** | Open Detail View. | Sees **"Approve"** and **"Reject"** buttons. | **PASS** |
| 3.3 | **Company Admin** | Click **"Approve"**. | System sets Approval to `Approved`. **Auto-Action**: Form Status updates to `Published`. | **PASS** |
| 3.4 | **Company User** | Log in. Check "Expensive Form". | Form is now `Published`. | **PASS** |

### Scenario 4: The "Proactive" Flow (Pre-Approval & Admin Bypass)
*Goal: Verify Admin can pre-approve a draft OR publish directly (Bypass).*

| Step | User Role | Action | Expected Result | Pass/Fail |
|------|-----------|--------|-----------------|-----------|
| 4.1 | **Company User** | Create Form "Urgent Form". Cost: **$600.00**. | Status: `Draft`. Approval: `No Approval`. | **PASS** |
| 4.2 | **Company Admin** | Log in. Open "Urgent Form". | Sees form is high cost ($600). Sees **"Publish"** button (Admin Bypass) or **"Pre-Approve"** button. | **PASS** |
| 4.3 | **Company Admin** | Click **"Pre-Approve"**. | Approval Status becomes `Approved`. Form Status remains `Draft`. | **PASS** |
| 4.4 | **Company User** | Log in. Click **"Publish"**. | System checks cost ($600 > Threshold) BUT sees `Approved`. publishes immediately. | **PASS** |
| 4.5 | **Company Admin** | **(Bonus)** Create "Urgent CA Form" ($670). Click "Publish". | **Admin Bypass**: Confirmation prompt appears. Confirms. Form publishes immediately (No pending state). No email sent to self. | **PASS** |

### Scenario 5: The "Global Overseer" (System Admin)
*Goal: Verify System Admin has full visibility and override capability.*

| Step | User Role | Action | Expected Result | Pass/Fail |
|------|-----------|--------|-----------------|-----------|
| 5.1 | **System Admin** | Log in. Navigate to Company. | Sees all forms (Standard, Expensive, Urgent) with correct statuses. | **PASS** |
| 5.2 | **System Admin** | Open a new Pending Form. | Can see and click "Approve"/"Reject" buttons (same as Company Admin). | **PASS** |

### Scenario 6: The "Restricted" Flow (Viewer)
*Goal: Verify read-only users cannot trigger workflows.*

| Step | User Role | Action | Expected Result | Pass/Fail |
|------|-----------|--------|-----------------|-----------|
| 6.1 | **Company Viewer** | Log in. Open Dashboard. | **Result:** Sees no forms initially (Access Control working). | **PASS** |
| 6.2 | **Company Admin** | Grant "VIEW" access to "Standard Form" for Viewer. | Access saved. | **PASS** |
| 6.3 | **Company Viewer** | Refresh Dashboard. Open "Standard Form". | **Read-Only**. No Edit/Delete/Publish buttons. | **PASS** |
| 6.4 | **Company Admin** | Grant "EDIT" access to "Expensive Form" for Viewer. | Access saved. | **PASS** |
| 6.5 | **Company Viewer** | Open Edit Modal ("Expensive Form"). | Can edit questions. **Cannot** edit "Deployment Cost" or "Status". | **PASS** |

## 📝 Notes
- **Cost Threshold:** Default is $100.00.
- **Auto-Publish:** Approving a *Pending* request automatically publishes it. Approving a *Draft* (Pre-approval) only authorizes future publishing.
- **Admin Bypass:** Admins creating high-cost forms can publish immediately, bypassing the pending/email workflow.
- **Self-Notifications:** Emails are suppressed if the approver is also the form owner.
