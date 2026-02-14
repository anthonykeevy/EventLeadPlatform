# Task T06: Form Builder Init API (Single Payload)

**Story:** 5.2 - Company Form Defaults (Brand System)  
**Task ID:** T06  
**Status:** ⏸️ Pending  
**Dependencies:** T00, T01  
**Estimated Time:** 2-3 hours  

---

## 📋 Task Overview

**Objective:** Implement the Form Builder Init API that returns a single payload with all data required to start building a new form. Request includes `companyId` and `eventId`; response contains merged defaults, component catalog, and initial DefinitionJSON skeleton.

**Reference:** `docs/stories/STORY-5.2-FORM-BUILDER-INIT-API.md`

---

## ✅ Scope (In)

- [ ] Endpoint `POST /api/form-builder/init` with body `{ companyId, eventId }`
- [ ] Resolve `CountryID` from `EventID` (Event.CountryID or equivalent)
- [ ] Load and merge Global + Company defaults (deep merge)
- [ ] Load components: Global ∪ Country(CountryID) ∪ Company(CompanyID)
- [ ] Assemble `defaultGridLayoutsByComponent` for allowed components only
- [ ] Generate initial DefinitionJSON skeleton (empty pages, schemaVersion)
- [ ] Return single response: schemaVersion, context, defaults, components, definitionJSON
- [ ] Response shape matches `docs/stories/STORY-5.2-FORM-BUILDER-INIT-API.md`

---

## 🚫 Scope (Out)

- ❌ Frontend changes (T03)
- ❌ Persist DefinitionJSON on save (separate flow; Form Builder writes back)
- ❌ Admin UI for components (backlog)

---

## ✅ Acceptance Criteria

### AC1: Endpoint exists and accepts request
- `POST /api/form-builder/init` with JSON body `{ "companyId": number, "eventId": number }`
- Returns 200 with valid payload for valid input
- Returns 400/404 for invalid companyId or eventId

### AC2: Response contains merged defaults
- `defaults.theme`, `defaults.globalStyles`, `defaults.canvasSettings` from Global + Company merge
- `defaults.defaultGridLayoutsByComponent` contains only components allowed for context

### AC3: Response contains component catalog
- `components` array: one entry per allowed component (Global ∪ Country ∪ Company)
- Each entry has: componentCode, displayName, category, sortOrder, propertiesSchema, structure, defaultGridLayoutVertical, defaultGridLayoutHorizontal, validationConfig

### AC4: Response contains DefinitionJSON skeleton
- `definitionJSON` with schemaVersion, empty pages array (one page), empty logic array
- theme, globalStyles, canvasSettings null (frontend applies from defaults)

### AC5: Context echoed
- `context.companyId`, `context.eventId`, `context.countryId` in response

---

## 🧪 Required Tests / Verification

- Unit test: resolver merges Global + Company defaults correctly
- Unit test: component query returns correct set for given CompanyID + CountryID
- Integration test: endpoint returns valid payload for known company+event
- Manual: response structure matches existing frontend ComponentRegistry / defaultGridLayoutsByComponent shape

---

## 📚 References

- API design: `docs/stories/STORY-5.2-FORM-BUILDER-INIT-API.md`
- Data schema: `docs/stories/STORY-5.2-DATA-SCHEMA.md`
- Component catalog: `docs/stories/COMPONENT-CATALOG-SCHEMA-DESIGN.md`
- Component framework: `docs/COMPONENT-FRAMEWORK-REFERENCE.md`

---

## 🌿 Git / PR Requirements

- Branch: `task/5.2/T06-form-builder-init-api`
- PR into: `story/epic5-5.2-company-form-defaults`

```powershell
scripts/git/new-task.ps1 -StoryBranch "story/epic5-5.2-company-form-defaults" -StoryId 5.2 -TaskId T06 -Slug "form-builder-init-api" -CreateWorktree
```

---

*Form Builder Init API — single payload for starting a new form*
