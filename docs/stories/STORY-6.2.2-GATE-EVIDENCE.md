# Story 6.2.2 — Gate Evidence (Automated)

- **Recorded:** 2026-03-31  
- **Repository / worktree:** `C:\wt\elp\story-epic6-6.2.2-file-upload-full-stack`

| Command | Working directory | Exit | Summary | Status |
|--------|-------------------|------|---------|--------|
| `npm run lint` | `...\frontend` | 0 | eslint `--max-warnings 0`, no issues | **PASS** |
| `npm run test:unit -- --watch=false` | `...\frontend` | 0 | 25 test files, 237 tests | **PASS** |
| `python -m pytest tests/test_story_622_file_upload.py --tb=short` | `...\backend` | 0 | 6 passed (integration DB) | **PASS** (dev machine) |

---

## `npm run lint`

- **Working dir:** `C:\wt\elp\story-epic6-6.2.2-file-upload-full-stack\frontend`  
- **Exit code:** 0  
- **Observed:** ESLint completed with `--max-warnings 0`.  
- **Run context:** 2026-03-31 (automated gate run).

---

## `npm run test:unit -- --watch=false`

- **Working dir:** `C:\wt\elp\story-epic6-6.2.2-file-upload-full-stack\frontend`  
- **Exit code:** 0  
- **Final summary:** Test Files 25 passed (25), Tests 237 passed (237), ~11s (Vitest).  
- **Run context:** 2026-03-31.

---

## `python -m pytest tests/test_story_622_file_upload.py --tb=short`

- **Working dir:** `C:\wt\elp\story-epic6-6.2.2-file-upload-full-stack\backend`  
- **Prerequisites:** `DATABASE_URL` consistent with project test DB; **Alembic revision 051** applied so `SubmissionAttachment` exists (SQL Server: `dbo.SubmissionAttachment`).  
- **Exit code:** 0  
- **Final summary (expected):** 6 passed — modules exercised:
  - `test_story_622_form_validate_accepts_file_upload`
  - `test_story_622_upload_submit_bind_and_download`
  - `test_story_622_reject_cross_session_attachment`
  - `test_story_622_dedupe_same_session_same_hash`
  - `test_story_622_reject_fake_attachment_id_on_submit`
  - `test_story_622_download_404_unknown_attachment`

**Subset log (2026-03-31, developer machine):**  
`python -m pytest tests/test_story_622_file_upload.py -v -k "reject_fake or reject_cross"` → **2 passed**, 4 deselected; HTTP logs show `422` on invalid submit as expected.

**Note:** Environments that only load SQLite fixtures with SQL Server–specific SQL may error during DB setup (`getutcdate()`). Use the same **MSSQL + migrated** setup used for the rest of the integration suite.

---

## Optional — full backend regression

On merge / CI, run the full backend suite per team policy, for example:

```powershell
cd C:\wt\elp\story-epic6-6.2.2-file-upload-full-stack\backend
python -m pytest --tb=short
```

Record exit code and the final “X passed” line in this file or CI artifacts.
