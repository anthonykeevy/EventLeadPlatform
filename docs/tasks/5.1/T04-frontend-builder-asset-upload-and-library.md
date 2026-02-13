# Task T04: Frontend Builder Asset Upload + Library + Reference Wiring

**Story:** 5.1 - Background Asset Management  
**Task ID:** T04  
**Status:** ✅ HumanDone
**Dependencies:** T01, T03  
**Estimated Time:** 3-5 hours  

---

## ðŸ“‹ Task Overview

**Objective:** Implement builder UX for background asset upload, selection, and reference storage in the form definition.

---

## âœ… Scope (In)

- [ ] Upload background image via asset API
- [ ] Display asset library/picker for background images
- [ ] Store asset references (no Data URLs) in `DefinitionJSON`
- [ ] Show clear errors for limit violations

---

## ðŸš« Scope (Out)

- âŒ Renderer parity wiring (T05)
- âŒ Placement intersection rule (T06)

---

## ðŸ”’ Forbidden Zones

| Path | Reason |
|------|--------|
| `backend/` | Frontend-only task |

---

## âœ… Acceptance Criteria

- Builder stores only asset references in `DefinitionJSON`
- Upload + picker flow works end-to-end with backend API
- Limits are surfaced clearly to users

---

## ðŸ§ª Required Tests / Verification

- `npm run lint` (if frontend touched)
- `npm run build` (if frontend touched)

---

## ðŸ” Out-of-Scope Handling

If asked to:
- Implement renderer parity â†’ route to **T05**
- Implement placement/cropping â†’ route to **T06**

---

## ðŸŒ¿ Git / PR Requirements (Mandatory)

- Create branch: `task/5.1/T04-frontend-builder-asset-upload-and-library`
- Open PR: `task/5.1/...` â†’ `story/epic5-5.1-background-asset-management`

```powershell
scripts/git/new-task.ps1 -StoryBranch "story/epic5-5.1-background-asset-management" -StoryId 5.1 -TaskId T04 -Slug "frontend-builder-asset-upload-and-library" -CreateWorktree
```

---

## ðŸ“š References

- Story: `docs/stories/story-5.1.md`


