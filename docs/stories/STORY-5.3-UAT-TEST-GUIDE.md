# Story 5.3 UAT Test Guide — Schema + Validation Alignment

**Story:** 5.3  
**Epic:** 5 - Form Builder Readiness + Review & Publishing  
**Status:** Skeleton — expand per task UAT results  
**Created:** 2026-02-16  

---

## Scope (UAT Coverage)

Story 5.3 UAT verifies:

1. **DC1:** Backend schema validates the full DefinitionJSON structure (theme, globalStyles, canvasSettings, logic, pages with background, device-specific page arrays)
2. **DC2:** Schema versioning documented; `schemaVersion` validated; compatibility/migration strategy exists; schema stored in `ref.FormDefaultsSchemaVersion.SchemaDocument`
3. **DC3:** Compatibility tests prove builder output passes backend validation; regression protection
4. **DC4:** Key invariants enforced: unique component IDs, logic rule integrity (sourceComponentId ≠ targetComponentId)
5. **DC5:** `GET /api/form-schema/{version}` returns DefinitionJSON JSON Schema from DB; Form Builder (or other clients) can fetch schema at init; all schema data managed from database

---

## Pre-conditions

- Stories 5.1 and 5.2 complete (assets, company defaults, Form Builder Init API, `ref.FormDefaultsSchemaVersion`)
- Backend running with schema changes
- Form Builder producing DefinitionJSON (save flow, Init API response)
- Test fixtures or live builder output available for validation

---

## UAT Steps (to be refined per task)

| DC | Focus | Key verification |
|----|-------|-------------------|
| DC1 | Schema coverage | Valid DefinitionJSON with globalStyles, canvasSettings, background, desktopPages passes validation |
| DC1 | Schema coverage | Invalid structure (missing formId, wrong theme shape) is rejected with clear error |
| DC2 | Versioning | schemaVersion "1.0" accepted; unknown versions handled per documented strategy; SchemaDocument populated in DB |
| DC3 | Compatibility | Automated tests: builder output (or representative fixture) validates successfully |
| DC3 | Regression | Changing builder output without schema update fails tests (expected; schema update required) |
| DC4 | Invariants | Duplicate component IDs rejected |
| DC4 | Invariants | Logic rule with sourceComponentId === targetComponentId rejected |
| DC5 | Schema-from-DB API | GET /api/form-schema/1.0 returns JSON Schema from ref.FormDefaultsSchemaVersion.SchemaDocument |
| DC5 | Schema-from-DB API | Response is valid JSON Schema; Form Builder can use for runtime validation or documentation |

---

## Manual UAT Checklist

### Valid builder output passes

- [ ] Export a form from the Form Builder (or use Form Builder Init API response) and submit DefinitionJSON to the backend save/validation endpoint.
- [ ] Confirm no validation errors for a form with: theme, globalStyles, canvasSettings, pages with background (asset ref or color), logic rules.
- [ ] Confirm forms with desktopPages/tabletPages/mobilePages (device-specific layouts) validate when present.

### Invalid structures rejected

- [ ] Missing `formId` → validation error.
- [ ] Duplicate component IDs across pages → validation error.
- [ ] Logic rule where `when.sourceComponentId === then.targetComponentId` → validation error.
- [ ] Invalid `schemaVersion` (if strategy is strict) → handled per documented behavior.

### Compatibility tests

- [ ] Run pytest (or equivalent) for schema/compatibility tests.
- [ ] All compatibility tests pass.
- [ ] A known-good builder output fixture is included and passes.

### Schema-from-DB API (DC5)

- [ ] GET /api/form-schema/1.0 returns 200 with JSON Schema in body.
- [ ] Response content matches `ref.FormDefaultsSchemaVersion.SchemaDocument` for version "1.0" (or mapping).
- [ ] GET /api/form-schema/99 (unknown version) returns 404 or documented error.
- [ ] Form Builder Init flow (or equivalent) can optionally fetch schema; no hardcoded schema in code paths that could read from DB.

---

## Task-specific UAT

- **Schema expansion task:** New Pydantic models for globalStyles, canvasSettings, FormPage.background, device-specific pages; existing endpoints accept full structure.
- **Versioning task:** schemaVersion validated; docs updated with compatibility strategy; SchemaDocument populated (migration or seed).
- **Schema-from-DB task:** GET /api/form-schema/{version} endpoint; reads from ref.FormDefaultsSchemaVersion; returns JSON Schema.
- **Invariants task:** Unique IDs and logic rule checks enforced; tests cover positive and negative cases.
- **Compatibility tests task:** Fixtures from builder output; tests run in CI; regression protection confirmed.

---

## Pass Criteria

- [ ] All DC1–DC5 manual checks pass.
- [ ] Automated compatibility tests pass in CI.
- [ ] No regressions in Form Builder save/load flow (builder can still save and load forms).

---

*Refine during task execution. Task UAT results feed into final PASS/FAIL.*
