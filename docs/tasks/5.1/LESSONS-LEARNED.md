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

---

### 2026-02-11 — T05 (Shared Resolver Parity — Builder + Renderer)

- **Dev Lessons:** Run `npm run build` after first implementation pass to catch dep drift (libphonenumber), type mismatches (objectFit), and branch-divergence issues (lib/auth). When adding JSX wrappers, verify closing tag count matches.
- **Testing Lessons:** Add unit test for `resolveAssetContentUrl` output format. Consider E2E for "upload asset → set background → verify builder + renderer show same image."
- **Process Lessons:** For resolver-parity tasks, include explicit contract verification in AC (e.g. URL format matches backend). UAT results should require explicit Pass/Fail per regression item. Orphan asset 404s (metadata exists, files missing) are data hygiene, not resolver defects.

**Links (T05):**
- Completion: `T05-shared-resolver-parity.completion.md`
- UAT results: `T05-shared-resolver-parity.uat-results.md`
- Retro: `T05-shared-resolver-parity.retro.md`

### 2026-02-13 — T06 (Placement + Intersection Rule + Cropping)

- **Dev Lessons:** Placement utils (`isBackgroundFullyOffCanvas`, `createDefaultPlacement`) are pure functions; add unit tests early for edge cases (fully on, fully off, partial overlap). Build after placement changes — canvas rendering is sensitive to placement object shape.
- **Testing Lessons:** Unit test placement utils. Integration: placement round-trip builder → definition → renderer. UAT automation candidates: console check when loading form with placement; definition check for `page.background.placement`.
- **Process Lessons:** Explicit regression checklist (color-only, external URL, console, form submit) works well for canvas/rendering tasks. Scope crop UI explicitly in/out to avoid ambiguity. T05 learning applied: explicit Pass/Fail per regression item in UAT results.

**Links (T06):**
- Completion: `T06-placement-intersection-and-cropping.completion.md`
- UAT results: `T06-placement-intersection-and-cropping.uat-results.md`
- Retro: `T06-placement-intersection-and-cropping.retro.md`

### 2026-02-13 — T07 (Data URL Guard + Cleanup)

- **Dev Lessons:** Shared utility pattern (`dataUrlGuard.ts`) for guard logic enables reuse across input, load, and save paths. Add unit tests for pure guard functions (isDataUrl, strip*) alongside implementation.
- **Testing Lessons:** Unit tests for dataUrlGuard cover isDataUrl, stripDataUrlFromBackground, DATA_URL_ERROR_MESSAGE. UAT automation candidates: AC1 (paste Data URL → assert error) via browser MCP; AC3 (save → assert no data: in definition) via response parsing.
- **Process Lessons:** Guard/cleanup tasks: list all entry points (input, load path(s), save path) in task spec. Human UAT deferred when agent lacks authenticated session; single-prompt cycle commits and pushes; human runs UAT then merge.

**Links (T07):**
- Completion: `T07-data-url-guard-and-cleanup.completion.md`
- UAT results: `T07-data-url-guard-and-cleanup.uat-results.md`
- Retro: `T07-data-url-guard-and-cleanup.retro.md`

