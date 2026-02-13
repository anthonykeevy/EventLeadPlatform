# Task T07: Validation Telemetry - Events + Storage + Resolved vs Abandoned

**Story:** 3.11 - Dynamic Submission (Outbox)  
**Task ID:** T07  
**Status:** ✅ HumanDone  
**Dependencies:** T05  
**Estimated Time:** 2-3 hours  

---

## Brief Scope

- Emit `validation_failed_submit` events when submit is blocked by validation.
- Include rule/component identity + value diagnostics (type/length/shape) and exclude raw values.
- Store telemetry in a queryable backend table (reuse existing frontend logging tables if present, otherwise add a minimal `log.FormValidationEvent`).
- Ensure we can derive **resolved vs abandoned** sessions via correlation (`clientSessionId` + `submission_captured`).

## Git / PR (Mandatory)

- Branch: `task/3.11/T07-validation-telemetry-events`
- PR: task → `story/epic3-3.11-dynamic-submission`

