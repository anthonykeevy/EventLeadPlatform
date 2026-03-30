# Component Framework Reference

**Purpose:** Comprehensive reference for the EventLead Form Builder component framework, including component definitions, properties, resize behavior, and state management.

**Design objective:** The component framework was designed with the objective to **move defaults to the database**. Frontend structures (globalStyles, theme, defaultGridLayoutsByComponent, etc.) were built to validate the data shape; the intent is to drive these from Global → Company → Form defaults in the database. A **Component Catalog** (multi-country, multi-company) will deliver components + schemas per form context. See [Inheritance Model & Data Defaults](#-inheritance-model--data-defaults-for-components) below, `docs/stories/STORY-5.2-DATA-SCHEMA.md`, and `docs/stories/COMPONENT-CATALOG-SCHEMA-DESIGN.md`.

> **Quick Reference:** [Component Framework Guide](./COMPONENT-FRAMEWORK-GUIDE.md) - Concise implementation guide for agents (read this first for any component work).

## 🧭 Quick Start (Agents & Developers)

This document is intended to be a **single source of truth** for how components behave across **toolbox / canvas / runtime**, and for how to extend the builder without creating one-off “special cases”.

### Core mental model

- **Global-first**: Users set defaults in `FormDefinition.globalStyles`, then apply smaller per-component overrides via `component.props.styleOverrides` and other `component.props.*` properties.
- **Three surfaces**:
  - **toolbox**: compact, non-interactive preview card
  - **canvas**: builder WYSIWYG (SmartBorder, resize handles, design-time guides)
  - **runtime**: public preview / production renderer (no builder chrome)
- **UniversalFieldShell is the “layout engine”**: it renders a component’s objects (`label`/`input`/`validation`/`action`/`divider`/etc.), applies object layout, and is the integration point for SmartBorder on canvas.
- **Object-Centric Design**: Components are composed of objects (Label, Input, Action, Validation, Divider) with individual sizing and styling. The framework applies universally to **ALL components**; only the target object type differs:
  - **Buttons**: `action` object (id: 'button')
  - **Input components**: `input` object
  - **Dividers**: `divider` object
  - **Labels**: `label` object (rarely resized directly)
- **Capabilities are declarative**:
  - `componentCapabilities.ts`: “does this component support a feature at all?”
  - `componentSurfaceCapabilities.ts`: “how does this feature behave on each surface?”
- **Capabilities impose constraints**: Component capabilities (collision detection, canvas boundaries, etc.) apply their rules and restrictions to limit achievable widths/heights. These constraints must be considered in all width calculations.

### Golden rules (reliability)

- **No ad-hoc margins/padding in object renderers**: do not “fix spacing” with random `mt-*`, `mb-*`, or inline `marginTop` hacks. Those break row alignment and create component-by-component drift.
- **All builder-only visuals must be surface-gated**: TextLengthIndicator, sizing guides, debug overlays must not appear in runtime unless explicitly allowed by `componentSurfaceCapabilities`.
- **Keep top-level structures small**: prefer canonical objects (`label`, `input`, `validation`) and render complex internal layouts *inside* the `input` object (e.g. selection + extra text).
- **Surface Style Parity**: The same property values must render identically on Toolbox, Canvas, and Runtime. Use the unified style resolution pipeline for all surfaces.
- **Object-Level Control**: Each object (Label, Input, Validation) has its own sizing and style properties. Component-level properties affect the container; object-level properties affect individual objects.

### Where to look (file map)

- **Structures**: `frontend/src/features/builder/registry/ComponentRegistry.tsx`
- **Layout + SmartBorder integration**: `frontend/src/features/builder/components/UniversalFieldShell.tsx`
- **Object renderers**: `frontend/src/features/builder/utils/objectRenderers.tsx`
- **Spacing math**: `frontend/src/features/builder/utils/spacingCalculation.ts`
- **Surface gates**: `frontend/src/features/builder/utils/componentSurfaceCapabilities.ts`
- **Feature gates**: `frontend/src/features/builder/utils/componentCapabilities.ts`
- **Collision solver**: `frontend/src/features/builder/utils/collisionDetection.ts`
- **Resize handles**: `frontend/src/features/builder/components/ui/ResizeHandles.tsx`
- **Resize logic + preview**: `frontend/src/features/builder/components/SortableComponent.tsx`
- **Resize hook (centralized logic)**: `frontend/src/features/builder/hooks/useComponentResize.ts`
- **SmartBorder (visual boundary)**: `frontend/src/features/builder/components/ui/SmartBorder.tsx`
- **Component snapshot (DOM metrics)**: `frontend/src/features/builder/utils/componentSnapshot.ts`

### Debug workflow (fast)

- **Step 1**: Identify the surface (`toolbox` vs `canvas` vs `runtime`).
- **Step 2**: Identify the layer (styles vs spacing vs layout vs constraints).
- **Step 3**: Confirm the feature is allowed on that surface (`componentSurfaceCapabilities`).
- **Step 4**: Confirm the component isn’t using ad-hoc margins/padding that bypass the layout engine.

## 📏 Spacing Model (Framework Contract)

Spacing is the most common source of “this component feels different” bugs. The framework uses **three spacing layers**. When debugging, always identify **which layer** is responsible.

### Layer 1: Inside-control padding (“input feel”)

- **What it is**: the padding inside inputs/selects/textareas (how far text is from the border), plus the input’s height.
- **Where it comes from**: `GlobalStyles.inputPaddingX`, `GlobalStyles.inputPaddingY`, `GlobalStyles.inputHeight`, `GlobalStyles.borderWidth`.
- **Where it’s applied**: computed input styles (via `computeFieldStyles` / `useComponentStyles`).
- **Symptoms when wrong**:
  - text looks vertically off-center
  - text truncates when height is reduced (height + padding conflict)

### Layer 2: Between object categories (Label ↔ Input ↔ Validation)

- **What it is**: the gap between the primary objects (label to input, input to validation/help).
- **Where it comes from**:
  - global defaults: `GlobalStyles.labelGap`, `GlobalStyles.inputHelpGap` (multipliers of `baseSpacing`)
  - resize overrides (px): `component.props.labelGapOverride`, `component.props.inputHelpGapOverride`
- **Where it’s applied**: UniversalFieldShell spacing + computed styles.
- **Symptoms when wrong**:
  - label feels “too far” from input everywhere
  - resizing height changes gaps unexpectedly (because overrides are being previewed)

### Layer 3: Object Layout gaps (rows/columns inside `ObjectLayout`)

- **What it is**: gaps between objects when objects are in the same row (`horizontalGap`) or when rows stack (`verticalSpacing`).
- **Where it comes from**:
  - per-component override: `component.props.objectSpacing` (today)
  - fallback: `GlobalStyles.baseSpacing` (today)
- **Where it’s applied**: `calculateSpacing(...)` / `calculateRowSpacing(...)` and `UniversalFieldShell` group styles.
- **Symptoms when wrong**:
  - objects in the same row look “squished” or “too spread out”
  - mixed layouts don’t feel consistent between components

### Debug checklist (spacing)

- **If text is clipped / vertically off**: check Layer 1 (`inputHeight` vs `inputPaddingY`).
- **If label/input/help spacing is inconsistent**: check Layer 2 (`labelGap`, `inputHelpGap`, overrides).
- **If objects in the same row are spaced oddly**: check Layer 3 (`objectSpacing.horizontalGap`, `objectSpacing.verticalSpacing`).

### Agent guidance: how to build components without spacing drift

- **Do not** add per-object margin hacks in renderers (`mt-1`, `marginTop: 6`, etc.).
- **Do** rely on:
  - `UniversalFieldShell` layout + spacing
  - `rowAlignment` for vertical alignment inside a row
  - `objectSpacing` for layout-engine gaps (not per-object tweaks)
- **Compound inputs** (dropdown + extra text, selection lists, etc.) should implement their internal spacing using a stable layout (prefer CSS grid) *inside* the `input` object renderer, but should still respect the component’s outer width and SmartBorder.

### Global spacing defaults for Object Layout (implemented)

To make spacing easier for non-frontend users and to keep all components consistent, the framework now provides **global defaults for Layer 3 spacing**:

- `GlobalStyles.objectRowGapPx` — default vertical gap between rows (and between objects in vertical layout)
- `GlobalStyles.objectColumnGapPx` — default horizontal gap within a row (and fallback object gap)

**Where applied (code):**

- Spacing fallbacks in `calculateSpacing(...)` / `calculateRowSpacing(...)` now prefer these keys over `baseSpacing`.
- The Global Styles panel exposes both values under **Object Layout**.
- Per-component `component.props.objectSpacing.*` still overrides these defaults when needed, and the component **Spacing** section supports “Reset to global”.

---

## 📐 Architecture Overview

### Current Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Form Definition                                 │
├─────────────────────────────────────────────────────────────────────────┤
│  globalStyles: GlobalStyles     ← Global default properties             │
│  canvasSettings: CanvasSettings ← Canvas dimensions & grid              │
│  desktopPages?: Page[]           ← Authored desktop pages (preferred)   │
│  pages: Page[]                   ← Legacy authored pages (fallback)    │
│    └── components: FormComponent[] ← Individual components              │
│          ├── position: { x, y }     ← Absolute position on canvas        │
│          ├── props: ComponentProps  ← Component-specific properties      │
│          │    ├── styleOverrides    ← Overrides to global styles         │
│          │    ├── objectLayout      ← Per-instance structure override    │
│          │    └── layoutGroups      ← Per-instance mixed layout groups   │
│          ├── children?: FormComponent[] ← Nested components (containers) │
│          └── structure: ComponentStructure ← Defined in ComponentRegistry│
└─────────────────────────────────────────────────────────────────────────┘
```

> **Authored pages selection contract (implemented):**
> - Prefer `definition.desktopPages` when present/non-empty.
> - Otherwise fall back to `definition.pages`.
> - Builder canvas, builder preview, and public preview/production must all select pages using the same rule to avoid “component exists in preview but not on canvas” discrepancies.

### Future Architecture (Database-Driven)

The framework was designed with the objective to drive defaults from the database. Inheritance model (Story 5.2):

```
┌─────────────────────────────────────────────────────────────────────────┐
│             Inheritance Model: Global → Company → Form → Component       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────┐                                                   │
│  │ Global Defaults   │ ← Database: dbo.GlobalFormDefaults                 │
│  │ (Platform-wide)  │   theme, globalStyles, defaultGridLayoutsByComponent│
│  └────────┬─────────┘   canvasSettings (Story 5.2)                       │
│           ↓ overrides                                                   │
│  ┌──────────────────┐                                                   │
│  │ Company Defaults │ ← Database: dbo.CompanyFormDefaults               │
│  │  (Per Company)   │   Company Settings → Form Branding Defaults       │
│  └────────┬─────────┘                                                   │
│           ↓ overrides                                                   │
│  ┌──────────────────┐                                                   │
│  │ Form Overrides   │ ← FormVersion.DefinitionJSON (theme, globalStyles)│
│  │   (Per Form)     │   User overrides in Global Properties Panel       │
│  └────────┬─────────┘                                                   │
│           ↓ overrides                                                   │
│  ┌──────────────────┐                                                   │
│  │ Component Props  │ ← FormVersion.DefinitionJSON → component.props     │
│  │ (Per Component)  │   styleOverrides, objectLayout, layoutGroups       │
│  └──────────────────┘                                                   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Database Tables (Story 5.2)

| Table | Schema | Purpose |
|-------|--------|---------|
| `ref.FormDefaultsSchemaVersion` | `ref` | Schema versioning for DefaultsJSON evolution |
| `dbo.GlobalFormDefaults` | `dbo` | Platform-wide theme, globalStyles, canvasSettings, defaultGridLayoutsByComponent |
| `dbo.CompanyFormDefaults` | `dbo` | Per-company defaults (versioned + audit trail) |
| `FormVersion.DefinitionJSON` | `dbo` | Form-level overrides + pages + logic |

See `docs/stories/STORY-5.2-DATA-SCHEMA.md`.

### Style Resolution Order

```
1. Global Defaults (database: dbo.GlobalFormDefaults)
       ↓
2. Company Defaults (database: dbo.CompanyFormDefaults)
       ↓
3. Form Overrides (FormVersion.DefinitionJSON.theme, .globalStyles)
       ↓
4. Component Style Overrides (component.props.styleOverrides)
       ↓
5. Component Scale (component.props.componentScale)
       ↓
6. Final Computed Styles
```

---

## 📦 Inheritance Model & Data Defaults for Components

This section documents **what data each tier provides** and **how components consume it**. The resolver merges Global → Company → Form; the component receives the merged result plus its own overrides.

### Data Provided by Each Tier

| Tier | Data keys | Source | What components receive |
|------|-----------|--------|-------------------------|
| **Global** | `theme`, `globalStyles`, `defaultGridLayoutsByComponent`, `canvasSettings` | `dbo.GlobalFormDefaults.DefaultsJSON` | Baseline for all forms in the platform |
| **Company** | Same structure (partial override) | `dbo.CompanyFormDefaults.DefaultsJSON` | Deep-merge over Global; company branding |
| **Form** | `theme`, `globalStyles` (partial), `pages`, `logic`, `canvasSettings` | `FormVersion.DefinitionJSON` | Form-specific overrides; pages + components |
| **Component** | `props.styleOverrides`, `props.objectLayout`, `props.objectSpacing`, etc. | `component.props` within DefinitionJSON | Per-instance overrides |

### How Components Use the Data

| Data category | Consumed by | Resolution path |
|---------------|-------------|-----------------|
| **globalStyles** (typography, spacing, colors) | UniversalFieldShell, objectRenderers, computeFieldStyles, getArchetypeStyle | Merged Global+Company+Form → `getResolvedGlobalStyles(definition)` → component reads resolved object |
| **defaultGridLayoutsByComponent** | UniversalFieldShell, layout engine | By component type; uses `vertical` or `horizontal` per `defaultLayout`/`defaultObjectLayout` |
| **theme** | Action buttons, primary color accents | Merged into resolved styles; `primaryColor`, `fontFamily` etc. |
| **canvasSettings** | Builder canvas (width, height, gridSize) | From definition; global-level baseline |
| **styleOverrides** | Per-component | Applied last; overrides resolved globalStyles for that component |

### Component Resolution Flow (Conceptual)

```
1. Resolver loads Global + Company + Form defaults
2. Deep-merge: Company overrides Global, Form overrides result
3. Component renderer receives: resolvedGlobalStyles + component.props
4. For each object (label, input, validation): 
   - Base style from resolvedGlobalStyles (e.g. labelFontFamily, textColor)
   - Override from component.props.styleOverrides if present
5. For layout: defaultGridLayoutsByComponent[type][vertical|horizontal]
   - Selected by defaultLayout / defaultObjectLayout
   - Per-component objectLayout overrides structure if present
```

### Resolver Implementation (Story 5.2 T06)

Same resolution rules in **Builder preview** and **Public renderer**:

| Context | Resolver | Source |
|---------|----------|--------|
| **Builder preview** (inline / canvas) | `resolveDefinitionForRender(initDefaults, formDefinition)` | Frontend: `frontend/src/features/builder/utils/definitionResolver.ts` |
| **Form Renderer page** (internal runtime) | Same as builder preview | Uses `initDefaults` from Init API |
| **Public form** (GET /api/public/forms/{token}) | `resolve_definition_for_render(db, company_id, version.definition)` | Backend: `backend/modules/form_defaults/service.py` |

Resolution order: **Global → Company → Form → Component**. Form overrides from DefinitionJSON override company defaults. Aligned with `docs/stories/STORY-5.2-DATA-SCHEMA.md`.

### Mapping: Global Properties Panel ↔ Inheritance

The Global Properties Panel controls map to `globalStyles`. When database-driven:

- **Global level:** Set in Administration Settings (Global Defaults screen — backlog)
- **Company level:** Set in Company Settings → Form Branding Defaults
- **Form level:** Set in Builder Global Properties Panel (today); saves to FormVersion.DefinitionJSON
- **Component level:** Set in Component Properties (styleOverrides, objectLayout, etc.)

---

## 🎛️ Global Properties Panel

The Global Properties Panel controls default styling for ALL components. It contains several sections:

### 1. Typography & Spacing Modal

Controls font, border, and spacing properties for **each object category**:

| Property | Applies To | Description |
|----------|------------|-------------|
| `fontFamily` | Label, Input, Help | Font family name |
| `fontSize` | Label, Input, Help | Font size (px) |
| `fontWeight` | Label, Input, Help | Font weight (100-900) |
| `fontStyle` | Label, Input, Help | normal, italic |
| `fontColor` | Label, Input, Help | Text color |
| `backgroundColor` | Label, Input, Help | Background color |
| `hasBorder` | Label, Input, Help | Boolean - show border |
| `borderColor` | Label, Input, Help | Border color |
| `borderWidth` | Label, Input, Help | Border width (px) |
| `borderRadius` | Label, Input, Help | Corner radius (px) |
| `spacing` | Between objects | Gap between object categories |

#### Global Typography & Spacing → `GlobalStyles` Mapping (foundation table)

This table is intentionally **global-only** (no component-specific props). It documents how each Global Properties control maps to `FormDefinition.globalStyles` keys and which object/archetype it affects.

> **Important implementation note (current code):**
> - Label borders are currently driven by `labelBorderColor/labelBorderWidth` (the boolean `labelHasBorder` is **not** enforced).
> - Input “Add Border” is driven by `textBorderColor/textBorderWidth` (the boolean `textHasBorder` is **not** enforced).
> - Help/Validation borders **do** use `helpTextHasBorder` + `helpTextBorderColor/helpTextBorderWidth`.
> - Divider styling is driven by `dividerBorderColor/dividerBorderWidth` (Global “Dividers & Lines”), and can be overridden per-component via `styleOverrides.dividerBorderColor/dividerBorderWidth`.
> - Divider length is driven by `dividerWidth` (Global “Dividers & Lines”), and can be overridden per-divider via `props.width` (Length field in Divider component properties).
> - Validation/help containers reserve `minHeight` for consistent layout, but **do not render border/background** when there is **no message**, to avoid empty “validation boxes” in runtime preview.
> - “IsTransparent” is represented by the background color key being `undefined` (or by using `'transparent'` at render-time).

| Global control (UI) | `GlobalStyles` key(s) | Type | Affects (Object/Archetype) | Current mapping notes |
|---|---|---|---|---|
| Label Text Font | `labelFontFamily` | `string` | `label` / `PrimaryLabel` | Used by `getArchetypeStyle('PrimaryLabel', ...)`. |
| Label Text FontSize | `labelFontSize` | `number` | `label` / `PrimaryLabel` | Scaled by `componentScale`. |
| Label Text FontWeight | `labelFontWeight` | `FontWeightValue` | `label` / `PrimaryLabel` | Scaled by `componentScale` (weight not scaled). |
| Label Text FontStyle | `labelFontStyle` | `'normal' \| 'italic'` | `label` / `PrimaryLabel` | — |
| Label Text FontColour | `labelColor` | `string` | `label` / `PrimaryLabel` | — |
| Label Text BackgroundColour | `labelBackgroundColor` | `string \| undefined` | `label` / `PrimaryLabel` | Rendered as `backgroundColor` (fallback `'transparent'`). |
| Label Text IsTransparent | `labelBackgroundColor` | `boolean (derived)` | `label` / `PrimaryLabel` | `true` when `labelBackgroundColor` is `undefined` (or explicitly `'transparent'`). |
| Label Text IsBorder | `labelHasBorder`, `labelBorderColor`, `labelBorderWidth` | `boolean + fields` | `label` / `PrimaryLabel` | **Not fully enforced**: label border currently appears if `labelBorderColor` is set and `labelBorderWidth > 0`; `labelHasBorder` is not checked in `getArchetypeStyle`. |
| Label Text BorderColour | `labelBorderColor` | `string \| undefined` | `label` / `PrimaryLabel` | Only affects rendering when border condition is met. |
| Label Text BorderWidth | `labelBorderWidth` | `number \| undefined` | `label` / `PrimaryLabel` | Only affects rendering when border condition is met. |
| Label Text BorderRadius | `labelBorderRadius` | `number \| undefined` | `label` / `PrimaryLabel` | Only affects rendering when border condition is met. |
| Label Input Vertical distance | `labelGap` + `baseSpacing` | `number (multiplier + base)` | spacing between label→input | **Single value used for both orientations today** (no separate vertical vs horizontal gap in `GlobalStyles`). |
| Label Input Horizontal distance | `labelGap` + `baseSpacing` | `number (multiplier + base)` | spacing between label→input | Same as above. In mixed/horizontal rows, actual on-canvas “side-by-side gap” can also be influenced by per-component `objectSpacing.horizontalGap`. |
| Input Text Font | `fontFamily` | `string` | `input` / `InputControl` | Used by `getArchetypeStyle('InputControl', ...)` and `computeFieldStyles.inputStyle`. |
| Input Text FontSize | `fontSize` | `number` | `input` / `InputControl` | Scaled by `componentScale`. |
| Input Text FontWeight | `fontWeight` | `FontWeightValue` | `input` / `InputControl` | — |
| Input Text FontStyle | `fontStyle` | `'normal' \| 'italic'` | `input` / `InputControl` | — |
| Input Text FontColour | `textColor` | `string` | `input` / `InputControl` | — |
| Input Text BackgroundColour | `textBackgroundColor` | `string \| undefined` | `input` / `InputControl` | Applied to `computeFieldStyles.inputStyle.backgroundColor`. |
| Input Text IsTransparent | `textBackgroundColor` | `boolean (derived)` | `input` / `InputControl` | `true` when `textBackgroundColor` is `undefined` (or explicitly `'transparent'`). |
| Input Text IsBorder | `textHasBorder`, `textBorderColor`, `textBorderWidth` | `boolean + fields` | `input` / `InputControl` | **Not fully enforced**: border currently appears if `textBorderColor` is set and `textBorderWidth > 0`; `textHasBorder` is not checked in `computeFieldStyles`. |
| Input Text BorderColour | `textBorderColor` | `string \| undefined` | `input` / `InputControl` | Drives the “Input Text Add Border” chrome used by `computeFieldStyles.inputStyle`. |
| Input Text BorderWidth | `textBorderWidth` | `number \| undefined` | `input` / `InputControl` | — |
| Input Text BorderRadius | `textBorderRadius` | `number \| undefined` | `input` / `InputControl` | — |
| Input Validation Vertical distance | `inputHelpGap` + `baseSpacing` | `number (multiplier + base)` | spacing between input→validation/help | Used as `marginTop` on `helpTextStyle` (vertical). |
| Input Validation Horizontal distance | *(not present)* | — | input→validation/help | There is **no global horizontal gap for validation** today. Horizontal placement spacing is controlled by row layout + `objectSpacing.horizontalGap`. |
| Validation Text Font | `helpTextFontFamily` | `string` | `validation` / `HelperText` | Used by `getArchetypeStyle('HelperText', ...)`. |
| Validation Text FontSize | `helpTextFontSize` | `number` | `validation` / `HelperText` | Scaled by `componentScale`. |
| Validation Text FontWeight | `helpTextFontWeight` | `FontWeightValue` | `validation` / `HelperText` | — |
| Validation Text FontStyle | `helpTextFontStyle` | `'normal' \| 'italic'` | `validation` / `HelperText` | — |
| Validation Text FontColour | `helpTextColor` | `string` | `validation` / `HelperText` | Defaults to red; user can change via **Help & Validation** text color. |
| Validation Text BackgroundColour | `helpTextBackgroundColor` | `string \| undefined` | `validation` / `HelperText` | Rendered as `backgroundColor` (fallback `'transparent'`). |
| Validation Text IsTransparent | `helpTextBackgroundColor` | `boolean (derived)` | `validation` / `HelperText` | `true` when `helpTextBackgroundColor` is `undefined` (or explicitly `'transparent'`). |
| Validation Text IsBorder | `helpTextHasBorder` + `helpTextBorder*` | `boolean + fields` | `validation` / `HelperText` | **Enforced** in `getArchetypeStyle('HelperText', ...)`. |
| Validation Text BorderColour | `helpTextBorderColor` | `string \| undefined` | `validation` / `HelperText` | Only affects rendering when `helpTextHasBorder === true`. |
| Validation Text BorderWidth | `helpTextBorderWidth` | `number \| undefined` | `validation` / `HelperText` | Only affects rendering when `helpTextHasBorder === true`. |
| Validation Text BorderRadius | `helpTextBorderRadius` | `number \| undefined` | `validation` / `HelperText` | Only affects rendering when `helpTextHasBorder === true`. |

##### Related “input chrome” global keys (currently not exposed as explicit Typography & Spacing controls)

These are global foundation keys that affect input box sizing/feel and may need dedicated controls:
- `inputHeight` (px) — base input height
- `inputPaddingX`, `inputPaddingY` (multipliers of `baseSpacing`) — internal padding used by `computeFieldStyles`
- `backgroundColor`, `borderColor`, `borderWidth`, `borderRadius`, `placeholderColor`, `primaryColor` — used variably across styled inputs and builder-mode dropdown rendering

### 2. Object Layout Modal

Specifies the layout arrangement for objects within components:

| Property | Type | Description |
|----------|------|-------------|
| `componentObjectLayout` | `'vertical' \| 'horizontal' \| 'mixed'` | Layout for objects within components |
| `componentLayoutGroups` | `Record<string, string[]>` | Groups for mixed layout arrangement |

> **Note:** Properties use "component" prefix, not "default" (e.g., `componentObjectLayout` not `defaultObjectLayout`)

#### Object Layout Modal UI (Enhanced)

The Object Layout modal now supports **three rows** with drag-and-drop for mixed layouts:

```
┌──────────────────────────────────────────────────────────┐
│  Object Layout                                           │
├──────────────────────────────────────────────────────────┤
│  Layout Type: ○ Vertical  ○ Horizontal  ● Mixed          │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Row 1 (Top):     ┌─────────┐                           │
│                   │ [Label] │  ← Drag objects here       │
│                   └─────────┘                           │
│                                                          │
│  Row 2 (Middle):  ┌─────────┐ ┌─────────┐               │
│                   │ [Label] │ │ [Input] │  ← Horizontal  │
│                   └─────────┘ └─────────┘               │
│                                                          │
│  Row 3 (Bottom):  ┌──────────────┐                      │
│                   │ [Validation] │  ← Help can go here   │
│                   └──────────────┘     OR horizontally   │
│                                                          │
│  Available Objects (not placed):                         │
│  ┌──────────┐ ┌────────────┐                            │
│  │ [Object] │ │ [Object]   │  ← Drag to rows above      │
│  └──────────┘ └────────────┘                            │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

#### Help Object Horizontal Placement

**NEW:** Help/Validation objects can now be placed horizontally alongside other objects:

```typescript
// Example: Label and Help on same row (horizontal)
{
    layoutGroups: {
        row1: ['label', 'validation'],  // Help beside Label
        row2: ['input']
    }
}

// Example: Input and Help on same row
{
    layoutGroups: {
        row1: ['label'],
        row2: ['input', 'validation']   // Help beside Input
    }
}

// Example: All objects on one row
{
    layoutGroups: {
        row1: ['label', 'input', 'validation']  // All horizontal
    }
}
```

### 3. ~~Layout (Legacy)~~ - REMOVED

This section has been deprecated and removed.

#### Global Layout (Legacy) → `GlobalStyles` Mapping

“Layout (Legacy)” has now been **removed from the UI**. The `defaultLayout` key may still exist in persisted data for backward compatibility, but new development should use **Object Layout** (`defaultObjectLayout`) instead.

> **Implementation note (current codebase):**
> - New/modern components render through `UniversalFieldShell` on all surfaces.
> - Legacy `FieldShell`-based runtime rendering has been removed from the main component registry; do not add new uses of `FieldShell`.

| Global control (UI) | `GlobalStyles` key(s) | Type | Purpose | Current mapping notes |
|---|---|---|---|---|
| Default Layout (Legacy) | `defaultLayout` | `'vertical' \| 'horizontal'` | Default label/input arrangement for legacy field renderers | **UI removed**. Kept only for backward compatibility with legacy renderers (e.g. `FieldShell`). |

#### Global Object Layout → `GlobalStyles` Mapping

| Global control (UI) | `GlobalStyles` key(s) | Type | Purpose | Current mapping notes |
|---|---|---|---|---|
| Default Object Layout | `defaultObjectLayout` | `ObjectLayoutType` | Default internal object layout (`vertical/horizontal/mixed`) | **Applied** by `UniversalFieldShell` when a component has no `props.objectLayout` override. |
| Default Layout Groups (Mixed) | `defaultLayoutGroups` | `Record<string, string[]> \| undefined` | Default row grouping for mixed layouts | Used as a fallback in `UniversalFieldShell` when a component has no `props.layoutGroups` override. |

---

## 🏷️ Object Categories

Every component has objects that map to one of **three general categories**:

### Category Definitions

| Category | Purpose | Width Calculation | Wrapping |
|----------|---------|-------------------|----------|
| **Label** | Field labels, headers | Based on label text content | ✅ Wraps when narrow |
| **Input** | User input controls | Text length estimator (maxLength + font) | ❌ Does NOT wrap |
| **Help** | Help text, validation messages | Longest validation message width | ✅ Wraps when narrow |

### Object-to-Category Mapping

When a new component is created, each object must be mapped to a category:

```typescript
// Example: Text Input Component
{
  objects: [
    { id: 'label', type: 'label', category: 'Label' },      // → Label category
    { id: 'input', type: 'input', category: 'Input' },      // → Input category
    { id: 'validation', type: 'validation', category: 'Help' }  // → Help category
  ]
}

// Example: Checkbox Component
{
  objects: [
    { id: 'input', type: 'input', category: 'Input' },      // Checkbox itself
    { id: 'label', type: 'label', category: 'Label' },      // Label text
    { id: 'validation', type: 'validation', category: 'Help' }
  ]
}
```

### Category Style Inheritance

Objects inherit their styling from their mapped category in Global Styles:

```
Global Styles (Typography & Spacing)
    ├── Label Category Styles → Applied to all 'Label' objects
    ├── Input Category Styles → Applied to all 'Input' objects
    └── Help Category Styles  → Applied to all 'Help' objects
```

---

## 🎨 Global Styles (GlobalStyles)

Global styles define **default values** for all components, organized by object category.

### Location
- **Type Definition:** `frontend/src/features/builder/types/builder.types.ts`
- **UI Control:** Properties Panel → Global Styles sections
- **Storage:** `FormDefinition.globalStyles`

### Label Category Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `labelFontFamily` | `string` | `'Inter'` | Label font family |
| `labelFontSize` | `number` | `14` | Label font size (px) |
| `labelFontWeight` | `number` | `500` | Label font weight |
| `labelFontStyle` | `string` | `'normal'` | Label font style |
| `labelColor` | `string` | `'#374151'` | Label text color |
| `labelBackgroundColor` | `string` | `'transparent'` | Label background |
| `labelBorderColor` | `string` | `'transparent'` | Label border color |
| `labelBorderWidth` | `number` | `0` | Label border width |
| `labelBorderRadius` | `number` | `0` | Label corner radius |

### Input Category Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `inputFontFamily` | `string` | `'Inter'` | Input font family |
| `inputFontSize` | `number` | `14` | Input font size (px) |
| `inputFontWeight` | `number` | `400` | Input font weight |
| `inputFontStyle` | `string` | `'normal'` | Input font style |
| `textColor` | `string` | `'#111827'` | Input text color |
| `backgroundColor` | `string` | `'#FFFFFF'` | Input background |
| `borderColor` | `string` | `'#D1D5DB'` | Input border color |
| `borderWidth` | `number` | `1` | Input border width (px) |
| `borderRadius` | `number` | `4` | Input corner radius (px) |
| `inputHeight` | `number` | `40` | Input height (px) |
| `inputMinHeight` | `number` | `28` | Minimum input height (px) |
| `inputMaxHeight` | `number` | `240` | Maximum input height (px) |
| `placeholderColor` | `string` | `'#9CA3AF'` | Placeholder text color |
| `focusBorderColor` | `string` | `'#3B82F6'` | Focus border color |

### Help Category Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `helpFontFamily` | `string` | `'Inter'` | Help text font family |
| `helpTextFontSize` | `number` | `12` | Help text font size (px) |
| `helpTextColor` | `string` | `'#DC2626'` | Help/validation text color (default red for visibility) |
| `validationFontSize` | `number` | `12` | Validation message font size (px) |
| `validationColor` | `string` | `'#EF4444'` | Validation error color |
| `helpBackgroundColor` | `string` | `'transparent'` | Label background |
| `helpBorderColor` | `string` | `'transparent'` | Label border color |
| `helpBorderWidth` | `number` | `0` | Label border width |
### Spacing Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `labelGap` | `number` | `8` | Gap between Label and Input (px) |
| `inputHelpGap` | `number` | `8` | Gap between Input and Help (px) |
| `labelGapMin` | `number` | `0` | Minimum label-input gap |
| `labelGapMax` | `number` | `48` | Maximum label-input gap |
| `inputHelpGapMin` | `number` | `0` | Minimum input-help gap |
| `inputHelpGapMax` | `number` | `48` | Maximum input-help gap |

### Layout Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `componentObjectLayout` | `ObjectLayoutType` | `'vertical'` | Object layout within components |
| `componentLayoutGroups` | `Record<string, string[]>` | `undefined` | Layout groups for mixed layout |

---

## 🧩 Component Definition (FormComponent)

Each component on the canvas is a `FormComponent` with these core properties:

### Core Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | `string` | Unique identifier (e.g., `'first-name-abc123'`) |
| `type` | `ComponentType` | Component type (e.g., `'text'`, `'email'`, `'divider'`) |
| `position` | `{ x: number, y: number }` | Absolute position on canvas (px) |
| `props` | `FormComponentProps` | Component-specific properties |
| `style` | `object` | Direct CSS styles (rarely used) |
| `children` | `FormComponent[]` | Nested components (for containers) |

> **Nested rendering parity (implemented):**
> - Public preview/production flattens nested `children` and renders positioned components.
> - Builder canvas also flattens nested `children` (and renders only components with a `position`) so “nested divider in preview but not on canvas” cannot occur.

### Component Props (FormComponentProps)

| Property | Type | Scope | Description |
|----------|------|-------|-------------|
| `label` | `string` | All inputs | Field label text |
| `placeholder` | `string` | Inputs | Placeholder text |
| `required` | `boolean` | Inputs | Is field required |
| `helpText` | `string` | Inputs | Help text below input |
| `validationMessage` | `string` | Inputs | Validation error message |
| `width` | `string` | All | Component width (e.g., `'300px'`) |
| `height` | `number` | Textarea | Textarea height (px) |
| `componentScale` | `number` | All | Proportional scale (50-200%) |
| `objectLayout` | `ObjectLayoutType` | All | Object layout override |
| `layoutGroups` | `Record<string, string[]>` | All | Layout groups for mixed layout |
| `styleOverrides` | `StyleOverrides` | All | Overrides to global styles |
| `labelGapOverride` | `number` | Inputs | Override label-input gap |
| `inputHelpGapOverride` | `number` | Inputs | Override input-help gap |
| `inputHeightOverride` | `number` | Inputs | Override input height |
| `inputWidthMode` | `'auto' \| 'fill'` | Inputs | Input width behavior |
| `labelWidthOverride` | `number` | All | Override label width (px) |
| `validationWidthOverride` | `number` | Inputs | Override validation width (px) |
| `initialVisibility` | `'visible' \| 'hidden'` | All | Initial visibility before logic rules |
| `initialEnabled` | `'enabled' \| 'disabled'` | All | Initial enabled state before logic rules |

---

## 📚 Properties Dictionary by Layer

This section documents **which property names represent intent vs resolved vs rendered values**. Agents should use this to interpret logs correctly.

### Layer Definitions
- **Intent (Props)**: Values set by the Properties Panel or defaults (what the user asked for).
- **Resolved (Computed)**: Values after layout rules are applied (gaps/padding/borders resolved to px).
- **Rendered (DOM)**: Actual browser layout metrics measured from the DOM.
- **Normalized (Canvas px)**: Rendered values mapped to the canvas coordinate system (default canvas is `1920x980`).

### Property Map (Common Width/Spacing)

| Layer | Primary Fields | Meaning |
|------|----------------|---------|
| Intent (Props) | `component.props.width`, `labelWidthOverride`, `inputWidthOverride`, `helpWidthOverride`, `labelGapOverride`, `inputHelpGapOverride`, `objectLayout`, `gridLayout` | Requested sizing/layout values (not guaranteed to match render). |
| Resolved (Computed) | `gridMetrics.containerWidth`, `gridMetrics.columnGapPx`, `gridMetrics.rowGapPx`, `gridMetrics.paddingLeftPx/rightPx`, `gridMetrics.borderLeftPx/rightPx` | Layout engine results in px (should be used for width equations). |
| Rendered (DOM) | `objectMetrics.rect.*`, `bounds.*`, `smartBorderBounds.*` | Actual on-screen widths/positions measured in screen px. |
| Normalized (Canvas px) | `objectMetrics.canvasRect.*`, `canvasBounds.*`, `canvasMetrics.screenToCanvasRatio` | Rendered values mapped to canvas coordinates. |

### Interpretation Rules
- **Do not compare `props.*WidthOverride` directly to `objectMetrics.rect.width`.** Overrides express intent; the layout engine may clamp or redistribute widths.
- **Use `objectMetrics.rect.width` for what the user sees.** This is the authoritative rendered width.
- **For width equations**, use resolved px values:  
  `componentWidth ≈ paddingLeftPx + labelRectWidth + columnGapPx + inputRectWidth + columnGapPx + validationRectWidth + paddingRightPx`
- **Normalized values** (`canvasRect`, `canvasBounds`) should be used when comparing to canvas coordinates or when scale is not 1.

---

## 🧭 Properties → UI Coverage Matrix (Component Props + Styling)

**Goal:** Identify component properties that are **not mapped** to a UI control, or are mapped to the wrong one.

**Legend (UI locations):**
- **Identity & Behavior**: Properties Panel → `GeneralSection` (top)
- **Data Collection**: Properties Panel → `GeneralSection` (bottom)
- **Validation Rules**: Properties Panel → `ValidationSection`
- **Object Layout**: Properties Panel → `ObjectLayoutSection`
- **Options**: Properties Panel → `OptionsSection`
- **Date Settings**: Properties Panel → `DatePropertiesSection`
- **Button Settings**: Properties Panel → `ButtonPropertiesSection`
- **Terms Settings**: Properties Panel → `TermsPropertiesSection`
- **Data Export**: Properties Panel → `DataExportSection`
- **Divider Properties**: Properties Panel → `DividerPropertiesSection`
- **Appearance > Dimensions / Typography & Colors / Spacing**: Properties Panel → `AppearanceSection`
- **Global Typography & Spacing**: Global Properties Panel → Typography & Spacing
- **Global Object Layout**: Global Properties Panel → Object Layout

---

## ✅ Component capabilities (feature enablement)

To avoid feature logic being scattered across many files, component feature enablement is centralized in:

- `frontend/src/features/builder/utils/componentCapabilities.ts`

Examples:
- **Text Length Indicator** is enabled only when `supportsTextLengthIndicator === true` (builder visual guide).
- **Object Layout panel** is shown only when `supportsObjectLayout === true` (e.g., Divider disables it).

### Surface capabilities (toolbox vs canvas vs runtime)

Surface-specific rendering differences are centralized in:

- `frontend/src/features/builder/utils/componentSurfaceCapabilities.ts`

This is separate from `componentCapabilities.ts`:
- `componentCapabilities.ts` answers “does this component support the feature at all?” (i.e. should the editor show controls).
- `componentSurfaceCapabilities.ts` answers “how should this feature behave on this surface?” (toolbox/canvas/runtime parity contract).

Key implemented surface differences:
- **Dropdown**: canvas can render using `displayMode: 'longest-option'` (sizing guide), runtime/toolbox use placeholder.
- **Textarea**: toolbox suppresses crowded text-length guides; canvas shows them; runtime hides them.
- **Submit button**: runtime shows status only `while-submitting`; toolbox/canvas never show the spinner.

### A) Core `ComponentProps` coverage (common input components)

| Property | Type | Affects (Object/Archetype) | first-name | text | number | email | phone | url | textarea | dropdown | date | address | rating |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `label` | `string` | `label` (`PrimaryLabel`) | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior |
| `placeholder` | `string` | `input` (`InputControl`) | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior | — | Identity & Behavior | — |
| `helpText` | `string` | `validation` (`HelperText`) | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior |
| `required` | `boolean` | `label` + validation/runtime | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior | Identity & Behavior |
| `exportName` | `string` | export schema | Data Collection | Data Collection | Data Collection | Data Collection | Data Collection | Data Collection | Data Collection | Data Collection | Data Collection | Data Collection | Data Collection |
| `tabOrder` | `number` | keyboard navigation | Data Collection | Data Collection | Data Collection | Data Collection | Data Collection | Data Collection | Data Collection | Data Collection | Data Collection | Data Collection | Data Collection |
| `validation` | `ValidationRules` | `input` validation + `validation` message | Validation Rules | Validation Rules | Validation Rules | Validation Rules | Validation Rules | Validation Rules | Validation Rules | Validation Rules | Validation Rules | Validation Rules | Validation Rules |
| `objectLayout` / `layoutGroups` / `rowAlignment` | object/enums | internal object grouping | Object Layout | Object Layout | Object Layout | Object Layout | Object Layout | Object Layout | Object Layout | Object Layout | Object Layout | Object Layout | Object Layout |
| `objectSpacing` | `{ horizontalGap?, verticalSpacing?, objectGap? }` | layout-engine object gaps | Appearance > Spacing | Appearance > Spacing | Appearance > Spacing | Appearance > Spacing | Appearance > Spacing | Appearance > Spacing | Appearance > Spacing | Appearance > Spacing | Appearance > Spacing | Appearance > Spacing | Appearance > Spacing |
| `width` / `height` / `textAlign` / `componentScale` | sizing/enums | container + object sizing | Appearance > Dimensions | Appearance > Dimensions | Appearance > Dimensions | Appearance > Dimensions | Appearance > Dimensions | Appearance > Dimensions | Appearance > Dimensions | Appearance > Dimensions | Appearance > Dimensions | Appearance > Dimensions | Appearance > Dimensions |
| `styleOverrides.*` | `StyleOverrides` | `PrimaryLabel` / `InputControl` / `HelperText` | Appearance > Typography & Colors | Appearance > Typography & Colors | Appearance > Typography & Colors | Appearance > Typography & Colors | Appearance > Typography & Colors | Appearance > Typography & Colors | Appearance > Typography & Colors | Appearance > Typography & Colors | Appearance > Typography & Colors | Appearance > Typography & Colors | Appearance > Typography & Colors |

### B) Component-type specific `ComponentProps` coverage (selection + display + special components)

| Property | Type | checkbox | radio | terms | submit-button | header | paragraph | divider | url | rating |
|---|---|---|---|---|---|---|---|---|---|---|
| `label` | `string` | Identity & Behavior | Identity & Behavior | Terms Settings *(also editable in Identity & Behavior)* | **Not exposed** (submit button uses `buttonText`) | Identity & Behavior | Identity & Behavior (`text` fallback supported) | — | Identity & Behavior | Identity & Behavior |
| `validation` | `ValidationRules` | Validation Rules *(selection limits)* | Validation Rules *(selection limits)* | Validation Rules | — | — | — | — | Validation Rules (`url`, `pattern`, `urlDnsCheck`) | Validation Rules (required/range if configured) |
| `options` / `optionsDirection` / defaults | option models | Options | Options | — | — | — | — | — | — | — |
| `termsUrl` / `termsContent` / `termsLinkText` | `string` | — | — | Terms Settings | — | — | — | — | — | — |
| `buttonText` / `buttonAction` / `buttonAlign` / `buttonWidth` | `string` / enums | — | — | — | Button Settings | — | — | — | — | — |
| `urlPrefix` | `string` | — | — | — | — | — | — | — | URL Settings | — |
| `ratingMax` / `ratingStyle` / `ratingLabels.low/high` | number/enums/object | — | — | — | — | — | — | — | — | Rating Settings |

**Submit button UI mapping (current):**
- Alignment is controlled by `buttonAlign` in **Button Settings**, not `textAlign`.
- Button width is controlled by `buttonWidth` in **Button Settings** (component `width` still controls container sizing).
- Button Settings → Button Width and Appearance → Dimensions → Width should stay synchronized.

### C) Width/spacing override support by component family

| Override | Input family (`text/number/email/phone/url/textarea/dropdown/date/address/rating/first-name`) | Selection (`checkbox/radio/terms`) | Action (`submit-button`) | Display (`header/paragraph/divider`) |
|---|---|---|---|---|
| `inputWidthOverride` | ✅ Supported where `input` object exists (canvas handle + persisted prop) | ⚠️ Group-level behavior varies by renderer; not universal per-option width contract | ❌ N/A | ❌ N/A |
| `labelWidthOverride` | ✅ Supported (layout engine applies to label object) | ✅ Supported where label object exists | ⚠️ Component-dependent | ⚠️ Limited value on divider |
| `validationWidthOverride` | ✅ Supported where validation/help object exists | ✅ Supported | ⚠️ Submit button uses status/loading objects; validation width semantics differ | ❌ N/A |
| `labelGapOverride` / `inputHelpGapOverride` | ✅ In `ComponentProps`, but no dedicated panel controls | ✅ In `ComponentProps`, but no dedicated panel controls | ⚠️ Not primary mechanism | ❌ N/A |
| `objectSpacing` (`horizontalGap` / `verticalSpacing` / `objectGap`) | ✅ Supported | ✅ Supported | ✅ Supported | ✅ Supported |

### D) “Should exist” but currently incomplete, mismatched, or not mapped in panel controls (gaps)

| Property | Type | Current status |
|---|---|---|
| `validationMessage` | `string` | Exists in type/docs and runtime usage; still lacks a dedicated Properties Panel control. |
| `labelGapOverride` / `inputHelpGapOverride` | `number` | Present in `ComponentProps`, but no direct controls; users rely on `styleOverrides.*Gap` and `objectSpacing`. |
| `inputWidthMode` / `inputWidth` / `labelWrap` | enums/number/boolean | Present in type; only partial UI exposure (auto-fit button pattern). |
| `inputHeightOverride` | `number` | Documented previously, but not present as first-class `ComponentProps` field; implemented via `styleOverrides.inputHeight` and textarea `height`. |
| `labelWidthOverride` / `validationWidthOverride` | `number` | Supported by framework and resize pipeline; panel coverage remains partial across component families. |
| `initialVisibility` / `initialEnabled` | enums | Supported in runtime base-state and logic pipeline; ensure all component editors expose consistently. |

## 🔗 Component Framework Dependency Map

Understanding dependencies prevents regressions when modifying the framework.

### Resize System Dependencies

| State/Prop | Defined In | Consumed By | Purpose |
|------------|------------|-------------|---------|
| `resizePreview` | SortableComponent | SortableComponent, UniversalFieldShell | Live preview state during drag |
| `isResizingState` | SortableComponent | SortableComponent, ResizeHandles | Tracks active resize operation |
| `resizingComponentId` | useBuilderStore | BuilderPage, SortableComponent | Prevents drag during resize |
| `frozenGridTemplateColumns` | SortableComponent | UniversalFieldShell | Optional grid-track freeze for corner-resize stability; E/W skips freeze so input + border previews stay synchronized |
| `previewWidth` | SortableComponent → UniversalFieldShell | UniversalFieldShell, SmartBorder | Container width during preview |
| `previewObjectWidthOverrides` | SortableComponent → UniversalFieldShell | Grid columns, object renderers | Object widths during preview |
| `inputWidthOverride` (renderer) | UniversalFieldShell → renderer | objectRenderers | Input element inline width |

### Style System Dependencies

| State/Prop | Defined In | Consumed By | Purpose |
|------------|------------|-------------|---------|
| `globalStyles` | FormDefinition | computeFieldStyles, UniversalFieldShell | Base styling defaults |
| `styleOverrides` | component.props | computeFieldStyles | Per-component style customization |
| `componentScale` | component.props | SortableComponent, UniversalFieldShell | Component zoom level (50-200%) |
| `fieldStyles` | computeFieldStyles() | UniversalFieldShell, objectRenderers | Resolved styles for rendering |

### Layout System Dependencies

| State/Prop | Defined In | Consumed By | Purpose |
|------------|------------|-------------|---------|
| `gridLayout` | component.props / globalStyles | UniversalFieldShell | CSS Grid configuration |
| `objectLayout` | component.props | UniversalFieldShell | Object arrangement (horizontal/vertical/mixed) |
| `smartBorderLayout` | SortableComponent | SmartBorder | Border sizing mode ('fill' vs 'shrink') |

### Modification Checklist

When modifying resize behavior, verify these still work:
- [ ] E/W resize: Border follows mouse during drag
- [ ] E/W resize: Objects update during drag (when columns fit)
- [ ] E/W resize: Commit saves correct width overrides
- [ ] N/S resize: Input height and gaps update during drag
- [ ] Corner resize: Non-proportional (combined N/S + E/W behavior)
- [ ] Drag: Component moves after resize completes
- [ ] Scale: Component renders correctly at different scales

---

## 📏 Resize Handle Behavior

### Resize Handle Implementation (Shared Code)

**All components use the same resize handle implementation:**
- **Component:** `frontend/src/features/builder/components/ui/ResizeHandles.tsx` (shared across all components)
- **Logic:** `frontend/src/features/builder/components/SortableComponent.tsx` → `handleWidthChange` (shared function)
- **Hook:** `frontend/src/features/builder/hooks/useComponentResize.ts` (centralized resize logic)

**Component-specific behavior:**
- Component-specific logic is handled via conditional checks (e.g., `if (component.type === 'submit-button')`)
- Button-specific code is isolated within shared functions
- This ensures fixes apply to all components while allowing component-specific behavior
- **Important:** When fixing resize issues for one component type, verify the fix doesn't break other component types

### Handle Positions and Actions

```
    nw ─────── n ─────── ne
    │                     │
    │                     │
    w       Component     e
    │                     │
    │                     │
    sw ─────── s ─────── se
```

### Handle Action Matrix

| Handle | Anchor | Primary Action | Secondary Action |
|--------|--------|----------------|------------------|
| **NW** | SE corner | **Corner resize** = W + N | Width: Component + object widths (+ position like W). Height: Input height → Label-Input gap (like N). |
| **N** | South edge | Input height → Label-Input gap | (see Height Resize) |
| **NE** | SW corner | **Corner resize** = E + N | Width: Component + object widths (like E). Height: Input height → Label-Input gap (like N). |
| **E** | West edge | Component + object widths | - |
| **SE** | NW corner | **Corner resize** = E + S | Width: Component + object widths (like E). Height: Input height → Input-Help gap (like S). |
| **S** | North edge | Input height → Input-Help gap | (see Height Resize) |
| **SW** | NE corner | **Corner resize** = W + S | Width: Component + object widths (+ position like W). Height: Input height → Input-Help gap (like S). |
| **W** | East edge | Component + object widths + position | - |

---

## ↔️ Width Resize (E/W Handles)

Width resize primarily updates the **component container width**. Internally, the framework treats the **Input** as the flexible object that absorbs width changes, while **Label** and **Help/Validation** remain content-sized (they do not “grow to fill” the extra space).

> **Architectural Note:** Some components (like `rating`) intentionally hide E/W and corner resize handles via `hideHorizontalHandles` to enforce strict architectural discipline, as their width is intrinsically driven by their content (e.g., number of stars).

### Width Calculation per Object Category

| Category | Width Source | Behavior |
|----------|--------------|----------|
| **Label** | Label text content | Known width from text; wraps if too narrow |
| **Input** | Text length estimator | `maxLength` + font properties → estimated visible width (has default min-width ~60-80px) |
| **Help/Validation** | Longest validation message | Calculated width; wraps if too narrow |
| **Action** (Button) | User-specified width | Set via `actionWidthOverride` or percentage width |
| **Divider** | User-specified width | Set via `width` prop (percentage or pixels). Acts as a flexible width object in grid layout. Min width 10px. |
| **Display** (Header, Paragraph) | User-specified width | Set via `width` prop and E/W resize overrides. Acts as a flexible width object in grid layout. Min width 10px. |

### Object-Aware Width Calculations

**Critical:** When calculating width for a target object, you must account for other objects in the component that are **NOT in the same column/row**.

**Calculation Formula:**
```
targetObjectWidth = (canvasWidth × percentage) - sum(otherObjectWidths) - gaps
```

**Example (Button component in horizontal layout):**
- Button has 3 objects: `button`, `validation`, `loading`
- User sets button width to 75% of canvas
- Validation width (known): 200px
- Loading width (known): 150px
- Column gaps: 16px
- Canvas width: 1920px
- **Button width = (1920 × 0.75) - 200 - 150 - 16 = 1074px**

**Example (Text Input in grid layout):**
- Objects: `label` (Column 1, 200px), `input` (Column 2, target), `validation` (Column 3, 150px)
- User sets input width to 50% of canvas
- Column gaps: 16px total
- **Input width = (1920 × 0.50) - 200 - 150 - 16 = 594px**

**Key Rules:**
1. Only subtract widths of objects **NOT in the same column/row** as the target object
2. Include all gaps between objects in the calculation
3. Grid layout adapts to object widths (objects don't adapt to grid)
4. This applies to **ALL components** regardless of layout type (vertical/horizontal/mixed/grid)

### NEW: Input-only width resize handle (Canvas)

In addition to the component-level E/W resize handles, the builder now supports an **input-only width handle** for text-like components rendered through `UniversalFieldShell`.

- **Where it appears**: Builder canvas only, when the component is selected. A small **green handle** appears on the **right edge of the Input object**.
- **What it changes**: Updates **only** `component.props.inputWidthOverride` (px).
- **What it does NOT change**:
  - Does **not** change `component.props.width` (the overall component width)
  - Does **not** change `labelWidthOverride` or `helpWidthOverride`
- **Why**: Enables short (or long) input controls without forcing label/help to shrink to the same width.

**Implementation note (current code):**
- Live preview uses `UniversalFieldShell.previewObjectWidthOverrides`.
- On commit, the value is persisted to `ComponentProps.inputWidthOverride`.

### Text Length Estimator

For Input objects, width is estimated using:
```typescript
estimatedWidth = estimateTextWidth(maxLength, {
    fontFamily: inputFontFamily,
    fontSize: inputFontSize,
    fontWeight: inputFontWeight,
});
```

### Width Resize Behavior

**East Handle (E):**
- Anchors the **West edge** (left side stays fixed)
- Expands/contracts the **East edge** (right side moves)
- Updates `props.width` and object width overrides
- **Label and Help stay fixed** at their current widths
- **Input, Display, and Divider objects absorb all width changes** (expands/contracts)
- During drag, input preview and SmartBorder preview resize together (E/W does not freeze grid tracks)
- Position remains unchanged
- **Row-aware budgeting:** only objects **in the same row as the flexible object** reduce the flexible object's available width.
  - **Vertical stack:** Label (row 1), Input (row 2), Validation (row 3) → Input expands to full component width (minus SmartBorder padding).
  - **Grid example:** Label above, Input + Validation on the same row → Input expands to the remaining width after Validation + gaps.

**West Handle (W):**
- Anchors the **East edge** (right side stays fixed)
- Expands/contracts the **West edge** (left side moves)
- Updates `props.width`, `position.x`, and object width overrides
- **Label and Help stay fixed** at their current widths
- **Input, Display, and Divider objects absorb all width changes** (expands/contracts)

**On Commit (drop):**
- `labelWidthOverride`, `inputWidthOverride`, `helpWidthOverride`, `actionWidthOverride` are persisted
- `props.width` is updated to new component width (px)

### Component Capabilities and Width Constraints

**Component capabilities impose constraints that limit achievable widths:**

**Collision Detection:**
- Prevents components from overlapping
- If collision detected during resize → resize stops
- Maximum achievable width = available space - blocking component width - gap

**Canvas Boundary Constraints:**
- Components must stay within canvas bounds
- If resize would exceed canvas → width is clamped to maximum allowed

**Example with Collision Detection:**
- User tries to set button to 100% width (1920px)
- Another component exists at x = 800px with width 300px
- Component's current position: x = 100px
- Collision detected: (100 + 1920) > 800
- **Maximum achievable width = 800 - 100 = 700px**
- Recalculate button width: 700px - otherObjectWidths - gaps = final width

**Implementation:**
- Capability constraints are checked during resize calculations
- Constraints apply to **ALL components** regardless of type
- Constraints must be considered when calculating percentage widths

### Narrow Component Behavior

When component becomes very narrow:
- **Label:** Text wraps to multiple lines ✅
- **Input:** Does NOT wrap (fixed single-line) ❌
- **Help:** Text wraps to multiple lines ✅

```
Wide:   [Label Text Here        ]
        [Input Field             ]
        [Help/Validation message ]

Narrow: [Label    ]
        [Text Here]
        [Input    ]
        [Help/Val-]
        [idation  ]
```

### E/W Resize Live Preview Architecture

During E/W resize drag, visual feedback requires coordinated updates across multiple layers:

**Data Flow (SortableComponent → UniversalFieldShell → Renderers):**
```
resizePreview state (SortableComponent)
    ├── previewWidth → container width + SmartBorder
    ├── previewLabelWidth/previewInputWidth/previewHelpWidth
    │       ↓
    │   previewObjectWidthOverrides prop (UniversalFieldShell)
    │       ├── gridTemplateColumns (CSS Grid columns)
    │       └── renderer props (inputWidthOverride, etc.)
    └── frozenGridTemplateColumns (optional, corner handles only)
```

**Grid Column Priority:**
```
previewGridTemplateColumns > (corner-only) frozenGridTemplateColumns > explicitGridTemplateColumns > base (1fr)
```

**Critical Implementation Rules:**
1. **Both grid AND renderers need preview values**: Grid columns control cell size, but input elements also have their own `width` style. Both must use preview values or the visual won't update.
2. **Column fit constraint**: Preview columns must fit within `previewWidth`. If `label + input + help + gaps > previewWidth`, browser can't render correctly—skip preview columns.
3. **Scale factor**: DOM measurements are screen pixels. Convert to base pixels: `basePx = screenPx / (componentScale/100 * canvasScale)`.
4. **SmartBorder synthetic segment**: During E/W resize, add a synthetic segment at `previewWidth` to force border to follow the preview width.

**Debug checklist (E/W resize not updating):**
- Check `previewObjectWidthOverrides` is passed to UniversalFieldShell
- Check `previewGridTemplateColumns` is generated (logs: `fieldshell.grid.preview-columns`)
- Check input renderer receives preview `inputWidthOverride` (not committed value)
- Check column widths fit within previewWidth
- Check `frozenGridTemplateColumns` is not active for E/W drag (`resize.grid.freeze.skip` expected)

### useComponentResize Hook

The `useComponentResize` hook (`hooks/useComponentResize.ts`) centralizes resize logic for maintainability:

```typescript
const [resizeState, resizeAPI] = useComponentResize(component, componentScale, canvasScale);

// Start resize
resizeAPI.startResize('e', containerRef);

// Update during drag
resizeAPI.setPreview({ width: newWidth, horizontalHandle: 'e', ...previewWidths });

// Get props for UniversalFieldShell
const { previewWidth, previewObjectWidthOverrides } = resizeAPI.getPreviewProps();

// Clear on commit
resizeAPI.clearResize('commit');
```

**Pure functions for testing:**
```typescript
import { calculatePreviewWidths, willColumnsFit, screenToBasePx } from './useComponentResize';

// Test width calculations
const widths = calculatePreviewWidths(500, capturedWidths);
expect(widths.inputWidthOverride).toBe(expectedInput);

// Test column fit
const fits = willColumnsFit(300, 70, 60, 200, 8);
expect(fits).toBe(false); // 70+60+200+16 > 300
```

---

## ↕️ Height Resize (N/S Handles)

Height resize uses a **two-phase adjustment** with cascading behavior.

### North Handle (N) - Anchors South Edge

Moving **North** (pulling up):
1. **Phase 1:** Increase Input Height until `inputMaxHeight`
2. **Phase 2:** Then increase Label-Input Gap until `labelGapMax`

Moving **South** (pushing down):
1. **Phase 1:** Decrease Input Height until `inputMinHeight`
2. **Phase 2:** Then decrease Label-Input Gap until `labelGapMin`

### South Handle (S) - Anchors North Edge

Moving **South** (pulling down):
1. **Phase 1:** Increase Input Height until `inputMaxHeight`
2. **Phase 2:** Then increase Input-Help Gap until `inputHelpGapMax`

Moving **North** (pushing up):
1. **Phase 1:** Decrease Input Height until `inputMinHeight`
2. **Phase 2:** Then decrease Input-Help Gap until `inputHelpGapMin`

### Height Resize Properties

| Property | Affected By | Min | Max |
|----------|-------------|-----|-----|
| `inputHeight` | N, S handles (for standard inputs) | 28px | 240px |
| `component.props.height` | N, S handles (for `display` objects) | 28px (or min-content) | 2000px |
| `dividerBorderWidth` | N, S handles (for `divider` component thickness) | 1px | 20px |
| `labelGap` | N handle | 0px | 48px |
| `inputHelpGap` | S handle | 0px | 48px |

### Visual Example

```
Before N resize:
┌──────────────────────┐
│ Label                │ ← labelGap: 8px
├──────────────────────┤
│ Input (40px)         │ ← inputHeight: 40px
├──────────────────────┤
│ Validation           │
└──────────────────────┘

After pulling N handle up:
┌──────────────────────┐
│ Label                │
│                      │ ← labelGap: 24px (increased)
├──────────────────────┤
│                      │
│ Input (80px)         │ ← inputHeight: 80px (at max)
│                      │
├──────────────────────┤
│ Validation           │
└──────────────────────┘
```

---

## 🔲 Corner Resize (NW/NE/SE/SW) — Non‑Proportional

Corner handles are **2-axis resize**, aligned with the N/S/E/W handles (not proportional scaling).

- **Key rule**: Corner handles **do not change** `componentScale`.
- **Mental model**: Dragging a corner is equivalent to dragging the matching horizontal + vertical edge handles at the same time.

### Corner-to-edge mapping

| Corner Handle | Anchor (fixed corner) | Equivalent edge handles |
|--------------|------------------------|--------------------------|
| **NW** | SE corner | W + N |
| **NE** | SW corner | E + N |
| **SE** | NW corner | E + S |
| **SW** | NE corner | W + S |

### What changes when you drag a corner

- **Width**: Uses the existing **E/W width resize** behavior (component width + internal object widths; W also adjusts `position.x`).
- **Height**: Uses the existing **N/S height resize** behavior (two-phase cascades: `inputHeight` then `labelGap` / `inputHelpGap`).

If a component type does not support height resizing, the vertical portion of the corner drag is effectively a no-op for that component.

---

## 🔍 Proportional Scale (Component Scale control only)

Proportional scaling is now **exclusive** to the Properties Panel control:

- **UI**: Properties Panel → Appearance → **Component Scale**
- **Data**: `component.props.componentScale` (50–200%)
- **Behavior**: scales typography/spacing/sizing consistently and supports anchor selection (NW/NE/SE/SW) so one corner can remain fixed during scaling.

---

## 🔧 Component Structure (UniversalFieldShell)

The `UniversalFieldShell` (`components/UniversalFieldShell.tsx`) is the universal wrapper for all form components. It manages layout, spacing, conditional visibility, and integrates the `SmartBorder`.

### Key Responsibilities
1. **Layout Management:** Supports **Grid Layout** *and* **Object Layout**.
   - **Grid Layout (preferred):** when `component.props.gridLayout` (or `globalStyles.defaultGridLayout`) is enabled, it renders a CSS Grid container (`data-layout-type="grid"`) and positions objects via `cellAssignments` (+ `mergedCells` / `objectSpans`) using `gridLayoutUtils`. **Note:** Columns containing `input`, `display`, or `divider` objects are rendered as flexible `minmax(0, 1fr)` tracks to allow stretching, while columns with only static objects (`label`, `validation`, etc.) use `minmax(0, max-content)`.
   - **Object Layout (legacy/transition):** otherwise it falls back to `vertical` / `horizontal` / `mixed` grouping via `groupObjectsByLayout`.
2. **Conditional Rendering:** Filters objects based on `conditionalContext`. In `builderMode`, conditional objects are always rendered (so SmartBorder accounts for their space).
3. **SmartBorder Integration:** Wraps content in `<SmartBorder>` when in `builderMode` to provide the collision/selection boundary.
4. **Spacing:** 
   - **Grid Layout:** uses `gridLayout` row/column gaps (including per-row/column overrides).
   - **Object Layout:** calculates gaps using `calculateSpacing` (global styles + overrides).

### NEW: Selection “Extra Text” pattern (Dropdown / Radio / Checkbox)

When a selection component needs an option-specific free-text capture, it should use the **per-option extra text** model (not a special-cased `allowOther` object). This keeps the framework consistent and works across Dropdown/Radio/Checkbox.
- SmartBorder accounts for the extra input(s) in builder mode (canvas shows the space required).
- Runtime conditionally shows the extra input only for the selected option(s) that have `hasExtraText=true`.

#### Properties (ComponentProps)

- `options[].hasExtraText?: boolean`
- `options[].extraPlaceholder?: string`
- `options[].group?: string` (visual section label)
- `extraTextValidation?: ValidationRules` (shared rules for all option extra inputs)
- `extraTextValidationMessage?: string`

#### Structure contract (object ids)

- Selection components continue to expose a single `input` object (plus `label`/`validation`) in the Object Layout.
- Per-option extra inputs are rendered **inside** the selection input renderer (as part of option rows), but still participate in SmartBorder sizing on canvas.

#### Default layout (recommended)

Keep the **top-level structure** simple and consistent:

- **Dropdown**: `vertical` (`label`, `input`, `validation`)
- **Radio**: `vertical` (`label`, `input`, `validation`)
- **Checkbox**: `horizontal` for (`input`, `label`) with `validation` below (via layout groups)

The per-option extra inputs are rendered **inside** the selection `input` renderer (not as separate top-level objects). Internally, the renderer uses a stable two-column layout:

- **Left edge (aligned)**: the extra input starts after the longest option label (e.g. “Vegetarian” sets the x-position).
- **Right edge (flush)**: the extra input fills the remaining space to the component’s right edge (no overflow).

For dropdown specifically:

- The **dropdown control width** is anchored to the longest option width (or a user override via the green input-only handle).
- The **extra input** fills the remaining width inside the component.
- Min-width rules keep both controls usable (see below).

#### Runtime visibility rule

- Canvas/Builder: when any option has `hasExtraText=true`, the component shows/allocates space for the extra input(s) so the user can size/layout correctly.
- Preview/Production: the extra input is shown **only for the selected option(s)** where `hasExtraText=true`.

#### Runtime value shape (for data binding + logic compatibility)

To preserve both the selection and any typed extra text:

- Dropdown / Radio:
  - `value: { value: string; extraTextByValue?: Record<string,string> }`
- Checkbox:
  - `value: { values: string[]; extraTextByValue?: Record<string,string> }`

The logic engine unwraps these shapes for comparisons (it compares on `value` / `values`).

#### TextLengthIndicator (canvas-only, surface controlled)

- The extra text input uses the existing surface capability gate:
  - `getComponentSurfaceCapabilities(type, 'canvas').textLengthIndicator.enabled === true`
- It is **canvas-only** (never shown in runtime), and uses `extraTextValidation.maxLength` as the max-length source.

#### Min-width + resizing rules (implemented)

- **Checkbox/Radio (when extra text enabled)**: component has a dynamic min-width:
  - longest option label + padding/gaps + **5 characters** worth of extra-input width
- **Dropdown (when extra text enabled)**:
  - dropdown control min-width: **10 characters** (plus arrow chrome) and never below the longest option width
  - extra input min-width: **10 characters**
  - the dropdown width handle is clamped so the extra input can never overflow the component.

### Rendering Surfaces (parity contract)

All UniversalFieldShell-based rendering is **surface-aware**:

- **toolbox**: compact preview card in the left toolbox (non-interactive, may suppress crowded helpers)
- **canvas**: builder WYSIWYG (shows SmartBorder, resize handles, sizing guides)
- **runtime**: public preview + production renderer (no builder chrome; must match production)

Implementation:
- `ComponentSurface` is threaded through `UniversalFieldShell` and the shared object renderers.
- Surface-specific behavior is declared centrally in `utils/componentSurfaceCapabilities.ts` via `getComponentSurfaceCapabilities(type, surface)`.

### SmartBorder Integration (Dual Skyline Algorithm)

The `SmartBorder` uses a **Dual Skyline (Geometric Union)** algorithm to draw a tight, padded boundary around the component's visible content, wrapping it closely on both the left and right sides.

#### SmartBorder sizing mode (implemented)

By default, SmartBorder is **shrink-to-content** (implemented via `inline-block` / `inline-flex`) so the border tightly wraps the component’s objects.

Some components must instead allow **percentage widths** (e.g. Divider with `width: '100%'`) to resolve against the stage width. For these cases, SmartBorder supports a **fill-width mode**:

- `SmartBorder.layout: 'shrink' | 'fill'` (default `'shrink'`)
- `UniversalFieldShell.builderMode.smartBorderLayout: 'shrink' | 'fill'`

Current usage:
- Divider on canvas sets `smartBorderLayout: 'fill'` so its `<hr>` width does not collapse to `0px` inside a shrink-wrapped container.

#### Algorithm Details
1. **Input:** Deeply iterates through the component's layout groups to identify individual leaf elements (Label, Input, Help, etc.).
2. **Padded Segments:** Converts each element into a "Padded Segment" rectangle:
   - `Top`: `element.top - padding`
   - `Bottom`: `element.bottom - marginBottom + padding`
   - `Left`: `element.left - padding`
   - `Right`: `element.right + padding`
3. **Dual Profiles:** Calculates two profiles for every vertical interval:
   - **Right Profile:** `maxX` of all segments in the interval.
   - **Left Profile:** `minX` of all segments in the interval.
4. **Gap Optimization (Minimal Area Bridging):** If there is a vertical gap between elements on either side:
   - The algorithm bridges the gap using the "inner" width to minimize enclosed empty space.
   - **Right Side:** Uses `min(prevX, nextX)` (favors inner edge).
   - **Left Side:** Uses `max(prevX, nextX)` (favors inner edge, i.e., larger X).
   - **Result:** The border creates a concave "C" shape or indent where appropriate (e.g., around a short label next to a tall input), eliminating empty space.

### Collision detection & drag constraints (Canvas)

**Purpose of SmartBorder (collision):**
- SmartBorder provides a stable **measured bounds** element per component (via `data-component-id`) so we can do reliable geometry checks for:
  - **Canvas boundary constraints** (keep components on-canvas)
  - **Inter-component collision detection** (prevent overlap)

**A) Canvas boundary constraint**
- **Implemented behavior:** Components are **hard-clamped** to the canvas while dragging and on drag end commit.
  - Utility: `frontend/src/features/builder/utils/collisionDetection.ts` → `checkCanvasBoundary(...)`.
  - Live enforcement occurs in `BuilderPage.tsx` (drag move + drag end parity).

**B) Component-to-component overlap prevention**
- **Implemented behavior (locked in):** While dragging, movement is constrained to avoid overlap using a **jump/slide** response driven by the **SmartBorder SVG shape**:
  - **Broad phase (performance):** AABB overlap is used only to cheaply find “could collide” pairs (and as an initial upper bound for resolution distance).
  - **Narrow phase (correctness):** Collision is tested using the **SmartBorder polygon** (parsed from the SVG `path d` produced by `SmartBorder`’s Dual Skyline algorithm).
  - **Resolution (“jumping”):** When a collision is detected, we resolve by searching for the **smallest axis movement** (left/right/up/down) that produces **no polygon collision**, then choose the best candidate (closest to the user’s intended position and stable frame-to-frame).
    - This preserves the desired “jumping” feel while ensuring the landing position matches the **SmartBorder outline**, not the component’s bounding rectangle.
  - **Existing overlap escape:** If the component starts overlapped (legacy/bad state), moves that **reduce overlap** are allowed; moves that **increase** overlap are blocked.
  - Enforcement is applied on **drag move** and re-checked on **drag end** for parity.
  - Core solver: `frontend/src/features/builder/utils/collisionDetection.ts` → `resolveMoveConstraints(...)` (uses SmartBorder polygon + polygon-aware separation search).

**C) Resize + Properties Panel non-overlap contract**
- **Resize handles:** keep the requested size change, then **auto-adjust position** to fit without overlap/bounds; if impossible, the change is rejected and a toast is shown.
- **Properties Panel size edits:** same policy—after a size-affecting edit, we verify collisions and either auto-adjust position or revert with a toast.

**Enablement (default-on for new components):**
- Canvas constraint feature flags are declared in `frontend/src/features/builder/utils/componentSurfaceCapabilities.ts`:
  - `dragConstraints` (canvas)
  - `resizeConstraints` (canvas)
  - Defaults are enabled in `BASE_BY_SURFACE.canvas`, so new component types inherit the behavior automatically.

### Submit Button (props parity: canvas ↔ runtime)

**Implemented behavior (locked in):**
- Submit button rendering is driven by `UniversalFieldShell` + `createActionRenderer()` (object renderer).
- `buttonWidth` and `buttonAlign` are applied consistently on **canvas** and **runtime**:
  - `buttonWidth: "auto"` → content-sized button
  - `buttonWidth: "full"` → button stretches to fill the available width
  - `buttonAlign: "left" | "center" | "right"` → alignment within the component container
- Behavior toggles (exposed in Properties Panel → Button Settings):
  - `showLoadingState` (spinner while submitting, runtime-only)
  - `showIcon` (paper airplane icon visibility)

**Button Width Control Synchronization:**

**Current Issue:**
- `buttonWidth: 'full'` must be set before percentage widths in Appearance → Dimensions → Width work
- This creates user confusion due to controls being in different sections

**Required Behavior (to be implemented):**
- **Button Settings → Button Width "Auto (fit content)"** → Automatically sets `width: undefined` (Auto)
- **Button Settings → Button Width "Full Width"** → Automatically sets `width: '100%'`
- **Appearance → Dimensions → Width** → Works independently, sets `width` and `actionWidthOverride` appropriately:
  - **Auto**: Uses global width for all objects in component
  - **25%, 33%, 50%, 66%, 75%, 100%**: Changes width of button object to that percentage of Canvas width (accounting for other objects and gaps)
  - **Custom (px)**: Sets pixel width of button object to custom value

**Width Calculation for Buttons:**
- Button component has 3 objects: `button`, `validation`, `loading`
- Validation and loading widths are known (based on longest text they display)
- When setting percentage width, calculate: `buttonWidth = (canvasWidth × percentage) - validationWidth - loadingWidth - gaps`
- Only subtract widths of objects **NOT in the same column/row** as the button
- Apply component capability constraints (collision detection, canvas boundaries) to limit achievable widths

### Structure Definition

Each component defines a `structure` (in `ComponentRegistry.tsx`) that describes its internal objects, default layout, and default row alignment. Instances can override `objectLayout` / `layoutGroups` via `component.props`.

```typescript
export type ObjectLayoutType = 'vertical' | 'horizontal' | 'mixed';
export type ObjectType = 'label' | 'input' | 'action' | 'status' | 'validation' | 'divider' | 'custom';

export type StyleArchetype =
  | 'PrimaryLabel'
  | 'InputControl'
  | 'HelperText'
  | 'Action'
  | 'Divider';

export interface ComponentObject {
  id: string;                 // e.g., 'label', 'input', 'validation'
  type: ObjectType;           // render object type
  archetype?: StyleArchetype; // which GlobalStyles bucket it inherits from
  required: boolean;
  order: number;
  conditional?: {
    type: 'prop' | 'state' | 'validation' | 'always';
    prop?: string;
    showInProperties?: boolean;
  };
}

export interface ComponentStructure {
  objects: ComponentObject[];
  defaultLayout: ObjectLayoutType;
  layoutGroups?: Record<string, string[]>;
  defaultRowAlignment?: 'top' | 'center' | 'bottom' | 'stretch';
}
```

### Object Types

| Type | Default archetype | Description |
|------|-------------------|-------------|
| `label` | `PrimaryLabel` | Text label for field |
| `input` | `InputControl` | User input control (text/select/checkbox/radio/etc.) |
| `validation` | `HelperText` | Help/validation message area |
| `action` | `Action` | Button/clickable action (e.g., submit) |
| `status` | `HelperText` | Status indicator (runtime submit spinner) |
| `divider` | `Divider` | Visual separator line |
| `display` | `DisplayBlock` | Read-only structural text (e.g., headers, paragraphs) that spans width and can be resized |
| `custom` | *(explicit)* | Custom object types (future) |

---

## 📦 Component Registry

### Location
- **File:** `frontend/src/features/builder/registry/ComponentRegistry.tsx`

### Component Registration (structure + archetypes)

```typescript
const ComponentRegistry: Record<ComponentType, ComponentDefinition> = {
    'text': {
        type: 'text',
        name: 'Text Input',
        icon: 'Type',
        category: 'input',
        defaultProps: { label: 'Text', placeholder: 'Enter text' },
        structure: {
            objects: [
                { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
                { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2 },
                { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3 }
            ],
            defaultLayout: 'vertical'
        },
    },
    'checkbox': {
        type: 'checkbox',
        name: 'Checkbox',
        structure: {
            objects: [
                { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 1 },
                { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 2 },
                { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3 }
            ],
            defaultLayout: 'horizontal',
            layoutGroups: { row1: ['input', 'label'], row2: ['validation'] }
        },
    },
    // ... other components
};
```

---

## 🎯 Style Resolution Flow

Styles are resolved in this order (later overrides earlier):

```
1. Theme defaults (from ThemeContext)
       ↓
2. Global Styles by Category (Label, Input, Help)
       ↓
3. Component Style Overrides (component.props.styleOverrides)
       ↓
4. Component Scale (component.props.componentScale)
       ↓
5. Final Computed Styles (passed to renderer)
```

### Component Scale and Object Widths (WYSIWYG)

**Important:** When `componentScale` changes, object width overrides (`labelWidthOverride`, `inputWidthOverride`, `helpWidthOverride`) are automatically scaled proportionally to maintain WYSIWYG between Builder Canvas and Public Preview.

**How it works:**
1. **Builder Canvas**: Applies `componentScale` via CSS `transform: scale()` for visual scaling
2. **When scale changes**: Object widths are scaled proportionally:
   - `newWidth = oldWidth * (newScale / oldScale)`
   - Example: Scale changes from 100% → 120%, object widths multiply by 1.2
3. **Public Preview**: Uses scaled object widths directly from `component.props.*WidthOverride`
   - Object widths are already scaled, so preview matches canvas appearance
   - Container width may also be scaled by `componentScale` depending on implementation

**Implementation:**
- **Single-select**: `AppearanceSection.tsx` scales object widths when Component Scale slider changes
- **Multi-select**: `PropertiesPanel.tsx` scales object widths for all selected components (based on first component's scale ratio)

**Why this matters:**
- Ensures Public Preview matches Builder Canvas appearance
- Object widths stored in props are "baked in" at the scaled size
- No need for Public Preview to apply componentScale to object widths separately

---

## 📋 Quick Reference: Property Change by Action

| User Action | Properties Changed | Handler |
|-------------|-------------------|---------|
| Drag component | `position.x`, `position.y` | `handleDragEnd` |
| E handle resize | `props.width`, object widths | `handleWidthChange` |
| W handle resize | `props.width`, `position.x`, object widths | `handleWidthChange` |
| N handle resize | `inputHeight`, `labelGap` (cascading) | `handleVerticalResizeEnd` |
| S handle resize | `inputHeight`, `inputHelpGap` (cascading) | `handleVerticalResizeEnd` |
| Corner resize | `props.width` (+ `position.x` for W), `inputHeight`, `labelGap` / `inputHelpGap` | `handleResize` |
| Component Scale slider | `props.componentScale`, `labelWidthOverride`, `inputWidthOverride`, `helpWidthOverride` | `AppearanceSection.onChange` / `PropertiesPanel.handleMultiPropsChange` |
| Properties Panel | Various `props.*` | `updateComponentProps` |
| Global styles | `globalStyles.*` by category | `updateGlobalStyles` |

---

## 🐛 Known Issues & Solutions

### Issue: Resize handles triggering drag instead of resize
**Cause:** dnd-kit uses `onPointerDown` while resize handles used `onMouseDown`
**Solution:** Use `onPointerDown` on handle elements with `e.stopPropagation()`

### Issue: West handle not anchoring East edge
**Cause:** Position not being adjusted when width changes
**Solution:** Calculate `leftShift` and update `position.x` along with width

### Issue: North/South handles not following two-phase adjustment
**Cause:** Single property adjustment instead of cascading
**Solution:** Implement phase detection: adjust height first, then gap

---

## 📚 Related Files

| File | Purpose |
|------|---------|
| `types/builder.types.ts` | Type definitions |
| `registry/ComponentRegistry.tsx` | Component definitions with categories |
| `components/SortableComponent.tsx` | Canvas component wrapper |
| `components/UniversalFieldShell.tsx` | Universal component shell |
| `components/ui/SmartBorder.tsx` | Smart border for collision/drag |
| `components/ui/ResizeHandles.tsx` | Resize handle UI |
| `utils/styleComputation.ts` | Style resolution by category |
| `utils/textLengthEstimator.ts` | Input width estimation |
| `utils/collisionDetection.ts` | Collision detection |
| `stores/useBuilderStore.ts` | State management |
| `types/validationRule.types.ts` | Validation rule type definitions |
| `utils/validationEngine.ts` | Validation execution engine |
| `data/validationRuleSeed.ts` | Built-in validation rules |

---

## ⏪ Undo/Redo Service

### Current Implementation

The undo/redo service in `useBuilderStore.ts` provides:

| Feature | Status |
|---------|--------|
| History stacks | ✅ `historyPast`, `historyFuture` |
| Max history size | ✅ 50 entries |
| Push to history | ✅ `pushToHistory()` |
| Undo/Redo actions | ✅ `undo()`, `redo()` |
| Can check availability | ✅ `canUndo()`, `canRedo()` |
| Action description | ❌ **MISSING** |

### Current FormSnapshot Interface

```typescript
// Current (no description)
interface FormSnapshot {
    formDefinition: FormDefinition;
    timestamp: number;
}
```

### Required Enhancement

```typescript
// Enhanced (with description for user)
interface FormSnapshot {
    formDefinition: FormDefinition;
    timestamp: number;
    description: string;  // ← NEW: Human-readable action description
}
```

### Action Description Examples

| Action | Description |
|--------|-------------|
| Add component | `"Add Text Input"` |
| Delete component | `"Delete Email Field"` |
| Move component | `"Move First Name to (120, 340)"` |
| Resize component | `"Resize Email width to 400px"` |
| Change property | `"Change label to 'Full Name'"` |
| Change validation | `"Add required validation"` |
| Global style change | `"Update label font size to 16px"` |
| Object layout change | `"Change layout to horizontal"` |
| Bulk edit | `"Update 3 components: required=true"` |

### Enhanced pushToHistory API

```typescript
// Current
pushToHistory: () => void;

// Enhanced
pushToHistory: (description: string) => void;

// Usage
get().pushToHistory('Change label to "Email Address"');
get().pushToHistory('Resize component width to 350px');
get().pushToHistory('Move component to (100, 200)');
```

### UI Display

```
┌─────────────────────────────────────┐
│  ↩️ Undo    ↪️ Redo                  │
├─────────────────────────────────────┤
│  Next Undo: "Change label to 'Email'"│
│  Next Redo: "Delete First Name"      │
└─────────────────────────────────────┘
```

---

## ✅ Validation Rule System

### Overview

The validation system is a **differentiating feature** with these capabilities:

| Feature | Description |
|---------|-------------|
| Multiple rules per component | Each component can have many validation rules |
| Priority ordering | Rules are checked in priority order |
| Country-specific rules | Phone, date, name validation per country |
| Auto-fix support | Some rules can auto-correct issues |
| Educational content | Pros, cons, best-for, warnings |

### Validation Display Behavior

**CRITICAL DIFFERENCE:** Validation messages are displayed differently depending on context:

#### Component Level (Input Fields)

At the component level, show **ONLY the first failed rule**:

```
┌────────────────────────────────────┐
│ Email Address                      │
├────────────────────────────────────┤
│ [invalid-email@              ]     │
│ ⚠️ Please enter a valid email      │  ← First failed rule only
└────────────────────────────────────┘
```

**Rationale:** 
- Reduces visual clutter
- Allows user to fix one issue at a time
- After fixing, next validation error (if any) appears

#### Button Component (Form Submission)

At the button level, show **ALL validation errors** that must be fixed:

```
┌────────────────────────────────────┐
│ Before you can submit:             │
│                                    │
│ ⚠️ Email: Enter a valid email      │
│ ⚠️ Phone: Required field           │
│ ⚠️ Name: Minimum 2 characters      │
│                                    │
│ [Submit] ← Disabled                │
└────────────────────────────────────┘
```

**Rationale:**
- User sees complete list of issues
- Button remains disabled until ALL fixed
- Clear indication of what's blocking submission

### Validation Display Logic

```typescript
// Component level: First failed rule only
function getComponentValidationMessage(component: FormComponent): string | null {
    const rules = component.props.validation?.rules || [];
    const sortedRules = rules.sort((a, b) => a.priority - b.priority);
    
    for (const rule of sortedRules) {
        const result = validateRule(rule, component.value);
        if (!result.isValid) {
            return result.errors[0].message;  // Return FIRST error only
        }
    }
    return null;
}

// Button level: ALL failed rules
function getFormValidationErrors(components: FormComponent[]): ValidationError[] {
    const allErrors: ValidationError[] = [];
    
    for (const component of components) {
        const rules = component.props.validation?.rules || [];
        for (const rule of rules) {
            const result = validateRule(rule, component.value);
            if (!result.isValid) {
                allErrors.push(...result.errors);  // Collect ALL errors
            }
        }
    }
    return allErrors;
}
```

### Validation Rule Priority

Rules are checked in priority order (lower number = higher priority):

| Priority | Rule Type | Example |
|----------|-----------|---------|
| 1 | Required | Field must have value |
| 10 | Format | Email format, phone format |
| 20 | Length | Min/max length |
| 30 | Pattern | Custom regex |
| 40 | Security | XSS prevention |
| 50 | Custom | User-defined rules |

### Integration with Undo/Redo

Validation rule changes should be tracked in undo/redo:

```typescript
// Example descriptions for validation changes
get().pushToHistory('Add required validation to Email');
get().pushToHistory('Remove minLength rule from Name');
get().pushToHistory('Update phone format to Australian');
```

---

## 🔍 Implementation Review & Gap Analysis

### Context: Toolbox Panel

**Current State (`ComponentSidebar.tsx`):**
- ✅ Retrieves `globalStyles` from store via `useBuilderStore`
- ✅ Computes `fieldStyles` using `computeFieldStyles(globalStyles)`
- ✅ Passes `fieldStyles` and `defaultObjectLayout` to preview components (legacy removed)
- ✅ React re-renders when store state changes

**Gaps Identified:**
| Gap | Description | Priority |
|-----|-------------|----------|
| Text Length Indicator | ✅ Visible on toolbox + canvas for free-form typing fields only (`first-name`, `email`, `address`, `text`, `textarea`) | Done |
| Explicit Re-render | No explicit subscription to global style changes (relies on React) | Low |

---

### Context: Global Properties Panel

**Current State (`GlobalStylesPanel.tsx`):**
- ✅ Focus Color section at top
- ✅ Typography & Spacing section with 3 TypographyCards (Label, Input, Help)
- ✅ SpacingDivider between cards for gaps
- ✅ Layout (Legacy) section removed
- ✅ Object Layout section present

**Gaps Identified:**
| Gap | Description | Priority |
|-----|-------------|----------|
| Remove Layout (Legacy) | ✅ Removed from GlobalStylesPanel | Done |
| Property Naming | Uses "default" prefix (e.g., `defaultObjectLayout`) - should be "component" | Medium |
| HasBorder Checkbox | No explicit checkbox - derives from border values | Medium |
| Help Border Properties | Help category has `showBorderOptions={true}` ✅ | Done |
| Horizontal Spacing | Spacing controls don't show both vertical AND horizontal gaps | High |

**Recommended Updates to Typography & Spacing:**

```typescript
// Each TypographyCard should have:
interface CategoryProperties {
    // Font Properties
    fontFamily: string;
    fontSize: number;
    fontWeight: FontWeightValue;
    fontStyle: FontStyleType;
    fontColor: string;  // renamed from 'color'
    
    // Background
    backgroundColor: string;
    
    // Border Properties (with HasBorder checkbox)
    hasBorder: boolean;     // ← NEW: Explicit checkbox
    borderColor: string;
    borderWidth: number;
    borderRadius: number;
}

// Spacing Properties (need both orientations)
interface SpacingProperties {
    // Vertical spacing (label above input)
    labelInputGapVertical: number;    // gap when layout is vertical
    inputHelpGapVertical: number;
    
    // Horizontal spacing (label beside input)
    labelInputGapHorizontal: number;  // gap when layout is horizontal
}
```

---

### Context: Multi-Component Selection

**Current State (`PropertiesPanel.tsx` lines 389-537):**
- ✅ Shows selection count and type breakdown
- ✅ Bulk edit: Required toggle, Layout buttons, Component Scale slider
- ✅ AppearanceSection for shared styling
- ✅ Merge helper for style overrides

**Gaps Identified:**
| Gap | Description | Priority |
|-----|-------------|----------|
| Limited Properties | Could expose more shared properties (label, width, etc.) | Low |
| Object Layout | Multi-select doesn't support objectLayout bulk edit | Medium |

---

### Context: Single Component Selection

**Current State (`PropertiesPanel.tsx` lines 542-727):**
- ✅ Full property editing for selected component
- ✅ Component-specific sections (Button, Terms, Textarea, Options, Date, Divider)
- ✅ GeneralSection, ValidationSection, ObjectLayoutSection, AppearanceSection
- ✅ Debug info (ID, Position, Export name)

**Gaps Identified:**
| Gap | Description | Priority |
|-----|-------------|----------|
| Property Naming | Uses `defaultObjectLayout` terminology | Medium |
| Text Length Indicator | ✅ Visible on canvas for free-form typing fields only (`first-name`, `email`, `address`, `text`, `textarea`) | Done |

---

### Context: Canvas Components

**Current State (`SortableComponent.tsx`):**
- ✅ Components render via UniversalFieldShell
- ✅ Resize handles attached
- ✅ SmartBorder for collision/drag
- ✅ Properties update immediately via store

**Gaps Identified:**
| Gap | Description | Priority |
|-----|-------------|----------|
| Text Length Indicator | ✅ Visible on toolbox + canvas for free-form typing fields only (`first-name`, `email`, `address`, `text`, `textarea`) | Done |
| Bidirectional Sync | Panel → Canvas works; Canvas → Panel needs verification | Medium |

---

### Context: Bidirectional Property Sync

**How It Works:**
1. **Panel → Canvas:** 
   - `updateComponentProps(id, updates)` → store update → React re-render
   
2. **Canvas → Panel (Resize handles):**
   - `handleWidthChange`, `handleScaleChange`, etc. → store update
   - PropertiesPanel subscribes to `getSelectedComponent()` → auto-updates

**Status:** ✅ Bidirectional sync should work via Zustand store reactivity.

---

### Context: Text Length Indicator

**Requirement:** Show estimated text-length guidance only for **free-form typing** inputs where the user can type unpredictable content.

**Current State:**
- ✅ Visible on **toolbox + canvas** for: `first-name`, `email`, `address`, `text`, `textarea` (Long Text)\n+- ✅ Not shown for: `dropdown`, `checkbox`, `radio`, `date`, `number`, `phone`, `terms`, `submit-button`, `divider`

**Notes:**\n- The indicator is a **builder-only** visual guide.\n- `maxLength` is used when present; otherwise a sensible default is used per component type (design-time only).

**Placement contract (implemented):**
- The Text Length Indicator’s **green bar** is **anchored to the inner bottom edge** of the input control (inside the border) for **all** indicator-enabled components.
- This ensures consistent placement across short inputs and tall textareas; previously the bar was offset upward by a fixed padding-derived amount, which was more noticeable on short inputs.
- **Implementation detail:** Inputs/selects/textareas are forced to `display: block` in `StyledInput`/`StyledSelect`/`StyledTextarea` to prevent baseline/line-box extra height in the wrapper, ensuring the indicator aligns to the control—not the line box.

---

## 📋 Complete Implementation Checklist

### High Priority
- [x] **Add Text Length Indicator to Canvas** - Only for free-form typing fields (`first-name`, `email`, `address`, `text`, `textarea`)
- [ ] **Two-phase N/S resize** - Height first, then gap (cascading)
- [ ] **Width resize affects object widths** - Proportional to Label/Input/Help
- [ ] **Add HasBorder checkbox** - Explicit toggle for each category
- [ ] **Undo/Redo description field** - Add `description` to FormSnapshot
- [ ] **Object Layout 3-row modal** - Help horizontal placement

### Medium Priority
- [x] **Remove Layout (Legacy)** - Deleted section from GlobalStylesPanel
- [ ] **Rename "default" to "component"** - `defaultObjectLayout` → `componentObjectLayout`
- [ ] **Add horizontal spacing control** - For horizontal layout gap
- [ ] **Object category mapping** - Add `category` field to object definitions
- [ ] **Multi-select objectLayout** - Bulk edit for object layout
- [ ] **Button validation display** - Show ALL failed rules on button

### Low Priority
- [ ] **Explicit global styles subscription** - Ensure toolbox re-renders
- [ ] **Verify bidirectional sync** - Test canvas → panel updates
- [ ] **Expand multi-select properties** - More shared properties

### Post-MVP (Documented)
- [ ] **Company Branding Wizard UI** - Company defaults setup
- [ ] **Form Template System** - Pre-built form templates

---

## 🏗️ Proposed Property Structure

### GlobalStyles (Updated)

```typescript
interface GlobalStyles {
    // Focus/Accent
    primaryColor: string;
    
    // ═══════════════════════════════════════════════════════
    // LABEL CATEGORY
    // ═══════════════════════════════════════════════════════
    labelFontFamily: string;
    labelFontSize: number;
    labelFontWeight: FontWeightValue;
    labelFontStyle: FontStyleType;
    labelColor: string;
    labelBackgroundColor: string;
    labelHasBorder: boolean;          // ← NEW
    labelBorderColor: string;
    labelBorderWidth: number;
    labelBorderRadius: number;
    
    // ═══════════════════════════════════════════════════════
    // INPUT CATEGORY  
    // ═══════════════════════════════════════════════════════
    inputFontFamily: string;          // rename from fontFamily
    inputFontSize: number;            // rename from fontSize
    inputFontWeight: FontWeightValue; // rename from fontWeight
    inputFontStyle: FontStyleType;    // rename from fontStyle
    inputTextColor: string;           // rename from textColor
    inputBackgroundColor: string;
    inputHasBorder: boolean;          // ← NEW
    inputBorderColor: string;
    inputBorderWidth: number;
    inputBorderRadius: number;
    inputHeight: number;
    inputMinHeight: number;
    inputMaxHeight: number;
    placeholderColor: string;
    focusBorderColor: string;
    
    // ═══════════════════════════════════════════════════════
    // HELP CATEGORY
    // ═══════════════════════════════════════════════════════
    helpFontFamily: string;
    helpFontSize: number;
    helpFontWeight: FontWeightValue;
    helpFontStyle: FontStyleType;
    helpTextColor: string;
    helpBackgroundColor: string;
    helpHasBorder: boolean;           // ← NEW
    helpBorderColor: string;
    helpBorderWidth: number;
    helpBorderRadius: number;
    validationColor: string;          // Error text color
    
    // ═══════════════════════════════════════════════════════
    // SPACING (Both orientations)
    // ═══════════════════════════════════════════════════════
    labelInputGapVertical: number;    // When label is above input
    labelInputGapHorizontal: number;  // When label is beside input
    inputHelpGapVertical: number;     // When help is below input
    
    // Min/Max for resize
    labelInputGapMin: number;
    labelInputGapMax: number;
    inputHelpGapMin: number;
    inputHelpGapMax: number;
    
    // ═══════════════════════════════════════════════════════
    // LAYOUT
    // ═══════════════════════════════════════════════════════
    componentObjectLayout: ObjectLayoutType;  // renamed from defaultObjectLayout
    componentLayoutGroups: Record<string, string[]>;
    
    // Base spacing multiplier
    baseSpacing: number;
}
```

---

---

## 🗄️ Big Picture: Database-Driven Configuration

### Overview

The EventLead platform uses a database-driven configuration system that allows:
- **System Defaults:** Hardcoded fallbacks for all properties
- **Company Defaults:** Per-company branding and styling
- **Form Defaults:** Per-form global styles
- **Component Overrides:** Per-component style customizations

### Company Onboarding Flow

```
1. Company Registration
       ↓
2. Company Defaults Setup (Branding Wizard)
   - Company logo & colors
   - Default typography (fonts, sizes)
   - Default component styling (borders, backgrounds)
   - Default layout preferences
       ↓
3. Store in company.CompanyDefaults table
       ↓
4. All new forms inherit Company Defaults
```

### Proposed Database Schema

#### `company.CompanyDefaults`

```sql
CREATE TABLE company.CompanyDefaults (
    CompanyDefaultsID INT IDENTITY(1,1) PRIMARY KEY,
    CompanyID INT NOT NULL REFERENCES company.Company(CompanyID),
    
    -- Brand Colors
    PrimaryColor NVARCHAR(7),           -- e.g., '#3B82F6'
    SecondaryColor NVARCHAR(7),
    AccentColor NVARCHAR(7),
    
    -- Label Category
    LabelFontFamily NVARCHAR(100),
    LabelFontSize INT,
    LabelFontWeight INT,
    LabelFontStyle NVARCHAR(20),
    LabelColor NVARCHAR(7),
    LabelBackgroundColor NVARCHAR(7),
    LabelHasBorder BIT,
    LabelBorderColor NVARCHAR(7),
    LabelBorderWidth INT,
    LabelBorderRadius INT,
    
    -- Input Category
    InputFontFamily NVARCHAR(100),
    InputFontSize INT,
    InputFontWeight INT,
    InputFontStyle NVARCHAR(20),
    InputTextColor NVARCHAR(7),
    InputBackgroundColor NVARCHAR(7),
    InputHasBorder BIT,
    InputBorderColor NVARCHAR(7),
    InputBorderWidth INT,
    InputBorderRadius INT,
    InputHeight INT,
    InputMinHeight INT,
    InputMaxHeight INT,
    PlaceholderColor NVARCHAR(7),
    FocusBorderColor NVARCHAR(7),
    
    -- Help Category
    HelpFontFamily NVARCHAR(100),
    HelpFontSize INT,
    HelpFontWeight INT,
    HelpFontStyle NVARCHAR(20),
    HelpTextColor NVARCHAR(7),
    HelpBackgroundColor NVARCHAR(7),
    HelpHasBorder BIT,
    HelpBorderColor NVARCHAR(7),
    HelpBorderWidth INT,
    HelpBorderRadius INT,
    ValidationColor NVARCHAR(7),
    
    -- Spacing
    LabelInputGapVertical INT,
    LabelInputGapHorizontal INT,
    InputHelpGapVertical INT,
    BaseSpacing INT,
    
    -- Layout
    ComponentObjectLayout NVARCHAR(20),  -- 'vertical' | 'horizontal' | 'mixed'
    ComponentLayoutGroups NVARCHAR(MAX), -- JSON
    
    -- Audit
    CreatedDate DATETIME2 DEFAULT GETUTCDATE(),
    UpdatedDate DATETIME2,
    UpdatedBy INT REFERENCES [user].[User](UserID)
);
```

#### `form.ComponentStructure` (Custom Structures)

```sql
CREATE TABLE form.ComponentStructure (
    ComponentStructureID INT IDENTITY(1,1) PRIMARY KEY,
    CompanyID INT REFERENCES company.Company(CompanyID),
    StructureName NVARCHAR(100) NOT NULL,
    StructureType NVARCHAR(50) NOT NULL,  -- 'custom' | 'template'
    
    -- Structure Definition (JSON)
    Objects NVARCHAR(MAX) NOT NULL,       -- JSON array of ObjectDefinition
    ComponentLayout NVARCHAR(20),
    LayoutGroups NVARCHAR(MAX),           -- JSON
    
    -- Metadata
    IsActive BIT DEFAULT 1,
    CreatedDate DATETIME2 DEFAULT GETUTCDATE(),
    CreatedBy INT REFERENCES [user].[User](UserID)
);
```

### API Endpoints (Proposed)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/companies/{id}/defaults` | GET | Get company defaults |
| `/api/v1/companies/{id}/defaults` | PUT | Update company defaults |
| `/api/v1/forms/{id}/globalStyles` | GET | Get form global styles |
| `/api/v1/forms/{id}/globalStyles` | PUT | Update form global styles |
| `/api/v1/structures` | GET | List available component structures |
| `/api/v1/structures` | POST | Create custom structure |

---

## 📝 Additional Documentation Needed

Based on the big picture requirements, the following documentation should be created:

### 1. Company Onboarding Guide
**File:** `docs/COMPANY-ONBOARDING.md`

| Topic | Description |
|-------|-------------|
| Registration Flow | How companies sign up |
| Branding Setup | Company defaults configuration |
| User Invitation | Adding team members |
| Permissions | Role-based access control |

### 2. Form Builder User Guide
**File:** `docs/FORM-BUILDER-USER-GUIDE.md`

| Topic | Description |
|-------|-------------|
| Canvas Navigation | Zoom, pan, grid snapping |
| Component Library | Available components |
| Drag & Drop | Adding/moving components |
| Resize Handles | Width, height, scale |
| Properties Panel | Styling and configuration |
| Object Layout | Mixed layouts, groups |
| Validation Rules | Built-in and custom |

### 3. Database Schema Reference
**File:** `docs/database-schema.md` (expand existing)

| Addition | Description |
|----------|-------------|
| Company Defaults | `company.CompanyDefaults` table |
| Component Structures | `form.ComponentStructure` table |
| Style Resolution | How styles cascade from DB |

### 4. API Reference
**File:** `docs/API-REFERENCE.md`

| Section | Description |
|---------|-------------|
| Company Defaults API | CRUD for company styling |
| Form Builder API | Form and component endpoints |
| Export/Import API | Form serialization |

### 5. Component Registry Reference
**File:** `docs/COMPONENT-REGISTRY.md`

| Topic | Description |
|-------|-------------|
| Built-in Components | All available components |
| Structure Definitions | Object configurations |
| Category Mappings | Label/Input/Help |
| Custom Components | How to extend |

---

*Last Updated: January 13, 2026*
