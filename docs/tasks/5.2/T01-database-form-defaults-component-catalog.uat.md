# T01 UAT: Database Form Defaults + Component Catalog

**Task:** T01 - Database Form Defaults + Component Catalog Schema + Seeds  
**Story:** 5.2 - Company Form Defaults (Brand System)  

---

## Prerequisites

- Database: EventLeadPlatform (SQL Server)
- Migration 038 applied
- Backend venv activated

---

## UAT Steps

### 1. Run migration

```powershell
cd backend
alembic upgrade head
```

**Expected:** Migration 039 applies successfully with no errors.

---

### 2. Validate Form Defaults schema

```sql
-- AC1: FormDefaultsSchemaVersion
SELECT * FROM [ref].[FormDefaultsSchemaVersion];
-- Expect: 1 row, SchemaVersion = 1

-- AC2: GlobalFormDefaults
SELECT GlobalFormDefaultsID, FormDefaultsSchemaVersionID, VersionNumber, IsActive,
       LEFT(DefaultsJSON, 200) AS DefaultsJSONPreview
FROM [dbo].[GlobalFormDefaults];
-- Expect: 1 row, IsActive = 1, DefaultsJSON starts with {"schemaVersion"

-- AC3: CompanyFormDefaults tables exist (no rows expected yet)
SELECT COUNT(*) FROM [dbo].[CompanyFormDefaults];
SELECT COUNT(*) FROM [dbo].[CompanyFormDefaultsVersion];
```

---

### 3. Validate Global defaults seed (AC4)

```sql
SELECT DefaultsJSON FROM [dbo].[GlobalFormDefaults] WHERE IsActive = 1;
```

**Verify DefaultsJSON contains:**
- `theme` (primaryColor, backgroundColor, fontFamily)
- `globalStyles` (fontFamily, fontSize, defaultGridLayoutsByComponent)
- `canvasSettings` (width, height, gridSize)

---

### 4. Validate Component Catalog schema (AC5)

```sql
-- ref.ComponentScope
SELECT * FROM [ref].[ComponentScope];
-- Expect: 3 rows (Global, Country, Company)

-- ref.ComponentType
SELECT ComponentTypeCode, DisplayName, Category FROM [ref].[ComponentType];
-- Expect: 14 rows (text, number, email, phone, first-name, date, checkbox, radio, textarea, dropdown, terms, submit-button, header, divider)

-- dbo.FormBuilderComponent
SELECT COUNT(*) FROM [dbo].[FormBuilderComponent];
-- Expect: 14 rows (global-scoped components)
```

---

### 5. Validate Component Catalog seed (AC6)

```sql
SELECT fbc.ComponentCode, fbc.DisplayName, fbc.SortOrder,
       CASE WHEN fbc.PropertiesSchemaJSON IS NOT NULL THEN 1 ELSE 0 END AS HasPropsSchema,
       CASE WHEN fbc.StructureJSON IS NOT NULL THEN 1 ELSE 0 END AS HasStructure,
       CASE WHEN fbc.DefaultGridLayoutVerticalJSON IS NOT NULL THEN 1 ELSE 0 END AS HasLayoutV,
       CASE WHEN fbc.DefaultGridLayoutHorizontalJSON IS NOT NULL THEN 1 ELSE 0 END AS HasLayoutH
FROM [dbo].[FormBuilderComponent] fbc
JOIN [ref].[ComponentScope] cs ON fbc.ComponentScopeID = cs.ComponentScopeID
WHERE cs.ScopeCode = 'Global' AND fbc.IsDeleted = 0
ORDER BY fbc.SortOrder;
```

**Expect:** At least 5 rows with HasPropsSchema=1, HasStructure=1, HasLayoutV=1, HasLayoutH=1.

---

## Pass Criteria

| AC | Criterion | Pass? |
|----|-----------|-------|
| AC1 | FormDefaultsSchemaVersion exists with seed row | ☐ |
| AC2 | GlobalFormDefaults + Version tables exist | ☐ |
| AC3 | CompanyFormDefaults + Version tables exist | ☐ |
| AC4 | Global defaults seeded with theme, globalStyles, canvasSettings | ☐ |
| AC5 | ComponentType, ComponentScope, FormBuilderComponent exist | ☐ |
| AC6 | Global-scoped MVP components seeded with schemas and layouts | ☐ |

---

*Record results in T01-database-form-defaults-component-catalog.uat-results.md*
