# Database Rebuild Plan Updates - October 16, 2025

## 📋 CHANGES IMPLEMENTED (Based on Anthony's Feedback)

### **Summary of Changes:**
Anthony reviewed the rebuild plan and requested proper normalization for enum-like fields (consistent with UserStatus/UserInvitationStatus), hierarchical table naming for token tables, and constraint fixes for the audit.Role table.

---

## 🆕 NEW REFERENCE TABLES (6 new tables)

### **1. `ref.UserCompanyStatus` (3 statuses)**
Replaces string field `UserCompany.Status` with FK to normalized table.

**Purpose:** Track user-company relationship status (active, suspended, removed)

**Fields:**
- `StatusCode`: 'active', 'suspended', 'removed'
- `AllowAccess`: Boolean flag for access control logic
- Standard audit fields

**Seed Data:**
- Active (AllowAccess=1)
- Suspended (AllowAccess=0)
- Removed (AllowAccess=0)

---

### **2. `ref.SettingCategory` (5 categories)**
Replaces string field `config.AppSetting.SettingCategory` with FK.

**Purpose:** Categorize application settings for better organization

**Fields:**
- `CategoryCode`: 'authentication', 'validation', 'email', 'security', 'invitation'
- `CategoryName`: Display name
- Standard audit fields

**Seed Data:**
- Authentication (JWT, password rules)
- Validation (token expiry rules)
- Email (SMTP configuration)
- Security (lockout policies)
- Invitation (team invitation rules)

---

### **3. `ref.SettingType` (5 types)**
Replaces string field `config.AppSetting.SettingType` with FK.

**Purpose:** Define data types for settings with optional validation patterns

**Fields:**
- `TypeCode`: 'integer', 'boolean', 'string', 'json', 'decimal'
- `ValidationPattern`: Regex for validation (e.g., `^[0-9]+$` for integers)
- Standard audit fields

**Seed Data:**
- Integer (with regex: `^[0-9]+$`)
- Boolean (with regex: `^(true|false)$`)
- String (no regex)
- JSON (no regex)
- Decimal (with regex: `^[0-9]+(\.[0-9]+)?$`)

---

### **4. `ref.RuleType` (5 types)**
Replaces string field `config.ValidationRule.RuleType` with FK.

**Purpose:** Define types of validation rules (phone, postal_code, tax_id, etc.)

**Fields:**
- `TypeCode`: 'phone', 'postal_code', 'tax_id', 'email', 'address'
- `TypeName`: Display name
- Standard audit fields

**Seed Data:**
- Phone Number
- Postal Code
- Tax ID (ABN, VAT, EIN)
- Email
- Address

---

### **5. `ref.CustomerTier` (3 tiers)**
Replaces string field `CompanyCustomerDetails.CustomerTier` with FK.

**Purpose:** Define subscription tiers with pricing and feature limits

**Fields:**
- `TierCode`: 'free', 'pro', 'enterprise'
- `MonthlyPrice`: DECIMAL(10,2) in AUD
- `MaxUsers`, `MaxEvents`, `MaxFormsPerEvent`: INT (NULL = unlimited)
- `FeatureAccess`: JSON (list of enabled features)
- Standard audit fields

**Seed Data:**
- Free: $0/month, 3 users, 5 forms per event
- Pro: $49/month, 10 users, unlimited forms
- Enterprise: $299/month, unlimited everything + whitelabel

---

### **6. `ref.JoinedVia` (3 methods)**
Replaces string field `UserCompany.JoinedVia` with FK.

**Purpose:** Track how user joined company for audit trail

**Fields:**
- `JoinedViaCode`: 'signup', 'invitation', 'transfer'
- `JoinedViaName`: Display name
- Standard audit fields

**Seed Data:**
- Signup (user created the company)
- Invitation (invited by another user)
- Transfer (admin action)

---

## ✏️ TABLE RENAMES (Hierarchical Naming)

### **1. `EmailVerificationToken` → `UserEmailVerificationToken`**
- Primary key: `UserEmailVerificationTokenID`
- FK constraint: `FK_UserEmailVerificationToken_User`
- Indexes: `IX_UserEmailVerificationToken_User`, `IX_UserEmailVerificationToken_ExpiresAt`, `IX_UserEmailVerificationToken_Token`

**Rationale:** Hierarchical naming makes it clear this is user-specific (not company or event verification).

---

### **2. `PasswordResetToken` → `UserPasswordResetToken`**
- Primary key: `UserPasswordResetTokenID`
- FK constraint: `FK_UserPasswordResetToken_User`
- Indexes: `IX_UserPasswordResetToken_User`, `IX_UserPasswordResetToken_ExpiresAt`, `IX_UserPasswordResetToken_Token`

**Rationale:** Consistency with `UserEmailVerificationToken` and hierarchical structure.

---

### **3. `InvitationStatus` → `UserInvitationStatus` (Already Renamed)**
- Already correct in rebuild plan ✅
- Added metadata fields: `CanResend`, `CanCancel`, `IsFinalState`

---

## 🔧 CONSTRAINT FIXES

### **1. `audit.Role` - Allow NULL for System Role Audits**

**Problem:** Original design had `UserCompanyID NOT NULL` and `CompanyID NOT NULL`, which prevented auditing User table system roles (User.UserRoleID).

**Solution:**
- Changed `UserCompanyID` to NULLABLE
- Changed `CompanyID` to NULLABLE
- Added `RoleType` field: 'system' or 'company'
- Added CHECK constraint to enforce:
  - If `RoleType = 'system'`: UserCompanyID and CompanyID must be NULL
  - If `RoleType = 'company'`: UserCompanyID and CompanyID must NOT be NULL

**Example:**
```sql
-- System role change (User.UserRoleID)
INSERT INTO [audit].[Role] 
(UserID, RoleType, OldRoleID, NewRoleID, ChangeType) VALUES
(123, 'system', NULL, 1, 'role_assigned');
-- UserCompanyID and CompanyID are NULL ✅

-- Company role change (UserCompany.UserCompanyRoleID)
INSERT INTO [audit].[Role] 
(UserID, UserCompanyID, CompanyID, RoleType, OldRoleID, NewRoleID, ChangeType) VALUES
(123, 456, 789, 'company', 2, 3, 'role_changed');
-- UserCompanyID and CompanyID are populated ✅
```

---

## 🔄 SCHEMA UPDATES

### **1. `config.AppSetting`**
**Before:**
```sql
SettingCategory NVARCHAR(50) NOT NULL,  -- 'authentication', 'validation'
SettingType NVARCHAR(20) NOT NULL,      -- 'integer', 'boolean'
```

**After:**
```sql
SettingCategoryID BIGINT NOT NULL,      -- FK to ref.SettingCategory
SettingTypeID BIGINT NOT NULL,          -- FK to ref.SettingType

CONSTRAINT FK_AppSetting_Category FOREIGN KEY (SettingCategoryID) 
    REFERENCES [ref].[SettingCategory](SettingCategoryID),
CONSTRAINT FK_AppSetting_Type FOREIGN KEY (SettingTypeID) 
    REFERENCES [ref].[SettingType](SettingTypeID)
```

**Indexes Added:**
- `IX_AppSetting_Category` (on SettingCategoryID)
- `IX_AppSetting_Type` (on SettingTypeID)

---

### **2. `config.ValidationRule`**
**Before:**
```sql
RuleType NVARCHAR(50) NOT NULL,  -- 'phone', 'postal_code', 'tax_id'
```

**After:**
```sql
RuleTypeID BIGINT NOT NULL,      -- FK to ref.RuleType

CONSTRAINT FK_ValidationRule_RuleType FOREIGN KEY (RuleTypeID) 
    REFERENCES [ref].[RuleType](RuleTypeID)
```

**Indexes Added:**
- `IX_ValidationRule_Country_RuleType` (composite)
- `IX_ValidationRule_RuleType`

---

### **3. `dbo.CompanyCustomerDetails`**
**Before:**
```sql
CustomerTier NVARCHAR(50) NOT NULL DEFAULT 'Free',  -- 'Free', 'Pro', 'Enterprise'
```

**After:**
```sql
CustomerTierID BIGINT NOT NULL,  -- FK to ref.CustomerTier

CONSTRAINT FK_CompanyCustomerDetails_Tier FOREIGN KEY (CustomerTierID) 
    REFERENCES [ref].[CustomerTier](CustomerTierID)
```

**Indexes Added:**
- `IX_CompanyCustomerDetails_Tier`

---

### **4. `dbo.UserCompany`**
**Before:**
```sql
Status NVARCHAR(20) NOT NULL DEFAULT 'active',  -- 'active', 'suspended', 'removed'
JoinedVia NVARCHAR(20) NOT NULL,                -- 'signup', 'invitation', 'transfer'
```

**After:**
```sql
StatusID BIGINT NOT NULL,        -- FK to ref.UserCompanyStatus
JoinedViaID BIGINT NOT NULL,     -- FK to ref.JoinedVia

CONSTRAINT FK_UserCompany_Status FOREIGN KEY (StatusID) 
    REFERENCES [ref].[UserCompanyStatus](UserCompanyStatusID),
CONSTRAINT FK_UserCompany_JoinedVia FOREIGN KEY (JoinedViaID) 
    REFERENCES [ref].[JoinedVia](JoinedViaID)
```

**Indexes Added:**
- `IX_UserCompany_Status`
- `IX_UserCompany_JoinedVia`
- Updated composite indexes to use StatusID instead of Status

---

### **5. `dbo.UserInvitation`**
**Before:**
```sql
CONSTRAINT FK_UserInvitation_Status FOREIGN KEY (StatusID) 
    REFERENCES [ref].[InvitationStatus](InvitationStatusID)
```

**After:**
```sql
CONSTRAINT FK_UserInvitation_Status FOREIGN KEY (StatusID) 
    REFERENCES [ref].[UserInvitationStatus](UserInvitationStatusID)
```

---

## 📊 SEED DATA UPDATES

### **1. AppSetting Seed Data (Updated)**
Now uses subqueries to reference normalized tables:

```sql
INSERT INTO [config].[AppSetting] 
(SettingKey, SettingValue, SettingCategoryID, SettingTypeID, DefaultValue, Description, SortOrder) 
VALUES
('jwt_access_token_expiry_minutes', '15', 
    (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode = 'authentication'), 
    (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode = 'integer'), 
    '15', 'JWT access token expiry in minutes', 10);
-- ... etc
```

---

### **2. ValidationRule Seed Data (Updated)**
Now uses subquery for RuleTypeID:

```sql
INSERT INTO [config].[ValidationRule] 
(CountryID, RuleTypeID, RuleName, ValidationPattern, ErrorMessage, MinLength, MaxLength, ExampleValue, SortOrder) 
VALUES
(1, (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode = 'phone'), 
    'Australian Mobile', '^\+61[4-5][0-9]{8}$', 
    'Mobile phone must be +61 followed by 4 or 5 and 8 digits', 12, 12, '+61412345678', 10);
-- ... etc
```

---

## 📈 UPDATED STATISTICS

### **Before Changes:**
- **39 tables** across 6 schemas
- **8 reference tables**

### **After Changes:**
- **45 tables** across 6 schemas (+6 tables)
- **14 reference tables** (+6 reference tables)

### **New Reference Table Breakdown:**
1. Country
2. Language
3. Industry
4. UserStatus
5. UserInvitationStatus ✅ (renamed)
6. UserRole
7. UserCompanyRole
8. UserCompanyStatus ✅ **NEW**
9. AuditRole
10. SettingCategory ✅ **NEW**
11. SettingType ✅ **NEW**
12. RuleType ✅ **NEW**
13. CustomerTier ✅ **NEW**
14. JoinedVia ✅ **NEW**

---

## ✅ COMPLIANCE WITH ANTHONY'S STANDARDS

### **1. Consistent Normalization**
✅ All enum-like fields now use reference tables (consistent with UserStatus approach)

### **2. Hierarchical Naming**
✅ Token tables renamed to `UserEmailVerificationToken` and `UserPasswordResetToken`

### **3. Flexible Audit Trail**
✅ `audit.Role` now supports both system roles (User.UserRoleID) and company roles (UserCompany.UserCompanyRoleID)

### **4. Foreign Key Integrity**
✅ All enum-like fields now have proper FK constraints and indexes

### **5. Seed Data Completeness**
✅ All 6 new reference tables have complete seed data with descriptions

---

## 🚀 BENEFITS OF THESE CHANGES

### **1. Better Data Integrity**
- Can't insert invalid values (FK constraints enforce valid references)
- Centralized lookup data (one source of truth)

### **2. Easier Maintenance**
- Add new tiers/statuses/types without schema changes
- Update display names without code changes
- Add metadata fields (e.g., `CanResend`, `AllowAccess`) for business logic

### **3. Better Queries**
```sql
-- Before (string comparison)
SELECT * FROM UserCompany WHERE Status = 'active';  -- Typo: 'actuve' would return 0 rows

-- After (FK with JOIN for clarity)
SELECT uc.*, s.StatusName, s.AllowAccess
FROM UserCompany uc
INNER JOIN ref.UserCompanyStatus s ON s.UserCompanyStatusID = uc.StatusID
WHERE s.StatusCode = 'active';  -- Invalid StatusCode would fail INSERT, not query
```

### **4. Consistent with Existing Pattern**
- Already had `ref.UserStatus` and `ref.UserInvitationStatus`
- Now all similar fields follow same pattern
- Reduces cognitive load for developers

---

## 📋 FINAL CHECKLIST

- [x] Create 6 new reference tables with full definitions
- [x] Add seed data for all 6 new reference tables
- [x] Rename `EmailVerificationToken` → `UserEmailVerificationToken`
- [x] Rename `PasswordResetToken` → `UserPasswordResetToken`
- [x] Fix `audit.Role` constraints to allow NULL for system role audits
- [x] Update `config.AppSetting` to use FKs (SettingCategoryID, SettingTypeID)
- [x] Update `config.ValidationRule` to use FK (RuleTypeID)
- [x] Update `dbo.CompanyCustomerDetails` to use FK (CustomerTierID)
- [x] Update `dbo.UserCompany` to use FKs (StatusID, JoinedViaID)
- [x] Update `dbo.UserInvitation` FK to `ref.UserInvitationStatus`
- [x] Update AppSetting seed data to use subqueries
- [x] Update ValidationRule seed data to use subqueries
- [x] Update indexes for new FK columns
- [x] Update summary section with new table counts
- [x] No linter errors ✅

---

## 📄 NEXT STEPS

**The rebuild plan is now ready for final review:**
- Review: `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md`
- Total: **45 tables** across **6 schemas**
- Reference tables: **14 tables** (all with seed data)
- All enum-like fields normalized consistently ✅

**Once approved:**
1. Create Alembic migration file (single migration for all 45 tables)
2. Create PowerShell automation script (drop/create database, run migration, verify)
3. Create SQL verification script (check table counts, FK integrity, seed data)

---

**Solomon** 📜  
*"Consistency in normalization. Clarity in naming. Precision in constraints."*

