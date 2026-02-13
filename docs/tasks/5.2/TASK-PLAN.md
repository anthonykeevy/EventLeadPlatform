# Task Plan: Story 5.2 - Company Form Defaults (Brand System)

**Story:** Story 5.2  
**Epic:** Epic 5 - Form Builder Readiness + Review & Publishing  
**Created:** 2026-02-13  
**Decomposition Pattern:** Foundation First + Dashboard Management + Builder Inheritance  
**Status:** ⏳ Ready  

---

## ✅ Git Discipline (Mandatory)

- **Story branch (to create):** `story/epic5-5.2-company-form-defaults`
- **Base branch:** `master` (or `story/epic5-5.1-background-asset-management` if 5.1 not yet merged)
- **Rule:** Do not implement on `master`
- **Rule:** Each task is implemented on `task/5.2/Txx-<slug>` with a PR into the story branch
- **Workflow:** `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`

---

## 📋 Story Done Criteria

Story 5.2 is complete when:

- [ ] **DC1:** Company defaults are persisted (DB or config-backed).
- [ ] **DC2:** Dashboard has a UI to manage company form branding defaults.
- [ ] **DC3:** Builder inherits company defaults and shows "inherited vs overridden".
- [ ] **DC4:** Inheritance model is documented and consistently applied (builder + renderer).
- [ ] **DC5:** UAT guide executed and marked PASSED.
- [ ] **DC6:** Story PR merged to `master`.

---

## 📊 Task Skeleton (Preliminary)

| Task | Title | Status | Depends On | Est. Time | Focus Area |
|------|-------|--------|------------|-----------|------------|
| **T01** | Company Defaults Model + API | ⏸️ Pending | - | 2-3 hrs | Backend |
| **T02** | Dashboard: Form Branding Defaults UI | ⏸️ Pending | T01 | 2-3 hrs | Dashboard |
| **T03** | Builder: Inherit Defaults + Override UX | ⏸️ Pending | T01 | 2-3 hrs | Builder |
| **T04** | Resolver: Apply Defaults in Renderer | ⏸️ Pending | T01, T03 | 1-2 hrs | Rendering |
| **T05** | Integration + UAT | ⏸️ Pending | T02-T04 | 2-3 hrs | Integration |

**Total Estimated Time:** 9–14 hours (2–3 days)

---

## 🔗 Dependency Graph

```
T01 (Company defaults model + API)
 ├── T02 (Dashboard UI)
 ├── T03 (Builder inherit + override UX)
 └── T04 (Resolver in renderer)

T05 (Integration + UAT) depends on T02–T04
```

---

## 📚 Reference Documents

- Story: `docs/stories/story-5.2.md`
- Epic scope: `docs/stories/EPIC-5-STATUS.md`
- UX ideation: `docs/stories/EPIC-5-UX-IDEATION.md`
- Workflow: `docs/stories/EPIC-5-WORKFLOW-GUIDE.md`
- Story 5.1: `docs/tasks/5.1/` (assets, globalStyles shape)

---

## 📝 Status Legend

- ⏳ **Ready** - Can start now (dependencies met)
- 🔄 **In Progress** - Currently being worked on
- ✅ **HumanDone** - Completed with required human execution and recorded UAT
- ⏸️ **Pending** - Waiting on dependencies

---

*Task Plan created for Story 5.2 kickoff*
