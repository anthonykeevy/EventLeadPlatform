# Component Styling Guide: Creating WYSIWYG Components

## Overview

This guide explains how to create form components that automatically apply styling from the form builder, ensuring **WYSIWYG** (What You See Is What You Get) between the builder and preview/production.

## Architecture

The styling system uses a **three-layer architecture**:

1. **Style Resolution** (`useComponentStyles` hook) - Resolves styles with precedence
2. **Styled Components** (`StyledInput`, `StyledSelect`, `StyledTextarea`) - Apply styles automatically
3. **FieldShell** - Handles layout, label, and validation styling

## Quick Start: Adding a New Component

### Step 1: Import Required Components

```typescript
import { StyledInput } from '../components/styled';
import { useComponentStyles } from '../hooks/useComponentStyles';
```

### Step 2: Create Component Definition

```typescript
'my-component': {
  type: 'my-component',
  label: 'My Component',
  icon: <MyIcon />,
  category: 'input',
  defaultProps: {
    label: 'My Field',
    placeholder: 'Enter value...',
    required: false,
    validation: { maxLength: 100 },
  },
  runtimeComponent: ({ 
    component, 
    value, 
    onChange, 
    disabled, 
    required, 
    error, 
    tabIndex, 
    primaryColor, 
    inputRef, 
    styleOverrides, 
    globalStyles, 
    layout 
  }) => {
    // Step 3: Use the hook to resolve styles
    const styles = useComponentStyles(styleOverrides, globalStyles);
    
    // Step 4: Render with FieldShell and StyledInput
    return (
      <FieldShell 
        label={String(component.props.label ?? 'My Field')} 
        required={required} 
        error={error}
        styleOverrides={styleOverrides}
        globalStyles={globalStyles}
        layout={layout}
      >
        <StyledInput
          ref={inputRef}
          styles={styles.input}
          primaryColor={primaryColor}
          disabled={disabled}
          type="text" // or "email", "number", "tel", "date", etc.
          placeholder={String(component.props.placeholder ?? '')}
          value={(value as string) ?? ''}
          onChange={e => onChange(e.target.value)}
          maxLength={component.props.validation?.maxLength}
          tabIndex={tabIndex}
        />
      </FieldShell>
    );
  }
}
```

**That's it!** The component automatically:
- ✅ Applies all styles from `styleOverrides` and `globalStyles`
- ✅ Handles focus/blur with primary color
- ✅ Supports horizontal/vertical layout
- ✅ Applies label and validation styling
- ✅ Matches builder preview exactly

## Component Types

### Text Input Components
Use `StyledInput` with appropriate `type`:
- `type="text"` - Standard text input
- `type="email"` - Email input
- `type="number"` - Number input
- `type="tel"` - Phone input
- `type="date"` - Date picker
- `type="password"` - Password input

### Select/Dropdown Components
Use `StyledSelect`:

```typescript
<StyledSelect
  ref={inputRef}
  styles={styles.input}
  primaryColor={primaryColor}
  disabled={disabled}
  value={(value as string) ?? ''}
  onChange={e => onChange(e.target.value)}
  options={component.props.options ?? []}
  placeholder={String(component.props.placeholder ?? 'Select…')}
  tabIndex={tabIndex}
/>
```

### Textarea Components
Use `StyledTextarea`:

```typescript
<StyledTextarea
  ref={inputRef}
  styles={styles.input}
  primaryColor={primaryColor}
  disabled={disabled}
  placeholder={String(component.props.placeholder ?? '')}
  value={(value as string) ?? ''}
  onChange={e => onChange(e.target.value)}
  maxLength={component.props.validation?.maxLength}
  rows={component.props.height ?? 4}
  tabIndex={tabIndex}
/>
```

## What Gets Applied Automatically

### Input Styles
- ✅ Font family, size, weight, style
- ✅ Text color and background color
- ✅ Border color, width, radius
- ✅ Input height
- ✅ Padding (from global styles)
- ✅ Focus styling (primary color)
- ✅ Disabled state styling

### Label Styles
- ✅ Font family, size, weight, style
- ✅ Label color and background color
- ✅ Label border (if specified)
- ✅ Label gap (spacing from input)

### Help Text/Validation Styles
- ✅ Font family, size, weight, style
- ✅ Help text color and background color
- ✅ Help text border (if specified)
- ✅ Input-help gap (spacing from input)

### Layout
- ✅ Horizontal layout (label left, input right)
- ✅ Vertical layout (label above input)
- ✅ Proper alignment (label aligns with input center, not validation)

## Style Precedence

Styles are resolved with this precedence (highest to lowest):

1. **Component `styleOverrides`** - Component-specific overrides
2. **Form `globalStyles`** - Form-level defaults
3. **System `DEFAULT_GLOBAL_STYLES`** - Fallback defaults

## Common Patterns

### Pattern 1: Simple Text Input
```typescript
const styles = useComponentStyles(styleOverrides, globalStyles);

return (
  <FieldShell label={label} required={required} error={error} styleOverrides={styleOverrides} globalStyles={globalStyles} layout={layout}>
    <StyledInput styles={styles.input} primaryColor={primaryColor} disabled={disabled} {...props} />
  </FieldShell>
);
```

### Pattern 2: With Validation Message
```typescript
const styles = useComponentStyles(styleOverrides, globalStyles);
const maxLength = component.props.validation?.maxLength;
const valueStr = (value as string) ?? '';
const isAtMaxLength = maxLength && valueStr.length >= maxLength;
const validationMessage = isAtMaxLength 
  ? (component.props.validationMessage || component.props.validation?.customError || `We only allow a max of ${maxLength} Characters`)
  : undefined;
const displayError = error || validationMessage;

return (
  <FieldShell label={label} required={required} error={displayError} styleOverrides={styleOverrides} globalStyles={globalStyles} layout={layout}>
    <StyledInput styles={styles.input} primaryColor={primaryColor} disabled={disabled} maxLength={maxLength} {...props} />
  </FieldShell>
);
```

### Pattern 3: Select with Options
```typescript
const styles = useComponentStyles(styleOverrides, globalStyles);

return (
  <FieldShell label={label} required={required} error={error} styleOverrides={styleOverrides} globalStyles={globalStyles} layout={layout}>
    <StyledSelect
      styles={styles.input}
      primaryColor={primaryColor}
      disabled={disabled}
      value={(value as string) ?? ''}
      onChange={e => onChange(e.target.value)}
      options={component.props.options ?? []}
      placeholder={String(component.props.placeholder ?? 'Select…')}
      tabIndex={tabIndex}
    />
  </FieldShell>
);
```

## Migration Checklist

When migrating an existing component:

- [ ] Import `StyledInput`/`StyledSelect`/`StyledTextarea`
- [ ] Import `useComponentStyles` hook
- [ ] Replace manual style resolution with `useComponentStyles(styleOverrides, globalStyles)`
- [ ] Replace `<input>` with `<StyledInput styles={styles.input} ... />`
- [ ] Remove manual `buildInputStyles()` calls
- [ ] Remove manual focus/blur handlers (handled by StyledInput)
- [ ] Remove hardcoded `inputBaseClass` usage
- [ ] Ensure `styleOverrides` and `globalStyles` are passed to `FieldShell`
- [ ] Test in builder and preview to verify WYSIWYG

## Benefits

✅ **5-10 lines of code** per component (vs 30-40 before)  
✅ **Automatic styling** - No manual style resolution  
✅ **WYSIWYG guaranteed** - Builder and preview match exactly  
✅ **Consistent** - All components use same styling system  
✅ **Type-safe** - TypeScript ensures correct usage  
✅ **Maintainable** - Style changes in one place affect all components  

## Files Created

- ✅ `frontend/src/features/builder/hooks/useComponentStyles.ts` - Style resolution hook
- ✅ `frontend/src/features/builder/components/styled/StyledInput.tsx` - Generic input component
- ✅ `frontend/src/features/builder/components/styled/StyledSelect.tsx` - Generic select component
- ✅ `frontend/src/features/builder/components/styled/StyledTextarea.tsx` - Generic textarea component
- ✅ `frontend/src/features/builder/components/styled/index.ts` - Exports

## Documentation

- 📄 `docs/analysis/component-styling-architecture.md` - Full architecture documentation
- 📄 `docs/analysis/component-properties-comparison.md` - Property comparison guide
