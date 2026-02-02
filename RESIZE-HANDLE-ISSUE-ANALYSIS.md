# Resize Handle Issue Analysis - Company Name Component (Form 44)

## Issue Description
When resizing the Company Name component using the right resize handle in a horizontal layout:
1. **During drag**: Component does not update visually
2. **On drop**: Component moves to the left instead of staying anchored and expanding right

## Component Details

### Initial State (Captured)
- **Component ID**: `text-1768184324292-685`
- **Component Type**: `text` (Text Input)
- **Label**: "Company Name"
- **Position**: x: 100px, y: 316.05px
- **Width**: `"50%"` (percentage, not pixels!)
- **Computed Width**: 960px (rendered)
- **Actual DOM Width**: 885.5px (scaled/rendered)
- **Object Layout**: Horizontal (objects arranged in a row)
- **Row Alignment**: Center

### Component Structure
- **Objects**: label, input, validation (all visible)
- **Layout Type**: Horizontal (flex display)
- **SmartBorder Layout**: `"fill"` (not "shrink")

## Root Cause Analysis

### Key Finding: Percentage Width + Horizontal Layout + Fill Mode

The component has:
1. **Width**: `"50%"` (percentage-based, not fixed pixels)
2. **Object Layout**: `horizontal` (objects in a row)
3. **SmartBorder Layout**: `"fill"` (component fills available width)

### Issue in Resize Logic

Looking at `SortableComponent.tsx` lines 724-742:

```typescript
let oldWidthPx: number;
if (oldWidth?.endsWith('px')) {
    oldWidthPx = parseInt(oldWidth, 10);
} else {
    // For percentage or undefined width, use actualDomWidth state
    if (actualDomWidth !== null) {
        oldWidthPx = actualDomWidth;
    } else {
        // Fallback: calculate percentage
        const canvasWidth = useBuilderStore.getState().formDefinition?.canvasSettings?.width || 1920;
        if (oldWidth?.endsWith('%')) {
            const pct = parseFloat(oldWidth);
            oldWidthPx = Math.max(50, Math.round((pct / 100) * canvasWidth));
        } else {
            oldWidthPx = 300; // Default fallback
        }
    }
}
```

**Problem**: When resizing a component with percentage width:
1. The code correctly calculates `oldWidthPx` from the percentage
2. It calculates `newWidth` based on the drag delta
3. **BUT**: It then sets `width: ${newWidth}px` (converting to pixels)
4. However, the **position calculation** might be using the wrong reference point

### Specific Issue for Horizontal Layout

For horizontal layouts with percentage widths:
- The component uses `smartBorderLayout: "fill"` 
- The SmartBorder wraps the content but the component container might be sized differently
- When the width changes from percentage to pixels, the position reference might shift

### Position Calculation Issue

Looking at lines 998-1002 (E handle commit):

```typescript
const westEdgeBefore = oldPosition.x ?? 0;
const eastEdgeBefore = (oldPosition.x ?? 0) + oldWidthPx;
const westEdgeAfter = oldPosition.x ?? 0;  // Should stay same
const eastEdgeAfter = (oldPosition.x ?? 0) + newWidth;  // Should expand right
```

**Expected Behavior (E handle)**:
- West edge (left) should stay at x: 100
- East edge (right) should expand: 100 + newWidth

**Actual Behavior**:
- Component moves left (west edge shifts)
- This suggests the position is being recalculated incorrectly

## Likely Causes

1. **Percentage to Pixel Conversion**: When converting from `"50%"` to pixels, the reference point for position calculation might be wrong
2. **SmartBorder Fill Mode**: With `smartBorderLayout: "fill"`, the component's visual bounds might differ from its logical bounds
3. **Horizontal Layout Spacing**: The horizontal layout might be affecting how width changes are applied
4. **Preview State**: The resize preview (`resizePreview`) might not be updating correctly during drag for percentage-width components

## Recommended Fixes

### Fix 1: Ensure Position Stays Anchored for E Handle
In `SortableComponent.tsx` `handleWidthChange`, ensure that for E handle:
- Position.x should NEVER change
- Only width should change

### Fix 2: Handle Percentage Width Conversion
When converting percentage to pixels during resize:
- Calculate the new percentage based on drag delta
- OR convert to pixels but ensure position reference is correct

### Fix 3: Fix Preview State for Horizontal Layouts
Ensure `resizePreview.width` is correctly calculated and applied during drag for horizontal layouts with percentage widths.

### Fix 4: SmartBorder Fill Mode Handling
When `smartBorderLayout: "fill"`, ensure resize calculations account for the fill behavior and don't cause position shifts.

## Testing Steps

1. Select Company Name component
2. Note initial position: x: 100, width: "50%"
3. Grab right resize handle (E handle)
4. Drag right 50px
5. **Expected**: Component stays at x: 100, width becomes ~1010px (or appropriate pixel value)
6. **Actual**: Component moves left, position changes incorrectly

## Logs to Check

After attempting resize, check logs for:
- `resize.handle.pointerdown`
- `resize.handle.start`
- `resize.handle.move` (should show delta values)
- `resize.handle.commit` (should show final width and position)
- `resize.width.calculated` (should show before/after widths)
- `resize.commit.edge.position` (should show edge positions)

## Fix Applied

### Changes Made to `SortableComponent.tsx`

1. **Early Width Constraint for E Handle** (before object width calculations):
   - Added canvas boundary check specifically for E handle resizes
   - If new width would exceed canvas bounds, constrain width instead of allowing position adjustment
   - Constraint happens BEFORE object width calculations, so object widths use the constrained component width

2. **Prevent Position Adjustment for E Handle**:
   - After collision resolution, check if this is an E handle resize
   - If collision resolver tries to adjust position for E handle, reject the position change
   - Position stays fixed at original x coordinate

### Code Changes

**Location**: `frontend/src/features/builder/components/SortableComponent.tsx`

1. **Lines ~743-770**: Added early width constraint check for E handle before object width calculations
2. **Lines ~873-895**: Modified collision resolution result handling to prevent position adjustments for E handle

### Expected Behavior After Fix

1. **During drag**: Component preview should update correctly (may need separate fix for preview)
2. **On drop**: 
   - Component position stays at x: 100 (west edge anchored)
   - Component width expands right (east edge moves)
   - If width would exceed canvas, it's constrained but position doesn't change

## Testing Steps

1. Select Company Name component
2. Note initial position: x: 100, width: "50%" (≈960px)
3. Grab right resize handle (E handle)
4. Drag right 50px
5. **Expected**: 
   - Component stays at x: 100
   - Width becomes ~1010px (or constrained if exceeds canvas)
   - Component does NOT move left
6. **Verify**: Check logs for `resize.east.handle.width.constrained` if width was constrained

## Investigation Update - Preview Not Showing

### Log Analysis Results

After testing the resize, logs show:

**✅ Preview State IS Being Set:**
- `resize.preview.width.applied`: `previewWidth: 1109.33px` ✓
- `resize.preview.applied`: `appliedStyles: { width: "1109.3333129882812px", left: 100 }` ✓

**❌ DOM Width NOT Updating:**
- `domBounds: { width: 1023.2445068359375 }` - stays at ~1023px instead of 1109px ✗
- Component width should be expanding but DOM shows no change

### Root Cause Identified

**Issue**: SmartBorder with `layout: "fill"` uses `w-full` (width: 100%) which fills its container. However, the container width IS being set correctly via `style.width: "1109px"`, but the **content inside SmartBorder is not respecting the container width** during resize preview.

**Specific Problem**: 
1. SortableComponent sets `style.width: "1109px"` on container ✓
2. SmartBorder wrapper gets `w-full` (100% of container) ✓  
3. BUT: UniversalFieldShell content inside SmartBorder is not using `previewWidth` correctly for horizontal layouts
4. The content is still using the original component width, so SmartBorder calculates bounds based on old content size

### Bug Location

**File**: `frontend/src/features/builder/components/UniversalFieldShell.tsx`

**Lines 309-324**: When calculating preview width ratios:
```typescript
if (previewWidth) {
    const currentWidthPx = component.props.width?.endsWith('px') 
        ? parseInt(component.props.width, 10) 
        : 300;  // ❌ WRONG: Defaults to 300px for percentage widths!
    const widthRatio = previewWidth / currentWidthPx;
    // ... scales object widths
}
```

**Problem**: 
- Component has `width: "50%"` (percentage)
- Code defaults to `300px` instead of using actual rendered width
- `widthRatio` calculation is completely wrong
- Object widths scale incorrectly
- SmartBorder calculates bounds from incorrectly-sized content

### Additional Issue: SmartBorder Fill Mode

When `smartBorderLayout: "fill"`:
- SmartBorder uses `w-full` (100% width)
- Content inside should respect container width
- But UniversalFieldShell's object groups might not be using the previewWidth correctly
- Need to ensure object groups get the correct width during preview

## Fixes Needed

### Fix 1: Use Actual Width for Preview Ratio Calculation

In `UniversalFieldShell.tsx`, when calculating `currentWidthPx` for preview:
- For percentage widths, use the actual rendered width (from `actualDomWidth` or calculate from percentage)
- Don't default to 300px

### Fix 2: Ensure Container Width is Applied During Preview

Ensure that when `previewWidth` is set:
- The container div gets the correct width
- SmartBorder respects the container width
- Content inside UniversalFieldShell uses the preview width for layout calculations

### Fix 3: Handle Horizontal Layout Preview

For horizontal layouts specifically:
- Object groups need to use the preview width
- Flex containers should expand to fill the preview width
- Label/Input/Help objects should scale proportionally

## Fix Applied - Preview Width Calculation

### Changes Made

**File**: `frontend/src/features/builder/components/UniversalFieldShell.tsx`

1. **Added `currentWidthPx` prop** to UniversalFieldShellProps interface
2. **Fixed preview width ratio calculation**:
   - Now uses `currentWidthPx` prop when available (for percentage-width components)
   - Falls back to parsing component.props.width for pixel values
   - Only uses 300px default as last resort
3. **Updated `renderObjectGroup` function** to accept and use `currentWidthPx`

**File**: `frontend/src/features/builder/components/SortableComponent.tsx`

1. **Added `currentWidthPxForPreview` calculation**:
   - Calculates current width from component.props.width or actualDomWidth
   - Handles percentage widths correctly by calculating from canvas width
   - Only calculated during horizontal resize preview
2. **Pass `currentWidthPx` to UniversalFieldShell**:
   - All UniversalFieldShell calls now pass `currentWidthPx={currentWidthPxForPreview}`
   - Ensures preview ratio calculation uses correct base width

### How It Works

1. **During resize drag**:
   - SortableComponent calculates `currentWidthPxForPreview` from component.props.width
   - For percentage widths: calculates from canvas width (1920px default)
   - Passes both `previewWidth` (new width) and `currentWidthPx` (old width) to UniversalFieldShell
   - UniversalFieldShell calculates `widthRatio = previewWidth / currentWidthPx`
   - Object widths scale proportionally: `newWidth = oldWidth * widthRatio`

2. **Result**:
   - Object widths scale correctly during preview
   - SmartBorder calculates bounds from correctly-sized content
   - Component visually expands during drag

## Fix Applied - Initialization Order Issue

### Bug: ReferenceError - Cannot access 'isHorizontalResize' before initialization

**Issue**: `currentWidthPxForPreview` useMemo was trying to use `isHorizontalResize` before it was defined.

**Fix**: Moved `currentWidthPxForPreview` calculation to after `isHorizontalResize` is defined, and updated the useMemo to calculate `isHorizontalResize` locally instead of relying on the outer variable.

**Location**: `frontend/src/features/builder/components/SortableComponent.tsx` lines ~1724-1740

## Testing After Fix

1. Select Company Name component
2. Grab right resize handle
3. **Expected during drag**: Component visually expands right, width increases
4. **Expected on drop**: Component stays at x: 100, width is updated to new value
5. **Verify**: DOM bounds should match preview width during drag
6. **Check logs**: `resize.preview.width.applied` should show correct previewWidth, and DOM bounds should update

## Summary of All Fixes Applied

1. ✅ **E Handle Position Fix**: Prevent position adjustment for E handle resizes
2. ✅ **Preview Width Calculation Fix**: Pass `currentWidthPx` to UniversalFieldShell for correct ratio calculation
3. ✅ **Initialization Order Fix**: Moved `currentWidthPxForPreview` calculation after `isHorizontalResize` definition
4. ✅ **Props Destructuring Fix**: Added `currentWidthPx` to props destructuring in UniversalFieldShell component

## Fix Applied - Props Destructuring

### Bug: ReferenceError - currentWidthPx is not defined

**Issue**: `currentWidthPx` was added to the interface and function signature, but was not destructured from props in the main component function.

**Fix**: Added `currentWidthPx` to the props destructuring in `UniversalFieldShell` component.

**Location**: `frontend/src/features/builder/components/UniversalFieldShell.tsx` line ~607

## Current Issue - Resize Handles Not Working

### User Report
- **Right resize handle (E handle)**: Does nothing - no visual feedback during drag
- **Left resize handle (W handle)**: Only moves the component instead of resizing

### Investigation

**Hypothesis**: `displayWidth` is not updating reactively when `resizePreview.width` changes during drag.

**Code Analysis**:
1. `resizePreview.width` is set in `handleResize` (line ~521) when E or W handle is dragged
2. `displayWidth` is calculated from `baseWidthPx` which uses `resizePreview?.width` (line ~1650)
3. `displayWidth` is applied to container `style.width` (line ~1782)

**Potential Issues**:
1. `resizePreview.width` might not be set correctly during drag
2. React might not be re-rendering when `resizePreview` state changes
3. Container style might not be applying the width correctly
4. CSS might be overriding the inline width style

### Fixes Applied

1. **Added debug logging** to track `resizePreview.width` and `displayWidth` calculation
2. **Enhanced logging** in `setResizePreview` to verify preview state is being set
3. **Improved `displayWidth` calculation** to ensure it always uses `resizePreview.width` when available during resize

### Next Steps

1. Test resize handles and check browser console for debug logs
2. Verify `resizePreview.width` is being set during drag
3. Verify `displayWidth` is being calculated correctly
4. Verify container `style.width` is being applied
5. Check for CSS conflicts that might prevent width from updating

## Log Analysis Results

### Test Results (2026-01-19 08:52)

**W Handle (Left) - WORKING:**
- ✅ `resize.handle.move` events logged
- ✅ `resize.width.calculated` shows correct previewWidth (985px)
- ✅ `resize.preview.width.applied` shows styleWidth is set correctly
- ✅ Component position updates correctly (moves left as expected)
- ⚠️ **Issue**: DOM width not updating - `domBounds.width: 909px` while `styleWidth: "985px"`

**E Handle (Right) - NOT WORKING:**
- ❌ **NO `resize.handle.move` events logged** - Handle not triggering at all
- ❌ No preview width calculations
- ❌ No style application logs
- **Root Cause**: E handle pointer events not being captured/processed

### Key Findings

1. **E Handle Not Triggering**: The E handle isn't generating any events, suggesting:
   - Handle might not be visible/clickable
   - Pointer events might be blocked
   - Handle might be positioned incorrectly
   - Z-index issue preventing clicks

2. **DOM Width Not Updating**: Even for W handle (which is working), the DOM width stays at 909px while style.width is set to 985px. This suggests:
   - CSS might be overriding inline styles
   - Container might have `min-width` or `max-width` constraints
   - SmartBorder or UniversalFieldShell might be preventing width update
   - React might not be re-rendering the container

### Next Investigation Steps

1. **Check E Handle Visibility**: Verify E handle is rendered and clickable
2. **Check Pointer Events**: Verify E handle has proper pointer event handlers
3. **Check DOM Width Issue**: Investigate why `style.width` isn't affecting DOM width
4. **Check CSS Overrides**: Look for CSS rules that might override inline width

## Component-Specific Behavior Discovery

### Key Finding: E Handle Works for Radio, Not for Text

**Radio Component (`radio-1768185353302-287`) - WORKING:**
- ✅ Many `resize.handle.move` events with `handle: "e"`
- ✅ `resize.preview.width.applied` logs show correct preview width
- ✅ Position stays anchored: `previewPositionLeft: 102`, `originalLeft: 102` (correct for E handle)
- ✅ Style width matches preview width: `styleWidth: "2220.3333740234375px"`

**Text Component (`text-1768184324292-685`) - NOT WORKING:**
- ❌ **NO `resize.handle.move` events** with `handle: "e"`
- ❌ E handle appears to not be triggering at all

### Differences Between Components

1. **Both use UniversalFieldShell**: Both text and radio components use the same rendering path (UniversalFieldShell)
2. **Both have ResizeHandles**: Both should have E/W handles rendered
3. **Different SmartBorder behavior**: Text components use `smartBorderLayout: "fill"` while radio might use different layout

### Hypothesis

The E handle might be:
1. **Positioned off-screen** for text components (SmartBorder with `fill` layout might be expanding beyond container)
2. **Blocked by SmartBorder SVG path** (the drag path might be covering the E handle)
3. **Z-index issue** (SmartBorder z-index: 20, ResizeHandles z-index: 50, but SmartBorder path might be intercepting)
4. **Container width issue** (if container width isn't updating, E handle position calculation might be wrong)

### Next Steps

1. **Check SmartBorder bounds** for text vs radio components
2. **Verify E handle position** relative to SmartBorder bounds
3. **Check if SmartBorder SVG path** is covering the E handle area
4. **Investigate `smartBorderLayout: "fill"`** behavior - does it cause SmartBorder to expand beyond container?

## Root Cause Analysis

### The Problem Chain

1. **Container width style is set** (`style.width: "985px"`) ✓
2. **DOM width doesn't update** (`domBounds.width: 909px`) ✗
3. **SmartBorder calculates bounds** from content (which is still 909px wide)
4. **SmartBorder path extends** beyond where container thinks it should be
5. **ResizeHandlesWrapper positions E handle** based on SmartBorder path bounds
6. **E handle ends up positioned incorrectly** (off-screen or outside clickable area)
7. **E handle clicks don't register** because handle isn't where user expects

### Why Radio Works But Text Doesn't

**Radio components:**
- May use different SmartBorder layout (`shrink` vs `fill`)
- May have different content structure that doesn't expand beyond container
- SmartBorder bounds match container width
- E handle positioned correctly

**Text components:**
- Use `smartBorderLayout: "fill"` 
- Horizontal layout with objects that might expand
- Container width set but DOM doesn't update
- SmartBorder calculates bounds from actual content (wrong size)
- E handle positioned incorrectly

### Solution Approach

The fix needs to ensure:
1. **Container width actually affects DOM** - Force React to re-render or ensure CSS doesn't override
2. **SmartBorder respects container width** - Ensure `fill` layout uses container width, not content width
3. **ResizeHandlesWrapper uses correct bounds** - Position handles relative to container, not SmartBorder path if path is wrong

## Fix Applied - Fallback Path Alignment

### Issue Identified

The fallback rendering path (used by radio, checkbox, and other components not in `universalFieldShellTypes`) had different behavior than the primary path:

**Primary Path (text, dropdown, etc.):**
- Uses `ResizeHandlesWrapper` for correct handle positioning
- Sets `smartBorderLayout: hasExplicitWidth ? 'fill' : 'shrink'`
- Uses `outerRef` which properly sets `outerContainerRef`

**Fallback Path (radio, checkbox, etc.):**
- Used `ResizeHandles` directly (no wrapper)
- Missing `smartBorderLayout` setting
- Used `combinedRef` instead of `outerRef`

### Changes Made

1. **Added logging** when fallback path is used:
   - Logs component type, reason for fallback, and recommendation
   - Event: `component.rendering.fallback`

2. **Aligned fallback path with primary path**:
   - Added `smartBorderLayout: hasExplicitWidth ? 'fill' : 'shrink'` to match primary path
   - Changed to use `ResizeHandlesWrapper` instead of direct `ResizeHandles`
   - Changed `ref={combinedRef}` to `ref={outerRef}` to match primary path

### Expected Behavior

- All components now use the same resize handle positioning logic
- Fallback path components will have consistent behavior with primary path
- Logging will show which components are using fallback (should be rare)
- Components with structures (like radio) should use primary path, not fallback

### Next Steps

1. Test resize handles on radio, checkbox, and text components
2. Check logs for `component.rendering.fallback` to see which components use fallback
3. Consider adding radio/checkbox to `universalFieldShellTypes` if they should always use primary path

---

## Fix Applied - Resize Delta Scaling Issue (2026-01-19)

### Problem
User reported that when adjusting the E handle, the resize happens at a rate "way more than what I am moving the mouse." Logs showed huge `deltaWidth` values (230-309px) for normal mouse movements.

### Root Cause
**ResizeHandles.tsx** was mixing screen pixels (`deltaX` from mouse events) with base pixels (`startSizeRef.current.width` from component props) in the calculation:
```typescript
newWidth = startSizeRef.current.width + widthDelta; // WRONG: mixing units!
```

Then it passed `deltaWidth = newWidth - startSizeRef.current.width = widthDelta` (screen pixels) to `onResize`.

**SortableComponent.tsx** was only accounting for `componentScale` (component's own scale like 100%, 150%) but NOT accounting for canvas zoom level, causing incorrect conversion from screen pixels to base pixels.

### Fix Applied

1. **ResizeHandles.tsx** (lines 258-276):
   - For E/W handles (`config.action === 'width'`), now passes raw screen pixel delta (`deltaX`) directly to `onResize`
   - Avoids mixing screen pixels with base pixels in the calculation
   - Added comment explaining the critical fix

2. **SortableComponent.tsx** (lines 501-530):
   - Now accounts for BOTH `componentScale` AND canvas zoom (`scale` from store)
   - Canvas scale is stored as decimal (0.5 = 50%, 1.0 = 100%, 2.0 = 200%)
   - Conversion: `baseWidthDelta = deltaWidth / (componentScaleFactor * canvasScaleFactor)`
   - Added detailed logging via `resize.delta.conversion` event to track conversions

### Expected Behavior
- Mouse movement of 10 screen pixels should now correctly resize by the appropriate number of base pixels
- At 100% canvas zoom and 100% component scale: 10 screen px = 10 base px
- At 50% canvas zoom and 100% component scale: 10 screen px = 20 base px
- At 200% canvas zoom and 100% component scale: 10 screen px = 5 base px

### Testing
Check logs for `resize.delta.conversion` events to verify:
- `deltaWidthScreenPx`: Should match actual mouse movement (typically 1-10px per event)
- `baseWidthDelta`: Should be correctly converted based on canvas and component scale
- `nextWidth`: Should increment smoothly and proportionally to mouse movement

---

## Fix Applied - Incremental Resize Base Width (2026-01-19)

### Problem
After fixing the scaling issue, resize was still not working correctly. Logs showed that `currentWidthPx` was staying constant (535px) for all resize events, meaning each delta was being calculated from the original starting position, not incrementally from the previous preview position.

### Root Cause
**SortableComponent.tsx** was always using `currentWidthPx` (the original component width from props) as the base for calculating `nextWidth`, even during an active resize preview. This caused:
- First event: `nextWidth = 535 + delta1` ✓
- Second event: `nextWidth = 535 + delta2` ✗ (should be `prevWidth + delta2`)
- Third event: `nextWidth = 535 + delta3` ✗ (should be `prevWidth + delta3`)

Each resize event was cumulative from the start position, not incremental from the previous preview.

### Fix Applied

**SortableComponent.tsx** (lines 517-518):
- Changed from: `const nextWidth = currentWidthPx + baseWidthDelta;`
- Changed to: 
  ```typescript
  const baseWidth = resizePreview?.width ?? currentWidthPx;
  const nextWidth = baseWidth + baseWidthDelta;
  ```
- Now uses `resizePreview.width` (the previous preview width) as the base if a resize is in progress
- Updated logging to show both `originalWidthPx` and `baseWidthUsed`
- Fixed edge position calculations to use `baseWidth` instead of `currentWidthPx`

### Expected Behavior
- First resize event: Uses original width as base
- Subsequent resize events: Use previous preview width as base
- Resize should now be smooth and incremental, matching mouse movement exactly

### Testing
Check logs for `resize.delta.conversion` events:
- `originalWidthPx`: Should be the component's original width (constant)
- `baseWidthUsed`: Should increment with each event (matches previous `nextWidth`)
- `nextWidth`: Should increment smoothly from `baseWidthUsed`, not jump back to original

---

## Fix Applied - Commit Width Uses Preview (2026-01-19)

### Problem
Even with correct preview behavior, the width could snap back on drop. Logs showed `resize.commit.width` using a smaller width than the preview, especially when canvas scale was not 1.0.

### Root Cause
`ResizeHandles` calculates the final width on pointer-up using only component scale, not canvas scale. This produced a `newWidth` that didn't match the preview width (which already accounted for canvas scale), causing a jump on commit.

### Fix Applied
**SortableComponent.tsx** (resize handle props):
- On `onWidthChange`, commit using the preview width when available:
  ```typescript
  const commitWidth = resizePreview?.width ?? newWidth;
  handleWidthChange(commitWidth);
  ```
- This ensures the committed width matches the live preview and avoids snap-back.

### Expected Behavior
- On drop, the component retains the same width shown during drag.
- `resize.commit.width.after.width` should match the last `resize.preview.width.applied.previewWidth`.

---

## Fix Applied - Clamp Object Widths to Container (2026-01-19)

### Problem
Even when the container width preview/commit was correct, the **input/label/help widths could remain larger** than the container (especially when a component hit its min width). This made components look like they weren’t resizing or were “stuck,” even though width was changing.

### Root Cause
Object widths were scaled proportionally but **never clamped** to the container width during preview or commit. For some components (radio/textarea), the input width remained large while the container hit a smaller width, causing visual mismatch.

### Fix Applied

1. **Preview Clamp (UniversalFieldShell.tsx)**  
   When `previewWidth` is active, label/input/help overrides are now clamped to `previewWidth` (min 10px) so object widths can never exceed the container.

2. **Commit Clamp (SortableComponent.tsx)**  
   On commit, `newLabelWidth`, `newInputWidth`, and `newHelpWidth` are now clamped to `newWidth` (min 10px).

### Expected Behavior
- Object widths always stay within the container during resize.
- Components visually shrink/expand with the handle instead of appearing stuck.

---

## Fix Applied - Grid Layout Respects Preview Width (2026-01-19)

### Problem
On grid layout components, the resize preview width was updating in state, but the **DOM width stayed fixed**, so objects appeared to float and the component looked unresponsive.

### Root Cause
`renderWithGridLayout()` only stretched the grid container (`width: 100%`) when the component had an explicit `props.width`.  
During live resize, `previewWidth` exists but `props.width` may still be `undefined`, so the grid container stayed auto-sized and ignored the preview width.

### Fix Applied
**UniversalFieldShell.tsx**
- Updated `renderWithGridLayout()` to **stretch the grid container when `previewWidth` is present**, not just when `props.width` is set.
- Now: `shouldStretchToContainer = hasExplicitWidth || previewWidth !== undefined`
- Ensures grid layout respects the live preview width during resize.

### Additional Logging
**SortableComponent.tsx**
- Added `layoutContext` to `fieldshell.resize.grabbed` with:
  - `objectLayout`, `layoutGroups`, `rowAlignment`, `objectSpacing`
  - `gridLayout`, `defaultGridLayout`
- This captures the exact layout config at the moment of grab for grid debugging.

### Expected Behavior
- Grid layout components resize visually with the handle.
- SmartBorder bounds should track the preview width instead of staying fixed.

---

## Fix Applied - Grid Layout Uses Explicit Preview Width (2026-01-20)

### Problem
Grid layout preview width was increasing, but `domBounds.width` stayed fixed (~503px).  
This caused huge apparent jumps (e.g., 15px mouse move → 200–500px width change) because the base width used for math was far larger than the actual visible DOM width.

### Root Cause
`renderWithGridLayout()` set `width: 100%` during resize, but **the grid container had no explicit pixel width**, so DOM bounds did not reflect `previewWidth`.

### Fix Applied
**UniversalFieldShell.tsx**
- When `previewWidth` exists, set grid container `width` to an **explicit pixel value**:
  ```typescript
  width: previewWidth ? `${Math.round(previewWidth)}px` : '100%'
  ```
- This forces DOM bounds to track the preview width during resize.

### Expected Behavior
- `domBounds.width` should now match `previewWidth` during grid resize.
- Small mouse deltas should produce proportional visual changes.

---

## Logging Added - Object Widths at Grab/Commit (2026-01-20)

### Problem
We need a full snapshot of object widths **before click** and **after drop**, even when the mouse doesn’t move.

### Change
**componentSnapshot.ts**
- Snapshot now includes:
  - `objectWidths` (by object id)
  - `objectWidthsSource` (`dom-grid` when grid layout is active)
- This is captured automatically in:
  - `fieldshell.resize.start`
  - `fieldshell.resize.grabbed`
  - `fieldshell.resize.commit`

### Expected Behavior
We can now compare **label/input/validation widths** before click and after drop for grid components.

### Follow-up
Added width-commit snapshots so `fieldshell.resize.commit` fires for E/W handles too, capturing `objectWidths` before/after drop.

### Follow-up 2
Added `gridMetrics` to component snapshots so we can account for column gaps, padding, and borders when object widths do not sum to container width.

### Follow-up 3
Added SmartBorder diagnostics so every path calculation run is logged (start + skip reasons + path summary). This captures container sizes, padding, scaling, group sizes, and path geometry when the SmartBorder shape changes on E-handle click.

### Follow-up 4
Added SmartBorder shape diff signals:
- `smartborder.calculate.start` now logs `gridWidth` and `widthBudget` (parent vs grid vs padding).
- `smartborder.path.calculated` now logs `bounds`, `pointCount`, and `pathHash` for stable before/after comparisons.

### Follow-up 5
Added a SmartBorder guard during resize:
- If `widthBudget.remainder` is significantly negative on resize, SmartBorder defers a path update to avoid the click-time shape jump.
- New log: `smartborder.calculate.defer` with the width budget.

### Follow-up 6
Adjusted grid preview sizing to avoid stretching object heights:
- `renderWithGridLayout()` now only sets explicit `width` during preview and keeps `alignItems/justifyItems` from `generateGridStyles`.
- Prevents label/help grid cells from stretching to input height on E-handle click.

### Follow-up 7
Added a zero-delta guard for horizontal resize preview:
- On initial grab, if `deltaWidth/deltaHeight` are ~0, we skip applying preview width.
- Added `resize.width.chain` log to capture width sources (props/DOM/smartborder/grid) at grab time.

### Follow-up 8
Freeze grid column sizing on resize start:
- Capture `gridTemplateColumns` on E/W handle grab and reapply during resize.
- Prevents auto-sizing from reflowing label/validation widths on click.
 - Added explicit logs for resize flow (`resize.handle.start`, `resize.handle.move`, `resize.grid.freeze.clear`) to trace which paths execute.
 - Clear frozen columns only after width commit (`width-commit`) so columns stay stable through commit.
 - Frozen columns now remain applied even after `isResizingState` flips false, and clear is delayed to let commit render stabilize.

### Follow-up 9
Resize handle now passes the active handle to `onResizeStart`, so we can reliably freeze grid columns on E/W grab.

### Findings (Form 46, text-1768866112931-605)
- On E-handle click, `smartborder.calculate.start` fires immediately with `isResizing: true`, `layout: fill`, and `contentPadding: 5px` each side.
- At click time: `parent.width = 506`, `wrapperRect.width = 503.89`, `scale.x ≈ 0.9958`, `groupChildCounts = [3]`.
- The grid container is `494px` wide. Add SmartBorder padding (`+10px`) and scale rounding to reach the `506px` parent width. This explains the “missing” pixels at click.
- As soon as resizing begins, parent width increments (506 → 507 → 509 → …) and `pathDLength` changes (e.g., 226 → 223), explaining the visible SmartBorder shape shift.
