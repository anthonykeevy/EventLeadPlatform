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

**Important:** The original platform seed data still contains the old “EventLeads” placeholder values. You must correct this **before** creating any Azure resources.

### 2.1 Run the Corrected Seed Script

A dedicated seed script has been created for this purpose:

**File:** `database/seeds/signal-platforms-seed.sql`

This script safely updates (or inserts) CompanyID = 1 with the correct legal entity details from your ABN Advice Letter:
- Legal Name: `SIGNAL PLATFORMS PTY LTD`
- ABN: `23 695 192 511`
- ACN: `695 192 511`
- Address: `4 Milburn Pl, St Ives Chase NSW 2075`
- Default Email: `noreply@signalplatforms.com.au`
- GST Registered: No (will be updated on production move)

**Run the script:**

```powershell
sqlcmd -S localhost -d EventLeadPlatform -i database/seeds/signal-platforms-seed.sql
```

### 2.2 Verify the Data

Run these queries to confirm the correction:

```sql
SELECT CompanyID, CompanyName, LegalEntityName, ABN, ACN, GSTRegistered, Email, Website
FROM [Company]
WHERE CompanyID = 1;

SELECT *
FROM [CompanyBillingDetails]
WHERE CompanyID = 1;
```

Expected results:
- `CompanyName` = “Signal Platforms”
- `LegalEntityName` = “SIGNAL PLATFORMS PTY LTD”
- `ABN` = “23695192511”
- `Email` = “noreply@signalplatforms.com.au”

### 2.3 Update the Alembic Migration (Future-Proofing)

For any future fresh database deployments, the same correction must be applied in the migration system.

See the companion document:

**`docs/deployment/seed-data-correction-instructions.md`**

It contains:
- The exact diff for `backend/migrations/versions/009_company_validation_architecture.py`
- Upgrade and downgrade changes
- Verification steps

**Do not proceed to Azure deployment until the local seed data has been verified.**

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