# Story 2.7 UX Review - Event Public Review Workflow Implementation

**Reviewer:** Sally 🎨 (UX Expert)  
**Date:** January 31, 2025  
**Story:** 2.7 - Event Public Review Workflow Implementation  
**Status:** ✅ Complete - Recommendations Provided

---

## Executive Summary

After reviewing Story 2.7 and the complete workflow mapping, I've identified **critical UX improvements** needed to ensure users understand and navigate the event public review workflow effectively. The story is primarily backend-focused, but **Task 13 (Frontend API Integration Updates)** needs significant UX enhancements to create a user-friendly experience.

### Key UX Concerns:
1. **Neutral Wording** - Use non-judgmental language ("Is this event open to the public?" not "Visible to others on the platform")
2. **Progressive Disclosure** - Multi-step flow to reduce cognitive load and avoid making users feel judged
3. **Platform Searchability Question** - Only ask about platform searchability if user skipped search (less intimidating)
4. **Review Status Communication** - Event creators need clear, actionable feedback on review status
5. **Validation Feedback** - Clear, helpful error messages for required fields
6. **User Guidance** - Contextual help explaining the review process
7. **State Transition Feedback** - Clear communication when visibility settings change

---

## UX Improvement Recommendations

### 1. Event Creation Workflow - Progressive Disclosure Pattern

**Current State:** Form launches → Public/Private selection → Full form appears immediately (no progressive disclosure)

**UX Recommendation - Multi-Step Progressive Disclosure:**

#### **Step 1: Event Type Selection (Intent Only - Neutral Wording)**
- **Show ONLY:** Public/Private radio buttons
- **Purpose:** Gather user intent - neutral, non-judgmental question
- **Important:** Use neutral wording to avoid making users feel judged
- **Wording:** "Is this event open to the public?" (not "Visible to others on the platform")
- **No visibility statements:** Remove visibility implications to reduce friction
- **Design:**
  ```
  ┌─────────────────────────────────────────────────┐
  │ Create Event                                     │
  ├─────────────────────────────────────────────────┤
  │                                                   │
  │  Is this event open to the public?                │
  │                                                   │
  │  (○) No, this is a private event                  │
  │                                                   │
  │  (●) Yes, this event is open to the public        │
  │                                                   │
  │  [Cancel]  [Continue]                              │
  └─────────────────────────────────────────────────┘
  ```

#### **Step 2A: If Private Selected → Show Full Form**
- **Immediate:** Show full event creation form
- **Set:** IsPublic = False (private event)
- **No search needed:** Private events don't need reference search
- **No platform sharing options:** Not applicable for private events
- **Proceed directly to:** Essential Information tab

#### **Step 2B: If Public Selected → Show Search/Skip Options**
- **Show TWO options:**
  1. **"Search for Existing Events"** button (primary action)
  2. **"Skip & Create New Event"** button (secondary action)
- **Purpose:** Help users find reference events before creating
- **Design:**
  ```
  ┌─────────────────────────────────────────────────┐
  │ Create Event                                     │
  ├─────────────────────────────────────────────────┤
  │                                                   │
  │  Event Type: Public Event                         │
  │                                                   │
  │  Would you like to search for existing public    │
  │  events to use as a reference?                   │
  │                                                   │
  │  ℹ️ Searching helps you find similar events      │
  │     and pre-fills the form with reference info.  │
  │                                                   │
  │  ┌─────────────────────────────────────────────┐ │
  │  │ [🔍 Search for Existing Events]              │ │
  │  └─────────────────────────────────────────────┘ │
  │                                                   │
  │  ┌─────────────────────────────────────────────┐ │
  │  │ [Skip & Create New Event]                    │ │
  │  └─────────────────────────────────────────────┘ │
  │                                                   │
  │  [← Back]                                         │
  └─────────────────────────────────────────────────┘
  ```

#### **Step 3A: If "Search for Existing Events" Selected**
- **Show:** Search interface with event list
- **Allow:** Select event to pre-fill form
- **After selection:** Show full form with pre-filled data
- **Design:**
  ```
  ┌─────────────────────────────────────────────────┐
  │ Create Event                                     │
  ├─────────────────────────────────────────────────┤
  │                                                   │
  │  Search for Existing Public Events                │
  │                                                   │
  │  [Search by event name...]  [🔍]                 │
  │                                                   │
  │  ┌─────────────────────────────────────────────┐ │
  │  │ Tech Summit 2025                            │ │
  │  │ Jan 15-17, 2025 | Sydney, Australia         │ │
  │  │ [Select]                                     │ │
  │  ├─────────────────────────────────────────────┤ │
  │  │ Innovation Conference 2024                  │ │
  │  │ Mar 20-22, 2024 | Melbourne, Australia     │ │
  │  │ [Select]                                     │ │
  │  └─────────────────────────────────────────────┘ │
  │                                                   │
  │  [← Back]  [Skip & Create New]                   │
  └─────────────────────────────────────────────────┘
  ```

#### **Step 3B: If "Skip & Create New Event" Selected → Show Platform Searchability Question**
- **Show:** Platform searchability question (ONLY if they skipped search)
- **Purpose:** Ask if they want to make event searchable on platform (less intimidating than "visible to others")
- **Design:**
  ```
  ┌─────────────────────────────────────────────────┐
  │ Create Event                                     │
  ├─────────────────────────────────────────────────┤
  │                                                   │
  │  Would you like to make this event searchable    │
  │  on the platform for others also creating forms  │
  │  for the same event?                              │
  │                                                   │
  │  ℹ️ Making your event searchable helps other     │
  │     companies discover and link to your event    │
  │     when creating forms. This requires admin     │
  │     review for quality assurance.                 │
  │                                                   │
  │  (○) No, keep it within my company network       │
  │      Visible to your company and attached        │
  │      companies only. No review required.          │
  │                                                   │
  │  (●) Yes, make it searchable on the platform      │
  │      Others can discover and link to this event. │
  │      Requires admin review.                      │
  │                                                   │
  │  [← Back]  [Continue]                              │
  └─────────────────────────────────────────────────┘
  ```
- **If "No, keep it within my company network" selected:**
  - IsPublic = True, IsSharedWithPlatform = False (company network only)
  - Proceed to full form
  
- **If "Yes, make it searchable on the platform" selected:**
  - IsPublic = True, IsSharedWithPlatform = True (platform-wide search)
  - PublicReviewStatusID = PENDING (requires admin review)
  - Proceed to full form with review status indicator

#### **Step 4: Full Form Display (After Platform Searchability Question)**
- **Show:** Full event creation form
- **Reduce search to:** Compact "Search Event" button next to event type indicator
- **Purpose:** Allow users to search later if needed, but don't block form entry
- **Design:**
  ```
  ┌─────────────────────────────────────────────────┐
  │ Create Event                                     │
  ├─────────────────────────────────────────────────┤
  │                                                   │
  │  Event Type: Public Event  [🔍 Search Event]     │
  │                                                   │
  │  ─────────────────────────────────────────────   │
  │                                                   │
  │  Tab 1: Essentials                                │
  │  Tab 2: Enhanced Details                          │
  │  Tab 3: Advanced                                  │
  │                                                   │
  │  [Full form fields here...]                       │
  │                                                   │
  └─────────────────────────────────────────────────┘
  ```

#### **Step 5: Platform Sharing Selection (Within Full Form - If Public Selected)**
- **Show:** Visibility options within the form
- **Options:**
  - 🌐 "Company Network Only" (IsSharedWithPlatform = False)
  - 🌍 "Share with Platform" (IsSharedWithPlatform = True)
- **Progressive Disclosure:**
  - Show platform sharing options ONLY when Public is selected
  - When "Share with Platform" selected → Show review status indicator
- **Help Text:**
  - Tooltip or info icon explaining each option
  - Link to Public Event Guidelines policy

---

### 2. Event Update Workflow - State Transition Feedback

**Current Gap:** No UX guidance for how to communicate visibility changes and their implications.

**UX Recommendations:**

#### **When Changing Private → Public:**
- **Confirmation Dialog:**
  ```
  "Make this event public?"
  
  Your event will be visible to:
  • Your company
  • Linked organizations
  
  Choose visibility option:
  [ ] Company Network Only (no review needed)
  [ ] Share with Platform (requires admin review)
  
  [Cancel] [Continue]
  ```
- **After Selection:**
  - If "Company Network Only" → Show success: "Event is now public to your network"
  - If "Share with Platform" → Show info banner: "Event submitted for review. You'll receive an email when reviewed."

#### **When Changing Public → Private:**
- **Warning Dialog:**
  ```
  "Make this event private?"
  
  This will:
  • Remove event from public visibility
  • Cancel any pending reviews
  • Keep event visible only to your company
  
  [Cancel] [Make Private]
  ```

#### **When Enabling Platform Sharing:**
- **Validation Check:**
  - If required fields missing → Show inline validation errors
  - If validation passes → Show info banner: "Event submitted for admin review"
- **Required Fields Indicator:**
  - Show warning icon next to missing fields
  - Tooltip: "Required for platform-sharing events"

---

### 3. Review Status Display - Event Creator View

**Current Gap:** Task 13 mentions "Update event display components to show review status from `PublicReviewStatusID` relationship" but doesn't specify HOW.

**UX Recommendations:**

#### **Review Status Badge Component:**
- **Pending Status:**
  ```
  ⏳ Pending Review
  Your event is awaiting admin review. You'll receive an email when reviewed.
  [View Guidelines]
  ```
- **Approved Status:**
  ```
  ✅ Approved
  Your event has been approved! Publish it to make it publicly visible.
  [Publish Event]
  ```
- **Rejected Status:**
  ```
  ❌ Rejected
  Your event was not approved for platform-wide visibility. Review feedback below.
  [View Feedback] [Edit & Resubmit]
  ```

#### **Review Status Panel:**
- **Location:** Event detail page, below event title
- **Content:**
  - Status badge (color-coded: yellow for pending, green for approved, red for rejected)
  - Review date and admin name (if reviewed)
  - Review comments (if rejected)
  - Action buttons (Resubmit, View Guidelines, etc.)

#### **Review Feedback Display (Rejected Events):**
- **Collapsible Panel:**
  ```
  ┌─────────────────────────────────────────┐
  │ Review Feedback                          │
  │ Reviewed by: Admin Name on [Date]       │
  ├─────────────────────────────────────────┤
  │ [Feedback comments here]                │
  │                                         │
  │ [Address Feedback & Resubmit]           │
  └─────────────────────────────────────────┘
  ```

---

### 4. Validation Feedback - Required Fields for Platform-Sharing

**Current Gap:** Task 3 mentions "Validate required fields for platform-sharing events" but doesn't specify UX for validation feedback.

**UX Recommendations:**

#### **Inline Validation:**
- **Missing Required Fields:**
  - Show red border and error icon next to field
  - Error message: "This field is required for platform-sharing events"
  - Show "Required for Platform Sharing" badge

#### **Bulk Validation (Before Enabling Platform Sharing):**
- **Validation Check Panel:**
  ```
  ┌─────────────────────────────────────────┐
  │ ⚠️ Complete these fields to share with   │
  │    platform:                            │
  ├─────────────────────────────────────────┤
  │ ✓ Event Name                            │
  │ ✗ Description (required)                │
  │ ✗ Start Date (required)                 │
  │ ✓ Event Type                            │
  │ ⚠ City (recommended)                    │
  │                                         │
  │ [Complete Fields] [Cancel]              │
  └─────────────────────────────────────────┘
  ```

#### **Warning Messages:**
- **Recommended Fields Missing:**
  - Yellow warning icon: "City is recommended for better event discovery"
  - Not blocking, but informative

---

### 5. User Guidance and Help Text

**UX Recommendations:**

#### **Contextual Help Text:**
- **Event Visibility Section:**
  - Info icon with tooltip explaining each option
  - Link to Public Event Guidelines policy
  - FAQ: "What's the difference between Company Network and Platform?"

#### **Review Process Explanation:**
- **Info Banner (when submitting for review):**
  ```
  ℹ️ Review Process
  Your event will be reviewed by our team within 24-48 hours. 
  We check for content quality, completeness, and compliance 
  with our guidelines. You'll receive an email when reviewed.
  
  [View Guidelines] [Learn More]
  ```

#### **Tooltips:**
- **IsSharedWithPlatform Toggle:**
  - "Enable platform-wide visibility. Requires admin review before going public."
- **PublicReviewStatus Badge:**
  - Pending: "Your event is awaiting admin review. Typically reviewed within 24-48 hours."
  - Approved: "Your event has been approved! Publish it to make it publicly visible."
  - Rejected: "Your event was not approved. Review feedback and resubmit if needed."

---

### 6. Progressive Disclosure Patterns

**UX Recommendations - Multi-Step Flow:**

#### **Step-by-Step Progressive Disclosure:**

**Step 1: Initial Launch (Intent Only - Neutral Wording)**
- Show ONLY: Public/Private radio buttons
- Hide: All form fields, search, tabs
- Purpose: Gather user intent - neutral, non-judgmental question
- Wording: "Is this event open to the public?" (not "Visible to others on the platform")
- No visibility statements: Remove visibility implications below options to reduce friction
- Important: This is just intent gathering, no judgment implied, no consequences yet

**Step 2A: Private Selected**
- Show: Full event creation form immediately
- Set: IsPublic = False (private event)
- Hide: Search functionality (not needed for private events)
- Hide: Platform sharing options (not applicable)
- Proceed: Directly to Essential Information tab

**Step 2B: Public Selected → Show Search/Skip Options**
- Show: Search/Skip options (don't show full form yet)
- Hide: Full form fields
- Purpose: Guide users to search for reference events first

**Step 3A: Search Selected**
- Show: Search interface with event list
- Allow: Select event to pre-fill form
- After selection: Show full form with pre-filled data
- Hide: Search/Skip options (user made choice)
- **Important:** If they select an existing event, skip platform searchability question (they're using reference)

**Step 3B: Skip Selected → Show Platform Searchability Question**
- Show: Platform searchability question (ONLY if they skipped search)
- Ask: "Would you like to make this event searchable on the platform for others also creating forms for the same event?"
- Purpose: Less intimidating wording than "visible to others"
- Options:
  - "No, keep it within my company network" → IsPublic = True, IsSharedWithPlatform = False
  - "Yes, make it searchable on the platform" → IsPublic = True, IsSharedWithPlatform = True, PublicReviewStatusID = PENDING
- After selection: Show full form with appropriate settings

**Step 4: Full Form Display**
- Show: Full event creation form
- Reduce search: Compact "Search Event" button next to event type indicator
- Show: Platform sharing status (if already set in Step 3B)
- Show: Review status indicator (if IsSharedWithPlatform = True)
- Show: "Required for Platform Sharing" field indicators (if IsSharedWithPlatform = True)
- Show: Review process info banner (if IsSharedWithPlatform = True)

#### **Review Status Panel:**
- **Show only when:**
  - IsSharedWithPlatform = True OR
  - PublicReviewStatusID is not NULL (has been reviewed)
- **Hide when:**
  - Private event (IsPublic = False)
  - Company network only (IsSharedWithPlatform = False, no review history)

#### **Form Field Progressive Disclosure:**
- **Private Event (IsPublic = False):**
  - Hide all review-related fields
  - Hide platform sharing option
  - Hide search functionality
  
- **Company Network Only (IsPublic = True, IsSharedWithPlatform = False):**
  - Show "Company Network Only" indicator
  - Hide review status (no review needed)
  - Show "Search Event" button (compact, next to Public radio)
  
- **Share with Platform (IsPublic = True, IsSharedWithPlatform = True):**
  - Show review status badge
  - Show "Required for Platform Sharing" field indicators
  - Show review process info banner
  - Show "Review Guidelines" link
  - Show "Search Event" button (compact, next to Public radio)

---

### 7. Error Message Improvements

**UX Recommendations:**

#### **State Transition Errors:**
- **Cannot Enable Platform Sharing (Missing Fields):**
  ```
  ⚠️ Cannot enable platform sharing
  
  Complete these required fields first:
  • Description
  • Start Date
  • Event Type
  
  [Complete Fields]
  ```

#### **Invalid State Errors:**
- **Cannot Change Status (Event Archived):**
  ```
  ⚠️ Cannot change visibility
  
  This event is archived and cannot be made public.
  Unarchive the event first to change visibility.
  ```

#### **Validation Errors:**
- **Clear, Actionable Messages:**
  - "Description is required for platform-sharing events"
  - "Start date is required for public events"
  - "Event type is required for platform-wide visibility"

---

### 8. Accessibility Considerations

**UX Recommendations:**

#### **Keyboard Navigation:**
- **Radio Button Group:**
  - Use native radio buttons (not custom)
  - Ensure proper tab order
  - Support arrow keys for selection

#### **Screen Reader Support:**
- **ARIA Labels:**
  - `aria-label="Event visibility options"`
  - `aria-describedby="visibility-help-text"`
  - `aria-live="polite"` for review status updates

#### **Focus Management:**
- **Modal Dialogs:**
  - Trap focus within modal
  - Return focus to trigger element on close
  - Focus on first interactive element when opened

#### **Color Contrast:**
- **Review Status Badges:**
  - Pending: Yellow background (#FFC107) with dark text
  - Approved: Green background (#28A745) with white text
  - Rejected: Red background (#DC3545) with white text
  - Ensure WCAG AA contrast ratios (4.5:1 for text)

#### **Visual Indicators:**
- **Don't rely on color alone:**
  - Use icons + color + text for status badges
  - Include text labels for all statuses

---

## Updated Story Tasks - UX Enhancements

### **Task 13: Frontend API Integration Updates** (Enhanced with UX)

**Additional UX Subtasks:**
- [ ] Create `EventVisibilitySelector` component with radio button group
- [ ] Create `ReviewStatusBadge` component with color-coded status display
- [ ] Create `ReviewFeedbackPanel` component for rejected events
- [ ] Create `ReviewProcessInfoBanner` component with help text
- [ ] Implement progressive disclosure for review-related fields
- [ ] Add contextual help tooltips for visibility options
- [ ] Implement inline validation for required fields
- [ ] Create confirmation dialogs for visibility changes
- [ ] Add accessibility attributes (ARIA labels, keyboard navigation)
- [ ] Test with screen readers (NVDA, JAWS, VoiceOver)

### **New Task 15: UX Components and User Guidance** (New)

- [ ] Implement multi-step progressive disclosure flow
  - [ ] Step 1: Initial visibility selection screen (Public/Private only)
  - [ ] Step 2A: Private selected → Show full form immediately
  - [ ] Step 2B: Public selected → Show Search/Skip options screen
  - [ ] Step 3A: Search selected → Show search interface with event list
  - [ ] Step 3B: Skip selected → Show full form with compact search button
  - [ ] Navigation: Back button to return to previous step
  - [ ] State management: Track current step and user selections

- [ ] Create `EventVisibilitySelector` component
  - Radio button group for visibility options (Public/Private)
  - Compact "Search Event" button next to Public radio (when in form)
  - Progressive disclosure based on selection
  - Help text and tooltips
  - Link to Public Event Guidelines
  
- [ ] Create `EventSearchStep` component
  - Search/Skip options screen (Step 2B)
  - "Search for Existing Events" button (primary)
  - "Skip & Create New Event" button (secondary)
  - Help text explaining search benefits
  - Back button to return to Step 1
  
- [ ] Create `CompactEventSearchButton` component
  - Compact button next to "Public" radio button
  - Opens search modal/panel when clicked
  - Only shown when user skipped search in Step 2B
  
- [ ] Create `ReviewStatusBadge` component
  - Color-coded status badges (Pending, Approved, Rejected)
  - Icons + text labels
  - Action buttons (Resubmit, View Guidelines)
  - Accessibility attributes
  
- [ ] Create `ReviewFeedbackPanel` component
  - Display review feedback for rejected events
  - Show admin name and review date
  - "Address Feedback & Resubmit" button
  - Collapsible panel
  
- [ ] Create `ReviewProcessInfoBanner` component
  - Explain review process
  - Show expected review time (24-48 hours)
  - Link to guidelines
  - Dismissible
  
- [ ] Create validation feedback components
  - Inline field validation
  - Bulk validation panel
  - Required field indicators
  - Warning messages for recommended fields
  
- [ ] Create confirmation dialogs
  - Private → Public confirmation
  - Public → Private warning
  - Platform sharing enable confirmation
  
- [ ] Add user guidance content
  - Help text for visibility options
  - Review process explanation
  - FAQ entries
  - Link to Public Event Guidelines policy

---

## User Interface Mockups / Descriptions

### Mockup 1: Event Creation Form - Step 1 (Initial State - Neutral Wording)

```
┌─────────────────────────────────────────────────────────┐
│ Create Event                                    [×]       │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Is this event open to the public?                        │
│                                                           │
│  (○) No, this is a private event                          │
│                                                           │
│  (●) Yes, this event is open to the public                │
│                                                           │
│  [Cancel]  [Continue]                                     │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

**Note:** No visibility statements in Step 1 to reduce friction. Visibility control happens later in Step 3B (platform searchability question).

### Mockup 1B: Event Creation Form - Step 2B (Public Selected - Search/Skip)

```
┌─────────────────────────────────────────────────────────┐
│ Create Event                                    [×]       │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Event Type: Public Event                                 │
│                                                           │
│  Would you like to search for existing public events      │
│  to use as a reference?                                   │
│                                                           │
│  ℹ️ Searching helps you find similar events and          │
│     pre-fills the form with reference information.        │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ [🔍 Search for Existing Events]                      │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ [Skip & Create New Event]                            │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  [← Back]                                                 │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### Mockup 1C: Event Creation Form - Step 3B (Skip Selected - Platform Searchability Question)

```
┌─────────────────────────────────────────────────────────┐
│ Create Event                                    [×]       │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Would you like to make this event searchable on the      │
│  platform for others also creating forms for the same    │
│  event?                                                   │
│                                                           │
│  ℹ️ Making your event searchable helps other companies    │
│     discover and link to your event when creating forms.  │
│     This requires admin review for quality assurance.      │
│                                                           │
│  (○) No, keep it within my company network                │
│      Visible to your company and attached                 │
│      companies only. No review required.                  │
│                                                           │
│  (●) Yes, make it searchable on the platform              │
│      Others can discover and link to this event.          │
│      Requires admin review.                               │
│                                                           │
│  [← Back]  [Continue]                                     │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

**Note:** This question is ONLY shown if user skipped search. If they selected an existing event from search, skip this question and proceed directly to full form.

### Mockup 1D: Event Creation Form - Step 3A (Search Selected - Search Interface)

```
┌─────────────────────────────────────────────────────────┐
│ Create Event                                    [×]       │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Search for Existing Public Events                       │
│                                                           │
│  [Search by event name...]  [🔍]                         │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ Tech Summit 2025                                    │ │
│  │ Jan 15-17, 2025 | Sydney, Australia                 │ │
│  │ [Select]                                             │ │
│  ├─────────────────────────────────────────────────────┤ │
│  │ Innovation Conference 2024                          │ │
│  │ Mar 20-22, 2024 | Melbourne, Australia             │ │
│  │ [Select]                                             │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  [← Back]  [Skip & Create New]                            │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### Mockup 1E: Event Creation Form - Step 4 (Full Form Display)

```
┌─────────────────────────────────────────────────────────┐
│ Create Event                                    [×]       │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Event Type: Public Event  [🔍 Search Event]              │
│                                                           │
│  ─────────────────────────────────────────────           │
│                                                           │
│  Tab 1: Essentials  |  Tab 2: Enhanced  |  Tab 3: Adv. │
│                                                           │
│  ⏳ Status: Pending Review (if platform searchable)       │
│                                                           │
│  [Full form fields here...]                               │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### Mockup 2: Event Detail Page - Review Status Panel

```
┌─────────────────────────────────────────────────────────┐
│ Event: Tech Summit 2026                                   │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ ⏳ Pending Review                                    │ │
│  │ Your event is awaiting admin review. You'll receive │ │
│  │ an email when reviewed.                             │ │
│  │                                                      │ │
│  │ [View Guidelines]                                    │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  Event Details:                                           │
│  ...                                                      │
└─────────────────────────────────────────────────────────┘
```

### Mockup 3: Rejected Event - Review Feedback Panel

```
┌─────────────────────────────────────────────────────────┐
│ Event: Tech Summit 2026                                   │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ ❌ Rejected                                          │ │
│  │ Reviewed by: Admin Name on Jan 30, 2025            │ │
│  ├─────────────────────────────────────────────────────┤ │
│  │ Review Feedback:                                     │ │
│  │                                                      │ │
│  │ The event description is too brief and doesn't      │ │
│  │ provide enough detail about the event content.      │ │
│  │ Please add more information about sessions,          │ │
│  │ speakers, or agenda items.                          │ │
│  │                                                      │ │
│  │ [Address Feedback & Resubmit]                      │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  Event Details:                                           │
│  ...                                                      │
└─────────────────────────────────────────────────────────┘
```

---

## User Guidance Text Suggestions

### Visibility Options Help Text

**Private Event:**
> "Only visible to your company. No review required. Perfect for internal events."

**Company Network Only:**
> "Visible to your company and linked organizations. No review required. Great for events shared with partners or suppliers."

**Share with Platform:**
> "Visible in platform-wide search. Requires admin review (typically 24-48 hours) before going public. Other companies can discover and link to your event."

### Review Process Explanation

**Info Banner:**
> "Your event will be reviewed by our team within 24-48 hours. We check for content quality, completeness, and compliance with our guidelines. You'll receive an email notification when reviewed."

### Review Status Messages

**Pending:**
> "Your event is awaiting admin review. Typically reviewed within 24-48 hours. You'll receive an email when reviewed."

**Approved:**
> "Your event has been approved! Publish it to make it publicly visible in platform-wide search."

**Rejected:**
> "Your event was not approved for platform-wide visibility. Review feedback below and resubmit after addressing the issues."

---

## Accessibility Checklist

- [ ] All interactive elements keyboard accessible
- [ ] Radio buttons use native HTML elements
- [ ] ARIA labels added to all form controls
- [ ] ARIA describedby for help text
- [ ] ARIA live regions for status updates
- [ ] Focus traps in modal dialogs
- [ ] Color contrast meets WCAG AA (4.5:1)
- [ ] Status indicators use icons + text (not color alone)
- [ ] Screen reader tested (NVDA, JAWS, VoiceOver)
- [ ] Keyboard navigation tested (Tab, Arrow keys, Enter, Escape)

---

## Summary

Story 2.7 needs **significant UX enhancements** to Task 13 (Frontend API Integration Updates) and a **new Task 15 (UX Components and User Guidance)** to ensure users understand and navigate the event public review workflow effectively.

**Key Deliverables:**
1. ✅ UX review document with recommendations (this document)
2. ✅ Updated story tasks with UX enhancements
3. ✅ User interface mockups/descriptions
4. ✅ User guidance text suggestions

**Next Steps:**
1. Update Story 2.7 with enhanced Task 13 and new Task 15
2. Create UX component specifications
3. Implement components during frontend development
4. Test with users for feedback

---

**Review Completed:** ✅  
**Recommendations Provided:** ✅  
**Ready for Implementation:** ✅

---

*UX Review by Sally 🎨 (UX Expert)*  
*Date: January 31, 2025*

