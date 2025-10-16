# Database Rebuild Plan - Epic 1
**Date:** October 16, 2025  
**Author:** Solomon 📜 (Database Migration Validator)  
**Purpose:** Clean database rebuild with all Epic 1 tables, schemas, and seed data  
**Status:** 📋 FOR REVIEW - Do NOT execute until approved

---

## 🎯 OBJECTIVE

**Drop existing database and recreate from scratch with:**
1. ✅ All Epic 1 tables organized by schema (dbo, log, ref, config, audit, cache)
2. ✅ Single Alembic migration (clean history)
3. ✅ All seed data (AppSettings, ValidationRules, Reference data)
4. ✅ International readiness (currency, tax, country-specific integrations)
5. ✅ 100% Solomon-compliant from day 1
6. ✅ Ready for Epic 1 development immediately

---

## ⚠️ WARNINGS & PRECAUTIONS

**CRITICAL - READ BEFORE EXECUTING:**

1. ✅ **No Production Data** - Confirmed: Database is development only, no production data
2. ⚠️ **Destructive Operation** - This will DELETE all existing tables, data, and migrations
3. ⚠️ **Cannot Be Undone** - Once dropped, data cannot be recovered
4. ✅ **Services Must Be Stopped** - Stop all backend services before executing
5. ✅ **Backup Existing Migrations** - Git commit existing work before proceeding

**Status Check:**
- [ ] All backend services stopped
- [ ] Current work committed to git
- [ ] Confirmed database is development only
- [ ] Reviewed all tables and schemas below
- [ ] Approved by Anthony

---

## 📋 EPIC 1 TABLES TO CREATE

### `dbo` Schema (Core Business Entities)

**Epic 1 Core Tables (13 tables):**
1. ✅ `dbo.User` - User accounts
2. ✅ `dbo.UserCompany` - User-company relationships (many-to-many)
3. ✅ `dbo.Company` - Company profiles
4. ✅ `dbo.CompanyCustomerDetails` - Customer-specific data (1-to-1 with Company)
5. ✅ `dbo.CompanyBillingDetails` - Billing information (1-to-1 with Company)
6. ✅ `dbo.CompanyOrganizerDetails` - Organizer-specific data (1-to-1 with Company)
7. ✅ `dbo.UserInvitation` - Team invitations (hierarchical naming)
8. ✅ `dbo.UserEmailVerificationToken` - Email verification tokens (hierarchical naming)
9. ✅ `dbo.UserPasswordResetToken` - Password reset tokens (hierarchical naming)

**Epic 2+ Tables (Not in initial migration):**
- Event (Epic 2)
- Form, Submission, FormField (Epic 5)
- Image (Epic 6)
- Payment, Invoice (Epic 7)

---

### `ref` Schema (Reference/Lookup Data)

**Epic 1 Reference Tables (14 tables):**
1. ✅ `ref.Country` - Country lookup
2. ✅ `ref.Language` - Language lookup
3. ✅ `ref.Industry` - Industry lookup
4. ✅ `ref.UserStatus` - User status lookup (Active, Pending, Locked, Inactive)
5. ✅ `ref.UserInvitationStatus` - User invitation status lookup (Pending, Accepted, Declined, Expired, Cancelled)
6. ✅ `ref.UserRole` - System-level roles (system_admin)
7. ✅ `ref.UserCompanyRole` - Company-level roles (company_admin, company_user, company_viewer)
8. ✅ `ref.UserCompanyStatus` - User-company relationship status (active, suspended, removed)
9. ✅ `ref.AuditRole` - Role change audit trail
10. ✅ `ref.SettingCategory` - AppSetting categories (authentication, validation, email, security)
11. ✅ `ref.SettingType` - AppSetting data types (integer, boolean, string, json, decimal)
12. ✅ `ref.RuleType` - ValidationRule types (phone, postal_code, tax_id, email, address)
13. ✅ `ref.CustomerTier` - Company subscription tiers (Free, Pro, Enterprise)
14. ✅ `ref.JoinedVia` - How user joined company (signup, invitation, transfer)

---

### `config` Schema (Configuration Management)

**Epic 1 Configuration Tables (2 tables):**
1. ✅ `config.AppSetting` - Runtime business rules
2. ✅ `config.ValidationRule` - Country-specific validation

---

### `log` Schema (Technical Logging)

**Epic 1 Logging Tables (4 tables):**
1. ✅ `log.ApiRequest` - HTTP request/response logging
2. ✅ `log.AuthEvent` - Authentication events
3. ✅ `log.ApplicationError` - Application errors
4. ✅ `log.EmailDelivery` - Email delivery tracking

---

### `audit` Schema (Compliance Audit Trail)

**Epic 1 Audit Tables (4 tables):**
1. ✅ `audit.ActivityLog` - All user actions (CRUD operations)
2. ✅ `audit.User` - User record changes (before/after snapshots)
3. ✅ `audit.Company` - Company record changes (before/after snapshots)
4. ✅ `audit.Role` - Role assignment changes (before/after snapshots)

---

### `cache` Schema (External API Cache)

**Epic 1 Cache Tables (1 table):**
1. ✅ `cache.ABRSearch` - ABR API lookup cache (Australian Business Register)

---

**Total Tables:** 45 tables across 6 schemas (14 reference tables, 13 core, 2 config, 4 log, 4 audit, 1 cache)

---

## 🗂️ SEED DATA TO POPULATE

### 1. Reference Data (Minimal for Epic 1)

**Countries (Australia only for Epic 1):**
```sql
INSERT INTO [ref].[Country] 
(CountryCode, CountryName, PhonePrefix, CurrencyCode, CurrencySymbol, CurrencyName, 
 TaxRate, TaxName, TaxInclusive, TaxNumberLabel,
 CompanyValidationProvider, AddressValidationProvider, IntegrationConfig, IsActive) 
VALUES
('AU', 'Australia', '+61', 'AUD', '$', 'Australian Dollar', 
 10.00, 'GST', 1, 'ABN',
 'ABR', 'Geoscape', 
 '{"ABR":{"apiUrl":"https://abr.business.gov.au/api/","cacheDays":30,"requiresGUID":true},"Geoscape":{"apiUrl":"https://api.psma.com.au/v2/","features":["address_autocomplete","address_validation"]}}',
 1);
```

**Notes:**
- **Tax**: Australia uses 10% GST (Goods and Services Tax) with inclusive pricing for consumers
- **Tax Number**: ABN (Australian Business Number) is used for tax registration
- **Integrations**: ABR (Australian Business Register) for company validation, Geoscape (PSMA) for address validation
- **IntegrationConfig**: JSON contains API URLs and provider-specific settings for both ABR and Geoscape

**Languages (English only for Epic 1):**
```sql
INSERT INTO [ref].[Language] (LanguageCode, LanguageName, IsActive) VALUES
('en', 'English', 1);
```

**Industries (Top 10 for Epic 1):**
```sql
INSERT INTO [ref].[Industry] (IndustryName, IsActive) VALUES
('Technology'),
('Healthcare'),
('Finance'),
('Education'),
('Retail'),
('Manufacturing'),
('Professional Services'),
('Real Estate'),
('Hospitality'),
('Other');
```

**User Roles (1 system role + 3 company roles):**
```sql
-- System-level roles (for platform administrators)
INSERT INTO [ref].[UserRole] (RoleCode, RoleName, Description, RoleLevel, CanManagePlatform, CanManageAllCompanies, CanViewAllData, CanAssignSystemRoles, IsActive, SortOrder) VALUES
('system_admin', 'System Administrator', 'Platform-wide administrator with full access to all features, companies, and system settings', 1, 1, 1, 1, 1, 1, 10);

-- Company-level roles (for users within companies)
INSERT INTO [ref].[UserCompanyRole] (RoleCode, RoleName, Description, RoleLevel, CanManageCompany, CanManageUsers, CanManageEvents, CanManageForms, CanExportData, CanViewReports, IsActive, SortOrder) VALUES
('company_admin', 'Company Administrator', 'Full access to manage company settings, users, events, forms, and data', 2, 1, 1, 1, 1, 1, 1, 1, 20),
('company_user', 'Company User', 'Standard user with access to create and manage events, forms, and leads', 3, 0, 0, 1, 1, 1, 1, 1, 30),
('company_viewer', 'Company Viewer', 'Read-only access to view events, forms, leads, and reports', 4, 0, 0, 0, 0, 0, 1, 1, 40);
```

**User Status (4 statuses):**
```sql
INSERT INTO [ref].[UserStatus] (StatusCode, StatusName, Description, IsActive, SortOrder) VALUES
('active', 'Active', 'User account is active and in good standing', 1, 1),
('pending', 'Pending', 'User registered but email not verified', 1, 2),
('locked', 'Locked', 'User account locked due to failed login attempts', 1, 3),
('inactive', 'Inactive', 'User account deactivated', 1, 4);
```

**User Invitation Status (5 statuses):**
```sql
INSERT INTO [ref].[UserInvitationStatus] (StatusCode, StatusName, Description, CanResend, CanCancel, IsFinalState, IsActive, SortOrder) VALUES
('pending', 'Pending', 'Invitation sent, awaiting response', 1, 1, 0, 1, 1),
('accepted', 'Accepted', 'Invitation accepted, user joined company', 0, 0, 1, 1, 2),
('declined', 'Declined', 'Invitation declined by recipient', 0, 0, 1, 1, 3),
('expired', 'Expired', 'Invitation expired before acceptance', 1, 0, 1, 1, 4),
('cancelled', 'Cancelled', 'Invitation cancelled by admin', 0, 0, 1, 1, 5);
```

**User Company Status (3 statuses):**
```sql
INSERT INTO [ref].[UserCompanyStatus] (StatusCode, StatusName, Description, AllowAccess, IsActive, SortOrder) VALUES
('active', 'Active', 'User has normal access to company', 1, 1, 1),
('suspended', 'Suspended', 'User temporarily suspended from company (access revoked)', 0, 1, 2),
('removed', 'Removed', 'User permanently removed from company (soft delete)', 0, 1, 3);
```

**Setting Categories (5 categories):**
```sql
INSERT INTO [ref].[SettingCategory] (CategoryCode, CategoryName, Description, IsActive, SortOrder) VALUES
('authentication', 'Authentication', 'Settings related to user authentication and JWT tokens', 1, 1),
('validation', 'Validation', 'Settings related to email and token validation rules', 1, 2),
('email', 'Email', 'Settings related to email delivery and SMTP configuration', 1, 3),
('security', 'Security', 'Settings related to security policies and brute force protection', 1, 4),
('invitation', 'Invitation', 'Settings related to team invitations and expiry', 1, 5);
```

**Setting Types (5 types):**
```sql
INSERT INTO [ref].[SettingType] (TypeCode, TypeName, Description, ValidationPattern, IsActive, SortOrder) VALUES
('integer', 'Integer', 'Whole number value (e.g., 15, 100)', '^[0-9]+$', 1, 1),
('boolean', 'Boolean', 'True/false value (represented as "true" or "false" string)', '^(true|false)$', 1, 2),
('string', 'String', 'Text value (alphanumeric and special characters)', NULL, 1, 3),
('json', 'JSON', 'Structured JSON data (object or array)', NULL, 1, 4),
('decimal', 'Decimal', 'Decimal number value (e.g., 10.50, 99.99)', '^[0-9]+(\.[0-9]+)?$', 1, 5);
```

**Rule Types (5 types):**
```sql
INSERT INTO [ref].[RuleType] (TypeCode, TypeName, Description, IsActive, SortOrder) VALUES
('phone', 'Phone Number', 'Phone number validation (mobile, landline)', 1, 1),
('postal_code', 'Postal Code', 'Postal/ZIP code validation', 1, 2),
('tax_id', 'Tax ID', 'Tax identification number (ABN, VAT, EIN)', 1, 3),
('email', 'Email', 'Email address validation', 1, 4),
('address', 'Address', 'Physical address validation', 1, 5);
```

**Customer Tiers (3 tiers):**
```sql
INSERT INTO [ref].[CustomerTier] (TierCode, TierName, Description, MonthlyPrice, MaxUsers, MaxEvents, MaxFormsPerEvent, FeatureAccess, IsActive, SortOrder) VALUES
('free', 'Free', 'Free tier with basic features', 0.00, 3, NULL, 5, '{"forms":true,"analytics":false,"api":false,"whitelabel":false}', 1, 1),
('pro', 'Pro', 'Professional tier with advanced features', 49.00, 10, NULL, NULL, '{"forms":true,"analytics":true,"api":true,"whitelabel":false}', 1, 2),
('enterprise', 'Enterprise', 'Enterprise tier with all features and unlimited usage', 299.00, NULL, NULL, NULL, '{"forms":true,"analytics":true,"api":true,"whitelabel":true,"priority_support":true}', 1, 3);
```

**Joined Via (3 methods):**
```sql
INSERT INTO [ref].[JoinedVia] (JoinedViaCode, JoinedViaName, Description, IsActive, SortOrder) VALUES
('signup', 'Signup', 'User created the company during signup (company founder)', 1, 1),
('invitation', 'Invitation', 'User joined via team invitation from another user', 1, 2),
('transfer', 'Transfer', 'User transferred to company by system administrator', 1, 3);
```

---

### 2. Configuration Data (Epic 1 Settings)

**AppSettings (12 settings):**
```sql
-- Note: Using subqueries to get CategoryID and TypeID from reference tables
INSERT INTO [config].[AppSetting] (SettingKey, SettingValue, SettingCategoryID, SettingTypeID, DefaultValue, Description, SortOrder) VALUES
-- Authentication
('jwt_access_token_expiry_minutes', '15', (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode = 'authentication'), (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode = 'integer'), '15', 'JWT access token expiry in minutes', 10),
('jwt_refresh_token_expiry_days', '7', (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode = 'authentication'), (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode = 'integer'), '7', 'JWT refresh token expiry in days', 20),
('password_min_length', '8', (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode = 'authentication'), (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode = 'integer'), '8', 'Minimum password length', 30),
('password_require_uppercase', 'true', (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode = 'authentication'), (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode = 'boolean'), 'true', 'Require uppercase letter in password', 40),
('password_require_lowercase', 'true', (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode = 'authentication'), (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode = 'boolean'), 'true', 'Require lowercase letter in password', 50),
('password_require_number', 'true', (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode = 'authentication'), (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode = 'boolean'), 'true', 'Require number in password', 60),
('password_require_special', 'false', (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode = 'authentication'), (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode = 'boolean'), 'false', 'Require special character in password', 70),

-- Security
('max_failed_login_attempts', '5', (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode = 'security'), (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode = 'integer'), '5', 'Max failed login attempts before lockout', 100),
('account_lockout_minutes', '15', (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode = 'security'), (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode = 'integer'), '15', 'Account lockout duration in minutes', 110),

-- Token Expiry
('email_verification_token_expiry_hours', '24', (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode = 'validation'), (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode = 'integer'), '24', 'Email verification token expiry in hours', 200),
('password_reset_token_expiry_hours', '1', (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode = 'validation'), (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode = 'integer'), '1', 'Password reset token expiry in hours', 210),
('invitation_token_expiry_days', '7', (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode = 'invitation'), (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode = 'integer'), '7', 'Team invitation expiry in days', 220);
```

**ValidationRules (Australia - 4 rules):**
```sql
-- Note: Using subqueries to get RuleTypeID from reference table
INSERT INTO [config].[ValidationRule] (CountryID, RuleTypeID, RuleName, ValidationPattern, ErrorMessage, MinLength, MaxLength, ExampleValue, SortOrder) VALUES
-- Australia CountryID = 1
(1, (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode = 'phone'), 'Australian Mobile', '^\+61[4-5][0-9]{8}$', 'Mobile phone must be +61 followed by 4 or 5 and 8 digits', 12, 12, '+61412345678', 10),
(1, (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode = 'phone'), 'Australian Landline', '^\+61[2-8][0-9]{8}$', 'Landline must be +61 followed by area code (2-8) and 8 digits', 12, 12, '+61298765432', 20),
(1, (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode = 'postal_code'), 'Australian Postcode', '^[0-9]{4}$', 'Postcode must be exactly 4 digits', 4, 4, '2000', 30),
(1, (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode = 'tax_id'), 'Australian ABN', '^[0-9]{11}$', 'ABN must be exactly 11 digits', 11, 11, '12345678901', 40);
```

---

## 🔄 EXECUTION PLAN

### Step 1: Backup & Preparation (Manual)

**1.1 Stop all services:**
```powershell
# Stop backend service if running
# (Ctrl+C in terminal or stop docker containers)
```

**1.2 Commit current work:**
```powershell
git status
git add .
git commit -m "Pre-database rebuild checkpoint"
```

**1.3 Backup existing migrations (optional):**
```powershell
# Copy existing migrations to backup folder
mkdir backend\migrations_backup
Copy-Item backend\migrations\versions\* backend\migrations_backup\
```

---

### Step 2: Drop Database (SQL Server)

**2.1 Connect to SQL Server:**
```sql
-- Connect to master database (NOT EventLeadPlatform)
USE master;
GO
```

**2.2 Drop database:**
```sql
-- Close all connections
ALTER DATABASE [EventLeadPlatform] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
GO

-- Drop database
DROP DATABASE IF EXISTS [EventLeadPlatform];
GO
```

**2.3 Recreate database:**
```sql
-- Create fresh database
CREATE DATABASE [EventLeadPlatform];
GO

-- Set to multi-user mode
ALTER DATABASE [EventLeadPlatform] SET MULTI_USER;
GO

-- Verify
SELECT name, state_desc, user_access_desc 
FROM sys.databases 
WHERE name = 'EventLeadPlatform';
GO
```

---

### Step 3: Reset Alembic (Backend)

**3.1 Delete existing migrations:**
```powershell
# Navigate to backend
cd backend

# Remove all version files
Remove-Item migrations\versions\*.py

# Verify
Get-ChildItem migrations\versions\
# Should show: No items found
```

**3.2 Verify Alembic configuration:**
```powershell
# Check alembic.ini points to correct database
# sqlalchemy.url should be: mssql+pyodbc://localhost/EventLeadPlatform?driver=ODBC+Driver+18+for+SQL+Server&Trusted_Connection=Yes&TrustServerCertificate=yes
```

---

### Step 4: Create Initial Migration (Automated)

**4.1 Create migration file:**
```powershell
# This will be provided as a complete migration script
# File: backend/migrations/versions/001_initial_epic1_schema.py
```

**4.2 Migration will create:**
- ✅ Schemas: log, ref, config (dbo exists by default)
- ✅ All 22 Epic 1 tables
- ✅ All foreign keys and constraints
- ✅ All indexes
- ✅ All seed data

---

### Step 5: Apply Migration

**5.1 Stamp Alembic (if needed):**
```powershell
cd backend
alembic stamp head
```

**5.2 Run migration:**
```powershell
alembic upgrade head
```

**5.3 Verify database:**
```sql
-- Check schemas created
SELECT name FROM sys.schemas WHERE name IN ('log', 'ref', 'config');

-- Check table count
SELECT s.name AS SchemaName, t.name AS TableName
FROM sys.tables t
INNER JOIN sys.schemas s ON s.schema_id = t.schema_id
WHERE s.name IN ('dbo', 'log', 'ref', 'config')
ORDER BY s.name, t.name;

-- Should show 22 tables

-- Check seed data
SELECT COUNT(*) FROM [ref].[Country];       -- Should be 1 (Australia)
SELECT COUNT(*) FROM [ref].[Language];      -- Should be 1 (English)
SELECT COUNT(*) FROM [ref].[Industry];      -- Should be 10
SELECT COUNT(*) FROM [config].[AppSetting]; -- Should be 12
SELECT COUNT(*) FROM [config].[ValidationRule]; -- Should be 4
```

---

## 📄 COMPLETE TABLE DEFINITIONS

### `ref.Country` (Reference Data)

```sql
CREATE TABLE [ref].[Country] (
    CountryID BIGINT IDENTITY(1,1) PRIMARY KEY,
    CountryCode NVARCHAR(2) NOT NULL UNIQUE,     -- ISO 3166-1 alpha-2: 'AU', 'US', 'NZ'
    CountryName NVARCHAR(100) NOT NULL,          -- 'Australia', 'United States'
    PhonePrefix NVARCHAR(10) NOT NULL,           -- '+61', '+1'
    
    -- Currency (essential for international billing/payments)
    CurrencyCode NVARCHAR(3) NOT NULL,           -- ISO 4217: 'AUD', 'USD', 'EUR'
    CurrencySymbol NVARCHAR(5) NOT NULL,         -- '$', '€', '£', '¥'
    CurrencyName NVARCHAR(100) NOT NULL,         -- 'Australian Dollar', 'US Dollar'
    
    -- Tax configuration (for international billing/compliance)
    TaxRate DECIMAL(5,2) NULL,                   -- 10.00 for 10% GST, 20.00 for 20% VAT
    TaxName NVARCHAR(50) NULL,                   -- 'GST', 'VAT', 'Sales Tax'
    TaxInclusive BIT NOT NULL DEFAULT 1,         -- TRUE = show prices inclusive of tax (AU/UK), FALSE = exclusive (US)
    TaxNumberLabel NVARCHAR(50) NULL,            -- 'ABN', 'VAT Number', 'EIN', 'Tax ID'
    
    -- Country-specific integrations (Australia-first approach)
    CompanyValidationProvider NVARCHAR(50) NULL, -- 'ABR', 'CompaniesHouse', 'Google', NULL
    AddressValidationProvider NVARCHAR(50) NULL, -- 'Geoscape', 'RoyalMail', 'USPS', 'Google', NULL
    IntegrationConfig NVARCHAR(MAX) NULL,        -- JSON: API endpoints, keys, provider-specific settings
    
    -- Status & sorting
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 999,
    
    -- Audit trail
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL
);

-- Indexes
CREATE INDEX IX_Country_CountryCode ON [ref].[Country](CountryCode) WHERE IsActive = 1;
CREATE INDEX IX_Country_CurrencyCode ON [ref].[Country](CurrencyCode) WHERE IsActive = 1;
```

**Design Philosophy:**
- **Tax fields**: Essential for international billing (Epic 7 Payments). Australia uses 10% GST with inclusive pricing for consumers.
- **Integration providers**: Country-specific APIs for company validation (ABR) and address validation (Geoscape) with fallback to Google.
- **IntegrationConfig JSON**: Flexible config for API URLs, keys, cache settings, feature flags per provider.
- **Extensibility**: Additional localization fields (DateFormat, TimeFormat, PostalCodeFormat) can be added in future epics when needed.

---

### `ref.Language` (Reference Data)

```sql
CREATE TABLE [ref].[Language] (
    LanguageID BIGINT IDENTITY(1,1) PRIMARY KEY,
    LanguageCode NVARCHAR(5) NOT NULL UNIQUE,    -- 'en', 'en-AU', 'es'
    LanguageName NVARCHAR(100) NOT NULL,         -- 'English', 'Spanish'
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 999,
    -- Audit trail
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL
);
```

---

### `ref.Industry` (Reference Data)

```sql
CREATE TABLE [ref].[Industry] (
    IndustryID BIGINT IDENTITY(1,1) PRIMARY KEY,
    IndustryName NVARCHAR(100) NOT NULL UNIQUE,
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 999,
    -- Audit trail
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL
);
```

---

### `config.AppSetting` (Configuration)

```sql
CREATE TABLE [config].[AppSetting] (
    AppSettingID BIGINT IDENTITY(1,1) PRIMARY KEY,
    SettingKey NVARCHAR(100) NOT NULL UNIQUE,
    SettingValue NVARCHAR(MAX) NOT NULL,
    SettingCategoryID BIGINT NOT NULL,           -- FK to ref.SettingCategory
    SettingTypeID BIGINT NOT NULL,               -- FK to ref.SettingType
    Description NVARCHAR(500) NOT NULL,
    DefaultValue NVARCHAR(MAX) NOT NULL,
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 999,
    -- Audit trail
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,
    CONSTRAINT FK_AppSetting_Category FOREIGN KEY (SettingCategoryID) REFERENCES [ref].[SettingCategory](SettingCategoryID),
    CONSTRAINT FK_AppSetting_Type FOREIGN KEY (SettingTypeID) REFERENCES [ref].[SettingType](SettingTypeID),
    CONSTRAINT FK_AppSetting_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_AppSetting_UpdatedBy FOREIGN KEY (UpdatedBy) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_AppSetting_DeletedBy FOREIGN KEY (DeletedBy) REFERENCES [dbo].[User](UserID)
);

-- Indexes
CREATE INDEX IX_AppSetting_Category ON [config].[AppSetting](SettingCategoryID) WHERE IsDeleted = 0;
CREATE INDEX IX_AppSetting_Type ON [config].[AppSetting](SettingTypeID) WHERE IsDeleted = 0;
CREATE INDEX IX_AppSetting_IsActive ON [config].[AppSetting](IsActive) WHERE IsDeleted = 0;
```

---

### `config.ValidationRule` (Configuration)

```sql
CREATE TABLE [config].[ValidationRule] (
    ValidationRuleID BIGINT IDENTITY(1,1) PRIMARY KEY,
    CountryID BIGINT NOT NULL,
    RuleTypeID BIGINT NOT NULL,                  -- FK to ref.RuleType
    RuleName NVARCHAR(100) NOT NULL,
    ValidationPattern NVARCHAR(500) NOT NULL,    -- Regex pattern
    ErrorMessage NVARCHAR(200) NOT NULL,
    MinLength INT NULL,
    MaxLength INT NULL,
    ExampleValue NVARCHAR(100) NULL,
    SortOrder INT NOT NULL DEFAULT 999,
    IsActive BIT NOT NULL DEFAULT 1,
    -- Audit trail
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,
    CONSTRAINT FK_ValidationRule_Country FOREIGN KEY (CountryID) REFERENCES [ref].[Country](CountryID),
    CONSTRAINT FK_ValidationRule_RuleType FOREIGN KEY (RuleTypeID) REFERENCES [ref].[RuleType](RuleTypeID),
    CONSTRAINT FK_ValidationRule_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_ValidationRule_UpdatedBy FOREIGN KEY (UpdatedBy) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_ValidationRule_DeletedBy FOREIGN KEY (DeletedBy) REFERENCES [dbo].[User](UserID),
    CONSTRAINT CK_ValidationRule_MinLength CHECK (MinLength IS NULL OR MinLength > 0),
    CONSTRAINT CK_ValidationRule_MaxLength CHECK (MaxLength IS NULL OR MaxLength > 0),
    CONSTRAINT CK_ValidationRule_LengthRange CHECK (MinLength IS NULL OR MaxLength IS NULL OR MinLength <= MaxLength)
);

-- Indexes
CREATE INDEX IX_ValidationRule_Country_RuleType ON [config].[ValidationRule](CountryID, RuleTypeID) WHERE IsDeleted = 0 AND IsActive = 1;
CREATE INDEX IX_ValidationRule_RuleType ON [config].[ValidationRule](RuleTypeID) WHERE IsDeleted = 0 AND IsActive = 1;
```

---

### `ref.UserRole` (System-Level Roles)

```sql
-- Purpose: System-level roles for platform administrators
-- Users with system roles can manage the entire platform
CREATE TABLE [ref].[UserRole] (
    UserRoleID BIGINT IDENTITY(1,1) PRIMARY KEY,
    RoleCode NVARCHAR(50) NOT NULL UNIQUE,       -- 'system_admin'
    RoleName NVARCHAR(100) NOT NULL,             -- 'System Administrator'
    Description NVARCHAR(500) NOT NULL,
    RoleLevel INT NOT NULL,                      -- 1 = highest privilege
    CanManagePlatform BIT NOT NULL DEFAULT 0,
    CanManageAllCompanies BIT NOT NULL DEFAULT 0,
    CanViewAllData BIT NOT NULL DEFAULT 0,
    CanAssignSystemRoles BIT NOT NULL DEFAULT 0,
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 0,
    -- Audit trail (simplified for reference data)
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL
);

-- Index for fast role lookups
CREATE INDEX IX_UserRole_RoleCode ON [ref].[UserRole](RoleCode) WHERE IsActive = 1;
```

---

### `ref.UserCompanyRole` (Company-Level Roles)

```sql
-- Purpose: Company-level roles for users within companies
-- These roles are assigned within a specific company context
CREATE TABLE [ref].[UserCompanyRole] (
    UserCompanyRoleID BIGINT IDENTITY(1,1) PRIMARY KEY,
    RoleCode NVARCHAR(50) NOT NULL UNIQUE,       -- 'company_admin', 'company_user', 'company_viewer'
    RoleName NVARCHAR(100) NOT NULL,             -- 'Company Administrator', etc.
    Description NVARCHAR(500) NOT NULL,
    RoleLevel INT NOT NULL,                      -- 2 = company_admin, 3 = company_user, 4 = company_viewer
    CanManageCompany BIT NOT NULL DEFAULT 0,
    CanManageUsers BIT NOT NULL DEFAULT 0,
    CanManageEvents BIT NOT NULL DEFAULT 0,
    CanManageForms BIT NOT NULL DEFAULT 0,
    CanExportData BIT NOT NULL DEFAULT 0,
    CanViewReports BIT NOT NULL DEFAULT 0,
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 0,
    -- Audit trail (simplified for reference data)
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL
);

-- Index for fast role lookups
CREATE INDEX IX_UserCompanyRole_RoleCode ON [ref].[UserCompanyRole](RoleCode) WHERE IsActive = 1;
```

---

### `ref.AuditRole` (Role Change Audit Trail)

```sql
-- Purpose: Track all role assignments/changes for security & compliance
-- Populated automatically via database triggers
CREATE TABLE [ref].[AuditRole] (
    AuditRoleID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- What was changed?
    TableName NVARCHAR(50) NOT NULL,             -- 'User', 'UserCompany'
    RecordID BIGINT NOT NULL,                    -- UserID or UserCompanyID
    ColumnName NVARCHAR(50) NOT NULL,            -- 'UserRoleID', 'UserCompanyRoleID'
    
    -- Role change details
    OldRoleID BIGINT NULL,                       -- Previous role ID (NULL if first assignment)
    NewRoleID BIGINT NULL,                       -- New role ID (NULL if removed)
    OldRoleName NVARCHAR(100) NULL,              -- For readability
    NewRoleName NVARCHAR(100) NULL,              -- For readability
    
    -- Who made the change?
    ChangedBy BIGINT NULL,                       -- UserID of person making change
    ChangedByEmail NVARCHAR(255) NULL,           -- For readability
    
    -- Context
    ChangeReason NVARCHAR(500) NULL,             -- Optional: "Promoted to admin"
    IPAddress NVARCHAR(50) NULL,                 -- Security tracking
    UserAgent NVARCHAR(500) NULL,                -- Security tracking
    
    -- Metadata
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    IsDeleted BIT NOT NULL DEFAULT 0,            -- Soft delete (audit records never truly deleted)
    
    CONSTRAINT FK_AuditRole_ChangedBy FOREIGN KEY (ChangedBy) REFERENCES [dbo].[User](UserID)
);

-- Indexes for fast querying
CREATE INDEX IX_AuditRole_RecordID ON [ref].[AuditRole](TableName, RecordID, CreatedDate DESC);
CREATE INDEX IX_AuditRole_ChangedBy ON [ref].[AuditRole](ChangedBy, CreatedDate DESC);
CREATE INDEX IX_AuditRole_Date ON [ref].[AuditRole](CreatedDate DESC);
```

---

### `ref.UserStatus` (Reference Data)

```sql
CREATE TABLE [ref].[UserStatus] (
    UserStatusID BIGINT IDENTITY(1,1) PRIMARY KEY,
    StatusCode NVARCHAR(20) NOT NULL UNIQUE,     -- 'active', 'pending', 'locked', 'inactive'
    StatusName NVARCHAR(50) NOT NULL,            -- 'Active', 'Pending', 'Locked', 'Inactive'
    Description NVARCHAR(500) NOT NULL,
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 999,
    -- Audit trail
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL
);
```

---

### `ref.UserInvitationStatus` (Reference Data)

```sql
CREATE TABLE [ref].[UserInvitationStatus] (
    UserInvitationStatusID BIGINT IDENTITY(1,1) PRIMARY KEY,
    StatusCode NVARCHAR(20) NOT NULL UNIQUE,     -- 'pending', 'accepted', 'declined', 'expired', 'cancelled'
    StatusName NVARCHAR(50) NOT NULL,            -- 'Pending', 'Accepted', 'Declined', 'Expired', 'Cancelled'
    Description NVARCHAR(500) NOT NULL,
    CanResend BIT NOT NULL DEFAULT 0,            -- Can invitation be resent in this status?
    CanCancel BIT NOT NULL DEFAULT 0,            -- Can invitation be cancelled in this status?
    IsFinalState BIT NOT NULL DEFAULT 0,         -- Is this a terminal state?
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 999,
    -- Audit trail
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL
);
```

---

### `ref.UserCompanyStatus` (Reference Data)

```sql
CREATE TABLE [ref].[UserCompanyStatus] (
    UserCompanyStatusID BIGINT IDENTITY(1,1) PRIMARY KEY,
    StatusCode NVARCHAR(20) NOT NULL UNIQUE,     -- 'active', 'suspended', 'removed'
    StatusName NVARCHAR(50) NOT NULL,            -- 'Active', 'Suspended', 'Removed'
    Description NVARCHAR(500) NOT NULL,
    AllowAccess BIT NOT NULL DEFAULT 1,          -- Can user access company in this status?
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 999,
    -- Audit trail
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL
);
```

---

### `ref.SettingCategory` (Reference Data)

```sql
CREATE TABLE [ref].[SettingCategory] (
    SettingCategoryID BIGINT IDENTITY(1,1) PRIMARY KEY,
    CategoryCode NVARCHAR(50) NOT NULL UNIQUE,   -- 'authentication', 'validation', 'email', 'security', 'invitation'
    CategoryName NVARCHAR(100) NOT NULL,         -- 'Authentication', 'Validation', 'Email', 'Security'
    Description NVARCHAR(500) NOT NULL,
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 999,
    -- Audit trail
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL
);
```

---

### `ref.SettingType` (Reference Data)

```sql
CREATE TABLE [ref].[SettingType] (
    SettingTypeID BIGINT IDENTITY(1,1) PRIMARY KEY,
    TypeCode NVARCHAR(20) NOT NULL UNIQUE,       -- 'integer', 'boolean', 'string', 'json', 'decimal'
    TypeName NVARCHAR(50) NOT NULL,              -- 'Integer', 'Boolean', 'String', 'JSON', 'Decimal'
    Description NVARCHAR(500) NOT NULL,
    ValidationPattern NVARCHAR(200) NULL,        -- Regex for validation (if applicable)
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 999,
    -- Audit trail
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL
);
```

---

### `ref.RuleType` (Reference Data)

```sql
CREATE TABLE [ref].[RuleType] (
    RuleTypeID BIGINT IDENTITY(1,1) PRIMARY KEY,
    TypeCode NVARCHAR(50) NOT NULL UNIQUE,       -- 'phone', 'postal_code', 'tax_id', 'email', 'address'
    TypeName NVARCHAR(100) NOT NULL,             -- 'Phone Number', 'Postal Code', 'Tax ID', 'Email', 'Address'
    Description NVARCHAR(500) NOT NULL,
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 999,
    -- Audit trail
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL
);
```

---

### `ref.CustomerTier` (Reference Data)

```sql
CREATE TABLE [ref].[CustomerTier] (
    CustomerTierID BIGINT IDENTITY(1,1) PRIMARY KEY,
    TierCode NVARCHAR(50) NOT NULL UNIQUE,       -- 'free', 'pro', 'enterprise'
    TierName NVARCHAR(100) NOT NULL,             -- 'Free', 'Pro', 'Enterprise'
    Description NVARCHAR(500) NOT NULL,
    MonthlyPrice DECIMAL(10,2) NOT NULL DEFAULT 0.00,  -- Price in AUD
    MaxUsers INT NULL,                           -- NULL = unlimited
    MaxEvents INT NULL,                          -- NULL = unlimited
    MaxFormsPerEvent INT NULL,                   -- NULL = unlimited
    FeatureAccess NVARCHAR(MAX) NULL,            -- JSON: List of features enabled
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 999,
    -- Audit trail
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL
);
```

---

### `ref.JoinedVia` (Reference Data)

```sql
CREATE TABLE [ref].[JoinedVia] (
    JoinedViaID BIGINT IDENTITY(1,1) PRIMARY KEY,
    JoinedViaCode NVARCHAR(20) NOT NULL UNIQUE,  -- 'signup', 'invitation', 'transfer'
    JoinedViaName NVARCHAR(50) NOT NULL,         -- 'Signup', 'Invitation', 'Transfer'
    Description NVARCHAR(500) NOT NULL,
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 999,
    -- Audit trail
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL
);
```

---

### `dbo.User` (Core Business - Dimitri's Enhanced Design)

```sql
CREATE TABLE [dbo].[User] (
    UserID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Authentication Credentials
    -- =====================================================================
    Email NVARCHAR(255) NOT NULL UNIQUE,
    PasswordHash NVARCHAR(500) NOT NULL,         -- bcrypt hash
    
    -- =====================================================================
    -- Profile (Dimitri's Design)
    -- =====================================================================
    FirstName NVARCHAR(100) NOT NULL,
    LastName NVARCHAR(100) NOT NULL,
    Phone NVARCHAR(20) NULL,
    RoleTitle NVARCHAR(100) NULL,                -- Job title: "Marketing Manager", "Event Coordinator"
    ProfilePictureUrl NVARCHAR(500) NULL,        -- Avatar URL (Azure Blob Storage)
    TimezoneIdentifier NVARCHAR(50) NOT NULL DEFAULT 'Australia/Sydney',  -- IANA timezone for UI display
    
    -- =====================================================================
    -- Status & Account State
    -- =====================================================================
    StatusID BIGINT NOT NULL,                    -- FK to ref.UserStatus
    IsEmailVerified BIT NOT NULL DEFAULT 0,
    EmailVerifiedAt DATETIME2 NULL,              -- When email was verified (audit trail)
    IsLocked BIT NOT NULL DEFAULT 0,
    LockedUntil DATETIME2 NULL,
    FailedLoginAttempts INT NOT NULL DEFAULT 0,
    LastLoginDate DATETIME2 NULL,
    LastPasswordChange DATETIME2 NULL,           -- For "change password every 90 days" policy
    
    -- =====================================================================
    -- Session Management (Dimitri's JWT Design - Critical for Security)
    -- =====================================================================
    SessionToken NVARCHAR(255) NULL,
    -- ^ Current session token for "logout all devices" feature
    -- Generated on signup, regenerated on password reset
    -- JWT contains session_token claim - validated on each request
    -- If JWT session_token != User.SessionToken → Token invalid
    
    AccessTokenVersion INT NOT NULL DEFAULT 1,
    -- ^ Increment to invalidate all access tokens (security)
    -- Use case: Suspicious activity detected, force re-login all devices
    
    RefreshTokenVersion INT NOT NULL DEFAULT 1,
    -- ^ Increment to invalidate all refresh tokens
    -- Use case: Password reset, force re-login all devices
    
    -- =====================================================================
    -- Onboarding Progress
    -- =====================================================================
    OnboardingComplete BIT NOT NULL DEFAULT 0,
    OnboardingStep INT NOT NULL DEFAULT 1,       -- Track exact step (1, 2, 3, etc.)
    
    -- =====================================================================
    -- References
    -- =====================================================================
    CountryID BIGINT NULL,                       -- FK to ref.Country
    PreferredLanguageID BIGINT NULL,             -- FK to ref.Language
    
    -- System role (optional - NULL for regular users, NOT NULL for system admins)
    UserRoleID BIGINT NULL,                      -- FK to ref.UserRole (system-level role)
    
    -- =====================================================================
    -- Audit Trail
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT FK_User_Status FOREIGN KEY (StatusID) REFERENCES [ref].[UserStatus](UserStatusID),
    CONSTRAINT FK_User_Country FOREIGN KEY (CountryID) REFERENCES [ref].[Country](CountryID),
    CONSTRAINT FK_User_Language FOREIGN KEY (PreferredLanguageID) REFERENCES [ref].[Language](LanguageID),
    CONSTRAINT FK_User_UserRole FOREIGN KEY (UserRoleID) REFERENCES [ref].[UserRole](UserRoleID),
    CONSTRAINT FK_User_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_User_UpdatedBy FOREIGN KEY (UpdatedBy) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_User_DeletedBy FOREIGN KEY (DeletedBy) REFERENCES [dbo].[User](UserID),
    
    -- Email format validation
    CONSTRAINT CK_User_Email CHECK (Email LIKE '%@%.%'),
    
    -- Audit trail consistency
    CONSTRAINT CK_User_AuditDates CHECK (
        CreatedDate <= ISNULL(UpdatedDate, '9999-12-31') AND
        CreatedDate <= ISNULL(DeletedDate, '9999-12-31')
    )
);

-- Indexes
CREATE UNIQUE INDEX UX_User_Email ON [dbo].[User](Email) WHERE IsDeleted = 0;
CREATE INDEX IX_User_StatusID ON [dbo].[User](StatusID) WHERE IsDeleted = 0;
CREATE INDEX IX_User_Country ON [dbo].[User](CountryID) WHERE IsDeleted = 0;
CREATE INDEX IX_User_UserRoleID ON [dbo].[User](UserRoleID) WHERE UserRoleID IS NOT NULL;  -- System admins
CREATE INDEX IX_User_SessionToken ON [dbo].[User](SessionToken) WHERE SessionToken IS NOT NULL;  -- JWT validation
CREATE INDEX IX_User_Timezone ON [dbo].[User](TimezoneIdentifier) WHERE IsDeleted = 0;  -- Timezone queries
```

**Design Notes (Dimitri's Enhancements):**
- **Session Management**: SessionToken + AccessTokenVersion + RefreshTokenVersion enable "logout all devices" and security-critical JWT invalidation
- **Timezone Support**: TimezoneIdentifier (IANA format) for displaying times in user's local timezone
- **Profile Fields**: RoleTitle and ProfilePictureUrl for better UX (avatars, job titles)
- **Audit Enhancements**: EmailVerifiedAt and LastPasswordChange for compliance and security policies
- **Self-Referential FKs**: CreatedBy/UpdatedBy/DeletedBy with FK constraints for data integrity

---

### `dbo.Company` (Core Business)

```sql
CREATE TABLE [dbo].[Company] (
    CompanyID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Name Management (Dimitri's Design - Flexible Display Names)
    -- =====================================================================
    CompanyName NVARCHAR(200) NOT NULL,
    -- ^ Primary display name (user's choice - for UI, dashboards, search)
    -- Can be: Legal name, business name, or custom override
    -- Example: "ICC Sydney" (user-friendly)
    
    LegalEntityName NVARCHAR(200) NULL,
    -- ^ Legal entity name from ABR API (for contracts, invoices, compliance)
    -- Example: "INTERNATIONAL CONVENTION CENTRE SYDNEY PTY LTD"
    -- Source: ABR <mainName><organisationName>
    -- NULL for non-Australian companies or when ABN not yet verified
    
    BusinessNames NVARCHAR(MAX) NULL,
    -- ^ JSON array of current business names from ABR API
    -- Example: ["ICC SYDNEY", "SYDNEY CONVENTION CENTRE"]
    -- Source: ABR <businessName><organisationName> (current only)
    -- Used for: Dropdown selection, name validation, user choice
    -- NULL = No registered business names
    
    CustomDisplayName NVARCHAR(200) NULL,
    -- ^ User-defined display name (override for branding)
    -- Example: "ICC Sydney Events" (custom branding)
    -- NULL = Use CompanyName (default behavior)
    
    DisplayNameSource NVARCHAR(20) NOT NULL DEFAULT 'User',
    -- ^ Source of CompanyName: 'Legal', 'Business', 'Custom', 'User'
    -- 'Legal' = LegalEntityName (fallback)
    -- 'Business' = First business name from BusinessNames (preferred)
    -- 'Custom' = CustomDisplayName (user override)
    -- 'User' = User-selected from available options (default)
    
    -- =====================================================================
    -- Australian Business Details (ABR API Integration)
    -- =====================================================================
    ABN NVARCHAR(11) NULL,
    -- ^ Australian Business Number (11 digits, no spaces)
    -- Example: "53004085616"
    -- Validated via ABN Lookup API
    
    ACN NVARCHAR(9) NULL,
    -- ^ Australian Company Number (9 digits)
    -- Example: "004085616"
    
    ABNStatus NVARCHAR(20) NULL,
    -- ^ ABN status from ABR API: 'Active', 'Cancelled', 'Historical'
    -- NULL = Not yet verified or non-Australian company
    -- Updated from ABN Lookup API (cached 30 days)
    
    EntityType NVARCHAR(100) NULL,
    -- ^ Entity type from ABR: "Australian Private Company", "Sole Trader", "Partnership"
    -- Source: ABR API response
    -- Used for: Understanding business structure, compliance requirements
    
    GSTRegistered BIT NULL,
    -- ^ Is company registered for GST? (from ABR API)
    -- NULL = Unknown (not yet verified)
    -- 0 = Not registered
    -- 1 = Registered (affects invoicing in Epic 7)
    
    -- =====================================================================
    -- Contact Information
    -- =====================================================================
    Phone NVARCHAR(20) NULL,
    -- ^ Primary contact phone (international format: +61 2 9215 7100)
    
    Email NVARCHAR(255) NULL,
    -- ^ Primary contact email
    
    Website NVARCHAR(500) NULL,
    -- ^ Company website URL
    
    -- =====================================================================
    -- Location & Classification
    -- =====================================================================
    CountryID BIGINT NOT NULL,
    -- ^ Company's primary country (foreign key to ref.Country)
    
    IndustryID BIGINT NULL,
    -- ^ Industry classification (foreign key to ref.Industry)
    
    -- =====================================================================
    -- Hierarchical Relationships (Parent-Subsidiary Support)
    -- =====================================================================
    ParentCompanyID BIGINT NULL,
    -- ^ Foreign key to parent company (for subsidiaries)
    -- Example: "Acme Events" (child) → "Acme Holdings" (parent)
    -- NULL = Top-level company (no parent)
    -- Enables: "Show all subsidiaries of Acme Holdings"
    -- Billing use case: Subsidiary invoices go to parent company
    
    -- =====================================================================
    -- Status
    -- =====================================================================
    IsActive BIT NOT NULL DEFAULT 1,
    -- ^ Is company active? (0 = inactive, 1 = active)
    
    -- =====================================================================
    -- Audit Trail
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT FK_Company_Country FOREIGN KEY (CountryID) REFERENCES [ref].[Country](CountryID),
    CONSTRAINT FK_Company_Industry FOREIGN KEY (IndustryID) REFERENCES [ref].[Industry](IndustryID),
    CONSTRAINT FK_Company_Parent FOREIGN KEY (ParentCompanyID) REFERENCES [dbo].[Company](CompanyID),
    
    -- ABN/ACN format validation
    CONSTRAINT CK_Company_ABN CHECK (ABN IS NULL OR LEN(ABN) = 11),
    CONSTRAINT CK_Company_ACN CHECK (ACN IS NULL OR LEN(ACN) = 9),
    
    -- ABN status validation
    CONSTRAINT CK_Company_ABNStatus CHECK (ABNStatus IS NULL OR ABNStatus IN ('Active', 'Cancelled', 'Historical')),
    
    -- DisplayNameSource validation
    CONSTRAINT CK_Company_DisplayNameSource CHECK (DisplayNameSource IN ('Legal', 'Business', 'Custom', 'User')),
    
    -- Ensure CustomDisplayName is set when DisplayNameSource = 'Custom'
    CONSTRAINT CK_Company_CustomDisplayName CHECK (
        (DisplayNameSource != 'Custom') OR (CustomDisplayName IS NOT NULL)
    ),
    
    -- Prevent circular parent relationships (company cannot be its own parent)
    CONSTRAINT CK_Company_NoSelfParent CHECK (ParentCompanyID IS NULL OR ParentCompanyID != CompanyID)
);

-- Indexes
CREATE INDEX IX_Company_CompanyName ON [dbo].[Company](CompanyName) WHERE IsDeleted = 0;
CREATE INDEX IX_Company_ABN ON [dbo].[Company](ABN) WHERE IsDeleted = 0 AND ABN IS NOT NULL;
CREATE INDEX IX_Company_Country ON [dbo].[Company](CountryID) WHERE IsDeleted = 0;
CREATE INDEX IX_Company_Industry ON [dbo].[Company](IndustryID) WHERE IsDeleted = 0;
CREATE INDEX IX_Company_Parent ON [dbo].[Company](ParentCompanyID) WHERE IsDeleted = 0 AND ParentCompanyID IS NOT NULL;
```

**Design Notes:**
- **Name flexibility**: Dimitri's sophisticated system supports legal names, business names, and custom branding
- **ABR integration**: Full capture of ABN Lookup API response (status, entity type, GST registration)
- **Hierarchical support**: Parent-subsidiary relationships for enterprise customers
- **Epic 7 ready**: ABNStatus and GSTRegistered fields prepare for billing/invoicing

---

### `dbo.CompanyCustomerDetails` (Extension Table)

```sql
CREATE TABLE [dbo].[CompanyCustomerDetails] (
    CompanyCustomerDetailsID BIGINT IDENTITY(1,1) PRIMARY KEY,
    CompanyID BIGINT NOT NULL UNIQUE,            -- 1-to-1 with Company
    
    -- Customer-specific fields
    CustomerSince DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CustomerTierID BIGINT NOT NULL,              -- FK to ref.CustomerTier ('free', 'pro', 'enterprise')
    TotalEvents INT NOT NULL DEFAULT 0,
    TotalLeadsCaptured INT NOT NULL DEFAULT 0,
    
    -- Audit trail
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,
    
    CONSTRAINT FK_CompanyCustomerDetails_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID),
    CONSTRAINT FK_CompanyCustomerDetails_Tier FOREIGN KEY (CustomerTierID) REFERENCES [ref].[CustomerTier](CustomerTierID)
);

-- Indexes
CREATE INDEX IX_CompanyCustomerDetails_Tier ON [dbo].[CompanyCustomerDetails](CustomerTierID);
```

---

### `dbo.CompanyBillingDetails` (Extension Table)

```sql
CREATE TABLE [dbo].[CompanyBillingDetails] (
    CompanyBillingDetailsID BIGINT IDENTITY(1,1) PRIMARY KEY,
    CompanyID BIGINT NOT NULL UNIQUE,            -- 1-to-1 with Company
    
    -- Billing contact
    BillingContactName NVARCHAR(200) NULL,
    BillingEmail NVARCHAR(255) NULL,
    BillingPhone NVARCHAR(20) NULL,
    
    -- Billing address
    BillingAddressLine1 NVARCHAR(255) NULL,
    BillingAddressLine2 NVARCHAR(255) NULL,
    BillingCity NVARCHAR(100) NULL,
    BillingState NVARCHAR(100) NULL,
    BillingPostalCode NVARCHAR(20) NULL,
    BillingCountryID BIGINT NULL,
    
    -- Payment
    StripeCustomerID NVARCHAR(100) NULL,         -- Stripe customer ID
    
    -- Audit trail
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,
    
    CONSTRAINT FK_CompanyBillingDetails_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID),
    CONSTRAINT FK_CompanyBillingDetails_Country FOREIGN KEY (BillingCountryID) REFERENCES [ref].[Country](CountryID)
);
```

---

### `dbo.CompanyOrganizerDetails` (Extension Table)

```sql
CREATE TABLE [dbo].[CompanyOrganizerDetails] (
    CompanyOrganizerDetailsID BIGINT IDENTITY(1,1) PRIMARY KEY,
    CompanyID BIGINT NOT NULL UNIQUE,            -- 1-to-1 with Company
    
    -- Organizer-specific fields
    OrganizerLicenseNumber NVARCHAR(100) NULL,
    EventTypesOrganized NVARCHAR(MAX) NULL,      -- JSON array or comma-separated
    AverageEventsPerYear INT NULL,
    
    -- Audit trail
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,
    
    CONSTRAINT FK_CompanyOrganizerDetails_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID)
);
```

---

### `dbo.UserCompany` (Many-to-Many Junction - Dimitri's Enhanced Design)

```sql
CREATE TABLE [dbo].[UserCompany] (
    -- =====================================================================
    -- Primary Key (Surrogate Key per Anthony's requirement)
    -- =====================================================================
    UserCompanyID BIGINT IDENTITY(1,1) PRIMARY KEY,
    -- ^ Surrogate primary key (even though we have composite unique key)
    -- Benefits: Simpler FK references, easier ORM relationships
    
    -- =====================================================================
    -- User-Company Relationship
    -- =====================================================================
    UserID BIGINT NOT NULL,
    CompanyID BIGINT NOT NULL,
    
    -- =====================================================================
    -- Role Per Company (User can be Admin in one, User in another)
    -- =====================================================================
    UserCompanyRoleID BIGINT NOT NULL,               -- FK to ref.UserCompanyRole
    
    -- =====================================================================
    -- Relationship Status & Preferences (Dimitri's Design)
    -- =====================================================================
    StatusID BIGINT NOT NULL,                    -- FK to ref.UserCompanyStatus
    -- ^ Options: 'active', 'suspended', 'removed'
    -- Active = Normal access
    -- Suspended = Admin temporarily revoked access (not removed from team)
    -- Removed = User removed from company (soft delete, retain historical data)
    
    IsPrimaryCompany BIT NOT NULL DEFAULT 0,
    -- ^ Which company loads on login? (only one per user can be default)
    -- User can switch companies via dropdown in navbar
    
    -- =====================================================================
    -- Relationship History (How did user join this company?)
    -- =====================================================================
    JoinedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    -- ^ When user joined this company
    
    JoinedViaID BIGINT NOT NULL,                 -- FK to ref.JoinedVia
    -- ^ How user joined: 'signup' (created company), 'invitation', 'transfer' (admin action)
    
    InvitedBy BIGINT NULL,
    -- ^ If JoinedVia = 'invitation', who invited them?
    
    InvitedDate DATETIME2 NULL,
    -- ^ When invitation was sent
    
    RemovedDate DATETIME2 NULL,
    -- ^ When user was removed from company (Status = 'removed')
    
    RemovedBy BIGINT NULL,
    -- ^ Admin who removed user from company
    
    RemovalReason NVARCHAR(500) NULL,
    -- ^ Optional reason for removal (displayed to user)
    
    -- =====================================================================
    -- Audit Trail
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    -- ^ UserID who added user to this company
    -- Company founder: Set to UserID (self-added)
    -- Invitation: Set to InviterUserID (who invited)
    -- System Admin: Set to SystemAdminUserID (admin action)
    
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
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
    
    -- Unique constraint: User can only have ONE active relationship per company
    CONSTRAINT UQ_UserCompany_User_Company UNIQUE (UserID, CompanyID)  -- Business key
);

-- Indexes
CREATE INDEX IX_UserCompany_User_Status ON [dbo].[UserCompany](UserID, StatusID);
CREATE INDEX IX_UserCompany_Company_Status ON [dbo].[UserCompany](CompanyID, StatusID);
CREATE INDEX IX_UserCompany_Status ON [dbo].[UserCompany](StatusID);
CREATE INDEX IX_UserCompany_RoleID ON [dbo].[UserCompany](UserCompanyRoleID);
CREATE INDEX IX_UserCompany_JoinedVia ON [dbo].[UserCompany](JoinedViaID);
CREATE INDEX IX_UserCompany_PrimaryCompany ON [dbo].[UserCompany](UserID, IsPrimaryCompany) WHERE IsPrimaryCompany = 1;
```

**Design Notes (Dimitri's Enhancements):**
- **Status Field**: Enables suspending users from companies (temporary access revocation) without full removal
- **JoinedVia**: Tracks how user joined (signup, invitation, transfer) for audit trail
- **Removal Tracking**: RemovedDate, RemovedBy, RemovalReason for complete audit trail
- **Multi-Company Support**: IsPrimaryCompany enables company switcher dropdown in UI

---

### `dbo.UserInvitation` (Core Business - Dimitri's Enhanced Design)

```sql
CREATE TABLE [dbo].[UserInvitation] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    UserInvitationID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Company & Inviter
    -- =====================================================================
    CompanyID BIGINT NOT NULL,
    InvitedBy BIGINT NOT NULL,                       -- UserID who sent invitation
    
    -- =====================================================================
    -- Invitee Details (Pre-filled by Admin)
    -- =====================================================================
    Email NVARCHAR(255) NOT NULL,
    FirstName NVARCHAR(100) NOT NULL,                -- Required: Admin must provide name
    LastName NVARCHAR(100) NOT NULL,
    
    -- =====================================================================
    -- Role Assignment
    -- =====================================================================
    UserCompanyRoleID BIGINT NOT NULL,               -- FK to ref.UserCompanyRole (company-level role)
    -- ^ What role will invitee get when they accept? (company_admin, company_user, company_viewer)
    
    -- =====================================================================
    -- Invitation Token (Secure)
    -- =====================================================================
    InvitationToken NVARCHAR(500) NOT NULL UNIQUE,
    -- ^ Cryptographically secure token (UUID v4 or similar)
    -- Used in invitation link: /accept-invitation?token=xxx
    
    -- =====================================================================
    -- Invitation Lifecycle
    -- =====================================================================
    StatusID BIGINT NOT NULL,                        -- FK to ref.InvitationStatus
    -- ^ References: 'pending', 'accepted', 'expired', 'cancelled', 'declined'
    
    InvitedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    -- ^ When invitation was sent
    
    ExpiresAt DATETIME2 NOT NULL,
    -- ^ InvitedAt + 7 days (configurable in AppSettings)
    
    AcceptedAt DATETIME2 NULL,
    AcceptedBy BIGINT NULL,                          -- UserID who accepted (if accepted)
    
    -- =====================================================================
    -- Cancellation Audit (Dimitri's Design)
    -- =====================================================================
    CancelledAt DATETIME2 NULL,
    CancelledBy BIGINT NULL,                         -- Admin who cancelled
    CancellationReason NVARCHAR(500) NULL,           -- Why was it cancelled?
    -- ^ Example: "User no longer needed", "Sent to wrong email"
    
    -- =====================================================================
    -- Decline Audit (Phase 2 Feature - Dimitri's Design)
    -- =====================================================================
    DeclinedAt DATETIME2 NULL,
    DeclineReason NVARCHAR(500) NULL,
    -- ^ Optional reason from invitee
    -- Example: "Not interested", "Already have account", "Wrong company"
    
    -- =====================================================================
    -- Resend Tracking (Rate Limiting - Dimitri's Design)
    -- =====================================================================
    ResendCount INT NOT NULL DEFAULT 0,
    -- ^ How many times invitation has been resent
    -- Used for rate limiting (max 3 resends)
    
    LastResentAt DATETIME2 NULL,
    -- ^ When invitation was last resent
    -- Used for rate limiting (1 resend per hour)
    
    -- =====================================================================
    -- Audit Trail
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT FK_UserInvitation_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID),
    CONSTRAINT FK_UserInvitation_UserCompanyRole FOREIGN KEY (UserCompanyRoleID) REFERENCES [ref].[UserCompanyRole](UserCompanyRoleID),
    CONSTRAINT FK_UserInvitation_Status FOREIGN KEY (StatusID) REFERENCES [ref].[UserInvitationStatus](UserInvitationStatusID),
    CONSTRAINT FK_UserInvitation_InvitedBy FOREIGN KEY (InvitedBy) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_UserInvitation_AcceptedBy FOREIGN KEY (AcceptedBy) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_UserInvitation_CancelledBy FOREIGN KEY (CancelledBy) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_UserInvitation_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_UserInvitation_UpdatedBy FOREIGN KEY (UpdatedBy) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_UserInvitation_DeletedBy FOREIGN KEY (DeletedBy) REFERENCES [dbo].[User](UserID),
    
    -- Email format validation
    CONSTRAINT CK_UserInvitation_Email CHECK (Email LIKE '%@%.%'),
    
    -- Expiry must be after InvitedAt
    CONSTRAINT CK_UserInvitation_ExpiryDate CHECK (ExpiresAt > InvitedAt)
);

-- Indexes
CREATE UNIQUE INDEX UX_UserInvitation_Token ON [dbo].[UserInvitation](InvitationToken);
CREATE INDEX IX_UserInvitation_Email_Status ON [dbo].[UserInvitation](Email, StatusID);
CREATE INDEX IX_UserInvitation_Company_Status ON [dbo].[UserInvitation](CompanyID, StatusID);
CREATE INDEX IX_UserInvitation_Expiry ON [dbo].[UserInvitation](ExpiresAt, StatusID) WHERE StatusID = (SELECT InvitationStatusID FROM [ref].[InvitationStatus] WHERE StatusCode = 'pending');
```

**Design Notes (Dimitri's Enhancements):**
- **Cancellation Tracking**: CancelledAt, CancelledBy, CancellationReason for complete audit trail
- **Decline Support**: DeclinedAt, DeclineReason (Phase 2 feature - allows invitees to decline gracefully)
- **Rate Limiting**: ResendCount + LastResentAt prevent invitation spam (max 3 resends, 1 per hour)
- **Required Names**: FirstName and LastName are NOT NULL (admin must provide names, not just email)
- **Expiry Validation**: CHECK constraint ensures ExpiresAt is always after InvitedAt

---

### `dbo.UserEmailVerificationToken` (Core Business - Hierarchical Naming)

```sql
CREATE TABLE [dbo].[UserEmailVerificationToken] (
    UserEmailVerificationTokenID BIGINT IDENTITY(1,1) PRIMARY KEY,
    UserID BIGINT NOT NULL,
    Token NVARCHAR(500) NOT NULL UNIQUE,
    ExpiresAt DATETIME2 NOT NULL,
    IsUsed BIT NOT NULL DEFAULT 0,
    UsedAt DATETIME2 NULL,
    
    -- Audit trail (minimal - tokens are short-lived)
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    
    CONSTRAINT FK_UserEmailVerificationToken_User FOREIGN KEY (UserID) REFERENCES [dbo].[User](UserID)
);

-- Indexes
CREATE INDEX IX_UserEmailVerificationToken_User ON [dbo].[UserEmailVerificationToken](UserID);
CREATE INDEX IX_UserEmailVerificationToken_ExpiresAt ON [dbo].[UserEmailVerificationToken](ExpiresAt) WHERE IsUsed = 0;
CREATE INDEX IX_UserEmailVerificationToken_Token ON [dbo].[UserEmailVerificationToken](Token) WHERE IsUsed = 0;
```

---

### `dbo.UserPasswordResetToken` (Core Business - Hierarchical Naming)

```sql
CREATE TABLE [dbo].[UserPasswordResetToken] (
    UserPasswordResetTokenID BIGINT IDENTITY(1,1) PRIMARY KEY,
    UserID BIGINT NOT NULL,
    Token NVARCHAR(500) NOT NULL UNIQUE,
    ExpiresAt DATETIME2 NOT NULL,
    IsUsed BIT NOT NULL DEFAULT 0,
    UsedAt DATETIME2 NULL,
    
    -- Security
    IPAddress NVARCHAR(50) NULL,                     -- IP that requested reset
    UserAgent NVARCHAR(500) NULL,                    -- Browser info
    
    -- Audit trail (minimal - tokens are short-lived)
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    
    CONSTRAINT FK_UserPasswordResetToken_User FOREIGN KEY (UserID) REFERENCES [dbo].[User](UserID)
);

-- Indexes
CREATE INDEX IX_UserPasswordResetToken_User ON [dbo].[UserPasswordResetToken](UserID);
CREATE INDEX IX_UserPasswordResetToken_ExpiresAt ON [dbo].[UserPasswordResetToken](ExpiresAt) WHERE IsUsed = 0;
CREATE INDEX IX_UserPasswordResetToken_Token ON [dbo].[UserPasswordResetToken](Token) WHERE IsUsed = 0;
```

---

### `log.ApiRequest` (Logging)

```sql
CREATE TABLE [log].[ApiRequest] (
    ApiRequestID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- Request details
    RequestMethod NVARCHAR(10) NOT NULL,             -- 'GET', 'POST', 'PUT', 'DELETE'
    RequestPath NVARCHAR(500) NOT NULL,              -- '/api/auth/login'
    RequestQuery NVARCHAR(MAX) NULL,                 -- Query string parameters
    RequestHeaders NVARCHAR(MAX) NULL,               -- JSON headers
    RequestBody NVARCHAR(MAX) NULL,                  -- Request body (sanitized)
    
    -- Response details
    ResponseStatus INT NOT NULL,                     -- 200, 400, 500, etc.
    ResponseBody NVARCHAR(MAX) NULL,                 -- Response body (sanitized)
    ResponseTime INT NOT NULL,                       -- Milliseconds
    
    -- Context
    UserID BIGINT NULL,                              -- Authenticated user (if any)
    CompanyID BIGINT NULL,                           -- Company context (if any)
    IPAddress NVARCHAR(50) NULL,
    UserAgent NVARCHAR(500) NULL,
    
    -- Audit trail (minimal - high volume table)
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    
    -- Constraints
    CONSTRAINT FK_ApiRequest_User FOREIGN KEY (UserID) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_ApiRequest_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID)
);

-- Indexes (optimized for queries, not writes)
CREATE INDEX IX_ApiRequest_User ON [log].[ApiRequest](UserID, CreatedDate);
CREATE INDEX IX_ApiRequest_Company ON [log].[ApiRequest](CompanyID, CreatedDate);
CREATE INDEX IX_ApiRequest_CreatedDate ON [log].[ApiRequest](CreatedDate);
CREATE INDEX IX_ApiRequest_Status ON [log].[ApiRequest](ResponseStatus, CreatedDate);
```

---

### `log.AuthEvent` (Logging)

```sql
CREATE TABLE [log].[AuthEvent] (
    AuthEventID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- Event details
    EventType NVARCHAR(50) NOT NULL,                 -- 'login', 'logout', 'token_refresh', 'login_failed'
    UserID BIGINT NULL,                              -- User involved (if known)
    Email NVARCHAR(255) NULL,                        -- Email attempted (even if user doesn't exist)
    
    -- Result
    IsSuccess BIT NOT NULL,
    FailureReason NVARCHAR(500) NULL,                -- 'invalid_password', 'account_locked', etc.
    
    -- Context
    IPAddress NVARCHAR(50) NULL,
    UserAgent NVARCHAR(500) NULL,
    
    -- Audit trail (minimal)
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    
    -- Constraints
    CONSTRAINT FK_AuthEvent_User FOREIGN KEY (UserID) REFERENCES [dbo].[User](UserID),
    CONSTRAINT CK_AuthEvent_EventType CHECK (EventType IN ('login', 'logout', 'token_refresh', 'login_failed', 'signup', 'email_verified', 'password_reset'))
);

-- Indexes
CREATE INDEX IX_AuthEvent_User ON [log].[AuthEvent](UserID, CreatedDate);
CREATE INDEX IX_AuthEvent_Email ON [log].[AuthEvent](Email, CreatedDate);
CREATE INDEX IX_AuthEvent_CreatedDate ON [log].[AuthEvent](CreatedDate);
CREATE INDEX IX_AuthEvent_EventType ON [log].[AuthEvent](EventType, CreatedDate);
```

---

### `log.ApplicationError` (Logging)

```sql
CREATE TABLE [log].[ApplicationError] (
    ApplicationErrorID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- Error details
    ErrorType NVARCHAR(100) NOT NULL,                -- 'ValueError', 'KeyError', 'DatabaseError'
    ErrorMessage NVARCHAR(MAX) NOT NULL,
    ErrorStackTrace NVARCHAR(MAX) NULL,
    
    -- Context
    UserID BIGINT NULL,
    CompanyID BIGINT NULL,
    RequestPath NVARCHAR(500) NULL,
    RequestMethod NVARCHAR(10) NULL,
    
    -- Audit trail (minimal)
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    
    -- Constraints
    CONSTRAINT FK_ApplicationError_User FOREIGN KEY (UserID) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_ApplicationError_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID)
);

-- Indexes
CREATE INDEX IX_ApplicationError_CreatedDate ON [log].[ApplicationError](CreatedDate);
CREATE INDEX IX_ApplicationError_ErrorType ON [log].[ApplicationError](ErrorType, CreatedDate);
```

---

### `log.EmailDelivery` (Logging)

```sql
CREATE TABLE [log].[EmailDelivery] (
    EmailDeliveryID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- Email details
    ToEmail NVARCHAR(255) NOT NULL,
    Subject NVARCHAR(500) NOT NULL,
    EmailType NVARCHAR(50) NOT NULL,                 -- 'verification', 'password_reset', 'invitation'
    
    -- Delivery status
    Status NVARCHAR(50) NOT NULL,                    -- 'sent', 'failed', 'bounced'
    FailureReason NVARCHAR(500) NULL,
    
    -- Context
    UserID BIGINT NULL,
    CompanyID BIGINT NULL,
    
    -- External tracking
    ExternalMessageID NVARCHAR(200) NULL,            -- SMTP/service message ID
    
    -- Audit trail (minimal)
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    SentDate DATETIME2 NULL,
    
    -- Constraints
    CONSTRAINT FK_EmailDelivery_User FOREIGN KEY (UserID) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_EmailDelivery_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID),
    CONSTRAINT CK_EmailDelivery_EmailType CHECK (EmailType IN ('verification', 'password_reset', 'invitation', 'welcome', 'notification')),
    CONSTRAINT CK_EmailDelivery_Status CHECK (Status IN ('sent', 'failed', 'bounced', 'delivered'))
);

-- Indexes
CREATE INDEX IX_EmailDelivery_ToEmail ON [log].[EmailDelivery](ToEmail, CreatedDate);
CREATE INDEX IX_EmailDelivery_CreatedDate ON [log].[EmailDelivery](CreatedDate);
CREATE INDEX IX_EmailDelivery_Status ON [log].[EmailDelivery](Status, CreatedDate);
```

---

### `audit.ActivityLog` (Compliance Audit Trail)

```sql
CREATE TABLE [audit].[ActivityLog] (
    ActivityLogID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- Actor (who did the action)
    UserID BIGINT NULL,
    UserEmail NVARCHAR(255) NULL,               -- Denormalized for audit integrity
    
    -- Action details
    ActionType NVARCHAR(50) NOT NULL,            -- 'create', 'update', 'delete', 'login', 'invite'
    EntityType NVARCHAR(100) NOT NULL,           -- 'User', 'Company', 'Form', 'Invitation'
    EntityID BIGINT NULL,                        -- ID of affected entity
    
    -- Context
    CompanyID BIGINT NULL,
    Description NVARCHAR(MAX) NOT NULL,          -- Human-readable description
    Changes NVARCHAR(MAX) NULL,                  -- JSON: before/after values
    
    -- Request context
    IPAddress NVARCHAR(50) NULL,
    UserAgent NVARCHAR(500) NULL,
    RequestPath NVARCHAR(500) NULL,
    
    -- Audit trail (append-only, NEVER update)
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    
    -- Constraints
    CONSTRAINT FK_ActivityLog_User FOREIGN KEY (UserID) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_ActivityLog_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID),
    CONSTRAINT CK_ActivityLog_ActionType CHECK (ActionType IN ('create', 'update', 'delete', 'login', 'logout', 'invite', 'accept_invite', 'verify_email', 'reset_password'))
);

-- Indexes for audit queries
CREATE INDEX IX_ActivityLog_User ON [audit].[ActivityLog](UserID, CreatedDate);
CREATE INDEX IX_ActivityLog_Company ON [audit].[ActivityLog](CompanyID, CreatedDate);
CREATE INDEX IX_ActivityLog_EntityType ON [audit].[ActivityLog](EntityType, EntityID, CreatedDate);
CREATE INDEX IX_ActivityLog_CreatedDate ON [audit].[ActivityLog](CreatedDate);
```

---

### `audit.User` (User Record Change History)

```sql
CREATE TABLE [audit].[User] (
    AuditUserID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- Audited entity
    UserID BIGINT NOT NULL,                      -- Original UserID
    
    -- Snapshot data (before change)
    Email NVARCHAR(255) NOT NULL,
    FirstName NVARCHAR(100) NOT NULL,
    LastName NVARCHAR(100) NOT NULL,
    Phone NVARCHAR(20) NULL,
    IsEmailVerified BIT NOT NULL,
    IsActive BIT NOT NULL,
    IsLocked BIT NOT NULL,
    StatusID BIGINT NULL,
    CountryID BIGINT NULL,
    
    -- Change metadata
    ChangeType NVARCHAR(20) NOT NULL,            -- 'insert', 'update', 'delete'
    ChangedBy BIGINT NULL,
    ChangedFields NVARCHAR(MAX) NULL,            -- JSON array of changed field names
    
    -- Audit trail (append-only)
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    
    -- Constraints
    CONSTRAINT FK_AuditUser_User FOREIGN KEY (UserID) REFERENCES [dbo].[User](UserID),
    CONSTRAINT CK_AuditUser_ChangeType CHECK (ChangeType IN ('insert', 'update', 'delete'))
);

-- Indexes
CREATE INDEX IX_AuditUser_User ON [audit].[User](UserID, CreatedDate);
CREATE INDEX IX_AuditUser_CreatedDate ON [audit].[User](CreatedDate);
```

---

### `audit.Company` (Company Record Change History)

```sql
CREATE TABLE [audit].[Company] (
    AuditCompanyID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- Audited entity
    CompanyID BIGINT NOT NULL,                   -- Original CompanyID
    
    -- Snapshot data (before change)
    CompanyName NVARCHAR(200) NOT NULL,
    ABN NVARCHAR(11) NULL,
    ACN NVARCHAR(9) NULL,
    Phone NVARCHAR(20) NULL,
    Email NVARCHAR(255) NULL,
    Website NVARCHAR(255) NULL,
    CountryID BIGINT NOT NULL,
    IndustryID BIGINT NULL,
    IsActive BIT NOT NULL,
    
    -- Change metadata
    ChangeType NVARCHAR(20) NOT NULL,            -- 'insert', 'update', 'delete'
    ChangedBy BIGINT NULL,
    ChangedFields NVARCHAR(MAX) NULL,            -- JSON array of changed field names
    
    -- Audit trail (append-only)
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    
    -- Constraints
    CONSTRAINT FK_AuditCompany_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID),
    CONSTRAINT CK_AuditCompany_ChangeType CHECK (ChangeType IN ('insert', 'update', 'delete'))
);

-- Indexes
CREATE INDEX IX_AuditCompany_Company ON [audit].[Company](CompanyID, CreatedDate);
CREATE INDEX IX_AuditCompany_CreatedDate ON [audit].[Company](CreatedDate);
```

---

### `audit.Role` (Role Assignment Change History)

```sql
CREATE TABLE [audit].[Role] (
    AuditRoleID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- Audited entity (NULL when auditing User table system roles)
    UserCompanyID BIGINT NULL,                   -- Original UserCompanyID (NULL for system role changes)
    UserID BIGINT NOT NULL,                      -- User whose role changed
    CompanyID BIGINT NULL,                       -- CompanyID (NULL for system role changes)
    
    -- Snapshot data (before change)
    OldRoleID BIGINT NULL,                       -- Previous role (system or company role)
    NewRoleID BIGINT NULL,                       -- New role (system or company role)
    OldRoleName NVARCHAR(50) NULL,               -- Denormalized for audit integrity
    NewRoleName NVARCHAR(50) NULL,               -- Denormalized for audit integrity
    RoleType NVARCHAR(20) NOT NULL,              -- 'system' or 'company' (to distinguish role type)
    
    -- Change metadata
    ChangeType NVARCHAR(20) NOT NULL,            -- 'role_assigned', 'role_changed', 'role_removed'
    ChangedBy BIGINT NULL,
    Reason NVARCHAR(500) NULL,                   -- Optional reason for change
    
    -- Audit trail (append-only)
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    
    -- Constraints
    CONSTRAINT FK_AuditRole_UserCompany FOREIGN KEY (UserCompanyID) REFERENCES [dbo].[UserCompany](UserCompanyID),
    CONSTRAINT FK_AuditRole_User FOREIGN KEY (UserID) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_AuditRole_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID),
    CONSTRAINT CK_AuditRole_ChangeType CHECK (ChangeType IN ('role_assigned', 'role_changed', 'role_removed')),
    CONSTRAINT CK_AuditRole_RoleType CHECK (RoleType IN ('system', 'company')),
    
    -- For system roles: UserCompanyID and CompanyID must be NULL
    -- For company roles: UserCompanyID and CompanyID must NOT be NULL
    CONSTRAINT CK_AuditRole_SystemRoleNulls CHECK (
        (RoleType = 'system' AND UserCompanyID IS NULL AND CompanyID IS NULL) OR
        (RoleType = 'company' AND UserCompanyID IS NOT NULL AND CompanyID IS NOT NULL)
    )
);

-- Indexes
CREATE INDEX IX_AuditRole_UserCompany ON [audit].[Role](UserCompanyID, CreatedDate) WHERE UserCompanyID IS NOT NULL;
CREATE INDEX IX_AuditRole_User ON [audit].[Role](UserID, CreatedDate);
CREATE INDEX IX_AuditRole_Company ON [audit].[Role](CompanyID, CreatedDate) WHERE CompanyID IS NOT NULL;
CREATE INDEX IX_AuditRole_RoleType ON [audit].[Role](RoleType, CreatedDate);
```

**Design Notes:**
- **RoleType**: Distinguishes between system-level roles (User.UserRoleID) and company-level roles (UserCompany.UserCompanyRoleID)
- **NULL Handling**: UserCompanyID and CompanyID are NULL when auditing system role changes on User table
- **CHECK Constraint**: Enforces proper NULL handling based on RoleType

---

### `cache.ABRSearch` (ABR API Cache - Enhanced Multi-Search)

```sql
CREATE TABLE [cache].[ABRSearch] (
    -- =====================================================================
    -- Composite Primary Key (Search Type + Key + Result Index)
    -- =====================================================================
    SearchType NVARCHAR(10) NOT NULL,
    -- ^ Search method: 'ABN', 'ACN', 'Name'
    -- Enables single table to handle all ABR search types efficiently
    
    SearchKey NVARCHAR(200) NOT NULL,
    -- ^ Search query: ABN (11 digits), ACN (9 digits), or Company Name
    -- NVARCHAR(200) handles long company names
    
    ResultIndex INT NOT NULL DEFAULT 0,
    -- ^ Result index for Name searches (0 = single result, 1+ = multiple results)
    -- ABN/ACN searches: Always 0 (single result)
    -- Name searches: 0, 1, 2, ... (multiple results from ABR API)
    
    -- =====================================================================
    -- Cached ABR API Response
    -- =====================================================================
    ResultJSON NVARCHAR(MAX) NOT NULL,
    -- ^ Full ABR API response as JSON
    -- Contains: ABN, ACN, entity_name, entity_type, business_names, 
    --           abn_status, gst_registered, state, postcode, etc.
    -- Flexible storage for varying ABR response structures
    
    SearchMetadata NVARCHAR(MAX) NULL,
    -- ^ Additional search metadata (JSON)
    -- Contains: search_timestamp, api_endpoint, response_time_ms, total_results
    -- Used for: Analytics, performance monitoring, debugging
    
    -- =====================================================================
    -- Extracted Key Fields (for fast querying without parsing JSON)
    -- =====================================================================
    ABN NVARCHAR(11) NULL,
    -- ^ Extracted ABN from result (for quick lookups)
    
    EntityName NVARCHAR(200) NULL,
    -- ^ Extracted entity name (for display in search results)
    
    EntityType NVARCHAR(100) NULL,
    -- ^ Extracted entity type: "Australian Private Company", "Sole Trader"
    
    ABNStatus NVARCHAR(20) NULL,
    -- ^ Extracted ABN status: 'Active', 'Cancelled', 'Historical'
    
    GSTRegistered BIT NULL,
    -- ^ Extracted GST registration status (affects invoicing)
    
    -- =====================================================================
    -- Cache Management
    -- =====================================================================
    CachedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    -- ^ When result was cached (UTC)
    -- Used for: TTL calculation, cache expiration
    
    ExpiresAt DATETIME2 NOT NULL,
    -- ^ Cache expiry timestamp (CachedDate + 30 days)
    -- ABR terms: 30-day cache allowed
    
    CacheVersion INT NOT NULL DEFAULT 1,
    -- ^ Cache version for invalidation/migration
    
    IsActive BIT NOT NULL DEFAULT 1,
    -- ^ Is cache entry active? (soft delete for cache management)
    
    -- =====================================================================
    -- Request Context (Optional - for analytics)
    -- =====================================================================
    CompanyID BIGINT NULL,
    -- ^ Company that made the request (if available)
    
    UserID BIGINT NULL,
    -- ^ User that made the request (if available)
    
    LastAccessedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    -- ^ Last time this cache entry was accessed
    
    AccessCount INT NOT NULL DEFAULT 1,
    -- ^ How many times this cache entry has been used (cache hit counter)
    
    -- =====================================================================
    -- Audit Trail (minimal - cache data)
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT PK_ABRSearch PRIMARY KEY (SearchType, SearchKey, ResultIndex),
    
    -- Search type validation
    CONSTRAINT CK_ABRSearch_SearchType CHECK (SearchType IN ('ABN', 'ACN', 'Name')),
    
    -- Result index validation (0+ for all search types)
    CONSTRAINT CK_ABRSearch_ResultIndex CHECK (ResultIndex >= 0),
    
    -- Cache version validation
    CONSTRAINT CK_ABRSearch_CacheVersion CHECK (CacheVersion >= 1),
    
    -- ABN format validation (if extracted)
    CONSTRAINT CK_ABRSearch_ABN_Format CHECK (ABN IS NULL OR LEN(ABN) = 11),
    
    -- ABN status validation (if extracted)
    CONSTRAINT CK_ABRSearch_ABNStatus CHECK (ABNStatus IS NULL OR ABNStatus IN ('Active', 'Cancelled', 'Historical')),
    
    -- Foreign key constraints (optional - for analytics)
    CONSTRAINT FK_ABRSearch_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID),
    CONSTRAINT FK_ABRSearch_User FOREIGN KEY (UserID) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_ABRSearch_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_ABRSearch_UpdatedBy FOREIGN KEY (UpdatedBy) REFERENCES [dbo].[User](UserID)
);

-- Indexes for cache lookups
CREATE INDEX IX_ABRSearch_Lookup ON [cache].[ABRSearch](SearchType, SearchKey, IsActive) WHERE IsActive = 1;
CREATE INDEX IX_ABRSearch_ABN ON [cache].[ABRSearch](ABN, ExpiresAt) WHERE ABN IS NOT NULL AND IsActive = 1;
CREATE INDEX IX_ABRSearch_Expiration ON [cache].[ABRSearch](ExpiresAt, IsActive) WHERE IsActive = 1;
CREATE INDEX IX_ABRSearch_Analytics ON [cache].[ABRSearch](SearchType, CachedDate, IsActive) WHERE IsActive = 1;
```

**Design Notes:**
- **Composite key**: Supports multiple search types (ABN, ACN, Name) in single table
- **Multiple results**: ResultIndex allows name searches to return multiple companies
- **Extracted fields**: Key ABR data extracted for fast querying without JSON parsing
- **30-day TTL**: Complies with ABR API terms (30-day cache allowed)
- **Soft delete**: IsActive flag for cache management without data loss
- **Analytics ready**: SearchMetadata and access tracking for performance monitoring

---

## ✅ VERIFICATION QUERIES

**Run after migration to verify:**

```sql
-- 1. Check all schemas created
SELECT name FROM sys.schemas 
WHERE name IN ('dbo', 'log', 'ref', 'config', 'audit', 'cache')
ORDER BY name;
-- Expected: 6 rows (audit, cache, config, dbo, log, ref)

-- 2. Check all tables created
SELECT 
    s.name AS SchemaName,
    t.name AS TableName,
    COUNT(c.column_id) AS ColumnCount
FROM sys.tables t
INNER JOIN sys.schemas s ON s.schema_id = t.schema_id
INNER JOIN sys.columns c ON c.object_id = t.object_id
WHERE s.name IN ('dbo', 'log', 'ref', 'config', 'audit', 'cache')
GROUP BY s.name, t.name
ORDER BY s.name, t.name;
-- Expected: 37 rows

-- 3. Check foreign keys
SELECT 
    s.name AS SchemaName,
    t.name AS TableName,
    fk.name AS ForeignKeyName,
    rs.name + '.' + rt.name AS ReferencedTable
FROM sys.foreign_keys fk
INNER JOIN sys.tables t ON t.object_id = fk.parent_object_id
INNER JOIN sys.schemas s ON s.schema_id = t.schema_id
INNER JOIN sys.tables rt ON rt.object_id = fk.referenced_object_id
INNER JOIN sys.schemas rs ON rs.schema_id = rt.schema_id
WHERE s.name IN ('dbo', 'log', 'ref', 'config')
ORDER BY s.name, t.name, fk.name;
-- Expected: 25+ foreign keys

-- 4. Check seed data
SELECT 'Country' AS TableName, COUNT(*) AS RowCount FROM [ref].[Country]
UNION ALL
SELECT 'Language', COUNT(*) FROM [ref].[Language]
UNION ALL
SELECT 'Industry', COUNT(*) FROM [ref].[Industry]
UNION ALL
SELECT 'UserRole', COUNT(*) FROM [ref].[UserRole]
UNION ALL
SELECT 'UserStatus', COUNT(*) FROM [ref].[UserStatus]
UNION ALL
SELECT 'InvitationStatus', COUNT(*) FROM [ref].[InvitationStatus]
UNION ALL
SELECT 'AppSetting', COUNT(*) FROM [config].[AppSetting]
UNION ALL
SELECT 'ValidationRule', COUNT(*) FROM [config].[ValidationRule];
-- Expected:
-- Country: 1
-- Language: 1
-- Industry: 10
-- UserRole: 3
-- UserStatus: 4
-- InvitationStatus: 4
-- AppSetting: 12
-- ValidationRule: 4

-- 5. Check indexes
SELECT 
    s.name AS SchemaName,
    t.name AS TableName,
    i.name AS IndexName,
    i.type_desc AS IndexType
FROM sys.indexes i
INNER JOIN sys.tables t ON t.object_id = i.object_id
INNER JOIN sys.schemas s ON s.schema_id = t.schema_id
WHERE s.name IN ('dbo', 'log', 'ref', 'config')
AND i.is_primary_key = 0  -- Exclude primary keys
AND i.name IS NOT NULL     -- Exclude heaps
ORDER BY s.name, t.name, i.name;
-- Expected: 20+ indexes

-- 6. View sample reference data
SELECT * FROM [ref].[Country];
SELECT * FROM [ref].[Language];
SELECT * FROM [ref].[Industry];
SELECT * FROM [config].[AppSetting] ORDER BY SortOrder;
SELECT * FROM [config].[ValidationRule] ORDER BY CountryID, SortOrder;
```

---

## 🎯 DELIVERABLES

**I will create:**
1. ✅ Complete Alembic migration file (`001_initial_epic1_schema.py`)
2. ✅ PowerShell execution script (`scripts/rebuild-database.ps1`)
3. ✅ SQL verification script (`database/scripts/verify-epic1-database.sql`)

**Files to be created:**
- `backend/migrations/versions/001_initial_epic1_schema.py` (migration)
- `scripts/rebuild-database.ps1` (automation)
- `database/scripts/verify-epic1-database.sql` (verification)

---

## ⏱️ ESTIMATED EXECUTION TIME

**Total: 5-10 minutes**
- Drop database: 30 seconds
- Create database: 10 seconds
- Delete old migrations: 10 seconds
- Run new migration: 2-3 minutes
- Verify database: 1 minute
- Review verification results: 1-2 minutes

---

## 🚨 ROLLBACK PLAN

**If something goes wrong:**

1. **Database still exists but migration failed:**
```powershell
# Rollback Alembic
alembic downgrade base

# Drop database and start over
USE master;
DROP DATABASE [EventLeadPlatform];
```

2. **Database dropped but can't recreate:**
```sql
-- Manually create database
CREATE DATABASE [EventLeadPlatform];
```

3. **Migration has errors:**
```powershell
# Delete migration file
Remove-Item backend\migrations\versions\001_initial_epic1_schema.py

# Restore from backup (if you backed up)
Copy-Item backend\migrations_backup\*.py backend\migrations\versions\
```

---

## ✅ APPROVAL CHECKLIST

**Before executing, confirm:**
- [ ] All backend services stopped
- [ ] Current work committed to git
- [ ] Database is development only (NO production data)
- [ ] Reviewed all 22 table definitions above
- [ ] Reviewed seed data (Country, Language, Industry, AppSettings, ValidationRules)
- [ ] Understand this is destructive (cannot undo)
- [ ] Ready to proceed with clean rebuild

---

## 🎉 POST-EXECUTION CHECKLIST

**After successful execution:**
- [ ] All verification queries pass
- [ ] 22 tables created across 4 schemas
- [ ] 4 seed data tables populated
- [ ] No errors in migration log
- [ ] SQLAlchemy models aligned with database
- [ ] Ready to start Epic 1 development

---

## 📞 NEXT STEPS AFTER APPROVAL

**Once you approve this plan:**
1. I'll create the complete Alembic migration file
2. I'll create the PowerShell automation script
3. I'll create the SQL verification script
4. You'll review the migration code
5. You'll execute the rebuild
6. We'll verify the database together

---

## ✅ ANTHONY'S DECISIONS

**All questions answered:**

1. **User Roles:** ✅ Option A - Create `ref.UserRole` table (flexible, database-driven)
2. **Status Tables:** ✅ Option A - Create `ref.InvitationStatus` and `ref.UserStatus` tables now
3. **Cache Schema:** ✅ Option A - Include `cache.ABRSearch` table now (for ABR integration)
4. **Test Data:** ✅ Option B - No test data (let onboarding flow create first user)
5. **Audit Tables:** ✅ Include audit schema tables (`audit.ActivityLog`, `audit.User`, `audit.Company`, `audit.Role`)

**Updated Scope:**
- **45 tables** across **6 schemas** (dbo, log, ref, config, audit, cache)
- **14 reference tables** for proper normalization (Anthony's preference):
  - Core references: Country, Language, Industry, UserStatus, UserInvitationStatus
  - Role hierarchy: UserRole, UserCompanyRole, UserCompanyStatus, AuditRole, JoinedVia
  - Configuration: SettingCategory, SettingType, RuleType, CustomerTier
- **Complete audit trail** for compliance (ActivityLog + audit snapshots + AuditRole with system/company role support)
- **Full ABR integration** (Dimitri's Company design preserved):
  - Company table: Name flexibility (Legal, Business, Custom display names)
  - Company table: Complete ABR fields (ABN, ACN, ABNStatus, EntityType, GSTRegistered)
  - Company table: BusinessNames JSON array from ABR API
  - Company table: Parent-subsidiary relationships for enterprise
  - ABRSearch cache: Enhanced multi-search (ABN, ACN, Name searches with composite key)
  - ABRSearch cache: 30-day TTL with extracted fields for fast queries
- **Full User domain** (Dimitri's comprehensive design integrated):
  - User table: 28 fields with session management (SessionToken, AccessTokenVersion, RefreshTokenVersion)
  - User table: Timezone support (TimezoneIdentifier) for correct date/time display
  - User table: Profile fields (RoleTitle, ProfilePictureUrl) for better UX
  - User table: Security enhancements (EmailVerifiedAt, LastPasswordChange)
  - UserCompany: Status tracking via FK to UserCompanyStatus (active, suspended, removed)
  - UserCompany: JoinedVia tracking via FK to JoinedVia (signup, invitation, transfer)
  - UserInvitation: Hierarchical naming (from Invitation → UserInvitation)
  - UserInvitation: Cancellation tracking, decline support, resend rate limiting
  - Token tables: Hierarchical naming (UserEmailVerificationToken, UserPasswordResetToken)
- **International readiness** in Country table:
  - Currency support (Code, Symbol, Name) for international payments
  - Tax configuration (Rate, Name, Inclusive flag, TaxNumberLabel) for billing compliance
  - Integration providers (CompanyValidationProvider, AddressValidationProvider) for country-specific APIs
  - JSON config for flexible provider settings (ABR, Geoscape for Australia)
- **Normalized configuration**:
  - AppSetting: FKs to SettingCategory and SettingType
  - ValidationRule: FK to RuleType
  - CompanyCustomerDetails: FK to CustomerTier

---

**STATUS:** 📋 READY FOR FINAL REVIEW

Once you confirm this updated plan, I'll create the migration files.


