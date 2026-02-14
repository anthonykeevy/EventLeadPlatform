# Story 5.2: Company Form Defaults (Brand System)

**Epic:** Epic 5 - Form Builder Readiness + Review & Publishing  
**Domain:** Form Builder + Dashboard  
**Status:** ⏳ Ready  
**Priority:** High (foundation for preview/production parity)  
**Created:** 2026-02-13  
**Owner:** Developer Agent  

---

## 📖 User Story

**As a** company admin (or marketer),  
**I want to** set form branding defaults (fonts, colors, typography, spacing) once per company,  
**So that** every new form inherits them automatically and I don't have to configure each form from scratch.

**Context & entry point:**  
- Story 5.1 is complete: Background assets are stored as references; builder has `globalStyles`.  
- Today `globalStyles` lives inside each form definition; there is no company-level persistence.  
- Epic 5 Phase A requires: "Set once, inherit everywhere."

---

## 🧭 Scope Boundary

### In scope (Story 5.2)

- **Inheritance model**
  - **Global Defaults → Company Defaults → Form Overrides → Component Overrides** (four tiers).
  - Document the inheritance rules; builder and renderer must resolve consistently.
- **Company Settings: Form Branding Defaults page**
  - Entry: Dashboard → Company container (cog icon) → Company Settings → "Form Branding Defaults".
  - Page contains: exact controls from Global Properties Panel + Toolbox components as visual guide (live preview).
- **Company-level defaults persistence**
  - Store company form defaults (fonts, colors, typography, spacing, background) in DB with versioning + audit trail.
  - Database stores every data point; versions saved with audit (who, when, what).
- **Builder UX**
  - Builder surfaces "inherited vs overridden" for defaults.
  - Show inherited values (read-only) with "Override" action.
  - Link: "Edit company defaults" (opens Company Settings).
  - **"Save to Company Defaults" button** on Global Properties Panel: saves current form's form overrides to company defaults (Company Admin only).
- **Audit trail**
  - Version history with who changed what and when; viewable in Company Settings → Form Branding Defaults.
- **Resolver integration**
  - Shared resolver applies defaults per inheritance model.
  - Preview + public renderer use same resolution rules.
- **Form Builder data via APIs (end-of-story target)**
  - Form Builder receives **all** component data and defaults via APIs from the database.
  - **Form Builder Init API:** Single payload (`POST /api/form-builder/init` with `companyId`, `eventId`) returns merged defaults + component catalog + initial DefinitionJSON skeleton.
  - Form context: CompanyID + EventID (Event.CountryID) define criteria; API returns correct components (Global ∪ Country ∪ Company).
  - Frontend manages changes and writes complete DefinitionJSON back on save.
- **Component catalog (database-driven)**
  - Components + schemas scoped by Global, Country, or Company; delivered via Form Builder Init response.

### Out of scope (Story 5.2)

- Preview vs production mode toggle (Story 5.5).
- Publish request workflow (Story 5.6+).
- Schema/validation alignment (Story 5.3).
- Per-component override UI beyond "inherited vs overridden" indication.
- **Global Defaults screen** (Administration Settings for Global Form Defaults — Epic 5 backlog).

---

## 🎯 Done Criteria

- [ ] **DC1:** Company defaults are persisted in DB with versioning + audit trail.
- [ ] **DC2:** Company Settings (cog entry) includes Form Branding Defaults page with Global Properties controls + Toolbox visual guide.
- [ ] **DC3:** Builder inherits company defaults and shows "inherited vs overridden"; has "Save to Company Defaults" button on Global Properties Panel.
- [ ] **DC4:** Inheritance model (Global → Company → Form → Component) is documented and consistently applied (builder + renderer).
- [ ] **DC5:** Audit trail viewable in Company Settings → Form Branding Defaults.
- [ ] **DC6:** UAT guide executed and marked PASSED.
- [ ] **DC7:** Form Builder receives all component data and defaults via Form Builder Init API; frontend replaces hardcoded values; persists DefinitionJSON on save.
- [ ] **DC8:** Story PR merged to `master`.

---

## 📚 References

- Epic scope: `docs/stories/EPIC-5-STATUS.md`
- **Form Builder Init API:** `docs/stories/STORY-5.2-FORM-BUILDER-INIT-API.md`
- UX ideation: `docs/stories/EPIC-5-UX-IDEATION.md` (Company-level brand defaults, Screen 4)
- **UX Expert consultation:** `docs/stories/STORY-5.2-UX-EXPERT-CONSULTATION.md`
- **Data schema:** `docs/stories/STORY-5.2-DATA-SCHEMA.md`
- **Component catalog:** `docs/stories/COMPONENT-CATALOG-SCHEMA-DESIGN.md`
- Story 5.1 assets: `docs/tasks/5.1/TASK-PLAN.md`
- Workflow: `docs/stories/EPIC-5-WORKFLOW-GUIDE.md`

---

*Story 5.2 created for Epic 5 Form Builder Readiness*
