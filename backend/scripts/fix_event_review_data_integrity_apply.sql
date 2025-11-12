-- =====================================================================
-- Fix Event Review Data Integrity Issues - APPLY FIXES
-- =====================================================================
-- Story: 2.7 - Event Public Review Workflow Implementation
-- Purpose: Fix inconsistent records in the Event table
-- 
-- WARNING: This script will UPDATE your database.
-- Review the dry-run script first: fix_event_review_data_integrity.sql
-- =====================================================================

USE [EventLeadPlatform];
GO

BEGIN TRANSACTION;

PRINT 'Starting data integrity fixes...';
PRINT '';

-- =====================================================================
-- Issue 1: Archived events with IsPublicReviewRequired=True
-- =====================================================================

PRINT 'Fixing Issue 1: Archived events with review required...';

DECLARE @ArchivedStatusID INT;
SELECT @ArchivedStatusID = EventStatusID 
FROM [ref].[EventStatus] 
WHERE StatusCode = 'ARCHIVED' AND IsDeleted = 0;

DECLARE @PendingReviewStatusID BIGINT;
SELECT @PendingReviewStatusID = PublicReviewStatusID 
FROM [ref].[PublicReviewStatus] 
WHERE StatusCode = 'PENDING' AND IsDeleted = 0;

DECLARE @Issue1Count INT;
SELECT @Issue1Count = COUNT(*)
FROM [dbo].[Event] e
WHERE e.IsPublicReviewRequired = 1
    AND e.EventStatusID = @ArchivedStatusID
    AND e.IsDeleted = 0;

PRINT '  Found ' + CAST(@Issue1Count AS VARCHAR(10)) + ' events to fix';

IF @Issue1Count > 0
BEGIN
    UPDATE e
    SET 
        e.IsPublicReviewRequired = 0,
        e.IsSharedWithPlatform = 0,
        e.PublicReviewStatusID = CASE 
            WHEN e.PublicReviewStatusID = @PendingReviewStatusID THEN NULL 
            ELSE e.PublicReviewStatusID 
        END,
        e.UpdatedDate = GETUTCDATE()
    FROM [dbo].[Event] e
    WHERE e.IsPublicReviewRequired = 1
        AND e.EventStatusID = @ArchivedStatusID
        AND e.IsDeleted = 0;
    
    PRINT '  Fixed ' + CAST(@Issue1Count AS VARCHAR(10)) + ' archived events';
END
ELSE
BEGIN
    PRINT '  No archived events with review required found';
END

PRINT '';

-- =====================================================================
-- Issue 2: Public events with IsPublic=True but PublicReviewStatusID=NULL
-- =====================================================================

PRINT 'Fixing Issue 2: Public events without review status...';

DECLARE @Issue2PlatformCount INT;
DECLARE @Issue2NetworkCount INT;

SELECT 
    @Issue2PlatformCount = COUNT(*)
FROM [dbo].[Event]
WHERE IsPublic = 1
    AND IsSharedWithPlatform = 1
    AND PublicReviewStatusID IS NULL
    AND IsDeleted = 0;

SELECT 
    @Issue2NetworkCount = COUNT(*)
FROM [dbo].[Event]
WHERE IsPublic = 1
    AND IsSharedWithPlatform = 0
    AND PublicReviewStatusID IS NULL
    AND IsDeleted = 0;

PRINT '  Found ' + CAST(@Issue2PlatformCount AS VARCHAR(10)) + ' platform events and ' + CAST(@Issue2NetworkCount AS VARCHAR(10)) + ' network-only events to review';

IF (@Issue2PlatformCount > 0 OR @Issue2NetworkCount > 0) AND @PendingReviewStatusID IS NOT NULL
BEGIN
    -- For platform-sharing events: Set PublicReviewStatusID=PENDING
    DECLARE @PlatformSharingCount INT;
    UPDATE e
    SET 
        e.PublicReviewStatusID = @PendingReviewStatusID,
        e.IsPublicReviewRequired = 1,
        e.UpdatedDate = GETUTCDATE()
    FROM [dbo].[Event] e
    WHERE e.IsPublic = 1
        AND e.PublicReviewStatusID IS NULL
        AND e.IsSharedWithPlatform = 1
        AND e.IsDeleted = 0;
    
    SET @PlatformSharingCount = @@ROWCOUNT;
    PRINT '  Set PublicReviewStatusID=PENDING for ' + CAST(@PlatformSharingCount AS VARCHAR(10)) + ' platform-sharing events';
    
    -- For company network only events: Set IsPublicReviewRequired=False
    UPDATE e
    SET 
        e.IsPublicReviewRequired = 0,
        e.UpdatedDate = GETUTCDATE()
    FROM [dbo].[Event] e
    WHERE e.IsPublic = 1
        AND e.PublicReviewStatusID IS NULL
        AND e.IsSharedWithPlatform = 0
        AND e.IsDeleted = 0;
    
    DECLARE @CompanyNetworkCount INT = @@ROWCOUNT;
    PRINT '  Set IsPublicReviewRequired=False for ' + CAST(@CompanyNetworkCount AS VARCHAR(10)) + ' company network only events';
END
ELSE IF (@Issue2PlatformCount > 0 OR @Issue2NetworkCount > 0)
BEGIN
    PRINT '  ERROR: PENDING review status not found in database';
END
ELSE
BEGIN
    PRINT '  No public events without review status found';
END

PRINT '';

-- =====================================================================
-- Issue 3: Invalid state combinations
-- =====================================================================

PRINT 'Fixing Issue 3: Invalid state combinations...';

DECLARE @Issue3Count INT;
SELECT @Issue3Count = COUNT(DISTINCT EventID)
FROM [dbo].[Event]
WHERE IsPublic = 0
    AND (
        PublicReviewStatusID IS NOT NULL
        OR IsSharedWithPlatform = 1
        OR IsPublicReviewRequired = 1
    )
    AND IsDeleted = 0;

PRINT '  Found ' + CAST(@Issue3Count AS VARCHAR(10)) + ' events to fix';

IF @Issue3Count > 0
BEGIN
    UPDATE [dbo].[Event]
    SET 
        PublicReviewStatusID = NULL,
        IsSharedWithPlatform = 0,
        IsPublicReviewRequired = 0,
        UpdatedDate = GETUTCDATE()
    WHERE IsPublic = 0
        AND (
            PublicReviewStatusID IS NOT NULL
            OR IsSharedWithPlatform = 1
            OR IsPublicReviewRequired = 1
        )
        AND IsDeleted = 0;
    
    PRINT '  Fixed ' + CAST(@Issue3Count AS VARCHAR(10)) + ' events with invalid state combinations';
END
ELSE
BEGIN
    PRINT '  No invalid state combinations found';
END

PRINT '';

-- =====================================================================
-- Issue 4: Rejected events with IsSharedWithPlatform=True
-- =====================================================================

PRINT 'Fixing Issue 4: Rejected events with platform sharing...';

DECLARE @RejectedStatusID BIGINT;
SELECT @RejectedStatusID = PublicReviewStatusID 
FROM [ref].[PublicReviewStatus] 
WHERE StatusCode = 'REJECTED' AND IsDeleted = 0;

DECLARE @Issue4Count INT;
SELECT @Issue4Count = COUNT(*)
FROM [dbo].[Event] e
WHERE e.PublicReviewStatusID = @RejectedStatusID
    AND e.IsSharedWithPlatform = 1
    AND e.IsDeleted = 0;

PRINT '  Found ' + CAST(@Issue4Count AS VARCHAR(10)) + ' events to fix';

IF @Issue4Count > 0
BEGIN
    UPDATE e
    SET 
        e.IsSharedWithPlatform = 0,
        e.UpdatedDate = GETUTCDATE()
    FROM [dbo].[Event] e
    WHERE e.PublicReviewStatusID = @RejectedStatusID
        AND e.IsSharedWithPlatform = 1
        AND e.IsDeleted = 0;
    
    PRINT '  Fixed ' + CAST(@Issue4Count AS VARCHAR(10)) + ' rejected events with platform sharing';
END
ELSE
BEGIN
    PRINT '  No rejected events with platform sharing found';
END

PRINT '';

-- =====================================================================
-- Summary
-- =====================================================================

DECLARE @TotalFixed INT = @Issue1Count + @Issue2PlatformCount + @Issue2NetworkCount + @Issue3Count + @Issue4Count;

PRINT '====================================================================';
PRINT 'Summary:';
PRINT '  Issue 1 (Archived with review): ' + CAST(@Issue1Count AS VARCHAR(10));
PRINT '  Issue 2 (Public without status): ' + CAST(@Issue2PlatformCount AS VARCHAR(10));
PRINT '  Issue 3 (Invalid combinations): ' + CAST(@Issue3Count AS VARCHAR(10));
PRINT '  Issue 4 (Rejected with sharing): ' + CAST(@Issue4Count AS VARCHAR(10));
PRINT '  Total events fixed: ' + CAST(@TotalFixed AS VARCHAR(10));
PRINT '====================================================================';
PRINT '';

-- Verify all issues are resolved
DECLARE @RemainingIssues INT;
SELECT @RemainingIssues = COUNT(DISTINCT EventID)
FROM (
    SELECT EventID FROM [dbo].[Event] e
    INNER JOIN [ref].[EventStatus] es ON e.EventStatusID = es.EventStatusID
    WHERE e.IsPublicReviewRequired = 1 AND es.StatusCode = 'ARCHIVED' AND e.IsDeleted = 0
    
    UNION
    
    SELECT EventID FROM [dbo].[Event]
    WHERE IsPublic = 1 AND IsSharedWithPlatform = 1 AND PublicReviewStatusID IS NULL AND IsDeleted = 0
    
    UNION
    
    SELECT EventID FROM [dbo].[Event]
    WHERE IsPublic = 0 AND (PublicReviewStatusID IS NOT NULL OR IsSharedWithPlatform = 1 OR IsPublicReviewRequired = 1)
    AND IsDeleted = 0
    
    UNION
    
    SELECT e.EventID FROM [dbo].[Event] e
    INNER JOIN [ref].[PublicReviewStatus] prs ON e.PublicReviewStatusID = prs.PublicReviewStatusID
    WHERE prs.StatusCode = 'REJECTED' AND e.IsSharedWithPlatform = 1 AND e.IsDeleted = 0
) AS Issues;

IF @RemainingIssues = 0
BEGIN
    PRINT '✅ All data integrity issues have been resolved!';
END
ELSE
BEGIN
    PRINT '⚠️  Warning: ' + CAST(@RemainingIssues AS VARCHAR(10)) + ' issues remain. Please review manually.';
END

PRINT '';
PRINT '====================================================================';
PRINT 'Review the changes above.';
PRINT 'If everything looks correct, run: COMMIT;';
PRINT 'To rollback changes, run: ROLLBACK;';
PRINT '====================================================================';

-- Uncomment the line below to automatically commit:
-- COMMIT;

-- Or keep the transaction open for manual review and commit

GO

