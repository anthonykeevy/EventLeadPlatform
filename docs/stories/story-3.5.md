# Story 3.5: Properties Panel & Configuration

**Epic:** 3 - Form Builder & Logic Engine  
**Domain:** Visual Builder  
**Status:** ✅ Complete  
**Priority:** High  

---

## 📖 User Story

**As a** Form Designer,  
**I want to** click on any component on the canvas and edit its properties (Label, Placeholder, Validation Rules) in a dedicated right sidebar,  
**So that** I can configure each form element precisely without leaving the visual editing context.

**Context & Entry Point:**  
The user has already:
1. Entered the Builder (Route: `/forms/:formId/builder`).
2. Dragged at least one component from the Toolbox (Left Sidebar) onto the Canvas.
3. They now want to *configure* the selected component.

**Sidebar Layout:**
- **Left Panel:** Toolbox (Component Library) - *Implemented in Story 3.4*.
- **Center:** Canvas with draggable components - *Implemented in Story 3.4*.
- **Right Panel:** **Properties Panel (This Story)** - "The Inspector."

---

## 🎯 Strategic Vision: "Brand DNA" System

### The Business Case
Marketing departments invest significant effort creating **Brand Guidelines** - precise specifications for colors, fonts, spacing, and visual identity. This story lays the foundation for a **"One-Time Setup, Perpetual Value"** system:

1. **Form-Level Global Styles** (This Story): Set defaults that apply to all components.
2. **Component-Level Overrides** (This Story): Fine-tune individual components when needed.
3. **Company Brand Profile** (Future): Import brand guidelines once per company.

**Result:** The platform becomes **sticky** because creating new forms takes seconds - the "Brand DNA" is already embedded. The detailed work is done **once**.

---

## 📐 Property Specification

**Full Specification:** `docs/stories/STORY-3.5-PROPERTY-SPEC.md`

This document defines 50+ controllable properties across 8 categories:
- **Typography** (fonts, sizes, weights)
- **Colors** (brand, text, borders, states)
- **Spacing** (margins, padding, gaps - using proportional multipliers)
- **Borders & Shapes** (radius, width, shadows)
- **Sizing** (dimensions, scale factor)
- **Layout** (orientation, alignment)
- **Behavior** (labels, placeholders, states)
- **Validation** (rules, patterns, messages)

---

## 🎯 User Concerns Addressed

### 1. Global vs. Individual Settings
> *"I need to set the font size for ALL inputs globally, but sometimes override just one."*

- **Global Styles Tab:** Define default values (Font, Size, Spacing, Colors) that apply to all components.
- **Individual Overrides:** Each component's properties panel shows inherited global values with an "Override" toggle.
- **Reset to Global:** A "Reset to Default" action clears individual overrides.

### 2. Layout Toggles
> *"I need to switch a single component between Vertical and Horizontal label layout."*

- **Layout Control:** Dropdown or toggle switch in the Properties Panel for supported components.
- **Options:** `Vertical` (Label on top) | `Horizontal` (Label on left).

### 3. Proportional Scaling
> *"If a user changes the size of a component, do padding and font size scale automatically?"*

- **Component Scale Factor:** A `componentScale` property (default 100%) that proportionally scales:
  - Font sizes (label, input, help text)
  - Padding (horizontal and vertical)
  - Border radius
  - Input height
- **Explicit Override:** Users can "break" proportional scaling by setting an explicit value on any individual property.

### 4. Spacing Consistency
> *"Spacing controls will be important, especially at a global level."*

- **Base Spacing Unit:** All spacing derives from a single `baseSpacing` value (default 8px).
- **Multipliers:** Properties like `componentMargin`, `labelGap`, `inputPaddingX` use multipliers (e.g., 2× = 16px).
- **Proportional Updates:** Changing `baseSpacing` automatically scales all related spacing values.

---

## ✅ Acceptance Criteria

### 1. Selection & Indicator
- [x] Clicking a component on the canvas selects it and highlights it with a visual indicator (e.g., thicker/colored Skyline border, resize handles).
- [x] The `selectedComponentId` is stored in `useBuilderStore`.
- [x] Clicking empty canvas area deselects the component (`selectedComponentId = null`).
- [x] Only one component can be selected at a time.

### 2. Properties Panel (Right Sidebar)
- [x] When a component is selected, the Right Sidebar displays the **Properties Panel** for that component type.
- [x] When nothing is selected, the Right Sidebar displays a "Select a component to edit" placeholder OR a **Global Styles** editor.
- [x] The panel title reflects the component type (e.g., "Text Input Properties", "First Name Properties").

### 3. Standard Property Editors (All Inputs)
The following fields must be editable for all input components:
- [x] **Label** (Text input) - The field's visible question/name.
- [x] **Required** (Toggle/Checkbox) - Whether the field is mandatory.
- [x] **Placeholder** (Text input) - Hint text inside the input.
- [x] **Help Text** (Text input) - Descriptive text below the field.
- [x] **Layout** (Dropdown: `Vertical` | `Horizontal`) - Label position relative to input.

### 4. Validation Rules Panel
- [x] A dedicated "Validation" accordion/section in the Properties Panel.
- [x] **Text Inputs:** Min Length, Max Length, Pattern (Regex).
- [x] **Number Inputs:** Min Value, Max Value.
- [x] **Email/URL:** Pre-filled patterns (read-only informational).
- [x] Custom validation error message field.

### 5. Global vs. Individual Control (The Theme System)
- [x] **Global Styles Tab:** Accessible when nothing is selected, OR via a "Theme" tab in the Properties Panel.
- [x] Global Styles include:
    - `fontFamily` (Dropdown: Inter, Roboto, Open Sans, etc.)
    - `fontSize` (Number input, pixels)
    - `primaryColor` (Color picker)
    - `textColor` (Color picker)
    - `borderRadius` (Number input, pixels)
    - `spacing` (Number input, pixels)
- [x] **"Use Global" Indicator:** Each property in the component editor shows a subtle indicator (icon or checkbox) if it's using the global value.
- [x] **Override Toggle:** Clicking the indicator or editing the value unlocks individual customization.
- [x] **Reset to Global:** A "Reset" button reverts the property to the global default.

### 6. Real-Time Preview
- [x] Changes in the Properties Panel are reflected **instantly** on the canvas (no "Apply" button needed).
- [x] State updates flow through `useBuilderStore.updateComponent()`.

### 7. Component-Specific Panels (Extensibility)
- [x] Architecture supports different property sections for different component types (type-aware rendering and property availability).
- [x] The `ComponentRegistry` maps each `type` to a Canvas render component and default props; the Properties Panel renders type-relevant controls from the component's props.

---

## 🛠️ Technical Notes

### State Management

**New Store Properties:**
```typescript
interface BuilderState {
  // ... existing ...
  selectedComponentId: string | null;     // The ID of the clicked component
  globalStyles: GlobalStyles;             // Master theme defaults
  
  // Actions
  selectComponent: (id: string | null) => void;
  updateGlobalStyles: (updates: Partial<GlobalStyles>) => void;
  resetPropertyToGlobal: (componentId: string, property: string) => void;
}
```

### Component Architecture

**Properties Panel Structure:**
```
<PropertiesPanel>
  ├── <PanelHeader title={componentType} />
  ├── <GeneralSection>
  │     ├── LabelInput
  │     ├── PlaceholderInput
  │     ├── RequiredToggle
  │     ├── HelpTextInput
  │     └── LayoutDropdown (Vertical/Horizontal)
  └── <ValidationSection>
  │     ├── MinLength / MaxLength
  │     ├── PatternInput
  │     └── CustomErrorMessage
  └── <StyleOverridesSection>
        ├── FontFamilyPicker (with "Use Global" toggle)
        ├── FontSizePicker (with "Use Global" toggle)
        └── ColorPickers (with "Use Global" toggle)
```

**Global Theme Cascade:**
- Global styles stored in `formDefinition.globalStyles`.
- Component props override globals: `effectiveValue = component.props[key] ?? globalStyles[key]`.
- "Reset to Global" action: `delete component.props[key]` or set to `undefined`.

### Component Registry Extension

```typescript
interface ComponentDefinition {
  type: ComponentType;
  label: string;                       // Display name in Toolbox
  icon: React.ComponentType;           // Toolbox icon
  RenderComponent: React.ComponentType;  // Canvas renderer
  PropertiesEditor: React.ComponentType; // Properties Panel (NEW)
  defaultProps: ComponentProps;
}
```

### Keyboard Accessibility
- `Escape` key deselects the current component.
- `Tab` navigates through Properties Panel fields.
- `Enter` in a text field commits and moves to next field.

---

## 📋 Dependencies

- **Story 3.3:** Canvas foundation with dnd-kit.
- **Story 3.4:** Component Library, Toolbox, Skyline Borders.
- **Existing:** `useBuilderStore`, `ComponentRegistry`, `FormComponent` types.

---

## 📚 Related Documentation

| Document | Purpose |
|----------|---------|
| `STORY-3.5-PROPERTY-SPEC.md` | Complete property specification (50+ properties, 8 categories) |
| `STORY-3.5-UAT-TEST-GUIDE.md` | User acceptance test scenarios |
| `story-context-3.5.xml` | Technical implementation context |
| `EPIC-3-ARCHITECTURE-REF.md` | Overall Epic 3 architecture |
| `BUILDER-GLOSSARY.md` | Visual Builder terminology |

---

## 🧪 UAT Test Guide

**Full Guide:** `docs/stories/STORY-3.5-UAT-TEST-GUIDE.md`

### Test Categories

1. **Selection Tests**
   - Click to select, click away to deselect
   - Visual indicator appears/disappears correctly
   - Only one component selected at a time

2. **Property Editing Tests**
   - Edit Label → Canvas updates immediately
   - Edit Placeholder → Input shows new placeholder
   - Toggle Required → Validation indicator appears
   - Change Layout → Component re-renders in new orientation

3. **Global vs. Individual Tests**
   - Change Global Font Size → All components update
   - Override one component's Font Size → Only that one changes
   - Reset to Global → Component reverts to global value
   - Visual indicator shows "Using Global" vs "Overridden"

4. **Validation Rules Tests**
   - Set Min/Max Length → Verify in preview mode
   - Set Pattern → Verify regex matching
   - Custom error message displays correctly

5. **Accessibility Tests**
   - Escape key deselects component
   - Tab navigation in Properties Panel
   - Screen reader announces panel sections

---

## 📋 Completion Criteria

- [x] All Acceptance Criteria checkboxes are completed.
- [x] UAT Test Guide created and all tests pass.
- [x] No console errors or TypeScript warnings.
- [x] Properties Panel is responsive (collapses gracefully).
- [x] Story 3.5 status updated to ✅ Complete in EPIC-3-STATUS.md.

---

## ✅ Completion Report

**Completed:** 2025-12-12  
**UAT:** ✅ PASSED — `docs/stories/STORY-3.5-UAT-TEST-GUIDE.md` (62 tests)  

### Delivered Outcomes
- **Properties Panel**: Component selection drives context-sensitive editing; Global Styles shown when nothing selected.
- **Global vs Overrides**: Form-level `globalStyles` with per-component `styleOverrides` + reset-to-global behavior.
- **Dimensions & Resizing**: Width presets (including %), auto-fit width, scale control, and handle-specific resizing (corners=scale, E/W=width, N/S=spacing/height rules).
- **Multi-select Bulk Edit**: Ctrl+Click selection + bulk editing for supported properties/overrides.
- **Undo/Redo**: Captures add/move/resize and property edits (single, bulk, global) with a bounded history.
- **Quality-of-life**: “Use suggested” for Export Field Name; transparent background preview swatch; consistent typography controls.

### Key Implementation Touchpoints
- `frontend/src/features/builder/components/PropertiesPanel.tsx`
- `frontend/src/features/builder/stores/useBuilderStore.ts`
- `frontend/src/features/builder/components/SortableComponent.tsx`
- `frontend/src/features/builder/components/properties/*`
- `frontend/src/features/builder/components/fields/StandardInput.tsx`
- `frontend/src/features/builder/utils/styleUtils.ts`

### Follow-ups (Story 3.6+)
- Add a dedicated **Logic** tab for conditional visibility rules and rule authoring UI (Story 3.6).

## 📝 Next Steps (Story 3.6 Preview)

After the Properties Panel is complete, Story 3.6 will introduce the **Conditional Logic UI** - allowing users to define rules like "Show Field X if Field Y equals 'Yes'". The Properties Panel will gain a new "Logic" tab for configuring visibility conditions.

