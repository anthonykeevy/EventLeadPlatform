# Logging Analysis & Improvements
## Comparison: Logs vs User Feedback

**Date:** 2025-12-23  
**Component:** Text Component (ID: `text-1766452530827-124`)

---

## Issue 1: Text Length Indicator Missing on Canvas

### User Feedback
> "The component in the Toolbox has a Text length indicator but the Component on the canvas does not."

### What Logs Show
- ✅ `canvas.textlength.calculated` events exist in code (`TextLengthIndicator.tsx` line 44)
- ❌ **NO logs found** for `canvas.textlength.calculated` in recent session
- ✅ `TextLengthIndicator` is used in `objectRenderers.tsx` (lines 174, 237) for toolbox preview
- ❌ `TextLengthIndicator` is **NOT** used in `StandardInput.tsx` (canvas component)

### Root Cause
`TextLengthIndicator` is only rendered in `objectRenderers.tsx` (used for toolbox preview), but not in `StandardInput.tsx` (used for canvas rendering via `UniversalFieldShell`).

### Logging Gap
- **Missing:** Log when `TextLengthIndicator` is rendered/not rendered
- **Missing:** Log which renderer path is used (toolbox vs canvas)

### Recommended Logging Enhancement
```typescript
// In StandardInput.tsx, add TextLengthIndicator and log:
devLogger.info('canvas.textlength.indicator.rendered', {
    componentId,
    maxLength,
    estimatedWidth,
    location: 'canvas', // vs 'toolbox'
    visible: true
});
```

---

## Issue 2: Component Position Shift on Drop

### User Feedback
> "When I dropped the text component on the canvas it shifted from the position I dropped it at."

### What Logs Show
- ❌ **NO logs found** for component drop events (`component.added`, `component.dropped`, `canvas.component`)
- ❌ **NO logs** for initial position calculation
- ❌ **NO logs** for position adjustment after drop

### Root Cause
No logging exists for drag-and-drop operations or position calculations.

### Logging Gap
- **Missing:** `component.dropped` event with drop coordinates
- **Missing:** `component.position.calculated` event showing initial vs final position
- **Missing:** `component.position.adjusted` event if position changes after drop

### Recommended Logging Enhancement
```typescript
// In drag-and-drop handler:
devLogger.info('component.dropped', {
    componentId,
    componentType,
    dropCoordinates: { x, y },
    initialPosition: { x: dropX, y: dropY },
    finalPosition: { x: finalX, y: finalY },
    positionShift: { deltaX, deltaY },
    reason: 'snap-to-grid' | 'collision-avoidance' | 'none'
});
```

---

## Issue 3: Help Text Border Not Showing

### User Feedback
> "I added borders to each object at a global level because it makes it easier to see when moving and resizing. Only the Help text did not get a border which it should have got."

### What Logs Show
- ❌ **NO logs** for border application to help text
- ❌ **NO logs** for global style application
- ✅ Border logic exists in `styleUtils.ts` (line 339) but checks `helpTextBorderColor && (helpTextBorderWidth ?? 1) > 0`
- ❌ **BUG:** Logic doesn't check `helpTextHasBorder` flag

### Root Cause
The border application logic in `styleUtils.ts` doesn't check the `helpTextHasBorder` boolean flag. It only checks if `helpTextBorderColor` is set and `helpTextBorderWidth > 0`.

### Logging Gap
- **Missing:** `style.border.applied` event for each object category (label, input, help)
- **Missing:** `style.global.applied` event showing which global styles were applied
- **Missing:** `style.border.skipped` event with reason (missing color, width=0, hasBorder=false)

### Recommended Logging Enhancement
```typescript
// In styleUtils.ts, when applying help text border:
devLogger.info('style.border.applied', {
    componentId,
    objectCategory: 'help',
    hasBorder: effective.helpTextHasBorder,
    borderColor: effective.helpTextBorderColor,
    borderWidth: effective.helpTextBorderWidth,
    applied: !!(effective.helpTextBorderColor && (effective.helpTextBorderWidth ?? 1) > 0 && effective.helpTextHasBorder),
    reason: effective.helpTextHasBorder ? 'hasBorder=true' : 'hasBorder=false'
});
```

---

## Issue 4: E Handle Resize - No Visual Guide

### User Feedback
> "I grabbed the East handle and moved it East and the object expanded to the correct position but there was no visual guide. What I mean by visual guide is that I want the component to redraw the component as the user is adjusting so they have a visual guide."

### What Logs Show
- ✅ `fieldshell.resize.preview` events **ARE being logged** (multiple events found)
- ✅ Preview state is being set: `setResizePreview({ width: nextWidth, horizontalHandle: handle, ... })`
- ❌ **NO logs** showing if preview is actually applied to DOM
- ❌ **NO logs** for resize preview rendering state

### Root Cause
Preview state is calculated and logged, but there's no logging to confirm:
1. If preview state is actually applied to component styles
2. If component re-renders during preview
3. If visual feedback is visible to user

### Logging Gap
- **Missing:** `resize.preview.applied` event confirming DOM update
- **Missing:** `resize.preview.render` event showing component re-render
- **Missing:** `resize.preview.visible` event confirming visual feedback

### Recommended Logging Enhancement
```typescript
// In SortableComponent.tsx, when applying preview:
devLogger.info('resize.preview.applied', {
    componentId,
    handle,
    previewState: resizePreview,
    appliedStyles: {
        width: previewWidth,
        transform: previewTransform,
        left: previewLeft
    },
    domBounds: containerRef.current?.getBoundingClientRect(),
    isVisible: true // Check if element is actually visible
});
```

---

## Issue 5: W Handle Resize - Incorrect Visual Behavior

### User Feedback
> "I grabbed the West handle and moved it west. The visual guide was present but showed the East moving west but at like half the speed of the West border but when I dropped the resize the East border snapped to it's anchor point."

### What Logs Show
- ✅ `fieldshell.resize.preview` events show W handle being used
- ✅ Preview logs show `leftShift: -deltaWidth` calculation
- ✅ Preview logs show `width: nextWidth` calculation
- ❌ **NO logs** showing actual DOM position during preview
- ❌ **NO logs** showing East edge position during preview
- ❌ **NO logs** comparing preview position vs final position

### Root Cause
The preview calculation for W handle sets `leftShift` and `width`, but:
1. The preview may not be applying both correctly
2. The East edge position isn't being tracked/logged
3. There's no comparison between preview state and final state

### Logging Gap
- **Missing:** `resize.preview.edge.position` event showing East/West edge positions
- **Missing:** `resize.preview.transform` event showing CSS transform values
- **Missing:** `resize.commit.edge.position` event showing final edge positions
- **Missing:** Comparison between preview and final positions

### Recommended Logging Enhancement
```typescript
// In handleResize for W handle:
const eastEdgeBefore = currentWidthPx + component.position.x;
const eastEdgeAfter = nextWidth + component.position.x + leftShift;
devLogger.info('resize.preview.edge.position', {
    componentId,
    handle: 'w',
    westEdge: { before: component.position.x, after: component.position.x + leftShift },
    eastEdge: { before: eastEdgeBefore, after: eastEdgeAfter },
    eastEdgeDelta: eastEdgeAfter - eastEdgeBefore,
    expectedEastEdgeDelta: 0, // Should stay anchored
    actualEastEdgeDelta: eastEdgeAfter - eastEdgeBefore // Log discrepancy
});

// In handleWidthChange after commit:
devLogger.info('resize.commit.edge.position', {
    componentId,
    handle: 'w',
    westEdge: component.position.x,
    eastEdge: component.position.x + newWidth,
    previewEastEdge: previewEastEdge, // From preview state
    eastEdgeSnapDelta: (component.position.x + newWidth) - previewEastEdge
});
```

---

## Summary: Logging Improvements Needed

### High Priority (Critical for Debugging)

1. **Component Drop Logging**
   - `component.dropped` - Drop coordinates and final position
   - `component.position.calculated` - Position calculation logic
   - `component.position.adjusted` - Position changes after drop

2. **Resize Preview Visibility**
   - `resize.preview.applied` - Confirm preview state applied to DOM
   - `resize.preview.edge.position` - Track edge positions during preview
   - `resize.commit.edge.position` - Final edge positions for comparison

3. **Border Application Logging**
   - `style.border.applied` - Log when borders are applied to each object category
   - `style.border.skipped` - Log when borders are skipped with reason

### Medium Priority (Helpful for Debugging)

4. **Text Length Indicator**
   - `canvas.textlength.indicator.rendered` - Log when indicator is rendered/not rendered
   - `canvas.textlength.indicator.location` - Distinguish toolbox vs canvas

5. **Global Style Application**
   - `style.global.applied` - Log which global styles were applied
   - `style.global.overridden` - Log component-level overrides

### Code Fixes Required (Not Just Logging)

1. ✅ **Fix Help Text Border**: Added `helpTextHasBorder` check in `styleUtils.ts`
2. ✅ **Fix Text Length Indicator**: Added `TextLengthIndicator` to `StandardInput.tsx` canvas rendering
3. ✅ **Fix E Handle Preview**: Added explicit `width` to container style during horizontal resize
4. ✅ **Fix W Handle Preview**: Fixed `leftShift` unit mismatch (was screen pixels, now canvas coordinates)
5. ✅ **Fix Boundary Constraint**: Fixed `getComponentDimensions` to use `getBoundingClientRect().width / scale` instead of incorrect `offsetWidth / scale`

---

## Fixes Applied (Session 2025-12-23)

### 1. Boundary Constraint Bug (Large Gap When Snapping Back)
**File**: `frontend/src/features/builder/utils/collisionDetection.ts`
**Issue**: `getComponentDimensions` was dividing `offsetWidth` by scale, but `offsetWidth` is already in canvas coordinates (not screen pixels).
**Fix**: Changed to use `getBoundingClientRect().width / scaleFactor` which correctly converts screen pixels to canvas coordinates.

### 2. W Handle Resize Preview (Distorted Visual)
**File**: `frontend/src/features/builder/components/SortableComponent.tsx`
**Issue**: `leftShift` was calculated as `-deltaWidth` (screen pixels) but `position.x` is in canvas coordinates, causing unit mismatch.
**Fix**: Changed to `leftShift = handle === 'w' ? -baseWidthDelta : 0` (canvas coordinates).

### 3. E Handle Resize Preview (No Visual Guide)
**File**: `frontend/src/features/builder/components/SortableComponent.tsx`
**Issue**: During E/W resize, the component's width wasn't being applied to the container style.
**Fix**: Added conditional `width: displayWidth` to container style when `isHorizontalResize` is true.

### 4. Logging Bug (Original Position)
**File**: `frontend/src/features/builder/pages/BuilderPage.tsx`
**Issue**: `collision.boundary.constrained` event logged the post-constraint position as "originalPosition".
**Fix**: Capture `originalPositionX` and `originalPositionY` BEFORE applying the constraint.

---

## Next Steps

1. ✅ Review logs vs user feedback (this document)
2. ✅ Implement logging enhancements
3. ✅ Fix code bugs (border, TextLengthIndicator, resize preview, boundary constraint)
4. ⏳ Test with enhanced logging
5. ⏳ Verify all issues resolved

---

## Remaining Issue: Drop Position Shift

The drop position shift issue may be due to:
1. **Grid snapping** - Component snaps to 8px grid after drop
2. **Toolbox item size vs canvas component size** - The dragged "ghost" from toolbox may have different dimensions than the rendered component

This needs further investigation with logging. The `component.dropped` event captures:
- `dropCoordinates` - Where cursor/ghost was on screen
- `initialPosition` - Calculated position before grid snap
- `finalPosition` - Position after grid snap
- `positionShift` - The delta between initial and final

Test by adding a component and checking the logs for this event.
