# Resize Handles & SmartBorder Sync Fixes - Based on Log Analysis

## Log Analysis Summary

After analyzing the logs, we identified **4 critical issues** causing resize handles and SmartBorder to respond independently:

### Issue 1: Multiple Rapid SmartBorder Recalculations
**Log Evidence:**
- `smartborder.path.calculated` fires 3-4 times within milliseconds
- Each calculation shows different segment widths
- Example: `xRight: 827px` → `xRight: 433px` → `xRight: 433px`

**Root Cause:** 
- `ResizeObserver` triggers on every DOM change
- React re-renders cause multiple path recalculations
- No batching/debouncing mechanism

### Issue 2: Circular Update Loop
**Log Evidence:**
- ResizeHandlesWrapper position updates trigger SmartBorder recalculation
- SmartBorder recalculation triggers React re-render
- Re-render triggers ResizeHandlesWrapper update again

**Root Cause:**
- ResizeHandlesWrapper's `ResizeObserver` observes SmartBorder container
- Position updates cause DOM changes
- DOM changes trigger SmartBorder's ResizeObserver

### Issue 3: DOM Bounds Mismatch
**Log Evidence:**
```
appliedStyles: { width: "627px" }
domBounds: { width: 731.4000854492188 }  // Much wider!
```

**Root Cause:**
- Outer container width (`627px`) doesn't match SmartBorder actual width (`731px`)
- Expansion logic uses `inputWidthOverride` directly, but SmartBorder includes padding

### Issue 4: Timing Race Condition
**Log Evidence:**
- `resize.width.calculated` shows `inputWidth: 424` preserved correctly
- But SmartBorder segments show different widths at different times
- Suggests SmartBorder recalculates before `inputWidthOverride` is applied

## Implemented Fixes

### Fix 1: Batch SmartBorder Recalculations ✅

**File:** `frontend/src/features/builder/components/ui/SmartBorder.tsx`

**Change:**
- Added `isScheduled` flag to prevent multiple rapid `requestAnimationFrame` calls
- Batches all ResizeObserver callbacks into a single RAF call
- Prevents redundant path calculations

**Code:**
```typescript
let rafId: number | null = null;
let isScheduled = false;

const scheduleCalculation = () => {
    if (isScheduled) return; // Already scheduled, skip
    isScheduled = true;
    rafId = requestAnimationFrame(() => {
        isScheduled = false;
        calculatePath();
    });
};
```

### Fix 2: Prevent Circular Updates in ResizeHandlesWrapper ✅

**File:** `frontend/src/features/builder/components/SortableComponent.tsx`

**Changes:**
1. **Batch updates via RAF**: All position updates batched through `requestAnimationFrame`
2. **Threshold checking**: Only update position if change > 0.5px (prevents micro-adjustments)
3. **Cancel previous RAF**: Cancel pending RAF before scheduling new one

**Code:**
```typescript
const scheduleUpdate = () => {
    if (rafIdRef.current !== null) {
        cancelAnimationFrame(rafIdRef.current);
    }
    rafIdRef.current = requestAnimationFrame(updatePosition);
};

// Threshold check prevents unnecessary re-renders
setPosition(prev => {
    if (!prev) return newPosition;
    const threshold = 0.5;
    if (/* all differences < threshold */) {
        return prev; // No significant change
    }
    return newPosition;
});
```

### Fix 3: Account for SmartBorder Padding in Outer Container Width ✅

**File:** `frontend/src/features/builder/components/SortableComponent.tsx`

**Change:**
- Calculate expected SmartBorder width including padding (5px on each side)
- Use this for outer container expansion instead of raw `inputWidthOverride`

**Code:**
```typescript
const smartBorderPadding = 5; // SmartBorder default padding
const expectedSmartBorderWidth = effectiveInputWidthOverride && baseWidthPx && effectiveInputWidthOverride > baseWidthPx
    ? effectiveInputWidthOverride + (smartBorderPadding * 2) // Add padding on both sides
    : baseWidthPx;
```

### Fix 4: Use Expanded Width for ResizeHandles ✅

**File:** `frontend/src/features/builder/components/SortableComponent.tsx`

**Change:**
- Pass `displayWidth` (expanded) to ResizeHandles instead of `component.props.width`
- Ensures handles know the correct container size

**Code:**
```typescript
const resizeHandleProps = {
    currentWidth: displayWidth ?? component.props.width, // Use expanded width
    // ...
};
```

### Fix 5: Preserve Manually Set inputWidthOverride ✅

**File:** `frontend/src/features/builder/components/SortableComponent.tsx`

**Change:**
- Detect when `inputWidthOverride` was manually set (not proportional)
- Preserve it during E/W resize instead of scaling proportionally

**Code:**
```typescript
const wasManuallySet = component.props.inputWidthOverride !== undefined && 
                        component.props.inputWidthOverride !== oldWidthPx &&
                        !isDropdownSplit;

const newInputWidth = wasManuallySet 
    ? currentInputWidth  // Preserve manual setting
    : Math.round(currentInputWidth * widthRatio);  // Scale proportionally
```

## Expected Behavior After Fixes

### Scenario 1: Resize inputWidthOverride (Green Handle)
1. User drags green handle → `inputWidthOverride` changes
2. SmartBorder recalculates **once** (batched via RAF)
3. Outer container expands to match SmartBorder width (including padding)
4. ResizeHandlesWrapper updates position **once** (threshold prevents micro-updates)
5. Resize handles align with SmartBorder ✅

### Scenario 2: Resize Component Width (E/W Handles)
1. User drags E/W handle → `component.props.width` changes
2. If `inputWidthOverride` was manually set → **preserved** (not scaled)
3. SmartBorder recalculates **once** (batched)
4. ResizeHandlesWrapper updates **only if position changed significantly** (>0.5px)
5. Resize handles stay aligned ✅

### Scenario 3: Multiple Rapid Changes
1. User drags handle rapidly
2. Multiple ResizeObserver callbacks fire
3. All callbacks batched into **single RAF** call
4. SmartBorder calculates **once** per frame
5. ResizeHandlesWrapper updates **only if significant change**
6. No circular update loops ✅

## Verification Queries

After implementing fixes, verify with these log queries:

```bash
# Check SmartBorder calculation frequency (should be ~1 per resize action)
python backend/enhanced_diagnostic_logs.py --frontend-only --frontend-filter "smartborder.path" --limit 20

# Check resize sequence (should show preserved inputWidthOverride)
python backend/enhanced_diagnostic_logs.py --frontend-only --frontend-component "text-1768298739656-235" --frontend-filter "resize.width" --limit 10

# Check for timing issues (should show consistent widths)
python backend/enhanced_diagnostic_logs.py --frontend-only --frontend-component "text-1768298739656-235" --limit 50 | grep -E "(resize.preview.applied|smartborder.path)" | head -20
```

## Success Criteria

✅ **Single SmartBorder calculation per resize**: Logs show 1 `smartborder.path.calculated` per resize action  
✅ **DOM bounds match**: `appliedStyles.width` matches `domBounds.width` (within scale factor)  
✅ **No circular updates**: ResizeHandlesWrapper updates don't trigger SmartBorder recalculation  
✅ **Input width preserved**: `resize.width.calculated` shows `inputWidth` preserved when manually set  
✅ **Handles aligned**: Visual inspection shows resize handles always form rectangle around SmartBorder

## Files Modified

1. `frontend/src/features/builder/components/ui/SmartBorder.tsx`
   - Added batching to `calculatePath()` via `isScheduled` flag

2. `frontend/src/features/builder/components/SortableComponent.tsx`
   - Enhanced `ResizeHandlesWrapper` with RAF batching and threshold checking
   - Fixed outer container width calculation to include SmartBorder padding
   - Updated `resizeHandleProps` to use expanded width
   - Preserved manually set `inputWidthOverride` during E/W resize

## Testing Checklist

- [ ] Resize inputWidthOverride → Handles stay aligned
- [ ] Resize component width → inputWidthOverride preserved (if manually set)
- [ ] Rapid resize → No excessive SmartBorder recalculations
- [ ] Check logs → Single calculation per resize action
- [ ] Visual inspection → Handles always form rectangle around SmartBorder
