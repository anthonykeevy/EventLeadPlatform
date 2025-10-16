# `dbo` Schema - Core Business Entities

**Schema Purpose:** Primary business data customers pay for  
**Table Count:** 13  
**Retention:** Permanent (soft delete only, never hard delete)  
**Backup Priority:** CRITICAL (hourly backups + point-in-time recovery)  
**Write Volume:** Medium

---

## Table Overview

| # | Table | Purpose | Key Relationships |
|---|-------|---------|-------------------|
| 1 | `User` | User accounts | → `UserStatus`, `Country`, `Language`, `UserRole` |
| 2 | `UserCompany` | User-company relationships | → `User`, `Company`, `UserCompanyRole`, `UserCompanyStatus` |
| 3 | `Company` | Company profiles | → `Country`, `Industry`, self-ref (ParentCompanyID) |
| 4 | `CompanyCustomerDetails` | Customer subscription data | → `Company`, `CustomerTier` |
| 5 | `CompanyBillingDetails` | Billing information | → `Company`, `Country` (billing address) |
| 6 | `CompanyOrganizerDetails` | Event organizer data | → `Company` |
| 7 | `UserInvitation` | Team invitations | → `Company`, `UserCompanyRole`, `UserInvitationStatus` |
| 8 | `UserEmailVerificationToken` | Email verification tokens | → `User` |
| 9 | `UserPasswordResetToken` | Password reset tokens | → `User` |

---

## 1. `dbo.User` - User Accounts

**Purpose:** Core user accounts (authentication + profile)

**Key Features:**
- JWT session management (SessionToken, AccessTokenVersion, RefreshTokenVersion)
- Comprehensive profile (RoleTitle, ProfilePictureUrl, TimezoneIdentifier)
- Security tracking (EmailVerifiedAt, LastPasswordChange, FailedLoginAttempts)
- Self-referential audit FKs (CreatedBy, UpdatedBy, DeletedBy → UserID)
- Account locking (IsLocked, LockedUntil, LockedReason)

**Primary Key:** `UserID` (BIGINT IDENTITY)

**Foreign Keys:**
- `StatusID` → `ref.UserStatus.UserStatusID`
- `UserRoleID` → `ref.UserRole.UserRoleID`
- `CountryID` → `ref.Country.CountryID`
- `LanguageID` → `ref.Language.LanguageID`
- `CreatedBy`, `UpdatedBy`, `DeletedBy` → `dbo.User.UserID` (self-referential)

**Unique Constraints:**
- `Email` (UQ_User_Email)
- `SessionToken` (UQ_User_SessionToken)

**Indexes:**
- `IX_User_Email` (frequent lookups)
- `IX_User_StatusID` (filtering by status)
- `IX_User_UserRoleID` (role-based queries)

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: dbo.User)

---

## 2. `dbo.UserCompany` - User-Company Relationships

**Purpose:** Many-to-many relationship between users and companies (team membership)

**Key Features:**
- Tracks invitation source (InvitedByUserID, JoinedVia)
- Comprehensive removal tracking (RemovedDate, RemovedBy, RemovalReason)
- Status management (active, suspended, removed)
- Notes field for administrative comments

**Primary Key:** `UserCompanyID` (BIGINT IDENTITY)

**Composite Unique Constraint:** `(UserID, CompanyID)` - User can only belong to company once

**Foreign Keys:**
- `UserID` → `dbo.User.UserID`
- `CompanyID` → `dbo.Company.CompanyID`
- `UserCompanyRoleID` → `ref.UserCompanyRole.UserCompanyRoleID`
- `UserCompanyStatusID` → `ref.UserCompanyStatus.UserCompanyStatusID`
- `JoinedViaID` → `ref.JoinedVia.JoinedViaID`
- `InvitedByUserID` → `dbo.User.UserID`
- `RemovedBy` → `dbo.User.UserID`

**Indexes:**
- `IX_UserCompany_UserID` (find all companies for user)
- `IX_UserCompany_CompanyID` (find all users in company)
- `IX_UserCompany_UserCompanyRoleID` (filter by role)

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: dbo.UserCompany)

---

## 3. `dbo.Company` - Company Profiles

**Purpose:** Company/organization accounts (multi-tenant isolation)

**Key Features:**
- ABR integration (LegalEntityName, ABN, ABNStatus, EntityType, GSTRegistered)
- Flexible naming (BusinessNames JSON array, CustomDisplayName, DisplayNameSource)
- Hierarchical relationships (ParentCompanyID for subsidiaries)
- Multi-tenant isolation (every tenant-specific table has FK to CompanyID)

**Primary Key:** `CompanyID` (BIGINT IDENTITY)

**Foreign Keys:**
- `CountryID` → `ref.Country.CountryID`
- `IndustryID` → `ref.Industry.IndustryID`
- `ParentCompanyID` → `dbo.Company.CompanyID` (self-referential)

**Unique Constraints:**
- `CompanyName` (UQ_Company_CompanyName)
- `ABN` (UQ_Company_ABN) - Australia-specific

**Indexes:**
- `IX_Company_CountryID` (filter by country)
- `IX_Company_ParentCompanyID` (hierarchical queries)

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: dbo.Company)

---

## 4. `dbo.CompanyCustomerDetails` - Customer Subscription Data

**Purpose:** 1-to-1 extension of Company for customer-specific data (subscription, billing cycle)

**Key Features:**
- Subscription tier tracking (CustomerTierID)
- Trial management (IsTrialActive, TrialStartDate, TrialEndDate)
- Billing cycle (BillingCycleDay, NextBillingDate)
- Feature usage tracking (UsedStorage, UsedSubmissions)

**Primary Key:** `CompanyCustomerDetailsID` (BIGINT IDENTITY)

**Foreign Keys:**
- `CompanyID` → `dbo.Company.CompanyID` (1-to-1)
- `CustomerTierID` → `ref.CustomerTier.CustomerTierID`

**Unique Constraints:**
- `CompanyID` (UQ_CompanyCustomerDetails_CompanyID) - Enforces 1-to-1

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: dbo.CompanyCustomerDetails)

---

## 5. `dbo.CompanyBillingDetails` - Billing Information

**Purpose:** 1-to-1 extension of Company for billing/invoicing data

**Key Features:**
- Billing contact (BillingEmail, BillingPhone)
- Billing address (separate from company address, FK to Country)
- Payment method tracking (not implemented yet, future)

**Primary Key:** `CompanyBillingDetailsID` (BIGINT IDENTITY)

**Foreign Keys:**
- `CompanyID` → `dbo.Company.CompanyID` (1-to-1)
- `BillingCountryID` → `ref.Country.CountryID`

**Unique Constraints:**
- `CompanyID` (UQ_CompanyBillingDetails_CompanyID) - Enforces 1-to-1

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: dbo.CompanyBillingDetails)

---

## 6. `dbo.CompanyOrganizerDetails` - Event Organizer Data

**Purpose:** 1-to-1 extension of Company for event organizer-specific data

**Key Features:**
- Public profile (Website, Description)
- Social media links (not implemented yet)
- Organizer-specific settings

**Primary Key:** `CompanyOrganizerDetailsID` (BIGINT IDENTITY)

**Foreign Keys:**
- `CompanyID` → `dbo.Company.CompanyID` (1-to-1)

**Unique Constraints:**
- `CompanyID` (UQ_CompanyOrganizerDetails_CompanyID) - Enforces 1-to-1

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: dbo.CompanyOrganizerDetails)

---

## 7. `dbo.UserInvitation` - Team Invitations

**Purpose:** Track team member invitations (pending, accepted, declined, expired, cancelled)

**Key Features:**
- Comprehensive lifecycle tracking (CancelledAt, DeclinedAt, ResendCount)
- Rate limiting (ResendCount, LastResentAt)
- Expiry management (ExpiresAt, typically 7 days)
- Security tracking (Token, IPAddress, UserAgent)

**Primary Key:** `UserInvitationID` (BIGINT IDENTITY)

**Foreign Keys:**
- `CompanyID` → `dbo.Company.CompanyID`
- `InvitedByUserID` → `dbo.User.UserID`
- `AcceptedByUserID` → `dbo.User.UserID` (NULL until accepted)
- `UserCompanyRoleID` → `ref.UserCompanyRole.UserCompanyRoleID`
- `UserInvitationStatusID` → `ref.UserInvitationStatus.UserInvitationStatusID`
- `CancelledBy` → `dbo.User.UserID`

**Unique Constraints:**
- `(InvitedEmail, CompanyID, UserInvitationStatusID)` - Prevent duplicate pending invitations
- `Token` (UQ_UserInvitation_Token)

**Indexes:**
- `IX_UserInvitation_CompanyID` (find all invitations for company)
- `IX_UserInvitation_InvitedEmail` (lookup by email)
- `IX_UserInvitation_ExpiresAt` (cleanup expired invitations)

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: dbo.UserInvitation)

---

## 8. `dbo.UserEmailVerificationToken` - Email Verification Tokens

**Purpose:** Secure token for email verification (generated after signup)

**Key Features:**
- Cryptographically secure token (GUID)
- 24-hour expiry
- One-time use (IsUsed flag)

**Primary Key:** `UserEmailVerificationTokenID` (BIGINT IDENTITY)

**Foreign Keys:**
- `UserID` → `dbo.User.UserID`

**Unique Constraints:**
- `Token` (UQ_UserEmailVerificationToken_Token)

**Indexes:**
- `IX_UserEmailVerificationToken_UserID` (find tokens for user)
- `IX_UserEmailVerificationToken_ExpiresAt` (cleanup expired tokens)

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: dbo.UserEmailVerificationToken)

---

## 9. `dbo.UserPasswordResetToken` - Password Reset Tokens

**Purpose:** Secure token for password reset (forgot password flow)

**Key Features:**
- Cryptographically secure token (GUID)
- 1-hour expiry (shorter than email verification)
- One-time use (IsUsed flag)
- Security tracking (IPAddress, UserAgent)

**Primary Key:** `UserPasswordResetTokenID` (BIGINT IDENTITY)

**Foreign Keys:**
- `UserID` → `dbo.User.UserID`

**Unique Constraints:**
- `Token` (UQ_UserPasswordResetToken_Token)

**Indexes:**
- `IX_UserPasswordResetToken_UserID` (find tokens for user)
- `IX_UserPasswordResetToken_ExpiresAt` (cleanup expired tokens)

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: dbo.UserPasswordResetToken)

---

## Common Patterns

### **Audit Columns (All Tables)**
Every table includes:
- `CreatedDate` (DATETIME2, default GETUTCDATE())
- `CreatedBy` (BIGINT, FK to User.UserID)
- `UpdatedDate` (DATETIME2, NULL)
- `UpdatedBy` (BIGINT, FK to User.UserID)

### **Soft Delete (All Tables)**
Every table includes:
- `IsDeleted` (BIT, default 0)
- `DeletedDate` (DATETIME2, NULL)
- `DeletedBy` (BIGINT, FK to User.UserID)

**Note:** NEVER hard delete records. Always set `IsDeleted = 1`.

### **Foreign Key Naming**
All foreign keys use pattern: `FK_[SourceTable]_[TargetTable]_[ColumnName]`

Example: `FK_UserCompany_Company_CompanyID`

### **Unique Constraint Naming**
All unique constraints use pattern: `UQ_[TableName]_[ColumnNames]`

Example: `UQ_User_Email`

### **Index Naming**
All indexes use pattern: `IX_[TableName]_[ColumnNames]`

Example: `IX_UserCompany_CompanyID`

---

## Multi-Tenant Isolation

**Critical: All tenant-specific tables MUST filter by `CompanyID`**

**Tenant-Specific Tables in `dbo` Schema:**
- `UserCompany` (links users to companies)
- `UserInvitation` (company-specific invitations)
- `CompanyCustomerDetails` (1-to-1 with Company)
- `CompanyBillingDetails` (1-to-1 with Company)
- `CompanyOrganizerDetails` (1-to-1 with Company)

**EVERY query that accesses tenant-specific data MUST include:**
```sql
WHERE CompanyID = @current_company_id
```

**Defense in Depth:**
1. Application layer: FastAPI dependency injection (get_current_company)
2. ORM layer: SQLAlchemy automatic filtering
3. Database layer: SQL Server Row-Level Security (RLS) policies

---

## Related Documentation

**Architecture:**
- `docs/solution-architecture.md` - Database Architecture section
- `docs/architecture/decisions/ADR-001-database-schema-organization.md`

**Database:**
- `docs/database/REBUILD-PLAN-SUMMARY.md` - Executive summary
- `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` - Full SQL definitions

**Implementation:**
- `docs/technical-guides/backend-database-abstraction-layer.md` - SQLAlchemy patterns
- `docs/technical-guides/backend-quick-reference.md` - Cheat sheet

---

**Winston** 🏗️  
*"These 13 tables are the foundation of everything."*

