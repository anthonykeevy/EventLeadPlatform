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

- [ ] **DC1:** Company defaults are persisted in DB with versioning + audit trail.
- [ ] **DC2:** Company Settings (cog entry) includes Form Branding Defaults page with Global Properties controls + Toolbox visual guide.
- [ ] **DC3:** Builder inherits company defaults and shows "inherited vs overridden"; has "Save to Company Defaults" button on Global Properties Panel.
- [ ] **DC4:** Inheritance model (Global → Company → Form → Component) is documented and consistently applied (builder + renderer).
- [ ] **DC5:** Audit trail viewable in Company Settings → Form Branding Defaults.
- [ ] **DC6:** UAT guide executed and marked PASSED.
- [ ] **DC7:** Form Builder receives all component data and defaults via Form Builder Init API; frontend replaces hardcoded values; persists DefinitionJSON on save.
- [ ] **DC8:** Story PR merged to `master`.

---

## 📊 Task Skeleton (Preliminary)

| Task | Title | Status | Depends On | Est. Time | Focus Area |
|------|-------|--------|------------|-----------|------------|
| **T00** | Database: Defaults + Component Catalog | ⏸️ Pending | - | 4-6 hrs | Database |
| **T01** | Company Defaults Model + API | ⏸️ Pending | T00 | 2-3 hrs | Backend |
| **T06** | Form Builder Init API (single payload) | ⏸️ Pending | T00, T01 | 2-3 hrs | Backend |
| **T02** | Dashboard: Form Branding Defaults UI | ⏸️ Pending | T01 | 2-3 hrs | Dashboard |
| **T03** | Builder: Inherit Defaults + Override UX | ⏸️ Pending | T01, T06 | 2-3 hrs | Builder |
| **T04** | Resolver: Apply Defaults in Renderer | ⏸️ Pending | T01, T03 | 1-2 hrs | Rendering |
| **T05** | Integration + UAT | ⏸️ Pending | T02-T06 | 2-3 hrs | Integration |

**Total Estimated Time:** 15–23 hours (2–3 days)

**Rule:** T00 must complete before T01. T00 includes both defaults and component catalog schema + seed data. Backend (T01, T06) built first; test against existing frontend; then replace frontend defaults with APIs.

---

## 🔗 Dependency Graph

```
T00 (Database: defaults + component catalog) — PREREQUISITE
 ├── T01 (Company defaults model + API)
 │    └── T02 (Dashboard UI)
 └── T06 (Form Builder Init API)
      └── T03 (Builder: inherit + override; consume Init API)
           └── T04 (Resolver in renderer)

T05 (Integration + UAT) depends on T02, T03, T04, T06
```

---

## 📚 Reference Documents

- **T00 spec:** `docs/tasks/5.2/T00-database-form-defaults-schema.md`
- **T06 spec:** `docs/tasks/5.2/T06-form-builder-init-api.md`
- **Form Builder Init API:** `docs/stories/STORY-5.2-FORM-BUILDER-INIT-API.md`
- **Component catalog:** `docs/stories/COMPONENT-CATALOG-SCHEMA-DESIGN.md`
- Story: `docs/stories/story-5.2.md`
- **UX Expert consultation:** `docs/stories/STORY-5.2-UX-EXPERT-CONSULTATION.md`
- **Data schema:** `docs/stories/STORY-5.2-DATA-SCHEMA.md`
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
