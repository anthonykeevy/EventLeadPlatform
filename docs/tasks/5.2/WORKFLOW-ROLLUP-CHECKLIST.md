# Workflow Rollup Checklist — Story 5.2 + Lint

**Generated:** 2026-02-16 (PM audit)  
**Purpose:** Ensure nothing is left behind before merging to master  

---

## ✅ Pre-Merge Audit Summary

| Item | Status |
|------|--------|
| T08 merged to story branch | ✅ Yes (PR #40) |
| Story branch has all T08 docs | ✅ spec, uat, uat-results, completion, retro |
| Story branch STATUS | ✅ T01–T08 Done |
| chore/lint-resolution on master | ✅ Already merged (b51d2d9) |
| Story 5.2 PR to master | 📋 PR #32 (DRAFT) — ready to merge |

---

## 🔧 1. Fix Story Worktree (Avoid Losing Work)

The **story worktree** (`C:\wt\elp\story-epic5-5.2-company-form-defaults`) has **stale local changes**:
- Modified: `STATUS.md`, `T07-builder-defaults-new-form-save-company.md`, `TASK-PLAN.md`
- Untracked: `T08-integration-uat.md`, `T08-integration-uat.uat.md`

**These are superseded by the T08 merge.** Origin already has the correct content. To sync:

```powershell
cd "C:\wt\elp\story-epic5-5.2-company-form-defaults"
git checkout -- docs/tasks/5.2/STATUS.md docs/tasks/5.2/T07-builder-defaults-new-form-save-company.md docs/tasks/5.2/TASK-PLAN.md
git pull origin story/epic5-5.2-company-form-defaults
# Optional: remove duplicate untracked T08 docs if desired
# git clean -n docs/tasks/5.2/T08-integration-uat.md docs/tasks/5.2/T08-integration-uat.uat.md
```

---

## 📋 2. Story 5.2 Finalization (Before Merge)

Add closeout doc and optional DC8 doc updates to story branch:

```powershell
cd "C:\wt\elp\story-epic5-5.2-company-form-defaults"
git add docs/stories/STORY-5.2-CLOSEOUT.md
# Optional: update story-5.2.md DC8 checkbox, EPIC-5-STATUS
git commit -m "docs(5.2): Story closeout, ready for merge to master"
git push origin story/epic5-5.2-company-form-defaults
```

---

## 🚀 3. Merge Story 5.2 to Master

1. **Option A — Merge master into story first** (recommended if story diverged early):
   ```powershell
   cd "C:\wt\elp\story-epic5-5.2-company-form-defaults"
   git merge origin/master
   # Resolve any conflicts; commit
   git push origin story/epic5-5.2-company-form-defaults
   ```

2. **Convert draft PR to ready** (GitHub): Open PR #32, click "Ready for review".

3. **Merge PR:**
   ```powershell
   gh pr merge 32 --squash
   ```
   Or use GitHub UI: Merge pull request (squash and merge).

---

## ⚠️ 4. Lint Branch — Already on Master

**chore/lint-resolution is already merged to master** (commit b51d2d9). No further lint rollup needed.

The **main project** (`EventLeadPlatform` on `chore/lint-resolution`) has **uncommitted changes**:
- Modified: docs, builder components, vite.config, etc.
- Untracked: T01–T07 task docs, formDefaultsApi, formBuilderInitApi, t05-impl.patch

**Action:** Review whether these are:
- **Stale copies** (story branch has canonical versions) → safe to `git checkout -- .` and `git clean -fd`
- **New work** never committed → commit to a branch and open PR before discarding

---

## 📊 5. Post-Merge

1. Update `docs/stories/EPIC-5-STATUS.md` — mark Story 5.2 complete.
2. Delete obsolete worktrees if desired: `git worktree list` then `git worktree remove <path>`.
3. Update `docs/stories/EPIC-5-WORKFLOW-GUIDE.md` — Story 5.2 status complete.

---

*PM workflow audit 2026-02-16*
