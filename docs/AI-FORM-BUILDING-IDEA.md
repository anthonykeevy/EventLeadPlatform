# AI-Assisted Form Building — Backlog Idea

**Status:** Backlog — consider after Epic 5 completes  
**Created:** 2026-02-18  
**Source:** PM assessment (platform readiness review)

---

## 1. Concept

**Hypothesis:** We can assign initial form *building* to an AI agent; the user still uses the Form Builder to make adjustments.

- **DefinitionJSON** is well-structured and suitable for AI generation.
- With clear guidance, an agent can produce valid DefinitionJSON from a natural-language prompt.
- The Form Builder validates the response and provides feedback (especially collision/boundary feedback) so the agent knows what to fix.
- User loads the AI-generated form into the Form Builder for refinement.

---

## 2. PM Readiness Assessment

**Verdict:** Platform is **ready** with focused preparation. Most building blocks exist; gaps are wiring and guidance.

### What We Have

| Capability | Evidence |
|------------|----------|
| **Structured DefinitionJSON** | Pydantic schema (`backend/schemas/form_definition.py`); `FormDefinition`, `FormComponent`, `FormPage`, etc. |
| **Schema API for AI** | `GET /api/form-schema/1.0` returns JSON Schema from DB — AI can fetch structure and constraints at init. |
| **Component type taxonomy** | `ComponentType` enum; documented types in `COMPONENT-FRAMEWORK-REFERENCE.md`. |
| **Dimension estimates without DOM** | `getComponentDimensions(component, null, scale)` in `collisionDetection.ts` — uses `heightEstimates` by type, `props.width`. |
| **Collision logic** | `boxesOverlap`, `checkCanvasBoundary`, `checkCollision` — rules for overlaps and canvas limits. |
| **Documentation** | `DEFINITIONJSON-SAVE-CHECKLIST`, `COMPONENT-FRAMEWORK-REFERENCE`, `COMPONENT-CATALOG-SCHEMA-DESIGN`. |

### Gaps (To Build)

| Gap | Description |
|-----|-------------|
| **Static collision validator** | Pure JSON validator: takes DefinitionJSON, computes collisions from `position` + estimated dimensions (no rendering). Returns machine-readable feedback for AI iteration. |
| **AI prompt pack** | Single "AI Form Builder Prompt" document: DefinitionJSON structure, component types/props, canvas coords, collision rules, dimension estimates, unique ID rules. |
| **Feedback loop contract** | Iteration protocol: prompt → AI generates DefinitionJSON → validate (schema + static collision) → return feedback → AI fixes → repeat until valid. |
| **Builder integration** | Option to load AI-generated DefinitionJSON into Form Builder; optionally surface validation warnings in canvas. |

---

## 3. Collision Boundary Feedback for AI

Current collision utilities expose the right concepts:

- `checkCanvasBoundary` → `{ isOutOfBounds, constrainedPosition, violations: { left, right, top, bottom } }`
- `checkCollision` → `{ hasCollision, collidingComponents }` (with IDs)
- `ConstraintResult` → `reason: 'collision' | 'boundary' | 'no-solution'`, `collidingComponentIds`

**Needed:** An API/validator that:

1. Accepts DefinitionJSON as input
2. Runs schema validation
3. Runs static collision + boundary checks (reuse `getComponentDimensions` fallback logic)
4. Returns unified response the agent can parse and act on

**Example feedback format:**

```json
{
  "valid": false,
  "schemaErrors": [...],
  "collisions": [
    { "componentId": "field-1", "collidingWith": ["field-2"], "overlapArea": 1200 }
  ],
  "boundaryViolations": [
    { "componentId": "field-3", "violations": { "right": true } }
  ]
}
```

---

## 4. Suggested Phased Roadmap

| Phase | Scope | Effort |
|-------|--------|--------|
| **Phase 1: Static validator** | Add `POST /api/form-validate` (or similar): accepts DefinitionJSON, runs schema + collision/boundary checks, returns structured feedback. | Low |
| **Phase 2: AI prompt pack** | Produce "AI Form Builder Prompt" document from existing docs + JSON Schema. | Low |
| **Phase 3: Agent loop** | Wire prompt pack into agent; implement retry loop using validation feedback. | Medium |
| **Phase 4: Builder integration** | Option to load AI-generated DefinitionJSON into Form Builder; surface validation warnings in canvas. | Medium |

---

## 5. References

- `docs/COMPONENT-FRAMEWORK-REFERENCE.md` — component framework, collision detection
- `docs/DEFINITIONJSON-SAVE-CHECKLIST.md` — save checklist, component props
- `docs/stories/COMPONENT-CATALOG-SCHEMA-DESIGN.md` — component catalog design
- `backend/schemas/form_definition.py` — Pydantic validation
- `frontend/src/features/builder/utils/collisionDetection.ts` — dimension estimates, `checkCanvasBoundary`, `checkCollision`
- `GET /api/form-schema/1.0` — JSON Schema for DefinitionJSON

---

*Backlog idea — discuss prioritisation after Epic 5 completion*
