-- =====================================================================
-- Fix Inconsistent Event Review Status
-- =====================================================================
-- Purpose: Fix existing events with inconsistent review status combinations:
--          - Events with IsPublicReviewRequired = True but EventStatus = ARCHIVED
--          - Events with IsPublicReviewRequired = True but EventStatus = APPROVED (should be PUBLISHED)
--          - Events with IsPublic = True but PublicReviewStatus = NULL
--          - Events with IsPublic = False but PublicReviewStatus is set
-- =====================================================================
-- Story 2.6: Admin Public Event Review Workflow
-- =====================================================================

BEGIN TRANSACTION;

-- =====================================================================
-- STEP 1: Show events that will be fixed
-- =====================================================================
PRINT '=== EVENTS TO BE FIXED ===';

-- Issue 1: Archived events with IsPublicReviewRequired = True
SELECT 
    'ISSUE 1: Archived events with review required' AS IssueType,
    EventID,
    Name,
    IsPublic,
    PublicReviewStatus,
    IsPublicReviewRequired,
    es.StatusCode AS EventStatusCode,
    es.StatusName AS EventStatusName
FROM [dbo].[Event] e
JOIN [ref].[EventStatus] es ON e.EventStatusID = es.EventStatusID
WHERE es.StatusCode = 'ARCHIVED'
  AND e.IsPublicReviewRequired = 1
  AND e.IsDeleted = 0;

-- Issue 2: Events with IsPublic = True but PublicReviewStatus = NULL
SELECT 
    'ISSUE 2: Public events without review status' AS IssueType,
    EventID,
    Name,
    IsPublic,
    PublicReviewStatus,
    IsPublicReviewRequired,
    es.StatusCode AS EventStatusCode,
    es.StatusName AS EventStatusName
FROM [dbo].[Event] e
JOIN [ref].[EventStatus] es ON e.EventStatusID = es.EventStatusID
WHERE e.IsPublic = 1
  AND (e.PublicReviewStatus IS NULL OR e.PublicReviewStatus NOT IN ('PENDING', 'APPROVED', 'REJECTED'))
  AND e.IsDeleted = 0;

-- Issue 3: Events with IsPublic = False but PublicReviewStatus is set
SELECT 
    'ISSUE 3: Private events with review status' AS IssueType,
    EventID,
    Name,
    IsPublic,
    PublicReviewStatus,
    IsPublicReviewRequired,
    es.StatusCode AS EventStatusCode,
    es.StatusName AS EventStatusName
FROM [dbo].[Event] e
JOIN [ref].[EventStatus] es ON e.EventStatusID = es.EventStatusID
WHERE e.IsPublic = 0
  AND e.PublicReviewStatus IS NOT NULL
  AND e.IsDeleted = 0;

-- Issue 4: Events with PublicReviewStatus = 'APPROVED' but EventStatus != 'PUBLISHED'
SELECT 
    'ISSUE 4: Approved events with wrong EventStatus' AS IssueType,
    EventID,
    Name,
    IsPublic,
    PublicReviewStatus,
    IsPublicReviewRequired,
    es.StatusCode AS EventStatusCode,
    es.StatusName AS EventStatusName
FROM [dbo].[Event] e
JOIN [ref].[EventStatus] es ON e.EventStatusID = es.EventStatusID
WHERE e.PublicReviewStatus = 'APPROVED'
  AND es.StatusCode != 'PUBLISHED'
  AND e.IsDeleted = 0;

-- =====================================================================
-- STEP 2: Fix Issue 1 - Archived events with IsPublicReviewRequired = True
-- =====================================================================
PRINT '=== FIXING ISSUE 1: Archived events ===';

DECLARE @ArchivedStatusID INT;
SELECT @ArchivedStatusID = EventStatusID FROM [ref].[EventStatus] WHERE StatusCode = 'ARCHIVED';

UPDATE [dbo].[Event]
SET 
    -- Clear review status if pending (archived events shouldn't be in review)
    PublicReviewStatus = CASE 
        WHEN PublicReviewStatus = 'PENDING' THEN NULL
        ELSE PublicReviewStatus  -- Keep APPROVED/REJECTED for history
    END,
    -- Clear review requirement
    IsPublicReviewRequired = 0
WHERE EventStatusID = @ArchivedStatusID
  AND IsPublicReviewRequired = 1
  AND IsDeleted = 0;

PRINT 'Archived events fixed: ' + CAST(@@ROWCOUNT AS VARCHAR(10));

-- =====================================================================
-- STEP 3: Fix Issue 2 - Public events without review status
-- =====================================================================
PRINT '=== FIXING ISSUE 2: Public events without review status ===';

DECLARE @PendingReviewStatusID INT;
SELECT @PendingReviewStatusID = EventStatusID FROM [ref].[EventStatus] WHERE StatusCode = 'PENDING_REVIEW';

UPDATE [dbo].[Event]
SET 
    PublicReviewStatus = 'PENDING',
    IsPublicReviewRequired = 1,
    EventStatusID = @PendingReviewStatusID
WHERE IsPublic = 1
  AND (PublicReviewStatus IS NULL OR PublicReviewStatus NOT IN ('PENDING', 'APPROVED', 'REJECTED'))
  AND IsDeleted = 0
  AND EXISTS (SELECT 1 FROM [ref].[EventStatus] WHERE StatusCode = 'PENDING_REVIEW');

PRINT 'Public events without review status fixed: ' + CAST(@@ROWCOUNT AS VARCHAR(10));

-- =====================================================================
-- STEP 4: Fix Issue 3 - Private events with review status
-- =====================================================================
PRINT '=== FIXING ISSUE 3: Private events with review status ===';

UPDATE [dbo].[Event]
SET 
    PublicReviewStatus = NULL,
    IsPublicReviewRequired = 0
WHERE IsPublic = 0
  AND PublicReviewStatus IS NOT NULL
  AND IsDeleted = 0;

PRINT 'Private events with review status fixed: ' + CAST(@@ROWCOUNT AS VARCHAR(10));

-- =====================================================================
-- STEP 5: Fix Issue 4 - Approved events with wrong EventStatus
-- =====================================================================
PRINT '=== FIXING ISSUE 4: Approved events with wrong EventStatus ===';

DECLARE @PublishedStatusID INT;
SELECT @PublishedStatusID = EventStatusID FROM [ref].[EventStatus] WHERE StatusCode = 'PUBLISHED';

UPDATE [dbo].[Event]
SET 
    EventStatusID = @PublishedStatusID,
    IsPublic = 1  -- Ensure approved events are public
WHERE PublicReviewStatus = 'APPROVED'
  AND EventStatusID != @PublishedStatusID
  AND IsDeleted = 0
  AND EXISTS (SELECT 1 FROM [ref].[EventStatus] WHERE StatusCode = 'PUBLISHED');

PRINT 'Approved events with wrong EventStatus fixed: ' + CAST(@@ROWCOUNT AS VARCHAR(10));

-- =====================================================================
-- STEP 6: Fix Issue 5 - Rejected events that are still public
-- =====================================================================
PRINT '=== FIXING ISSUE 5: Rejected events that are still public ===';

DECLARE @DraftStatusID INT;
SELECT @DraftStatusID = EventStatusID FROM [ref].[EventStatus] WHERE StatusCode = 'DRAFT';

UPDATE [dbo].[Event]
SET 
    IsPublic = 0,  -- Rejected events should be private
    EventStatusID = CASE 
        WHEN EventStatusID = @PendingReviewStatusID THEN @DraftStatusID
        ELSE EventStatusID  -- Keep current status if not PENDING_REVIEW
    END
WHERE PublicReviewStatus = 'REJECTED'
  AND IsPublic = 1
  AND IsDeleted = 0
  AND EXISTS (SELECT 1 FROM [ref].[EventStatus] WHERE StatusCode = 'DRAFT');

PRINT 'Rejected events that are still public fixed: ' + CAST(@@ROWCOUNT AS VARCHAR(10));

-- =====================================================================
-- STEP 7: Verify fixes
-- =====================================================================
PRINT '=== VERIFICATION ===';

-- Check for remaining issues
DECLARE @RemainingIssues INT = 0;

-- Count remaining archived events with review required
SELECT @RemainingIssues = @RemainingIssues + COUNT(*)
FROM [dbo].[Event] e
JOIN [ref].[EventStatus] es ON e.EventStatusID = es.EventStatusID
WHERE es.StatusCode = 'ARCHIVED'
  AND e.IsPublicReviewRequired = 1
  AND e.IsDeleted = 0;

-- Count remaining public events without review status
SELECT @RemainingIssues = @RemainingIssues + COUNT(*)
FROM [dbo].[Event] e
WHERE e.IsPublic = 1
  AND (e.PublicReviewStatus IS NULL OR e.PublicReviewStatus NOT IN ('PENDING', 'APPROVED', 'REJECTED'))
  AND e.IsDeleted = 0;

-- Count remaining private events with review status
SELECT @RemainingIssues = @RemainingIssues + COUNT(*)
FROM [dbo].[Event] e
WHERE e.IsPublic = 0
  AND e.PublicReviewStatus IS NOT NULL
  AND e.IsDeleted = 0;

-- Count remaining approved events with wrong status
SELECT @RemainingIssues = @RemainingIssues + COUNT(*)
FROM [dbo].[Event] e
JOIN [ref].[EventStatus] es ON e.EventStatusID = es.EventStatusID
WHERE e.PublicReviewStatus = 'APPROVED'
  AND es.StatusCode != 'PUBLISHED'
  AND e.IsDeleted = 0;

IF @RemainingIssues > 0
BEGIN
    PRINT 'WARNING: ' + CAST(@RemainingIssues AS VARCHAR(10)) + ' issues remaining. Review manually.';
END
ELSE
BEGIN
    PRINT 'SUCCESS: All issues fixed!';
END

-- Show summary
SELECT 
    PublicReviewStatus,
    COUNT(*) AS Count,
    SUM(CASE WHEN IsPublic = 1 THEN 1 ELSE 0 END) AS PublicEvents,
    SUM(CASE WHEN IsPublic = 0 THEN 1 ELSE 0 END) AS PrivateEvents
FROM [dbo].[Event]
WHERE IsDeleted = 0
GROUP BY PublicReviewStatus
ORDER BY PublicReviewStatus;

-- If everything looks good, uncomment the COMMIT line below
-- COMMIT;

-- To rollback if needed:
-- ROLLBACK;

PRINT 'Script completed. Review the results and COMMIT if correct.';
GO

