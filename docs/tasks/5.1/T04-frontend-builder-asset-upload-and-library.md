# Task T04: Frontend Builder Asset Upload + Library + Reference Wiring

**Story:** 5.1 - Background Asset Management  
**Task ID:** T04  
**Status:** ⏳ Ready  
**Dependencies:** T01, T03  
**Estimated Time:** 3-5 hours  

---

## 📋 Task Overview

**Objective:** Implement builder UX for background asset upload, selection, and reference storage in the form definition.

---

## ✅ Scope (In)

- [ ] Upload background image via asset API
- [ ] Display asset library/picker for background images
- [ ] Store asset references (no Data URLs) in `DefinitionJSON`
- [ ] Show clear errors for limit violations

---

## 🚫 Scope (Out)

- ❌ Renderer parity wiring (T05)
- ❌ Placement intersection rule (T06)

---

## 🔒 Forbidden Zones

| Path | Reason |
|------|--------|
| `backend/` | Frontend-only task |

---

## ✅ Acceptance Criteria

- Builder stores only asset references in `DefinitionJSON`
- Upload + picker flow works end-to-end with backend API
- Limits are surfaced clearly to users

---

## 🧪 Required Tests / Verification

- `npm run lint` (if frontend touched)
- `npm run build` (if frontend touched)

---

## 🔁 Out-of-Scope Handling

If asked to:
- Implement renderer parity → route to **T05**
- Implement placement/cropping → route to **T06**

---

## 🌿 Git / PR Requirements (Mandatory)

- Create branch: `task/5.1/T04-frontend-builder-asset-upload-and-library`
- Open PR: `task/5.1/...` → `story/epic5-5.1-background-asset-management`

```powershell
scripts/git/new-task.ps1 -StoryBranch "story/epic5-5.1-background-asset-management" -StoryId 5.1 -TaskId T04 -Slug "frontend-builder-asset-upload-and-library" -CreateWorktree
```

---

## 📚 References

- Story: `docs/stories/story-5.1.md`

