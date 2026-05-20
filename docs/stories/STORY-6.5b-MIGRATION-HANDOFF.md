# Story 6.5b - Migration Handoff (Tony executes)

**Status:** ✅ Complete (2026-05-20). Tony executed migrations 078–083 on LocalDB; PR #104 merged; Azure Test R6 verification green.

**PR:** [#104](https://github.com/SignalPlatforms/EventLeadPlatform/pull/104) — merged to `develop`. Migration **083** (Block A trim) ships in the SM closeout housekeeping PR if not already on `develop`.

**Branch:** `story/epic6-6.5b-registry-foundation` (worktree at `C:\wt\elp\story-epic6-6.5b-registry-foundation`).

---

## TL;DR

Five migrations renumbered from `073-077` to `078-082` to avoid collision with the existing `073_seed_platform_owner_user_signalplatforms.py` / `074_seed_platform_owner_onboarding_complete.py` chain. The 6.5b chain pivots off head revision `074` (onboarding complete) and ends at `082`.

```powershell
# Tony runs these in order, against LocalDB first, then Test:
cd backend
alembic current             # should report 074 (or whatever the current chain head is)
alembic upgrade head        # applies 078 -> 079 -> 080 -> 081 -> 082
alembic current             # should now report 082
```

The migrations are **purely additive** for the registry tables (new `config.PromptAssemblyRegistry*` tables) and **add two columns** to `dbo.GenerationRun` (`PromptAssemblyRegistryVersionID`, `PromptVariantSnapshot`). No existing rows are modified. All migrations have working `downgrade()` paths.

---

## Migration set

| File | Revision | Down | Purpose | Rows affected |
|------|----------|------|---------|---------------|
| `078_story_6_5b_prompt_assembly_registry_schema.py` | `078` | `074` | Creates the four registry tables: `config.PromptAssemblyRegistry`, `PromptAssemblyRegistryVersion`, `PromptSection`, `PromptSectionVariant`, `PromptSectionData`. Adds CHECK constraints on `DataStructureType` / `DataType`. | 0 (DDL only) |
| `079_story_6_5b_seed_form_ai_v1_profile.py` | `079` | `078` | Inserts the `FORM_AI_V1` registry, an active `VersionNumber=1`, and the five `PromptSection` rows for blocks A / B / C / G / I in their current emission order. | +1 registry row, +1 version row, +5 section rows |
| `080_story_6_5b_seed_variants_a_b_c_i.py` | `080` | `079` | Seeds `PromptSectionVariant` rows: A (`DEFAULT`), B (`DEFAULT`), I (`DEFAULT`), C (`local` [IsDefault=1] / `heritage` / `neutral` / `transcreate`). Block A/B/I prose mirrors the literals that lived in `service.py`. Block C variants mirror the strings returned by `_render_brand_posture_block`. | +7 variant rows |
| `081_story_6_5b_seed_block_g_context_pack.py` | `081` | `080` | Seeds Block G `DEFAULT` variant from a Python literal containing the trimmed `STORY-6.2-AI-CONTEXT-PACK.md` content (computed offline at base commit `cb339ed`; SHA256 in the migration docstring). **This is the migration that closes R6** — once applied, runtime no longer reads the markdown file. | +1 variant row |
| `082_story_6_5b_generation_run_assembly_audit.py` | `082` | `081` | Adds `PromptAssemblyRegistryVersionID BIGINT NULL` (FK to `config.PromptAssemblyRegistryVersion`) and `PromptVariantSnapshot NVARCHAR(MAX) NULL` to `dbo.GenerationRun`. | 0 row mutations; ALTER TABLE only |

**Downgrade behaviour:** Each migration's `downgrade()` reverses the upgrade exactly. 082 drops the FK + columns; 081 deletes the seeded Block G variant; 080 deletes the seven A/B/C/I variants; 079 deletes the five sections + version + registry; 078 drops the four registry tables. Running `alembic downgrade 074` returns the schema to pre-6.5b state.

---

## Step-by-step procedure (Tony)

### 1. Apply migrations on LocalDB

```powershell
cd backend
alembic current
alembic upgrade head
alembic current   # expect: 082
```

### 2. Verification SELECTs (LocalDB)

Run these against LocalDB (SSMS or `sqlcmd`) to confirm seeding worked.

```sql
-- 079: registry + version + 5 sections
SELECT TOP 1 [PromptAssemblyRegistryID], [Code], [Description], [IsActive]
FROM [config].[PromptAssemblyRegistry]
WHERE [Code] = 'FORM_AI_V1';
-- Expected: 1 row, IsActive=1

SELECT [PromptAssemblyRegistryVersionID], [VersionNumber], [IsActive]
FROM [config].[PromptAssemblyRegistryVersion] prv
INNER JOIN [config].[PromptAssemblyRegistry] pr
  ON pr.[PromptAssemblyRegistryID] = prv.[PromptAssemblyRegistryID]
WHERE pr.[Code] = 'FORM_AI_V1';
-- Expected: 1 row, VersionNumber=1, IsActive=1

SELECT [SectionCode], [SortOrder], [IsRequired], [DataStructureType]
FROM [config].[PromptSection] ps
INNER JOIN [config].[PromptAssemblyRegistryVersion] prv
  ON prv.[PromptAssemblyRegistryVersionID] = ps.[PromptAssemblyRegistryVersionID]
INNER JOIN [config].[PromptAssemblyRegistry] pr
  ON pr.[PromptAssemblyRegistryID] = prv.[PromptAssemblyRegistryID]
WHERE pr.[Code] = 'FORM_AI_V1'
ORDER BY [SortOrder];
-- Expected: 5 rows in SortOrder (A, B, I, G, C)

-- 080: 7 A/B/C/I variants (1 + 1 + 4 + 1)
SELECT ps.[SectionCode], psv.[VariantCode], psv.[IsDefault],
       LEN(psv.[PromptSnippet]) AS SnippetLen
FROM [config].[PromptSectionVariant] psv
INNER JOIN [config].[PromptSection] ps
  ON ps.[PromptSectionID] = psv.[PromptSectionID]
WHERE ps.[SectionCode] IN ('A', 'B', 'C', 'I')
ORDER BY ps.[SectionCode], psv.[VariantCode];
-- Expected:
--   A | DEFAULT     | 1 | ~245
--   B | DEFAULT     | 1 | ~750
--   C | heritage    | 0 | ~150
--   C | local       | 1 | ~73
--   C | neutral     | 0 | ~120
--   C | transcreate | 0 | ~125
--   I | DEFAULT     | 1 | ~1750

-- 081: Block G variant exists with non-empty Snippet
SELECT psv.[VariantCode], LEN(psv.[PromptSnippet]) AS SnippetLen
FROM [config].[PromptSectionVariant] psv
INNER JOIN [config].[PromptSection] ps
  ON ps.[PromptSectionID] = psv.[PromptSectionID]
WHERE ps.[SectionCode] = 'G';
-- Expected: 1 row, VariantCode='DEFAULT', SnippetLen ~6800-7400.

-- Quick spot-check the trimmed marker is NOT in the seeded prose
-- (i.e. the trim happened correctly).
SELECT
  CASE
    WHEN psv.[PromptSnippet] LIKE '%## Operational Notes%' THEN 'FAIL: trim marker present'
    ELSE 'OK: trim correct'
  END AS BlockGTrimVerdict
FROM [config].[PromptSectionVariant] psv
INNER JOIN [config].[PromptSection] ps
  ON ps.[PromptSectionID] = psv.[PromptSectionID]
WHERE ps.[SectionCode] = 'G';
-- Expected: 'OK: trim correct'

-- 082: GenerationRun has new columns (no rows yet, just schema check)
SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME = 'GenerationRun'
  AND COLUMN_NAME IN ('PromptAssemblyRegistryVersionID', 'PromptVariantSnapshot');
-- Expected: 2 rows — both nullable, types BIGINT and NVARCHAR(MAX).
```

### 3. Local backend smoke test (after migrations apply)

```powershell
# Terminal 1 - backend
cd backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload --port 8000

# Terminal 2 - frontend
cd frontend
npm run dev

# Browser:
# - Sign in as a normal company-admin user.
# - Open the AI Agent panel (form builder).
# - Submit prompt: "Build a contact form for a Sydney tech conference."
# - Expect: success status; the generated form renders to the canvas.
# - Confirm the AI panel terminal trace does NOT contain
#   `context-pack-load-failed` or `prompt-assembly-resolution-failed`.
```

### 4. Verify GenerationRun audit columns populate

After the local smoke test, run:

```sql
SELECT TOP 3
  GenerationRunID,
  Status,
  TerminalReason,
  PromptAssemblyRegistryVersionID,
  LEN(PromptVariantSnapshot)            AS SnapshotLen,
  PromptVariantSnapshot
FROM dbo.GenerationRun
ORDER BY GenerationRunID DESC;
-- Expected: most recent row has PromptAssemblyRegistryVersionID populated
-- (FK to a real registry version row, NOT NULL) and PromptVariantSnapshot
-- contains a JSON object with keys A/B/C/G/I and integer variant IDs.
```

### 5. AC-19 sign-off

Open `docs/stories/STORY-6.5b-PROMPT-EQUIVALENCE-DIFF.md`. Tick the three Tony-sign-off checkboxes after confirming:

- All five blocks (A, B, C, G, I) report `IDENTICAL` for every of the four postures.
- Top-level verdict is `PASS`.
- Top-level commit SHA in the report matches the latest commit on the branch when you reviewed it (regenerate via `python backend/scripts/story_6_5b_prompt_equivalence_diff.py` if it drifts).

### 6. PR Draft → Ready

Once steps 1-5 are clean:

```powershell
gh pr ready 104
```

### 7. After merge to develop + Test deploy

Re-run the smoke test against the deployed Test environment. The success criteria is **R6 verified resolved**: AI generation completes without the `context-pack-load-failed` terminal reason that PR #101 surfaced. Once verified, flip `EPIC-6-STATUS.md` row 6.5b to ✅ Complete (parity-check date stamp).

---

## Rollback plan (if Step 1 or Step 3 fails)

```powershell
cd backend
alembic downgrade 074
```

This reverses 082 → 081 → 080 → 079 → 078 in turn, restoring the pre-6.5b schema. After downgrade, runtime AI generation will fail with `prompt-assembly-resolution-failed` because the resolver no longer finds an active `FORM_AI_V1` registry. To restore pre-6.5b runtime behaviour, also revert `service.py` to the commit before this branch (or simply revert the merge commit).

If the issue is _seed-only_ (Block G prose drift, etc.) and the schema is fine, you can re-apply just the data-side migrations:

```powershell
alembic downgrade 080  # roll back 081 + 082
alembic upgrade head   # re-apply
```

---

## Notes for Tony

- **Naming reconciliation deferred to 6.5c.** The architecture document refers to these tables as `config.PromptAssemblyProfile*`. The implementation uses `config.PromptAssemblyRegistry*` to avoid collision with the existing `config.PromptAssemblyProfile` (Story 6.3.1 governance step profile, FK'd from `dbo.GenerationRun.PromptAssemblyProfileID`). Story 6.5c will reconcile the architecture doc to the implementation name (or rename the tables — Dev's call given the existing FK lineage).
- **Context pack file kept on disk.** `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md` retains a documentation banner pointing at the registry; runtime no longer reads it. Migration 081 is the single source of truth for Block G prose.
- **Eval harness still works.** `backend/tests/form_ai_eval/au_diagnostics.py::build_context_sections` was updated to call the resolver/renderer the same way runtime does. The AU eval suite (`tests/test_form_ai_eval_*`) passes 23/23 on the branch.
- **Pre-existing test failures unchanged.** Two tests in `test_form_ai_first_shot.py` and one in `test_story_63_context_pack_path.py` fail on this branch; they were already failing on the base commit `cb339ed`. The mock signature mismatch (`'str' object has no attribute 'content'`) is unrelated to 6.5b. They are flagged in `STORY-6.5b-GATE-EVIDENCE.md`.
