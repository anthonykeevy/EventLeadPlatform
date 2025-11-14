# Database Naming Rules - EventLeadPlatform

**Purpose:** Quick reference guide for database naming conventions and standards  
**Target Audience:** Agents, Developers, Database Administrators  
**Related Document:** `docs/database-schema.md` - Complete schema reference with examples  
**Status:** MANDATORY - All database objects must follow these rules

---

## Overview

This document defines the **mandatory naming conventions** for all database objects in EventLeadPlatform. These rules ensure consistency, self-documentation, and maintainability across the entire database schema.

**Key Principle:** The database uses **PascalCase** for all tables and columns, following SQL Server best practices and enterprise standards.

---

## Core Rules Summary

| Object Type | Convention | Example | ❌ Never |
|------------|------------|---------|----------|
| **Tables** | PascalCase, singular noun | `User`, `Company`, `Event` | `users`, `user_table`, `USER` |
| **Columns** | PascalCase | `UserID`, `FirstName`, `Email` | `user_id`, `firstName`, `email` |
| **Primary Keys** | `[TableName]ID` | `UserID`, `CompanyID` | `id`, `ID`, `UserId`, `pk_user` |
| **Foreign Keys** | `[ReferencedTable]ID` | `CompanyID`, `UserRoleID` | `company_id`, `fk_company`, `companyRef` |
| **Booleans** | `Is` or `Has` prefix | `IsActive`, `IsDeleted`, `HasAccess` | `Active`, `Deleted`, `active` |
| **Dates** | Descriptive suffix | `CreatedDate`, `UpdatedDate`, `ExpiresAt` | `created`, `updated_at`, `expiry` |
| **Schemas** | lowercase, single word | `dbo`, `ref`, `log`, `audit` | `DBO`, `Ref`, `Logging` |
| **Constraints** | `[Type]_[Table]_[Column]` | `PK_User_UserID`, `FK_User_CountryID` | `pk_user`, `user_pk` |
| **Indexes** | `IX_[Table]_[Column]` | `IX_User_Email`, `IX_Form_CompanyID` | `idx_user_email`, `user_email_idx` |

---

## 1. Table Naming Rules

### Rule: PascalCase, Singular Noun

**✅ GOOD Examples:**
- `User` (not `Users`)
- `Company` (not `Companies`)
- `Event` (not `Events`)
- `Form` (not `Forms`)
- `UserCompany` (junction table)
- `CompanyBillingDetails` (extension table)

**❌ BAD Examples:**
- `users` (lowercase)
- `user_table` (snake_case with suffix)
- `USER` (uppercase)
- `Users` (plural)
- `tblUser` (prefix)

**Reference Examples from `database-schema.md`:**
- `dbo.User` - Core user table
- `dbo.Company` - Core company table
- `dbo.UserCompany` - Junction table for many-to-many relationship
- `ref.UserStatus` - Reference/lookup table

---

## 2. Column Naming Rules

### Rule: PascalCase for All Columns

**✅ GOOD Examples:**
- `UserID` (primary key)
- `FirstName` (not `first_name`)
- `LastName` (not `last_name`)
- `Email` (not `email_address`)
- `CompanyName` (not `company_name`)
- `CreatedDate` (not `created_date`)

**❌ BAD Examples:**
- `user_id` (snake_case)
- `firstName` (camelCase)
- `email_address` (snake_case with underscore)
- `created_date` (snake_case)

**Reference Examples from `database-schema.md`:**
- `dbo.User` table: `UserID`, `FirstName`, `LastName`, `Email`, `PasswordHash`
- `dbo.Company` table: `CompanyID`, `CompanyName`, `ABN`, `CountryID`

---

## 3. Primary Key Naming Rules

### Rule: MUST be `[TableName]ID`

**✅ GOOD Examples:**
- `UserID` (for `User` table)
- `CompanyID` (for `Company` table)
- `EventID` (for `Event` table)
- `FormID` (for `Form` table)
- `UserCompanyID` (for `UserCompany` junction table)

**❌ BAD Examples:**
- `id` (generic)
- `ID` (generic)
- `UserId` (inconsistent casing)
- `user_id` (snake_case)
- `pk_user` (prefix)

**Type:** `BIGINT IDENTITY(1,1)` (preferred) or `INT IDENTITY(1,1)`

**Reference Examples from `database-schema.md`:**
- `dbo.User.UserID` - Primary key
- `dbo.Company.CompanyID` - Primary key
- `dbo.UserCompany.UserCompanyID` - Primary key for junction table

---

## 4. Foreign Key Naming Rules

### Rule: MUST be `[ReferencedTableName]ID`

**Key Principle:** Foreign key column name must match the primary key column name of the referenced table exactly.

**✅ GOOD Examples:**
- `CompanyID` → references `dbo.Company.CompanyID`
- `UserID` → references `dbo.User.UserID`
- `UserRoleID` → references `ref.UserRole.UserRoleID`
- `CountryID` → references `ref.Country.CountryID`
- `EventID` → references `dbo.Event.EventID`

**❌ BAD Examples:**
- `company_id` (snake_case)
- `fk_company` (prefix)
- `companyRef` (camelCase)
- `CompanyRefID` (non-standard suffix)

**Self-Documenting:** The column name reveals the relationship:
- `UserRoleID` tells you `UserRole` table exists
- `CountryID` tells you `Country` table exists
- `CreatedBy` tells you it references `User.UserID`

**Reference Examples from `database-schema.md`:**
- `dbo.User.StatusID` → `FK→ref.UserStatus` (different schema)
- `dbo.User.CompanyID` → `FK→User` (same schema, simplified)
- `dbo.UserCompany.UserID` → `FK→User` (references `dbo.User.UserID`)
- `dbo.UserCompany.CompanyID` → `FK→Company` (references `dbo.Company.CompanyID`)

---

## 5. Boolean Field Naming Rules

### Rule: MUST use `Is` or `Has` prefix

**✅ GOOD Examples:**
- `IsActive` (not `Active`)
- `IsDeleted` (not `Deleted`)
- `IsEmailVerified` (not `EmailVerified`)
- `IsLocked` (not `Locked`)
- `HasAccess` (not `Access`)
- `IsPublic` (not `Public`)

**❌ BAD Examples:**
- `Active` (missing prefix)
- `EmailVerified` (missing prefix)
- `active` (lowercase, missing prefix)
- `is_active` (snake_case)

**Type:** `BIT NOT NULL DEFAULT 0` in SQL Server, `Boolean` in SQLAlchemy

**Reference Examples from `database-schema.md`:**
- `dbo.User.IsEmailVerified` - Boolean field
- `dbo.User.IsLocked` - Boolean field
- `dbo.User.IsDeleted` - Soft delete flag
- `dbo.Company.IsActive` - Boolean field

---

## 6. Date/Time Field Naming Rules

### Rule: Descriptive suffix with `Date` or `At`

**✅ GOOD Examples:**
- `CreatedDate` (not `created`)
- `UpdatedDate` (not `updated`)
- `DeletedDate` (not `deleted_at`)
- `ExpiresAt` (not `expires`)
- `EmailVerifiedAt` (not `email_verified_at`)
- `LastLoginDate` (not `last_login`)

**❌ BAD Examples:**
- `created` (no suffix)
- `created_at` (snake_case)
- `CreatedAt` (inconsistent with `CreatedDate`)
- `updated` (no suffix)

**Type:** `DATETIME2 NOT NULL DEFAULT GETUTCDATE()` for creation dates  
**Type:** `DATETIME2 NULL` for nullable dates (updated, deleted, etc.)

**All timestamps stored in UTC** - conversion happens at application layer.

**Reference Examples from `database-schema.md`:**
- `dbo.User.CreatedDate` - Creation timestamp (UTC)
- `dbo.User.UpdatedDate` - Last update timestamp (UTC)
- `dbo.User.EmailVerifiedAt` - Email verification timestamp
- `dbo.User.LastLoginDate` - Last login timestamp

---

## 7. Audit Column Naming Rules

### Standard Audit Columns (ALL tables MUST have):

**Mandatory Columns:**
```sql
CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE()
CreatedBy BIGINT NULL  -- FK to User.UserID (can be NULL for system actions)
```

**For Mutable Tables (tables that can be updated):**
```sql
UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE()
UpdatedBy BIGINT NULL  -- FK to User.UserID
```

**For Soft Delete (most tables):**
```sql
IsDeleted BIT NOT NULL DEFAULT 0
DeletedDate DATETIME2 NULL
DeletedBy BIGINT NULL  -- FK to User.UserID
```

**✅ GOOD Examples:**
- `CreatedDate`, `CreatedBy`, `UpdatedDate`, `UpdatedBy`
- `IsDeleted`, `DeletedDate`, `DeletedBy`

**❌ BAD Examples:**
- `created_date`, `created_by` (snake_case)
- `CreatedAt`, `UpdatedAt` (inconsistent with `Date` suffix)
- `Deleted` (boolean without `Is` prefix)

**Reference Examples from `database-schema.md`:**
- All tables include `CreatedDate`, `CreatedBy`, `UpdatedDate`, `UpdatedBy`, `IsDeleted`, `DeletedDate`, `DeletedBy`

---

## 8. Schema Naming Rules

### Rule: Lowercase, Single Word

**✅ GOOD Examples:**
- `dbo` (default schema)
- `ref` (reference/lookup tables)
- `log` (technical logging)
- `audit` (audit trail)
- `config` (configuration)
- `cache` (cache tables)

**❌ BAD Examples:**
- `DBO` (uppercase)
- `Ref` (PascalCase)
- `Logging` (multiple words)
- `audit_trail` (snake_case)

**Table Reference Format:** `[SchemaName].[TableName]`
- `dbo.User` - Core business entity
- `ref.Country` - Reference table
- `log.ApiRequest` - Logging table
- `audit.ActivityLog` - Audit table

**Reference Examples from `database-schema.md`:**
- Schema prefixes shown in all table names: `dbo.User`, `ref.Country`, `log.ApiRequest`

---

## 9. Constraint Naming Rules

### Rule: `[Type]_[TableName]_[ColumnNames]`

**Constraint Types:**
- `PK_` = Primary Key
- `FK_` = Foreign Key
- `UQ_` = Unique Constraint
- `CK_` = Check Constraint
- `DF_` = Default Constraint

**✅ GOOD Examples:**
```sql
CONSTRAINT PK_User_UserID PRIMARY KEY (UserID)
CONSTRAINT FK_User_Country_CountryID FOREIGN KEY (CountryID) REFERENCES [ref].[Country](CountryID)
CONSTRAINT UQ_User_Email UNIQUE (Email)
CONSTRAINT CK_User_Status CHECK (StatusID IN (1, 2, 3))
CONSTRAINT DF_User_IsActive DEFAULT 1
```

**❌ BAD Examples:**
```sql
CONSTRAINT pk_user PRIMARY KEY (UserID)  -- Missing table/column
CONSTRAINT user_pk PRIMARY KEY (UserID)  -- Wrong order
CONSTRAINT FK_User_Country FOREIGN KEY (CountryID) ...  -- Missing column
```

---

## 10. Index Naming Rules

### Rule: `IX_[TableName]_[ColumnNames]`

**✅ GOOD Examples:**
```sql
CREATE INDEX IX_User_Email ON [dbo].[User](Email)
CREATE INDEX IX_Form_CompanyID ON [dbo].[Form](CompanyID)
CREATE INDEX IX_UserCompany_UserID_CompanyID ON [dbo].[UserCompany](UserID, CompanyID)
```

**❌ BAD Examples:**
```sql
CREATE INDEX idx_user_email ON [dbo].[User](Email)  -- Wrong prefix
CREATE INDEX user_email_idx ON [dbo].[User](Email)  -- Wrong order
CREATE INDEX IX_User_Email_Idx ON [dbo].[User](Email)  -- Redundant suffix
```

---

## 11. Data Type Rules

### Unicode Support (CRITICAL)

**Rule:** ALL text fields MUST be `NVARCHAR` (never `VARCHAR`)

**Why:** International platform requires Unicode support (Chinese, Arabic, emoji, special characters)

**✅ GOOD Examples:**
```sql
FirstName NVARCHAR(100) NOT NULL
Email NVARCHAR(255) NOT NULL
Description NVARCHAR(500) NULL
```

**❌ BAD Examples:**
```sql
FirstName VARCHAR(100) NOT NULL  -- No Unicode support
Email VARCHAR(255) NOT NULL  -- No Unicode support
```

**Exception:** Very specific cases where VARCHAR is acceptable (e.g., internal codes, ASCII-only identifiers)

---

## 12. Common Patterns

### Junction Tables (Many-to-Many)

**Naming:** `[Table1][Table2]` (both table names, no separator)

**✅ GOOD Examples:**
- `UserCompany` (junction between `User` and `Company`)
- `UserIndustry` (junction between `User` and `Industry`)

**Primary Key:** `[Table1][Table2]ID`
- `UserCompanyID` (for `UserCompany` table)
- `UserIndustryID` (for `UserIndustry` table)

**Reference Examples from `database-schema.md`:**
- `dbo.UserCompany` - Junction table with `UserCompanyID` as PK
- `dbo.UserIndustry` - Junction table with `UserIndustryID` as PK

---

### Extension Tables (Additional Details)

**Naming:** `[BaseTable][Purpose]Details`

**✅ GOOD Examples:**
- `CompanyBillingDetails` (billing info for Company)
- `CompanyCustomerDetails` (customer-specific data for Company)
- `CompanyOrganizerDetails` (organizer-specific data for Company)

**Foreign Key:** `CompanyID` (references `dbo.Company.CompanyID`)

**Reference Examples from `database-schema.md`:**
- `dbo.CompanyBillingDetails` - Extension table for `dbo.Company`
- `dbo.CompanyCustomerDetails` - Extension table for `dbo.Company`
- `dbo.CompanyOrganizerDetails` - Extension table for `dbo.Company`

---

### Reference/Lookup Tables

**Naming:** Same as the entity name (singular PascalCase)

**Schema:** `ref` (reference schema)

**✅ GOOD Examples:**
- `ref.Country` (not `ref.Countries`)
- `ref.UserStatus` (not `ref.UserStatuses`)
- `ref.EventType` (not `ref.EventTypes`)
- `ref.UserRole` (not `ref.UserRoles`)

**Primary Key Pattern:** `[TableName]ID`
- `ref.Country.CountryID`
- `ref.UserStatus.UserStatusID`
- `ref.EventType.EventTypeID`

**Reference Examples from `database-schema.md`:**
- All `ref.*` schema tables follow this pattern

---

## 13. ENUM Fields - Use Reference Tables Instead

### Rule: NEVER use ENUM types - Always create reference tables

**CRITICAL:** EventLeadPlatform does **NOT** use SQL Server ENUM types or CHECK constraints with hardcoded values. Instead, we create reference tables in the `ref` schema.

**Why Reference Tables?**
- ✅ **Referential integrity** - Database enforces valid values automatically
- ✅ **Extensibility** - Add new values without code changes or deployments
- ✅ **Rich metadata** - Store descriptions, sort orders, colors, icons for UI
- ✅ **Centralized definition** - Single source of truth for all valid values
- ✅ **Audit trail** - Track changes to reference data over time
- ✅ **UI dropdowns** - Query reference tables directly for SELECT options
- ✅ **Self-documenting** - JOIN reveals human-readable names in queries

**❌ NEVER Do This:**
```sql
-- ❌ BAD: Using ENUM type
Status ENUM('pending', 'active', 'suspended', 'locked')

-- ❌ BAD: Using CHECK constraint with hardcoded values
Status NVARCHAR(20) CHECK (Status IN ('pending', 'active', 'suspended', 'locked'))

-- ❌ BAD: Using integer with magic numbers
StatusID INT CHECK (StatusID IN (1, 2, 3, 4))
```

**✅ ALWAYS Do This:**
```sql
-- 1. Create reference table in ref schema
CREATE TABLE [ref].[UserStatus] (
    UserStatusID BIGINT IDENTITY(1,1) PRIMARY KEY,
    StatusCode NVARCHAR(50) NOT NULL UNIQUE,  -- 'pending', 'active', etc.
    StatusName NVARCHAR(100) NOT NULL,        -- 'Active', 'Pending Verification'
    Description NVARCHAR(500) NOT NULL,       -- Human-readable explanation
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 0,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedDate DATETIME2 NULL,
    CONSTRAINT UQ_UserStatus_StatusCode UNIQUE (StatusCode)
);

-- 2. Use foreign key in business table
CREATE TABLE [dbo].[User] (
    UserID BIGINT IDENTITY(1,1) PRIMARY KEY,
    StatusID BIGINT NOT NULL,
    CONSTRAINT FK_User_UserStatus FOREIGN KEY (StatusID) 
        REFERENCES [ref].[UserStatus](UserStatusID)
);
```

**Standard Reference Table Pattern:**
```sql
CREATE TABLE [ref].[{EntityName}] (
    {EntityName}ID BIGINT IDENTITY(1,1) PRIMARY KEY,
    {Code}Code NVARCHAR(50) NOT NULL UNIQUE,      -- Machine-readable code
    {Code}Name NVARCHAR(100) NOT NULL,            -- Human-readable name
    Description NVARCHAR(500) NOT NULL,           -- Full explanation (for UI tooltips)
    IsActive BIT NOT NULL DEFAULT 1,              -- Can be disabled without deletion
    SortOrder INT NOT NULL DEFAULT 0,             -- For UI dropdowns (ORDER BY SortOrder)
    
    -- Audit trail
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    
    CONSTRAINT UQ_{EntityName}_{Code}Code UNIQUE ({Code}Code)
);
```

**When to Create Reference Table:**
- ✅ Fixed set of values (3-20 typical options)
- ✅ Values need human-readable descriptions
- ✅ Values may change over time (add/remove/rename)
- ✅ Values need metadata (sort order, color, icon, IsActive flag)
- ✅ Values used in multiple tables
- ✅ UI needs dropdown/select options

**Examples from Actual Schema:**
- `ref.UserStatus` - User account statuses (pending, active, suspended, locked)
- `ref.UserRole` - System-level roles (system_admin, company_user)
- `ref.UserCompanyRole` - Company-level roles (company_admin, company_user, company_viewer)
- `ref.EventType` - Event types (conference, workshop, meetup, etc.)
- `ref.EventStatus` - Event statuses (draft, published, cancelled, etc.)
- `ref.Country` - Country lookup with currency/tax/integration metadata
- `ref.Language` - Language lookup

**Reference Examples from `database-schema.md`:**
- All enum-like fields use reference tables (no ENUM types or CHECK constraints with hardcoded values)
- See `ref.*` schema tables for examples of reference table pattern

**Related Document:** `docs/architecture/decisions/ADR-004-database-normalization-for-enum-like-fields.md` - Full architectural decision on this pattern

---

## Validation Checklist

When creating or modifying database objects, verify:

- [ ] Table names use PascalCase, singular noun
- [ ] Column names use PascalCase
- [ ] Primary keys follow `[TableName]ID` pattern. Double check that [TableName] is the entire table name.
- [ ] Foreign keys follow `[ReferencedTable]ID` pattern
- [ ] Boolean fields use `Is` or `Has` prefix
- [ ] Date fields use `Date` or `At` suffix
- [ ] All text fields use `NVARCHAR` (not `VARCHAR`)
- [ ] Schema names use lowercase, single word
- [ ] Constraints follow `[Type]_[Table]_[Column]` pattern
- [ ] Indexes follow `IX_[Table]_[Column]` pattern
- [ ] Standard audit columns included (CreatedDate, CreatedBy, etc.)
- [ ] **NO ENUM types** - Use reference tables in `ref` schema instead
- [ ] **NO CHECK constraints with hardcoded values** - Use foreign keys to reference tables

---

## Related Documents

- **`docs/database-schema.md`** - Complete schema reference with all tables and columns (real examples)
- **`docs/architecture/decisions/ADR-003-naming-convention-strategy.md`** - Full architectural decision on naming conventions
- **`docs/solution-architecture.md`** - Database standards section (authoritative source)

---

## Quick Reference

**For Agents:** When reviewing or creating database objects, refer to `docs/database-schema.md` for real examples of these naming rules in practice.

**Key Takeaways:**
1. **PascalCase** for all tables and columns
2. **`[TableName]ID`** for primary keys
3. **`[ReferencedTable]ID`** for foreign keys
4. **`Is`/`Has`** prefix for booleans
5. **`NVARCHAR`** for all text fields
6. **Lowercase** schema names
7. **Standard audit columns** on all tables
8. **NO ENUMs** - Use reference tables in `ref` schema instead

---

**Last Updated:** 2025-11-04  
**Maintained By:** Database Standards (Solomon 📜)

