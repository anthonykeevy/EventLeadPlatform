# Story 1.20 - Phone Validation Architecture Summary

**For:** Anthony Keevy  
**Purpose:** Complete understanding before running migration 009

---

## ✅ What Migration 009 Creates

### **1. CompanyValidationRule Table** (`config` schema)
- Links companies to their allowed validation rules
- Soft delete support (IsDeleted, DeletedDate, DeletedBy)
- Company can override rule precedence (SortOrderOverride)
- All database standards met ✅

### **2. Five Countries Seeded**
| Country | Phone Prefix | Currency | Tax | Tax Label |
|---------|--------------|----------|-----|-----------|
| 🇦🇺 Australia | +61 | AUD $ | 10% GST (incl) | ABN |
| 🇳🇿 New Zealand | +64 | NZD $ | 15% GST (incl) | NZBN |
| 🇺🇸 USA | +1 | USD $ | Sales Tax* | EIN |
| 🇬🇧 UK | +44 | GBP £ | 20% VAT (incl) | VAT Number |
| 🇨🇦 Canada | +1 | CAD $ | 5% GST (excl)** | BN |

\* Sales tax varies by state  
** Provinces add PST

### **3. Phone Validation Rules (All Countries)**

**Australia (6 active + 3 disabled):**
- ✅ Mobile local (`04XX XXX XXX`)
- ✅ Mobile international (`+61 4XX XXX XXX`)
- ✅ Landline local (`02/03/07/08 XXXX XXXX`)
- ✅ Landline international (`+61 2/3/7/8 XXXX XXXX`)
- ✅ Satellite (`014X XXXXXX`)
- ✅ Location-independent (`018X XXXXXX`)
- ❌ Toll-free (`1800`) - Disabled
- ❌ Local rate (`1300`) - Disabled
- ❌ Premium (`19XX`) - Disabled

**New Zealand (2 active + 1 disabled):**
- ✅ Mobile (`021/022/027/028/029`)
- ✅ Landline (`03/04/06/07/09`)
- ❌ Toll-free (`0800/0508`) - Disabled

**USA (2 active + 1 disabled):**
- ✅ Local format (`XXX-XXX-XXXX`)
- ✅ International (`+1 XXX XXX XXXX`)
- ❌ Toll-free (`1-800/888/etc`) - Disabled

**UK (2 active + 1 disabled):**
- ✅ Mobile (`07XXX XXXXXX`)
- ✅ Landline (`01/02 XXXX XXXX`)
- ❌ Toll-free (`0800`) - Disabled

**Canada (2 active):**
- ✅ Local format (same as USA)
- ✅ International (`+1 XXX XXX XXXX`)

### **4. EventLeads Company Seed Data**

**Company:**
- CompanyID: 1 (reserved)
- CompanyName: "EventLeads"
- CompanyType: "Platform Owner"
- Country: Australia

**EventLeads Validation Configuration:**
- ✅ ACCEPT: Mobile (local + intl)
- ✅ ACCEPT: Landline (local + intl)
- ✅ ACCEPT: Satellite
- ✅ ACCEPT: Location-independent
- ❌ REJECT: Toll-free (not in CompanyValidationRule = rejected)
- ❌ REJECT: Local rate (not in CompanyValidationRule = rejected)
- ❌ REJECT: Premium (not in CompanyValidationRule = rejected)

---

## 🔧 How Validation Works

### **Validation Logic:**

```sql
-- Get usable rules for EventLeads (CompanyID = 1)
SELECT vr.*
FROM [config].[ValidationRule] vr
INNER JOIN [config].[CompanyValidationRule] cvr 
    ON vr.ValidationRuleID = cvr.ValidationRuleID
WHERE cvr.CompanyID = 1
  AND vr.IsActive = 1          -- Country enables it
  AND cvr.IsEnabled = 1        -- Company enables it
  AND vr.IsDeleted = 0
  AND cvr.IsDeleted = 0
ORDER BY COALESCE(cvr.SortOrderOverride, vr.SortOrder)  -- Company override or default
```

**Result for EventLeads:**
- Mobile local (SortOrder 10)
- Mobile intl (SortOrder 11)
- Landline local (SortOrder 20)
- Landline intl (SortOrder 21)
- Satellite (SortOrder 25)
- Location-independent (SortOrder 26)

**NOT returned:** Toll-free, Local rate, Premium (not in CompanyValidationRule)

---

## 🧪 Test Examples After Migration

**Test 1: Valid Mobile (10 digits)**
```
Input: "0412345678"
Rule matched: PHONE_MOBILE_FORMAT ✅
Normalized: "+61412345678"
Result: Valid ✅
```

**Test 2: Invalid Mobile (8 digits)**
```
Input: "04147852"
Rule tried: PHONE_MOBILE_FORMAT
Pattern: ^0[4-5]\d{8}$ (requires 04/05 + 8 more = 10 total)
Actual: 04 + 6 more = 8 total
MinLength: 10, Actual: 8
Result: Invalid ❌
Error: "Mobile must be 04 or 05 followed by 8 digits (10 total). Try: 0412345678"
```

**Test 3: Valid Landline**
```
Input: "0298765432"
Rule matched: PHONE_LANDLINE_FORMAT ✅
Normalized: "+61298765432"
Result: Valid ✅
```

**Test 4: Toll-free (Rejected for EventLeads)**
```
Input: "1800123456"
Available rules: Only EventLeads-enabled rules queried
Toll-free rule: NOT in CompanyValidationRule for EventLeads
Result: Invalid ❌
Error: "Mobile must be 04 or 05..." (first rule's error)
```

---

## 📊 Database Standards Compliance

✅ **NVARCHAR** for all text fields  
✅ **PascalCase** naming (CompanyValidationRuleID, IsEnabled)  
✅ **[TableName]ID** pattern for PKs  
✅ **[ReferencedTable]ID** for FKs  
✅ **Is/Has** prefix for booleans  
✅ **UTC timestamps** with DATETIME2  
✅ **Audit columns** (CreatedDate, CreatedBy, UpdatedBy)  
✅ **Soft delete** (IsDeleted, DeletedDate, DeletedBy)  
✅ **Named constraints** (PK_, FK_, UQ_, IX_)  

---

## 🚀 Ready to Run

**Command:**
```powershell
alembic upgrade head
```

**What will happen:**
1. Creates `config.CompanyValidationRule` table
2. Seeds 4 new countries (NZ, US, UK, CA) with full details
3. Updates Australian phone rules (local + international formats)
4. Creates comprehensive phone rules for all 5 countries
5. Creates EventLeads company (CompanyID = 1)
6. Configures EventLeads validation (mobile, landline, satellite, location-independent)

**After migration:**
- `04147852` will correctly **FAIL** (too short)
- `0412345678` will correctly **PASS** and normalize to `+61412345678`
- EventLeads will reject toll-free/local-rate/premium numbers

---

**All your requirements met, Anthony!** Ready to run the migration? 🎯


