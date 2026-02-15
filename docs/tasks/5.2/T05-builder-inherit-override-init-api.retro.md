# Task Retrospective: T05 Builder Inherit Defaults + Override UX + Init API Integration

**Story:** 5.2 - Company Form Defaults (Brand System)  
**Task:** T05 - Builder Inherit Defaults + Override UX + Init API Integration  
**Final Status:** ✅ Complete (implementation)  
**Date:** 2026-02-15

---

## What Went Well

| What Went Well | Evidence |
|----------------|----------|
| Build passed after type fix | `npm run build` exit 0 |
| Graceful degradation when Init API unavailable | formBuilderInit returns null on 404/5xx; fallback to hardcoded defaults |
| Toolbox filtering by Init components | ComponentSidebar uses initComponents when available |
| Save to Company Defaults + Edit link wired | GlobalStylesPanel, PropertiesPanel |
| Full DefinitionJSON already persisted | saveDraft unchanged; AC5 satisfied by existing flow |

---

## What Went Wrong

| Issue | Root Cause | Evidence |
|-------|------------|----------|
| Type error: GlobalStyles vs Record | putCompanyFormDefaults expects Record<string, unknown> | TS2322 in useBuilderStore saveToCompanyDefaults |
| Full UAT not executable | T02/T03/T04 may not be merged in base branch | Init API 404; form-defaults 404; Form Branding Defaults route may not exist |

---

## Prevention Actions

| Issue | Prevention Action | Owner |
|-------|-------------------|-------|
| API payload type mismatch | Define shared types for form-defaults payload; align GlobalStyles with API schema | ralf-sm |
| Cross-task UAT dependency | Document in task spec: "Full UAT requires T02, T03, T04 merged" | ralf-sm |

---

## If We Ran This Again

1. **Run build early** — Caught GlobalStyles type at build time.
2. **Document fallback behavior** — When Init API unavailable, Builder still works with hardcoded defaults.

---

*Retro completed 2026-02-15*
