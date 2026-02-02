# Component Framework V2 Specification

**Purpose:** Define a scalable, object-centric component framework that supports hundreds of components with consistent rendering across all surfaces.

**Created:** 2026-01-13

---

## 1. Executive Summary

The Component Framework V2 is designed around three core principles:

1. **Object-Centric**: Components are containers for Objects, each with independent controls
2. **Global-First**: 80% of users achieve desired results using Global Settings alone
3. **Surface Parity**: Same properties render identically on Toolbox, Canvas, and Runtime

---

## 2. Architecture Overview

### 2.1 Component Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Form Definition                                  │
├─────────────────────────────────────────────────────────────────────────┤
│  globalStyles: GlobalStyles     ← Default values for ALL objects        │
│  components: FormComponent[]                                            │
│      └── props: ComponentProps  ← Component-level overrides             │
│          └── objectOverrides: ObjectOverrides[] ← Per-object overrides  │
│              ├── labelOverrides                                         │
│              ├── inputOverrides                                         │
│              └── validationOverrides                                    │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Style Resolution Pipeline

```
                    ┌─────────────────┐
                    │ System Defaults │  Hardcoded fallbacks
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Global Settings │  User's form-wide defaults
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Component Props │  Per-component overrides
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Object Overrides│  Per-object overrides
                    └────────┬────────┘
                             ↓
            ┌────────────────┴────────────────┐
            ↓                ↓                ↓
       ┌─────────┐     ┌─────────┐     ┌─────────┐
       │ Toolbox │     │ Canvas  │     │ Runtime │
       └─────────┘     └─────────┘     └─────────┘
       
       ALL surfaces use the SAME resolution pipeline
```

---

## 3. Object Model

### 3.1 Standard Objects

Every component can have up to 5 standard object types:

| Object Type | Purpose | Auto-Sizing | User Controls |
|-------------|---------|-------------|---------------|
| `label` | Field label/header | Based on text content | Width, padding |
| `input` | User input control | TextLengthIndicator for text | Width, height, padding |
| `validation` | Error/help messages | Based on longest message | Padding only |
| `action` | Buttons/actions | Based on button text | Width, padding |
| `status` | Status indicators | Fixed/minimal | None |

### 3.2 Object Properties Schema

Each object can have these properties (overridable at any level):

```typescript
interface ObjectProperties {
  // ═══════════════════════════════════════════
  // SIZING
  // ═══════════════════════════════════════════
  
  /** Width mode: how the object determines its width */
  widthMode: 'auto' | 'fixed' | 'fill' | 'percentage';
  
  /** Width value (used when widthMode is 'fixed' or 'percentage') */
  width?: number | string; // e.g., 200 (px) or '50%'
  
  /** Minimum width (prevents shrinking below this) */
  minWidth?: number;
  
  /** Maximum width (prevents growing beyond this) */
  maxWidth?: number;
  
  /** Height (primarily for input objects) */
  height?: number;
  
  /** Minimum height */
  minHeight?: number;
  
  /** Maximum height */
  maxHeight?: number;
  
  // ═══════════════════════════════════════════
  // PADDING (inside the object, between content and border)
  // ═══════════════════════════════════════════
  
  /** Padding inside the object (all sides) */
  padding?: number;
  
  /** Horizontal padding (left and right) */
  paddingX?: number;
  
  /** Vertical padding (top and bottom) */
  paddingY?: number;
  
  // ═══════════════════════════════════════════
  // SPACING (outside the object, between objects)
  // ═══════════════════════════════════════════
  
  /** Gap after this object (to next object) */
  gapAfter?: number;
  
  // ═══════════════════════════════════════════
  // BORDER
  // ═══════════════════════════════════════════
  
  /** Whether to show border */
  hasBorder?: boolean;
  
  /** Border color */
  borderColor?: string;
  
  /** Border width */
  borderWidth?: number;
  
  /** Border radius */
  borderRadius?: number;
  
  // ═══════════════════════════════════════════
  // TYPOGRAPHY
  // ═══════════════════════════════════════════
  
  /** Font family */
  fontFamily?: string;
  
  /** Font size */
  fontSize?: number;
  
  /** Font weight */
  fontWeight?: number | string;
  
  /** Font style (normal, italic) */
  fontStyle?: 'normal' | 'italic';
  
  /** Text color */
  textColor?: string;
  
  /** Background color */
  backgroundColor?: string;
  
  /** Text alignment */
  textAlign?: 'left' | 'center' | 'right';
}
```

### 3.3 Property Scope Matrix

This matrix defines where each property can be set:

| Property | Global | Component | Object | Notes |
|----------|--------|-----------|--------|-------|
| `fontFamily` | ✅ Per-category | ✅ | ✅ | Global has Label/Input/Help categories |
| `fontSize` | ✅ Per-category | ✅ | ✅ | |
| `fontWeight` | ✅ Per-category | ✅ | ✅ | |
| `textColor` | ✅ Per-category | ✅ | ✅ | |
| `backgroundColor` | ✅ Per-category | ✅ | ✅ | |
| `borderWidth` | ✅ Per-category | ✅ | ✅ | |
| `borderColor` | ✅ Per-category | ✅ | ✅ | |
| `borderRadius` | ✅ Per-category | ✅ | ✅ | |
| `padding` | ✅ Per-category | ✅ | ✅ | |
| `paddingX` | ✅ Per-category | ✅ | ✅ | |
| `paddingY` | ✅ Per-category | ✅ | ✅ | |
| `widthMode` | ❌ | ✅ | ✅ | Component/Object level only |
| `width` | ❌ | ✅ | ✅ | Component/Object level only |
| `height` | ❌ | ✅ | ✅ | Component/Object level only |
| `gapAfter` | ✅ (labelGap, etc.) | ✅ | ✅ | Global has named gaps |

---

## 4. Global Settings Structure

### 4.1 Current GlobalStyles (to be enhanced)

```typescript
interface GlobalStyles {
  // ═══════════════════════════════════════════
  // OBJECT CATEGORY DEFAULTS (existing)
  // ═══════════════════════════════════════════
  
  // Label Category
  labelFontFamily: string;
  labelFontSize: number;
  labelFontWeight: number;
  labelColor: string;
  labelBackgroundColor: string;
  labelBorderWidth: number;
  labelBorderColor: string;
  labelBorderRadius: number;
  labelPaddingX: number;      // NEW
  labelPaddingY: number;      // NEW
  
  // Input Category
  inputFontFamily: string;
  inputFontSize: number;
  inputFontWeight: number;
  inputTextColor: string;
  inputBackgroundColor: string;
  inputBorderWidth: number;
  inputBorderColor: string;
  inputBorderRadius: number;
  inputPaddingX: number;
  inputPaddingY: number;
  inputHeight: number;        // Default input height
  
  // Validation/Help Category
  helpFontFamily: string;
  helpFontSize: number;
  helpFontWeight: number;
  helpTextColor: string;
  helpBackgroundColor: string;
  helpBorderWidth: number;
  helpBorderColor: string;
  helpBorderRadius: number;
  helpPaddingX: number;       // NEW
  helpPaddingY: number;       // NEW
  
  // ═══════════════════════════════════════════
  // SPACING DEFAULTS (enhanced)
  // ═══════════════════════════════════════════
  
  /** Gap between Label and Input objects */
  labelInputGap: number;
  
  /** Gap between Input and Validation objects */
  inputValidationGap: number;
  
  /** Base spacing unit for calculations */
  baseSpacing: number;
  
  // ═══════════════════════════════════════════
  // AUTO-SIZING DEFAULTS (NEW)
  // ═══════════════════════════════════════════
  
  /** Default width mode for Label objects */
  labelDefaultWidthMode: 'auto' | 'fixed' | 'fill';
  
  /** Default width mode for Input objects */
  inputDefaultWidthMode: 'auto' | 'fill';
  
  /** Default width mode for Validation objects */
  validationDefaultWidthMode: 'auto' | 'fill';
}
```

### 4.2 New: Object Overrides at Component Level

```typescript
interface ComponentProps {
  // ... existing props ...
  
  /**
   * Per-object property overrides.
   * Allows customizing individual objects without affecting others.
   */
  objectOverrides?: {
    label?: Partial<ObjectProperties>;
    input?: Partial<ObjectProperties>;
    validation?: Partial<ObjectProperties>;
    action?: Partial<ObjectProperties>;
    status?: Partial<ObjectProperties>;
  };
}
```

---

## 5. Style Resolution Function

### 5.1 Unified Resolver

```typescript
/**
 * Resolves final properties for an object, applying the cascade:
 * System Defaults → Global Settings → Component Props → Object Overrides
 */
function resolveObjectProperties(
  objectType: 'label' | 'input' | 'validation' | 'action' | 'status',
  globalStyles: GlobalStyles,
  componentProps: ComponentProps,
  objectOverrides?: Partial<ObjectProperties>
): ObjectProperties {
  
  // Step 1: Get system defaults for this object type
  const systemDefaults = SYSTEM_DEFAULTS[objectType];
  
  // Step 2: Get global settings for this object category
  const categoryKey = OBJECT_TO_CATEGORY[objectType]; // e.g., 'label' → 'label', 'input' → 'input', 'validation' → 'help'
  const globalSettings = extractCategorySettings(globalStyles, categoryKey);
  
  // Step 3: Get component-level styleOverrides
  const componentOverrides = componentProps.styleOverrides || {};
  
  // Step 4: Get object-level overrides
  const specificOverrides = objectOverrides || {};
  
  // Step 5: Merge with priority (later wins)
  return deepMerge(
    systemDefaults,
    globalSettings,
    componentOverrides,
    specificOverrides
  );
}
```

### 5.2 Surface-Agnostic Rendering

```typescript
/**
 * All surfaces use the same rendering logic.
 * Surface differences are handled by ComponentSurfaceCapabilities.
 */
function renderObject(
  object: ComponentObject,
  resolvedProps: ObjectProperties,
  surface: 'toolbox' | 'canvas' | 'runtime',
  capabilities: ComponentSurfaceCapabilities
): React.ReactNode {
  
  // Apply surface-specific adjustments (e.g., toolbox uses compact mode)
  const surfaceAdjustedProps = applySurfaceAdjustments(
    resolvedProps,
    surface,
    capabilities
  );
  
  // Render using the object type's renderer
  return ObjectRenderers[object.type](surfaceAdjustedProps);
}
```

---

## 6. Auto-Sizing Intelligence

### 6.1 Label Object Auto-Sizing

```typescript
function calculateLabelWidth(
  labelText: string,
  properties: ObjectProperties
): number {
  // Measure text width using canvas
  const textWidth = measureTextWidth(
    labelText,
    properties.fontFamily,
    properties.fontSize,
    properties.fontWeight
  );
  
  // Add padding and border
  const totalWidth = textWidth 
    + (properties.paddingX * 2) 
    + (properties.borderWidth * 2);
  
  // Apply constraints
  return Math.max(
    properties.minWidth || 0,
    Math.min(properties.maxWidth || Infinity, totalWidth)
  );
}
```

### 6.2 Input Object Auto-Sizing

```typescript
function calculateInputWidth(
  component: FormComponent,
  properties: ObjectProperties
): number {
  const maxLength = component.props.validation?.maxLength;
  
  if (maxLength && properties.widthMode === 'auto') {
    // Use TextLengthIndicator logic
    return estimateCharacterWidth(maxLength, {
      fontFamily: properties.fontFamily,
      fontSize: properties.fontSize,
      fontWeight: properties.fontWeight,
    });
  }
  
  // Fall back to fixed or fill mode
  return properties.width || 200; // Default
}
```

### 6.3 Validation Object Auto-Sizing

```typescript
function calculateValidationWidth(
  component: FormComponent,
  properties: ObjectProperties
): number {
  // Get all possible validation messages
  const messages = [
    component.props.validationMessage,
    component.props.helpText,
    // Add other potential messages
  ].filter(Boolean);
  
  if (messages.length === 0) {
    return 0; // No space needed if no messages
  }
  
  // Find longest message
  const longestMessage = messages.reduce((a, b) => 
    a.length > b.length ? a : b
  );
  
  // Calculate width for longest message
  return measureTextWidth(
    longestMessage,
    properties.fontFamily,
    properties.fontSize,
    properties.fontWeight
  ) + (properties.paddingX * 2);
}
```

---

## 7. Properties Panel Controls

### 7.1 Object-Level Width Controls

Add to Properties Panel → Appearance → Dimensions:

```
┌─────────────────────────────────────────────────────────────────┐
│ Dimensions                                                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Component Width:  [========= 75% =========] ▼ % / px           │
│                                                                  │
│  ── Object Widths ──────────────────────────────────            │
│                                                                  │
│  Label:    ○ Auto   ○ Fixed [120px]   ○ Fill                    │
│  Input:    ○ Auto   ○ Fixed [200px]   ○ Fill                    │
│  Validation: ○ Auto (longest message)  ○ Fill                   │
│                                                                  │
│  [↻ Reset to Global Defaults]                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 Object-Level Padding Controls

Add to Properties Panel → Appearance → Spacing:

```
┌─────────────────────────────────────────────────────────────────┐
│ Spacing                                                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ── Object Gaps ──────────────────────────────────              │
│  Label → Input:       [8px] ▼                                   │
│  Input → Validation:  [4px] ▼                                   │
│                                                                  │
│  ── Object Padding ─────────────────────────────────            │
│  Label:    X [12] Y [4]  [Reset]                                │
│  Input:    X [12] Y [8]  [Reset]                                │
│  Validation: X [8] Y [4] [Reset]                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. Global Settings Panel Enhancements

### 8.1 Typography & Spacing Per Category

The current Typography & Spacing modal should be enhanced:

```
┌─────────────────────────────────────────────────────────────────┐
│ Typography & Spacing - Label                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Font:     [Inter ▼] [14px] [Medium ▼]                          │
│  Color:    [■ #374151] Background: [□ transparent]              │
│  Border:   [□ Add Border] Color: [■ #E5E7EB] Width: [1px]       │
│                                                                  │
│  Padding:  X [12px]  Y [4px]       ← NEW                        │
│                                                                  │
│  Default Width Mode: ○ Auto  ○ Fixed  ○ Fill    ← NEW           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2 Object Layout Defaults

```
┌─────────────────────────────────────────────────────────────────┐
│ Object Layout                                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Default Layout:  ○ Vertical  ○ Horizontal  ○ Mixed             │
│                                                                  │
│  Default Gaps:                                                   │
│    Label → Input:       [8px]                                   │
│    Input → Validation:  [4px]                                   │
│                                                                  │
│  Default Row Alignment: [Center ▼]                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 9. JSONDefinition Storage

### 9.1 Complete Property Storage

The FormDefinition must store all properties needed for accurate recreation:

```typescript
interface FormDefinition {
  // Form metadata
  id: string;
  name: string;
  version: number;
  
  // Global defaults (used by Toolbox and as fallback)
  globalStyles: GlobalStyles;
  
  // Canvas settings
  canvasSettings: CanvasSettings;
  
  // Pages and components
  pages: Page[];
  
  // Each component stores its overrides
  // Component.props.objectOverrides stores per-object settings
}
```

### 9.2 Property Serialization Contract

When saving:
1. Only store properties that **differ from Global Settings**
2. Store null/undefined to explicitly "remove" a global setting
3. Store the exact value to override a global setting

When loading:
1. Apply Global Settings as base
2. Apply Component Props overrides
3. Apply Object Overrides
4. Render the resolved result

---

## 10. Implementation Phases

### Phase 1: Foundation (Fixes Current Issues)
1. Implement unified style resolution function
2. Apply same resolution on all surfaces (fix WYSIWYG issues)
3. Add `objectOverrides` to ComponentProps type

### Phase 2: Object Width Controls
4. Add `widthMode` and `width` to each object type
5. Add UI controls in Properties Panel → Dimensions
6. Implement auto-sizing for Label and Validation objects

### Phase 3: Object Padding Controls
7. Add `paddingX`/`paddingY` to GlobalStyles per category
8. Add UI controls in Properties Panel → Spacing
9. Add UI controls in Global Settings → Typography & Spacing

### Phase 4: Polish & Documentation
10. Update Component Framework Reference
11. Migrate existing components to new schema
12. Add "Reset to Global" buttons throughout

---

## 11. Benefits of This Architecture

| Benefit | Description |
|---------|-------------|
| **Scalability** | New components inherit all framework features automatically |
| **Consistency** | Same resolution logic = same rendering everywhere |
| **Maintainability** | Fix once, works for all components |
| **User Experience** | 80% of users only need Global Settings |
| **Brand Support** | Future: Brand guidelines auto-populate Global Settings |
| **Debugging** | Clear cascade makes issues easy to trace |

---

## 12. Questions for Approval

1. **Object Overrides Location**: Should `objectOverrides` be:
   - A) Top-level in ComponentProps (as proposed)
   - B) Nested under `styleOverrides`
   - C) Separate per object (e.g., `labelWidth`, `inputWidth`)

2. **Global Padding**: Should Global Settings have:
   - A) Single padding value per category (paddingX, paddingY)
   - B) Full padding object (top, right, bottom, left)
   - C) Keep simple for now, add full control later

3. **Auto-Sizing Toggle**: Should auto-sizing be:
   - A) Default ON, user can switch to Fixed
   - B) Default OFF, user can enable
   - C) Depends on object type (Label=Auto, Input=Fill)

4. **Migration Strategy**: For existing forms:
   - A) Auto-migrate on load (calculate objectOverrides from current state)
   - B) Leave as-is, new properties only affect new components
   - C) Prompt user to "Upgrade" form to new schema

---

*This specification should be reviewed and approved before implementation.*
