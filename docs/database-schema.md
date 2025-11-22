# Database Schema - EventLeadPlatform

**Generated:** 2025-11-19 19:21:39
**Updated:** 2025-01-XX (Added agency role, ownership transfer, access function)
**Total Tables:** 61
**Stored Procedures:** 1 (sp_TransferFormOwnership)
**Functions:** 1 (fn_GetUserFormAccess)

## Overview

This document provides a complete schema reference for the EventLeadPlatform database. Tables are grouped by **domain** (User, Company, Event, Form, etc.) rather than schema. Each table name includes its schema prefix (e.g., `dbo.User`, `ref.Country`) for clarity.

**Notation:**
- `PK` = Primary Key column
- `FK→Table` = Foreign Key to another table (table name shown; schema prefix included if different schema)
- `FK→dbo.User` = Foreign Key to dbo.User (different schema)
- `FK→User` = Foreign Key to User table in same schema
- Empty cells in Default column = no default value

**Schema Organization:**
- `dbo` = Core business entities (User, Company, Event, Form)
- `ref` = Reference/lookup tables (Country, UserStatus, EventType, etc.)
- `config` = Configuration tables (AppSetting, ValidationRule)
- `audit` = Audit trail tables (compliance tracking)
- `log` = Technical logging tables (API requests, errors, etc.)
- `cache` = Cache tables (ABR search results)

## User Domain

### Table: audit.User

**Columns (13):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| AuditUserID | BIGINT | NO |  | PK |
| UserID | BIGINT | NO |  | FK→dbo.User |
| FieldName | NVARCHAR(100) | NO |  |  |
| OldValue | NVARCHAR(-1) | YES |  |  |
| NewValue | NVARCHAR(-1) | YES |  |  |
| ChangeType | NVARCHAR(50) | NO |  |  |
| ChangeReason | NVARCHAR(500) | YES |  |  |
| ChangedBy | BIGINT | YES |  | FK→dbo.User |
| ChangedByEmail | NVARCHAR(255) | YES |  |  |
| IPAddress | NVARCHAR(50) | YES |  |  |
| UserAgent | NVARCHAR(500) | YES |  |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| IsDeleted | BIT | NO | 0 |  |

---

### Table: dbo.User

**Columns (38):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| UserID | BIGINT | NO |  | PK |
| Email | NVARCHAR(255) | NO |  |  |
| PasswordHash | NVARCHAR(500) | NO |  |  |
| FirstName | NVARCHAR(100) | NO |  |  |
| LastName | NVARCHAR(100) | NO |  |  |
| Phone | NVARCHAR(20) | YES |  |  |
| RoleTitle | NVARCHAR(100) | YES |  |  |
| ProfilePictureUrl | NVARCHAR(500) | YES |  |  |
| TimezoneIdentifier | NVARCHAR(50) | NO | 'Australia/Sydney' |  |
| StatusID | BIGINT | NO |  | FK→ref.UserStatus |
| IsEmailVerified | BIT | NO | 0 |  |
| EmailVerifiedAt | DATETIME2 | YES |  |  |
| IsLocked | BIT | NO | 0 |  |
| LockedUntil | DATETIME2 | YES |  |  |
| LockedReason | NVARCHAR(500) | YES |  |  |
| FailedLoginAttempts | INT | NO | 0 |  |
| LastLoginDate | DATETIME2 | YES |  |  |
| LastPasswordChange | DATETIME2 | YES |  |  |
| SessionToken | NVARCHAR(255) | YES |  |  |
| AccessTokenVersion | INT | NO | 1 |  |
| RefreshTokenVersion | INT | NO | 1 |  |
| OnboardingComplete | BIT | NO | 0 |  |
| OnboardingStep | INT | NO | 1 |  |
| CountryID | BIGINT | YES |  | FK→ref.Country |
| PreferredLanguageID | BIGINT | YES |  | FK→ref.Language |
| UserRoleID | BIGINT | YES |  | FK→ref.UserRole |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  | FK→User |
| UpdatedDate | DATETIME2 | NO | getutcdate() |  |
| UpdatedBy | BIGINT | YES |  | FK→User |
| IsDeleted | BIT | NO | 0 |  |
| DeletedDate | DATETIME2 | YES |  |  |
| DeletedBy | BIGINT | YES |  | FK→User |
| Bio | VARCHAR(500) | YES |  |  |
| ThemePreferenceID | BIGINT | YES |  | FK→ref.ThemePreference |
| LayoutDensityID | BIGINT | YES |  | FK→ref.LayoutDensity |
| FontSizeID | BIGINT | YES |  | FK→ref.FontSize |
| IsExternalApprover | BIT | NO | 0 |  |

---

### Table: log.UserAction

**Columns (7):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| UserActionID | BIGINT | NO |  | PK |
| UserID | BIGINT | NO |  | FK→dbo.User |
| Action | NVARCHAR(100) | NO |  |  |
| Details | NVARCHAR(-1) | YES |  |  |
| Path | NVARCHAR(500) | YES |  |  |
| RequestID | NVARCHAR(100) | YES |  |  |
| CreatedDate | DATETIME | NO | getutcdate() |  |

---

### Table: dbo.UserCompany

**Columns (20):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| UserCompanyID | BIGINT | NO |  | PK |
| UserID | BIGINT | NO |  | FK→User |
| CompanyID | BIGINT | NO |  | FK→Company |
| UserCompanyRoleID | BIGINT | NO |  | FK→ref.UserCompanyRole |
| StatusID | BIGINT | NO |  | FK→ref.UserCompanyStatus |
| IsPrimaryCompany | BIT | NO | 0 |  |
| JoinedDate | DATETIME2 | NO | getutcdate() |  |
| JoinedViaID | BIGINT | NO |  | FK→ref.JoinedVia |
| InvitedBy | BIGINT | YES |  | FK→User |
| InvitedDate | DATETIME2 | YES |  |  |
| RemovedDate | DATETIME2 | YES |  |  |
| RemovedBy | BIGINT | YES |  | FK→User |
| RemovalReason | NVARCHAR(500) | YES |  |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  | FK→User |
| UpdatedDate | DATETIME2 | NO | getutcdate() |  |
| UpdatedBy | BIGINT | YES |  | FK→User |
| IsDeleted | BIT | NO | 0 |  |
| DeletedDate | DATETIME2 | YES |  |  |
| DeletedBy | BIGINT | YES |  | FK→User |

---

### Table: ref.UserCompanyRole

**Columns (17):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| UserCompanyRoleID | BIGINT | NO |  | PK |
| RoleCode | NVARCHAR(50) | NO |  |  |
| RoleName | NVARCHAR(100) | NO |  |  |
| Description | NVARCHAR(500) | NO |  |  |
| RoleLevel | INT | NO |  |  |
| CanManageCompany | BIT | NO | 0 |  |
| CanManageUsers | BIT | NO | 0 |  |
| CanManageEvents | BIT | NO | 0 |  |
| CanManageForms | BIT | NO | 0 |  |
| CanExportData | BIT | NO | 0 |  |
| CanViewReports | BIT | NO | 0 |  |
| IsActive | BIT | NO | 1 |  |
| SortOrder | INT | NO | 0 |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  |  |
| UpdatedDate | DATETIME2 | YES |  |  |
| UpdatedBy | BIGINT | YES |  |  |

---

### Table: ref.UserCompanyStatus

**Columns (10):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| UserCompanyStatusID | BIGINT | NO |  | PK |
| StatusCode | NVARCHAR(20) | NO |  |  |
| StatusName | NVARCHAR(50) | NO |  |  |
| Description | NVARCHAR(500) | NO |  |  |
| IsActive | BIT | NO | 1 |  |
| SortOrder | INT | NO | 0 |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  |  |
| UpdatedDate | DATETIME2 | YES |  |  |
| UpdatedBy | BIGINT | YES |  |  |

---

### Table: dbo.UserEmailVerificationToken

**Columns (7):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| UserEmailVerificationTokenID | BIGINT | NO |  | PK |
| UserID | BIGINT | NO |  | FK→User |
| Token | NVARCHAR(500) | NO |  |  |
| ExpiresAt | DATETIME2 | NO |  |  |
| IsUsed | BIT | NO | 0 |  |
| UsedAt | DATETIME2 | YES |  |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |

---

### Table: dbo.UserIndustry

**Columns (12):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| UserIndustryID | BIGINT | NO |  | PK |
| UserID | BIGINT | NO |  | FK→User |
| IndustryID | BIGINT | NO |  | FK→ref.Industry |
| IsPrimary | BIT | NO | 0 |  |
| SortOrder | INT | NO | 0 |  |
| CreatedDate | DATETIME | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  | FK→User |
| UpdatedDate | DATETIME | YES |  |  |
| UpdatedBy | BIGINT | YES |  | FK→User |
| IsDeleted | BIT | NO | 0 |  |
| DeletedDate | DATETIME | YES |  |  |
| DeletedBy | BIGINT | YES |  | FK→User |

---

### Table: dbo.UserInvitation

**Columns (27):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| UserInvitationID | BIGINT | NO |  | PK |
| CompanyID | BIGINT | NO |  | FK→Company |
| InvitedBy | BIGINT | NO |  | FK→User |
| Email | NVARCHAR(255) | NO |  |  |
| FirstName | NVARCHAR(100) | NO |  |  |
| LastName | NVARCHAR(100) | NO |  |  |
| UserCompanyRoleID | BIGINT | NO |  | FK→ref.UserCompanyRole |
| InvitationToken | NVARCHAR(500) | NO |  |  |
| StatusID | BIGINT | NO |  | FK→ref.UserInvitationStatus |
| InvitedAt | DATETIME2 | NO | getutcdate() |  |
| ExpiresAt | DATETIME2 | NO |  |  |
| AcceptedAt | DATETIME2 | YES |  |  |
| AcceptedBy | BIGINT | YES |  | FK→User |
| CancelledAt | DATETIME2 | YES |  |  |
| CancelledBy | BIGINT | YES |  | FK→User |
| CancellationReason | NVARCHAR(500) | YES |  |  |
| DeclinedAt | DATETIME2 | YES |  |  |
| DeclineReason | NVARCHAR(500) | YES |  |  |
| ResendCount | INT | NO | 0 |  |
| LastResentAt | DATETIME2 | YES |  |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  | FK→User |
| UpdatedDate | DATETIME2 | NO | getutcdate() |  |
| UpdatedBy | BIGINT | YES |  | FK→User |
| IsDeleted | BIT | NO | 0 |  |
| DeletedDate | DATETIME2 | YES |  |  |
| DeletedBy | BIGINT | YES |  | FK→User |

---

### Table: ref.UserInvitationStatus

**Columns (13):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| UserInvitationStatusID | BIGINT | NO |  | PK |
| StatusCode | NVARCHAR(20) | NO |  |  |
| StatusName | NVARCHAR(50) | NO |  |  |
| Description | NVARCHAR(500) | NO |  |  |
| CanResend | BIT | NO | 0 |  |
| CanCancel | BIT | NO | 0 |  |
| IsFinalState | BIT | NO | 0 |  |
| IsActive | BIT | NO | 1 |  |
| SortOrder | INT | NO | 0 |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  |  |
| UpdatedDate | DATETIME2 | YES |  |  |
| UpdatedBy | BIGINT | YES |  |  |

---

### Table: dbo.UserPasswordResetToken

**Columns (9):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| UserPasswordResetTokenID | BIGINT | NO |  | PK |
| UserID | BIGINT | NO |  | FK→User |
| Token | NVARCHAR(500) | NO |  |  |
| ExpiresAt | DATETIME2 | NO |  |  |
| IsUsed | BIT | NO | 0 |  |
| UsedAt | DATETIME2 | YES |  |  |
| IPAddress | NVARCHAR(50) | YES |  |  |
| UserAgent | NVARCHAR(500) | YES |  |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |

---

### Table: dbo.UserRefreshToken

**Columns (9):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| UserRefreshTokenID | BIGINT | NO |  | PK |
| UserID | BIGINT | NO |  | FK→User |
| Token | VARCHAR(500) | NO |  |  |
| ExpiresAt | DATETIME | NO |  |  |
| IsUsed | BIT | NO | 0 |  |
| UsedAt | DATETIME | YES |  |  |
| IsRevoked | BIT | NO | 0 |  |
| RevokedAt | DATETIME | YES |  |  |
| CreatedDate | DATETIME | NO | getutcdate() |  |

---

### Table: ref.UserRole

**Columns (15):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| UserRoleID | BIGINT | NO |  | PK |
| RoleCode | NVARCHAR(50) | NO |  |  |
| RoleName | NVARCHAR(100) | NO |  |  |
| Description | NVARCHAR(500) | NO |  |  |
| RoleLevel | INT | NO |  |  |
| CanManagePlatform | BIT | NO | 0 |  |
| CanManageAllCompanies | BIT | NO | 0 |  |
| CanViewAllData | BIT | NO | 0 |  |
| CanAssignSystemRoles | BIT | NO | 0 |  |
| IsActive | BIT | NO | 1 |  |
| SortOrder | INT | NO | 0 |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  |  |
| UpdatedDate | DATETIME2 | YES |  |  |
| UpdatedBy | BIGINT | YES |  |  |

---

### Table: ref.UserStatus

**Columns (11):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| UserStatusID | BIGINT | NO |  | PK |
| StatusCode | NVARCHAR(20) | NO |  |  |
| StatusName | NVARCHAR(50) | NO |  |  |
| Description | NVARCHAR(500) | NO |  |  |
| AllowLogin | BIT | NO | 0 |  |
| IsActive | BIT | NO | 1 |  |
| SortOrder | INT | NO | 0 |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  |  |
| UpdatedDate | DATETIME2 | YES |  |  |
| UpdatedBy | BIGINT | YES |  |  |

---

## Company Domain

### Table: dbo.Company

**Columns (25):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| CompanyID | BIGINT | NO |  | PK |
| CompanyName | NVARCHAR(200) | NO |  |  |
| LegalEntityName | NVARCHAR(200) | YES |  |  |
| BusinessNames | NVARCHAR(-1) | YES |  |  |
| CustomDisplayName | NVARCHAR(200) | YES |  |  |
| DisplayNameSource | NVARCHAR(20) | NO | 'User' |  |
| ABN | NVARCHAR(11) | YES |  |  |
| ACN | NVARCHAR(9) | YES |  |  |
| ABNStatus | NVARCHAR(20) | YES |  |  |
| EntityType | NVARCHAR(100) | YES |  |  |
| GSTRegistered | BIT | YES |  |  |
| Phone | NVARCHAR(20) | YES |  |  |
| Email | NVARCHAR(255) | YES |  |  |
| Website | NVARCHAR(500) | YES |  |  |
| CountryID | BIGINT | NO |  | FK→ref.Country |
| IndustryID | BIGINT | YES |  | FK→ref.Industry |
| ParentCompanyID | BIGINT | YES |  | FK→Company |
| IsActive | BIT | NO | 1 |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  |  |
| UpdatedDate | DATETIME2 | NO | getutcdate() |  |
| UpdatedBy | BIGINT | YES |  |  |
| IsDeleted | BIT | NO | 0 |  |
| DeletedDate | DATETIME2 | YES |  |  |
| DeletedBy | BIGINT | YES |  |  |

---

### Table: audit.Company

**Columns (13):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| AuditCompanyID | BIGINT | NO |  | PK |
| CompanyID | BIGINT | NO |  | FK→dbo.Company |
| FieldName | NVARCHAR(100) | NO |  |  |
| OldValue | NVARCHAR(-1) | YES |  |  |
| NewValue | NVARCHAR(-1) | YES |  |  |
| ChangeType | NVARCHAR(50) | NO |  |  |
| ChangeReason | NVARCHAR(500) | YES |  |  |
| ChangedBy | BIGINT | YES |  | FK→dbo.User |
| ChangedByEmail | NVARCHAR(255) | YES |  |  |
| IPAddress | NVARCHAR(50) | YES |  |  |
| UserAgent | NVARCHAR(500) | YES |  |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| IsDeleted | BIT | NO | 0 |  |

---

### Table: dbo.CompanyBillingDetails

**Columns (19):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| CompanyBillingDetailsID | BIGINT | NO |  | PK |
| CompanyID | BIGINT | NO |  | FK→Company |
| BillingContactName | NVARCHAR(200) | YES |  |  |
| BillingEmail | NVARCHAR(255) | YES |  |  |
| BillingPhone | NVARCHAR(20) | YES |  |  |
| BillingAddressLine1 | NVARCHAR(255) | YES |  |  |
| BillingAddressLine2 | NVARCHAR(255) | YES |  |  |
| BillingCity | NVARCHAR(100) | YES |  |  |
| BillingState | NVARCHAR(100) | YES |  |  |
| BillingPostalCode | NVARCHAR(20) | YES |  |  |
| BillingCountryID | BIGINT | YES |  | FK→ref.Country |
| StripeCustomerID | NVARCHAR(100) | YES |  |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  | FK→User |
| UpdatedDate | DATETIME2 | NO | getutcdate() |  |
| UpdatedBy | BIGINT | YES |  | FK→User |
| IsDeleted | BIT | NO | 0 |  |
| DeletedDate | DATETIME2 | YES |  |  |
| DeletedBy | BIGINT | YES |  | FK→User |

---

### Table: dbo.CompanyCustomerDetails

**Columns (13):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| CompanyCustomerDetailsID | BIGINT | NO |  | PK |
| CompanyID | BIGINT | NO |  | FK→Company |
| CustomerSince | DATETIME2 | NO | getutcdate() |  |
| CustomerTierID | BIGINT | NO |  | FK→ref.CustomerTier |
| TotalEvents | INT | NO | 0 |  |
| TotalLeadsCaptured | INT | NO | 0 |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  | FK→User |
| UpdatedDate | DATETIME2 | NO | getutcdate() |  |
| UpdatedBy | BIGINT | YES |  | FK→User |
| IsDeleted | BIT | NO | 0 |  |
| DeletedDate | DATETIME2 | YES |  |  |
| DeletedBy | BIGINT | YES |  | FK→User |

---

### Table: dbo.CompanyOrganizerDetails

**Columns (12):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| CompanyOrganizerDetailsID | BIGINT | NO |  | PK |
| CompanyID | BIGINT | NO |  | FK→Company |
| OrganizerLicenseNumber | NVARCHAR(100) | YES |  |  |
| EventTypesOrganized | NVARCHAR(-1) | YES |  |  |
| AverageEventsPerYear | INT | YES |  |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  | FK→User |
| UpdatedDate | DATETIME2 | NO | getutcdate() |  |
| UpdatedBy | BIGINT | YES |  | FK→User |
| IsDeleted | BIT | NO | 0 |  |
| DeletedDate | DATETIME2 | YES |  |  |
| DeletedBy | BIGINT | YES |  | FK→User |

---

### Table: dbo.CompanyRelationship

**Columns (14):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| CompanyRelationshipID | BIGINT | NO |  | PK |
| ParentCompanyID | BIGINT | NO |  | FK→Company |
| ChildCompanyID | BIGINT | NO |  | FK→Company |
| RelationshipTypeID | INT | NO |  | FK→ref.CompanyRelationshipType |
| Status | VARCHAR(20) | NO |  |  |
| EstablishedBy | BIGINT | NO |  | FK→User |
| EstablishedAt | DATETIME | NO | getutcdate() |  |
| CreatedDate | DATETIME | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  | FK→User |
| UpdatedDate | DATETIME | NO | getutcdate() |  |
| UpdatedBy | BIGINT | YES |  | FK→User |
| IsDeleted | BIT | NO |  |  |
| DeletedDate | DATETIME | YES |  |  |
| DeletedBy | BIGINT | YES |  | FK→User |

---

### Table: ref.CompanyRelationshipType

**Columns (11):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| CompanyRelationshipTypeID | INT | NO |  | PK |
| TypeName | VARCHAR(50) | NO |  |  |
| TypeDescription | VARCHAR(255) | YES |  |  |
| IsActive | BIT | NO |  |  |
| CreatedDate | DATETIME | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  | FK→dbo.User |
| UpdatedDate | DATETIME | NO | getutcdate() |  |
| UpdatedBy | BIGINT | YES |  | FK→dbo.User |
| IsDeleted | BIT | NO |  |  |
| DeletedDate | DATETIME | YES |  |  |
| DeletedBy | BIGINT | YES |  | FK→dbo.User |

---

### Table: dbo.CompanySwitchRequest

**Columns (25):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| RequestID | BIGINT | NO |  | PK |
| UserID | BIGINT | NO |  | FK→User |
| FromCompanyID | BIGINT | YES |  | FK→Company |
| ToCompanyID | BIGINT | NO |  | FK→Company |
| RequestedBy | BIGINT | NO |  | FK→User |
| RequestedAt | DATETIME | NO | getutcdate() |  |
| Reason | VARCHAR(500) | YES |  |  |
| ApprovedBy | BIGINT | YES |  | FK→User |
| ApprovedAt | DATETIME | YES |  |  |
| RejectedBy | BIGINT | YES |  | FK→User |
| RejectedAt | DATETIME | YES |  |  |
| RejectionReason | VARCHAR(500) | YES |  |  |
| CreatedDate | DATETIME | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  | FK→User |
| UpdatedDate | DATETIME | NO | getutcdate() |  |
| UpdatedBy | BIGINT | YES |  | FK→User |
| IsDeleted | BIT | NO |  |  |
| DeletedDate | DATETIME | YES |  |  |
| DeletedBy | BIGINT | YES |  | FK→User |
| RequestTypeID | INT | NO |  | FK→ref.CompanySwitchRequestType |
| StatusID | INT | NO |  | FK→ref.CompanySwitchRequestStatus |
| RequestedAmount | DECIMAL | YES |  |  |
| RequestDescription | VARCHAR(-1) | YES |  |  |
| EventDate | DATETIME | YES |  |  |
| UrgencyLevel | VARCHAR(20) | YES |  |  |

---

### Table: ref.CompanySwitchRequestStatus

**Columns (4):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| CompanySwitchRequestStatusID | INT | NO |  | PK |
| StatusName | VARCHAR(50) | NO |  |  |
| StatusDescription | VARCHAR(255) | YES |  |  |
| IsActive | BIT | NO | '1' |  |

---

### Table: ref.CompanySwitchRequestType

**Columns (4):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| CompanySwitchRequestTypeID | INT | NO |  | PK |
| TypeName | VARCHAR(50) | NO |  |  |
| TypeDescription | VARCHAR(255) | YES |  |  |
| IsActive | BIT | NO | '1' |  |

---

### Table: config.CompanyValidationRule

**Columns (12):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| CompanyValidationRuleID | BIGINT | NO |  | PK |
| CompanyID | BIGINT | NO |  | FK→dbo.Company |
| ValidationRuleID | BIGINT | NO |  | FK→ValidationRule |
| IsEnabled | BIT | NO | 1 |  |
| SortOrderOverride | INT | YES |  |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  | FK→dbo.User |
| UpdatedDate | DATETIME2 | NO | getutcdate() |  |
| UpdatedBy | BIGINT | YES |  | FK→dbo.User |
| IsDeleted | BIT | NO | 0 |  |
| DeletedDate | DATETIME2 | YES |  |  |
| DeletedBy | BIGINT | YES |  | FK→dbo.User |

---

## Event Domain

### Table: dbo.Event

**Columns (45):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| EventID | BIGINT | NO |  | PK |
| Name | VARCHAR(200) | NO |  |  |
| Description | VARCHAR(-1) | YES |  |  |
| ShortDescription | VARCHAR(500) | YES |  |  |
| CompanyID | BIGINT | NO |  | FK→Company |
| StartDateTime | DATETIME | NO |  |  |
| EndDateTime | DATETIME | YES |  |  |
| TimezoneIdentifier | VARCHAR(50) | YES |  |  |
| VenueName | VARCHAR(200) | YES |  |  |
| VenueAddress | VARCHAR(500) | YES |  |  |
| City | VARCHAR(100) | YES |  |  |
| State | VARCHAR(100) | YES |  |  |
| CountryID | BIGINT | YES |  | FK→ref.Country |
| Latitude | DECIMAL | YES |  |  |
| Longitude | DECIMAL | YES |  |  |
| EventTypeID | INT | NO |  | FK→ref.EventType |
| IndustryID | BIGINT | YES |  | FK→ref.Industry |
| Tags | VARCHAR(-1) | YES |  |  |
| IsPublic | BIT | NO | 0 |  |
| EventStatusID | INT | NO |  | FK→ref.EventStatus |
| IsRecurring | BIT | NO | 0 |  |
| RecurrencePatternID | INT | YES |  | FK→ref.RecurrencePattern |
| IsPublicReviewRequired | BIT | NO | 1 |  |
| PublicReviewDate | DATETIME | YES |  |  |
| PublicReviewBy | BIGINT | YES |  | FK→User |
| PublicReviewComments | VARCHAR(-1) | YES |  |  |
| PublicVisibilityDate | DATETIME | YES |  |  |
| DuplicateEventID | BIGINT | YES |  | FK→Event |
| IsDuplicate | BIT | NO | 0 |  |
| OrganizerCompanyID | BIGINT | YES |  | FK→Company |
| OrganizerContactEmail | VARCHAR(100) | YES |  |  |
| OrganizerWebsite | VARCHAR(200) | YES |  |  |
| ExpectedAttendees | INT | YES |  |  |
| ActualAttendees | INT | YES |  |  |
| FormsCreated | INT | NO | 0 |  |
| TotalSubmissions | INT | NO | 0 |  |
| CreatedDate | DATETIME | NO | getutcdate() |  |
| CreatedBy | BIGINT | NO |  | FK→User |
| UpdatedDate | DATETIME | YES |  |  |
| UpdatedBy | BIGINT | YES |  | FK→User |
| IsDeleted | BIT | NO | 0 |  |
| DeletedDate | DATETIME | YES |  |  |
| DeletedBy | BIGINT | YES |  | FK→User |
| IsSharedWithPlatform | BIT | NO | '0' |  |
| PublicReviewStatusID | BIGINT | YES |  | FK→ref.PublicReviewStatus |

---

### Table: dbo.EventCompany

**Columns (17):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| EventCompanyID | BIGINT | NO |  | PK |
| EventID | BIGINT | NO |  | FK→Event |
| CompanyID | BIGINT | NO |  | FK→Company |
| EventCompanyRoleID | BIGINT | NO |  | FK→ref.EventCompanyRole |
| FormsCreated | INT | NO | '0' |  |
| FirstUsedDate | DATETIME | YES |  |  |
| LastUsedDate | DATETIME | YES |  |  |
| IsActive | BIT | NO | '1' |  |
| DisassociatedDate | DATETIME | YES |  |  |
| DisassociatedBy | BIGINT | YES |  | FK→User |
| CreatedDate | DATETIME | NO | getutcdate() |  |
| CreatedBy | BIGINT | NO |  | FK→User |
| UpdatedDate | DATETIME | YES |  |  |
| UpdatedBy | BIGINT | YES |  | FK→User |
| IsDeleted | BIT | NO | '0' |  |
| DeletedDate | DATETIME | YES |  |  |
| DeletedBy | BIGINT | YES |  | FK→User |

---

### Table: ref.EventCompanyRole

**Columns (17):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| EventCompanyRoleID | BIGINT | NO |  | PK |
| RoleCode | NVARCHAR(50) | NO |  |  |
| RoleName | NVARCHAR(100) | NO |  |  |
| Description | NVARCHAR(500) | NO |  |  |
| RoleLevel | INT | NO |  |  |
| HasEditEvent | BIT | NO | '0' |  |
| HasDeleteEvent | BIT | NO | '0' |  |
| HasManageParticipants | BIT | NO | '0' |  |
| HasViewEvent | BIT | NO | '1' |  |
| IsActive | BIT | NO | '1' |  |
| SortOrder | INT | NO | '0' |  |
| CreatedDate | DATETIME | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  | FK→dbo.User |
| UpdatedDate | DATETIME | YES |  |  |
| UpdatedBy | BIGINT | YES |  | FK→dbo.User |
| HasViewAllFormsForEvent | BIT | NO | '0' |  |
| HasEditAllFormsForEvent | BIT | NO | '0' |  |

---

### Table: ref.EventStatus

**Columns (15):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| EventStatusID | INT | NO |  | PK |
| StatusCode | VARCHAR(20) | NO |  |  |
| StatusName | VARCHAR(50) | NO |  |  |
| StatusDescription | VARCHAR(200) | YES |  |  |
| StatusColor | VARCHAR(7) | YES |  |  |
| StatusIcon | VARCHAR(50) | YES |  |  |
| IsActive | BIT | NO | 1 |  |
| SortOrder | INT | NO | 0 |  |
| CreatedDate | DATETIME | NO | getutcdate() |  |
| CreatedBy | BIGINT | NO |  | FK→dbo.User |
| UpdatedDate | DATETIME | YES |  |  |
| UpdatedBy | BIGINT | YES |  | FK→dbo.User |
| IsDeleted | BIT | NO | 0 |  |
| DeletedDate | DATETIME | YES |  |  |
| DeletedBy | BIGINT | YES |  | FK→dbo.User |

---

### Table: ref.EventType

**Columns (13):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| EventTypeID | INT | NO |  | PK |
| TypeCode | VARCHAR(20) | NO |  |  |
| TypeName | VARCHAR(50) | NO |  |  |
| TypeDescription | VARCHAR(200) | YES |  |  |
| IsActive | BIT | NO | 1 |  |
| SortOrder | INT | NO | 0 |  |
| CreatedDate | DATETIME | NO | getutcdate() |  |
| CreatedBy | BIGINT | NO |  | FK→dbo.User |
| UpdatedDate | DATETIME | YES |  |  |
| UpdatedBy | BIGINT | YES |  | FK→dbo.User |
| IsDeleted | BIT | NO | 0 |  |
| DeletedDate | DATETIME | YES |  |  |
| DeletedBy | BIGINT | YES |  | FK→dbo.User |

---

## Form Domain

### Table: dbo.Form

**Columns (23):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| FormID | BIGINT | NO |  | PK |
| FormName | VARCHAR(200) | NO |  |  |
| FormDescription | VARCHAR(-1) | YES |  |  |
| CompanyID | BIGINT | NO |  | FK→Company |
| EventID | BIGINT | YES |  | FK→Event |
| FormStatusID | INT | NO |  | FK→ref.FormStatus |
| FormApprovalStatusID | INT | NO |  | FK→ref.FormApprovalStatus |
| IsPublic | BIT | NO | 0 |  |
| DeploymentCost | DECIMAL | YES |  |  |
| TotalSubmissions | INT | NO | 0 |  |
| DemoLeadsCollected | INT | NO | 0 |  |
| ProductionLeadsCollected | INT | NO | 0 |  |
| LastSubmissionDate | DATETIME | YES |  |  |
| LastActivityDate | DATETIME | YES |  |  |
| FormThumbnailURL | VARCHAR(500) | YES |  |  |
| FormPreviewURL | VARCHAR(500) | YES |  |  |
| CreatedDate | DATETIME | NO | getutcdate() |  |
| CreatedBy | BIGINT | NO |  | FK→User |
| UpdatedDate | DATETIME | YES |  |  |
| UpdatedBy | BIGINT | YES |  | FK→User |
| IsDeleted | BIT | NO | 0 |  |
| DeletedDate | DATETIME | YES |  |  |
| DeletedBy | BIGINT | YES |  | FK→User |

---

### Table: dbo.FormAccessControl

**Columns (14):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| FormAccessControlID | BIGINT | NO |  | PK |
| FormID | BIGINT | NO |  | FK→Form |
| UserID | BIGINT | NO |  | FK→User |
| CompanyID | BIGINT | NO |  | FK→Company |
| FormAccessControlAccessTypeID | INT | NO |  | FK→ref.FormAccessControlAccessType |
| CompanyRelationshipTypeID | INT | NO |  | FK→ref.CompanyRelationshipType |
| GrantedBy | BIGINT | NO |  | FK→User |
| GrantedDate | DATETIME | NO | getutcdate() |  |
| ExpiryDate | DATETIME | YES |  |  |
| CreatedDate | DATETIME | NO | getutcdate() |  |
| CreatedBy | BIGINT | NO |  | FK→User |
| UpdatedDate | DATETIME | YES |  |  |
| UpdatedBy | BIGINT | YES |  | FK→User |
| IsDeleted | BIT | NO | 0 |  |

---

### Table: ref.FormAccessControlAccessType

**Columns (13):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| FormAccessControlAccessTypeID | INT | NO |  | PK |
| AccessTypeCode | VARCHAR(20) | NO |  |  |
| AccessTypeName | VARCHAR(50) | NO |  |  |
| AccessTypeDescription | VARCHAR(200) | YES |  |  |
| IsActive | BIT | NO | 1 |  |
| SortOrder | INT | NO | 0 |  |
| CreatedDate | DATETIME | NO | getutcdate() |  |
| CreatedBy | BIGINT | NO |  | FK→dbo.User |
| UpdatedDate | DATETIME | YES |  |  |
| UpdatedBy | BIGINT | YES |  | FK→dbo.User |
| IsDeleted | BIT | NO | 0 |  |
| DeletedDate | DATETIME | YES |  |  |
| DeletedBy | BIGINT | YES |  | FK→dbo.User |

---

### Table: ref.FormApprovalStatus

**Columns (14):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| FormApprovalStatusID | INT | NO |  | PK |
| ApprovalStatusCode | VARCHAR(20) | NO |  |  |
| ApprovalStatusName | VARCHAR(50) | NO |  |  |
| ApprovalStatusDescription | VARCHAR(200) | YES |  |  |
| IsRequiresApproval | BIT | NO | 0 |  |
| IsActive | BIT | NO | 1 |  |
| SortOrder | INT | NO | 0 |  |
| CreatedDate | DATETIME | NO | getutcdate() |  |
| CreatedBy | BIGINT | NO |  | FK→dbo.User |
| UpdatedDate | DATETIME | YES |  |  |
| UpdatedBy | BIGINT | YES |  | FK→dbo.User |
| IsDeleted | BIT | NO | 0 |  |
| DeletedDate | DATETIME | YES |  |  |
| DeletedBy | BIGINT | YES |  | FK→dbo.User |

---

### Table: ref.FormStatus

**Columns (15):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| FormStatusID | INT | NO |  | PK |
| StatusCode | VARCHAR(20) | NO |  |  |
| StatusName | VARCHAR(50) | NO |  |  |
| StatusDescription | VARCHAR(200) | YES |  |  |
| StatusColor | VARCHAR(7) | YES |  |  |
| StatusIcon | VARCHAR(50) | YES |  |  |
| IsActive | BIT | NO | 1 |  |
| SortOrder | INT | NO | 0 |  |
| CreatedDate | DATETIME | NO | getutcdate() |  |
| CreatedBy | BIGINT | NO |  | FK→dbo.User |
| UpdatedDate | DATETIME | YES |  |  |
| UpdatedBy | BIGINT | YES |  | FK→dbo.User |
| IsDeleted | BIT | NO | 0 |  |
| DeletedDate | DATETIME | YES |  |  |
| DeletedBy | BIGINT | YES |  | FK→dbo.User |

---

## Reference

### Table: ref.Country

**Columns (23):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| CountryID | BIGINT | NO |  | PK |
| CountryCode | NVARCHAR(2) | NO |  |  |
| CountryName | NVARCHAR(100) | NO |  |  |
| PhonePrefix | NVARCHAR(10) | NO |  |  |
| CurrencyCode | NVARCHAR(3) | NO |  |  |
| CurrencySymbol | NVARCHAR(5) | NO |  |  |
| CurrencyName | NVARCHAR(100) | NO |  |  |
| TaxRate | DECIMAL | YES |  |  |
| TaxName | NVARCHAR(50) | YES |  |  |
| TaxInclusive | BIT | NO | 0 |  |
| TaxNumberLabel | NVARCHAR(50) | YES |  |  |
| CompanyValidationProvider | NVARCHAR(50) | YES |  |  |
| AddressValidationProvider | NVARCHAR(50) | YES |  |  |
| IntegrationConfig | NVARCHAR(-1) | YES |  |  |
| IsActive | BIT | NO | 1 |  |
| SortOrder | INT | NO | 999 |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  |  |
| UpdatedDate | DATETIME2 | NO | getutcdate() |  |
| UpdatedBy | BIGINT | YES |  |  |
| IsDeleted | BIT | NO | 0 |  |
| DeletedDate | DATETIME2 | YES |  |  |
| DeletedBy | BIGINT | YES |  |  |

---

### Table: ref.CustomerTier

**Columns (15):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| CustomerTierID | BIGINT | NO |  | PK |
| TierCode | NVARCHAR(50) | NO |  |  |
| TierName | NVARCHAR(100) | NO |  |  |
| Description | NVARCHAR(500) | NO |  |  |
| MonthlyPrice | DECIMAL | YES |  |  |
| AnnualPrice | DECIMAL | YES |  |  |
| MaxUsers | INT | YES |  |  |
| MaxForms | INT | YES |  |  |
| MaxSubmissionsPerMonth | INT | YES |  |  |
| IsActive | BIT | NO | 1 |  |
| SortOrder | INT | NO | 0 |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  |  |
| UpdatedDate | DATETIME2 | YES |  |  |
| UpdatedBy | BIGINT | YES |  |  |

---

### Table: ref.FontSize

**Columns (12):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| FontSizeID | BIGINT | NO |  | PK |
| SizeCode | VARCHAR(20) | NO |  |  |
| SizeName | VARCHAR(50) | NO |  |  |
| Description | VARCHAR(200) | NO |  |  |
| CSSClass | VARCHAR(50) | NO |  |  |
| BaseFontSize | VARCHAR(10) | NO |  |  |
| IsActive | BIT | NO | 1 |  |
| SortOrder | INT | NO | 0 |  |
| CreatedDate | DATETIME | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  |  |
| UpdatedDate | DATETIME | YES |  |  |
| UpdatedBy | BIGINT | YES |  |  |

---

### Table: ref.Industry

**Columns (10):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| IndustryID | BIGINT | NO |  | PK |
| IndustryCode | NVARCHAR(50) | NO |  |  |
| IndustryName | NVARCHAR(100) | NO |  |  |
| Description | NVARCHAR(500) | NO |  |  |
| IsActive | BIT | NO | 1 |  |
| SortOrder | INT | NO | 0 |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  |  |
| UpdatedDate | DATETIME2 | YES |  |  |
| UpdatedBy | BIGINT | YES |  |  |

---

### Table: ref.JoinedVia

**Columns (10):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| JoinedViaID | BIGINT | NO |  | PK |
| MethodCode | NVARCHAR(20) | NO |  |  |
| MethodName | NVARCHAR(50) | NO |  |  |
| Description | NVARCHAR(500) | NO |  |  |
| IsActive | BIT | NO | 1 |  |
| SortOrder | INT | NO | 0 |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  |  |
| UpdatedDate | DATETIME2 | YES |  |  |
| UpdatedBy | BIGINT | YES |  |  |

---

### Table: ref.Language

**Columns (12):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| LanguageID | BIGINT | NO |  | PK |
| LanguageCode | NVARCHAR(5) | NO |  |  |
| LanguageName | NVARCHAR(100) | NO |  |  |
| IsActive | BIT | NO | 1 |  |
| SortOrder | INT | NO | 999 |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  |  |
| UpdatedDate | DATETIME2 | NO | getutcdate() |  |
| UpdatedBy | BIGINT | YES |  |  |
| IsDeleted | BIT | NO | 0 |  |
| DeletedDate | DATETIME2 | YES |  |  |
| DeletedBy | BIGINT | YES |  |  |

---

### Table: ref.LayoutDensity

**Columns (11):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| LayoutDensityID | BIGINT | NO |  | PK |
| DensityCode | VARCHAR(20) | NO |  |  |
| DensityName | VARCHAR(50) | NO |  |  |
| Description | VARCHAR(200) | NO |  |  |
| CSSClass | VARCHAR(50) | NO |  |  |
| IsActive | BIT | NO | 1 |  |
| SortOrder | INT | NO | 0 |  |
| CreatedDate | DATETIME | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  |  |
| UpdatedDate | DATETIME | YES |  |  |
| UpdatedBy | BIGINT | YES |  |  |

---

### Table: ref.PublicReviewStatus

**Columns (15):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| PublicReviewStatusID | BIGINT | NO |  | PK |
| StatusCode | NVARCHAR(20) | NO |  |  |
| StatusName | NVARCHAR(50) | NO |  |  |
| StatusDescription | NVARCHAR(200) | YES |  |  |
| StatusColor | NVARCHAR(7) | YES |  |  |
| StatusIcon | NVARCHAR(50) | YES |  |  |
| IsActive | BIT | NO | '1' |  |
| SortOrder | INT | NO | '0' |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  | FK→dbo.User |
| UpdatedDate | DATETIME2 | YES |  |  |
| UpdatedBy | BIGINT | YES |  | FK→dbo.User |
| IsDeleted | BIT | NO | '0' |  |
| DeletedDate | DATETIME2 | YES |  |  |
| DeletedBy | BIGINT | YES |  | FK→dbo.User |

---

### Table: ref.RecurrencePattern

**Columns (14):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| RecurrencePatternID | INT | NO |  | PK |
| PatternCode | VARCHAR(20) | NO |  |  |
| PatternName | VARCHAR(50) | NO |  |  |
| PatternDescription | VARCHAR(200) | YES |  |  |
| PatternFormula | VARCHAR(100) | YES |  |  |
| IsActive | BIT | NO | 1 |  |
| SortOrder | INT | NO | 0 |  |
| CreatedDate | DATETIME | NO | getutcdate() |  |
| CreatedBy | BIGINT | NO |  | FK→dbo.User |
| UpdatedDate | DATETIME | YES |  |  |
| UpdatedBy | BIGINT | YES |  | FK→dbo.User |
| IsDeleted | BIT | NO | 0 |  |
| DeletedDate | DATETIME | YES |  |  |
| DeletedBy | BIGINT | YES |  | FK→dbo.User |

---

### Table: ref.RuleType

**Columns (10):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| RuleTypeID | BIGINT | NO |  | PK |
| TypeCode | NVARCHAR(50) | NO |  |  |
| TypeName | NVARCHAR(100) | NO |  |  |
| Description | NVARCHAR(500) | NO |  |  |
| IsActive | BIT | NO | 1 |  |
| SortOrder | INT | NO | 0 |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  |  |
| UpdatedDate | DATETIME2 | YES |  |  |
| UpdatedBy | BIGINT | YES |  |  |

---

### Table: ref.SettingCategory

**Columns (10):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| SettingCategoryID | BIGINT | NO |  | PK |
| CategoryCode | NVARCHAR(50) | NO |  |  |
| CategoryName | NVARCHAR(100) | NO |  |  |
| Description | NVARCHAR(500) | NO |  |  |
| IsActive | BIT | NO | 1 |  |
| SortOrder | INT | NO | 0 |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  |  |
| UpdatedDate | DATETIME2 | YES |  |  |
| UpdatedBy | BIGINT | YES |  |  |

---

### Table: ref.SettingType

**Columns (11):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| SettingTypeID | BIGINT | NO |  | PK |
| TypeCode | NVARCHAR(20) | NO |  |  |
| TypeName | NVARCHAR(50) | NO |  |  |
| Description | NVARCHAR(500) | NO |  |  |
| ValidationPattern | NVARCHAR(200) | YES |  |  |
| IsActive | BIT | NO | 1 |  |
| SortOrder | INT | NO | 0 |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  |  |
| UpdatedDate | DATETIME2 | YES |  |  |
| UpdatedBy | BIGINT | YES |  |  |

---

### Table: ref.ThemePreference

**Columns (11):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| ThemePreferenceID | BIGINT | NO |  | PK |
| ThemeCode | VARCHAR(20) | NO |  |  |
| ThemeName | VARCHAR(50) | NO |  |  |
| Description | VARCHAR(200) | NO |  |  |
| CSSClass | VARCHAR(50) | NO |  |  |
| IsActive | BIT | NO | 1 |  |
| SortOrder | INT | NO | 0 |  |
| CreatedDate | DATETIME | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  |  |
| UpdatedDate | DATETIME | YES |  |  |
| UpdatedBy | BIGINT | YES |  |  |

---

## Config

### Table: config.AppSetting

**Columns (20):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| AppSettingID | BIGINT | NO |  | PK |
| SettingKey | NVARCHAR(100) | NO |  |  |
| SettingValue | NVARCHAR(-1) | NO |  |  |
| SettingCategoryID | BIGINT | NO |  | FK→ref.SettingCategory |
| SettingTypeID | BIGINT | NO |  | FK→ref.SettingType |
| Description | NVARCHAR(500) | NO |  |  |
| DefaultValue | NVARCHAR(-1) | NO |  |  |
| IsEditable | BIT | NO | 1 |  |
| ValidationRegex | NVARCHAR(500) | YES |  |  |
| MinValue | DECIMAL | YES |  |  |
| MaxValue | DECIMAL | YES |  |  |
| IsActive | BIT | NO | 1 |  |
| SortOrder | INT | NO | 999 |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  |  |
| UpdatedDate | DATETIME2 | NO | getutcdate() |  |
| UpdatedBy | BIGINT | YES |  |  |
| IsDeleted | BIT | NO | 0 |  |
| DeletedDate | DATETIME2 | YES |  |  |
| DeletedBy | BIGINT | YES |  |  |

---

### Table: config.ValidationRule

**Columns (24):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| ValidationRuleID | BIGINT | NO |  | PK |
| RuleKey | NVARCHAR(100) | NO |  |  |
| RuleTypeID | BIGINT | NO |  | FK→ref.RuleType |
| CountryID | BIGINT | YES |  | FK→ref.Country |
| ValidationPattern | NVARCHAR(500) | NO |  |  |
| ValidationMessage | NVARCHAR(500) | NO |  |  |
| Description | NVARCHAR(500) | NO |  |  |
| IsActive | BIT | NO | 1 |  |
| Priority | INT | NO | 0 |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  |  |
| UpdatedDate | DATETIME2 | NO | getutcdate() |  |
| UpdatedBy | BIGINT | YES |  |  |
| IsDeleted | BIT | NO | 0 |  |
| DeletedDate | DATETIME2 | YES |  |  |
| DeletedBy | BIGINT | YES |  |  |
| MinLength | INT | YES |  |  |
| MaxLength | INT | YES |  |  |
| ExampleValue | VARCHAR(100) | YES |  |  |
| SortOrder | INT | NO |  |  |
| DisplayFormat | NVARCHAR(100) | YES |  |  |
| DisplayExample | NVARCHAR(100) | YES |  |  |
| StripPrefix | BIT | NO | 0 |  |
| SpacingPattern | NVARCHAR(50) | YES |  |  |

---

## Audit

### Table: audit.ActivityLog

**Columns (13):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| ActivityLogID | BIGINT | NO |  | PK |
| UserID | BIGINT | YES |  | FK→dbo.User |
| UserEmail | NVARCHAR(255) | YES |  |  |
| Action | NVARCHAR(100) | NO |  |  |
| EntityType | NVARCHAR(50) | NO |  |  |
| EntityID | BIGINT | YES |  |  |
| CompanyID | BIGINT | YES |  | FK→dbo.Company |
| OldValue | NVARCHAR(-1) | YES |  |  |
| NewValue | NVARCHAR(-1) | YES |  |  |
| IPAddress | NVARCHAR(50) | YES |  |  |
| UserAgent | NVARCHAR(500) | YES |  |  |
| RequestID | NVARCHAR(100) | YES |  |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |

---

### Table: audit.ApprovalAuditTrail

**Columns (10):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| ApprovalAuditTrailID | BIGINT | NO |  | PK |
| CompanySwitchRequestID | BIGINT | NO |  | FK→dbo.CompanySwitchRequest |
| Action | VARCHAR(50) | NO |  |  |
| ActionDate | DATETIME | NO | getutcdate() |  |
| PerformedBy | BIGINT | NO |  | FK→dbo.User |
| Comments | VARCHAR(-1) | YES |  |  |
| PreviousStatus | VARCHAR(20) | YES |  |  |
| NewStatus | VARCHAR(20) | YES |  |  |
| CreatedDate | DATETIME | NO | getutcdate() |  |
| CreatedBy | BIGINT | NO |  | FK→dbo.User |

---

## Log

### Table: log.ApiRequest

**Columns (15):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| ApiRequestID | BIGINT | NO |  | PK |
| RequestID | NVARCHAR(100) | NO |  |  |
| Method | NVARCHAR(10) | NO |  |  |
| Path | NVARCHAR(500) | NO |  |  |
| QueryParams | NVARCHAR(-1) | YES |  |  |
| StatusCode | INT | NO |  |  |
| DurationMs | INT | NO |  |  |
| UserID | BIGINT | YES |  | FK→dbo.User |
| CompanyID | BIGINT | YES |  | FK→dbo.Company |
| IPAddress | NVARCHAR(50) | YES |  |  |
| UserAgent | NVARCHAR(500) | YES |  |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| RequestPayload | NVARCHAR(-1) | YES |  |  |
| ResponsePayload | NVARCHAR(-1) | YES |  |  |
| Headers | NVARCHAR(-1) | YES |  |  |

---

### Table: log.ApplicationError

**Columns (15):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| ApplicationErrorID | BIGINT | NO |  | PK |
| ErrorType | NVARCHAR(100) | NO |  |  |
| ErrorMessage | NVARCHAR(-1) | NO |  |  |
| StackTrace | NVARCHAR(-1) | YES |  |  |
| Severity | NVARCHAR(20) | NO |  |  |
| RequestID | NVARCHAR(100) | YES |  |  |
| Path | NVARCHAR(500) | YES |  |  |
| Method | NVARCHAR(10) | YES |  |  |
| UserID | BIGINT | YES |  | FK→dbo.User |
| CompanyID | BIGINT | YES |  | FK→dbo.Company |
| IPAddress | NVARCHAR(50) | YES |  |  |
| UserAgent | NVARCHAR(500) | YES |  |  |
| AdditionalData | NVARCHAR(-1) | YES |  |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| ExceptionType | NVARCHAR(100) | YES |  |  |

---

### Table: log.AuthEvent

**Columns (10):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| AuthEventID | BIGINT | NO |  | PK |
| EventType | NVARCHAR(50) | NO |  |  |
| UserID | BIGINT | YES |  | FK→dbo.User |
| Email | NVARCHAR(255) | YES |  |  |
| Reason | NVARCHAR(255) | YES |  |  |
| IPAddress | NVARCHAR(50) | YES |  |  |
| UserAgent | NVARCHAR(500) | YES |  |  |
| RequestID | NVARCHAR(100) | YES |  |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| SessionID | NVARCHAR(100) | YES |  |  |

---

### Table: log.EmailDelivery

**Columns (16):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| EmailDeliveryID | BIGINT | NO |  | PK |
| EmailType | NVARCHAR(50) | NO |  |  |
| RecipientEmail | NVARCHAR(255) | NO |  |  |
| Subject | NVARCHAR(255) | NO |  |  |
| Status | NVARCHAR(50) | NO |  |  |
| ProviderMessageID | NVARCHAR(255) | YES |  |  |
| ErrorMessage | NVARCHAR(-1) | YES |  |  |
| SentAt | DATETIME2 | YES |  |  |
| DeliveredAt | DATETIME2 | YES |  |  |
| OpenedAt | DATETIME2 | YES |  |  |
| ClickedAt | DATETIME2 | YES |  |  |
| UserID | BIGINT | YES |  | FK→dbo.User |
| CompanyID | BIGINT | YES |  | FK→dbo.Company |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| ProviderResponse | NVARCHAR(-1) | YES |  |  |
| RetryCount | INT | NO | '0' |  |

---

### Table: log.IntegrationEvent

**Columns (9):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| IntegrationEventID | BIGINT | NO |  | PK |
| EventType | NVARCHAR(100) | NO |  |  |
| SourceDomain | NVARCHAR(50) | NO |  |  |
| TargetDomain | NVARCHAR(50) | NO |  |  |
| EntityID | BIGINT | YES |  |  |
| Details | NVARCHAR(-1) | YES |  |  |
| UserID | BIGINT | YES |  | FK→dbo.User |
| RequestID | NVARCHAR(100) | YES |  |  |
| CreatedDate | DATETIME | NO | getutcdate() |  |

---

### Table: log.PerformanceMetric

**Columns (8):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| PerformanceMetricID | BIGINT | NO |  | PK |
| MetricType | NVARCHAR(50) | NO |  |  |
| Endpoint | NVARCHAR(500) | YES |  |  |
| Value | NUMERIC | NO |  |  |
| StatusCode | INT | YES |  |  |
| UserID | BIGINT | YES |  | FK→dbo.User |
| Details | NVARCHAR(-1) | YES |  |  |
| CreatedDate | DATETIME | NO | getutcdate() |  |

---

## Cache

### Table: cache.ABRSearch

**Columns (20):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| SearchType | NVARCHAR(10) | NO |  | PK |
| SearchValue | NVARCHAR(255) | NO |  | PK |
| ResultIndex | INT | NO | 0 | PK |
| ABN | NVARCHAR(11) | YES |  |  |
| LegalEntityName | NVARCHAR(255) | YES |  |  |
| EntityType | NVARCHAR(100) | YES |  |  |
| ABNStatus | NVARCHAR(20) | YES |  |  |
| GSTRegistered | BIT | YES |  |  |
| FullResponse | NVARCHAR(-1) | NO |  |  |
| SearchDate | DATETIME2 | NO | getutcdate() |  |
| ExpiresAt | DATETIME2 | NO |  |  |
| IsDeleted | BIT | NO | 0 |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| CreatedBy | BIGINT | YES |  | FK→dbo.User |
| UpdatedDate | DATETIME2 | YES |  |  |
| UpdatedBy | BIGINT | YES |  | FK→dbo.User |
| CompanyID | BIGINT | YES |  | FK→dbo.Company |
| UserID | BIGINT | YES |  | FK→dbo.User |
| HitCount | INT | NO | '0' |  |
| LastHitAt | DATETIME | YES |  |  |

---

## System

### Table: dbo.alembic_version

**Columns (1):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| version_num | VARCHAR(32) | NO |  | PK |

---

## Other

### Table: audit.Role

**Columns (19):**

| Column Name | Data Type | Nullable | Default | Notes |
|------------|-----------|----------|---------|-------|
| AuditRoleID | BIGINT | NO |  | PK |
| TableName | NVARCHAR(50) | NO |  |  |
| RecordID | BIGINT | NO |  |  |
| ColumnName | NVARCHAR(50) | NO |  |  |
| RoleType | NVARCHAR(50) | NO |  |  |
| UserCompanyID | BIGINT | YES |  | FK→dbo.UserCompany |
| UserID | BIGINT | NO |  | FK→dbo.User |
| CompanyID | BIGINT | YES |  | FK→dbo.Company |
| OldRoleID | BIGINT | YES |  |  |
| NewRoleID | BIGINT | YES |  |  |
| OldRoleName | NVARCHAR(100) | YES |  |  |
| NewRoleName | NVARCHAR(100) | YES |  |  |
| ChangeReason | NVARCHAR(500) | YES |  |  |
| ChangedBy | BIGINT | YES |  | FK→dbo.User |
| ChangedByEmail | NVARCHAR(255) | YES |  |  |
| IPAddress | NVARCHAR(50) | YES |  |  |
| UserAgent | NVARCHAR(500) | YES |  |  |
| CreatedDate | DATETIME2 | NO | getutcdate() |  |
| IsDeleted | BIT | NO | 0 |  |

---

## Stored Procedures

### Procedure: dbo.sp_TransferFormOwnership

**Purpose:** Bulk transfer form ownership from one user to another (for user off-boarding scenarios)

**Parameters:**

| Parameter | Data Type | Nullable | Description |
|-----------|-----------|----------|-------------|
| @FromUserID | BIGINT | NO | User ID to transfer ownership FROM (off-boarding user) |
| @ToUserID | BIGINT | NO | User ID to transfer ownership TO (new owner) |
| @CompanyID | BIGINT | NO | Company ID (must match company of both users) |
| @PerformedBy | BIGINT | NO | User ID performing the transfer (must be Company Admin or System Admin) |
| @Reason | NVARCHAR(500) | YES | Optional reason for transfer (e.g., "Bulk ownership transfer on offboarding") |

**Returns:**
- `FormsTransferred` (INT) - Number of forms transferred
- `AccessControlsTransferred` (INT) - Number of access control entries transferred
- `Status` (VARCHAR) - 'SUCCESS' or error status
- `Message` (NVARCHAR) - Status message

**Behavior:**
- Validates that `@PerformedBy` has Company Admin privileges for `@CompanyID` OR is System Admin
- Updates `Form.CreatedBy` from `@FromUserID` to `@ToUserID` for all forms in the company
- Updates `FormAccessControl.UserID` from `@FromUserID` to `@ToUserID` for all access control entries
- Inserts audit records into `audit.ActivityLog` for each transferred form
- Transaction-safe with rollback on error

---

## Functions

### Function: dbo.fn_GetUserFormAccess

**Purpose:** Centralized table-valued function that determines a user's effective access to a form

**Parameters:**

| Parameter | Data Type | Description |
|-----------|-----------|-------------|
| @UserID | BIGINT | User ID to check access for |
| @FormID | BIGINT | Form ID to check access for |

**Returns (Table):**

| Column | Data Type | Description |
|--------|-----------|-------------|
| UserID | BIGINT | User ID (input parameter) |
| FormID | BIGINT | Form ID (input parameter) |
| EffectiveAccessTypeID | INT | Effective access type ID (from ref.FormAccessControlAccessType) |
| EffectiveAccessTypeCode | VARCHAR(20) | Effective access type code ('MANAGE', 'EDIT', 'ANALYZE', 'SUBMIT', 'VIEW', or NULL) |
| CanView | BIT | Can user view the form? |
| CanSubmit | BIT | Can user submit responses? |
| CanAnalyze | BIT | Can user view analytics? |
| CanEdit | BIT | Can user edit the form? |
| CanManage | BIT | Can user manage the form (delete, grant access)? |
| AccessSource | VARCHAR(50) | Source of access ('system_admin', 'ownership', 'explicit_acl', 'agency_event', 'company_role', 'none') |
| AccessReason | NVARCHAR(500) | Human-readable explanation of access source |

**Access Check Priority:**
1. System Admin Override → MANAGE
2. Resource Ownership → MANAGE (form creator)
3. Explicit FormAccessControl → Use specified access type
4. Agency Event-Scoped Access → VIEW/EDIT all forms for event (if `agency_form_builder` role)
5. Company Role Default → Default based on company role
6. No Access → NULL (requires explicit FormAccessControl entry)

---
