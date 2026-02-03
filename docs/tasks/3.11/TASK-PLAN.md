# Task Plan: Story 3.11 - Dynamic Submission (Outbox)

**Story:** Story 3.11  
**Epic:** Epic 3 - Form Builder & Logic Engine  
**Created:** 2026-02-03  
**Decomposition Pattern:** Foundation First + Migration Safety + API-First  
**Status:** ⏳ Planned  

---

## ✅ Git Discipline (Mandatory)

- **Active story branch (confirmed):** `story/epic3-3.11-dynamic-submission` (pushed to `origin`)
- **Rule:** Do not implement on `master`
- **Rule:** Each task is implemented on `task/3.11/Txx-<slug>` with a PR into the story branch
- **Workflow:** `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`

---

## 📋 Story Done Criteria

Story 3.11 is complete when:

- [ ] **DC1:** All Story acceptance criteria pass (online submit, offline queue, auto-sync, idempotency, token behavior, shared-device safety, validation telemetry).
- [ ] **DC2:** `docs/stories/STORY-3.11-UAT-TEST-GUIDE.md` is executed and marked ✅ PASSED.
- [ ] **DC3:** Submission UX is reliable offline-first (no lost submissions during UAT scenarios).
- [ ] **DC4:** Implementation is merged via Story PR → `master`.

---

## 📊 Task Skeleton

| Task | Title | Status | Depends On | Est. Time | Focus Area |
|------|-------|--------|------------|-----------|------------|
| **T01** | Submission Contracts + Foundations | ❌ FailedUAT | - | 2-3 hrs | Foundation |
| **T02** | DB Migration: `dbo.FormSubmission` (naming rules compliant) | ⏸️ Pending | T01 | 1-2 hrs | Database |
| **T03** | Backend: Public Submission Endpoint + Idempotency | ⏸️ Pending | T02 | 2-3 hrs | Backend/API |
| **T04** | Frontend: Public Outbox (IndexedDB) + Client IDs | ⏸️ Pending | T01 | 2-3 hrs | Frontend/Offline |
| **T05** | Renderer Integration: Submit → Upload/Queue + Clear-after-capture | ⏸️ Pending | T03, T04 | 2-3 hrs | Frontend/UX |
| **T06** | Kiosk Mode (optional): Auto-reset + Countdown + Session Rotation | ⏸️ Pending | T05 | 1-2 hrs | UX |
| **T07** | Validation Telemetry: Diagnostics + Storage + “Resolved vs Abandoned” Signals | ⏸️ Pending | T05 | 2-3 hrs | Observability |
| **T08** | Client Context: Compatibility + Device/Browser Signals (safe) | ⏸️ Pending | T03, T04 | 1-2 hrs | Observability |
| **T09** | Integration + UAT Polish (Scenarios 1–10) | ⏸️ Pending | T03-T08 | 2-3 hrs | Integration |

**Total Estimated Time:** 13–21 hours (3–5 days)

---

## 🔗 Dependency Graph

```
T01 (Contracts + Foundation)
 ├── T02 (DB Migration: FormSubmission)
 │    └── T03 (Backend Public Submission + Idempotency)
 │         ├── T05 (Renderer Submit Integration)
 │         │    ├── T06 (Kiosk Mode)
 │         │    └── T07 (Validation Telemetry)
 │         └── T08 (Client Context)
 └── T04 (Frontend Public Outbox)
      ├── T05 (Renderer Submit Integration)
      └── T08 (Client Context)

T09 (Integration + UAT) depends on: T03–T08
```

---

## 📁 Task Files

| Task | Task Spec | Status |
|------|-----------|--------|
| T01 | `T01-submission-contracts-and-foundation.md` | ❌ FailedUAT |
| T02 | `T02-db-migration-formsubmission.md` | ⏸️ Pending |
| T03 | `T03-backend-public-submission-endpoint.md` | ⏸️ Pending |
| T04 | `T04-frontend-public-outbox-indexeddb.md` | ⏸️ Pending |
| T05 | `T05-renderer-submit-integration.md` | ⏸️ Pending |
| T06 | `T06-kiosk-mode-auto-reset.md` | ⏸️ Pending |
| T07 | `T07-validation-telemetry-events.md` | ⏸️ Pending |
| T08 | `T08-client-context-and-compatibility.md` | ⏸️ Pending |
| T09 | `T09-integration-and-uat-polish.md` | ⏸️ Pending |

---

## 🎯 Decomposition Rationale

**Why this split works for Story 3.11:**
- The story crosses frontend + backend + DB, so we must **lock contracts first** (T01) to avoid integration surprises.
- DB changes are high risk; we isolate migration work (T02) per “Migration Safety” guidance.
- Backend endpoint and idempotency must exist before the renderer can safely “capture” submissions (T03 → T05).
- Public outbox is auth-free and must not reuse the authenticated `offlineQueue` (T04).
- Telemetry and compatibility signals are separated so they don’t bloat the core outbox path (T07–T08).
- Final task is an explicit integration/UAT checkpoint to ensure end-to-end reliability (T09).

**Risk mitigations:**
- Each task includes explicit scope boundaries + forbidden zones.
- Each task is designed to be runnable in a fresh chat (task isolation).
- The UAT guide is expanded to include kiosk + telemetry scenarios; T09 validates them.

---

## 📚 Reference Documents

- Story: `docs/stories/story-3.11.md`
- Context: `docs/stories/story-context-3.11.xml`
- UAT Guide: `docs/stories/STORY-3.11-UAT-TEST-GUIDE.md`
- Architecture: `docs/solution-architecture.md`
- Component framework: `docs/COMPONENT-FRAMEWORK-REFERENCE.md`
- Offline reference: `docs/technical-guides/OFFLINE-LEAD-CAPTURE-ARCHITECTURE.md`
- Logging: `docs/AGENT-LOGGING-GUIDE.md`
- DB standards: `docs/database-naming-rules.md`
- Git workflow: `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`

---

## ⚠️ Global Forbidden Zones

These areas are off-limits unless a task explicitly says otherwise:

| Zone | Reason |
|------|--------|
| `frontend/src/features/builder/` | Builder is complete; Story 3.11 is renderer/submission |
| `frontend/src/features/auth/` | Public renderer/submission must remain auth-free |
| `backend/modules/auth/` | Out of scope |
| `docs/tasks/3.10/` | Completed story artifacts; avoid accidental edits |

---

## 📝 Status Legend

- ⏳ **Ready** - Can start now (dependencies met)
- 🔄 **In Progress** - Currently being worked on
- ✅ **Done** - Completed and merged into story branch
- ❌ **FailedUAT** - UAT failed, needs fix task
- ⏸️ **Pending** - Waiting on dependencies

---

*Task Plan created by Ralf-SM*  
*Last Updated: 2026-02-03*

