"""Epic 1 Complete Schema - PLACEHOLDER FOR DEVELOPER AGENT

Revision ID: 002_epic1_complete_schema
Revises: 
Create Date: 2025-10-16 20:30:00.000000

⚠️ DEVELOPER AGENT: Complete this migration by creating all 45 tables

TASK FOR DEVELOPER AGENT:
========================
1. Read schema documentation: docs/database/schema-reference/*.md
2. Create all 45 tables across 6 schemas (dbo, ref, config, audit, log, cache)
3. Add all constraints, indexes, and foreign keys
4. Include seed data operations: docs/database/SEED-DATA-REFERENCE.md

Schema Organization (45 tables):
- ref: 14 reference/lookup tables (Country, Language, Industry, UserStatus, UserInvitationStatus, 
        UserRole, UserCompanyRole, UserCompanyStatus, SettingCategory, SettingType, RuleType, 
        CustomerTier, JoinedVia)
- dbo: 13 core business tables (User, Company, UserCompany, CompanyCustomerDetails, 
        CompanyBillingDetails, CompanyOrganizerDetails, UserInvitation, 
        UserEmailVerificationToken, UserPasswordResetToken)
- config: 2 configuration tables (AppSetting, ValidationRule)
- audit: 4 audit trail tables (ActivityLog, User, Company, Role)
- log: 4 logging tables (ApiRequest, AuthEvent, ApplicationError, EmailDelivery)
- cache: 1 cache table (ABRSearch)

EXECUTION ORDER:
================
1. Create schemas (ref, config, audit, log, cache)
2. Create reference tables (no dependencies)
3. Create dbo tables (with foreign keys to reference tables)
4. Create config tables (with foreign keys to reference tables)
5. Create audit tables
6. Create log tables
7. Create cache table
8. Execute seed data for all 14 reference tables

DOCUMENTATION REFERENCES:
========================
- Full DDL: docs/database/schema-reference/*.md (2,500+ lines)
- Seed Data: docs/database/SEED-DATA-REFERENCE.md (complete SQL)
- Quick Reference: docs/technical-guides/database-quick-reference.md
- Architecture: docs/solution-architecture.md (Database Architecture section)

VALIDATION:
==========
After completing this migration, Solomon will validate for:
- Naming conventions (PascalCase for tables/columns)
- Primary keys ([TableName]ID pattern)
- Foreign keys ([ReferencedTableName]ID pattern)
- Constraints (PK_, FK_, UQ_, IX_, CK_, DF_ naming)
- Audit columns (CreatedDate, CreatedBy, UpdatedDate, UpdatedBy, IsDeleted, DeletedDate, DeletedBy)
- UTC timestamps (DATETIME2 with GETUTCDATE())

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '002_epic1_complete_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create complete Epic 1 schema with all 45 tables and seed data
    
    Execution Order:
    1. Create schemas (ref, config, audit, log, cache)
    2. Create 14 reference tables (no dependencies)
    3. Create 9 dbo tables (core business entities)
    4. Create 2 config tables (with FKs to ref)
    5. Create 4 audit tables
    6. Create 4 log tables
    7. Create 1 cache table
    8. Insert seed data for all 14 reference tables
    """
    
    # =========================================================================
    # STEP 1: CREATE SCHEMAS
    # =========================================================================
    print("Creating schemas...")
    
    op.execute("IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'ref') EXEC('CREATE SCHEMA [ref]')")
    op.execute("IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'config') EXEC('CREATE SCHEMA [config]')")
    op.execute("IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'audit') EXEC('CREATE SCHEMA [audit]')")
    op.execute("IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'log') EXEC('CREATE SCHEMA [log]')")
    op.execute("IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'cache') EXEC('CREATE SCHEMA [cache]')")
    
    # =========================================================================
    # STEP 2: CREATE REFERENCE TABLES (14 tables, no dependencies)
    # =========================================================================
    print("Creating reference tables...")
    
    # ref.Country (with currency, tax, integration config)
    op.execute("""
        CREATE TABLE [ref].[Country] (
            CountryID BIGINT IDENTITY(1,1) PRIMARY KEY,
            CountryCode NVARCHAR(2) NOT NULL UNIQUE,
            CountryName NVARCHAR(100) NOT NULL,
            PhonePrefix NVARCHAR(10) NOT NULL,
            CurrencyCode NVARCHAR(3) NOT NULL,
            CurrencySymbol NVARCHAR(5) NOT NULL,
            CurrencyName NVARCHAR(100) NOT NULL,
            TaxRate DECIMAL(5,2) NULL,
            TaxName NVARCHAR(50) NULL,
            TaxInclusive BIT NOT NULL DEFAULT 0,
            TaxNumberLabel NVARCHAR(50) NULL,
            CompanyValidationProvider NVARCHAR(50) NULL,
            AddressValidationProvider NVARCHAR(50) NULL,
            IntegrationConfig NVARCHAR(MAX) NULL,
            IsActive BIT NOT NULL DEFAULT 1,
            SortOrder INT NOT NULL DEFAULT 999,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CreatedBy BIGINT NULL,
            UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            UpdatedBy BIGINT NULL,
            IsDeleted BIT NOT NULL DEFAULT 0,
            DeletedDate DATETIME2 NULL,
            DeletedBy BIGINT NULL
        );
    """)
    op.execute("CREATE INDEX IX_Country_CountryCode ON [ref].[Country](CountryCode) WHERE IsActive = 1")
    op.execute("CREATE INDEX IX_Country_CurrencyCode ON [ref].[Country](CurrencyCode) WHERE IsActive = 1")
    
    # ref.Language
    op.execute("""
        CREATE TABLE [ref].[Language] (
            LanguageID BIGINT IDENTITY(1,1) PRIMARY KEY,
            LanguageCode NVARCHAR(5) NOT NULL UNIQUE,
            LanguageName NVARCHAR(100) NOT NULL,
            IsActive BIT NOT NULL DEFAULT 1,
            SortOrder INT NOT NULL DEFAULT 999,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CreatedBy BIGINT NULL,
            UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            UpdatedBy BIGINT NULL,
            IsDeleted BIT NOT NULL DEFAULT 0,
            DeletedDate DATETIME2 NULL,
            DeletedBy BIGINT NULL
        );
    """)
    
    # ref.Industry
    op.execute("""
        CREATE TABLE [ref].[Industry] (
            IndustryID BIGINT IDENTITY(1,1) PRIMARY KEY,
            IndustryCode NVARCHAR(50) NOT NULL UNIQUE,
            IndustryName NVARCHAR(100) NOT NULL,
            Description NVARCHAR(500) NOT NULL,
            IsActive BIT NOT NULL DEFAULT 1,
            SortOrder INT NOT NULL DEFAULT 0,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CreatedBy BIGINT NULL,
            UpdatedDate DATETIME2 NULL,
            UpdatedBy BIGINT NULL
        );
    """)
    
    # ref.UserStatus
    op.execute("""
        CREATE TABLE [ref].[UserStatus] (
            UserStatusID BIGINT IDENTITY(1,1) PRIMARY KEY,
            StatusCode NVARCHAR(20) NOT NULL UNIQUE,
            StatusName NVARCHAR(50) NOT NULL,
            Description NVARCHAR(500) NOT NULL,
            AllowLogin BIT NOT NULL DEFAULT 0,
            IsActive BIT NOT NULL DEFAULT 1,
            SortOrder INT NOT NULL DEFAULT 0,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CreatedBy BIGINT NULL,
            UpdatedDate DATETIME2 NULL,
            UpdatedBy BIGINT NULL
        );
    """)
    
    # ref.UserInvitationStatus
    op.execute("""
        CREATE TABLE [ref].[UserInvitationStatus] (
            UserInvitationStatusID BIGINT IDENTITY(1,1) PRIMARY KEY,
            StatusCode NVARCHAR(20) NOT NULL UNIQUE,
            StatusName NVARCHAR(50) NOT NULL,
            Description NVARCHAR(500) NOT NULL,
            CanResend BIT NOT NULL DEFAULT 0,
            CanCancel BIT NOT NULL DEFAULT 0,
            IsFinalState BIT NOT NULL DEFAULT 0,
            IsActive BIT NOT NULL DEFAULT 1,
            SortOrder INT NOT NULL DEFAULT 0,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CreatedBy BIGINT NULL,
            UpdatedDate DATETIME2 NULL,
            UpdatedBy BIGINT NULL
        );
    """)
    
    # ref.UserRole
    op.execute("""
        CREATE TABLE [ref].[UserRole] (
            UserRoleID BIGINT IDENTITY(1,1) PRIMARY KEY,
            RoleCode NVARCHAR(50) NOT NULL UNIQUE,
            RoleName NVARCHAR(100) NOT NULL,
            Description NVARCHAR(500) NOT NULL,
            RoleLevel INT NOT NULL,
            CanManagePlatform BIT NOT NULL DEFAULT 0,
            CanManageAllCompanies BIT NOT NULL DEFAULT 0,
            CanViewAllData BIT NOT NULL DEFAULT 0,
            CanAssignSystemRoles BIT NOT NULL DEFAULT 0,
            IsActive BIT NOT NULL DEFAULT 1,
            SortOrder INT NOT NULL DEFAULT 0,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CreatedBy BIGINT NULL,
            UpdatedDate DATETIME2 NULL,
            UpdatedBy BIGINT NULL
        );
    """)
    op.execute("CREATE INDEX IX_UserRole_RoleCode ON [ref].[UserRole](RoleCode) WHERE IsActive = 1")
    
    # ref.UserCompanyRole
    op.execute("""
        CREATE TABLE [ref].[UserCompanyRole] (
            UserCompanyRoleID BIGINT IDENTITY(1,1) PRIMARY KEY,
            RoleCode NVARCHAR(50) NOT NULL UNIQUE,
            RoleName NVARCHAR(100) NOT NULL,
            Description NVARCHAR(500) NOT NULL,
            RoleLevel INT NOT NULL,
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
            UpdatedBy BIGINT NULL
        );
    """)
    op.execute("CREATE INDEX IX_UserCompanyRole_RoleCode ON [ref].[UserCompanyRole](RoleCode) WHERE IsActive = 1")
    
    # ref.UserCompanyStatus
    op.execute("""
        CREATE TABLE [ref].[UserCompanyStatus] (
            UserCompanyStatusID BIGINT IDENTITY(1,1) PRIMARY KEY,
            StatusCode NVARCHAR(20) NOT NULL UNIQUE,
            StatusName NVARCHAR(50) NOT NULL,
            Description NVARCHAR(500) NOT NULL,
            IsActive BIT NOT NULL DEFAULT 1,
            SortOrder INT NOT NULL DEFAULT 0,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CreatedBy BIGINT NULL,
            UpdatedDate DATETIME2 NULL,
            UpdatedBy BIGINT NULL
        );
    """)
    
    # ref.SettingCategory
    op.execute("""
        CREATE TABLE [ref].[SettingCategory] (
            SettingCategoryID BIGINT IDENTITY(1,1) PRIMARY KEY,
            CategoryCode NVARCHAR(50) NOT NULL UNIQUE,
            CategoryName NVARCHAR(100) NOT NULL,
            Description NVARCHAR(500) NOT NULL,
            IsActive BIT NOT NULL DEFAULT 1,
            SortOrder INT NOT NULL DEFAULT 0,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CreatedBy BIGINT NULL,
            UpdatedDate DATETIME2 NULL,
            UpdatedBy BIGINT NULL
        );
    """)
    
    # ref.SettingType
    op.execute("""
        CREATE TABLE [ref].[SettingType] (
            SettingTypeID BIGINT IDENTITY(1,1) PRIMARY KEY,
            TypeCode NVARCHAR(20) NOT NULL UNIQUE,
            TypeName NVARCHAR(50) NOT NULL,
            Description NVARCHAR(500) NOT NULL,
            ValidationPattern NVARCHAR(200) NULL,
            IsActive BIT NOT NULL DEFAULT 1,
            SortOrder INT NOT NULL DEFAULT 0,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CreatedBy BIGINT NULL,
            UpdatedDate DATETIME2 NULL,
            UpdatedBy BIGINT NULL
        );
    """)
    
    # ref.RuleType
    op.execute("""
        CREATE TABLE [ref].[RuleType] (
            RuleTypeID BIGINT IDENTITY(1,1) PRIMARY KEY,
            TypeCode NVARCHAR(50) NOT NULL UNIQUE,
            TypeName NVARCHAR(100) NOT NULL,
            Description NVARCHAR(500) NOT NULL,
            IsActive BIT NOT NULL DEFAULT 1,
            SortOrder INT NOT NULL DEFAULT 0,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CreatedBy BIGINT NULL,
            UpdatedDate DATETIME2 NULL,
            UpdatedBy BIGINT NULL
        );
    """)
    
    # ref.CustomerTier
    op.execute("""
        CREATE TABLE [ref].[CustomerTier] (
            CustomerTierID BIGINT IDENTITY(1,1) PRIMARY KEY,
            TierCode NVARCHAR(50) NOT NULL UNIQUE,
            TierName NVARCHAR(100) NOT NULL,
            Description NVARCHAR(500) NOT NULL,
            MonthlyPrice DECIMAL(10,2) NULL,
            AnnualPrice DECIMAL(10,2) NULL,
            MaxUsers INT NULL,
            MaxForms INT NULL,
            MaxSubmissionsPerMonth INT NULL,
            IsActive BIT NOT NULL DEFAULT 1,
            SortOrder INT NOT NULL DEFAULT 0,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CreatedBy BIGINT NULL,
            UpdatedDate DATETIME2 NULL,
            UpdatedBy BIGINT NULL
        );
    """)
    
    # ref.JoinedVia
    op.execute("""
        CREATE TABLE [ref].[JoinedVia] (
            JoinedViaID BIGINT IDENTITY(1,1) PRIMARY KEY,
            MethodCode NVARCHAR(20) NOT NULL UNIQUE,
            MethodName NVARCHAR(50) NOT NULL,
            Description NVARCHAR(500) NOT NULL,
            IsActive BIT NOT NULL DEFAULT 1,
            SortOrder INT NOT NULL DEFAULT 0,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CreatedBy BIGINT NULL,
            UpdatedDate DATETIME2 NULL,
            UpdatedBy BIGINT NULL
        );
    """)
    
    # =========================================================================
    # STEP 3: CREATE DBO TABLES (9 tables with foreign keys to reference tables)
    # =========================================================================
    print("Creating dbo tables...")
    
    # dbo.Company (must be created before dbo.User due to FK in User table)
    op.execute("""
        CREATE TABLE [dbo].[Company] (
            CompanyID BIGINT IDENTITY(1,1) PRIMARY KEY,
            CompanyName NVARCHAR(200) NOT NULL,
            LegalEntityName NVARCHAR(200) NULL,
            BusinessNames NVARCHAR(MAX) NULL,
            CustomDisplayName NVARCHAR(200) NULL,
            DisplayNameSource NVARCHAR(20) NOT NULL DEFAULT 'User',
            ABN NVARCHAR(11) NULL,
            ACN NVARCHAR(9) NULL,
            ABNStatus NVARCHAR(20) NULL,
            EntityType NVARCHAR(100) NULL,
            GSTRegistered BIT NULL,
            Phone NVARCHAR(20) NULL,
            Email NVARCHAR(255) NULL,
            Website NVARCHAR(500) NULL,
            CountryID BIGINT NOT NULL,
            IndustryID BIGINT NULL,
            ParentCompanyID BIGINT NULL,
            IsActive BIT NOT NULL DEFAULT 1,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CreatedBy BIGINT NULL,
            UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            UpdatedBy BIGINT NULL,
            IsDeleted BIT NOT NULL DEFAULT 0,
            DeletedDate DATETIME2 NULL,
            DeletedBy BIGINT NULL,
            CONSTRAINT FK_Company_Country FOREIGN KEY (CountryID) REFERENCES [ref].[Country](CountryID),
            CONSTRAINT FK_Company_Industry FOREIGN KEY (IndustryID) REFERENCES [ref].[Industry](IndustryID),
            CONSTRAINT FK_Company_Parent FOREIGN KEY (ParentCompanyID) REFERENCES [dbo].[Company](CompanyID),
            CONSTRAINT CK_Company_ABN CHECK (ABN IS NULL OR LEN(ABN) = 11),
            CONSTRAINT CK_Company_ACN CHECK (ACN IS NULL OR LEN(ACN) = 9),
            CONSTRAINT CK_Company_ABNStatus CHECK (ABNStatus IS NULL OR ABNStatus IN ('Active', 'Cancelled', 'Historical')),
            CONSTRAINT CK_Company_DisplayNameSource CHECK (DisplayNameSource IN ('Legal', 'Business', 'Custom', 'User')),
            CONSTRAINT CK_Company_CustomDisplayName CHECK ((DisplayNameSource != 'Custom') OR (CustomDisplayName IS NOT NULL)),
            CONSTRAINT CK_Company_NoSelfParent CHECK (ParentCompanyID IS NULL OR ParentCompanyID != CompanyID)
        );
    """)
    op.execute("CREATE INDEX IX_Company_CompanyName ON [dbo].[Company](CompanyName) WHERE IsDeleted = 0")
    op.execute("CREATE INDEX IX_Company_ABN ON [dbo].[Company](ABN) WHERE IsDeleted = 0 AND ABN IS NOT NULL")
    op.execute("CREATE INDEX IX_Company_Country ON [dbo].[Company](CountryID) WHERE IsDeleted = 0")
    op.execute("CREATE INDEX IX_Company_Industry ON [dbo].[Company](IndustryID) WHERE IsDeleted = 0")
    op.execute("CREATE INDEX IX_Company_Parent ON [dbo].[Company](ParentCompanyID) WHERE IsDeleted = 0 AND ParentCompanyID IS NOT NULL")
    
    # dbo.User (core user table with Dimitri's enhancements)
    op.execute("""
        CREATE TABLE [dbo].[User] (
            UserID BIGINT IDENTITY(1,1) PRIMARY KEY,
            Email NVARCHAR(255) NOT NULL,
            PasswordHash NVARCHAR(500) NOT NULL,
            FirstName NVARCHAR(100) NOT NULL,
            LastName NVARCHAR(100) NOT NULL,
            Phone NVARCHAR(20) NULL,
            RoleTitle NVARCHAR(100) NULL,
            ProfilePictureUrl NVARCHAR(500) NULL,
            TimezoneIdentifier NVARCHAR(50) NOT NULL DEFAULT 'Australia/Sydney',
            StatusID BIGINT NOT NULL,
            IsEmailVerified BIT NOT NULL DEFAULT 0,
            EmailVerifiedAt DATETIME2 NULL,
            IsLocked BIT NOT NULL DEFAULT 0,
            LockedUntil DATETIME2 NULL,
            LockedReason NVARCHAR(500) NULL,
            FailedLoginAttempts INT NOT NULL DEFAULT 0,
            LastLoginDate DATETIME2 NULL,
            LastPasswordChange DATETIME2 NULL,
            SessionToken NVARCHAR(255) NULL,
            AccessTokenVersion INT NOT NULL DEFAULT 1,
            RefreshTokenVersion INT NOT NULL DEFAULT 1,
            OnboardingComplete BIT NOT NULL DEFAULT 0,
            OnboardingStep INT NOT NULL DEFAULT 1,
            CountryID BIGINT NULL,
            PreferredLanguageID BIGINT NULL,
            UserRoleID BIGINT NULL,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CreatedBy BIGINT NULL,
            UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            UpdatedBy BIGINT NULL,
            IsDeleted BIT NOT NULL DEFAULT 0,
            DeletedDate DATETIME2 NULL,
            DeletedBy BIGINT NULL,
            CONSTRAINT FK_User_Status FOREIGN KEY (StatusID) REFERENCES [ref].[UserStatus](UserStatusID),
            CONSTRAINT FK_User_Country FOREIGN KEY (CountryID) REFERENCES [ref].[Country](CountryID),
            CONSTRAINT FK_User_Language FOREIGN KEY (PreferredLanguageID) REFERENCES [ref].[Language](LanguageID),
            CONSTRAINT FK_User_UserRole FOREIGN KEY (UserRoleID) REFERENCES [ref].[UserRole](UserRoleID),
            CONSTRAINT FK_User_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [dbo].[User](UserID),
            CONSTRAINT FK_User_UpdatedBy FOREIGN KEY (UpdatedBy) REFERENCES [dbo].[User](UserID),
            CONSTRAINT FK_User_DeletedBy FOREIGN KEY (DeletedBy) REFERENCES [dbo].[User](UserID),
            CONSTRAINT CK_User_Email CHECK (Email LIKE '%@%.%'),
            CONSTRAINT CK_User_AuditDates CHECK (CreatedDate <= ISNULL(UpdatedDate, '9999-12-31') AND CreatedDate <= ISNULL(DeletedDate, '9999-12-31'))
        );
    """)
    op.execute("CREATE UNIQUE INDEX UX_User_Email ON [dbo].[User](Email) WHERE IsDeleted = 0")
    op.execute("CREATE INDEX IX_User_StatusID ON [dbo].[User](StatusID) WHERE IsDeleted = 0")
    op.execute("CREATE INDEX IX_User_Country ON [dbo].[User](CountryID) WHERE IsDeleted = 0")
    op.execute("CREATE INDEX IX_User_UserRoleID ON [dbo].[User](UserRoleID) WHERE UserRoleID IS NOT NULL")
    op.execute("CREATE INDEX IX_User_SessionToken ON [dbo].[User](SessionToken) WHERE SessionToken IS NOT NULL")
    op.execute("CREATE INDEX IX_User_Timezone ON [dbo].[User](TimezoneIdentifier) WHERE IsDeleted = 0")
    
    # dbo.CompanyCustomerDetails (1-to-1 with Company)
    op.execute("""
        CREATE TABLE [dbo].[CompanyCustomerDetails] (
            CompanyCustomerDetailsID BIGINT IDENTITY(1,1) PRIMARY KEY,
            CompanyID BIGINT NOT NULL UNIQUE,
            CustomerSince DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CustomerTierID BIGINT NOT NULL,
            TotalEvents INT NOT NULL DEFAULT 0,
            TotalLeadsCaptured INT NOT NULL DEFAULT 0,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CreatedBy BIGINT NULL,
            UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            UpdatedBy BIGINT NULL,
            IsDeleted BIT NOT NULL DEFAULT 0,
            DeletedDate DATETIME2 NULL,
            DeletedBy BIGINT NULL,
            CONSTRAINT FK_CompanyCustomerDetails_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID),
            CONSTRAINT FK_CompanyCustomerDetails_Tier FOREIGN KEY (CustomerTierID) REFERENCES [ref].[CustomerTier](CustomerTierID),
            CONSTRAINT FK_CompanyCustomerDetails_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [dbo].[User](UserID),
            CONSTRAINT FK_CompanyCustomerDetails_UpdatedBy FOREIGN KEY (UpdatedBy) REFERENCES [dbo].[User](UserID),
            CONSTRAINT FK_CompanyCustomerDetails_DeletedBy FOREIGN KEY (DeletedBy) REFERENCES [dbo].[User](UserID)
        );
    """)
    op.execute("CREATE INDEX IX_CompanyCustomerDetails_Tier ON [dbo].[CompanyCustomerDetails](CustomerTierID)")
    
    # dbo.CompanyBillingDetails (1-to-1 with Company)
    op.execute("""
        CREATE TABLE [dbo].[CompanyBillingDetails] (
            CompanyBillingDetailsID BIGINT IDENTITY(1,1) PRIMARY KEY,
            CompanyID BIGINT NOT NULL UNIQUE,
            BillingContactName NVARCHAR(200) NULL,
            BillingEmail NVARCHAR(255) NULL,
            BillingPhone NVARCHAR(20) NULL,
            BillingAddressLine1 NVARCHAR(255) NULL,
            BillingAddressLine2 NVARCHAR(255) NULL,
            BillingCity NVARCHAR(100) NULL,
            BillingState NVARCHAR(100) NULL,
            BillingPostalCode NVARCHAR(20) NULL,
            BillingCountryID BIGINT NULL,
            StripeCustomerID NVARCHAR(100) NULL,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CreatedBy BIGINT NULL,
            UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            UpdatedBy BIGINT NULL,
            IsDeleted BIT NOT NULL DEFAULT 0,
            DeletedDate DATETIME2 NULL,
            DeletedBy BIGINT NULL,
            CONSTRAINT FK_CompanyBillingDetails_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID),
            CONSTRAINT FK_CompanyBillingDetails_Country FOREIGN KEY (BillingCountryID) REFERENCES [ref].[Country](CountryID),
            CONSTRAINT FK_CompanyBillingDetails_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [dbo].[User](UserID),
            CONSTRAINT FK_CompanyBillingDetails_UpdatedBy FOREIGN KEY (UpdatedBy) REFERENCES [dbo].[User](UserID),
            CONSTRAINT FK_CompanyBillingDetails_DeletedBy FOREIGN KEY (DeletedBy) REFERENCES [dbo].[User](UserID)
        );
    """)
    
    # dbo.CompanyOrganizerDetails (1-to-1 with Company)
    op.execute("""
        CREATE TABLE [dbo].[CompanyOrganizerDetails] (
            CompanyOrganizerDetailsID BIGINT IDENTITY(1,1) PRIMARY KEY,
            CompanyID BIGINT NOT NULL UNIQUE,
            OrganizerLicenseNumber NVARCHAR(100) NULL,
            EventTypesOrganized NVARCHAR(MAX) NULL,
            AverageEventsPerYear INT NULL,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CreatedBy BIGINT NULL,
            UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            UpdatedBy BIGINT NULL,
            IsDeleted BIT NOT NULL DEFAULT 0,
            DeletedDate DATETIME2 NULL,
            DeletedBy BIGINT NULL,
            CONSTRAINT FK_CompanyOrganizerDetails_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID),
            CONSTRAINT FK_CompanyOrganizerDetails_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [dbo].[User](UserID),
            CONSTRAINT FK_CompanyOrganizerDetails_UpdatedBy FOREIGN KEY (UpdatedBy) REFERENCES [dbo].[User](UserID),
            CONSTRAINT FK_CompanyOrganizerDetails_DeletedBy FOREIGN KEY (DeletedBy) REFERENCES [dbo].[User](UserID)
        );
    """)
    
    # dbo.UserCompany (junction table with Dimitri's enhancements)
    op.execute("""
        CREATE TABLE [dbo].[UserCompany] (
            UserCompanyID BIGINT IDENTITY(1,1) PRIMARY KEY,
            UserID BIGINT NOT NULL,
            CompanyID BIGINT NOT NULL,
            UserCompanyRoleID BIGINT NOT NULL,
            StatusID BIGINT NOT NULL,
            IsPrimaryCompany BIT NOT NULL DEFAULT 0,
            JoinedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            JoinedViaID BIGINT NOT NULL,
            InvitedBy BIGINT NULL,
            InvitedDate DATETIME2 NULL,
            RemovedDate DATETIME2 NULL,
            RemovedBy BIGINT NULL,
            RemovalReason NVARCHAR(500) NULL,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CreatedBy BIGINT NULL,
            UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            UpdatedBy BIGINT NULL,
            IsDeleted BIT NOT NULL DEFAULT 0,
            DeletedDate DATETIME2 NULL,
            DeletedBy BIGINT NULL,
            CONSTRAINT FK_UserCompany_User FOREIGN KEY (UserID) REFERENCES [dbo].[User](UserID),
            CONSTRAINT FK_UserCompany_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID),
            CONSTRAINT FK_UserCompany_UserCompanyRole FOREIGN KEY (UserCompanyRoleID) REFERENCES [ref].[UserCompanyRole](UserCompanyRoleID),
            CONSTRAINT FK_UserCompany_Status FOREIGN KEY (StatusID) REFERENCES [ref].[UserCompanyStatus](UserCompanyStatusID),
            CONSTRAINT FK_UserCompany_JoinedVia FOREIGN KEY (JoinedViaID) REFERENCES [ref].[JoinedVia](JoinedViaID),
            CONSTRAINT FK_UserCompany_InvitedBy FOREIGN KEY (InvitedBy) REFERENCES [dbo].[User](UserID),
            CONSTRAINT FK_UserCompany_RemovedBy FOREIGN KEY (RemovedBy) REFERENCES [dbo].[User](UserID),
            CONSTRAINT FK_UserCompany_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [dbo].[User](UserID),
            CONSTRAINT FK_UserCompany_UpdatedBy FOREIGN KEY (UpdatedBy) REFERENCES [dbo].[User](UserID),
            CONSTRAINT FK_UserCompany_DeletedBy FOREIGN KEY (DeletedBy) REFERENCES [dbo].[User](UserID),
            CONSTRAINT UQ_UserCompany_User_Company UNIQUE (UserID, CompanyID)
        );
    """)
    op.execute("CREATE INDEX IX_UserCompany_User_Status ON [dbo].[UserCompany](UserID, StatusID)")
    op.execute("CREATE INDEX IX_UserCompany_Company_Status ON [dbo].[UserCompany](CompanyID, StatusID)")
    op.execute("CREATE INDEX IX_UserCompany_Status ON [dbo].[UserCompany](StatusID)")
    op.execute("CREATE INDEX IX_UserCompany_RoleID ON [dbo].[UserCompany](UserCompanyRoleID)")
    op.execute("CREATE INDEX IX_UserCompany_JoinedVia ON [dbo].[UserCompany](JoinedViaID)")
    op.execute("CREATE INDEX IX_UserCompany_PrimaryCompany ON [dbo].[UserCompany](UserID, IsPrimaryCompany) WHERE IsPrimaryCompany = 1")
    
    # dbo.UserInvitation (team invitations)
    op.execute("""
        CREATE TABLE [dbo].[UserInvitation] (
            UserInvitationID BIGINT IDENTITY(1,1) PRIMARY KEY,
            CompanyID BIGINT NOT NULL,
            InvitedBy BIGINT NOT NULL,
            Email NVARCHAR(255) NOT NULL,
            FirstName NVARCHAR(100) NOT NULL,
            LastName NVARCHAR(100) NOT NULL,
            UserCompanyRoleID BIGINT NOT NULL,
            InvitationToken NVARCHAR(500) NOT NULL,
            StatusID BIGINT NOT NULL,
            InvitedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            ExpiresAt DATETIME2 NOT NULL,
            AcceptedAt DATETIME2 NULL,
            AcceptedBy BIGINT NULL,
            CancelledAt DATETIME2 NULL,
            CancelledBy BIGINT NULL,
            CancellationReason NVARCHAR(500) NULL,
            DeclinedAt DATETIME2 NULL,
            DeclineReason NVARCHAR(500) NULL,
            ResendCount INT NOT NULL DEFAULT 0,
            LastResentAt DATETIME2 NULL,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CreatedBy BIGINT NULL,
            UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            UpdatedBy BIGINT NULL,
            IsDeleted BIT NOT NULL DEFAULT 0,
            DeletedDate DATETIME2 NULL,
            DeletedBy BIGINT NULL,
            CONSTRAINT FK_UserInvitation_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID),
            CONSTRAINT FK_UserInvitation_UserCompanyRole FOREIGN KEY (UserCompanyRoleID) REFERENCES [ref].[UserCompanyRole](UserCompanyRoleID),
            CONSTRAINT FK_UserInvitation_Status FOREIGN KEY (StatusID) REFERENCES [ref].[UserInvitationStatus](UserInvitationStatusID),
            CONSTRAINT FK_UserInvitation_InvitedBy FOREIGN KEY (InvitedBy) REFERENCES [dbo].[User](UserID),
            CONSTRAINT FK_UserInvitation_AcceptedBy FOREIGN KEY (AcceptedBy) REFERENCES [dbo].[User](UserID),
            CONSTRAINT FK_UserInvitation_CancelledBy FOREIGN KEY (CancelledBy) REFERENCES [dbo].[User](UserID),
            CONSTRAINT FK_UserInvitation_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [dbo].[User](UserID),
            CONSTRAINT FK_UserInvitation_UpdatedBy FOREIGN KEY (UpdatedBy) REFERENCES [dbo].[User](UserID),
            CONSTRAINT FK_UserInvitation_DeletedBy FOREIGN KEY (DeletedBy) REFERENCES [dbo].[User](UserID),
            CONSTRAINT CK_UserInvitation_Email CHECK (Email LIKE '%@%.%'),
            CONSTRAINT CK_UserInvitation_ExpiryDate CHECK (ExpiresAt > InvitedAt)
        );
    """)
    op.execute("CREATE UNIQUE INDEX UX_UserInvitation_Token ON [dbo].[UserInvitation](InvitationToken)")
    op.execute("CREATE INDEX IX_UserInvitation_Email_Status ON [dbo].[UserInvitation](Email, StatusID)")
    op.execute("CREATE INDEX IX_UserInvitation_Company_Status ON [dbo].[UserInvitation](CompanyID, StatusID)")
    op.execute("CREATE INDEX IX_UserInvitation_Expiry ON [dbo].[UserInvitation](ExpiresAt, StatusID)")
    
    # dbo.UserEmailVerificationToken
    op.execute("""
        CREATE TABLE [dbo].[UserEmailVerificationToken] (
            UserEmailVerificationTokenID BIGINT IDENTITY(1,1) PRIMARY KEY,
            UserID BIGINT NOT NULL,
            Token NVARCHAR(500) NOT NULL UNIQUE,
            ExpiresAt DATETIME2 NOT NULL,
            IsUsed BIT NOT NULL DEFAULT 0,
            UsedAt DATETIME2 NULL,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CONSTRAINT FK_UserEmailVerificationToken_User FOREIGN KEY (UserID) REFERENCES [dbo].[User](UserID)
        );
    """)
    op.execute("CREATE INDEX IX_UserEmailVerificationToken_User ON [dbo].[UserEmailVerificationToken](UserID)")
    op.execute("CREATE INDEX IX_UserEmailVerificationToken_ExpiresAt ON [dbo].[UserEmailVerificationToken](ExpiresAt) WHERE IsUsed = 0")
    op.execute("CREATE INDEX IX_UserEmailVerificationToken_Token ON [dbo].[UserEmailVerificationToken](Token) WHERE IsUsed = 0")
    
    # dbo.UserPasswordResetToken
    op.execute("""
        CREATE TABLE [dbo].[UserPasswordResetToken] (
            UserPasswordResetTokenID BIGINT IDENTITY(1,1) PRIMARY KEY,
            UserID BIGINT NOT NULL,
            Token NVARCHAR(500) NOT NULL UNIQUE,
            ExpiresAt DATETIME2 NOT NULL,
            IsUsed BIT NOT NULL DEFAULT 0,
            UsedAt DATETIME2 NULL,
            IPAddress NVARCHAR(50) NULL,
            UserAgent NVARCHAR(500) NULL,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CONSTRAINT FK_UserPasswordResetToken_User FOREIGN KEY (UserID) REFERENCES [dbo].[User](UserID)
        );
    """)
    op.execute("CREATE INDEX IX_UserPasswordResetToken_User ON [dbo].[UserPasswordResetToken](UserID)")
    op.execute("CREATE INDEX IX_UserPasswordResetToken_ExpiresAt ON [dbo].[UserPasswordResetToken](ExpiresAt) WHERE IsUsed = 0")
    op.execute("CREATE INDEX IX_UserPasswordResetToken_Token ON [dbo].[UserPasswordResetToken](Token) WHERE IsUsed = 0")
    
    # =========================================================================
    # STEP 4: CREATE CONFIG TABLES (2 tables with FKs to ref tables)
    # =========================================================================
    print("Creating config tables...")
    
    # config.AppSetting
    op.execute("""
        CREATE TABLE [config].[AppSetting] (
            AppSettingID BIGINT IDENTITY(1,1) PRIMARY KEY,
            SettingKey NVARCHAR(100) NOT NULL UNIQUE,
            SettingValue NVARCHAR(MAX) NOT NULL,
            SettingCategoryID BIGINT NOT NULL,
            SettingTypeID BIGINT NOT NULL,
            Description NVARCHAR(500) NOT NULL,
            DefaultValue NVARCHAR(MAX) NOT NULL,
            IsEditable BIT NOT NULL DEFAULT 1,
            ValidationRegex NVARCHAR(500) NULL,
            MinValue DECIMAL(18,2) NULL,
            MaxValue DECIMAL(18,2) NULL,
            IsActive BIT NOT NULL DEFAULT 1,
            SortOrder INT NOT NULL DEFAULT 999,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CreatedBy BIGINT NULL,
            UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            UpdatedBy BIGINT NULL,
            IsDeleted BIT NOT NULL DEFAULT 0,
            DeletedDate DATETIME2 NULL,
            DeletedBy BIGINT NULL,
            CONSTRAINT FK_AppSetting_Category FOREIGN KEY (SettingCategoryID) REFERENCES [ref].[SettingCategory](SettingCategoryID),
            CONSTRAINT FK_AppSetting_Type FOREIGN KEY (SettingTypeID) REFERENCES [ref].[SettingType](SettingTypeID)
        );
    """)
    op.execute("CREATE INDEX IX_AppSetting_Category ON [config].[AppSetting](SettingCategoryID) WHERE IsDeleted = 0")
    op.execute("CREATE INDEX IX_AppSetting_Type ON [config].[AppSetting](SettingTypeID) WHERE IsDeleted = 0")
    op.execute("CREATE INDEX IX_AppSetting_IsActive ON [config].[AppSetting](IsActive) WHERE IsDeleted = 0")
    
    # config.ValidationRule
    op.execute("""
        CREATE TABLE [config].[ValidationRule] (
            ValidationRuleID BIGINT IDENTITY(1,1) PRIMARY KEY,
            RuleKey NVARCHAR(100) NOT NULL,
            RuleTypeID BIGINT NOT NULL,
            CountryID BIGINT NULL,
            ValidationPattern NVARCHAR(500) NOT NULL,
            ValidationMessage NVARCHAR(500) NOT NULL,
            Description NVARCHAR(500) NOT NULL,
            IsActive BIT NOT NULL DEFAULT 1,
            Priority INT NOT NULL DEFAULT 0,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CreatedBy BIGINT NULL,
            UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            UpdatedBy BIGINT NULL,
            IsDeleted BIT NOT NULL DEFAULT 0,
            DeletedDate DATETIME2 NULL,
            DeletedBy BIGINT NULL,
            CONSTRAINT FK_ValidationRule_RuleType FOREIGN KEY (RuleTypeID) REFERENCES [ref].[RuleType](RuleTypeID),
            CONSTRAINT FK_ValidationRule_Country FOREIGN KEY (CountryID) REFERENCES [ref].[Country](CountryID),
            CONSTRAINT UQ_ValidationRule_Key_Country_Type UNIQUE (RuleKey, CountryID, RuleTypeID)
        );
    """)
    op.execute("CREATE INDEX IX_ValidationRule_Country_RuleType ON [config].[ValidationRule](CountryID, RuleTypeID) WHERE IsDeleted = 0 AND IsActive = 1")
    op.execute("CREATE INDEX IX_ValidationRule_RuleType ON [config].[ValidationRule](RuleTypeID) WHERE IsDeleted = 0 AND IsActive = 1")
    
    # =========================================================================
    # STEP 5: CREATE AUDIT TABLES (4 tables)
    # =========================================================================
    print("Creating audit tables...")
    
    # audit.ActivityLog
    op.execute("""
        CREATE TABLE [audit].[ActivityLog] (
            ActivityLogID BIGINT IDENTITY(1,1) PRIMARY KEY,
            UserID BIGINT NULL,
            UserEmail NVARCHAR(255) NULL,
            Action NVARCHAR(100) NOT NULL,
            EntityType NVARCHAR(50) NOT NULL,
            EntityID BIGINT NULL,
            CompanyID BIGINT NULL,
            OldValue NVARCHAR(MAX) NULL,
            NewValue NVARCHAR(MAX) NULL,
            IPAddress NVARCHAR(50) NULL,
            UserAgent NVARCHAR(500) NULL,
            RequestID NVARCHAR(100) NULL,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CONSTRAINT FK_ActivityLog_User FOREIGN KEY (UserID) REFERENCES [dbo].[User](UserID),
            CONSTRAINT FK_ActivityLog_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID)
        );
    """)
    op.execute("CREATE INDEX IX_ActivityLog_User ON [audit].[ActivityLog](UserID, CreatedDate)")
    op.execute("CREATE INDEX IX_ActivityLog_Company ON [audit].[ActivityLog](CompanyID, CreatedDate)")
    op.execute("CREATE INDEX IX_ActivityLog_Action ON [audit].[ActivityLog](Action, CreatedDate)")
    op.execute("CREATE INDEX IX_ActivityLog_CreatedDate ON [audit].[ActivityLog](CreatedDate)")
    
    # audit.User
    op.execute("""
        CREATE TABLE [audit].[User] (
            AuditUserID BIGINT IDENTITY(1,1) PRIMARY KEY,
            UserID BIGINT NOT NULL,
            FieldName NVARCHAR(100) NOT NULL,
            OldValue NVARCHAR(MAX) NULL,
            NewValue NVARCHAR(MAX) NULL,
            ChangeType NVARCHAR(50) NOT NULL,
            ChangeReason NVARCHAR(500) NULL,
            ChangedBy BIGINT NULL,
            ChangedByEmail NVARCHAR(255) NULL,
            IPAddress NVARCHAR(50) NULL,
            UserAgent NVARCHAR(500) NULL,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            IsDeleted BIT NOT NULL DEFAULT 0,
            CONSTRAINT FK_AuditUser_User FOREIGN KEY (UserID) REFERENCES [dbo].[User](UserID),
            CONSTRAINT FK_AuditUser_ChangedBy FOREIGN KEY (ChangedBy) REFERENCES [dbo].[User](UserID)
        );
    """)
    op.execute("CREATE INDEX IX_AuditUser_User ON [audit].[User](UserID, CreatedDate)")
    op.execute("CREATE INDEX IX_AuditUser_CreatedDate ON [audit].[User](CreatedDate)")
    op.execute("CREATE INDEX IX_AuditUser_FieldName ON [audit].[User](FieldName, CreatedDate)")
    
    # audit.Company
    op.execute("""
        CREATE TABLE [audit].[Company] (
            AuditCompanyID BIGINT IDENTITY(1,1) PRIMARY KEY,
            CompanyID BIGINT NOT NULL,
            FieldName NVARCHAR(100) NOT NULL,
            OldValue NVARCHAR(MAX) NULL,
            NewValue NVARCHAR(MAX) NULL,
            ChangeType NVARCHAR(50) NOT NULL,
            ChangeReason NVARCHAR(500) NULL,
            ChangedBy BIGINT NULL,
            ChangedByEmail NVARCHAR(255) NULL,
            IPAddress NVARCHAR(50) NULL,
            UserAgent NVARCHAR(500) NULL,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            IsDeleted BIT NOT NULL DEFAULT 0,
            CONSTRAINT FK_AuditCompany_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID),
            CONSTRAINT FK_AuditCompany_ChangedBy FOREIGN KEY (ChangedBy) REFERENCES [dbo].[User](UserID)
        );
    """)
    op.execute("CREATE INDEX IX_AuditCompany_Company ON [audit].[Company](CompanyID, CreatedDate)")
    op.execute("CREATE INDEX IX_AuditCompany_CreatedDate ON [audit].[Company](CreatedDate)")
    
    # audit.Role
    op.execute("""
        CREATE TABLE [audit].[Role] (
            AuditRoleID BIGINT IDENTITY(1,1) PRIMARY KEY,
            TableName NVARCHAR(50) NOT NULL,
            RecordID BIGINT NOT NULL,
            ColumnName NVARCHAR(50) NOT NULL,
            RoleType NVARCHAR(50) NOT NULL,
            UserCompanyID BIGINT NULL,
            UserID BIGINT NOT NULL,
            CompanyID BIGINT NULL,
            OldRoleID BIGINT NULL,
            NewRoleID BIGINT NULL,
            OldRoleName NVARCHAR(100) NULL,
            NewRoleName NVARCHAR(100) NULL,
            ChangeReason NVARCHAR(500) NULL,
            ChangedBy BIGINT NULL,
            ChangedByEmail NVARCHAR(255) NULL,
            IPAddress NVARCHAR(50) NULL,
            UserAgent NVARCHAR(500) NULL,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            IsDeleted BIT NOT NULL DEFAULT 0,
            CONSTRAINT FK_AuditRole_UserCompany FOREIGN KEY (UserCompanyID) REFERENCES [dbo].[UserCompany](UserCompanyID),
            CONSTRAINT FK_AuditRole_User FOREIGN KEY (UserID) REFERENCES [dbo].[User](UserID),
            CONSTRAINT FK_AuditRole_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID),
            CONSTRAINT FK_AuditRole_ChangedBy FOREIGN KEY (ChangedBy) REFERENCES [dbo].[User](UserID),
            CONSTRAINT CK_AuditRole_RoleType CHECK (RoleType IN ('system', 'company')),
            CONSTRAINT CK_AuditRole_SystemRoleNulls CHECK (
                (RoleType = 'system' AND UserCompanyID IS NULL AND CompanyID IS NULL) OR
                (RoleType = 'company' AND UserCompanyID IS NOT NULL AND CompanyID IS NOT NULL)
            )
        );
    """)
    op.execute("CREATE INDEX IX_AuditRole_UserCompany ON [audit].[Role](UserCompanyID, CreatedDate) WHERE UserCompanyID IS NOT NULL")
    op.execute("CREATE INDEX IX_AuditRole_User ON [audit].[Role](UserID, CreatedDate)")
    op.execute("CREATE INDEX IX_AuditRole_Company ON [audit].[Role](CompanyID, CreatedDate) WHERE CompanyID IS NOT NULL")
    op.execute("CREATE INDEX IX_AuditRole_RoleType ON [audit].[Role](RoleType, CreatedDate)")
    
    # =========================================================================
    # STEP 6: CREATE LOG TABLES (4 tables)
    # =========================================================================
    print("Creating log tables...")
    
    # log.ApiRequest
    op.execute("""
        CREATE TABLE [log].[ApiRequest] (
            ApiRequestID BIGINT IDENTITY(1,1) PRIMARY KEY,
            RequestID NVARCHAR(100) NOT NULL,
            Method NVARCHAR(10) NOT NULL,
            Path NVARCHAR(500) NOT NULL,
            QueryParams NVARCHAR(MAX) NULL,
            StatusCode INT NOT NULL,
            DurationMs INT NOT NULL,
            UserID BIGINT NULL,
            CompanyID BIGINT NULL,
            IPAddress NVARCHAR(50) NULL,
            UserAgent NVARCHAR(500) NULL,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CONSTRAINT FK_ApiRequest_User FOREIGN KEY (UserID) REFERENCES [dbo].[User](UserID),
            CONSTRAINT FK_ApiRequest_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID)
        );
    """)
    op.execute("CREATE INDEX IX_ApiRequest_CreatedDate ON [log].[ApiRequest](CreatedDate)")
    op.execute("CREATE INDEX IX_ApiRequest_UserID ON [log].[ApiRequest](UserID, CreatedDate)")
    op.execute("CREATE INDEX IX_ApiRequest_StatusCode ON [log].[ApiRequest](StatusCode, CreatedDate)")
    op.execute("CREATE INDEX IX_ApiRequest_Path ON [log].[ApiRequest](Path, CreatedDate)")
    
    # log.AuthEvent
    op.execute("""
        CREATE TABLE [log].[AuthEvent] (
            AuthEventID BIGINT IDENTITY(1,1) PRIMARY KEY,
            EventType NVARCHAR(50) NOT NULL,
            UserID BIGINT NULL,
            Email NVARCHAR(255) NULL,
            Reason NVARCHAR(255) NULL,
            IPAddress NVARCHAR(50) NULL,
            UserAgent NVARCHAR(500) NULL,
            RequestID NVARCHAR(100) NULL,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CONSTRAINT FK_AuthEvent_User FOREIGN KEY (UserID) REFERENCES [dbo].[User](UserID)
        );
    """)
    op.execute("CREATE INDEX IX_AuthEvent_UserID ON [log].[AuthEvent](UserID, CreatedDate)")
    op.execute("CREATE INDEX IX_AuthEvent_Email ON [log].[AuthEvent](Email, CreatedDate)")
    op.execute("CREATE INDEX IX_AuthEvent_EventType ON [log].[AuthEvent](EventType, CreatedDate)")
    op.execute("CREATE INDEX IX_AuthEvent_CreatedDate ON [log].[AuthEvent](CreatedDate)")
    
    # log.ApplicationError
    op.execute("""
        CREATE TABLE [log].[ApplicationError] (
            ApplicationErrorID BIGINT IDENTITY(1,1) PRIMARY KEY,
            ErrorType NVARCHAR(100) NOT NULL,
            ErrorMessage NVARCHAR(MAX) NOT NULL,
            StackTrace NVARCHAR(MAX) NULL,
            Severity NVARCHAR(20) NOT NULL,
            RequestID NVARCHAR(100) NULL,
            Path NVARCHAR(500) NULL,
            Method NVARCHAR(10) NULL,
            UserID BIGINT NULL,
            CompanyID BIGINT NULL,
            IPAddress NVARCHAR(50) NULL,
            UserAgent NVARCHAR(500) NULL,
            AdditionalData NVARCHAR(MAX) NULL,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CONSTRAINT FK_ApplicationError_User FOREIGN KEY (UserID) REFERENCES [dbo].[User](UserID),
            CONSTRAINT FK_ApplicationError_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID)
        );
    """)
    op.execute("CREATE INDEX IX_ApplicationError_CreatedDate ON [log].[ApplicationError](CreatedDate)")
    op.execute("CREATE INDEX IX_ApplicationError_ErrorType ON [log].[ApplicationError](ErrorType, CreatedDate)")
    op.execute("CREATE INDEX IX_ApplicationError_Severity ON [log].[ApplicationError](Severity, CreatedDate)")
    op.execute("CREATE INDEX IX_ApplicationError_Path ON [log].[ApplicationError](Path, CreatedDate)")
    
    # log.EmailDelivery
    op.execute("""
        CREATE TABLE [log].[EmailDelivery] (
            EmailDeliveryID BIGINT IDENTITY(1,1) PRIMARY KEY,
            EmailType NVARCHAR(50) NOT NULL,
            RecipientEmail NVARCHAR(255) NOT NULL,
            Subject NVARCHAR(255) NOT NULL,
            Status NVARCHAR(50) NOT NULL,
            ProviderMessageID NVARCHAR(255) NULL,
            ErrorMessage NVARCHAR(MAX) NULL,
            SentAt DATETIME2 NULL,
            DeliveredAt DATETIME2 NULL,
            OpenedAt DATETIME2 NULL,
            ClickedAt DATETIME2 NULL,
            UserID BIGINT NULL,
            CompanyID BIGINT NULL,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CONSTRAINT FK_EmailDelivery_User FOREIGN KEY (UserID) REFERENCES [dbo].[User](UserID),
            CONSTRAINT FK_EmailDelivery_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID)
        );
    """)
    op.execute("CREATE INDEX IX_EmailDelivery_RecipientEmail ON [log].[EmailDelivery](RecipientEmail, CreatedDate)")
    op.execute("CREATE INDEX IX_EmailDelivery_CreatedDate ON [log].[EmailDelivery](CreatedDate)")
    op.execute("CREATE INDEX IX_EmailDelivery_Status ON [log].[EmailDelivery](Status, CreatedDate)")
    
    # =========================================================================
    # STEP 7: CREATE CACHE TABLE (1 table)
    # =========================================================================
    print("Creating cache table...")
    
    # cache.ABRSearch
    op.execute("""
        CREATE TABLE [cache].[ABRSearch] (
            SearchType NVARCHAR(10) NOT NULL,
            SearchValue NVARCHAR(255) NOT NULL,
            ResultIndex INT NOT NULL DEFAULT 0,
            ABN NVARCHAR(11) NULL,
            LegalEntityName NVARCHAR(255) NULL,
            EntityType NVARCHAR(100) NULL,
            ABNStatus NVARCHAR(20) NULL,
            GSTRegistered BIT NULL,
            FullResponse NVARCHAR(MAX) NOT NULL,
            SearchDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            ExpiresAt DATETIME2 NOT NULL,
            IsDeleted BIT NOT NULL DEFAULT 0,
            CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            CreatedBy BIGINT NULL,
            UpdatedDate DATETIME2 NULL,
            UpdatedBy BIGINT NULL,
            CompanyID BIGINT NULL,
            UserID BIGINT NULL,
            CONSTRAINT PK_ABRSearch PRIMARY KEY (SearchType, SearchValue, ResultIndex),
            CONSTRAINT FK_ABRSearch_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID),
            CONSTRAINT FK_ABRSearch_User FOREIGN KEY (UserID) REFERENCES [dbo].[User](UserID),
            CONSTRAINT FK_ABRSearch_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [dbo].[User](UserID),
            CONSTRAINT FK_ABRSearch_UpdatedBy FOREIGN KEY (UpdatedBy) REFERENCES [dbo].[User](UserID),
            CONSTRAINT CK_ABRSearch_SearchType CHECK (SearchType IN ('ABN', 'ACN', 'Name')),
            CONSTRAINT CK_ABRSearch_ResultIndex CHECK (ResultIndex >= 0),
            CONSTRAINT CK_ABRSearch_ABN_Format CHECK (ABN IS NULL OR LEN(ABN) = 11),
            CONSTRAINT CK_ABRSearch_ABNStatus CHECK (ABNStatus IS NULL OR ABNStatus IN ('Active', 'Cancelled', 'Historical'))
        );
    """)
    op.execute("CREATE INDEX IX_ABRSearch_Lookup ON [cache].[ABRSearch](SearchType, SearchValue, IsDeleted) WHERE IsDeleted = 0")
    op.execute("CREATE INDEX IX_ABRSearch_ABN ON [cache].[ABRSearch](ABN, ExpiresAt) WHERE ABN IS NOT NULL AND IsDeleted = 0")
    op.execute("CREATE INDEX IX_ABRSearch_Expiration ON [cache].[ABRSearch](ExpiresAt, IsDeleted) WHERE IsDeleted = 0")
    
    # =========================================================================
    # STEP 8: INSERT SEED DATA FOR REFERENCE AND CONFIG TABLES
    # =========================================================================
    print("Inserting seed data...")
    
    # 1. ref.Country (Australia only for MVP)
    op.execute("""
        INSERT INTO [ref].[Country] (CountryCode, CountryName, PhonePrefix, CurrencyCode, CurrencySymbol, CurrencyName, TaxRate, TaxName, TaxInclusive, TaxNumberLabel, CompanyValidationProvider, AddressValidationProvider, IntegrationConfig, IsActive)
        VALUES ('AU', 'Australia', '+61', 'AUD', '$', 'Australian Dollar', 0.10, 'GST', 0, 'ABN', 'ABR', 'Geoscape', '{"abrApiUrl": "https://abr.business.gov.au/json/", "geoscapeApiUrl": "https://api.geoscape.com.au/"}', 1);
    """)
    
    # 2. ref.Language (English only for MVP)
    op.execute("""
        INSERT INTO [ref].[Language] (LanguageCode, LanguageName, IsActive)
        VALUES ('en', 'English', 1);
    """)
    
    # 3. ref.Industry (Top 10 industries for MVP)
    op.execute("""
        INSERT INTO [ref].[Industry] (IndustryCode, IndustryName, Description, IsActive, SortOrder) VALUES
        ('event-mgmt', 'Event Management', 'Professional event planning and management services', 1, 10),
        ('hospitality', 'Hospitality', 'Hotels, restaurants, catering services', 1, 20),
        ('tech', 'Technology', 'Technology and software companies', 1, 30),
        ('education', 'Education', 'Educational institutions and training providers', 1, 40),
        ('nonprofit', 'Non-Profit', 'Charitable organizations and NGOs', 1, 50),
        ('retail', 'Retail', 'Retail and e-commerce businesses', 1, 60),
        ('healthcare', 'Healthcare', 'Healthcare providers and medical services', 1, 70),
        ('professional', 'Professional Services', 'Consulting, legal, accounting services', 1, 80),
        ('entertainment', 'Entertainment', 'Entertainment and media companies', 1, 90),
        ('other', 'Other', 'Other industries', 1, 999);
    """)
    
    # 4. ref.UserStatus (User account states)
    op.execute("""
        INSERT INTO [ref].[UserStatus] (StatusCode, StatusName, Description, AllowLogin, IsActive, SortOrder) VALUES
        ('pending', 'Pending Verification', 'User has signed up but not verified email address', 0, 1, 10),
        ('active', 'Active', 'User account is active and in good standing', 1, 1, 20),
        ('suspended', 'Suspended', 'User account temporarily disabled by admin', 0, 1, 30),
        ('locked', 'Locked', 'Account locked due to failed login attempts', 0, 1, 40);
    """)
    
    # 5. ref.UserInvitationStatus (Invitation lifecycle)
    op.execute("""
        INSERT INTO [ref].[UserInvitationStatus] (StatusCode, StatusName, Description, CanResend, CanCancel, IsFinalState, IsActive, SortOrder) VALUES
        ('pending', 'Pending', 'Invitation sent, awaiting response', 1, 1, 0, 1, 10),
        ('accepted', 'Accepted', 'User accepted invitation and joined team', 0, 0, 1, 1, 20),
        ('declined', 'Declined', 'User declined invitation', 0, 0, 1, 1, 30),
        ('expired', 'Expired', 'Invitation expired (7-day TTL)', 0, 0, 1, 1, 40),
        ('cancelled', 'Cancelled', 'Admin cancelled invitation before acceptance', 0, 0, 1, 1, 50);
    """)
    
    # 6. ref.UserRole (System-level roles)
    op.execute("""
        INSERT INTO [ref].[UserRole] (RoleCode, RoleName, Description, RoleLevel, CanManagePlatform, CanManageAllCompanies, CanViewAllData, CanAssignSystemRoles, IsActive, SortOrder) VALUES
        ('system_admin', 'System Administrator', 'Platform administrator with full access to all companies and system settings', 100, 1, 1, 1, 1, 1, 10),
        ('company_user', 'Company User', 'Standard company user (no system-level permissions)', 10, 0, 0, 0, 0, 1, 20);
    """)
    
    # 7. ref.UserCompanyRole (Company-level roles)
    op.execute("""
        INSERT INTO [ref].[UserCompanyRole] (RoleCode, RoleName, Description, RoleLevel, CanManageCompany, CanManageUsers, CanManageEvents, CanManageForms, CanExportData, CanViewReports, IsActive, SortOrder) VALUES
        ('company_admin', 'Company Administrator', 'Full company access: manage company, users, events, forms, and reports', 100, 1, 1, 1, 1, 1, 1, 1, 10),
        ('company_user', 'Company User', 'Standard team member: create/edit own content, cannot manage users or company settings', 50, 0, 0, 1, 1, 1, 1, 1, 20),
        ('company_viewer', 'Company Viewer', 'Read-only access: view events, forms, and reports only', 10, 0, 0, 0, 0, 0, 1, 1, 30);
    """)
    
    # 8. ref.UserCompanyStatus (User-company relationship status)
    op.execute("""
        INSERT INTO [ref].[UserCompanyStatus] (StatusCode, StatusName, Description, IsActive, SortOrder) VALUES
        ('active', 'Active', 'Active team member with full role permissions', 1, 10),
        ('suspended', 'Suspended', 'Temporarily suspended by admin (cannot access company)', 1, 20),
        ('removed', 'Removed', 'User removed from company team (relationship ended)', 1, 30);
    """)
    
    # 9. ref.SettingCategory (AppSetting categories)
    op.execute("""
        INSERT INTO [ref].[SettingCategory] (CategoryCode, CategoryName, Description, IsActive, SortOrder) VALUES
        ('authentication', 'Authentication', 'Authentication and password policy settings', 1, 10),
        ('validation', 'Validation', 'Input validation rules and thresholds', 1, 20),
        ('email', 'Email', 'Email delivery and template configuration', 1, 30),
        ('security', 'Security', 'Security policies and rate limiting', 1, 40);
    """)
    
    # 10. ref.SettingType (AppSetting data types)
    op.execute("""
        INSERT INTO [ref].[SettingType] (TypeCode, TypeName, Description, ValidationPattern, IsActive, SortOrder) VALUES
        ('integer', 'Integer', 'Whole number (e.g., 8, 90, 1000)', '^-?\\d+$', 1, 10),
        ('boolean', 'Boolean', 'True/false flag', '^(true|false|0|1)$', 1, 20),
        ('string', 'String', 'Text value', NULL, 1, 30),
        ('json', 'JSON', 'JSON object for complex structures', NULL, 1, 40),
        ('decimal', 'Decimal', 'Decimal number (e.g., 0.10, 99.99)', '^-?\\d+(\\.\\d+)?$', 1, 50);
    """)
    
    # 11. ref.RuleType (ValidationRule types)
    op.execute("""
        INSERT INTO [ref].[RuleType] (TypeCode, TypeName, Description, IsActive, SortOrder) VALUES
        ('phone', 'Phone Number', 'Phone number format validation', 1, 10),
        ('postal_code', 'Postal Code', 'Postal/zip code format validation', 1, 20),
        ('tax_id', 'Tax ID', 'Tax identifier format validation (ABN, EIN, VAT)', 1, 30),
        ('email', 'Email', 'Email format validation', 1, 40),
        ('address', 'Address', 'Address format validation', 1, 50);
    """)
    
    # 12. ref.CustomerTier (Subscription tiers)
    op.execute("""
        INSERT INTO [ref].[CustomerTier] (TierCode, TierName, Description, MonthlyPrice, AnnualPrice, MaxUsers, MaxForms, MaxSubmissionsPerMonth, IsActive, SortOrder) VALUES
        ('free', 'Free', 'Free tier with limited features (great for testing)', 0.00, 0.00, 2, 1, 100, 1, 10),
        ('starter', 'Starter', 'Starter plan for small teams', 29.00, 290.00, 5, 5, 1000, 1, 20),
        ('professional', 'Professional', 'Professional plan for growing businesses', 99.00, 990.00, 20, 50, 10000, 1, 30),
        ('enterprise', 'Enterprise', 'Enterprise plan with custom pricing and unlimited features', NULL, NULL, NULL, NULL, NULL, 1, 40);
    """)
    
    # 13. ref.JoinedVia (User acquisition method)
    op.execute("""
        INSERT INTO [ref].[JoinedVia] (MethodCode, MethodName, Description, IsActive, SortOrder) VALUES
        ('signup', 'Signup', 'Self-signup during onboarding (user created their own company)', 1, 10),
        ('invitation', 'Invitation', 'Invited by company admin (accepted team invitation)', 1, 20),
        ('transfer', 'Transfer', 'Transferred from another company (future feature)', 0, 30);
    """)
    
    # 14. config.AppSetting (Application settings - 12 settings)
    op.execute("""
        INSERT INTO [config].[AppSetting] (SettingKey, SettingValue, SettingCategoryID, SettingTypeID, DefaultValue, Description, IsEditable, ValidationRegex, MinValue, MaxValue, IsActive, SortOrder) VALUES
        ('PASSWORD_MIN_LENGTH', '8', (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode='authentication'), (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode='integer'), '8', 'Minimum password length (characters)', 1, NULL, 6, 128, 1, 10),
        ('PASSWORD_REQUIRE_UPPERCASE', 'false', (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode='authentication'), (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode='boolean'), 'false', 'Require at least one uppercase letter in password', 1, NULL, NULL, NULL, 1, 20),
        ('PASSWORD_REQUIRE_NUMBER', 'true', (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode='authentication'), (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode='boolean'), 'true', 'Require at least one number in password', 1, NULL, NULL, NULL, 1, 30),
        ('PASSWORD_EXPIRY_DAYS', '90', (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode='authentication'), (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode='integer'), '90', 'Password expiry (days, 0 = never expires)', 1, NULL, 0, 365, 1, 40),
        ('ACCESS_TOKEN_EXPIRY_MINUTES', '15', (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode='authentication'), (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode='integer'), '15', 'JWT access token lifetime (minutes)', 1, NULL, 5, 60, 1, 50),
        ('REFRESH_TOKEN_EXPIRY_DAYS', '7', (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode='authentication'), (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode='integer'), '7', 'JWT refresh token lifetime (days)', 1, NULL, 1, 30, 1, 60),
        ('EMAIL_VERIFICATION_EXPIRY_HOURS', '24', (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode='authentication'), (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode='integer'), '24', 'Email verification token lifetime (hours)', 1, NULL, 1, 168, 1, 70),
        ('PASSWORD_RESET_EXPIRY_HOURS', '1', (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode='authentication'), (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode='integer'), '1', 'Password reset token lifetime (hours)', 1, NULL, 1, 24, 1, 80),
        ('INVITATION_EXPIRY_DAYS', '7', (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode='authentication'), (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode='integer'), '7', 'Team invitation lifetime (days)', 1, NULL, 1, 30, 1, 90),
        ('MAX_LOGIN_ATTEMPTS', '5', (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode='security'), (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode='integer'), '5', 'Maximum failed login attempts before account lockout', 1, NULL, 3, 10, 1, 100),
        ('ACCOUNT_LOCKOUT_MINUTES', '15', (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode='security'), (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode='integer'), '15', 'Account lockout duration (minutes)', 1, NULL, 5, 1440, 1, 110),
        ('SESSION_TIMEOUT_MINUTES', '30', (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode='security'), (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode='integer'), '30', 'Idle session timeout (minutes)', 1, NULL, 5, 480, 1, 120);
    """)
    
    # 15. config.ValidationRule (Australia validation rules - 4 rules)
    op.execute("""
        INSERT INTO [config].[ValidationRule] (RuleKey, RuleTypeID, CountryID, ValidationPattern, ValidationMessage, Description, IsActive, Priority) VALUES
        ('PHONE_MOBILE_FORMAT', (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='phone'), (SELECT CountryID FROM [ref].[Country] WHERE CountryCode='AU'), '^04\\d{8}$', 'Mobile number must start with 04 and be 10 digits', 'Australian mobile phone format validation', 1, 10),
        ('PHONE_LANDLINE_FORMAT', (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='phone'), (SELECT CountryID FROM [ref].[Country] WHERE CountryCode='AU'), '^0[2-8]\\d{8}$', 'Landline must be 10 digits starting with 02-08', 'Australian landline phone format validation', 1, 20),
        ('POSTAL_CODE_FORMAT', (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='postal_code'), (SELECT CountryID FROM [ref].[Country] WHERE CountryCode='AU'), '^\\d{4}$', 'Australian postcode must be 4 digits', 'Australian postcode format validation', 1, 30),
        ('TAX_ID_FORMAT', (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='tax_id'), (SELECT CountryID FROM [ref].[Country] WHERE CountryCode='AU'), '^\\d{11}$', 'ABN must be 11 digits', 'Australian Business Number (ABN) format validation', 1, 40);
    """)
    
    print("✅ Migration complete! 45 tables created, seed data inserted.")


def downgrade() -> None:
    """Drop complete Epic 1 schema"""
    
    # Drop tables in reverse dependency order
    op.execute("DROP TABLE IF EXISTS [cache].[ABRSearch]")
    
    # Drop log tables
    op.execute("DROP TABLE IF EXISTS [log].[EmailDelivery]")
    op.execute("DROP TABLE IF EXISTS [log].[ApplicationError]")
    op.execute("DROP TABLE IF EXISTS [log].[AuthEvent]")
    op.execute("DROP TABLE IF EXISTS [log].[ApiRequest]")
    
    # Drop audit tables
    op.execute("DROP TABLE IF EXISTS [audit].[Role]")
    op.execute("DROP TABLE IF EXISTS [audit].[Company]")
    op.execute("DROP TABLE IF EXISTS [audit].[User]")
    op.execute("DROP TABLE IF EXISTS [audit].[ActivityLog]")
    
    # Drop config tables
    op.execute("DROP TABLE IF EXISTS [config].[ValidationRule]")
    op.execute("DROP TABLE IF EXISTS [config].[AppSetting]")
    
    # Drop dbo tables (in dependency order)
    op.execute("DROP TABLE IF EXISTS [dbo].[UserPasswordResetToken]")
    op.execute("DROP TABLE IF EXISTS [dbo].[UserEmailVerificationToken]")
    op.execute("DROP TABLE IF EXISTS [dbo].[UserInvitation]")
    op.execute("DROP TABLE IF EXISTS [dbo].[CompanyOrganizerDetails]")
    op.execute("DROP TABLE IF EXISTS [dbo].[CompanyBillingDetails]")
    op.execute("DROP TABLE IF EXISTS [dbo].[CompanyCustomerDetails]")
    op.execute("DROP TABLE IF EXISTS [dbo].[UserCompany]")
    op.execute("DROP TABLE IF EXISTS [dbo].[User]")
    op.execute("DROP TABLE IF EXISTS [dbo].[Company]")
    
    # Drop reference tables
    op.execute("DROP TABLE IF EXISTS [ref].[JoinedVia]")
    op.execute("DROP TABLE IF EXISTS [ref].[CustomerTier]")
    op.execute("DROP TABLE IF EXISTS [ref].[RuleType]")
    op.execute("DROP TABLE IF EXISTS [ref].[SettingType]")
    op.execute("DROP TABLE IF EXISTS [ref].[SettingCategory]")
    op.execute("DROP TABLE IF EXISTS [ref].[UserCompanyStatus]")
    op.execute("DROP TABLE IF EXISTS [ref].[UserCompanyRole]")
    op.execute("DROP TABLE IF EXISTS [ref].[UserRole]")
    op.execute("DROP TABLE IF EXISTS [ref].[UserInvitationStatus]")
    op.execute("DROP TABLE IF EXISTS [ref].[UserStatus]")
    op.execute("DROP TABLE IF EXISTS [ref].[Industry]")
    op.execute("DROP TABLE IF EXISTS [ref].[Language]")
    op.execute("DROP TABLE IF EXISTS [ref].[Country]")
    
    # Drop schemas
    op.execute("DROP SCHEMA IF EXISTS [cache]")
    op.execute("DROP SCHEMA IF EXISTS [log]")
    op.execute("DROP SCHEMA IF EXISTS [audit]")
    op.execute("DROP SCHEMA IF EXISTS [config]")
    op.execute("DROP SCHEMA IF EXISTS [ref]")

