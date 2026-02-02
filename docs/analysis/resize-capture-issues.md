# Resize Capture Analysis - Issues Requiring Attention

Based on the captured test data from `docs/analysis/resize-capture-report.md`, the following issues have been identified:

## 🔴 Critical Issues

### 1. **Corner Handles Show No Net Size Change After Drop**

**Problem**: All corner handles (NE, SE, NW, SW) show `Δbounds.width: 0` and `Δinput.height: 0` (or near-zero) after drop, meaning the resize operation **does not persist**.

**Evidence from Report**:
- **NE handle**: `Δbounds.width: 0`, `Δinput.height: 32.58` (height works, width doesn't)
- **SE handle**: `Δbounds.width: 0`, `Δinput.height: 0` (nothing persists)
- **NW handle**: `Δbounds.width: 0`, `Δinput.height: 0.00` (nothing persists)
- **SW handle**: `Δbounds.width: 0`, `Δinput.height: 0` (nothing persists)

**Impact**: Users cannot resize components using corner handles - the visual preview shows during drag, but the size reverts when released.

**Root Cause Hypothesis**: 
- `handleCornerResizeEnd` may not be committing width correctly
- The `resizePreview.width` check `if (resizePreview?.width !== undefined)` might be failing
- Width commit might be happening but then getting reverted by a subsequent operation

### 2. **Corner Handles Show Unexpected Width Drops During Drag**

**Problem**: At sample#8, all corner handles show a **-34.99px width change** regardless of mouse direction, which contradicts the expected resize direction.

**Evidence from Report**:
- **NE handle** (expected: width increase): `sample#8: expected Δw sign(1) from mouseΔx=5 but got Δbounds.w=-34.99`
- **SE handle** (expected: width increase): `sample#8: expected Δw sign(1) from mouseΔx=5 but got Δbounds.w=-34.99`
- **NW handle** (expected: width decrease): `sample#8: expected Δw sign(1) from mouseΔx=-5 but got Δbounds.w=-34.99` (sign mismatch)
- **SW handle** (expected: width decrease): `sample#8: expected Δw sign(1) from mouseΔx=-5 but got Δbounds.w=-34.99` (sign mismatch)

**Impact**: Visual preview during drag shows incorrect size changes, making it difficult for users to predict final size.

**Root Cause Hypothesis**:
- Width preview calculation in `handleResize` for corner handles might be using incorrect `startWidth`
- The `baseWidthDelta` calculation might be incorrect for corner handles
- There might be a state reset or conflict between width and vertical preview updates

### 3. **NE Handle Only Resizes Height, Not Width**

**Problem**: The NE handle shows `Δinput.height: 32.58` (height works) but `Δbounds.width: 0` (width doesn't work), suggesting only the vertical portion of the corner resize is being committed.

**Evidence from Report**:
```
### Run `cap_1769322683813_0b1cv4`
- Start(afterGrab): bounds=518.89×171.06, ...
- End(afterDrop): bounds=518.89×203.65, ...
- Δbounds.width: 0
- Δinput.height: 32.58
```

**Impact**: NE corner handle behaves like an N handle (vertical only) instead of a 2-axis resize.

**Root Cause Hypothesis**:
- `handleCornerResizeEnd` might be skipping width commit for NE handle specifically
- The `resizePreview.width` might be undefined for NE handle
- There might be a condition that prevents width commit for certain corner handles

## ✅ Working Correctly

### Edge Handles (N, S, W, E)
- **N handle**: ✅ Works correctly - `Δinput.height: -7.87` or `32.58`, no mismatches
- **S handle**: ✅ Works correctly - `Δinput.height: 32.58`, no mismatches  
- **W handle**: ✅ Works correctly - `Δbounds.width: 35.03`, no mismatches
- **E handle**: ✅ Works correctly - `Δbounds.width: 37.00` or `35.03`, no mismatches

All edge handles show:
- ✅ No direction mismatches
- ✅ Correct size changes persist after drop
- ✅ Expected behavior matches actual behavior

## 🔍 Investigation Needed

### Code Areas to Review

1. **`handleCornerResizeEnd` (SortableComponent.tsx:2069-2105)**
   - Check if `resizePreview.width` is being set correctly during corner drag
   - Verify the width commit logic: `if (resizePreview?.width !== undefined) { handleWidthChange(resizePreview.width); }`
   - Check if there's any code that clears `resizePreview` before commit

2. **`handleResize` corner branch (SortableComponent.tsx:653-769)**
   - Verify `startWidth` calculation: `const startWidth = resizePreview?.startWidth ?? currentWidthPx;`
   - Check if `baseWidthDelta` calculation accounts for both component scale and canvas scale correctly
   - Verify the merged preview is being set correctly: `setResizePreview(mergedPreview);`

3. **Width Preview Application (SortableComponent.tsx:2367-2458)**
   - Check if corner handle previews are being applied to DOM correctly
   - Verify `resizePreview?.width` is being used in display calculations
   - Check for any conditions that might prevent width preview from rendering

4. **State Management**
   - Check if `resizePreview` state is being cleared prematurely
   - Verify `lastVerticalPreviewRef` is being updated correctly for corner handles
   - Check for race conditions between width and vertical preview updates

## 📋 Recommended Fix Priority

1. **HIGH**: Fix corner handle width commit in `handleCornerResizeEnd` - this prevents any corner resize from persisting
2. **HIGH**: Fix width preview calculation during corner drag - this causes incorrect visual feedback
3. **MEDIUM**: Investigate why NE handle only commits height - might be related to #1
4. **LOW**: Add additional logging around corner resize commit to catch future regressions

## 🧪 Testing Recommendations

After fixes, verify:
1. Corner handles persist both width AND height changes after drop
2. Width preview during corner drag matches mouse movement direction
3. All four corner handles (NE, SE, NW, SW) behave consistently
4. Edge handles continue to work correctly (regression test)
