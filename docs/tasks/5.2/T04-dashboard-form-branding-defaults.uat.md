# UAT Checklist: T04 — Form Branding Defaults Page

**Story:** 5.2 - Company Form Defaults (Brand System)  
**Task:** T04 - Dashboard Form Branding Defaults  
**Generated:** 2026-02-14  

---

## Pre-conditions

- [ ] Backend server is running (`cd backend && python main.py`)
- [ ] Frontend is running (`cd frontend && npm run dev`)
- [ ] User is logged in with **Company Admin** role for at least one company
- [ ] Migration 039 has been run (Form Defaults tables + seed)
- [ ] User has switched to/selected a company (Dashboard shows company containers)

---

## Test Steps

### AC1: Page exists and is reachable

- [ ] Step 1: Go to Dashboard
- [ ] Step 2: Find a company container where you are **Company Admin**
- [ ] Step 3: Click the **Settings (cog)** icon on the company header
- [ ] **Verify:** Navigates to Form Branding Defaults page
- [ ] **Verify:** Page title shows "Form Branding Defaults"
- [ ] **Verify:** URL is `/dashboard/companies/{companyId}/form-branding-defaults`

### AC2: Controls match Global Properties Panel

- [ ] Step 1: On Form Branding Defaults page, locate **Theme** section
- [ ] **Verify:** Primary Color (color picker + text input), Background Color, Font Family
- [ ] Step 2: Locate **Typography** section
- [ ] **Verify:** Base Font Family, Base Font Size, Label Font Family, Label Color, Input Text Color
- [ ] Step 3: Locate **Canvas Settings** section
- [ ] **Verify:** Width, Height, Grid Size inputs

### AC3: Toolbox preview visible

- [ ] Step 1: On Form Branding Defaults page, locate **Component Preview** section (right column)
- [ ] **Verify:** Live preview area shows styled inputs (e.g. "Full Name", "Email")
- [ ] Step 2: Change Primary Color in Theme section
- [ ] **Verify:** "Submit (primary color)" button updates immediately with new color
- [ ] Step 3: Change Font Family
- [ ] **Verify:** Preview area reflects new font

### AC4: Save persists to company defaults

- [ ] Step 1: Change Primary Color (e.g. to `#FF5500`)
- [ ] Step 2: Click **Save**
- [ ] **Verify:** Toast shows "Form branding defaults saved"
- [ ] Step 3: Click **Show History**
- [ ] **Verify:** New version appears in Change History
- [ ] Step 4: Navigate away (Back to Dashboard) then return via Settings cog
- [ ] **Verify:** Primary Color remains changed (`#FF5500`)

### AC5: Audit trail viewable

- [ ] Step 1: Click **Show History**
- [ ] **Verify:** Change History section appears
- [ ] **Verify:** Entries show Version number, change summary (if any), date, User ID
- [ ] **Verify:** After a save, latest version appears at top

---

## Regression Check

- [ ] Dashboard still loads and shows company list
- [ ] Company selection and expand still works
- [ ] Team Management panel still opens from Users icon
- [ ] No console errors in browser when navigating to Form Branding Defaults
- [ ] Back button returns to Dashboard correctly

---

## Access Control (Company Admin only)

- [ ] Step 1: Log in as **Company User** or **Company Viewer**
- [ ] Step 2: Check company container
- [ ] **Verify:** Settings (cog) icon is **not** visible
- [ ] Step 3: If user has Company Admin for Company A but not Company B: cog visible only for Company A

---

## Post-conditions

- [ ] Form Branding Defaults page functional for Company Admins
- [ ] Data persists via PUT to `/api/companies/{id}/form-defaults`
- [ ] Version history stored and retrievable

---

**Instructions for Human Tester:**
1. Execute each step in order
2. Mark ✅ or ❌ for each item
3. Add notes for any failures
4. When complete, create `T04-dashboard-form-branding-defaults.uat-results.md` with results
