# Task T05: Builder — Inherit Defaults + Override UX + Init API Integration

**Story:** 5.2 - Company Form Defaults (Brand System)  
**Task ID:** T05  
**Status:** ✅ HumanDone (PR #37 merged 2026-02-15)  
**Dependencies:** T02, T03  
**Estimated Time:** 3–4 hours  

---

## 📋 Task Overview

**Objective:** Form Builder inherits company defaults; surfaces "inherited vs overridden"; provides "Save to Company Defaults" button; consumes Form Builder Init API instead of hardcoded values; persists complete DefinitionJSON on save.

---

## ✅ Scope (In)

- [x] Call `POST /api/form-builder/init` when starting new form (companyId, eventId from form context)
- [x] Replace hardcoded defaults and component catalog with API response
- [x] Global Properties Panel: show inherited values (read-only) with "Override" action
- [x] Link: "Edit company defaults" → opens Company Settings (Dashboard)
- [x] "Save to Company Defaults" button on Global Properties Panel (Company Admin only)
- [x] Save full DefinitionJSON to FormVersion on form save
- [x] Toolbox populated from Init API `components` array

---

## 🚫 Scope (Out)

- ❌ Per-component override UI beyond inherited vs overridden (out of scope)
- ❌ Resolver in renderer (T06)

---

## ✅ Acceptance Criteria

### AC1: Init API consumed on new form
- Builder calls Init API with companyId, eventId when starting new form
- Defaults and components from API, not hardcoded

### AC2: Inherited vs overridden visible
- Global Properties Panel shows inherited values (read-only)
- "Override" action allows form-level override
- Clear indication of source (company vs form)

### AC3: Save to Company Defaults works
- Button visible to Company Admin
- Saves current form's form overrides to company defaults
- Version history updated

### AC4: Edit company defaults link
- Link opens Company Settings → Form Branding Defaults

### AC5: DefinitionJSON persisted on save
- Full DefinitionJSON written to FormVersion on form save

---

## 📚 References

- `docs/stories/STORY-5.2-FORM-BUILDER-INIT-API.md`
- `docs/stories/STORY-5.2-UX-EXPERT-CONSULTATION.md`
- `docs/COMPONENT-FRAMEWORK-REFERENCE.md`

---

## 🌿 Git

- Branch: `task/5.2/T05-builder-inherit-override-init-api`
- PR into: `story/epic5-5.2-company-form-defaults`
