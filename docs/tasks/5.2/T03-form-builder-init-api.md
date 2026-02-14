# Task T03: Form Builder Init API (Single Payload)

**Story:** 5.2 - Company Form Defaults (Brand System)  
**Task ID:** T03  
**Status:** ✅ HumanDone (pending merge)
**Dependencies:** T01, T02  
**Estimated Time:** 2–3 hours  

---

## 📋 Task Overview

**Objective:** Implement `POST /api/form-builder/init` that returns a single payload with merged defaults, component catalog, and initial DefinitionJSON skeleton for a form context (companyId, eventId).

**Reference:** `docs/stories/STORY-5.2-FORM-BUILDER-INIT-API.md`

---

## ✅ Scope (In)

- [x] Endpoint `POST /api/form-builder/init` with body `{ companyId, eventId }`
- [x] Resolve CountryID from EventID (Event.CountryID or equivalent)
- [x] Load and merge Global + Company defaults (use T02 resolver)
- [x] Load components: Global ∪ Country(CountryID) ∪ Company(CompanyID)
- [x] Assemble defaultGridLayoutsByComponent for allowed components only
- [x] Generate initial DefinitionJSON skeleton (empty pages, schemaVersion)
- [x] Return: schemaVersion, context, defaults, components, definitionJSON

---

## 🚫 Scope (Out)

- ❌ Frontend changes (T05)
- ❌ Persist DefinitionJSON on save (separate flow)

---

## ✅ Acceptance Criteria

### AC1: Endpoint exists
- POST `/api/form-builder/init` with `{ companyId, eventId }`
- Returns 200 with valid payload for valid input
- Returns 400/404 for invalid companyId or eventId

### AC2: Response contains merged defaults
- `defaults.theme`, `defaults.globalStyles`, `defaults.canvasSettings`
- `defaults.defaultGridLayoutsByComponent` (allowed components only)

### AC3: Response contains component catalog
- `components` array: one per allowed component (Global ∪ Country ∪ Company)
- Each has: componentCode, displayName, propertiesSchema, structure, defaultGridLayoutVertical, defaultGridLayoutHorizontal

### AC4: Response contains DefinitionJSON skeleton
- `definitionJSON` with schemaVersion, empty pages, empty logic

### AC5: Context echoed
- `context.companyId`, `context.eventId`, `context.countryId`

---

## 📚 References

- `docs/stories/STORY-5.2-FORM-BUILDER-INIT-API.md`
- `docs/stories/COMPONENT-CATALOG-SCHEMA-DESIGN.md`

---

## 🌿 Git

- Branch: `task/5.2/T03-form-builder-init-api`
- PR into: `story/epic5-5.2-company-form-defaults`
