# Task T04: Frontend - Public Outbox (IndexedDB) + Client IDs

**Story:** 3.11 - Dynamic Submission (Outbox)  
**Task ID:** T04  
**Status:** ⏸️ Pending  
**Dependencies:** T01  
**Estimated Time:** 2-3 hours  

---

## Brief Scope

- Implement an auth-free public outbox service backed by IndexedDB (do **not** reuse `frontend/src/utils/offlineQueue.ts` which assumes authenticated userId).
- Support enqueue, retry with backoff, status transitions, and auto-process on `online` event.
- Implement `clientDeviceId` persistence and `clientSessionId` rotation rules (kiosk-safe).

## Git / PR (Mandatory)

- Branch: `task/3.11/T04-frontend-public-outbox-indexeddb`
- PR: task → `story/epic3-3.11-dynamic-submission`

