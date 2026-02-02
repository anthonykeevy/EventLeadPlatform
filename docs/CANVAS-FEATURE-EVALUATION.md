# Canvas/BuilderMode Feature Evaluation (Component vs Object vs Sub-control)

**Purpose:** Identify features currently controlled by *canvas/builderMode* checks (or surface gates) and decide the correct attachment level so the framework remains scalable for a future “component builder tool”.

This document complements `docs/COMPONENT-FRAMEWORK-REFERENCE.md` by focusing on **where a capability attaches**:

- **Component-level**: affects the whole component wrapper (SmartBorder, drag/resize constraints, component resize handles).
- **Object-level**: attaches to a top-level object in the structure (`label`, `input`, `validation`, `divider`, `custom`).
- **Sub-control-level**: attaches to internal controls rendered *inside* an object renderer (e.g. dropdown option “extra text” inputs). These are **not** top-level objects.

## Evaluation Matrix

| Feature (today) | How it is currently controlled | Recommended attachment level | Benefit of changing (or not) | Notes / risks |
|---|---|---|---|---|
| TextLengthIndicator (bar + label + textarea line badge) | Implemented inside `createInputRenderer` and gated by `getComponentSurfaceCapabilities(type, surface).textLengthIndicator` | **Object-level feature/decorator** on the `input` object | Removes renderer special-casing and makes the capability assignable per object | Must honor `showBar/showLabel/showTextareaLineEstimate` and use DOM measurement (not `props.width`) |
| Selection “extra text” sub-input + its TextLengthIndicator (dropdown/checkbox/radio) | Implemented inside selection input renderer; indicator gated by `surface === 'canvas'` and `surfaceCaps.textLengthIndicator.enabled` | **Sub-control-level feature/decorator** (inside `input` renderer) | Keeps the structure contract (single `input` object) while reusing the same overlay logic | Config comes from `options[].hasExtraText` + validation source; do not create new top-level objects |
| Dropdown sizing guide (“longest-option”) | `componentSurfaceCapabilities.dropdown.displayMode` and dropdown renderer logic | **Surface policy** (stay component+surface mapped) | Correctly models a surface-only rendering decision | Orthogonal to object decorators; may still use shared measurement hook |
| Validation placeholder rendering in builder mode | Today still has a heuristic fallback: `builderMode ?? (!error && ...)` in the validation renderer | **Surface policy** (explicitly surface-driven) | Eliminates heuristic drift between different builder entry points | Must preserve “no empty bordered box in runtime when no message” contract |
| Input-only width resize handle (green handle) | Canvas-only via `componentSurfaceCapabilities.objectResizeHandles.inputWidthHandle` | **Object-level capability** (keep) | Already object-scoped; aligns with per-object interactions | Can be expressed as metadata on the `input` object (“inputWidthResizable”) |
| SmartBorder (collision bounds + selection outline) | Enabled in builder/canvas mode; disabled in runtime | **Component-level builder chrome** (keep) | Defines the component’s boundary/collision model; not an object concern | Divider needs fill-width mode in some contexts |
| Component resize handles (NWSE + edges) | Canvas-only UI | **Component-level builder chrome** (keep) | Operates on component props/position, not individual objects | Object-only handles remain separate |
| Drag constraints + resize constraints (collision/bounds) | Canvas-only constraints via surface capabilities | **Component-level surface policy** (keep) | Keeps geometry policies centralized and consistent across drag/resize/panel edits | Must remain stable frame-to-frame |
| Submit button runtime status (spinner) | Runtime-only via `submitButton.showStatus` caps; structure uses a `status` object with conditional | **Object-level conditional rendering** (already good) | Already follows “structure + conditionals” framework model | Toolbox/canvas should continue to suppress runtime-only status |

## Conclusion

- **Surface mapping is necessary but not sufficient** for scalability: it answers “where does it behave differently?”.
- To be “assignable to any component or object”, a capability also needs an **attachment level**: component-level vs object-level vs sub-control-level.
- The most impactful improvements for long-term scalability are:
  - Move “visual overlays” like TextLengthIndicator into an **object feature/decorator pipeline**.
  - Remove heuristic builder detection and rely on explicit `surface` / surface capabilities.

