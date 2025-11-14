# Event Public Review Workflow - Complete Process Mapping

**Date:** 2025-01-XX  
**Story:** 2.6 - Admin Public Event Review Workflow  
**Purpose:** Define the complete event creation and public review workflow with proper field mappings and guards

**CRITICAL CLARIFICATIONS:**
1. **EventStatus is USER-CONTROLLED** - Admins do NOT change EventStatus during review
2. **PublicReviewStatus uses a REFERENCE TABLE** - Foreign key to `ref.PublicReviewStatus`
3. **Admin approval is a "human in the loop"** - Only prevents bad data, doesn't control event lifecycle
4. **Event visibility requires BOTH conditions:** `PublicReviewStatus = 'APPROVED'` AND `EventStatus = 'PUBLISHED'`

---

## Key Field Relationships

### 1. **IsPublic** (Boolean)
- **Purpose:** User's intent - "I want this event to be publicly visible"
- **Values:** `True` = Public, `False` = Private (company-only)
- **User Control:** User can set this during event creation/update

### 2. **PublicReviewStatusID** (Foreign Key → ref.PublicReviewStatus | NULL)
- **Purpose:** Admin review decision for public visibility (human-in-the-loop quality check)
- **Reference Table:** `ref.PublicReviewStatus`
- **Values:**
  - `NULL` = Not submitted for review OR private event
  - `PENDING` (StatusCode) = Awaiting admin review
  - `APPROVED` (StatusCode) = Admin approved - event can go public when user publishes it
  - `REJECTED` (StatusCode) = Admin rejected - event cannot be made public
- **Admin Control:** Only system admins can change this
- **Important:** This is a quality gate, NOT a lifecycle control

### 3. **EventStatusID** (Foreign Key → ref.EventStatus)
- **Purpose:** Event lifecycle status - **USER CONTROLLED**
- **Reference Table:** `ref.EventStatus`
- **Values:**
  - `DRAFT` = Event being created/edited (user's internal status)
  - `PUBLISHED` = Event is live and accepting forms (user has published it)
  - `COMPLETED` = Event has finished (user marks as completed)
  - `CANCELLED` = Event cancelled (user cancels the event)
  - `ARCHIVED` = Event archived (user archives it)
- **Control:** **USER CONTROLS THIS** - Users/Organizers set and change EventStatus
- **Admin Impact:** Admins do NOT change EventStatus during review
- **Visibility Rule:** Event is publicly visible only if `PublicReviewStatus = 'APPROVED'` AND `EventStatus = 'PUBLISHED'`

### 4. **IsPublicReviewRequired** (Boolean)
- **Purpose:** System flag indicating if review is required
- **Values:** `True` = Review required, `False` = Review not required
- **Default:** `True` (all public events require review)
- **Control:** System-controlled, should match `IsPublic` and `PublicReviewStatus` state

### 5. **IsSharedWithPlatform** (Boolean)
- **Purpose:** User's choice to share event with platform-wide search (beyond company network)
- **Values:** `True` = Share with platform (visible in public search), `False` = Company network only
- **Default:** `False` (company network only)
- **User Control:** User sets this when creating/updating public events
- **Impact:** `True` requires admin review, `False` does not require review
- **Visibility:** 
  - `IsPublic = True` AND `IsSharedWithPlatform = False` → Visible to company and linked organizations only
  - `IsPublic = True` AND `IsSharedWithPlatform = True` → Visible to company, linked organizations, AND platform-wide search

---

## State Mapping Table

| IsPublic | IsSharedWithPlatform | PublicReviewStatus | EventStatus | IsPublicReviewRequired | Platform-Wide Visible? | Description | Action |
|----------|---------------------|-------------------|-------------|----------------------|----------------------|-------------|--------|
| `False` | `False` | `NULL` | `DRAFT` | `False` | ❌ No | Private event (default) | ✅ Valid |
| `True` | `False` | `NULL` | Any | `False` | ❌ No | Public event, company network only (no review needed) | ✅ Valid |
| `True` | `True` | `NULL` | Any | `True` | ❌ No | **INVALID** - Platform-shared event without review status | ❌ Auto-set to PENDING |
| `True` | `True` | `PENDING` | `DRAFT` | `True` | ❌ No | Platform-shared event awaiting admin review (user has it in draft) | ✅ Valid |
| `True` | `True` | `PENDING` | `PUBLISHED` | `True` | ❌ No | Platform-shared event awaiting admin review (user published but not reviewed) | ✅ Valid |
| `True` | `True` | `APPROVED` | `DRAFT` | `True` | ❌ No | Admin approved, but user hasn't published yet | ✅ Valid |
| `True` | `True` | `APPROVED` | `PUBLISHED` | `True` | ✅ **YES** | Admin approved AND user published → **PLATFORM-WIDE VISIBLE** | ✅ Valid |
| `True` | `True` | `APPROVED` | `CANCELLED` | `True` | ❌ No | Event was approved but user cancelled it | ✅ Valid (notify stakeholders) |
| `True` | `True` | `REJECTED` | Any | `True` | ❌ No | Admin rejected - cannot share with platform | ✅ Valid (IsSharedWithPlatform should be False) |
| `False` | `True` | `PENDING` | Any | `True` | ❌ No | **INVALID** - Private event with platform sharing | ❌ Clear IsSharedWithPlatform |
| `False` | `True` | `APPROVED` | Any | `False` | ❌ No | **INVALID** - Private event approved for platform | ❌ Clear IsSharedWithPlatform |
| `False` | `False` | `PENDING` | Any | `True` | ❌ No | **INVALID** - Private event with review status | ❌ Clear PublicReviewStatus |
| `False` | `False` | `APPROVED` | Any | `False` | ❌ No | **INVALID** - Private event approved | ❌ Clear PublicReviewStatus |
| `False` | `False` | `REJECTED` | Any | `False` | ❌ No | **INVALID** - Private event rejected | ❌ Clear PublicReviewStatus |

**Key Rules:**
- **Platform-Wide Visible =** `IsPublic = True` AND `IsSharedWithPlatform = True` AND `PublicReviewStatus = 'APPROVED'` AND `EventStatus = 'PUBLISHED'`
- **Company Network Visible =** `IsPublic = True` (regardless of `IsSharedWithPlatform`)
- **EventStatus is USER-CONTROLLED** - Admins never change it
- **PublicReviewStatus is ADMIN-CONTROLLED** - Users never change it
- **IsSharedWithPlatform is USER-CONTROLLED** - User chooses whether to share with platform

---

## Event Creation Workflow

### Scenario 1: Create Private Event (IsPublic = False)
```
1. User creates event with IsPublic = False
2. System sets:
   - IsPublic = False
   - PublicReviewStatus = NULL
   - EventStatus = DRAFT
   - IsPublicReviewRequired = False
3. ✅ Event is ready for company use (private)
```

### Scenario 2: Create Public Event (IsPublic = True)
```
1. User creates event with IsPublic = True
2. User sets EventStatus (usually DRAFT initially, but user controls this)
3. User selects visibility option:
   - Option A: "Company Network Only" (IsSharedWithPlatform = False)
   - Option B: "Share with Platform" (IsSharedWithPlatform = True)
4. System sets:
   - IsPublic = True
   - IsSharedWithPlatform = User's choice ← USER CONTROLLED
   - If IsSharedWithPlatform = True:
     * PublicReviewStatusID = PENDING  ← AUTOMATIC (FK to ref.PublicReviewStatus)
     * IsPublicReviewRequired = True   ← AUTOMATIC
   - If IsSharedWithPlatform = False:
     * PublicReviewStatusID = NULL     ← No review needed
     * IsPublicReviewRequired = False  ← No review needed
   - EventStatusID = User's choice (DRAFT, PUBLISHED, etc.) ← USER CONTROLLED
5. ✅ Event visibility determined:
   - If IsSharedWithPlatform = True → Event is in admin review queue
   - If IsSharedWithPlatform = False → Event is visible to company network immediately
6. ⚠️ Platform-wide visibility (if IsSharedWithPlatform = True):
   - NOT yet visible until: PublicReviewStatus = APPROVED AND EventStatus = PUBLISHED
```

### Scenario 3: Change Private to Public (Update IsPublic: False → True)
```
1. User updates existing private event: IsPublic = True
2. User's EventStatus remains unchanged (user controls this)
3. System validates ADDITIONAL REQUIRED FIELDS for public events:
   - Name (required)
   - Description (required for public events)
   - StartDateTime (required)
   - EventTypeID (required)
   - City (recommended, warning if missing)
   - CountryID (recommended for physical/hybrid events)
   - VenueName or VenueAddress (recommended for physical/hybrid events)
4. If validation fails, show error: "Please complete required fields for public events"
5. System checks:
   - If PublicReviewStatusID is NULL
6. System sets:
   - IsPublic = True
   - PublicReviewStatusID = PENDING  ← AUTOMATIC (FK to ref.PublicReviewStatus)
   - EventStatusID = Unchanged ← USER CONTROLLED (not changed by system)
   - IsPublicReviewRequired = True   ← AUTOMATIC
7. ✅ Event is now in admin review queue
8. ⚠️ Event is NOT yet publicly visible until:
   - Admin approves (PublicReviewStatus = APPROVED)
   - AND User publishes (EventStatus = PUBLISHED)
   - AND User has enabled "Share with Platform" (if option exists)
```

### Scenario 4A: Change Public to Private (Update IsPublic: True → False)
```
1. User updates existing public event: IsPublic = False
2. User's EventStatus remains unchanged (user controls this)
3. System sets:
   - IsPublic = False
   - IsSharedWithPlatform = False    ← CLEAR (no longer sharing with platform)
   - PublicReviewStatusID = NULL     ← CLEAR (no longer needs review)
   - EventStatusID = Unchanged       ← USER CONTROLLED (not changed by system)
   - IsPublicReviewRequired = False  ← AUTOMATIC
4. ✅ Event is now private (removed from review queue)
5. Event is no longer visible to company network or platform (even if previously approved)
```

### Scenario 4B: Public Event Options (IsPublic = True, with visibility control)
```
1. User creates/updates event with IsPublic = True
2. User selects visibility option:
   - Option A: "Company Network Only" (IsSharedWithPlatform = False)
     * Visible to company and linked organizations
     * NO admin review required
     * NOT visible in platform-wide public search
     * Useful for events shared with partners/suppliers
   
   - Option B: "Share with Platform" (IsSharedWithPlatform = True)
     * Visible to company and linked organizations
     * AND visible in platform-wide public search
     * REQUIRES admin review (PublicReviewStatusID = PENDING)
     * Other companies can discover and link to event
3. System sets:
   - If IsSharedWithPlatform = True:
     * PublicReviewStatusID = PENDING (admin review required)
     * IsPublicReviewRequired = True
   - If IsSharedWithPlatform = False:
     * PublicReviewStatusID = NULL (no review needed)
     * IsPublicReviewRequired = False
4. ✅ Event visibility determined by user's choice
```

---

## Admin Review Workflow

### Scenario 5: Admin Approves Event (PublicReviewStatus: PENDING → APPROVED)
```
1. Admin reviews event in Admin Dashboard (only events with IsSharedWithPlatform = True)
2. Admin clicks "Approve" (with optional comment)
3. System validates:
   - Event has IsSharedWithPlatform = True (platform-sharing event)
   - Event has PublicReviewStatusID = PENDING
4. System sets:
   - PublicReviewStatusID = APPROVED ← FK to ref.PublicReviewStatus
   - PublicReviewDate = NOW()
   - PublicReviewBy = Admin UserID
   - PublicReviewComments = Admin comment (optional)
   - EventStatusID = UNCHANGED       ← USER CONTROLLED (admin does NOT change)
   - IsPublic = True                 ← KEEP (already True)
   - IsSharedWithPlatform = True     ← KEEP (already True, admin does NOT change)
   - PublicVisibilityDate = NOW() or specified date
5. ⚠️ Event is NOT yet platform-wide visible:
   - If EventStatus = DRAFT → Event is approved but user hasn't published yet
   - If EventStatus = PUBLISHED → Event is now platform-wide visible ✅
   - If EventStatus = CANCELLED → Event was cancelled by user (notify stakeholders)
5. Email sent to event creator with polite, explanatory messaging:
   - Subject: "Your event has been approved for public visibility"
   - Content: 
     * Thank them for submitting their event
     * Explain we have a quality check to ensure no offensive language or inappropriate content
     * Reference public event guidelines policy
     * If EventStatus = PUBLISHED: "Your event is now publicly visible"
     * If EventStatus = DRAFT: "Your event is approved. Publish it to make it public"
     * If EventStatus = CANCELLED: "Your event was approved but is currently cancelled"
   - Include link to view event and public event guidelines
```

### Scenario 6: Admin Rejects Event (PublicReviewStatus: PENDING → REJECTED)
```
1. Admin reviews event in Admin Dashboard (only events with IsSharedWithPlatform = True)
2. Admin clicks "Reject" (REQUIRED comment)
3. System validates:
   - Event has IsSharedWithPlatform = True (platform-sharing event)
   - Event has PublicReviewStatusID = PENDING
4. System sets:
   - PublicReviewStatusID = REJECTED ← FK to ref.PublicReviewStatus
   - PublicReviewDate = NOW()
   - PublicReviewBy = Admin UserID
   - PublicReviewComments = Admin feedback (REQUIRED)
   - EventStatusID = UNCHANGED        ← USER CONTROLLED (admin does NOT change)
   - IsPublic = True                  ← KEEP (still public for company network)
   - IsSharedWithPlatform = False     ← AUTOMATIC (disable platform sharing)
   - IsPublicReviewRequired = True    ← KEEP (still required if resubmitted)
5. ✅ Event is now company network only (not platform-wide visible, even if EventStatus = PUBLISHED)
6. Event creator can still use event for their company and linked organizations
6. Email sent to event creator with polite, explanatory messaging:
   - Subject: "Update on your event review"
   - Content:
     * Apologize that we can't make the event public on our platform
     * Explain reasons for rejection (from feedback)
     * Reassure that event is still available to them and linked organizations
     * Explain event will not be visible to others on platform until issues are addressed
     * Provide clear instructions for resubmission
     * Include link to public event guidelines policy
     * Include link to edit event and resubmit for review
   - Include resubmission button: "Address Feedback & Resubmit"
7. User can resubmit by:
   - Editing event to address feedback
   - Clicking "Resubmit for Review" button
   - System sets PublicReviewStatusID = PENDING again
```

### Scenario 7: Resubmit Rejected Event (PublicReviewStatus: REJECTED → PENDING)
```
1. User edits rejected event to address feedback
2. User sets IsSharedWithPlatform = True (enables platform sharing again)
3. User clicks "Resubmit for Review" button
4. System validates:
   - Event has PublicReviewStatusID = REJECTED
   - Event has IsSharedWithPlatform = True
   - Required fields are complete (Name, Description, StartDateTime, EventTypeID, etc.)
5. If validation fails, show error: "Please complete required fields and enable platform sharing"
6. System sets:
   - IsSharedWithPlatform = True     ← ENABLE platform sharing
   - PublicReviewStatusID = PENDING  ← Reset to pending
   - PublicReviewDate = NULL         ← Clear previous review date
   - PublicReviewBy = NULL           ← Clear previous reviewer
   - PublicReviewComments = NULL     ← Clear previous comments
   - IsPublic = True                 ← Ensure public
   - IsPublicReviewRequired = True   ← Review required again
7. ✅ Event is back in admin review queue
8. Email sent to admin: "Event resubmitted for review"
9. Admin reviews updated event and makes decision (approve/reject)
```

---

## Guards and Validation Rules

### Guard 1: Event Creation Guard
```python
# When creating event with IsPublic = True:
if is_public == True:
    # Check if user wants to share with platform
    if is_shared_with_platform == True:
        # REQUIRED: Set review status for platform-sharing events
        assert public_review_status_id == pending_review_status_id, \
            "Platform-sharing events must have PENDING review status"
        assert is_public_review_required == True, \
            "Platform-sharing events must require review"
    else:
        # Company network only - no review needed
        assert public_review_status_id is None, \
            "Company network only events should not have review status"
        assert is_public_review_required == False, \
            "Company network only events do not require review"
    # NOTE: EventStatusID is user-controlled, do NOT set it automatically
```

### Guard 2: IsPublic Update Guard
```python
# When updating IsPublic from False to True:
if was_public == False and new_is_public == True:
    # User must select platform sharing option
    if new_is_shared_with_platform == True:
        # Platform-sharing requires review
        pending_status = db.query(PublicReviewStatus).filter(
            PublicReviewStatus.StatusCode == 'PENDING'
        ).first()
        event.public_review_status_id = pending_status.PublicReviewStatusID
        event.is_public_review_required = True
        event.is_shared_with_platform = True
    else:
        # Company network only - no review needed
        event.public_review_status_id = None
        event.is_public_review_required = False
        event.is_shared_with_platform = False
    # NOTE: EventStatusID is user-controlled, do NOT change it
```

### Guard 3: PublicReviewStatus Update Guard
```python
# Only admins can update PublicReviewStatus
assert current_user.role == 'system_admin', "Only admins can review events"

# Can only review platform-sharing events
assert event.is_shared_with_platform == True, \
    "Can only review events that are shared with platform"

# Get status IDs from reference table
pending_status = db.query(PublicReviewStatus).filter(
    PublicReviewStatus.StatusCode == 'PENDING'
).first()
approved_status = db.query(PublicReviewStatus).filter(
    PublicReviewStatus.StatusCode == 'APPROVED'
).first()
rejected_status = db.query(PublicReviewStatus).filter(
    PublicReviewStatus.StatusCode == 'REJECTED'
).first()

# Can only approve/reject PENDING events
if new_status_id in [approved_status.PublicReviewStatusID, rejected_status.PublicReviewStatusID]:
    assert event.public_review_status_id == pending_status.PublicReviewStatusID, \
        "Can only approve/reject PENDING events"
    
    if new_status_id == approved_status.PublicReviewStatusID:
        # APPROVE: Set review status, but DO NOT change EventStatus or IsSharedWithPlatform
        event.public_review_status_id = approved_status.PublicReviewStatusID
        event.is_public = True  # Ensure public
        event.is_shared_with_platform = True  # Keep platform sharing enabled
        event.public_visibility_date = now() or specified_date
        # EventStatusID remains unchanged (user controls this)
    
    elif new_status_id == rejected_status.PublicReviewStatusID:
        # REJECT: Set review status, disable platform sharing, but DO NOT change EventStatus
        assert comment is not None, "Rejection requires comment"
        event.public_review_status_id = rejected_status.PublicReviewStatusID
        event.is_public = True  # Keep public (still visible to company network)
        event.is_shared_with_platform = False  # Disable platform sharing
        # EventStatusID remains unchanged (user controls this)
```

### Guard 4A: IsSharedWithPlatform Update Guard
```python
# When user changes IsSharedWithPlatform directly:
if was_shared_with_platform != new_is_shared_with_platform:
    if new_is_shared_with_platform == True:
        # User wants to enable platform sharing
        # Validate required fields for platform-sharing events
        assert event.description is not None, "Description required for platform-sharing events"
        assert event.name is not None and len(event.name.strip()) > 0, "Name required"
        assert event.start_datetime is not None, "StartDateTime required"
        assert event.event_type_id is not None, "EventTypeID required"
        
        # Set review status
        pending_status = db.query(PublicReviewStatus).filter(
            PublicReviewStatus.StatusCode == 'PENDING'
        ).first()
        event.public_review_status_id = pending_status.PublicReviewStatusID
        event.is_public_review_required = True
        event.is_shared_with_platform = True
    else:
        # User wants to disable platform sharing
        # Clear review status if pending
        pending_status = db.query(PublicReviewStatus).filter(
            PublicReviewStatus.StatusCode == 'PENDING'
        ).first()
        if event.public_review_status_id == pending_status.PublicReviewStatusID:
            event.public_review_status_id = None
        event.is_shared_with_platform = False
        event.is_public_review_required = False
        # Keep review history if approved/rejected (for audit trail)
```

### Guard 4B: EventStatus Update Guard
```python
# NOTE: EventStatus is user-controlled, but we can react to changes
# If EventStatus is set to ARCHIVED or CANCELLED, notify stakeholders if needed

archived_status = db.query(EventStatus).filter(
    EventStatus.StatusCode == 'ARCHIVED'
).first()
cancelled_status = db.query(EventStatus).filter(
    EventStatus.StatusCode == 'CANCELLED'
).first()

if new_event_status_id == archived_status.EventStatusID:
    # Archived events shouldn't be in review
    pending_status = db.query(PublicReviewStatus).filter(
        PublicReviewStatus.StatusCode == 'PENDING'
    ).first()
    if event.public_review_status_id == pending_status.PublicReviewStatusID:
        # Cancel review if archived while pending
        event.public_review_status_id = None
        event.is_shared_with_platform = False  # Disable platform sharing
        event.is_public_review_required = False
    else:
        # Keep review history but clear review requirement
        event.is_shared_with_platform = False  # Disable platform sharing
        event.is_public_review_required = False

elif new_event_status_id == cancelled_status.EventStatusID:
    # If event is cancelled and was approved for platform sharing, notify stakeholders
    approved_status = db.query(PublicReviewStatus).filter(
        PublicReviewStatus.StatusCode == 'APPROVED'
    ).first()
    if (event.public_review_status_id == approved_status.PublicReviewStatusID and 
        event.is_shared_with_platform == True):
        # Notify organizers/companies that attached to this event
        notify_event_cancelled(event)
```

### Guard 5: Data Integrity Guard (Database Constraint)
```sql
-- Check constraint to ensure consistency
ALTER TABLE [Event] ADD CONSTRAINT CK_Event_PublicReviewConsistency 
CHECK (
    -- If IsPublic = False, PublicReviewStatus should be NULL
    (IsPublic = 0 AND PublicReviewStatus IS NULL) OR
    -- If IsPublic = True, PublicReviewStatus must be set
    (IsPublic = 1 AND PublicReviewStatus IS NOT NULL) OR
    -- Allow transition states (user just changed IsPublic)
    (IsPublic = 1 AND PublicReviewStatus IN ('PENDING', 'APPROVED', 'REJECTED'))
);

-- If EventStatus = ARCHIVED, PublicReviewStatus should be NULL or historical
ALTER TABLE [Event] ADD CONSTRAINT CK_Event_ArchivedNoReview
CHECK (
    (EventStatusID != (SELECT EventStatusID FROM ref.EventStatus WHERE StatusCode = 'ARCHIVED')) OR
    (PublicReviewStatus IS NULL OR PublicReviewStatus != 'PENDING')
);
```

### Guard 6: Query Guard (Admin Dashboard)
```python
# Only show events in pending review that are actually pending
def get_pending_review_events():
    pending_status = db.query(PublicReviewStatus).filter(
        PublicReviewStatus.StatusCode == 'PENDING'
    ).first()
    archived_status = db.query(EventStatus).filter(
        EventStatus.StatusCode == 'ARCHIVED'
    ).first()
    
    return db.query(Event).filter(
        Event.IsPublic == True,                      # Must be public
        Event.IsSharedWithPlatform == True,          # Must be shared with platform
        Event.PublicReviewStatusID == pending_status.PublicReviewStatusID,  # Must be pending
        Event.IsDeleted == False,                    # Not deleted
        # EXCLUDE archived events (user archived it)
        Event.EventStatusID != archived_status.EventStatusID
    ).all()
```

### Guard 7: Platform-Wide Visibility Query Guard
```python
# Only show events that are actually visible in platform-wide search
def get_platform_wide_visible_events():
    approved_status = db.query(PublicReviewStatus).filter(
        PublicReviewStatus.StatusCode == 'APPROVED'
    ).first()
    published_status = db.query(EventStatus).filter(
        EventStatus.StatusCode == 'PUBLISHED'
    ).first()
    
    return db.query(Event).filter(
        Event.IsPublic == True,                          # Must be public
        Event.IsSharedWithPlatform == True,              # Must be shared with platform
        Event.PublicReviewStatusID == approved_status.PublicReviewStatusID,  # Must be approved
        Event.EventStatusID == published_status.EventStatusID,  # Must be published
        Event.IsDeleted == False                        # Not deleted
    ).all()

### Guard 8: Company Network Visibility Query Guard
```python
# Show events visible to company network (company and linked organizations)
def get_company_network_visible_events(company_id: int):
    return db.query(Event).filter(
        Event.IsPublic == True,                          # Must be public
        Event.IsDeleted == False,                        # Not deleted
        # Additional filters for company network visibility
        # (Event.CompanyID == company_id OR linked via EventCompany)
    ).all()
```

---

## Current Issues and Fixes

### Issue 1: Events with IsPublicReviewRequired = True but wrong status
**Problem:**
- 2 events with `IsPublicReviewRequired = True` and `EventStatus = ARCHIVED`
- 1 event with `IsPublicReviewRequired = True` and `EventStatus = APPROVED`

**Root Cause:**
- Events were archived or approved without clearing `IsPublicReviewRequired`
- No guards to prevent this inconsistency

**Fix:**
1. Run data cleanup script to fix existing records
2. Add Guards 4 and 5 above to prevent future issues
3. Update `update_event()` service to enforce guards

### Issue 2: Events with IsPublic = True but PublicReviewStatus = NULL
**Problem:**
- Events exist with `IsPublic = True` but `PublicReviewStatus = NULL`
- These don't show up in admin review queue

**Root Cause:**
- Events created before review workflow was implemented
- No automatic guard during creation/update

**Fix:**
1. Run data migration script: `fix-existing-public-events-review-status.sql`
2. Add Guards 1 and 2 to prevent future issues
3. Update `create_event()` and `update_event()` services

---

## Implementation Checklist

- [ ] **Guard 1:** Add validation in `create_event()` - enforce PENDING status for public events
- [ ] **Guard 2:** Add auto-set logic in `update_event()` - set PENDING when IsPublic changes to True
- [ ] **Guard 3:** Add validation in `approve_event()` / `reject_event()` - enforce workflow rules
- [ ] **Guard 4:** Add logic to clear review status when EventStatus = ARCHIVED
- [ ] **Guard 5:** Add database constraints for data integrity
- [ ] **Guard 6:** Update admin review queries to exclude archived events
- [ ] **Data Cleanup:** Run migration script to fix existing inconsistent records
- [ ] **Testing:** Test all workflow scenarios to ensure guards work correctly

---

## Summary

**Key Principles:** 
1. **EventStatus is USER-CONTROLLED** - Users/organizers control event lifecycle (DRAFT, PUBLISHED, CANCELLED, etc.)
2. **IsSharedWithPlatform is USER-CONTROLLED** - Users choose whether to share event with platform-wide search
3. **PublicReviewStatus is ADMIN-CONTROLLED** - Admins control review decisions (PENDING, APPROVED, REJECTED) for platform-sharing events
4. **PublicReviewStatus uses REFERENCE TABLE** - Foreign key to `ref.PublicReviewStatus` (not NVARCHAR)
5. **Admin approval is a quality gate** - Prevents bad data, does NOT control event lifecycle
6. **Platform-wide visibility requires ALL conditions:**
   - `IsPublic = True` (user wants event public)
   - AND `IsSharedWithPlatform = True` (user wants platform-wide visibility)
   - AND `PublicReviewStatus = 'APPROVED'` (admin approved)
   - AND `EventStatus = 'PUBLISHED'` (user published)
7. **Company network visibility requires:**
   - `IsPublic = True` (regardless of `IsSharedWithPlatform`)
8. **Event cancellation notification** - If approved platform-sharing event is cancelled, notify stakeholders
9. **Platform-sharing events require additional fields** - Description, City, etc. for better discovery
10. **Resubmission workflow** - Rejected events can be edited and resubmitted for review (must re-enable `IsSharedWithPlatform`)
11. **Company network only option** - Users can set event as public but NOT share with platform (visible to company and linked organizations only, no review needed)

**Critical Guards:**
1. Platform-sharing events (`IsSharedWithPlatform = True`) MUST have `PublicReviewStatusID = PENDING` on creation
2. Company network only events (`IsSharedWithPlatform = False`) do NOT require review
3. Only `PENDING` events can be approved/rejected
4. Only platform-sharing events (`IsSharedWithPlatform = True`) can be reviewed
5. Admins NEVER change `EventStatusID` or `IsSharedWithPlatform` during review
6. Rejected events have `IsSharedWithPlatform = False` (cannot be platform-shared)
7. Archived/Cancelled events should NOT be in review queue
8. Platform-wide visibility query checks: `IsPublic = True` AND `IsSharedWithPlatform = True` AND `PublicReviewStatus = APPROVED` AND `EventStatus = PUBLISHED`
