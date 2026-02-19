# Company Settings Domain — Data Model Analysis

**Purpose:** Review database structure for Story 5.7 (Company Settings Hub) and propose a unified table for company defaults per domain.  
**Story:** 5.7 - Company Settings Hub — Foundation  
**Created:** 2026-02-17  

---

## 1. Executive Summary

Story 5.7 requires a central Company Settings area with:
- **Company Details** (invoicing-ready)
- **Form Branding** (Company Form Defaults)
- **Form Workflow** (test thresholds, publish approval)
- **Assets** (images + Terms of Agreement)

Today we have **domain-specific tables** for each area. This document reviews the current structure, confirms support for Story 5.7, and proposes a **CompanyDomainDefault** table as the foundation for future domain expansion.

---

## 2. Current Database Structure (Story 5.7 Support)

### 2.1 Form Branding → `CompanyFormDefaults`

| Table | Purpose | Structure |
|-------|---------|-----------|
| **dbo.CompanyFormDefaults** | Per-company form branding (theme, globalStyles, etc.) | One row per CompanyID; DefaultsJSON; FormDefaultsSchemaVersionID |
| **dbo.CompanyFormDefaultsVersion** | Audit history | Append-only; VersionNumber, DefaultsJSON, ChangeSummary |

- **Key:** `CompanyID` (unique)  
- **Values:** DefaultsJSON (NVARCHAR(MAX)), schema version  
- **Used by:** Form Builder Init API, form save/load  

### 2.2 Form Workflow → `CompanyFormTestConfig`

| Table | Purpose | Structure |
|-------|---------|-----------|
| **dbo.CompanyFormTestConfig** | Per-company test threshold and publish approval | One row per CompanyID; typed columns |

| Column | Type | Purpose |
|--------|------|---------|
| CompanyFormTestConfigID | BIGINT PK | |
| CompanyID | BIGINT FK, UQ | One config per company |
| TestThresholdEnabled | BIT | Enforce demo test requirement |
| TestThresholdValue | INT | Runs required (0–100) |
| RequirePublishApproval | BIT | Company User must request publish (Story 5.6) |

- **Used by:** Readiness service, GET/PUT `/api/forms/company-test-config`  

### 2.3 Company Assets → `Asset` (no CompanyAsset table)

Company assets are stored in **dbo.Asset** with `CompanyID`:

| Table | Purpose | Structure |
|-------|---------|-----------|
| **dbo.Asset** | All company assets (images, documents) | CompanyID + AssetTypeID + storage metadata |
| **ref.AssetType** | Asset type reference | TypeCode: IMAGE, TERMS, DOCUMENT, VIDEO (all four for Story 5.7) |

| Asset columns | Notes |
|--------------|-------|
| AssetID, CompanyID, AssetTypeID | Key structure |
| Sha256, MimeType, SizeBytes | Storage metadata |
| WidthPx, HeightPx | **Required today** — make nullable for documents (Story 5.7 migration) |
| StorageProvider, StorageKey | Blob/local path |
| DisplayName, OriginalFileName | Display metadata |

**No separate `CompanyAsset` table** — `Asset.CompanyID` provides company scoping.

### 2.4 Company Details & Billing → `Company`, `CompanyBillingDetails`

| Table | Purpose |
|-------|---------|
| **dbo.Company** | CompanyName, ABN, Phone, Email, CountryID, etc. |
| **dbo.CompanyBillingDetails** | BillingContactName, BillingEmail, BillingAddressLine1/2, City, State, PostalCode, BillingCountryID (1:1 with Company) |

- **Story 5.7:** Company Settings hub needs GET/PUT APIs for Company + CompanyBillingDetails (verify existence/extend).  

---

## 3. Story 5.7 Data Model Requirements

| Area | Current Table(s) | Story 5.7 Need | Gap |
|------|------------------|-----------------|-----|
| Company Details | Company, CompanyBillingDetails | GET/PUT APIs | Confirm APIs exist |
| Form Branding | CompanyFormDefaults | UI in hub (tab) | None — data exists |
| Form Workflow | CompanyFormTestConfig | UI bound to existing API | None — data exists |
| Assets (Images) | Asset (AssetType=IMAGE) | List, upload, delete | Extend asset API for list/delete UI |
| Assets (Terms/Document/Video) | Asset (AssetType) | IMAGE, TERMS, DOCUMENT, VIDEO | Migration: add ref.AssetType TERMS, DOCUMENT, VIDEO; Asset.WidthPx/HeightPx nullable |

**Conclusion:** Current schema supports Story 5.7 with:
- **Migration 1:** Add ref.AssetType `DOCUMENT` or `TERMS`
- **Migration 2:** Make Asset.WidthPx, Asset.HeightPx nullable for non-image assets

---

## 4. Proposed: Company Defaults per Domain Table

You requested a table that stores **Defaults for companies for each domain**. Today we have separate tables per domain (CompanyFormDefaults, CompanyFormTestConfig). A unified pattern would:

1. Allow new settings domains without new tables
2. Provide a single place for “company defaults by domain”
3. Support schema-versioned JSON per domain (like CompanyFormDefaults)

### 4.1 Reference Table: `ref.CompanyDomain`

Defines available domains for company defaults:

```sql
-- ref.CompanyDomain: Defines settings domains
CREATE TABLE [ref].[CompanyDomain] (
    CompanyDomainID INT IDENTITY(1,1) PRIMARY KEY,
    DomainCode NVARCHAR(50) NOT NULL UNIQUE,   -- e.g. FORM_BRANDING, FORM_WORKFLOW
    DomainName NVARCHAR(100) NOT NULL,
    Description NVARCHAR(500) NULL,
    SchemaVersionRef NVARCHAR(100) NULL,       -- e.g. FormDefaultsSchemaVersion, or inline schema
    IsActive BIT NOT NULL DEFAULT 1,
    DisplayOrder INT NOT NULL DEFAULT 0,
    -- Audit
    CreatedDate DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    UpdatedDate DATETIME2 NULL
);

-- Seed domains (align with existing tables)
INSERT INTO [ref].[CompanyDomain] (DomainCode, DomainName, Description, DisplayOrder) VALUES
('FORM_BRANDING', 'Form Branding', 'Theme, global styles, default grid layouts', 1),
('FORM_WORKFLOW', 'Form Workflow', 'Test threshold, publish approval', 2);
-- Future: ASSETS_POLICY, FONTS_PREFERENCES, etc.
```

### 4.2 Data Table: `dbo.CompanyDomainDefault`

Stores defaults per company per domain:

```sql
-- dbo.CompanyDomainDefault: One row per company per domain
CREATE TABLE [dbo].[CompanyDomainDefault] (
    CompanyDomainDefaultID BIGINT IDENTITY(1,1) PRIMARY KEY,
    CompanyID BIGINT NOT NULL,
    CompanyDomainID INT NOT NULL,
    DefaultsJSON NVARCHAR(MAX) NOT NULL,
    SchemaVersionString NVARCHAR(20) NULL,       -- e.g. "1.0" for JSON schema version
    IsActive BIT NOT NULL DEFAULT 1,
    IsDeleted BIT NOT NULL DEFAULT 0,
    -- Audit
    CreatedDate DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,
    -- Constraints
    CONSTRAINT UQ_CompanyDomainDefault_Company_Domain UNIQUE (CompanyID, CompanyDomainID),
    CONSTRAINT FK_CompanyDomainDefault_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID),
    CONSTRAINT FK_CompanyDomainDefault_Domain FOREIGN KEY (CompanyDomainID) REFERENCES [ref].[CompanyDomain](CompanyDomainID),
    CONSTRAINT FK_CompanyDomainDefault_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_CompanyDomainDefault_UpdatedBy FOREIGN KEY (UpdatedBy) REFERENCES [dbo].[User](UserID)
);

CREATE INDEX IX_CompanyDomainDefault_CompanyID ON [dbo].[CompanyDomainDefault] (CompanyID);
CREATE INDEX IX_CompanyDomainDefault_CompanyDomainID ON [dbo].[CompanyDomainDefault] (CompanyDomainID);
```

**DefaultsJSON examples by domain:**
- **FORM_BRANDING:** Same structure as CompanyFormDefaults.DefaultsJSON (theme, globalStyles, etc.)
- **FORM_WORKFLOW:** `{"testThresholdEnabled": true, "testThresholdValue": 5, "requirePublishApproval": true}`
- **Future domains:** Domain-specific JSON structure

### 4.3 Migration Path

| Phase | Action |
|-------|--------|
| **Immediate (Story 5.7)** | No change — use existing CompanyFormDefaults, CompanyFormTestConfig, Asset |
| **Follow-on** | Add ref.CompanyDomain + dbo.CompanyDomainDefault; seed domains |
| **Optional later** | Migrate CompanyFormTestConfig into CompanyDomainDefault (FORM_WORKFLOW) for unified pattern; keep CompanyFormDefaults for now (it has version history) |

**Recommendation:** Implement `ref.CompanyDomain` and `dbo.CompanyDomainDefault` in a follow-on story *after* 5.7. Use them for **new** domains (e.g. ASSETS_POLICY, FONTS_PREFERENCES). Migrate FORM_WORKFLOW from CompanyFormTestConfig only if the team opts for full unification.

---

## 5. Story 5.7 Implementation Checklist

| Item | Action | Migration? |
|------|--------|------------|
| Company + CompanyBillingDetails | Ensure GET/PUT APIs for Company Admin | No |
| CompanyFormDefaults | Form Branding tab reads/writes via existing service | No |
| CompanyFormTestConfig | Form Workflow tab uses GET/PUT `/api/forms/company-test-config` | No |
| CompanyFormTestConfigVersion | Audit trail for Form Workflow changes | Yes |
| CompanyBillingDetailsVersion | Audit trail for billing/invoicing changes | Yes |
| CompanyVersion | Audit trail for Company details (optional in 5.7) | Yes (if in scope) |
| ref.AssetType | Add DOCUMENT or TERMS | Yes |
| Asset | WidthPx, HeightPx nullable | Yes |
| CompanyDomainDefault | Defer to follow-on | N/A |

---

## 6. Audit Trail — Form Branding Pattern

Form Branding uses an **append-only version table** for audit. The same pattern should apply to other Company Settings areas.

### 6.1 Form Branding Pattern (Reference)

| Table | Purpose | Pattern |
|-------|---------|---------|
| **CompanyFormDefaults** | Current effective state | One row per CompanyID; UpdatedBy, UpdatedDate |
| **CompanyFormDefaultsVersion** | Immutable audit history | Append-only; insert on every change; VersionNumber, DefaultsJSON (full snapshot), ChangeSummary, CreatedDate, CreatedBy |

**Behaviour:** On every PUT, insert a new row into the Version table with the full snapshot, then update the main table. Version history API returns rows ordered by VersionNumber desc.

### 6.2 Audit Requirements by Area

| Area | Main Table | Version Table | Notes |
|------|-------------|----------------|--------|
| **Form Branding** | CompanyFormDefaults | CompanyFormDefaultsVersion | ✅ Exists |
| **Form Workflow** | CompanyFormTestConfig | CompanyFormTestConfigVersion | ❌ Add |
| **Company Details** | Company | CompanyVersion | ❌ Add (or extend ActivityLog) |
| **Billing** | CompanyBillingDetails | CompanyBillingDetailsVersion | ❌ Add — important for invoicing |
| **Company Domain Defaults** (future) | CompanyDomainDefault | CompanyDomainDefaultVersion | ❌ Add with initial implementation |
| **Assets** | Asset | — | Soft delete + CreatedBy/UpdatedBy; content immutable (replace = new asset) |
| **Terms URL** (if stored at company level) | In Company or CompanyAsset | Version or ActivityLog | Depends on storage model |

### 6.3 Proposed Version Tables

#### CompanyFormTestConfigVersion

```sql
-- Append-only audit for Form Workflow changes
CREATE TABLE [dbo].[CompanyFormTestConfigVersion] (
    CompanyFormTestConfigVersionID BIGINT IDENTITY(1,1) PRIMARY KEY,
    CompanyID BIGINT NOT NULL,
    TestThresholdEnabled BIT NOT NULL,
    TestThresholdValue INT NOT NULL,
    RequirePublishApproval BIT NOT NULL,
    ChangeSummary NVARCHAR(500) NULL,
    CreatedDate DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    CreatedBy BIGINT NULL,
    CONSTRAINT FK_CompanyFormTestConfigVersion_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID),
    CONSTRAINT FK_CompanyFormTestConfigVersion_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [dbo].[User](UserID)
);
CREATE INDEX IX_CompanyFormTestConfigVersion_CompanyID ON [dbo].[CompanyFormTestConfigVersion] (CompanyID, CreatedDate DESC);
```

#### CompanyBillingDetailsVersion

```sql
-- Append-only audit for billing/invoicing changes
CREATE TABLE [dbo].[CompanyBillingDetailsVersion] (
    CompanyBillingDetailsVersionID BIGINT IDENTITY(1,1) PRIMARY KEY,
    CompanyID BIGINT NOT NULL,
    BillingContactName NVARCHAR(200) NULL,
    BillingEmail NVARCHAR(255) NULL,
    BillingPhone NVARCHAR(20) NULL,
    BillingAddressLine1 NVARCHAR(255) NULL,
    BillingAddressLine2 NVARCHAR(255) NULL,
    BillingCity NVARCHAR(100) NULL,
    BillingState NVARCHAR(100) NULL,
    BillingPostalCode NVARCHAR(20) NULL,
    BillingCountryID BIGINT NULL,
    ChangeSummary NVARCHAR(500) NULL,
    CreatedDate DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    CreatedBy BIGINT NULL,
    CONSTRAINT FK_CompanyBillingDetailsVersion_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID),
    CONSTRAINT FK_CompanyBillingDetailsVersion_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [dbo].[User](UserID)
);
CREATE INDEX IX_CompanyBillingDetailsVersion_CompanyID ON [dbo].[CompanyBillingDetailsVersion] (CompanyID, CreatedDate DESC);
```

#### CompanyDomainDefaultVersion (when CompanyDomainDefault is added)

```sql
-- Append-only audit for domain defaults (mirrors CompanyFormDefaultsVersion)
CREATE TABLE [dbo].[CompanyDomainDefaultVersion] (
    CompanyDomainDefaultVersionID BIGINT IDENTITY(1,1) PRIMARY KEY,
    CompanyID BIGINT NOT NULL,
    CompanyDomainID INT NOT NULL,
    VersionNumber INT NOT NULL,
    DefaultsJSON NVARCHAR(MAX) NOT NULL,
    ChangeSummary NVARCHAR(500) NULL,
    CreatedDate DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    CreatedBy BIGINT NULL,
    CONSTRAINT FK_CompanyDomainDefaultVersion_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID),
    CONSTRAINT FK_CompanyDomainDefaultVersion_Domain FOREIGN KEY (CompanyDomainID) REFERENCES [ref].[CompanyDomain](CompanyDomainID),
    CONSTRAINT FK_CompanyDomainDefaultVersion_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [dbo].[User](UserID)
);
CREATE INDEX IX_CompanyDomainDefaultVersion_Company_Domain ON [dbo].[CompanyDomainDefaultVersion] (CompanyID, CompanyDomainID, VersionNumber DESC);
```

### 6.4 Company (Details) Audit

Company fields (CompanyName, ABN, Phone, Email, etc.) change less often than billing. Options:

- **Option A:** `CompanyVersion` — full snapshot of company fields on each change (same pattern).
- **Option B:** Rely on `ActivityLog` or similar if it already captures company changes.
- **Option C:** Combine with `CompanyBillingDetailsVersion` if company edits happen in the same flow — store company snapshot in a separate table or as JSON in a generic `CompanySettingsVersion` table.

**Recommendation:** Add `CompanyVersion` for invoicing/compliance — ABN, legal name, and company details changes should be auditable.

### 6.5 Implementation Order

| Phase | Action |
|-------|--------|
| **Story 5.7** | Add CompanyFormTestConfigVersion, CompanyBillingDetailsVersion (and CompanyVersion if scope allows) — migrations; update PUT services to insert version row on change |
| **Follow-on** | CompanyDomainDefaultVersion when CompanyDomainDefault is implemented |
| **Assets** | No version table; Asset has CreatedBy/UpdatedBy; soft delete; content changes = new asset |

### 6.6 Service Pattern

For each PUT that mutates audited data:

1. Load current row.
2. Compute `ChangeSummary` (e.g. "Updated test threshold to 5, enabled publish approval").
3. Insert row into `*Version` table with new values (or full JSON snapshot).
4. Update main table.

Expose `GET /api/.../version-history` (or equivalent) for version history UI.

---

## 7. Summary

- **Form Branding:** `CompanyFormDefaults` + `CompanyFormDefaultsVersion` — no change for 5.7  
- **Form Workflow:** `CompanyFormTestConfig` — add `CompanyFormTestConfigVersion` for audit  
- **Billing:** `CompanyBillingDetails` — add `CompanyBillingDetailsVersion` for invoicing audit  
- **Company Details:** Consider `CompanyVersion` for ABN/legal name audit  
- **Company Assets:** `Asset` with soft delete; no version table (content immutable)  
- **Company Domain Defaults (future):** `CompanyDomainDefault` + `CompanyDomainDefaultVersion` — version table from day one  

---

*Last Updated: 2026-02-17*
