# PublicReviewStatus Seed Data Review

**Date:** 2025-01-XX  
**Analyst:** Dimitri 🔍 (Data Domain Architect)  
**Story:** 2.6 - Admin Public Event Review Workflow  
**Purpose:** Verify all required statuses are included in `ref.PublicReviewStatus` seed data

---

## Workflow Status Requirements

Based on `docs/event-public-review-workflow.md`, the following statuses are required:

| StatusCode | Workflow Usage | Description from Workflow |
|-----------|----------------|--------------------------|
| **PENDING** | Events awaiting admin review | "Awaiting admin review" - Event is in admin review queue |
| **APPROVED** | Admin approved events | "Admin approved - event can go public when user publishes it" - Quality gate passed, but user must publish |
| **REJECTED** | Admin rejected events | "Admin rejected - event cannot be made public" - Can be resubmitted after edits |
| **NULL** | Not submitted / Private | Not a status - absence of status (private events, not yet submitted) |

**Note:** `NULL` is not a status in the ref table - it represents the absence of a status.

---

## Current Seed Data Analysis

### ✅ Statuses Present (3/3 Required)

| StatusCode | StatusName | Current Description | Workflow Match | Issues |
|-----------|------------|-------------------|----------------|--------|
| PENDING | Pending Review | "Event is awaiting admin review for public visibility" | ✅ Matches | Description could be more detailed |
| APPROVED | Approved | "Event has been approved by admin and is ready to go public when published" | ✅ Matches | Good - emphasizes user must publish |
| REJECTED | Rejected | "Event has been rejected by admin and cannot be made public" | ⚠️ Partial | Missing resubmission context |

---

## Recommended Seed Data Updates

### Current Seed Data (Lines 84-86):
```sql
('PENDING', 'Pending Review', 'Event is awaiting admin review for public visibility', '#FFC107', 'clock-icon', 1, 1, 1),
('APPROVED', 'Approved', 'Event has been approved by admin and is ready to go public when published', '#28A745', 'check-circle-icon', 1, 2, 1),
('REJECTED', 'Rejected', 'Event has been rejected by admin and cannot be made public', '#DC3545', 'x-circle-icon', 1, 3, 1);
```

### Recommended Enhanced Seed Data:

```sql
-- PENDING: Event is in admin review queue
('PENDING', 'Pending Review', 'Event is awaiting admin review for platform-wide visibility. Admin will review content quality before approving.', '#FFC107', 'clock-icon', 1, 1, 1),

-- APPROVED: Admin approved, but user controls publication
('APPROVED', 'Approved', 'Event has been approved by admin for platform-wide visibility. Event will be publicly visible when user publishes it (EventStatus = PUBLISHED).', '#28A745', 'check-circle-icon', 1, 2, 1),

-- REJECTED: Admin rejected, but can be resubmitted
('REJECTED', 'Rejected', 'Event has been rejected by admin and cannot be shared with platform-wide search. Event remains visible to company network only. User can edit and resubmit for review.', '#DC3545', 'x-circle-icon', 1, 3, 1);
```

**Key Improvements:**
1. **PENDING**: Clarifies it's for "platform-wide visibility" (not just "public visibility")
2. **APPROVED**: Emphasizes that user must publish (EventStatus = PUBLISHED) for visibility
3. **REJECTED**: Clarifies:
   - Event remains visible to company network
   - User can resubmit after edits
   - Platform sharing is disabled

---

## Status Transition Validation

### Valid Transitions (from Workflow):

| From | To | Trigger | Notes |
|------|-----|---------|-------|
| NULL | PENDING | User sets `IsSharedWithPlatform = True` | Auto-set when platform sharing enabled |
| PENDING | APPROVED | Admin approves | Admin action |
| PENDING | REJECTED | Admin rejects | Admin action (requires comment) |
| REJECTED | PENDING | User resubmits | User resubmission workflow |
| Any | NULL | User sets `IsSharedWithPlatform = False` OR `IsPublic = False` | Clearing review status |

**All transitions are covered by the three statuses.** ✅

---

## Status Code Validation

### Case Sensitivity Check:

Workflow uses: `'PENDING'`, `'APPROVED'`, `'REJECTED'` (UPPERCASE)  
Seed data uses: `'PENDING'`, `'APPROVED'`, `'REJECTED'` (UPPERCASE)  

✅ **Match confirmed** - Case-sensitive matching is correct

---

## SortOrder Validation

| Status | SortOrder | Rationale | ✅/❌ |
|--------|-----------|-----------|-------|
| PENDING | 1 | First in workflow (initial state) | ✅ Correct |
| APPROVED | 2 | Second (after approval) | ✅ Correct |
| REJECTED | 3 | Last (after rejection) | ✅ Correct |

**SortOrder is logical for UI dropdowns and workflow display.** ✅

---

## Color & Icon Validation

| Status | Color | Icon | Rationale | ✅/❌ |
|--------|-------|------|-----------|-------|
| PENDING | `#FFC107` (Yellow/Amber) | `clock-icon` | Warning/attention needed | ✅ Appropriate |
| APPROVED | `#28A745` (Green) | `check-circle-icon` | Success/positive | ✅ Appropriate |
| REJECTED | `#DC3545` (Red) | `x-circle-icon` | Error/negative | ✅ Appropriate |

**Colors follow standard UI conventions (yellow=warning, green=success, red=error).** ✅

---

## Missing Statuses Check

### Potential Edge Cases Reviewed:

1. **"UNDER_REVIEW"** - Not needed - covered by PENDING
2. **"CANCELLED"** - Not needed - handled by EventStatus, not PublicReviewStatus
3. **"EXPIRED"** - Not needed - review doesn't expire in workflow
4. **"WITHDRAWN"** - Not needed - user can set `IsSharedWithPlatform = False` to remove from review

**Conclusion:** All required statuses are present. No additional statuses needed. ✅

---

## Schema File Issues (Already Identified)

| Issue | Current | Should Be | Status |
|-------|---------|-----------|--------|
| Primary Key Type | `INT IDENTITY(1,1)` | `BIGINT IDENTITY(1,1)` | ❌ Needs Fix |
| CreatedBy Nullable | `BIGINT NOT NULL` | `BIGINT NULL` | ❌ Needs Fix |

**Note:** These schema issues must be fixed before creating the table.

---

## Final Recommendation

### ✅ Seed Data Status: **COMPLETE** (with minor improvements recommended)

**Required Statuses:** 3/3 ✅  
**Status Codes:** Match workflow exactly ✅  
**SortOrder:** Logical sequence ✅  
**Colors/Icons:** Appropriate ✅  
**Descriptions:** Good, but could be enhanced for clarity

### Action Items:

1. ✅ **Keep all 3 statuses** - PENDING, APPROVED, REJECTED
2. ⚠️ **Enhance descriptions** - Make them more comprehensive (see recommended updates above)
3. ❌ **Fix schema issues** - Change INT to BIGINT, CreatedBy to NULL
4. ✅ **Seed data is complete** - All workflow statuses are covered

---

## Updated Seed Data Script

```sql
-- Insert default public review statuses (ENHANCED DESCRIPTIONS)
INSERT INTO [ref].[PublicReviewStatus] (
    StatusCode, 
    StatusName, 
    StatusDescription, 
    StatusColor, 
    StatusIcon, 
    IsActive, 
    SortOrder, 
    CreatedBy
) VALUES
-- PENDING: Event is in admin review queue
('PENDING', 'Pending Review', 
    'Event is awaiting admin review for platform-wide visibility. Admin will review content quality before approving.', 
    '#FFC107', 'clock-icon', 1, 1, 1),

-- APPROVED: Admin approved, but user controls publication
('APPROVED', 'Approved', 
    'Event has been approved by admin for platform-wide visibility. Event will be publicly visible when user publishes it (EventStatus = PUBLISHED).', 
    '#28A745', 'check-circle-icon', 1, 2, 1),

-- REJECTED: Admin rejected, but can be resubmitted
('REJECTED', 'Rejected', 
    'Event has been rejected by admin and cannot be shared with platform-wide search. Event remains visible to company network only. User can edit and resubmit for review.', 
    '#DC3545', 'x-circle-icon', 1, 3, 1);
GO
```

---

**Generated by:** Dimitri 🔍 (Data Domain Architect)  
**Date:** 2025-01-XX  
**Related Documents:**
- `docs/event-public-review-workflow.md` - Workflow requirements
- `database/schemas/public-review-status-ref-table.sql` - Schema file (needs fixes)
- `docs/data-domains/event-review-workflow-schema-analysis.md` - Schema analysis

