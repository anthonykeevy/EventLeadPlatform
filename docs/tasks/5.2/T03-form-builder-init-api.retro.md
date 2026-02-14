# T03 Retro: Form Builder Init API

**Task:** T03 - Form Builder Init API (Single Payload)  
**Date:** 2026-02-14  
**Executor:** Ralf-Dev  

---

## What Went Well

- **Reuse:** T02 `resolve_merged_defaults` used directly; no duplication.
- **Raw SQL for FormBuilderComponent:** No ORM model yet for FormBuilderComponent; `sqlalchemy.text()` with parameterized query worked cleanly.
- **CountryID resolution:** Event.CountryID → Company.CountryID fallback implemented per design.
- **Scope filtering:** Component query (Global ∪ Country ∪ Company) and defaultGridLayoutsByComponent filtering by allowed components implemented as specified.

---

## What Could Be Improved

- **Test isolation:** TestClient with app middleware (anyio) caused ExceptionGroup; deferred automated tests; manual UAT required.
- **FormBuilderComponent model:** Future task could add SQLAlchemy model to avoid raw SQL and improve type safety.

---

## Lessons Captured

See LESSONS-LEARNED.md (T03 entry).

---

*Ralf-Dev*
