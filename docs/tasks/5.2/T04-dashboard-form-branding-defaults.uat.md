# T04 UAT: Dashboard — Form Branding Defaults Page

**Task:** T04 - Dashboard: Form Branding Defaults Page  
**Story:** 5.2 - Company Form Defaults (Brand System)  

---

## Prerequisites

- T02 API working (GET/PUT /api/companies/{id}/form-defaults)
- Frontend running; valid company_admin JWT
- Company exists for tests

---

## UAT Steps

### AC1: Page exists and is reachable

- Entry path: Dashboard → Company container (cog) → Company Settings → Form Branding Defaults
- Page loads without error

### AC2: Controls match Global Properties Panel

- Theme (primaryColor, backgroundColor, fontFamily)
- GlobalStyles (typography, spacing, label/input defaults)
- Canvas settings

### AC3: Toolbox preview visible

- Live preview of toolbox components using current defaults

### AC4: Save persists to company defaults

- PUT succeeds; version history updated

### AC5: Audit trail viewable

- Version history with who, when, what

---

*Execute steps; record results in T04-dashboard-form-branding-defaults.uat-results.md*
