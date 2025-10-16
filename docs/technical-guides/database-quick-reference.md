# Database Quick Reference - Epic 1

**Purpose:** At-a-glance view of all database tables  
**Tables:** 45 across 6 schemas  
**Last Updated:** 2025-10-16

---

## 📊 Table Count by Schema

| Schema | Tables | Purpose | Retention |
|--------|--------|---------|-----------|
| **dbo** | 13 | Core business entities | Permanent |
| **ref** | 14 | Reference/lookup data | Permanent |
| **config** | 2 | Runtime configuration | Permanent |
| **log** | 4 | Technical logging | 90 days |
| **audit** | 4 | Compliance audit trail | 7 years |
| **cache** | 1 | External API cache | 90 days |
| **TOTAL** | **45** | | |

---

## 🗂️ dbo Schema (Core Business - 13 tables)

| # | Table | Primary Key | Key Foreign Keys | Purpose |
|---|-------|-------------|------------------|---------|
| 1 | `User` | `UserID` | StatusID, UserRoleID, CountryID | User accounts |
| 2 | `UserCompany` | `UserCompanyID` | UserID, CompanyID, UserCompanyRoleID | User-company relationships |
| 3 | `Company` | `CompanyID` | CountryID, IndustryID, ParentCompanyID | Company profiles |
| 4 | `CompanyCustomerDetails` | `CompanyCustomerDetailsID` | CompanyID, CustomerTierID | Subscription data (1-to-1) |
| 5 | `CompanyBillingDetails` | `CompanyBillingDetailsID` | CompanyID, BillingCountryID | Billing info (1-to-1) |
| 6 | `CompanyOrganizerDetails` | `CompanyOrganizerDetailsID` | CompanyID | Organizer data (1-to-1) |
| 7 | `UserInvitation` | `UserInvitationID` | CompanyID, UserCompanyRoleID, UserInvitationStatusID | Team invitations |
| 8 | `UserEmailVerificationToken` | `UserEmailVerificationTokenID` | UserID | Email verification tokens |
| 9 | `UserPasswordResetToken` | `UserPasswordResetTokenID` | UserID | Password reset tokens |

**Detailed docs:** `docs/database/schema-reference/dbo-schema.md`

---

## 🔍 ref Schema (Reference Data - 14 tables)

| # | Table | Records | Purpose |
|---|-------|---------|---------|
| 1 | `Country` | 1 (AU) | Country master data (currency, tax, integrations) |
| 2 | `Language` | 1 (EN) | Language/locale master data |
| 3 | `Industry` | TBD | Industry categorization |
| 4 | `UserStatus` | 4 | User account status (pending, active, suspended, locked) |
| 5 | `UserInvitationStatus` | 5 | Invitation status (pending, accepted, declined, expired, cancelled) |
| 6 | `UserRole` | 2 | System-level roles (system_admin, company_user) |
| 7 | `UserCompanyRole` | 3 | Company-level roles (admin, user, viewer) |
| 8 | `UserCompanyStatus` | 3 | User-company status (active, suspended, removed) |
| 9 | `SettingCategory` | 4 | AppSetting categories (authentication, validation, email, security) |
| 10 | `SettingType` | 5 | AppSetting data types (integer, boolean, string, json, decimal) |
| 11 | `RuleType` | 5 | ValidationRule types (phone, postal_code, tax_id, email, address) |
| 12 | `CustomerTier` | 4 | Subscription tiers (free, starter, professional, enterprise) |
| 13 | `JoinedVia` | 3 | How user joined (signup, invitation, transfer) |

**Detailed docs:** `docs/database/schema-reference/ref-schema.md`

---

## ⚙️ config Schema (Configuration - 2 tables)

| # | Table | Records | Purpose |
|---|-------|---------|---------|
| 1 | `AppSetting` | ~15 | Runtime business rules (password policy, token expiry) |
| 2 | `ValidationRule` | ~20 | Country-specific validation patterns |

**Detailed docs:** `docs/database/schema-reference/config-schema.md`

---

## 📋 log Schema (Technical Logging - 4 tables)

| # | Table | Write Volume | Purpose |
|---|-------|--------------|---------|
| 1 | `ApiRequest` | VERY HIGH | HTTP request/response logging |
| 2 | `AuthEvent` | MEDIUM | Authentication events (login, logout) |
| 3 | `ApplicationError` | LOW | Application errors (exceptions, 500s) |
| 4 | `EmailDelivery` | MEDIUM | Email delivery tracking |

**Detailed docs:** `docs/database/schema-reference/log-schema.md`

---

## 🔐 audit Schema (Compliance Audit - 4 tables)

| # | Table | Write Volume | Purpose |
|---|-------|--------------|---------|
| 1 | `ActivityLog` | MEDIUM | Business actions (login, create, update, delete) |
| 2 | `User` | LOW | User record snapshots (before/after) |
| 3 | `Company` | LOW | Company record snapshots |
| 4 | `Role` | LOW | Role assignment changes |

**Detailed docs:** `docs/database/schema-reference/audit-schema.md`

---

## 💾 cache Schema (External API Cache - 1 table)

| # | Table | Cache Duration | Purpose |
|---|-------|----------------|---------|
| 1 | `ABRSearch` | 90 days | ABR (Australian Business Register) API results |

**Detailed docs:** `docs/database/schema-reference/cache-schema.md`

---

## 🔗 Entity Relationship Diagram (Simplified)

```
┌─────────────────────────────────────────────────────────────┐
│                     CORE ENTITIES (dbo)                      │
└─────────────────────────────────────────────────────────────┘

   ┌──────────────┐         ┌──────────────┐
   │  ref.Country │◄────────│   Company    │
   └──────────────┘         └──────┬───────┘
                                   │
                                   │ FK: CompanyID
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         │                         │                         │
         │                         │                         │
   ┌─────▼──────┐          ┌──────▼─────────┐      ┌───────▼────────┐
   │ Customer   │          │    Billing     │      │   Organizer    │
   │  Details   │          │    Details     │      │    Details     │
   │  (1-to-1)  │          │    (1-to-1)    │      │    (1-to-1)    │
   └────────────┘          └────────────────┘      └────────────────┘


   ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
   │ ref.UserRole │◄────────│     User     │────────►│ref.UserStatus│
   └──────────────┘         └──────┬───────┘         └──────────────┘
                                   │
                                   │ FK: UserID
                                   │
                            ┌──────▼─────────┐
                            │  UserCompany   │ (Many-to-Many)
                            │                │
                            │ FK: CompanyID  │
                            │ FK: UserID     │
                            └────────────────┘
                                   │
                                   ├────► ref.UserCompanyRole
                                   └────► ref.UserCompanyStatus


   ┌──────────────┐
   │ UserInvitation│
   │                │
   │ FK: CompanyID  │
   │ FK: RoleID     │
   │ FK: StatusID   │
   └────────────────┘
         │
         └────► ref.UserInvitationStatus


   ┌──────────────────┐         ┌──────────────────┐
   │ EmailVerification│         │ PasswordReset    │
   │     Token        │         │     Token        │
   │                  │         │                  │
   │ FK: UserID       │         │ FK: UserID       │
   └──────────────────┘         └──────────────────┘
```

---

## 📐 Common Columns (All Tables)

**Audit Trail:**
- `CreatedDate` (DATETIME2, default GETUTCDATE())
- `CreatedBy` (BIGINT, FK → User.UserID)
- `UpdatedDate` (DATETIME2, NULL)
- `UpdatedBy` (BIGINT, FK → User.UserID)

**Soft Delete:**
- `IsDeleted` (BIT, default 0)
- `DeletedDate` (DATETIME2, NULL)
- `DeletedBy` (BIGINT, FK → User.UserID)

---

## 🏷️ Naming Conventions

**Tables:**
- Singular noun, PascalCase: `User`, `Company`, `Form`

**Primary Keys:**
- `[TableName]ID`: `UserID`, `CompanyID`, `FormID`

**Foreign Keys:**
- `[ReferencedTableName]ID`: `CompanyID`, `UserRoleID`, `CountryID`

**Booleans:**
- `Is` or `Has` prefix: `IsActive`, `IsDeleted`, `HasAccess`

**Dates:**
- Descriptive suffix: `CreatedDate`, `UpdatedDate`, `ExpiresAt`

**Constraints:**
- `PK_[Table]_[Column]`: `PK_User_UserID`
- `FK_[SourceTable]_[TargetTable]_[Column]`: `FK_User_Country_CountryID`
- `UQ_[Table]_[Column]`: `UQ_User_Email`
- `IX_[Table]_[Column]`: `IX_User_Email`

---

## 🔍 Common Query Patterns

### **Get User with Status**

```sql
SELECT u.*, us.StatusName
FROM dbo.User u
INNER JOIN ref.UserStatus us ON u.StatusID = us.UserStatusID
WHERE u.Email = 'john@example.com';
```

### **Get Company's Team Members**

```sql
SELECT u.FirstName, u.LastName, u.Email, ucr.RoleName
FROM dbo.UserCompany uc
INNER JOIN dbo.User u ON uc.UserID = u.UserID
INNER JOIN ref.UserCompanyRole ucr ON uc.UserCompanyRoleID = ucr.UserCompanyRoleID
WHERE uc.CompanyID = @company_id
  AND uc.IsDeleted = 0;
```

### **Multi-Tenant Filtering (CRITICAL)**

```sql
-- ✅ CORRECT: Filter by CompanyID
SELECT * FROM dbo.Form WHERE CompanyID = @current_company_id;

-- ❌ WRONG: No company filter (security breach!)
SELECT * FROM dbo.Form;
```

---

## 🚦 Database Health Checks

```sql
-- Table count by schema
SELECT TABLE_SCHEMA, COUNT(*) as TableCount
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
GROUP BY TABLE_SCHEMA;

-- Foreign key count
SELECT COUNT(*) as ForeignKeyCount
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE CONSTRAINT_TYPE = 'FOREIGN KEY';

-- Index count
SELECT COUNT(*) as IndexCount
FROM sys.indexes
WHERE type > 0;  -- Exclude heaps

-- Row counts per table
SELECT 
    s.name + '.' + t.name as TableName,
    SUM(p.rows) as RowCount
FROM sys.tables t
INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
INNER JOIN sys.partitions p ON t.object_id = p.object_id
WHERE p.index_id IN (0, 1)  -- Heap or clustered index
GROUP BY s.name, t.name
ORDER BY RowCount DESC;
```

---

## 📊 Schema Statistics

**Totals:**
- **Tables:** 45
- **Foreign Keys:** ~60
- **Unique Constraints:** ~25
- **Indexes:** ~40
- **Seed Records:** ~150

**Relationships:**
- `User` ↔ `Company`: Many-to-Many (via `UserCompany`)
- `Company` ↔ `CompanyCustomerDetails`: 1-to-1
- `Company` ↔ `Company`: Hierarchical (ParentCompanyID)
- `User` ↔ `UserEmailVerificationToken`: 1-to-Many
- `Company` ↔ `UserInvitation`: 1-to-Many

---

## 📚 Related Documentation

**Database Details:**
- `docs/database/REBUILD-PLAN-SUMMARY.md` - Executive summary
- `docs/database/schema-reference/dbo-schema.md` - Core business tables
- `docs/database/schema-reference/ref-schema.md` - Reference tables
- `docs/database/schema-reference/config-schema.md` - Configuration tables
- `docs/database/schema-reference/audit-schema.md` - Audit tables
- `docs/database/schema-reference/log-schema.md` - Logging tables
- `docs/database/schema-reference/cache-schema.md` - Cache tables

**Architecture:**
- `docs/solution-architecture.md` - Overall architecture
- `docs/architecture/decisions/ADR-001-database-schema-organization.md`
- `docs/architecture/decisions/ADR-004-database-normalization.md`

---

**Winston** 🏗️  
*"45 tables organized into 6 schemas. That's the foundation."*

