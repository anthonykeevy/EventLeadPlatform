# Story 3.8: Public Form Renderer

**Epic:** 3 - Form Builder & Logic Engine  
**Domain:** Rendering & Submission  
**Status:** ✅ Complete (UAT Passed)  
**Priority:** High  

---

## 📖 User Story

**As a** Form Respondent (Event Attendee),  
**I want to** open a public form link and complete the form exactly as it was authored,  
**So that** I can submit accurate lead details quickly on the intended device/profile.

**Context & Entry Point:**  
- Story 3.7 is complete: runtime rule evaluation exists and can drive `visible/enabled/required` during entry.
- A published form version exists in `FormVersion.DefinitionJSON` (validated by backend).
- An internal parity renderer exists (`/forms/:formId/render`) but is explicitly noted as minimal and **not** the final public renderer.
- ✅ **UAT prerequisite resolved:** Story 3.9 is complete (Builder persistence + Preview token flow), enabling end-to-end renderer UAT from stored `DefinitionJSON`.

---

## 🧭 Scope Boundary (CRITICAL)

**In scope (Story 3.8):**
- A **public renderer view** that loads and renders a form **from stored `FormVersion.DefinitionJSON`**.
- Rendering includes:
  - Theme + global styles
  - Canvas/profile dimensions and absolute positioning (design fidelity)
  - Pages + components
- **Uses the same Component Registry as the Builder** (no duplicated component type switch logic).
- Runtime effects from Story 3.7 are applied live during entry:
  - `visible` (show/hide)
  - `enabled` (enable/disable)
  - `required` (require/unrequire)
- Client-side data entry UX:
  - Field state management (values map)
  - Required-field validation and **validation message area** for fields
  - A “Submit” interaction that performs client-side validation and produces a submission payload in memory
- Safe behavior:
  - Unknown component `type` or malformed component config must render a fallback UI and **must not crash**.
- **Design fidelity rule (critical):** The renderer must render at the **authored canvas/device profile** dimensions and layout. It must not “auto reflow” into a different layout.

**Out of scope (Story 3.8):**
- Submission transport and async pipeline (Outbox/Queue/Sync) — **Story 3.11**.
- Server-side submission validation/processing.
- Responsive redesign/reflow of authored layouts.
- Multi-profile rendering from a single definition. If a customer needs Desktop + Tablet variants, they create **separate designs/profiles**.

---

## 🎯 Functional Requirements (High Level)

### 1) Public route/view loads `DefinitionJSON`
- Provide a public-facing route/view that:
  - Fetches the active/published form definition (DefinitionJSON) and parses it.
  - Shows a loading state.
  - Shows a non-crashing error state if:
    - The form is not found
    - No published version exists
    - JSON is malformed

### 2) Canvas/profile fidelity (no responsive reflow)
- Render the form inside a fixed “artboard” matching the authored profile:
  - Use `definition.canvasSettings.width/height` (or equivalent stored canvas dimensions) as the authoritative size.
  - Render components with absolute positions from the definition.
- The renderer may scale-to-fit the viewport for usability, but:
  - Internal coordinate system and layout must remain authored (no reflow).
  - Scaling must be visual-only (content should not change layout).

### 3) Registry-driven component rendering (shared with Builder)
- Rendering must use the existing Component Registry as the source of truth for:
  - Component type lookup
  - The runtime render implementation per type
- The renderer must not implement a second “type switch” that duplicates component rendering logic.
- Unknown component types must render a stable fallback component:
  - Shows “Unsupported component type: <type>”
  - Reserves a reasonable visual box so the layout does not collapse

### 4) Runtime logic integration (Story 3.7)
- Rule outputs must apply during entry, identical to Builder Preview parity:
  - Hidden components are not rendered and removed from tab order.
  - Disabled components display as disabled and do not accept input.
  - Required components show required indicator and participate in validation.

### 5) Data entry UX + client-side validation (transport deferred)
- Maintain a values map keyed by `FormComponent.id`.
- Provide a validation mode (e.g., when user clicks Submit):
  - Required validation for currently visible required components.
  - Display errors in the validation message area.
- The submit action for Story 3.8:
  - Must **not** send network requests for submission.
  - Must produce a submission payload (e.g., `{ formId, formVersionId?, submittedAtClient, answersByComponentId }`) in memory and show a UI confirmation that submission handling is deferred to Story 3.11.

### 6) Safety and resilience
- Malformed component props/config must not crash the renderer.
- Missing/malformed layout data should degrade gracefully (e.g., default position to (0,0), display a warning block, continue rendering).

---

## ✅ Acceptance Criteria

### 1) Public renderer loads and renders from stored DefinitionJSON
- [x] Given an active/published form version, the renderer view fetches and renders the form from `FormVersion.DefinitionJSON`.
- [x] Loading and error states render correctly (no white screen / crash).

### 2) Canvas/profile fidelity
- [x] The rendered form matches the authored canvas size (from `canvasSettings`) and component absolute positions.
- [x] The renderer does not reflow the layout into another profile/device size.

### 3) Shared Component Registry
- [x] Rendering uses the existing Component Registry as the source of truth for component type → runtime component mapping.
- [x] There is no duplicated renderer-specific “switch(type)” mapping for known components.

### 4) Runtime logic parity (Story 3.7)
- [x] `show/hide` affects visibility live as values change.
- [x] `enable/disable` affects interactivity live as values change.
- [x] `require/unrequire` affects required indicator and validation live as values change.

### 5) Unknown/malformed component safety
- [x] Unknown component types render a fallback UI and do not crash the page.
- [x] Malformed config does not crash; a fallback UI is shown and other components still render.

### 6) Client-side validation UX present (no transport)
- [x] Clicking Submit runs required validation for visible required fields.
- [x] Validation messages appear in the field validation area.
- [x] Submission transport/outbox is not implemented; renderer shows a clear “deferred to Story 3.11” confirmation.

---

## 🛠️ Technical Notes (Guidance)

### Known starting point (from Story 3.7)
- Current internal parity renderer route: `/forms/:formId/render`.
- Current internal runtime view: `frontend/src/features/builder/components/runtime/RuntimeFormView.tsx`.
- Current Component Registry: `frontend/src/features/builder/registry/ComponentRegistry.tsx`.

### Recommended direction for Story 3.8
- Refactor runtime rendering so the registry can provide runtime renderers (not only preview metadata).
- Keep **one** runtime rendering pipeline shared by:
  - Builder preview runtime
  - Public renderer runtime
- Add a resilient “UnknownComponentFallback” that can render for any unknown `type`.

### Backend/API note (minimal contract)
- The renderer must be able to retrieve the active/published version definition.
- If no unauthenticated endpoint exists, add a minimal public endpoint (token-protected or `IsPublic`-gated) that returns the published `DefinitionJSON`.

---

## 📋 Dependencies

- Story 3.7: Rule Evaluation Engine (`frontend/src/features/logic-engine/*`)
- Component Registry (Builder): `frontend/src/features/builder/registry/ComponentRegistry.tsx`
- Form definition contract + canvas settings: `frontend/src/features/builder/types/builder.types.ts`
- Backend schema validation: `backend/schemas/form_definition.py`
- FormVersion access/publish: `backend/modules/forms/version_service.py` and `backend/modules/forms/version_router.py`

---

## 📚 Related Documentation

- `docs/stories/EPIC-3-ARCHITECTURE-REF.md`
- `docs/stories/story-3.7.md`
- `docs/stories/story-context-3.7.xml`
- `docs/stories/EPIC-3-STATUS.md`

---

## 🧪 UAT Test Guide (COMPLETED)

**Guide:** `docs/stories/STORY-3.8-3.9-UAT-TEST-GUIDE.md`  
**Result:** ✅ PASSED (Scenarios 5–31)

**Key evidence (selected scenarios):**
- ✅ **Render from stored `DefinitionJSON` (happy path):** Scenario 5
- ✅ **Canvas/profile fidelity (artboard sizing) + no responsive reflow:** Scenarios 6–7
- ✅ **Unknown/malformed component fallback (non-crashing):** Scenarios 8–9
- ✅ **Runtime logic parity (show/hide, enable/disable, require/unrequire):** Scenarios 10–12
- ✅ **Submit UX is client-side only (no transport):** Scenario 15
- ✅ **Builder vs Preview WYSIWYG (programmatic):** Scenario 24 (see `docs/WYSIWYG-COMPARISON-RESULTS.md`)

---

## 📋 Completion Criteria

- [x] All Acceptance Criteria are completed.
- [x] UAT Test Guide section above is completed and tests pass.
- [x] No known console errors introduced during UAT scenarios.

---

## ✅ Completion Report

**Completed:** 2026-02-02  
**UAT:** ✅ Passed (see `docs/stories/STORY-3.8-3.9-UAT-TEST-GUIDE.md`)

### What was delivered
- Public renderer loads and renders from stored `FormVersion.DefinitionJSON` (token-based public flow), with safe loading/error states.
- Fixed artboard rendering at authored canvas dimensions (no responsive reflow; scale-to-fit is visual-only).
- Shared Component Registry runtime rendering (no duplicated renderer-only type switch).
- Runtime logic parity with Story 3.7 (`show/hide`, `enable/disable`, `require/unrequire`) including correct tab-order removal for hidden fields.
- Safety fallbacks for unknown component types and malformed configs (non-crashing).
- Client-side validation + Submit produces an in-memory payload; submission transport remains out of scope (**Story 3.11**).

### UAT blockers resolved
- Story 3.9 (Builder persistence + Preview token flow) unblocked end-to-end renderer verification from stored definitions.

### Residual issues / deferred (non-blocking)
- Access control UX gaps (VIEW users / dashboard vs direct URL / view-only mode) are deferred to the Unified Form Workspace specification (`docs/stories/UNIFIED-FORM-WORKSPACE-SPECIFICATION.md`). Security behavior was verified (403/404 show dedicated error pages).
- Submit Button `buttonWidth` / `buttonAlign` has a failed retest (2026-01-26). Not blocking core renderer, but should be addressed.
- Divider drag preview is cosmetic and deferred.
- Header/Paragraph components are not in the toolbox yet (deferred).
