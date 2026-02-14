# Story 5.2: Data Schema — Global & Company Form Defaults

**Story:** 5.2 - Company Form Defaults (Brand System)  
**Consultant:** Data Domain Architect / Business Analyst  
**Created:** 2026-02-13  
**Updated:** 2026-02-13 (schema versioning, grid layout, T00 prerequisite)  
**Status:** Draft for Review  
**References:**  
- `docs/stories/STORY-5.2-UX-EXPERT-CONSULTATION.md`  
- `docs/stories/STORY-5.2-DEFINITION-JSON-DATABASE-DRIVEN-EVALUATION.md` (DefinitionJSON alignment, schemaVersion, grid layout)  
- `docs/database-naming-rules.md` (MANDATORY)  
- `docs/solution-architecture.md`  

---

## Executive Summary

This document defines the database schema to support a **multi-tenant, multi-user platform** with:

1. **Global Defaults** — platform-wide form branding baseline (including grid layout defaults)
2. **Company Defaults** — per-company form branding defaults
3. **Schema versioning** — `ref.FormDefaultsSchemaVersion` tracks DefaultsJSON structure evolution across platform enhancements
4. **Full audit trail** — who changed what, when; version history with immutable snapshots
5. **Robustness** — tenant isolation, indexes for scale, NVARCHAR for Unicode

All tables follow `docs/database-naming-rules.md`: PascalCase, `[TableName]ID` PKs, standard audit columns, constraints, indexes.

---

## 1. Inheritance Model (Data Perspective)

| Tier | Table(s) | Scope |
|------|----------|-------|
| **Global Defaults** | `dbo.GlobalFormDefaults`, `dbo.GlobalFormDefaultsVersion` | Platform-wide; one effective row |
| **Company Defaults** | `dbo.CompanyFormDefaults`, `dbo.CompanyFormDefaultsVersion` | Per CompanyID (one row per company) |
| **Form Overrides** | Stored in `FormVersion.DefinitionJSON` | Per form |
| **Component Overrides** | Stored in `FormVersion.DefinitionJSON` | Per component |

---

## 2. Schema Versioning

**Why:** As the platform evolves, the DefaultsJSON structure will change (new fields, breaking changes). We must track which schema version each payload conforms to for compatibility and migration.

**Table:** `ref.FormDefaultsSchemaVersion`

| Column | Type | Constraints |
|--------|------|-------------|
| FormDefaultsSchemaVersionID | BIGINT | PK, IDENTITY |
| SchemaVersion | INT | NOT NULL, UNIQUE |
| SchemaName | NVARCHAR(100) | NOT NULL |
| Description | NVARCHAR(500) | NULL |
| SchemaDocument | NVARCHAR(MAX) | NULL (JSON schema or field list) |
| IsActive | BIT | NOT NULL, DEFAULT 1 |
| CreatedDate | DATETIME2 | NOT NULL, DEFAULT GETUTCDATE() |
| CreatedBy | BIGINT | NULL, FK → dbo.User.UserID |

**Usage:** `GlobalFormDefaults` and `CompanyFormDefaults` (and their Version tables) reference `FormDefaultsSchemaVersionID`. Resolver and API can validate/transform payloads based on schema version.

---

## 3. Data Points to Store

Aligned with actual DefinitionJSON structure. See `STORY-5.2-DEFINITION-JSON-DATABASE-DRIVEN-EVALUATION.md`.

| Category | Fields | Scope | Notes |
|----------|--------|-------|-------|
| **theme** | primaryColor, backgroundColor, fontFamily | Global, Company | Subset of DefinitionJSON.theme |
| **globalStyles** | Full object (fontFamily, fontSize, labelFontFamily, defaultGridLayoutsByComponent, etc.) | Global, Company | 30+ fields; core of defaults |
| **defaultGridLayoutsByComponent** | Per component: `vertical` and `horizontal` layouts | Global, Company | Each has rows, columns, cellAssignments |
| **canvasSettings** | width, height, gridSize | Global | Design-system level |
| **background** | asset reference + placement | Global, Company, Form | Story 5.1 |

**defaultGridLayoutsByComponent** — Store both dimensions:
```json
"defaultGridLayoutsByComponent": {
  "text": {
    "vertical": { "rows": 3, "columns": 1, "cellAssignments": { ... } },
    "horizontal": { "rows": 2, "columns": 3, "cellAssignments": { ... } }
  }
}
```
Frontend switches by defaultLayout; both provided from DB.

---

## 4. Table Definitions (Full DDL Style)

All definitions follow `docs/database-naming-rules.md`.

### 4.1 ref.FormDefaultsSchemaVersion

```sql
CREATE TABLE [ref].[FormDefaultsSchemaVersion] (
    FormDefaultsSchemaVersionID BIGINT IDENTITY(1,1) NOT NULL,
    SchemaVersion INT NOT NULL,
    SchemaName NVARCHAR(100) NOT NULL,
    Description NVARCHAR(500) NULL,
    SchemaDocument NVARCHAR(MAX) NULL,
    IsActive BIT NOT NULL DEFAULT 1,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,

    CONSTRAINT PK_FormDefaultsSchemaVersion_FormDefaultsSchemaVersionID PRIMARY KEY (FormDefaultsSchemaVersionID),
    CONSTRAINT UQ_FormDefaultsSchemaVersion_SchemaVersion UNIQUE (SchemaVersion),
    CONSTRAINT FK_FormDefaultsSchemaVersion_User_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [dbo].[User](UserID)
);

CREATE INDEX IX_FormDefaultsSchemaVersion_IsActive ON [ref].[FormDefaultsSchemaVersion](IsActive);
```

**Seed:** Insert initial schema version (e.g. SchemaVersion = 1) for MVP structure.

---

### 4.2 dbo.GlobalFormDefaults

**Purpose:** Single effective row for platform-wide defaults. Updated in place; history in Version table.

```sql
CREATE TABLE [dbo].[GlobalFormDefaults] (
    GlobalFormDefaultsID BIGINT IDENTITY(1,1) NOT NULL,
    FormDefaultsSchemaVersionID BIGINT NOT NULL,
    VersionNumber INT NOT NULL,
    DefaultsJSON NVARCHAR(MAX) NOT NULL,
    IsActive BIT NOT NULL DEFAULT 1,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,

    CONSTRAINT PK_GlobalFormDefaults_GlobalFormDefaultsID PRIMARY KEY (GlobalFormDefaultsID),
    CONSTRAINT FK_GlobalFormDefaults_FormDefaultsSchemaVersion FOREIGN KEY (FormDefaultsSchemaVersionID) REFERENCES [ref].[FormDefaultsSchemaVersion](FormDefaultsSchemaVersionID),
    CONSTRAINT FK_GlobalFormDefaults_User_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_GlobalFormDefaults_User_UpdatedBy FOREIGN KEY (UpdatedBy) REFERENCES [dbo].[User](UserID)
);

CREATE UNIQUE INDEX IX_GlobalFormDefaults_IsActive ON [dbo].[GlobalFormDefaults](IsActive) WHERE IsActive = 1;
```

**Constraint:** Only one row with `IsActive = 1` (enforced by unique filtered index).

---

### 4.3 dbo.GlobalFormDefaultsVersion

**Purpose:** Immutable audit history for global defaults. Insert on every change.

```sql
CREATE TABLE [dbo].[GlobalFormDefaultsVersion] (
    GlobalFormDefaultsVersionID BIGINT IDENTITY(1,1) NOT NULL,
    FormDefaultsSchemaVersionID BIGINT NOT NULL,
    VersionNumber INT NOT NULL,
    DefaultsJSON NVARCHAR(MAX) NOT NULL,
    ChangeSummary NVARCHAR(500) NULL,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,

    CONSTRAINT PK_GlobalFormDefaultsVersion_GlobalFormDefaultsVersionID PRIMARY KEY (GlobalFormDefaultsVersionID),
    CONSTRAINT FK_GlobalFormDefaultsVersion_FormDefaultsSchemaVersion FOREIGN KEY (FormDefaultsSchemaVersionID) REFERENCES [ref].[FormDefaultsSchemaVersion](FormDefaultsSchemaVersionID),
    CONSTRAINT FK_GlobalFormDefaultsVersion_User_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [dbo].[User](UserID)
);

CREATE INDEX IX_GlobalFormDefaultsVersion_VersionNumber ON [dbo].[GlobalFormDefaultsVersion](VersionNumber);
```

---

### 4.4 dbo.CompanyFormDefaults

**Purpose:** Current effective defaults per company. One row per CompanyID.

```sql
CREATE TABLE [dbo].[CompanyFormDefaults] (
    CompanyFormDefaultsID BIGINT IDENTITY(1,1) NOT NULL,
    CompanyID BIGINT NOT NULL,
    FormDefaultsSchemaVersionID BIGINT NOT NULL,
    VersionNumber INT NOT NULL,
    DefaultsJSON NVARCHAR(MAX) NOT NULL,
    IsActive BIT NOT NULL DEFAULT 1,
    IsDeleted BIT NOT NULL DEFAULT 0,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,

    CONSTRAINT PK_CompanyFormDefaults_CompanyFormDefaultsID PRIMARY KEY (CompanyFormDefaultsID),
    CONSTRAINT UQ_CompanyFormDefaults_CompanyID UNIQUE (CompanyID),
    CONSTRAINT FK_CompanyFormDefaults_Company_CompanyID FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID),
    CONSTRAINT FK_CompanyFormDefaults_FormDefaultsSchemaVersion FOREIGN KEY (FormDefaultsSchemaVersionID) REFERENCES [ref].[FormDefaultsSchemaVersion](FormDefaultsSchemaVersionID),
    CONSTRAINT FK_CompanyFormDefaults_User_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_CompanyFormDefaults_User_UpdatedBy FOREIGN KEY (UpdatedBy) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_CompanyFormDefaults_User_DeletedBy FOREIGN KEY (DeletedBy) REFERENCES [dbo].[User](UserID)
);

CREATE INDEX IX_CompanyFormDefaults_CompanyID ON [dbo].[CompanyFormDefaults](CompanyID);
CREATE INDEX IX_CompanyFormDefaults_IsActive_IsDeleted ON [dbo].[CompanyFormDefaults](IsActive, IsDeleted);
```

**Tenant isolation:** All company-scoped queries MUST filter by `CompanyID` from the authenticated user's context. RBAC enforces company access.

---

### 4.5 dbo.CompanyFormDefaultsVersion

**Purpose:** Immutable audit history per company. Insert on every change.

```sql
CREATE TABLE [dbo].[CompanyFormDefaultsVersion] (
    CompanyFormDefaultsVersionID BIGINT IDENTITY(1,1) NOT NULL,
    CompanyID BIGINT NOT NULL,
    FormDefaultsSchemaVersionID BIGINT NOT NULL,
    VersionNumber INT NOT NULL,
    DefaultsJSON NVARCHAR(MAX) NOT NULL,
    ChangeSummary NVARCHAR(500) NULL,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,

    CONSTRAINT PK_CompanyFormDefaultsVersion_CompanyFormDefaultsVersionID PRIMARY KEY (CompanyFormDefaultsVersionID),
    CONSTRAINT FK_CompanyFormDefaultsVersion_Company_CompanyID FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID),
    CONSTRAINT FK_CompanyFormDefaultsVersion_FormDefaultsSchemaVersion FOREIGN KEY (FormDefaultsSchemaVersionID) REFERENCES [ref].[FormDefaultsSchemaVersion](FormDefaultsSchemaVersionID),
    CONSTRAINT FK_CompanyFormDefaultsVersion_User_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [dbo].[User](UserID)
);

CREATE INDEX IX_CompanyFormDefaultsVersion_CompanyID_VersionNumber ON [dbo].[CompanyFormDefaultsVersion](CompanyID, VersionNumber DESC);
```

**Audit query:** Efficient for "change history" by CompanyID.

---

## 5. DefaultsJSON Payload (Schema Version 1)

Structure aligned with DefinitionJSON. Backend merges Global → Company → form overrides to produce full DefinitionJSON for frontend.

```json
{
  "schemaVersion": "1.0",
  "theme": {
    "primaryColor": "#0055FF",
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter"
  },
  "globalStyles": {
    "fontFamily": "Inter",
    "fontSize": 14,
    "fontWeight": 400,
    "labelFontFamily": "Inter",
    "defaultLayout": "vertical",
    "defaultObjectLayout": "vertical",
    "defaultGridLayoutsByComponent": {
      "text": {
        "vertical": { "rows": 3, "columns": 1, "cellAssignments": { "0-0": "label", "1-0": "input", "2-0": "validation" } },
        "horizontal": { "rows": 2, "columns": 3, "cellAssignments": { ... } }
      }
    }
  },
  "canvasSettings": {
    "width": 1920,
    "height": 980,
    "gridSize": 8
  },
  "background": { "asset": { }, "placement": { } }
}
```

**defaultGridLayoutsByComponent:** Both `vertical` and `horizontal` per component, stored in DB. Frontend uses defaultLayout to select.

---

## 6. Security & Multi-Tenancy

| Concern | Implementation |
|---------|----------------|
| **Tenant isolation** | Company defaults: always filter by `CompanyID` from user's company. Middleware validates user belongs to company. |
| **Global access** | Global defaults: only System Admin / platform admin can read/write. RBAC check. |
| **Audit** | Every change records `CreatedBy`/`UpdatedBy` (UserID). Version tables are append-only. |
| **Soft delete** | CompanyFormDefaults supports `IsDeleted`, `DeletedDate`, `DeletedBy` for reversible removal. |
| **Schema evolution** | New schema versions added to `ref.FormDefaultsSchemaVersion`. Migration logic converts old → new when needed. |

---

## 7. Resolver Logic (Conceptual)

1. Load **Global Defaults** (includes `gridLayout`).
2. Load **Company Defaults** for form's company.
3. Deep merge: Company overrides Global (gridLayout from global unless company overrides).
4. Apply **Form Overrides** from `FormVersion.DefinitionJSON`.
5. Apply **Component Overrides** from component props.

---

## 8. T00 Prerequisite — Database Setup

**Task T00** must complete before any API or frontend work (T01+). T00 covers **defaults and component catalog**.

**T00 deliverables:**
1. Migration creating `ref.FormDefaultsSchemaVersion` + seed row(s)
2. Migration creating `dbo.GlobalFormDefaults`, `dbo.GlobalFormDefaultsVersion`
3. Migration creating `dbo.CompanyFormDefaults`, `dbo.CompanyFormDefaultsVersion`
4. Seed initial global defaults (with grid layout)
5. Migration creating `ref.ComponentType`, `ref.ComponentScope`, `dbo.FormBuilderComponent`
6. Seed component catalog (Global-scoped MVP components)
7. Validation against `docs/database-naming-rules.md`

See `docs/tasks/5.2/T00-database-form-defaults-schema.md` and `docs/stories/COMPONENT-CATALOG-SCHEMA-DESIGN.md`.

---

## 9. Migration Checklist

- [ ] Create `ref.FormDefaultsSchemaVersion` + seed SchemaVersion 1
- [ ] Create `dbo.GlobalFormDefaults`, `dbo.GlobalFormDefaultsVersion`
- [ ] Create `dbo.CompanyFormDefaults`, `dbo.CompanyFormDefaultsVersion`
- [ ] Seed `dbo.GlobalFormDefaults` (one row, IsActive=1, with gridLayout)
- [ ] Create `ref.ComponentType`, `ref.ComponentScope`, `dbo.FormBuilderComponent`
- [ ] Seed `ref.ComponentScope` (Global, Country, Company)
- [ ] Seed `ref.ComponentType` (MVP types)
- [ ] Seed `dbo.FormBuilderComponent` (global-scoped MVP components)
- [ ] Indexes per specs
- [ ] Validate against `docs/database-naming-rules.md`

---

## 10. API Contract (Post-T00)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/form-defaults/global` | GET | Current global defaults (admin only) |
| `/api/form-defaults/global` | PUT | Update global defaults (admin only) |
| `/api/form-defaults/global/history` | GET | Global version history (admin only) |
| `/api/companies/{id}/form-defaults` | GET | Current company defaults (merged with global) |
| `/api/companies/{id}/form-defaults` | PUT | Update company defaults (company admin) |
| `/api/companies/{id}/form-defaults/history` | GET | Company version history |
| `/api/form-builder/init` | POST | **Single payload:** merged defaults + component catalog + DefinitionJSON skeleton. Body: `{ companyId, eventId }`. See `docs/stories/STORY-5.2-FORM-BUILDER-INIT-API.md`. |

---

## 11. Backlog Items

| Item | Description |
|------|-------------|
| **Global Defaults screen** | Administration Settings page for Global Form Defaults (mirror of Company Defaults page). |

**Note:** Form Builder Init API and Component Catalog delivery are in scope for Story 5.2.

---

*Data Schema — prepared for Story 5.2 implementation*  
*Conforms to docs/database-naming-rules.md*  
*Last Updated: 2026-02-13*
