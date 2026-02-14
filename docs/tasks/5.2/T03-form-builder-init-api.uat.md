# T03 UAT: Form Builder Init API

**Task:** T03 - Form Builder Init API (Single Payload)  
**Story:** 5.2 - Company Form Defaults (Brand System)  

---

## Prerequisites

- Database: Migration 039 applied (T01)
- T02 Defaults API working (Global + Company seeds)
- Backend venv activated
- Valid JWT; CompanyID and EventID exist

---

## UAT Steps

### AC1: Endpoint exists

#### POST /api/form-builder/init
- **Body:** `{ "companyId": 1, "eventId": 1 }`
- **Expected:** 200, valid payload
- **400/404:** Invalid companyId or eventId

### AC2: Response contains merged defaults

- `defaults.theme`, `defaults.globalStyles`, `defaults.canvasSettings`
- `defaults.defaultGridLayoutsByComponent` (allowed components only)

### AC3: Response contains component catalog

- `components` array: one per allowed component
- Each has: componentCode, displayName, propertiesSchema, structure, defaultGridLayoutVertical, defaultGridLayoutHorizontal

### AC4: Response contains DefinitionJSON skeleton

- `definitionJSON` with schemaVersion, empty pages, empty logic

### AC5: Context echoed

- `context.companyId`, `context.eventId`, `context.countryId`

---

*Execute steps; record results in T03-form-builder-init-api.uat-results.md*
