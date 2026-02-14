# Task T01: Database — Form Defaults + Component Catalog Schema + Seeds

**Story:** 5.2 - Company Form Defaults (Brand System)  
**Task ID:** T01  
**Status:** ✅ Done (UAT passed 2026-02-14) 
**Dependencies:** None (first task)  
**Estimated Time:** 4–6 hours  

---

## 📋 Task Overview

**Objective:** Create the complete database schema for Form Defaults and Component Catalog, plus all seed data, **before** any API or frontend work. This is the prerequisite for all other Story 5.2 tasks.

All tables must conform to `docs/database-naming-rules.md`. **Human runs migration** — agent never runs Alembic directly (per .cursorrules).

---

## ✅ Scope (In)

### Form Defaults
- [ ] Migration: `ref.FormDefaultsSchemaVersion` + seed (SchemaVersion = 1)
- [ ] Migration: `dbo.GlobalFormDefaults`, `dbo.GlobalFormDefaultsVersion`
- [ ] Migration: `dbo.CompanyFormDefaults`, `dbo.CompanyFormDefaultsVersion`
- [ ] Seed: One row in `dbo.GlobalFormDefaults` (IsActive=1) with DefaultsJSON including theme, globalStyles, defaultGridLayoutsByComponent, canvasSettings

### Component Catalog
- [ ] Migration: `ref.ComponentType` + seed MVP types (text, number, email, phone, first-name, date, checkbox, radio, textarea, dropdown, terms, submit-button, header, divider)
- [ ] Migration: `ref.ComponentScope` + seed (Global, Country, Company)
- [ ] Migration: `dbo.FormBuilderComponent`
- [ ] Seed: Global-scoped MVP components with PropertiesSchemaJSON, StructureJSON, DefaultGridLayoutVerticalJSON, DefaultGridLayoutHorizontalJSON

### General
- [ ] All constraints, indexes, FKs per reference docs
- [ ] Validate against `docs/database-naming-rules.md`

---

## 🚫 Scope (Out)

- ❌ API endpoints (T02, T03)
- ❌ Frontend changes (T04, T05)
- ❌ Resolver implementation (T02, T06)

---

## 🔒 Forbidden Zones

| Path | Reason |
|------|--------|
| `frontend/` | DB-only task |
| `backend/modules/` routers, services | API work is T02+ |

---

## ✅ Acceptance Criteria

### AC1: Form defaults schema exists
- `ref.FormDefaultsSchemaVersion` with FormDefaultsSchemaVersionID, SchemaVersion, SchemaName, Description, SchemaDocument, IsActive, audit columns
- Seed row (SchemaVersion = 1)

### AC2: Global defaults tables exist
- `dbo.GlobalFormDefaults` with FormDefaultsSchemaVersionID FK, DefaultsJSON, VersionNumber, IsActive, audit columns
- `dbo.GlobalFormDefaultsVersion` for audit history
- Filtered unique index: only one row with IsActive = 1

### AC3: Company defaults tables exist
- `dbo.CompanyFormDefaults` with CompanyID (unique), FormDefaultsSchemaVersionID FK, DefaultsJSON, VersionNumber, IsActive, IsDeleted, full audit columns
- `dbo.CompanyFormDefaultsVersion` for audit history

### AC4: Global defaults seeded
- One row in `dbo.GlobalFormDefaults` (IsActive=1)
- DefaultsJSON includes theme, globalStyles (with defaultGridLayoutsByComponent), canvasSettings

### AC5: Component catalog tables exist
- `ref.ComponentType`, `ref.ComponentScope`, `dbo.FormBuilderComponent`
- Indexes per `docs/stories/COMPONENT-CATALOG-SCHEMA-DESIGN.md`

### AC6: Component catalog seeded
- Seed `ref.ComponentScope` (Global, Country, Company)
- Seed `ref.ComponentType` (MVP types)
- Seed `dbo.FormBuilderComponent` (global-scoped MVP components with schemas and layouts)

---

## 🧪 Required Tests / Verification

- Migration file linted for naming conventions
- **Human runs migration**
- Seed data validated: at least one global default, at least 5 global components with schemas

---

## 📚 References

- `docs/stories/STORY-5.2-DATA-SCHEMA.md`
- `docs/stories/COMPONENT-CATALOG-SCHEMA-DESIGN.md`
- `docs/database-naming-rules.md`

---

## 🌿 Git

- Branch: `task/5.2/T01-database-form-defaults-component-catalog`
- PR into: `story/epic5-5.2-company-form-defaults`

```powershell
scripts/git/new-task.ps1 -StoryBranch "story/epic5-5.2-company-form-defaults" -StoryId 5.2 -TaskId T01 -Slug "database-form-defaults-component-catalog" -CreateWorktree
```
