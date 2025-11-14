# Event Creation Workflow - Implementation Gap Analysis

**Date:** January 15, 2025  
**Author:** Amelia 💻 (Developer Agent)  
**Status:** Story 2.4 - Event Management CRUD  
**Purpose:** Identify additional work required to implement the Event Creation Workflow document

---

## Executive Summary

The current implementation has **basic event CRUD functionality** but is missing the **3-page progressive disclosure workflow**, **EventCompany relationship management**, **smart field inference**, and **public event review workflow** described in the Event Creation Workflow document.

**Estimated Additional Work:** ~15-20 tasks across backend, frontend, and database layers.

---

## Current State Assessment

### ✅ What's Already Implemented

1. **Basic Event CRUD** - Create, Read, Update, Delete operations
2. **Event Type & Status Management** - Reference data integration
3. **Multi-Tenant Filtering** - Company-scoped event access
4. **Public Event Search** - Basic search functionality exists
5. **Event Form Validation** - Basic validation rules
6. **Timezone Detection** - Browser timezone auto-detection
7. **Database Schema** - Event table and EventCompany table exist (per database-schema.md)

### ❌ What's Missing

1. **EventCompany Model & Service** - No SQLAlchemy model or relationship creation logic
2. **3-Page Form Structure** - Current form is single-page
3. **Progressive Disclosure** - Form shows all fields at once
4. **Smart Field Inference APIs** - Timezone→Country mapping, user profile, company billing
5. **EventCompany Relationship Creation** - Not created when events are created/selected
6. **Public Event Review Workflow** - Admin review process not implemented
7. **Page Navigation** - No multi-step form navigation
8. **Skip Functionality** - Cannot skip Pages 2 & 3
9. **Summary Screen** - No summary/preview before submission
10. **Accessibility Enhancements** - Tooltip behavior, ARIA labels, keyboard navigation

---

## Detailed Gap Analysis

### 1. Backend: EventCompany Model & Service

**Status:** ❌ **NOT IMPLEMENTED**

**Current State:**
- EventCompany table exists in database (per database-schema.md)
- EventCompanyRole reference table exists
- No SQLAlchemy model in `backend/models/`
- No service methods for creating/managing EventCompany relationships

**Required Work:**

1. **Create EventCompany Model:**
   - File: `backend/models/event_company.py`
   - SQLAlchemy model mapping `dbo.EventCompany` table
   - Relationships: Event, Company, EventCompanyRole
   - Fields: EventID, CompanyID, EventCompanyRoleID, IsActive, FormsCreated, etc.

2. **Create EventCompanyRole Model:**
   - File: `backend/models/ref/event_company_role.py`
   - SQLAlchemy model mapping `ref.EventCompanyRole` table
   - Fields: RoleCode, RoleName, HasEditEvent, HasDeleteEvent, etc.

3. **Create EventCompany Service:**
   - File: `backend/modules/events/event_company_service.py`
   - Methods:
     - `create_event_company_relationship()` - Create owner/organizer/participant relationship
     - `get_event_companies()` - Get all companies for an event
     - `get_company_events()` - Get all events for a company
     - `disassociate_company_from_event()` - Soft delete participant relationship

4. **Update Event Service:**
   - File: `backend/modules/events/service.py`
   - In `create_event()`:
     - Create EventCompany relationship with `event_owner` role
     - If OrganizerCompanyID different from owner, create `event_organizer` relationship
   - In `get_events()`:
     - Filter by EventCompany relationships (not just Event.CompanyID)
     - Support participant role (companies using public events)

**Estimated Effort:** 2-3 days

---

### 2. Frontend: Tab-Based Form Structure with Progressive Disclosure

**Status:** ❌ **NOT IMPLEMENTED**

**Current State:**
- Single-page form in `CreateEventModal.tsx`
- All fields visible at once
- No tab structure or progressive disclosure

**Required Work:**

1. **Refactor CreateEventModal to Use Tabs:**
   - Keep same modal/popup structure
   - Add tab navigation component:
     - **Tab 1:** Essential Information (always visible after Private/Public selection)
     - **Tab 2:** Enhanced Details (Venue, Description, Industry)
     - **Tab 3:** Advanced Features (Organizer, Tags, Recurring, Metrics)
   - Tabs are clickable for navigation
   - Current tab is highlighted/active

2. **Progressive Disclosure (CRITICAL):**
   - **Initially:** Show ONLY Private/Public selection question
   - **No tabs visible** until Private/Public is selected
   - **After Private/Public selection:**
     - Show Tab 1 (Essential Information) with required fields
     - Tabs 2 and 3 become visible/accessible
     - Smooth animation/transition when fields appear
   - **Tab 2 & 3:** Can be skipped (optional content)

3. **Tab Navigation:**
   - User can click tabs to navigate between sections
   - "Skip" button available on Tab 2 & 3
   - "Create Event" button always visible (disabled until required fields complete)
   - "Skip to Summary" button available after Tab 1 complete

4. **Summary Screen (Optional Enhancement):**
   - Preview all entered data before final submission
   - Can be implemented later if needed

**Estimated Effort:** 2-3 days (reduced from 3-4 days due to tab-based approach)

---

### 3. Smart Field Inference

**Status:** ⚠️ **PARTIALLY IMPLEMENTED**

**Current State:**
- Browser timezone detection ✅
- User profile fallback ❌
- Company billing city fallback ❌
- Timezone → Country mapping ❌
- Previous event cities ❌
- IP geolocation ❌

**Required Work:**

1. **Backend API Endpoints:**

   **a. Timezone → Country Mapping:**
   - Endpoint: `GET /api/timezones/{timezone_identifier}/country`
   - File: `backend/modules/reference/timezone_router.py`
   - Query: `SELECT c.CountryID, c.CountryCode, c.CountryName FROM ref.Timezone t JOIN ref.Country c ON t.CountryCode = c.CountryCode WHERE t.TimezoneIdentifier = @TimezoneIdentifier`
   - Returns: Country info for timezone

   **b. User Profile Data:**
   - Endpoint: `GET /api/users/me/profile` (may exist, verify)
   - Returns: User.TimezoneIdentifier, User.CountryID
   - Enhance if missing: Add timezone and country to response

   **c. Company Profile Data:**
   - Endpoint: `GET /api/companies/{company_id}/profile` (may exist, verify)
   - Returns: Company.CountryID, CompanyBillingDetails.BillingCity
   - Enhance if missing: Add billing city to response

   **d. Recent Event Cities:**
   - Endpoint: `GET /api/events/recent-cities`
   - File: `backend/modules/events/router.py`
   - Query: `SELECT TOP 5 City, CountryID, MAX(CreatedDate) as LastUsed FROM dbo.Event WHERE CompanyID = @CompanyID AND IsDeleted = 0 GROUP BY City, CountryID ORDER BY LastUsed DESC`
   - Returns: List of recently used cities

   **e. IP Geolocation (Optional):**
   - Endpoint: `GET /api/geolocation/ip`
   - File: `backend/modules/geolocation/router.py`
   - Use external service (e.g., ipapi.co, ip-api.com)
   - Returns: Approximate city/country from IP
   - **Privacy Notice:** Must inform user

2. **Frontend Smart Inference:**
   - Call APIs on form load
   - Pre-fill fields with smart defaults
   - Show visual indicators (🔍 Auto-detected, 🔍 From your profile)
   - Allow user to override all pre-filled values

**Estimated Effort:** 2-3 days

---

### 4. Public Event Search & Selection

**Status:** ⚠️ **PARTIALLY IMPLEMENTED**

**Current State:**
- Public event search exists (`searchPublicEvents()`)
- Search results display event name, location, date
- User can select event to pre-fill form

**Required Work:**

1. **Update Public Event Search UX:**
   - Show search FIRST when Public is selected (before form fields)
   - Display: Event name, Location (City, State), Date range, Organizer company
   - "Use This Event" button for each result
   - "Similar events" section for near-matches
   - "Create New Public Event" button always visible

2. **Event Selection Logic:**
   - When user selects existing public event:
     - Create EventCompany relationship with `event_participant` role
     - Skip to summary screen (not create new event)
     - Show success message: "You're now using this public event"

3. **Backend: Create Participant Relationship:**
   - New endpoint: `POST /api/events/{event_id}/participate`
   - File: `backend/modules/events/router.py`
   - Creates EventCompany relationship with `event_participant` role
   - Returns: EventCompany relationship details

**Estimated Effort:** 1-2 days

---

### 5. Public Event Review Workflow

**Status:** ❌ **NOT IMPLEMENTED**

**Current State:**
- Event has `IsPublicReviewRequired`, `PublicReviewStatus` fields in database
- No admin review interface
- No status change logic when creating public events

**Required Work:**

1. **Backend: Update Event Creation:**
   - File: `backend/modules/events/service.py`
   - In `create_event()`:
     - If `IsPublic = True`:
       - Set `EventStatusID = PENDING_REVIEW` (not DRAFT)
       - Set `IsPublicReviewRequired = True`
       - Set `PublicReviewStatus = 'PENDING'`
       - Set `PublicReviewDate = NULL`
       - Set `PublicReviewBy = NULL`

2. **Backend: Admin Review Endpoints:**
   - Endpoint: `GET /api/admin/events/review-queue`
   - Returns: List of events with `PublicReviewStatus = 'PENDING'`
   - Endpoint: `POST /api/admin/events/{event_id}/approve`
   - Sets: `PublicReviewStatus = 'APPROVED'`, `PublicReviewDate`, `PublicReviewBy`, `EventStatusID = PUBLISHED`
   - Endpoint: `POST /api/admin/events/{event_id}/reject`
   - Sets: `PublicReviewStatus = 'REJECTED'`, `PublicReviewDate`, `PublicReviewBy`, `PublicReviewComments`

3. **Frontend: Admin Review Interface (Future Story):**
   - Admin dashboard for reviewing public events
   - Approve/Reject actions
   - Review comments

4. **Frontend: User Status Display:**
   - Show "Pending Review" badge on public events
   - Show "Rejected" badge with reason if rejected
   - Show "Published" badge if approved

**Estimated Effort:** 2-3 days (backend only, admin UI is separate story)

---

### 6. Progressive Disclosure Pattern

**Status:** ❌ **NOT IMPLEMENTED**

**Current State:**
- Form shows all fields when opened
- No progressive disclosure

**Required Work:**

1. **Form Initial State:**
   - Show ONLY Private/Public selection buttons
   - Hide all tabs and fields
   - No tabs visible until selection made
   - Smooth fade-in animation when content appears

2. **After Private/Public Selection:**
   - Show Tab 1 (Essential Information) with required fields
   - Tabs 2 and 3 become visible/accessible
   - Smooth animation/transition when tabs appear
   - Focus moves to first required field in Tab 1

3. **Tab Visibility:**
   - Tab 1: Always visible after Private/Public selection
   - Tab 2: Visible but optional (can be skipped)
   - Tab 3: Visible but optional (can be skipped)

4. **Visual Indicators:**
   - Show "🔍 Auto-detected" badge on auto-filled fields
   - Show "🔍 From your profile" badge on profile-sourced fields
   - Help text explains source of pre-filled values

**Estimated Effort:** 1 day (integrated with tab structure)

---

### 7. Form Validation & Button States

**Status:** ⚠️ **PARTIALLY IMPLEMENTED**

**Current State:**
- Basic validation exists
- Create Event button not always disabled when required fields incomplete
- No tooltip showing incomplete fields

**Required Work:**

1. **Real-Time Validation:**
   - Validate fields as user types/selects
   - Show inline error messages
   - Update button state immediately

2. **Create Event Button:**
   - Disabled when required fields incomplete
   - Tooltip on hover/focus showing incomplete fields
   - Format: "Please complete the following required fields: Event Name, Start Date, End Date, Event Type"
   - Keyboard accessible (appears on focus)

3. **Validation Rules:**
   - Private Events: Name (3-200 chars), Start/End Date, Event Type
   - Public Events: Name (10-200 chars), Start/End Date, City, Country, Event Type, Organizer Company, Short Description (50-500 chars)

**Estimated Effort:** 1-2 days

---

### 8. Accessibility Enhancements

**Status:** ⚠️ **PARTIALLY IMPLEMENTED**

**Current State:**
- Basic ARIA labels
- Some keyboard navigation
- Tooltip accessibility not implemented

**Required Work:**

1. **ARIA Labels:**
   - `aria-label` on all interactive elements
   - `aria-describedby` linking fields to help text
   - `aria-disabled="true"` on disabled buttons
   - `aria-required="true"` on required fields

2. **Keyboard Navigation:**
   - Tab key moves through fields
   - Shift+Tab for reverse navigation
   - Enter on button submits/continues
   - Escape closes modal

3. **Screen Reader Support:**
   - Announce field names and requirements
   - Announce validation errors immediately
   - Announce incomplete fields when button focused
   - Announce tooltip content

4. **Focus Management:**
   - Focus moves to first required field after selection
   - Focus moves to first incomplete field after validation error
   - Focus remains on Create Event button after submission

**Estimated Effort:** 1-2 days

---

### 9. Summary Screen (Optional Enhancement)

**Status:** ❌ **NOT IMPLEMENTED**

**Note:** This is optional and can be implemented later if needed. The tab-based approach allows users to review all tabs before submitting.

**Required Work (If Implemented):**

1. **Summary Component:**
   - File: `frontend/src/features/events/components/EventSummary.tsx`
   - Display all entered data in organized sections (matches tab structure)
   - Edit buttons for each section (returns to that tab)
   - "Create Event" final submission button

2. **Data Review:**
   - Show all fields with values
   - Highlight required fields that are empty
   - Show validation errors if any

**Estimated Effort:** 1 day (optional, can be deferred)

---

### 10. Skip Functionality

**Status:** ❌ **NOT IMPLEMENTED**

**Required Work:**

1. **Skip Buttons:**
   - "Skip to Summary" button (Pages 2 & 3)
   - "Skip This Page" button (Pages 2 & 3)
   - Only enabled after Page 1 required fields complete

2. **Skip Logic:**
   - Skip Page 2 → Go to Page 3 or Summary
   - Skip Page 3 → Go to Summary
   - Preserve entered data when skipping

**Estimated Effort:** 0.5 days

---

## Implementation Priority

### Phase 1: Core Workflow (High Priority)
1. ✅ EventCompany Model & Service
2. ✅ Tab-Based Form Structure (with Progressive Disclosure)
3. ✅ Progressive Disclosure Pattern
4. ✅ Public Event Selection → Participant Relationship

**Estimated Effort:** 4-6 days (reduced due to tab-based approach)

### Phase 2: Smart Features (Medium Priority)
5. ✅ Smart Field Inference APIs
6. ✅ Frontend Smart Inference Integration
7. ✅ Timezone → Country Mapping

**Estimated Effort:** 2-3 days

### Phase 3: Review Workflow (Medium Priority)
8. ✅ Public Event Review Backend Logic
9. ✅ Status Management for Public Events

**Estimated Effort:** 2-3 days

### Phase 4: UX Enhancements (Lower Priority)
10. ✅ Form Validation & Button States
11. ✅ Accessibility Enhancements
12. ✅ Summary Screen
13. ✅ Skip Functionality

**Estimated Effort:** 3-4 days

---

## Task Breakdown

### Backend Tasks

1. **Create EventCompany Model** (`backend/models/event_company.py`)
2. **Create EventCompanyRole Model** (`backend/models/ref/event_company_role.py`)
3. **Create EventCompany Service** (`backend/modules/events/event_company_service.py`)
4. **Update Event Service** - Add EventCompany relationship creation
5. **Create Timezone → Country API** (`GET /api/timezones/{timezone}/country`)
6. **Create Recent Cities API** (`GET /api/events/recent-cities`)
7. **Enhance User Profile API** - Add timezone/country if missing
8. **Enhance Company Profile API** - Add billing city if missing
9. **Create Participant Relationship Endpoint** (`POST /api/events/{event_id}/participate`)
10. **Update Event Creation** - Set PENDING_REVIEW for public events
11. **Create Admin Review Endpoints** (GET review queue, POST approve/reject)

### Frontend Tasks

12. **Refactor CreateEventModal** - Tab-based structure (Tab 1: Essentials, Tab 2: Enhanced Details, Tab 3: Advanced)
13. **Add Progressive Disclosure** - Show only Private/Public initially, then reveal tabs and fields
14. **Add Smart Field Inference** - Call APIs and pre-fill fields
15. **Add Public Event Search UX** - Show search first, then selection
16. **Add Tab Navigation** - Clickable tabs to navigate between sections
17. **Add Skip Functionality** - Skip buttons for Tabs 2 & 3 (optional)
18. **Add Form Validation** - Real-time validation with button states
19. **Add Tooltip Accessibility** - Show incomplete fields on button hover/focus
20. **Add Accessibility Enhancements** - ARIA labels, keyboard navigation, screen reader support

---

## Database Verification

**Per database-schema.md, the following tables exist:**
- ✅ `dbo.Event` - All required fields present
- ✅ `dbo.EventCompany` - Table exists with required fields
- ✅ `ref.EventCompanyRole` - Reference table exists
- ✅ `ref.EventType` - Exists
- ✅ `ref.EventStatus` - Exists
- ✅ `dbo.CompanyBillingDetails` - Exists (for city pre-fill)
- ✅ `ref.Timezone` - Verify CountryCode field exists for timezone→country mapping

**Action Required:**
- Verify `ref.Timezone` has `CountryCode` field
- If missing, add migration to add `CountryCode` to `ref.Timezone`

---

## Testing Requirements

1. **Unit Tests:**
   - EventCompany relationship creation
   - Smart field inference logic
   - Public event review status changes

2. **Integration Tests:**
   - Event creation with EventCompany relationship
   - Public event selection creates participant relationship
   - Timezone → Country mapping

3. **E2E Tests:**
   - 3-page form navigation
   - Progressive disclosure workflow
   - Public event search and selection
   - Summary screen and submission

---

## Documentation Updates

1. **API Documentation:**
   - Document new EventCompany endpoints
   - Document smart inference endpoints
   - Document admin review endpoints

2. **User Guide:**
   - Update event creation workflow documentation
   - Add screenshots of 3-page form
   - Document smart field inference features

---

## Summary

**Total Estimated Effort:** 11-15 days (reduced due to tab-based approach)

**Critical Path:**
1. EventCompany Model & Service (blocking)
2. Tab-Based Form Structure (blocking)
3. Progressive Disclosure (blocking)
4. Public Event Selection (blocking)

**Recommendation:** Implement in phases, starting with Phase 1 (Core Workflow) to establish the foundation, then adding smart features and enhancements incrementally.

---

**Last Updated:** January 15, 2025  
**Next Review:** After Phase 1 implementation

