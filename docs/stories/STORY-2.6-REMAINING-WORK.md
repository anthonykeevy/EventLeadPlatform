# Story 2.6: Remaining Work Analysis

**Date:** November 12, 2025  
**Based on:** Story 2.7 Completion  
**Status:** Analysis of what's left to implement

---

## ✅ **What Was Already Implemented in Story 2.7**

### **Backend (Mostly Complete):**
- ✅ **Admin Review Service** (`admin_review_service.py`) - approve/reject methods implemented
- ✅ **Admin Review Router** (`admin_review_router.py`) - API endpoints exist
- ✅ **Admin Review Schemas** (`admin_review_schemas.py`) - Request/response models
- ✅ **Admin Dashboard Service** (`dashboard_service.py`) - Platform-wide KPIs and events
- ✅ **Admin Dashboard Router** (`dashboard_router.py`) - Admin dashboard endpoints
- ✅ **Public Visibility Logic** - Implemented in `approve_event()`
- ✅ **Audit Trail** - Logging implemented
- ✅ **Review Queue Query** - `get_pending_review_events()` implemented

### **Frontend (Mostly Complete):**
- ✅ **Admin Dashboard Page** (`AdminDashboard.tsx`) - Exists with Overview and Event Management tabs
- ✅ **Event Management Tab** (`EventManagementTab.tsx`) - Table with filtering and pagination
- ✅ **Event Review Modal** (`EventReviewModal.tsx`) - Approve/reject interface
- ✅ **Review History Component** (`ReviewHistory.tsx`) - Review history display
- ✅ **Admin APIs** (`adminDashboardApi.ts`, `adminReviewApi.ts`) - API integration
- ✅ **DataTable Component** (`DataTable.tsx`) - TanStack Table v8 integration
- ✅ **TanStack Table v8** - Installed and integrated
- ✅ **Admin Role Hook** (`useRequireAdmin.ts`) - Role verification
- ✅ **UserMenu Integration** - Admin Dashboard link for system admins
- ✅ **Admin Route** - `/admin/dashboard` route configured
- ✅ **Review Status Display** - ReviewStatusBadge in EventDetailView

---

## ❌ **What's Still Missing for Story 2.6**

### **1. Email Notification Integration** (Task 8 - HIGH PRIORITY)
**Status:** Email service exists, but NOT called from review service

**Missing:**
- ❌ `approve_event()` does NOT call `send_event_approval_notification()`
- ❌ `reject_event()` does NOT call `send_event_rejection_notification()`
- ❌ Email templates exist but not integrated

**Files to Update:**
- `backend/modules/events/admin_review_service.py` - Add email notification calls
- Verify email templates: `backend/templates/emails/event_approved.html` and `event_rejected.html`

**Implementation:**
```python
# In approve_event() method:
from services.email_service import EmailService

email_service = EmailService(self.db)
await email_service.send_event_approval_notification(
    event_creator_email=event.created_by_user.Email,
    event_name=event.Name,
    event_id=event.EventID,
    admin_comment=comment
)
```

### **2. Inline Editing in EventManagementTab** (Task 4 - MEDIUM PRIORITY)
**Status:** DataTable supports inline editing, but EventManagementTab doesn't use it

**Missing:**
- ❌ Inline editing for EventType (dropdown)
- ❌ Inline editing for EventStatus (dropdown)
- ❌ Inline editing for Industry (dropdown, optional)
- ❌ Inline editing for Company (dropdown)
- ❌ Save on change functionality

**Current State:**
- DataTable component has `enableInlineEditing` prop
- EventManagementTab uses DataTable but doesn't enable inline editing
- No `onCellEdit` handler implemented

**Implementation Needed:**
- Add `enableInlineEditing={true}` to DataTable in EventManagementTab
- Implement `onCellEdit` handler to call `adminDashboardApi.updateEvent()`
- Add foreign key dropdowns for editable columns
- Add save/cancel buttons for editing mode

### **3. Expandable Row Form** (Task 4 - MEDIUM PRIORITY)
**Status:** DataTable supports expandable rows, but EventManagementTab doesn't use it

**Missing:**
- ❌ Expand button on rows
- ❌ Form below row with all event fields
- ❌ Save/cancel buttons in expanded form

**Current State:**
- DataTable component has `enableExpandableRows` and `renderExpandedRow` props
- EventManagementTab doesn't use expandable rows

**Implementation Needed:**
- Add `enableExpandableRows={true}` to DataTable
- Create `renderExpandedRow` function with full event edit form
- Add expand/collapse button to each row

### **4. Foreign Key Dropdowns for Inline Editing** (Task 4 - MEDIUM PRIORITY)
**Status:** Reference data fetching exists, but dropdowns not integrated for editing

**Missing:**
- ❌ EventType dropdown in editable cells
- ❌ EventStatus dropdown in editable cells
- ❌ Industry dropdown in editable cells (optional)
- ❌ Company dropdown for owner/organizer

**Current State:**
- Reference data can be fetched (EventTypes, EventStatuses, etc.)
- Dropdowns exist in DataTable but not configured for EventManagementTab columns

**Implementation Needed:**
- Create `useReferenceData` hook (or use existing pattern)
- Configure column definitions with dropdown editors
- Handle foreign key updates via API

### **5. System Admin Detection in UserMenu** (Task 0 - LOW PRIORITY)
**Status:** Partially implemented

**Current State:**
- UserMenu checks `user.role === 'system_admin'`
- Admin Dashboard link exists
- BUT: Need to verify user.role is populated correctly from backend

**Missing:**
- ❌ Verify backend returns `role` field in user profile
- ❌ Verify role is set to `'system_admin'` for admin users
- ❌ Test that menu item appears only for admins

### **6. Admin Dashboard Enhancements** (Task 3 - LOW PRIORITY)
**Status:** Basic structure exists, but may need enhancements

**Missing:**
- ❌ Verify "Return to User Dashboard" link works (may already exist)
- ❌ Verify Overview tab shows all companies correctly
- ❌ Verify KPIs are platform-wide (not filtered by company)

**Current State:**
- AdminDashboard exists with tabs
- AdminCompanyList exists
- AdminKPISection may need verification

### **7. Review Status Display for Creators** (Task 12 - LOW PRIORITY)
**Status:** Partially implemented

**Current State:**
- ReviewStatusBadge exists
- EventDetailView may already show review status

**Missing:**
- ❌ Verify review status displays correctly in EventDetailView
- ❌ Verify review feedback shows for rejected events
- ❌ Verify review date and admin name display

### **8. Comprehensive Testing** (Task 16 - HIGH PRIORITY)
**Status:** UAT tests need to be created/executed

**Missing:**
- ❌ UAT test document for Story 2.6
- ❌ End-to-end review workflow testing
- ❌ Email notification testing
- ❌ Inline editing testing
- ❌ Role-based access control testing
- ❌ Logging validation (run `enhanced_diagnostic_logs.py`)

---

## 📋 **Prioritized Task List for Story 2.6**

### **🔥 High Priority (Must Have):**

1. **Email Notification Integration** (Task 8)
   - Add email calls to `approve_event()` and `reject_event()`
   - Test email delivery
   - Verify email templates render correctly
   - **Estimated:** 2-3 hours

2. **Comprehensive Testing** (Task 16)
   - Create UAT test document
   - Execute all test cases
   - Validate logging
   - **Estimated:** 4-6 hours

### **📊 Medium Priority (Should Have):**

3. **Inline Editing in EventManagementTab** (Task 4)
   - Enable inline editing in DataTable
   - Implement `onCellEdit` handler
   - Add foreign key dropdowns
   - **Estimated:** 4-6 hours

4. **Expandable Row Form** (Task 4)
   - Enable expandable rows
   - Create expanded row form
   - Add save/cancel functionality
   - **Estimated:** 3-4 hours

5. **Foreign Key Dropdowns** (Task 4)
   - Create `useReferenceData` hook
   - Configure dropdown editors for columns
   - Handle FK updates
   - **Estimated:** 2-3 hours

### **💡 Low Priority (Nice to Have):**

6. **System Admin Detection Verification** (Task 0)
   - Verify role population
   - Test menu visibility
   - **Estimated:** 1 hour

7. **Admin Dashboard Enhancements** (Task 3)
   - Verify all features work
   - Add any missing polish
   - **Estimated:** 1-2 hours

8. **Review Status Display Verification** (Task 12)
   - Verify display in EventDetailView
   - Test feedback display
   - **Estimated:** 1 hour

---

## 🎯 **Estimated Total Remaining Work**

**High Priority:** 6-9 hours  
**Medium Priority:** 9-13 hours  
**Low Priority:** 3-4 hours  
**Total:** 18-26 hours (~2-3 days)

---

## 📝 **Implementation Notes**

### **Email Notification Integration:**
- Email service already exists in `backend/services/email_service.py`
- Methods: `send_event_approval_notification()` and `send_event_rejection_notification()`
- Templates exist: `event_approved.html` and `event_rejected.html`
- Just need to call them from `admin_review_service.py`

### **Inline Editing:**
- DataTable component already supports inline editing
- Need to configure column definitions with `cell` renderer that shows dropdown when editing
- Use TanStack Table's `cell` function to conditionally render dropdown vs text

### **Expandable Rows:**
- DataTable component already supports expandable rows
- Need to create a form component for event editing
- Can reuse EditEventModal form fields or create a simplified inline form

### **Foreign Key Dropdowns:**
- Reference data can be fetched via existing API endpoints
- Use TanStack Query to cache reference data
- Create dropdown components that work within table cells

---

## ✅ **Completion Criteria**

Story 2.6 will be complete when:
1. ✅ Email notifications sent on approve/reject
2. ✅ Inline editing works for EventType, EventStatus, Industry, Company
3. ✅ Expandable row form works for full event editing
4. ✅ All UAT tests pass
5. ✅ Logging validation passes
6. ✅ Role-based access control verified

---

**Next Steps:**
1. Start with email notification integration (highest priority, easiest to implement)
2. Then implement inline editing and expandable rows
3. Finally, comprehensive testing and validation

