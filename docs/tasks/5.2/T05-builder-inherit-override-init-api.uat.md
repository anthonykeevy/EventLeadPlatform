# UAT Checklist: T05 — Builder Inherit Defaults + Override UX + Init API Integration

**Story:** 5.2 - Company Form Defaults (Brand System)  
**Task:** T05 - Builder Inherit Defaults + Override UX + Init API Integration  
**Generated:** 2026-02-15  

---

## Pre-conditions

- [ ] Backend server is running (with T02/T03 APIs when available)
- [ ] Frontend is running
- [ ] User is logged in as Company Admin (for Save to Company Defaults)
- [ ] Form exists with CompanyID and EventID (created in Event context)
- [ ] Migration 039 run (T01 — Form Defaults schema)
- [ ] Company has Form Branding Defaults page (T04) if testing Edit link

---

## Test Steps

### AC1: Init API consumed on new form

- [ ] Step 1: Create a new form (Event → Create Form)
- [ ] Step 2: Open Form Builder for the new form
- [ ] Step 3: Verify Builder loads without error (no Init API → fallback to hardcoded)
- [ ] Step 4: (When T03 deployed) Verify network shows POST `/api/form-builder/init` with companyId, eventId
- [ ] Step 5: Verify defaults and components from API (or hardcoded when API unavailable)

### AC2: Inherited vs overridden visible

- [ ] Step 1: Open Global Properties Panel (deselect any component)
- [ ] Step 2: Verify note "Values can be inherited from company defaults or overridden for this form" when companyId present
- [ ] Step 3: Change a Global Style (e.g. primary color)
- [ ] Step 4: Verify change persists (form-level override)

### AC3: Save to Company Defaults works

- [ ] Step 1: Log in as Company Admin
- [ ] Step 2: Open Builder for a form
- [ ] Step 3: Change Global Styles (e.g. primary color)
- [ ] Step 4: Click "Save to Company Defaults" in Global Properties Panel
- [ ] Step 5: Verify toast "Form branding defaults saved"
- [ ] Step 6: (When T04 deployed) Navigate to Company Settings → Form Branding Defaults and verify values persisted

### AC4: Edit company defaults link

- [ ] Step 1: Open Builder for a form with companyId
- [ ] Step 2: Open Global Properties Panel
- [ ] Step 3: Verify "Edit company defaults" link is visible
- [ ] Step 4: Click link → opens `/dashboard/companies/{id}/form-branding-defaults` in new tab
- [ ] Step 5: (When route exists) Verify Form Branding Defaults page loads

### AC5: DefinitionJSON persisted on save

- [ ] Step 1: Add component(s) to form, change Global Styles
- [ ] Step 2: Click Save (or auto-save)
- [ ] Step 3: Close and reopen Builder
- [ ] Step 4: Verify full definition restored (pages, components, globalStyles, theme)

---

## Regression Check

- [ ] Existing form with versions loads correctly
- [ ] Toolbox shows components (filtered by Init API when available)
- [ ] Save to Company Defaults hidden for non-Company Admin
- [ ] No console errors in browser when opening Builder
- [ ] Form with null eventId still loads (Init API skipped gracefully)

---

## Post-conditions

- [ ] Builder works with or without Init API (graceful degradation)
- [ ] Edit company defaults link and Save button present when companyId available
- [ ] Full DefinitionJSON saved on form save

---

**Instructions for Human Tester:**
1. Execute each step in order
2. Mark ✅ or ❌ for each item
3. Add notes for any failures
4. When complete, run `@ralf-uat *record-uat` with your results
