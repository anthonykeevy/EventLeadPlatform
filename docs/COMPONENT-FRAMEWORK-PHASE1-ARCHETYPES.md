# Component Framework - Phase 1: Style Archetypes

**Version:** 1.0
**Status:** Implemented
**Related Story:** Phase 1 - Formalize Object Schema

## 🎯 Purpose

The **Style Archetype** system solves the ambiguity problem in the component framework. It provides a deterministic way to style any object within a component structure by explicitly declaring its "visual category" (Archetype), regardless of its functional `type`.

This prevents issues where a `label` type might be styled incorrectly (e.g., looking like a tiny input label when it should be a big header).

---

## 🏗️ The Archetypes

We have defined **5 Core Archetypes** that map directly to the Global Styles system. Every object in a component structure MUST declare one of these.

| Archetype | Maps To (Global Styles) | Intended Use |
| :--- | :--- | :--- |
| **`PrimaryLabel`** | `label*` properties (Font, Color, Border) | The main label for a field. Also used for Headers. |
| **`InputControl`** | `*` (Base) properties (Font, Color, Background) | The actual input element (text, select, radio). |
| **`HelperText`** | `helpText*` properties | Validation messages, help text, status indicators. |
| **`Action`** | Inherits `PrimaryLabel` typography + `PrimaryColor` | Buttons, submit actions, clickable links. |
| **`Divider`** | `border*` properties | Visual separators, horizontal lines. |

---

## 💻 Usage in Component Registry

When defining a component structure in `ComponentRegistry.tsx`, you must now provide the `archetype` property.

### Example: Standard Text Input

```typescript
structure: {
  objects: [
    // This is a label function, styled as a Primary Label
    { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true },
    
    // This is an input function, styled as an Input Control
    { id: 'input', type: 'input', archetype: 'InputControl', required: true },
    
    // This is a validation function, styled as Helper Text
    { id: 'validation', type: 'validation', archetype: 'HelperText', required: false }
  ],
  defaultLayout: 'vertical'
}
```

### Example: Submit Button

```typescript
structure: {
  objects: [
    // This is an action function, styled as an Action (Button)
    { id: 'button', type: 'action', archetype: 'Action', required: true }
  ]
}
```

---

## 🔧 Technical Implementation

### Type Definition (`builder.types.ts`)

```typescript
export type StyleArchetype = 
    | 'PrimaryLabel'
    | 'InputControl'
    | 'HelperText'
    | 'Action'
    | 'Divider';

export interface ComponentObject {
    // ...
    archetype?: StyleArchetype; // Optional for backward compat, but highly recommended
}
```

### Style Resolution (`styleUtils.ts`)

The `computeFieldStyles` function now exposes `getArchetypeStyle(archetype, styles, scale)` helper.

```typescript
// How to use in a renderer:
const styles = computeFieldStyles(globalStyles, overrides);

// Get the specific style for this object's archetype
const objectStyle = getArchetypeStyle(object.archetype, styles.effective, scale);
```

---

## 🚀 Benefits

1.  **Stability:** Adding a new object doesn't break styling logic. The object declares "I look like X", and the system applies Style X.
2.  **Flexibility:** You can mix and match. Want a read-only text field that looks like a Label?
    *   `type: 'input'` (Function: Input)
    *   `archetype: 'PrimaryLabel'` (Style: Label)
3.  **Custom Components:** When we build the Custom Component Builder (future phase), users will simply select "Add Object -> Choose Function -> Choose Look", and this system handles the mapping automatically.



