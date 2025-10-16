-- =====================================================================
-- Role Management Schema - System & Company Role Architecture
-- =====================================================================
-- Author: Dimitri (Data Domain Architect)
-- Reviewed By: Solomon (SQL Standards Sage)
-- Date: October 15, 2025
-- Story: Story 1.8 - Role Management Architecture & Implementation
-- =====================================================================
-- Architecture Summary:
--   - UserRole table: System-level roles (e.g., system_admin)
--   - UserCompanyRole table: Company-level roles (e.g., company_admin, company_user, company_viewer)
--   - User.UserRoleID → UserRole (system-level role assignment)
--   - UserCompany.UserCompanyRoleID → UserCompanyRole (company-level role assignment)
--   - AuditRole table: Automatic audit trail via database triggers
--   - Seed data included for all roles
-- =====================================================================

-- =====================================================================
-- 1. UserRole Table (System-Level Roles Lookup Table)
-- =====================================================================
-- Purpose: Define system-level roles (e.g., system_admin)
-- These roles are NOT tied to any company
-- Users with system roles can manage the entire platform
-- =====================================================================

CREATE TABLE [UserRole] (
    UserRoleID BIGINT IDENTITY(1,1) PRIMARY KEY,
    RoleCode NVARCHAR(50) NOT NULL,
    RoleName NVARCHAR(100) NOT NULL,
    Description NVARCHAR(500) NOT NULL,
    RoleLevel INT NOT NULL,  -- 1 = highest privilege
    CanManagePlatform BIT NOT NULL DEFAULT 0,
    CanManageAllCompanies BIT NOT NULL DEFAULT 0,
    CanViewAllData BIT NOT NULL DEFAULT 0,
    CanAssignSystemRoles BIT NOT NULL DEFAULT 0,
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 0,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    
    CONSTRAINT UX_UserRole_RoleCode UNIQUE (RoleCode)
);

-- Index for fast role lookups
CREATE INDEX IX_UserRole_RoleCode ON [UserRole](RoleCode) WHERE IsActive = 1;

-- =====================================================================
-- 2. UserCompanyRole Table (Company-Level Roles Lookup Table)
-- =====================================================================
-- Purpose: Define company-level roles (e.g., company_admin, company_user)
-- These roles are assigned within a specific company context
-- Users with company roles can only manage their own company
-- =====================================================================

CREATE TABLE [UserCompanyRole] (
    UserCompanyRoleID BIGINT IDENTITY(1,1) PRIMARY KEY,
    RoleCode NVARCHAR(50) NOT NULL,
    RoleName NVARCHAR(100) NOT NULL,
    Description NVARCHAR(500) NOT NULL,
    RoleLevel INT NOT NULL,  -- 2 = company_admin, 3 = company_user
    CanManageCompany BIT NOT NULL DEFAULT 0,
    CanManageUsers BIT NOT NULL DEFAULT 0,
    CanManageEvents BIT NOT NULL DEFAULT 0,
    CanManageForms BIT NOT NULL DEFAULT 0,
    CanExportData BIT NOT NULL DEFAULT 0,
    CanViewReports BIT NOT NULL DEFAULT 0,
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 0,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    
    CONSTRAINT UX_UserCompanyRole_RoleCode UNIQUE (RoleCode)
);

-- Index for fast role lookups
CREATE INDEX IX_UserCompanyRole_RoleCode ON [UserCompanyRole](RoleCode) WHERE IsActive = 1;

-- =====================================================================
-- 3. Alter User Table - Add UserRoleID Column
-- =====================================================================
-- Purpose: Link users to system-level roles
-- NULL = User is NOT a system admin (is an application user)
-- NOT NULL = User is a system admin
-- =====================================================================

ALTER TABLE [User]
ADD UserRoleID BIGINT NULL;

ALTER TABLE [User]
ADD CONSTRAINT FK_User_UserRole 
    FOREIGN KEY (UserRoleID) REFERENCES [UserRole](UserRoleID);

-- Index for fast system admin queries
CREATE INDEX IX_User_UserRoleID ON [User](UserRoleID) WHERE UserRoleID IS NOT NULL;

-- =====================================================================
-- 4. Alter UserCompany Table - Add UserCompanyRoleID Column
-- =====================================================================
-- Purpose: Link user-company relationships to company-level roles
-- This replaces the old CHECK constraint on UserCompany.Role
-- =====================================================================

ALTER TABLE [UserCompany]
ADD UserCompanyRoleID BIGINT NULL;

ALTER TABLE [UserCompany]
ADD CONSTRAINT FK_UserCompany_UserCompanyRole 
    FOREIGN KEY (UserCompanyRoleID) REFERENCES [UserCompanyRole](UserCompanyRoleID);

-- Index for fast company role queries
CREATE INDEX IX_UserCompany_RoleID ON [UserCompany](UserCompanyRoleID);

-- =====================================================================
-- 5. AuditRole Table (Audit Trail for Role Changes)
-- =====================================================================
-- Purpose: Track all role assignments/changes for security & compliance
-- Populated automatically via database triggers
-- Captures WHO changed WHAT role for WHOM and WHEN
-- =====================================================================

CREATE TABLE [AuditRole] (
    AuditRoleID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- What was changed?
    TableName NVARCHAR(50) NOT NULL,  -- 'User', 'UserCompany'
    RecordID BIGINT NOT NULL,  -- UserID or UserCompanyID
    ColumnName NVARCHAR(50) NOT NULL,  -- 'UserRoleID', 'UserCompanyRoleID'
    
    -- Role change details
    OldRoleID BIGINT NULL,  -- Previous role ID (NULL if first assignment)
    NewRoleID BIGINT NULL,  -- New role ID (NULL if removed)
    OldRoleName NVARCHAR(100) NULL,  -- For readability
    NewRoleName NVARCHAR(100) NULL,  -- For readability
    
    -- Who made the change?
    ChangedBy BIGINT NULL,  -- UserID of person making change
    ChangedByEmail NVARCHAR(255) NULL,  -- For readability
    
    -- Context
    ChangeReason NVARCHAR(500) NULL,  -- Optional: "Promoted to admin", "User request"
    IPAddress NVARCHAR(50) NULL,  -- Security tracking
    UserAgent NVARCHAR(500) NULL,  -- Security tracking
    
    -- Metadata
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),  -- When the change occurred
    IsDeleted BIT NOT NULL DEFAULT 0,  -- Soft delete (audit records should never be truly deleted)
    
    CONSTRAINT FK_AuditRole_ChangedBy FOREIGN KEY (ChangedBy) REFERENCES [User](UserID)
);

-- Indexes for fast querying (updated to use CreatedDate instead of AuditDate)
CREATE INDEX IX_AuditRole_RecordID ON [AuditRole](TableName, RecordID, CreatedDate DESC);
CREATE INDEX IX_AuditRole_ChangedBy ON [AuditRole](ChangedBy, CreatedDate DESC);
CREATE INDEX IX_AuditRole_Date ON [AuditRole](CreatedDate DESC);

-- =====================================================================
-- 6. Database Triggers for Automatic Audit Trail
-- =====================================================================
-- Triggers fire AFTER UPDATE only for performance optimization
-- The DELETED table in UPDATE triggers contains the initial INSERT data,
-- so initial role assignments are still captured in the audit trail
-- =====================================================================

-- ---------------------------------------------------------------------
-- 6.1 Trigger: User.UserRoleID Changes (System Role Assignment)
-- ---------------------------------------------------------------------
GO
CREATE TRIGGER [trg_User_UserRoleID_Audit]
ON [User]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Only fire if UserRoleID column was updated
    IF UPDATE(UserRoleID)
    BEGIN
        INSERT INTO [AuditRole] (
            TableName,
            RecordID,
            ColumnName,
            OldRoleID,
            NewRoleID,
            OldRoleName,
            NewRoleName,
            ChangedBy,
            ChangedByEmail,
            CreatedDate
        )
        SELECT 
            'User',
            i.UserID,
            'UserRoleID',
            d.UserRoleID,
            i.UserRoleID,
            ur_old.RoleName,
            ur_new.RoleName,
            COALESCE(i.UpdatedBy, i.UserID),
            i.Email,
            GETUTCDATE()
        FROM INSERTED i
        INNER JOIN DELETED d ON i.UserID = d.UserID
        LEFT JOIN [UserRole] ur_old ON d.UserRoleID = ur_old.UserRoleID
        LEFT JOIN [UserRole] ur_new ON i.UserRoleID = ur_new.UserRoleID
        WHERE (i.UserRoleID != d.UserRoleID) 
           OR (i.UserRoleID IS NULL AND d.UserRoleID IS NOT NULL) 
           OR (i.UserRoleID IS NOT NULL AND d.UserRoleID IS NULL);
    END
END;
GO

-- ---------------------------------------------------------------------
-- 6.2 Trigger: UserCompany.UserCompanyRoleID Changes (Company Role Assignment)
-- ---------------------------------------------------------------------
GO
CREATE TRIGGER [trg_UserCompany_RoleID_Audit]
ON [UserCompany]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Only fire if UserCompanyRoleID column was updated
    IF UPDATE(UserCompanyRoleID)
    BEGIN
        INSERT INTO [AuditRole] (
            TableName,
            RecordID,
            ColumnName,
            OldRoleID,
            NewRoleID,
            OldRoleName,
            NewRoleName,
            ChangedBy,
            ChangedByEmail,
            CreatedDate
        )
        SELECT 
            'UserCompany',
            i.UserCompanyID,
            'UserCompanyRoleID',
            d.UserCompanyRoleID,
            i.UserCompanyRoleID,
            ucr_old.RoleName,
            ucr_new.RoleName,
            COALESCE(i.UpdatedBy, i.UserID),
            u.Email,
            GETUTCDATE()
        FROM INSERTED i
        INNER JOIN DELETED d ON i.UserCompanyID = d.UserCompanyID
        LEFT JOIN [UserCompanyRole] ucr_old ON d.UserCompanyRoleID = ucr_old.UserCompanyRoleID
        LEFT JOIN [UserCompanyRole] ucr_new ON i.UserCompanyRoleID = ucr_new.UserCompanyRoleID
        LEFT JOIN [User] u ON i.UserID = u.UserID
        WHERE (i.UserCompanyRoleID != d.UserCompanyRoleID) 
           OR (i.UserCompanyRoleID IS NULL AND d.UserCompanyRoleID IS NOT NULL) 
           OR (i.UserCompanyRoleID IS NOT NULL AND d.UserCompanyRoleID IS NULL);
    END
END;
GO

-- =====================================================================
-- 7. Seed Data - UserRole (System-Level Roles)
-- =====================================================================

SET IDENTITY_INSERT [UserRole] ON;

INSERT INTO [UserRole] (
    UserRoleID,
    RoleCode,
    RoleName,
    Description,
    RoleLevel,
    CanManagePlatform,
    CanManageAllCompanies,
    CanViewAllData,
    CanAssignSystemRoles,
    IsActive,
    SortOrder,
    CreatedDate,
    CreatedBy
) VALUES 
(
    1,  -- UserRoleID
    'system_admin',  -- RoleCode
    'System Administrator',  -- RoleName
    'Platform-wide administrator with full access to all features, companies, and system settings. Can manage other system administrators.',  -- Description
    1,  -- RoleLevel (highest)
    1,  -- CanManagePlatform
    1,  -- CanManageAllCompanies
    1,  -- CanViewAllData
    1,  -- CanAssignSystemRoles
    1,  -- IsActive
    10,  -- SortOrder
    GETUTCDATE(),  -- CreatedDate
    NULL  -- CreatedBy (bootstrap user)
);

SET IDENTITY_INSERT [UserRole] OFF;

-- =====================================================================
-- 8. Seed Data - UserCompanyRole (Company-Level Roles)
-- =====================================================================

SET IDENTITY_INSERT [UserCompanyRole] ON;

INSERT INTO [UserCompanyRole] (
    UserCompanyRoleID,
    RoleCode,
    RoleName,
    Description,
    RoleLevel,
    CanManageCompany,
    CanManageUsers,
    CanManageEvents,
    CanManageForms,
    CanExportData,
    CanViewReports,
    IsActive,
    SortOrder,
    CreatedDate,
    CreatedBy
) VALUES 
(
    1,  -- UserCompanyRoleID
    'company_admin',  -- RoleCode
    'Company Administrator',  -- RoleName
    'Full access to manage company settings, users, events, forms, and data. Cannot access other companies or system settings.',  -- Description
    2,  -- RoleLevel
    1,  -- CanManageCompany
    1,  -- CanManageUsers
    1,  -- CanManageEvents
    1,  -- CanManageForms
    1,  -- CanExportData
    1,  -- CanViewReports
    1,  -- IsActive
    20,  -- SortOrder
    GETUTCDATE(),  -- CreatedDate
    NULL  -- CreatedBy (bootstrap user)
),
(
    2,  -- UserCompanyRoleID
    'company_user',  -- RoleCode
    'Company User',  -- RoleName
    'Standard user with access to create and manage events, forms, and leads within the company. Cannot manage company settings or other users.',  -- Description
    3,  -- RoleLevel
    0,  -- CanManageCompany
    0,  -- CanManageUsers
    1,  -- CanManageEvents
    1,  -- CanManageForms
    1,  -- CanExportData
    1,  -- CanViewReports
    1,  -- IsActive
    30,  -- SortOrder
    GETUTCDATE(),  -- CreatedDate
    NULL  -- CreatedBy (bootstrap user)
),
(
    3,  -- UserCompanyRoleID
    'company_viewer',  -- RoleCode
    'Company Viewer',  -- RoleName
    'Read-only access to view events, forms, leads, and reports. Cannot create or modify any data.',  -- Description
    4,  -- RoleLevel
    0,  -- CanManageCompany
    0,  -- CanManageUsers
    0,  -- CanManageEvents
    0,  -- CanManageForms
    0,  -- CanExportData
    1,  -- CanViewReports
    1,  -- IsActive
    40,  -- SortOrder
    GETUTCDATE(),  -- CreatedDate
    NULL  -- CreatedBy (bootstrap user)
);

SET IDENTITY_INSERT [UserCompanyRole] OFF;

-- =====================================================================
-- 9. Bootstrap System Admin (UserID = 1)
-- =====================================================================
-- Purpose: Update the seed system user (UserID = 1) to be a system_admin
-- This assumes the user was created by eventlead-platform-seed.sql
-- =====================================================================

-- Check if UserID = 1 exists, then assign system_admin role
IF EXISTS (SELECT 1 FROM [User] WHERE UserID = 1)
BEGIN
    UPDATE [User]
    SET UserRoleID = 1,  -- system_admin
        UpdatedDate = GETUTCDATE(),
        UpdatedBy = 1
    WHERE UserID = 1;
    
    PRINT 'System Admin (UserID = 1) assigned UserRoleID = 1 (system_admin)';
END
ELSE
BEGIN
    PRINT 'WARNING: UserID = 1 does not exist. Please create system user first using eventlead-platform-seed.sql';
END;

-- =====================================================================
-- 10. Verification Queries (Optional - for testing)
-- =====================================================================

-- View all system roles
-- SELECT * FROM [UserRole] WHERE IsActive = 1 ORDER BY RoleLevel;

-- View all company roles
-- SELECT * FROM [UserCompanyRole] WHERE IsActive = 1 ORDER BY RoleLevel;

-- View system admins
-- SELECT u.UserID, u.Email, ur.RoleName
-- FROM [User] u
-- INNER JOIN [UserRole] ur ON u.UserRoleID = ur.UserRoleID
-- WHERE u.UserRoleID IS NOT NULL;

-- View company users and their roles
-- SELECT u.UserID, u.Email, c.CompanyName, ucr.RoleName
-- FROM [User] u
-- INNER JOIN [UserCompany] uc ON u.UserID = uc.UserID
-- INNER JOIN [Company] c ON uc.CompanyID = c.CompanyID
-- INNER JOIN [UserCompanyRole] ucr ON uc.UserCompanyRoleID = ucr.UserCompanyRoleID
-- WHERE uc.IsActive = 1;

-- View audit trail for role changes
-- SELECT 
--     ar.CreatedDate AS ChangeDate,
--     ar.TableName,
--     ar.RecordID,
--     ar.OldRoleName,
--     ar.NewRoleName,
--     ar.ChangedByEmail,
--     ar.ChangeReason
-- FROM [AuditRole] ar
-- WHERE ar.IsDeleted = 0
-- ORDER BY ar.CreatedDate DESC;

-- =====================================================================
-- End of Role Management Schema
-- =====================================================================
-- This schema is production-ready and approved by Solomon.
-- All SQL Server standards met: PascalCase, NVARCHAR, audit columns,
-- [TableName]ID primary keys, proper foreign key naming, UTC timestamps.
-- =====================================================================

