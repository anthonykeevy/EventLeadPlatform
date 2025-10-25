# ABN Deduplication Strategy
**Story 1.19: Preventing Duplicate Companies**

Generated: 2025-10-25

---

## Business Rule

**One Company Per ABN:** Each unique ABN can only exist once in the system.

**Exception:** Companies WITHOUT an ABN (sole traders, manual entries, non-AU companies) can have duplicates.

---

## Why This Matters

### **Problem Without Deduplication:**

```
User A creates: "Atlassian Pty Ltd" - ABN 53102443916
User B creates: "Atlassian Pty Ltd" - ABN 53102443916
  ↓
Database now has 2 companies representing the SAME legal entity!
  ↓
Issues:
- Duplicate invoices
- Split financial data
- Compliance risks (which company for GST?)
- User confusion
```

### **Correct Behavior:**

```
User A creates: "Atlassian Pty Ltd" - ABN 53102443916 ✅
User B tries: "Atlassian Pty Ltd" - ABN 53102443916 ❌
  ↓
Error: "A company with ABN 53102443916 already exists.
       Company name: Atlassian Pty Ltd.
       If you work for this company, please request access."
  ↓
User B requests access → Existing admin approves → User B joins existing company ✅
```

---

## Implementation

### **Layer 1: Database Constraint (Data Safety)**

**Filtered Unique Index:**
```sql
CREATE UNIQUE NONCLUSTERED INDEX UQ_Company_ABN
ON dbo.Company(ABN)
WHERE ABN IS NOT NULL AND IsDeleted = 0;
```

**Why Filtered:**
- Enforces uniqueness ONLY when ABN is NOT NULL
- SQL Server treats NULL as distinct values
- Allows multiple companies with ABN = NULL (sole traders, etc.)
- Excludes deleted companies (IsDeleted = 1)

**Migration:** `backend/migrations/versions/011_unique_abn_constraint.py`

---

### **Layer 2: Application Check (User Experience)**

**Code:** `backend/modules/companies/service.py`

```python
# Check for duplicate ABN (Story 1.19)
if abn:
    existing_company = db.execute(
        select(Company).where(
            Company.ABN == abn,
            Company.IsDeleted == False
        )
    ).first()
    
    if existing_company:
        raise ValueError(
            f"A company with ABN {abn} already exists in the system. "
            f"Company name: {existing_company[0].CompanyName}. "
            f"If you work for this company, please request access."
        )
```

**Benefits:**
- ✅ Friendly error message before database exception
- ✅ Shows user the existing company name
- ✅ Guides user to request access instead
- ✅ Prevents cryptic database constraint error

---

## Scenarios Covered

### ✅ **Scenario 1: Duplicate ABN Prevention**

```
Existing: Atlassian Pty Ltd - ABN 53102443916
New attempt: Atlassian Pty Ltd - ABN 53102443916

Result: ❌ REJECTED
Error: "A company with ABN 53102443916 already exists."
```

### ✅ **Scenario 2: Multiple NULL ABNs Allowed**

```
Company A: "Anthony Keevy Consulting" - ABN NULL
Company B: "Sarah Smith Design" - ABN NULL
Company C: "Mike Jones Photography" - ABN NULL

Result: ✅ ALL ALLOWED
Reason: NULL ABNs are not unique (sole traders, manual entries)
```

### ✅ **Scenario 3: ACN Deduplication (Indirect)**

Since ABN is derived from ACN for companies, ACN uniqueness is enforced indirectly:

```
Company with ACN 102443916 → ABN 53102443916 (registered)
  ↓
Another user tries to register ACN 102443916
  ↓
ABR returns same ABN 53102443916
  ↓
Duplicate ABN check triggers ❌
  ↓
Prevents duplicate company ✅
```

### ✅ **Scenario 4: Deleted Companies Don't Block**

```
Company A: "Test Company" - ABN 12345678901 (IsDeleted = 1)
Company B: "Test Company" - ABN 12345678901 (IsDeleted = 0)

Result: ✅ ALLOWED
Reason: Filtered index excludes deleted companies
```

---

## User Journey: Duplicate Detection

### **User Tries to Create Duplicate:**

**Frontend Error Display:**
```
┌─────────────────────────────────────────────────────┐
│ ⚠️ Company Already Exists                           │
│                                                     │
│ A company with ABN 53 102 443 916 already exists   │
│ in the system:                                      │
│                                                     │
│ Company: Atlassian Pty Ltd                          │
│                                                     │
│ If you work for this company, please request       │
│ access from an existing administrator.              │
│                                                     │
│ [ Request Access ] [ Enter Different Company ]     │
└─────────────────────────────────────────────────────┘
```

### **Recommended Next Steps for User:**

1. **Contact existing admin** → Get invitation email
2. **Accept invitation** → Join existing company
3. **OR search for a different company** (if they entered wrong ABN)

---

## Edge Cases Handled

| Scenario | ABN Value | Allowed? | Reason |
|----------|-----------|----------|---------|
| First registration | `53102443916` | ✅ Yes | No duplicate |
| Second registration (same ABN) | `53102443916` | ❌ No | Duplicate ABN |
| Sole trader #1 | `NULL` | ✅ Yes | NULL allowed |
| Sole trader #2 | `NULL` | ✅ Yes | NULL != NULL in index |
| Manual entry (no ABN) | `NULL` | ✅ Yes | NULL allowed |
| Non-AU company | `NULL` | ✅ Yes | NULL allowed |
| Deleted company | `12345678901` (IsDeleted=1) | ✅ Yes | Excluded from index |
| Re-register deleted | `12345678901` | ✅ Yes | Can reuse ABN after deletion |

---

## Migration Instructions

**Run this migration to add the unique constraint:**

```powershell
cd backend
alembic upgrade head
```

**Verify the constraint:**
```sql
-- Check if index exists
SELECT 
    i.name AS IndexName,
    i.is_unique AS IsUnique,
    i.has_filter AS HasFilter,
    i.filter_definition AS FilterDefinition
FROM sys.indexes i
WHERE i.object_id = OBJECT_ID('dbo.Company')
AND i.name = 'UQ_Company_ABN';
```

**Expected Result:**
```
IndexName: UQ_Company_ABN
IsUnique: 1
HasFilter: 1
FilterDefinition: ([ABN] IS NOT NULL AND [IsDeleted]=(0))
```

---

## Future Enhancement: Access Request Flow

When duplicate ABN detected, we could automatically:

1. **Look up company admins** for the existing company
2. **Show "Request Access" button**
3. **Send access request** to existing admins
4. **Admin approves** → User joins company

**Implementation:** Story for Epic 2 (Team collaboration features)

---

## Testing the Constraint

**Test Case 1: Create duplicate ABN**
```sql
-- This should fail with unique constraint violation
INSERT INTO dbo.Company (CompanyName, ABN, CountryID, CreatedBy, UpdatedBy)
VALUES ('Test Duplicate', '53102443916', 1, 1, 1);
```

**Expected Error:**
```
Cannot insert duplicate key in object 'dbo.Company'. 
The duplicate key value is (53102443916).
```

**Test Case 2: Create multiple NULL ABNs**
```sql
-- These should ALL succeed
INSERT INTO dbo.Company (CompanyName, ABN, CountryID, CreatedBy, UpdatedBy)
VALUES ('Sole Trader 1', NULL, 1, 1, 1);

INSERT INTO dbo.Company (CompanyName, ABN, CountryID, CreatedBy, UpdatedBy)
VALUES ('Sole Trader 2', NULL, 1, 1, 1);
```

**Expected:** ✅ Both succeed (NULL allowed multiple times)

---

**This prevents duplicate companies while maintaining flexibility for sole traders and manual entries!** 🎯

