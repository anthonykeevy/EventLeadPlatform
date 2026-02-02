# Resize Handle Discrepancy Analysis

## Executive Summary

After testing all 8 resize handles (N, S, E, W, NE, NW, SE, SW), significant discrepancies have been identified between the expected component position/size based on mouse movement and the final committed values.

## Test Results Overview

| Handle | Operations | Perfect Matches | Critical Issues |
|--------|-----------|----------------|-----------------|
| **SE** | 19 | 0 (0%) | Width -47.33px max |
| **NE** | 3 | 0 (0%) | Position Y -6px |
| **SW** | 3 | 0 (0%) | Position X +8.67px, Width -8.67px |
| **NW** | 3 | 0 (0%) | **Position Y -79.33px**, Position X +6.67px, Width -6.67px |

**Zero perfect matches** across all tested handles - all resize operations have discrepancies > 1px tolerance.

## Critical Finding: Corner Handles Use Wrong Base Calculation

### The Problem

In `SortableComponent.tsx`, the corner resize logic at line 2150-2161 calculates the **expected** position/size using:

```typescript
// Calculate expected final position/size based on mouse movement
const expectedPosition = { ...currentPosition };
const expectedWidth = currentWidth + deltaX * (horizontalHandle === 'w' ? -1 : 1);

// For W handles, position should shift left by deltaX
if (horizontalHandle === 'w') {
    expectedPosition.x = currentPosition.x + deltaX;
}

// For N handles, position should shift up by deltaY
if (verticalHandle === 'n') {
    expectedPosition.y = currentPosition.y + deltaY;
}
```

**This calculation is INCORRECT** because it assumes:
- `deltaX` directly translates to width change
- `deltaY` directly translates to height change
- Mouse delta = component size delta

But this **does NOT account for**:
1. **Object width redistribution** in `handleWidthChange`
2. **Min/max width constraints**
3. **Grid padding, borders, gaps** (totalExtras)
4. **Two-phase height/gap cascading** in vertical resize
5. **Collision detection adjustments**

### The Actual Implementation (E/W Handles)

The **actual** width calculation in `handleWidthChange` (lines 1385-1750) is vastly more complex:

```typescript
// 1. Apply scale factor
const scaleFactor = componentScale / 100 * scale;
const oldWidthPx = parseFloat(component.props.width || '300px');

// 2. Calculate total extras (gaps, padding, borders)
const totalExtras = (columnGap * 2) + 10 + paddingLeftPx + paddingRightPx + borderLeftPx + borderRightPx;

// 3. Calculate available space for objects
const adjustedWidth = oldWidthPx + widthDelta;
const available = adjustedWidth - totalExtras;

// 4. Lock label/help widths, input absorbs ALL change
const lockedLabelWidth = Math.max(component.props.labelWidthOverride ?? measuredLabelWidth, minLabelWidth);
const lockedHelpWidth = Math.max(component.props.helpWidthOverride ?? measuredHelpWidth, minHelpWidth);

// 5. Calculate input width
const remainingForInput = newWidth - lockedLabelWidth - lockedHelpWidth - totalExtras;
const adjustedInputWidth = Math.max(minInputWidth, Math.round(remainingForInput));

// 6. If input hits minimum, expand component to fit
const calculatedWidth = lockedLabelWidth + adjustedInputWidth + lockedHelpWidth + totalExtras;
if (calculatedWidth > newWidth) {
    newWidth = Math.round(calculatedWidth);
}

// 7. Apply collision detection constraints
const resolved = resolveResizeConstraints(...);
if (!resolved.accepted) {
    // Resize rejected
    return;
}

// 8. For W handle: calculate left shift based on ACTUAL width change
const actualWidthChange = newWidth - oldWidthPx;
const leftShift = -(actualWidthChange * scaleFactor);
```

**Key Point**: The final `leftShift` for W handles is based on the **actual** width change after all constraints, NOT the simple `deltaX`.

### Why This Causes Discrepancies

#### Width Discrepancy (All W handles: NW, SW)
The **expected** width is: `currentWidth + deltaX * -1`  
The **actual** width is: `oldWidthPx + (complex calculation with constraints)`

Result: Width is consistently **narrower** than expected (negative discrepancy up to -47.33px for SE, -8.67px for SW/NW).

#### Position X Discrepancy (W handles: NW, SW)
The **expected** position is: `currentPosition.x + deltaX`  
The **actual** position is: `currentPosition.x + leftShift` (where `leftShift = -(actualWidthChange * scaleFactor)`)

Since `actualWidthChange < deltaX` (due to constraints), `leftShift` is smaller, so position doesn't shift left as much.

Result: Component shifts **less** to the left than expected (positive X discrepancy up to +8.67px).

#### Position Y Discrepancy (N handles: NE, NW)
The **expected** position is: `currentPosition.y + deltaY`  
The **actual** position uses two-phase logic in `handleVerticalResizeEnd`:

```typescript
// Phase 1: Adjust input height
const heightDeltaUsed = finalInputHeight - currentInputHeight;

// Phase 2: Adjust gap (if height maxed out)
const spacingDeltaUsed = appliedLabelGap - currentLabelGap;

// Calculate top shift
const fallbackShift = -(heightDeltaUsed + spacingDeltaUsed);
const appliedShift = previewTopShift ?? fallbackShift;
```

Result: Position shift is based on **actual height + gap changes**, not simple `deltaY`. This causes massive discrepancies (NW: -79.33px!).

## Root Cause Analysis

### The Core Issue

The `handleCornerResizeEnd` function calculates "expected" values **assuming direct mouse-to-component mapping**, but then delegates to `handleWidthChange` and `handleVerticalResizeEnd` which apply:
1. Constraint logic
2. Min/max clamping
3. Object width redistribution
4. Two-phase cascading
5. Scale factor adjustments
6. Collision detection

**These actual implementations produce different results than the naive mouse-delta calculation.**

### Why E/S Handles Don't Show Position Discrepancies

- **E handle**: Position is **anchored** (west edge stays fixed), so position.x never changes. Width discrepancy still exists but isn't visible as a position mismatch.
- **S handle**: Position is **anchored** (north edge stays fixed), so position.y never changes. Height/gap changes don't affect position.

### Why N/W Handles Show Large Discrepancies

- **N handle**: Two-phase logic (height→gap) means `deltaY` doesn't directly map to position shift. The actual shift depends on which phase consumed the delta.
- **W handle**: Width constraints mean `deltaX` doesn't directly map to width change OR position shift. The actual leftShift is calculated from constrained width change.

## Solution Approaches

### Option 1: Remove "Expected" Calculation (Quick Fix)

**Remove the expectedPosition/expectedWidth calculation entirely** and just log the discrepancy between:
- Initial state (before resize)
- Final state (after resize)
- Mouse delta

This eliminates the false "expected" values that don't match the actual implementation logic.

**Pros**: 
- Simple, no logic changes
- Accurately reflects what actually happened

**Cons**:
- Doesn't fix the underlying issue that final != expected
- Still need to determine if discrepancy is a bug or expected behavior

### Option 2: Calculate Expected After Constraints (Accurate)

**Move the expected calculation to AFTER `handleWidthChange`/`handleVerticalResizeEnd` complete**, capturing their actual return values.

This would require refactoring these functions to return the actual changes applied:

```typescript
interface ResizeResult {
    finalWidth: number;
    finalPosition: { x: number; y: number };
    applied: {
        widthChange: number;
        heightChange: number;
        gapChange: number;
        positionShift: { x: number; y: number };
    };
}
```

**Pros**:
- Accurate "expected" values that match implementation
- Can still detect discrepancies (implementation bugs)

**Cons**:
- Requires significant refactoring
- Complex to implement

### Option 3: Reverse-Calculate Expected from Implementation (Best)

**Use the same logic that `handleWidthChange`/`handleVerticalResizeEnd` use** to calculate the expected final state in `handleCornerResizeEnd`.

This means duplicating (or extracting) the constraint/calculation logic:

```typescript
// Calculate expected using ACTUAL implementation logic
const { expectedWidth, expectedPositionShift } = calculateExpectedWidthResize(
    component,
    deltaX,
    horizontalHandle,
    { measureObjectWidths, applyConstraints: true }
);

const { expectedHeightChange, expectedGapChange, expectedTopShift } = calculateExpectedVerticalResize(
    component,
    deltaY,
    verticalHandle,
    { measureObjectHeights, applyConstraints: true }
);

const expectedPosition = {
    x: currentPosition.x + (horizontalHandle === 'w' ? expectedPositionShift.x : 0),
    y: currentPosition.y + (verticalHandle === 'n' ? expectedTopShift : 0),
};
```

**Pros**:
- Accurate expected values
- Matches actual implementation
- Can detect real bugs (discrepancies between expected and actual)

**Cons**:
- Requires extracting calculation logic to pure functions
- More work upfront

## Recommendation

**Option 3** is the best long-term solution because it:
1. Provides accurate "expected" values that match the implementation
2. Allows detection of real bugs (when final != expected after applying same logic)
3. Improves code maintainability by extracting calculation logic to pure functions

However, given the complexity, **Option 1** (remove expected calculation) could be a quick interim solution to get accurate measurements of what's actually happening.

## Next Steps

1. **Clarify user intent**: Does the user want the corner handle to move the component edge to exactly where the mouse pointer is? Or is it acceptable for constraints to cause deviation?

2. **If exact mouse placement is required**:
   - Need to refactor resize logic to work backwards from mouse position
   - Calculate: "what widths/heights/gaps would place the corner exactly at mouse pointer?"
   - This is a fundamentally different approach than current "apply delta, then constrain"

3. **If constraint-based behavior is acceptable**:
   - Implement Option 3 to accurately predict final state
   - Document that constraints may cause corner to not align exactly with mouse pointer
   - Ensure discrepancies are minimal (< 5px) for good UX

4. **Test with updated logging**:
   - Remove naive expected calculation
   - Log actual state changes
   - Measure user perception of "corner following mouse"
