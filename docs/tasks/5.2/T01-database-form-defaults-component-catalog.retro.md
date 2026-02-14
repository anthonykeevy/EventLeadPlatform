# Retrospective: T01 — Database Form Defaults + Component Catalog

**Task:** T01 - Database Form Defaults + Component Catalog Schema + Seeds  
**Story:** 5.2 - Company Form Defaults (Brand System)  
**UAT Result:** ✅ PASS  
**Retro Date:** 2026-02-14  

---

## 1. What Went Well

| Area | Evidence |
|------|----------|
| **Scope discipline** | Task stayed DB-only; no API/frontend drift. Forbidden zones respected. |
| **Schema design** | Tables match `STORY-5.2-DATA-SCHEMA.md` and `COMPONENT-CATALOG-SCHEMA-DESIGN.md`. |
| **Seed data** | Global defaults + 14 MVP components seeded; JSON structure validated. |
| **UAT coverage** | Checklist (T01-database-form-defaults-component-catalog.uat.md) mapped 1:1 to ACs; all 6 passed. |
| **Human migration rule** | `.cursorrules` prevented agent from running Alembic; human ran downgrade/upgrade cycle correctly. |

---

## 2. What Went Wrong

| Issue | Evidence | Root Cause |
|-------|----------|------------|
| **VARCHAR vs NVARCHAR** | Initial migration used `sa.Text()` and `sa.NVARCHAR()`; DB produced VARCHAR(MAX) | SQLAlchemy `sa.Text()` maps to VARCHAR(MAX) on MSSQL; `sa.NVARCHAR` may not match `mssql.NVARCHAR` for DDL |
| **Rework cycle** | Downgrade 039 → fix migration → upgrade head required | Migration pattern (mssql.NVARCHAR) not consulted before implementation |

---

## 3. Root Cause Summary

- **Prevention:** Database task spec and/or pre-merge checklist did not require "review existing migrations (036, 038) for MSSQL type patterns."
- **Detection gap:** No automated check for VARCHAR in schema before UAT.

---

## 4. Scope Creep

| Item | Classification |
|------|----------------|
| — | None. UAT results: "Out of Scope: None." |

---

## 5. Test Improvements

| Improvement | Type | Rationale |
|-------------|------|-----------|
| **Migration smoke test** | Integration | After `alembic upgrade head`, assert key tables exist + seed row counts (e.g. FormDefaultsSchemaVersion=1, GlobalFormDefaults=1, FormBuilderComponent≥5). |
| **VARCHAR / NVARCHAR assertion** | Integration | Post-migration, query `INFORMATION_SCHEMA.COLUMNS` for new tables; assert `DATA_TYPE = 'nvarchar'` for all string columns. |

---

## 6. Process Improvements

| For | Improvement |
|-----|-------------|
| **Ralf-Dev / Task Spec** | Add to database-task template: "Review `backend/migrations/versions/036_*.py` and `038_*.py` for MSSQL type usage (mssql.NVARCHAR, mssql.NVARCHAR(length=None) for MAX)." |
| **Pre-merge** | Consider adding a "Database naming check" step: grep for sa.Text/sa.VARCHAR in new migration; flag if not mssql.NVARCHAR. |
| **Ralf-SM** | When decomposing DB tasks, include explicit AC or verification step: "All text columns use NVARCHAR per docs/database-naming-rules.md." |

---

## 7. Prevention Actions

1. **Template update:** Add MSSQL type pattern to DB task checklist.
2. **Agent memory:** Store pattern "MSSQL migrations: use mssql.NVARCHAR(length=N) for fixed-length, mssql.NVARCHAR(length=None) for MAX."
3. **UAT addition:** Optional UAT step 6: Run INFORMATION_SCHEMA query to verify no VARCHAR in new tables.

---

## 8. If We Ran This Again

- Start by opening 036/038 before writing 039.
- Add NVARCHAR verification to UAT checklist up front.
- Create migration smoke test script (or pytest) as part of T01 deliverable.

---

*Retro by Ralf-Retro — Evidence-first, prevention-focused*
