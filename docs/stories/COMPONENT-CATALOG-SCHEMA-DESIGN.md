# Component Catalog Schema — Multi-Country, Multi-Company Design

**Purpose:** Database schema to support component availability and schema delivery scoped by Global, Country, or Company  
**Created:** 2026-02-13  
**Status:** Design for Future Implementation  
**References:**  
- `docs/stories/STORY-5.2-DATA-SCHEMA.md` (defaults)  
- `docs/COMPONENT-FRAMEWORK-REFERENCE.md` (framework)  
- `docs/database-naming-rules.md` (MANDATORY)  

---

## 1. Business Requirements

| Requirement | Description |
|-------------|-------------|
| **Multi-country** | Components can be country-specific (e.g. AU address validation, US phone format) |
| **Multi-company** | Companies can have custom components only they can use |
| **Global** | Platform-wide components (text, email, etc.) available to everyone |
| **Scalable** | 1000s of components; Form Builder receives only schema data for **allowed** components |
| **Controlled delivery** | When a form is created: DB provides component catalog for that form's Country + Company |
| **Schema per component** | Each component has properties schema, structure, defaultGridLayouts — stored in DB, not hardcoded |
| **globalStyles alignment** | Component schemas reference which globalStyles keys they use; defaults payload can be trimmed |

---

## 2. Scope Model

Components are available at one of three scopes:

| Scope | ScopeRef | Who sees it |
|-------|----------|-------------|
| **Global** | NULL | All forms, all countries, all companies |
| **Country** | CountryID | Forms whose Company/Event is in that country |
| **Company** | CompanyID | Forms belonging to that company only |

**Resolution for form creation:** Given `CompanyID` and `CountryID` (from `Company.CountryID` or `Event.CountryID`):
- Include all components where Scope = Global
- Include all components where Scope = Country AND CountryID = @CountryID
- Include all components where Scope = Company AND CompanyID = @CompanyID

---

## 3. Entity Relationship Overview

```
ref.ComponentType (base component kinds)
       │
       │ 1:N
       ▼
dbo.FormBuilderComponent (scoped component definition)
       ├── Scope: Global | Country | Company
       ├── ScopeRefID: NULL | CountryID | CompanyID
       ├── PropertiesSchemaJSON
       ├── StructureJSON
       ├── DefaultGridLayoutVerticalJSON
       ├── DefaultGridLayoutHorizontalJSON
       └── ValidationConfigJSON (e.g. country-specific address rules)

ref.ComponentType
       │
       │ N:1 (optional - for base layout inheritance)
       ▼
dbo.FormBuilderComponent (can extend/override base)
```

---

## 4. Table Definitions

### 4.1 ref.ComponentType

**Purpose:** Base catalog of component "kinds". One row per component type (text, email, address, phone, etc.). Used as reference; actual availability and schema come from FormBuilderComponent.

```sql
CREATE TABLE [ref].[ComponentType] (
    ComponentTypeID BIGINT IDENTITY(1,1) NOT NULL,
    ComponentTypeCode NVARCHAR(50) NOT NULL,
    DisplayName NVARCHAR(100) NOT NULL,
    Description NVARCHAR(500) NULL,
    Category NVARCHAR(50) NULL,
    SortOrder INT NOT NULL DEFAULT 0,
    IsActive BIT NOT NULL DEFAULT 1,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,

    CONSTRAINT PK_ComponentType_ComponentTypeID PRIMARY KEY (ComponentTypeID),
    CONSTRAINT UQ_ComponentType_ComponentTypeCode UNIQUE (ComponentTypeCode),
    CONSTRAINT FK_ComponentType_User_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_ComponentType_User_UpdatedBy FOREIGN KEY (UpdatedBy) REFERENCES [dbo].[User](UserID)
);

CREATE INDEX IX_ComponentType_ComponentTypeCode ON [ref].[ComponentType](ComponentTypeCode);
CREATE INDEX IX_ComponentType_IsActive_SortOrder ON [ref].[ComponentType](IsActive, SortOrder);
```

**Seed:** text, number, email, phone, address, first-name, date, checkbox, radio, textarea, dropdown, terms, submit-button, header, divider, etc.

---

### 4.2 ref.ComponentScope

**Purpose:** Reference table for scope type (avoids magic strings).

```sql
CREATE TABLE [ref].[ComponentScope] (
    ComponentScopeID BIGINT IDENTITY(1,1) NOT NULL,
    ScopeCode NVARCHAR(20) NOT NULL,
    ScopeName NVARCHAR(100) NOT NULL,
    Description NVARCHAR(500) NULL,
    IsActive BIT NOT NULL DEFAULT 1,

    CONSTRAINT PK_ComponentScope_ComponentScopeID PRIMARY KEY (ComponentScopeID),
    CONSTRAINT UQ_ComponentScope_ScopeCode UNIQUE (ScopeCode)
);

-- Seed: Global, Country, Company
```

---

### 4.3 dbo.FormBuilderComponent

**Purpose:** Scoped component definition. Defines which components are available at Global, Country, or Company level, with full schema data (properties, structure, layouts). The Form Builder receives only rows applicable to the form's context.

```sql
CREATE TABLE [dbo].[FormBuilderComponent] (
    FormBuilderComponentID BIGINT IDENTITY(1,1) NOT NULL,
    ComponentTypeID BIGINT NOT NULL,
    ComponentScopeID BIGINT NOT NULL,
    CountryID BIGINT NULL,
    CompanyID BIGINT NULL,
    ComponentCode NVARCHAR(100) NOT NULL,
    DisplayName NVARCHAR(200) NOT NULL,
    Description NVARCHAR(500) NULL,
    SortOrder INT NOT NULL DEFAULT 0,
    PropertiesSchemaJSON NVARCHAR(MAX) NULL,
    StructureJSON NVARCHAR(MAX) NULL,
    DefaultGridLayoutVerticalJSON NVARCHAR(MAX) NULL,
    DefaultGridLayoutHorizontalJSON NVARCHAR(MAX) NULL,
    ValidationConfigJSON NVARCHAR(MAX) NULL,
    GlobalStylesRelevantKeys NVARCHAR(MAX) NULL,
    IsActive BIT NOT NULL DEFAULT 1,
    IsDeleted BIT NOT NULL DEFAULT 0,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,

    CONSTRAINT PK_FormBuilderComponent_FormBuilderComponentID PRIMARY KEY (FormBuilderComponentID),
    CONSTRAINT FK_FormBuilderComponent_ComponentType FOREIGN KEY (ComponentTypeID) REFERENCES [ref].[ComponentType](ComponentTypeID),
    CONSTRAINT FK_FormBuilderComponent_ComponentScope FOREIGN KEY (ComponentScopeID) REFERENCES [ref].[ComponentScope](ComponentScopeID),
    CONSTRAINT FK_FormBuilderComponent_Country FOREIGN KEY (CountryID) REFERENCES [ref].[Country](CountryID),
    CONSTRAINT FK_FormBuilderComponent_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID),
    CONSTRAINT FK_FormBuilderComponent_User_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_FormBuilderComponent_User_UpdatedBy FOREIGN KEY (UpdatedBy) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_FormBuilderComponent_User_DeletedBy FOREIGN KEY (DeletedBy) REFERENCES [dbo].[User](UserID)
);

-- Scope invariant (enforce in application): Global => CountryID NULL, CompanyID NULL; Country => CountryID NOT NULL, CompanyID NULL; Company => CompanyID NOT NULL, CountryID NULL

CREATE INDEX IX_FormBuilderComponent_ComponentTypeID ON [dbo].[FormBuilderComponent](ComponentTypeID);
CREATE INDEX IX_FormBuilderComponent_Scope_Country ON [dbo].[FormBuilderComponent](ComponentScopeID, CountryID) WHERE CountryID IS NOT NULL;
CREATE INDEX IX_FormBuilderComponent_Scope_Company ON [dbo].[FormBuilderComponent](ComponentScopeID, CompanyID) WHERE CompanyID IS NOT NULL;
CREATE INDEX IX_FormBuilderComponent_ScopeGlobal ON [dbo].[FormBuilderComponent](ComponentScopeID) WHERE CountryID IS NULL AND CompanyID IS NULL;
CREATE INDEX IX_FormBuilderComponent_IsActive_IsDeleted ON [dbo].[FormBuilderComponent](IsActive, IsDeleted);
```

**Column usage:**

| Column | Purpose |
|--------|---------|
| ComponentTypeID | Links to base component kind |
| ComponentScopeID | Global, Country, or Company |
| CountryID | Set when Scope=Country; NULL otherwise |
| CompanyID | Set when Scope=Company; NULL otherwise |
| ComponentCode | Unique identifier for Form Builder (e.g. "text", "address-au", "custom-widget-x") |
| PropertiesSchemaJSON | JSON Schema or field list for component props (label, required, placeholder, options, styleOverrides, etc.) |
| StructureJSON | Object structure (label, input, validation, etc.); matches ComponentRegistry structure |
| DefaultGridLayoutVerticalJSON | rows, columns, cellAssignments for vertical layout |
| DefaultGridLayoutHorizontalJSON | rows, columns, cellAssignments for horizontal layout |
| ValidationConfigJSON | Country/company-specific validation (e.g. AU address fields, US postal format) |
| GlobalStylesRelevantKeys | JSON array of globalStyles keys this component uses; for lean defaults payload |

---

## 5. Resolver: Components for a Form

**Input:** `CompanyID`, `CountryID` (from `Company.CountryID` or `Event.CountryID`)

**Query logic (conceptual):**
```sql
SELECT fbc.*
FROM dbo.FormBuilderComponent fbc
WHERE fbc.IsActive = 1 AND fbc.IsDeleted = 0
  AND (
    (fbc.ComponentScopeID = @ScopeGlobal)
    OR (fbc.ComponentScopeID = @ScopeCountry AND fbc.CountryID = @CountryID)
    OR (fbc.ComponentScopeID = @ScopeCompany AND fbc.CompanyID = @CompanyID)
  )
ORDER BY fbc.SortOrder, fbc.DisplayName;
```

**Output:** List of components with full schema (PropertiesSchemaJSON, StructureJSON, DefaultGridLayoutVerticalJSON, DefaultGridLayoutHorizontalJSON, ValidationConfigJSON). Form Builder receives only these; no need to load 1000s.

---

## 6. Integration with Defaults

**defaultGridLayoutsByComponent** in GlobalFormDefaults/CompanyFormDefaults can:
- **Option A:** Remain as today — single blob with all component layouts. Resolver filters to allowed components only when building payload.
- **Option B:** Move to FormBuilderComponent — each component row stores its own DefaultGridLayoutVerticalJSON, DefaultGridLayoutHorizontalJSON. Global/Company defaults no longer store defaultGridLayoutsByComponent; instead, resolver assembles it from FormBuilderComponent rows for allowed components.

**Recommendation for scale:** Option B. Component layouts are component-specific; storing them per component supports country/company variants (e.g. AU address has different layout than US address).

**globalStyles:** Remain in GlobalFormDefaults/CompanyFormDefaults. Optional: use GlobalStylesRelevantKeys to trim the payload to only keys used by allowed components (optimization for very large globalStyles).

---

## 7. Example Data (Conceptual)

| ComponentCode | Scope | CountryID | CompanyID | Use case |
|---------------|-------|-----------|-----------|----------|
| text | Global | NULL | NULL | All forms |
| email | Global | NULL | NULL | All forms |
| phone | Global | NULL | NULL | Generic phone |
| address | Country | 1 (AU) | NULL | AU address with AU validation |
| address | Country | 2 (US) | NULL | US address with US validation |
| custom-lead-widget | Company | NULL | 123 | Company 123 only |

---

## 8. API Contract

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/form-builder/components` | GET | Components for form context. Query params: `companyId`, `countryId`. Returns catalog with schemas for allowed components. |
| `/api/form-builder/components/{componentCode}` | GET | Single component schema (admin or when adding to form). |
| `/api/admin/components` | GET/POST/PUT | Manage FormBuilderComponent (System Admin). |
| `/api/companies/{id}/components` | GET/POST/PUT | Company-scoped components (Company Admin). |

---

## 9. Migration Phasing

| Phase | Scope | Tables |
|-------|-------|--------|
| **Phase 1 (Story 5.2)** | Defaults only | FormDefaultsSchemaVersion, GlobalFormDefaults, CompanyFormDefaults (existing) |
| **Phase 2** | Component catalog (Global) | ref.ComponentType, ref.ComponentScope, dbo.FormBuilderComponent. Seed global components. |
| **Phase 3** | Country-scoped components | Add country-specific rows (address per country, etc.). |
| **Phase 4** | Company-scoped components | Company custom components. UI for Company Admin to add. |

---

## 10. Backward Compatibility

- **MVP:** Form Builder continues to use hardcoded component list and schemas. No breaking change.
- **Transition:** When component catalog is implemented, API `/api/form-builder/components` returns same structure as current frontend expects. Frontend switches from static registry to API-driven.
- **Existing forms:** DefinitionJSON stores `component.type` (e.g. "text", "address"). Resolver must map ComponentCode to type; existing forms keep working.

---

## 11. Summary

| Concern | Design |
|---------|--------|
| **Multi-country** | FormBuilderComponent rows with Scope=Country, CountryID set |
| **Multi-company** | FormBuilderComponent rows with Scope=Company, CompanyID set |
| **Scalability** | Resolver returns only allowed components; Form Builder loads no unused schemas |
| **Schema in DB** | PropertiesSchemaJSON, StructureJSON, DefaultGridLayoutVertical/Horizontal per component |
| **Validation** | ValidationConfigJSON for country-specific rules (address, phone) |
| **Aligned with framework** | Structure matches ComponentRegistry; defaultGridLayouts by component; globalStyles keys optional trim |

---

*Component Catalog Schema — design for multi-country, multi-company, scalable component delivery*  
*Last Updated: 2026-02-13*
