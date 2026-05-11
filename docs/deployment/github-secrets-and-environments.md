# GitHub Actions Secrets & Environment Setup – Test Environment

**Document Version:** 1.0  
**Date:** 11 May 2026

---

## 1. GitHub Environment: `test`

In your GitHub repository, go to:

**Settings → Environments → New environment**

Create an environment named exactly: **`test`**

This environment will be used to protect the test slot deployment and store its secrets.

---

## 2. Required Secrets (Add These in the `test` Environment)

Go to:

**Settings → Environments → `test` → Secrets and variables → Actions → New repository secret**

Add the following secrets one by one.

### 2.1 `AZURE_WEBAPP_PUBLISH_PROFILE_TEST`

**Value:** The Publish Profile XML for the **test slot**.

**How to obtain it:**

1. Go to the Azure Portal
2. Navigate to your App Service: `signalplatforms-test`
3. In the left menu, go to **Deployment → Deployment Center**
4. Click **Download Publish Profile** (or go to the **test** slot and download its publish profile)
5. Open the downloaded `.PublishSettings` file in a text editor
6. Copy the **entire contents** (it is a long XML block)
7. Paste it into the GitHub secret `AZURE_WEBAPP_PUBLISH_PROFILE_TEST`

**Alternative (more secure long-term):** Create a Service Principal and use `azure/login` + `azure/webapps-deploy`. Publish Profile is simpler for the test phase.

### 2.2 `DATABASE_URL_TEST`

**Value:** The full connection string for the **test** Azure SQL Database.

**Example format:**
```
mssql+pyodbc://signaladmin:YourStrong!TestPassword123@signalplatforms-test-sql.database.windows.net:1433/EventLeadPlatformTest?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no
```

**How to obtain it:**
- Azure Portal → SQL Database → Connection strings → Copy the **ADO.NET** string and adapt it to the SQLAlchemy format above.

### 2.3 `ACS_CONNECTION_STRING_TEST`

**Value:** The connection string for your Azure Communication Services resource.

**How to obtain it:**
- Azure Portal → Communication Services → `signalplatforms-test-acs` → Keys → Copy the **Connection String**

### 2.4 `STORAGE_ACCOUNT_NAME_TEST`

**Value:** The name of your storage account (e.g. `signalplatformstestsa`)

### 2.5 `STORAGE_ACCOUNT_KEY_TEST`

**Value:** One of the access keys from the storage account.

### 2.6 `APPINSIGHTS_INSTRUMENTATION_KEY_TEST`

**Value:** The Instrumentation Key from Application Insights (or the Connection String).

### 2.7 `JWT_SECRET_KEY_TEST`

**Value:** A long random string (minimum 32 characters). Generate one and keep it secret.

**Example command to generate:**
```powershell
openssl rand -base64 48
```

### 2.8 `STRIPE_SECRET_KEY_TEST` (Optional for now)

Leave empty or put your Stripe test key if you want payments enabled in test.

### 2.9 `FRONTEND_URL_TEST`

**Value:** `https://signalplatforms-test.azurewebsites.net` (or your custom test domain once configured)

---

## 3. Additional App Settings (Recommended)

In the Azure Portal, go to the **test** slot and add these Application Settings (Configuration → Application settings). These complement the GitHub secrets.

- `ENVIRONMENT` = `test`
- `EMAIL_PROVIDER` = `acs`
- `TEST_MODE` = `true`
- `TEST_CATCHALL_EMAIL` = `test-inbox@signalplatforms.io`
- `EMAIL_FROM` = `noreply@signalplatforms.com.au`
- `EMAIL_FROM_NAME` = `Signal Platforms`

These can also be set via the GitHub workflow if you prefer (see the workflow file).

---

## 4. Security Notes

- Never commit secrets to the repository.
- The `test` GitHub Environment can have **required reviewers** (you can add yourself) so deployments only happen after manual approval.
- For production later, create a second environment called `production` with stricter protection rules.

---

## 5. Next Steps After Adding Secrets

1. Commit and push the workflow file (`.github/workflows/deploy-to-test.yml`) to the `develop` branch.
2. The workflow will trigger automatically on the next push to `develop`.
3. You can also trigger it manually from the **Actions** tab.

---

**Document Status**: Ready for use. All values above are placeholders — replace them with your real Azure values.