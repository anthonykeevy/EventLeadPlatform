# Event Creation Workflow - Smoke Test

**Date:** November 4, 2025  
**Story:** 2.4 - Event Management CRUD  
**Purpose:** Quick validation of implemented features

> **💡 Automation Tip:** This smoke test can be automated using Cursor's browser tools.  
> See [BROWSER-AUTOMATION-SMOKE-TEST-GUIDE.md](./BROWSER-AUTOMATION-SMOKE-TEST-GUIDE.md) for instructions.  
> Quick start: Ask Cursor to "Run the Event Creation Smoke Test from docs/SMOKE-TEST-EVENT-CREATION.md"

---

## ✅ **Test 1: Event Creation Modal - Progressive Disclosure**

### Steps:
1. Navigate to Dashboard
2. Click "Create Event" button
3. **Expected:** Modal opens showing ONLY "Event" label with "Private" and "Public" radio buttons
4. **Expected:** No tabs visible yet
5. Select "Private"
6. **Expected:** Tabs appear (Tab 1: Essentials, Tab 2: Enhanced Details, Tab 3: Advanced)
7. **Expected:** Tab 1 (Essentials) is automatically selected and visible

### Validation:
- ✅ Progressive disclosure works (visibility selection first)
- ✅ Tabs appear after Private/Public selection
- ✅ Tab 1 is the default active tab

---

## ✅ **Test 2: Form Validation & Button States**

### Steps:
1. With Create Event modal open and Tab 1 visible
2. **Expected:** "Create Event" button is DISABLED (grayed out)
3. Hover over disabled button
4. **Expected:** Tooltip appears listing incomplete required fields:
   - "Event Name"
   - "Start Date/Time"
   - "Event Type"
   - "Event Visibility (Private/Public)"
5. Fill in Event Name: "Test Event"
6. **Expected:** "Create Event" button still disabled (other fields incomplete)
7. Fill in Start Date and Time
8. Select Event Type
9. **Expected:** "Create Event" button becomes ENABLED (all required fields complete)

### Validation:
- ✅ Button disabled when required fields incomplete
- ✅ Tooltip shows incomplete fields
- ✅ Button enabled when all required fields complete
- ✅ Real-time validation as you type

---

## ✅ **Test 3: Tab Navigation**

### Steps:
1. With modal open and Tab 1 visible
2. Click "Tab 2: Enhanced Details"
3. **Expected:** Tab 2 content appears (Location Information section)
4. **Expected:** Tab 2 button is highlighted/active
5. Click "Tab 3: Advanced"
6. **Expected:** Tab 3 content appears (Advanced Features section)
7. Click "← Back to Tab 1: Essentials" button
8. **Expected:** Returns to Tab 1

### Validation:
- ✅ Tab navigation works
- ✅ Active tab is visually highlighted
- ✅ "Skip" buttons work (Tab 2 → Tab 3, Tab 3 → Tab 1)

---

## ✅ **Test 4: Smart Field Inference**

### Steps:
1. Open Create Event modal
2. Select "Public"
3. **Expected:** Search interface appears for public events
4. Navigate to Tab 1: Essentials
5. Check Timezone field
6. **Expected:** Timezone is pre-filled with browser timezone
7. **Expected:** Visual indicator (🔍) shows "Auto-detected from timezone" or "From your profile"
8. Check Country field
9. **Expected:** Country may auto-fill from timezone (e.g., "Australia/Sydney" → "Australia")
10. **Expected:** Visual indicator shows source (e.g., "🔍 Auto-detected from timezone")
11. Check City field
12. **Expected:** City may pre-fill from recent events if available
13. **Expected:** Visual indicator shows "🔍 From your recent events" if pre-filled
14. Manually change any pre-filled field
15. **Expected:** Visual indicator disappears (field is now manually entered)

### Validation:
- ✅ Timezone auto-detected from browser
- ✅ Country auto-detected from timezone
- ✅ City pre-fills from recent events
- ✅ Visual indicators show source of pre-filled values
- ✅ User can override all pre-filled values
- ✅ Indicators disappear when user manually changes field

---

## ✅ **Test 5: Create Event**

### Steps:
1. Fill in all required fields:
   - Event Name: "Smoke Test Event"
   - Start Date: Today
   - Start Time: Current time + 1 hour
   - Event Type: Any type
2. Click "Create Event" button
3. **Expected:** Button shows loading state ("Creating...")
4. **Expected:** Success notification appears
5. **Expected:** Modal closes
6. **Expected:** Event appears in event list/dashboard

### Validation:
- ✅ Event creation succeeds
- ✅ Success notification appears
- ✅ Event appears in list after creation

---

## ✅ **Test 6: Event List & Detail View**

### Steps:
1. Navigate to Events page (if separate page exists) or Dashboard
2. **Expected:** Event list displays with events
3. Click on an event card
4. **Expected:** Event Detail View modal opens
5. **Expected:** All event information is displayed:
   - Event name, description
   - Date/time
   - Location
   - Event type, status
   - Organizer info (if available)
   - Metrics (expected attendees, forms created, etc.)
6. Click "Edit Event" button
7. **Expected:** Edit Event modal opens
8. Click "Delete Event" button
9. **Expected:** Delete confirmation dialog appears

### Validation:
- ✅ Event list displays correctly
- ✅ Event cards are clickable
- ✅ Event Detail View shows all information
- ✅ Edit and Delete actions work

---

## ✅ **Test 6a: Role-Based Access Control (Edit Event)**

### Steps:
1. Navigate to Dashboard and find an event where you are a **participant** (not owner/organizer)
   - Example: CeBIT event if you're a participant
2. Click on the event card to open Edit Event modal
3. **Expected:** Modal header shows "Your role: Participant (View Only)" or similar
4. **Expected:** All form fields are **greyed out** and **disabled**:
   - Event Name field: disabled
   - Start Date/Time fields: disabled
   - Event Type dropdown: disabled
   - All location fields: disabled
   - All other fields: disabled
5. **Expected:** "Update Event" button is **disabled** and greyed out
6. Hover over disabled "Update Event" button
7. **Expected:** Tooltip appears explaining why button is disabled (e.g., "You don't have permission to edit this event")
8. Try to click on any disabled field
9. **Expected:** Fields remain disabled, no interaction possible
10. Close modal and open an event where you are the **owner**
11. **Expected:** All fields are **enabled** and editable
12. **Expected:** "Update Event" button is **enabled**
13. **Expected:** Modal header shows "Your role: Owner" (no "View Only" badge)

### Validation:
- ✅ Participant role: All fields disabled
- ✅ Participant role: Update button disabled with tooltip
- ✅ Participant role: Visual "View Only" indicator in header
- ✅ Owner role: All fields enabled
- ✅ Owner role: Update button enabled
- ✅ Role information displayed correctly in modal header
- ✅ No separate API call needed for role (included in event response)

---

## ✅ **Test 6b: Organizer Company Field (Public Events)**

### Steps:
1. Open Create Event modal
2. Select "Public" visibility
3. Navigate to Tab 1: Essentials
4. **Expected:** "Organizer Company" dropdown field appears
5. **Expected:** Field is marked as **required** (red asterisk or label indicator)
6. **Expected:** Dropdown is populated with your companies
7. Select a company from the dropdown
8. **Expected:** Company is selected
9. Try to submit form without selecting Organizer Company
10. **Expected:** Validation error appears for "Organizer Company"
11. Select "Private" visibility
12. **Expected:** "Organizer Company" field is **hidden** (not needed for private events)

### Validation:
- ✅ Organizer Company field appears for public events
- ✅ Field is required for public events
- ✅ Dropdown populated with user's companies
- ✅ Field hidden for private events
- ✅ Validation works correctly

---

## ✅ **Test 6c: City Pre-filling (Public Events)**

### Steps:
1. Open Create Event modal
2. Select "Public" visibility
3. Navigate to Tab 1: Essentials
4. **Expected:** City field is visible and required
5. **Expected:** If you have recent events with cities, City field may be pre-filled
6. **Expected:** Visual indicator (🔍) shows source if city is pre-filled
7. **Expected:** You can manually override the pre-filled city
8. Select "Private" visibility
9. Navigate to Tab 2: Enhanced Details
10. **Expected:** City field is in Tab 2 (not Tab 1) and is **optional**

### Validation:
- ✅ City field in Tab 1 for public events (required)
- ✅ City field in Tab 2 for private events (optional)
- ✅ City pre-fills from recent events if available
- ✅ Visual indicator shows source of pre-filled data
- ✅ User can override pre-filled values

---

## ✅ **Test 7: Accessibility Features**

### Steps:
1. Open Create Event modal
2. Press Tab key
3. **Expected:** Focus moves through form fields
4. Press Shift+Tab
5. **Expected:** Focus moves backwards
6. Press Escape key
7. **Expected:** Modal closes
8. Use screen reader (if available) or check browser DevTools
9. **Expected:** ARIA labels are present on interactive elements
10. **Expected:** Required fields have `aria-required="true"`

### Validation:
- ✅ Keyboard navigation works (Tab, Shift+Tab, Escape)
- ✅ ARIA labels present
- ✅ Required fields have proper ARIA attributes
- ✅ Screen reader friendly

---

## ✅ **Test 8: Public Event Search (If Public Selected)**

### Steps:
1. Open Create Event modal
2. Select "Public"
3. **Expected:** Search interface appears
4. Type "Sydney" in search box
5. **Expected:** Search results appear (if public events exist)
6. **Expected:** Results show event name, location, date range
7. Click "Use This Event" on a result
8. **Expected:** Form pre-fills with event details
9. **Expected:** "Create New Public Event" button is visible

### Validation:
- ✅ Public event search works
- ✅ Search results display correctly
- ✅ "Use This Event" pre-fills form
- ✅ Can skip search and create new event
- ✅ "Use This Event" creates participant relationship (idempotent - can click multiple times)
- ✅ Success message shows if already using event

---

## 🚨 **Quick Failure Checks:**

### If any of these fail, stop and investigate:
- ❌ Modal doesn't open
- ❌ JSX/compilation errors in console
- ❌ "Create Event" button always disabled (even with all fields filled)
- ❌ Tab navigation doesn't work
- ❌ Event creation fails (check network tab for 4xx/5xx errors)
- ❌ Event doesn't appear in list after creation
- ❌ Participant can edit events (should be view-only)
- ❌ Owner can't edit events (should be able to edit)
- ❌ Role information not displayed in Edit Event modal
- ❌ Organizer Company field missing for public events
- ❌ City field in wrong tab for public/private events

---

## 📝 **Notes:**

- **Browser:** Chrome/Edge recommended for best compatibility
- **Console:** Check browser DevTools for any errors
- **Network:** Check Network tab for failed API requests
  - **Important:** Role should be included in event response (no separate `/my-role` API call)
- **Time:** Each test should take 1-2 minutes
- **Total Time:** ~15-20 minutes for full smoke test
- **Role Testing:** 
  - To test participant role, use an event where your company is a participant (not owner)
  - To test owner role, create a new event or use an event you own
  - Role information is automatically included in event data (check Network tab to verify)

---

## ✅ **Success Criteria:**

All tests pass = ✅ Implementation validated  
Any test fails = ❌ Investigate and fix before proceeding

---

**Last Updated:** November 4, 2025  
**Tested By:** [Your Name]  
**Status:** [ ] Passed [ ] Failed [ ] Partial

---

## 🔄 **Recent Updates (November 4, 2025):**

### New Features Added:
1. **Role-Based Access Control (Test 6a)**
   - Edit Event modal now respects user roles (owner, organizer, participant)
   - Participant users see disabled fields and "View Only" status
   - Role information included in event response (no separate API call)

2. **Organizer Company Field (Test 6b)**
   - Required field for public events in Tab 1: Essentials
   - Populated with user's companies
   - Hidden for private events

3. **City Pre-filling (Test 6c)**
   - City field location differs for public vs private events
   - Public: Tab 1 (required)
   - Private: Tab 2 (optional)
   - Smart inference from recent events

4. **Enhanced Smart Field Inference (Test 4)**
   - Country auto-detection from timezone
   - City pre-filling from recent events
   - Visual indicators show source of pre-filled data

5. **Idempotent "Use This Event" (Test 8)**
   - Can click "Use This Event" multiple times without error
   - Success message if already using event

