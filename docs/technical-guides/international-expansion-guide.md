# International Expansion - Schema Design Guide

**Author:** Dimitri 🔍 (Data Domain Architect)  
**Date:** October 13, 2025  
**Purpose:** Schema modifications to support international customers (beyond Australia)

---

## Executive Summary

EventLead Platform is launching in **Australia** (MVP) but needs to scale globally. This guide analyzes schema changes required to support international customers across **US, UK, EU, Canada, Asia-Pacific** markets.

**Key Challenges:**
- 🌍 **Tax Systems:** Australia (ABN + GST), US (EIN + Sales Tax), UK (VAT + UTR), EU (VAT + VIES)
- 💰 **Currency:** AUD → USD, GBP, EUR, multiple currencies
- 📍 **Address Formats:** Different countries have different address structures
- 🔢 **Tax ID Formats:** ABN (11 digits) vs EIN (9 digits) vs VAT (variable)
- ⚖️ **Compliance:** GDPR (EU), SOC 2 (US), Privacy Act (Australia)

**Strategic Recommendation:** **Design for international NOW** (minimal cost), activate features LATER (when entering new markets).

---

## 1. Current Schema (Australian-Only)

### Current `CompanyBillingDetails` Table:
```sql
CREATE TABLE [CompanyBillingDetails] (
    CompanyID BIGINT PRIMARY KEY,
    
    -- Australian-specific fields
    ABN NVARCHAR(11) NOT NULL,              -- ❌ Australia-only
    ABNStatus NVARCHAR(20) NOT NULL,        -- ❌ Australia-only
    GSTRegistered BIT NOT NULL,             -- ❌ Australia-only (should be TaxRegistered)
    EntityType NVARCHAR(100) NULL,
    
    TaxInvoiceName NVARCHAR(200) NOT NULL,
    BillingEmail NVARCHAR(100) NOT NULL,
    BillingAddress NVARCHAR(500) NOT NULL,   -- ❌ Single text field (should be structured)
    
    -- ... audit fields
);
```

**Problems for International:**
1. ❌ **ABN field hardcoded** (US uses EIN, UK uses UTR, EU uses VAT number)
2. ❌ **GSTRegistered flag** (GST is Australian - US has Sales Tax, UK has VAT)
3. ❌ **ABNStatus** (doesn't apply to non-Australian businesses)
4. ❌ **No country field** (can't differentiate Australian vs US vs UK companies)
5. ❌ **No currency field** (all invoices assumed AUD)
6. ❌ **Unstructured address** (countries have different address formats)

---

## 2. International Tax Systems Analysis

### Tax ID Systems by Country:

| Country/Region | Tax ID Name | Format | Example | Validation API |
|----------------|-------------|--------|---------|----------------|
| **Australia** 🇦🇺 | ABN (Australian Business Number) | 11 digits | 53004085616 | ABR API (FREE) |
| **United States** 🇺🇸 | EIN (Employer Identification Number) | 9 digits (XX-XXXXXXX) | 12-3456789 | IRS (no public API) |
| **United Kingdom** 🇬🇧 | UTR (Unique Taxpayer Reference) + VAT | 10 digits / VAT: 9-12 chars | 1234567890 / GB123456789 | HMRC API (paid) |
| **European Union** 🇪🇺 | VAT Number (VIES) | Country code + 8-12 digits | DE123456789 | VIES API (FREE) |
| **Canada** 🇨🇦 | BN (Business Number) | 9 digits + program code | 123456789RC0001 | CRA (no public API) |
| **New Zealand** 🇳🇿 | NZBN (NZ Business Number) | 13 digits | 9429000000000 | NZBN API (FREE) |
| **Singapore** 🇸🇬 | UEN (Unique Entity Number) | 9-10 characters | 199700001W | ACRA (paid API) |

### Tax Systems by Country:

| Country | Tax Type | Rate | Applies To | Invoice Requirements |
|---------|----------|------|------------|----------------------|
| **Australia** 🇦🇺 | GST (Goods & Services Tax) | 10% | All goods/services | ABN, GST amount, tax invoice |
| **United States** 🇺🇸 | Sales Tax (state-level) | 0-10% (varies by state) | Physical goods (usually) | Sales tax varies by state |
| **United Kingdom** 🇬🇧 | VAT (Value Added Tax) | 20% | Most goods/services | VAT number, VAT amount |
| **European Union** 🇪🇺 | VAT | 15-27% (varies by country) | B2C; B2B reverse charge | VIES VAT validation |
| **Canada** 🇨🇦 | GST + PST/HST | 5-15% (varies by province) | Most goods/services | GST/HST number |
| **New Zealand** 🇳🇿 | GST | 15% | All goods/services | GST number |

**Key Insight:** Tax systems are **NOT standardized** globally. Each country has different:
- Tax ID format (9-13 characters)
- Tax type (GST, VAT, Sales Tax)
- Tax rate (5-27%)
- Invoice requirements

---

## 3. Proposed Schema Changes

### Strategy: **Flexible Multi-Country Design**

**Core Principles:**
1. ✅ **Generic field names** (not country-specific)
2. ✅ **Country as first-class citizen** (Country field determines validation rules)
3. ✅ **Structured addresses** (not single text field)
4. ✅ **Currency support** (multi-currency invoicing)
5. ✅ **Extensible tax data** (JSON for country-specific fields)

---

### 3.1 Updated `CompanyBillingDetails` Table

```sql
-- =====================================================================
-- CompanyBillingDetails - INTERNATIONAL VERSION
-- =====================================================================
CREATE TABLE [CompanyBillingDetails] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    CompanyID BIGINT PRIMARY KEY,
    
    -- =====================================================================
    -- Country & Currency (NEW - Critical for International)
    -- =====================================================================
    Country NVARCHAR(2) NOT NULL DEFAULT 'AU',
    -- ^ ISO 3166-1 alpha-2 country code (AU, US, GB, DE, etc.)
    -- Determines: Tax ID validation rules, tax type, address format
    -- DEFAULT 'AU' for backward compatibility (MVP = Australia)
    
    Currency NVARCHAR(3) NOT NULL DEFAULT 'AUD',
    -- ^ ISO 4217 currency code (AUD, USD, GBP, EUR, etc.)
    -- Used for: Invoice amounts, payment processing
    -- DEFAULT 'AUD' for backward compatibility
    
    -- =====================================================================
    -- Tax Identification (GENERIC - Not Country-Specific)
    -- =====================================================================
    TaxID NVARCHAR(20) NOT NULL,
    -- ^ RENAMED from ABN → TaxID (generic name)
    -- Content varies by country:
    --   AU: ABN (11 digits) "53004085616"
    --   US: EIN (9 digits) "12-3456789"
    --   GB: UTR or VAT "1234567890" or "GB123456789"
    --   EU: VAT number "DE123456789"
    -- Validation rules based on Country field
    
    TaxIDType NVARCHAR(20) NOT NULL DEFAULT 'ABN',
    -- ^ Type of tax ID: 'ABN', 'EIN', 'UTR', 'VAT', 'BN', 'NZBN', 'UEN'
    -- Helps identify which validation API to use
    -- DEFAULT 'ABN' for backward compatibility
    
    TaxIDStatus NVARCHAR(20) NOT NULL DEFAULT 'Active',
    -- ^ RENAMED from ABNStatus → TaxIDStatus (generic)
    -- Values: 'Active', 'Cancelled', 'Historical', 'Unverified', 'International'
    -- 'Unverified' = User entered manually (no API validation available)
    -- 'International' = Non-domestic company (e.g., US company using AU platform)
    
    TaxIDVerifiedDate DATETIME2 NULL,
    -- ^ RENAMED from ABNLastVerified → TaxIDVerifiedDate
    -- Last verification via API (ABR, VIES, etc.)
    
    TaxIDVerificationResponse NVARCHAR(MAX) NULL,
    -- ^ RENAMED from ABNVerificationResponse → TaxIDVerificationResponse
    -- Cached JSON response from validation API
    
    -- =====================================================================
    -- Tax Registration (GENERIC - Not GST-Specific)
    -- =====================================================================
    TaxRegistered BIT NOT NULL DEFAULT 0,
    -- ^ RENAMED from GSTRegistered → TaxRegistered (generic)
    -- 0 = Not registered for consumption tax (GST/VAT/Sales Tax)
    -- 1 = Registered (must charge tax on invoices)
    
    TaxType NVARCHAR(20) NULL,
    -- ^ Type of tax: 'GST', 'VAT', 'Sales Tax', 'HST'
    -- Derived from Country:
    --   AU → 'GST'
    --   GB/EU → 'VAT'
    --   US → 'Sales Tax' (state-specific)
    --   CA → 'GST' or 'HST' (province-specific)
    
    TaxRate DECIMAL(5, 2) NULL,
    -- ^ Tax rate as percentage (e.g., 10.00 for 10% GST, 20.00 for 20% VAT)
    -- Varies by country:
    --   AU: 10.00% (GST)
    --   GB: 20.00% (VAT)
    --   US: 0.00-10.00% (varies by state)
    --   EU: 15.00-27.00% (varies by country)
    -- NULL = tax-exempt or not tax-registered
    
    TaxStatus NVARCHAR(200) NULL,
    -- ^ RENAMED from GSTStatus → TaxStatus
    -- Human-readable tax status (e.g., "Registered for GST from 01 Jul 2000")
    
    -- =====================================================================
    -- Entity Details
    -- =====================================================================
    EntityType NVARCHAR(100) NULL,
    -- ^ Entity type (varies by country):
    --   AU: "Australian Private Company", "Sole Trader", "Partnership"
    --   US: "Corporation", "LLC", "Sole Proprietorship"
    --   UK: "Limited Company", "Partnership", "Sole Trader"
    
    TaxInvoiceName NVARCHAR(200) NOT NULL,
    -- ^ Legal entity name for invoices (from tax authority if validated)
    
    -- =====================================================================
    -- Billing Contact
    -- =====================================================================
    BillingEmail NVARCHAR(100) NOT NULL,
    BillingContactName NVARCHAR(200) NULL,
    BillingPhone NVARCHAR(20) NULL,
    
    -- =====================================================================
    -- Structured Address (NEW - Replaces single BillingAddress text field)
    -- =====================================================================
    AddressLine1 NVARCHAR(200) NOT NULL,
    -- ^ Street address, building number
    -- Example: "14 Darling Drive" or "123 Main Street, Suite 400"
    
    AddressLine2 NVARCHAR(200) NULL,
    -- ^ Additional address details (optional)
    -- Example: "Building B, Floor 3" or "Attn: Finance Department"
    
    City NVARCHAR(100) NOT NULL,
    -- ^ City name
    
    StateProvince NVARCHAR(100) NULL,
    -- ^ State/Province/Region (required for US, CA, AU; optional for others)
    -- US: "California", "New York"
    -- AU: "New South Wales", "Victoria"
    -- UK: NULL (not used)
    
    PostalCode NVARCHAR(20) NULL,
    -- ^ Zip/Postal code (format varies by country)
    -- US: "90210" (5 digits)
    -- AU: "2000" (4 digits)
    -- UK: "SW1A 1AA" (alphanumeric)
    -- Some countries don't use postal codes (e.g., Ireland rural areas)
    
    -- Country already defined above (ISO 3166-1 alpha-2)
    
    -- =====================================================================
    -- Country-Specific Extensions (NEW)
    -- =====================================================================
    CountrySpecificData NVARCHAR(MAX) NULL,
    -- ^ JSON field for country-specific tax data
    -- Example (US - Sales Tax):
    --   {"state_tax_id": "12-3456789-ST", "sales_tax_permit": "ST123456"}
    -- Example (EU - VIES):
    --   {"vies_validated": true, "vat_exemption_reason": "Intra-EU supply"}
    -- Extensible for future country requirements without schema migration
    
    -- =====================================================================
    -- Compliance & Locking (Unchanged)
    -- =====================================================================
    FirstInvoiceDate DATETIME2 NULL,
    IsLocked BIT NOT NULL DEFAULT 0,
    LockedDate DATETIME2 NULL,
    LockedBy BIGINT NULL,
    
    -- =====================================================================
    -- Audit Trail (Unchanged)
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NOT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    
    -- =====================================================================
    -- Constraints (UPDATED for international)
    -- =====================================================================
    CONSTRAINT FK_CompanyBillingDetails_Company FOREIGN KEY (CompanyID) 
        REFERENCES [Company](CompanyID) ON DELETE CASCADE,
    
    CONSTRAINT FK_CompanyBillingDetails_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [User](UserID),
    
    CONSTRAINT FK_CompanyBillingDetails_UpdatedBy FOREIGN KEY (UpdatedBy) 
        REFERENCES [User](UserID),
    
    CONSTRAINT FK_CompanyBillingDetails_LockedBy FOREIGN KEY (LockedBy) 
        REFERENCES [User](UserID),
    
    -- Tax ID length validation (flexible for different countries)
    CONSTRAINT CK_CompanyBillingDetails_TaxID_Length CHECK (
        LEN(TaxID) BETWEEN 8 AND 20
    ),
    
    -- Tax ID type validation
    CONSTRAINT CK_CompanyBillingDetails_TaxIDType CHECK (
        TaxIDType IN ('ABN', 'EIN', 'UTR', 'VAT', 'BN', 'NZBN', 'UEN', 'OTHER')
    ),
    
    -- Tax ID status validation
    CONSTRAINT CK_CompanyBillingDetails_TaxIDStatus CHECK (
        TaxIDStatus IN ('Active', 'Cancelled', 'Historical', 'Unverified', 'International')
    ),
    
    -- Country code validation (ISO 3166-1 alpha-2)
    CONSTRAINT CK_CompanyBillingDetails_Country CHECK (
        LEN(Country) = 2
    ),
    
    -- Currency code validation (ISO 4217)
    CONSTRAINT CK_CompanyBillingDetails_Currency CHECK (
        LEN(Currency) = 3
    ),
    
    -- If locked, FirstInvoiceDate must be set
    CONSTRAINT CK_CompanyBillingDetails_LockedIntegrity CHECK (
        (IsLocked = 0) OR (IsLocked = 1 AND FirstInvoiceDate IS NOT NULL)
    )
);
GO

-- Index for Tax ID lookup (replaces ABN unique index)
CREATE UNIQUE INDEX UX_CompanyBillingDetails_TaxID ON [CompanyBillingDetails](TaxID, Country);
-- ^ Composite unique index: Same Tax ID can exist for different countries
--   Example: EIN "12-3456789" for US company, completely different from AU ABN
GO

-- Index for country filtering ("Show all US customers", "Show all AU customers")
CREATE INDEX IX_CompanyBillingDetails_Country ON [CompanyBillingDetails](Country);
GO

-- Index for locked status (unchanged)
CREATE INDEX IX_CompanyBillingDetails_Locked ON [CompanyBillingDetails](IsLocked);
GO

PRINT 'CompanyBillingDetails table updated for international support!';
GO
```

---

### 3.2 New Table: `CountryTaxConfig` (Tax Rules Per Country)

```sql
-- =====================================================================
-- CountryTaxConfig - Tax Configuration Per Country
-- =====================================================================
-- Purpose: Centralize tax rules for each country (avoids hardcoding)
-- Enables: Add new countries without code changes
-- =====================================================================
CREATE TABLE [CountryTaxConfig] (
    CountryCode NVARCHAR(2) PRIMARY KEY,
    -- ^ ISO 3166-1 alpha-2 (AU, US, GB, DE, etc.)
    
    CountryName NVARCHAR(100) NOT NULL,
    -- ^ Full country name (Australia, United States, United Kingdom)
    
    Currency NVARCHAR(3) NOT NULL,
    -- ^ Default currency for country (ISO 4217: AUD, USD, GBP)
    
    TaxIDType NVARCHAR(20) NOT NULL,
    -- ^ Primary tax ID type (ABN, EIN, UTR, VAT)
    
    TaxIDFormat NVARCHAR(100) NULL,
    -- ^ Regex or description of format
    --   AU: "11 digits"
    --   US: "XX-XXXXXXX (9 digits)"
    --   GB: "10 digits or VAT format"
    
    TaxIDValidationAPI NVARCHAR(200) NULL,
    -- ^ API endpoint for validation (if available)
    --   AU: "https://abr.business.gov.au/abrxmlsearch"
    --   EU: "https://ec.europa.eu/taxation_customs/vies"
    --   US: NULL (no public API)
    
    TaxType NVARCHAR(20) NOT NULL,
    -- ^ Type of consumption tax (GST, VAT, Sales Tax)
    
    DefaultTaxRate DECIMAL(5, 2) NULL,
    -- ^ Default tax rate (e.g., 10.00 for AU GST, 20.00 for UK VAT)
    --   NULL if tax rate varies (US sales tax varies by state)
    
    TaxRateVariable BIT NOT NULL DEFAULT 0,
    -- ^ Does tax rate vary within country?
    --   0 = Fixed rate (AU: always 10%, UK: always 20%)
    --   1 = Variable rate (US: 0-10% by state, EU: 15-27% by country)
    
    RequiresStateProvince BIT NOT NULL DEFAULT 0,
    -- ^ Is State/Province required for addresses?
    --   1 = Yes (US, CA, AU)
    --   0 = No (most EU countries, UK)
    
    AddressFormat NVARCHAR(500) NULL,
    -- ^ Typical address format for country (informational)
    --   AU: "[AddressLine1], [City] [StateProvince] [PostalCode]"
    --   US: "[AddressLine1], [City], [StateProvince] [PostalCode]"
    --   UK: "[AddressLine1], [City], [PostalCode]"
    
    IsSupported BIT NOT NULL DEFAULT 1,
    -- ^ Is country currently supported by platform?
    --   1 = Supported (AU for MVP)
    --   0 = Not yet supported (coming soon)
    
    LaunchDate DATETIME2 NULL,
    -- ^ When country support launched (for analytics)
    
    Notes NVARCHAR(MAX) NULL,
    -- ^ Additional notes (compliance requirements, special rules)
    
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedDate DATETIME2 NULL
);
GO

-- Seed data: Australia (MVP)
INSERT INTO CountryTaxConfig (
    CountryCode, CountryName, Currency, TaxIDType, TaxIDFormat,
    TaxIDValidationAPI, TaxType, DefaultTaxRate, TaxRateVariable,
    RequiresStateProvince, AddressFormat, IsSupported, LaunchDate
) VALUES (
    'AU', 'Australia', 'AUD', 'ABN', '11 digits',
    'https://abr.business.gov.au/abrxmlsearch',
    'GST', 10.00, 0, 1,
    '[AddressLine1], [City] [StateProvince] [PostalCode]',
    1, '2025-10-01'
);

-- Seed data: United States (planned Phase 2)
INSERT INTO CountryTaxConfig (
    CountryCode, CountryName, Currency, TaxIDType, TaxIDFormat,
    TaxIDValidationAPI, TaxType, DefaultTaxRate, TaxRateVariable,
    RequiresStateProvince, AddressFormat, IsSupported, LaunchDate
) VALUES (
    'US', 'United States', 'USD', 'EIN', 'XX-XXXXXXX (9 digits)',
    NULL,  -- No public API
    'Sales Tax', NULL, 1,  -- Variable by state (0-10%)
    1,
    '[AddressLine1], [City], [StateProvince] [PostalCode]',
    0, NULL  -- Not yet supported
);

-- Seed data: United Kingdom (planned Phase 2)
INSERT INTO CountryTaxConfig (
    CountryCode, CountryName, Currency, TaxIDType, TaxIDFormat,
    TaxIDValidationAPI, TaxType, DefaultTaxRate, TaxRateVariable,
    RequiresStateProvince, AddressFormat, IsSupported, LaunchDate
) VALUES (
    'GB', 'United Kingdom', 'GBP', 'VAT', 'GB + 9-12 characters',
    'https://api.service.hmrc.gov.uk/organisations/vat',
    'VAT', 20.00, 0, 0,
    '[AddressLine1], [City], [PostalCode]',
    0, NULL  -- Not yet supported
);

GO
```

---

### 3.3 Migration Path (Alembic)

```python
"""
Add international support to CompanyBillingDetails

Revision ID: international_001
Revises: company_billing_001
Create Date: 2025-10-13
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Add new columns for international support
    op.add_column('CompanyBillingDetails', 
        sa.Column('Country', sa.String(2), nullable=False, server_default='AU'))
    
    op.add_column('CompanyBillingDetails',
        sa.Column('Currency', sa.String(3), nullable=False, server_default='AUD'))
    
    # Rename ABN → TaxID (data migration)
    op.add_column('CompanyBillingDetails',
        sa.Column('TaxID', sa.String(20), nullable=True))
    
    # Migrate existing ABN data to TaxID
    op.execute("UPDATE CompanyBillingDetails SET TaxID = ABN WHERE ABN IS NOT NULL")
    
    # Make TaxID NOT NULL after migration
    op.alter_column('CompanyBillingDetails', 'TaxID', nullable=False)
    
    # Add TaxIDType column
    op.add_column('CompanyBillingDetails',
        sa.Column('TaxIDType', sa.String(20), nullable=False, server_default='ABN'))
    
    # Rename GSTRegistered → TaxRegistered
    op.add_column('CompanyBillingDetails',
        sa.Column('TaxRegistered', sa.Boolean, nullable=False, server_default='0'))
    
    op.execute("UPDATE CompanyBillingDetails SET TaxRegistered = GSTRegistered")
    
    # Add new tax columns
    op.add_column('CompanyBillingDetails',
        sa.Column('TaxType', sa.String(20), nullable=True))
    
    op.add_column('CompanyBillingDetails',
        sa.Column('TaxRate', sa.Numeric(5, 2), nullable=True))
    
    # Migrate existing GST data
    op.execute("UPDATE CompanyBillingDetails SET TaxType = 'GST', TaxRate = 10.00 WHERE TaxRegistered = 1")
    
    # Split BillingAddress into structured fields
    op.add_column('CompanyBillingDetails',
        sa.Column('AddressLine1', sa.String(200), nullable=True))
    
    op.add_column('CompanyBillingDetails',
        sa.Column('AddressLine2', sa.String(200), nullable=True))
    
    op.add_column('CompanyBillingDetails',
        sa.Column('City', sa.String(100), nullable=True))
    
    op.add_column('CompanyBillingDetails',
        sa.Column('StateProvince', sa.String(100), nullable=True))
    
    op.add_column('CompanyBillingDetails',
        sa.Column('PostalCode', sa.String(20), nullable=True))
    
    # Manual migration needed for BillingAddress → structured fields
    # (Cannot be automated - requires address parsing)
    print("WARNING: Manual data migration required for BillingAddress → AddressLine1/City/StateProvince/PostalCode")
    
    # Add CountrySpecificData JSON column
    op.add_column('CompanyBillingDetails',
        sa.Column('CountrySpecificData', sa.Text, nullable=True))
    
    # Drop old columns (after data migration complete)
    # op.drop_column('CompanyBillingDetails', 'ABN')
    # op.drop_column('CompanyBillingDetails', 'ABNStatus')
    # op.drop_column('CompanyBillingDetails', 'GSTRegistered')
    # op.drop_column('CompanyBillingDetails', 'BillingAddress')
    
    # Create CountryTaxConfig table
    op.create_table(
        'CountryTaxConfig',
        sa.Column('CountryCode', sa.String(2), primary_key=True),
        sa.Column('CountryName', sa.String(100), nullable=False),
        sa.Column('Currency', sa.String(3), nullable=False),
        sa.Column('TaxIDType', sa.String(20), nullable=False),
        sa.Column('TaxIDFormat', sa.String(100), nullable=True),
        sa.Column('TaxIDValidationAPI', sa.String(200), nullable=True),
        sa.Column('TaxType', sa.String(20), nullable=False),
        sa.Column('DefaultTaxRate', sa.Numeric(5, 2), nullable=True),
        sa.Column('TaxRateVariable', sa.Boolean, nullable=False, default=False),
        sa.Column('RequiresStateProvince', sa.Boolean, nullable=False, default=False),
        sa.Column('AddressFormat', sa.String(500), nullable=True),
        sa.Column('IsSupported', sa.Boolean, nullable=False, default=True),
        sa.Column('LaunchDate', sa.DateTime, nullable=True),
        sa.Column('Notes', sa.Text, nullable=True),
        sa.Column('CreatedDate', sa.DateTime, nullable=False),
        sa.Column('UpdatedDate', sa.DateTime, nullable=True)
    )

def downgrade():
    # Reverse migration (if needed)
    pass
```

---

## 4. Tax ID Validation APIs by Country

### 4.1 Australia (ABN) - **Already Implemented**
- **API:** ABR (Australian Business Register)
- **Cost:** FREE
- **Coverage:** 100% of Australian businesses
- **Response Time:** ~500ms

### 4.2 European Union (VAT) - **VIES System**
```python
# EU VAT Validation via VIES API
import httpx
import xml.etree.ElementTree as ET

async def validate_eu_vat(vat_number: str, country_code: str) -> dict:
    """
    Validate EU VAT number via VIES (VAT Information Exchange System)
    
    Args:
        vat_number: VAT number without country code (e.g., "123456789")
        country_code: ISO country code (e.g., "DE", "FR", "NL")
        
    Returns:
        {
            "valid": True,
            "name": "COMPANY NAME GMBH",
            "address": "Street 123, 12345 City"
        }
    """
    endpoint = "https://ec.europa.eu/taxation_customs/vies/services/checkVatService"
    
    # SOAP request (VIES uses SOAP, not REST)
    soap_request = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
        <soapenv:Body>
            <checkVat xmlns="urn:ec.europa.eu:taxud:vies:services:checkVat:types">
                <countryCode>{country_code}</countryCode>
                <vatNumber>{vat_number}</vatNumber>
            </checkVat>
        </soapenv:Body>
    </soapenv:Envelope>
    """
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            endpoint,
            content=soap_request,
            headers={"Content-Type": "text/xml"}
        )
        
        root = ET.fromstring(response.text)
        # Parse SOAP response...
        
        return {
            "valid": True,  # Parsed from response
            "name": "COMPANY NAME",
            "address": "Street address"
        }
```

**VIES API Details:**
- **Cost:** FREE
- **Coverage:** All EU member states
- **Rate Limit:** No official limit (recommended < 1000/day)
- **Response Time:** ~1-2 seconds

### 4.3 United States (EIN) - **No Public API** ❌
- **IRS (US Tax Authority):** No public API for EIN validation
- **Options:**
  1. **Manual verification** (user enters EIN, no validation)
  2. **Third-party APIs** (TaxJar, Avalara - paid, $0.10-$0.50 per lookup)
  3. **IRS EIN Assistant** (web form, manual lookup only)

**Recommendation:** Accept EIN without validation (MVP), add third-party validation later (paid tier).

### 4.4 United Kingdom (UTR/VAT) - **HMRC API** (Paid)
- **HMRC (UK Tax Authority):** VAT validation API
- **Cost:** £0.50 per lookup (~$0.65 USD)
- **Registration:** OAuth2 application required

### 4.5 Canada (BN) - **No Public API** ❌
- Similar to US - no public API
- Accept manually entered Business Number

### 4.6 Summary: Tax ID Validation Availability

| Country | API Available | Cost | Recommendation |
|---------|---------------|------|----------------|
| **Australia** 🇦🇺 | ✅ ABR API | FREE | ✅ Validate (already implemented) |
| **EU (27 countries)** 🇪🇺 | ✅ VIES API | FREE | ✅ Validate (Phase 2) |
| **New Zealand** 🇳🇿 | ✅ NZBN API | FREE | ✅ Validate (Phase 2) |
| **United Kingdom** 🇬🇧 | ⚠️ HMRC API | £0.50/lookup | ⚠️ Optional (paid tier) |
| **United States** 🇺🇸 | ❌ No public API | - | ❌ Manual entry only (MVP) |
| **Canada** 🇨🇦 | ❌ No public API | - | ❌ Manual entry only (MVP) |
| **Singapore** 🇸🇬 | ⚠️ ACRA API | Paid | ⚠️ Optional (paid tier) |

---

## 5. Invoice Generation Changes

### 5.1 Multi-Currency Invoices

```python
# Invoice model additions
class Invoice(Base):
    __tablename__ = "invoices"
    
    invoice_id = Column(BigInteger, primary_key=True)
    company_id = Column(BigInteger, ForeignKey("Company.CompanyID"))
    
    # Currency fields (NEW)
    currency = Column(String(3), nullable=False)  # AUD, USD, GBP, EUR
    subtotal = Column(Numeric(10, 2), nullable=False)  # Amount before tax
    tax_amount = Column(Numeric(10, 2), nullable=False)  # Tax amount
    total = Column(Numeric(10, 2), nullable=False)  # Total amount
    
    # Tax details (NEW)
    tax_type = Column(String(20), nullable=False)  # GST, VAT, Sales Tax
    tax_rate = Column(Numeric(5, 2), nullable=False)  # 10.00, 20.00, etc.
    tax_id = Column(String(20), nullable=False)  # ABN, VAT, EIN
    
    # ... other fields


# Invoice PDF generation
def generate_invoice_pdf(invoice: Invoice) -> bytes:
    """Generate PDF invoice with country-specific formatting"""
    
    billing = invoice.company.billing_details
    
    if billing.country == 'AU':
        # Australian tax invoice
        return generate_australian_gst_invoice(invoice, billing)
    
    elif billing.country in ['GB', 'DE', 'FR', 'NL']:  # EU countries
        # EU VAT invoice
        return generate_eu_vat_invoice(invoice, billing)
    
    elif billing.country == 'US':
        # US sales tax invoice (varies by state)
        return generate_us_sales_tax_invoice(invoice, billing)
    
    else:
        # Generic invoice (fallback)
        return generate_generic_invoice(invoice, billing)
```

### 5.2 Country-Specific Invoice Templates

**Australian GST Invoice:**
```
TAX INVOICE

From:
EventLead Platform Pty Ltd
ABN: 12 345 678 901
123 Tech Street, Sydney NSW 2000

To:
ICC SYDNEY PTY LTD
ABN: 53 004 085 616
14 Darling Drive, Sydney NSW 2000

Invoice Number: INV-2025-001
Date: 13 October 2025

Item                     Qty    Unit Price (ex GST)    Amount
Form Publication          3     $90.00 AUD             $270.00

Subtotal (ex GST):                                    $270.00
GST (10%):                                             $27.00
──────────────────────────────────────────────────────────
Total (inc GST):                                      $297.00 AUD

This is a tax invoice for GST purposes.
```

**UK VAT Invoice:**
```
VAT INVOICE

From:
EventLead Platform Ltd
VAT Number: GB123456789
Company Number: 12345678
123 Tech Road, London EC1A 1BB

To:
EXAMPLE COMPANY LTD
VAT Number: GB987654321
456 Business Street, London W1A 1AA

Invoice Number: INV-2025-001
Date: 13 October 2025

Description              Qty    Unit Price (ex VAT)    Amount
Form Publication          3     £75.00 GBP             £225.00

Net Total:                                            £225.00
VAT @ 20%:                                             £45.00
──────────────────────────────────────────────────────────
Gross Total:                                          £270.00 GBP

VAT is charged at the standard UK rate of 20%.
```

---

## 6. Address Validation & Formatting

### 6.1 Country-Specific Address Formats

```python
# Address formatting service
class AddressFormatter:
    """Format addresses according to country conventions"""
    
    def format_address(self, billing: CompanyBillingDetails) -> str:
        """
        Format address for invoice/display based on country
        """
        if billing.country == 'AU':
            # Australian format: "14 Darling Drive, Sydney NSW 2000"
            return f"{billing.address_line1}, {billing.city} {billing.state_province} {billing.postal_code}"
        
        elif billing.country == 'US':
            # US format: "123 Main Street, Suite 400, San Francisco, CA 94102"
            line2 = f", {billing.address_line2}" if billing.address_line2 else ""
            return f"{billing.address_line1}{line2}, {billing.city}, {billing.state_province} {billing.postal_code}"
        
        elif billing.country == 'GB':
            # UK format: "10 Downing Street, London SW1A 2AA"
            return f"{billing.address_line1}, {billing.city}, {billing.postal_code}"
        
        elif billing.country in ['DE', 'FR', 'NL']:  # EU countries
            # EU format varies, but generally: "Street, Postal Code City"
            return f"{billing.address_line1}, {billing.postal_code} {billing.city}"
        
        else:
            # Generic fallback
            parts = [billing.address_line1, billing.city, billing.state_province, billing.postal_code]
            return ", ".join([p for p in parts if p])
```

---

## 7. Implementation Roadmap

### Phase 1: MVP (Australia Only) - **Already Complete** ✅
- ✅ ABN validation via ABR API
- ✅ Australian GST invoicing (10%)
- ✅ AUD currency only
- ✅ Australian address format

### Phase 2: Schema International-Ready (NOW) - **2 weeks**
- [ ] Rename fields: ABN → TaxID, GSTRegistered → TaxRegistered
- [ ] Add Country, Currency fields
- [ ] Split BillingAddress → AddressLine1, City, StateProvince, PostalCode
- [ ] Create CountryTaxConfig table
- [ ] Alembic migration (backward compatible)
- [ ] Update business logic to use Country field

**Effort:** 2 weeks (schema changes, data migration, testing)  
**Risk:** Low (backward compatible with AU data)

### Phase 3: EU Expansion - **4 weeks**
- [ ] VIES API integration (EU VAT validation)
- [ ] Multi-currency support (EUR, GBP)
- [ ] EU VAT invoice template (20% VAT)
- [ ] Address formatting (EU countries)
- [ ] Country selector in signup flow

**Launch Countries:** UK, Germany, France, Netherlands  
**Effort:** 4 weeks (VIES API, invoice templates, testing)

### Phase 4: US Expansion - **6 weeks**
- [ ] US address validation (USPS API optional)
- [ ] USD currency support
- [ ] Sales tax calculation (state-specific)
- [ ] US invoice template (no federal tax, state tax varies)
- [ ] Manual EIN entry (no validation API)

**Complexity:** High (50 states, variable sales tax rates)  
**Effort:** 6 weeks (sales tax rules complex)

### Phase 5: Asia-Pacific - **3 weeks per country**
- [ ] New Zealand (NZBN API, 15% GST)
- [ ] Singapore (UEN, 8% GST)
- [ ] Canada (BN, 5-15% GST/HST)

---

## 8. Risk Analysis & Mitigation

### Risk 1: Tax Compliance Errors (HIGH)
**Risk:** Incorrect tax rates, missing tax IDs on invoices → legal penalties

**Mitigation:**
- ✅ CountryTaxConfig table (centralized tax rules)
- ✅ Tax ID validation APIs where available (AU, EU, NZ)
- ✅ Country-specific invoice templates reviewed by tax professional
- ✅ Manual review: Accountant reviews first 10 invoices per new country

### Risk 2: Currency Conversion Errors (MEDIUM)
**Risk:** Invoice amounts in wrong currency, exchange rate disputes

**Mitigation:**
- ✅ Currency locked at time of invoice (no retroactive conversion)
- ✅ Display currency prominently: "$297.00 AUD" not just "$297"
- ✅ Use Stripe for multi-currency payments (handles conversion)
- ✅ Never auto-convert currencies (user selects currency at signup)

### Risk 3: Address Format Errors (LOW)
**Risk:** Addresses formatted incorrectly for country (postal delivery fails)

**Mitigation:**
- ✅ Structured address fields (not single text field)
- ✅ Country-specific address formatting (AddressFormatter service)
- ✅ Address validation APIs (Google Maps, USPS) optional
- ✅ User can edit formatted address before save

### Risk 4: Tax ID Validation API Downtime (MEDIUM)
**Risk:** ABR/VIES API down → users can't complete signup

**Mitigation:**
- ✅ Fallback: Accept manual entry if API fails (mark as "Unverified")
- ✅ Retry logic: 3 retries with exponential backoff
- ✅ Admin review: Flag "Unverified" tax IDs for manual verification
- ✅ Cache validation results (30 days) to reduce API dependency

---

## 9. Cost Analysis (International)

### API Costs by Country:

| Country | Validation API | Cost per Lookup | Annual Cost (1000 companies) |
|---------|----------------|-----------------|------------------------------|
| **Australia** 🇦🇺 | ABR (FREE) | $0 | $0 |
| **EU (27)** 🇪🇺 | VIES (FREE) | $0 | $0 |
| **New Zealand** 🇳🇿 | NZBN (FREE) | $0 | $0 |
| **United Kingdom** 🇬🇧 | HMRC (paid) | £0.50 (~$0.65) | $650 |
| **United States** 🇺🇸 | Third-party (optional) | $0.10-$0.50 | $100-$500 (if used) |
| **Canada** 🇨🇦 | None | $0 | $0 |

**Total Annual Cost (if validating all):** ~$750-$1,150

**Recommendation:** Only validate where FREE APIs available (AU, EU, NZ). Manual entry for US/UK/CA.

---

## 10. Next Steps

### Immediate Actions (Phase 2 - Schema Changes):
1. ✅ **Review this guide** with team (dev, product, finance)
2. ✅ **Approve schema changes** (rename ABN → TaxID, add Country/Currency)
3. ✅ **Create Alembic migration** (backward compatible)
4. ✅ **Test migration** on staging environment (existing AU data)
5. ✅ **Update business logic** to use Country field
6. ✅ **Deploy to production** (no user-facing changes yet)

**Timeline:** 2 weeks  
**Effort:** 40-60 hours (schema, migration, testing)

### Questions for Decision:
1. **Which countries to launch first?** (UK, EU, US, NZ?)
2. **MVP tax validation strategy:** Validate all (expensive) or only free APIs (AU, EU, NZ)?
3. **Currency strategy:** Lock at signup or allow user to change later?
4. **Address validation:** Use third-party APIs (Google Maps, USPS) or manual entry only?

---

## Summary

**Schema changes proposed:**
- ✅ Generic field names (TaxID, TaxRegistered, TaxType)
- ✅ Country & Currency fields (ISO standards)
- ✅ Structured addresses (not single text field)
- ✅ CountryTaxConfig table (centralized tax rules)
- ✅ Extensible design (CountrySpecificData JSON field)

**Benefits:**
- ✅ **Future-proof:** Add new countries without schema changes
- ✅ **Backward compatible:** Existing AU data migrates seamlessly
- ✅ **Scalable:** Supports 100+ countries with same schema
- ✅ **Compliant:** Country-specific tax rules enforced

**Ready to proceed with Phase 2 schema changes?** Let me know if you have questions!

---

*Dimitri - Data Domain Architect* 🔍  
*"Building for Australia today, the world tomorrow"*

