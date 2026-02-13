# Task T01: Asset Contracts + Config Foundations

**Story:** 5.1 - Background Asset Management  
**Task ID:** T01  
**Status:** ⏳ Ready  
**Dependencies:** None  
**Estimated Time:** 2-3 hours  

---

## 📋 Task Overview

**Objective:** Lock down the contracts and configuration primitives before any storage or UI work:
- Asset metadata shape (backend + frontend)
- Background placement metadata shape
- Config-backed limits (keys + default behavior)
- Shared resolver interface contract (no implementation yet)

This task must be runnable in isolation and must not require DB migrations or new endpoints.

---

## ✅ Scope (In)

- [ ] Define **asset metadata contract** (backend schema + frontend type)
- [ ] Define **background placement contract** (positioning + sizing + crop metadata)
- [ ] Define **resolver interface contract** (input asset reference → runtime URL)
- [ ] Define **config key list** for limits in `config.AppSetting`
- [ ] Document **Data URL guard** expectations (where/when to validate)

---

## 🚫 Scope (Out)

- ❌ No DB migrations (T02)
- ❌ No backend API routes (T03)
- ❌ No UI changes or builder wiring (T04+)
- ❌ No storage provider implementation (T03)

---

## 🔒 Forbidden Zones

| Path | Reason |
|------|--------|
| `backend/migrations/` | Migration work is isolated to T02 |
| `frontend/src/features/auth/` | No auth changes |

---

## ✅ Acceptance Criteria

### AC1: Asset metadata contract exists (FE + BE)
- **Criterion:** A single asset metadata shape exists in TypeScript and backend schema.
- **Verification:** Shapes match field-for-field and are documented in code comments.

### AC2: Placement contract is defined
- **Criterion:** Background placement metadata covers position, size, and crop.
- **Verification:** Type is referenced by the background definition and resolver contract.

### AC3: Config keys are documented
- **Criterion:** Limit keys are specified and match the Epic 5 scope.
- **Verification:** Keys documented and referenced in code or task notes.

### AC4: Resolver contract is defined
- **Criterion:** A clear interface exists for resolving asset references to URLs.
- **Verification:** Interface can be implemented without changing the definition schema.

---

## 🔧 Implementation Details (Concrete)

Suggested config keys (draft):
- `forms.assets.images.max_upload_bytes`
- `forms.assets.images.max_width_px`
- `forms.assets.images.max_height_px`
- `forms.assets.images.allowed_mime_types` (JSON array)

Suggested TypeScript types (example names):
- `BackgroundAssetRef`
- `BackgroundPlacement`
- `BackgroundAssetMetadata`
- `BackgroundAssetResolver`

Suggested backend schema:
- `backend/modules/assets/asset_schemas.py` (Pydantic models)

---

## 🧪 Required Tests / Verification

- None (contracts only)
- Ensure TypeScript builds if types are introduced in shared modules

---

## 🔁 Out-of-Scope Handling

If asked to:
- Create DB tables → route to **T02**
- Implement upload/download API → route to **T03**
- Modify builder UI → route to **T04**

---

## 🌿 Git / PR Requirements (Mandatory)

- Create branch: `task/5.1/T01-asset-contracts-and-config-foundations`
- Open PR: `task/5.1/...` → `story/epic5-5.1-background-asset-management`

Recommended (PowerShell):

```powershell
scripts/git/new-task.ps1 -StoryBranch "story/epic5-5.1-background-asset-management" -StoryId 5.1 -TaskId T01 -Slug "asset-contracts-and-config-foundations" -CreateWorktree
```

---

## 📤 Handoff Requirements

After completion, provide:
1. List of files created/modified
2. Config key list confirmed
3. Resolver contract documented

---

## 📚 References

- Story: `docs/stories/story-5.1.md`
- Context: `docs/stories/story-context-5.1.xml`
- Git workflow: `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`

---

*Task spec created using Epic 5 workflow guide*  
