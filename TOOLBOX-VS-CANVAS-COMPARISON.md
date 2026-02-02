# Toolbox vs Canvas Component Rendering Comparison

## Current Architecture

### Toolbox Rendering (`ComponentSidebar.tsx`)

**How it works:**
1. Uses `ComponentRegistry[type].previewComponent` directly
2. For text components, `previewComponent` is `<StandardInput />` with hardcoded props
3. `StandardInput` includes `TextLengthIndicator` when `maxLength` is set
4. Component is wrapped in a draggable container

**Example:**
```tsx
// ComponentRegistry.tsx
previewComponent: <StandardInput 
    label="Text Field" 
    icon={Type} 
    placeholder="Enter text..." 
    validationMessage="Validation error example"
/>
```

**Key Features:**
- ✅ Shows `TextLengthIndicator` (because `StandardInput` includes it)
- ✅ Uses `StandardInput` component directly
- ✅ Hardcoded preview props (label, placeholder, validationMessage)
- ✅ Simple, standalone rendering

---

### Canvas Rendering (`SortableComponent.tsx` → `UniversalFieldShell.tsx`)

**How it works:**
1. Uses `UniversalFieldShell` wrapper
2. `UniversalFieldShell` uses `objectRenderers` to render each object (label, input, validation)
3. Input renderer (`createInputRenderer`) creates `StyledInput` + `TextLengthIndicator`
4. Component structure is defined in `ComponentRegistry[type].structure`

**Example:**
```tsx
// SortableComponent.tsx
<UniversalFieldShell
    structure={structure}
    renderers={renderers}  // ← Uses renderers, not StandardInput
    component={component}
    // ...
/>
```

**Key Features:**
- ✅ Uses `UniversalFieldShell` for consistent structure
- ✅ Uses renderers for flexible object rendering
- ✅ Supports object layout (vertical/horizontal/mixed)
- ✅ Supports conditional rendering
- ⚠️ `TextLengthIndicator` SHOULD be showing (code is there) but might not be visible

---

## Differences Summary

| Aspect | Toolbox | Canvas |
|--------|---------|--------|
| **Component Used** | `StandardInput` directly | `UniversalFieldShell` → renderers → `StyledInput` |
| **Structure** | Hardcoded JSX | Defined in `ComponentRegistry[type].structure` |
| **TextLengthIndicator** | ✅ Included in `StandardInput` | ✅ Included in input renderer (line 237) |
| **Object Layout** | ❌ Not supported | ✅ Supports vertical/horizontal/mixed |
| **Conditional Rendering** | ❌ Not supported | ✅ Supports conditional objects |
| **Style Resolution** | Uses `fieldStyles` prop | Uses `computeFieldStyles` internally |
| **Props Source** | Hardcoded in registry | From `component.props` |

---

## Why TextLengthIndicator Might Not Be Showing on Canvas

### Possible Causes:

1. **`maxLength` not set**: The indicator only shows if `component.props.validation?.maxLength` is set
   ```tsx
   // objectRenderers.tsx line 233
   if (maxLength) {  // ← Only renders if maxLength exists
       return (
           <div className="relative">
               {inputElement}
               <TextLengthIndicator ... />
           </div>
       );
   }
   ```

2. **CSS visibility issue**: The indicator uses `absolute right-1 bottom-1` positioning
   - Needs a `relative` parent (which is provided)
   - Might be hidden behind other elements
   - Might be outside viewport

3. **Component type mismatch**: Some component types might not use the input renderer

---

## Solution: Unify to Use Same Component

### Option 1: Use `StandardInput` on Canvas (Simpler)

**Pros:**
- ✅ Already includes `TextLengthIndicator`
- ✅ Consistent rendering between toolbox and canvas
- ✅ Less code duplication

**Cons:**
- ❌ Loses flexibility of renderer system
- ❌ Can't support object layout variations
- ❌ Can't support conditional rendering

**Implementation:**
```tsx
// In UniversalFieldShell or SortableComponent
if (component.type === 'text') {
    return <StandardInput 
        label={component.props.label}
        placeholder={component.props.placeholder}
        validationMessage={component.props.validationMessage}
        // ... other props
    />;
}
```

---

### Option 2: Use `UniversalFieldShell` in Toolbox (Better Architecture)

**Pros:**
- ✅ Consistent rendering everywhere
- ✅ Supports all features (layout, conditional rendering)
- ✅ Single source of truth for component rendering

**Cons:**
- ⚠️ More complex (need to create FormComponent objects for toolbox)
- ⚠️ Need to ensure TextLengthIndicator works correctly

**Implementation:**
```tsx
// In ComponentSidebar.tsx
const previewComponent = useMemo(() => {
    const previewComponent: FormComponent = {
        id: `preview-${item.type}`,
        type: item.type,
        position: { x: 0, y: 0 },
        props: {
            label: item.defaultProps?.label || 'Preview',
            placeholder: item.defaultProps?.placeholder || '',
            validation: { maxLength: 50 }, // ← Ensure maxLength is set
            // ... other default props
        }
    };
    
    return (
        <UniversalFieldShell
            structure={item.structure}
            renderers={getRenderersForComponent(item.type, item.structure)}
            component={previewComponent}
            globalStyles={globalStyles}
            builderMode={{ showBorder: false }}
        />
    );
}, [item, globalStyles]);
```

---

### Option 3: Fix TextLengthIndicator on Canvas (Recommended)

**Keep current architecture but ensure TextLengthIndicator works:**

1. **Ensure `maxLength` is set**: Add default `maxLength` to component props if not set
2. **Verify visibility**: Check CSS positioning and z-index
3. **Add logging**: Log when indicator should/shouldn't render

**Implementation:**
```tsx
// In objectRenderers.tsx - ensure maxLength has a default
const maxLength = component.props.validation?.maxLength ?? 
    (component.type === 'text' ? 50 : undefined); // Default for text inputs

// Ensure TextLengthIndicator is always visible in builder mode
if (maxLength || builderMode) {  // Show in builder mode even without maxLength
    return (
        <div className="relative">
            {inputElement}
            {maxLength && (
                <TextLengthIndicator
                    maxLength={maxLength}
                    fontFamily={styles.computed.fontFamily}
                    fontSize={styles.computed.fontSize}
                    fontWeight={styles.computed.fontWeight}
                    visible={true}
                    componentId={componentId}
                />
            )}
        </div>
    );
}
```

---

## Recommended Approach

**Use Option 3** (Fix TextLengthIndicator on Canvas) because:

1. ✅ Maintains flexible architecture
2. ✅ Supports all features (layout, conditional rendering)
3. ✅ Minimal changes needed
4. ✅ Keeps toolbox simple (can stay as-is or migrate later)

### Steps:

1. **Add default `maxLength`** to text components when created
2. **Ensure `TextLengthIndicator` is visible** in builder mode
3. **Add logging** to debug visibility issues
4. **Test** that indicator shows on canvas

---

## Functions Available

### Toolbox (`ComponentSidebar.tsx`)
- ✅ Drag and drop (`useDraggable`)
- ✅ Visual preview
- ❌ No resize handles
- ❌ No property editing
- ❌ No selection state

### Canvas (`SortableComponent.tsx`)
- ✅ Drag and drop (`useSortable`)
- ✅ Resize handles (E/W/N/S/corners)
- ✅ Property editing (via PropertiesPanel)
- ✅ Selection state
- ✅ SmartBorder for collision detection
- ✅ Undo/redo support
- ✅ Position tracking

---

## Next Steps

1. **Investigate why TextLengthIndicator isn't showing** on canvas
2. **Add default `maxLength`** to text components
3. **Ensure visibility** in builder mode
4. **Consider unifying** toolbox to use `UniversalFieldShell` for consistency (future enhancement)
