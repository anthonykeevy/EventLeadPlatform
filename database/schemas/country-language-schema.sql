-- =====================================================================
-- Country & Language Domain Schema - Reference Data Tables
-- =====================================================================
-- Author: Dimitri (Data Domain Architect)
-- Date: October 13, 2025
-- Version: 1.0.0
-- =====================================================================
-- Purpose:
--   Reference data tables for countries and languages.
--   Separate domains (not embedded in Company table).
--   MVP: Australia-only, but designed for international expansion.
-- 
-- Strategy:
--   - Country table: ISO 3166-1 standard (alpha-2 codes)
--   - Language table: ISO 639-1 standard (alpha-2 codes)
--   - CompanyBillingDetails.Country → FK to Country table
--   - Future: User language preferences, localized content
--
-- Standards:
--   - PascalCase naming (Solomon's requirement)
--   - NVARCHAR for text (UTF-8 support)
--   - DATETIME2 with UTC timestamps
--   - Soft deletes (IsDeleted flag)
--   - Full audit trail on all tables
-- =====================================================================

USE [EventLeadPlatform];
GO

-- =====================================================================
-- TABLE: Country (ISO 3166-1 Reference Data)
-- =====================================================================
CREATE TABLE [Country] (
    -- =====================================================================
    -- Primary Key (Surrogate Key)
    -- =====================================================================
    CountryID BIGINT IDENTITY(1,1) PRIMARY KEY,
    -- ^ Surrogate key for foreign key relationships
    -- Used for: FK references, joins, performance
    
    -- =====================================================================
    -- ISO Standard Code
    -- =====================================================================
    CountryCode NVARCHAR(2) NOT NULL UNIQUE,
    -- ^ ISO 3166-1 alpha-2 code (AU, US, GB, DE, FR, etc.)
    -- Why alpha-2 not alpha-3? Shorter, more common in APIs (Stripe, tax APIs)
    
    -- =====================================================================
    -- Country Details
    -- =====================================================================
    CountryName NVARCHAR(100) NOT NULL,
    -- ^ Full country name in English (e.g., "Australia", "United States")
    
    CountryNameLocal NVARCHAR(100) NULL,
    -- ^ Country name in local language (optional, future feature)
    -- Example: Deutschland (Germany), 日本 (Japan)
    
    Region NVARCHAR(50) NULL,
    -- ^ Geographic region: "Asia-Pacific", "Europe", "North America", "South America", "Africa", "Middle East"
    -- Used for: Regional filtering, analytics
    
    Continent NVARCHAR(20) NULL,
    -- ^ Continent: "Asia", "Europe", "North America", "South America", "Africa", "Oceania", "Antarctica"
    
    -- =====================================================================
    -- Currency (ISO 4217)
    -- =====================================================================
    CurrencyCode NVARCHAR(3) NOT NULL,
    -- ^ ISO 4217 currency code (AUD, USD, GBP, EUR)
    -- One-to-one with country for MVP (future: countries with multiple currencies)
    
    CurrencyName NVARCHAR(50) NOT NULL,
    -- ^ Currency name (e.g., "Australian Dollar", "US Dollar")
    
    CurrencySymbol NVARCHAR(5) NULL,
    -- ^ Currency symbol ($, £, €, ¥)
    
    -- =====================================================================
    -- Tax System Details
    -- =====================================================================
    TaxIDType NVARCHAR(20) NULL,
    -- ^ Primary tax ID type: 'ABN', 'EIN', 'VAT', 'UTR', 'BN', 'NZBN'
    -- Used for: Validation rules, invoice requirements
    
    TaxIDLabel NVARCHAR(50) NULL,
    -- ^ Human-readable label for tax ID (e.g., "ABN", "Tax ID", "VAT Number")
    -- Used for: Form labels ("Enter your ABN" vs "Enter your EIN")
    
    TaxIDFormat NVARCHAR(100) NULL,
    -- ^ Format description or regex
    -- Example: "11 digits" (AU), "XX-XXXXXXX" (US), "GB + 9-12 characters" (UK)
    
    TaxIDValidationAPI NVARCHAR(200) NULL,
    -- ^ API endpoint for tax ID validation (if available)
    -- Example: "https://abr.business.gov.au" (AU), NULL (US - no public API)
    
    ConsumptionTaxName NVARCHAR(50) NULL,
    -- ^ Name of consumption tax: "GST", "VAT", "Sales Tax"
    
    ConsumptionTaxRate DECIMAL(5, 2) NULL,
    -- ^ Default consumption tax rate (e.g., 10.00 for AU GST, 20.00 for UK VAT)
    -- NULL if variable (e.g., US sales tax varies by state)
    
    ConsumptionTaxVariable BIT NOT NULL DEFAULT 0,
    -- ^ Does tax rate vary within country?
    -- 0 = Fixed rate (AU: always 10%)
    -- 1 = Variable rate (US: 0-10% by state)
    
    -- =====================================================================
    -- Address Format
    -- =====================================================================
    AddressFormat NVARCHAR(500) NULL,
    -- ^ Typical address format for country (informational)
    -- Example: "[AddressLine1], [City] [StateProvince] [PostalCode]" (AU)
    
    RequiresStateProvince BIT NOT NULL DEFAULT 0,
    -- ^ Is State/Province required in addresses?
    -- 1 = Yes (US, AU, CA)
    -- 0 = No (most EU countries, UK)
    
    PostalCodeLabel NVARCHAR(50) NULL,
    -- ^ Label for postal code field
    -- Example: "Postcode" (AU/UK), "ZIP Code" (US), "Postal Code" (CA)
    
    PostalCodeFormat NVARCHAR(100) NULL,
    -- ^ Postal code format description
    -- Example: "4 digits" (AU), "5 digits" (US), "Alphanumeric" (UK)
    
    -- =====================================================================
    -- Phone Format & Validation
    -- =====================================================================
    PhoneCountryCode NVARCHAR(5) NULL,
    -- ^ International dialing code (e.g., "+61" for AU, "+1" for US, "+44" for UK)
    
    PhoneLandlineRegex NVARCHAR(500) NULL,
    -- ^ Regex pattern for landline validation
    -- AU: "^\+61\s?[2378]\s?\d{4}\s?\d{4}$" (area code 2,3,7,8)
    -- US: "^\+1\s?\([2-9]\d{2}\)\s?\d{3}-?\d{4}$"
    -- UK: "^\+44\s?[1-9]\d{8,9}$"
    
    PhoneMobileRegex NVARCHAR(500) NULL,
    -- ^ Regex pattern for mobile validation
    -- AU: "^\+61\s?4\d{2}\s?\d{3}\s?\d{3}$" (04XX XXX XXX)
    -- US: Same as landline (no distinction in North America)
    -- UK: "^\+44\s?7\d{9}$" (07XXX XXXXXX)
    
    PhoneFreeCallRegex NVARCHAR(500) NULL,
    -- ^ Regex pattern for toll-free/free call numbers
    -- AU: "^(1800|1300)\s?\d{3}\s?\d{3}$" (1800 XXX XXX or 1300 XXX XXX)
    -- US: "^\+1\s?(800|888|877|866|855|844|833)\s?\d{3}\s?\d{4}$"
    -- UK: "^\+44\s?(800|808)\s?\d{6,7}$"
    
    PhoneSpecialRegex NVARCHAR(500) NULL,
    -- ^ Regex pattern for special short codes (6 digits, premium, emergency)
    -- AU: "^(13\s?\d{4}|1900\s?\d{6})$" (13XXXX or 1900 XXX XXX premium)
    -- Emergency: 000, 112 (not validated - too sensitive)
    -- US: "^\d{5,6}$" (5-6 digit short codes)
    
    PhoneFormatExample NVARCHAR(200) NULL,
    -- ^ Human-readable format examples (informational, for UI hints)
    -- AU: "Landline: +61 2 9215 7100, Mobile: +61 400 123 456, Free: 1800 123 456"
    -- US: "Phone: +1 (555) 123-4567, Toll-free: +1 (800) 555-1234"
    
    -- =====================================================================
    -- Platform Support Status
    -- =====================================================================
    IsSupported BIT NOT NULL DEFAULT 0,
    -- ^ Is country currently supported by platform?
    -- 1 = Supported (Australia for MVP)
    -- 0 = Coming soon (future markets)
    
    LaunchDate DATETIME2 NULL,
    -- ^ When country support launched (UTC)
    -- Used for: Analytics, "Launched in AU: Oct 2025"
    
    SupportPriority INT NULL,
    -- ^ Launch priority (1 = highest, 10 = lowest)
    -- Used for: Roadmap planning
    -- Example: 1 = AU (MVP), 2 = UK, 3 = US, 4 = NZ, 5 = EU
    
    -- =====================================================================
    -- Localization
    -- =====================================================================
    DefaultLanguageCode NVARCHAR(2) NULL,
    -- ^ Default language for country (ISO 639-1)
    -- Example: "en" (AU, US, UK), "de" (Germany), "fr" (France)
    -- Foreign key to Language table
    
    Locale NVARCHAR(10) NULL,
    -- ^ BCP 47 locale code (language + region)
    -- Example: "en-AU" (Australian English), "en-US" (US English), "fr-FR" (France French)
    
    DateFormat NVARCHAR(20) NULL,
    -- ^ Typical date format for country
    -- Example: "DD/MM/YYYY" (AU/UK), "MM/DD/YYYY" (US)
    
    TimeFormat NVARCHAR(20) NULL,
    -- ^ Typical time format: "24-hour" or "12-hour"
    
    -- =====================================================================
    -- Metadata
    -- =====================================================================
    Notes NVARCHAR(MAX) NULL,
    -- ^ Additional notes (compliance requirements, special considerations)
    -- Example: "GDPR compliance required" (EU), "State sales tax varies" (US)
    
    -- =====================================================================
    -- Audit Trail (Standard for ALL tables - Solomon's requirement)
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NOT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT FK_Country_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [User](UserID),
    CONSTRAINT FK_Country_UpdatedBy FOREIGN KEY (UpdatedBy) REFERENCES [User](UserID),
    CONSTRAINT FK_Country_DeletedBy FOREIGN KEY (DeletedBy) REFERENCES [User](UserID),
    CONSTRAINT FK_Country_DefaultLanguage FOREIGN KEY (DefaultLanguageCode) REFERENCES [Language](LanguageCode),
    
    -- Country code validation (ISO 3166-1 alpha-2 = 2 uppercase letters)
    CONSTRAINT CK_Country_Code CHECK (
        LEN(CountryCode) = 2 AND CountryCode = UPPER(CountryCode)
    ),
    
    -- Currency code validation (ISO 4217 = 3 uppercase letters)
    CONSTRAINT CK_Country_Currency CHECK (
        LEN(CurrencyCode) = 3 AND CurrencyCode = UPPER(CurrencyCode)
    )
);
GO

-- Index for country name search/autocomplete
CREATE INDEX IX_Country_Name ON [Country](CountryName, IsDeleted)
    WHERE IsDeleted = 0;
GO

-- Index for supported countries (active dropdown in UI)
CREATE INDEX IX_Country_Supported ON [Country](IsSupported, IsDeleted)
    WHERE IsDeleted = 0 AND IsSupported = 1;
GO

PRINT 'Country table created successfully!';
GO

-- =====================================================================
-- TABLE: Language (ISO 639-1 Reference Data)
-- =====================================================================
CREATE TABLE [Language] (
    -- =====================================================================
    -- Primary Key (Surrogate Key)
    -- =====================================================================
    LanguageID BIGINT IDENTITY(1,1) PRIMARY KEY,
    -- ^ Surrogate key for foreign key relationships
    -- Used for: FK references, joins, performance
    
    -- =====================================================================
    -- ISO Standard Code
    -- =====================================================================
    LanguageCode NVARCHAR(2) NOT NULL UNIQUE,
    -- ^ ISO 639-1 alpha-2 code (en, de, fr, es, ja, zh, etc.)
    -- Why alpha-2 not alpha-3? Shorter, matches HTML lang attribute
    
    -- =====================================================================
    -- Language Details
    -- =====================================================================
    LanguageName NVARCHAR(100) NOT NULL,
    -- ^ Language name in English (e.g., "English", "German", "French")
    
    LanguageNameLocal NVARCHAR(100) NULL,
    -- ^ Language name in native script (optional)
    -- Example: Deutsch (German), Français (French), 日本語 (Japanese)
    
    LanguageFamily NVARCHAR(50) NULL,
    -- ^ Language family: "Germanic", "Romance", "Slavic", "Sino-Tibetan", "Japonic"
    -- Used for: Linguistic analysis, grouping
    
    Direction NVARCHAR(3) NOT NULL DEFAULT 'LTR',
    -- ^ Text direction: 'LTR' (left-to-right) or 'RTL' (right-to-left)
    -- LTR: English, German, French, Spanish (most languages)
    -- RTL: Arabic, Hebrew
    
    -- =====================================================================
    -- Platform Support Status
    -- =====================================================================
    IsSupported BIT NOT NULL DEFAULT 0,
    -- ^ Is language currently supported by platform?
    -- 1 = Supported (English for MVP)
    -- 0 = Coming soon (future translations)
    
    TranslationCompleteness INT NULL,
    -- ^ Percentage of UI translated (0-100)
    -- Example: 100 = fully translated, 50 = partially translated
    
    LaunchDate DATETIME2 NULL,
    -- ^ When language support launched (UTC)
    
    SupportPriority INT NULL,
    -- ^ Translation priority (1 = highest, 10 = lowest)
    -- Example: 1 = English (MVP), 2 = Spanish, 3 = French, 4 = German
    
    -- =====================================================================
    -- Localization Details
    -- =====================================================================
    PluralRules NVARCHAR(500) NULL,
    -- ^ Plural rules for translations (JSON)
    -- Example: {"zero": "no items", "one": "1 item", "other": "{n} items"}
    -- Used for: Proper pluralization in UI strings
    
    DateFormatExample NVARCHAR(50) NULL,
    -- ^ Example date format in this language
    -- Example: "13/10/2025" (en-AU), "10/13/2025" (en-US)
    
    NumberFormat NVARCHAR(50) NULL,
    -- ^ Number format: "1,234.56" (English) vs "1.234,56" (German)
    
    -- =====================================================================
    -- Metadata
    -- =====================================================================
    Notes NVARCHAR(MAX) NULL,
    -- ^ Additional notes (translation considerations, special requirements)
    
    -- =====================================================================
    -- Audit Trail (Standard for ALL tables - Solomon's requirement)
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NOT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT FK_Language_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [User](UserID),
    CONSTRAINT FK_Language_UpdatedBy FOREIGN KEY (UpdatedBy) REFERENCES [User](UserID),
    CONSTRAINT FK_Language_DeletedBy FOREIGN KEY (DeletedBy) REFERENCES [User](UserID),
    
    -- Language code validation (ISO 639-1 alpha-2 = 2 lowercase letters)
    CONSTRAINT CK_Language_Code CHECK (
        LEN(LanguageCode) = 2 AND LanguageCode = LOWER(LanguageCode)
    ),
    
    -- Direction validation
    CONSTRAINT CK_Language_Direction CHECK (
        Direction IN ('LTR', 'RTL')
    )
);
GO

-- Index for language name search
CREATE INDEX IX_Language_Name ON [Language](LanguageName, IsDeleted)
    WHERE IsDeleted = 0;
GO

-- Index for supported languages (active dropdown in UI)
CREATE INDEX IX_Language_Supported ON [Language](IsSupported, IsDeleted)
    WHERE IsDeleted = 0 AND IsSupported = 1;
GO

PRINT 'Language table created successfully!';
GO

-- =====================================================================
-- SEED DATA: Australia (MVP)
-- =====================================================================

-- Insert Australia (MVP supported country)
INSERT INTO [Country] (
    CountryCode, CountryName, Region, Continent,
    CurrencyCode, CurrencyName, CurrencySymbol,
    TaxIDType, TaxIDLabel, TaxIDFormat, TaxIDValidationAPI,
    ConsumptionTaxName, ConsumptionTaxRate, ConsumptionTaxVariable,
    AddressFormat, RequiresStateProvince, PostalCodeLabel, PostalCodeFormat,
    PhoneCountryCode, PhoneLandlineRegex, PhoneMobileRegex, PhoneFreeCallRegex, PhoneSpecialRegex, PhoneFormatExample,
    IsSupported, LaunchDate, SupportPriority,
    DefaultLanguageCode, Locale, DateFormat, TimeFormat,
    Notes,
    CreatedBy
) VALUES (
    'AU', 'Australia', 'Asia-Pacific', 'Oceania',
    'AUD', 'Australian Dollar', '$',
    'ABN', 'ABN (Australian Business Number)', '11 digits', 'https://abr.business.gov.au/abrxmlsearch',
    'GST', 10.00, 0,
    '[AddressLine1], [City] [StateProvince] [PostalCode]', 1, 'Postcode', '4 digits',
    '+61', 
    '^\+61\s?[2378]\s?\d{4}\s?\d{4}$',  -- Landline: +61 2 9215 7100 (NSW), +61 3 XXXX XXXX (VIC), +61 7 XXXX XXXX (QLD), +61 8 XXXX XXXX (SA/WA/NT)
    '^\+61\s?4\d{2}\s?\d{3}\s?\d{3}$',  -- Mobile: +61 4XX XXX XXX (04XX XXX XXX without +61)
    '^(1800|1300)\s?\d{3}\s?\d{3}$',    -- Free call: 1800 123 456 (toll-free) or 1300 123 456 (local rate)
    '^(13\s?\d{4}|1900\s?\d{6})$',      -- Special: 13XXXX (6 digits) or 1900 XXX XXX (premium rate)
    'Landline: +61 2 9215 7100 | Mobile: +61 400 123 456 | Free call: 1800 123 456 | Special: 13 1234',
    1, '2025-10-01', 1,
    'en', 'en-AU', 'DD/MM/YYYY', '24-hour',
    'MVP launch market. ABN validation via ABR API (FREE). GST compliance required for invoices.',
    1  -- System user
);

-- Insert English (MVP supported language)
INSERT INTO [Language] (
    LanguageCode, LanguageName, LanguageNameLocal, LanguageFamily, Direction,
    IsSupported, TranslationCompleteness, LaunchDate, SupportPriority,
    PluralRules, DateFormatExample, NumberFormat,
    Notes,
    CreatedBy
) VALUES (
    'en', 'English', 'English', 'Germanic', 'LTR',
    1, 100, '2025-10-01', 1,
    '{"one": "1 item", "other": "{n} items"}', '13/10/2025', '1,234.56',
    'Primary platform language. Australian English dialect (en-AU) for MVP.',
    1  -- System user
);

GO

PRINT '========================================';
PRINT 'Country & Language Domain Complete!';
PRINT '========================================';
PRINT 'Tables Created:';
PRINT '  1. Country (30 fields) - ISO 3166-1';
PRINT '  2. Language (17 fields) - ISO 639-1';
PRINT '';
PRINT 'Seed Data:';
PRINT '  ✅ Australia (AU) - Supported, GST 10%';
PRINT '  ✅ English (en) - Supported, 100% complete';
PRINT '';
PRINT 'Key Features:';
PRINT '  ✅ ISO standard codes (CountryCode, LanguageCode)';
PRINT '  ✅ Tax system details (ABN, GST, validation API)';
PRINT '  ✅ Currency aligned with country (AUD for AU)';
PRINT '  ✅ Address format specifications';
PRINT '  ✅ Full audit trails (Solomon standards)';
PRINT '  ✅ International-ready (add countries without schema changes)';
PRINT '';
PRINT 'Next Steps:';
PRINT '  1. Update CompanyBillingDetails to FK Country.CountryCode';
PRINT '  2. Validate with Solomon (Database Migration Validator)';
PRINT '  3. Add future countries as IsSupported=0 (not active yet)';
PRINT '========================================';
GO

