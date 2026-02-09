# Task Plan: Story 5.1 - Background Asset Management

**Story:** Story 5.1  
**Epic:** Epic 5 - Form Builder Readiness + Review & Publishing  
**Created:** 2026-02-09  
**Decomposition Pattern:** Foundation First + Storage Abstraction + Parity  
**Status:** ⏳ In Progress  

---

## ✅ Git Discipline (Mandatory)

- **Active story branch (confirmed):** `story/epic5-5.1-background-asset-management` (pushed to `origin`)
- **Rule:** Do not implement on `master`
- **Rule:** Each task is implemented on `task/5.1/Txx-<slug>` with a PR into the story branch
- **Workflow:** `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`

---

## 📋 Story Done Criteria

Story 5.1 is complete when:

- [ ] **DC1:** Backgrounds stored as asset references (no Data URLs in DefinitionJSON).
- [ ] **DC2:** Builder + renderer resolve assets consistently.
- [ ] **DC3:** Upload/runtime limits enforced via `config.AppSetting`.
- [ ] **DC4:** `docs/stories/STORY-5.1-UAT-TEST-GUIDE.md` executed and marked ✅ PASSED.
- [ ] **DC5:** Story PR merged to `master`.

---

## 📊 Task Skeleton

| Task | Title | Status | Depends On | Est. Time | Focus Area |
|------|-------|--------|------------|-----------|------------|
| **T01** | Asset Contracts + Config Foundations | ✅ HumanDone | - | 2-3 hrs | Foundation |
| **T02** | DB Migration: Asset Metadata Tables | ✅ HumanDone | T01 | 1-2 hrs | Database |
| **T03** | Backend: Asset Service + Upload API | ✅ HumanDone | T02 | 2-3 hrs | Backend/API |
| **T04** | Frontend: Builder Asset Upload + Library + Ref | ⏸️ Pending | T01, T03 | 3-5 hrs | Frontend/Builder |
| **T05** | Shared Resolver Parity (Builder + Renderer) | ⏸️ Pending | T03, T04 | 2-3 hrs | Rendering |
| **T06** | Placement + Intersection Rule + Cropping | ⏸️ Pending | T04, T05 | 2-3 hrs | UX/Canvas |
| **T07** | Data URL Guard + Regression Cleanup | ⏸️ Pending | T04 | 1-2 hrs | Safety |
| **T08** | Integration + UAT Polish | ⏸️ Pending | T03-T07 | 2-3 hrs | Integration |

**Total Estimated Time:** 15–24 hours (4–6 days)

---

## 🔗 Dependency Graph

```
T01 (Contracts + config foundations)
 └── T02 (DB migration: asset metadata)
      └── T03 (Backend asset service + API)
           ├── T04 (Builder asset upload + library + refs)
           │    └── T06 (Placement + intersection rule + cropping)
           ├── T05 (Shared resolver parity)
           └── T07 (Data URL guard + cleanup)

T08 (Integration + UAT) depends on T03–T07
```

---

## 📁 Task Files

| Task | Task Spec | Status |
|------|-----------|--------|
| T01 | `T01-asset-contracts-and-config-foundations.md` | ✅ HumanDone |
| T02 | `T02-db-migration-asset-metadata.md` | ✅ HumanDone |
| T03 | `T03-backend-asset-service-and-upload-api.md` | ✅ HumanDone |
| T04 | `T04-frontend-builder-asset-upload-and-library.md` | ⏸️ Pending |
| T05 | `T05-shared-resolver-parity.md` | ⏸️ Pending |
| T06 | `T06-placement-intersection-and-cropping.md` | ⏸️ Pending |
| T07 | `T07-data-url-guard-and-cleanup.md` | ⏸️ Pending |
| T08 | `T08-integration-and-uat-polish.md` | ⏸️ Pending |

---

## 🎯 Decomposition Rationale

**Why this split works for Story 5.1:**
- The story crosses frontend + backend + storage; we **lock contracts and config first** (T01).
- DB changes are isolated (T02) so migration risk is explicit and human-run.
- Backend service and API must exist before the builder can bind to asset references (T03 → T04).
- Resolver parity is isolated to avoid drift between builder/renderer (T05).
- Placement + intersection rules are separate to minimize UI churn (T06).
- Data URL guard is isolated for regression safety (T07).
- T08 is an explicit integration/UAT checkpoint for end-to-end validation.

---

## 📚 Reference Documents

- Story: `docs/stories/story-5.1.md`
- Context: `docs/stories/story-context-5.1.xml`
- UAT Guide: `docs/stories/STORY-5.1-UAT-TEST-GUIDE.md`
- Epic scope: `docs/stories/EPIC-5-STATUS.md`
- Workflow: `docs/stories/EPIC-5-WORKFLOW-GUIDE.md`
- Git workflow: `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`
- DB standards: `docs/database-naming-rules.md`

---

## ⚠️ Global Forbidden Zones

These areas are off-limits unless a task explicitly says otherwise:

| Zone | Reason |
|------|--------|
| `frontend/src/features/auth/` | No auth changes for asset work |
| `backend/modules/auth/` | Out of scope |
| `docs/tasks/3.*` | Completed Epic 3 artifacts; avoid edits |

---

## 📝 Status Legend

- ⏳ **Ready** - Can start now (dependencies met)
- 🔄 **In Progress** - Currently being worked on
- ✅ **Done** - Completed and merged into story branch
- ✅ **HumanDone** - Completed with required human execution (e.g., DB migrations) and recorded UAT
- ❌ **FailedUAT** - UAT failed, needs fix task
- ⏸️ **Pending** - Waiting on dependencies

---

*Task Plan created using Epic 5 workflow guide*  
