# Button Controls Synchronization - Review & Requirements

**Date:** 2026-01-28  
**Status:** Requirements Clarification & Documentation Review

## 🔍 Component Framework Reference Review

### Current Documentation Status

**Location:** `docs/COMPONENT-FRAMEWORK-REFERENCE.md`

#### ✅ Clear Sections:
- Line 1153-1164: Submit Button section clearly describes `buttonWidth` behavior
- Line 667: Notes that `buttonWidth` controls button width, `width` controls container sizing
- Line 758-816: Width Resize (E/W Handles) section describes resize behavior for all components

#### ⚠️ Missing/Unclear Information:

1. **Button Settings ↔ Appearance Dimensions Relationship (MISSING)**
   - Current doc says: "Button width is controlled by `buttonWidth` in **Button Settings** (component `width` still controls container sizing)."
   - **Missing:** No mention that `buttonWidth: 'full'` is REQUIRED for percentage widths to work
   - **Missing:** No explanation of how these two controls interact

2. **Component Framework Universality (NEEDS CLARIFICATION)**
   - Line 758-816 describes width resize for "Input" objects, but buttons use "Action" objects
   - **Missing:** Explicit statement that framework applies to all components, with object type differences:
     - Buttons: `action` object (id: 'button')
     - Most components: `input` object
     - Dividers: `divider` object

3. **Horizontal Layout / Multi-Column Considerations (MISSING)**
   - Current doc doesn't mention that width calculations must account for:
     - Objects to left/right of target object (in horizontal/mixed layouts)
     - Multiple columns (grid layout)
     - Component capabilities (surface capabilities, constraints)

4. **Resize Handle Code Sharing (CONFIRMED BUT NOT DOCUMENTED)**
   - ✅ All components use same `ResizeHandles.tsx` component
   - ✅ All components use same `handleWidthChange` in `SortableComponent.tsx`
   - ✅ Button-specific logic is conditional within shared code
   - **Missing:** Explicit documentation that resize handle code is shared/common

## 📋 User Requirements (Re-explained)

### Control Synchronization Requirements

**Current Problem:**
- Button Settings → Button Width must be set to "Full Width" before Appearance → Dimensions → Width percentage values work
- This creates confusion because controls are in different sections

**Required Behavior:**

#### 1. Button Settings → Button Width (2 actions)
- **"Auto (fit content)"** → Should automatically set Appearance → Dimensions → Width to **"Auto"**
- **"Full Width"** → Should automatically set Appearance → Dimensions → Width to **"100%"**

#### 2. Appearance → Dimensions → Width (9 actions)
- **"Auto"** → Uses global width for all objects in component
- **"25%"** → Changes width of button object to 25% of Canvas width
- **"33%"** → Changes width of button object to 33% of Canvas width
- **"50%"** → Changes width of button object to 50% of Canvas width
- **"66%"** → Changes width of button object to 66% of Canvas width
- **"75%"** → Changes width of button object to 75% of Canvas width
- **"100%"** → Changes width of button object to 100% of Canvas width
- **"Custom (px)"** → Sets pixel width of button object to custom value; user can adjust Button Object width

**Note:** For other components (not buttons), replace "button object" with:
- **Input components:** "input object"
- **Divider components:** "divider object"
- **Other object types:** appropriate object type

### Component Framework Universality

**Key Principle:**
- The Component Framework applies to **ALL components**
- The only difference is which **object type** is being sized:
  - Buttons: `action` object (id: 'button')
  - Most inputs: `input` object
  - Dividers: `divider` object
  - Labels: `label` object (rarely resized directly)

**Current Context:**
- Testing is being done on button component in **vertical layout**
- Button width is the only object width we need to be concerned about
- **Future considerations:**
  - If button is in **horizontal layout** or has **multiple columns**, we need to account for:
    - Width of objects to the left/right of the button
    - Grid column calculations
    - Component capabilities (constraints, surface capabilities)

### Resize Handle Code Sharing Confirmation

**Question:** Are resize handles using common/shared code?

**Answer: YES - Confirmed:**

1. **Shared Component:** `frontend/src/features/builder/components/ui/ResizeHandles.tsx`
   - Single component used by ALL components
   - Generic props interface, no component-specific logic

2. **Shared Logic:** `frontend/src/features/builder/components/SortableComponent.tsx`
   - Single `handleWidthChange` function for all components
   - Component-specific logic is conditional (e.g., `if (component.type === 'submit-button')`)
   - Button-specific code is isolated within shared function

3. **Shared Hook:** `frontend/src/features/builder/hooks/useComponentResize.ts`
   - Centralized resize logic
   - Used by all components

**Conclusion:**
- ✅ Resize handle code IS common/shared
- ✅ Button-specific fixes will NOT break other components (as long as conditional logic is correct)
- ⚠️ However, button resize rendering issues suggest there may be button-specific bugs in the shared code

## 🎯 Recommended Documentation Updates

### 1. Add Button Settings ↔ Appearance Dimensions Relationship Section

**Location:** After line 1164 (Submit Button section)

```markdown
### Button Width Control Synchronization

**Current Behavior (to be fixed):**
- `buttonWidth: 'full'` must be set before percentage widths in Appearance → Dimensions → Width work
- This creates user confusion due to controls being in different sections

**Required Behavior:**
- **Button Settings → Button Width "Auto"** → Automatically sets `width: undefined` (Auto)
- **Button Settings → Button Width "Full Width"** → Automatically sets `width: '100%'`
- **Appearance → Dimensions → Width** → Works independently, sets `width` and `actionWidthOverride` appropriately
```

### 2. Clarify Component Framework Universality

**Location:** Add to "Core mental model" section (around line 13)

```markdown
- **Object-Centric Design**: Components are composed of objects (Label, Input, Action, Validation, Divider) with individual sizing and styling. The framework applies universally to all components; only the target object type differs:
  - Buttons: `action` object (id: 'button')
  - Input components: `input` object
  - Dividers: `divider` object
```

### 3. Document Resize Handle Code Sharing

**Location:** Add to "Resize Handle Behavior" section (around line 729)

```markdown
### Resize Handle Implementation (Shared Code)

**All components use the same resize handle implementation:**
- **Component:** `frontend/src/features/builder/components/ui/ResizeHandles.tsx` (shared)
- **Logic:** `frontend/src/features/builder/components/SortableComponent.tsx` → `handleWidthChange` (shared)
- **Hook:** `frontend/src/features/builder/hooks/useComponentResize.ts` (shared)

**Component-specific behavior:**
- Component-specific logic is handled via conditional checks (e.g., `if (component.type === 'submit-button')`)
- Button-specific code is isolated within shared functions
- This ensures fixes apply to all components while allowing component-specific behavior
```

### 4. Add Horizontal Layout / Multi-Column Considerations

**Location:** Add to "Width Resize (E/W Handles)" section (around line 816)

```markdown
### Width Calculation for Horizontal/Mixed Layouts

When components use horizontal or mixed layouts, or have multiple columns:
- Width calculations must account for objects to the left/right of the target object
- Grid layout column calculations must be considered
- Component capabilities (constraints, surface capabilities) apply their rules

**Example (Button in horizontal layout):**
- If button is beside a label, button width = component width - label width - gaps
- If button is in a grid with multiple columns, button width = column width - padding
```

## ✅ Next Steps

1. **Review this document** - Confirm understanding is correct
2. **Update Component Framework Reference** - Add missing sections
3. **Implement synchronization** - Make Button Settings sync with Appearance Dimensions
4. **Fix resize rendering issues** - Investigate why button has rendering issues when other components don't (despite shared code)
