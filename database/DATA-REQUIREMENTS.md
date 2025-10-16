# EventLead Platform - Data Requirements & Seeding Strategy

## Purpose
This document defines all reference/lookup data requirements for the EventLead Platform database to prevent foreign key violations and ensure smooth production deployments.

## Last Updated
**Date:** October 15, 2025  
**Updated By:** Amelia (Developer Agent)  
**Story:** Story 1.1 - User Signup and Email Verification

---

## 1. Lookup Tables (Require Seed Data)

### 1.1 UserStatus
**Location:** `database/schemas/user-schema-v2.sql` (lines 59-67)  
**Status:** ✅ **POPULATED**

| StatusCode | DisplayName | AllowLogin | Description |
|-----------|-------------|------------|-------------|
| active | Active | Yes | User account is active and can log in normally |
| unverified | Unverified Email | No | User signed up but has not verified email address yet |
| suspended | Suspended | No | User account suspended by admin |
| locked | Locked (Brute Force) | No | Account temporarily locked due to failed login attempts |
| deleted | Deleted | No | User account soft-deleted (retain data for audit trail) |

**Seeding Command:**
```sql
sqlcmd -S localhost -d EventLeadPlatform -i database/seeds/production/01-reference-data-seed.sql
```

---

### 1.2 InvitationStatus
**Location:** `database/schemas/user-schema-v2.sql` (lines 106-112)  
**Status:** ✅ **POPULATED**

| StatusCode | DisplayName | CanResend | CanCancel | IsFinalState |
|-----------|-------------|-----------|-----------|--------------|
| pending | Pending | Yes | Yes | No |
| accepted | Accepted | No | No | Yes |
| expired | Expired | Yes | No | Yes |
| cancelled | Cancelled | No | No | Yes |
| declined | Declined | No | No | Yes |

**Seeding Command:**
```sql
sqlcmd -S localhost -d EventLeadPlatform -i database/seeds/production/01-reference-data-seed.sql
```

---

## 2. System Records (Required for Operations)

### 2.1 System User (UserID = 1)
**Purpose:** Required for audit trails (CreatedBy, UpdatedBy) when no specific user context exists  
**Status:** ⚠️ **NEEDS TO BE CREATED**

**Record:**
- UserID: 1
- Email: system@eventlead.com.au
- FirstName: System
- LastName: User
- Status: active
- EmailVerified: 1
- OnboardingComplete: 1

**Seeding Command:**
```sql
sqlcmd -S localhost -d EventLeadPlatform -i database/seeds/production/01-reference-data-seed.sql
```

---

### 2.2 EventLead Platform Company (CompanyID = 1)
**Purpose:** Represents EventLead as a seller on tax invoices (Australian GST compliance)  
**Status:** ❓ **UNKNOWN** (Check with `SELECT * FROM Company WHERE CompanyID = 1`)

**Location:** `database/schemas/eventlead-platform-seed.sql`  
**Seeding Command:**
```sql
sqlcmd -S localhost -d EventLeadPlatform -i database/schemas/eventlead-platform-seed.sql
```

---

## 3. CHECK Constraints (No Seed Data Required)

### 3.1 UserCompany.Role
**Valid Values (enforced by constraint):**
- `viewer` - Read-only access
- `company_user` - Regular user access
- `manager` - Management access
- `admin` - Full administrative access

**✅ No lookup table needed** - enforced by CHECK constraint

---

### 3.2 UserCompany.Status
**Valid Values (enforced by constraint):**
- `active` - Normal access
- `suspended` - Admin temporarily revoked access
- `inactive` - User removed from company

**✅ No lookup table needed** - enforced by CHECK constraint

---

### 3.3 UserCompany.JoinedVia
**Valid Values (enforced by constraint):**
- `self_join` - User created the company
- `invitation` - User invited by admin
- `direct_add` - Admin added user directly

**✅ No lookup table needed** - enforced by CHECK constraint

---

## 4. Potential Missing Lookup Tables

### 4.1 Country (for international expansion)
**Location:** `database/schemas/country-language-schema.sql`  
**Status:** ❓ **UNKNOWN**  
**Priority:** Low (Phase 2 - currently Australia-only)

### 4.2 Language (for i18n)
**Location:** `database/schemas/country-language-schema.sql`  
**Status:** ❓ **UNKNOWN**  
**Priority:** Low (Phase 2 - currently English-only)

### 4.3 Industry (for company categorization)
**Location:** `database/schemas/industry-schema.sql`  
**Status:** ❓ **UNKNOWN**  
**Priority:** Medium (could be useful for analytics)

---

## 5. Current Database State

### Verified Tables
```sql
-- Run this to check current state:
SELECT 
    'UserStatus' AS TableName, 
    COUNT(*) AS RecordCount,
    CASE WHEN COUNT(*) >= 5 THEN '✅ OK' ELSE '❌ MISSING DATA' END AS Status
FROM UserStatus
UNION ALL
SELECT 
    'InvitationStatus', 
    COUNT(*),
    CASE WHEN COUNT(*) >= 5 THEN '✅ OK' ELSE '❌ MISSING DATA' END
FROM InvitationStatus
UNION ALL
SELECT 
    'System User', 
    COUNT(*),
    CASE WHEN COUNT(*) = 1 THEN '✅ OK' ELSE '❌ MISSING' END
FROM [User] WHERE UserID = 1
UNION ALL
SELECT 
    'EventLead Company', 
    COUNT(*),
    CASE WHEN COUNT(*) = 1 THEN '✅ OK' ELSE '❌ MISSING' END
FROM Company WHERE CompanyID = 1;
```

---

## 6. Production Deployment Checklist

### Pre-Deployment
- [ ] Run `01-reference-data-seed.sql` to populate lookup tables
- [ ] Verify UserStatus has 5 records
- [ ] Verify InvitationStatus has 5 records
- [ ] Verify System User (UserID = 1) exists
- [ ] Verify EventLead Platform Company (CompanyID = 1) exists

### Post-Deployment Verification
```sql
-- Verify all reference data
EXEC sp_MSforeachtable 'SELECT ''?'' AS TableName, COUNT(*) AS RecordCount FROM ?'

-- Test user signup (should not fail on foreign keys)
-- Test via API: POST /api/auth/signup
```

---

## 7. Known Issues & Resolutions

### Issue 1: User Signup Fails (Oct 15, 2025)
**Error:** `An error occurred during signup. Please try again.`  
**Root Cause:** 
1. UserStatus table was empty (foreign key violation on User.Status)
2. Backend model had missing required fields (LoginAttempts, TwoFactorEnabled, etc.)

**Resolution:**
1. ✅ Populated UserStatus table with 5 statuses
2. ✅ Populated InvitationStatus table with 5 statuses
3. ✅ Updated User model to include all required fields with defaults
4. ✅ Updated AuthService.signup_user to set all NOT NULL columns

**Files Modified:**
- `backend/models/user.py` - Added Status foreign key
- `backend/modules/auth/service.py` - Added all required fields to User creation

---

## 8. Schema File Locations

| Schema | Location | Purpose |
|--------|----------|---------|
| User & Auth | `database/schemas/user-schema-v2.sql` | User, UserStatus, InvitationStatus, Invitation, UserCompany |
| Company | `database/schemas/company-schema.sql` | Company, CompanyBillingDetails, etc. |
| Events | `database/schemas/event-schema.sql` | Event, EventForm, etc. |
| Platform Seed | `database/schemas/eventlead-platform-seed.sql` | EventLead Company (CompanyID = 1) |
| Reference Data | `database/seeds/production/01-reference-data-seed.sql` | UserStatus, InvitationStatus, System User |

---

## 9. Contact & Maintenance

**Database Architect:** Dimitri 🔍 (Data Domain Architect)  
**Migration Validator:** Solomon 📜 (SQL Standards Sage)  
**Current Story:** Story 1.1 - User Signup and Email Verification  
**Developer:** Amelia (Developer Agent)

**Questions?** Reference: `docs/guardian-agents-guide.md`

