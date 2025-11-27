# UAT Test Guide - Story 2.12: External Approver Support

## 📋 Test Information
- **Story:** 2.12 External Approver Support
- **Tester:** [Your Name]
- **Date:** 2025-11-27
- **Status:** ✅ PASSED

## 🛠️ Pre-requisites
1.  **Browser:** Chrome/Edge (plus Incognito window for external simulation).
2.  **Test Emails:**
    *   `creator@company.com` (Internal User)
    *   `cfo@company.com` (Internal Colleague - No Account)
    *   `client@external.com` (External Client - No Account)
3.  **Database Access:** Ability to run SQL queries (or use `scripts/` tools) to toggle settings.

---

## 🧪 Test Scenarios

### ⚙️ Configuration Setup (Crucial for Scenario 1)
*By default, the system blocks internal domains to prevent circumvention. For the "Busy CFO" scenario, we must enable internal domains.*

**Action:** Run this SQL in your database:
```sql
UPDATE [config].[AppSetting] 
SET SettingValue = 'true' 
WHERE SettingKey = 'forms.approval.allow_internal_domains';
```

---

### Scenario 1: The "Busy CFO" (Internal Domain, No Account)
*Goal: Verify you can send an approval request to a colleague (same domain) who doesn't have a login.*

| Step | User Role | Action | Expected Result | Pass/Fail |
|------|-----------|--------|-----------------|-----------|
| 1.1 | **Creator** | Create Form "Budget Form". Cost: **$2,000.00**. | Form created. Status: `Draft`. | ✅ |
| 1.2 | **Creator** | Open Detail View -> **"Publish (Request Approval)"**. | Select **"External Approval"**. | ✅ |
| 1.3 | **Creator** | Enter Email: `cfo@company.com` (Use a real testing alias if possible). | **Success:** Request sent. (If this fails, check Config Step above). | ✅ |
| 1.4 | **System** | (Backend Check) Check `User` table for `cfo@company.com`. | **Result:** New User created. Status=`EXTERNAL`. | ✅ |
| 1.5 | **CFO** | (Simulated) Open link from email in **Incognito**. | Approval Page loads. Shows "Budget Form". | ✅ |
| 1.6 | **CFO** | Click **"Approve"**. | Success message. | ✅ |
| 1.7 | **Creator** | Refresh Dashboard. | Form is `Published`. Audit Log: "Approved by external user cfo@company.com". | ✅ |

### Scenario 2: The "Agency Client" (External Domain)
*Goal: Verify standard external approval works for different domains.*

| Step | User Role | Action | Expected Result | Pass/Fail |
|------|-----------|--------|-----------------|-----------|
| 2.1 | **Creator** | Create Form "Client Campaign". Cost: **$500.00**. | Form created. | ✅ |
| 2.2 | **Creator** | Request Approval -> `client@external.com`. | **Success:** Request sent. | ✅ |
| 2.3 | **Client** | Open link -> Click **"Reject"**. Enter Reason: "Logo is wrong". | Success message. | ✅ |
| 2.4 | **Creator** | Refresh Dashboard. | Form Status: `Rejected`. Audit Log: "Rejected... Reason: Logo is wrong". | ✅ |

### Scenario 3: The "Self-Approval" Block (Fraud Check)
*Goal: Verify that even with Internal Domains ENABLED, you cannot approve your own form.*

| Step | User Role | Action | Expected Result | Pass/Fail |
|------|-----------|--------|-----------------|-----------|
| 3.1 | **Creator** | Create Form "Fraud Test". Cost: **$150.00**. | Form created. | ✅ |
| 3.2 | **Creator** | Request Approval -> Enter **YOUR OWN** email (`creator@company.com`). | **Error:** "Self-approval is not allowed. Please choose a different approver." | ✅ |
| 3.3 | **Creator** | (Edge Case) Try case variation `Creator@Company.com`. | **Error:** Still blocked (Case insensitive check). | ✅ |

### Scenario 4: The "Upgrade" Flow (History Retention)
*Goal: Verify if the CFO later gets an account, their history is kept.*

| Step | User Role | Action | Expected Result | Pass/Fail |
|------|-----------|--------|-----------------|-----------|
| 4.1 | **CFO** | Go to **Sign Up** page. | Signup form loads. | ✅ |
| 4.2 | **CFO** | Sign up as `cfo@company.com` (Same email from Scenario 1). | **Success:** Account created. | ✅ |
| 4.3 | **System** | (Backend Check) Check `User` table. | **Result:** Still only 1 record for `cfo@company.com`. Status changed `EXTERNAL` -> `ACTIVE`. | ✅ |
| 4.4 | **System** | Check `ActivityLog` for the approval in Step 1.6. | The `UserID` on the log matches the new CFO account ID. | ✅ |

### Scenario 5: The "Unauthorized Internal User" Block
*Goal: Verify you cannot bypass permissions by sending an "external" request to a regular internal user.*

| Step | User Role | Action | Expected Result | Pass/Fail |
|------|-----------|--------|-----------------|-----------|
| 5.1 | **Admin** | Create a new user `intern@company.com` with role `Company User`. | User created. | ✅ |
| 5.2 | **Creator** | Create Form "Permission Test". | Form created. | ✅ |
| 5.3 | **Creator** | Request Approval -> Enter `intern@company.com`. | **Error:** "User intern@company.com is a member of this company but does not have approval permissions." | ✅ |
| 5.4 | **Creator** | Request Approval -> Enter an existing **Admin's** email. | **Success:** Request sent (Admins are allowed). | ✅ |

## 📝 Notes
- **MailHog:** Use http://localhost:8025 to capture emails.
- **Urgency:** If testing urgency, set the Event Date to tomorrow. The External Page should show an amber "Urgent" warning.
