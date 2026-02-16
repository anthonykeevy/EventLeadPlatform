# Story 5.3: Schema Versioning & Compatibility

**Story:** 5.3 - Schema + Validation Alignment  
**Created:** 2026-02-16  
**Purpose:** Document DefinitionJSON schema versioning, compatibility strategy, and migration approach.

---

## 1. Schema Version Identifier

- **DefinitionJSON.schemaVersion:** String, e.g. `"1.0"`.
- **Database mapping:** `ref.FormDefaultsSchemaVersion.SchemaVersion` (INT) = 1 maps to DefinitionJSON `"1.0"`.
- **API contract:** `GET /api/form-schema/{version}` accepts `"1.0"` or `"1"`; returns JSON Schema from `SchemaDocument`.

---

## 2. Version 1.0 Structure

| Key | Required | Notes |
|-----|----------|-------|
| schemaVersion | ✅ | Literal `"1.0"` |
| formId | ✅ | Non-empty string |
| theme | ✅ | primaryColor, backgroundColor, fontFamily |
| pages | ✅ | At least one FormPage |
| globalStyles | ❌ | 30+ fields; optional |
| logic | ❌ | rules array |
| canvasSettings | ❌ | width, height, gridSize |
| desktopPages | ❌ | Device-specific layout |
| tabletPages | ❌ | Device-specific layout |
| mobilePages | ❌ | Device-specific layout |

**FormPage:** id, title, components, background?  
**FormComponent:** id, type, props, position?, style?, styleOverrides?, children?, gridLayout?

---

## 3. Key Invariants (Enforced by Backend)

- **Unique component IDs** within each page array (pages, desktopPages, tabletPages, mobilePages). Same ID may appear in different device arrays (same component, different layout).
- **Logic rule integrity:** `when.sourceComponentId` ≠ `then.targetComponentId`.

---

## 4. Compatibility Strategy

### Adding new schema versions

1. Add a new row to `ref.FormDefaultsSchemaVersion`:
   - `SchemaVersion` = next INT (e.g. 2)
   - `SchemaVersionString` = `"2.0"` (for API)
   - `SchemaDocument` = JSON Schema for v2.0
   - `IsActive` = 1

2. Backend validation:
   - Current: Pydantic model validates `schemaVersion "1.0"` only.
   - Future: Support multiple schema versions; route validation by `schemaVersion`.

3. Migration of existing forms:
   - Forms with `schemaVersion "1.0"` remain valid.
   - New forms may use `"2.0"` when deployed.
   - Resolver/migration logic converts old → new when needed (future story).

### Backward compatibility (v1.0 → v1.1 hypothetical)

- **Additive changes:** New optional fields do not break v1.0 clients.
- **Breaking changes:** New required fields or structural changes require new major version (e.g. `"2.0"`).
- **Deprecation:** Document deprecated fields in schema description; remove in next major.

---

## 5. SchemaDocument in Database

- **Table:** `ref.FormDefaultsSchemaVersion`
- **Column:** `SchemaDocument` (NVARCHAR(MAX))
- **Content:** JSON Schema (draft-07 or compatible) describing DefinitionJSON structure.
- **Source:** Generated from Pydantic model (`model.model_json_schema()`) or hand-crafted.
- **Usage:** `GET /api/form-schema/1.0` returns this JSON; Form Builder or other clients can fetch at init.

---

## 6. API Version Mapping

| Request | Resolved |
|---------|----------|
| `GET /api/form-schema/1.0` | SchemaDocument for SchemaVersionString = "1.0" |
| `GET /api/form-schema/1` | Same as "1.0" (convenience) |
| `GET /api/form-schema/99` | 404 Not Found |

---

*Story 5.3 - Schema Versioning Documentation*  
*Last Updated: 2026-02-16*
