# Event Review Workflow - Critical Corrections

**Date:** 2025-01-XX  
**Story:** 2.6 - Admin Public Event Review Workflow  
**Status:** ✅ Documentation Updated

---

## Critical Corrections Made

### 1. **PublicReviewStatus → Reference Table**
- **Before:** `PublicReviewStatus` was `NVARCHAR(20)` with check constraint
- **After:** `PublicReviewStatusID` as foreign key to `ref.PublicReviewStatus` table
- **Files Created:**
  - `database/schemas/public-review-status-ref-table.sql` - Creates reference table
  - `database/migrations/change-public-review-status-to-fk.sql` - Migration script

### 2. **EventStatus is USER-CONTROLLED**
- **Before:** Workflow assumed admins could change EventStatus during review
- **After:** EventStatus is USER-CONTROLLED - admins NEVER change it
- **Impact:** Completely different workflow and visibility logic

---

## Updated Workflow Summary

### **Key Principle:**
- **EventStatus** = User's control over their event lifecycle (DRAFT, PUBLISHED, CANCELLED, etc.)
- **PublicReviewStatus** = Admin's quality gate (PENDING, APPROVED, REJECTED)
- **Public Visibility** = BOTH conditions must be true:
  - `PublicReviewStatus = 'APPROVED'` (admin approved)
  - AND `EventStatus = 'PUBLISHED'` (user published)

### **Workflow Examples:**

#### Example 1: User Creates Public Event in DRAFT
```
1. User creates event: IsPublic = True, EventStatus = DRAFT
2. System sets: PublicReviewStatusID = PENDING
3. Admin reviews and approves: PublicReviewStatusID = APPROVED
4. ⚠️ Event is NOT yet publicly visible (EventStatus is still DRAFT)
5. User publishes event: EventStatus = PUBLISHED
6. ✅ Event is now publicly visible (both conditions met)
```

#### Example 2: User Publishes Before Admin Approval
```
1. User creates event: IsPublic = True, EventStatus = PUBLISHED
2. System sets: PublicReviewStatusID = PENDING
3. ⚠️ Event is NOT yet publicly visible (needs admin approval)
4. Admin reviews and approves: PublicReviewStatusID = APPROVED
5. ✅ Event is now publicly visible (both conditions met)
```

#### Example 3: User Cancels Approved Event
```
1. Event is approved and published: PublicReviewStatus = APPROVED, EventStatus = PUBLISHED
2. ✅ Event is publicly visible
3. User cancels event: EventStatus = CANCELLED
4. ❌ Event is no longer publicly visible (EventStatus changed)
5. System notifies stakeholders (organizers/companies attached to event)
```

---

## Code Changes Required

### **Backend Changes:**

1. **Update Event Model**
   - Change `PublicReviewStatus` from `String` to foreign key relationship
   - Add `PublicReviewStatusID` column

2. **Update Admin Review Service**
   - Remove `EventStatusID` changes from `approve_event()` and `reject_event()`
   - Use reference table lookups for status IDs

3. **Update Event Service**
   - Remove automatic `EventStatusID` changes when `IsPublic` changes
   - Only set `PublicReviewStatusID` when `IsPublic = True`

4. **Update Public Visibility Queries**
   - Add new query: `get_publicly_visible_events()`
   - Check BOTH `PublicReviewStatus = APPROVED` AND `EventStatus = PUBLISHED`

5. **Add Event Cancellation Notification**
   - When `EventStatus = CANCELLED` and `PublicReviewStatus = APPROVED`
   - Notify organizers/companies that attached to the event

### **Database Changes:**

1. **Create Reference Table**
   ```sql
   -- Run: database/schemas/public-review-status-ref-table.sql
   ```

2. **Migrate Existing Data**
   ```sql
   -- Run: database/migrations/change-public-review-status-to-fk.sql
   ```

3. **Drop Old Column** (after migration verified)
   ```sql
   ALTER TABLE [dbo].[Event] DROP COLUMN PublicReviewStatus;
   ```

---

## Updated Documentation

- ✅ `docs/event-public-review-workflow.md` - Complete workflow updated
- ✅ State mapping table updated with new visibility rules
- ✅ All 6 scenarios updated to reflect user-controlled EventStatus
- ✅ Guards updated to never change EventStatus during admin review
- ✅ New Guard 7: Public visibility query guard

---

## Next Steps

1. **Database Migration:**
   - Run `database/schemas/public-review-status-ref-table.sql`
   - Run `database/migrations/change-public-review-status-to-fk.sql`
   - Verify migration results
   - Drop old `PublicReviewStatus` NVARCHAR column

2. **Backend Updates:**
   - Update Event model to use foreign key
   - Remove EventStatus changes from admin review service
   - Add public visibility query logic
   - Implement event cancellation notification

3. **Frontend Updates:**
   - Update API clients to use PublicReviewStatusID
   - Update UI to show review status from reference table
   - Add messaging for "approved but not published" state

4. **Testing:**
   - Test all workflow scenarios
   - Verify public visibility logic
   - Test event cancellation notifications

---

## Summary

**Critical Changes:**
1. ✅ PublicReviewStatus now uses reference table (not NVARCHAR)
2. ✅ EventStatus is USER-CONTROLLED (admins never change it)
3. ✅ Public visibility requires BOTH conditions (APPROVED + PUBLISHED)
4. ✅ Event cancellation notifications added

**Files Updated:**
- `docs/event-public-review-workflow.md` - Complete rewrite
- `database/schemas/public-review-status-ref-table.sql` - NEW
- `database/migrations/change-public-review-status-to-fk.sql` - NEW

**Files to Update (Code Changes):**
- `backend/models/event.py` - Change to foreign key
- `backend/modules/events/admin_review_service.py` - Remove EventStatus changes
- `backend/modules/events/service.py` - Remove EventStatus changes
- `backend/modules/events/router.py` - Add public visibility query
- All API clients and schemas


