# Task T06: Placement + Intersection Rule + Cropping

**Story:** 5.1 - Background Asset Management  
**Task ID:** T06  
**Status:** ✅ Complete (2026-02-11)  
**Dependencies:** T04, T05  
**Estimated Time:** 2-3 hours  

---

## 📋 Task Overview

**Objective:** Implement background placement metadata, cropping behavior, and the off-canvas intersection rule.

---

## ✅ Scope (In)

- [ ] Store placement in canvas coordinates (support negative offsets)
- [ ] Apply cropping based on placement metadata
- [ ] If fully off-canvas, auto-remove background from the canvas

---

## 🚫 Scope (Out)

- ❌ Asset storage changes (T03)
- ❌ Data URL guard (T07)

---

## ✅ Acceptance Criteria

- Background placement is persisted and applied correctly
- Fully off-canvas backgrounds are removed from canvas
- Asset remains in the library after auto-removal

---

## 🧪 Required Tests / Verification

- Manual: move background off-canvas → it disappears from canvas but stays in library

---

## 🌿 Git / PR Requirements (Mandatory)

- Create branch: `task/5.1/T06-placement-intersection-and-cropping`
- Open PR: `task/5.1/...` → `story/epic5-5.1-background-asset-management`

```powershell
scripts/git/new-task.ps1 -StoryBranch "story/epic5-5.1-background-asset-management" -StoryId 5.1 -TaskId T06 -Slug "placement-intersection-and-cropping" -CreateWorktree
```

---

## 📚 References

- Story: `docs/stories/story-5.1.md`

