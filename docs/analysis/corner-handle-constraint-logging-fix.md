# Corner Handle Constraint Logging - Fix Implementation

## 🐛 **Problem Identified**

After implementing constraint logging for E/W/N/S handles, we discovered that **corner handles (NE, SE, NW, SW) were NOT logging constraints** when they were applied. This made it impossible to distinguish between:
- **Expected discrepancies** (due to min/max constraints being enforced)
- **Unexpected discrepancies** (actual bugs in the resize logic)

### Analysis Results (Before Fix)

From test session with 23 resize operations:
- **SE Handle**: 3 operations with discrepancies, only 1 had constraint log
- **SW Handle**: 3 operations with discrepancies, 0 had constraint logs  
- **NW Handle**: 1 operation with discrepancy, 0 had constraint logs

This left 6 out of 7 constrained operations **without evidence** of which constraint caused the discrepancy.

---

## 🔧 **Root Cause**

Constraint logging was only implemented in:
1. `handleWidthChange` - Called by E/W handles ✅
2. `handleVerticalResizeEnd` - Called by N/S handles ✅

However, **corner handles take a different path**:
1. User drags corner handle
2. `handleResize` is called with corner handle (e.g., 'se')
3. Inside `handleResize`, constraints are applied **during preview calculation** (lines 664-817)
4. Preview is set with already-constrained values
5. On drop, `handleCornerResizeEnd` calls `handleWidthChange` and `handleVerticalResizeEnd`
6. But by this point, the constraints were already applied in step 3!
7. `handleWidthChange` receives `widthToCommit` from preview (already constrained)
8. It doesn't detect a constraint because the value is already within limits

**Result**: No constraint logs for corner handles.

---

## ✅ **Fix Applied**

Added constraint tracking directly in the **corner handle branch of `handleResize`** where constraints are actually applied during preview calculation.

### Changes Made to `SortableComponent.tsx`

#### 1. Width Constraint Tracking (Lines ~716-732)

**Before**:
```typescript
const minWidthPx = computeSelectionMinWidthPx() ?? 100;
const unclampedWidth = baseWidth + baseWidthDelta;
let nextWidth = Math.max(minWidthPx, unclampedWidth);  // ❌ No logging

if (nextWidth > maxAllowedBaseWidth) {
    nextWidth = Math.max(minWidthPx, maxAllowedBaseWidth);  // ❌ No logging
}
```

**After**:
```typescript
const minWidthPx = computeSelectionMinWidthPx() ?? 100;
const unclampedWidth = baseWidth + baseWidthDelta;
let nextWidth = Math.max(minWidthPx, unclampedWidth);

// Track width constraints for corner handles
const widthConstraints: string[] = [];
if (unclampedWidth < minWidthPx) {
    widthConstraints.push(`componentWidth: ${unclampedWidth.toFixed(1)}px -> ${nextWidth.toFixed(1)}px (MIN: ${minWidthPx}px)`);
}

// ... canvas boundary check ...
if (nextWidth > maxAllowedBaseWidth) {
    const constrainedWidth = Math.max(minWidthPx, maxAllowedBaseWidth);
    widthConstraints.push(`componentWidth: ${nextWidth.toFixed(1)}px -> ${constrainedWidth.toFixed(1)}px (canvas boundary)`);
    nextWidth = constrainedWidth;
}
```

#### 2. Vertical Constraint Tracking (Lines ~759-801)

**Before**:
```typescript
let newInputHeight = Math.max(minInputHeight, Math.min(maxInputHeight, currentInputHeight + remainingDelta));  // ❌ No logging

if (verticalHandle === 'n') {
    const newGap = Math.max(0, Math.min(48, currentLabelGap + remainingDelta));  // ❌ No logging
    verticalPreview.labelGap = newGap;
}
```

**After**:
```typescript
const verticalConstraints: string[] = [];

const requestedInputHeight = currentInputHeight + remainingDelta;
let newInputHeight = Math.max(minInputHeight, Math.min(maxInputHeight, requestedInputHeight));

// Track height constraints
if (requestedInputHeight < minInputHeight) {
    verticalConstraints.push(`inputHeight: ${requestedInputHeight.toFixed(1)}px -> ${newInputHeight.toFixed(1)}px (MIN: ${minInputHeight.toFixed(1)}px)`);
} else if (requestedInputHeight > maxInputHeight) {
    verticalConstraints.push(`inputHeight: ${requestedInputHeight.toFixed(1)}px -> ${newInputHeight.toFixed(1)}px (MAX: ${maxInputHeight.toFixed(1)}px)`);
}

// ... gap handling with constraint tracking ...
if (verticalHandle === 'n') {
    const requestedGap = currentLabelGap + remainingDelta;
    const newGap = Math.max(0, Math.min(48, requestedGap));
    verticalPreview.labelGap = newGap;
    
    // Track gap constraints
    if (requestedGap < 0) {
        verticalConstraints.push(`labelGap: ${requestedGap.toFixed(1)}px -> ${newGap}px (MIN: 0px)`);
    } else if (requestedGap > 48) {
        verticalConstraints.push(`labelGap: ${requestedGap.toFixed(1)}px -> ${newGap}px (MAX: 48px)`);
    }
}
```

#### 3. Constraint Event Logging (Lines ~815-855)

**Added after `setResizePreview(mergedPreview)`**:

```typescript
// Log constraints if any were applied during preview calculation (Agent Logging System)
if (widthConstraints.length > 0) {
    devLogger.info('resize.constraints.width', {
        componentId: component.id,
        componentType: component.type,
        handle,  // e.g., 'se', 'sw', 'ne', 'nw'
        horizontalHandle,  // e.g., 'e', 'w'
        constraintsApplied: widthConstraints,
        requested: {
            width: unclampedWidth,
            widthDelta: baseWidthDelta,
        },
        final: {
            width: nextWidth,
            widthDelta: nextWidth - baseWidth,
        },
        reason: 'Corner handle width preview limited by constraints',
    });
}

if (verticalConstraints.length > 0) {
    devLogger.info('resize.constraints.vertical', {
        componentId: component.id,
        componentType: component.type,
        handle,  // e.g., 'se', 'sw', 'ne', 'nw'
        verticalHandle,  // e.g., 'n', 's'
        constraintsApplied: verticalConstraints,
        requested: {
            deltaY: deltaHeight,
        },
        actual: {
            heightChange: newInputHeight - currentInputHeight,
            gapChange: {
                labelGap: verticalPreview.labelGap !== undefined ? verticalPreview.labelGap - currentLabelGap : 0,
                inputHelpGap: verticalPreview.inputHelpGap !== undefined ? verticalPreview.inputHelpGap - currentInputHelpGap : 0,
            },
        },
        reason: 'Corner handle vertical preview limited by constraints',
    });
}
```

---

## 📊 **Expected Results After Fix**

After hard refresh (Ctrl+Shift+R) and new test session:

### For Clean Operations (No Constraints)
- **Discrepancy**: 0.00px in all dimensions ✅
- **Constraint Events**: None (as expected)

### For Constrained Operations
- **Discrepancy**: Non-zero (e.g., mouse moved 47.3px but width only changed 0px)
- **Constraint Events**: Now logged with specific constraint details ✅

**Example constraint log**:
```json
{
  "eventType": "resize.constraints.width",
  "handle": "se",
  "horizontalHandle": "e",
  "constraintsApplied": [
    "componentWidth: 252.7px -> 300px (MIN: 300px)"
  ],
  "requested": {
    "width": 252.7,
    "widthDelta": -47.3
  },
  "final": {
    "width": 300,
    "widthDelta": 0
  }
}
```

This log **proves** the 47.3px discrepancy was due to hitting minimum width constraint, not a bug.

---

## 🧪 **Testing Instructions**

1. **Hard refresh frontend** (Ctrl+Shift+R) to load updated code
2. **Open form** in builder (e.g., form 46)
3. **Test corner handles** - deliberately try to hit constraints:
   - **SE handle**: Drag left/down to shrink (hit MIN width)
   - **SW handle**: Drag right/down to shrink (hit MIN width)
   - **NE handle**: Drag up/right to expand (hit MAX height or gap)
   - **NW handle**: Drag up/left (test both axes)

4. **Extract logs**:
```bash
# Get constraint events
python backend/enhanced_diagnostic_logs.py --frontend-only --frontend-filter "resize.constraints" --limit 50

# Get corner commit events
python backend/enhanced_diagnostic_logs.py --frontend-only --frontend-filter "resize.corner.commit" --limit 50
```

5. **Run analysis**:
```bash
python backend/scripts/_tmp_analyze_constraints_v2.py
```

6. **Verify**:
   - ✅ Clean operations still show 0.00px discrepancy
   - ✅ Constrained operations now have matching constraint events
   - ✅ No operations show "[!] NO CONSTRAINTS LOGGED" when discrepancy exists

---

## 🎯 **Benefits**

1. **Evidence-Based Analysis**: Can now prove which discrepancies are due to constraints vs bugs
2. **Complete Coverage**: All resize handles (E/W/N/S/NE/SE/NW/SW) now log constraints
3. **Debugging Clarity**: When mouse moves 50px but component only grows 30px, we can see exactly which constraint (MIN/MAX) was hit
4. **Validation**: Can confirm core resize math is perfect (0.00px discrepancy when no constraints)

---

## 📝 **Related Files**

- **Modified**: `frontend/src/features/builder/components/SortableComponent.tsx`
- **Analysis Script**: `backend/scripts/_tmp_analyze_constraints_v2.py`
- **Documentation**: `docs/AGENT-LOGGING-GUIDE.md` (already includes `resize.constraints.*` event types)
- **Implementation Summary**: `docs/analysis/constraint-logging-implementation.md`

---

## ✅ **Status**

**Implementation**: Complete ✅  
**Testing**: Pending user validation  
**Next Step**: User should hard refresh and perform new test session to validate constraint logging now works for corner handles.
