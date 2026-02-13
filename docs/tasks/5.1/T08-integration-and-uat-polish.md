# Task T08: Integration + UAT Polish

**Story:** 5.1 - Background Asset Management  
**Task ID:** T08  
**Status:** 🔄 In Progress  
**Dependencies:** T03-T07  
**Estimated Time:** 2-3 hours  

---

## 📋 Task Overview

**Objective:** Validate end-to-end asset flow, run automated checks, and prep UAT evidence.

---

## ✅ Scope (In)

- [ ] Run relevant automated checks (frontend lint/build; backend smoke tests if touched)
- [ ] Validate builder + renderer parity
- [ ] Update UAT guide with evidence notes if needed

---

## 🚫 Scope (Out)

- ❌ New feature work (handled in earlier tasks)

---

## ✅ Acceptance Criteria

- Automated checks captured with pass/fail evidence
- UAT guide ready for human execution
- No open blockers on integration path

---

## 🧪 Required Tests / Verification

- Frontend (if touched):
  - `npm run lint`
  - `npm run build`
- Backend (if touched):
  - `python -m compileall backend`

---

## 🌿 Git / PR Requirements (Mandatory)

- Create branch: `task/5.1/T08-integration-and-uat-polish`
- Open PR: `task/5.1/...` → `story/epic5-5.1-background-asset-management`

```powershell
scripts/git/new-task.ps1 -StoryBranch "story/epic5-5.1-background-asset-management" -StoryId 5.1 -TaskId T08 -Slug "integration-and-uat-polish" -CreateWorktree
```

---

## 📚 References

- UAT Guide: `docs/stories/STORY-5.1-UAT-TEST-GUIDE.md`

