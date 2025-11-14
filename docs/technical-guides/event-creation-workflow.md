# Event Creation Workflow - User Experience Guide

**Author:** Dimitri 🔍 (Data Domain Architect) + Sally 🎨 (UX Expert)  
**Date:** January 15, 2025  
**Status:** Epic 2 - Event Management System  
**Purpose:** Complete user experience workflow for event creation and management

---

## Overview

This document defines the complete user experience workflow for creating and managing events in EventLeadPlatform. It covers the 3-page form structure, Private vs Public event paths, EventCompany relationships, and the public event review process.

**Key Principle:** Start simple, reveal complexity as needed. Support both small businesses (quick creation) and event managers (comprehensive details).

---

## Table of Contents

1. [Event Creation Overview](#event-creation-overview)
2. [Page 1: Essential Information](#page-1-essential-information)
3. [Smart Field Inference](#smart-field-inference)
4. [Page 2: Enhanced Details](#page-2-enhanced-details)
5. [Page 3: Advanced Features](#page-3-advanced-features)
6. [Public Event Review Workflow](#public-event-review-workflow)
7. [EventCompany Relationships](#eventcompany-relationships)
8. [User Experience: What Users See](#user-experience-what-users-see)
9. [Database Structure](#database-structure)

---

## Event Creation Overview

### Workflow Decision Tree

```mermaid
graph TB
    START[User Clicks 'Create Event'] --> PAGE1[Page 1 Opens]
    PAGE1 --> DECISION{Private or Public?}
    
    DECISION -->|Private Selected| PRIVATEPATH[Private Event Path]
    DECISION -->|Public Selected| SEARCH[Search Existing Public Events]
    
    PRIVATEPATH --> MINIMAL[Minimal Required Fields<br/>- Event Name*<br/>- Start Date*<br/>- Start Time*<br/>- End Date*<br/>- End Time*<br/>- Timezone<br/>- Event Type*]
    MINIMAL --> PRIVATECONTINUE[Continue to Page 2<br/>Optional Details]
    
    SEARCH --> RESULTS{Events Found?}
    RESULTS -->|Yes - User Selects| SELECTED[User Selects Existing Event]
    RESULTS -->|No - User Creates| CREATEPUBLIC[Create New Public Event]
    
    SELECTED --> PARTICIPANT[User Becomes Participant<br/>EventCompany Created<br/>Skip to Summary]
    
    CREATEPUBLIC --> PUBLICREQUIRED[Public Event Required Fields<br/>- Event Name*<br/>- Start Date*<br/>- Start Time*<br/>- End Date*<br/>- End Time*<br/>- Timezone (auto-detected)<br/>- Country* (inferred from timezone)<br/>- City* (pre-filled from company/previous)<br/>- Event Type*<br/>- Organizer Company*<br/>- Short Description*]
    PUBLICREQUIRED --> VALIDATE[Validate & Check Duplicates]
    VALIDATE --> REVIEW[Status: PENDING_REVIEW<br/>Awaiting Admin Approval]
    REVIEW --> APPROVED{Admin Approved?}
    APPROVED -->|Yes| PUBLIC[Event Becomes Public<br/>Status: PUBLISHED]
    APPROVED -->|No| REJECTED[Event Rejected<br/>Status: REJECTED]
    
    PRIVATECONTINUE --> PAGE2[Page 2: Enhanced Details]
    PUBLIC --> PAGE2
    
    PAGE2 --> PAGE3[Page 3: Advanced Features]
    PAGE3 --> SUMMARY[Summary Screen]
    SUMMARY --> SUBMIT[Submit Event]
    
    style PRIVATEPATH fill:#e8f5e9
    style SEARCH fill:#fff4e1
    style SELECTED fill:#e3f2fd
    style CREATEPUBLIC fill:#fff4e1
    style REVIEW fill:#fff9c4
    style PUBLIC fill:#e8f5e9
```

---

## Page 1: Essential Information

### Progressive Disclosure Pattern

**Form Initial State:**
- Form opens with **ONLY** the Private/Public selection question
- No other fields are visible initially
- This reduces cognitive load and prevents confusion

**After Private/Public Selection:**
- Required fields appear based on selection path (Private or Public)
- Fields appear with smooth animation/transition
- Form validates in real-time as user completes fields

**Create Event Button:**
- Always visible but disabled until all required fields are complete
- Tooltip shows incomplete fields when hovering or tabbing to disabled button
- Button becomes active (clickable) only when all required fields are valid

### Step 1: Private/Public Decision (Always First)

**Purpose:** Determine event visibility and complexity upfront. This is the ONLY question shown when the form first opens.

**Progressive Disclosure:**
- **Initially:** Only Private/Public selection buttons are visible
- **After Selection:** Required fields appear based on choice (Private or Public path)
- **No Fields Shown:** Until user makes Private/Public selection
- **Purpose:** Reduces cognitive load and prevents confusion about which fields apply

**User Experience:**
- Large, clear buttons with explanatory text
- Visual distinction between Private and Public
- Help text explaining the difference
- **No other fields visible** until selection is made
- Smooth animation/transition when fields appear after selection

**Layout:**
```
┌─────────────────────────────────────────────────┐
│  Create Event                                   │
│  Step 1 of 3: The Essentials                   │
│  ⚪⚪⚪                                          │
├─────────────────────────────────────────────────┤
│                                                  │
│  Is this a Private or Public event? *           │
│                                                  │
│  ┌─────────────┐  ┌─────────────┐              │
│  │   🔒 PRIVATE │  │   🌍 PUBLIC │              │
│  │             │  │             │              │
│  │ Only my     │  │ All         │              │
│  │ company can │  │ companies   │              │
│  │ see this    │  │ can see and │              │
│  │             │  │ use this    │              │
│  │ Quick setup │  │ Search first│              │
│  │ Minimal info│  │ More details│              │
│  └─────────────┘  └─────────────┘              │
│                                                  │
│  ℹ️ Private: Perfect for internal events        │
│  ℹ️ Public: Great for trade shows, conferences  │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

### Step 2A: Private Event Path (If Private Selected)

**Progressive Disclosure:**
- After selecting Private, required fields appear below the selection
- Fields appear smoothly with animation
- No page refresh required

**After selecting Private:**

**Required Fields:**
- **Event Name*** (text input, required)
- **Start Date*** (date picker, required)
- **Start Time*** (time picker, required)
- **End Date*** (date picker, required)
- **End Time*** (time picker, required)
- **Timezone** (dropdown, auto-detected from browser, user can override)
- **Event Type*** (dropdown, required)

**Smart Field Inference (Private Events):**
- **Timezone:** Auto-detected from browser (`Intl.DateTimeFormat().resolvedOptions().timeZone`)
- **Falls back to:** User profile timezone (`User.TimezoneIdentifier`)
- **Default:** `Australia/Sydney` if neither available
- **User Can Override:** Dropdown allows changing timezone if event is in different location

**Auto-Set:**
- `IsPublic = 0` (Private)
- `EventStatusID = DRAFT` (Draft status)
- `CompanyID = CurrentUser.CompanyID` (Owner company)

**User Experience:**
- Clean, minimal layout
- Clear required field indicators (*)
- Helpful hints for each field
- **Create Event Button:** Disabled until all required fields are complete
- **Button Tooltip:** Shows list of incomplete fields when hovering or tabbing to disabled button
- "Continue" button proceeds to Page 2 (optional) - only enabled after all required fields complete
- "Skip to Summary" button available (minimal event) - only enabled after all required fields complete

**Create Event Button Behavior:**
- **Disabled State:** Button is visually disabled (grayed out) when required fields are incomplete
- **Tooltip Trigger:** Hover (mouse) or focus (keyboard tab) on disabled button
- **Tooltip Content:** Lists all incomplete required fields in clear, actionable format
- **Tooltip Format:** "Please complete the following required fields: Event Name, Start Date, End Date, Event Type"
- **Accessibility:** Tooltip is keyboard accessible (appears on focus), screen reader announces incomplete fields
- **Enabled State:** Button becomes active (clickable) only when all required fields are valid and complete

**Validation:**
- Name: 3-200 characters
- Start Date: Must be today or future
- End Date: Must be after Start Date
- End Time: Must be after Start Time if same date, or any time if End Date is after Start Date
- Event Type: Must select from dropdown

**Business Rules:**
- Private events require minimal information
- Can skip Pages 2 & 3 for quick creation
- No review process required
- Immediately available within company

**Accessibility Notes:**
- **Keyboard Navigation:** All fields accessible via Tab key
- **Screen Reader Support:** ARIA labels announce field names and requirements
- **Focus Management:** Focus moves to first required field after Private selection
- **Error Announcements:** Screen reader announces incomplete fields when button is focused
- **Tooltip Accessibility:** Tooltip appears on focus (keyboard) and hover (mouse)
- **Visual Indicators:** Disabled button uses both color and text indicators (not color alone)
- **Form Validation:** Real-time validation with clear error messages
- **Required Field Indicators:** Asterisk (*) plus text "required" for screen readers

---

### Step 2B: Public Event Path (If Public Selected)

**After selecting Public:**

**Sub-step 2B.1: Search Existing Events**

**Purpose:** Prevent duplicate public events and allow users to participate in existing events.

**User Experience:**
```
┌─────────────────────────────────────────────────┐
│  Create Event - Public                          │
│  Step 1 of 3: The Essentials                   │
│  ⚪⚪⚪                                          │
├─────────────────────────────────────────────────┤
│                                                  │
│  🔍 Search for existing events first             │
│                                                  │
│  Type event name, location, or organizer...     │
│  [Search: "CES 2025 Las Vegas"  🔍]            │
│                                                  │
│  ⚡ Searching...                                 │
│                                                  │
│  ┌─ Found Events ────────────────────────────┐  │
│  │                                          │  │
│  │ ✅ CES 2025                              │  │
│  │    📍 Las Vegas, Nevada                 │  │
│  │    📅 January 7-10, 2025                 │  │
│  │    👥 Organized by: Consumer Technology │  │
│  │    [Use This Event]                      │  │
│  │                                          │  │
│  │ 💡 Similar:                              │  │
│  │    Consumer Electronics Show 2025       │  │
│  │    📍 Las Vegas, Nevada                 │  │
│  │    [This might be the same event]       │  │
│  │                                          │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  ┌─ Or Create New Event ─────────────────────┐  │
│  │                                            │  │
│  │  [Create New Public Event]                 │  │
│  │                                            │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
└─────────────────────────────────────────────────┘
```

**Search Behavior:**
- Auto-search as user types (debounced 500ms)
- Real-time results showing:
  - Event name
  - Location (City, State)
  - Date range
  - Organizer company name
- "Use This Event" button for each result
- "Similar events" section for near-matches
- "Create New Public Event" option always visible

**If User Selects Existing Event:**
- User becomes participant (EventCompany relationship created)
- Skip to summary screen
- EventCompany record created:
  - `EventID` = Selected event ID
  - `CompanyID` = User's company ID
  - `EventCompanyRoleID` = `event_participant` role (references `ref.EventCompanyRole.EventCompanyRoleID`)
  - `IsActive` = 1
  - `CreatedBy` = Current user ID

**If User Clicks "Create New Public Event":**
- Proceed to Sub-step 2B.2

---

**Sub-step 2B.2: Create New Public Event**

**Progressive Disclosure:**
- After clicking "Create New Public Event", required fields appear
- Fields appear smoothly with animation
- No page refresh required

**Smart Field Inference (Reduces Customer Burden):**

The form intelligently pre-fills location-related fields to minimize data entry:

1. **Timezone Auto-Detection:**
   - **Browser Timezone:** Automatically detects user's browser timezone (e.g., `Intl.DateTimeFormat().resolvedOptions().timeZone`)
   - **User Profile:** Falls back to `User.TimezoneIdentifier` if available
   - **Default:** `Australia/Sydney` if neither available
   - **User Can Override:** Dropdown allows user to change if event is in different timezone

2. **Country Inference from Timezone:**
   - **Timezone → Country Mapping:** Uses `ref.Timezone.CountryCode` to infer country from selected timezone
   - **Example:** `Australia/Sydney` → `AU` (Australia)
   - **User Profile:** Falls back to `User.CountryID` if timezone doesn't map to country
   - **Company Profile:** Falls back to `Company.CountryID` if user country not available
   - **User Can Override:** Dropdown allows user to change if event is in different country

3. **City Pre-Fill:**
   - **Company Billing City:** If `CompanyBillingDetails.BillingCity` exists, pre-fill with billing city
   - **Previous Events:** If user has created events before, suggest most recent event city
   - **IP Geolocation:** As fallback, infer approximate city from user's IP address (with privacy notice)
   - **User Can Override:** Autocomplete allows user to search and select different city

4. **State/Province Auto-Suggestion:**
   - **City-Based:** When city is selected, suggest common state/province for that city
   - **Country-Based:** If city not found, suggest states/provinces for selected country
   - **Optional:** User can skip if not applicable to their country

**Benefits:**
- **Reduced Data Entry:** Most users only need to verify/confirm pre-filled values
- **Faster Form Completion:** Smart defaults reduce time to create event
- **Better UX:** Users feel the form "knows" their context
- **Error Prevention:** Less manual typing reduces typos and validation errors

**User Experience:**
- Fields appear with pre-filled values (clearly indicated as "suggested")
- Users can easily override any pre-filled value
- Clear visual indicators show which fields are auto-filled vs manually entered
- Help text explains where values came from (e.g., "Detected from your browser" or "From your company profile")

**Required Fields (Public Events):**
- **Event Name*** (text input, required, min 10 chars)
- **Start Date*** (date picker, required)
- **Start Time*** (time picker, required)
- **End Date*** (date picker, required)
- **End Time*** (time picker, required)
- **Location Group** (smart pre-fill with inference):
  - **Timezone** (dropdown, auto-detected from browser, user can override)
  - **Country*** (dropdown, auto-inferred from timezone, pre-filled from user/company, user can override)
  - **City*** (text input with autocomplete, pre-filled from company billing or previous events, user can override)
  - **State/Province** (text input, optional but recommended, auto-suggested based on city)
- **Event Type*** (dropdown, required)
- **Organizer Company*** (searchable dropdown, required)
- **Short Description*** (textarea, 50-500 chars, required)

**User Experience:**
```
┌─────────────────────────────────────────────────┐
│  Create Event - Public (New)                    │
│  Step 1 of 3: Essential Information            │
│  ⚪⚪⚪                                          │
├─────────────────────────────────────────────────┤
│                                                  │
│  ✓ Public Event (All companies can see)         │
│  ℹ️ More information required for public events │
│                                                  │
│  Event Name *                                    │
│  [_____________________________]                │
│  ℹ️ Make it specific to avoid duplicates        │
│                                                  │
│  When does it start? *                           │
│  Start Date: [📅] Start Time: [🕐]             │
│                                                  │
│  When does it end? *                             │
│  End Date: [📅] End Time: [🕐]                  │
│                                                  │
│  Where is it located? *                          │
│  Timezone: [Australia/Sydney ▼] 🔍 Auto-detected │
│  Country: [Australia ▼] 🔍 Inferred from timezone │
│  City: [Sydney] 🔍 From your company profile     │
│  State/Province: [New South Wales] (optional)    │
│  ℹ️ Location helps others find your event        │
│  ℹ️ You can change any suggested values          │
│                                                  │
│  What type of event? *                           │
│  [Trade Show ▼]                                 │
│                                                  │
│  Who is organizing this event? *                 │
│  [Search event organizers... ▼]               │
│  ℹ️ Select the company organizing this event   │
│                                                  │
│  Brief description * (max 500 characters)      │
│  [________________________________]             │
│  [___/500] Used in event listings              │
│  Example: "World's largest consumer..."         │
│                                                  │
│  ⚠️ This event will require admin review        │
│     before becoming public                       │
│                                                  │
├─────────────────────────────────────────────────┤
│  [← Back to Search]  [Save Draft]  [Create Event] │
│                      (disabled)  (tooltip on hover) │
└─────────────────────────────────────────────────┘
```

**Create Event Button Tooltip Example:**
When hovering or tabbing to disabled "Create Event" button:
```
┌─────────────────────────────────────────────┐
│ Please complete the following required      │
│ fields:                                      │
│ • Event Name                                 │
│ • Start Date                                 │
│ • End Date                                   │
│ • City                                       │
│ • Country                                    │
│ • Event Type                                 │
│ • Organizer Company                          │
│ • Short Description                          │
└─────────────────────────────────────────────┘
```

**Create Event Button Behavior:**
- **Disabled State:** Button is visually disabled (grayed out) when required fields are incomplete
- **Tooltip Trigger:** Hover (mouse) or focus (keyboard tab) on disabled button
- **Tooltip Content:** Lists all incomplete required fields in clear, actionable format
- **Tooltip Format:** "Please complete the following required fields: Event Name, Start Date, Start Time, End Date, End Time, City, Country, Event Type, Organizer Company, Short Description"
- **Accessibility:** 
  - Tooltip is keyboard accessible (appears on focus when button receives keyboard focus)
  - Screen reader announces incomplete fields when button is focused
  - ARIA attributes: `aria-disabled="true"` when disabled, `aria-describedby` points to tooltip
  - Button has `aria-label` explaining why it's disabled
- **Enabled State:** Button becomes active (clickable) only when all required fields are valid and complete
- **Real-time Validation:** Button state updates as user completes fields (no page refresh needed)
- **Visual Feedback:** Button state changes are animated (subtle fade in/out) for better UX

**Accessibility Notes:**
- **Keyboard Navigation:** All fields accessible via Tab key, Shift+Tab for reverse navigation
- **Screen Reader Support:** 
  - ARIA labels announce field names and requirements
  - Screen reader announces "required field" for each required field
  - Tooltip content is announced when button receives focus
- **Focus Management:** 
  - Focus moves to first required field after Public selection
  - Focus moves to first incomplete field after validation error
  - Focus remains on Create Event button after successful submission
- **Error Announcements:** 
  - Screen reader announces incomplete fields when button is focused
  - Inline error messages appear below each field with validation errors
  - Error messages are announced immediately when field loses focus
- **Tooltip Accessibility:** 
  - Tooltip appears on focus (keyboard) and hover (mouse)
  - Tooltip positioned to not obscure form fields
  - Tooltip content is accessible to screen readers
- **Visual Indicators:** 
  - Disabled button uses both color (grayed) and text (disabled state) indicators
  - Required fields use asterisk (*) plus visual styling
  - Error states use both color and icon indicators
- **Form Validation:** 
  - Real-time validation with clear error messages
  - Validation errors are announced to screen readers
  - Error messages are specific and actionable

**Validation (Before Proceeding):**
- Name: 10-200 characters (public events require more detail)
- Start Date: Must be future date
- End Date: Must be after Start Date
- End Time: Must be after Start Time if same date, or any time if End Date is after Start Date
- City: Required (cannot be empty)
- Country: Required (must select from dropdown)
- Event Type: Required (must select from dropdown)
- Organizer Company: Required (must select from searchable list)
- Short Description: 50-500 characters

**Duplicate Detection:**
- Before proceeding, check for potential duplicates:
  - Exact name match + same date + same city
  - Similar name (Levenshtein distance ≤ 5) + same date + same city
  - Same organizer + similar date (±3 days) + similar name
- If HIGH confidence duplicate found: Show warning, allow override
- If MEDIUM confidence: Show suggestion, allow proceed
- If LOW confidence: Proceed normally

**After Validation:**
- Create event with status: `PENDING_REVIEW`
- Set `IsPublicReviewRequired = 1`
- Set `PublicReviewStatus = 'PENDING'`
- Create EventCompany relationship:
  - `EventID` = New event ID
  - `CompanyID` = User's company ID
  - `EventCompanyRoleID` = `event_owner` role (references `ref.EventCompanyRole.EventCompanyRoleID`)
  - `IsActive` = 1
  - `CreatedBy` = Current user ID
- If OrganizerCompanyID different from owner:
  - Create additional EventCompany relationship:
    - `EventID` = New event ID
    - `CompanyID` = OrganizerCompanyID
    - `EventCompanyRoleID` = `event_organizer` role (references `ref.EventCompanyRole.EventCompanyRoleID`)
    - `IsActive` = 1
    - `CreatedBy` = Current user ID

**Continue to Page 2:**
- User can add more details (optional)
- Event remains in `PENDING_REVIEW` status
- Not visible to public until approved

---

## Smart Field Inference

### Overview

To reduce customer burden and improve form completion speed, the event creation form intelligently infers and pre-fills location-related fields using multiple data sources.

### Inference Strategy (Priority Order)

**1. Browser Detection (Highest Priority)**
- **Timezone:** Automatically detects browser timezone using `Intl.DateTimeFormat().resolvedOptions().timeZone`
- **Example:** User in Sydney sees `Australia/Sydney` automatically selected
- **Benefit:** No user input required for most cases
- **Override:** User can change timezone if event is in different location

**2. User Profile Data**
- **Timezone:** Falls back to `User.TimezoneIdentifier` if browser detection fails
- **Country:** Falls back to `User.CountryID` if timezone doesn't map to country
- **Benefit:** Consistent experience across devices for logged-in users

**3. Company Profile Data**
- **Country:** Falls back to `Company.CountryID` if user country not available
- **City:** Uses `CompanyBillingDetails.BillingCity` if available
- **Benefit:** Events for company often in same location as company

**4. Previous Event History**
- **City:** If user has created events before, suggest most recently used city
- **Timezone:** If user has created events in specific timezone, suggest that timezone
- **Benefit:** Users often create events in same location (e.g., trade show organizer)

**5. IP Geolocation (Fallback Only)**
- **City/Country:** As last resort, infer approximate location from user's IP address
- **Privacy Notice:** Must inform user that IP geolocation is being used
- **Accuracy:** Typically accurate to city level, but may be less precise
- **Benefit:** Works even for new users with no profile data

### Timezone → Country Mapping

**How It Works:**
- Uses `ref.Timezone.CountryCode` to map IANA timezone to ISO country code
- **Example:** `Australia/Sydney` → `AU` (Australia)
- **Example:** `America/New_York` → `US` (United States)
- **Example:** `Europe/London` → `GB` (United Kingdom)

**Edge Cases:**
- **Multiple Countries:** Some timezones span multiple countries (e.g., `America/New_York` could be US or Canada)
  - **Solution:** Show most common country, but allow user to override
  - **Fallback:** Use user/company country if available
- **Timezone Without Country:** If timezone doesn't have `CountryCode` in database
  - **Solution:** Fall back to user/company country
  - **Default:** Australia (`AU`) if no country available

### City Autocomplete and Suggestions

**Pre-Fill Sources (Priority Order):**
1. **Company Billing City:** `CompanyBillingDetails.BillingCity` (if available)
2. **Previous Events:** Most recent event city from user's event history
3. **IP Geolocation:** Approximate city from IP address (with privacy notice)

**Autocomplete Features:**
- **Smart Search:** As user types, search cities in selected country
- **State/Province Suggestions:** When city is selected, suggest common state/province
- **Popular Cities First:** Show most common cities for country first
- **Recent Cities:** Show user's previously used cities at top of list

### User Experience

**Visual Indicators:**
- **Auto-Filled Fields:** Show "🔍 Auto-detected" or "🔍 From your profile" badge
- **Editable:** All auto-filled fields are clearly editable
- **Help Text:** Explain where values came from (e.g., "Detected from your browser")
- **Override Clear:** User can easily change any pre-filled value

**Example Flow:**
1. User opens form → Timezone auto-detected: `Australia/Sydney`
2. Country auto-inferred: `Australia` (from timezone)
3. City pre-filled: `Sydney` (from company billing address)
4. User can verify/confirm or change any field
5. User types different city → Autocomplete suggests cities in Australia
6. User selects city → State/Province suggests "New South Wales"

**Benefits:**
- **Reduced Data Entry:** Most users only verify pre-filled values
- **Faster Completion:** Form fills in 2-3 seconds vs 30+ seconds manually
- **Better Accuracy:** Less manual typing reduces typos
- **Improved UX:** Users feel form "knows" their context

### Technical Implementation Notes

**Frontend:**
- Detect browser timezone on form load
- Call API to get timezone → country mapping
- Call API to get user/company profile data
- Call API to get previous event cities
- Pre-fill fields with smart defaults
- Show visual indicators for auto-filled fields

**Backend API Endpoints:**
- `GET /api/timezones/{timezone_id}/country` - Get country from timezone
- `GET /api/users/me/profile` - Get user profile (timezone, country)
- `GET /api/companies/{company_id}/profile` - Get company profile (country, billing city)
- `GET /api/events/recent-cities` - Get user's recently used cities
- `GET /api/geolocation/ip` - Get approximate location from IP (with privacy notice)

**Database Queries:**
```sql
-- Get country from timezone
SELECT c.CountryID, c.CountryCode, c.CountryName
FROM ref.Timezone t
JOIN ref.Country c ON t.CountryCode = c.CountryCode
WHERE t.TimezoneIdentifier = @TimezoneIdentifier;

-- Get user's recent cities
SELECT TOP 5 City, CountryID, MAX(CreatedDate) as LastUsed
FROM dbo.Event
WHERE CompanyID = @CompanyID
  AND IsDeleted = 0
GROUP BY City, CountryID
ORDER BY LastUsed DESC;
```

---

## Page 2: Enhanced Details

**Purpose:** Optional enhanced details for better event information.

**Visibility:**
- **Private Events:** Optional, can skip
- **Public Events:** Optional, but recommended for better discovery

**Fields:**
- **Location Section** (collapsible):
  - Venue Name (text input)
  - Venue Address (text input)
  - GPS Coordinates (auto-filled from address or manual entry)
- **Description Section:**
  - Short Description (if not filled on Page 1)
  - Full Description (rich text editor, optional)
- **Industry** (dropdown, optional, helps with recommendations)

**User Experience:**
- "Skip This Page" button prominently placed
- Collapsible sections for optional content
- Location auto-detection button
- Real-time character count for Short Description
- Help text explaining why fields help

**Validation:**
- Venue Address: If Venue Name provided, suggest completing address

**Business Rules:**
- All fields optional
- Can skip to Page 3 or Summary
- Auto-save on field changes

---

## Page 3: Advanced Features

**Purpose:** Advanced options for power users and comprehensive event management.

**Visibility:**
- **Private Events:** Optional, expert mode
- **Public Events:** Optional, expert mode

**Fields:**
- **Organizer Section** (if not filled on Page 1):
  - Organizer Company (searchable dropdown)
  - Organizer Contact Email (text input with validation)
  - Organizer Website (text input with URL validation)
- **Event Classification:**
  - Tags (multi-select with suggestions)
  - Industry (if not set on Page 2)
- **Recurring Event Settings:**
  - Is Recurring (toggle)
  - If enabled: Recurrence Pattern (daily, weekly, monthly, yearly, custom)
- **Review Settings:**
  - Public Visibility Date (date picker, optional - when to make public, only for public events)
- **Metrics** (post-event tracking):
  - Expected Attendees (number input, optional)
  - Actual Attendees (number input, disabled until after event)

**User Experience:**
- "Expert Mode" badge/indicator
- All sections optional
- Collapsible panels for advanced features
- Help tooltips explaining advanced features
- "Skip This Page" button available

**Validation:**
- Organizer Email: Valid email format if provided
- Organizer Website: Valid URL format if provided
- Public Visibility Date: Must be future date if provided
- Expected Attendees: Must be positive number if provided

**Business Rules:**
- All fields optional
- Can skip to Summary
- Expert features for experienced users

---

## Public Event Review Workflow

### Review Process Overview

**Purpose:** Ensure quality and prevent duplicate/low-quality public events.

**Trigger:** When user creates or updates a public event.

**Workflow:**
```
┌─────────────────────────────────────────────────┐
│  Public Event Review Workflow                  │
└─────────────────────────────────────────────────┘

1. User Creates/Updates Public Event
   ↓
2. Event Status: PENDING_REVIEW
   ↓
3. Admin Reviews Event
   ↓
4. Admin Decision:
   ├─ APPROVED → Event becomes PUBLIC
   └─ REJECTED → Event stays PRIVATE, user notified
```

---

### Step 1: Event Creation/Update

**When User Creates New Public Event:**
- Event created with:
  - `IsPublic = 1`
  - `EventStatusID = PENDING_REVIEW`
  - `IsPublicReviewRequired = 1`
  - `PublicReviewStatus = 'PENDING'`
  - `PublicReviewDate = NULL`
  - `PublicReviewBy = NULL`
- EventCompany relationship created:
  - `EventID` = New event ID
  - `CompanyID` = User's company ID
  - `EventCompanyRoleID` = `event_owner` role (references `ref.EventCompanyRole.EventCompanyRoleID`)
  - `IsActive` = 1

**When User Updates Existing Public Event:**
- Check if event is already public (`PublicReviewStatus = 'APPROVED'`)
- If yes: Set status to `PENDING_REVIEW` for update review
- If no: Update normally (still in review)

**User Experience:**
- After submitting public event:
  - Show message: "Your event has been submitted for review"
  - Show status badge: "Pending Review"
  - Explain: "This event will be available to all companies after admin approval"

---

### Step 2: Admin Review Process

**Admin Dashboard:**
- Review queue shows all events with `PublicReviewStatus = 'PENDING'`
- Shows event details:
  - Event Name
  - Location (City, State, Country)
  - Date/Time
  - Organizer Company
  - Short Description
  - Created By (user and company)
  - Created Date

**Admin Actions:**
1. **Approve Event:**
   - Set `PublicReviewStatus = 'APPROVED'`
   - Set `PublicReviewDate = GETUTCDATE()`
   - Set `PublicReviewBy = Admin UserID`
   - Set `EventStatusID = PUBLISHED`
   - If `PublicVisibilityDate` is set and future: Wait until that date
   - If `PublicVisibilityDate` is NULL or past: Make public immediately
   - Event becomes visible to all companies

2. **Reject Event:**
   - Set `PublicReviewStatus = 'REJECTED'`
   - Set `PublicReviewDate = GETUTCDATE()`
   - Set `PublicReviewBy = Admin UserID`
   - Set `PublicReviewComments = 'Admin rejection reason'`
   - Event remains private (only visible to owner company)
   - User notified with rejection reason

**Admin Review Criteria:**
- Event name is clear and specific
- Location information is complete
- Organizer company is valid
- Short description is informative (50-500 chars)
- No duplicate detected (or duplicate is acceptable)
- Event information is accurate

---

### Step 3: Update Review Process

**When User Updates Approved Public Event:**
- Before update: Save current state (for comparison)
- After update: Set `PublicReviewStatus = 'PENDING'` (for update review)
- Admin reviews changes:
  - Compare old vs new values
  - Approve or reject update
  - If approved: Update goes live
  - If rejected: Revert to previous approved state

**User Experience:**
- When updating approved public event:
  - Show warning: "This event is public. Changes require admin review."
  - Show current approved values (read-only)
  - Allow editing with clear indication changes need review
  - After saving: Show "Changes submitted for review"

---

### Step 4: Review Status Visibility

**User Dashboard:**
- Events show status badges:
  - **Draft** (Orange) - Private event, not yet submitted
  - **Pending Review** (Yellow) - Submitted for public review
  - **Published** (Green) - Approved and public
  - **Rejected** (Red) - Rejected by admin (with reason)
  - **Completed** (Blue) - Event has finished
  - **Cancelled** (Gray) - Event cancelled

**User Experience:**
- Status badges clearly visible on event cards
- Clicking status shows details:
  - Pending Review: "Submitted on [date], awaiting admin approval"
  - Rejected: "Rejected on [date]. Reason: [admin comments]"
  - Published: "Approved on [date] by admin"

---

## EventCompany Relationships

### Purpose

Track which companies participate in which events and their roles.

### Relationship Types

**1. Owner (event_owner):**
- Company that created the event
- Full control over event details
- Can edit all fields
- Can delete event
- Can manage participants

**2. Organizer (event_organizer):**
- Company organizing the event (if different from owner)
- Can edit extended fields (description, tags, organizer details)
- Cannot edit core fields (name, dates, location) unless granted
- Cannot delete event

**3. Participant (event_participant):**
- Company using public event for forms
- Read-only access (can view event details)
- Can disassociate from event
- Cannot edit event

---

### EventCompany Table Structure

```sql
CREATE TABLE [dbo].[EventCompany] (
    EventCompanyID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- Relationships
    EventID BIGINT NOT NULL,
    CompanyID BIGINT NOT NULL,
    EventCompanyRoleID BIGINT NOT NULL,  -- References ref.EventCompanyRole (event_owner, event_organizer, event_participant)
    
    -- Usage Metrics
    FormsCreated INT NOT NULL DEFAULT 0,
    FirstUsedDate DATETIME2 NULL,
    LastUsedDate DATETIME2 NULL,
    
    -- Access Control
    IsActive BIT NOT NULL DEFAULT 1,
    DisassociatedDate DATETIME2 NULL,
    DisassociatedBy BIGINT NULL,
    
    -- Audit Trail
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NOT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,
    
    CONSTRAINT FK_EventCompany_Event FOREIGN KEY (EventID) 
        REFERENCES [dbo].[Event](EventID),
    CONSTRAINT FK_EventCompany_Company FOREIGN KEY (CompanyID) 
        REFERENCES [dbo].[Company](CompanyID),
    CONSTRAINT FK_EventCompany_EventCompanyRole FOREIGN KEY (EventCompanyRoleID) 
        REFERENCES [ref].[EventCompanyRole](EventCompanyRoleID),
    CONSTRAINT UQ_EventCompany_Event_Company_Active UNIQUE (EventID, CompanyID, IsActive)
        WHERE IsActive = 1
);
GO
```

---

### Relationship Creation Workflows

**Workflow 1: User Creates Private Event**
```sql
-- Auto-create owner relationship
INSERT INTO [dbo].[EventCompany] (
    EventID, 
    CompanyID, 
    EventCompanyRoleID,  -- event_owner
    CreatedBy
)
VALUES (
    @NewEventID,
    @UserCompanyID,
    (SELECT EventCompanyRoleID FROM [ref].[EventCompanyRole] WHERE RoleCode = 'event_owner'),
    @CurrentUserID
);
```

**Workflow 2: User Creates Public Event**
```sql
-- Auto-create owner relationship
INSERT INTO [dbo].[EventCompany] (
    EventID, 
    CompanyID, 
    EventCompanyRoleID,  -- event_owner
    CreatedBy
)
VALUES (
    @NewEventID,
    @UserCompanyID,
    (SELECT EventCompanyRoleID FROM [ref].[EventCompanyRole] WHERE RoleCode = 'event_owner'),
    @CurrentUserID
);

-- If OrganizerCompanyID different from owner, create organizer relationship
IF @OrganizerCompanyID IS NOT NULL AND @OrganizerCompanyID != @OwnerCompanyID
BEGIN
    INSERT INTO [dbo].[EventCompany] (
        EventID, 
        CompanyID, 
        EventCompanyRoleID,  -- event_organizer
        CreatedBy
    )
    VALUES (
        @NewEventID,
        @OrganizerCompanyID,
        (SELECT EventCompanyRoleID FROM [ref].[EventCompanyRole] WHERE RoleCode = 'event_organizer'),
        @CurrentUserID
    );
END
```

**Workflow 3: User Selects Existing Public Event**
```sql
-- Create participant relationship
INSERT INTO [dbo].[EventCompany] (
    EventID, 
    CompanyID, 
    EventCompanyRoleID,  -- event_participant
    CreatedBy,
    FirstUsedDate
)
VALUES (
    @ExistingEventID,
    @UserCompanyID,
    (SELECT EventCompanyRoleID FROM [ref].[EventCompanyRole] WHERE RoleCode = 'event_participant'),
    @CurrentUserID,
    GETUTCDATE()
);
```

**Workflow 4: User Disassociates from Event**
```sql
-- Soft delete participant relationship
UPDATE [dbo].[EventCompany]
SET 
    IsActive = 0,
    DisassociatedDate = GETUTCDATE(),
    DisassociatedBy = @CurrentUserID,
    UpdatedDate = GETUTCDATE(),
    UpdatedBy = @CurrentUserID
WHERE EventID = @EventID
  AND CompanyID = @UserCompanyID
  AND EventCompanyRoleID = (SELECT EventCompanyRoleID FROM [ref].[EventCompanyRole] WHERE RoleCode = 'event_participant')
  AND IsActive = 1;
```

---

## User Experience: What Users See

### Company Dashboard: Events View

**What Users See:**
- **All events created by their company:**
  - Private events (always visible)
  - Public events (pending review, approved, rejected)
  - Status badges for each event
  - Created by information (who in their company created it)

**Filtering:**
- **By Status:**
  - All Events
  - Draft (private events not yet submitted)
  - Pending Review (public events awaiting approval)
  - Published (approved public events)
  - Rejected (public events rejected by admin)
  - Completed (events that have finished)
  - Cancelled (cancelled events)

- **By Type:**
  - Private Events
  - Public Events
  - All Events

- **By Date:**
  - Upcoming Events
  - Past Events
  - All Events

**Event Cards Display:**
- Event Name
- Date/Time (formatted for user's timezone)
- Location (City, State)
- Event Type
- Status Badge (color-coded)
- Created By (user name from their company)
- Created Date
- Forms Created (count)
- Actions: Edit, Delete, View Details

---

### Event Detail View

**What Users See:**
- **Complete event information:**
  - All event fields (as editable/read-only based on role)
  - Status badge and review information
  - Created/Updated information
  - EventCompany relationships (who participates)

**Status Information:**
- **If Pending Review:**
  - "Submitted for review on [date]"
  - "Awaiting admin approval"
  - "This event will be public after approval"

- **If Rejected:**
  - "Rejected on [date]"
  - "Reason: [admin comments]"
  - "Edit event to resubmit for review"

- **If Published:**
  - "Approved on [date] by admin"
  - "This event is visible to all companies"
  - "X companies are using this event" (if public)

**Edit Capabilities:**
- **Owner:** Can edit all fields
- **Organizer:** Can edit extended fields (description, tags, organizer details)
- **Participant:** Read-only view (cannot edit)

**Update Workflow:**
- **If Published Public Event:**
  - Show warning: "This event is public. Changes require admin review."
  - Allow editing with clear indication
  - After saving: Show "Changes submitted for review"
  - Status changes to "Pending Review" for update

---

### Public Event Search (When Creating Event)

**What Users See:**
- **Search Results:**
  - Event name
  - Location (City, State, Country)
  - Date range
  - Organizer company name
  - Short description preview
  - "Use This Event" button

- **Similar Events:**
  - Near-matches shown with "This might be the same event" label
  - User can select if it's the same event

- **Empty State:**
  - "No events found matching your search"
  - "Create new public event" button
  - Tips to refine search

---

### Review Status Indicators

**Visual Indicators:**
- **Draft** (Orange badge): Private event, not yet submitted
- **Pending Review** (Yellow badge): Submitted for public review, awaiting approval
- **Published** (Green badge): Approved and public, visible to all companies
- **Rejected** (Red badge): Rejected by admin, shows rejection reason
- **Completed** (Blue badge): Event has finished
- **Cancelled** (Gray badge): Event cancelled

**Status Messages:**
- Clear, actionable status messages
- Review timeline information
- Next steps guidance

---

## Database Structure

### EventCompanyRole Reference Table

**Purpose:** Define participation roles for companies in events with permission flags.

**Key Fields:**
- `EventCompanyRoleID` - Primary key (full table name + ID)
- `RoleCode` - Unique role code (event_owner, event_organizer, event_participant)
- `RoleName` - Display name (Event Owner, Event Organizer, Event Participant)
- `Description` - Full description of role permissions
- `RoleLevel` - Numeric hierarchy level (higher = more permissions)
- `HasEditEvent` - Can edit event details (boolean)
- `HasDeleteEvent` - Can delete event (boolean)
- `HasManageParticipants` - Can manage event participants (boolean)
- `HasViewEvent` - Can view event details (boolean)
- `IsActive` - Whether role is available for assignment
- `SortOrder` - Display order for role selection
- Standard audit columns

**Seed Data:**
- `event_owner` - Full control (HasEditEvent=1, HasDeleteEvent=1, HasManageParticipants=1, HasViewEvent=1)
- `event_organizer` - Extended edit only (HasEditEvent=1, HasDeleteEvent=0, HasManageParticipants=0, HasViewEvent=1)
- `event_participant` - Read-only (HasEditEvent=0, HasDeleteEvent=0, HasManageParticipants=0, HasViewEvent=1)

---

### EventCompany Table

**Purpose:** Track company-event relationships with roles.

**Key Fields:**
- `EventCompanyID` - Primary key (full table name + ID)
- `EventID` - Foreign key to Event
- `CompanyID` - Foreign key to Company
- `EventCompanyRoleID` - Foreign key to ref.EventCompanyRole (event_owner, event_organizer, event_participant)
- `FormsCreated` - Usage metric
- `FirstUsedDate` - When company first used event
- `LastUsedDate` - When company last used event
- `IsActive` - Active participation flag
- `DisassociatedDate` - When company disassociated
- Standard audit columns

**Indexes:**
- `IX_EventCompany_Event` - For event lookup
- `IX_EventCompany_Company` - For company lookup
- `IX_EventCompany_EventCompanyRole` - For role-based queries
- `IX_EventCompany_Active` - For active relationships

---

### Event Table Updates

**Public Review Fields (Already Exist):**
- `IsPublicReviewRequired` - Review required flag
- `PublicReviewStatus` - Review status (PENDING, APPROVED, REJECTED)
- `PublicReviewDate` - When review completed
- `PublicReviewBy` - Admin who reviewed
- `PublicReviewComments` - Rejection reason/comments
- `PublicVisibilityDate` - When to make public (optional delayed visibility)

**Status Workflow:**
- `DRAFT` → Private event, not yet submitted
- `PENDING_REVIEW` → Public event submitted for review
- `PUBLISHED` → Public event approved and visible
- `REJECTED` → Public event rejected by admin
- `COMPLETED` → Event has finished
- `CANCELLED` → Event cancelled

---

## Summary

### Key Workflows

1. **Private Event Creation:**
   - Page 1: Minimal fields (Name, Date, Type)
   - Pages 2 & 3: Optional
   - No review required
   - Immediately available within company

2. **Public Event Creation:**
   - Page 1: Search first, then required fields
   - Create event → Status: PENDING_REVIEW
   - Admin reviews → APPROVED or REJECTED
   - If approved: Event becomes public

3. **Public Event Update:**
   - User updates approved public event
   - Status changes to PENDING_REVIEW (for update)
   - Admin reviews changes
   - If approved: Update goes live
   - If rejected: Revert to previous approved state

4. **Using Existing Public Event:**
   - User searches and selects existing event
   - EventCompany relationship created (participant role)
   - User can create forms for this event

### User Experience Principles

1. **Progressive Disclosure:** Start simple, reveal complexity as needed
   - Form opens with ONLY Private/Public question
   - Required fields appear only after selection
   - Optional fields remain hidden until needed

2. **Clear Status Indicators:** Users always know event status
   - Disabled buttons clearly indicate incomplete forms
   - Tooltips provide actionable feedback on what's missing
   - Real-time validation updates button state

3. **Helpful Guidance:** Clear messages about review process
   - Tooltips list incomplete fields in plain language
   - Error messages are specific and actionable
   - Help text appears contextually

4. **Company Context:** Users see events created by their company
   - Events filtered by company ownership
   - Clear indication of who created each event

5. **Review Transparency:** Users understand review requirements
   - Clear explanation of review process for public events
   - Status badges show review state
   - Admin feedback visible when events are rejected

6. **Accessibility:** Form is usable by all users
   - Keyboard navigation supported throughout
   - Screen readers announce form state and incomplete fields
   - Tooltips accessible via keyboard focus
   - ARIA labels for all interactive elements
   - Color is not the only indicator (disabled state has visual + text indicators)

---

**Last Updated:** January 15, 2025  
**Maintained By:** Dimitri 🔍 (Data Domain Architect) + Sally 🎨 (UX Expert)

