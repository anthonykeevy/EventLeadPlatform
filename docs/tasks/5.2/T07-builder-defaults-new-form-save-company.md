# Task T07: Builder — Defaults on New Form + Save to Company Defaults UX

**Story:** 5.2 - Company Form Defaults (Brand System)  
**Task ID:** T07  
**Status:** In Progress  
**Dependencies:** T05  
**Estimated Time:** 1–2 hours  

---

## 📋 Task Overview

**Objective:** Ensure (1) Company Defaults are applied to Form Global Settings when creating a new form, and (2) the "Save to Company Defaults" button is visible and functional for Company Admins in the Global Properties Panel.

---

## ✅ Scope (In)

- [ ] New form creation: Company Defaults (from Init API) populate form's theme, globalStyles, canvasSettings in Form Global Settings
- [ ] Init API called reliably when entering builder for a new form (formContext/companyId set)
- [ ] "Save to Company Defaults" button visible in Global Properties Panel when: Company Admin, form has company context, no component selected
- [ ] Button saves current form's form-level overrides (theme, globalStyles) to company defaults
- [ ] Fix any gaps: formContext availability, role check, create-flow handoff to builder with companyId/eventId

---

## 🚫 Scope (Out)

- ❌ Company Form Branding Defaults page (T04)
- ❌ Resolver in renderer (T06)
- ❌ Per-component override UI

---

## ✅ Acceptance Criteria

### AC1: Company defaults on new form
- Create new form via Dashboard/Events → Form Builder opens
- Form Global Settings show company defaults (theme, globalStyles, canvasSettings) — not hardcoded fallbacks
- Init API called with companyId, eventId; formDefinitionFromInit applies merged defaults to definition

### AC2: Save to Company Defaults visible
- Company Admin: Button visible in Global Styles panel when no component selected and formContext.companyId present
- Non-admin: Button not shown
- If formContext/companyId missing: diagnose and fix so button appears when context available

### AC3: Save to Company Defaults works
- Click button → PUT company defaults with current form's theme, globalStyles
- Success toast; version history updated in Company Form Branding Defaults page

---

## 📚 References

- `docs/stories/story-5.2.md` (DC3, Builder UX)
- `docs/stories/STORY-5.2-FORM-BUILDER-INIT-API.md`
- `frontend/src/features/builder/components/properties/GlobalStylesPanel.tsx`
- `frontend/src/features/builder/stores/useBuilderStore.ts` (formDefinitionFromInit, initializeForm, formContext)

---

## 🌿 Git

- Branch: `task/5.2/T07-builder-defaults-new-form-save-company`
- PR into: `story/epic5-5.2-company-form-defaults`
