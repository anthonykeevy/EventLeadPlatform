# Task T08: Integration + UAT

**Story:** 5.2 - Company Form Defaults (Brand System)  
**Task ID:** T08  
**Status:** ⏸️ Ready  
**Dependencies:** T04, T05, T06, T07  
**Estimated Time:** 2–3 hours  

---

## 📋 Task Overview

**Objective:** End-to-end integration verification; execute Story 5.2 UAT guide; resolve any integration issues; ensure all Story 5.2 done criteria pass. **This task is primarily UAT** — the agent must log in, run through all verification steps, and record results.

---

## ✅ Scope (In)

- [ ] Integration: Dashboard ↔ API ↔ Builder ↔ Renderer
- [ ] Execute `docs/stories/STORY-5.2-UAT-TEST-GUIDE.md` and `T08-integration-uat.uat.md`
- [ ] Document UAT results (PASS/FAIL per DC)
- [ ] Fix any critical integration bugs discovered
- [ ] Story branch ready for final PR merge to master

---

## 🚫 Scope (Out)

- ❌ New feature implementation (all in T01–T07)
- ❌ Schema/validation alignment (Story 5.3)

---

## ✅ Acceptance Criteria

### AC1: All DCs verified
- DC1–DC7 verified via UAT
- UAT results documented in `T08-integration-uat.uat-results.md`

### AC2: No critical integration defects
- Form creation flow works
- Company defaults persist and inherit
- Builder shows inherited vs overridden; Save to Company Defaults works
- Renderer uses resolved defaults

### AC3: UAT guide executed
- Each step in UAT checklist executed
- Results recorded in UAT results file

---

## 📚 References

- `docs/stories/STORY-5.2-UAT-TEST-GUIDE.md`
- `docs/stories/story-5.2.md` (Done Criteria)
- `docs/AGENT-LOGGING-GUIDE.md` (diagnostics, form-builder logging)

---

## 🌿 Git

- Branch: `task/5.2/T08-integration-uat`
- PR into: `story/epic5-5.2-company-form-defaults`
