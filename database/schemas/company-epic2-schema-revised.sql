-- =====================================================================
-- Company Domain Epic 2 Schema - REVISED FOR EXISTING SCHEMA
-- Enhanced Billing Relationships & Approval Workflows
-- =====================================================================
-- Author: Dimitri (Data Domain Architect)
-- Date: January 15, 2025
-- Version: 2.1.0 (REVISED)
-- =====================================================================
-- Purpose:
--   Epic 2 enhancements to Company domain using EXISTING tables:
--   1. Extend CompanySwitchRequest for form deployment approval workflows
--   2. Use existing CompanyRelationship for billing relationships
--   3. Add ApprovalAuditTrail for complete audit trail
--   4. Maintain Epic 1 schema integrity (no breaking changes)
-- 
-- Strategy:
--   REVISED APPROACH - Extend existing tables instead of creating new ones:
--   - Extend CompanySwitchRequest (add fields for form deployment)
--   - Use CompanyRelationship (already handles parent-child relationships)
--   - Add ApprovalAuditTrail (new table for audit compliance)
--   - Extend reference tables (add new request types and statuses)
-- =====================================================================
-- Industry Research:
--   - Salesforce: Parent-child account hierarchies with centralized billing
--   - Microsoft Azure: Cost center-based approval workflows with escalation
--   - Enterprise SaaS: Threshold-based routing ($0-1K auto, $1K-5K manager, $5K+ exec)
--   - Audit Requirements: Complete trail for SOX compliance
-- =====================================================================

USE [EventLeadPlatform];
GO

-- =====================================================================
-- PHASE 1: EXTEND EXISTING TABLES
-- =====================================================================

-- =====================================================================
-- 1. EXTEND CompanySwitchRequest TABLE
-- =====================================================================
-- Purpose: Add fields for form deployment approval workflows
-- Strategy: Extend existing table rather than create new one
-- =====================================================================

ALTER TABLE [dbo].[CompanySwitchRequest] ADD
    -- =====================================================================
    -- Form Deployment Fields
    -- =====================================================================
    RequestedAmount DECIMAL(10,2) NULL,
    -- ^ Cost amount for form deployment (NULL if not applicable)
    -- Example: $500.00 for form deployment costs
    -- Used for: Budget validation, approval thresholds
    
    RequestDescription NVARCHAR(MAX) NULL,
    -- ^ Detailed description of what's being requested
    -- Example: "Deploy customer feedback form for Q1 survey campaign"
    -- Required: Approvers need context to make decisions
    
    EventDate DATETIME2 NULL,
    -- ^ Event date for urgency calculation (NULL if no event)
    -- Used for: Urgency calculation (EventDate - today)
    -- Business rule: Urgent if < 7 days away
    
    UrgencyLevel NVARCHAR(20) NULL;
    -- ^ Calculated urgency: 'Low', 'Medium', 'High'
    -- Low = EventDate > 30 days away
    -- Medium = EventDate 7-30 days away  
    -- High = EventDate < 7 days away
    -- NULL = No event date (default to Medium)
GO

-- Add constraints for new fields
ALTER TABLE [dbo].[CompanySwitchRequest] ADD
    -- Validate UrgencyLevel values
    CONSTRAINT CK_CompanySwitchRequest_UrgencyLevel CHECK (
        UrgencyLevel IS NULL OR UrgencyLevel IN ('Low', 'Medium', 'High')
    ),
    
    -- Validate RequestedAmount is positive
    CONSTRAINT CK_CompanySwitchRequest_Amount CHECK (
        RequestedAmount IS NULL OR RequestedAmount >= 0
    );
GO

-- Create index for urgency-based queries
CREATE INDEX IX_CompanySwitchRequest_Urgency ON [dbo].[CompanySwitchRequest](UrgencyLevel, RequestedAt)
    WHERE UrgencyLevel IS NOT NULL;
GO

-- Create index for amount-based queries
CREATE INDEX IX_CompanySwitchRequest_Amount ON [dbo].[CompanySwitchRequest](RequestedAmount, RequestedAt)
    WHERE RequestedAmount IS NOT NULL;
GO

PRINT 'CompanySwitchRequest table extended successfully!';
GO

-- =====================================================================
-- 2. EXTEND CompanySwitchRequestType REFERENCE TABLE
-- =====================================================================
-- Purpose: Add new request types for Epic 2 workflows
-- =====================================================================

-- Add new request types for Epic 2
INSERT INTO [ref].[CompanySwitchRequestType] VALUES
(4, 'FormDeployment', 'Request approval for form deployment costs', 1),
(5, 'BillingChange', 'Request approval for billing relationship changes', 1);
GO

PRINT 'CompanySwitchRequestType table extended successfully!';
GO

-- =====================================================================
-- 3. EXTEND CompanySwitchRequestStatus REFERENCE TABLE
-- =====================================================================
-- Purpose: Add new status types for Epic 2 workflows
-- =====================================================================

-- Add new status types for Epic 2
INSERT INTO [ref].[CompanySwitchRequestStatus] VALUES
(4, 'Escalated', 'Request escalated to higher authority', 1),
(5, 'UnderReview', 'Request under detailed review', 1);
GO

PRINT 'CompanySwitchRequestStatus table extended successfully!';
GO

-- =====================================================================
-- PHASE 2: CREATE NEW AUDIT TRAIL TABLE
-- =====================================================================

-- =====================================================================
-- 4. CREATE ApprovalAuditTrail TABLE
-- =====================================================================
-- Purpose: Complete audit trail for all approval actions (compliance)
-- Key Insight: Immutable audit log - never updated, only inserted
-- =====================================================================
CREATE TABLE [dbo].[ApprovalAuditTrail] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    AuditID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Request Reference
    -- =====================================================================
    RequestID BIGINT NOT NULL,
    -- ^ Link to CompanySwitchRequest record
    -- Used for: Tracking all actions on a specific approval request
    
    -- =====================================================================
    -- Action Details
    -- =====================================================================
    Action NVARCHAR(50) NOT NULL,
    -- ^ Action performed: 'Submitted', 'Approved', 'Rejected', 'Escalated', 'Commented', 'Viewed'
    -- Submitted = Request was created
    -- Approved = Request was approved
    -- Rejected = Request was rejected
    -- Escalated = Request moved to higher authority
    -- Commented = Additional comments added
    -- Viewed = Request was viewed by approver
    
    ActionDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    -- ^ When action was performed (UTC)
    -- Used for: Timeline reconstruction, SLA tracking
    
    PerformedBy BIGINT NOT NULL,
    -- ^ User who performed the action (foreign key to User)
    -- Used for: Accountability, compliance reporting
    
    Comments NVARCHAR(MAX) NULL,
    -- ^ Additional comments or notes about this action
    -- Example: "Approved - within budget limits"
    -- Optional: Provides context for audit reviewers
    
    -- =====================================================================
    -- Status Tracking
    -- =====================================================================
    PreviousStatus NVARCHAR(20) NULL,
    -- ^ Status before this action (for state transitions)
    -- Example: 'Pending' → 'Approved'
    
    NewStatus NVARCHAR(20) NULL,
    -- ^ Status after this action (for state transitions)
    -- Example: 'Pending' → 'Approved'
    
    -- =====================================================================
    -- Audit Trail (Immutable - Never Updated)
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NOT NULL,
    -- Note: No UpdatedDate/UpdatedBy - audit trail is immutable
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT FK_ApprovalAuditTrail_Request FOREIGN KEY (RequestID) 
        REFERENCES [dbo].[CompanySwitchRequest](RequestID),
    
    CONSTRAINT FK_ApprovalAuditTrail_PerformedBy FOREIGN KEY (PerformedBy) 
        REFERENCES [dbo].[User](UserID),
    
    CONSTRAINT FK_ApprovalAuditTrail_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [dbo].[User](UserID),
    
    -- Validate Action values
    CONSTRAINT CK_ApprovalAuditTrail_Action CHECK (
        Action IN ('Submitted', 'Approved', 'Rejected', 'Escalated', 'Commented', 'Viewed')
    ),
    
    -- Validate Status values
    CONSTRAINT CK_ApprovalAuditTrail_Status CHECK (
        (PreviousStatus IS NULL OR PreviousStatus IN ('Pending', 'Approved', 'Rejected', 'Escalated', 'UnderReview')) AND
        (NewStatus IS NULL OR NewStatus IN ('Pending', 'Approved', 'Rejected', 'Escalated', 'UnderReview'))
    )
);
GO

-- Index for workflow audit history
CREATE INDEX IX_ApprovalAuditTrail_Request ON [dbo].[ApprovalAuditTrail](RequestID, ActionDate);
GO

-- Index for user action history
CREATE INDEX IX_ApprovalAuditTrail_User ON [dbo].[ApprovalAuditTrail](PerformedBy, ActionDate);
GO

-- Index for action type queries
CREATE INDEX IX_ApprovalAuditTrail_Action ON [dbo].[ApprovalAuditTrail](Action, ActionDate);
GO

PRINT 'ApprovalAuditTrail table created successfully!';
GO

-- =====================================================================
-- PHASE 3: CREATE HELPER FUNCTIONS
-- =====================================================================

-- =====================================================================
-- 5. CREATE Urgency Calculation Function
-- =====================================================================
-- Purpose: Calculate urgency level based on event date
-- =====================================================================
CREATE FUNCTION [dbo].[CalculateUrgencyLevel](@EventDate DATETIME2)
RETURNS NVARCHAR(20)
AS
BEGIN
    DECLARE @UrgencyLevel NVARCHAR(20);
    
    IF @EventDate IS NULL
        SET @UrgencyLevel = 'Medium';  -- Default for no event date
    ELSE IF DATEDIFF(DAY, GETUTCDATE(), @EventDate) < 7
        SET @UrgencyLevel = 'High';    -- Urgent: < 7 days
    ELSE IF DATEDIFF(DAY, GETUTCDATE(), @EventDate) <= 30
        SET @UrgencyLevel = 'Medium';   -- Moderate: 7-30 days
    ELSE
        SET @UrgencyLevel = 'Low';     -- Low: > 30 days
    
    RETURN @UrgencyLevel;
END;
GO

PRINT 'Urgency calculation function created successfully!';
GO

-- =====================================================================
-- 6. CREATE Approval Threshold Function
-- =====================================================================
-- Purpose: Determine approval level based on amount
-- =====================================================================
CREATE FUNCTION [dbo].[GetApprovalLevel](@Amount DECIMAL(10,2))
RETURNS NVARCHAR(20)
AS
BEGIN
    DECLARE @ApprovalLevel NVARCHAR(20);
    
    IF @Amount IS NULL OR @Amount = 0
        SET @ApprovalLevel = 'Auto';      -- No amount = auto approve
    ELSE IF @Amount <= 1000
        SET @ApprovalLevel = 'Manager';   -- $0-1K = Manager approval
    ELSE IF @Amount <= 5000
        SET @ApprovalLevel = 'Director';  -- $1K-5K = Director approval
    ELSE
        SET @ApprovalLevel = 'Executive'; -- $5K+ = Executive approval
    
    RETURN @ApprovalLevel;
END;
GO

PRINT 'Approval threshold function created successfully!';
GO

-- =====================================================================
-- SUMMARY
-- =====================================================================
PRINT '========================================';
PRINT 'Company Domain Epic 2 Schema Complete!';
PRINT '========================================';
PRINT 'REVISED APPROACH - Using Existing Tables:';
PRINT '';
PRINT 'Extended Tables:';
PRINT '  1. CompanySwitchRequest (added 4 fields)';
PRINT '  2. CompanySwitchRequestType (added 2 types)';
PRINT '  3. CompanySwitchRequestStatus (added 2 statuses)';
PRINT '';
PRINT 'New Tables:';
PRINT '  4. ApprovalAuditTrail (audit trail - 10 fields)';
PRINT '';
PRINT 'New Functions:';
PRINT '  5. CalculateUrgencyLevel (urgency calculation)';
PRINT '  6. GetApprovalLevel (approval threshold)';
PRINT '';
PRINT 'Existing Tables Used (No Changes):';
PRINT '  - CompanyRelationship (parent-child relationships)';
PRINT '  - CompanyRelationshipType (branch, subsidiary, partner)';
PRINT '';
PRINT 'Key Benefits:';
PRINT '  ✅ Minimal schema changes (1 new table vs 3 originally)';
PRINT '  ✅ Leverages existing CompanySwitchRequest workflow';
PRINT '  ✅ Uses existing CompanyRelationship for billing';
PRINT '  ✅ Complete audit trail for compliance';
PRINT '  ✅ Industry-standard approval patterns';
PRINT '  ✅ Backward compatible with Epic 1';
PRINT '';
PRINT 'Next Steps:';
PRINT '  1. Sally UX review (approval interface design)';
PRINT '  2. Solomon schema validation (Database Migration Validator)';
PRINT '  3. Developer implementation planning';
PRINT '  4. Epic 2 testing strategy';
PRINT '========================================';
GO
