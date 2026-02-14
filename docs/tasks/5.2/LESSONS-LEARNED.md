# Lessons Learned — Story 5.2

This file is updated after each task retro.

---

## Entries

### T01 — Database Form Defaults + Component Catalog (2026-02-14)

**Pattern: MSSQL migrations — use mssql.NVARCHAR**

- **Fixed-length strings:** `mssql.NVARCHAR(length=N)` — produces NVARCHAR(N).
- **MAX-length strings:** `mssql.NVARCHAR(length=None)` — produces NVARCHAR(MAX).
- **Avoid:** `sa.Text()` (→ VARCHAR(MAX)), `sa.NVARCHAR` (may not render same as mssql.NVARCHAR for DDL).
- **Reference:** `backend/migrations/versions/036_kb_knowledge_base.py`, `038_asset_metadata_tables.py`.
- **Source:** T01 retro; VARCHAR columns discovered at UAT; fix applied per existing pattern.

---

### T02 — Defaults API CRUD + Merge Resolver (2026-02-14)

**Pattern: Company-scoped routes under /api/companies/{id}/**

- **Spec alignment:** AC2 required GET/PUT `/api/companies/{id}/form-defaults` and `/history`. These live in the companies router, not a separate form-defaults prefix, to match REST conventions.
- **Global vs company:** Global endpoints in form_defaults router (`/api/form-defaults/global`); company endpoints in companies router (`/api/companies/{id}/form-defaults`).

---

### T04 — Dashboard Form Branding Defaults (2026-02-14)

**Pattern: Standalone dashboard sub-pages**

- **Route structure:** Add routes like `/dashboard/companies/:companyId/form-branding-defaults` without nesting under DashboardLayout; page provides own Back button.
- **API alignment:** T02 company endpoints (`GET/PUT /api/companies/{id}/form-defaults`) were ready; T04 only needed frontend API client + page.
- **Entry point:** CompanyContainer Settings cog (Company Admin only) navigates directly to Form Branding Defaults.

---

### (Previous entries above)
