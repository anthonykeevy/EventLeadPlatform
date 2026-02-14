# Task T02: Defaults API — CRUD + Merge Resolver

**Story:** 5.2 - Company Form Defaults (Brand System)  
**Task ID:** T02  
**Status:** ⏸️ Pending  
**Dependencies:** T01  
**Estimated Time:** 2–3 hours  

---

## 📋 Task Overview

**Objective:** Implement backend API for Global and Company Form Defaults: CRUD endpoints plus a merge resolver that applies Global + Company defaults for a given CompanyID.

---

## ✅ Scope (In)

- [ ] Models: GlobalFormDefaults, CompanyFormDefaults (and Version tables)
- [ ] CRUD: GET/PUT global defaults (admin); GET/PUT company defaults (company admin)
- [ ] Version history endpoints (audit trail)
- [ ] Merge resolver: given CompanyID, return Global deep-merged with Company overrides
- [ ] RBAC: company-scoped access; global admin for global defaults

---

## 🚫 Scope (Out)

- ❌ Form Builder Init API (T03)
- ❌ Dashboard UI (T04)
- ❌ Component catalog query (T03)

---

## ✅ Acceptance Criteria

### AC1: Global defaults API exists
- GET `/api/form-defaults/global` — current global defaults
- PUT `/api/form-defaults/global` — update (admin only)
- GET `/api/form-defaults/global/history` — version history

### AC2: Company defaults API exists
- GET `/api/companies/{id}/form-defaults` — merged defaults (Global + Company)
- PUT `/api/companies/{id}/form-defaults` — update company defaults
- GET `/api/companies/{id}/form-defaults/history` — audit trail

### AC3: Merge resolver produces correct structure
- Deep merge: Company overrides Global
- Response includes theme, globalStyles, canvasSettings, defaultGridLayoutsByComponent

### AC4: Version tables populated on update
- Every PUT inserts into Version table with CreatedBy, CreatedDate

---

## 📚 References

- `docs/stories/STORY-5.2-DATA-SCHEMA.md`
- `docs/stories/STORY-5.2-FORM-BUILDER-INIT-API.md`

---

## 🌿 Git

- Branch: `task/5.2/T02-defaults-api-crud-merge-resolver`
- PR into: `story/epic5-5.2-company-form-defaults`
