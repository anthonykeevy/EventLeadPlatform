# Task Plan: Story 5.2 - Company Form Defaults (Brand System)

**Story:** 5.2  
**Epic:** Epic 5 - Form Builder Readiness + Review & Publishing  
**Created:** 2026-02-13 (Ralf-SM decomposition)  
**Decomposition Pattern:** Foundation First — Database → Backend APIs → Dashboard → Builder → Renderer → Integration  
**Status:** ⏳ Ready  

---

## ✅ Git Discipline (Mandatory)

- **Story branch:** `story/epic5-5.2-company-form-defaults` (exists, pushed)
- **Rule:** Do not work on `master`
- **Rule:** Each task on `task/5.2/Txx-<slug>` with PR into story branch
- **Workflow:** `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`

---

## 📋 Story Done Criteria (Mapping)

| DC | Criterion | Tasks |
|----|-----------|-------|
| DC1 | Company defaults persisted in DB with versioning + audit trail | T01, T02 |
| DC2 | Company Settings Form Branding Defaults page | T04 |
| DC3 | Builder inherits, inherited vs overridden, Save to Company Defaults | T05 |
| DC4 | Inheritance model documented and applied (builder + renderer) | T02, T05, T06 |
| DC5 | Audit trail viewable | T02, T04 |
| DC6 | UAT guide executed and marked PASSED | T07 |
| DC7 | Form Builder Init API; frontend replaces hardcoded; persists DefinitionJSON | T03, T05 |
| DC8 | Story PR merged to master | — |

---

## 📊 Task Decomposition

| Task | Title | Status | Depends On | Est. Time | Focus Area |
|------|-------|--------|------------|-----------|------------|
| **T01** | Database: Form Defaults + Component Catalog Schema + Seeds | ✅ HumanDone | — | 4–6 hrs | Database |
| **T02** | Defaults API: CRUD + Merge Resolver | ✅ HumanDone | T01 | 2–3 hrs | Backend |
| **T03** | Form Builder Init API (single payload) | ✅ HumanDone | T01, T02 | 2–3 hrs | Backend |
| **T04** | Dashboard: Form Branding Defaults Page | ✅ HumanDone | T02 | 2–3 hrs | Dashboard |
| **T05** | Builder: Inherit Defaults + Override UX + Init API Integration | ✅ HumanDone | T02, T03 | 3–4 hrs | Builder |
| **T06** | Resolver: Apply Defaults in Renderer | ⏸️ Pending | T02, T05 | 1–2 hrs | Rendering |
| **T07** | Integration + UAT | ⏸️ Pending | T04, T05, T06 | 2–3 hrs | Integration |

**Total Estimated Time:** 16–24 hours (2–3 days)

---

## 🔗 Dependency Graph

```
T01 (Database: defaults + component catalog) — PREREQUISITE
 ├── T02 (Defaults API + merge resolver)
 │    ├── T03 (Form Builder Init API)
 │    ├── T04 (Dashboard Form Branding Defaults)
 │    └── T06 (Resolver in renderer)
 └── T03 (also needs T02 for merge logic)
      └── T05 (Builder: inherit + override + consume Init API)
           └── T06 (resolver needs Builder context)

T07 (Integration + UAT) depends on T04, T05, T06
```

---

## 📚 Reference Documents

- Story: `docs/stories/story-5.2.md`
- Context: `docs/stories/story-context-5.2.xml`
- Data schema: `docs/stories/STORY-5.2-DATA-SCHEMA.md`
- Component catalog: `docs/stories/COMPONENT-CATALOG-SCHEMA-DESIGN.md`
- Form Builder Init API: `docs/stories/STORY-5.2-FORM-BUILDER-INIT-API.md`
- UX Expert consultation: `docs/stories/STORY-5.2-UX-EXPERT-CONSULTATION.md`
- Database naming: `docs/database-naming-rules.md`
- Epic scope: `docs/stories/EPIC-5-STATUS.md`

---

## 📝 Status Legend

- ⏳ **Ready** — Can start (dependencies met)
- 🔄 **In Progress** — Being worked on
- ✅ **HumanDone** — UAT passed, PR merged
- ⏸️ **Pending** — Waiting on dependencies

---

*Decomposition by Ralf-SM — Database first, then backend, then frontend*
