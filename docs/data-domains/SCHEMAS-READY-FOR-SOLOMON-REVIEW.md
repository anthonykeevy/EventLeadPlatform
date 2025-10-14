# Schemas Ready for Solomon's Review 📜

**Date:** October 13, 2025  
**Author:** Dimitri 🔍 (Data Domain Architect)  
**Reviewer Needed:** Solomon 📜 (Database Migration Validator)

---

## Summary

Three comprehensive schemas have been designed for EventLead Platform, ready for Solomon's validation against Anthony's database standards:

1. ✅ **Company Domain** (4 tables) - Multi-context normalized design
2. ✅ **Country & Language Domain** (2 tables) - Reference data with phone validation
3. ✅ **ABN API Integration** - Complete implementation guide

---

## Files for Solomon to Review

### 1. Company Domain Schema
**Location:** `database/schemas/company-schema.sql`

**Tables (4):**
- `Company` (11 fields) - Core company identity
- `CompanyCustomerDetails` (11 fields) - SaaS multi-tenant context
- `CompanyBillingDetails` (17 fields) - Australian tax compliance context
- `CompanyOrganizerDetails` (13 fields) - Event organizer B2B context

**Key Design Decisions:**
- Hybrid normalized approach (1 core + 3 extension tables)
- Handles overlapping roles: customer + organizer + billing
- Australian ABN validation (11 digits)
- Billing entity locking (after first invoice)
- Parent-subsidiary relationships (ParentCompanyID)

**Solomon Standards Checklist:**
- ✅ NVARCHAR for ALL text fields
- ✅ PascalCase naming (Company, CompanyID, TaxInvoiceName)
- ✅ [TableName]ID pattern (CompanyID, not just ID)
- ✅ Foreign keys: [ReferencedTable]ID (CompanyID references Company)
- ✅ Boolean prefix: IsDeleted, IsLocked, IsPublic, GSTRegistered
- ✅ UTC timestamps: DATETIME2, GETUTCDATE()
- ✅ Audit columns: CreatedDate, CreatedBy, UpdatedDate, UpdatedBy, IsDeleted, DeletedDate, DeletedBy
- ✅ Constraint naming: FK_CompanyBillingDetails_Company, CK_Company_AuditDates
- ✅ Soft deletes: IsDeleted flag (not hard DELETE)

**Potential Issues for Solomon to Check:**
1. ⚠️ `GSTRegistered` field - Should this be `IsTaxRegistered`? (more generic for international)
2. ⚠️ `ABN` field - Should this be `TaxID`? (currently ABN-specific, international expansion needed)
3. ⚠️ CHECK constraints - Are regex patterns correctly formatted for SQL Server?

---

### 2. Country & Language Domain Schema
**Location:** `database/schemas/country-language-schema.sql`

**Tables (2):**
- `Country` (30 fields) - ISO 3166-1 country reference data
- `Language` (17 fields) - ISO 639-1 language reference data

**Key Design Decisions:**
- ISO standard codes (CountryCode NVARCHAR(2), LanguageCode NVARCHAR(2))
- Currency aligned with Country (CurrencyCode NVARCHAR(3) - ISO 4217)
- Tax system details per country (ABN, GST for AU)
- Phone validation regex (4 types: landline, mobile, free call, special)
- Structured address format specifications
- International-ready (add countries without schema changes)

**Solomon Standards Checklist:**
- ✅ NVARCHAR for ALL text fields
- ✅ PascalCase naming (Country, CountryCode, CurrencyCode)
- ✅ Primary keys: CountryCode (not CountryID - using ISO standard)
- ✅ Foreign keys: DefaultLanguageCode → Language(LanguageCode)
- ✅ Boolean prefix: IsSupported, RequiresStateProvince, ConsumptionTaxVariable
- ✅ UTC timestamps: DATETIME2, GETUTCDATE()
- ✅ Audit columns: CreatedDate, CreatedBy, UpdatedDate, UpdatedBy, IsDeleted, DeletedDate, DeletedBy
- ✅ Constraint naming: FK_Country_DefaultLanguage, CK_Country_Code
- ✅ Soft deletes: IsDeleted flag

**Potential Issues for Solomon to Check:**
1. ⚠️ Primary keys: CountryCode (NVARCHAR(2)) instead of CountryID (BIGINT) - Is this acceptable? (Trade-off: ISO standard vs Anthony's [TableName]ID pattern)
2. ⚠️ CHECK constraint for ISO codes: `LEN(CountryCode) = 2 AND CountryCode = UPPER(CountryCode)` - Is this correct?
3. ⚠️ Phone regex fields: NVARCHAR(500) - Is this large enough for complex regex patterns?
4. ⚠️ Seed data: INSERT statements use hard-coded CreatedBy = 1 (System user) - Is this correct pattern?

---

### 3. Foreign Key Relationships

**CompanyBillingDetails → Country:**
```sql
ALTER TABLE CompanyBillingDetails
ADD CONSTRAINT FK_CompanyBillingDetails_Country 
    FOREIGN KEY (Country) REFERENCES Country(CountryCode);
```

**Country → Language:**
```sql
-- Already defined in schema:
CONSTRAINT FK_Country_DefaultLanguage 
    FOREIGN KEY (DefaultLanguageCode) REFERENCES [Language](LanguageCode)
```

**Question for Solomon:** Should foreign keys reference ISO code (CountryCode) or should we use surrogate keys (CountryID BIGINT)?

---

## Specific Questions for Solomon

### 1. ISO Codes as Primary Keys
**Current Design:**
```sql
CREATE TABLE [Country] (
    CountryCode NVARCHAR(2) PRIMARY KEY,  -- ISO 3166-1 (e.g., "AU")
    ...
);

CREATE TABLE [Language] (
    LanguageCode NVARCHAR(2) PRIMARY KEY,  -- ISO 639-1 (e.g., "en")
    ...
);
```

**Anthony's Standard:**
```sql
-- Usual pattern: [TableName]ID
CompanyID BIGINT IDENTITY(1,1) PRIMARY KEY
```

**Question:** Is it acceptable to use ISO standard codes as primary keys (CountryCode, LanguageCode) instead of surrogate keys (CountryID, LanguageID)?

**Rationale for ISO codes:**
- ✅ Industry standard (ISO 3166-1, ISO 639-1)
- ✅ Readable in queries: `WHERE Country = 'AU'` vs `WHERE CountryID = 1`
- ✅ Matches external APIs (Stripe, tax APIs use "AU", "US", not IDs)
- ✅ Stable codes (won't change, unlike surrogate keys)

**Rationale for surrogate keys:**
- ✅ Matches Anthony's [TableName]ID pattern
- ✅ Faster joins (BIGINT vs NVARCHAR(2))
- ✅ Consistent with other tables

**Recommendation:** Use ISO codes (stable, standard), but open to Solomon's guidance.

---

### 2. Boolean Field Naming - GSTRegistered

**Current Name:** `GSTRegistered` (CompanyBillingDetails table)

**Question:** Should this be renamed to `IsTaxRegistered` for international expansion?

**Current (Australian-specific):**
```sql
GSTRegistered BIT NOT NULL,  -- Is company registered for GST?
```

**International (generic):**
```sql
IsTaxRegistered BIT NOT NULL,  -- Is company registered for consumption tax (GST/VAT/Sales Tax)?
```

**Recommendation:** Keep `GSTRegistered` for MVP (Australia-only), refactor in Phase 2 (international).

---

### 3. ABN Field - Should It Be Generic?

**Current Name:** `ABN` (CompanyBillingDetails table)

**Question:** Should this be renamed to `TaxID` for international expansion?

**Current (Australian-specific):**
```sql
ABN NVARCHAR(11) NOT NULL,  -- Australian Business Number
```

**International (generic):**
```sql
TaxID NVARCHAR(20) NOT NULL,  -- Tax ID (ABN, EIN, VAT, etc.)
TaxIDType NVARCHAR(20) NOT NULL,  -- 'ABN', 'EIN', 'VAT'
```

**Recommendation:** Rename to `TaxID` NOW (backward compatible migration), future-proof schema.

---

### 4. CHECK Constraints for Regex

**Example:**
```sql
CONSTRAINT CK_Country_Code CHECK (
    LEN(CountryCode) = 2 AND CountryCode = UPPER(CountryCode)
)
```

**Question:** Is this CHECK constraint correctly formatted for SQL Server? Should we use `LIKE '[A-Z][A-Z]'` instead?

---

### 5. Audit Column Consistency

**Example from Country table:**
```sql
CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
CreatedBy BIGINT NOT NULL,
UpdatedDate DATETIME2 NULL,
UpdatedBy BIGINT NULL,
IsDeleted BIT NOT NULL DEFAULT 0,
DeletedDate DATETIME2 NULL,
DeletedBy BIGINT NULL,
```

**Question:** Does this match Anthony's exact pattern? Should DeletedBy also reference User(UserID)?

**Current:**
```sql
CONSTRAINT FK_Country_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [User](UserID),
CONSTRAINT FK_Country_UpdatedBy FOREIGN KEY (UpdatedBy) REFERENCES [User](UserID),
CONSTRAINT FK_Country_DeletedBy FOREIGN KEY (DeletedBy) REFERENCES [User](UserID),
```

---

## Solomon's Review Checklist

Please validate the following for **all 3 schema files**:

### Critical Standards (Must Fix):
- [ ] ✅ NVARCHAR for ALL text fields (no VARCHAR)
- [ ] ✅ PascalCase naming (tables and columns)
- [ ] ⚠️ Primary keys: [TableName]ID pattern (exception: ISO codes?)
- [ ] ✅ Foreign keys: [ReferencedTable]ID pattern
- [ ] ⚠️ Boolean prefix: Is/Has (GSTRegistered → IsTaxRegistered?)

### High Priority Standards:
- [ ] ✅ UTC timestamps: DATETIME2 with GETUTCDATE()
- [ ] ✅ Audit columns: CreatedDate, CreatedBy, UpdatedDate, UpdatedBy
- [ ] ✅ Soft deletes: IsDeleted, DeletedDate, DeletedBy

### Medium Priority Standards:
- [ ] ✅ Constraint naming: PK_, FK_, UQ_, IX_, CK_, DF_
- [ ] ✅ Indexes: Named appropriately (IX_Country_Name)
- [ ] ⚠️ CHECK constraints: Correctly formatted for SQL Server?

---

## Expected Solomon Feedback

**Anticipated Issues:**
1. **ISO codes as primary keys** (CountryCode vs CountryID)
   - Deviation from [TableName]ID pattern
   - Solomon will teach: "Why surrogate keys are preferred in enterprise schemas"
   - Dimitri's defense: "ISO codes are industry standard, stable, readable"

2. **GSTRegistered naming** (not `IsTaxRegistered`)
   - Deviation from generic naming for international
   - Solomon will recommend: "Rename to IsTaxRegistered for future markets"

3. **CHECK constraint syntax**
   - Possible SQL Server compatibility issues
   - Solomon will correct: Proper regex validation syntax

4. **Foreign key to User table**
   - DeletedBy references User(UserID) - is User table created?
   - Solomon will flag: "User table must exist before Company migration"

---

## Migration Order (After Solomon's Approval)

**Correct Order:**
1. ✅ `User` table (already exists - assumption)
2. ✅ `Language` table (no dependencies)
3. ✅ `Country` table (depends on Language for DefaultLanguageCode)
4. ✅ `Company` table (depends on User for audit columns)
5. ✅ `CompanyCustomerDetails` (depends on Company)
6. ✅ `CompanyBillingDetails` (depends on Company, optionally Country)
7. ✅ `CompanyOrganizerDetails` (depends on Company)

---

## Next Steps After Solomon's Review

1. **Fix any violations** Solomon identifies
2. **Update schemas** with Solomon's recommendations
3. **Create Alembic migrations** (Python migration scripts)
4. **Test migrations** on local SQL Server
5. **Import seed data** (Australia, English)
6. **Deploy to staging** for testing

---

## Files Summary

| File | Lines | Tables | Purpose | Status |
|------|-------|--------|---------|--------|
| `company-schema.sql` | 800+ | 4 | Company domain (customer + billing + organizer) | ✅ Ready for review |
| `country-language-schema.sql` | 450+ | 2 | Reference data (countries, languages, phone regex) | ✅ Ready for review |
| `abn-api-integration-guide.md` | 650+ | N/A | FastAPI implementation guide | ℹ️ Informational (not SQL) |
| `international-expansion-guide.md` | 1000+ | N/A | Schema changes for global support | ℹ️ Informational (Phase 2+) |
| `phone-validation-guide.md` | 700+ | N/A | Phone regex implementation guide | ℹ️ Informational |
| `stripe-currency-conversion-guide.md` | 400+ | N/A | Stripe multi-currency setup | ℹ️ Informational |

---

## Anthony's Approval Needed

**Before Solomon's review:**
1. ✅ **Approve ISO codes as primary keys?** (CountryCode vs CountryID)
2. ✅ **Rename ABN → TaxID now?** (future-proof for international)
3. ✅ **Rename GSTRegistered → IsTaxRegistered now?** (or wait for Phase 2?)

**After Solomon's review:**
1. ✅ **Approve schema changes** Solomon recommends
2. ✅ **Create Alembic migrations** (or delegate to dev team)
3. ✅ **Deploy to staging** for testing

---

## Call Solomon for Review

**Command:** `@solomon *validate-migration`

**Files to validate:**
1. `database/schemas/company-schema.sql`
2. `database/schemas/country-language-schema.sql`

**Expected Review Time:** 30-45 minutes (Solomon is thorough!)

---

**Dimitri's Sign-Off:**

All schemas are designed with Anthony's standards in mind, but I want Solomon's expert validation before we commit. These are foundational tables - getting them right now saves months of painful migrations later.

Ready for Solomon's review! 📜

---

*Dimitri - Data Domain Architect* 🔍  
*"Design for today, architect for tomorrow"*

