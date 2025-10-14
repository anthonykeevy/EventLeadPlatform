-- =====================================================================
-- EventLead Platform Seed Data - Platform as Company
-- =====================================================================
-- Author: Dimitri (Data Domain Architect)
-- Date: October 13, 2025
-- Version: 1.0.0
-- =====================================================================
-- Purpose:
--   Create EventLead Platform as CompanyID = 1 in the Company table.
--   This allows EventLead to have its own ABN, billing details, and
--   participate in the same multi-tenant structure as customers.
--
-- Strategy:
--   - EventLead Platform = CompanyID = 1 (special system company)
--   - Customer companies start from CompanyID = 2+
--   - EventLead's ABN used as SELLER ABN on tax invoices
--   - Customer's ABN used as BUYER ABN on tax invoices
--
-- Australian GST Compliance:
--   Tax invoices require BOTH seller's ABN (EventLead) and buyer's ABN (customer).
--   Both stored in Company table structure.
-- =====================================================================

USE [EventLeadPlatform];
GO

-- =====================================================================
-- Create System User (if not exists)
-- =====================================================================
-- EventLead Platform needs a "CreatedBy" user for audit trail
-- Using UserID = 1 for system operations

IF NOT EXISTS (SELECT 1 FROM [User] WHERE UserID = 1)
BEGIN
    INSERT INTO [User] (
        UserID,  -- Explicit ID for system user
        Email, 
        FirstName, 
        LastName, 
        IsActive,
        CreatedDate,
        CreatedBy
    ) VALUES (
        1,
        'system@eventlead.com.au',
        'System',
        'User',
        1,
        GETUTCDATE(),
        1  -- Self-referencing (system creates itself)
    );
    
    PRINT 'System User (UserID = 1) created successfully';
END
ELSE
BEGIN
    PRINT 'System User (UserID = 1) already exists';
END
GO

-- =====================================================================
-- EventLead Platform Company (CompanyID = 1)
-- =====================================================================
-- Create EventLead Platform as the first company in the system
-- This company represents US (EventLead Platform) as the seller

INSERT INTO [Company] (
    CompanyID,  -- Explicit ID = 1 for EventLead Platform
    DisplayName,
    LegalEntityName,
    BusinessNames,
    CustomDisplayName,
    DisplayNameSource,
    Website,
    Phone,
    Industry,
    ParentCompanyID,  -- NULL (EventLead is the parent company)
    CreatedDate,
    CreatedBy,
    UpdatedDate,
    UpdatedBy,
    IsDeleted,
    DeletedDate,
    DeletedBy
) VALUES (
    1,  -- EventLead Platform CompanyID
    'EventLead Platform',  -- Display name (user-friendly)
    'EVENTLEAD PLATFORM PTY LTD',  -- Legal entity name (ABR format)
    '["EventLead Platform", "EventLead"]',  -- Business names (JSON array)
    NULL,  -- No custom override
    'Business',  -- Source: First business name
    'https://eventlead.com.au',
    '+61 2 9215 7100',
    'Software as a Service (SaaS)',
    NULL,  -- No parent company
    GETUTCDATE(),
    1,  -- Created by System User
    NULL,
    NULL,
    0,  -- Not deleted
    NULL,
    NULL
);

PRINT 'EventLead Platform Company (CompanyID = 1) created successfully';
GO

-- =====================================================================
-- EventLead Platform Billing Details (SELLER ABN for Tax Invoices)
-- =====================================================================
-- This is EventLead Platform's own ABN - used as SELLER ABN on invoices
-- Customer companies will have their own ABN as BUYER ABN

INSERT INTO [CompanyBillingDetails] (
    CompanyID,  -- FK to Company table (EventLead Platform = 1)
    ABN,
    ABNStatus,
    EntityName,
    GSTRegistered,
    BillingAddress,
    BillingEmail,
    BillingPhone,
    TaxInvoiceLegalName,
    TaxInvoiceDisplayName,
    FirstInvoiceDate,  -- NULL (we haven't sent ourselves an invoice!)
    IsLocked,  -- 0 (can be updated until first invoice)
    LockedDate,
    LockedBy,
    ABNLegalName,
    ABNBusinessNames,
    ABNNamesLastUpdated,
    CreatedDate,
    CreatedBy,
    UpdatedDate,
    UpdatedBy,
    IsDeleted,
    DeletedDate,
    DeletedBy
) VALUES (
    1,  -- EventLead Platform CompanyID
    '12345678901',  -- ⚠️ CHANGE THIS TO YOUR ACTUAL ABN!
    'Active',
    'EVENTLEAD PLATFORM PTY LTD',
    1,  -- Yes, EventLead Platform is GST registered
    '123 Tech Street, Sydney NSW 2000, Australia',  -- ⚠️ CHANGE TO YOUR ADDRESS
    'billing@eventlead.com.au',
    '+61 2 9215 7100',
    'EVENTLEAD PLATFORM PTY LTD',  -- Legal name for tax invoices
    'EventLead Platform',  -- Display name for tax invoices (user-friendly)
    NULL,  -- No first invoice date yet
    0,  -- Not locked (can update until first invoice)
    NULL,
    NULL,
    'EVENTLEAD PLATFORM PTY LTD',  -- Cached legal name from ABR
    '["EventLead Platform", "EventLead"]',  -- Cached business names from ABR
    GETUTCDATE(),  -- Names just fetched
    GETUTCDATE(),
    1,  -- Created by System User
    NULL,
    NULL,
    0,  -- Not deleted
    NULL,
    NULL
);

PRINT 'EventLead Platform Billing Details created successfully';
PRINT '⚠️  IMPORTANT: Update ABN and address with your actual details!';
GO

-- =====================================================================
-- EventLead Platform Customer Details (SaaS Subscription Context)
-- =====================================================================
-- EventLead Platform is also a "customer" of its own platform
-- This allows for internal testing, demo accounts, etc.

INSERT INTO [CompanyCustomerDetails] (
    CompanyID,  -- FK to Company table (EventLead Platform = 1)
    SubscriptionPlan,
    SubscriptionStart,
    SubscriptionEnd,
    BillingCompanyID,  -- Self-billing (CompanyID = 1)
    TestThreshold,  -- No test threshold for platform company
    AnalyticsOptOut,  -- Platform company can see all analytics
    MaxUsers,  -- Unlimited users for platform company
    CreatedDate,
    CreatedBy,
    UpdatedDate,
    UpdatedBy,
    IsDeleted,
    DeletedDate,
    DeletedBy
) VALUES (
    1,  -- EventLead Platform CompanyID
    'Enterprise',  -- Highest tier for platform company
    GETUTCDATE(),  -- Started today
    NULL,  -- No end date (perpetual)
    1,  -- Self-billing (EventLead bills itself)
    0,  -- No test threshold
    0,  -- Analytics enabled (platform needs to see data)
    999,  -- Unlimited users
    GETUTCDATE(),
    1,  -- Created by System User
    NULL,
    NULL,
    0,  -- Not deleted
    NULL,
    NULL
);

PRINT 'EventLead Platform Customer Details created successfully';
GO

-- =====================================================================
-- EventLead Platform Organizer Details (Public Profile Context)
-- =====================================================================
-- EventLead Platform can also be an event organizer
-- Useful for platform-hosted events, demos, training sessions

INSERT INTO [CompanyOrganizerDetails] (
    CompanyID,  -- FK to Company table (EventLead Platform = 1)
    PublicProfileName,
    LogoUrl,
    BrandColorPrimary,
    BrandColorSecondary,
    Description,
    VenueDetails,
    ContactEmail,
    ContactPhone,
    CreatedDate,
    CreatedBy,
    UpdatedDate,
    UpdatedBy,
    IsDeleted,
    DeletedDate,
    DeletedBy
) VALUES (
    1,  -- EventLead Platform CompanyID
    'EventLead Platform',
    'https://eventlead.com.au/logo.png',  -- ⚠️ UPDATE WITH ACTUAL LOGO URL
    '#0066CC',  -- Primary brand color (blue)
    '#FFFFFF',  -- Secondary brand color (white)
    'Leading event lead generation platform for Australian businesses. We help event organizers capture, qualify, and convert leads through intelligent forms and analytics.',
    'Online Platform - Virtual Events Supported',
    'events@eventlead.com.au',
    '+61 2 9215 7100',
    GETUTCDATE(),
    1,  -- Created by System User
    NULL,
    NULL,
    0,  -- Not deleted
    NULL,
    NULL
);

PRINT 'EventLead Platform Organizer Details created successfully';
GO

-- =====================================================================
-- Summary and Next Steps
-- =====================================================================

PRINT '========================================';
PRINT 'EventLead Platform Seed Data Complete!';
PRINT '========================================';
PRINT '';
PRINT 'EventLead Platform Company Created:';
PRINT '  CompanyID: 1';
PRINT '  Display Name: EventLead Platform';
PRINT '  Legal Entity Name: EVENTLEAD PLATFORM PTY LTD';
PRINT '  Business Names: ["EventLead Platform", "EventLead"]';
PRINT '  Display Name Source: Business (first business name)';
PRINT '  ABN: 12345678901 (⚠️ CHANGE THIS!)';
PRINT '  Address: 123 Tech Street, Sydney NSW 2000 (⚠️ CHANGE THIS!)';
PRINT '  GST Registered: Yes';
PRINT '';
PRINT 'Multi-Role Support:';
PRINT '  ✅ Customer (SaaS subscription - Enterprise tier)';
PRINT '  ✅ Billing (SELLER ABN for tax invoices)';
PRINT '  ✅ Organizer (public profile for platform events)';
PRINT '';
PRINT 'Tax Invoice Usage:';
PRINT '  SELLER ABN: EventLead Platform ABN (from CompanyBillingDetails)';
PRINT '  BUYER ABN: Customer Company ABN (from their CompanyBillingDetails)';
PRINT '';
PRINT '⚠️  CRITICAL ACTIONS REQUIRED:';
PRINT '  1. Update ABN with your actual Australian Business Number';
PRINT '  2. Update billing address with your actual business address';
PRINT '  3. Update logo URL with your actual logo';
PRINT '  4. Test ABN lookup API integration';
PRINT '';
PRINT 'Next Steps:';
PRINT '  1. Customer companies start from CompanyID = 2';
PRINT '  2. Implement ABN validation for customer companies';
PRINT '  3. Test tax invoice generation with both ABNs';
PRINT '========================================';
GO
