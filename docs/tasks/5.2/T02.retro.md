# T02 Retro: Defaults API — CRUD + Merge Resolver

**Task:** T02  
**Story:** 5.2  
**Date:** 2026-02-14  

---

## What Went Well

- **Models + routers implemented cleanly** — Form defaults models (ref + dbo) added; form_defaults router for global; company routes under /api/companies/{id}/form-defaults per spec.
- **Deep merge logic unit-tested** — 3 tests for `deep_merge` (flat, nested, defaultGridLayouts); all pass.
- **RBAC enforced** — system_admin for global; company_admin + company_access for company endpoints.
- **Version history on every PUT** — GlobalFormDefaultsVersion and CompanyFormDefaultsVersion populated with CreatedBy, CreatedDate.

---

## Test Improvements

- Add integration tests for resolve_merged_defaults with mocked DB (Global + Company rows).
- Add API tests (TestClient) for form-defaults endpoints with mocked auth.

---

## Prevention Actions

- None; no defects found during agent verification.

---

*Ralf-Dev / Ralf-Retro*
