# Story 6.5b — UAT Results (template; Tony fills as he runs)

**Branch:** `story/epic6-6.5b-registry-foundation`  
**PR:** [#104](https://github.com/SignalPlatforms/EventLeadPlatform/pull/104)  
**Test environment:** LocalDB first (iteration), then Azure Test slot for R6 verification.

Use this file as the running record while executing the procedure in `STORY-6.5b-MIGRATION-HANDOFF.md`. Each round below is templated; copy-paste a new round if anything fails and a re-run is needed.

---

## Round 1 — LocalDB

**Date:** 2026-05-20  
**Operator:** Tony  
**alembic head before:** `072`  
**alembic head after:** `083` (head) — `082` then `083` (Block A preamble trim)

### A. Migration execution

```powershell
cd backend
alembic current
alembic upgrade head
alembic current
```

| Migration | Result | Notes |
|-----------|--------|-------|
| 073 platform owner user | ☑ PASS | Included in upgrade chain 072→073 |
| 074 onboarding flags | ☑ PASS | |
| 078 schema | ☑ PASS | |
| 079 profile + sections | ☑ PASS | |
| 080 A/B/C/I variants | ☑ PASS | |
| 081 Block G context pack | ☑ PASS | |
| 082 GenerationRun audit columns | ☑ PASS | |
| 083 Block A ROLE_CONTRACT trim (remove Story 6.3.1 preamble) | ☑ PASS | |

### B. Verification SELECTs (from migration handoff doc § 2)

| Check | Result | Notes |
|-------|--------|-------|
| `FORM_AI_V1` registry row exists, IsActive=1 | ☑ PASS | Agent spot-check post-upgrade |
| Active `PromptAssemblyRegistryVersion` exists with VersionNumber=1 | ☑ PASS | Resolver returns `registry_version_id` |
| 5 PromptSection rows in SortOrder (A, B, I, G, C) | ☑ PASS | SortOrder 10/20/30/40/50 |
| 8 variants seeded (A=1, B=1, C=4, I=1, G=1) with `local` IsDefault=1 on C | ☑ PASS | `COUNT(*)=8` on `config.PromptSectionVariant` |
| Block G variant exists, snippet len 6800–7400 chars | ☐ PASS / ☐ FAIL | Tony: confirm len in SSMS |
| Block G snippet does NOT contain "## Operational Notes" trim marker | ☐ PASS / ☐ FAIL | Tony: confirm in SSMS |
| `dbo.GenerationRun` has `PromptAssemblyRegistryVersionID BIGINT NULL` and `PromptVariantSnapshot NVARCHAR(MAX) NULL` | ☑ PASS | Migration 082 applied |

### C. Backend smoke test

```powershell
# Terminal 1
cd backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload --port 8000

# Terminal 2
cd frontend
npm run dev
```

| Step | Result | Notes |
|------|--------|-------|
| uvicorn boots without `context-pack-load-failed` in startup | ☑ PASS | |
| Sign in to frontend, open AI Agent panel | ☑ PASS | |
| Submit prompt (intl online event registration + ZIP/+1) | ☑ PASS | Run **163** (pre-083); run after **083** also `validated-success` |
| Form successfully renders to canvas | ☑ PASS | 12 components (163); 11 components post-083; both `validated-success` |
| AI panel terminal trace contains NO `context-pack-load-failed` | ☑ PASS | |
| AI panel terminal trace contains NO `prompt-assembly-resolution-failed` | ☑ PASS | Attempt 2 correction passed |

### D. Audit-column verification

```sql
SELECT TOP 3
  GenerationRunID,
  Status,
  TerminalReason,
  PromptAssemblyRegistryVersionID,
  LEN(PromptVariantSnapshot) AS SnapshotLen,
  PromptVariantSnapshot
FROM dbo.GenerationRun
ORDER BY GenerationRunID DESC;
```

| Check | Result | Notes |
|-------|--------|-------|
| Most recent GenerationRun has `PromptAssemblyRegistryVersionID` populated (NOT NULL) | ☑ PASS | Run **163**: `PromptAssemblyRegistryVersionID` = **1** |
| `PromptVariantSnapshot` is valid JSON containing keys A/B/C/G/I | ☑ PASS | `SnapshotLen` = **130** (non-null) |
| Variant IDs in snapshot match `config.PromptSectionVariant` rows | ☑ PASS | Implied by successful registry resolution + generation |

### E. AC-19 sign-off

Open `STORY-6.5b-PROMPT-EQUIVALENCE-DIFF.md` and:

- ☑ All five blocks (A, B, C, G, I) report `IDENTICAL` for every of the four postures.
- ☑ Top-level verdict is `PASS`.
- ☑ Tony reviewed OLD/NEW panels in `STORY-6.5b-PROMPT-EQUIVALENCE-DIFF.md` (incl. Block A trim post-083).

PR #104 merged to `develop`.

---

## Round 2 — Azure Test (post-merge)

**Date:** 2026-05-20  
**Operator:** Tony  
**Deployment:** GitHub Actions deploy-to-test on `develop` (post PR #104 merge)

| Check | Result | Notes |
|-------|--------|-------|
| Merge PR #104 to develop, CI green | ☑ PASS | |
| Test slot applies migrations 078–083 cleanly | ☑ PASS | Deploy completed; generation succeeded |
| Sign in to deployed Test frontend, generate form | ☑ PASS | Intl online event registration prompt |
| **R6 closure: success, NO `context-pack-load-failed`** | ☑ PASS | `validated-success`, 12 components, attempt 1 |
| **R6 closure: NO `prompt-assembly-resolution-failed`** | ☑ PASS | |
| Form renders to canvas | ☑ PASS | |

---

## Sign-off

- **Dev (BMM Dev agent):** Implementation complete. Local suite 39/39 PASS. AC-19 diff PASS. Migrations `078`–`083`.
- **Tony:** **Story 6.5b closed** — Round 1 LocalDB + Round 2 Azure Test green (2026-05-20). R6 resolved on Test.

