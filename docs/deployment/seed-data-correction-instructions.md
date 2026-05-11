# Seed Data Correction Instructions – Signal Platforms

**Date:** 11 May 2026  
**Status:** Ready to Execute (Documentation Only)

---

## Overview

The original platform seed data (CompanyID = 1) was created with placeholder “EventLeads” values. This document provides the exact corrections needed so the test environment is created with the correct legal entity.

**Correct Details (from ABN Advice Letter)**
- ABN: `23 695 192 511`
- Legal Entity Name: `SIGNAL PLATFORMS PTY LTD`
- ACN: `695 192 511`
- Address: `4 Milburn Pl, St Ives Chase NSW 2075`
- GST Registered: No (will be updated on production move)
- Default Email: `noreply@signalplatforms.com.au`

---

## Step 1: Run the Corrected Standalone Seed Script (Development)

Run this script in your local development database **before** any Azure deployment.

```powershell
sqlcmd -S localhost -d EventLeadPlatform -i database/seeds/signal-platforms-seed.sql
```

This script:
- Updates (or inserts) CompanyID = 1 with correct Signal Platforms data.
- Inserts or updates the corresponding CompanyBillingDetails row.
- Is safe to re-run (uses IF EXISTS checks).

**Verification Query**

```sql
SELECT 
    CompanyID,
    CompanyName,
    LegalEntityName,
    ABN,
    ACN,
    GSTRegistered,
    Email,
    Website
FROM [Company]
WHERE CompanyID = 1;

SELECT *
FROM [CompanyBillingDetails]
WHERE CompanyID = 1;
```

Expected results:
- CompanyName = “Signal Platforms”
- LegalEntityName = “SIGNAL PLATFORMS PTY LTD”
- ABN = “23695192511”
- Email = “noreply@signalplatforms.com.au”

---

## Step 2: Update the Alembic Migration (Required for Future Databases)

The seed logic lives in:

`backend/migrations/versions/009_company_validation_architecture.py`

### Changes Required in the `upgrade()` function

**Replace the three scenarios (lines ~844–900) with the following corrected block:**

```python
# ========================================
# STEP 8: Signal Platforms Company Seed (Corrected)
# ========================================

op.execute("""
    DECLARE @SignalPlatformsExists BIT = 0;
    DECLARE @CompanyIDOne BIT = 0;
    
    IF EXISTS (SELECT 1 FROM [dbo].[Company] WHERE CompanyName = 'Signal Platforms')
        SET @SignalPlatformsExists = 1;
    
    IF EXISTS (SELECT 1 FROM [dbo].[Company] WHERE CompanyID = 1)
        SET @CompanyIDOne = 1;
    
    -- Scenario 1: Fresh database - INSERT Signal Platforms as CompanyID = 1
    IF @SignalPlatformsExists = 0 AND @CompanyIDOne = 0
    BEGIN
        SET IDENTITY_INSERT [dbo].[Company] ON;
        
        INSERT INTO [dbo].[Company] (
            CompanyID,
            CompanyName,
            LegalEntityName,
            DisplayNameSource,
            ABN,
            ACN,
            ABNStatus,
            EntityType,
            GSTRegistered,
            Email,
            Website,
            CountryID,
            IsActive
        )
        VALUES (
            1,
            'Signal Platforms',
            'SIGNAL PLATFORMS PTY LTD',
            'Legal',
            '23695192511',
            '695192511',
            'Active',
            'Australian Private Company',
            0,
            'noreply@signalplatforms.com.au',
            'https://signalplatforms.com.au',
            (SELECT CountryID FROM [ref].[Country] WHERE CountryCode = 'AU'),
            1
        );
        
        SET IDENTITY_INSERT [dbo].[Company] OFF;
    END
    
    -- Scenario 2: Dev database - UPDATE existing CompanyID = 1
    IF @SignalPlatformsExists = 0 AND @CompanyIDOne = 1
    BEGIN
        UPDATE [dbo].[Company]
        SET 
            CompanyName = 'Signal Platforms',
            LegalEntityName = 'SIGNAL PLATFORMS PTY LTD',
            ABN = '23695192511',
            ACN = '695192511',
            ABNStatus = 'Active',
            EntityType = 'Australian Private Company',
            GSTRegistered = 0,
            Email = 'noreply@signalplatforms.com.au',
            Website = 'https://signalplatforms.com.au',
            UpdatedDate = GETUTCDATE()
        WHERE CompanyID = 1;
    END
""")

# Also insert CompanyBillingDetails for CompanyID = 1 if missing
op.execute("""
    IF NOT EXISTS (SELECT 1 FROM [dbo].[CompanyBillingDetails] WHERE CompanyID = 1)
    BEGIN
        INSERT INTO [dbo].[CompanyBillingDetails] (
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
    END
""")
```

### Changes Required in the `downgrade()` function

Replace the existing delete logic with:

```python
op.execute("DELETE FROM [dbo].[CompanyBillingDetails] WHERE CompanyID = 1")
op.execute("DELETE FROM [config].[CompanyValidationRule] WHERE CompanyID = 1")
op.execute("DELETE FROM [dbo].[Company] WHERE CompanyID = 1 AND CompanyName = 'Signal Platforms'")
```

---

## Summary of Files to Update

| File | Action | When |
|------|--------|------|
| `database/seeds/signal-platforms-seed.sql` | Create & run manually | Before any Azure deployment |
| `backend/migrations/versions/009_company_validation_architecture.py` | Edit upgrade + downgrade | When ready to commit migration change |
| `docs/deployment/test-environment-setup-guide.md` | Reference new seed file | Already updated |

---

**Next Step**  
Once you have run the seed script and verified the data, reply “Ready” and I will provide the complete GitHub Actions workflow + secrets list for the test environment deployment.