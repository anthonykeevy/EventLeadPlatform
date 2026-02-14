# Task T07: Integration + UAT

**Story:** 5.2 - Company Form Defaults (Brand System)  
**Task ID:** T07  
**Status:** ⏸️ Pending  
**Dependencies:** T04, T05, T06  
**Estimated Time:** 2–3 hours  

---

## 📋 Task Overview

**Objective:** End-to-end integration verification; execute UAT guide; resolve any integration issues; ensure all Story 5.2 done criteria pass.

---

## ✅ Scope (In)

- [ ] Integration: Dashboard ↔ API ↔ Builder ↔ Renderer
- [ ] Execute `docs/stories/STORY-5.2-UAT-TEST-GUIDE.md`
- [ ] Document UAT results (PASS/FAIL per DC)
- [ ] Fix any integration bugs
- [ ] Story branch ready for final PR merge to master

---

## 🚫 Scope (Out)

- ❌ New feature implementation (all in T01–T06)
- ❌ Schema/validation alignment (Story 5.3)

---

## ✅ Acceptance Criteria

### AC1: All DCs verified
- DC1–DC7 verified via UAT
- UAT results documented

### AC2: No critical integration defects
- Form creation flow works
- Company defaults persist and inherit
- Builder shows inherited vs overridden
- Renderer uses resolved defaults

### AC3: UAT guide executed
- Each step in UAT guide executed
- Results recorded in UAT results file

---

## 📚 References

- `docs/stories/STORY-5.2-UAT-TEST-GUIDE.md`
- `docs/stories/story-5.2.md` (Done Criteria)

---

## 🌿 Git

- Branch: `task/5.2/T07-integration-uat`
- PR into: `story/epic5-5.2-company-form-defaults`
