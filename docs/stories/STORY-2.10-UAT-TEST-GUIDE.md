# Story 2.10 UAT Test Guide
**Form-Event Integration & Agency Access**

Date: 2025-11-22
Status: **Ready for Testing** 🧪

---

## 📝 **Overview**

This story implements the integration between Forms and Events, enabling:
1.  **Event-Form Linking:** Managing forms directly from the Event context.
2.  **Agency Access:** Allowing external agencies to view and work on events they are invited to.
3.  **Agency Sharing:** Host admins can share events with agencies.
4.  **Bulk Ownership Transfer:** Transferring all forms from one user to another (off-boarding).

---

## 👤 **Test Roles & Prerequisites**

You will need **two different browser sessions** (or Incognito window) to test the Agency Sharing flow effectively.

1.  **Host Admin (User A):** Admin of "Host Company" (e.g., `admin@host.com`).
2.  **Agency User (User B):** User of "Agency Company" (e.g., `user@agency.com`).
    *   *Note: If you don't have an Agency Company, create a new account and sign up as a new company.*
3.  **Host User (User C):** Another user in "Host Company" (for Ownership Transfer).

---

## 🧪 **Test Scenarios**

### **Category 1: Event-Form Linking (Event Detail View)**

**User:** Host Admin (User A)

| ID | Test Case | Steps | Expected Result | Pass/Fail |
|----|-----------|-------|-----------------|-----------|
| **1.1** | **View Linked Forms** | 1. Open an existing Event.<br>2. Scroll to "Linked Forms" section. | Section exists. Shows "No forms linked" or list of forms. | |
| **1.2** | **Create Form for Event** | 1. Click "Add Form" in Event Detail.<br>2. Complete Form Creation Modal.<br>3. Click Create. | Form is created.<br>Modal closes.<br>New form appears in "Linked Forms" list immediately. | |
| **1.3** | **Edit Form from Event** | 1. Click "Edit" (Pencil icon) on a linked form in the list. | User is navigated to Form Builder/Edit view for that form. | |
| **1.4** | **Unlink Form (Delete)** | 1. Click "Delete" (Trash icon) on a linked form.<br>2. Confirm deletion. | Form is removed from the list.<br>*Note: This performs a soft delete of the form.* | |

---

### **Category 2: Agency Sharing (Host Side)**

**User:** Host Admin (User A)

| ID | Test Case | Steps | Expected Result | Pass/Fail |
|----|-----------|-------|-----------------|-----------|
| **2.1** | **Open Share Modal** | 1. Go to Dashboard (Company Container).<br>2. Find an event card.<br>3. Click the purple "Share" icon (next to Edit/Delete). | "Share Event" modal opens. | |
| **2.2** | **Search Agency User** | 1. Enter the **Email Address** of the Agency User (User B) in the input field.<br>*(e.g., `test3@user.com`)* | Input field accepts email. | |
| **2.3** | **Share Event** | 1. Click "Grant Access". | System searches for user.<br>Success message appears: "Event shared with [Agency Name]".<br>Modal closes.<br>Event is now shared. | |

---

### **Category 3: Agency Access (Agency Side)**

**User:** Agency User (User B)
*Log in to a different browser/incognito window*

| ID | Test Case | Steps | Expected Result | Pass/Fail |
|----|-----------|-------|-----------------|-----------|
| **3.1** | **View Shared Event** | 1. Go to Dashboard.<br>2. Look at Event List. | The shared event from Host Company appears in the list.<br>Should be distinguishable or mixed in with access. | |
| **3.2** | **Access Shared Event** | 1. Click the shared event to open details. | Event Detail modal opens.<br>User can view event details (Read-only or Edit depending on role - specifically `agency_form_builder` allows form management). | |
| **3.3** | **Create Form for Shared Event** | 1. In Event Detail (Agency side), click "Add Form".<br>2. Create a form. | Form created successfully.<br>Form appears in "Linked Forms".<br>**Validation:** Form is linked to Host's Event. | |
| **3.4** | **View Host Forms** | 1. Observe "Linked Forms" list. | User B sees forms created by Host Admin (User A) if User B has access permissions (Agency role usually grants view/edit of event forms). | |

---

### **Category 4: Bulk Ownership Transfer**

**User:** Host Admin (User A)

| ID | Test Case | Steps | Expected Result | Pass/Fail |
|----|-----------|-------|-----------------|-----------|
| **4.1** | **Open Transfer Modal** | 1. Go to Team Management (Dashboard -> Users icon).<br>2. Find User C (or create a dummy user).<br>3. Click "Transfer" (Rotate icon) on User C's row. | "Transfer Form Ownership" modal opens.<br>Shows User C as "From". | |
| **4.2** | **Execute Transfer** | 1. Select User A (yourself) as "To User".<br>2. Enter reason "Testing".<br>3. Click "Transfer Ownership". | Success message.<br>Summary shows count of forms transferred.<br>Modal shows "Transfer Complete". | |

---

## 🐛 **Troubleshooting**

*   **No Events Showing for Agency?**
    *   Ensure the "Share" action in 2.3 actually succeeded (green toast).
    *   Ensure User B is actually in the "Agency Company" you selected.
*   **"Add Form" button missing?**
    *   Ensure the Event isn't Archived or Cancelled (unless allowed).
    *   Ensure you have permission (Company Admin or Agency Form Builder).
*   **"User not found" error in Share Modal?**
    *   Ensure the email entered matches exactly the email of User B in the system.
    *   User B must already be signed up and belong to a company.

---

## ✅ **Sign-Off**

**Tester Name:** ____________________
**Date:** ____________________
**Pass Rate:** ______ / 10

**Comments/Issues:**
