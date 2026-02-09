# Task T07: Data URL Guard + Cleanup

**Story:** 5.1 - Background Asset Management  
**Task ID:** T07  
**Status:** ⏸️ Pending  
**Dependencies:** T04  
**Estimated Time:** 1-2 hours  

---

## 📋 Task Overview

**Objective:** Prevent Data URL backgrounds from entering definitions and clean up any legacy paths.

---

## ✅ Scope (In)

- [ ] Detect and block Data URL backgrounds in builder input
- [ ] Strip/normalize any Data URL background found in definition load path
- [ ] Surface clear user-facing error messages

---

## 🚫 Scope (Out)

- ❌ Storage provider work (T03)
- ❌ Placement/cropping work (T06)

---

## ✅ Acceptance Criteria

- Data URL backgrounds are rejected or stripped with clear errors
- No base64 blobs remain in `DefinitionJSON` after save

---

## 🧪 Required Tests / Verification

- Attempt to inject Data URL background → blocked/stripped
- Definition save contains asset references only

---

## 🌿 Git / PR Requirements (Mandatory)

- Create branch: `task/5.1/T07-data-url-guard-and-cleanup`
- Open PR: `task/5.1/...` → `story/epic5-5.1-background-asset-management`

```powershell
scripts/git/new-task.ps1 -StoryBranch "story/epic5-5.1-background-asset-management" -StoryId 5.1 -TaskId T07 -Slug "data-url-guard-and-cleanup" -CreateWorktree
```

---

## 📚 References

- Story: `docs/stories/story-5.1.md`

