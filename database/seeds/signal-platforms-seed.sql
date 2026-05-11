-- =====================================================================
-- Signal Platforms – Corrected Platform Company Seed (CompanyID = 1)
-- =====================================================================
-- Purpose: Replace old EventLeads seed data with correct Signal Platforms details
-- Run this in your local development database BEFORE deploying to test environment.
-- =====================================================================

USE [EventLeadPlatform];
GO

PRINT '========================================';
PRINT 'Correcting Platform Company to Signal Platforms';
PRINT '========================================';

-- Update CompanyID = 1 with correct Signal Platforms data
IF EXISTS (SELECT 1 FROM [Company] WHERE CompanyID = 1)
BEGIN
    UPDATE [Company]
    SET
        CompanyName = 'Signal Platforms',
        LegalEntityName = 'SIGNAL PLATFORMS PTY LTD',
        BusinessNames = '["Signal Platforms"]',
        CustomDisplayName = NULL,
        DisplayNameSource = 'Legal',
        ABN = '23695192511',
        ACN = '695192511',
        ABNStatus = 'Active',
        EntityType = 'Australian Private Company',
        GSTRegistered = 0,  -- Not yet GST registered (update when you move to production)
        Phone = NULL,
        Email = 'noreply@signalplatforms.com.au',
        Website = 'https://signalplatforms.com.au',
        CountryID = (SELECT CountryID FROM [ref].[Country] WHERE CountryCode = 'AU'),
        IndustryID = NULL,  -- Can be linked later if Industry ref table exists
        UpdatedDate = GETUTCDATE(),
        UpdatedBy = 1
    WHERE CompanyID = 1;

    PRINT '✅ CompanyID = 1 updated to Signal Platforms';
END
ELSE
BEGIN
    PRINT '⚠️  CompanyID = 1 does not exist. Inserting new record...';
    
    SET IDENTITY_INSERT [Company] ON;
    
    INSERT INTO [Company] (
        CompanyID,
        CompanyName,
        LegalEntityName,
        BusinessNames,
        DisplayNameSource,
        ABN,
        ACN,
        ABNStatus,
        EntityType,
        GSTRegistered,
        Email,
        Website,
        CountryID,
        IsActive,
        CreatedDate,
        CreatedBy,
        IsDeleted
    )
    VALUES (
        1,
        'Signal Platforms',
        'SIGNAL PLATFORMS PTY LTD',
        '["Signal Platforms"]',
        'Legal',
        '23695192511',
        '695192511',
        'Active',
        'Australian Private Company',
        0,
        'noreply@signalplatforms.com.au',
        'https://signalplatforms.com.au',
        (SELECT CountryID FROM [ref].[Country] WHERE CountryCode = 'AU'),
        1,
        GETUTCDATE(),
        1,
        0
    );
    
    SET IDENTITY_INSERT [Company] OFF;
    
    PRINT '✅ CompanyID = 1 inserted as Signal Platforms';
END
GO

-- Insert or Update CompanyBillingDetails for CompanyID = 1
IF EXISTS (SELECT 1 FROM [CompanyBillingDetails] WHERE CompanyID = 1)
BEGIN
    UPDATE [CompanyBillingDetails]
    SET
        BillingAddressLine1 = '4 Milburn Pl',
        BillingCity = 'St Ives Chase',
        BillingState = 'NSW',
        BillingPostalCode = '2075',
        BillingCountryID = (SELECT CountryID FROM [ref].[Country] WHERE CountryCode = 'AU'),
        BillingEmail = 'noreply@signalplatforms.com.au',
        UpdatedDate = GETUTCDATE(),
        UpdatedBy = 1
    WHERE CompanyID = 1;
    
    PRINT '✅ CompanyBillingDetails updated for CompanyID = 1';
END
ELSE
BEGIN
    INSERT INTO [CompanyBillingDetails] (
        CompanyID,
        BillingAddressLine1,
        BillingCity,
        BillingState,
        BillingPostalCode,
        BillingCountryID,
        BillingEmail,
        CreatedDate,
        CreatedBy,
        IsDeleted
    )
    VALUES (
        1,
        '4 Milburn Pl',
        'St Ives Chase',
        'NSW',
        '2075',
        (SELECT CountryID FROM [ref].[Country] WHERE CountryCode = 'AU'),
        'noreply@signalplatforms.com.au',
        GETUTCDATE(),
        1,
        0
    );
    
    PRINT '✅ CompanyBillingDetails inserted for CompanyID = 1';
END
GO

PRINT '========================================';
PRINT 'Signal Platforms seed data correction complete.';
PRINT 'Please verify the data before deploying to test environment.';
PRINT '========================================';
GO