# Story 5.2: DefinitionJSON — Database-Driven Architecture Evaluation

**Purpose:** Rationalize and evaluate moving Form Builder data from frontend-hardcoded to database-driven  
**Created:** 2026-02-13  
**Context:** DefinitionJSON structure now known; Form Builder is stable; opportunity to drive platform from database  

---

## 1. Your Position (Summary)

| Area | Your thinking |
|------|---------------|
| **Database-first** | Drive the platform from the database; backend provides JSON to frontend |
| **schemaVersion** | Store schema definition (class) in DB; provide to FormBuilder so it stays lean |
| **theme** | Consider a table for Theme at Global, Company, Form, Component levels |
| **globalStyles** | Must be in DB |
| **defaultGridLayoutsByComponent** | Add Vertical/Horizontal layer (currently frontend only); store both in DB; frontend switches |
| **logic** | Empty until customer configures; not part of defaults |
| **canvasSettings** | Store in DB |
| **pages** | Form-specific; stores overrides |

---

## 2. schemaVersion — Rationalization & Pros/Cons

### What schemaVersion Actually Is

Today `schemaVersion` (e.g. `"1.0"`) is a **version identifier** — it tells the frontend “this DefinitionJSON conforms to structure v1.0.” The frontend has a **type/class** (TypeScript interface or runtime validator) that defines the expected shape. If the backend sends v1.1 with new fields, the frontend either ignores them or must be updated.

**Your idea:** Store the schema *definition* (the class / type / JSON Schema) in the database and serve it to the FormBuilder. The FormBuilder then uses only the schema it receives — no hardcoded structure.

### Pros of Schema Definition in Database

| Pro | Explanation |
|-----|-------------|
| **Single source of truth** | Schema lives in DB; backend and frontend both read from it. No drift between BE/FE type definitions. |
| **Lean FormBuilder** | FormBuilder doesn’t ship with every possible schema version; it gets the one it needs at runtime. |
| **Runtime polymorphism** | New schema versions can be deployed to DB without frontend deploy. Backend serves both schema and data. |
| **Multi-version support** | Old forms (v1.0) and new forms (v1.1) can coexist; resolver returns schema + data matching each form. |
| **Audit & governance** | Schema evolution is versioned and auditable in the database. |

### Cons of Schema Definition in Database

| Con | Explanation |
|-----|-------------|
| **Complexity** | FormBuilder must dynamically interpret schema (e.g. JSON Schema → runtime validation, or codegen at load). More complex than compile-time types. |
| **TypeScript** | Static typing is weakened — no compile-time safety if structure comes from API. Need runtime validation. |
| **Bootstrap chicken-egg** | FormBuilder needs *something* to parse the schema (meta-schema). That meta-schema is still frontend code. |
| **Performance** | Fetching schema + data on every load adds latency. Caching helps but adds complexity. |
| **Debugging** | Type errors become runtime; stack traces are harder. |
| **Version pinning** | FormBuilder may need to support multiple schema versions; increases bundle/runtime complexity. |

### Recommendation: Hybrid

**Phase 1 (Story 5.2):**  
- Keep `schemaVersion` as a **version identifier** (string like `"1.0"`).  
- Store it in DB and in DefinitionJSON.  
- Store the **JSON Schema** (or structured field list) in `ref.FormDefaultsSchemaVersion.SchemaDocument`.  
- Backend uses it for validation and migration.  
- Frontend keeps a minimal v1.0 type for the structure it *knows* it supports; unknown fields are allowed.

**Phase 2 (Backlog):**  
- Add API: `GET /api/form-schema/{version}` returning the schema definition.  
- FormBuilder fetches schema at init; uses it for runtime validation and optional dynamic UI generation.  
- Enables future schema versions without frontend deploy.

**Not recommended now:**  
- Shipping the full “class” (TypeScript) from DB. TypeScript is compile-time; runtime schema is JSON Schema or similar. Generating TS from DB is possible but adds a build-time step.

---

## 3. theme — Separate Table?

### Option A: Theme as its own table(s)

```
ref.Theme (or dbo.GlobalTheme, dbo.CompanyTheme)
├── ThemeID
├── primaryColor, backgroundColor, fontFamily, ...
```

**Pros:** Normalized; reusable; clear theme entity.  
**Cons:** Theme is small (3–5 fields). Many joins. DefinitionJSON already has theme; duplication of concepts.

### Option B: Theme inside DefaultsJSON

Theme is a subtree of `theme` in the defaults payload — as in your DefinitionJSON.

**Pros:** Matches current structure; simple; one payload for defaults.  
**Cons:** Not normalized; harder to query “all companies using font X.”

### Option C: Hybrid — Theme as JSON in a dedicated column

```
dbo.GlobalFormDefaults
├── ThemeJSON NVARCHAR(MAX)   -- just theme
├── GlobalStylesJSON NVARCHAR(MAX)
├── ...
```

**Pros:** Slightly more structured than one big blob.  
**Cons:** More columns; theme + globalStyles often used together; resolver still merges.

### Recommendation

**Keep theme inside the defaults payload (Option B)** for now. It’s small and tightly coupled to globalStyles. A separate Theme table adds complexity without clear benefit for Global/Company defaults. If you later need “find all companies with primaryColor X,” add a search index or computed column.

**For Form/Component overrides:** Theme stays inside `FormVersion.DefinitionJSON` as today — form and component overrides live in the definition, not in separate theme tables.

---

## 4. globalStyles — Agreed, In Database

`globalStyles` is large and rich (30+ fields). It should live in the database as the backbone of Global and Company defaults. The current STORY-5.2-DATA-SCHEMA uses `DefaultsJSON`; that blob should include `globalStyles` as a top-level key, consistent with your DefinitionJSON.

**Alignment:** Ensure `DefaultsJSON` in Global/Company tables stores `globalStyles` with the full field set you showed (fontFamily, fontSize, fontWeight, labelFontFamily, defaultGridLayoutsByComponent, etc.).

---

## 5. defaultGridLayoutsByComponent — Vertical/Horizontal Layer

**Current:** `defaultGridLayoutsByComponent` is keyed by component type (`"text"`, `"email"`, etc.), each with `rows`, `columns`, `cellAssignments`. There is no vertical vs horizontal split in the structure.

**Your idea:** Introduce a layer:

```json
"defaultGridLayoutsByComponent": {
  "text": {
    "vertical": { "rows": 3, "columns": 1, "cellAssignments": { ... } },
    "horizontal": { "rows": 2, "columns": 3, "cellAssignments": { ... } }
  },
  "checkbox": {
    "vertical": { ... },
    "horizontal": { ... }
  }
}
```

**Pros:**
- Single source of truth for both orientations.
- Frontend switches by `defaultLayout` (vertical/horizontal) without recomputing.
- Backend stores both; no layout logic in frontend.

**Cons:**
- Bigger payload; more to maintain per component.

**Recommendation:** Do it. Store both `vertical` and `horizontal` per component in the database. Frontend already has `defaultLayout` and `defaultObjectLayout`; the DB simply provides both layouts and the frontend picks the one matching the current layout mode. Aligns with “drive from database” and avoids layout logic in the client.

---

## 6. logic — Empty Until Configured

Agreed. Logic is form-specific and user-configured. Defaults should have `"logic": { "rules": [] }`. No need for a separate logic defaults table; it belongs in the form definition.

---

## 7. canvasSettings — In Database

`canvasSettings` (width, height, gridSize) is platform-wide configuration. It fits in **Global** defaults.

| Option | Recommendation |
|--------|-----------------|
| Global only | Yes — canvas dimensions are design-system level. |
| Company override | Optional later — e.g. “our brand uses 1080×1920.” |
| Form override | Already in DefinitionJSON today; keep. |

Add `canvasSettings` to the Global defaults payload in the schema.

---

## 8. pages — Form Overrides

`pages` is form-specific (structure, components, overrides). It stays in `FormVersion.DefinitionJSON`, not in Global/Company defaults. Company defaults supply `theme`, `globalStyles`, `canvasSettings`, `defaultGridLayoutsByComponent`; the resolver merges them with form-level `pages` and any overrides.

Correct as-is.

---

## 9. Overall: Database-Driven Platform

Your approach:

1. Build Form Builder first with frontend data classes for speed.
2. Stabilize.
3. Move data to database where possible.
4. Backend assembles DefinitionJSON and provides it to frontend.

Evaluation:

- **Practical:** Valid pattern. You validated the shape with the builder; now you can persist it properly.
- **Architectural:** Aligns with multi-tenant, configurable SaaS. Defaults in DB support per-company customization and future schema evolution.
- **Risk:** Migration from “frontend owns structure” to “backend owns structure” needs:
  - Clear schema versioning.
  - Resolver that always produces valid DefinitionJSON.
  - Backward compatibility for existing forms during rollout.
- **Phasing:** Do Global + Company defaults first (Story 5.2). Form-level DefinitionJSON (pages, logic, overrides) stays in FormVersion; you’re adding defaults that the resolver merges in.

---

## 10. Updated Data Model Alignment

Given your DefinitionJSON, the defaults payload should align as follows:

| DefinitionJSON Key | Source | Scope |
|--------------------|--------|-------|
| `schemaVersion` | From `ref.FormDefaultsSchemaVersion` or form | Metadata |
| `formId` | Form context | Form |
| `theme` | Defaults (Global → Company) + form override | Global, Company, Form |
| `globalStyles` | Defaults (Global → Company) + form override | Global, Company, Form |
| `globalStyles.defaultGridLayoutsByComponent` | Defaults, with `vertical` and `horizontal` per component | Global, Company |
| `logic` | Form definition | Form |
| `canvasSettings` | Defaults (Global) + optional Company/Form override | Global, Company, Form |
| `pages` | Form definition | Form |

**Resolver output:** Backend merges Global → Company → Form and returns a complete DefinitionJSON for the FormBuilder.

---

## 11. Summary

| Your idea | Verdict | Notes |
|-----------|---------|-------|
| Database-driven platform | ✅ Align | Phase rollout; start with defaults. |
| schemaVersion in DB | ✅ Partial | Use as version id + store JSON Schema in SchemaDocument; full “class from DB” is Phase 2. |
| Separate Theme table | ⚠️ Defer | Keep theme inside defaults payload for now. |
| globalStyles in DB | ✅ Agree | Core of Global/Company defaults. |
| defaultGridLayoutsByComponent with vertical/horizontal | ✅ Agree | Add layer; store both in DB. |
| logic empty by default | ✅ Agree | Form-level only. |
| canvasSettings in DB | ✅ Agree | In Global defaults. |
| pages = form overrides | ✅ Agree | Stay in FormVersion.DefinitionJSON. |

---

*Evaluation prepared for Story 5.2 design decisions*  
*Last Updated: 2026-02-13*
