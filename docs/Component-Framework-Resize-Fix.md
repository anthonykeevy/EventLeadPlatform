# Component Framework Resize Fix

## Problem Statement (Current Understanding)
E/W resize interactions are writing width overrides that change layout structure even when users only click (no drag), or when they expect only the input width to change. This causes erratic behavior: gaps inflate, validation appears shorter, and the component re-renders with unexpected proportions. The N/S handles do not show the same structural side effects, which indicates the E/W resize path is mutating width-related props while N/S is not.

## Goal (As Set by User)
- Clicking E/W handles should **not** change component structure or props.
- Dragging E/W handles should **keep label + validation widths fixed**, and **only adjust input width** to expand/shrink the component within canvas limits.
- When shrinking, **input width should reduce until its minimum**, and only then should the overall component width be constrained (avoid shrinking label/validation first).
- Logging must provide reliable, layer-specific metrics (props vs computed vs rendered) in **canvas px** for consistent interpretation.

---

## Attempt 1 — Expand Logging for Object Metrics + Grid Metrics
**Intent:** Capture object widths and grid metrics to reconcile DOM layout vs props.  
**Changes:** Added `objectMetrics`, `gridMetrics`, `bounds`, and metadata in component snapshots; added `MetricsJson` and summary columns in `log.FrontendEvent`; enhanced diagnostic logs and documentation.  
**Outcome:** Enabled inspection of DOM widths vs props; revealed that prop overrides do not reflect actual rendered widths.

---

## Attempt 2 — Add Object/Cell Data Attributes
**Intent:** Enable reliable per-object measurement in DOM.  
**Changes:** Added `data-object-id`, `data-object-type` to object wrappers; added grid object identifiers.  
**Outcome:** Measurement now consistently finds label/input/validation nodes.

---

## Attempt 3 — Resolve Metrics in px + Canvas-normalized Values
**Intent:** Remove ambiguity when CSS uses `normal` gaps and when canvas is scaled.  
**Changes:** Added `columnGapPx`, `rowGapPx`, numeric padding/border widths; captured canvas scale and canvas-normalized rects (`canvasRect`, `canvasBounds`).  
**Outcome:** Measurements now align to canvas px and can be compared against screenshot geometry.

---

## Attempt 4 — Suppress Click-only E/W Structural Mutation
**Intent:** Clicking E/W should not write overrides or change layout.  
**Changes:** Added width delta detection; if width delta is 0, do not write overrides and emit a no-op commit.  
**Outcome:** Click-only E/W no longer writes width overrides in logs.

---

## Attempt 5 — Seed Overrides from DOM Widths
**Intent:** When dragging E/W, begin from actual rendered widths instead of component width.  
**Changes:** Used `objectMetrics.rect.width` for label/input/validation as baseline.  
**Outcome:** Reduced mismatch between overrides and visible widths, but still saw input override values smaller than rendered input width.

---

## Attempt 6 — Input-only Resize Logic for E/W
**Intent:** Keep label/validation widths stable and use input width to absorb resize.  
**Changes:** Compute available input width from component width minus label/help widths and resolved gaps/padding/border.  
**Outcome:** Input overrides sometimes set below rendered input width, causing erratic state and confusing visual changes after drop.

---

## Attempt 7 — Min Width Rules (10-char Input, Text-fit Label/Validation)
**Intent:** Ensure input never shrinks below a 10-character visual width, and allow label/validation to shrink only to the width needed to display their text.  
**Changes:** Compute `minInputWidth` as 10-character width using `measureTextWidth`, plus input padding/border. Compute `minLabelWidth` and `minHelpWidth` from measured text width plus padding/border, then only shrink label/help to these minima when input hits its minimum.  
**Outcome:** Pending re-test after applying logic.

---

## Attempt 8 — Pointer Position Logging
**Intent:** Capture pointer start/end positions and deltas to correlate mouse travel with resize results.  
**Changes:** Added `resize.pointer.down` and `resize.pointer.up` logs with handle, action, start/end positions, and starting size.  
**Outcome:** Pending re-test after applying logging.

---

## Attempt 9 — Pointer Capture + Delta Sign Logging
**Intent:** Ensure pointer move events are captured consistently and log delta sign conversion for E/W handles.  
**Changes:** Added pointer capture on handle down and `resize.pointer.delta` logs (deltaX vs widthDelta).  
**Outcome:** Pending re-test after applying logging.

---

## Attempt 10 — Raw Delta Sign Fix (E Handle)
**Intent:** Ensure rightward drags on the E handle always produce positive width deltas.  
**Changes:** In the E-handle path, if computed base width delta is negative, flip to positive and log `resize.delta.sign.corrected`.  
**Outcome:** Pending re-test after applying fix.

---

## Attempt 11 — E/W Preview Clamp + No-Drag Commit Guard
**Intent:** Prevent click-only commits from mutating width, and keep preview width aligned with canvas boundary constraints.  
**Changes:** Suppress width commits when pointer delta is ~0; remove unconditional E-handle sign flip; clamp E-handle preview width to canvas bounds and log `resize.preview.width.constrained`.  
**Outcome:** Re-test showed left-drag deltas only; right-drag deltas did not reach the handler. Left drags clamp to min width (~223px), so small left drags appear to do nothing while large left drags shrink slightly.

---

## Current Status (Latest Test)
- Only **left-drag** E-handle deltas are appearing in logs (`deltaX` negative); no right-drag events captured.  
- Component width changes are clamped by **minimum width constraints**, explaining “no response” for small left drags and small shrink for large left drags.  
- Preview and commit widths now align (no overshoot), but **right-drag input is not reaching the resize handler**, which blocks expansion testing.

---

## Consolidated Review (Findings)
- **E/W path writes width overrides** which shifts the grid structure even with minimal interaction.
- **N/S handles don’t mutate width props**, so they preserve structure.
- **Props are intent**, not actual rendered widths; **DOM metrics** are authoritative for what users see.
- **Gaps and scaling** were missing from logs originally; now logged in px and canvas-normalized.
- **Current E/W logic** still can set input width below rendered input width, which causes mismatch and “snap” effects after drop.

---

## Conclusion
We now have accurate logging and a clear separation of intent vs rendered values, but the E/W resize path still produces undesired state transitions. The core issue is that input overrides are sometimes set smaller than the rendered input width, and the grid redistributes space in unexpected ways when overrides are written.

---

## Reference Files
- `frontend/src/features/builder/components/SortableComponent.tsx` (E/W and N/S resize behavior, width overrides)
- `frontend/src/features/builder/utils/componentSnapshot.ts` (metrics capture, px resolution, canvas normalization)
- `frontend/src/features/builder/components/UniversalFieldShell.tsx` (object wrappers, data attributes)
- `frontend/src/features/builder/utils/objectRenderers.tsx` (input width application, inputWidthOverride behavior)
- `backend/modules/logging/router.py` (metrics ingestion, summary columns)
- `backend/models/log/frontend_event.py` (metrics storage model)
- `backend/enhanced_diagnostic_logs.py` (metrics display)
- `docs/COMPONENT-FRAMEWORK-REFERENCE.md` (properties dictionary by layer)
- `docs/GRID-LAYOUT-GUIDE.md` (grid behavior + layout model)
- `docs/AGENT-LOGGING-GUIDE.md` (logging usage and interpretation)

---

## Next Steps (Planned)
1. **Clamp input override to rendered input width** (never set below DOM width).  
2. **Apply a minimum input width rule** of *~10 characters wide* (visual guide only, not text-length derived).  
3. **Allow label/validation widths to shrink as needed**, but keep them wide enough to display their text.  
4. **Re-test E/W drag** with the new clamp and validate against screenshots.  
5. **If gaps still inflate**, log resolved grid column widths (resolved `grid-template-columns`) to attribute the extra space precisely.  
6. **Document final behavior** once the resize logic matches the goal.

---

## Attempt 12 — Fundamental Architecture Change: Input-Only Width Adjustment

**Date:** 2026-01-21

**Intent:** Previous attempts patched the existing proportional-resize logic, but the fundamental architecture fights against the goal. This attempt takes a different approach: **E/W resize should only adjust input width**, leaving label and help widths unchanged.

**Root Cause Analysis (from log review):**
1. **Right-drag events not captured**: All logged `deltaX` values were negative; positive (rightward) deltas never reached the handler.
2. **Proportional recalculation destroys layout**: On shrink from 824px to 449px, help width collapsed from 180px to 10px, causing text wrapping.
3. **Grid reconfigures**: After resize, grid showed equal columns (`266px 8px 266px 8px 266px`) instead of fixed label/help.

**Log Evidence (resize.width.calculated):**
```json
"before": { "labelWidth": 61, "inputWidth": 312, "helpWidth": 180 },
"after": { "labelWidth": 58, "inputWidth": 133, "helpWidth": 10 }  // ← Help collapsed!
```

**Changes Planned:**
1. **Fix right-drag capture**: Investigate why positive deltaX doesn't reach handler (possibly pointer capture or event propagation issue).
2. **Remove proportional width recalculation for label/help**: In `handleWidthChange`, do NOT update `labelWidthOverride` or `helpWidthOverride`.
3. **Input absorbs all width delta**: Only update `inputWidthOverride` = currentInputWidth + widthDelta.
4. **Component width reflects actual content**: `props.width` = label + gaps + input + gaps + help (sum of fixed + adjusted).

**Files Modified:**
- `frontend/src/features/builder/components/SortableComponent.tsx` - `handleWidthChange` function

**Changes Made (2026-01-21):**
1. Modified the `updates` object in `handleWidthChange` to NOT include `labelWidthOverride` or `helpWidthOverride`
2. Added new calculation: `adjustedInputWidth = currentInputWidth + widthDelta` (input absorbs all width change)
3. Added new log: `resize.attempt12.input-only` to track the new approach
4. Updated commit log to show label/help unchanged

**Code Changes:**
```typescript
// BEFORE (proportional recalculation):
const updates = { 
    width: `${newWidth}px`,
    inputWidthMode: 'fill',
    labelWidthOverride: newLabelWidth,  // Recalculated
    helpWidthOverride: newHelpWidth,    // Recalculated
};
updates.inputWidthOverride = newInputWidth;

// AFTER (input-only adjustment):
const adjustedInputWidth = Math.max(minInputWidth, currentInputWidthPx + widthDelta);
const updates = { 
    width: `${newWidth}px`,
    inputWidthMode: 'fill',
    // REMOVED: labelWidthOverride and helpWidthOverride
};
updates.inputWidthOverride = adjustedInputWidth;
```

**Outcome (Test 1):** Right-drag captured correctly (deltaX: +392.67), preview expanded to 959px, but commit showed widthDelta: 0.

**Root Cause Found:** `oldWidthPx` was calculated from `actualDomWidth` which reflected the preview state (960px), not the original width (506px). This caused `widthDelta = newWidth - oldWidthPx = 960 - 960 = 0`.

**Fix Applied (2026-01-21 16:25):**
- Use `startWidth` from resize preview (captured at pointer down) instead of current DOM width
- Added logging to show which source was used for `oldWidthPx`

**Code Change:**
```typescript
// BEFORE: Used current DOM width (which reflects preview)
if (actualDomWidth !== null) {
    oldWidthPx = actualDomWidth;
}

// AFTER: Use startWidth from preview (original width at pointer down)
const startWidthFromPreview = (previewData as any)?.startWidth;
if (startWidthFromPreview !== undefined && startWidthFromPreview > 0) {
    oldWidthPx = startWidthFromPreview;
}
```

**Outcome (Test 2):** Right-drag works but:
- Validation text wrapping (help width changed despite not updating helpWidthOverride)
- Gap between label and input much bigger
- Input didn't increase width as expected on larger drags

**Root Cause Found (Grid Redistribution):**
Grid columns showed equal distribution after resize:
- Before: `"70.2917px 8px 201.333px 8px 207.979px"` (label=70, input=201, help=208)
- After: `"312px 8px 312px 8px 312px"` (equal distribution!)

Without explicit width overrides, grid columns use `1fr` which shares extra space equally.

**Fix Applied (2026-01-21 16:35) - Attempt 12 v2:**
- SET `labelWidthOverride` and `helpWidthOverride` to their **current DOM values** (locks them)
- Only `inputWidthOverride` absorbs the width delta

**Code Change:**
```typescript
// Get current widths from DOM to LOCK them
const lockedLabelWidth = component.props.labelWidthOverride ?? Math.round(measuredLabelWidth);
const lockedHelpWidth = component.props.helpWidthOverride ?? Math.round(measuredHelpWidth);

const updates = { 
    width: `${newWidth}px`,
    inputWidthMode: 'fill',
    // LOCK label/help widths to current DOM values (not recalculated)
    labelWidthOverride: lockedLabelWidth,
    helpWidthOverride: lockedHelpWidth,
    inputWidthOverride: adjustedInputWidth,  // Absorbs delta
};
```

**Outcome (Test 3):** Right-drag works but:
- Component expanded less than expected
- Resize handles stayed in original position
- Label and validation objects got narrower

**Root Cause Found (Grid Template Columns):**
Grid was STILL reverting to equal distribution after resize commit because:
- Width overrides are written to props correctly
- But `generateGridStyles()` uses `1fr` for all columns (equal distribution)
- Width overrides are passed to renderers but NOT used for grid column widths
- After resize, `frozenGridTemplateColumns` is cleared → grid reverts to `1fr`

**Fix Applied (2026-01-21 16:45) - Attempt 12 v3:**
- Modified `renderWithGridLayout` in `UniversalFieldShell.tsx`
- Calculate explicit grid template columns from width overrides
- Priority: `frozenGridTemplateColumns` (during resize) > `explicitGridTemplateColumns` (from overrides) > `baseGridStyles` (1fr)

**Code Change (UniversalFieldShell.tsx):**
```typescript
// When width overrides are set, build explicit column widths
if (labelOverride !== undefined || inputOverride !== undefined || helpOverride !== undefined) {
    const columnGap = gridLayout.columnGap ?? 8;
    const labelCol = labelOverride !== undefined ? `${labelOverride}px` : 'auto';
    const inputCol = inputOverride !== undefined ? `${inputOverride}px` : '1fr';
    const helpCol = helpOverride !== undefined ? `${helpOverride}px` : 'auto';
    explicitGridTemplateColumns = `${labelCol} ${columnGap}px ${inputCol} ${columnGap}px ${helpCol}`;
}

// Apply to grid styles
...(frozenGridTemplateColumns
    ? { gridTemplateColumns: frozenGridTemplateColumns }
    : explicitGridTemplateColumns
        ? { gridTemplateColumns: explicitGridTemplateColumns }
        : {}),
```

**Outcome (Test 4):**
- Right-drag: Component narrower than drop position, resize handles in wrong position
- Left-drag: Validation behind input, resize handles in wrong position
- Large gap between input and validation

**Root Cause Found (Width Mismatch):**
`newWidth` came from preview (781px), but sum of overrides was only 706px:
- label: 61px + gap: 8px + input: 449px + gap: 8px + help: 180px = 706px
- **75px gap inflation** because component width didn't match content

**Fix Applied (2026-01-21 16:55) - Attempt 12 v4:**
- Calculate component width from **sum of overrides** instead of preview width
- `calculatedWidth = lockedLabelWidth + gap + adjustedInputWidth + gap + lockedHelpWidth`

**Code Change (SortableComponent.tsx):**
```typescript
// BEFORE: Used preview width (mismatched content)
const updates = { 
    width: `${newWidth}px`,  // From preview
    ...
};

// AFTER: Calculate width from sum of overrides
const calculatedWidth = lockedLabelWidth + columnGap + adjustedInputWidth + columnGap + lockedHelpWidth;
const updates = { 
    width: `${calculatedWidth}px`,  // Exact match to content
    ...
};
```

**Outcome (Test 5):** Same issues as before (component smaller than drag position), but validation no longer behind input.

**Root Cause Found (Original Slack):**
Original component width (506px) was larger than sum of objects (431px). When calculating input from widthDelta, we lose this 75px slack.

**Fix Applied (2026-01-21 17:00) - Attempt 12 v5:**
- Use **preview width** for component (matches drag position)
- Calculate **input to fill remaining space**: `input = newWidth - label - help - gaps`
- This ensures input exactly fills space between label and help

**Code Change (SortableComponent.tsx):**
```typescript
// BEFORE: Input = currentInput + widthDelta (loses slack)
const adjustedInputWidth = Math.max(minInputWidth, currentInputWidthPx + widthDelta);

// AFTER: Input fills remaining space
const remainingForInput = newWidth - lockedLabelWidth - lockedHelpWidth - (columnGap * 2);
const adjustedInputWidth = Math.max(minInputWidth, remainingForInput);
```

**Outcome (Test 6):** Much better! Component width now matches drag position. But two issues remain:
1. **Resize handles not refreshing** after resize commit (stay in original position)
2. **No visual feedback during drag** (hard to see where component will end up)

**Root Cause Analysis:**
1. Resize handles are positioned by `ResizeHandlesWrapper` which uses a `ResizeObserver` on the SmartBorder container. After resize commit, the observer may not trigger fast enough.
2. The SmartBorder's `calculatePath` is called via RAF on ResizeObserver events, but the handles wrapper needs the path's bounding box to position correctly.

**Fix Applied (2026-01-21 17:10) - Attempt 12 v6:**
- Added `forceUpdateKey` prop to `ResizeHandlesWrapper`
- Key changes when width props change, forcing position recalculation
- This ensures resize handles update after resize commit

**Code Change (SortableComponent.tsx):**
```typescript
// ResizeHandlesWrapper now accepts forceUpdateKey
const ResizeHandlesWrapper: React.FC<{
    ...
    forceUpdateKey?: string | number;  // NEW
}> = ({ ..., forceUpdateKey }) => {
    const [updateTrigger, setUpdateTrigger] = useState(0);
    
    // When forceUpdateKey changes, force recalculation
    useEffect(() => {
        if (forceUpdateKey !== undefined) {
            setUpdateTrigger(prev => prev + 1);
        }
    }, [forceUpdateKey]);
    
    // Added updateTrigger to dependencies
    useEffect(() => { ... }, [..., updateTrigger]);
};

// Usage - pass width-related props as key
<ResizeHandlesWrapper 
    ...
    forceUpdateKey={`${width}-${inputWidthOverride}-${labelWidthOverride}-${helpWidthOverride}`}
>
```

**Outcome (v6):** User reported resize handles still not refreshing and no visual feedback during drag.

**Root Cause Analysis (v7):**
Deep analysis revealed a fundamental mismatch:

1. **Preview vs Commit Mismatch**: During E/W drag PREVIEW, `UniversalFieldShell` uses proportional scaling for ALL object widths. But during COMMIT, only the input is adjusted (label/help stay fixed). This causes the preview to show a different layout than what gets committed.

2. **Frozen Grid Columns Block Preview**: At resize start, grid template columns are frozen to prevent redistribution. But this also blocks the preview from showing the correct layout during drag - the columns stay frozen even when `previewWidth` changes.

3. **No Preview Object Widths**: The preview system wasn't passing calculated object widths, so the SmartBorder couldn't recalculate its path based on the new layout.

**Fix Applied (2026-01-21 - Attempt 12 v7):**

**1. Capture Object Widths at Resize Start:**
```typescript
// New ref to store initial object widths
const resizeStartObjectWidthsRef = useRef<{
    labelWidth: number;
    inputWidth: number;
    helpWidth: number;
    columnGapPx: number;
    totalExtras: number;
} | null>(null);

// In handleResizeStart, capture when E/W handle is grabbed:
if (handle === 'e' || handle === 'w') {
    const preSnapshot = captureComponentSnapshot(component, smartBorderContainerRef);
    const measuredWidths = preSnapshot?.objectMetrics || {};
    resizeStartObjectWidthsRef.current = {
        labelWidth: component.props.labelWidthOverride ?? measuredWidths.label?.rect?.width ?? 0,
        helpWidth: component.props.helpWidthOverride ?? measuredWidths.validation?.rect?.width ?? 0,
        inputWidth: component.props.inputWidthOverride ?? measuredWidths.input?.rect?.width ?? 0,
        columnGapPx,
        totalExtras,
    };
}
```

**2. Calculate Preview Object Widths During Drag:**
```typescript
// In handleResize for E/W handles:
const capturedWidths = resizeStartObjectWidthsRef.current;
if (capturedWidths) {
    // Keep label and help fixed at their captured widths
    previewLabelWidth = Math.round(capturedWidths.labelWidth);
    previewHelpWidth = Math.round(capturedWidths.helpWidth);
    
    // Input fills the remaining space
    const availableForInput = nextWidth - capturedWidths.labelWidth - capturedWidths.helpWidth - capturedWidths.totalExtras;
    previewInputWidth = Math.max(60, Math.round(availableForInput));
}

// Include in preview state
setResizePreview({
    width: nextWidth,
    previewLabelWidth,
    previewInputWidth,
    previewHelpWidth,
    ...
});
```

**3. Pass Preview Object Widths to UniversalFieldShell:**
```typescript
previewObjectWidthOverrides={
    isHorizontalResize && resizePreview?.previewInputWidth !== undefined
        ? {
            labelWidthOverride: resizePreview.previewLabelWidth,
            inputWidthOverride: resizePreview.previewInputWidth,
            helpWidthOverride: resizePreview.previewHelpWidth,
        }
        : ...
}
```

**4. Use Preview Grid Columns Over Frozen Columns:**
```typescript
// In renderWithGridLayout - previewGridTemplateColumns takes highest priority
if (hasPreviewObjectWidths) {
    previewGridTemplateColumns = `${labelCol} ${columnGap}px ${inputCol} ${columnGap}px ${helpCol}`;
}

// Priority: previewGridTemplateColumns > frozenGridTemplateColumns > explicitGridTemplateColumns > 1fr
```

**5. Delayed Position Updates in ResizeHandlesWrapper:**
```typescript
useEffect(() => {
    if (forceUpdateKey !== undefined) {
        setUpdateTrigger(prev => prev + 1);
        // Delayed triggers to catch DOM updates after React re-render
        const timer1 = setTimeout(() => setUpdateTrigger(prev => prev + 1), 50);
        const timer2 = setTimeout(() => setUpdateTrigger(prev => prev + 1), 150);
        return () => { clearTimeout(timer1); clearTimeout(timer2); };
    }
}, [forceUpdateKey]);
```

**Expected Outcome:**
1. **Visual feedback during drag**: SmartBorder should now update during drag because the grid template columns are calculated from preview object widths
2. **Preview matches commit**: Both use the same "input-only" adjustment strategy
3. **Resize handles update after commit**: Delayed updates catch the DOM recalculation

**Files Changed:**
- `frontend/src/features/builder/components/SortableComponent.tsx`
  - Added `resizeStartObjectWidthsRef` to capture object widths at resize start
  - Modified `handleResizeStart` to capture object widths for E/W handles
  - Modified `handleResize` to calculate preview object widths
  - Updated `resizePreview` state type to include preview object widths
  - Updated `previewObjectWidthOverrides` prop passing
  - Added delayed update triggers in `ResizeHandlesWrapper`
  - Added cleanup of `resizeStartObjectWidthsRef` on resize end
  
- `frontend/src/features/builder/components/UniversalFieldShell.tsx`
  - Modified `renderWithGridLayout` to calculate `previewGridTemplateColumns` from preview object widths
  - Changed priority: `previewGridTemplateColumns` > `frozenGridTemplateColumns` > `explicitGridTemplateColumns`

**Outcome (v7 Test):** User reported:
- Label and validation objects reduced their width (should stay fixed!)
- Large gap between input and validation objects
- Border jumped ~100px on shrink, then jumped back on drop
- Resize handles now positioned correctly (improvement!)

**Root Cause Analysis (v7.1):**
The captured object widths from DOM are in **screen pixels** (affected by canvas zoom and component scale), but the component width calculations are in **base pixels** (unscaled). This mismatch caused:
1. Label/help appearing smaller than expected (screen px interpreted as base px)
2. Input calculated too large (to fill the "extra" space)
3. Visual jumps due to coordinate system mismatch

**Fix Applied (v7.1) - Scale Conversion:**
```typescript
// Calculate effective scale factor (canvas scale * component scale)
const componentScaleFactor = componentScale / 100;
const canvasScaleFactor = scale || 1.0;
const effectiveScaleFactor = componentScaleFactor * canvasScaleFactor;

// DOM measurements are in screen pixels - convert to base pixels
const measuredLabelWidthScreen = measuredWidths.label?.rect?.width ?? 0;
const measuredLabelWidthBase = effectiveScaleFactor > 0 
    ? measuredLabelWidthScreen / effectiveScaleFactor 
    : measuredLabelWidthScreen;

// Use props if set (already in base pixels), otherwise use converted DOM measurements
const labelWidth = component.props.labelWidthOverride ?? measuredLabelWidthBase;
```

Also converted gap, padding, and border measurements from screen to base pixels.

**Outcome (v7.1 Test):** User reported:
- Label immediately got narrower (started wrapping) during drag
- Input stayed same width instead of expanding
- Large gap between input and validation
- Border still "jumps" on shrink

**Root Cause Analysis (v8):**
The preview system is trying to control too many things at once:
1. Grid template columns (via `previewGridTemplateColumns`)
2. Object widths (via `previewObjectWidthOverrides`)
3. Container width (via `previewWidth`)

These are conflicting. The grid cells have their widths set, but the objects inside might have their own width logic applied by renderers, causing conflicts.

**Attempt 12 v8 - Simplified Approach:**
Focus on getting the **COMMIT** working correctly first, then add preview later.

Strategy:
1. Remove `previewObjectWidthOverrides` during E/W resize - stop trying to preview object widths
2. Remove `previewWidth` during E/W resize - stop triggering proportional scaling
3. Keep frozen grid columns during drag (no visual preview, but stable)
4. On commit, apply the input-only adjustment correctly
5. Ensure resize handles update after commit

This sacrifices live visual preview during drag but ensures the final result is correct.

**Code Changes:**
```typescript
// Changed from:
previewWidth={isHorizontalResize ? resizePreview?.width : undefined}

// To:
previewWidth={undefined}  // Don't pass during E/W resize
```

Also removed `previewObjectWidthOverrides` for E/W resize.

**Expected Behavior:**
1. Drag E handle - component stays FROZEN (no visual change during drag)
2. Release E handle - component JUMPS to new size with correct widths
3. Label/validation stay fixed, input adjusts
4. Resize handles update to match new size

**Outcome (v8 Test):** User reported:
- Component expanded to almost correct position
- Label and validation are BOTH still narrower (wrapping)
- Big space between input and validation on expand
- User observed: "These 3 objects are in a Grid created by the Grid Object and I am sure the Grid has it's own padding and spacing"

**Root Cause Analysis (v8.1):**
The COMMIT logic in `handleWidthChange` has the same scale conversion bug as the preview logic:
- `measuredLabelWidth`, `measuredInputWidth`, `measuredHelpWidth` come from DOM snapshots
- DOM measurements are in **screen pixels** (affected by canvas zoom)
- But `oldWidthPx` and `newWidth` are in **base pixels**
- This mismatch causes incorrect width calculations

**Fix Applied (v8.1) - Scale Conversion in Commit Logic:**
```typescript
// Calculate effective scale factor (canvas scale * component scale)
const canvasScaleFactor = scale || 1.0;
const effectiveScaleFactor = scaleFactor * canvasScaleFactor;

// DOM measurements are in screen pixels - convert to base pixels
const measuredLabelWidthScreen = measuredWidths.label?.rect?.width ?? 0;
const measuredLabelWidth = effectiveScaleFactor > 0 
    ? measuredLabelWidthScreen / effectiveScaleFactor 
    : measuredLabelWidthScreen;
```

Also converted grid metrics (gap, padding, border) from screen to base pixels.

**Outcome (v8.1 Test):** User reported:
- Component expanded slightly longer than drop position
- Validation NOT wrapped - good!
- Label IS still wrapped - issue
- Input has SAME width - should be expanding!
- Gap between input and validation - extra space going to gap instead of input

User asked: "Why is there a gap between input and validation instead of input expanding to fill?"

**Root Cause Analysis (v8.2):**
The calculation wasn't accounting for **SmartBorder padding** (default 5px on each side = 10px total).

Example:
- Component width: 500px
- SmartBorder padding: 5px left + 5px right = 10px
- Grid container width: 490px
- Calculated input: 500 - label - help - gaps = 304px
- Grid template: 100 + 8 + 304 + 8 + 80 = 500px
- But container is only 490px!

The grid columns add up to MORE than the container, causing compression and gaps.

**Fix Applied (v8.2) - Include SmartBorder Padding:**
```typescript
// SmartBorder has default 5px padding on each side (wraps the grid content)
const smartBorderPadding = 5;
const smartBorderPaddingTotal = smartBorderPadding * 2;

const totalExtras = (columnGapPx * 2) + paddingLeftPx + paddingRightPx + borderLeftPx + borderRightPx + smartBorderPaddingTotal;
```

Added to both `handleResizeStart` and `handleWidthChange`.

**Outcome (v8.2 Test):** User reported:
- Component expansion more precise to drop position - improvement!
- Shrinking only reduced by half the distance
- Label still narrower (wrapping) - issue
- Input same width - should be expanding!
- Validation looks good (no wrapping)

**Root Cause Analysis (v8.3):**
Found that `remainingForInput` calculation (line 1434) only subtracted column gaps:
```typescript
// BEFORE (wrong):
const remainingForInput = newWidth - lockedLabelWidth - lockedHelpWidth - (columnGap * 2);
```

But `totalExtras` includes SmartBorder padding (10px), grid padding, and borders. This was being included in `available` calculation for initial sizing but NOT in the final `remainingForInput` calculation.

**Fix Applied (v8.3) - Use totalExtras in remainingForInput:**
```typescript
// AFTER (correct):
const remainingForInput = newWidth - lockedLabelWidth - lockedHelpWidth - totalExtras;
const calculatedWidth = lockedLabelWidth + adjustedInputWidth + lockedHelpWidth + totalExtras;
```

**Enhanced Logging:**
Added comprehensive `resize.width.comparison` log showing:
- BEFORE: component width, label, input, help, extras, SUM
- AFTER: component width, label, input, help, extras, SUM
- EXTRAS_BREAKDOWN: column gaps, SmartBorder padding, grid padding, border
- CHANGES: label change, input change, help change
- Sum verification: does SUM match component width?

**Outcome (v8.3 Test):** User tested, logs showed:
- EXPAND: `totalExtras=25.99`, `sumMatchesComponent=true` ✓
- SHRINK: `totalExtras=156.67`, `sumMatchesComponent=false` ✗

The `columnGapPxScreen` jumped from 6.92 to 76.42 between operations!

**Root Cause Analysis (v8.4):**
When grid uses explicit columns for gaps (e.g., `"70px 8px 332px 8px 208px"`), the CSS `column-gap` property is `0`. This triggers a fallback in `componentSnapshot.ts` that **computes the gap from object positions**:
```typescript
gap = next.left - (current.left + current.width)
```

After a resize, the DOM hasn't repositioned objects yet, so this measures the VISUAL gap (which includes the unfilled input space), not the intended 8px gap.

**Fix Applied (v8.4) - Use Known Gap Value:**
```typescript
// Do NOT use gridMetrics.columnGapPx - it's computed from object positions
// and becomes incorrect after resize
const columnGapPx = typeof component.props.labelGapOverride === 'number' 
    ? component.props.labelGapOverride 
    : 8; // Default gap
```

**Outcome (v8.4 Test):** Gap fix worked - `totalExtras` now consistent at 26.
But SHRINK showed mismatch:
- `componentWidth=417`, `SUM=437` (difference: 20px)
- Input hit minimum (133), but component wasn't expanded to fit

**Fix Applied (v8.5) - Expand Component When Input Hits Minimum:**
```typescript
// If input hit minimum and sum exceeds target width, expand component to fit
if (calculatedWidth > newWidth) {
    newWidth = Math.round(calculatedWidth);
}
```

**Outcome (v8.5 Test):** User reported same issue. Further investigation revealed:

**Root Cause Analysis (v8.6):**
User noticed the same behavior when using **Properties Panel** to change input width - this confirmed the issue is in how `inputWidthOverride` is applied, not just in resize logic.

**Two Issues Found:**

1. **`inputWidthMode: 'fill'` conflicts with `inputWidthOverride`**
   - In `objectRenderers.tsx`, the condition `allowInputWidthOverride` checks:
     ```javascript
     (inputWidthMode === 'fixed' || inputWidthMode == null)
     ```
   - We were setting `inputWidthMode: 'fill'` in commit, making `allowInputWidthOverride = false`
   - Result: `inputWidthOverride` was ignored!
   - **Fix:** Removed `inputWidthMode: 'fill'` from resize commit updates

2. **Input element has no default width**
   - `inputStyle` in `styleUtils.ts` had no `width` property
   - Input element defaulted to `width: auto`, not filling its grid cell
   - **Fix:** Added `width: '100%'` and `boxSizing: 'border-box'` to inputStyle

**Outcome (v8.6 Test):** Input resizing now works correctly!
But label width was wrapping at 70px - needed to be 71px to stop wrapping.

**Root Cause Analysis (v8.7):**
Canvas `measureText` API gives slightly different measurements than actual DOM rendering due to:
- Sub-pixel rendering differences
- Font hinting
- Kerning/letter-spacing

**Fix Applied (v8.7) - Text Width Safety Margin:**
```typescript
const TEXT_WIDTH_SAFETY_MARGIN = 2; // Accounts for rendering differences

const labelTextWidth = labelText
    ? measureTextWidth(...) + TEXT_WIDTH_SAFETY_MARGIN
    : 0;
```

**Outcome (v8.7 Test):** Still calculating label at 70px.

**Root Cause Analysis (v8.8):**
The `minLabelWidth` was calculated correctly with safety margin, but we weren't USING it!
We were locking the label to the current DOM width (70px - already wrapped) instead of 
ensuring it's at least `minLabelWidth` (72px - non-wrapping).

**Fix Applied (v8.8) - Enforce Minimum Label/Help Widths:**
```typescript
const rawLabelWidth = component.props.labelWidthOverride ?? measuredLabelWidth;
const lockedLabelWidth = Math.max(rawLabelWidth, minLabelWidth); // Ensure no wrapping
```

**Outcome (v8.8 Test):** Label width kept growing by 2px each resize (compounding safety margin).

**Root Cause Analysis (v8.9):**
The safety margin was being added to the DOM width every time, even after it had already been applied.

**Fix Applied (v8.9) - Conditional Safety Margin:**
Only add safety margin on FIRST resize (when no existing override exists):
```typescript
const labelSafetyMargin = component.props.labelWidthOverride === undefined ? 2 : 0;
const minLabelWidth = Math.max(10, calculatedMinLabelWidth, domMinLabelWidth + labelSafetyMargin);
```

**Outcome (v8.9 Test):** Works! But user asked about detecting text wrapping instead of using arbitrary safety margin.

**Enhancement (v8.10) - Text Wrapping Detection:**
Instead of conditional safety margin based on existing override, now we:
1. Detect actual text wrapping using `getClientRects().length` and height comparison
2. Add safety margin only when text IS wrapped

```typescript
// In componentSnapshot.ts - capture wrapping state using multi-line detection
const lineCount = target.getClientRects().length;
const isMultiLine = actualHeight > expectedSingleLineHeight * 1.2;
const isTextWrapped = lineCount > 1 || isMultiLine;
```

**Outcome (v8.10 Test):** First resize still resulted in 70px (wrapped). The issue:
- `scrollWidth > clientWidth` only detects **overflow**, not **wrapping**
- Multi-line detection didn't catch it on first resize because text wasn't wrapped yet at 70.29px
- After rounding to 70px, text wraps

**Fix (v8.11) - Use Math.ceil Instead of Math.round:**
The root cause is sub-pixel precision loss. At 70.29px text doesn't wrap, but `Math.round(70.29) = 70` and 70px wraps.

Solution: Use `Math.ceil` for all DOM width measurements to always round UP:

```typescript
// Use Math.ceil to prevent sub-pixel precision loss
const domMinLabelWidth = Math.ceil(currentLabelWidth); // 70.29 -> 71
const domMinHelpWidth = Math.ceil(currentHelpWidth);
let targetLabelWidth = Math.ceil(currentLabelWidth);
let targetHelpWidth = Math.ceil(currentHelpWidth);
const rawLabelWidth = component.props.labelWidthOverride ?? Math.ceil(measuredLabelWidth ?? currentLabelWidth);
```

**Outcome (v8.11 Test):** Label no longer wraps on first resize!

**Enhancement (v8.12) - Restore Visual Border Feedback:**
Re-enabled visual border feedback during E/W drag while keeping objects frozen:

1. Pass `previewWidth` for horizontal resize (border updates)
2. Check `frozenGridTemplateColumns` in UniversalFieldShell
3. Skip proportional object scaling when grid is frozen

```typescript
// In SortableComponent.tsx
previewWidth={isHorizontalResize ? resizePreview?.width : undefined}

// In UniversalFieldShell.tsx
const hasFrozenGrid = builderMode?.frozenGridTemplateColumns !== null && ...;
if (previewWidth && !hasFrozenGrid) {
    // Only scale objects if grid is NOT frozen
}
```

## Object Width Modes - Clarification

| Mode | Grid Column | Behavior | Applies To |
|------|-------------|----------|------------|
| **Auto** | `auto` | Shrink to fit text content | Label, Validation |
| **Fill** | `1fr` | Expand to fill remaining space | Input (default) |
| **Custom** | `{px}px` | Fixed pixel width | All (set by E/W resize) |

### E/W Handle Resize Behavior
- Sets ALL objects to Custom mode with explicit pixel widths
- Locks label/help widths to prevent redistribution
- Expands/shrinks input to fill remaining space

### Fill Mode Issue (TODO)
Fill mode (`1fr`) should make the input expand to fill remaining space. But when
`inputWidthOverride` is set, it overrides the `1fr` with a fixed `{px}px` value.
Need to clear `inputWidthOverride` when switching to Fill mode.

**Outcome (v8.12 Test):** User reported:
1. Visual border doesn't grow during E/W resize
2. Drag and drop reverts to original position (but keyboard movement works)

**Fix (v8.13) - Clear resizingComponentId After Resize:**
The drag revert issue was caused by `resizingComponentId` not being cleared in the store
after E/W resize completes. This caused `handleDragEnd` in BuilderPage.tsx to skip the
position update (line 795: `if (resizingComponentId === component.id) return;`).

```typescript
// In SortableComponent.tsx - onWidthChange callback
handleWidthChange(commitWidth);
setIsResizingState(false);
useBuilderStore.getState().setResizingComponentId(null); // NEW: Clear to re-enable drag
```

**Fix (v8.13) - SmartBorder Fill Mode During Resize:**
Updated `smartBorderLayout` to use 'fill' during horizontal resize so the border
expands with the container:

```typescript
smartBorderLayout: (isHorizontalResize || hasExplicitWidth) ? 'fill' : 'shrink',
```

**Outcome (v8.13 Test):** Drag now works. But E/W visual preview still not showing.

**Root Cause Analysis - Why N/S works but E/W doesn't:**
- N/S: Passes `previewStyleOverrides` which changes the **content** (like `inputHeight`), 
  so content re-renders at new size, SmartBorder measures new size and updates border.
- E/W: Content is **frozen** (objects stay at original widths via `frozenGridTemplateColumns`),
  so SmartBorder measures unchanged content and doesn't update border.

**Fix (v8.14) - Pass previewWidth to SmartBorder:**
Added `previewWidth` prop to SmartBorder that overrides the measured width during resize:

```typescript
// SmartBorder.tsx - interface
interface SmartBorderProps {
    // ...existing props
    previewWidth?: number; // Forces border to draw at this width during E/W resize
}

// SmartBorder.tsx - use previewWidth when calculating border
const measuredWidth = contentWrapper.offsetWidth;
const parentWidth = previewWidth !== undefined ? previewWidth : measuredWidth;

// UniversalFieldShell.tsx - pass previewWidth to SmartBorder
<SmartBorder
    previewWidth={previewWidth}
    // ...other props
>
```

**Outcome (v8.14 Test):** Border still not updating. SmartBorder calculates path from children's 
bounding rects, not container width. Since grid columns are frozen, children span less than previewWidth.

**Fix (v8.15) - Synthetic Segment for Preview Width:**
SmartBorder's algorithm iterates children to find boundaries. During resize, children are frozen and 
don't span the full preview width. Added a synthetic segment at the right edge of `previewWidth` to 
force the border algorithm to extend to the preview width:

```typescript
// SmartBorder.tsx - after iterating real segments
if (previewWidth !== undefined && segments.length > 0) {
    const minY = Math.min(...segments.map(s => s.yStart));
    const maxY = Math.max(...segments.map(s => s.yEnd));
    const syntheticRightX = wrapperOffsetX + previewWidth + p;
    segments.push({
        yStart: minY,
        yEnd: maxY,
        xLeft: syntheticRightX - 1,  // 1px wide at right edge
        xRight: syntheticRightX,
        source: { tag: 'synthetic-preview' },
    });
}
```

**Outcome (v8.15 Test):** Border now updates during E/W resize! But objects (label, input, validation) 
don't re-render until drop. N/S resize shows both border AND objects updating live.

**Fix (v8.16) - Pass Preview Object Widths During E/W Resize:**
The issue was that `previewObjectWidthOverrides` was only passed for input-only resize, not for E/W 
component resize. Without preview widths, `previewGridTemplateColumns` wasn't generated, so the 
frozen columns were used instead.

```typescript
// SortableComponent.tsx - pass E/W preview widths
previewObjectWidthOverrides={
    isHorizontalResize && (resizePreview?.previewLabelWidth !== undefined || 
                           resizePreview?.previewInputWidth !== undefined || 
                           resizePreview?.previewHelpWidth !== undefined)
        ? {
            labelWidthOverride: resizePreview.previewLabelWidth,
            inputWidthOverride: resizePreview.previewInputWidth,
            helpWidthOverride: resizePreview.previewHelpWidth,
        }
        : // fallback for input-only resize...
}
```

This triggers `previewGridTemplateColumns` generation in UniversalFieldShell, which takes priority 
over `frozenGridTemplateColumns`.

**Outcome (v8.16 Test):** Border updates during resize. But objects don't update visually despite 
correct React renders (logs confirmed correct gridStyles generated).

**Root Cause Analysis:**
From logs:
- `previewWidth: 308px`
- `gridTemplateColumns: "73px 8px 60px 8px 208px"` = 357px total

The preview grid columns (357px) **exceed the container width** (308px). When shrinking:
label (73) + help (208) + min input (60) + gaps (16) = 357px > 308px.

CSS Grid with fixed pixel columns won't shrink below specified size, so browser can't render the layout.

**Fix (v8.17) - Only Apply Preview Columns When They Fit:**
Added a check to ensure preview columns fit within previewWidth before applying:

```typescript
const totalColumnsWidth = (previewLabelWidth || 0) + (previewInputWidth || 0) + 
                          (previewHelpWidth || 0) + (columnGap * 2);
const columnsWillFit = previewWidth !== undefined && totalColumnsWidth <= previewWidth;

if (columnsWillFit) {
    previewGridTemplateColumns = `${labelCol} ${columnGap}px ${inputCol} ${columnGap}px ${helpCol}`;
}
```

When columns don't fit, the frozen columns handle layout (border still shows preview via synthetic segment).

**Outcome (v8.17 Test):** Label and validation move during drag, but input stays fixed until drop.

**Root Cause:** Grid layout renderer passed **committed** width overrides to input renderer:
```typescript
inputWidthOverride: component.props.inputWidthOverride,  // ← uses committed value!
```

The input element's fixed width (from committed override) overrides the grid column width.

**Fix (v8.18) - Pass Preview Width Overrides to Grid Layout Renderer:**

```typescript
// Use preview width overrides during resize, fallback to committed values
const effectiveInputWidthOverride = previewObjectWidthOverrides?.inputWidthOverride 
    ?? component.props.inputWidthOverride;

const node = renderer({
    // ...
    inputWidthOverride: effectiveInputWidthOverride,  // ← now uses preview!
});
```

**Test:** E/W resize should now show ALL objects (including input) updating during drag.
