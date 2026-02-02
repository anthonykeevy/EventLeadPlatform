# Button Resize & Width Fixes - Summary

**Date:** 2026-01-28  
**Status:** Fixes Applied - Ready for UAT

## Issues Fixed

### ✅ Issue #1: Panel Percentage Width Not Working
**Problem:** Selecting percentage widths (25%, 33%, etc.) in Appearance → Dimensions → Width doesn't change component width

**Root Cause:** 
- Button wrapper div was always converting widths to pixels
- Container wasn't using percentage width directly

**Fix Applied:**
- Container now uses `component.props.width` directly for percentage widths
- Falls back to `displayWidth` for pixel widths
- During resize preview, uses `previewWidth` in pixels

**Files Changed:**
- `frontend/src/features/builder/components/SortableComponent.tsx` (line 3883)

---

### ✅ Issue #2: Button Not Updating During Drag Preview
**Problem:** Button width doesn't visually change during E handle drag

**Root Cause:**
- `ObjectRendererProps` interface didn't include `actionWidthOverride`
- Button renderer couldn't receive preview width overrides
- Renderer only read from `component.props.actionWidthOverride` (not updated during preview)

**Fix Applied:**
- Added `actionWidthOverride` to `ObjectRendererProps` interface
- Pass `actionWidthOverride` from `renderObjectGroup` to button renderer
- Button renderer now uses preview override if provided: `preview override > props override > buttonWidth prop > component width`

**Files Changed:**
- `frontend/src/features/builder/utils/objectRenderers.tsx` (lines 140, 1281, 1326-1336)
- `frontend/src/features/builder/components/UniversalFieldShell.tsx` (line 444)

---

### ✅ Issue #3: Validation Object Shrinking During Drag
**Problem:** Validation message goes very narrow during drag preview (should stay fixed width)

**Root Cause:**
- Proportional scaling was applied to ALL objects during preview
- For buttons, only the action object should scale, validation should stay fixed

**Fix Applied:**
- Added button-specific check in proportional scaling logic
- For buttons: only scale `actionWidthOverride`, skip `labelWidthOverride`, `inputWidthOverride`, `helpWidthOverride`
- For other components: scale all objects proportionally (existing behavior)

**Files Changed:**
- `frontend/src/features/builder/components/UniversalFieldShell.tsx` (lines 326-359)

---

### ✅ Issue #4: Container Width During Preview
**Problem:** Container width wasn't updating during drag preview

**Fix Applied:**
- Container now uses `previewWidth` (in pixels) during horizontal resize
- Falls back to percentage/pixel width when not resizing

**Files Changed:**
- `frontend/src/features/builder/components/SortableComponent.tsx` (line 3883)

---

### ⚠️ Issue #5: SmartBorder Misalignment After Drop
**Problem:** SmartBorder is slightly shorter than button after drop, corrects on selection

**Status:** Not yet fixed - SmartBorder already receives `previewWidth` prop, but may need recalculation trigger after commit

**Next Steps:**
- Check if SmartBorder recalculates on component props update
- May need to force SmartBorder recalculation after resize commit

---

## Code Changes Summary

### 1. `objectRenderers.tsx`
- Added `actionWidthOverride?: number` to `ObjectRendererProps`
- Updated `createActionRenderer` to accept and use `actionWidthOverride` prop
- Priority: preview override > props override > buttonWidth prop > component width

### 2. `UniversalFieldShell.tsx`
- Fixed proportional scaling to skip validation/help for buttons
- Pass `actionWidthOverride` to renderer in `renderObjectGroup`
- Only scale action object for buttons during preview

### 3. `SortableComponent.tsx`
- Container width uses `previewWidth` during resize preview
- Falls back to percentage/pixel width when not resizing

---

## Expected Behavior After Fixes

1. **Panel Width Changes:**
   - Selecting 25%, 33%, 50%, etc. should immediately change button width
   - Button should fill the percentage of canvas width
   - SmartBorder should wrap correctly

2. **Resize Preview:**
   - Button width should update visually during drag
   - Validation message should stay fixed width (not shrink)
   - SmartBorder should expand/contract with button during drag
   - Resize handles should follow SmartBorder

3. **Resize Commit:**
   - Button width should match drop position
   - Validation should remain correct width
   - SmartBorder should wrap correctly (may still need fix for post-drop alignment)

---

## Testing Checklist

- [ ] Panel: Select 25% → button width = 25% of canvas
- [ ] Panel: Select 33% → button width = 33% of canvas
- [ ] Panel: Select 50% → button width = 50% of canvas
- [ ] Panel: Select Custom → button width = custom px value
- [ ] Resize: Drag E handle → button width updates during drag
- [ ] Resize: Validation stays fixed width during drag
- [ ] Resize: SmartBorder updates during drag
- [ ] Resize: Button width matches drop position
- [ ] Resize: SmartBorder wraps correctly after drop (may need selection to correct)
