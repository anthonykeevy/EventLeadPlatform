# Story 5.2 UAT Test Guide — Company Form Defaults (Brand System)

**Story:** 5.2  
**Epic:** 5 - Form Builder Readiness + Review & Publishing  
**Status:** Skeleton — expand per task UAT results  
**Created:** 2026-02-13  

---

## Scope (UAT Coverage)

Story 5.2 UAT verifies:

1. **DC1:** Company defaults persisted in DB with versioning + audit trail
2. **DC2:** Company Settings → Form Branding Defaults page with Global Properties controls + Toolbox preview
3. **DC3:** Builder inherits company defaults; shows inherited vs overridden; Save to Company Defaults button
4. **DC4:** Inheritance model (Global → Company → Form → Component) applied consistently
5. **DC5:** Audit trail viewable in Company Settings
6. **DC7:** Form Builder receives all data via Form Builder Init API; frontend replaces hardcoded; persists DefinitionJSON on save

---

## Pre-conditions

- Story 5.1 complete (assets, globalStyles)
- Database migrations for T00 executed (defaults + component catalog)
- Backend APIs deployed (T01, T06)
- Dashboard + Builder frontend deployed

---

## UAT Steps (to be refined per task)

| DC | Focus | Key verification |
|----|-------|-------------------|
| DC1 | Persistence | Company defaults CRUD; version history visible |
| DC2 | Dashboard UI | Form Branding Defaults page exists; controls match Global Properties Panel |
| DC3 | Builder UX | Inherited values shown; Override action; Save to Company Defaults button |
| DC4 | Resolver | Preview + renderer use same resolution rules |
| DC5 | Audit trail | Version history in Company Settings |
| DC7 | Init API | POST /api/form-builder/init returns full payload; Builder uses it; DefinitionJSON saved |

---

## Task-specific UAT

- **T00:** Migration runs; seed data present; naming rules validated
- **T01:** Defaults CRUD endpoints work; merge resolver returns correct structure
- **T06:** Init API returns schemaVersion, context, defaults, components, definitionJSON
- **T02:** Form Branding Defaults page renders; controls functional
- **T03:** Builder shows inherited vs overridden; Save to Company Defaults works
- **T04:** Resolver applies in renderer
- **T05:** End-to-end flow; all DCs pass

---

*Refine during task execution. Task UAT results feed into final PASS/FAIL.*
