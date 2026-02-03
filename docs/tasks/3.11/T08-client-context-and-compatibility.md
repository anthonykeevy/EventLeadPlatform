# Task T08: Client Context - Compatibility + Device/Browser Signals

**Story:** 3.11 - Dynamic Submission (Outbox)  
**Task ID:** T08  
**Status:** ⏸️ Pending  
**Dependencies:** T03, T04  
**Estimated Time:** 1-2 hours  

---

## Brief Scope

- Capture and persist client context with submissions (safe, non-fingerprinting):
  - browser/OS (UA), screen/viewport/DPR, canvas size/scale, touch/orientation, etc.
- Store in submission `ContextJSON` (and/or selected columns if needed later for queries).
- Record server-derived country signal (`ipCountryCode`) if available/feasible (privacy-aware; retention rules).

## Git / PR (Mandatory)

- Branch: `task/3.11/T08-client-context-and-compatibility`
- PR: task → `story/epic3-3.11-dynamic-submission`

