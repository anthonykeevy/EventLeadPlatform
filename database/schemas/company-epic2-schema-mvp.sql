-- =====================================================================
-- Company Domain Epic 2 Schema - SIMPLIFIED FOR MVP
-- Enhanced Billing Relationships & Approval Workflows
-- =====================================================================
-- Author: Dimitri (Data Domain Architect)
-- Date: January 15, 2025
-- Version: 3.0.0 (SIMPLIFIED FOR MVP)
-- =====================================================================
-- Purpose:
--   Epic 2 enhancements to Company domain - SIMPLIFIED FOR MVP:
--   1. Core approval workflow with single approver per relationship
--   2. External approver support (email-only approvers)
--   3. New user roles for relationship types
--   4. Complete audit trail for compliance
--   5. Maintains hierarchical dashboard view for all users
-- 
-- Strategy:
--   SIMPLIFIED MVP APPROACH - Focus on core functionality:
--   - Single approver per relationship type (no escalation chains)
--   - External approvers via email only
--   - Complete audit trail
--   - Defer complex features to future releases
-- =====================================================================
-- MVP Scope Decisions:
--   - REMOVED: EscalationChain table (too complex for MVP)
--   - REMOVED: FormAccessControl table (defer to Form domain)
--   - REMOVED: Complex escalation logic (manual escalation only)
--   - FOCUSED: Core approval workflow with single approver per relationship
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

-- Create indexes for new fields
CREATE INDEX IX_CompanySwitchRequest_Urgency ON [dbo].[CompanySwitchRequest](UrgencyLevel, RequestedAt)
    WHERE UrgencyLevel IS NOT NULL;
GO

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
(5, 'BillingChange', 'Request approval for billing relationship changes', 1),
(6, 'AccessRequest', 'Request access to company resources', 1),
(7, 'FormAccess', 'Request access to specific forms', 1);
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
(5, 'UnderReview', 'Request under detailed review', 1),
(6, 'PendingApprover', 'Waiting for specific approver', 1),
(7, 'EscalationRequired', 'Escalation needed - approver unavailable', 1);
GO

PRINT 'CompanySwitchRequestStatus table extended successfully!';
GO

-- =====================================================================
-- 4. EXTEND User TABLE FOR EXTERNAL APPROVERS
-- =====================================================================
-- Purpose: Support external approvers who don't have platform accounts
-- Strategy: Extend existing User table with simple flag
-- =====================================================================

ALTER TABLE [dbo].[User] ADD
    -- =====================================================================
    -- External Approver Field
    -- =====================================================================
    IsExternalApprover BIT NOT NULL DEFAULT 0;
    -- ^ Flag indicating if user is external approver (no platform account)
    -- 0 = Platform user (normal user)
    -- 1 = External approver (email-only approval)
GO

-- Create index for external approvers
CREATE INDEX IX_User_ExternalApprover ON [dbo].[User](IsExternalApprover)
    WHERE IsExternalApprover = 1;
GO

PRINT 'User table extended for external approvers successfully!';
GO

-- =====================================================================
-- 5. EXTEND UserRole REFERENCE TABLE
-- =====================================================================
-- Purpose: Add new user roles for relationship types
-- =====================================================================

-- Add new user roles for Epic 2
INSERT INTO [ref].[UserRole] (RoleCode, RoleName, Description, RoleLevel, CanManagePlatform, CanManageAllCompanies, CanViewAllData, CanAssignSystemRoles, IsActive, SortOrder) VALUES
('HEAD_OFFICE_ADMIN', 'Head Office Administrator', 'Manages company relationships and approval workflows', 10, 0, 1, 1, 1, 1, 10),
('PARTNER_USER', 'Partner User', 'Form-level access to partner companies', 5, 0, 0, 0, 0, 1, 50),
('VENDOR_USER', 'Vendor User', 'Form-level access to vendor relationships', 5, 0, 0, 0, 0, 1, 51),
('CLIENT_USER', 'Client User', 'View-only access to assigned forms', 3, 0, 0, 0, 0, 1, 52),
('AFFILIATE_USER', 'Affiliate User', 'Form-level access to affiliate relationships', 5, 0, 0, 0, 0, 1, 53),
('EXTERNAL_APPROVER', 'External Approver', 'Email-only approver without platform access', 7, 0, 0, 0, 0, 1, 40);
GO

PRINT 'UserRole table extended successfully!';
GO

-- =====================================================================
-- PHASE 2: CREATE NEW TABLES
-- =====================================================================

-- =====================================================================
-- 6. CREATE ApprovalAuditTrail TABLE
-- =====================================================================
-- Purpose: Complete audit trail for all approval actions (compliance)
-- Key Insight: Immutable audit log - never updated, only inserted
-- Schema: audit (as per user requirements)
-- =====================================================================
CREATE TABLE [audit].[ApprovalAuditTrail] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    ApprovalAuditTrailID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Request Reference
    -- =====================================================================
    CompanySwitchRequestID BIGINT NOT NULL,
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
    CONSTRAINT FK_ApprovalAuditTrail_Request FOREIGN KEY (CompanySwitchRequestID) 
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
        (PreviousStatus IS NULL OR PreviousStatus IN ('Pending', 'Approved', 'Rejected', 'Escalated', 'UnderReview', 'PendingApprover', 'EscalationRequired')) AND
        (NewStatus IS NULL OR NewStatus IN ('Pending', 'Approved', 'Rejected', 'Escalated', 'UnderReview', 'PendingApprover', 'EscalationRequired'))
    )
);
GO

-- Index for workflow audit history
CREATE INDEX IX_ApprovalAuditTrail_Request ON [audit].[ApprovalAuditTrail](CompanySwitchRequestID, ActionDate);
GO

-- Index for user action history
CREATE INDEX IX_ApprovalAuditTrail_User ON [audit].[ApprovalAuditTrail](PerformedBy, ActionDate);
GO

-- Index for action type queries
CREATE INDEX IX_ApprovalAuditTrail_Action ON [audit].[ApprovalAuditTrail](Action, ActionDate);
GO

PRINT 'ApprovalAuditTrail table created successfully!';
GO

-- =====================================================================
-- PHASE 3: CREATE HELPER FUNCTIONS
-- =====================================================================

-- =====================================================================
-- 7. CREATE Urgency Calculation Function
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
-- 8. CREATE Approval Threshold Function
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
PRINT 'SIMPLIFIED MVP APPROACH:';
PRINT '';
PRINT 'Extended Tables:';
PRINT '  1. CompanySwitchRequest (added 4 fields)';
PRINT '  2. CompanySwitchRequestType (added 4 types)';
PRINT '  3. CompanySwitchRequestStatus (added 4 statuses)';
PRINT '  4. User (added 1 field for external approvers)';
PRINT '  5. UserRole (added 6 new roles)';
PRINT '';
PRINT 'New Tables:';
PRINT '  6. ApprovalAuditTrail (audit schema - 8 fields)';
PRINT '';
PRINT 'New Functions:';
PRINT '  7. CalculateUrgencyLevel (urgency calculation)';
PRINT '  8. GetApprovalLevel (approval threshold)';
PRINT '';
PRINT 'Key Features:';
PRINT '  ✅ Simple approval workflow (single approver per relationship)';
PRINT '  ✅ External approver support (email-only)';
PRINT '  ✅ New user roles for relationship types';
PRINT '  ✅ Complete audit trail (audit schema)';
PRINT '  ✅ Dashboard consistency maintained';
PRINT '  ✅ Backward compatible with Epic 1';
PRINT '';
PRINT 'MVP Scope Decisions:';
PRINT '  ✅ REMOVED: EscalationChain table (too complex for MVP)';
PRINT '  ✅ REMOVED: FormAccessControl table (defer to Form domain)';
PRINT '  ✅ REMOVED: Complex escalation logic (manual escalation only)';
PRINT '  ✅ FOCUSED: Core approval workflow with single approver per relationship';
PRINT '';
PRINT 'Next Steps:';
PRINT '  1. Sally UX review (completed and incorporated)';
PRINT '  2. Solomon schema validation (Database Migration Validator)';
PRINT '  3. Developer implementation planning';
PRINT '  4. Epic 2 testing strategy with basic approval scenarios';
PRINT '========================================';
GO
