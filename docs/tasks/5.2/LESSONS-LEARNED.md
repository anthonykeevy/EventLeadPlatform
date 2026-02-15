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

### T03 — Form Builder Init API (2026-02-14)

**Pattern: Raw SQL when ORM model absent**

- **FormBuilderComponent:** Migration 039 creates table but no SQLAlchemy model. Used `sqlalchemy.text()` with parameterized query for component resolution. Consider adding model in future for type safety.
- **CountryID fallback:** Event.CountryID → Company.CountryID when Event.CountryID is null; validate Event belongs to Company before resolution.
- **defaults shape:** API design requires `defaults.defaultGridLayoutsByComponent` at top level; merged from T02 has it inside `globalStyles`. Build response with both; filter by allowed component codes only.

**Retro additions (Ralf-Retro 2026-02-14):**

- **UAT:** Agent UAT got 404 when backend ran from different worktree (e.g. T04). Add "Backend started from worktree with task code" to UAT prerequisites.
- **Testing:** Automated integration tests deferred due to TestClient/anyio; manual UAT required. Future: add integration test for POST /api/form-builder/init.
- **Process:** Smoke-test endpoint from this worktree before marking dev complete.

**Links:**
- UAT: T03-form-builder-init-api.uat-results.md
- Retro: T03-form-builder-init-api.retro.md

---

### T04 — Dashboard Form Branding Defaults (2026-02-14)

**Pattern: Standalone dashboard sub-pages**

- **Route structure:** Add routes like `/dashboard/companies/:companyId/form-branding-defaults` without nesting under DashboardLayout; page provides own Back button.
- **API alignment:** T02 company endpoints (`GET/PUT /api/companies/{id}/form-defaults`) were ready; T04 only needed frontend API client + page.
- **Entry point:** CompanyContainer Settings cog (Company Admin only) navigates directly to Form Branding Defaults.

---

### T04 — Full Retro (2026-02-15)

**Dev Lessons:**
- When implementing audit trails, prefer user-identifiable fields (email) over internal IDs when available.
- Run frontend build before completion to catch unused imports (e.g. PropertySelect) and type errors.

**Testing Lessons:**
- For layout controls (row gap, spacing): add UAT step "verify spacing uniform between object rows" if that's the expected UX.
- UAT automation candidate: persistence check (change → save → navigate → return → verify) could be e2e.

**Process Lessons:**
- AC5 "who, when, what" should specify: who = user email or display name when available; what = change summary or modified fields when available.
- Enhancements discovered during UAT (email vs User ID, change summary, row gap) were correctly classified; none were defects.

**Links:**
- Completion: `T04-dashboard-form-branding-defaults.completion.md`
- UAT: `T04-dashboard-form-branding-defaults.uat-results.md`
- Retro: `T04-dashboard-form-branding-defaults.retro.md`
---

### (Previous entries above)
