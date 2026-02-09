# Task T02: DB Migration — Asset Metadata Tables

**Story:** 5.1 - Background Asset Management  
**Task ID:** T02  
**Status:** 🔄 In Progress (Approved)
**Dependencies:** T01  
**Estimated Time:** 1-2 hours  

---

## 📋 Task Overview

**Objective:** Add DB tables for asset metadata and references, following naming rules.
This task includes migration file creation and human-run migration execution.

**Naming decisions (locked for Epic 5):**
- Asset table: `dbo.Asset`
- Asset type enum table: `ref.AssetType` (FK from `dbo.Asset.AssetTypeID`)

---

## ✅ Scope (In)

- [ ] Create migration for:
  - `ref.AssetType` (enum/reference table)
  - `dbo.Asset` (asset metadata)
- [ ] Add required indexes/constraints (hash dedup, soft-delete support)
- [ ] Seed required `ref.AssetType` rows (minimum: `IMAGE`)

---

## 🚫 Scope (Out)

- ❌ No API endpoints (T03)
- ❌ No frontend changes (T04+)

---

## 🔒 Forbidden Zones

| Path | Reason |
|------|--------|
| `frontend/` | DB-only task |

---

## ✅ Acceptance Criteria

- Migration file exists and follows `docs/database-naming-rules.md`
- `ref.AssetType` exists and contains at least `IMAGE`
- `dbo.Asset` exists with:
  - `AssetTypeID` FK → `ref.AssetType`
  - hash-based dedup support (e.g., unique constraint/index scoped to Company + AssetType + Sha256)
  - soft-delete support
  - display name support
- Human-run migration recorded in task completion note

---

## 🧪 Required Tests / Verification

- Migration file is linted for naming conventions
- Human runs migration (agent must not run Alembic commands)

---

## 🔁 Out-of-Scope Handling

If asked to:
- Implement API endpoints → route to **T03**
- Modify builder UI → route to **T04**

---

## 🌿 Git / PR Requirements (Mandatory)

- Create branch: `task/5.1/T02-db-migration-asset-metadata`
- Open PR: `task/5.1/...` → `story/epic5-5.1-background-asset-management`

```powershell
scripts/git/new-task.ps1 -StoryBranch "story/epic5-5.1-background-asset-management" -StoryId 5.1 -TaskId T02 -Slug "db-migration-asset-metadata" -CreateWorktree
```

---

## 📚 References

- Story: `docs/stories/story-5.1.md`
- DB rules: `docs/database-naming-rules.md`

