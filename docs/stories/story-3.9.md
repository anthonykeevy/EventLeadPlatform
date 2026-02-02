# Story 3.9: Builder Persistence (Save/Load FormVersion)

**Epic:** 3 - Form Builder & Logic Engine  
**Domain:** Visual Builder (Persistence Bridge)  
**Status:** 🛠️ Next (Ready for Development)  
**Priority:** High  

---

## 📖 User Story

**As a** Form Builder User (Company Admin / Form Designer),  
**I want to** save and reload my authored form definition to/from the database,  
**So that** the public renderer and token-based previews can be tested and used end-to-end using stored `FormVersion.DefinitionJSON`.

---

## 🧭 Scope Boundary (CRITICAL)

**In scope (Story 3.9):**
- **Load-from-DB:** Opening the Form Builder loads the latest stored definition for that form from the backend (not a fixed mock template).
- **Save Draft:** The Builder can persist the current in-memory `FormDefinition` into `FormVersion.DefinitionJSON` as a **DRAFT** version.
- **Schema validation:** Saved definitions must pass backend schema validation (`backend/schemas/form_definition.py`) or fail with a safe error state.
- **Preview uses public token flow:** Builder “Preview” generates a **PREVIEW** token and opens `/forms/:token` so preview is rendered from stored definition.
- **Source of truth clarified:** The database (FormVersion) is the authoritative source for renderer and preview links.

**Out of scope (Story 3.9):**
- Submission pipeline/outbox/sync (this becomes **Story 3.10**).
- Lead creation, attribution, or persistence of responses.
- Advanced collaboration features (multi-user locking, conflict resolution).
- Auto-save/offline queue for drafts (can be added later if required).

---

## 🎯 Functional Requirements (High Level)

### 1) Builder loads the latest saved definition
- When user navigates to `/forms/:formId/builder`, the app must fetch a definition from the backend:
  - Prefer “latest DRAFT” if that concept exists, otherwise use the latest version number.
  - If no versions exist, show a clear empty-state and allow creating the first draft.
- The builder must no longer always start from the same mock 3-field template for every form.

### 2) Save Draft writes `DefinitionJSON` to FormVersion
- A Save Draft action writes the current `formDefinition` to the backend as `DefinitionJSON`.
- Save Draft must:
  - create a new version or update a draft version (implementation choice), but must be deterministic and user-friendly
  - surface backend validation errors without crashing
  - confirm success in UI

### 3) Preview uses the same public renderer flow as production
- Builder Preview must create a PREVIEW token via:
  - `POST /api/forms/{formId}/public-links` with `linkType=PREVIEW`
- Builder Preview opens `/forms/:token`
- Renderer resolves PREVIEW token to the latest version (draft or published) so designers can validate rules/layout without publishing.

### 4) Safety and resilience
- If the backend is unavailable, show a non-crashing error and preserve the in-memory builder state.
- Validation failures must not corrupt local in-memory state.

---

## ✅ Acceptance Criteria

### Load-from-DB
- [ ] Opening the builder loads the latest saved definition from the backend (no fixed mock template by default).
- [ ] If no saved versions exist, a safe empty-state is shown (no crash).

### Save Draft
- [ ] Save Draft persists the current form definition to `FormVersion.DefinitionJSON`.
- [ ] Backend validation errors are shown to the user and do not crash the UI.

### Preview token flow
- [ ] Builder Preview creates a PREVIEW token and opens `/forms/:token`.
- [ ] Public renderer loads from stored DefinitionJSON associated with that token.

---

## 🧪 UAT Test Guide (PLACEHOLDER)

**Planned (to be authored/approved):** `docs/stories/STORY-3.9-UAT-TEST-GUIDE.md`

---

## 📋 Completion Criteria

- [ ] All Acceptance Criteria are completed.
- [ ] UAT Test Guide section above is completed and tests pass.
- [ ] Story 3.8 can now be executed end-to-end and finalized using stored `DefinitionJSON`.

---

## ✅ Completion Report (PLACEHOLDER)

**Completed:** TBD  
**UAT:** TBD  

### What was delivered
- TBD

---

## 🧩 Retro / Process Note (for Epic Retrospective)

**Why this story exists (discovered during Story 3.8):**
- The backend versioning architecture (Story 3.1) exists, but the **Form Builder frontend** was still initializing from a **mock template/localStorage** and the **Save** UX was not wired to persist `FormDefinition` into `FormVersion.DefinitionJSON`.
- This created an **integration gap**: Story 3.8’s public renderer depends on stored `FormVersion.DefinitionJSON`, so Story 3.8 could not be UAT’d end-to-end using normal UI flows.

**Process improvements (actionable):**
- Add a “UAT Readiness Gate” before development starts: verify the UAT prerequisites can be produced via UI/API flows (not manual DB edits).
- Track “source-of-truth” explicitly per domain: when renderer depends on DB, builder must have a DB persistence story before renderer UAT.

