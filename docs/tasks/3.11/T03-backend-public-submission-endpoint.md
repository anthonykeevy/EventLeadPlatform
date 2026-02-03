# Task T03: Backend - Public Submission Endpoint + Idempotency

**Story:** 3.11 - Dynamic Submission (Outbox)  
**Task ID:** T03  
**Status:** ⏸️ Pending  
**Dependencies:** T02  
**Estimated Time:** 2-3 hours  

---

## Brief Scope

- Implement token-gated `POST /api/public/forms/{token}/submissions` using the T01 contract.
- Validate token/link state and resolve correct `FormVersionID` (PREVIEW vs PRODUCTION behavior matches resolver rules).
- Persist to `dbo.FormSubmission` with idempotency (duplicate idempotency key returns the existing submission id).
- Update `dbo.Form` counters (`TotalSubmissions`, `LastSubmissionDate`) as appropriate.

## Git / PR (Mandatory)

- Branch: `task/3.11/T03-backend-public-submission-endpoint`
- PR: task → `story/epic3-3.11-dynamic-submission`

