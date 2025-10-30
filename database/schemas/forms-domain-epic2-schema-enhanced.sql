-- =====================================================================
-- Forms Domain Epic 2 Schema - ENHANCED FOR DASHBOARD
-- Form Header & Access Control with Dashboard Optimization
-- =====================================================================
-- Author: Dimitri (Data Domain Architect)
-- Date: January 15, 2025
-- Version: 3.0.0 (ENHANCED FOR DASHBOARD)
-- =====================================================================
-- Purpose:
--   Epic 2 Forms domain - ENHANCED FOR DASHBOARD:
--   1. Form header management with dashboard summary fields
--   2. Form deployment approval workflow integration (from Company domain)
--   3. Form-level access control for external relationships
--   4. Event integration for form context and urgency calculation
--   5. Dashboard-optimized form cards with activity metrics
--   6. Foundation for future form builder (Epic 3+)
-- =====================================================================
-- Epic 2 Enhancements:
--   ✅ Form Header: Enhanced with dashboard summary fields
--   ✅ Form Access Control: Proper reference tables for data integrity
--   ✅ Dashboard Optimization: Activity metrics and visual elements
--   ✅ Reference Tables: FormStatus, FormAccessControlAccessType, FormApprovalStatus
--   ❌ Form Builder: Defer to future Epic (FormField, FormSubmission, FormResponse)
--   ❌ Form Analytics: Defer to future Epic
--   ❌ Complex Field Types: Defer to future Epic
--   ❌ Form Templates: Defer to future Epic
-- =====================================================================
-- Integration Points:
--   - Company Domain: Form ownership, access control, approval workflow
--   - Event Domain: Form context, urgency calculation
--   - User Domain: Form creators, access control
-- =====================================================================

USE [EventLeadPlatform];
GO

-- =====================================================================
-- PHASE 1: CREATE REFERENCE TABLES
-- =====================================================================

-- =====================================================================
-- 1. CREATE FormStatus REFERENCE TABLE
-- =====================================================================
-- Purpose: Form status reference with dashboard visual elements
-- =====================================================================
CREATE TABLE [ref].[FormStatus] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    FormStatusID INT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Status Identity
    -- =====================================================================
    StatusCode NVARCHAR(20) NOT NULL UNIQUE,
    -- ^ Status code for system use
    -- Examples: 'DRAFT', 'PUBLISHED', 'ARCHIVED'
    
    StatusName NVARCHAR(50) NOT NULL,
    -- ^ Human-readable status name
    -- Examples: 'Draft', 'Published', 'Archived'
    
    StatusDescription NVARCHAR(200) NULL,
    -- ^ Detailed description of status
    -- Example: 'Form is being created and edited'
    
    -- =====================================================================
    -- Dashboard Visual Elements
    -- =====================================================================
    StatusColor NVARCHAR(7) NULL,
    -- ^ Hex color code for dashboard display
    -- Examples: '#FFA500' (orange for draft), '#28A745' (green for published)
    
    StatusIcon NVARCHAR(50) NULL,
    -- ^ Icon name for dashboard display
    -- Examples: 'draft-icon', 'published-icon', 'archived-icon'
    
    -- =====================================================================
    -- Configuration
    -- =====================================================================
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 0,
    
    -- =====================================================================
    -- Audit Trail
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NOT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    
    CONSTRAINT FK_FormStatus_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_FormStatus_UpdatedBy FOREIGN KEY (UpdatedBy) 
        REFERENCES [dbo].[User](UserID)
);
GO

-- Insert comprehensive form statuses
INSERT INTO [ref].[FormStatus] (StatusCode, StatusName, StatusDescription, StatusColor, StatusIcon, IsActive, SortOrder, CreatedBy) VALUES
('DRAFT', 'Draft', 'Form is being created and edited', '#FFA500', 'draft-icon', 1, 1, 1),
('REVIEW', 'Under Review', 'Form is being reviewed before publication', '#17A2B8', 'review-icon', 1, 2, 1),
('PUBLISHED', 'Published', 'Form is live and accepting submissions', '#28A745', 'published-icon', 1, 3, 1),
('PAUSED', 'Paused', 'Form is temporarily paused', '#FFC107', 'paused-icon', 1, 4, 1),
('ARCHIVED', 'Archived', 'Form is no longer accessible', '#6C757D', 'archived-icon', 1, 5, 1),
('DELETED', 'Deleted', 'Form has been deleted', '#DC3545', 'deleted-icon', 0, 6, 1);
GO

PRINT 'FormStatus reference table created successfully!';
GO

-- =====================================================================
-- 2. CREATE FormAccessControlAccessType REFERENCE TABLE
-- =====================================================================
-- Purpose: Access type reference for form access control
-- =====================================================================
CREATE TABLE [ref].[FormAccessControlAccessType] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    FormAccessControlAccessTypeID INT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Access Type Identity
    -- =====================================================================
    AccessTypeCode NVARCHAR(20) NOT NULL UNIQUE,
    -- ^ Access type code for system use
    -- Examples: 'VIEW', 'EDIT', 'MANAGE'
    
    AccessTypeName NVARCHAR(50) NOT NULL,
    -- ^ Human-readable access type name
    -- Examples: 'View', 'Edit', 'Manage'
    
    AccessTypeDescription NVARCHAR(200) NULL,
    -- ^ Detailed description of access type
    -- Example: 'Can view form and basic information'
    
    -- =====================================================================
    -- Configuration
    -- =====================================================================
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 0,
    
    -- =====================================================================
    -- Audit Trail
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NOT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    
    CONSTRAINT FK_FormAccessControlAccessType_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_FormAccessControlAccessType_UpdatedBy FOREIGN KEY (UpdatedBy) 
        REFERENCES [dbo].[User](UserID)
);
GO

-- Insert comprehensive access types
INSERT INTO [ref].[FormAccessControlAccessType] (AccessTypeCode, AccessTypeName, AccessTypeDescription, IsActive, SortOrder, CreatedBy) VALUES
('VIEW', 'View', 'Can view form and basic information', 1, 1, 1),
('EDIT', 'Edit', 'Can edit form content and settings', 1, 2, 1),
('MANAGE', 'Manage', 'Can manage form settings and access control', 1, 3, 1),
('SUBMIT', 'Submit', 'Can submit responses to the form', 1, 4, 1),
('ANALYZE', 'Analyze', 'Can view form analytics and responses', 1, 5, 1);
GO

PRINT 'FormAccessControlAccessType reference table created successfully!';
GO

-- =====================================================================
-- 3. CREATE FormApprovalStatus REFERENCE TABLE
-- =====================================================================
-- Purpose: Approval status reference for form deployment workflow
-- =====================================================================
CREATE TABLE [ref].[FormApprovalStatus] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    FormApprovalStatusID INT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Approval Status Identity
    -- =====================================================================
    ApprovalStatusCode NVARCHAR(20) NOT NULL UNIQUE,
    -- ^ Approval status code for system use
    -- Examples: 'NO_APPROVAL', 'PENDING', 'APPROVED', 'REJECTED'
    
    ApprovalStatusName NVARCHAR(50) NOT NULL,
    -- ^ Human-readable approval status name
    -- Examples: 'No Approval Required', 'Pending Approval', 'Approved', 'Rejected'
    
    ApprovalStatusDescription NVARCHAR(200) NULL,
    -- ^ Detailed description of approval status
    -- Example: 'Form deployment requires head office approval'
    
    -- =====================================================================
    -- Approval Configuration
    -- =====================================================================
    IsRequiresApproval BIT NOT NULL DEFAULT 0,
    -- ^ Does this status require approval workflow?
    -- 0 = No approval required
    -- 1 = Approval required
    
    -- =====================================================================
    -- Configuration
    -- =====================================================================
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 0,
    
    -- =====================================================================
    -- Audit Trail
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NOT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    
    CONSTRAINT FK_FormApprovalStatus_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_FormApprovalStatus_UpdatedBy FOREIGN KEY (UpdatedBy) 
        REFERENCES [dbo].[User](UserID)
);
GO

-- Insert comprehensive approval statuses
INSERT INTO [ref].[FormApprovalStatus] (ApprovalStatusCode, ApprovalStatusName, ApprovalStatusDescription, IsRequiresApproval, IsActive, SortOrder, CreatedBy) VALUES
('NO_APPROVAL', 'No Approval Required', 'Form can be deployed without approval', 0, 1, 1, 1),
('PENDING', 'Pending Approval', 'Form deployment awaiting head office approval', 1, 1, 2, 1),
('APPROVED', 'Approved', 'Form deployment has been approved', 0, 1, 3, 1),
('REJECTED', 'Rejected', 'Form deployment has been rejected', 0, 1, 4, 1),
('CANCELLED', 'Cancelled', 'Form deployment request was cancelled', 0, 1, 5, 1),
('EXPIRED', 'Expired', 'Form deployment request has expired', 0, 1, 6, 1);
GO

PRINT 'FormApprovalStatus reference table created successfully!';
GO

-- =====================================================================
-- PHASE 2: CREATE CORE FORM TABLES
-- =====================================================================

-- =====================================================================
-- 4. CREATE Form TABLE (ENHANCED FOR DASHBOARD)
-- =====================================================================
-- Purpose: Form header with dashboard summary fields
-- =====================================================================
CREATE TABLE [dbo].[Form] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    FormID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Form Identity
    -- =====================================================================
    FormName NVARCHAR(200) NOT NULL,
    -- ^ Form title/name
    -- Example: "Customer Feedback Survey"
    -- Required: Users need to identify forms
    
    FormDescription NVARCHAR(MAX) NULL,
    -- ^ Detailed description of form purpose
    -- Example: "Collect feedback from customers after event attendance"
    -- Optional: Provides context for form users
    
    -- =====================================================================
    -- Ownership and Context
    -- =====================================================================
    CompanyID BIGINT NOT NULL,
    -- ^ Owner company (foreign key to Company)
    -- Used for: Form ownership and access control
    
    EventID BIGINT NULL,
    -- ^ Associated event (foreign key to Event)
    -- Used for: Event-specific forms and context
    -- NULL = General form not tied to specific event
    
    -- =====================================================================
    -- Status and Approval (Reference Tables)
    -- =====================================================================
    FormStatusID INT NOT NULL,
    -- ^ Form status (foreign key to FormStatus)
    -- Used for: Dashboard status display and workflow
    
    FormApprovalStatusID INT NOT NULL,
    -- ^ Approval status (foreign key to FormApprovalStatus)
    -- Used for: Approval workflow integration
    
    -- =====================================================================
    -- Dashboard Summary Fields
    -- =====================================================================
    IsPublic BIT NOT NULL DEFAULT 0,
    -- ^ Can form be accessed without authentication?
    -- 0 = Requires authentication
    -- 1 = Public access (no login required)
    
    DeploymentCost DECIMAL(10,2) NULL,
    -- ^ Cost for form deployment (for approval workflow)
    -- Example: $500.00 for complex form deployment
    -- Used for: Company domain approval workflow
    
    -- =====================================================================
    -- Activity Summary (Dashboard Metrics)
    -- =====================================================================
    TotalSubmissions INT NOT NULL DEFAULT 0,
    -- ^ Total form submissions across all environments
    -- Used for: Dashboard activity summary
    
    DemoLeadsCollected INT NOT NULL DEFAULT 0,
    -- ^ Demo environment leads collected
    -- Used for: Dashboard activity summary
    
    ProductionLeadsCollected INT NOT NULL DEFAULT 0,
    -- ^ Production environment leads collected
    -- Used for: Dashboard activity summary
    
    LastSubmissionDate DATETIME2 NULL,
    -- ^ Last submission timestamp
    -- Used for: Dashboard activity summary
    
    LastActivityDate DATETIME2 NULL,
    -- ^ Last activity timestamp (any form interaction)
    -- Used for: Dashboard activity summary
    
    -- =====================================================================
    -- Visual Identification
    -- =====================================================================
    FormThumbnailURL NVARCHAR(500) NULL,
    -- ^ Thumbnail URL for dashboard display
    -- Example: "https://cdn.eventlead.com/thumbnails/form_123.png"
    -- Used for: Dashboard visual identification
    
    FormPreviewURL NVARCHAR(500) NULL,
    -- ^ Preview URL for dashboard display
    -- Example: "https://eventlead.com/preview/form/123"
    -- Used for: Dashboard form preview
    
    -- =====================================================================
    -- Audit Trail
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NOT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT FK_Form_Company FOREIGN KEY (CompanyID) 
        REFERENCES [dbo].[Company](CompanyID),
    CONSTRAINT FK_Form_Event FOREIGN KEY (EventID) 
        REFERENCES [dbo].[Event](EventID),
    CONSTRAINT FK_Form_FormStatus FOREIGN KEY (FormStatusID) 
        REFERENCES [ref].[FormStatus](FormStatusID),
    CONSTRAINT FK_Form_FormApprovalStatus FOREIGN KEY (FormApprovalStatusID) 
        REFERENCES [ref].[FormApprovalStatus](FormApprovalStatusID),
    CONSTRAINT FK_Form_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_Form_UpdatedBy FOREIGN KEY (UpdatedBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_Form_DeletedBy FOREIGN KEY (DeletedBy) 
        REFERENCES [dbo].[User](UserID),
    
    -- Validate DeploymentCost is positive
    CONSTRAINT CK_Form_DeploymentCost CHECK (
        DeploymentCost IS NULL OR DeploymentCost >= 0
    ),
    
    -- Validate submission counts are non-negative
    CONSTRAINT CK_Form_SubmissionCounts CHECK (
        TotalSubmissions >= 0 AND
        DemoLeadsCollected >= 0 AND
        ProductionLeadsCollected >= 0
    )
);
GO

-- Create indexes for Form table
CREATE INDEX IX_Form_Company ON [dbo].[Form](CompanyID, IsDeleted)
    WHERE IsDeleted = 0;
GO

CREATE INDEX IX_Form_Event ON [dbo].[Form](EventID, IsDeleted)
    WHERE IsDeleted = 0 AND EventID IS NOT NULL;
GO

CREATE INDEX IX_Form_Status ON [dbo].[Form](FormStatusID, IsDeleted)
    WHERE IsDeleted = 0;
GO

CREATE INDEX IX_Form_ApprovalStatus ON [dbo].[Form](FormApprovalStatusID, IsDeleted)
    WHERE IsDeleted = 0;
GO

CREATE INDEX IX_Form_Public ON [dbo].[Form](IsPublic, FormStatusID, IsDeleted)
    WHERE IsDeleted = 0;
GO

CREATE INDEX IX_Form_Activity ON [dbo].[Form](LastActivityDate, IsDeleted)
    WHERE IsDeleted = 0;
GO

PRINT 'Form table created successfully!';
GO

-- =====================================================================
-- 5. CREATE FormAccessControl TABLE (ENHANCED)
-- =====================================================================
-- Purpose: Form-level access control with proper reference tables
-- =====================================================================
CREATE TABLE [dbo].[FormAccessControl] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    FormAccessControlID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Form and User References
    -- =====================================================================
    FormID BIGINT NOT NULL,
    -- ^ Form being accessed (foreign key to Form)
    -- Used: Linking access control to forms
    
    UserID BIGINT NOT NULL,
    -- ^ User with access (foreign key to User)
    -- Used: Identifying who has access
    
    CompanyID BIGINT NOT NULL,
    -- ^ Company granting access (foreign key to Company)
    -- Used: Tracking which company granted access
    
    -- =====================================================================
    -- Access Control Details (Reference Tables)
    -- =====================================================================
    FormAccessControlAccessTypeID INT NOT NULL,
    -- ^ Access type (foreign key to FormAccessControlAccessType)
    -- Used: Proper reference table for access types
    
    CompanyRelationshipTypeID INT NOT NULL,
    -- ^ Relationship type (foreign key to CompanyRelationshipType)
    -- Used: Tracking relationship type (Partner, Vendor, Client, Affiliate)
    
    -- =====================================================================
    -- Access Management
    -- =====================================================================
    GrantedBy BIGINT NOT NULL,
    -- ^ User who granted access (foreign key to User)
    -- Used: Audit trail and access management
    
    GrantedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    -- ^ When access was granted (UTC)
    -- Used: Access timeline tracking
    
    ExpiryDate DATETIME2 NULL,
    -- ^ When access expires (NULL = no expiry)
    -- Used: Temporary access grants
    
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
    CONSTRAINT FK_FormAccessControl_AccessType FOREIGN KEY (FormAccessControlAccessTypeID) 
        REFERENCES [ref].[FormAccessControlAccessType](FormAccessControlAccessTypeID),
    CONSTRAINT FK_FormAccessControl_CompanyRelationshipType FOREIGN KEY (CompanyRelationshipTypeID) 
        REFERENCES [ref].[CompanyRelationshipType](CompanyRelationshipTypeID),
    CONSTRAINT FK_FormAccessControl_GrantedBy FOREIGN KEY (GrantedBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_FormAccessControl_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_FormAccessControl_UpdatedBy FOREIGN KEY (UpdatedBy) 
        REFERENCES [dbo].[User](UserID),
    
    -- Ensure ExpiryDate is after GrantedDate
    CONSTRAINT CK_FormAccessControl_ExpiryDate CHECK (
        ExpiryDate IS NULL OR ExpiryDate > GrantedDate
    )
);
GO

-- Create indexes for FormAccessControl table
CREATE INDEX IX_FormAccessControl_Form ON [dbo].[FormAccessControl](FormID, IsDeleted)
    WHERE IsDeleted = 0;
GO

CREATE INDEX IX_FormAccessControl_User ON [dbo].[FormAccessControl](UserID, IsDeleted)
    WHERE IsDeleted = 0;
GO

CREATE INDEX IX_FormAccessControl_Company ON [dbo].[FormAccessControl](CompanyID, IsDeleted)
    WHERE IsDeleted = 0;
GO

CREATE INDEX IX_FormAccessControl_AccessType ON [dbo].[FormAccessControl](FormAccessControlAccessTypeID, IsDeleted)
    WHERE IsDeleted = 0;
GO

-- Unique constraint to prevent duplicate access grants
CREATE UNIQUE INDEX UX_FormAccessControl_Unique ON [dbo].[FormAccessControl](FormID, UserID, CompanyID)
    WHERE IsDeleted = 0;
GO

PRINT 'FormAccessControl table created successfully!';
GO

-- =====================================================================
-- PHASE 3: CREATE HELPER FUNCTIONS
-- =====================================================================

-- =====================================================================
-- 6. CREATE Form Access Check Function
-- =====================================================================
-- Purpose: Check if user has access to form
-- =====================================================================
CREATE FUNCTION [dbo].[CheckFormAccess](@FormID BIGINT, @UserID BIGINT, @AccessTypeCode NVARCHAR(20))
RETURNS BIT
AS
BEGIN
    DECLARE @HasAccess BIT = 0;
    
    -- Check if user has the required access type
    IF EXISTS (
        SELECT 1
        FROM [dbo].[FormAccessControl] fac
        INNER JOIN [ref].[FormAccessControlAccessType] fat ON fac.FormAccessControlAccessTypeID = fat.FormAccessControlAccessTypeID
        WHERE fac.FormID = @FormID 
            AND fac.UserID = @UserID 
            AND fat.AccessTypeCode = @AccessTypeCode
            AND fac.IsDeleted = 0
            AND fat.IsActive = 1
            AND (fac.ExpiryDate IS NULL OR fac.ExpiryDate > GETUTCDATE())
    )
        SET @HasAccess = 1;
    
    RETURN @HasAccess;
END;
GO

PRINT 'Form access check function created successfully!';
GO

-- =====================================================================
-- 7. CREATE Form Dashboard Summary Function
-- =====================================================================
-- Purpose: Get form summary for dashboard display
-- =====================================================================
CREATE FUNCTION [dbo].[GetFormDashboardSummary](@FormID BIGINT)
RETURNS TABLE
AS
RETURN
(
    SELECT 
        f.FormID,
        f.FormName,
        f.FormDescription,
        f.CompanyID,
        f.EventID,
        fs.StatusName as FormStatus,
        fs.StatusColor as FormStatusColor,
        fs.StatusIcon as FormStatusIcon,
        fas.ApprovalStatusName as ApprovalStatus,
        f.IsPublic,
        f.DeploymentCost,
        f.TotalSubmissions,
        f.DemoLeadsCollected,
        f.ProductionLeadsCollected,
        f.LastSubmissionDate,
        f.LastActivityDate,
        f.FormThumbnailURL,
        f.FormPreviewURL,
        f.CreatedDate,
        f.UpdatedDate
    FROM [dbo].[Form] f
    INNER JOIN [ref].[FormStatus] fs ON f.FormStatusID = fs.FormStatusID
    INNER JOIN [ref].[FormApprovalStatus] fas ON f.FormApprovalStatusID = fas.FormApprovalStatusID
    WHERE f.FormID = @FormID 
        AND f.IsDeleted = 0
        AND fs.IsActive = 1
        AND fas.IsActive = 1
);
GO

PRINT 'Form dashboard summary function created successfully!';
GO

-- =====================================================================
-- 8. CREATE Form Activity Update Function
-- =====================================================================
-- Purpose: Update form activity metrics when submissions change
-- =====================================================================
CREATE FUNCTION [dbo].[UpdateFormActivity](@FormID BIGINT, @Environment NVARCHAR(20))
RETURNS BIT
AS
BEGIN
    DECLARE @Success BIT = 0;
    
    BEGIN TRY
        -- Update form activity metrics
        UPDATE [dbo].[Form]
        SET 
            TotalSubmissions = TotalSubmissions + 1,
            DemoLeadsCollected = CASE 
                WHEN @Environment = 'Demo' THEN DemoLeadsCollected + 1 
                ELSE DemoLeadsCollected 
            END,
            ProductionLeadsCollected = CASE 
                WHEN @Environment = 'Production' THEN ProductionLeadsCollected + 1 
                ELSE ProductionLeadsCollected 
            END,
            LastSubmissionDate = GETUTCDATE(),
            LastActivityDate = GETUTCDATE(),
            UpdatedDate = GETUTCDATE()
        WHERE FormID = @FormID;
        
        SET @Success = 1;
    END TRY
    BEGIN CATCH
        SET @Success = 0;
    END CATCH
    
    RETURN @Success;
END;
GO

PRINT 'Form activity update function created successfully!';
GO

-- =====================================================================
-- SUMMARY
-- =====================================================================
PRINT '========================================';
PRINT 'Forms Domain Epic 2 Schema Complete!';
PRINT '========================================';
PRINT 'ENHANCED FOR DASHBOARD:';
PRINT '';
PRINT 'Reference Tables:';
PRINT '  1. FormStatus (with dashboard visual elements)';
PRINT '  2. FormAccessControlAccessType (proper reference table)';
PRINT '  3. FormApprovalStatus (approval workflow integration)';
PRINT '';
PRINT 'Core Tables:';
PRINT '  4. Form (enhanced with dashboard summary fields)';
PRINT '  5. FormAccessControl (enhanced with proper references)';
PRINT '';
PRINT 'Helper Functions:';
PRINT '  6. CheckFormAccess (access validation with reference tables)';
PRINT '  7. GetFormDashboardSummary (dashboard data retrieval)';
PRINT '  8. UpdateFormActivity (activity metrics update)';
PRINT '';
PRINT 'Key Features:';
PRINT '  ✅ Form header with dashboard summary fields';
PRINT '  ✅ Activity metrics (submissions, leads, timestamps)';
PRINT '  ✅ Visual elements (thumbnails, status colors, icons)';
PRINT '  ✅ Proper reference tables for data integrity';
PRINT '  ✅ Form deployment approval integration';
PRINT '  ✅ Form-level access control';
PRINT '  ✅ Event integration';
PRINT '  ✅ Company domain integration';
PRINT '  ✅ Audit trail on all tables';
PRINT '  ✅ Foundation for form builder (Epic 3+)';
PRINT '';
PRINT 'Dashboard Optimization:';
PRINT '  ✅ Activity summary fields for fast dashboard loading';
PRINT '  ✅ Visual identification elements (thumbnails, colors, icons)';
PRINT '  ✅ Status and approval information';
PRINT '  ✅ Lead count tracking (demo and production)';
PRINT '  ✅ Last activity timestamps';
PRINT '';
PRINT 'Epic 2 Scope Decisions:';
PRINT '  ✅ Form Header: Enhanced with dashboard summary fields';
PRINT '  ✅ Form Access Control: Proper reference tables for data integrity';
PRINT '  ✅ Dashboard Optimization: Activity metrics and visual elements';
PRINT '  ❌ Form Builder: Defer to future Epic (FormField, FormSubmission, FormResponse)';
PRINT '  ❌ Form Analytics: Defer to future Epic';
PRINT '  ❌ Complex Field Types: Defer to future Epic';
PRINT '  ❌ Form Templates: Defer to future Epic';
PRINT '';
PRINT 'Integration Points:';
PRINT '  ✅ Company Domain: Form ownership, access control, approval workflow';
PRINT '  ✅ Event Domain: Form context, urgency calculation';
PRINT '  ✅ User Domain: Form creators, access control';
PRINT '';
PRINT 'Next Steps:';
PRINT '  1. Solomon schema validation (Database Migration Validator)';
PRINT '  2. Sally UX review (dashboard form card design)';
PRINT '  3. Developer implementation planning';
PRINT '  4. Form header and access control testing';
PRINT '========================================';
GO
