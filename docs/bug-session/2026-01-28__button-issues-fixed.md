# Button Issues - Analysis & Fixes

**Date:** 2026-01-28  
**Session:** Button Dimensions Width & Resize Handles  
**Status:** Fixes Applied

## Issues Identified

### Issue #1: Panel Width Selection Not Applying (FIXED)
**Problem:** Selecting percentage widths (25%, 33%, etc.) in Appearance → Dimensions → Width doesn't change component width

**Root Cause:** 
- Button wrapper div uses `displayWidth` which is always converted to pixels
- For percentage widths, we need to use `component.props.width` directly
- The wrapper was using `${finalDisplayWidthPx}px` which converts percentages to pixels

**Fix Applied:**
```typescript
// In SortableComponent.tsx - button wrapper style
width: component.props.width?.endsWith('%') 
    ? component.props.width 
    : displayWidth,
```

**Status:** ✅ Fixed - Button container now respects percentage widths

---

### Issue #2: Resize Delta Multiplier (NEEDS INVESTIGATION)
**Problem:** User dragged E handle 30px but component expanded very wide (106px)

**Evidence from Logs:**
- `deltaWidthScreenPx: 102.67px` (but user reported 30px drag)
- `startWidth: 1385px`
- `baseWidthDelta: 106.78px` (after scale conversion)
- `nextWidth: 1491.78px`
- Scale factor: `0.9614583333333333` (96.15% canvas zoom)

**Analysis:**
- The scale conversion is working correctly: `102.67px / 0.961 = 106.78px`
- But user reported only 30px drag, not 102px
- Possible causes:
  1. Delta is cumulative from drag start (not incremental)
  2. Mouse movement tracking includes acceleration/momentum
  3. User's perception doesn't match actual pixel movement

**Next Steps:**
- Add logging to track initial drag position vs current position
- Verify delta calculation is incremental, not cumulative
- Check if ResizeHandles is passing correct delta values

**Status:** ⚠️ Needs more investigation

---

### Issue #3: SmartBorder Narrower Than Button Initially (NEEDS INVESTIGATION)
**Problem:** After resize, SmartBorder is narrower than button, then corrects on selection

**Possible Causes:**
1. SmartBorder calculation happens before button width is fully applied
2. React render cycle: button width updates before SmartBorder recalculates
3. SmartBorder uses cached bounds that don't update immediately

**Next Steps:**
- Check SmartBorder calculation timing vs component width updates
- Verify SmartBorder recalculates on selection (which triggers re-render)
- Add logging to track SmartBorder bounds vs button width

**Status:** ⚠️ Needs more investigation

---

## Code Changes Made

### 1. Fixed Button Percentage Width Support
**File:** `frontend/src/features/builder/components/SortableComponent.tsx`
- Changed button wrapper to use `component.props.width` directly for percentage widths
- Falls back to `displayWidth` for pixel widths

### 2. Enhanced Logging
**File:** `frontend/src/features/builder/components/properties/AppearanceSection.tsx`
- Added explicit logging of `actionWidthOverride: undefined` for percentage widths
- Helps verify that undefined values are being set correctly

---

## Testing Recommendations

1. **Test Panel Width Changes:**
   - Select 25%, 33%, 50%, 66%, 75% in Appearance → Dimensions → Width
   - Verify button width changes to match percentage of canvas width
   - Check logs for `panel.button.width.preset.applied` with correct updates

2. **Test Resize Delta:**
   - Perform small drags (10px, 20px, 30px) and check logs
   - Verify `deltaWidthScreenPx` matches actual mouse movement
   - Check if delta is incremental or cumulative

3. **Test SmartBorder Sync:**
   - Resize button and immediately check SmartBorder width
   - Verify SmartBorder matches button width without needing selection
   - Check if there's a timing issue in React render cycle

---

## Log Commands

```bash
# View panel changes
python backend/enhanced_diagnostic_logs.py --frontend-only --frontend-filter "panel.button" --limit 20

# View resize operations
python backend/enhanced_diagnostic_logs.py --frontend-only --frontend-filter "resize.button" --limit 30

# View commit operations
python backend/enhanced_diagnostic_logs.py --frontend-only --frontend-filter "resize.width.button.commit" --limit 10

# View button width calculations
python backend/enhanced_diagnostic_logs.py --frontend-only --frontend-filter "button.width.calculated" --limit 20
```
