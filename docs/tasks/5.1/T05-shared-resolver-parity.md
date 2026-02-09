# Task T05: Shared Resolver Parity (Builder + Renderer)

**Story:** 5.1 - Background Asset Management  
**Task ID:** T05  
**Status:** ⏸️ Pending  
**Dependencies:** T03, T04  
**Estimated Time:** 2-3 hours  

---

## 📋 Task Overview

**Objective:** Ensure builder preview and public renderer resolve background assets using the same rules and resolver logic.

---

## ✅ Scope (In)

- [ ] Implement shared resolver module for asset references
- [ ] Use the resolver in builder preview and public renderer
- [ ] Ensure runtime URL generation matches backend contract

---

## 🚫 Scope (Out)

- ❌ Placement/cropping logic (T06)
- ❌ Data URL guard (T07)

---

## ✅ Acceptance Criteria

- Builder preview and renderer display the same background asset
- Resolver logic is centralized (no duplicated resolver code)

---

## 🧪 Required Tests / Verification

- Verify builder preview + public renderer show identical background

---

## 🌿 Git / PR Requirements (Mandatory)

- Create branch: `task/5.1/T05-shared-resolver-parity`
- Open PR: `task/5.1/...` → `story/epic5-5.1-background-asset-management`

```powershell
scripts/git/new-task.ps1 -StoryBranch "story/epic5-5.1-background-asset-management" -StoryId 5.1 -TaskId T05 -Slug "shared-resolver-parity" -CreateWorktree
```

---

## 📚 References

- Story: `docs/stories/story-5.1.md`

