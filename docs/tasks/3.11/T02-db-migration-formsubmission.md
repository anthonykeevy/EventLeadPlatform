# Task T02: DB Migration - `dbo.FormSubmission`

**Story:** 3.11 - Dynamic Submission (Outbox)  
**Task ID:** T02  
**Status:** ⏸️ Pending  
**Dependencies:** T01  
**Estimated Time:** 1-2 hours  

---

## Brief Scope

- Create a DB migration that adds `dbo.FormSubmission` (and required indexes/constraints) to persist public submissions.
- Must follow `docs/database-naming-rules.md` (PascalCase, NVARCHAR, constraint/index naming, audit columns).
- Include idempotency protection (unique constraint on `IdempotencyKey` or scoped uniqueness per form/link).
- Human executes migration commands (agent prepares files + exact commands only).

## Git / PR (Mandatory)

- Branch: `task/3.11/T02-db-migration-formsubmission`
- PR: task → `story/epic3-3.11-dynamic-submission`

