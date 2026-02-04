# Task T05: Renderer Integration - Submit → Upload/Queue + Clear-after-capture

**Story:** 3.11 - Dynamic Submission (Outbox)  
**Task ID:** T05  
**Status:** ✅ Done  
**Dependencies:** T03, T04  
**Estimated Time:** 2-3 hours  

---

## Brief Scope

- Wire the renderer submit flow to:
  - validate
  - upload immediately when online, or enqueue when offline/failure
  - show success/queued UX
  - clear values after capture (uploaded or queued) for shared-device safety
- Ensure idempotency key is generated once per submission capture.

## Git / PR (Mandatory)

- Branch: `task/3.11/T05-renderer-submit-integration`
- PR: task → `story/epic3-3.11-dynamic-submission`

