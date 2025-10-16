# `ref` Schema - Reference/Lookup Data

**Schema Purpose:** Static or slowly-changing reference/lookup data  
**Table Count:** 14  
**Retention:** Permanent  
**Backup Priority:** MEDIUM (changes rarely, can restore from seed scripts)  
**Write Volume:** VERY LOW (admin changes only)

---

## Schema Overview

Reference tables provide lookup data for dropdowns, validation, and enforcing data integrity through foreign keys. All reference tables follow a standard pattern with rich metadata.

**Standard Reference Table Pattern:**
- Primary Key: `[TableName]ID` (BIGINT IDENTITY)
- Code Column: `[Code]Code` (NVARCHAR(50), UNIQUE) - Machine-readable identifier
- Name Column: `[Code]Name` (NVARCHAR(100)) - Human-readable display name
- `Description` (NVARCHAR(500)) - Full explanation for UI tooltips
- `IsActive` (BIT, default 1) - Can be disabled without deletion
- `SortOrder` (INT, default 0) - For UI dropdown ordering
- Audit columns: `CreatedDate`, `CreatedBy`, `UpdatedDate`, `UpdatedBy`

---

## Table Overview

| # | Table | Purpose | Record Count | Updateable |
|---|-------|---------|--------------|------------|
| 1 | `Country` | Country lookup with currency/tax/integration metadata | 1 (AU), expandable to 250+ | Admin |
| 2 | `Language` | Language lookup | 1 (EN), expandable to 100+ | Admin |
| 3 | `Industry` | Industry/sector lookup | TBD (future) | Admin |
| 4 | `UserStatus` | User account status | 4 (pending, active, suspended, locked) | System |
| 5 | `UserInvitationStatus` | Invitation lifecycle status | 5 (pending, accepted, declined, expired, cancelled) | System |
| 6 | `UserRole` | System-level roles | 2 (system_admin, company_user) | System |
| 7 | `UserCompanyRole` | Company-level roles | 3 (company_admin, company_user, company_viewer) | System |
| 8 | `UserCompanyStatus` | User-company relationship status | 3 (active, suspended, removed) | System |
| 9 | `SettingCategory` | AppSetting categories | 4 (authentication, validation, email, security) | System |
| 10 | `SettingType` | AppSetting data types | 5 (integer, boolean, string, json, decimal) | System |
| 11 | `RuleType` | ValidationRule types | 5 (phone, postal_code, tax_id, email, address) | System |
| 12 | `CustomerTier` | Subscription tiers | 4 (free, starter, professional, enterprise) | Admin |
| 13 | `JoinedVia` | How user joined company | 3 (signup, invitation, transfer) | System |

---

## 1. `ref.Country` - Country Lookup

**Purpose:** Country master data with currency, tax, and integration metadata

**Key Features:**
- Currency information (code, symbol, name - ISO 4217)
- Tax configuration (rate, name, inclusive flag, tax number label)
- Country-specific integration providers (ABR, Geoscape for Australia)
- IntegrationConfig (JSON) for provider-specific settings

**Primary Key:** `CountryID` (BIGINT IDENTITY)

**Unique Constraints:**
- `CountryCode` (ISO 3166-1 alpha-2: 'AU', 'US', 'UK')
- `CountryName`

**Key Columns:**
- `CountryCode` - ISO 3166-1 alpha-2 code
- `CountryName` - Full country name
- `PhonePrefix` - International dialing code (e.g., '+61')
- `CurrencyCode` - ISO 4217 (e.g., 'AUD', 'USD')
- `CurrencySymbol` - Currency symbol (e.g., '$')
- `CurrencyName` - Full currency name
- `TaxRate` - Default tax rate (decimal, e.g., 0.10 for 10%)
- `TaxName` - Tax name (e.g., 'GST', 'VAT', 'Sales Tax')
- `TaxInclusive` - Whether prices include tax (boolean)
- `TaxNumberLabel` - Label for tax identifier (e.g., 'ABN', 'EIN', 'VAT Number')
- `CompanyValidationProvider` - Company validation service (e.g., 'ABR', 'Companies House')
- `AddressValidationProvider` - Address validation service (e.g., 'Geoscape', 'USPS')
- `IntegrationConfig` - JSON config for integration providers

**Seed Data (Australia):**
```json
{
  "countryCode": "AU",
  "countryName": "Australia",
  "phonePrefix": "+61",
  "currencyCode": "AUD",
  "currencySymbol": "$",
  "currencyName": "Australian Dollar",
  "taxRate": 0.10,
  "taxName": "GST",
  "taxInclusive": false,
  "taxNumberLabel": "ABN",
  "companyValidationProvider": "ABR",
  "addressValidationProvider": "Geoscape",
  "integrationConfig": {
    "abrApiUrl": "https://abr.business.gov.au/json/",
    "geoscapeApiUrl": "https://api.geoscape.com.au/"
  }
}
```

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: ref.Country)

---

## 2. `ref.Language` - Language Lookup

**Purpose:** Language/locale master data

**Key Columns:**
- `LanguageCode` - ISO 639-1 code (e.g., 'en', 'es', 'fr')
- `LanguageName` - Full language name (e.g., 'English', 'Spanish')

**Seed Data:**
- English ('en', 'English')

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: ref.Language)

---

## 3. `ref.Industry` - Industry/Sector Lookup

**Purpose:** Industry categorization for companies

**Key Columns:**
- `IndustryCode` - Machine-readable code
- `IndustryName` - Human-readable name
- `Description` - Full description

**Seed Data:** TBD (future)

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: ref.Industry)

---

## 4. `ref.UserStatus` - User Account Status

**Purpose:** Valid states for user accounts

**Key Columns:**
- `StatusCode` - Machine-readable code
- `StatusName` - Human-readable name
- `Description` - Full explanation

**Seed Data:**
1. `pending` - "Pending Verification" - User has signed up but not verified email
2. `active` - "Active" - User account is active and in good standing
3. `suspended` - "Suspended" - User account temporarily disabled by admin
4. `locked` - "Locked" - Account locked due to failed login attempts

**Referenced By:**
- `dbo.User.StatusID`

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: ref.UserStatus)

---

## 5. `ref.UserInvitationStatus` - Invitation Lifecycle Status

**Purpose:** Track invitation state through its lifecycle

**Key Columns:**
- `StatusCode` - Machine-readable code
- `StatusName` - Human-readable name
- `Description` - Full explanation

**Seed Data:**
1. `pending` - "Pending" - Invitation sent, awaiting response
2. `accepted` - "Accepted" - User accepted invitation
3. `declined` - "Declined" - User declined invitation
4. `expired` - "Expired" - Invitation expired (7-day TTL)
5. `cancelled` - "Cancelled" - Admin cancelled invitation before acceptance

**Referenced By:**
- `dbo.UserInvitation.UserInvitationStatusID`

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: ref.UserInvitationStatus)

---

## 6. `ref.UserRole` - System-Level Roles

**Purpose:** Platform-wide roles (system administration)

**Key Columns:**
- `RoleCode` - Machine-readable code
- `RoleName` - Human-readable name
- `Description` - Full explanation
- `RoleLevel` - Hierarchy level (higher = more privileges)
- Permission flags:
  - `CanManagePlatform` - Can access admin panel
  - `CanManageAllCompanies` - Can access any company's data
  - `CanViewAllData` - Can view cross-company reports
  - `CanAssignSystemRoles` - Can promote users to system admin

**Seed Data:**
1. `system_admin` - "System Administrator" - Platform administrator (all permissions)
2. `company_user` - "Company User" - Standard company user (no system permissions)

**Referenced By:**
- `dbo.User.UserRoleID`
- `audit.Role` (for role change audit)

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: ref.UserRole)

---

## 7. `ref.UserCompanyRole` - Company-Level Roles

**Purpose:** Roles within a company (team member permissions)

**Key Columns:**
- `RoleCode` - Machine-readable code
- `RoleName` - Human-readable name
- `Description` - Full explanation
- `RoleLevel` - Hierarchy level (higher = more privileges)
- Permission flags:
  - `CanManageCompany` - Can edit company profile
  - `CanManageUsers` - Can invite/remove team members
  - `CanManageEvents` - Can create/edit events
  - `CanManageForms` - Can publish forms
  - `CanExportData` - Can export submission data
  - `CanViewReports` - Can view analytics

**Seed Data:**
1. `company_admin` - "Company Administrator" - Full company access (all permissions)
2. `company_user` - "Company User" - Standard team member (create/edit own content)
3. `company_viewer` - "Company Viewer" - Read-only access (view only)

**Referenced By:**
- `dbo.UserCompany.UserCompanyRoleID`
- `dbo.UserInvitation.UserCompanyRoleID`
- `audit.Role` (for role change audit)

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: ref.UserCompanyRole)

---

## 8. `ref.UserCompanyStatus` - User-Company Relationship Status

**Purpose:** Status of user's relationship with a company

**Key Columns:**
- `StatusCode` - Machine-readable code
- `StatusName` - Human-readable name
- `Description` - Full explanation

**Seed Data:**
1. `active` - "Active" - Active team member
2. `suspended` - "Suspended" - Temporarily suspended by admin
3. `removed` - "Removed" - User removed from company team

**Referenced By:**
- `dbo.UserCompany.UserCompanyStatusID`

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: ref.UserCompanyStatus)

---

## 9. `ref.SettingCategory` - AppSetting Categories

**Purpose:** Logical grouping for AppSettings (UI organization)

**Key Columns:**
- `CategoryCode` - Machine-readable code
- `CategoryName` - Human-readable name
- `Description` - Full explanation

**Seed Data:**
1. `authentication` - "Authentication" - Auth-related settings (password policy, token expiry)
2. `validation` - "Validation" - Validation rules and thresholds
3. `email` - "Email" - Email configuration
4. `security` - "Security" - Security policies

**Referenced By:**
- `config.AppSetting.SettingCategoryID`

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: ref.SettingCategory)

---

## 10. `ref.SettingType` - AppSetting Data Types

**Purpose:** Data type for AppSetting values (validation + UI rendering)

**Key Columns:**
- `TypeCode` - Machine-readable code
- `TypeName` - Human-readable name
- `Description` - Full explanation
- `ValidationPattern` - Regex pattern for validation (optional)

**Seed Data:**
1. `integer` - "Integer" - Whole number
2. `boolean` - "Boolean" - True/false flag
3. `string` - "String" - Text value
4. `json` - "JSON" - JSON object (complex structures)
5. `decimal` - "Decimal" - Decimal number (e.g., currency, percentages)

**Referenced By:**
- `config.AppSetting.SettingTypeID`

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: ref.SettingType)

---

## 11. `ref.RuleType` - ValidationRule Types

**Purpose:** Categorize ValidationRules (apply to different data types)

**Key Columns:**
- `TypeCode` - Machine-readable code
- `TypeName` - Human-readable name
- `Description` - Full explanation

**Seed Data:**
1. `phone` - "Phone Number" - Phone number format validation
2. `postal_code` - "Postal Code" - Postal/zip code format validation
3. `tax_id` - "Tax ID" - Tax identifier format validation (ABN, EIN, VAT)
4. `email` - "Email" - Email format validation
5. `address` - "Address" - Address format validation

**Referenced By:**
- `config.ValidationRule.RuleTypeID`

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: ref.RuleType)

---

## 12. `ref.CustomerTier` - Subscription Tiers

**Purpose:** Company subscription/pricing tiers (controls feature access)

**Key Columns:**
- `TierCode` - Machine-readable code
- `TierName` - Human-readable name
- `Description` - Full explanation
- `MonthlyPrice` - Base monthly price (DECIMAL(10,2))
- `AnnualPrice` - Base annual price (with discount)
- `MaxUsers` - Maximum team members allowed
- `MaxForms` - Maximum published forms allowed
- `MaxSubmissionsPerMonth` - Submission quota per month

**Seed Data:**
1. `free` - "Free" - Free tier (limited features) - $0/month
2. `starter` - "Starter" - Starter plan - $XX/month
3. `professional` - "Professional" - Professional plan - $XXX/month
4. `enterprise` - "Enterprise" - Enterprise plan - Custom pricing

**Referenced By:**
- `dbo.CompanyCustomerDetails.CustomerTierID`

**Future Enhancements:**
- Add feature flags per tier (CanUseCustomBranding, CanExportData, etc.)
- Add per-country pricing variations

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: ref.CustomerTier)

---

## 13. `ref.JoinedVia` - How User Joined Company

**Purpose:** Track user acquisition method (analytics + audit)

**Key Columns:**
- `MethodCode` - Machine-readable code
- `MethodName` - Human-readable name
- `Description` - Full explanation

**Seed Data:**
1. `signup` - "Signup" - Self-signup during onboarding (created company)
2. `invitation` - "Invitation" - Invited by company admin
3. `transfer` - "Transfer" - Transferred from another company (future)

**Referenced By:**
- `dbo.UserCompany.JoinedViaID`

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: ref.JoinedVia)

---

## Common Patterns

### **Standard Reference Table Structure**

All reference tables follow this template:

```sql
CREATE TABLE [ref].[{EntityName}] (
    {EntityName}ID BIGINT IDENTITY(1,1) PRIMARY KEY,
    {Code}Code NVARCHAR(50) NOT NULL UNIQUE,
    {Code}Name NVARCHAR(100) NOT NULL,
    Description NVARCHAR(500) NOT NULL,
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 0,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    CONSTRAINT UQ_{EntityName}_{Code}Code UNIQUE ({Code}Code)
);
```

### **Benefits of Reference Tables**

1. **Referential Integrity:**
   - Cannot insert invalid StatusID (foreign key constraint)
   - Database enforces data validity

2. **Rich Metadata:**
   - Description for UI tooltips
   - SortOrder for dropdown ordering
   - IsActive flag for soft disable

3. **Extensibility:**
   - Add new status/tier via INSERT (no code deploy needed)
   - Admin UI can manage reference data

4. **Self-Documenting Queries:**
   ```sql
   SELECT u.FirstName, us.StatusName
   FROM dbo.User u
   JOIN ref.UserStatus us ON u.StatusID = us.UserStatusID;
   -- Result: "John", "Active" (not "John", 2)
   ```

---

## Query Patterns

### **Get All Active Reference Values (For Dropdown)**

```sql
SELECT 
    UserStatusID as value,
    StatusName as label,
    Description as tooltip
FROM ref.UserStatus
WHERE IsActive = 1
ORDER BY SortOrder;
```

### **Lookup by Code (Application Logic)**

```sql
SELECT UserStatusID
FROM ref.UserStatus
WHERE StatusCode = 'active';
```

### **Admin: Disable Reference Value (Soft Disable)**

```sql
UPDATE ref.CustomerTier
SET IsActive = 0, UpdatedDate = GETUTCDATE(), UpdatedBy = @admin_user_id
WHERE TierCode = 'legacy_tier';
```

---

## Performance Considerations

**Caching Strategy:**
- Reference tables are tiny (< 100 rows each)
- VERY low write volume (admin changes only)
- HIGH read volume (every query joins to status/role tables)
- **Recommendation:** Cache aggressively in application layer (Redis or in-memory)

**Index Strategy:**
- Primary key (clustered index): Automatic
- Unique constraint on Code: Automatic non-clustered index
- Additional indexes generally not needed (tables are tiny)

**JOIN Cost:**
- Reference table JOINs are effectively free (fully cached in memory)
- Benchmark: < 0.1ms per JOIN

---

## Related Documentation

**Architecture:**
- `docs/architecture/decisions/ADR-004-database-normalization-for-enum-like-fields.md`

**Database:**
- `docs/database/REBUILD-PLAN-SUMMARY.md`
- `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` - Full SQL definitions

---

**Winston** 🏗️  
*"Reference tables are the vocabulary of your database."*

