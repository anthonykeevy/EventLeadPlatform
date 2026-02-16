# UAT Results: T07 — Builder Defaults on New Form + Save to Company Defaults

**Story:** 5.2 - Company Form Defaults (Brand System)  
**Task:** T07 - Builder Defaults on New Form + Save to Company Defaults  
**Result:** ✅ PASS  
**Tester:** Anthony Keevy  
**Date:** 2026-02-16  

---

## Summary

All acceptance criteria and regression checks passed. Task T07 is complete.

---

## Step Results

### AC1: Company defaults on new form

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1.1 | Create new form via Dashboard/Events | Form Builder opens | ✅ Pass |
| 1.2 | Verify Form Global Settings | Company defaults shown (theme, globalStyles, canvasSettings) — not hardcoded fallbacks | ✅ Pass |
| 1.3 | Verify Init API | POST `/api/form-builder/init` called with companyId, eventId | ✅ Pass |
| 1.4 | Verify formDefinitionFromInit | Merged defaults applied to definition | ✅ Pass |

### AC2: Save to Company Defaults visible

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 2.1 | Log in as Company Admin | — | ✅ Pass |
| 2.2 | Open Form Builder for form with company context | — | ✅ Pass |
| 2.3 | Deselect any component | Click canvas background or Esc | ✅ Pass |
| 2.4 | Verify button visibility | "Save to Company Defaults" visible in Global Styles panel | ✅ Pass |
| 2.5 | Log in as non-admin | Button NOT shown | ✅ Pass |
| 2.6 | formContext/companyId diagnostics | If missing: verify form has companyId in DB | ✅ Pass |

### AC3: Save to Company Defaults works

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 3.1 | Company Admin, form with company context, no component selected | — | ✅ Pass |
| 3.2 | Change theme or globalStyles (e.g. primary color) | — | ✅ Pass |
| 3.3 | Click "Save to Company Defaults" | — | ✅ Pass |
| 3.4 | Verify success feedback | Toast "Form branding defaults saved" | ✅ Pass |
| 3.5 | Company Settings → Form Branding Defaults | Version history updated | ✅ Pass |
| 3.6 | Create new form for same company | Saved defaults applied | ✅ Pass |

### Regression Check

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| R1 | Form with eventId=null | Still loads; formContext from companyId; Init skipped; Save button visible | ✅ Pass |
| R2 | Existing form with versions | Loads correctly | ✅ Pass |
| R3 | Edit company defaults link | Visible when companyId present | ✅ Pass |
| R4 | Builder open | No console errors | ✅ Pass |

---

## Defects

| ID | AC | Description |
|----|-----|-------------|
| — | — | None |

---

## Out of Scope

| Item | Classification |
|------|-----------------|
| Logic rules fix (radio/dropdown value extraction in evaluateRules) | Enhancement — resolved during session; works per spec |

---

## Testing Improvement Notes

- Logic rule behavior (show/hide, require/unrequire) for radio/dropdown was fixed in evaluateRules; regression coverage for logic rules with compound component types recommended in future.

---

*UAT recorded by Ralf-UAT — 2026-02-16*
