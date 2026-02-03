# UAT Checklist: T02

**Story:** 3.11  
**Task:** DB Migration - `dbo.FormSubmission`  
**Generated:** 2026-02-03  

---

## Pre-conditions

- [ ] DB connection available for local/dev environment
- [ ] Working directory is repo root
- [ ] Alembic is available (`cd backend; alembic --help`)

## Test Steps

### AC1: Table exists and follows naming rules

- [ ] Step 1: Run `cd backend; alembic upgrade head` → Verify: migration completes without errors.
- [ ] Step 2: Inspect schema (`dbo.FormSubmission`) → Verify: PascalCase columns, NVARCHAR text fields, audit columns present.

### AC2: Idempotency uniqueness is enforced

- [ ] Step 1: Inspect constraints on `dbo.FormSubmission` → Verify: `UQ_FormSubmission_IdempotencyKey` exists.

### AC3: Referential integrity exists

- [ ] Step 1: Inspect FK constraints → Verify: FKs to `dbo.Form`, `dbo.FormVersion`, `dbo.FormPublicLink` (and audit FKs if present).

### AC4: Migration is reversible (downgrade)

- [ ] Step 1: Run `cd backend; alembic downgrade 034` → Verify: `dbo.FormSubmission` is removed cleanly.

## Regression Check

- [ ] `git diff --name-only origin/story/epic3-3.11-dynamic-submission...HEAD` → Verify: no changes under `frontend/` or `backend/modules/`.

## Post-conditions

- [ ] Alembic head is restored to desired revision (upgrade back to head if downgrade was executed).

## Edge Cases (if applicable)

- [ ] Attempt to insert duplicate `IdempotencyKey` → Verify: DB rejects duplicates (unique constraint enforced).

---

**Instructions for Human Tester:**
1. Execute each step in order
2. Mark ✅ or ❌ for each item
3. Add notes for any failures
4. When complete, run `@ralf-uat *record-uat` with your results
