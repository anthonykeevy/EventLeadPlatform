# Task T06: Resolver — Apply Defaults in Renderer

**Story:** 5.2 - Company Form Defaults (Brand System)  
**Task ID:** T06  
**Status:** ✅ HumanDone (PR #38 merged 2026-02-15)  
**Dependencies:** T02, T05  
**Estimated Time:** 1–2 hours  

---

## 📋 Task Overview

**Objective:** Shared resolver applies defaults (Global → Company → Form → Component) in preview and public renderer. Preview and production use same resolution rules.

---

## ✅ Scope (In)

- [x] Resolver logic: merge Global + Company + Form overrides for a given form
- [x] Preview mode: use resolver when rendering
- [x] Public renderer: use resolver when rendering
- [x] Inheritance model documented (builder + renderer alignment)
- [x] Consistency: same resolution rules in Builder preview and public runtime

---

## 🚫 Scope (Out)

- ❌ Preview vs production mode toggle (Story 5.5)
- ❌ Form Builder Init API (T03)

---

## ✅ Acceptance Criteria

### AC1: Resolver applies inheritance
- Global → Company → Form → Component resolution order
- Form overrides from DefinitionJSON override company defaults

### AC2: Preview uses resolver
- Builder preview renders with resolved defaults
- Matches public renderer behavior

### AC3: Public renderer uses resolver
- Production/public form render uses same resolution
- No hardcoded fallbacks that bypass resolver

### AC4: Inheritance documented
- Resolution rules documented and aligned with `docs/stories/STORY-5.2-DATA-SCHEMA.md`

---

## 📚 References

- `docs/stories/STORY-5.2-DATA-SCHEMA.md`
- `docs/COMPONENT-FRAMEWORK-REFERENCE.md`

---

## 🌿 Git

- Branch: `task/5.2/T06-resolver-apply-defaults-renderer`
- PR into: `story/epic5-5.2-company-form-defaults`
