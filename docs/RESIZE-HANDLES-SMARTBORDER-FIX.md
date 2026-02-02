# Resize Handles Losing Connection with SmartBorder - Fix

## Problem

When using the input-only width resize handle (green handle on the input object), the resize handles that should always form a rectangle around the SmartBorder lose connection with the SmartBorder shape.

### Root Cause

1. **ResizeHandles positioning**: ResizeHandles are positioned absolutely relative to the **outer container** (`outerRef`), which has a fixed width based on `component.props.width`.

2. **SmartBorder sizing**: SmartBorder calculates its path based on the actual content size. When `inputWidthOverride` changes (via the green input-only handle), the SmartBorder container grows wider than the outer container.

3. **Mismatch**: The resize handles stay positioned relative to the fixed-width outer container, while the SmartBorder shape changes based on the actual content size. This causes the handles to appear disconnected from the SmartBorder.

### Example Scenario

- Component width: `325px` (outer container width)
- Input width override: `685px` (makes SmartBorder wider)
- SmartBorder actual width: `613px` (wider than outer container)
- Resize handles: Still positioned relative to `325px` container
- **Result**: Handles don't align with SmartBorder edges

## Solution

Two-part fix:

### Part 1: ResizeHandlesWrapper

Created a `ResizeHandlesWrapper` component that:

1. **Tracks SmartBorder container bounds**: Uses `ResizeObserver` and event listeners to monitor the SmartBorder container's position and size.

2. **Positions handles relative to SmartBorder**: Creates a wrapper div positioned absolutely relative to the outer container, but sized and positioned to match the SmartBorder container's bounds.

3. **Updates dynamically**: Automatically updates when:
   - SmartBorder container resizes (via ResizeObserver)
   - Window resizes
   - Page scrolls

### Part 2: Preserve Manual inputWidthOverride

When resizing using E/W handles (main resize handles), the code now:

1. **Detects manually set `inputWidthOverride`**: Checks if `inputWidthOverride` was explicitly set (different from proportional width).

2. **Preserves manual settings**: When `inputWidthOverride` was manually set via the green handle, it's preserved during E/W resize instead of being scaled proportionally.

3. **Expands outer container**: When `inputWidthOverride` makes SmartBorder wider than `component.props.width`, the outer container expands to match SmartBorder width so resize handles align properly.

### Implementation

```typescript
const ResizeHandlesWrapper: React.FC<{
    smartBorderContainerRef: React.RefObject<HTMLDivElement | null>;
    outerContainerRef: React.RefObject<HTMLDivElement | null>;
    children: React.ReactNode;
}> = ({ smartBorderContainerRef, outerContainerRef, children }) => {
    // Tracks SmartBorder container position/size relative to outer container
    // Wraps ResizeHandles in a positioned container that matches SmartBorder bounds
}
```

### Usage

```tsx
<ResizeHandlesWrapper 
    smartBorderContainerRef={smartBorderContainerRef}
    outerContainerRef={outerRef}
>
    <ResizeHandles {...resizeHandleProps} />
</ResizeHandlesWrapper>
```

### Preserve Manual inputWidthOverride

```typescript
// In handleWidthChange:
const wasManuallySet = component.props.inputWidthOverride !== undefined && 
                        component.props.inputWidthOverride !== oldWidthPx &&
                        !isDropdownSplit;

// Only scale inputWidthOverride if it wasn't manually set
const newInputWidth = wasManuallySet 
    ? currentInputWidth  // Preserve manual setting
    : Math.round(currentInputWidth * widthRatio);  // Scale proportionally
```

### Expand Outer Container

```typescript
// When inputWidthOverride makes SmartBorder wider, expand outer container
const effectiveInputWidthOverride = resizePreview?.inputWidthOverride ?? component.props.inputWidthOverride;
const shouldExpandForInputWidth = effectiveInputWidthOverride && 
                                   baseWidthPx && 
                                   effectiveInputWidthOverride > baseWidthPx &&
                                   !isResizingState;
const finalDisplayWidthPx = shouldExpandForInputWidth 
    ? effectiveInputWidthOverride * (displayScale / 100)
    : displayWidthPx;
```

## Files Changed

- `frontend/src/features/builder/components/SortableComponent.tsx`
  - Added `ResizeHandlesWrapper` component
  - Wrapped `ResizeHandles` in `ResizeHandlesWrapper` for UniversalFieldShell components
  - Modified `handleWidthChange` to preserve manually set `inputWidthOverride` during E/W resize
  - Updated outer container width calculation to expand when `inputWidthOverride` makes SmartBorder wider

## Testing

To verify the fix:

1. Navigate to form builder: `http://localhost:3000/forms/45/builder`
2. Select a text component (e.g., `text-1768298739656-235`)
3. Use the green input-only width handle to resize the input
4. Verify that the resize handles (blue corners, green edges) stay aligned with the SmartBorder shape
5. Check logs: `python backend/enhanced_diagnostic_logs.py --frontend-only --frontend-component "text-1768298739656-235" --limit 20`

## Related Logs

The following logs help diagnose this issue:

- `smartborder.path.calculated` - Shows SmartBorder path calculation
- `resize.input.preview` - Shows input width override changes
- `resize.preview.applied` - Shows DOM bounds changes during resize

## Notes

- This fix only applies to components using `UniversalFieldShell` (text, email, phone, etc.)
- Divider and submit button components have their own resize handle logic and are not affected
- The wrapper uses `pointerEvents: 'none'` to ensure handles remain interactive
