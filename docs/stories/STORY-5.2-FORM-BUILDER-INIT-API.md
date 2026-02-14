# Form Builder Init API — Single Payload Design

**Purpose:** Single API that returns all data required to start building a new form. Form Builder receives one payload; frontend manages changes and writes complete DefinitionJSON back on save.  
**Story:** 5.2  
**Status:** Design  
**Created:** 2026-02-13  

---

## 1. Context

- **Form Header** holds `CompanyID` and `EventID`. `Event` has `CountryID` (or derives from event context).
- **Start new form flow:** User selects Event (or Company) → navigates to Form Builder → request includes `CompanyID`, `EventID`.
- **API responsibility:** Return merged defaults + component catalog + initial DefinitionJSON skeleton for that form’s context.

---

## 2. Request Contract

### Endpoint

```
POST /api/form-builder/init
```

**Request body:**

```json
{
  "companyId": 123,
  "eventId": 456
}
```

**Alternative (query params):**

```
GET /api/form-builder/init?companyId=123&eventId=456
```

**Resolution:**
- `CompanyID` → used for company defaults and company-scoped components.
- `EventID` → used to resolve `CountryID` (e.g. `Event.CountryID` or `Event.Venue.CountryID`). Used for country-scoped components and defaults.

---

## 3. Response Contract (Single Payload)

```json
{
  "schemaVersion": 1,
  "context": {
    "companyId": 123,
    "eventId": 456,
    "countryId": 42
  },
  "defaults": {
    "theme": { "primaryColor": "#...", "fontFamily": "...", ... },
    "globalStyles": { "labelFontFamily": "...", "baseSpacing": 8, ... },
    "canvasSettings": { "width": 1200, "height": 630, "gridSize": 8 },
    "defaultGridLayoutsByComponent": {
      "text": { "vertical": {...}, "horizontal": {...} },
      "email": { "vertical": {...}, "horizontal": {...} }
    }
  },
  "components": [
    {
      "componentCode": "text",
      "displayName": "Text",
      "category": "basic",
      "sortOrder": 0,
      "propertiesSchema": { ... },
      "structure": { "objects": [...], "defaultLayout": "vertical" },
      "defaultGridLayoutVertical": { "rows": 1, "columns": 2, "cellAssignments": {...} },
      "defaultGridLayoutHorizontal": { "rows": 1, "columns": 2, "cellAssignments": {...} },
      "validationConfig": null
    }
  ],
  "definitionJSON": {
    "schemaVersion": 1,
    "theme": null,
    "globalStyles": null,
    "canvasSettings": null,
    "pages": [ { "id": "...", "components": [] } ],
    "logic": []
  }
}
```

---

## 4. Payload Sections

| Section | Source | Description |
|---------|--------|-------------|
| `schemaVersion` | `ref.FormDefaultsSchemaVersion` | Schema version for defaults + DefinitionJSON evolution. |
| `context` | Request + resolved | Echo back companyId, eventId, countryId for frontend reference. |
| `defaults` | Resolver merge | Global + Company defaults merged. `defaultGridLayoutsByComponent` includes **only** allowed components. |
| `components` | `dbo.FormBuilderComponent` | Components for CompanyID + CountryID (Global ∪ Country ∪ Company). Full schema per component. |
| `definitionJSON` | Generated | Skeleton: empty pages, no form overrides. Frontend hydrates with defaults and fills as user builds. |

---

## 5. Resolver Logic (Backend)

1. Resolve `CountryID` from `EventID` (Event.CountryID or equivalent).
2. Load global defaults from `dbo.GlobalFormDefaults` (IsActive=1).
3. Load company defaults from `dbo.CompanyFormDefaults` (CompanyID, IsActive=1).
4. Deep-merge: Company overrides Global.
5. Load components from `dbo.FormBuilderComponent`:
   - Global scope (CountryID NULL, CompanyID NULL)
   - Country scope (CountryID = @CountryID)
   - Company scope (CompanyID = @CompanyID)
6. Assemble `defaultGridLayoutsByComponent` from:
   - Either defaults JSON (filtered by allowed component codes), or
   - Component rows (DefaultGridLayoutVerticalJSON, DefaultGridLayoutHorizontalJSON per component).
7. Generate initial `definitionJSON` skeleton with empty pages.

---

## 6. Frontend Flow

1. **Start new form:** Call `POST /api/form-builder/init` with `companyId`, `eventId`.
2. **Receive payload:** Store `defaults`, `components`, `definitionJSON`.
3. **Initialize builder state:** Use `definitionJSON` as base; apply `defaults` for rendering; use `components` as toolbox catalog.
4. **User edits:** Frontend updates `definitionJSON` (pages, components, logic, theme, globalStyles).
5. **Save:** Persist full `definitionJSON` to `FormVersion.DefinitionJSON` (or equivalent). No need to re-fetch defaults on save.

---

## 7. Relationship to Existing Tables

| Table | Role |
|-------|------|
| `ref.FormDefaultsSchemaVersion` | Version for defaults schema |
| `dbo.GlobalFormDefaults` | Global theme, globalStyles, canvasSettings, defaultGridLayoutsByComponent |
| `dbo.CompanyFormDefaults` | Company overrides (same structure) |
| `ref.ComponentType` | Base component kinds |
| `ref.ComponentScope` | Global, Country, Company |
| `dbo.FormBuilderComponent` | Scoped component definitions with schemas and layouts |

---

## 8. Implementation Order

1. **T00:** Database schema + seeds (defaults + component catalog).
2. **Backend:** Form Builder Init API (T01+); resolver for defaults + components.
3. **Validation:** Test API against existing frontend structure; ensure response matches expected shapes.
4. **Frontend:** Replace hardcoded defaults/components with API response; persist DefinitionJSON on save.

---

*Single payload design — Form Builder gets everything in one call.*
