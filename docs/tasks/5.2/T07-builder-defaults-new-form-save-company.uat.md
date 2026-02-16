# UAT Checklist: T07 — Builder Defaults on New Form + Save to Company Defaults

**Story:** 5.2 - Company Form Defaults (Brand System)  
**Task:** T07 - Builder Defaults on New Form + Save to Company Defaults  
**Generated:** 2026-02-16  

---

## Pre-conditions

- [ ] Backend server running (Init API + form-defaults)
- [ ] Frontend running
- [ ] User logged in as Company Admin (for Save to Company Defaults)
- [ ] Migration 039 run (Form Defaults schema)
- [ ] Company has Form Branding Defaults page (T04)

---

## Test Steps

### AC1: Company defaults on new form

- [ ] Step 1: Create new form via Dashboard/Events → Form Builder opens
- [ ] Step 2: Verify Form Global Settings show company defaults (theme, globalStyles, canvasSettings) — not hardcoded fallbacks
- [ ] Step 3: Verify Init API called with companyId, eventId (Network tab: POST `/api/form-builder/init`)
- [ ] Step 4: Verify formDefinitionFromInit applies merged defaults to definition

### AC2: Save to Company Defaults visible

- [ ] Step 1: Log in as Company Admin
- [ ] Step 2: Open Form Builder for a form with company context
- [ ] Step 3: Deselect any component (click canvas background or Esc)
- [ ] Step 4: Verify "Save to Company Defaults" button visible in Global Styles panel
- [ ] Step 5: Log in as non-admin (Company User) — verify button NOT shown
- [ ] Step 6: If formContext/companyId missing: verify diagnostics (check form has companyId in DB)

### AC3: Save to Company Defaults works

- [ ] Step 1: Company Admin, form with company context, no component selected
- [ ] Step 2: Change theme or globalStyles (e.g. primary color)
- [ ] Step 3: Click "Save to Company Defaults" button
- [ ] Step 4: Verify success toast "Form branding defaults saved"
- [ ] Step 5: Navigate to Company Settings → Form Branding Defaults — verify version history updated
- [ ] Step 6: Create new form for same company — verify saved defaults applied

---

## Regression Check

- [ ] Form with eventId=null still loads (formContext set from companyId; Init skipped; Save button visible)
- [ ] Existing form with versions loads correctly
- [ ] Edit company defaults link visible when companyId present
- [ ] No console errors when opening Builder

---

## Post-conditions

- [ ] Company defaults apply to new form Global Settings
- [ ] Save to Company Defaults button visible and functional for Company Admins
- [ ] formContext available when companyId present (even if eventId null)

---

**Instructions for Human Tester:**
1. Execute each step in order
2. Mark ✅ or ❌ for each item
3. Add notes for any failures
4. When complete, run `@ralf-uat *record-uat` with your results
