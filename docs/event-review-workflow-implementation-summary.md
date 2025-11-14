# Event Review Workflow - Complete Implementation Summary

**Date:** 2025-01-XX  
**Story:** 2.6 - Admin Public Event Review Workflow  
**Status:** ✅ Documentation Complete, Ready for Implementation

---

## Summary of Changes

All requested updates have been implemented in the documentation:

### ✅ 1. Scenario 3 - Additional Required Fields
- Added validation for additional required fields when changing private to public:
  - Name (required)
  - Description (required for public events)
  - StartDateTime (required)
  - EventTypeID (required)
  - City (recommended, warning if missing)
  - CountryID (recommended for physical/hybrid events)
  - VenueName or VenueAddress (recommended for physical/hybrid events)

### ✅ 2. Email Templates - Polite & Explanatory
- **Approval Email** (`backend/templates/emails/event_approved.html`):
  - Explains quality check process
  - Explains why we review events (no offensive language/inappropriate content)
  - References public event guidelines policy
  - Different messages based on EventStatus (PUBLISHED, DRAFT, CANCELLED)
  - Professional, helpful tone

- **Rejection Email** (`backend/templates/emails/event_rejected.html`):
  - Polite apology for rejection
  - Explains why we can't make event public
  - Reassures event is still available to company and linked organizations
  - Explains event won't be visible to others until issues addressed
  - Clear resubmission instructions
  - Link to public event guidelines
  - "Address Feedback & Resubmit" button

### ✅ 3. Public Event Guidelines Policy
- Created `docs/policies/public-event-guidelines.md`
- Explains review process and quality standards
- Lists common rejection reasons
- Provides resubmission process
- Explains event visibility options

### ✅ 4. Resubmission Workflow
- Added Scenario 7: Resubmit Rejected Event
- User can edit event and click "Resubmit for Review"
- System resets PublicReviewStatusID to PENDING
- Clears previous review data
- Event goes back to admin review queue

### ✅ 5. Company-Only Public Option
- Added Scenario 4B: Public Event Options
- Two visibility options:
  - **Company Network Only** (IsSharedWithPlatform = False):
    * No admin review required
    * Visible to company and linked organizations
    * NOT visible in platform-wide search
  
  - **Share with Platform** (IsSharedWithPlatform = True):
    * Requires admin review
    * Visible in platform-wide search
    * Other companies can discover and link

---

## Implementation Checklist

### **Database Schema**
- [ ] Add `IsSharedWithPlatform` field to Event table (if not exists)
- [ ] Create `ref.PublicReviewStatus` reference table
- [ ] Migrate `PublicReviewStatus` from NVARCHAR to FK
- [ ] Add index on `PublicReviewStatusID`

### **Backend Services**
- [ ] Update `create_event()` to validate additional fields for public events
- [ ] Update `update_event()` to validate additional fields when IsPublic changes to True
- [ ] Add resubmission endpoint: `POST /api/events/{event_id}/resubmit-review`
- [ ] Update `approve_event()` to NOT change EventStatus
- [ ] Update `reject_event()` to NOT change EventStatus
- [ ] Update email service to use new email templates
- [ ] Add event cancellation notification logic

### **Backend API**
- [ ] Add `IsSharedWithPlatform` field to event schemas
- [ ] Add resubmission endpoint
- [ ] Update public visibility query to check `IsSharedWithPlatform`
- [ ] Add validation for additional required fields for public events

### **Frontend**
- [ ] Add "Share with Platform" toggle/checkbox
- [ ] Add validation UI for additional required fields
- [ ] Add "Resubmit for Review" button for rejected events
- [ ] Update email template rendering (if needed)
- [ ] Add link to public event guidelines policy
- [ ] Update event creation/edit forms with new fields

### **Documentation**
- [x] Update workflow documentation
- [x] Create public event guidelines policy
- [x] Update email templates
- [ ] Update API documentation
- [ ] Update user guide

---

## Files Created/Updated

### **Created:**
1. `docs/policies/public-event-guidelines.md` - Public event policy document
2. `backend/templates/emails/event_approved.html` - Updated approval email
3. `backend/templates/emails/event_rejected.html` - Updated rejection email

### **Updated:**
1. `docs/event-public-review-workflow.md` - Complete workflow with all scenarios
2. `docs/event-review-workflow-implementation-summary.md` - This file

---

## Key Features

### **1. Additional Required Fields for Public Events**
- Description (required)
- City (recommended)
- CountryID (recommended for physical/hybrid)
- VenueName or VenueAddress (recommended for physical/hybrid)

### **2. Polite Email Messaging**
- Explains quality check process
- Reassures users about event availability
- Provides clear next steps
- Links to guidelines and support

### **3. Resubmission Workflow**
- User can resubmit rejected events
- System resets review status
- Event goes back to review queue

### **4. Company-Only Public Option**
- Users can make events public without platform-wide visibility
- No admin review required for company network only
- Useful for partner/supplier events

---

## Next Steps

1. **Review Documentation** - Ensure all requirements are captured
2. **Implement Database Changes** - Add `IsSharedWithPlatform` field and reference table
3. **Update Backend Services** - Implement validation, resubmission, and email updates
4. **Update Frontend** - Add UI for new options and validation
5. **Test Workflow** - End-to-end testing of all scenarios
6. **Deploy** - Roll out to production

---

## Questions for Clarification

1. **IsSharedWithPlatform Field**: Should this be a new field, or should we use `IsPublic` with a different meaning?
   - Proposed: Add `IsSharedWithPlatform` boolean field
   - `IsPublic = True` means "available to company network"
   - `IsSharedWithPlatform = True` means "visible in platform-wide search"

2. **Resubmission Limit**: Should there be a limit on resubmissions?
   - Proposed: No limit, but track resubmission count for admin visibility

3. **Event Cancellation Notification**: Who should be notified when an approved event is cancelled?
   - Proposed: Companies that linked to the event (EventCompany relationships)

---

**Status:** Documentation complete, ready for implementation review.
