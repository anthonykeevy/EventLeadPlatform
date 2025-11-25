# UAT Test Guide - Story 2.11: Approval Workflows

## 📋 Test Information
- **Story:** 2.11 Approval Workflow Extensions
- **Tester:** [Your Name]
- **Date:** [Date]
- **Status:** Pending

## 🛠️ Pre-requisites
1.  Log in as **Company Admin** (to test approval).
2.  Log in as **Form Owner** (to test submission).
3.  Ensure **Email Service** is capturing emails (check logs or MailHog).
4.  **Cost Threshold** is configured to $100.00 (default).

## 🧪 Test Scenarios

### Scenario 1: Low Cost Form Workflow
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1.1 | Create new form "Low Cost Form" | Form created | |
| 1.2 | Set Deployment Cost to $50.00 | Saved successfully | |
| 1.3 | Verify "Submit for Approval" | Button should NOT be visible/required (or optional) | |
| 1.4 | Click "Publish" | Form publishes successfully | |

### Scenario 2: High Cost Form Submission
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 2.1 | Create new form "High Cost Form" | Form created | |
| 2.2 | Set Deployment Cost to $500.00 | Saved successfully | |
| 2.3 | Click "Publish" | **Blocked**. Error/Alert showing approval needed. | |
| 2.4 | Click "Submit for Approval" | Status changes to `PENDING`. Admin notified. | |
| 2.5 | Verify Dashboard Status | Shows "Pending Approval" badge. | |

### Scenario 3: Admin Approval
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 3.1 | Log in as Company Admin | Dashboard shows pending form | |
| 3.2 | Open "High Cost Form" | "Approve" and "Reject" buttons visible. | |
| 3.3 | Click "Approve" | Status changes to `APPROVED`. Owner notified. | |
| 3.4 | Log in as Owner | Verify status is `APPROVED`. | |
| 3.5 | Click "Publish" | Form publishes successfully. | |

### Scenario 4: Admin Rejection
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 4.1 | Create another High Cost Form | Status `PENDING` | |
| 4.2 | Log in as Admin | View form | |
| 4.3 | Click "Reject" | Prompt for reason appears. | |
| 4.4 | Enter reason "Too expensive" | Status changes to `REJECTED`. Owner notified. | |
| 4.5 | Click "Publish" (as Owner) | **Blocked**. | |
| 4.6 | Edit Cost to $50.00 | Saved. | |
| 4.7 | Publish | Allowed (Cost < Threshold). | |

## 📝 Notes
- Verify email content in logs.
- Verify Audit Trail logs for each action.
