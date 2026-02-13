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

- **Company-level defaults persistence**
  - Store company form defaults (fonts, colors, typography, spacing) in a new entity or config structure.
  - Dashboard UI: Company Settings → "Form Branding Defaults" (or equivalent).
- **Inheritance model**
  - Company defaults → form overrides → component overrides.
  - Document the inheritance rules; builder and renderer must resolve consistently.
- **Builder UX**
  - Builder surfaces "inherited vs overridden" for defaults.
  - Show inherited values (read-only) with "Override" action.
  - Link: "Edit company defaults" (opens dashboard settings).
- **Resolver integration**
  - Shared resolver (or equivalent) applies company defaults when form lacks explicit overrides.
  - Preview + public renderer use same resolution rules.

### Out of scope (Story 5.2)

- Preview vs production mode toggle (Story 5.5).
- Publish request workflow (Story 5.6+).
- Schema/validation alignment (Story 5.3).
- Per-component override UI beyond "inherited vs overridden" indication.

---

## 🎯 Done Criteria

- [ ] **DC1:** Company defaults are persisted (DB or config-backed).
- [ ] **DC2:** Dashboard has a UI to manage company form branding defaults.
- [ ] **DC3:** Builder inherits company defaults and shows "inherited vs overridden".
- [ ] **DC4:** Inheritance model is documented and consistently applied (builder + renderer).
- [ ] **DC5:** UAT guide executed and marked PASSED.
- [ ] **DC6:** Story PR merged to `master`.

---

## 📚 References

- Epic scope: `docs/stories/EPIC-5-STATUS.md`
- UX ideation: `docs/stories/EPIC-5-UX-IDEATION.md` (Company-level brand defaults, Screen 4)
- Story 5.1 assets: `docs/tasks/5.1/TASK-PLAN.md`
- Workflow: `docs/stories/EPIC-5-WORKFLOW-GUIDE.md`

---

*Story 5.2 created for Epic 5 Form Builder Readiness*
