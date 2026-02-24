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
- [x] Login as a Company Admin.
- [x] Navigate to Company Settings -> Form Approval Workflow.
- [x] Enable "Require Publish Approval".
- [x] Enable "Enforce Demo/Test Requirement" and set the threshold to `2`.
- [x] Navigate to Company Settings -> Form Defaults.
- [x] Set custom brand colors, a specific font family, and upload a default Terms & Conditions document (or URL).
- [x] **Pass Criteria**: Settings are saved and persist upon page reload.

### 1.2 Form Creation & Asset Management (Company User)
- [x] Login as a Company User (different account in the same company).
- [x] Create a new Event and navigate to the Event Dashboard.
- [x] Click "Create Form".
- [x] Verify that the Form Builder initializes with the Company Defaults applied (colors, fonts).
- [x] Upload a custom background image via the builder.
- [x] Drag and drop various components (Name, Email, Terms).
- [x] Verify the Terms component inherits the default Terms document.
- [x] **Pass Criteria**: Background uploads successfully, components reflect company defaults, form saves successfully as a draft.

---

## 🧪 Phase 2: Preview Governance & Publish Request

### 2.1 Preview Testing Gate (Company User)
- [x] In the Form Builder, note the Test Counter (should say `0 / 2 tests completed`).
- [x] Attempt to click "Request Publish" or "Publish" (depending on the button state).
- [x] **Pass Criteria**: The action is blocked, and the user is informed they must complete 2 preview tests.

### 2.2 Executing Preview Tests (Company User)
- [x] Toggle to "Preview Mode" or click the Preview link.
- [x] Submit the form with test data.
- [x] Repeat to submit a second test.
- [x] Return to the Builder/Dashboard.
- [x] **Pass Criteria**: Test Counter updates to `2 / 2`. The block on publishing is lifted.

### 2.3 Requesting Publish (Company User)
- [x] Click "Request Publish".
- [x] Select a Company Admin from the list and add an optional message.
- [x] **Pass Criteria**: Request is sent successfully. Form status updates to `Pending Admin Review`.

---

## 🧪 Phase 3: Admin Review, Publish, and Activation

### 3.1 Admin Review Queue (Company Admin)
- [x] Login as the Company Admin.
- [x] Navigate to the Event Dashboard or Form Review Queue.
- [x] Locate the form in `Pending Admin Review` status.
- [x] Click "Review and Publish".
- [x] **Pass Criteria**: Admin can view the form in a read-only review mode, seeing the exact layout, background, and defaults the user designed.

### 3.2 Publishing & Activation (Company Admin)
- [x] Approve the publish request.
- [x] (Simulated Payment) Confirm the publish action.
- [x] **Pass Criteria**: Form status changes to `Published`. A stable public URL is generated.
- [x] Open the public URL in an incognito window.
- [x] **Pass Criteria**: Form renders perfectly, matching the preview (Shared Resolver Parity).
- [x] Verify Activation Windows:
  - [x] Check if the form accepts submissions if within the event time window (± 3 hours).
  - [x] Modify the event dates to be in the past.
  - [x] Refresh the public URL.
  - [x] **Pass Criteria**: Form displays "This event has ended" (or similar) and blocks submissions.

---

## 🐞 Defect Tracking

Log any regressions, bugs, or UX friction points discovered during execution here.

| ID | Phase | Description | Expected Behavior | Actual Behavior | Status |
|----|-------|-------------|-------------------|-----------------|--------|
| 1  | 1.2   | Terms default not applied | Company default Terms document applied to Terms field | Terms field does not have company default document | Fixed  |
| 2  | 1.2   | Missing Authorization on Terms Link | Clicking Terms link in Preview mode shows PDF | Shows JSON error `{"detail": "Missing authorization header"}` | Fixed  |
| 3  | 1.2   | Terms PDF downloads instead of inline | Clicking Terms link opens a modal or inline view | Browser downloads the PDF file | Fixed  |
| 4  | 3.1   | Requester message missing on Review Page | Admin sees the message the requester typed when asking to publish | Message is not displayed on Review & Publish page | Fixed  |
| 5  | 1.1   | Form Branding on existing forms | New brand colors should optionally update existing forms | Only applies to new forms | Works as Intended (Added to Backlog) |
| 6  | 3.2   | No chat history for Publish Requests | Admin can reply, requester sees history | No history table/reply mechanism | Works as Intended (Added to Backlog) |

*(Dev agent will pick up Open defects from this table during the hardening cycle).*