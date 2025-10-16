# EventLead Platform - Complete Data Requirements
## Dimitri's 🔍 Comprehensive Review

**Date:** October 15, 2025  
**Reviewed By:** Dimitri (Data Domain Architect) + Amelia (Developer Agent)  
**Status:** ✅ **Production-Ready Checklist**

---

## Executive Summary

Based on Dimitri's extensive domain analysis and current database state, here are **ALL** data requirements for Event Lead Platform:

**Current Status:**
- ✅ 2 Lookup Tables POPULATED (UserStatus, InvitationStatus)
- ❌ 1 System Record MISSING (System User - UserID = 1)
- ❓ Unknown: EventLead Platform Company (CompanyID = 1)
- ❓ Unknown: Country/Language seed data

---

## 1. CRITICAL: Lookup Tables (REQUIRED FOR STORY 1.1)

### 1.1 UserStatus ✅ POPULATED
**Current State:** ✅ **5 records exist**

```sql
-- Verify:
SELECT StatusCode, DisplayName, AllowLogin FROM UserStatus ORDER BY SortOrder;
```

| StatusCode | DisplayName | AllowLogin | Required For |
|-----------|-------------|------------|--------------|
| active | Active | Yes | Normal user operations |
| unverified | Unverified Email | No | **Signup flow (Story 1.1)** ⭐ |
| suspended | Suspended | No | Admin suspension |
| locked | Locked (Brute Force) | No | Security (5 failed logins) |
| deleted | Deleted | No | Soft delete (audit trail) |

**Foreign Key Impact:**
- `User.Status` → `UserStatus.StatusCode`
- **Without this data, signup fails with FK violation** ❌

---

### 1.2 InvitationStatus ✅ POPULATED
**Current State:** ✅ **5 records exist**

```sql
-- Verify:
SELECT StatusCode, DisplayName, CanResend, IsFinalState FROM InvitationStatus ORDER BY SortOrder;
```

| StatusCode | DisplayName | CanResend | IsFinalState | Required For |
|-----------|-------------|-----------|--------------|--------------|
| pending | Pending | Yes | No | Team invitation flow (Story 1.14) |
| accepted | Accepted | No | Yes | Invitation acceptance |
| expired | Expired | Yes | Yes | Auto-expiry (7 days) |
| cancelled | Cancelled | No | Yes | Admin cancellation |
| declined | Declined | No | Yes | User decline (Phase 2) |

**Foreign Key Impact:**
- `Invitation.Status` → `InvitationStatus.StatusCode`
- **Not required for Story 1.1** (signup only) ✅

---

## 2. CRITICAL: System Records

### 2.1 System User (UserID = 1) ❌ MISSING
**Current State:** ❌ **NOT CREATED**

**Why Required:**
All tables have audit columns (`CreatedBy`, `UpdatedBy`, `DeletedBy`) that reference `User(UserID)`. When system operations occur (seed data, automated processes), we need a system user to reference.

**Required Fields:**
```sql
UserID = 1 (explicit)
Email = 'system@eventlead.com.au'
FirstName = 'System'
LastName = 'User'
Status = 'active'
EmailVerified = 1
OnboardingComplete = 1
LoginAttempts = 0
TwoFactorEnabled = 0
AccessTokenVersion = 1
RefreshTokenVersion = 1
IsDeleted = 0
CreatedBy = 1 (self-referencing)
```

**Impact:**
- ✅ **Story 1.1 works WITHOUT this** (users set CreatedBy to their own UserID after signup)
- ❌ **Seed data operations WILL FAIL** without this record
- ❌ **Automated processes** (background jobs, migrations) need this

**Seed Script Location:** `database/seeds/production/01-reference-data-seed.sql`

---

### 2.2 EventLead Platform Company (CompanyID = 1) ❓ UNKNOWN
**Current State:** ❓ **NEEDS VERIFICATION**

```sql
-- Check if exists:
SELECT CompanyID, DisplayName FROM Company WHERE CompanyID = 1;
```

**Why Required (Per Dimitri's Analysis):**
- Australian GST tax invoices require **SELLER ABN** (EventLead Platform)
- Multi-tenant architecture: EventLead is CompanyID = 1 (special system company)
- Customer companies start from CompanyID = 2

**Schema Location:** `database/schemas/eventlead-platform-seed.sql`

**Impact:**
- ✅ **Story 1.1 works WITHOUT this** (signup doesn't require company yet)
- ❌ **Story 1.2 (Company Onboarding) REQUIRES this** ⚠️

---

## 3. USER ROLES: No Lookup Table Required ✅

### Important Clarification
**There is NO `UserRole` table!** 

Roles are enforced by **CHECK constraints** on `UserCompany.Role`:

```sql
CONSTRAINT CK_UserCompany_Role CHECK (
    [Role]='viewer' OR 
    [Role]='company_user' OR 
    [Role]='manager' OR 
    [Role]='admin'
)
```

**Valid Values:**
- `viewer` - Read-only access
- `company_user` - Regular user (create drafts, cannot publish)
- `manager` - Management access (review, approve)
- `admin` - Full administrative access (publish, billing, invite)

**Why No Lookup Table?**
- ✅ Roles are **static and rarely change** (architectural decision)
- ✅ **Faster queries** (no JOIN required)
- ✅ **Simpler architecture** (fewer tables to maintain)
- ✅ **No risk of accidentally deleting** a role that's in use

**Dimitri's Recommendation:** ✅ **Approved pattern for stable enums**

---

## 4. FUTURE: Reference Data (Phase 2)

### 4.1 Country Table ❓ NOT YET REQUIRED
**Schema Location:** `database/schemas/country-language-schema.sql`

**Purpose:**
- International expansion (multi-country support)
- Phone number validation regex per country
- Address format specifications
- Tax system details (ABN for AU, EIN for US, VAT for EU)

**MVP Status:** ✅ **Australia-only** (no Country table needed for Story 1.1)

**Phase 2 Requirements:**
```sql
Country (30 fields):
- CountryCode (ISO 3166-1, e.g., "AU")
- CountryName ("Australia")
- PhoneRegexMobile, PhoneRegexLandline
- CurrencyCode (ISO 4217, e.g., "AUD")
- TaxIDLabel ("ABN" for Australia)
```

**Seed Data:** Australia + English (MVP baseline)

---

### 4.2 Language Table ❓ NOT YET REQUIRED
**Schema Location:** `database/schemas/country-language-schema.sql`

**Purpose:**
- Internationalization (i18n) support
- Multi-language UI/emails
- Date/time formatting per locale

**MVP Status:** ✅ **English-only** (no Language table needed for Story 1.1)

**Phase 2 Requirements:**
```sql
Language (17 fields):
- LanguageCode (ISO 639-1, e.g., "en")
- LanguageName ("English")
- NativeName ("English")
- ISO639_3 ("eng")
```

**Seed Data:** English + Australian English (en-AU)

---

### 4.3 Industry Table ❓ POTENTIALLY USEFUL
**Schema Location:** `database/schemas/industry-schema.sql`

**Purpose:**
- Company categorization (SaaS, Events, Healthcare, etc.)
- Analytics segmentation
- Custom features per industry

**Dimitri's Analysis:** Medium priority - could enhance analytics

**Impact on Story 1.1:** ✅ **Not required** (company onboarding is Story 1.2)

---

## 5. DATABASE STATE VERIFICATION SCRIPT

Run this to check **all** data requirements:

```sql
-- =====================================================================
-- EventLead Platform - Data Requirements Verification
-- =====================================================================
USE [EventLeadPlatform];
GO

PRINT '========================================';
PRINT 'EventLead Platform - Data Requirements';
PRINT '========================================';
PRINT '';

-- 1. Lookup Tables
SELECT 
    'UserStatus' AS [Table],
    COUNT(*) AS [RecordCount],
    CASE 
        WHEN COUNT(*) >= 5 THEN '✅ OK (5 statuses)'
        ELSE '❌ MISSING DATA'
    END AS [Status]
FROM UserStatus

UNION ALL

SELECT 
    'InvitationStatus',
    COUNT(*),
    CASE 
        WHEN COUNT(*) >= 5 THEN '✅ OK (5 statuses)'
        ELSE '❌ MISSING DATA'
    END
FROM InvitationStatus

UNION ALL

-- 2. System Records
SELECT 
    'System User (UserID=1)',
    COUNT(*),
    CASE 
        WHEN COUNT(*) = 1 THEN '✅ EXISTS'
        ELSE '❌ MISSING (Required for seed operations)'
    END
FROM [User] WHERE UserID = 1

UNION ALL

SELECT 
    'EventLead Company (CompanyID=1)',
    COUNT(*),
    CASE 
        WHEN COUNT(*) = 1 THEN '✅ EXISTS'
        ELSE '⚠️ MISSING (Required for Story 1.2)'
    END
FROM Company WHERE CompanyID = 1

UNION ALL

-- 3. Reference Tables (Phase 2)
SELECT 
    'Country (Reference Data)',
    COUNT(*),
    CASE 
        WHEN COUNT(*) > 0 THEN '✅ EXISTS (Phase 2)'
        WHEN EXISTS(SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Country')
            THEN '⚠️ TABLE EXISTS but EMPTY'
        ELSE 'ℹ️ NOT REQUIRED (Australia-only MVP)'
    END
FROM Country

UNION ALL

SELECT 
    'Language (Reference Data)',
    COUNT(*),
    CASE 
        WHEN COUNT(*) > 0 THEN '✅ EXISTS (Phase 2)'
        WHEN EXISTS(SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Language')
            THEN '⚠️ TABLE EXISTS but EMPTY'
        ELSE 'ℹ️ NOT REQUIRED (English-only MVP)'
    END
FROM [Language];

PRINT '';
PRINT '========================================';
PRINT 'Verification Complete!';
PRINT '========================================';
GO
```

---

## 6. PRODUCTION DEPLOYMENT CHECKLIST

### Pre-Deployment (Story 1.1 - User Signup)
- [x] ✅ UserStatus table populated (5 records)
- [x] ✅ InvitationStatus table populated (5 records)
- [ ] ❌ System User (UserID = 1) created
- [ ] ❓ EventLead Company (CompanyID = 1) verified

### Pre-Deployment (Story 1.2 - Company Onboarding)
- [ ] ❌ EventLead Company (CompanyID = 1) must exist
- [ ] ❓ CompanyBillingDetails seed data (EventLead's ABN)
- [ ] ❓ CompanyCustomerDetails seed data
- [ ] ❓ CompanyOrganizerDetails seed data

### Phase 2 (International Expansion)
- [ ] Country table populated (Australia + others)
- [ ] Language table populated (English + others)
- [ ] Industry table populated (optional)

---

## 7. SEED DATA EXECUTION ORDER

```bash
# 1. Reference Data (CRITICAL - Run First)
sqlcmd -S localhost -d EventLeadPlatform -i database/seeds/production/01-reference-data-seed.sql

# Populates:
# - UserStatus (5 records)
# - InvitationStatus (5 records)
# - System User (UserID = 1)

# 2. EventLead Platform Company (Run Second)
sqlcmd -S localhost -d EventLeadPlatform -i database/schemas/eventlead-platform-seed.sql

# Creates:
# - EventLead Platform Company (CompanyID = 1)
# - CompanyBillingDetails (EventLead's ABN)
# - CompanyCustomerDetails (Enterprise tier)
# - CompanyOrganizerDetails (Platform events)

# 3. Test Users (Development Only)
# sqlcmd -S localhost -d EventLeadPlatform -i database/seeds/test/user_test_data.sql

# 4. Country/Language (Phase 2)
# sqlcmd -S localhost -d EventLeadPlatform -i database/seeds/production/country-language-seed.sql
```

---

## 8. CURRENT ISSUE RESOLUTION (Story 1.1 Signup)

### Problem
User signup was failing with error: `"An error occurred during signup. Please try again."`

### Root Causes Identified
1. ❌ UserStatus table was **EMPTY** → Foreign key violation on `User.Status = 'unverified'`
2. ❌ InvitationStatus table was **EMPTY** → Would fail if invitations used
3. ❌ Backend model missing required fields → NULL violations on `LoginAttempts`, `TwoFactorEnabled`, etc.

### Resolution Applied ✅
1. ✅ Populated UserStatus table (5 records)
2. ✅ Populated InvitationStatus table (5 records)
3. ✅ Updated `backend/models/user.py` to add `Status` foreign key
4. ✅ Updated `backend/modules/auth/service.py` to set all required fields explicitly

### Remaining Actions
- [ ] Create System User (UserID = 1) for seed operations
- [ ] Verify EventLead Company (CompanyID = 1) exists before Story 1.2
- [ ] Document seed data execution in deployment guide

---

## 9. DIMITRI'S RECOMMENDATIONS

### Immediate (Story 1.1) ⭐
1. ✅ **DONE:** Populate UserStatus and InvitationStatus tables
2. ❌ **TODO:** Create System User (UserID = 1) for future operations
3. ✅ **DONE:** Fix backend model to match database schema

### Before Story 1.2 (Company Onboarding) ⚠️
1. ❌ **TODO:** Create EventLead Platform Company (CompanyID = 1)
2. ❌ **TODO:** Seed CompanyBillingDetails with EventLead's actual ABN
3. ❌ **TODO:** Test company creation flow end-to-end

### Phase 2 (International Expansion) 📅
1. Populate Country table (Australia baseline, then expand)
2. Populate Language table (English baseline, then expand)
3. Consider Industry table for analytics segmentation

---

## 10. SCHEMA FILE LOCATIONS

| Domain | Schema File | Seed Data File | Status |
|--------|-------------|----------------|--------|
| User & Auth | `database/schemas/user-schema-v2.sql` | `database/seeds/production/01-reference-data-seed.sql` | ✅ Ready |
| Company | `database/schemas/company-schema.sql` | `database/schemas/eventlead-platform-seed.sql` | ❓ Verify |
| Events | `database/schemas/event-schema.sql` | N/A (Phase 2) | 📅 Future |
| Country/Language | `database/schemas/country-language-schema.sql` | N/A (Phase 2) | 📅 Future |
| Industry | `database/schemas/industry-schema.sql` | N/A (Optional) | 📅 Future |

---

## 11. QUESTIONS FOR ANTHONY

### Immediate
1. ❓ Should we create System User (UserID = 1) now or defer?
2. ❓ Has EventLead Platform Company (CompanyID = 1) been created?
3. ❓ What is EventLead's actual ABN for CompanyBillingDetails?

### Strategic
1. ❓ When do we need Country/Language tables? (Phase 2 timing)
2. ❓ Should we add Industry table for analytics? (Nice-to-have)
3. ❓ Data governance: Who approves production seed data changes?

---

## 12. CONTACT & SUPPORT

**Data Architecture Questions:** @dimitri 🔍 (Data Domain Architect)  
**Database Standards:** @solomon 📜 (SQL Standards Sage)  
**Development Implementation:** Amelia (Developer Agent)  

**Documentation:**
- `docs/data-domains/user-domain-COMPLETE.md` - Full user domain analysis
- `docs/data-domains/SCHEMAS-READY-FOR-SOLOMON-REVIEW.md` - Schema review checklist
- `database/DATA-REQUIREMENTS.md` - Quick reference guide

---

## 13. VERSION HISTORY

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | Oct 15, 2025 | Initial comprehensive review based on Dimitri's analysis | Amelia |
| 1.0.1 | Oct 15, 2025 | Added UserStatus/InvitationStatus seed data confirmation | Amelia |
| 1.0.2 | Oct 15, 2025 | Clarified UserRole CHECK constraint (no lookup table) | Amelia + Dimitri |

---

**Status:** ✅ **READY FOR STORY 1.1 (User Signup)**  
**Next Review:** Before Story 1.2 (Company Onboarding)

---

*"Design for today, architect for tomorrow"* - Dimitri 🔍

