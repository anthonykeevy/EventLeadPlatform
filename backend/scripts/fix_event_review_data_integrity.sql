-- =====================================================================
-- Fix Event Review Data Integrity Issues
-- =====================================================================
-- Story: 2.7 - Event Public Review Workflow Implementation
-- Purpose: Fix inconsistent records in the Event table
-- 
-- This script fixes:
-- 1. Events with IsPublicReviewRequired=True and EventStatusID=ARCHIVED
-- 2. Events with IsPublic=True but PublicReviewStatusID=NULL
-- 3. Invalid state combinations (private events with review status)
-- 4. Rejected events with IsSharedWithPlatform=True
-- 
-- Usage:
--   1. Review the queries in dry-run mode (commented SELECT statements)
--   2. Uncomment the UPDATE statements when ready to apply fixes
--   3. Run each section one at a time
-- =====================================================================

USE [EventLeadPlatform];
GO

-- =====================================================================
-- Issue 1: Archived events with IsPublicReviewRequired=True
-- =====================================================================

-- DRY-RUN: Check what will be fixed
SELECT 
    e.EventID,
    e.Name,
    e.IsPublic,
    e.IsSharedWithPlatform,
    e.IsPublicReviewRequired,
    e.PublicReviewStatusID,
    e.EventStatusID,
    es.StatusCode AS EventStatusCode
FROM [dbo].[Event] e
INNER JOIN [ref].[EventStatus] es ON e.EventStatusID = es.EventStatusID
WHERE e.IsPublicReviewRequired = 1
    AND es.StatusCode = 'ARCHIVED'
    AND e.IsDeleted = 0;

-- FIX: Update archived events
-- Uncomment to apply fix:
/*
UPDATE e
SET 
    e.IsPublicReviewRequired = 0,
    e.IsSharedWithPlatform = 0,
    e.PublicReviewStatusID = CASE 
        WHEN e.PublicReviewStatusID = (SELECT PublicReviewStatusID FROM [ref].[PublicReviewStatus] WHERE StatusCode = 'PENDING')
        THEN NULL 
        ELSE e.PublicReviewStatusID 
    END,
    e.UpdatedDate = GETUTCDATE()
FROM [dbo].[Event] e
INNER JOIN [ref].[EventStatus] es ON e.EventStatusID = es.EventStatusID
WHERE e.IsPublicReviewRequired = 1
    AND es.StatusCode = 'ARCHIVED'
    AND e.IsDeleted = 0;
*/

-- =====================================================================
-- Issue 2: Public events with IsPublic=True but PublicReviewStatusID=NULL
-- =====================================================================

-- DRY-RUN: Check what will be fixed
SELECT 
    e.EventID,
    e.Name,
    e.IsPublic,
    e.IsSharedWithPlatform,
    e.PublicReviewStatusID,
    e.IsPublicReviewRequired
FROM [dbo].[Event] e
WHERE e.IsPublic = 1
    AND e.PublicReviewStatusID IS NULL
    AND e.IsDeleted = 0;

-- FIX: Update public events without review status
-- Uncomment to apply fix:
/*
-- For platform-sharing events: Set PublicReviewStatusID=PENDING
UPDATE e
SET 
    e.PublicReviewStatusID = (SELECT PublicReviewStatusID FROM [ref].[PublicReviewStatus] WHERE StatusCode = 'PENDING'),
    e.IsPublicReviewRequired = 1,
    e.UpdatedDate = GETUTCDATE()
FROM [dbo].[Event] e
WHERE e.IsPublic = 1
    AND e.PublicReviewStatusID IS NULL
    AND e.IsSharedWithPlatform = 1
    AND e.IsDeleted = 0;

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
*/

-- =====================================================================
-- Issue 3: Invalid state combinations
-- =====================================================================

-- DRY-RUN: Check what will be fixed
-- Case 1: Private events with PublicReviewStatusID set
SELECT 
    e.EventID,
    e.Name,
    e.IsPublic,
    e.PublicReviewStatusID,
    e.IsSharedWithPlatform,
    e.IsPublicReviewRequired,
    prs.StatusCode AS ReviewStatusCode
FROM [dbo].[Event] e
LEFT JOIN [ref].[PublicReviewStatus] prs ON e.PublicReviewStatusID = prs.PublicReviewStatusID
WHERE e.IsPublic = 0
    AND e.PublicReviewStatusID IS NOT NULL
    AND e.IsDeleted = 0;

-- Case 2: Private events with IsSharedWithPlatform=True
SELECT 
    e.EventID,
    e.Name,
    e.IsPublic,
    e.IsSharedWithPlatform,
    e.IsPublicReviewRequired
FROM [dbo].[Event] e
WHERE e.IsPublic = 0
    AND e.IsSharedWithPlatform = 1
    AND e.IsDeleted = 0;

-- Case 3: Private events with IsPublicReviewRequired=True
SELECT 
    e.EventID,
    e.Name,
    e.IsPublic,
    e.IsPublicReviewRequired
FROM [dbo].[Event] e
WHERE e.IsPublic = 0
    AND e.IsPublicReviewRequired = 1
    AND e.IsDeleted = 0;

-- FIX: Clear all review-related fields for private events
-- Uncomment to apply fix:
/*
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
*/

-- =====================================================================
-- Issue 4: Rejected events with IsSharedWithPlatform=True
-- =====================================================================

-- DRY-RUN: Check what will be fixed
SELECT 
    e.EventID,
    e.Name,
    e.IsPublic,
    e.IsSharedWithPlatform,
    e.PublicReviewStatusID,
    prs.StatusCode AS ReviewStatusCode
FROM [dbo].[Event] e
INNER JOIN [ref].[PublicReviewStatus] prs ON e.PublicReviewStatusID = prs.PublicReviewStatusID
WHERE prs.StatusCode = 'REJECTED'
    AND e.IsSharedWithPlatform = 1
    AND e.IsDeleted = 0;

-- FIX: Set IsSharedWithPlatform=False for rejected events
-- Uncomment to apply fix:
/*
UPDATE e
SET 
    e.IsSharedWithPlatform = 0,
    e.UpdatedDate = GETUTCDATE()
FROM [dbo].[Event] e
INNER JOIN [ref].[PublicReviewStatus] prs ON e.PublicReviewStatusID = prs.PublicReviewStatusID
WHERE prs.StatusCode = 'REJECTED'
    AND e.IsSharedWithPlatform = 1
    AND e.IsDeleted = 0;
*/

-- =====================================================================
-- Summary Query: Check all issues at once
-- =====================================================================

SELECT 
    'Issue 1: Archived with review required' AS IssueType,
    COUNT(*) AS Count
FROM [dbo].[Event] e
INNER JOIN [ref].[EventStatus] es ON e.EventStatusID = es.EventStatusID
WHERE e.IsPublicReviewRequired = 1
    AND es.StatusCode = 'ARCHIVED'
    AND e.IsDeleted = 0

UNION ALL

SELECT 
    'Issue 2: Public without review status' AS IssueType,
    COUNT(*) AS Count
FROM [dbo].[Event]
WHERE IsPublic = 1
    AND IsSharedWithPlatform = 1
    AND PublicReviewStatusID IS NULL
    AND IsDeleted = 0

UNION ALL

SELECT 
    'Issue 3: Invalid state combinations' AS IssueType,
    COUNT(DISTINCT EventID) AS Count
FROM [dbo].[Event]
WHERE IsPublic = 0
    AND (
        PublicReviewStatusID IS NOT NULL
        OR IsSharedWithPlatform = 1
        OR IsPublicReviewRequired = 1
    )
    AND IsDeleted = 0

UNION ALL

SELECT 
    'Issue 4: Rejected with platform sharing' AS IssueType,
    COUNT(*) AS Count
FROM [dbo].[Event] e
INNER JOIN [ref].[PublicReviewStatus] prs ON e.PublicReviewStatusID = prs.PublicReviewStatusID
WHERE prs.StatusCode = 'REJECTED'
    AND e.IsSharedWithPlatform = 1
    AND e.IsDeleted = 0;

GO

-- =====================================================================
-- Verify fixes after running UPDATE statements
-- =====================================================================

-- Run this after applying fixes to verify all issues are resolved
SELECT 
    'Remaining Issues' AS Status,
    COUNT(*) AS Count
FROM (
    -- Issue 1
    SELECT EventID FROM [dbo].[Event] e
    INNER JOIN [ref].[EventStatus] es ON e.EventStatusID = es.EventStatusID
    WHERE e.IsPublicReviewRequired = 1 AND es.StatusCode = 'ARCHIVED' AND e.IsDeleted = 0
    
    UNION
    
    -- Issue 2
    SELECT EventID FROM [dbo].[Event]
    WHERE IsPublic = 1 AND IsSharedWithPlatform = 1 AND PublicReviewStatusID IS NULL AND IsDeleted = 0
    
    UNION
    
    -- Issue 3
    SELECT EventID FROM [dbo].[Event]
    WHERE IsPublic = 0 AND (PublicReviewStatusID IS NOT NULL OR IsSharedWithPlatform = 1 OR IsPublicReviewRequired = 1)
    AND IsDeleted = 0
    
    UNION
    
    -- Issue 4
    SELECT e.EventID FROM [dbo].[Event] e
    INNER JOIN [ref].[PublicReviewStatus] prs ON e.PublicReviewStatusID = prs.PublicReviewStatusID
    WHERE prs.StatusCode = 'REJECTED' AND e.IsSharedWithPlatform = 1 AND e.IsDeleted = 0
) AS Issues;

GO

