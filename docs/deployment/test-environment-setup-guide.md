# Test Environment Setup Guide – Signal Platforms
**Complete Step-by-Step Instructions**

**Document Version:** 1.0  
**Date:** 11 May 2026  
**Branch:** `cursor/azure-infrastructure-documentation`  
**Audience:** Anthony Keevy (you will run all commands)

---

## 1. Important Prerequisites & Order of Work

**Before creating anything in Azure, you must first correct the seed company data in your local development environment.**

This ensures that when the test environment is deployed, it already contains the correct “Signal Platforms” company record (CompanyID = 1) instead of the old “EventLead Platform” data.

**Recommended Order**
1. Update seed data locally (development).
2. Create Azure test environment resources.
3. Set up GitHub Actions + deployment slot.
4. Deploy to test slot.
5. Verify.

---

## 2. Step 1: Correct Seed Company Data (Development Environment)

### 2.1 Create Updated Seed Script

Create a new file:

**Path:** `database/seeds/signal-platforms-seed.sql`

**Content (replace placeholder values with your real details):**

```sql
-- =====================================================================
-- Signal Platforms – Production Seed Data (CompanyID = 1)
-- =====================================================================

USE [EventLeadPlatform];
GO

PRINT 'Updating platform company to Signal Platforms...';

-- Update existing CompanyID = 1 (or insert if it does not exist)
IF EXISTS (SELECT 1 FROM [Company] WHERE CompanyID = 1)
BEGIN
    UPDATE [Company]
    SET
        DisplayName = 'Signal Platforms',
        LegalEntityName = 'SIGNAL PLATFORMS PTY LTD',
        BusinessNames = '["Signal Platforms", "Signal Platforms"]',
        Website = 'https://signalplatforms.com.au',
        Phone = '+61 2 9215 7100',
        Industry = 'Software as a Service (SaaS)',
        UpdatedDate = GETUTCDATE()
    WHERE CompanyID = 1;
    PRINT 'CompanyID = 1 updated to Signal Platforms';
END
ELSE
BEGIN
    INSERT INTO [Company] (CompanyID, DisplayName, LegalEntityName, BusinessNames, Website, Phone, Industry, CreatedDate, CreatedBy, IsDeleted)
    VALUES (1, 'Signal Platforms', 'SIGNAL PLATFORMS PTY LTD', '["Signal Platforms"]', 'https://signalplatforms.com.au', '+61 2 9215 7100', 'Software as a Service (SaaS)', GETUTCDATE(), 1, 0);
    PRINT 'CompanyID = 1 created as Signal Platforms';
END
GO

-- Update Billing Details (replace with your real ABN and address)
UPDATE [CompanyBillingDetails]
SET
    ABN = '12 345 678 901',                    -- ← REPLACE WITH YOUR REAL ABN
    EntityName = 'SIGNAL PLATFORMS PTY LTD',
    BillingAddress = 'Level 5, 123 George Street, Sydney NSW 2000, Australia',  -- ← UPDATE
    BillingEmail = 'billing@signalplatforms.com.au',
    BillingPhone = '+61 2 9215 7100',
    TaxInvoiceLegalName = 'SIGNAL PLATFORMS PTY LTD',
    TaxInvoiceDisplayName = 'Signal Platforms',
    UpdatedDate = GETUTCDATE()
WHERE CompanyID = 1;
PRINT 'Billing details updated';

-- Update Organizer Details
UPDATE [CompanyOrganizerDetails]
SET
    PublicProfileName = 'Signal Platforms',
    LogoUrl = 'https://signalplatforms.com.au/logo.png',  -- ← UPDATE WHEN AVAILABLE
    BrandColorPrimary = '#0066CC',
    Description = 'Professional customer engagement form builder for Australian businesses.',
    ContactEmail = 'hello@signalplatforms.com.au',
    ContactPhone = '+61 2 9215 7100',
    UpdatedDate = GETUTCDATE()
WHERE CompanyID = 1;
PRINT 'Organizer details updated';

PRINT '✅ Signal Platforms seed data updated successfully.';
GO
```

**Action Required**
- Replace the placeholder ABN, address, phone, and logo URL with your real details.
- Run the script in your local development database:

```powershell
sqlcmd -S localhost -d EventLeadPlatform -i database/seeds/signal-platforms-seed.sql
```

- Verify the data looks correct before proceeding.

---

## 3. Step 2: Create Azure Test Environment

You will run these commands after logging in with `az login`.

### 3.1 Login to Azure

```powershell
az login
```

Follow the browser prompt to authenticate with your Azure account.

### 3.2 Set Variables (edit these)

```powershell
$ResourceGroup = "signal-platforms-test-rg"
$Location = "australiaeast"
$AppServicePlan = "signal-platforms-test-plan"
$AppServiceName = "signalplatforms-test"
$SqlServerName = "signalplatforms-test-sql"
$SqlAdminUser = "signaladmin"
$SqlAdminPassword = "YourStrong!TestPassword123"   # ← CHANGE THIS
$DatabaseName = "EventLeadPlatformTest"
$KeyVaultName = "signalplatforms-test-kv"
```

### 3.3 Create Resource Group

```powershell
az group create `
  --name $ResourceGroup `
  --location $Location
```

### 3.4 Create App Service Plan + App Service + Test Slot

```powershell
# Create App Service Plan (B1 is cheap and sufficient for test)
az appservice plan create `
  --name $AppServicePlan `
  --resource-group $ResourceGroup `
  --sku B1 `
  --is-linux `
  --location $Location

# Create App Service
az webapp create `
  --name $AppServiceName `
  --plan $AppServicePlan `
  --resource-group $ResourceGroup `
  --runtime "PYTHON:3.12"

# Create Test Deployment Slot
az webapp deployment slot create `
  --name $AppServiceName `
  --resource-group $ResourceGroup `
  --slot test
```

### 3.5 Create Azure SQL Server + Database (Serverless)

```powershell
# Create SQL Server
az sql server create `
  --name $SqlServerName `
  --resource-group $ResourceGroup `
  --location $Location `
  --admin-user $SqlAdminUser `
  --admin-password $SqlAdminPassword

# Create Serverless Database
az sql db create `
  --name $DatabaseName `
  --server $SqlServerName `
  --resource-group $ResourceGroup `
  --edition GeneralPurpose `
  --compute-model Serverless `
  --minvcores 0.5 `
  --maxvcores 2
```

### 3.6 Create Blob Storage, Key Vault, Application Insights, ACS

```powershell
# Storage Account + Container
$StorageName = "signalplatformstestsa"
az storage account create `
  --name $StorageName `
  --resource-group $ResourceGroup `
  --location $Location `
  --sku Standard_LRS

az storage container create `
  --name assets `
  --account-name $StorageName `
  --auth-mode login

# Key Vault
az keyvault create `
  --name $KeyVaultName `
  --resource-group $ResourceGroup `
  --location $Location

# Application Insights
az monitor app-insights component create `
  --app signalplatforms-test-insights `
  --location $Location `
  --resource-group $ResourceGroup

# Azure Communication Services (Email)
az communication create `
  --name signalplatforms-test-acs `
  --resource-group $ResourceGroup `
  --location $Location `
  --data-location "Australia"
```

### 3.7 Configure App Service Settings (Test Slot)

You will add these via the Azure Portal or CLI after the resources exist. Key settings include:

- `ENVIRONMENT` = `test`
- `EMAIL_PROVIDER` = `acs`
- `TEST_MODE` = `true`
- `TEST_CATCHALL_EMAIL` = `test-inbox@signalplatforms.io`
- `DATABASE_URL` = the connection string from the test database
- `STORAGE_ACCOUNT` and `STORAGE_KEY` from the storage account
- `ACS_CONNECTION_STRING` from the ACS resource

---

## 4. Step 3: GitHub Actions Workflow

Create the file `.github/workflows/deploy-to-test.yml` with the workflow that deploys to the `test` slot on pushes to the `develop` branch (or manually).

(The full workflow content will be provided in a follow-up task once you confirm you are ready to implement.)

---

## 5. Next Actions

Please confirm the following:

1. You have updated the seed data locally and it is correct.
2. You are ready for me to provide the complete GitHub Actions workflow file and the exact list of GitHub Environment secrets.
3. You want to proceed with running the Azure CLI commands above.

Once you give the go-ahead, I will give you the next precise block of commands and files.

---

**Document Status**: Ready for execution when you are.