-- =====================================================================
-- CREATE PublicReviewStatus REFERENCE TABLE
-- =====================================================================
-- Purpose: Reference table for public event review status
-- Schema: ref.PublicReviewStatus
-- Story: 2.6 - Admin Public Event Review Workflow
-- =====================================================================

USE [EventLeadPlatform];
GO

-- =====================================================================
-- CREATE PublicReviewStatus REFERENCE TABLE
-- =====================================================================
CREATE TABLE [ref].[PublicReviewStatus] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    PublicReviewStatusID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Status Identity
    -- =====================================================================
    StatusCode NVARCHAR(20) NOT NULL UNIQUE,
    -- ^ Status code for system use
    -- Examples: 'PENDING', 'APPROVED', 'REJECTED'
    
    StatusName NVARCHAR(50) NOT NULL,
    -- ^ Human-readable status name
    -- Examples: 'Pending Review', 'Approved', 'Rejected'
    
    StatusDescription NVARCHAR(200) NULL,
    -- ^ Detailed description of status
    -- Example: 'Event is awaiting admin review for public visibility'
    
    -- =====================================================================
    -- Dashboard Visual Elements
    -- =====================================================================
    StatusColor NVARCHAR(7) NULL,
    -- ^ Hex color code for dashboard display
    -- Examples: '#FFC107' (yellow for pending), '#28A745' (green for approved), '#DC3545' (red for rejected)
    
    StatusIcon NVARCHAR(50) NULL,
    -- ^ Icon name for dashboard display
    -- Examples: 'pending-icon', 'approved-icon', 'rejected-icon'
    
    -- =====================================================================
    -- Configuration
    -- =====================================================================
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 0,
    
    -- =====================================================================
    -- Audit Trail
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,
    
    CONSTRAINT FK_PublicReviewStatus_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_PublicReviewStatus_UpdatedBy FOREIGN KEY (UpdatedBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_PublicReviewStatus_DeletedBy FOREIGN KEY (DeletedBy) 
        REFERENCES [dbo].[User](UserID)
);
GO

-- Insert default public review statuses
-- All statuses required by workflow: PENDING, APPROVED, REJECTED
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

PRINT 'PublicReviewStatus reference table created successfully!';
GO


