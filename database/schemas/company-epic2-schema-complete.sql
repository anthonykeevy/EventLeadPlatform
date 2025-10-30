-- =====================================================================
-- Company Domain Epic 2 Schema - COMPLETE WITH UX REFINEMENTS
-- Enhanced Billing Relationships & Approval Workflows
-- =====================================================================
-- Author: Dimitri (Data Domain Architect)
-- Date: January 15, 2025
-- Version: 2.2.0 (COMPLETE WITH UX REFINEMENTS)
-- =====================================================================
-- Purpose:
--   Epic 2 enhancements to Company domain incorporating UX expert feedback:
--   1. Complete escalation chain support with external approvers
--   2. Form-level access control for external relationships
--   3. External approver support (email-only approvers)
--   4. New system roles for relationship types
--   5. Maintains hierarchical dashboard view for all users
-- 
-- Strategy:
--   COMPLETE SOLUTION - Extends existing tables + adds new tables for:
--   - Escalation chain management
--   - Form-level access control
--   - External approver support
--   - Enhanced audit trail
-- =====================================================================
-- UX Expert Input Incorporated:
--   - Sally's feedback on escalation handling
--   - Form-level access for partners/vendors/clients
--   - External approver support without platform accounts
--   - Dashboard consistency maintained
--   - Role-based access control
-- =====================================================================

USE [EventLeadPlatform];
GO

-- =====================================================================
-- PHASE 1: EXTEND EXISTING TABLES
-- =====================================================================

-- =====================================================================
-- 1. EXTEND CompanySwitchRequest TABLE
-- =====================================================================
-- Purpose: Add fields for form deployment approval workflows + escalation
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
    
    UrgencyLevel NVARCHAR(20) NULL,
    -- ^ Calculated urgency: 'Low', 'Medium', 'High'
    -- Low = EventDate > 30 days away
    -- Medium = EventDate 7-30 days away  
    -- High = EventDate < 7 days away
    -- NULL = No event date (default to Medium)
    
    -- =====================================================================
    -- Escalation Chain Fields
    -- =====================================================================
    EscalationChain NVARCHAR(MAX) NULL,
    -- ^ JSON array of escalation chain for this request
    -- Example: [{"Level":1,"ApproverID":123,"Email":"manager@company.com","Hours":48}]
    -- Used for: Tracking escalation path and current approver
    
    CurrentApproverID BIGINT NULL;
    -- ^ Current approver in escalation chain (foreign key to User)
    -- Used for: Tracking who should receive notifications
    -- NULL = No current approver (escalation complete or failed)
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
    ),
    
    -- Validate CurrentApproverID references User table
    CONSTRAINT FK_CompanySwitchRequest_CurrentApprover FOREIGN KEY (CurrentApproverID) 
        REFERENCES [dbo].[User](UserID);
GO

-- Create indexes for new fields
CREATE INDEX IX_CompanySwitchRequest_Urgency ON [dbo].[CompanySwitchRequest](UrgencyLevel, RequestedAt)
    WHERE UrgencyLevel IS NOT NULL;
GO

CREATE INDEX IX_CompanySwitchRequest_Amount ON [dbo].[CompanySwitchRequest](RequestedAmount, RequestedAt)
    WHERE RequestedAmount IS NOT NULL;
GO

CREATE INDEX IX_CompanySwitchRequest_CurrentApprover ON [dbo].[CompanySwitchRequest](CurrentApproverID, StatusID)
    WHERE CurrentApproverID IS NOT NULL;
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
-- Strategy: Extend existing User table with flags
-- =====================================================================

ALTER TABLE [dbo].[User] ADD
    -- =====================================================================
    -- External Approver Fields
    -- =====================================================================
    IsExternalApprover BIT NOT NULL DEFAULT 0,
    -- ^ Flag indicating if user is external approver (no platform account)
    -- 0 = Platform user (normal user)
    -- 1 = External approver (email-only approval)
    
    ExternalApproverRole NVARCHAR(100) NULL,
    -- ^ Role in external organization (for external approvers only)
    -- Example: "Finance Manager", "Department Head", "Executive"
    -- Used for: Email notifications and approval context
    
    ApprovalMethod NVARCHAR(20) NOT NULL DEFAULT 'Platform';
    -- ^ How this user receives approval requests
    -- 'Platform' = Via platform interface
    -- 'Email' = Via email only (external approvers)
GO

-- Add constraints for new fields
ALTER TABLE [dbo].[User] ADD
    -- Validate ApprovalMethod values
    CONSTRAINT CK_User_ApprovalMethod CHECK (
        ApprovalMethod IN ('Platform', 'Email')
    ),
    
    -- Ensure ExternalApproverRole is set when IsExternalApprover = 1
    CONSTRAINT CK_User_ExternalApproverRole CHECK (
        (IsExternalApprover = 0) OR (IsExternalApprover = 1 AND ExternalApproverRole IS NOT NULL)
    );
GO

-- Create index for external approvers
CREATE INDEX IX_User_ExternalApprover ON [dbo].[User](IsExternalApprover, ApprovalMethod)
    WHERE IsExternalApprover = 1;
GO

PRINT 'User table extended for external approvers successfully!';
GO

-- =====================================================================
-- 5. EXTEND SystemRole REFERENCE TABLE
-- =====================================================================
-- Purpose: Add new system roles for relationship types
-- =====================================================================

-- Add new system roles for Epic 2
INSERT INTO [ref].[SystemRole] VALUES
(10, 'HeadOfficeAdmin', 'Head Office Administrator - manages company relationships', 1),
(11, 'PartnerUser', 'Partner User - form-level access to partner companies', 1),
(12, 'VendorUser', 'Vendor User - form-level access to vendor relationships', 1),
(13, 'ClientUser', 'Client User - view-only access to assigned forms', 1),
(14, 'AffiliateUser', 'Affiliate User - form-level access to affiliate relationships', 1);
GO

PRINT 'SystemRole table extended successfully!';
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
    
    EscalationReason NVARCHAR(MAX) NULL,
    -- ^ Why request was escalated (if applicable)
    -- Example: "Approver unavailable - auto-escalated after 48 hours"
    
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
        (PreviousStatus IS NULL OR PreviousStatus IN ('Pending', 'Approved', 'Rejected', 'Escalated', 'UnderReview', 'PendingApprover', 'EscalationRequired')) AND
        (NewStatus IS NULL OR NewStatus IN ('Pending', 'Approved', 'Rejected', 'Escalated', 'UnderReview', 'PendingApprover', 'EscalationRequired'))
    )
);
GO

-- Index for workflow audit history
CREATE INDEX IX_ApprovalAuditTrail_Request ON [audit].[ApprovalAuditTrail](RequestID, ActionDate);
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
-- 7. CREATE FormAccessControl TABLE
-- =====================================================================
-- Purpose: Form-level access control for external relationships
-- Key Insight: Partners/Vendors/Clients get form-level access only
-- =====================================================================
CREATE TABLE [dbo].[FormAccessControl] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    AccessID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Access Control Details
    -- =====================================================================
    FormID BIGINT NOT NULL,
    -- ^ Link to Form table (assumes Form table exists)
    -- Used for: Controlling access to specific forms
    
    UserID BIGINT NOT NULL,
    -- ^ User with access (foreign key to User)
    -- Used for: Identifying who has access
    
    CompanyID BIGINT NOT NULL,
    -- ^ Company granting access (foreign key to Company)
    -- Used for: Tracking which company granted the access
    
    AccessType NVARCHAR(20) NOT NULL,
    -- ^ Type of access: 'View', 'Edit', 'Manage'
    -- View = Can view form and responses
    -- Edit = Can edit form content
    -- Manage = Can manage form settings and access
    
    RelationshipTypeID INT NOT NULL,
    -- ^ Link to CompanyRelationshipType
    -- Used for: Tracking relationship type (Partner, Vendor, Client, Affiliate)
    
    -- =====================================================================
    -- Access Management
    -- =====================================================================
    GrantedBy BIGINT NOT NULL,
    -- ^ User who granted access (foreign key to User)
    -- Used for: Audit trail and access management
    
    GrantedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    -- ^ When access was granted (UTC)
    
    ExpiryDate DATETIME2 NULL,
    -- ^ When access expires (NULL = no expiry)
    -- Used for: Temporary access grants
    
    -- =====================================================================
    -- Audit Trail
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NOT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT FK_FormAccessControl_Form FOREIGN KEY (FormID) 
        REFERENCES [dbo].[Form](FormID),
    
    CONSTRAINT FK_FormAccessControl_User FOREIGN KEY (UserID) 
        REFERENCES [dbo].[User](UserID),
    
    CONSTRAINT FK_FormAccessControl_Company FOREIGN KEY (CompanyID) 
        REFERENCES [dbo].[Company](CompanyID),
    
    CONSTRAINT FK_FormAccessControl_RelationshipType FOREIGN KEY (RelationshipTypeID) 
        REFERENCES [ref].[CompanyRelationshipType](CompanyRelationshipTypeID),
    
    CONSTRAINT FK_FormAccessControl_GrantedBy FOREIGN KEY (GrantedBy) 
        REFERENCES [dbo].[User](UserID),
    
    CONSTRAINT FK_FormAccessControl_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [dbo].[User](UserID),
    
    CONSTRAINT FK_FormAccessControl_UpdatedBy FOREIGN KEY (UpdatedBy) 
        REFERENCES [dbo].[User](UserID),
    
    -- Validate AccessType values
    CONSTRAINT CK_FormAccessControl_AccessType CHECK (
        AccessType IN ('View', 'Edit', 'Manage')
    ),
    
    -- Ensure ExpiryDate is after GrantedDate
    CONSTRAINT CK_FormAccessControl_ExpiryDate CHECK (
        ExpiryDate IS NULL OR ExpiryDate > GrantedDate
    )
);
GO

-- Index for form access queries
CREATE INDEX IX_FormAccessControl_Form ON [dbo].[FormAccessControl](FormID, IsDeleted)
    WHERE IsDeleted = 0;
GO

-- Index for user access queries
CREATE INDEX IX_FormAccessControl_User ON [dbo].[FormAccessControl](UserID, IsDeleted)
    WHERE IsDeleted = 0;
GO

-- Index for company access queries
CREATE INDEX IX_FormAccessControl_Company ON [dbo].[FormAccessControl](CompanyID, IsDeleted)
    WHERE IsDeleted = 0;
GO

-- Unique constraint to prevent duplicate access grants
CREATE UNIQUE INDEX UX_FormAccessControl_Unique ON [dbo].[FormAccessControl](FormID, UserID, CompanyID)
    WHERE IsDeleted = 0;
GO

PRINT 'FormAccessControl table created successfully!';
GO

-- =====================================================================
-- 8. CREATE EscalationChain TABLE
-- =====================================================================
-- Purpose: Escalation chain configuration for approval workflows
-- Key Insight: Supports both platform and external approvers
-- =====================================================================
CREATE TABLE [dbo].[EscalationChain] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    ChainID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Relationship Reference
    -- =====================================================================
    CompanyRelationshipID BIGINT NOT NULL,
    -- ^ Link to CompanyRelationship
    -- Used for: Defining escalation chain for specific relationships
    
    -- =====================================================================
    -- Approval Configuration
    -- =====================================================================
    ApprovalType NVARCHAR(50) NOT NULL,
    -- ^ Type of approval: 'FormDeployment', 'BillingChange', 'AccessRequest'
    -- Used for: Different escalation chains for different approval types
    
    AmountThreshold DECIMAL(10,2) NULL,
    -- ^ Threshold for this escalation level (NULL = all amounts)
    -- Example: $1000.00 - this chain applies to requests >= $1000
    -- Used for: Amount-based escalation routing
    
    -- =====================================================================
    -- Escalation Level
    -- =====================================================================
    EscalationLevel INT NOT NULL,
    -- ^ Level in escalation chain: 1, 2, 3, etc.
    -- Used for: Ordering escalation sequence
    
    -- =====================================================================
    -- Approver Details
    -- =====================================================================
    ApproverUserID BIGINT NULL,
    -- ^ Platform user approver (foreign key to User)
    -- NULL = External approver (use ApproverEmail)
    
    ApproverEmail NVARCHAR(100) NULL,
    -- ^ External approver email (for external approvers)
    -- Used for: Email-only approval process
    
    ApproverName NVARCHAR(200) NULL,
    -- ^ External approver name (for external approvers)
    -- Used for: Email notifications and audit trail
    
    -- =====================================================================
    -- Escalation Timing
    -- =====================================================================
    EscalationHours INT NOT NULL DEFAULT 48,
    -- ^ Hours before escalating to next level
    -- Used for: Auto-escalation timing
    
    -- =====================================================================
    -- Status
    -- =====================================================================
    IsActive BIT NOT NULL DEFAULT 1,
    -- ^ Is this escalation level active?
    -- Used for: Enabling/disabling escalation levels
    
    -- =====================================================================
    -- Audit Trail
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NOT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT FK_EscalationChain_Relationship FOREIGN KEY (CompanyRelationshipID) 
        REFERENCES [dbo].[CompanyRelationship](CompanyRelationshipID),
    
    CONSTRAINT FK_EscalationChain_Approver FOREIGN KEY (ApproverUserID) 
        REFERENCES [dbo].[User](UserID),
    
    CONSTRAINT FK_EscalationChain_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [dbo].[User](UserID),
    
    CONSTRAINT FK_EscalationChain_UpdatedBy FOREIGN KEY (UpdatedBy) 
        REFERENCES [dbo].[User](UserID),
    
    -- Validate ApprovalType values
    CONSTRAINT CK_EscalationChain_ApprovalType CHECK (
        ApprovalType IN ('FormDeployment', 'BillingChange', 'AccessRequest', 'FormAccess')
    ),
    
    -- Validate EscalationLevel is positive
    CONSTRAINT CK_EscalationChain_EscalationLevel CHECK (
        EscalationLevel > 0
    ),
    
    -- Validate EscalationHours is positive
    CONSTRAINT CK_EscalationChain_EscalationHours CHECK (
        EscalationHours > 0
    ),
    
    -- Ensure either ApproverUserID or ApproverEmail is set
    CONSTRAINT CK_EscalationChain_Approver CHECK (
        (ApproverUserID IS NOT NULL AND ApproverEmail IS NULL) OR
        (ApproverUserID IS NULL AND ApproverEmail IS NOT NULL)
    ),
    
    -- Ensure AmountThreshold is positive
    CONSTRAINT CK_EscalationChain_AmountThreshold CHECK (
        AmountThreshold IS NULL OR AmountThreshold >= 0
    )
);
GO

-- Index for relationship queries
CREATE INDEX IX_EscalationChain_Relationship ON [dbo].[EscalationChain](CompanyRelationshipID, ApprovalType, IsActive)
    WHERE IsActive = 1;
GO

-- Index for approver queries
CREATE INDEX IX_EscalationChain_Approver ON [dbo].[EscalationChain](ApproverUserID, IsActive)
    WHERE IsActive = 1 AND ApproverUserID IS NOT NULL;
GO

-- Index for external approver queries
CREATE INDEX IX_EscalationChain_ExternalApprover ON [dbo].[EscalationChain](ApproverEmail, IsActive)
    WHERE IsActive = 1 AND ApproverEmail IS NOT NULL;
GO

-- Unique constraint to prevent duplicate escalation levels
CREATE UNIQUE INDEX UX_EscalationChain_Unique ON [dbo].[EscalationChain](CompanyRelationshipID, ApprovalType, EscalationLevel, AmountThreshold)
    WHERE IsActive = 1;
GO

PRINT 'EscalationChain table created successfully!';
GO

-- =====================================================================
-- PHASE 3: CREATE HELPER FUNCTIONS
-- =====================================================================

-- =====================================================================
-- 9. CREATE Urgency Calculation Function
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
-- 10. CREATE Approval Threshold Function
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
-- 11. CREATE Escalation Chain Builder Function
-- =====================================================================
-- Purpose: Build escalation chain JSON for CompanySwitchRequest
-- =====================================================================
CREATE FUNCTION [dbo].[BuildEscalationChain](@CompanyRelationshipID BIGINT, @ApprovalType NVARCHAR(50), @Amount DECIMAL(10,2))
RETURNS NVARCHAR(MAX)
AS
BEGIN
    DECLARE @EscalationChain NVARCHAR(MAX) = '[';
    DECLARE @First BIT = 1;
    
    DECLARE escalation_cursor CURSOR FOR
    SELECT 
        EscalationLevel,
        ISNULL(ApproverUserID, 0) as ApproverUserID,
        ISNULL(ApproverEmail, '') as ApproverEmail,
        ISNULL(ApproverName, '') as ApproverName,
        EscalationHours
    FROM [dbo].[EscalationChain]
    WHERE CompanyRelationshipID = @CompanyRelationshipID
        AND ApprovalType = @ApprovalType
        AND (AmountThreshold IS NULL OR @Amount >= AmountThreshold)
        AND IsActive = 1
    ORDER BY EscalationLevel;
    
    DECLARE @Level INT, @ApproverID BIGINT, @Email NVARCHAR(100), @Name NVARCHAR(200), @Hours INT;
    
    OPEN escalation_cursor;
    FETCH NEXT FROM escalation_cursor INTO @Level, @ApproverID, @Email, @Name, @Hours;
    
    WHILE @@FETCH_STATUS = 0
    BEGIN
        IF @First = 0
            SET @EscalationChain = @EscalationChain + ',';
        
        SET @EscalationChain = @EscalationChain + '{"Level":' + CAST(@Level AS NVARCHAR(10)) + 
            ',"ApproverID":' + CAST(@ApproverID AS NVARCHAR(20)) + 
            ',"Email":"' + @Email + '"' +
            ',"Name":"' + @Name + '"' +
            ',"Hours":' + CAST(@Hours AS NVARCHAR(10)) + '}';
        
        SET @First = 0;
        FETCH NEXT FROM escalation_cursor INTO @Level, @ApproverID, @Email, @Name, @Hours;
    END;
    
    CLOSE escalation_cursor;
    DEALLOCATE escalation_cursor;
    
    SET @EscalationChain = @EscalationChain + ']';
    
    RETURN @EscalationChain;
END;
GO

PRINT 'Escalation chain builder function created successfully!';
GO

-- =====================================================================
-- SUMMARY
-- =====================================================================
PRINT '========================================';
PRINT 'Company Domain Epic 2 Schema Complete!';
PRINT '========================================';
PRINT 'COMPLETE SOLUTION WITH UX REFINEMENTS:';
PRINT '';
PRINT 'Extended Tables:';
PRINT '  1. CompanySwitchRequest (added 6 fields)';
PRINT '  2. CompanySwitchRequestType (added 4 types)';
PRINT '  3. CompanySwitchRequestStatus (added 4 statuses)';
PRINT '  4. User (added 3 fields for external approvers)';
PRINT '  5. SystemRole (added 5 new roles)';
PRINT '';
PRINT 'New Tables:';
PRINT '  6. ApprovalAuditTrail (audit schema - 10 fields)';
PRINT '  7. FormAccessControl (form-level access - 12 fields)';
PRINT '  8. EscalationChain (escalation management - 12 fields)';
PRINT '';
PRINT 'New Functions:';
PRINT '  9. CalculateUrgencyLevel (urgency calculation)';
PRINT '  10. GetApprovalLevel (approval threshold)';
PRINT '  11. BuildEscalationChain (escalation chain builder)';
PRINT '';
PRINT 'Key Features:';
PRINT '  ✅ Complete escalation chain support';
PRINT '  ✅ External approver support (email-only)';
PRINT '  ✅ Form-level access control';
PRINT '  ✅ New system roles for relationship types';
PRINT '  ✅ Enhanced audit trail (audit schema)';
PRINT '  ✅ Dashboard consistency maintained';
PRINT '  ✅ Backward compatible with Epic 1';
PRINT '';
PRINT 'UX Expert Input Incorporated:';
PRINT '  ✅ Sally''s feedback on escalation handling';
PRINT '  ✅ Form-level access for partners/vendors/clients';
PRINT '  ✅ External approver support without platform accounts';
PRINT '  ✅ Dashboard consistency maintained';
PRINT '  ✅ Role-based access control';
PRINT '';
PRINT 'Next Steps:';
PRINT '  1. Sally UX review (completed and incorporated)';
PRINT '  2. Solomon schema validation (Database Migration Validator)';
PRINT '  3. Developer implementation planning';
PRINT '  4. Epic 2 testing strategy with escalation scenarios';
PRINT '========================================';
GO
