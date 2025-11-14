-- =====================================================================
-- MIGRATION: Change PublicReviewStatus from NVARCHAR to Foreign Key
-- =====================================================================
-- Purpose: Convert PublicReviewStatus from NVARCHAR(20) to foreign key
--          to ref.PublicReviewStatus table
-- Story: 2.6 - Admin Public Event Review Workflow
-- =====================================================================

USE [EventLeadPlatform];
GO

BEGIN TRANSACTION;

-- =====================================================================
-- STEP 1: Ensure PublicReviewStatus reference table exists
-- =====================================================================
-- Note: Run database/schemas/public-review-status-ref-table.sql first
-- This script assumes the table already exists

-- =====================================================================
-- STEP 2: Add new PublicReviewStatusID column (nullable initially)
-- =====================================================================
ALTER TABLE [dbo].[Event]
ADD PublicReviewStatusID INT NULL;
GO

-- =====================================================================
-- STEP 3: Migrate existing data from NVARCHAR to FK
-- =====================================================================
-- Map existing PublicReviewStatus values to new PublicReviewStatusID

UPDATE e
SET e.PublicReviewStatusID = prs.PublicReviewStatusID
FROM [dbo].[Event] e
INNER JOIN [ref].[PublicReviewStatus] prs ON e.PublicReviewStatus = prs.StatusCode
WHERE e.PublicReviewStatus IS NOT NULL;
GO

-- =====================================================================
-- STEP 4: Add foreign key constraint
-- =====================================================================
ALTER TABLE [dbo].[Event]
ADD CONSTRAINT FK_Event_PublicReviewStatus 
    FOREIGN KEY (PublicReviewStatusID) 
    REFERENCES [ref].[PublicReviewStatus](PublicReviewStatusID);
GO

-- =====================================================================
-- STEP 5: Create index for performance
-- =====================================================================
CREATE INDEX IX_Event_PublicReviewStatus 
    ON [dbo].[Event](PublicReviewStatusID, IsDeleted)
    WHERE IsDeleted = 0;
GO

-- =====================================================================
-- STEP 6: Drop old NVARCHAR column (after verifying data migration)
-- =====================================================================
-- CAUTION: Only uncomment after verifying the migration worked correctly
-- ALTER TABLE [dbo].[Event]
-- DROP CONSTRAINT CK_Event_PublicReviewStatus;  -- Drop check constraint first
-- GO
-- ALTER TABLE [dbo].[Event]
-- DROP COLUMN PublicReviewStatus;
-- GO

-- =====================================================================
-- STEP 7: Verification
-- =====================================================================
PRINT '=== VERIFICATION ===';

-- Check data migration
SELECT 
    'Data Migration Check' AS CheckType,
    COUNT(*) AS TotalEvents,
    SUM(CASE WHEN PublicReviewStatus IS NOT NULL AND PublicReviewStatusID IS NULL THEN 1 ELSE 0 END) AS UnmigratedRecords,
    SUM(CASE WHEN PublicReviewStatus IS NULL AND PublicReviewStatusID IS NULL THEN 1 ELSE 0 END) AS NullRecords,
    SUM(CASE WHEN PublicReviewStatusID IS NOT NULL THEN 1 ELSE 0 END) AS MigratedRecords
FROM [dbo].[Event]
WHERE IsDeleted = 0;

-- Show distribution
SELECT 
    prs.StatusCode,
    prs.StatusName,
    COUNT(e.EventID) AS EventCount
FROM [ref].[PublicReviewStatus] prs
LEFT JOIN [dbo].[Event] e ON prs.PublicReviewStatusID = e.PublicReviewStatusID AND e.IsDeleted = 0
GROUP BY prs.StatusCode, prs.StatusName
ORDER BY prs.SortOrder;

-- If everything looks good, uncomment the COMMIT line below
-- COMMIT;

-- To rollback if needed:
-- ROLLBACK;

PRINT 'Migration completed. Review the results and COMMIT if correct.';
PRINT 'After committing, manually drop the old PublicReviewStatus NVARCHAR column.';
GO


