# Component Framework Guide

**Purpose:** Concise guide for agents implementing component features. Read this before any component-related work.

**Last Updated:** 2026-01-12 (Implementation Complete)

---

## Core Principles

1. **Object-Centric**: Components contain Objects (Label, Input, Validation). Each object has independent sizing/styling.
2. **Global-First**: Set defaults in `GlobalStyles`, override at component level via `props.*Override`.
3. **Surface Parity**: Canvas and Runtime must render identically. Toolbox may use compact rendering.

---

## Standard Objects

| Object | Content | Auto-Sizes To | Override Property |
|--------|---------|---------------|-------------------|
| Label | Known text | Text width + padding | `labelWidthOverride` |
| Input | User types | TextLengthIndicator estimate | `inputWidthOverride` |
| Validation | Known messages | Longest message width | `validationWidthOverride` |
| Action | Button text | Button text width | `buttonWidth` |

---

## Key Files

| Purpose | File |
|---------|------|
| Component registry | `registry/ComponentRegistry.tsx` |
| Layout engine | `components/UniversalFieldShell.tsx` |
| Object renderers | `utils/objectRenderers.tsx` |
| Surface capabilities | `utils/componentSurfaceCapabilities.ts` |
| Feature capabilities | `utils/componentCapabilities.ts` |

---

## Component Props Reference

### Width/Sizing Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `width` | `string` | - | Component container width (e.g., `'300px'`, `'100%'`) |
| `inputWidthOverride` | `number` | `undefined` | Input object fixed width (px). `undefined` = auto-size. |
| `labelWidthOverride` | `number` | `undefined` | Label object fixed width (px). `undefined` = auto-size. |
| `validationWidthOverride` | `number` | `undefined` | Validation object fixed width (px). `undefined` = auto-size. |
| `inputHeightOverride` | `number` | `undefined` | Input height override (px). |
| `height` | `number` | - | Textarea height (px). |
| `componentScale` | `number` | `100` | Proportional scale 50-200%. |

### Initial State Properties (NEW)

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `initialVisibility` | `'visible' \| 'hidden'` | `'visible'` | Starting visibility. Logic rules can override. |
| `initialEnabled` | `'enabled' \| 'disabled'` | `'enabled'` | Starting enabled state. Logic rules can override. |

**Canvas behavior**: Hidden components show at 50% opacity with "Hidden" badge.
**Runtime behavior**: Hidden components are not rendered.

### Button Properties

| Property | Type | Values | Description |
|----------|------|--------|-------------|
| `buttonWidth` | `string` | `'auto'`, `'full'` | Button sizing mode. |
| `buttonAlign` | `string` | `'left'`, `'center'`, `'right'` | Button alignment in container. |

---

## Surface Style Parity Contract

**Rule**: Properties must be applied identically on Canvas and Runtime.

### surfaceStyles Capability

Add to `componentSurfaceCapabilities.ts`:

```typescript
surfaceStyles: {
  applyComponentWidth: boolean;      // Apply props.width to container
  applyButtonStyling: boolean;       // Apply buttonWidth/buttonAlign
  applyLabelWidth: boolean;          // Apply labelWidthOverride
  applyInputWidthOverride: boolean;  // Apply inputWidthOverride
}
```

### Surface Defaults

| Surface | applyComponentWidth | applyButtonStyling | applyLabelWidth | applyInputWidthOverride |
|---------|---------------------|--------------------|-----------------|--------------------------| 
| Toolbox | No | Yes | No | No |
| Canvas | Yes | Yes | Yes | Yes |
| Runtime | Yes | Yes | Yes | Yes |

### Fixing WYSIWYG Issues

1. Find where property is applied in `PublicFormArtboard.tsx` (runtime)
2. Ensure same logic exists in `SortableComponent.tsx` (canvas)
3. Use `surfaceStyles` capability to gate the application

---

## Form-Level Validation Context

**Problem**: Submit button needs access to all form validation errors.

### FormValidationContext Interface

```typescript
interface FormValidationContext {
  errors: Record<string, string>;           // All errors by component ID
  errorsByPriority: Array<{                 // Sorted by tabOrder
    componentId: string; 
    error: string; 
    tabOrder: number; 
  }>;
  firstError?: string;                      // First error for display
  errorCount: number;                       // Total count
}
```

### Implementation

1. Build `formValidationContext` in `PublicFormArtboard.tsx` after validation runs
2. Pass via `runtimeMode.formValidationContext` to submit button's `UniversalFieldShell`
3. Display `firstError` in submit button's validation object

---

## Component Capabilities

Add to `componentCapabilities.ts`:

```typescript
interface ComponentCapabilities {
  // Existing
  supportsObjectLayout: boolean;
  supportsTextLengthIndicator: boolean;
  
  // NEW
  supportsExportName: boolean;
  supportsTabOrder: boolean;
  supportsInitialState: boolean;
}
```

### Usage in Properties Panel

```typescript
const caps = getComponentCapabilities(component.type);

{caps.supportsExportName && <ExportNameControl />}
{caps.supportsInitialState && <InitialStateControls />}
```

---

## Drag Preview (Divider Fix)

**Problem**: Divider has no visual during drag.

### Solution

Add `dragPreview` to surface capabilities:

```typescript
dragPreview: {
  enabled: boolean;
  type: 'snapshot' | 'placeholder';
}
```

For divider: `type: 'placeholder'` renders a simple line placeholder.

---

## Implementation Checklist

### Phase 1: WYSIWYG (Issues 2, 3, 9) - COMPLETE
- [x] Add `surfaceStyles` to ComponentSurfaceCapabilities
- [x] Apply `width` in SortableComponent.tsx matching PublicFormArtboard.tsx
- [x] Apply `buttonWidth`/`buttonAlign` in action renderer for both surfaces

### Phase 2: Validation (Issue 7) - COMPLETE
- [x] Build `formValidationContext` in PublicFormArtboard.tsx
- [x] Pass context via `RuntimeComponentProps` to submit button
- [x] Display firstError on submit button (via objectRenderers.tsx)

### Phase 3: Properties (Issues 10, 11) - COMPLETE
- [x] Add `initialVisibility`/`initialEnabled` to ComponentProps type
- [x] Add UI controls in GeneralSection.tsx (gated by capabilities)
- [x] Add `supportsExportName`/`supportsTabOrder`/`supportsInitialState` to capabilities

### Phase 4: Polish (Issues 8, 13) - COMPLETE
- [x] SmartBorder uses `shrink-to-content` by default for proper sizing
- [x] Add drag preview capability for divider (placeholder type)

---

## Golden Rules

1. **No ad-hoc margins/padding** - Use layout engine, not inline hacks
2. **Surface-gate builder visuals** - TextLengthIndicator, resize handles only on canvas
3. **Canvas = Runtime** - If it looks different, it's a bug
4. **Width overrides are px** - Return `undefined` for auto-sizing, number for fixed
5. **Check capabilities before showing UI** - Don't show controls for unsupported features

---

## Quick Debug

| Symptom | Check |
|---------|-------|
| Canvas differs from Runtime | Compare property application in SortableComponent vs PublicFormArtboard |
| Width not applied | Is `surfaceStyles.applyComponentWidth` true for the surface? |
| Object too wide/narrow | Is `*WidthOverride` set? Check auto-sizing logic. |
| Component hidden unexpectedly | Check `initialVisibility` and logic rules |
| Validation not showing | Is `formValidationContext` passed? Check conditional rendering. |

---

*This guide supersedes COMPONENT-FRAMEWORK-IMPROVEMENTS.md and COMPONENT-FRAMEWORK-ADDITIONS.md*
