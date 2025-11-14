-- =====================================================================
-- Fix Existing Public Events Review Status
-- =====================================================================
-- Purpose: Set PublicReviewStatus = 'PENDING' for existing events that
--          have IsPublic = True but PublicReviewStatus is NULL
--          This ensures existing public events show up in admin review queue
-- =====================================================================
-- Story 2.6: Admin Public Event Review Workflow
-- =====================================================================

BEGIN TRANSACTION;

-- Show events that will be updated
SELECT 
    EventID,
    Name,
    IsPublic,
    PublicReviewStatus,
    PublicReviewDate,
    EventStatusID,
    CreatedDate
FROM [dbo].[Event]
WHERE IsPublic = 1 
  AND (PublicReviewStatus IS NULL OR PublicReviewStatus NOT IN ('PENDING', 'APPROVED', 'REJECTED'))
  AND IsDeleted = 0
ORDER BY CreatedDate DESC;

-- Update events: Set PublicReviewStatus = 'PENDING' for public events without review status
UPDATE [dbo].[Event]
SET 
    PublicReviewStatus = 'PENDING',
    IsPublicReviewRequired = 1,
    -- Set EventStatusID to PENDING_REVIEW if not already set
    EventStatusID = (
        SELECT EventStatusID 
        FROM [ref].[EventStatus] 
        WHERE StatusCode = 'PENDING_REVIEW'
    )
WHERE IsPublic = 1 
  AND (PublicReviewStatus IS NULL OR PublicReviewStatus NOT IN ('PENDING', 'APPROVED', 'REJECTED'))
  AND IsDeleted = 0
  -- Only update if PENDING_REVIEW status exists
  AND EXISTS (SELECT 1 FROM [ref].[EventStatus] WHERE StatusCode = 'PENDING_REVIEW');

-- Show count of updated events
SELECT @@ROWCOUNT AS EventsUpdated;

-- Verify the update
SELECT 
    EventID,
    Name,
    IsPublic,
    PublicReviewStatus,
    EventStatusID,
    CreatedDate
FROM [dbo].[Event]
WHERE IsPublic = 1 
  AND PublicReviewStatus = 'PENDING'
  AND IsDeleted = 0
ORDER BY CreatedDate DESC;

-- If everything looks good, uncomment the COMMIT line below
-- COMMIT;

-- To rollback if needed:
-- ROLLBACK;

PRINT 'Script completed. Review the results and COMMIT if correct.';
GO

