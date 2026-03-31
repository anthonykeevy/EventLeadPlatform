# Story 6.2.2 — Single-Session Dev Prompt

**Story:** 6.2.2 — File Upload Component (Full Stack)  
**Agent:** `@bmad-agent-bmm-dev`  
**Worktree:** `C:\wt\elp\story-epic6-6.2.2-file-upload-full-stack`  
**Branch:** `story/epic6-6.2.2-file-upload-full-stack`  
**PR:** #55 (Draft)

---

## Execution contract

You are the Dev agent. Implement the full story in `docs/stories/story-6.2.2.md` using `docs/stories/story-context-6.2.2.xml` as the implementation map. Follow **Green CI/CD** rules in `docs/stories/EPIC-6-WORKFLOW-GUIDE.md`. Do **not** claim complete until evidence exists.

---

## Step 0 — Preflight

```powershell
.\scripts\workflow\preflight-story.ps1 `
  -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.2.2-file-upload-full-stack" `
  -ExpectedBranch "story/epic6-6.2.2-file-upload-full-stack" `
  -ReportFile "docs/stories/STORY-6.2.2-PREFLIGHT.md"
```

---

## Step 1 — Read sources

1. `docs/stories/story-6.2.2.md`  
2. `docs/stories/story-context-6.2.2.xml`  
3. `docs/COMPONENT-FRAMEWORK-GUIDE.md`  
4. `backend/modules/forms/public_form_router.py` + `public_submission_schemas.py`  
5. `backend/models/form_submission.py`

---

## Step 2 — Database (Anthony executes Alembic)

1. Confirm current head: from `backend/`, `alembic heads` (human may run).  
2. Add migration creating **`dbo.SubmissionAttachment`** (or agreed name) with FKs to `FormPublicLink`, nullable FK to `FormSubmission`, indexes for lookup by public id and by submission.  
3. **Do not** run `alembic upgrade` in agent automation. At closeout, print exact commands for Anthony, e.g.:

```text
cd backend
alembic upgrade head
```

---

## Step 3 — Backend implementation order (suggested)

1. Model + migration file (include **Sha256**, **StorageProvider**, **StorageKey**; optional session columns for §2.4.1 dedupe).  
2. Storage: **reuse** `modules/assets/storage.py` (`load_storage_config`, `get_storage_provider`) with submission-specific **storage keys** — do **not** use `dbo.Asset` for public uploads.  
3. `POST` multipart upload endpoint: resolve token → link → enforce size/MIME → write file → insert row with `FormSubmissionID NULL` + `PublicAttachmentId`.  
4. Submission path: parse file-upload answers; verify each id belongs to this link + session rule from story; on commit set `FormSubmissionID`.  
5. Authenticated download endpoint with company ACL.  
6. Tests: `test_story_622_*` covering validate, upload, submit bind, cross-submission rejection, download auth.

---

## Step 4 — Frontend

1. Types + registry + structureDefaults + preview + `FileUploadPropertiesSection`.  
2. Runtime: upload before submit; map answers; handle errors.  
3. Unit tests if Vitest patterns exist for API layer.

---

## Step 5 — Docs

- `COMPONENT-FRAMEWORK-GUIDE.md` inventory.  
- `STORY-6.2-AI-CONTEXT-PACK.md` — file-upload **available** with constraints.

---

## Step 6 — Green gates + evidence

```powershell
.\scripts\workflow\run-green-gate.ps1 `
  -StoryId "6.2.2" `
  -FocusedTestCommand "python -m pytest tests/test_story_622_file_upload.py --tb=short" `
  -BackendGateCommand "python -m pytest --tb=short" `
  -EvidenceFile "docs/stories/STORY-6.2.2-GATE-EVIDENCE.md"
```

Frontend (from `frontend/`):

```powershell
npm run lint
npm run test:unit -- --watch=false
```

Mirror summaries into `STORY-6.2.2-UAT-RESULTS.md` (automation section).

---

## Step 7 — Closeout

1. `STORY-6.2.2-CLOSEOUT-REPORT.md`  
2. Update `story-6.2.2.md` Dev Agent Record + status when ready for UAT  
3. Push branch; ensure Draft PR #55 description lists UAT + migration commands

---

## Forbidden

- Alembic upgrade/downgrade/revision **execution** by agent  
- Storing absolute server paths in client-visible JSON  
- Serving files without ACL check
