# UAT Checklist: T08 — Integration + UAT

**Story:** 5.2 - Company Form Defaults (Brand System)  
**Task:** T08 - Integration + UAT  
**Generated:** 2026-02-16  

---

## 🔑 AGENT UAT PREREQUISITES (Required for automated/human UAT)

**The agent must have this information to complete UAT. Ensure all items are available before starting.**

### 1. Service startup

| Service | Command | URL when ready |
|---------|---------|----------------|
| Backend | `cd backend ; python -m uvicorn main:app --reload` | http://localhost:8000 |
| Frontend | `cd frontend ; npm run dev` | http://localhost:5173 |
| (Optional) All services | `.\scripts\start-services-clean.ps1` | — |

Or use `.\scripts\start-services-clean.ps1` from repo root (starts backend, frontend, mailhog, etc.).

### 2. Test user credentials

| User | Email | Password | Role | Use for |
|------|-------|----------|------|---------|
| **Company Admin** | `user2@test.com` | `JChMom7KYLfL88&!` | company_admin (if configured) | Form Branding Defaults, Save to Company Defaults, Create forms |
| **Alternative** | *(Human provides)* | — | company_admin | If user2 is not company_admin in DB |

**Important:** The "Save to Company Defaults" button and Form Branding Defaults page require **company_admin** role. If `user2@test.com` does not have company_admin for any company, the human must provide alternative credentials or run:

```sql
-- Verify/update user role (run in DB if needed)
SELECT u.UserID, u.Email, ucr.RoleCode
FROM dbo.[User] u
JOIN dbo.UserCompany uc ON uc.UserID = u.UserID
JOIN ref.UserCompanyRole ucr ON ucr.UserCompanyRoleID = uc.UserCompanyRoleID
WHERE u.Email = 'user2@test.com';
```

### 3. Database state

- [ ] Migration 039 (or latest) has been run (Form Defaults tables: GlobalFormDefaults, CompanyFormDefaults, etc.)
- [ ] Seed data present (Global defaults row; optionally Company defaults for test company)
- **User must run migrations themselves** — do not run alembic commands from agent.

### 4. Key URLs

| Page | URL |
|------|-----|
| Login | http://localhost:5173/login |
| Dashboard | http://localhost:5173/dashboard |
| Form Branding Defaults | http://localhost:5173/dashboard/companies/{companyId}/form-branding-defaults |
| Form Builder | http://localhost:5173/builder/{formId} |
| Public form (renderer) | http://localhost:5173/form/{formId} (or equivalent public route) |

### 5. Test data (optional — for reproducible UAT)

- **Company ID:** Use any company where the test user is Company Admin. Dashboard shows company containers; cog icon opens Form Branding Defaults.
- **Form ID:** Create a new form via Dashboard → Events → Add Form, or use existing form. New forms should receive Company Defaults (T07).
- **Event ID:** Required for Init API; forms linked to events have eventId. Forms with eventId=null still show Save button (T07 regression R1).

---

## Pre-conditions

- [ ] Backend server running (port 8000)
- [ ] Frontend running (port 5173)
- [ ] User logged in with **Company Admin** role
- [ ] Migrations run; seed data present
- [ ] User has selected a company (Dashboard shows company containers)

---

## UAT Steps (by Done Criterion)

### DC1: Company defaults persisted in DB

- [ ] Step 1: Dashboard → Company (cog) → Form Branding Defaults
- [ ] Step 2: Change Primary Color, save
- [ ] **Verify:** Success toast / no errors
- [ ] Step 3: Refresh page
- [ ] **Verify:** Saved values persist
- [ ] Step 4: Check version history section
- [ ] **Verify:** Version history shows entry

### DC2: Form Branding Defaults page

- [ ] Step 1: Navigate to Form Branding Defaults (as above)
- [ ] **Verify:** Page title "Form Branding Defaults"
- [ ] **Verify:** Theme, Typography, Canvas Settings sections present
- [ ] **Verify:** Live preview (toolbox components) visible
- [ ] **Verify:** Controls match Global Properties Panel layout

### DC3: Builder inherits; Save to Company Defaults

- [ ] Step 1: Create new form OR open existing form in Builder
- [ ] Step 2: Deselect any component (click canvas background) → Global Styles panel shows
- [ ] **Verify:** "Edit company defaults" link visible when companyId present
- [ ] **Verify:** "Save to Company Defaults" button visible (Company Admin only)
- [ ] Step 3: Change Primary Color in Global Styles
- [ ] Step 4: Click "Save to Company Defaults"
- [ ] **Verify:** Toast "Form branding defaults saved"
- [ ] Step 5: Open Form Branding Defaults page
- [ ] **Verify:** Version history updated with new entry

### DC4: Inheritance model (resolver)

- [ ] Step 1: Open form in Builder with Company defaults set
- [ ] **Verify:** Preview shows company theme/globalStyles (primary color, font)
- [ ] Step 2: Open same form as public/renderer (if route available)
- [ ] **Verify:** Rendered form uses same resolved styles

### DC5: Audit trail viewable

- [ ] Step 1: Form Branding Defaults page
- [ ] **Verify:** Version history section with who, when, what

### DC7: Form Builder Init API

- [ ] Step 1: Create new form → Builder opens
- [ ] Step 2: Open DevTools → Network tab; filter for `form-builder` or `init`
- [ ] **Verify:** POST `/api/form-builder/init` called with companyId, eventId
- [ ] **Verify:** Form Global Settings show company defaults (not hardcoded fallbacks)
- [ ] Step 3: Add component, make change, save form
- [ ] **Verify:** DefinitionJSON persisted (form reloads with changes)

---

## Regression checks

- [ ] R1: Form with eventId=null — Builder loads; Save to Company Defaults visible
- [ ] R2: Non–Company Admin user — Save to Company Defaults button NOT shown
- [ ] R3: Existing form with versions — Loads correctly; no console errors

---

## Defects (record if found)

| ID | DC | Description | Severity |
|----|-----|-------------|----------|
| — | — | — | — |

---

## Results

| DC | Pass/Fail | Notes |
|----|-----------|-------|
| DC1 | | |
| DC2 | | |
| DC3 | | |
| DC4 | | |
| DC5 | | |
| DC7 | | |
| Regression | | |

**Overall: PASS / FAIL**

---

*Record detailed results in T08-integration-uat.uat-results.md*
