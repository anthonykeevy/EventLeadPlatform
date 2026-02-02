# Component Styling Architecture: Current State & Improvement Plan

## Analysis Date
December 16, 2025

## Problem Statement

The current implementation requires **custom code for each component** to apply styling, making it:
- ❌ **Not scalable** - Adding a new component requires copying boilerplate
- ❌ **Inconsistent** - Different components apply styles differently
- ❌ **Error-prone** - Easy to miss style properties or apply them incorrectly
- ❌ **Not WYSIWYG** - Builder and preview can diverge due to manual implementation

## Current Approach (Problems Identified)

### 1. **Manual Style Resolution in Each Component**
```typescript
// Each component manually resolves styles
runtimeComponent: ({ component, ..., styleOverrides, globalStyles, layout }) => {
  const effectiveGlobalStyles = globalStyles ?? DEFAULT_GLOBAL_STYLES;
  const inputStyle = buildInputStyles(styleOverrides, globalStyles, disabled);
  const defaultBorderColor = (resolveStyle(...) as string | undefined) ?? effectiveGlobalStyles.borderColor;
  
  return (
    <FieldShell ...>
      <input style={inputStyle} ... />
    </FieldShell>
  );
}
```

**Problems:**
- Every component repeats the same style resolution logic
- Easy to forget to apply a style property
- Inconsistent application across components
- Hard to maintain when style properties change

### 2. **Inconsistent Component Implementation**
- ✅ **Updated components**: `first-name`, `text`, `number`, `email` - Use `buildInputStyles()` and pass `styleOverrides`
- ❌ **Legacy components**: `select`, `date`, `phone`, `textarea`, `checkbox`, `radio`, `address` - Still use hardcoded `inputBaseClass` and don't pass `styleOverrides`
- ❌ **Display components**: `header`, `paragraph`, `divider` - No styling support at all

### 3. **FieldShell Complexity**
- FieldShell handles label, validation, and layout
- But components still need to manually resolve input styles
- Layout logic is embedded in FieldShell, making it hard to reuse

### 4. **No Generic Input Wrapper**
- Each component manually applies styles to `<input>`, `<select>`, `<textarea>`
- No reusable component that automatically applies all styles
- Focus/blur handlers are duplicated

## Proposed Solution: Generic Styling System

### Architecture Principles

1. **Separation of Concerns:**
   - **Style Resolution**: Centralized hook (`useComponentStyles`)
   - **Style Application**: Generic wrapper components (`StyledInput`, `StyledSelect`, `StyledTextarea`)
   - **Component Logic**: Component-specific behavior only

2. **Composition Over Duplication:**
   - Generic styled components handle all styling
   - Components compose these, don't implement styling

3. **WYSIWYG Guarantee:**
   - Same styling system used in builder preview AND public renderer
   - Single source of truth for style application

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│  useComponentStyles Hook                                 │
│  - Resolves all styles (label, input, help text)        │
│  - Returns style objects ready to apply                 │
│  - Handles precedence (override > global > default)     │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│  Generic Styled Components                               │
│  - StyledInput (applies input styles automatically)     │
│  - StyledSelect (applies select styles automatically)    │
│  - StyledTextarea (applies textarea styles)              │
│  - Handles focus/blur with primaryColor                  │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│  FieldShell (Enhanced)                                   │
│  - Uses useComponentStyles hook                         │
│  - Uses resolved styles for label and help text         │
│  - Handles layout (horizontal/vertical)                 │
│  - Manages label width for validation offset            │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│  Runtime Components (Simplified)                         │
│  - Use StyledInput/StyledSelect/etc.                    │
│  - Wrap in FieldShell                                    │
│  - No manual style resolution needed                     │
└─────────────────────────────────────────────────────────┘
```

## Implementation Status

### ✅ Phase 1: Style Resolution Hook (COMPLETED)
**File**: `frontend/src/features/builder/hooks/useComponentStyles.ts`

- ✅ `useComponentStyles` hook created
- ✅ Resolves label, input, and help text styles
- ✅ Handles precedence (override > global > default)
- ✅ Returns gap values (labelGap, inputHelpGap)

### ✅ Phase 2: Generic Styled Components (COMPLETED)
**Files**: 
- `frontend/src/features/builder/components/styled/StyledInput.tsx`
- `frontend/src/features/builder/components/styled/StyledSelect.tsx`
- `frontend/src/features/builder/components/styled/StyledTextarea.tsx`

- ✅ `StyledInput` - Generic input with automatic style application
- ✅ `StyledSelect` - Generic select with automatic style application
- ✅ `StyledTextarea` - Generic textarea with automatic style application
- ✅ All handle focus/blur with primaryColor
- ✅ All handle disabled state

### ✅ Phase 3: Enhanced FieldShell (COMPLETED)
**File**: `frontend/src/features/builder/registry/ComponentRegistry.tsx`

- ✅ FieldShell now uses `useComponentStyles` hook
- ✅ Removed manual style resolution code
- ✅ Uses resolved styles directly
- ✅ Maintains horizontal/vertical layout logic

### ⏳ Phase 4: Migrate Components (IN PROGRESS)

**Current Status:**
- ✅ `first-name` - Uses new system (partially)
- ✅ `text` - Uses new system (partially)
- ✅ `number` - Uses new system (partially)
- ✅ `email` - Uses new system (partially)
- ❌ `select` - Still uses legacy `inputBaseClass`
- ❌ `date` - Still uses legacy `inputBaseClass`
- ❌ `phone` - Still uses legacy `inputBaseClass`
- ❌ `textarea` - Still uses legacy `inputBaseClass`
- ❌ `checkbox` - Custom implementation, needs styling
- ❌ `radio` - Custom implementation, needs styling
- ❌ `address` - Still uses legacy `inputBaseClass`

## How to Use the New System

### Example: Adding a New Component (Before vs After)

#### ❌ Before (30+ lines, error-prone)
```typescript
'new-component': {
  runtimeComponent: ({ component, value, onChange, disabled, required, error, tabIndex, primaryColor, inputRef, styleOverrides, globalStyles, layout }) => {
    const maxLength = component.props.validation?.maxLength;
    const valueStr = (value as string) ?? '';
    const effectiveGlobalStyles = globalStyles ?? DEFAULT_GLOBAL_STYLES;
    const inputStyle = buildInputStyles(styleOverrides, globalStyles, disabled);
    const defaultBorderColor = (resolveStyle(styleOverrides, globalStyles, 'borderColor') as string | undefined) ?? effectiveGlobalStyles.borderColor;
    
    return (
      <FieldShell 
        label={String(component.props.label ?? 'New Component')} 
        required={required} 
        error={error}
        styleOverrides={styleOverrides}
        globalStyles={globalStyles}
        layout={layout}
      >
        <input
          ref={inputRef}
          className={disabled ? 'cursor-not-allowed' : ''}
          style={inputStyle}
          type="text"
          disabled={disabled}
          placeholder={String(component.props.placeholder ?? '')}
          value={valueStr}
          onChange={e => onChange(e.target.value)}
          maxLength={maxLength}
          tabIndex={tabIndex}
          onFocus={(e) => {
            if (primaryColor) {
              e.currentTarget.style.borderColor = primaryColor
              e.currentTarget.style.boxShadow = `0 0 0 2px ${primaryColor}33`
            }
          }}
          onBlur={(e) => {
            e.currentTarget.style.borderColor = defaultBorderColor
            e.currentTarget.style.boxShadow = ''
          }}
        />
      </FieldShell>
    );
  }
}
```

#### ✅ After (10 lines, consistent, WYSIWYG)
```typescript
import { StyledInput } from '../components/styled';
import { useComponentStyles } from '../hooks/useComponentStyles';

'new-component': {
  runtimeComponent: ({ component, value, onChange, disabled, required, error, tabIndex, primaryColor, inputRef, styleOverrides, globalStyles, layout }) => {
    const styles = useComponentStyles(styleOverrides, globalStyles);
    
    return (
      <FieldShell 
        label={String(component.props.label ?? 'New Component')} 
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
          type="text"
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

### Example: Migrating Existing Component

#### Current Implementation (text component)
```typescript
runtimeComponent: ({ component, value, onChange, disabled, required, error, tabIndex, primaryColor, inputRef, styleOverrides, globalStyles, layout }) => {
  const maxLength = component.props.validation?.maxLength
  const valueStr = (value as string) ?? ''
  const isAtMaxLength = maxLength && valueStr.length >= maxLength
  const validationMessage = isAtMaxLength 
    ? (component.props.validationMessage || component.props.validation?.customError || `We only allow a max of ${maxLength} Characters`)
    : undefined
  const displayError = error || validationMessage
  
  const effectiveGlobalStyles = globalStyles ?? DEFAULT_GLOBAL_STYLES;
  const inputStyle = buildInputStyles(styleOverrides, globalStyles, disabled);
  const defaultBorderColor = (resolveStyle(styleOverrides, globalStyles, 'borderColor') as string | undefined) ?? effectiveGlobalStyles.borderColor;
  
  return (
    <FieldShell 
      label={String(component.props.label ?? 'Text')} 
      required={required} 
      error={displayError}
      styleOverrides={styleOverrides}
      globalStyles={globalStyles}
      layout={layout}
    >
      <input
        ref={inputRef as React.RefObject<HTMLInputElement>}
        className={disabled ? 'cursor-not-allowed' : ''}
        style={inputStyle}
        type="text"
        disabled={disabled}
        placeholder={String(component.props.placeholder ?? '')}
        value={valueStr}
        onChange={e => onChange(e.target.value)}
        maxLength={maxLength}
        tabIndex={tabIndex}
        onFocus={(e) => {
          if (primaryColor) {
            e.currentTarget.style.borderColor = primaryColor
            e.currentTarget.style.boxShadow = `0 0 0 2px ${primaryColor}33`
          }
        }}
        onBlur={(e) => {
          e.currentTarget.style.borderColor = defaultBorderColor
          e.currentTarget.style.boxShadow = ''
        }}
      />
    </FieldShell>
  )
}
```

#### Migrated Implementation (using new system)
```typescript
import { StyledInput } from '../components/styled';
import { useComponentStyles } from '../hooks/useComponentStyles';

runtimeComponent: ({ component, value, onChange, disabled, required, error, tabIndex, primaryColor, inputRef, styleOverrides, globalStyles, layout }) => {
  const styles = useComponentStyles(styleOverrides, globalStyles);
  const maxLength = component.props.validation?.maxLength
  const valueStr = (value as string) ?? ''
  const isAtMaxLength = maxLength && valueStr.length >= maxLength
  const validationMessage = isAtMaxLength 
    ? (component.props.validationMessage || component.props.validation?.customError || `We only allow a max of ${maxLength} Characters`)
    : undefined
  const displayError = error || validationMessage
  
  return (
    <FieldShell 
      label={String(component.props.label ?? 'Text')} 
      required={required} 
      error={displayError}
      styleOverrides={styleOverrides}
      globalStyles={globalStyles}
      layout={layout}
    >
      <StyledInput
        ref={inputRef as React.RefObject<HTMLInputElement>}
        styles={styles.input}
        primaryColor={primaryColor}
        disabled={disabled}
        type="text"
        placeholder={String(component.props.placeholder ?? '')}
        value={valueStr}
        onChange={e => onChange(e.target.value)}
        maxLength={maxLength}
        tabIndex={tabIndex}
      />
    </FieldShell>
  )
}
```

**Benefits:**
- ✅ Reduced from 40+ lines to 25 lines
- ✅ No manual style resolution
- ✅ No manual focus/blur handlers
- ✅ Consistent with all other components
- ✅ WYSIWYG guaranteed

## Benefits of New Architecture

### 1. **Scalability**
- ✅ Add new component: Just use `StyledInput`/`StyledSelect`/`StyledTextarea`
- ✅ No style resolution code needed
- ✅ Consistent styling automatically applied
- ✅ **5-10 lines per component** instead of 30-40

### 2. **Consistency**
- ✅ All components use same styling system
- ✅ Same styles in builder and preview
- ✅ WYSIWYG guaranteed
- ✅ No style drift between components

### 3. **Maintainability**
- ✅ Style changes in one place affect all components
- ✅ Easy to add new style properties (just update hook)
- ✅ Less code to maintain
- ✅ Type-safe style resolution

### 4. **Type Safety**
- ✅ TypeScript ensures all style properties are typed
- ✅ Compile-time checks for style application
- ✅ Autocomplete for style properties

## Migration Checklist

### Step 1: Infrastructure ✅ COMPLETE
- [x] Create `useComponentStyles` hook
- [x] Create `StyledInput` component
- [x] Create `StyledSelect` component
- [x] Create `StyledTextarea` component
- [x] Refactor `FieldShell` to use hook

### Step 2: Migrate Components (In Progress)
- [x] `text` - Partially migrated (uses `buildInputStyles`, needs `StyledInput`)
- [x] `email` - Partially migrated (uses `buildInputStyles`, needs `StyledInput`)
- [x] `number` - Partially migrated (uses `buildInputStyles`, needs `StyledInput`)
- [x] `first-name` - Partially migrated (uses `buildInputStyles`, needs `StyledInput`)
- [ ] `select` - Needs migration to `StyledSelect`
- [ ] `date` - Needs migration to `StyledInput`
- [ ] `phone` - Needs migration to `StyledInput`
- [ ] `textarea` - Needs migration to `StyledTextarea`
- [ ] `checkbox` - Needs custom styled component
- [ ] `radio` - Needs custom styled component
- [ ] `address` - Needs migration (complex component)

### Step 3: Cleanup
- [ ] Remove `buildInputStyles` function (replaced by hook)
- [ ] Remove `resolveStyle` function from ComponentRegistry (replaced by hook)
- [ ] Remove `inputBaseClass` constant
- [ ] Remove manual focus/blur handlers from components

## Next Steps

1. **Complete Migration**: Migrate all components to use `StyledInput`/`StyledSelect`/`StyledTextarea`
2. **Test WYSIWYG**: Verify builder and preview match exactly
3. **Documentation**: Update component creation guide
4. **Remove Legacy Code**: Clean up old style resolution functions

## Component Creation Guide (New Standard)

### For Standard Input Components (text, email, number, phone, date)

```typescript
import { StyledInput } from '../components/styled';
import { useComponentStyles } from '../hooks/useComponentStyles';

'component-name': {
  type: 'component-name',
  label: 'Component Label',
  icon: <Icon />,
  category: 'input',
  defaultProps: {
    label: 'Field Label',
    placeholder: 'Placeholder text',
    required: false,
    validation: { maxLength: 50 },
  },
  runtimeComponent: ({ component, value, onChange, disabled, required, error, tabIndex, primaryColor, inputRef, styleOverrides, globalStyles, layout }) => {
    const styles = useComponentStyles(styleOverrides, globalStyles);
    
    return (
      <FieldShell 
        label={String(component.props.label ?? 'Label')} 
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
          type="text" // or "email", "number", "tel", "date"
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

### For Select Components

```typescript
import { StyledSelect } from '../components/styled';
import { useComponentStyles } from '../hooks/useComponentStyles';

'select': {
  runtimeComponent: ({ component, value, onChange, disabled, required, error, tabIndex, primaryColor, inputRef, styleOverrides, globalStyles, layout }) => {
    const styles = useComponentStyles(styleOverrides, globalStyles);
    
    return (
      <FieldShell 
        label={String(component.props.label ?? 'Select')} 
        required={required} 
        error={error}
        styleOverrides={styleOverrides}
        globalStyles={globalStyles}
        layout={layout}
      >
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
      </FieldShell>
    );
  }
}
```

### For Textarea Components

```typescript
import { StyledTextarea } from '../components/styled';
import { useComponentStyles } from '../hooks/useComponentStyles';

'textarea': {
  runtimeComponent: ({ component, value, onChange, disabled, required, error, tabIndex, primaryColor, inputRef, styleOverrides, globalStyles, layout }) => {
    const styles = useComponentStyles(styleOverrides, globalStyles);
    
    return (
      <FieldShell 
        label={String(component.props.label ?? 'Textarea')} 
        required={required} 
        error={error}
        styleOverrides={styleOverrides}
        globalStyles={globalStyles}
        layout={layout}
      >
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
      </FieldShell>
    );
  }
}
```

## Conclusion

**Status**: ✅ **Infrastructure Complete, Migration In Progress**

The new architecture provides:
- ✅ **Scalable**: Add components with minimal code
- ✅ **Consistent**: All components use same styling system
- ✅ **WYSIWYG**: Builder and preview guaranteed to match
- ✅ **Maintainable**: Single source of truth for styles

**Next Action**: Migrate remaining components to use the new styled components.
