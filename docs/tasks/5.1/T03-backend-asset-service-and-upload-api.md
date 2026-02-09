# Task T03: Backend Asset Service + Upload API

**Story:** 5.1 - Background Asset Management  
**Task ID:** T03  
**Status:** ⏸️ Pending  
**Dependencies:** T02  
**Estimated Time:** 2-3 hours  

---

## 📋 Task Overview

**Objective:** Implement backend asset storage service, upload endpoints, and runtime URL resolution.

---

## ✅ Scope (In)

- [ ] Storage provider abstraction (Local dev + Azure Blob via config)
- [ ] Asset upload endpoint for background images
- [ ] Asset retrieval URL resolver (no absolute URLs persisted)
- [ ] Enforce config-backed limits (bytes/dimensions/mime)
- [ ] Dedup by hash and soft-delete support

---

## 🚫 Scope (Out)

- ❌ Builder UI wiring (T04)
- ❌ Renderer/builder parity integration (T05)

---

## 🔒 Forbidden Zones

| Path | Reason |
|------|--------|
| `frontend/` | Backend-only task |

---

## ✅ Acceptance Criteria

- Backend can store an asset and return metadata + reference
- Upload limits enforced via `config.AppSetting`
- Runtime resolver returns correct URLs without storing absolute hosts
- Dedup by hash prevents duplicate asset records

---

## 🧪 Required Tests / Verification

- Backend endpoint responds to valid upload
- Oversized/invalid mime uploads rejected with clear errors

---

## 🔁 Out-of-Scope Handling

If asked to:
- Modify builder UI → route to **T04**
- Implement placement logic → route to **T06**

---

## 🌿 Git / PR Requirements (Mandatory)

- Create branch: `task/5.1/T03-backend-asset-service-and-upload-api`
- Open PR: `task/5.1/...` → `story/epic5-5.1-background-asset-management`

```powershell
scripts/git/new-task.ps1 -StoryBranch "story/epic5-5.1-background-asset-management" -StoryId 5.1 -TaskId T03 -Slug "backend-asset-service-and-upload-api" -CreateWorktree
```

---

## 📚 References

- Story: `docs/stories/story-5.1.md`

