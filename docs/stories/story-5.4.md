# Story 5.4: Shared Resolver Parity

**Epic:** Epic 5 - Form Builder Readiness + Review & Publishing  
**Domain:** Form Builder + Public Renderer integration  
**Status:** Complete (UAT passed; merge pending)
**Priority:** High (preview/production parity)  
**Created:** 2026-02-16  
**Owner:** Developer Agent  

---

## 📖 User Story

**As a** platform maintainer,  
**I want** a single resolver for defaults and assets used by builder preview, public renderer, and (future) admin review,  
**So that** preview and production render identically and we avoid drift between code paths.

**Context & entry point:**  
- Stories 5.1, 5.2, and 5.3 are complete: assets, company defaults, Form Builder Init API, schema validation.  
- Today: **defaults resolution** exists in two places—backend `resolve_definition_for_render` (Python) and frontend `resolveDefinitionForRender` (TypeScript). Public form uses backend; builder preview uses frontend. Parity is assumed but not verified.  
- **Asset resolution** is shared via `useBackgroundImageUrl` and `backgroundAssetResolver`; both builder preview and PublicFormArtboard use them.  
- **"Review and Publish"** (admin) flow does not exist yet (Story 5.6); this story ensures the resolver infrastructure is ready.

---

## 🧭 Scope Boundary

### In scope (Story 5.4)

- **Defaults resolution parity**
  - Verify backend (Python) and frontend (TypeScript) merge logic produce identical output for theme, globalStyles, canvasSettings given same inputs.
  - Add parity tests (fixtures: merged defaults + form overrides → compare outputs).
  - Fix any drift; document merge algorithm in one place (`docs/stories/STORY-5.4-RESOLUTION-RULES.md`).
- **Asset resolution consistency**
  - Audit: builder preview and public renderer use `useBackgroundImageUrl` / `getBackgroundImageSource` for backgrounds.
  - Ensure no divergent code paths; document asset resolution rules in the same doc.
- **Prepare for Review and Publish**
  - Document that future admin "Review and Publish" UI (Story 5.6) must use the same resolver—either backend `resolve_definition_for_render` (e.g. via preview token) or verified frontend parity.
  - No new "Review" UI in this story; prep only.

### Out of scope (Story 5.4)

- Preview vs production mode toggle (Story 5.5).
- Publish request workflow (Story 5.6).
- Changing Init API or Form Builder save flow.
- Anonymous asset access for public forms (if required later, separate story).

---

## 🎯 Done Criteria

- [x] **DC1:** Backend and frontend defaults resolution produce identical theme, globalStyles, canvasSettings for the same inputs (parity tests pass).
- [x] **DC2:** Parity tests added in `backend/tests/` (or equivalent) using shared fixtures.
- [x] **DC3:** `docs/stories/STORY-5.4-RESOLUTION-RULES.md` documents merge algorithm and asset resolution rules.
- [x] **DC4:** Builder preview and public renderer use the same asset resolution path (`useBackgroundImageUrl` / `getBackgroundImageSource`); audit confirms no divergence.
- [x] **DC5:** Future Review and Publish integration documented (resolver contract for Story 5.6).
- [x] **DC6:** UAT guide executed and marked PASSED.
- [ ] **DC7:** Story PR merged to `master`.

---

## 📐 Current Resolution Paths (Reference)

| Surface         | Defaults source           | Merge logic                  | Asset resolution       |
|-----------------|---------------------------|-----------------------------|------------------------|
| Builder preview  | Init API (Global+Company)  | `resolveDefinitionForRender`| `useBackgroundImageUrl`|
| Public renderer | Backend API (pre-resolved) | N/A (backend does it)        | `useBackgroundImageUrl`|
| FormRendererPage| Init API + formDefinition | `resolveDefinitionForRender`| shared                 |

Backend: `modules/form_defaults/service.py` — `resolve_definition_for_render`, `resolve_merged_defaults`, `deep_merge`.  
Frontend: `definitionResolver.ts` — `resolveDefinitionForRender`, `deepMerge`.  
Assets: `backgroundAssetResolver.ts` — `getBackgroundImageSource`, `resolveAssetContentUrl`; `useBackgroundImageUrl.ts`.

---

## 📚 References

- Epic scope: `docs/stories/EPIC-5-STATUS.md`
- Story 5.2 resolver: `backend/modules/form_defaults/service.py`, `frontend/.../definitionResolver.ts`
- Story 5.1 assets: `frontend/.../backgroundAssetResolver.ts`, `useBackgroundImageUrl.ts`
- Form Builder Init API: `docs/stories/STORY-5.2-FORM-BUILDER-INIT-API.md`
- Git workflow: `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`

---

*Story 5.4 - Shared Resolver Parity*  
*Last Updated: 2026-02-16*
