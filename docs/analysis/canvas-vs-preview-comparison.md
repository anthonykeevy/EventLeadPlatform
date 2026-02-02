# Canvas vs Preview: Positioning and Sizing Comparison

## Summary
Analysis of differences between Form Builder Canvas and Public Form Preview rendering.

## Key Differences Found

### 1. **Component Scale Not Applied in Preview**

**Builder (SortableComponent.tsx:384):**
```typescript
const displayScale = resizePreview?.scale ?? componentScale;
const baseWidthPx = resizePreview?.width ?? parseComponentWidthPx(component.props.width);
const displayWidthPx = baseWidthPx * (displayScale / 100);  // ⚠️ Applies component scale
const displayWidth = `${displayWidthPx}px`;
```

**Preview (PublicFormArtboard.tsx:214):**
```typescript
const widthFromProps = c.props.width
const widthFromStyle = c.style?.width != null ? `${c.style.width}px` : null
const width = widthFromProps || widthFromStyle || '360px'  // ⚠️ No component scale applied
```

**Impact:** If a component has `componentScale: 120` (120%), the builder shows it 20% wider, but the preview uses the raw width. This causes size discrepancies.

### 2. **Transform Origin Difference**

**Builder (FormBuilderCanvas.tsx:208):**
```typescript
transform: `scale(${scale})`,
transformOrigin: 'center center'  // ⚠️ Scales from center
```

**Preview (PublicFormArtboard.tsx:195):**
```typescript
transform: `scale(${scale})`,
transformOrigin: 'top left'  // ⚠️ Scales from top-left
```

**Impact:** When the canvas is scaled (e.g., 69%), components shift position differently because scaling happens from different anchor points.

### 3. **Width Calculation Logic**

**Builder:**
- Parses `component.props.width` (handles percentages, px, etc.)
- Applies `componentScale` multiplier
- Uses `displayWidth` which is the scaled pixel value

**Preview:**
- Directly uses `component.props.width` string (e.g., "385px")
- No component scale applied
- No percentage-to-pixel conversion

**Impact:** Components with percentage widths or component scale will render differently.

## Recommendations

### Fix 1: Apply Component Scale in Preview
Update `PublicFormArtboard.tsx` to apply `componentScale`:

```typescript
const componentScale = c.props.componentScale ?? 100
const widthFromProps = c.props.width
const widthFromStyle = c.style?.width != null ? `${c.style.width}px` : null

// Parse width to pixels, then apply component scale
let baseWidthPx: number
if (widthFromProps) {
  if (widthFromProps.endsWith('px')) {
    baseWidthPx = parseInt(widthFromProps, 10)
  } else if (widthFromProps.endsWith('%')) {
    // Convert percentage to pixels based on canvas width
    const pct = parseInt(widthFromProps, 10)
    baseWidthPx = Math.round((pct / 100) * canvasWidth)
  } else {
    baseWidthPx = parseInt(widthFromProps, 10) || 360
  }
} else if (widthFromStyle) {
  baseWidthPx = parseInt(widthFromStyle, 10)
} else {
  baseWidthPx = 360
}

const scaledWidthPx = baseWidthPx * (componentScale / 100)
const width = `${scaledWidthPx}px`
```

### Fix 2: Align Transform Origin (Optional)
Consider using `top left` in builder for consistency, or document that builder uses center-origin for better UX during editing.

## Current Status

Based on screenshots provided:
- ✅ Background color: **MATCHING** (light green)
- ✅ Component widths: **VISUALLY SIMILAR** (Email widest, Last Name intermediate, First Name narrowest)
- ⚠️ **Potential discrepancies** due to component scale not being applied
- ⚠️ **Position shifts** possible due to transform origin difference when canvas is scaled

## Next Steps

1. Implement component scale in preview
2. Test with components that have `componentScale !== 100`
3. Verify positioning matches exactly at different canvas scales
4. Consider standardizing transform origin if position shifts are noticeable
