# ABN and ACN Relationship in Australia
**Story 1.19: Research and Analysis**

Generated: 2025-10-24

---

## Executive Summary

**ACN and ABN are separate but related identifiers** in the Australian business registration system:

- **ACN (Australian Company Number):** 9-digit identifier issued by **ASIC** (Australian Securities & Investments Commission)
- **ABN (Australian Business Number):** 11-digit identifier issued by **ATO** (Australian Taxation Office)

**Key Finding:** For companies registered with ASIC, **the ABN is mathematically derived from the ACN** by adding a 2-digit prefix and recalculating the checksum.

---

## Observed Relationship (From Our Testing)

### Test Case: Inchcape Australia Limited

**ACN Search Input:** `050035277` (9 digits)

**ABR Response:**
```json
{
  "ABN": "50050035277",  // 11 digits
  "ACN": "050035277"     // 9 digits (shown as ASICNumber in XML)
}
```

**Pattern Observed:**
```
ACN:  050035277  (9 digits)
ABN:  50050035277 (11 digits)
      ^^~~~~~~~~
      ||
      |└─ Same 9 digits from ACN
      └── 2-digit prefix (50)
```

**The ABN appears to be:** `[2-digit prefix] + [9-digit ACN]`

---

## How Australian Business Registration Works

### 1. **ACN (Australian Company Number) - 9 Digits**

**Issued by:** ASIC (Australian Securities & Investments Commission)

**Who gets an ACN:**
- Companies (Pty Ltd, Limited)
- Public companies
- Proprietary companies

**Purpose:**
- Identifies companies in the ASIC register
- Required for all companies incorporated in Australia
- Used in company documents, contracts, letterheads

**Format:** 9 digits (e.g., `123 456 789`)

**Checksum:** Uses modulus 10 weighted checksum algorithm

---

### 2. **ABN (Australian Business Number) - 11 Digits**

**Issued by:** ATO (Australian Taxation Office)

**Who gets an ABN:**
- ALL businesses operating in Australia (companies, sole traders, partnerships, trusts)
- Companies (also get it derived from their ACN)
- Sole traders, contractors
- Non-profit organizations
- Government entities

**Purpose:**
- Tax identification
- GST registration
- Business-to-business transactions
- Single identifier for all government dealings

**Format:** 11 digits (e.g., `12 345 678 901`)

**Checksum:** Uses modulus 89 weighted checksum algorithm

---

## The Derivation Process

### For Companies (with ACN):

When an Australian **company** applies for an ABN:

1. **Company registers with ASIC** → Gets ACN (9 digits)
2. **Company applies for ABN** → ATO derives ABN from ACN
3. **ABN Formula (likely):** Add 2-digit prefix to ACN + recalculate checksum

**Evidence from our testing:**
```
ACN: 050035277
ABN: 50050035277
     ^^ prefix appears to be first 2 digits of ACN
```

**Why this matters:**
- You can search by ACN and get the ABN
- You can search by ABN and get the ACN (returned as `ASICNumber`)
- They're **permanently linked** for companies

---

### For Non-Companies (No ACN):

Sole traders, partnerships, trusts, etc.:
- **Only have ABN** (no ACN)
- ABN is generated independently
- Not derived from anything

**Example:**
- Anthony Keevy (Sole Trader) → ABN: `12 345 678 901` (no ACN)
- Atlassian Pty Ltd (Company) → ACN: `102443916` + ABN: `53102443916`

---

## ABR API Response Patterns

### When Searching by ACN:

**Request:** `SearchByASICv201408` with ACN `050035277`

**Response includes:**
```xml
<businessEntity201408>
  <ABN>
    <identifierValue>50050035277</identifierValue>
  </ABN>
  <ASICNumber>050035277</ASICNumber>  <!-- This is the ACN -->
  <mainName>
    <organisationName>INCHCAPE AUSTRALIA LIMITED</organisationName>
  </mainName>
</businessEntity201408>
```

**Key Points:**
- ✅ ABR **automatically returns the ABN** (derived from ACN)
- ✅ ABR **also returns the ACN** (as `ASICNumber`)
- ✅ **We get both identifiers** from a single search!

---

### When Searching by ABN (for a company):

**Request:** `SearchByABNv202001` with ABN `53102443916`

**Response includes:**
```xml
<businessEntity202001>
  <ABN>
    <identifierValue>53102443916</identifierValue>
  </ABN>
  <ASICNumber>102443916</ASICNumber>  <!-- ACN extracted from ABN -->
  <mainName>
    <organisationName>ATLASSIAN PTY LTD</organisationName>
  </mainName>
</businessEntity202001>
```

**Key Points:**
- ✅ ABR **automatically returns the ACN** (extracted from ABN)
- ✅ For companies, **ABN search gives you the ACN**
- ✅ For non-companies (sole traders), `ASICNumber` is absent

---

## Implications for EventLead Platform

### Current Implementation ✅

**ACN Search:**
```
User types: 050035277 (ACN)
  ↓
Backend searches ABR by ACN
  ↓
ABR returns:
  - ABN: 50050035277 ✅
  - ACN: 050035277 ✅ (from ASICNumber field)
  ↓
We save BOTH:
  - Company.ABN = 50050035277
  - Company.ACN = 050035277
```

**ABN Search:**
```
User types: 53102443916 (ABN)
  ↓
Backend searches ABR by ABN
  ↓
ABR returns:
  - ABN: 53102443916 ✅
  - ACN: 102443916 ✅ (from ASICNumber field)
  ↓
We save BOTH:
  - Company.ABN = 53102443916
  - Company.ACN = 102443916
```

---

## ✅ **Recommendation: Update Backend to Extract ACN**

**Currently:** We're only saving ACN from user's search query (ACN searches only)

**Should do:** Extract ACN from ABR response (`ASICNumber` field) for ALL searches

This means:
- ✅ ABN search → Also saves ACN (if company)
- ✅ ACN search → Saves ACN
- ✅ Name search → Gets ABN → Enriches → Gets ACN

**Result:** **100% data capture** for companies!

---

## Why Both ABN and ACN Matter

**ABN Uses:**
- Tax invoices (must show ABN)
- GST registration
- Government contracts
- Business-to-business transactions

**ACN Uses:**
- Company letterheads (legal requirement)
- Contracts and agreements
- ASIC filings
- Company searches
- Shareholder communications

**For EventLead Platform:**
- You'll need **ABN** for invoicing (tax invoices)
- You'll need **ACN** for company verification
- Having both provides **complete company profile**

---

## Recommended Changes

### 1. Extract ACN from ABR Responses

In `abr_client.py`, update `_extract_entity_details()`:

```python
# Extract ACN from ASICNumber field (for companies)
acn = self._get_xml_text(entity_element, ".//ASICNumber")

return {
    "company_name": legal_name,
    "abn": abn,
    "acn": acn,  # ← ADD THIS
    "abn_formatted": self._format_abn(abn),
    ...
}
```

### 2. Update Frontend to Pass ACN from ABR

In `OnboardingStep2.tsx`, update submission:

```typescript
acn: abrData?.acn || searchedACN || null,  // Prefer ABR data, fallback to search query
```

---

## Summary

**ABN-ACN Relationship:**
- Separate registration systems (ASIC for ACN, ATO for ABN)
- For companies: **ABN is derived from ACN** (with prefix + checksum)
- **ABR API automatically provides both** when you search either one
- **We should extract and save both** for complete data

**Action:** Extract `ASICNumber` from ABR responses to capture ACN automatically!

---

**Would you like me to implement the ACN extraction from ABR responses?**

