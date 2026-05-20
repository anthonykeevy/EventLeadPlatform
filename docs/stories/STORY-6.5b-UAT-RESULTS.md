# Story 6.5b — UAT Results (template; Tony fills as he runs)

**Branch:** `story/epic6-6.5b-registry-foundation`  
**PR:** [#104](https://github.com/SignalPlatforms/EventLeadPlatform/pull/104)  
**Test environment:** LocalDB first (iteration), then Azure Test slot for R6 verification.

Use this file as the running record while executing the procedure in `STORY-6.5b-MIGRATION-HANDOFF.md`. Each round below is templated; copy-paste a new round if anything fails and a re-run is needed.

---

## Round 1 — LocalDB

**Date:** _YYYY-MM-DD_  
**Operator:** Tony  
**alembic head before:** _e.g. `074`_  
**alembic head after:** _expected `082`_

### A. Migration execution

```powershell
cd backend
alembic current
alembic upgrade head
alembic current
```

| Migration | Result | Notes |
|-----------|--------|-------|
| 078 schema | ☐ PASS / ☐ FAIL | |
| 079 profile + sections | ☐ PASS / ☐ FAIL | |
| 080 A/B/C/I variants | ☐ PASS / ☐ FAIL | |
| 081 Block G context pack | ☐ PASS / ☐ FAIL | |
| 082 GenerationRun audit columns | ☐ PASS / ☐ FAIL | |

### B. Verification SELECTs (from migration handoff doc § 2)

| Check | Result | Notes |
|-------|--------|-------|
| `FORM_AI_V1` registry row exists, IsActive=1 | ☐ PASS / ☐ FAIL | |
| Active `PromptAssemblyRegistryVersion` exists with VersionNumber=1 | ☐ PASS / ☐ FAIL | |
| 5 PromptSection rows in SortOrder (A, B, I, G, C) | ☐ PASS / ☐ FAIL | |
| 7 variants seeded (A=1, B=1, C=4, I=1) with `local` IsDefault=1 | ☐ PASS / ☐ FAIL | |
| Block G variant exists, snippet len 6800–7400 chars | ☐ PASS / ☐ FAIL | actual len: ___ |
| Block G snippet does NOT contain "## Operational Notes" trim marker | ☐ PASS / ☐ FAIL | |
| `dbo.GenerationRun` has `PromptAssemblyRegistryVersionID BIGINT NULL` and `PromptVariantSnapshot NVARCHAR(MAX) NULL` | ☐ PASS / ☐ FAIL | |

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
| uvicorn boots without `context-pack-load-failed` in startup | ☐ PASS / ☐ FAIL | |
| Sign in to frontend, open AI Agent panel | ☐ PASS / ☐ FAIL | |
| Submit prompt: "Build a contact form for a Sydney tech conference." | ☐ PASS / ☐ FAIL | RequestID: ___ |
| Form successfully renders to canvas | ☐ PASS / ☐ FAIL | |
| AI panel terminal trace contains NO `context-pack-load-failed` | ☐ PASS / ☐ FAIL | |
| AI panel terminal trace contains NO `prompt-assembly-resolution-failed` | ☐ PASS / ☐ FAIL | |

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
| Most recent GenerationRun has `PromptAssemblyRegistryVersionID` populated (NOT NULL) | ☐ PASS / ☐ FAIL | observed value: ___ |
| `PromptVariantSnapshot` is valid JSON containing keys A/B/C/G/I | ☐ PASS / ☐ FAIL | |
| Variant IDs in snapshot match `config.PromptSectionVariant` rows | ☐ PASS / ☐ FAIL | |

### E. AC-19 sign-off

Open `STORY-6.5b-PROMPT-EQUIVALENCE-DIFF.md` and:

- ☐ All five blocks (A, B, C, G, I) report `IDENTICAL` for every of the four postures.
- ☐ Top-level verdict is `PASS`.
- ☐ Commit SHA in the diff matches the PR's HEAD when reviewed (regenerate via `python backend/scripts/story_6_5b_prompt_equivalence_diff.py` if it drifts).

If all three boxes are ticked: `gh pr ready 104` to flip Draft → Ready.

---

## Round 2 — Azure Test (post-merge)

**Date:** _YYYY-MM-DD_  
**Deployment workflow:** _.github workflow run id ___

| Check | Result | Notes |
|-------|--------|-------|
| Merge PR #104 to develop, CI green | ☐ PASS / ☐ FAIL | |
| Test slot startup logs apply migrations 078–082 cleanly (no failures) | ☐ PASS / ☐ FAIL | |
| `https://signalplatforms-test.azurewebsites.net/api/health` returns 200 | ☐ PASS / ☐ FAIL | |
| Sign in to deployed frontend, generate AU form | ☐ PASS / ☐ FAIL | RequestID: ___ |
| **R6 closure: response is success and contains NO `context-pack-load-failed`** | ☐ PASS / ☐ FAIL | |
| `dbo.GenerationRun.PromptAssemblyRegistryVersionID` populated on Test DB | ☐ PASS / ☐ FAIL | |

If all checks pass: flip `EPIC-6-STATUS.md` row 6.5b to ✅ Complete and close the R6 entry.

---

## Sign-off

- **Dev (BMM Dev agent):** Implementation complete (commit `e1d9fbb` + uncommitted dev work — see Section 8 of GATE-EVIDENCE for inventory). Local 6.5b test suite 39/39 PASS. Equivalence diff PASS. Ready for Tony's UAT.
- **Tony:** _Sign here when Round 1 + Round 2 both green._

