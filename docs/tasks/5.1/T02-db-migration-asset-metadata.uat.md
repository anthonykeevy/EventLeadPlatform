# UAT Checklist: T02

**Story:** 5.1  
**Task:** DB Migration — Asset Metadata Tables (`dbo.Asset` + `ref.AssetType`)  
**Generated:** 2026-02-09  

---

## Pre-conditions

- [ ] DB connection available for local/dev environment
- [ ] Working directory is repo root
- [ ] Alembic is available (`cd backend; alembic --help`)

## Test Steps

### AC1: Migration file exists and follows naming rules

- [ ] Step 1: Inspect `backend/migrations/versions/038_asset_metadata_tables.py` → Verify: PascalCase names, `ref`/`dbo` schemas, NVARCHAR text fields, audit + soft-delete columns.

### AC2: `ref.AssetType` exists and contains at least `IMAGE`

- [ ] Step 1: Run `cd backend; alembic upgrade head` → Verify: migration completes without errors.
- [ ] Step 2: Query `ref.AssetType` → Verify: row exists with `TypeCode='IMAGE'` and `IsDeleted = 0`.

### AC3: `dbo.Asset` exists with required columns/constraints

- [ ] Step 1: Inspect schema (`dbo.Asset`) → Verify: `AssetTypeID` FK to `ref.AssetType`.
- [ ] Step 2: Inspect columns → Verify: `DisplayName`, `OriginalFileName`, `IsDeleted`, `DeletedDate`, `DeletedBy`, `Sha256`.
- [ ] Step 3: Inspect indexes → Verify: `UQ_Asset_CompanyID_AssetTypeID_Sha256` exists and is filtered on `IsDeleted = 0`.

### AC4: Human-run migration recorded in task completion note

- [ ] Step 1: Open `docs/tasks/5.1/T02-db-migration-asset-metadata.completion.md` → Verify: migration commands + verification steps are recorded.

## Regression Check

- [ ] `git diff --name-only origin/story/epic5-5.1-background-asset-management...HEAD` → Verify: no changes under `frontend/`.

## Post-conditions

- [ ] Alembic head is at the desired revision (upgrade back to head if downgrade was executed).

## Edge Cases (optional)

- [ ] (If you have a sample upload flow ready) Attempt inserting a duplicate `(CompanyID, AssetTypeID, Sha256)` with `IsDeleted=0` → Verify: DB rejects duplicates (unique filtered index enforced).

---

**Instructions for Human Tester:**
1. Execute each step in order
2. Mark ✅ or ❌ for each item
3. Add notes for any failures
4. When complete, run `@ralf-uat *record-uat` with your results

