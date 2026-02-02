# Resize Handles & SmartBorder Sync Issue - Log Analysis

## Log Analysis Findings

### Issue 1: Multiple SmartBorder Recalculations

**Observation:**
- `smartborder.path.calculated` fires **multiple times** in rapid succession (sometimes 3-4 times within milliseconds)
- Each calculation shows slightly different segment widths
- Example from logs:
  ```
  [11:19:04.437] xRight: 827.9999775520165  (very wide)
  [11:19:04.505] xRight: 433.9999408540971  (narrower)
  [11:19:04.538] xRight: 433.9999408540971  (same)
  ```

**Root Cause:**
- `ResizeObserver` in SmartBorder triggers on every DOM change
- React re-renders cause multiple path recalculations
- `ResizeHandlesWrapper` position updates trigger additional SmartBorder recalculations (circular dependency)

### Issue 2: DOM Bounds Mismatch

**Observation:**
From `resize.preview.applied` logs:
```
appliedStyles: { width: "627px" }
domBounds: { width: 731.4000854492188 }  // Much wider!
```

**Root Cause:**
- Outer container width (`627px`) doesn't match SmartBorder actual width (`731px`)
- The expansion logic (`shouldExpandForInputWidth`) isn't working correctly
- SmartBorder width includes padding and content, but outer container only uses `component.props.width`

### Issue 3: Input Width Preservation Works, But Timing Is Off

**Observation:**
From `resize.width.calculated`:
```
before: { inputWidth: 424 }
after: { inputWidth: 424 }  // ✅ Preserved correctly
```

But SmartBorder segments show different widths at different times, suggesting:
- SmartBorder recalculates BEFORE the preserved `inputWidthOverride` is applied
- Or SmartBorder recalculates MULTIPLE times with different values

### Issue 4: ResizeHandlesWrapper Position Updates

**Observation:**
- `ResizeHandlesWrapper` uses `ResizeObserver` on SmartBorder container
- When SmartBorder recalculates, it triggers ResizeObserver
- ResizeObserver updates wrapper position
- Position update might trigger React re-render
- Re-render triggers SmartBorder recalculation again (loop)

## Root Causes Identified

1. **Circular Dependency**: ResizeHandlesWrapper → ResizeObserver → SmartBorder recalculation → React re-render → ResizeHandlesWrapper update
2. **Timing Race Condition**: SmartBorder recalculates before `inputWidthOverride` is fully applied to DOM
3. **Width Calculation Mismatch**: Outer container width expansion logic doesn't account for SmartBorder's actual rendered width (includes padding, content, etc.)
4. **Multiple Re-renders**: React re-renders cause multiple SmartBorder path calculations in quick succession

## Proposed Fixes

### Fix 1: Debounce SmartBorder Recalculation

Add debouncing to `SmartBorder.calculatePath()` to prevent rapid-fire recalculations:

```typescript
// In SmartBorder.tsx
const calculatePathDebounced = useMemo(
  () => debounce(calculatePath, 16), // ~1 frame at 60fps
  [calculatePath]
);
```

### Fix 2: Use Actual SmartBorder Width for Outer Container

Instead of using `inputWidthOverride` directly, measure the actual SmartBorder container width:

```typescript
// Measure SmartBorder actual width after render
useEffect(() => {
  if (smartBorderContainerRef.current && effectiveInputWidthOverride) {
    const actualWidth = smartBorderContainerRef.current.getBoundingClientRect().width;
    const scaleFactor = scale / 100;
    const baseWidth = actualWidth / scaleFactor;
    
    // Only expand if SmartBorder is wider than component width
    if (baseWidth > baseWidthPx) {
      setExpandedWidth(baseWidth);
    }
  }
}, [smartBorderContainerRef.current, effectiveInputWidthOverride, scale]);
```

### Fix 3: Prevent ResizeHandlesWrapper from Triggering SmartBorder Recalculation

Use `requestAnimationFrame` batching and check if position actually changed:

```typescript
// In ResizeHandlesWrapper
const updatePosition = useCallback(() => {
  const smartBorder = smartBorderContainerRef.current;
  const outer = outerContainerRef.current;
  
  if (!smartBorder || !outer) {
    setPosition(null);
    return;
  }
  
  const smartRect = smartBorder.getBoundingClientRect();
  const outerRect = outer.getBoundingClientRect();
  
  const newPosition = {
    top: smartRect.top - outerRect.top,
    left: smartRect.left - outerRect.left,
    width: smartRect.width,
    height: smartRect.height,
  };
  
  // Only update if position actually changed (prevent unnecessary re-renders)
  setPosition(prev => {
    if (!prev) return newPosition;
    const threshold = 0.5; // 0.5px threshold
    if (
      Math.abs(prev.top - newPosition.top) < threshold &&
      Math.abs(prev.left - newPosition.left) < threshold &&
      Math.abs(prev.width - newPosition.width) < threshold &&
      Math.abs(prev.height - newPosition.height) < threshold
    ) {
      return prev; // No change, prevent re-render
    }
    return newPosition;
  });
}, [smartBorderContainerRef, outerContainerRef]);
```

### Fix 4: Batch SmartBorder Recalculations

Use `useLayoutEffect` with `requestAnimationFrame` to batch recalculations:

```typescript
// In SmartBorder.tsx
useLayoutEffect(() => {
  let rafId: number;
  const schedule = () => {
    rafId = requestAnimationFrame(() => {
      calculatePath();
    });
  };
  
  schedule();
  
  const observer = new ResizeObserver(() => {
    schedule(); // Batch via RAF
  });
  
  // ... observe logic
  
  return () => {
    cancelAnimationFrame(rafId);
    observer.disconnect();
  };
}, [children, padding]);
```

## Implementation Priority

1. **High Priority**: Fix 3 (Prevent circular updates) - This will stop the infinite loop
2. **High Priority**: Fix 4 (Batch recalculations) - This will reduce redundant calculations
3. **Medium Priority**: Fix 2 (Use actual SmartBorder width) - This will fix alignment
4. **Low Priority**: Fix 1 (Debounce) - May not be needed if Fix 4 works

## Testing Strategy

After implementing fixes, verify:

1. **Single SmartBorder calculation per resize**: Check logs for `smartborder.path.calculated` - should fire once per resize action
2. **DOM bounds match**: `appliedStyles.width` should match `domBounds.width` (within scale factor)
3. **No circular updates**: ResizeHandlesWrapper position updates shouldn't trigger SmartBorder recalculation
4. **Input width preserved**: `resize.width.calculated` should show `inputWidth` preserved when manually set

## Log Queries for Verification

```bash
# Check for excessive SmartBorder recalculations
python backend/enhanced_diagnostic_logs.py --frontend-only --frontend-filter "smartborder.path" --limit 20

# Check resize sequence
python backend/enhanced_diagnostic_logs.py --frontend-only --frontend-component "text-1768298739656-235" --frontend-filter "resize" --limit 30

# Check for timing issues
python backend/enhanced_diagnostic_logs.py --frontend-only --frontend-component "text-1768298739656-235" --limit 50 | grep -E "(resize|smartborder)" | head -40
```
