# Task Completion: T02

**Story:** 5.1  
**Task:** DB Migration — Asset Metadata Tables (`dbo.Asset` + `ref.AssetType`)  
**Completed:** 2026-02-09  
**Status:** Complete  

---

## Summary of Changes

Added a new Alembic migration that creates `ref.AssetType` (seeded with `IMAGE`) and `dbo.Asset` with required audit/soft-delete columns, referential integrity, and hash-based deduplication support (unique filtered index). Synced missing KB migrations (`036`, `037`) into the worktree to align Alembic history with the current DB revision.

## Files Changed

| File | Change | Reason |
|------|--------|--------|
| `backend/migrations/versions/036_kb_knowledge_base.py` | Created | Bring KB migration into worktree (needed for Alembic history) |
| `backend/migrations/versions/037_kb_docref_null_safe_uniqueness.py` | Created | Bring KB migration into worktree (needed for Alembic history) |
| `backend/migrations/versions/038_asset_metadata_tables.py` | Created | Create `ref.AssetType` + `dbo.Asset`, seed `IMAGE`, add dedup/indexes |
| `docs/tasks/5.1/T02-db-migration-asset-metadata.md` | Modified | PR bootstrap: mark task as In Progress (Approved) |

## Acceptance Criteria Verification

### AC1: Migration file exists and follows naming rules
- **Status:** PASS
- **Evidence:** `backend/migrations/versions/038_asset_metadata_tables.py` uses PascalCase tables/columns, `ref`/`dbo` schemas, and `NVARCHAR` for text fields.

### AC2: `ref.AssetType` exists and contains at least `IMAGE`
- **Status:** PASS (on migration execution)
- **Evidence:** Migration creates `ref.AssetType` and seeds `TypeCode='IMAGE'` if not present.

### AC3: `dbo.Asset` exists with required columns/constraints
- **Status:** PASS (on migration execution)
- **Evidence:** Migration creates `dbo.Asset` with:
  - `AssetTypeID` FK → `ref.AssetType.AssetTypeID` (`FK_Asset_AssetTypeID`)
  - **Hash dedup**: `UQ_Asset_CompanyID_AssetTypeID_Sha256` (unique filtered index where `IsDeleted = 0`)
  - **Soft-delete**: `IsDeleted`, `DeletedDate`, `DeletedBy`
  - **Display name support**: `DisplayName` + `OriginalFileName`

### AC4: Human-run migration recorded in task completion note
- **Status:** PASS
- **Evidence:** Commands + verification steps included below.

## Test Evidence

### Automated Tests
```bash
python -m py_compile "backend/migrations/versions/038_asset_metadata_tables.py"
```

### Human-Executed Migration Commands (REQUIRED)
```powershell
cd backend
alembic upgrade head
```

### Optional rollback (if needed)
```powershell
cd backend
alembic downgrade 037
```

### Post-migration verification queries (recommended)
```sql
-- Seed exists
SELECT AssetTypeID, TypeCode, TypeName, IsActive, IsDeleted
FROM ref.AssetType
WHERE TypeCode = 'IMAGE';

-- Table exists (smoke)
SELECT TOP (1) *
FROM dbo.Asset;

-- Dedup unique index exists (filtered on IsDeleted = 0)
SELECT
  i.name,
  i.is_unique,
  i.filter_definition
FROM sys.indexes i
JOIN sys.objects o ON o.object_id = i.object_id
JOIN sys.schemas s ON s.schema_id = o.schema_id
WHERE s.name = 'dbo'
  AND o.name = 'Asset'
  AND i.name = 'UQ_Asset_CompanyID_AssetTypeID_Sha256';
```

## Manual UAT Steps

For human verification:

1. [ ] Run `cd backend; alembic upgrade head` → Verify: migration completes without errors.
2. [ ] Inspect DB schema → Verify: `ref.AssetType` exists and includes `TypeCode='IMAGE'`.
3. [ ] Inspect DB schema → Verify: `dbo.Asset` exists with expected columns and FK `FK_Asset_AssetTypeID`.
4. [ ] Inspect indexes → Verify: `UQ_Asset_CompanyID_AssetTypeID_Sha256` exists and is filtered on `IsDeleted = 0`.
5. [ ] Optional: `cd backend; alembic downgrade 037` → Verify: clean rollback (tables removed).

## Known Limitations / Out-of-Scope Items

- [ ] Migration execution requires a human (agent does not run Alembic).

## Recommended Next Step

Ready for UAT by human.

