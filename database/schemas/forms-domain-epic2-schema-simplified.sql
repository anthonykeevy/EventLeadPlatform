-- =====================================================================
-- Forms Domain Epic 2 Schema - SIMPLIFIED FOR MVP
-- Form Header & Access Control Foundation
-- =====================================================================
-- Author: Dimitri (Data Domain Architect)
-- Date: January 15, 2025
-- Version: 2.0.0 (SIMPLIFIED FOR EPIC 2)
-- =====================================================================
-- Purpose:
--   Epic 2 Forms domain - SIMPLIFIED SCOPE:
--   1. Form header management for basic form metadata
--   2. Form deployment approval workflow integration (from Company domain)
--   3. Form-level access control for external relationships
--   4. Event integration for form context and urgency calculation
--   5. Foundation for future form builder (Epic 3+)
-- =====================================================================
-- Epic 2 Scope Decisions:
--   - ✅ Form Header: Core form metadata and management
--   - ✅ Form Access Control: Integration with Company domain
--   - ❌ Form Builder: Defer to future Epic (FormField, FormSubmission, FormResponse)
--   - ❌ Form Analytics: Defer to future Epic
--   - ❌ Complex Field Types: Defer to future Epic
--   - ❌ Form Templates: Defer to future Epic
-- =====================================================================
-- Integration Points:
--   - Company Domain: Form ownership, access control, approval workflow
--   - Event Domain: Form context, urgency calculation
--   - User Domain: Form creators, access control
-- =====================================================================

USE [EventLeadPlatform];
GO

-- =====================================================================
-- PHASE 1: CREATE CORE FORM TABLES
-- =====================================================================

-- =====================================================================
-- 1. CREATE Form TABLE
-- =====================================================================
-- Purpose: Form header and metadata management
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
    -- Form Status and Configuration
    -- =====================================================================
    FormStatus NVARCHAR(20) NOT NULL DEFAULT 'Draft',
    -- ^ Form status: 'Draft', 'Published', 'Archived'
    -- Draft = Being created/edited
    -- Published = Live and accessible
    -- Archived = No longer accessible
    
    IsPublic BIT NOT NULL DEFAULT 0,
    -- ^ Can form be accessed without authentication?
    -- 0 = Requires authentication
    -- 1 = Public access (no login required)
    
    RequiresApproval BIT NOT NULL DEFAULT 0,
    -- ^ Does form deployment require approval?
    -- 0 = Auto-publish when ready
    -- 1 = Requires head office approval (Epic 2 integration)
    
    -- =====================================================================
    -- Deployment Configuration
    -- =====================================================================
    DeploymentCost DECIMAL(10,2) NULL,
    -- ^ Cost for form deployment (for approval workflow)
    -- Example: $500.00 for complex form deployment
    -- Used for: Company domain approval workflow
    
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
    CONSTRAINT FK_Form_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_Form_UpdatedBy FOREIGN KEY (UpdatedBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_Form_DeletedBy FOREIGN KEY (DeletedBy) 
        REFERENCES [dbo].[User](UserID),
    
    -- Validate FormStatus values
    CONSTRAINT CK_Form_Status CHECK (
        FormStatus IN ('Draft', 'Published', 'Archived')
    ),
    
    -- Validate DeploymentCost is positive
    CONSTRAINT CK_Form_DeploymentCost CHECK (
        DeploymentCost IS NULL OR DeploymentCost >= 0
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

CREATE INDEX IX_Form_Status ON [dbo].[Form](FormStatus, IsDeleted)
    WHERE IsDeleted = 0;
GO

CREATE INDEX IX_Form_Public ON [dbo].[Form](IsPublic, FormStatus, IsDeleted)
    WHERE IsDeleted = 0;
GO

PRINT 'Form table created successfully!';
GO

-- =====================================================================
-- 2. CREATE FormAccessControl TABLE
-- =====================================================================
-- Purpose: Form-level access control for external relationships
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
    -- Access Control Details
    -- =====================================================================
    AccessType NVARCHAR(20) NOT NULL,
    -- ^ Type of access: 'View', 'Edit', 'Manage'
    -- View = Can view form and basic information
    -- Edit = Can edit form content (when form builder is added)
    -- Manage = Can manage form settings and access
    
    RelationshipTypeID INT NOT NULL,
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

-- Unique constraint to prevent duplicate access grants
CREATE UNIQUE INDEX UX_FormAccessControl_Unique ON [dbo].[FormAccessControl](FormID, UserID, CompanyID)
    WHERE IsDeleted = 0;
GO

PRINT 'FormAccessControl table created successfully!';
GO

-- =====================================================================
-- PHASE 2: CREATE HELPER FUNCTIONS
-- =====================================================================

-- =====================================================================
-- 3. CREATE Form Access Check Function
-- =====================================================================
-- Purpose: Check if user has access to form
-- =====================================================================
CREATE FUNCTION [dbo].[CheckFormAccess](@FormID BIGINT, @UserID BIGINT, @AccessType NVARCHAR(20))
RETURNS BIT
AS
BEGIN
    DECLARE @HasAccess BIT = 0;
    
    -- Check if user has the required access type
    IF EXISTS (
        SELECT 1
        FROM [dbo].[FormAccessControl]
        WHERE FormID = @FormID 
            AND UserID = @UserID 
            AND AccessType = @AccessType
            AND IsDeleted = 0
            AND (ExpiryDate IS NULL OR ExpiryDate > GETUTCDATE())
    )
        SET @HasAccess = 1;
    
    RETURN @HasAccess;
END;
GO

PRINT 'Form access check function created successfully!';
GO

-- =====================================================================
-- 4. CREATE Form Deployment Cost Function
-- =====================================================================
-- Purpose: Calculate basic deployment cost for approval workflow
-- =====================================================================
CREATE FUNCTION [dbo].[CalculateFormDeploymentCost](@FormID BIGINT)
RETURNS DECIMAL(10,2)
AS
BEGIN
    DECLARE @DeploymentCost DECIMAL(10,2) = 0;
    
    -- Basic cost calculation (can be enhanced in future)
    -- For Epic 2, we'll use a simple base cost
    -- Future: Can factor in form complexity, field count, etc.
    
    SELECT @DeploymentCost = ISNULL(DeploymentCost, 100.00)
    FROM [dbo].[Form]
    WHERE FormID = @FormID;
    
    -- If no cost set, use default
    IF @DeploymentCost IS NULL
        SET @DeploymentCost = 100.00;
    
    RETURN @DeploymentCost;
END;
GO

PRINT 'Form deployment cost function created successfully!';
GO

-- =====================================================================
-- 5. CREATE Form Status Check Function
-- =====================================================================
-- Purpose: Check if form is ready for deployment
-- =====================================================================
CREATE FUNCTION [dbo].[IsFormReadyForDeployment](@FormID BIGINT)
RETURNS BIT
AS
BEGIN
    DECLARE @IsReady BIT = 0;
    
    -- Check if form is in Draft status and has basic required fields
    IF EXISTS (
        SELECT 1
        FROM [dbo].[Form]
        WHERE FormID = @FormID 
            AND FormStatus = 'Draft'
            AND FormName IS NOT NULL
            AND LEN(TRIM(FormName)) > 0
            AND IsDeleted = 0
    )
        SET @IsReady = 1;
    
    RETURN @IsReady;
END;
GO

PRINT 'Form status check function created successfully!';
GO

-- =====================================================================
-- SUMMARY
-- =====================================================================
PRINT '========================================';
PRINT 'Forms Domain Epic 2 Schema Complete!';
PRINT '========================================';
PRINT 'SIMPLIFIED FOR EPIC 2 SCOPE:';
PRINT '';
PRINT 'Core Tables:';
PRINT '  1. Form (form header and metadata)';
PRINT '  2. FormAccessControl (access control)';
PRINT '';
PRINT 'Helper Functions:';
PRINT '  3. CheckFormAccess (access validation)';
PRINT '  4. CalculateFormDeploymentCost (cost calculation)';
PRINT '  5. IsFormReadyForDeployment (deployment readiness)';
PRINT '';
PRINT 'Key Features:';
PRINT '  ✅ Form header management';
PRINT '  ✅ Form deployment approval integration';
PRINT '  ✅ Form-level access control';
PRINT '  ✅ Event integration';
PRINT '  ✅ Company domain integration';
PRINT '  ✅ Audit trail on all tables';
PRINT '  ✅ Foundation for form builder (Epic 3+)';
PRINT '';
PRINT 'Epic 2 Scope Decisions:';
PRINT '  ✅ Form Header: Core form metadata and management';
PRINT '  ✅ Form Access Control: Integration with Company domain';
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
PRINT '  2. Sally UX review (form header interface design)';
PRINT '  3. Developer implementation planning';
PRINT '  4. Form header and access control testing';
PRINT '========================================';
GO
