# Validation Architecture - Complete End-to-End Guide

**Story 1.20:** Frontend Validation UI + International Phone Validation  
**Author:** Amelia (Dev Agent) + Anthony Keevy (Product Owner)  
**Purpose:** Complete understanding of validation flow from database → backend → frontend

---

## 🎯 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         DATABASE LAYER                          │
│  ┌──────────────┐   ┌─────────────────┐   ┌──────────────────┐ │
│  │   Country    │   │ ValidationRule  │   │ CompanyValidation│ │
│  │              │   │ (base rules)    │   │ Rule (overrides) │ │
│  │ - AU (+61)   │───│ - Phone formats │───│ - EventLeads     │ │
│  │ - NZ (+64)   │   │ - Postal codes  │   │   config         │ │
│  │ - US (+1)    │   │ - Tax IDs       │   │                  │ │
│  └──────────────┘   └─────────────────┘   └──────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│                         BACKEND LAYER                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              ValidationEngine Service                     │   │
│  │                                                           │   │
│  │  1. Get rules from DB (with caching)                     │   │
│  │  2. Filter by country + company (if configured)          │   │
│  │  3. Try rules in SortOrder precedence                    │   │
│  │  4. First match wins                                     │   │
│  │  5. Normalize to international (storage)                 │   │
│  │  6. Calculate display value (local format)               │   │
│  │  7. Return ValidationResult                              │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                ↓                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │      POST /api/countries/{id}/validate                   │   │
│  │      Returns: {is_valid, formatted_value, display_value} │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND LAYER                           │
│  ┌──────────────────┐   ┌─────────────────┐   ┌──────────────┐ │
│  │  useValidation   │   │   PhoneInput    │   │ PostalCode   │ │
│  │  Hook            │───│   Component     │   │ Input        │ │
│  │                  │   │                 │   │              │ │
│  │  - Calls API     │   │ - Shows local   │   │ - Validates  │ │
│  │  - Transforms    │   │   format        │   │   format     │ │
│  │    snake_case    │   │ - Green/red     │   │ - Shows      │ │
│  │                  │   │   borders       │   │   errors     │ │
│  └──────────────────┘   └─────────────────┘   └──────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 DATABASE LAYER - Detailed Structure

### **Table 1: ref.Country**

**Purpose:** Countries supported by platform

```sql
[ref].[Country]
  CountryID (PK)          Country Code    Phone Prefix    Postal Label    Tax Label
  1                       AU              +61             Postcode        GST (10%)
  2                       NZ              +64             Postcode        GST (15%)
  3                       US              +1              ZIP Code        Sales Tax
  4                       GB              +44             Postcode        VAT (20%)
  5                       CA              +1              Postal Code     GST (5%)
```

**Key Fields:**
- `PhonePrefix`: Used for phone normalization (+61 → 0)
- `TaxLabel`: GST vs VAT vs Sales Tax
- `TaxRate`: Default tax rate

---

### **Table 2: config.ValidationRule**

**Purpose:** Base validation rules per country

```sql
[config].[ValidationRule]
  ValidationRuleID (PK)
  RuleKey               e.g., 'PHONE_MOBILE_FORMAT', 'POSTAL_CODE_FORMAT'
  CountryID (FK)        Links to ref.Country
  RuleTypeID (FK)       Links to ref.RuleType (phone, postal_code, tax_id)
  
  -- Validation Logic
  ValidationPattern     Regex: '^0[4-5]\\d{8}$'
  ValidationMessage     Error message: 'Mobile must be 04 or 05...'
  MinLength            10
  MaxLength            10
  ExampleValue         '0412345678'
  SortOrder            10 (lower = higher priority)
  IsActive             1 (country enables/disables)
  
  -- Display Formatting (Story 1.20)
  DisplayFormat        '04XX XXX XXX' (how users see it)
  DisplayExample       '0412 345 678' (formatted example)
  StripPrefix          1 (remove +61 for display)
  SpacingPattern       'XXXX XXX XXX' (digit spacing)
```

**Example Rules:**

**Australia Phone Rules:**
| RuleKey | Pattern | SortOrder | IsActive | DisplayFormat |
|---------|---------|-----------|----------|---------------|
| PHONE_MOBILE_FORMAT | `^0[4-5]\d{8}$` | 10 | 1 | 04XX XXX XXX |
| PHONE_AU_MOBILE_INTL | `^\+61[4-5]\d{8}$` | 11 | 1 | 04XX XXX XXX |
| PHONE_LANDLINE_FORMAT | `^0[2-3,7-8]\d{8}$` | 20 | 1 | 0X XXXX XXXX |
| PHONE_AU_TOLLFREE | `^1800\d{6}$` | 30 | 0 | 1800 XXX XXX |
| POSTAL_CODE_FORMAT | `^\d{4}$` | 10 | 1 | XXXX |

**New Zealand Phone Rules:**
| RuleKey | Pattern | SortOrder | IsActive |
|---------|---------|-----------|----------|
| PHONE_NZ_MOBILE | `^0(21\|22\|27\|28\|29)\d{6,8}$` | 10 | 1 |
| PHONE_NZ_LANDLINE | `^0[3-4,6-7,9]\d{7,8}$` | 20 | 1 |
| POSTAL_CODE_NZ | `^\d{4}$` | 10 | 1 |

---

### **Table 3: config.CompanyValidationRule**

**Purpose:** Company-level rule configuration (overrides country defaults)

```sql
[config].[CompanyValidationRule]
  CompanyValidationRuleID (PK)
  CompanyID (FK)             1 (EventLeads)
  ValidationRuleID (FK)      Links to specific rule
  IsEnabled                  1 (company enables this rule)
  SortOrderOverride          NULL or custom order
```

**EventLeads Configuration:**
```
CompanyID=1 (EventLeads) ENABLES:
  - PHONE_MOBILE_FORMAT (local mobile)
  - PHONE_AU_MOBILE_INTL (intl mobile)
  - PHONE_LANDLINE_FORMAT (local landline)
  - PHONE_AU_LANDLINE_INTL (intl landline)
  - PHONE_AU_SATELLITE
  - PHONE_AU_LOCATION_INDEP

CompanyID=1 (EventLeads) REJECTS (not in CompanyValidationRule):
  - PHONE_AU_TOLLFREE (1800)
  - PHONE_AU_LOCALRATE (1300)
  - PHONE_AU_PREMIUM (19XX)
```

---

## 🔧 BACKEND LAYER - Validation Engine Flow

### **Step-by-Step Process:**

```python
# User calls: POST /api/countries/1/validate
# Body: {"rule_type": "phone", "value": "0412345678"}

┌──────────────────────────────────────────────────────────────────┐
│ STEP 1: Validation Engine - Get Rules                           │
└──────────────────────────────────────────────────────────────────┘

def get_validation_rules(country_id=1, rule_type='phone'):
    # Query database
    SELECT vr.*
    FROM [config].[ValidationRule] vr
    INNER JOIN [ref].[RuleType] rt ON vr.RuleTypeID = rt.RuleTypeID
    WHERE vr.CountryID = 1
      AND rt.TypeCode = 'phone'
      AND vr.IsActive = 1
      AND vr.IsDeleted = 0
    ORDER BY vr.SortOrder
    
    # Returns list of rules sorted by precedence
    
┌──────────────────────────────────────────────────────────────────┐
│ STEP 2: Filter by Company (if applicable)                       │
└──────────────────────────────────────────────────────────────────┘

# For EventLeads (CompanyID=1), filter to only enabled rules
# Check CompanyValidationRule table
# Only return rules where:
#   vr.IsActive = 1 (country level)
#   AND cvr.IsEnabled = 1 (company level)

┌──────────────────────────────────────────────────────────────────┐
│ STEP 3: Try Rules in Precedence Order                           │
└──────────────────────────────────────────────────────────────────┘

Input: "0412345678"

Rule 1 (SortOrder=10): PHONE_MOBILE_FORMAT
  Pattern: ^0[4-5]\d{8}$
  MinLength check: 10 >= 10 ✓
  MaxLength check: 10 <= 10 ✓
  Regex match: ^0[4-5]\d{8}$ matches "0412345678" ✓
  → MATCH FOUND! Stop trying rules.

┌──────────────────────────────────────────────────────────────────┐
│ STEP 4: Normalize to International Format                       │
└──────────────────────────────────────────────────────────────────┘

def _normalize_australian_phone("0412345678"):
    if phone.startswith('0'):
        return '+61' + phone[1:]  # "0412345678" → "+61412345678"

┌──────────────────────────────────────────────────────────────────┐
│ STEP 5: Calculate Display Value (Local Format)                  │
└──────────────────────────────────────────────────────────────────┘

def _get_display_value("+61412345678", rule):
    strip_prefix = rule.StripPrefix  # 1 (True)
    
    if international_value.startsWith('+61'):
        return '0' + international_value[3:]  # "+61412345678" → "0412345678"

┌──────────────────────────────────────────────────────────────────┐
│ STEP 6: Return ValidationResult                                 │
└──────────────────────────────────────────────────────────────────┘

return ValidationResult(
    is_valid=True,
    formatted_value="+61412345678",    # Store this (international)
    display_value="0412345678",        # Show this (local)
    matched_rule="PHONE_MOBILE_FORMAT",
    display_format="04XX XXX XXX",
    spacing_pattern="XXXX XXX XXX"
)
```

---

## 🌐 FRONTEND LAYER - Component Architecture

### **Component 1: useValidation Hook**

```typescript
// frontend/src/features/validation/hooks/useValidation.ts

const { validate, isValidating } = useValidation(countryId)

// When called:
const result = await validate('phone', '0412345678')

// Hook does:
1. POST to http://localhost:8000/api/countries/1/validate
2. Sends: {rule_type: "phone", value: "0412345678"}  ← snake_case
3. Receives: {is_valid, formatted_value, display_value, ...}  ← snake_case
4. Transforms to: {isValid, formattedValue, displayValue, ...}  ← camelCase
5. Returns ValidationResult
```

---

### **Component 2: PhoneInput**

```typescript
// frontend/src/features/validation/components/PhoneInput.tsx

<PhoneInput 
  value={phone}
  onChange={setPhone}
  countryId={1}
  onCountryDetected={setCountry}
/>

// Component logic:
1. User types: "0412345678"
2. onChange fires: value stored in state
3. User tabs out: onBlur fires
4. Calls: validate('phone', '0412345678')
5. Backend returns: {
     isValid: true,
     formattedValue: "+61412345678",  ← Store in database
     displayValue: "0412345678"       ← Show to user
   }
6. If valid AND displayValue different:
     onChange(displayValue)  ← Update field to local format
7. Show green border + checkmark
```

**Auto-Detection:**
```typescript
// If user types international prefix
User types: "+61412..."
→ Detects '+61'
→ Calls: onCountryDetected(1)  // Australia
→ Parent updates country dropdown
```

---

### **Component 3: CountrySelector**

```typescript
<CountrySelector 
  value={selectedCountry}
  onChange={setSelectedCountry}
  autoDetect={true}
/>

// Auto-detection logic:
1. Check browser timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
2. Map timezone to country:
   - "Australia/Sydney" → CountryID=1
   - "Pacific/Auckland" → CountryID=2
   - "America/New_York" → CountryID=3
3. Call onChange(detectedCountryId)
```

---

## 🔍 DEBUGGING GUIDE - Systematic Validation

### **🗄️ STEP 1: Verify Database Has Rules**

Run this query to check postal code rules exist:

```sql
SELECT 
    c.CountryCode,
    rt.TypeCode,
    vr.RuleKey,
    vr.ValidationPattern,
    vr.IsActive,
    vr.SortOrder,
    vr.MinLength,
    vr.MaxLength
FROM [config].[ValidationRule] vr
INNER JOIN [ref].[Country] c ON vr.CountryID = c.CountryID
INNER JOIN [ref].[RuleType] rt ON vr.RuleTypeID = rt.RuleTypeID
WHERE rt.TypeCode = 'postal_code'
ORDER BY c.CountryCode, vr.SortOrder
```

**Expected Results:**
- AU: POSTAL_CODE_FORMAT (4 digits)
- NZ: POSTAL_CODE_NZ (4 digits)
- US: POSTAL_CODE_US (5 or 5+4 digits)
- UK: POSTAL_CODE_UK (AA9A 9AA format)
- CA: POSTAL_CODE_CA (A9A 9A9 format)

**If NO RESULTS:** Migration 010 didn't insert rules properly.  
**If RESULTS EXIST:** Problem is in backend validation engine.

---

### **🔧 STEP 2: Test Backend Validation Engine Directly**

```python
# backend/test_validation_engine.py
from modules.countries.validation_engine import ValidationEngine
from common.database import SessionLocal

db = SessionLocal()
engine = ValidationEngine(db)

# Test USA postal code
result = engine.validate_field(
    country_id=3,  # USA
    rule_type='postal_code',
    value='94102'
)

print(f"Valid: {result.is_valid}")
print(f"Error: {result.error_message}")
print(f"Formatted: {result.formatted_value}")
```

**Expected:** `is_valid=True` for 94102

**If FAIL with "No rules configured":**
- Check: `engine.get_validation_rules(3, 'postal_code')`
- Debug: Why query returns empty

**Common Causes:**
1. RuleType table doesn't have TypeCode='postal_code'
2. CountryID mismatch (wrong ID for USA)
3. IsActive=0 or IsDeleted=1
4. Cached old data (clear cache)

---

### **🌐 STEP 3: Test API Endpoint**

```bash
curl -X POST http://localhost:8000/api/countries/3/validate \
  -H "Content-Type: application/json" \
  -d '{"rule_type": "postal_code", "value": "94102"}'
```

**Expected Response:**
```json
{
  "is_valid": true,
  "formatted_value": "94102",
  "display_value": "94102",
  "error_message": null
}
```

**If FAIL:** Router not passing through correctly.

---

### **💻 STEP 4: Test Frontend Hook**

```typescript
// In browser console
const result = await fetch('http://localhost:8000/api/countries/3/validate', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({rule_type: 'postal_code', value: '94102'})
}).then(r => r.json())

console.log(result)
```

**Expected:** Same as STEP 3

---

### **🎨 STEP 5: Test Frontend Component**

Open onboarding:
1. Change country to "United States"
2. Enter ZIP: "94102"
3. Tab out
4. Check network tab for API call
5. Check response

---

## 📞 PHONE NUMBER VALIDATION - Complete Flow

### **Example: Australian Mobile**

**Input:** `0412345678`  
**Country:** Australia (ID=1)

#### **Database Query:**

```sql
-- Get phone rules for Australia
SELECT * FROM [config].[ValidationRule] vr
INNER JOIN [ref].[RuleType] rt ON vr.RuleTypeID = rt.RuleTypeID
WHERE vr.CountryID = 1
  AND rt.TypeCode = 'phone'
  AND vr.IsActive = 1
ORDER BY vr.SortOrder

-- Returns (example):
RuleKey                   SortOrder   Pattern             MinLen  MaxLen
PHONE_MOBILE_FORMAT       10          ^0[4-5]\d{8}$       10      10
PHONE_AU_MOBILE_INTL      11          ^\+61[4-5]\d{8}$    12      12
PHONE_LANDLINE_FORMAT     20          ^0[2-3,7-8]\d{8}$   10      10
...
```

#### **Validation Engine Processing:**

```python
# 1. Clean input
value = "0412345678".strip()  # "0412345678"

# 2. Try Rule 1 (SortOrder=10): PHONE_MOBILE_FORMAT
pattern = "^0[4-5]\\d{8}$"
min_length = 10
max_length = 10

# Length check
len("0412345678") = 10
10 >= 10 (min) ✓
10 <= 10 (max) ✓

# Regex check
re.match("^0[4-5]\\d{8}$", "0412345678") → MATCH ✓

# 3. Normalize
_normalize_australian_phone("0412345678"):
  starts with '0' → return '+61' + "412345678" = "+61412345678"

# 4. Display value
_get_display_value("+61412345678", rule):
  rule.StripPrefix = 1 (True)
  starts with '+61' → return '0' + "412345678" = "0412345678"

# 5. Return result
ValidationResult(
    is_valid=True,
    formatted_value="+61412345678",
    display_value="0412345678",
    display_format="04XX XXX XXX",
    spacing_pattern="XXXX XXX XXX"
)
```

#### **API Response:**

```json
{
  "is_valid": true,
  "error_message": null,
  "formatted_value": "+61412345678",
  "display_value": "0412345678",
  "matched_rule": "PHONE_MOBILE_FORMAT",
  "display_format": "04XX XXX XXX",
  "spacing_pattern": "XXXX XXX XXX"
}
```

#### **Frontend Display:**

```typescript
// PhoneInput component receives result:
result.isValid = true
result.displayValue = "0412345678"

// If displayValue different from current value:
if (result.displayValue !== value) {
  onChange("0412345678")  // Update input field
}

// Shows:
- Input field: "0412345678" ← User sees local format
- Green border
- Checkmark icon
- "✓ Valid phone number"

// Stored in form state: "0412345678"
// When submitted to backend: normalized to "+61412345678"
```

---

## 📮 POSTAL CODE VALIDATION - Complete Flow

### **Example: USA ZIP Code**

**Input:** `94102`  
**Country:** USA (ID=3)

#### **Database Query:**

```sql
SELECT * FROM [config].[ValidationRule] vr
INNER JOIN [ref].[RuleType] rt ON vr.RuleTypeID = rt.RuleTypeID
WHERE vr.CountryID = 3
  AND rt.TypeCode = 'postal_code'
  AND vr.IsActive = 1
ORDER BY vr.SortOrder

-- Should return:
RuleKey           Pattern              MinLen  MaxLen  Example
POSTAL_CODE_US    ^\d{5}(-\d{4})?$     5       10      94102
```

#### **Validation Engine Processing:**

```python
# 1. Get rules
rules = get_validation_rules(country_id=3, rule_type='postal_code')

# DEBUG: If rules is empty list []
#   → Migration 010 didn't insert
#   OR RuleType.TypeCode doesn't match
#   OR CountryID wrong

# 2. If rules found, try each:
for rule in rules:
    pattern = rule.ValidationPattern  # "^\d{5}(-\d{4})?$"
    
    # Length check
    len("94102") = 5
    5 >= 5 (min) ✓
    5 <= 10 (max) ✓
    
    # Regex
    re.match("^\d{5}(-\d{4})?$", "94102") → MATCH ✓
    
    return ValidationResult(is_valid=True, formatted_value="94102")
```

---

## 🐛 DEBUGGING CHECKLIST

### **Problem: "No validation rules configured"**

**Check 1: Do rules exist in database?**
```sql
SELECT COUNT(*) FROM [config].[ValidationRule] 
WHERE CountryID = 3 AND RuleTypeID = (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='postal_code')
```
- If 0: Migration didn't run
- If >0: Query in validation engine is wrong

**Check 2: Is RuleType correct?**
```sql
SELECT * FROM [ref].[RuleType] WHERE TypeCode='postal_code'
```
- Should exist with RuleTypeID

**Check 3: Test validation engine query directly**
```python
from common.database import SessionLocal
from models.config.validation_rule import ValidationRule
from models.ref.rule_type import RuleType

db = SessionLocal()

rules = db.query(ValidationRule).join(
    RuleType, ValidationRule.RuleTypeID == RuleType.RuleTypeID
).filter(
    ValidationRule.CountryID == 3,
    RuleType.TypeCode == 'postal_code',
    ValidationRule.IsActive == True,
    ~ValidationRule.IsDeleted
).all()

print(f"Found {len(rules)} rules")
for rule in rules:
    print(f"  - {rule.RuleKey}: {rule.ValidationPattern}")
```

---

## 📋 SYSTEMATIC DEBUG STEPS FOR YOU

**Anthony, please run these in order:**

### **Step 1: Check Database**
```sql
-- Query in SQL Server Management Studio or Azure Data Studio
SELECT 
    c.CountryCode,
    rt.TypeCode,
    vr.RuleKey,
    vr.IsActive
FROM [config].[ValidationRule] vr
INNER JOIN [ref].[Country] c ON vr.CountryID = c.CountryID
INNER JOIN [ref].[RuleType] rt ON vr.RuleTypeID = rt.RuleTypeID
WHERE rt.TypeCode IN ('phone', 'postal_code')
ORDER BY c.CountryCode, rt.TypeCode, vr.SortOrder
```

**Expected:** Should see POSTAL_CODE_US, POSTAL_CODE_UK, POSTAL_CODE_NZ, POSTAL_CODE_CA

**If NOT FOUND:** Migration 010 didn't insert them.

---

### **Step 2: If Rules Found, Test Backend**
```powershell
cd backend
python check_postal_rules.py
```

This will show if Python can query the rules.

---

### **Step 3: Test API Directly**
```powershell
python test_postal_codes.py
```

See if API returns valid/invalid correctly.

---

**Let me know what Step 1 shows, and we'll debug from there!** 🔍

This systematic approach will find exactly where the flow breaks.


