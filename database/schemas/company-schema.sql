-- =====================================================================
-- Company Domain Schema - Multi-Context Normalized Design
-- =====================================================================
-- Author: Dimitri (Data Domain Architect)
-- Date: October 13, 2025
-- Version: 1.0.0
-- =====================================================================
-- Purpose:
--   Supports EventLead Platform's Company domain with THREE overlapping contexts:
--   1. Event Organizers (B2B - companies that RUN events like ICC Sydney)
--   2. SaaS Customers (multi-tenant - companies that SUBSCRIBE to platform)
--   3. Billing Entities (invoicing - companies we INVOICE for Australian tax compliance)
-- 
-- Strategy:
--   Hybrid normalized approach:
--   - ONE core Company table (single source of truth)
--   - THREE extension tables (role-specific context):
--     • CompanyCustomerDetails (multi-tenant SaaS context)
--     • CompanyBillingDetails (Australian tax compliance context)
--     • CompanyOrganizerDetails (event organizer B2B context)
--
-- Standards:
--   - PascalCase naming (Solomon's requirement)
--   - NVARCHAR for text (UTF-8 support)
--   - DATETIME2 with UTC timestamps
--   - Soft deletes (IsDeleted flag)
--   - Full audit trail on all tables
-- =====================================================================
-- Industry Research:
--   - Salesforce: Single Account table with flexible roles (inspired our core design)
--   - Stripe + Xero: Separate billing entities (inspired extension tables)
--   - Eventbrite: Public organizer profiles (inspired OrganizerDetails)
--   - ABN Lookup API: Australian Business Register for tax compliance
-- =====================================================================

USE [EventLeadPlatform];
GO

-- =====================================================================
-- TABLE 1: Company (Core Entity - Universal Company Data)
-- =====================================================================
CREATE TABLE [Company] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    CompanyID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Company Identity (Universal Fields - Applicable to ALL Roles)
    -- =====================================================================
    DisplayName NVARCHAR(200) NOT NULL,
    -- ^ Primary display name (user's choice)
    -- Used for: Event cards, dashboards, search results, user-facing lists
    -- Can be: Legal name, business name, or custom override
    -- Example: "ICC Sydney" (user-friendly)
    
    LegalEntityName NVARCHAR(200) NOT NULL,
    -- ^ Legal entity name from ABR API (Australian Business Register)
    -- Used for: Tax invoices, legal documents, contracts, ATO compliance
    -- Example: "INTERNATIONAL CONVENTION CENTRE SYDNEY PTY LTD"
    -- Source: ABR <mainName><organisationName>
    -- NOT NULL: All companies must have legal entity name
    
    BusinessNames NVARCHAR(MAX) NULL,
    -- ^ JSON array of current business names from ABR API
    -- Used for: Dropdown selection, name validation, user choice
    -- Example: ["ICC SYDNEY", "SYDNEY CONVENTION CENTRE"]
    -- Source: ABR <businessName><organisationName> (current only)
    -- NULL: No registered business names (sole traders, etc.)
    
    CustomDisplayName NVARCHAR(200) NULL,
    -- ^ User-defined display name (override)
    -- Used when: User wants different name than ABR provides
    -- Example: "ICC Sydney Events" (custom branding)
    -- NULL = Use DisplayName (default behavior)
    
    DisplayNameSource NVARCHAR(20) NOT NULL DEFAULT 'User',
    -- ^ Source of DisplayName: 'Legal', 'Business', 'Custom', 'User'
    -- Used for: Audit trail, data quality, name change tracking
    -- 'Legal' = LegalEntityName (fallback)
    -- 'Business' = First business name from BusinessNames (preferred)
    -- 'Custom' = CustomDisplayName (user override)
    -- 'User' = User-selected from available options (default)
    
    Website NVARCHAR(500) NULL,
    -- ^ Company website URL (https://iccsydney.com)
    -- Optional. Used for organizer profiles, trust signals
    
    Phone NVARCHAR(20) NULL,
    -- ^ Primary contact phone number (international format: +61 2 9215 7100)
    -- Optional. Useful for organizers, customer support
    
    Industry NVARCHAR(100) NULL,
    -- ^ Industry classification (e.g., "Events & Exhibitions", "Technology", "Healthcare")
    -- Used for filtering, analytics, market segmentation
    
    -- =====================================================================
    -- Hierarchical Relationships (Parent-Subsidiary Support)
    -- =====================================================================
    ParentCompanyID BIGINT NULL,
    -- ^ Foreign key to parent company (for subsidiaries)
    -- Example: "Acme Events" (child) → "Acme Holdings" (parent)
    -- NULL = top-level company (no parent)
    -- Enables: "Show all subsidiaries of Acme Holdings"
    -- Billing use case: Subsidiary invoices go to parent company
    
    -- =====================================================================
    -- Audit Trail (Standard for ALL tables - Solomon's requirement)
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    -- ^ Record creation timestamp (UTC)
    
    CreatedBy BIGINT NOT NULL,
    -- ^ UserID who created this record (foreign key to User table)
    
    UpdatedDate DATETIME2 NULL,
    -- ^ Last update timestamp (UTC)
    
    UpdatedBy BIGINT NULL,
    -- ^ UserID who last updated this record
    
    IsDeleted BIT NOT NULL DEFAULT 0,
    -- ^ Soft delete flag (0 = active, 1 = deleted)
    -- Retain historical data for audit trail
    
    DeletedDate DATETIME2 NULL,
    -- ^ Deletion timestamp (UTC)
    
    DeletedBy BIGINT NULL,
    -- ^ UserID who soft-deleted this record
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT FK_Company_Parent FOREIGN KEY (ParentCompanyID) REFERENCES [Company](CompanyID),
    CONSTRAINT FK_Company_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [User](UserID),
    CONSTRAINT FK_Company_UpdatedBy FOREIGN KEY (UpdatedBy) REFERENCES [User](UserID),
    CONSTRAINT FK_Company_DeletedBy FOREIGN KEY (DeletedBy) REFERENCES [User](UserID),
    
    -- Audit trail consistency
    CONSTRAINT CK_Company_AuditDates CHECK (
        CreatedDate <= ISNULL(UpdatedDate, '9999-12-31') AND
        CreatedDate <= ISNULL(DeletedDate, '9999-12-31')
    ),
    
    -- Prevent circular parent relationships (company cannot be its own parent)
    CONSTRAINT CK_Company_NoSelfParent CHECK (ParentCompanyID != CompanyID),
    
    -- Validate DisplayNameSource values
    CONSTRAINT CK_Company_DisplayNameSource CHECK (
        DisplayNameSource IN ('Legal', 'Business', 'Custom', 'User')
    ),
    
    -- Ensure CustomDisplayName is set when DisplayNameSource = 'Custom'
    CONSTRAINT CK_Company_CustomDisplayName CHECK (
        (DisplayNameSource != 'Custom') OR (CustomDisplayName IS NOT NULL)
    )
);
GO

-- Index for company lookup by display name (user search, autocomplete)
CREATE INDEX IX_Company_DisplayName ON [Company](DisplayName, IsDeleted)
    WHERE IsDeleted = 0;
GO

-- Index for parent-child hierarchy queries ("Show all subsidiaries")
CREATE INDEX IX_Company_Parent ON [Company](ParentCompanyID, IsDeleted)
    WHERE IsDeleted = 0 AND ParentCompanyID IS NOT NULL;
GO

PRINT 'Company table created successfully (core entity)!';
GO

-- =====================================================================
-- TABLE 2: CompanyCustomerDetails (SaaS Multi-Tenant Context)
-- =====================================================================
-- Purpose: Companies that SUBSCRIBE to EventLead Platform (SaaS customers)
-- Key Insight: Row exists ONLY if company is a customer. No row = not a customer.
-- =====================================================================
CREATE TABLE [CompanyCustomerDetails] (
    -- =====================================================================
    -- Primary Key (also Foreign Key to Company)
    -- =====================================================================
    CompanyID BIGINT PRIMARY KEY,
    -- ^ One-to-one relationship with Company
    -- PK = FK pattern: CompanyID is BOTH primary key AND foreign key
    -- Existence of row indicates company IS a SaaS customer
    
    -- =====================================================================
    -- Subscription Details (SaaS Business Model)
    -- =====================================================================
    SubscriptionPlan NVARCHAR(50) NOT NULL DEFAULT 'Free',
    -- ^ Subscription tier: 'Free', 'Starter', 'Professional', 'Enterprise'
    -- MVP: Free tier only ("Create Free, Pay to Publish" model)
    -- Future: Paid plans with different feature access
    
    SubscriptionStartDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    -- ^ When company became a customer (UTC)
    -- Used for: Subscription age, customer lifetime value (CLV), churn analysis
    
    SubscriptionEndDate DATETIME2 NULL,
    -- ^ When subscription ends (UTC). NULL = active subscription (no end date)
    -- Used for: Churn tracking, renewal reminders
    
    SubscriptionStatus NVARCHAR(20) NOT NULL DEFAULT 'Active',
    -- ^ Status: 'Active', 'Suspended', 'Cancelled', 'Trial'
    -- Active = Normal operation
    -- Suspended = Payment overdue, forms deactivated
    -- Cancelled = Soft-cancelled, retain historical data
    -- Trial = Free trial period (future feature)
    
    -- =====================================================================
    -- Billing Relationship (Where Invoices Go)
    -- =====================================================================
    BillingCompanyID BIGINT NOT NULL,
    -- ^ Foreign key to Company (billing entity - where invoices are sent)
    -- Can be SELF (same company) or DIFFERENT company (parent company)
    -- Example: "Acme Corp" (customer) → invoices to "Acme Holdings" (billing entity)
    -- Default: SELF (CompanyID = BillingCompanyID) for solo companies
    -- Enterprise use case: Subsidiaries → parent company billing
    
    -- =====================================================================
    -- Platform Settings (Company-Wide Configuration)
    -- =====================================================================
    TestThreshold INT NOT NULL DEFAULT 5,
    -- ^ Required preview tests before publish (0-20)
    -- Solution-architecture requirement: Min 5 tests, Company Admin can adjust
    -- Range: 0 (no testing required) to 20 (strict QA)
    -- Business rule: Forms cannot publish until test count >= threshold
    
    AnalyticsOptOut BIT NOT NULL DEFAULT 0,
    -- ^ Opt-out of platform analytics (PostHog/Plausible)
    -- 0 = Analytics enabled (default)
    -- 1 = Opted out (privacy preference)
    -- Australian Privacy Principles compliance (users can opt-out)
    
    MaxUsers INT NULL,
    -- ^ Maximum team members (NULL = unlimited for MVP)
    -- Future: Paid plans have user limits (e.g., Starter = 5 users, Professional = 20)
    
    -- =====================================================================
    -- Audit Trail
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NOT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT FK_CompanyCustomerDetails_Company FOREIGN KEY (CompanyID) 
        REFERENCES [Company](CompanyID) ON DELETE CASCADE,
    
    CONSTRAINT FK_CompanyCustomerDetails_BillingCompany FOREIGN KEY (BillingCompanyID) 
        REFERENCES [Company](CompanyID),
    
    CONSTRAINT FK_CompanyCustomerDetails_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [User](UserID),
    
    CONSTRAINT FK_CompanyCustomerDetails_UpdatedBy FOREIGN KEY (UpdatedBy) 
        REFERENCES [User](UserID),
    
    -- Validate TestThreshold range (0-20)
    CONSTRAINT CK_CompanyCustomerDetails_TestThreshold CHECK (
        TestThreshold BETWEEN 0 AND 20
    ),
    
    -- Validate SubscriptionStatus values
    CONSTRAINT CK_CompanyCustomerDetails_Status CHECK (
        SubscriptionStatus IN ('Active', 'Suspended', 'Cancelled', 'Trial')
    )
);
GO

-- Index for subscription status queries (active customers, suspended, cancelled)
CREATE INDEX IX_CompanyCustomerDetails_Status ON [CompanyCustomerDetails](SubscriptionStatus);
GO

-- Index for billing company relationships ("Show all customers billed through Acme Holdings")
CREATE INDEX IX_CompanyCustomerDetails_BillingCompany ON [CompanyCustomerDetails](BillingCompanyID);
GO

PRINT 'CompanyCustomerDetails table created successfully (SaaS context)!';
GO

-- =====================================================================
-- TABLE 3: CompanyBillingDetails (Invoicing & Tax Compliance Context)
-- =====================================================================
-- Purpose: Australian tax compliance data for invoicing. LOCKED after first invoice.
-- Key Insight: GST-compliant invoices require legal name + ABN (11 digits).
-- =====================================================================
CREATE TABLE [CompanyBillingDetails] (
    -- =====================================================================
    -- Primary Key (also Foreign Key to Company)
    -- =====================================================================
    CompanyID BIGINT PRIMARY KEY,
    
    -- =====================================================================
    -- Australian Tax Compliance (MANDATORY for GST-compliant invoicing)
    -- =====================================================================
    ABN NVARCHAR(11) NOT NULL,
    -- ^ Australian Business Number (11 digits, no spaces)
    -- Example: "53004085616"
    -- MUST validate via ABN Lookup API before accepting
    -- Required for GST-compliant tax invoices (Australian law)
    
    ABNStatus NVARCHAR(20) NOT NULL DEFAULT 'Active',
    -- ^ ABN status from ABR API: 'Active', 'Cancelled', 'Historical', 'International'
    -- Updated from ABN Lookup API (cached 30 days)
    -- Invoice generation blocked if status != 'Active' (business rule)
    -- 'International' = non-Australian company (placeholder ABN)
    
    GSTRegistered BIT NOT NULL,
    -- ^ Is company registered for GST (Goods & Services Tax)?
    -- 0 = Not registered (no GST added to invoices)
    -- 1 = Registered (add 10% GST to all invoices)
    -- Verified via ABN Lookup API
    
    EntityType NVARCHAR(100) NULL,
    -- ^ Entity type from ABR: "Australian Private Company", "Sole Trader", "Partnership", "Trust"
    -- Optional. Useful for understanding business structure
    -- Populated from ABN Lookup API response
    
    -- =====================================================================
    -- Legal Invoicing Details (Tax Invoice Requirements)
    -- =====================================================================
    TaxInvoiceLegalName NVARCHAR(200) NOT NULL,
    -- ^ Legal entity name for tax invoices (ABR <mainName>)
    -- Example: "INTERNATIONAL CONVENTION CENTRE SYDNEY PTY LTD"
    -- MUST match ABR records for tax compliance (ATO requirement)
    -- Source: ABR <mainName><organisationName>
    
    TaxInvoiceDisplayName NVARCHAR(200) NULL,
    -- ^ Display name on tax invoices (user choice)
    -- Can be: Legal name or business name (user preference)
    -- Example: "ICC Sydney" (shorter, user-friendly)
    -- NULL = Use TaxInvoiceLegalName (default)
    -- Used for: Customer-facing invoice display
    
    BillingEmail NVARCHAR(100) NOT NULL,
    -- ^ Email address for invoice delivery
    -- Must be company email (not personal Gmail)
    -- Used for: Invoice PDFs, payment receipts, overdue reminders
    
    BillingAddress NVARCHAR(500) NOT NULL,
    -- ^ Full billing address (street, city, state, postcode)
    -- Required for GST tax invoices (Australian law)
    -- Example: "14 Darling Drive, Sydney NSW 2000, Australia"
    
    BillingContactName NVARCHAR(200) NULL,
    -- ^ Billing contact person (optional)
    -- Example: "Jane Smith, Finance Manager"
    
    BillingPhone NVARCHAR(20) NULL,
    -- ^ Billing contact phone (optional)
    
    -- =====================================================================
    -- Compliance & Locking (Audit Integrity - Critical for Tax Compliance)
    -- =====================================================================
    FirstInvoiceDate DATETIME2 NULL,
    -- ^ Date of first invoice issued (UTC)
    -- NULL = No invoices yet (billing details can be edited freely)
    -- NOT NULL = Invoices issued (billing details LOCKED for audit integrity)
    -- Business rule: Lock billing details after first invoice to prevent tampering
    
    IsLocked BIT NOT NULL DEFAULT 0,
    -- ^ Is billing entity locked? (0 = editable, 1 = locked)
    -- Locked after first invoice to maintain audit trail (ATO compliance)
    -- Changes after lock require System Admin override + audit log entry
    
    LockedDate DATETIME2 NULL,
    -- ^ When billing details were locked (UTC)
    
    LockedBy BIGINT NULL,
    -- ^ UserID who locked billing details (system-triggered or admin override)
    
    -- =====================================================================
    -- ABN Validation Cache (Performance Optimization)
    -- =====================================================================
    ABNLastVerified DATETIME2 NULL,
    -- ^ Last ABN verification via ABR API (UTC)
    -- Re-verify if > 30 days old (ABR terms allow 30-day cache)
    -- Reduces API calls (ABN rarely changes for established companies)
    
    ABNVerificationResponse NVARCHAR(MAX) NULL,
    -- ^ Cached JSON response from ABN Lookup API
    -- Stores: EntityName, ABNStatus, GSTStatus, EntityType, BusinessNames
    -- Reduces API costs (cache for 30 days)
    
    -- =====================================================================
    -- ABN Name Cache (Performance & Validation)
    -- =====================================================================
    ABNLegalName NVARCHAR(200) NOT NULL,
    -- ^ Cached legal name from last ABN lookup
    -- Used for: Validation, comparison with current ABR data
    -- Example: "INTERNATIONAL CONVENTION CENTRE SYDNEY PTY LTD"
    -- Source: ABR <mainName><organisationName>
    
    ABNBusinessNames NVARCHAR(MAX) NULL,
    -- ^ Cached business names from last ABN lookup (JSON array)
    -- Used for: Dropdown options, name selection UI
    -- Example: ["ICC SYDNEY", "SYDNEY CONVENTION CENTRE"]
    -- Source: ABR <businessName><organisationName> (current only)
    
    ABNNamesLastUpdated DATETIME2 NULL,
    -- ^ When names were last fetched from ABR API (UTC)
    -- Re-fetch if > 30 days old (ABR terms)
    -- Used for: Cache invalidation, name freshness tracking
    
    -- =====================================================================
    -- Audit Trail
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NOT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT FK_CompanyBillingDetails_Company FOREIGN KEY (CompanyID) 
        REFERENCES [Company](CompanyID) ON DELETE CASCADE,
    
    CONSTRAINT FK_CompanyBillingDetails_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [User](UserID),
    
    CONSTRAINT FK_CompanyBillingDetails_UpdatedBy FOREIGN KEY (UpdatedBy) 
        REFERENCES [User](UserID),
    
    CONSTRAINT FK_CompanyBillingDetails_LockedBy FOREIGN KEY (LockedBy) 
        REFERENCES [User](UserID),
    
    -- ABN format validation (11 digits, numeric only)
    CONSTRAINT CK_CompanyBillingDetails_ABN_Format CHECK (
        LEN(ABN) = 11 AND ABN NOT LIKE '%[^0-9]%'
    ),
    
    -- ABN status validation
    CONSTRAINT CK_CompanyBillingDetails_ABNStatus CHECK (
        ABNStatus IN ('Active', 'Cancelled', 'Historical', 'International')
    ),
    
    -- If locked, FirstInvoiceDate must be set (audit integrity check)
    CONSTRAINT CK_CompanyBillingDetails_LockedIntegrity CHECK (
        (IsLocked = 0) OR (IsLocked = 1 AND FirstInvoiceDate IS NOT NULL)
    )
);
GO

-- Index for ABN lookup (unique constraint - one ABN per billing entity)
-- Ensures no duplicate ABNs in system (business rule)
CREATE UNIQUE INDEX UX_CompanyBillingDetails_ABN ON [CompanyBillingDetails](ABN);
GO

-- Index for locked status (queries for editable billing entities)
CREATE INDEX IX_CompanyBillingDetails_Locked ON [CompanyBillingDetails](IsLocked);
GO

PRINT 'CompanyBillingDetails table created successfully (tax compliance context)!';
GO

-- =====================================================================
-- TABLE 4: CompanyOrganizerDetails (Event Organizer B2B Context)
-- =====================================================================
-- Purpose: Public-facing profile for event organizers. Displayed on event pages.
-- Key Insight: User-facing table (public profiles). Supports branding, trust signals.
-- =====================================================================
CREATE TABLE [CompanyOrganizerDetails] (
    -- =====================================================================
    -- Primary Key (also Foreign Key to Company)
    -- =====================================================================
    CompanyID BIGINT PRIMARY KEY,
    
    -- =====================================================================
    -- Public Profile (Displayed on Event Pages - "Organized by...")
    -- =====================================================================
    PublicProfileName NVARCHAR(200) NOT NULL,
    -- ^ Display name for "Organized by..." (can differ from Company.Name)
    -- Example: "ICC Sydney" (public brand) vs "International Convention Centre..." (legal)
    -- Used on event cards, event detail pages
    
    Description NVARCHAR(MAX) NULL,
    -- ^ Organizer description (markdown-safe, multi-paragraph)
    -- Example: "ICC Sydney is Australia's premier convention and exhibition centre..."
    -- Displayed on organizer profile page, event detail pages
    -- Helps users trust the event ("Organized by reputable venue")
    
    -- =====================================================================
    -- Branding Assets (Visual Identity)
    -- =====================================================================
    LogoUrl NVARCHAR(500) NULL,
    -- ^ Logo image URL (Azure Blob Storage)
    -- Displayed on event cards: "Organized by [LOGO] ICC Sydney"
    -- Trust signal: Recognizable logo = reputable organizer (Eventbrite pattern)
    
    BrandColorPrimary NVARCHAR(7) NULL,
    -- ^ Primary brand color (hex code: #0066CC)
    -- Used for organizer profile page theme (future feature)
    
    BrandColorSecondary NVARCHAR(7) NULL,
    -- ^ Secondary brand color (hex code)
    
    CoverImageUrl NVARCHAR(500) NULL,
    -- ^ Cover banner image for organizer profile page
    -- Example: Hero image of ICC Sydney venue exterior
    
    -- =====================================================================
    -- Contact & Discovery (Public Contact Information)
    -- =====================================================================
    ContactEmail NVARCHAR(100) NULL,
    -- ^ Public contact email for event inquiries
    -- Example: "events@iccsydney.com"
    -- Displayed on organizer profile ("Contact us about hosting events")
    
    ContactPhone NVARCHAR(20) NULL,
    -- ^ Public contact phone (international format)
    
    VenueDetails NVARCHAR(MAX) NULL,
    -- ^ Venue information (capacity, facilities, location details)
    -- Example: "25,000 sqm exhibition space, 8,000-seat auditorium, Darling Harbour location"
    -- JSON or plain text. Future: Structured venue data
    
    -- =====================================================================
    -- Quality & Source Attribution (Hybrid Strategy - Like Event Domain)
    -- =====================================================================
    OrganizerSource NVARCHAR(20) NOT NULL DEFAULT 'UserGenerated',
    -- ^ Data quality flag: 'Curated', 'UserGenerated', 'Verified'
    -- Matches Event domain hybrid strategy
    -- 'Curated' = Dimitri's manual research (ICC Sydney, Reed Exhibitions) - high quality
    -- 'UserGenerated' = User-added organizer - variable quality
    -- 'Verified' = User-added but admin/community verified - medium quality
    
    SourceUrl NVARCHAR(500) NULL,
    -- ^ Source URL for curated organizers (attribution for data governance)
    -- Example: "https://www.iccsydney.com/about"
    
    SourceAttribution NVARCHAR(200) NULL,
    -- ^ Credit source (data governance requirement)
    -- Example: "Sourced from ICC Sydney official website"
    
    IsPublic BIT NOT NULL DEFAULT 1,
    -- ^ Is organizer profile public? (1 = discoverable, 0 = private)
    -- Public = Discoverable in event organizer list (default)
    -- Private = Company doesn't want public organizer profile (edge case)
    
    -- =====================================================================
    -- Audit Trail
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NOT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT FK_CompanyOrganizerDetails_Company FOREIGN KEY (CompanyID) 
        REFERENCES [Company](CompanyID) ON DELETE CASCADE,
    
    CONSTRAINT FK_CompanyOrganizerDetails_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [User](UserID),
    
    CONSTRAINT FK_CompanyOrganizerDetails_UpdatedBy FOREIGN KEY (UpdatedBy) 
        REFERENCES [User](UserID),
    
    -- Validate OrganizerSource values
    CONSTRAINT CK_CompanyOrganizerDetails_Source CHECK (
        OrganizerSource IN ('Curated', 'UserGenerated', 'Verified')
    ),
    
    -- Validate hex color format (#RRGGBB)
    CONSTRAINT CK_CompanyOrganizerDetails_ColorFormat CHECK (
        (BrandColorPrimary IS NULL OR BrandColorPrimary LIKE '#[0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f]') AND
        (BrandColorSecondary IS NULL OR BrandColorSecondary LIKE '#[0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f]')
    )
);
GO

-- Index for public organizer discovery (event selection page)
CREATE INDEX IX_CompanyOrganizerDetails_Public ON [CompanyOrganizerDetails](IsPublic, OrganizerSource)
    WHERE IsPublic = 1;
GO

-- Index for organizer source filtering (curated vs user-generated)
CREATE INDEX IX_CompanyOrganizerDetails_Source ON [CompanyOrganizerDetails](OrganizerSource);
GO

PRINT 'CompanyOrganizerDetails table created successfully (event organizer context)!';
GO

-- =====================================================================
-- SUMMARY
-- =====================================================================
PRINT '========================================';
PRINT 'Company Domain Schema Complete!';
PRINT '========================================';
PRINT 'Tables Created:';
PRINT '  1. Company (core entity - 11 fields)';
PRINT '  2. CompanyCustomerDetails (SaaS context - 11 fields)';
PRINT '  3. CompanyBillingDetails (tax compliance - 17 fields)';
PRINT '  4. CompanyOrganizerDetails (event organizer - 13 fields)';
PRINT '';
PRINT 'Key Features:';
PRINT '  ✅ Multi-role support (customer + organizer + billing)';
PRINT '  ✅ Australian tax compliance (ABN validation, GST)';
PRINT '  ✅ Billing entity locking (after first invoice)';
PRINT '  ✅ Parent-subsidiary relationships';
PRINT '  ✅ Curated organizer support (hybrid strategy)';
PRINT '  ✅ Full audit trails (Solomon standards)';
PRINT '';
PRINT 'Next Steps:';
PRINT '  1. Import production seed data (25 curated organizers)';
PRINT '  2. Implement ABN Lookup API integration';
PRINT '  3. Validate schema with Solomon (Database Migration Validator)';
PRINT '========================================';
GO

