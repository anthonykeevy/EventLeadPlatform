# Epic 1 Seed Data Reference

**Purpose:** Reference guide for populating Epic 1 reference tables

**Execution:** Manual INSERT or via Alembic migration data operations

---

## Overview

Total reference tables requiring seed data: **14 tables**

**Priority Order:**
1. Foundation (Country, Language, Industry) - No dependencies
2. User/Auth (UserStatus, UserInvitationStatus, UserRole, UserCompanyRole, UserCompanyStatus)
3. Configuration (SettingCategory, SettingType, RuleType, CustomerTier, JoinedVia)

---

## 1. `ref.Country` - Australia Only (MVP)

```sql
INSERT INTO [ref].[Country] (CountryCode, CountryName, PhonePrefix, CurrencyCode, CurrencySymbol, CurrencyName, TaxRate, TaxName, TaxInclusive, TaxNumberLabel, CompanyValidationProvider, AddressValidationProvider, IntegrationConfig, IsActive)
VALUES (
    'AU', 
    'Australia', 
    '+61', 
    'AUD', 
    '$', 
    'Australian Dollar', 
    0.10, 
    'GST', 
    0, 
    'ABN',
    'ABR',
    'Geoscape',
    '{"abrApiUrl": "https://abr.business.gov.au/json/", "geoscapeApiUrl": "https://api.geoscape.com.au/"}',
    1
);
```

---

## 2. `ref.Language` - English Only (MVP)

```sql
INSERT INTO [ref].[Language] (LanguageCode, LanguageName, IsActive)
VALUES ('en', 'English', 1);
```

---

## 3. `ref.Industry` - Common Industries (MVP)

```sql
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
```

---

## 4. `ref.UserStatus` - User Account States

```sql
INSERT INTO [ref].[UserStatus] (StatusCode, StatusName, Description, AllowLogin, IsActive, SortOrder) VALUES
('pending', 'Pending Verification', 'User has signed up but not verified email address', 0, 1, 10),
('active', 'Active', 'User account is active and in good standing', 1, 1, 20),
('suspended', 'Suspended', 'User account temporarily disabled by admin', 0, 1, 30),
('locked', 'Locked', 'Account locked due to failed login attempts', 0, 1, 40);
```

---

## 5. `ref.UserInvitationStatus` - Invitation Lifecycle

```sql
INSERT INTO [ref].[UserInvitationStatus] (StatusCode, StatusName, Description, CanResend, CanCancel, IsFinalState, IsActive, SortOrder) VALUES
('pending', 'Pending', 'Invitation sent, awaiting response', 1, 1, 0, 1, 10),
('accepted', 'Accepted', 'User accepted invitation and joined team', 0, 0, 1, 1, 20),
('declined', 'Declined', 'User declined invitation', 0, 0, 1, 1, 30),
('expired', 'Expired', 'Invitation expired (7-day TTL)', 0, 0, 1, 1, 40),
('cancelled', 'Cancelled', 'Admin cancelled invitation before acceptance', 0, 0, 1, 1, 50);
```

---

## 6. `ref.UserRole` - System-Level Roles

```sql
INSERT INTO [ref].[UserRole] (RoleCode, RoleName, Description, RoleLevel, CanManagePlatform, CanManageAllCompanies, CanViewAllData, CanAssignSystemRoles, IsActive, SortOrder) VALUES
('system_admin', 'System Administrator', 'Platform administrator with full access to all companies and system settings', 100, 1, 1, 1, 1, 1, 10),
('company_user', 'Company User', 'Standard company user (no system-level permissions)', 10, 0, 0, 0, 0, 1, 20);
```

---

## 7. `ref.UserCompanyRole` - Company-Level Roles

```sql
INSERT INTO [ref].[UserCompanyRole] (RoleCode, RoleName, Description, RoleLevel, CanManageCompany, CanManageUsers, CanManageEvents, CanManageForms, CanExportData, CanViewReports, IsActive, SortOrder) VALUES
('company_admin', 'Company Administrator', 'Full company access: manage company, users, events, forms, and reports', 100, 1, 1, 1, 1, 1, 1, 1, 10),
('company_user', 'Company User', 'Standard team member: create/edit own content, cannot manage users or company settings', 50, 0, 0, 1, 1, 1, 1, 1, 20),
('company_viewer', 'Company Viewer', 'Read-only access: view events, forms, and reports only', 10, 0, 0, 0, 0, 0, 1, 1, 30);
```

---

## 8. `ref.UserCompanyStatus` - User-Company Relationship Status

```sql
INSERT INTO [ref].[UserCompanyStatus] (StatusCode, StatusName, Description, IsActive, SortOrder) VALUES
('active', 'Active', 'Active team member with full role permissions', 1, 10),
('suspended', 'Suspended', 'Temporarily suspended by admin (cannot access company)', 1, 20),
('removed', 'Removed', 'User removed from company team (relationship ended)', 1, 30);
```

---

## 9. `ref.SettingCategory` - AppSetting Categories

```sql
INSERT INTO [ref].[SettingCategory] (CategoryCode, CategoryName, Description, IsActive, SortOrder) VALUES
('authentication', 'Authentication', 'Authentication and password policy settings', 1, 10),
('validation', 'Validation', 'Input validation rules and thresholds', 1, 20),
('email', 'Email', 'Email delivery and template configuration', 1, 30),
('security', 'Security', 'Security policies and rate limiting', 1, 40);
```

---

## 10. `ref.SettingType` - AppSetting Data Types

```sql
INSERT INTO [ref].[SettingType] (TypeCode, TypeName, Description, ValidationPattern, IsActive, SortOrder) VALUES
('integer', 'Integer', 'Whole number (e.g., 8, 90, 1000)', '^-?\d+$', 1, 10),
('boolean', 'Boolean', 'True/false flag', '^(true|false|0|1)$', 1, 20),
('string', 'String', 'Text value', NULL, 1, 30),
('json', 'JSON', 'JSON object for complex structures', NULL, 1, 40),
('decimal', 'Decimal', 'Decimal number (e.g., 0.10, 99.99)', '^-?\d+(\.\d+)?$', 1, 50);
```

---

## 11. `ref.RuleType` - ValidationRule Types

```sql
INSERT INTO [ref].[RuleType] (TypeCode, TypeName, Description, IsActive, SortOrder) VALUES
('phone', 'Phone Number', 'Phone number format validation', 1, 10),
('postal_code', 'Postal Code', 'Postal/zip code format validation', 1, 20),
('tax_id', 'Tax ID', 'Tax identifier format validation (ABN, EIN, VAT)', 1, 30),
('email', 'Email', 'Email format validation', 1, 40),
('address', 'Address', 'Address format validation', 1, 50);
```

---

## 12. `ref.CustomerTier` - Subscription Tiers

```sql
INSERT INTO [ref].[CustomerTier] (TierCode, TierName, Description, MonthlyPrice, AnnualPrice, MaxUsers, MaxForms, MaxSubmissionsPerMonth, IsActive, SortOrder) VALUES
('free', 'Free', 'Free tier with limited features (great for testing)', 0.00, 0.00, 2, 1, 100, 1, 10),
('starter', 'Starter', 'Starter plan for small teams', 29.00, 290.00, 5, 5, 1000, 1, 20),
('professional', 'Professional', 'Professional plan for growing businesses', 99.00, 990.00, 20, 50, 10000, 1, 30),
('enterprise', 'Enterprise', 'Enterprise plan with custom pricing and unlimited features', NULL, NULL, NULL, NULL, NULL, 1, 40);
```

---

## 13. `ref.JoinedVia` - User Acquisition Method

```sql
INSERT INTO [ref].[JoinedVia] (MethodCode, MethodName, Description, IsActive, SortOrder) VALUES
('signup', 'Signup', 'Self-signup during onboarding (user created their own company)', 1, 10),
('invitation', 'Invitation', 'Invited by company admin (accepted team invitation)', 1, 20),
('transfer', 'Transfer', 'Transferred from another company (future feature)', 0, 30);
```

---

## 14. `config.AppSetting` - Application Settings (12 settings)

```sql
INSERT INTO [config].[AppSetting] (SettingKey, SettingValue, SettingCategoryID, SettingTypeID, DefaultValue, Description, IsEditable, ValidationRegex, MinValue, MaxValue, IsActive, SortOrder) 
VALUES
-- Authentication Settings
('PASSWORD_MIN_LENGTH', '8', (SELECT SettingCategoryID FROM ref.SettingCategory WHERE CategoryCode='authentication'), (SELECT SettingTypeID FROM ref.SettingType WHERE TypeCode='integer'), '8', 'Minimum password length (characters)', 1, NULL, 6, 128, 1, 10),
('PASSWORD_REQUIRE_UPPERCASE', 'false', (SELECT SettingCategoryID FROM ref.SettingCategory WHERE CategoryCode='authentication'), (SELECT SettingTypeID FROM ref.SettingType WHERE TypeCode='boolean'), 'false', 'Require at least one uppercase letter in password', 1, NULL, NULL, NULL, 1, 20),
('PASSWORD_REQUIRE_NUMBER', 'true', (SELECT SettingCategoryID FROM ref.SettingCategory WHERE CategoryCode='authentication'), (SELECT SettingTypeID FROM ref.SettingType WHERE TypeCode='boolean'), 'true', 'Require at least one number in password', 1, NULL, NULL, NULL, 1, 30),
('PASSWORD_EXPIRY_DAYS', '90', (SELECT SettingCategoryID FROM ref.SettingCategory WHERE CategoryCode='authentication'), (SELECT SettingTypeID FROM ref.SettingType WHERE TypeCode='integer'), '90', 'Password expiry (days, 0 = never expires)', 1, NULL, 0, 365, 1, 40),
('ACCESS_TOKEN_EXPIRY_MINUTES', '15', (SELECT SettingCategoryID FROM ref.SettingCategory WHERE CategoryCode='authentication'), (SELECT SettingTypeID FROM ref.SettingType WHERE TypeCode='integer'), '15', 'JWT access token lifetime (minutes)', 1, NULL, 5, 60, 1, 50),
('REFRESH_TOKEN_EXPIRY_DAYS', '7', (SELECT SettingCategoryID FROM ref.SettingCategory WHERE CategoryCode='authentication'), (SELECT SettingTypeID FROM ref.SettingType WHERE TypeCode='integer'), '7', 'JWT refresh token lifetime (days)', 1, NULL, 1, 30, 1, 60),
('EMAIL_VERIFICATION_EXPIRY_HOURS', '24', (SELECT SettingCategoryID FROM ref.SettingCategory WHERE CategoryCode='authentication'), (SELECT SettingTypeID FROM ref.SettingType WHERE TypeCode='integer'), '24', 'Email verification token lifetime (hours)', 1, NULL, 1, 168, 1, 70),
('PASSWORD_RESET_EXPIRY_HOURS', '1', (SELECT SettingCategoryID FROM ref.SettingCategory WHERE CategoryCode='authentication'), (SELECT SettingTypeID FROM ref.SettingType WHERE TypeCode='integer'), '1', 'Password reset token lifetime (hours)', 1, NULL, 1, 24, 1, 80),
('INVITATION_EXPIRY_DAYS', '7', (SELECT SettingCategoryID FROM ref.SettingCategory WHERE CategoryCode='authentication'), (SELECT SettingTypeID FROM ref.SettingType WHERE TypeCode='integer'), '7', 'Team invitation lifetime (days)', 1, NULL, 1, 30, 1, 90),

-- Security Settings
('MAX_LOGIN_ATTEMPTS', '5', (SELECT SettingCategoryID FROM ref.SettingCategory WHERE CategoryCode='security'), (SELECT SettingTypeID FROM ref.SettingType WHERE TypeCode='integer'), '5', 'Maximum failed login attempts before account lockout', 1, NULL, 3, 10, 1, 100),
('ACCOUNT_LOCKOUT_MINUTES', '15', (SELECT SettingCategoryID FROM ref.SettingCategory WHERE CategoryCode='security'), (SELECT SettingTypeID FROM ref.SettingType WHERE TypeCode='integer'), '15', 'Account lockout duration (minutes)', 1, NULL, 5, 1440, 1, 110),
('SESSION_TIMEOUT_MINUTES', '30', (SELECT SettingCategoryID FROM ref.SettingCategory WHERE CategoryCode='security'), (SELECT SettingTypeID FROM ref.SettingType WHERE TypeCode='integer'), '30', 'Idle session timeout (minutes)', 1, NULL, 5, 480, 1, 120);
```

---

## 15. `config.ValidationRule` - Australia Validation Rules (4 rules)

```sql
INSERT INTO [config].[ValidationRule] (RuleKey, RuleTypeID, CountryID, ValidationPattern, ValidationMessage, Description, IsActive, Priority) 
VALUES
-- Australian phone validation
('PHONE_MOBILE_FORMAT', (SELECT RuleTypeID FROM ref.RuleType WHERE TypeCode='phone'), (SELECT CountryID FROM ref.Country WHERE CountryCode='AU'), '^04\d{8}$', 'Mobile number must start with 04 and be 10 digits', 'Australian mobile phone format validation', 1, 10),
('PHONE_LANDLINE_FORMAT', (SELECT RuleTypeID FROM ref.RuleType WHERE TypeCode='phone'), (SELECT CountryID FROM ref.Country WHERE CountryCode='AU'), '^0[2-8]\d{8}$', 'Landline must be 10 digits starting with 02-08', 'Australian landline phone format validation', 1, 20),

-- Australian postal code validation
('POSTAL_CODE_FORMAT', (SELECT RuleTypeID FROM ref.RuleType WHERE TypeCode='postal_code'), (SELECT CountryID FROM ref.Country WHERE CountryCode='AU'), '^\d{4}$', 'Australian postcode must be 4 digits', 'Australian postcode format validation', 1, 30),

-- Australian ABN validation
('TAX_ID_FORMAT', (SELECT RuleTypeID FROM ref.RuleType WHERE TypeCode='tax_id'), (SELECT CountryID FROM ref.Country WHERE CountryCode='AU'), '^\d{11}$', 'ABN must be 11 digits', 'Australian Business Number (ABN) format validation', 1, 40);
```

---

## Execution Order (Important!)

**Step 1: Foundation (No FKs)**
1. ref.Country
2. ref.Language
3. ref.Industry
4. ref.UserStatus
5. ref.UserInvitationStatus
6. ref.UserRole
7. ref.UserCompanyRole
8. ref.UserCompanyStatus
9. ref.SettingCategory
10. ref.SettingType
11. ref.RuleType
12. ref.CustomerTier
13. ref.JoinedVia

**Step 2: Configuration (Has FKs to Foundation)**
14. config.AppSetting (FK to SettingCategory, SettingType)
15. config.ValidationRule (FK to RuleType, Country)

---

## Verification Queries

```sql
-- Check row counts
SELECT 'Country' AS TableName, COUNT(*) AS RowCount FROM [ref].[Country]
UNION ALL SELECT 'Language', COUNT(*) FROM [ref].[Language]
UNION ALL SELECT 'Industry', COUNT(*) FROM [ref].[Industry]
UNION ALL SELECT 'UserStatus', COUNT(*) FROM [ref].[UserStatus]
UNION ALL SELECT 'UserInvitationStatus', COUNT(*) FROM [ref].[UserInvitationStatus]
UNION ALL SELECT 'UserRole', COUNT(*) FROM [ref].[UserRole]
UNION ALL SELECT 'UserCompanyRole', COUNT(*) FROM [ref].[UserCompanyRole]
UNION ALL SELECT 'UserCompanyStatus', COUNT(*) FROM [ref].[UserCompanyStatus]
UNION ALL SELECT 'SettingCategory', COUNT(*) FROM [ref].[SettingCategory]
UNION ALL SELECT 'SettingType', COUNT(*) FROM [ref].[SettingType]
UNION ALL SELECT 'RuleType', COUNT(*) FROM [ref].[RuleType]
UNION ALL SELECT 'CustomerTier', COUNT(*) FROM [ref].[CustomerTier]
UNION ALL SELECT 'JoinedVia', COUNT(*) FROM [ref].[JoinedVia]
UNION ALL SELECT 'AppSetting', COUNT(*) FROM [config].[AppSetting]
UNION ALL SELECT 'ValidationRule', COUNT(*) FROM [config].[ValidationRule];

-- Expected:
-- Country: 1
-- Language: 1
-- Industry: 10
-- UserStatus: 4
-- UserInvitationStatus: 5
-- UserRole: 2
-- UserCompanyRole: 3
-- UserCompanyStatus: 3
-- SettingCategory: 4
-- SettingType: 5
-- RuleType: 5
-- CustomerTier: 4
-- JoinedVia: 3
-- AppSetting: 12
-- ValidationRule: 4
```

---

**Winston** 🏗️  
*"Seed data: The vocabulary of your application."*

