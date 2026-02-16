# Story 5.3: Schema + Validation Alignment

**Epic:** Epic 5 - Form Builder Readiness + Review & Publishing  
**Domain:** Backend + Form Builder integration  
**Status:** ⏳ Ready  
**Priority:** High (foundation for drift prevention)  
**Created:** 2026-02-16  
**Owner:** Developer Agent  

---

## 📖 User Story

**As a** platform maintainer,  
**I want** the backend definition schema to validate the real builder output (structure + key invariants),  
**So that** we prevent drift between what the Form Builder produces and what we persist, and we can safely evolve the schema over time.

**Context & entry point:**  
- Stories 5.1 and 5.2 are complete: assets, company defaults, and Form Builder Init API are in place.  
- Today `backend/schemas/form_definition.py` is **minimal** compared to what the builder produces (globalStyles, theme, canvasSettings, defaultGridLayoutsByComponent, background, pages, logic, desktopPages/tabletPages/mobilePages).  
- Unknown keys are effectively ignored; we are not validating what we ship → drift risk.

---

## 🧭 Scope Boundary

**Principle:** All form data (including schema definitions) must be managed from the database. Story 5.3 builds on Story 5.2's `ref.FormDefaultsSchemaVersion` table, which already provides `SchemaDocument` (NVARCHAR(MAX)) for storing JSON Schema or field definitions.

### In scope (Story 5.3)

- **Schema alignment**
  - Backend Pydantic schema models the **real** DefinitionJSON structure produced by the builder.
  - Validate top-level keys: `schemaVersion`, `formId`, `theme`, `globalStyles`, `logic`, `canvasSettings`, `pages` (and device variants `desktopPages`, `tabletPages`, `mobilePages`).
  - Validate key invariants: unique component IDs, logic rule integrity (source ≠ target), non-empty pages where required.
  - Reject or handle unknown keys explicitly (no silent ignore by default).
- **Schema versioning**
  - Track DefinitionJSON schema version (e.g. `"1.0"`); support compatibility/migration strategy.
  - Document how new schema versions are introduced and how backward compatibility is maintained.
  - **Integrate with `ref.FormDefaultsSchemaVersion`** (Story 5.2): Populate `SchemaDocument` with DefinitionJSON JSON Schema; backend validation and API read from DB.
- **Schema-from-DB API**
  - `GET /api/form-schema/{version}` — Returns the schema definition (JSON Schema) for the requested version from `ref.FormDefaultsSchemaVersion.SchemaDocument`.
  - Enables Form Builder and other clients to fetch schema at runtime; supports future schema versions without frontend deploy.
  - Version mapping: DefinitionJSON uses string `"1.0"`; DB has `SchemaVersion` INT. Add `SchemaVersionString` (e.g. `"1.0"`) to support API contract, or document mapping (1 → "1.0").
- **Compatibility tests**
  - Tests that builder output (or representative fixtures) passes backend validation.
  - Regression protection: changes to builder output must not break validation without explicit schema update.

### Out of scope (Story 5.3)

- Shared resolver parity (Story 5.4).
- Preview/production governance (Story 5.5+).
- Publish workflow (Story 5.6+).
- Changing frontend TypeScript types (frontend stays authoritative for its types; backend aligns to them).

---

## 🎯 Done Criteria

- [ ] **DC1:** Backend schema validates the full DefinitionJSON structure produced by the builder (theme, globalStyles, canvasSettings, logic, pages with background, desktopPages/tabletPages/mobilePages where present).
- [ ] **DC2:** Schema versioning is documented; `schemaVersion` is validated; compatibility/migration strategy exists (even if minimal for v1.0); schema definition stored in `ref.FormDefaultsSchemaVersion.SchemaDocument`.
- [ ] **DC3:** Compatibility tests prove builder output passes backend validation; regression protection in place.
- [ ] **DC4:** Key invariants enforced: unique component IDs, logic rule integrity (sourceComponentId ≠ targetComponentId).
- [ ] **DC5:** `GET /api/form-schema/{version}` returns DefinitionJSON JSON Schema from DB; Form Builder (or other clients) can fetch schema at init; all schema data managed from database.
- [ ] **DC6:** UAT guide executed and marked PASSED.
- [ ] **DC7:** Story PR merged to `master`.

---

## 📐 Builder Output Structure (Reference)

The Form Builder produces DefinitionJSON with this structure (from `frontend/src/features/builder/types/builder.types.ts` and `useBuilderStore.ts`):

| Key | Type | Notes |
|-----|------|-------|
| `schemaVersion` | string | e.g. `"1.0"` |
| `formId` | string | Form identifier |
| `theme` | `{ primaryColor, backgroundColor, fontFamily }` | FormTheme |
| `globalStyles` | GlobalStyles | 30+ fields: typography, colors, spacing, borders, layout, defaultGridLayout, defaultGridLayoutsByComponent |
| `logic` | `{ rules: LogicRule[] }` | Optional; rules have when/then, operators (equals, notEquals, contains, isEmpty, etc.), actions (show, hide, require, etc.) |
| `canvasSettings` | `{ width, height, gridSize, backgroundColor? }` | Optional |
| `pages` | FormPage[] | Legacy; at least one page |
| `desktopPages` | FormPage[]? | Device-specific; same structure as pages |
| `tabletPages` | FormPage[]? | Device-specific |
| `mobilePages` | FormPage[]? | Device-specific |

**FormPage:** `{ id, title, components, background? }`  
**background:** `{ type: 'color' | 'image', value?, assetRef?, placement? }` (Story 5.1: asset ref, not base64)  
**FormComponent:** `{ id, type, props, position?, styleOverrides?, children?, gridLayout? }`  

**Current backend gap:** `form_definition.py` has `theme`, `pages`, `logic` only; misses `globalStyles`, `canvasSettings`, `background` on pages, device-specific page arrays, and the full component/grid structure.

---

## 📚 References

- Epic scope: `docs/stories/EPIC-5-STATUS.md`
- Story 5.2 data schema: `docs/stories/STORY-5.2-DATA-SCHEMA.md` — `ref.FormDefaultsSchemaVersion` (SchemaVersion, SchemaDocument) is the source of truth for schema definitions
- Builder output evaluation: `docs/stories/STORY-5.2-DEFINITION-JSON-DATABASE-DRIVEN-EVALUATION.md`
- Current backend schema: `backend/schemas/form_definition.py`
- Builder types: `frontend/src/features/builder/types/builder.types.ts`
- PRD: `docs/prd.md`
- Git workflow: `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`

---

*Story 5.3 - Schema + Validation Alignment*  
*Last Updated: 2026-02-16*
