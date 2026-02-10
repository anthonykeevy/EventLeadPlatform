# Lessons Learned — Story 5.1

This file is updated after each task retro.

---

## Entries

### 2026-02-09 — T01 (Asset Contracts + Config Foundations)

- **Baseline reality:** frontend build/typecheck currently fails due to pre-existing TypeScript errors; treat as baseline, record evidence, and run scoped verification for touched areas.
- **Workflow improvements:**
  - Task spec is approval → avoid re-confirm prompts during execution.
  - Frontend verification must run from `frontend/` in the correct worktree.
  - Rename generic `T01.*` artifacts to `${TaskBase}.*` before commit/merge.

**Links (T01):**
- Transcript: `docs/Transcripts/Epic-5-Story-5.1-Task-T01.md`
- Completion: `T01-asset-contracts-and-config-foundations.completion.md`
- UAT results: `T01-asset-contracts-and-config-foundations.uat-results.md`
- Retro: `T01-asset-contracts-and-config-foundations.retro.md`

### 2026-02-09 — T02 (DB Migration — Asset Metadata Tables)

- **Dev Lessons:** Multi-worktree DB tasks need a migration-history sync preflight before creating new Alembic revisions.
- **Testing Lessons:** Add a scripted preflight to compare DB `alembic_version` to latest migration file before human runs.
- **Process Lessons:** Include revision-chain sanity checks in DB task specs and UAT checklists.

**Links (T02):**
- Completion: `T02-db-migration-asset-metadata.completion.md`
- UAT results: `T02-db-migration-asset-metadata.uat-results.md`
- Retro: `T02-db-migration-asset-metadata.retro.md`

### 2026-02-09 — T03 (Backend Asset Service + Upload API)

- **Dev Lessons:** SQLite test harness needs schema-attach and explicit IDs when using schema-qualified models.
- **Testing Lessons:** Add a deterministic dedup integration test (upload same file twice, assert `isDuplicate=true`).
- **Process Lessons:** Include explicit resolver URL expectations (local vs azure) in AC verification.

**Links (T03):**
- Transcript: `docs/Transcripts/cursor_epic_5_story_5_1_task_t03.md`
- Completion: `T03-backend-asset-service-and-upload-api.completion.md`
- UAT results: `T03-backend-asset-service-and-upload-api.uat-results.md`
- Retro: `T03-backend-asset-service-and-upload-api.retro.md`

### 2026-02-10 — T04 (Frontend Builder Asset Upload + Library + Ref)

- **Dev Lessons:** Python stdlib logging: first positional arg is message; no `msg=` keyword. Do not put reserved names (e.g. `filename`, `message`) in `extra` — use prefixed keys (e.g. `asset_filename`).
- **Testing Lessons:** Relax client file-type check when `file.type` is empty but extension is image; normalize `image/jpg` → `image/jpeg` server-side for JPG uploads.
- **Process Lessons:** When Background Style toggles (Image ↔ Colour), persist both branches (e.g. `colorValue` for colour; keep asset/imageSize/imagePosition when switching to Colour).

**Links (T04):**
- Completion: `T04-frontend-builder-asset-upload-and-library.completion.md`
- UAT results: `T04-frontend-builder-asset-upload-and-library.uat-results.md`
- Retro: `T04-frontend-builder-asset-upload-and-library.retro.md`

