# Task T00: Database — Form Defaults + Component Catalog Schema

**Story:** 5.2 - Company Form Defaults (Brand System)  
**Task ID:** T00  
**Status:** ⏸️ Pending  
**Dependencies:** None  
**Estimated Time:** 4-6 hours  

---

## 📋 Task Overview

**Objective:** Create the complete database schema for Form Defaults **and** Component Catalog **before** any API or frontend work. This task is a prerequisite for T01. By end of Story 5.2, the Form Builder will receive all component data via APIs from this schema.

All tables must conform to `docs/database-naming-rules.md`. Human executes migration.

---

## ✅ Scope (In)

### Form Defaults
- [ ] Create migration for `ref.FormDefaultsSchemaVersion` + seed initial schema version
- [ ] Create migration for `dbo.GlobalFormDefaults`, `dbo.GlobalFormDefaultsVersion`
- [ ] Create migration for `dbo.CompanyFormDefaults`, `dbo.CompanyFormDefaultsVersion`
- [ ] Seed `dbo.GlobalFormDefaults` with one row (platform baseline including grid layout)

### Component Catalog
- [ ] Create migration for `ref.ComponentType` + seed MVP component types
- [ ] Create migration for `ref.ComponentScope` + seed Global, Country, Company
- [ ] Create migration for `dbo.FormBuilderComponent`
- [ ] Seed global-scoped components for MVP (text, number, email, phone, first-name, date, checkbox, etc.) — schemas, structure, default layouts

### General
- [ ] All constraints, indexes, FKs per `docs/stories/STORY-5.2-DATA-SCHEMA.md` and `docs/stories/COMPONENT-CATALOG-SCHEMA-DESIGN.md`
- [ ] Validate naming against `docs/database-naming-rules.md`

---

## 🚫 Scope (Out)

- ❌ No API endpoints (T01)
- ❌ No frontend changes (T02, T03)
- ❌ No resolver implementation (T04)

---

## 🔒 Forbidden Zones

| Path | Reason |
|------|--------|
| `frontend/` | DB-only task |
| `backend/modules/` routers, services | API work is T01 |

---

## ✅ Acceptance Criteria

### AC1: Schema versioning table exists
- `ref.FormDefaultsSchemaVersion` with FormDefaultsSchemaVersionID, SchemaVersion, SchemaName, Description, SchemaDocument, IsActive, CreatedDate, CreatedBy
- At least one seed row (SchemaVersion = 1)

### AC2: Global defaults tables exist
- `dbo.GlobalFormDefaults` with FormDefaultsSchemaVersionID FK, DefaultsJSON, VersionNumber, IsActive, audit columns
- `dbo.GlobalFormDefaultsVersion` for audit history
- Filtered unique index so only one row has IsActive = 1

### AC3: Company defaults tables exist
- `dbo.CompanyFormDefaults` with CompanyID (unique), FormDefaultsSchemaVersionID FK, DefaultsJSON, VersionNumber, IsActive, IsDeleted, full audit columns
- `dbo.CompanyFormDefaultsVersion` for audit history
- Index on (CompanyID, VersionNumber) for efficient history queries

### AC4: Global defaults seeded
- One row in `dbo.GlobalFormDefaults` with IsActive = 1
- DefaultsJSON includes theme, typography, spacing, **gridLayout** (vertical, horizontal), background placeholder

### AC5: Naming rules compliance
- All tables/columns follow `docs/database-naming-rules.md` (PascalCase, NVARCHAR, PK/FK patterns, audit columns, constraints, indexes)

### AC6: Component catalog tables exist
- `ref.ComponentType` with ComponentTypeID, ComponentTypeCode, DisplayName, Category, SortOrder, IsActive, audit columns
- `ref.ComponentScope` with ScopeCode (Global, Country, Company)
- `dbo.FormBuilderComponent` with ComponentTypeID, ComponentScopeID, CountryID, CompanyID, ComponentCode, DisplayName, PropertiesSchemaJSON, StructureJSON, DefaultGridLayoutVerticalJSON, DefaultGridLayoutHorizontalJSON, ValidationConfigJSON, SortOrder, IsActive, IsDeleted, audit columns
- Indexes per `docs/stories/COMPONENT-CATALOG-SCHEMA-DESIGN.md` for efficient scope+country+company resolution

### AC7: Component catalog seeded
- Seed `ref.ComponentScope` with Global, Country, Company
- Seed `ref.ComponentType` with MVP types (text, number, email, phone, first-name, date, checkbox, radio, textarea, dropdown, terms, submit-button, header, divider, etc.)
- Seed `dbo.FormBuilderComponent` with global-scoped rows for MVP components (Scope=Global, CountryID=NULL, CompanyID=NULL)
- Each component row has PropertiesSchemaJSON, StructureJSON, DefaultGridLayoutVerticalJSON, DefaultGridLayoutHorizontalJSON matching current frontend `ComponentRegistry` / `defaultGridLayoutsByComponent` shape

---

## 🧪 Required Tests / Verification

- Migration file linted for naming conventions (Solomon checklist or manual review)
- **Human runs migration** (agent must not run Alembic commands per `.cursorrules`)
- Seed data validates: at least one global default, at least 5 global components with schemas

---

## 📚 References

- Data schema: `docs/stories/STORY-5.2-DATA-SCHEMA.md`
- Component catalog: `docs/stories/COMPONENT-CATALOG-SCHEMA-DESIGN.md`
- Form Builder Init API: `docs/stories/STORY-5.2-FORM-BUILDER-INIT-API.md`
- Naming rules: `docs/database-naming-rules.md`
- Story: `docs/stories/story-5.2.md`

---

## 🌿 Git / PR Requirements (Mandatory)

- Branch: `task/5.2/T00-database-form-defaults-component-catalog`
- PR into: `story/epic5-5.2-company-form-defaults`

```powershell
scripts/git/new-task.ps1 -StoryBranch "story/epic5-5.2-company-form-defaults" -StoryId 5.2 -TaskId T00 -Slug "database-form-defaults-component-catalog" -CreateWorktree
```

---

*T00 ensures complete database foundation (defaults + component catalog) is in place before APIs and frontend depend on it. Single payload API (Form Builder Init) consumes this data.*
