# Story 5.9 UAT Test Guide: End-to-End Epic 5 Lifecycle

This guide covers the complete end-to-end testing of the Form Builder Readiness and Review/Publish Governance features built during Epic 5.

## Test Environment Setup
- **Database**: Clean local database or a test company with no existing forms.
- **Roles Required**: 
  1. `Company Admin` (for settings, approvals, and publishing)
  2. `Company User` (for form creation and publish requests)
- **Services**: Frontend, Backend (with Azure Blob Storage or local storage configured for assets).

---

## 🧪 Phase 1: Company Setup & Form Builder Readiness

### 1.1 Company Settings & Defaults (Company Admin)
- [ ] Login as a Company Admin.
- [ ] Navigate to Company Settings -> Form Approval Workflow.
- [ ] Enable "Require Publish Approval".
- [ ] Enable "Enforce Demo/Test Requirement" and set the threshold to `2`.
- [ ] Navigate to Company Settings -> Form Defaults.
- [ ] Set custom brand colors, a specific font family, and upload a default Terms & Conditions document (or URL).
- [ ] **Pass Criteria**: Settings are saved and persist upon page reload.

### 1.2 Form Creation & Asset Management (Company User)
- [ ] Login as a Company User (different account in the same company).
- [ ] Create a new Event and navigate to the Event Dashboard.
- [ ] Click "Create Form".
- [ ] Verify that the Form Builder initializes with the Company Defaults applied (colors, fonts).
- [ ] Upload a custom background image via the builder.
- [ ] Drag and drop various components (Name, Email, Terms).
- [ ] Verify the Terms component inherits the default Terms document.
- [ ] **Pass Criteria**: Background uploads successfully, components reflect company defaults, form saves successfully as a draft.

---

## 🧪 Phase 2: Preview Governance & Publish Request

### 2.1 Preview Testing Gate (Company User)
- [ ] In the Form Builder, note the Test Counter (should say `0 / 2 tests completed`).
- [ ] Attempt to click "Request Publish" or "Publish" (depending on the button state).
- [ ] **Pass Criteria**: The action is blocked, and the user is informed they must complete 2 preview tests.

### 2.2 Executing Preview Tests (Company User)
- [ ] Toggle to "Preview Mode" or click the Preview link.
- [ ] Submit the form with test data.
- [ ] Repeat to submit a second test.
- [ ] Return to the Builder/Dashboard.
- [ ] **Pass Criteria**: Test Counter updates to `2 / 2`. The block on publishing is lifted.

### 2.3 Requesting Publish (Company User)
- [ ] Click "Request Publish".
- [ ] Select a Company Admin from the list and add an optional message.
- [ ] **Pass Criteria**: Request is sent successfully. Form status updates to `Pending Admin Review`.

---

## 🧪 Phase 3: Admin Review, Publish, and Activation

### 3.1 Admin Review Queue (Company Admin)
- [ ] Login as the Company Admin.
- [ ] Navigate to the Event Dashboard or Form Review Queue.
- [ ] Locate the form in `Pending Admin Review` status.
- [ ] Click "Review and Publish".
- [ ] **Pass Criteria**: Admin can view the form in a read-only review mode, seeing the exact layout, background, and defaults the user designed.

### 3.2 Publishing & Activation (Company Admin)
- [ ] Approve the publish request.
- [ ] (Simulated Payment) Confirm the publish action.
- [ ] **Pass Criteria**: Form status changes to `Published`. A stable public URL is generated.
- [ ] Open the public URL in an incognito window.
- [ ] **Pass Criteria**: Form renders perfectly, matching the preview (Shared Resolver Parity).
- [ ] Verify Activation Windows:
  - Check if the form accepts submissions if within the event time window (± 3 hours).
  - Modify the event dates to be in the past.
  - Refresh the public URL.
  - **Pass Criteria**: Form displays "This event has ended" (or similar) and blocks submissions.

---

## 🐞 Defect Tracking

Log any regressions, bugs, or UX friction points discovered during execution here.

| ID | Phase | Description | Expected Behavior | Actual Behavior | Status |
|----|-------|-------------|-------------------|-----------------|--------|
| 1  |       |             |                   |                 | Open   |
| 2  |       |             |                   |                 | Open   |
| 3  |       |             |                   |                 | Open   |

*(Dev agent will pick up Open defects from this table during the hardening cycle).*