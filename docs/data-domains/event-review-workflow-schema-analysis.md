# Event Review Workflow - Schema Analysis & Required Changes

**Date:** 2025-01-XX  
**Analyst:** Dimitri 🔍 (Data Domain Architect)  
**Story:** 2.6 - Admin Public Event Review Workflow  
**Purpose:** Identify required database schema changes to support the event public review workflow

---

## Executive Summary

After reviewing the `event-public-review-workflow.md` against the current database schema, I've identified **3 critical schema changes** required to fully support the workflow:

1. ✅ **`ref.PublicReviewStatus` table** - Exists but needs corrections (data type, nullable audit fields)
2. ❌ **`IsSharedWithPlatform` field** - **MISSING** from `dbo.Event` table
3. ❌ **`PublicReviewStatusID` FK** - Current `PublicReviewStatus VARCHAR(20)` must be converted to FK

---

## Current State Analysis

### ❌ Missing: `ref.PublicReviewStatus` Reference Table

**Location:** `database/schemas/public-review-status-ref-table.sql` (schema file only - **NOT EXECUTED**)

**Status:** Table **DOES NOT EXIST** in database. Schema file exists but has **2 naming rule violations** that need to be fixed before creation:

| Issue | Current | Should Be | Rule Violation |
|-------|---------|-----------|----------------|
| Primary Key Type | `INT IDENTITY(1,1)` | `BIGINT IDENTITY(1,1)` | Primary keys should be BIGINT per standards |
| CreatedBy Nullable | `BIGINT NOT NULL` | `BIGINT NULL` | System-created records may not have a creator |

**Evidence Table Does NOT Exist:**
- ❌ No SQLAlchemy model in `backend/models/ref/public_review_status.py`
- ❌ Not listed in `docs/database-schema.md`
- ❌ Migration file says "Run database/schemas/public-review-status-ref-table.sql first" (implies not executed)
- ❌ Backend model still uses `PublicReviewStatus = Column(String(20))` (not FK)

**Schema File (needs corrections before execution):**
```sql
CREATE TABLE [ref].[PublicReviewStatus] (
    PublicReviewStatusID INT IDENTITY(1,1) PRIMARY KEY,  -- ❌ Should be BIGINT
    StatusCode NVARCHAR(20) NOT NULL UNIQUE,
    StatusName NVARCHAR(50) NOT NULL,
    StatusDescription NVARCHAR(200) NULL,
    StatusColor NVARCHAR(7) NULL,
    StatusIcon NVARCHAR(50) NULL,
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 0,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NOT NULL,  -- ❌ Should be NULL
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,
    -- Foreign keys...
);
```

**Seed Data:** ✅ Correctly includes PENDING, APPROVED, REJECTED statuses

---

### ❌ Missing: `IsSharedWithPlatform` Field in `dbo.Event`

**Workflow Requirement:** Field #5 in `event-public-review-workflow.md`

**Purpose:** User's choice to share event with platform-wide search (beyond company network)

**Current State:** **FIELD DOES NOT EXIST** in `dbo.Event` table

**Required Field:**
```sql
IsSharedWithPlatform BIT NOT NULL DEFAULT 0
-- ^ User's choice to share event with platform-wide search
-- 0 = Company network only (no review needed)
-- 1 = Share with platform (requires admin review)
```

**Business Logic:**
- `IsPublic = True` AND `IsSharedWithPlatform = False` → Visible to company and linked organizations only
- `IsPublic = True` AND `IsSharedWithPlatform = True` → Visible to company, linked organizations, AND platform-wide search (requires review)

---

### ❌ Incorrect: `PublicReviewStatus` VARCHAR(20) in `dbo.Event`

**Current State:** `dbo.Event` has:
```sql
PublicReviewStatus VARCHAR(20) NULL,  -- ❌ Should be FK, not VARCHAR
```

**Workflow Requirement:** Should be `PublicReviewStatusID BIGINT NULL FK→ref.PublicReviewStatus`

**Current Schema (from `database-schema.md`):**
```sql
PublicReviewStatus VARCHAR(20) NULL,
-- ^ Public review status
-- Values: 'PENDING', 'APPROVED', 'REJECTED'
-- NULL = Not submitted for public review
```

**Problems:**
1. ❌ Uses `VARCHAR` instead of `NVARCHAR` (Unicode support required)
2. ❌ Uses string values instead of foreign key (violates normalization standards)
3. ❌ No referential integrity (database can't enforce valid values)
4. ❌ CHECK constraint with hardcoded values (violates naming rules - should use reference table)

**Required Change:**
```sql
PublicReviewStatusID BIGINT NULL,
-- ^ Public review status (foreign key to ref.PublicReviewStatus)
-- NULL = Not submitted for review OR private event
-- FK to ref.PublicReviewStatus (PENDING, APPROVED, REJECTED)
CONSTRAINT FK_Event_PublicReviewStatus FOREIGN KEY (PublicReviewStatusID) 
    REFERENCES [ref].[PublicReviewStatus](PublicReviewStatusID)
```

---

## Required Schema Changes

### Change 1: Create `ref.PublicReviewStatus` Reference Table

**File:** `database/schemas/public-review-status-ref-table.sql` (exists but needs corrections before execution)

**Status:** Table **DOES NOT EXIST** - needs to be created from scratch

**Action Required:**
1. Fix the schema file (change INT to BIGINT, CreatedBy to NULL)
2. Execute the schema file to create the table
3. Create SQLAlchemy model in `backend/models/ref/public_review_status.py`

**Corrected Schema (to be created):**
```sql
CREATE TABLE [ref].[PublicReviewStatus] (
    PublicReviewStatusID BIGINT IDENTITY(1,1) PRIMARY KEY,  -- ✅ Fixed
    StatusCode NVARCHAR(20) NOT NULL UNIQUE,
    StatusName NVARCHAR(50) NOT NULL,
    StatusDescription NVARCHAR(200) NULL,
    StatusColor NVARCHAR(7) NULL,
    StatusIcon NVARCHAR(50) NULL,
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 0,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,  -- ✅ Fixed (system-created records)
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,
    -- Foreign keys remain the same
);
```

---

### Change 2: Add `IsSharedWithPlatform` Field to `dbo.Event`

**Migration Required:** Add new column to existing `dbo.Event` table

**SQL Migration:**
```sql
-- =====================================================================
-- ADD IsSharedWithPlatform Field to Event Table
-- =====================================================================
-- Story: 2.6 - Admin Public Event Review Workflow
-- Purpose: User's choice to share event with platform-wide search
-- =====================================================================

USE [EventLeadPlatform];
GO

-- Add IsSharedWithPlatform column
ALTER TABLE [dbo].[Event]
ADD IsSharedWithPlatform BIT NOT NULL DEFAULT 0;
GO

-- Add column description
EXEC sp_addextendedproperty 
    @name = N'MS_Description',
    @value = N'User''s choice to share event with platform-wide search (beyond company network). 0 = Company network only (no review needed), 1 = Share with platform (requires admin review)',
    @level0type = N'SCHEMA', @level0name = N'dbo',
    @level1type = N'TABLE', @level1name = N'Event',
    @level2type = N'COLUMN', @level2name = N'IsSharedWithPlatform';
GO

-- Update existing events: If IsPublic = True and PublicReviewStatus is not NULL,
-- assume they want platform sharing (for backward compatibility)
UPDATE [dbo].[Event]
SET IsSharedWithPlatform = 1
WHERE IsPublic = 1 
    AND (PublicReviewStatus IS NOT NULL OR IsPublicReviewRequired = 1);
GO

PRINT 'IsSharedWithPlatform column added successfully!';
GO
```

**Position in Table:** Should be placed after `IsPublic` and before `EventStatusID` for logical grouping

---

### Change 3: Convert `PublicReviewStatus` VARCHAR to `PublicReviewStatusID` FK

**Migration Required:** Data migration from VARCHAR to FK with data mapping

**Steps:**
1. Create `ref.PublicReviewStatus` table (if not exists) with corrected schema
2. Add new `PublicReviewStatusID` column to `dbo.Event`
3. Migrate existing data: Map VARCHAR values to FK IDs
4. Drop old `PublicReviewStatus` column
5. Drop CHECK constraint (if exists)
6. Add foreign key constraint
7. Update indexes

**SQL Migration:**
```sql
-- =====================================================================
-- MIGRATE PublicReviewStatus from VARCHAR to FK
-- =====================================================================
-- Story: 2.6 - Admin Public Event Review Workflow
-- Purpose: Convert PublicReviewStatus VARCHAR to Foreign Key
-- =====================================================================

USE [EventLeadPlatform];
GO

-- Step 1: Ensure ref.PublicReviewStatus table exists with correct schema
-- (Run public-review-status-ref-table.sql first with BIGINT fix)

-- Step 2: Add new PublicReviewStatusID column (nullable for now)
ALTER TABLE [dbo].[Event]
ADD PublicReviewStatusID BIGINT NULL;
GO

-- Step 3: Migrate existing data from VARCHAR to FK
UPDATE e
SET e.PublicReviewStatusID = prs.PublicReviewStatusID
FROM [dbo].[Event] e
INNER JOIN [ref].[PublicReviewStatus] prs 
    ON e.PublicReviewStatus = prs.StatusCode
WHERE e.PublicReviewStatus IS NOT NULL;
GO

-- Step 4: Drop old CHECK constraint (if exists)
IF EXISTS (
    SELECT 1 
    FROM sys.check_constraints 
    WHERE name = 'CK_Event_PublicReviewStatus'
)
BEGIN
    ALTER TABLE [dbo].[Event]
    DROP CONSTRAINT CK_Event_PublicReviewStatus;
END
GO

-- Step 5: Drop old PublicReviewStatus VARCHAR column
ALTER TABLE [dbo].[Event]
DROP COLUMN PublicReviewStatus;
GO

-- Step 6: Add foreign key constraint
ALTER TABLE [dbo].[Event]
ADD CONSTRAINT FK_Event_PublicReviewStatus 
    FOREIGN KEY (PublicReviewStatusID) 
    REFERENCES [ref].[PublicReviewStatus](PublicReviewStatusID);
GO

-- Step 7: Update indexes (drop old, create new)
-- Drop old index if it exists
IF EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_Event_PublicReview')
BEGIN
    DROP INDEX IX_Event_PublicReview ON [dbo].[Event];
END
GO

-- Create new index with PublicReviewStatusID
CREATE INDEX IX_Event_PublicReview 
ON [dbo].[Event](IsPublic, IsSharedWithPlatform, PublicReviewStatusID, IsDeleted)
WHERE IsDeleted = 0;
GO

PRINT 'PublicReviewStatus migrated to PublicReviewStatusID FK successfully!';
GO
```

---

## Schema Validation Against Naming Rules

### ✅ Compliance Checklist

| Rule | Status | Notes |
|------|--------|-------|
| **Tables:** PascalCase, singular | ✅ | `PublicReviewStatus` (reference table) |
| **Columns:** PascalCase | ✅ | `PublicReviewStatusID`, `IsSharedWithPlatform` |
| **Primary Keys:** `[TableName]ID` | ✅ | `PublicReviewStatusID` |
| **Foreign Keys:** `[ReferencedTable]ID` | ✅ | `PublicReviewStatusID` → `ref.PublicReviewStatus` |
| **Booleans:** `Is` or `Has` prefix | ✅ | `IsSharedWithPlatform`, `IsPublic`, `IsPublicReviewRequired` |
| **Dates:** `Date` or `At` suffix | ✅ | `PublicReviewDate`, `PublicVisibilityDate` |
| **Text fields:** `NVARCHAR` (not VARCHAR) | ⚠️ | `PublicReviewStatus` currently VARCHAR(20) - will be removed |
| **Schema:** lowercase | ✅ | `ref` schema |
| **Reference Tables:** `ref` schema | ✅ | `ref.PublicReviewStatus` |
| **NO ENUMs:** Use reference tables | ✅ | Using `ref.PublicReviewStatus` instead of VARCHAR |

---

## Data Migration Considerations

### Existing Data Handling

**Scenario 1: Events with `PublicReviewStatus = 'PENDING'`**
- Map to `PublicReviewStatusID` = (SELECT PublicReviewStatusID FROM ref.PublicReviewStatus WHERE StatusCode = 'PENDING')
- Set `IsSharedWithPlatform = 1` (if IsPublic = True)

**Scenario 2: Events with `PublicReviewStatus = 'APPROVED'`**
- Map to `PublicReviewStatusID` = (SELECT PublicReviewStatusID FROM ref.PublicReviewStatus WHERE StatusCode = 'APPROVED')
- Set `IsSharedWithPlatform = 1` (if IsPublic = True)

**Scenario 3: Events with `PublicReviewStatus = 'REJECTED'`**
- Map to `PublicReviewStatusID` = (SELECT PublicReviewStatusID FROM ref.PublicReviewStatus WHERE StatusCode = 'REJECTED')
- Set `IsSharedWithPlatform = 0` (rejected events cannot be platform-shared)

**Scenario 4: Events with `PublicReviewStatus = NULL`**
- Set `PublicReviewStatusID = NULL`
- If `IsPublic = True` and `IsPublicReviewRequired = 1`: Set `IsSharedWithPlatform = 1` (assume they want platform sharing)
- If `IsPublic = True` and `IsPublicReviewRequired = 0`: Set `IsSharedWithPlatform = 0` (company network only)
- If `IsPublic = False`: Set `IsSharedWithPlatform = 0` (private event)

---

## Impact Analysis

### Backend Code Changes Required

1. **SQLAlchemy Models:**
   - Update `backend/models/event.py`:
     - Change `PublicReviewStatus` to `PublicReviewStatusID` (BIGINT FK)
     - Add `IsSharedWithPlatform` (Boolean)
     - Add relationship to `PublicReviewStatus` model

2. **Service Layer:**
   - Update `backend/modules/events/service.py`:
     - Update all queries that reference `PublicReviewStatus`
     - Add logic to set `IsSharedWithPlatform` based on user input
     - Update guards to check `IsSharedWithPlatform`

3. **Admin Review Service:**
   - Update `backend/modules/events/admin_review_service.py`:
     - Update queries to filter by `IsSharedWithPlatform = True`
     - Update approve/reject logic to handle `IsSharedWithPlatform`

### Frontend Code Changes Required

1. **Event Creation/Edit Forms:**
   - Add UI control for `IsSharedWithPlatform` selection
   - Show "Company Network Only" vs "Share with Platform" options
   - Display review status based on `PublicReviewStatusID` (not string)

2. **Admin Dashboard:**
   - Update queries to filter by `IsSharedWithPlatform = True`
   - Display review status from `PublicReviewStatusID` relationship

---

## Implementation Priority

### Phase 1: Critical (Must Have)
1. ✅ Create/fix `ref.PublicReviewStatus` table (with BIGINT fix)
2. ✅ Add `IsSharedWithPlatform` field to `dbo.Event`
3. ✅ Migrate `PublicReviewStatus` VARCHAR → `PublicReviewStatusID` FK

### Phase 2: Backend Updates
4. Update SQLAlchemy models
5. Update service layer logic
6. Update admin review service

### Phase 3: Frontend Updates
7. Update event creation/edit forms
8. Update admin dashboard
9. Update event display components

---

## Testing Checklist

- [ ] Verify `ref.PublicReviewStatus` table has correct schema (BIGINT, nullable CreatedBy)
- [ ] Verify `IsSharedWithPlatform` column exists in `dbo.Event`
- [ ] Verify `PublicReviewStatusID` FK exists and references `ref.PublicReviewStatus`
- [ ] Verify existing data migrated correctly (VARCHAR → FK mapping)
- [ ] Verify foreign key constraint enforces referential integrity
- [ ] Verify indexes are updated for new column structure
- [ ] Test event creation with `IsSharedWithPlatform = True` (should set `PublicReviewStatusID = PENDING`)
- [ ] Test event creation with `IsSharedWithPlatform = False` (should set `PublicReviewStatusID = NULL`)
- [ ] Test admin approval workflow (should update `PublicReviewStatusID` to APPROVED)
- [ ] Test admin rejection workflow (should update `PublicReviewStatusID` to REJECTED and set `IsSharedWithPlatform = False`)

---

## Summary

**Total Changes Required: 3**

1. ❌ **CREATE `ref.PublicReviewStatus` table** - Table does not exist. Create with BIGINT PK, nullable CreatedBy
2. ❌ **Add `IsSharedWithPlatform` field** - New BIT column in `dbo.Event`
3. ❌ **Convert `PublicReviewStatus` to FK** - Migrate VARCHAR(20) to `PublicReviewStatusID BIGINT FK`

**All changes comply with database naming rules and normalization standards.**

---

**Next Steps:**
1. Review this analysis
2. Create migration scripts for all 3 changes
3. Test migrations on development database
4. Update backend models and services
5. Update frontend components

---

**Generated by:** Dimitri 🔍 (Data Domain Architect)  
**Date:** 2025-01-XX  
**Related Documents:**
- `docs/event-public-review-workflow.md` - Workflow requirements
- `docs/database-schema.md` - Current schema reference
- `docs/database-naming-rules.md` - Naming standards
- `database/schemas/public-review-status-ref-table.sql` - Reference table schema

