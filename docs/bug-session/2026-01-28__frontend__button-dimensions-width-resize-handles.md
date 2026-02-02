# Bug Session — Button Dimensions Width & Resize Handles Not Working

- **SessionId**: 2026-01-28__frontend__button-dimensions-width-resize-handles
- **Area**: frontend
- **Status**: Active
- **Created**: 2026-01-28
- **Owner**: Anthony (UAT gate) / Agent (implementation + automation)

## Problem statement

- **Expected**: 
  - When changing width via Appearance → Dimensions → Width (e.g., 25%, 33%), the Button component width should expand to that percentage of Canvas width
  - SmartBorder should calculate the wrapper around the button object
  - When dragging E/W resize handles, the button object width should be the main change
  - Behavior should match other components (which use `input` object), but Button uses `action` object

- **Actual**: 
  - Dimensions section width changes don't affect button width
  - E/W resize handles don't stretch the button component
  - Only Button Settings → Button Width works (sets `buttonWidth: 'full'`)

- **Impact**: 
  - Inconsistent behavior between Button and other components
  - Users cannot control button width via Dimensions section
  - Resize handles are non-functional for buttons

- **Scope boundaries** (must not change / protected zones):
  - Button Settings → Button Width should continue to work
  - Other components' width behavior should not be affected
  - Component Framework architecture should be respected

## Repro (minimum)

1. Add a Submit Button component to canvas
2. Select the button
3. Open Properties Panel → Appearance → Dimensions
4. Change Width to "25%" or "33%"
5. **Observe**: Button width does not change
6. Try dragging E/W resize handles
7. **Observe**: Handles don't resize the button

## Done criteria (machine-verifiable where possible)

- [ ] DC1: Setting Dimensions → Width to 25% makes button width = 25% of canvas width
- [ ] DC2: Setting Dimensions → Width to 33% makes button width = 33% of canvas width  
- [ ] DC3: E/W resize handles change button object width (not just container)
- [ ] DC4: SmartBorder wraps correctly around button object after width change
- [ ] DC5: Button Settings → Button Width still works (backwards compatibility)

## Instrumentation plan (baseline first)

- **Frontend evidence**: 
  - Snapshot + screenshot of button before/after Dimensions width change
  - Console logs showing component props and rendered widths
  - Network requests (if any)
  
- **Code scope**: 
  - `ComponentRegistry.tsx` - Button structure definition
  - `objectRenderers.tsx` - Button action renderer width logic
  - `SortableComponent.tsx` - handleWidthChange for E/W handles
  - `DimensionsSection.tsx` - Width preset handling
  - `UniversalFieldShell.tsx` - Grid layout and width application
  - `builder.types.ts` - ComponentProps type definitions

- **Automation**: 
  - Create minimal repro script to test button width changes
  - Verify button object width vs container width

## Baseline evidence (ARTIFACT LINKS)

- Snapshot: _to be captured_
- Screenshot: _to be captured_
- Console: _to be captured_
- Network: _to be captured_
- Backend logs: _N/A (frontend-only issue)_
- Notes: 
  - Button uses `action` object (id: 'button'), not `input` object
  - No `actionWidthOverride` prop exists (unlike `inputWidthOverride`)
  - Button renderer checks `buttonWidth` prop and `component.props.width` but doesn't apply width to button element correctly
  - `handleWidthChange` only handles `inputWidthOverride`, `labelWidthOverride`, `helpWidthOverride` - no action width handling

## Working hypotheses (max 3 at a time)

- H1 (confidence 9/10): **Missing `actionWidthOverride` prop** - Button needs an `actionWidthOverride` prop similar to `inputWidthOverride` for other components. The Dimensions section should set this prop, and E/W resize should update it.
  
- H2 (confidence 8/10): **Button renderer width logic incomplete** - The button renderer at `objectRenderers.tsx:1319-1354` checks `component.props.width` but doesn't apply it correctly to the button element. It only uses `buttonWidth: 'full'` to set `width: '100%'`, but doesn't handle percentage or pixel widths.

- H3 (confidence 7/10): **Resize handler doesn't support action objects** - `handleWidthChange` in `SortableComponent.tsx` only handles `inputWidthOverride` for input objects. It needs to also handle `actionWidthOverride` for action objects (buttons).

## Attempt ledger (do not repeat failed attempts)

> Each attempt MUST follow the loop: instrument → observe → hypothesize → attempt → verify → record.

---

#### Attempt 01 — Add actionWidthOverride support for Button component
- **Hypothesis tested**: H1, H2, H3
- **Change summary**:
  - Files:
    - `frontend/src/features/builder/types/builder.types.ts` - Added `actionWidthOverride?: number` to ComponentProps
    - `frontend/src/features/builder/components/properties/DimensionsSection.tsx` - Updated to set `actionWidthOverride` for buttons when width changes
    - `frontend/src/features/builder/utils/objectRenderers.tsx` - Updated button renderer to use `actionWidthOverride` or `component.props.width`
    - `frontend/src/features/builder/components/SortableComponent.tsx` - Added button handling in `handleWidthChange` to update `actionWidthOverride`
    - `frontend/src/features/builder/components/UniversalFieldShell.tsx` - Added `actionWidthOverride` support in preview object width overrides and grid layout
  - Key change: 
    - Added `actionWidthOverride` prop to support button object width control (similar to `inputWidthOverride` for inputs)
    - Dimensions section now converts width to pixels and sets `actionWidthOverride` for buttons
    - Button renderer prioritizes `actionWidthOverride` > `buttonWidth` prop > `component.props.width`
    - E/W resize handles now update `actionWidthOverride` for buttons
- **Instrumentation**:
  - Artifacts created: _to be created during verification_
- **Verification**:
  - Automated checks run: Linter check passed (no errors)
  - Result: **Partially Fixed** - Code changes complete, but UAT revealed issues
- **What we learned**:
  - Button component uses `action` object (id: 'button'), not `input` object
  - Button structure is simpler (vertical layout: button/loading/validation)
  - Button renderer already reads from `component.props`, so adding `actionWidthOverride` prop was sufficient
- **UAT Results**:
  - ❌ Dimensions section width changes don't work
  - ⚠️ E/W resize handles work once then stop
  - ✅ SmartBorder renders correctly
  - ✅ Button Settings still works

---

#### Attempt 02 — Fix Appearance section and add resize preview support
- **Hypothesis tested**: H1, H2, H3
- **Change summary**:
  - Files:
    - `frontend/src/features/builder/components/properties/AppearanceSection.tsx` - Added button handling: set `actionWidthOverride: undefined` for percentages, set pixel value for pixel widths
    - `frontend/src/features/builder/utils/objectRenderers.tsx` - Added debug logging for button width calculation
    - `frontend/src/features/builder/components/SortableComponent.tsx` - Added preview support for buttons: pass `previewWidth` and `previewObjectWidthOverrides.actionWidthOverride` during resize
  - Key change:
    - **AppearanceSection** (not DimensionsSection) is used for buttons - updated `handleWidthPresetChange` to handle buttons
    - For percentage widths: set `width: "25%"` and `actionWidthOverride: undefined` so button fills container (100%)
    - For pixel widths: set both `width` and `actionWidthOverride` to same pixel value
    - Button renderer: when `actionWidthOverride` is undefined but `width` is set, use `100%` to fill container
    - Resize preview: pass `previewWidth` and `previewObjectWidthOverrides.actionWidthOverride` to UniversalFieldShell during E/W resize for live preview
    - Resize handler: clear preview state after button resize commit to allow subsequent resizes
- **Instrumentation**:
  - Artifacts created: _to be created during verification_
- **Verification**:
  - Automated checks run: Linter check passed (no errors)
  - Result: **Partially Fixed** - UAT revealed issues
- **What we learned**:
  - **Buttons use AppearanceSection, not DimensionsSection** - this was the main issue!
  - Percentage widths need `actionWidthOverride: undefined` so button fills container
  - Buttons need preview support (`previewWidth` and `previewObjectWidthOverrides`) for live resize preview
  - Resize preview state must be cleared after commit to allow subsequent resizes
- **UAT Results**:
  - ❌ Appearance width change still does nothing
  - ❌ E handle dragged 100px but expanded 1000px (10x multiplier issue)
  - ❌ After first resize, subsequent resizes give unexpected results

---

#### Attempt 03 — Add comprehensive logging for button resize debugging
- **Hypothesis tested**: Need instrumentation to diagnose 10x multiplier and panel change issues
- **Change summary**:
  - Files:
    - `frontend/src/features/builder/components/SortableComponent.tsx` - Added comprehensive button resize logging:
      - `resize.button.start` - Logs initial state when resize starts
      - `resize.button.preview.calculation` - Logs delta conversion and width calculation during drag
      - `resize.button.preview.updated` - Logs preview state updates
      - `resize.width.button.commit` - Comprehensive BEFORE/AFTER logging with multiplier calculation
      - `resize.width.button.position.adjusted` - Logs W handle position adjustments
    - `frontend/src/features/builder/components/properties/AppearanceSection.tsx` - Added panel change logging:
      - `panel.button.width.preset.changed` - Logs when preset width is selected
      - `panel.button.width.preset.applied` - Logs the updates being applied
      - `panel.button.width.custom.changed` - Logs custom width changes
      - `panel.button.width.auto.applied` - Logs when auto is selected
    - `frontend/src/features/builder/utils/objectRenderers.tsx` - Enhanced button width calculation logging:
      - `button.width.calculated` - Enhanced to show priority chain and final width value
  - Key logging additions:
    - **Delta conversion tracking**: Logs `deltaWidthScreenPx`, scale factors, `baseWidthDelta`, and multiplier
    - **Width calculation tracking**: Logs `startWidth`, `baseWidth`, `nextWidth`, and width delta
    - **Props tracking**: Logs BEFORE/AFTER props state for both resize and panel changes
    - **Multiplier calculation**: Logs the ratio between screen delta and base delta to detect 10x issues
- **Instrumentation**:
  - Logging follows pattern from `docs/Component-Framework-Resize-Fix.md`
  - All logs sent to backend via `devLogger` (controlled by `VITE_ENABLE_DEV_LOGS` and `VITE_LOG_SEND_TO_BACKEND`)
  - View logs with: `python backend/enhanced_diagnostic_logs.py --frontend-only --frontend-filter "button" --limit 50`
- **Verification**:
  - Automated checks run: Linter check passed (no errors)
  - Result: **Ready for UAT with logging**
- **Next step**:
  - UAT: Test Appearance → Dimensions → Width changes and check logs
  - UAT: Test E/W resize handles and check logs for multiplier issue
  - Analyze logs to identify root cause of 10x multiplier and panel change failures

---

#### Attempt 04 — Fix preview system and percentage width handling
- **Hypothesis tested**: Preview not working, validation shrinking, percentage widths not applying
- **Change summary**:
  - Files:
    - `frontend/src/features/builder/utils/objectRenderers.tsx` - Added `actionWidthOverride` to `ObjectRendererProps`, updated button renderer to use preview override, fixed percentage width logic
    - `frontend/src/features/builder/components/UniversalFieldShell.tsx` - Fixed proportional scaling to skip validation/help for buttons, pass `actionWidthOverride` to renderer
    - `frontend/src/features/builder/components/SortableComponent.tsx` - Fixed container width to use `previewWidth` during resize preview
  - Key changes:
    - **Added `actionWidthOverride` prop**: Button renderer can now receive preview width overrides via `ObjectRendererProps`
    - **Button-only scaling**: During preview, only action object scales proportionally, validation/help stay fixed width
    - **Container width during preview**: Uses `previewWidth` (in pixels) during resize, falls back to percentage/pixel width otherwise
    - **Percentage width fix**: Button renderer now ignores `actionWidthOverride` when `component.props.width` is a percentage, always uses `100%` to fill container
    - **Preview override priority**: Preview override > props override > buttonWidth prop > component width
- **Instrumentation**:
  - Enhanced logging already in place from Attempt 03
- **Verification**:
  - Automated checks run: Linter check passed (no errors)
  - Result: **Partially Fixed** - UAT revealed issues persist
- **UAT Results**:
  - ❌ Panel percentage widths still have no effect
  - ❌ Resize preview still exactly the same (button not updating, validation shrinking)
  - ✅ SmartBorder works correctly
- **Root Cause Analysis**:
  - **Panel issue**: Logs show `updates: { width: "25%" }` but `actionWidthOverride: undefined` is NOT being set/deleted. Button renderer still sees old `actionWidthOverride` value (392px) and uses it instead of percentage width.
  - **Preview issue**: Button renderer receives `actionWidthOverride` prop, but container width may not be updating correctly, or validation is being constrained by container width changes.

---

#### Attempt 05 — Fix percentage width priority and validation group width constraint
- **Hypothesis tested**: `actionWidthOverride` being used even for percentage widths, validation groups constrained by container width during preview
- **Change summary**:
  - Files:
    - `frontend/src/features/builder/utils/objectRenderers.tsx` - Fixed button renderer to check `isPercentageWidth` FIRST, ignore `actionWidthOverride` for percentages
    - `frontend/src/features/builder/components/UniversalFieldShell.tsx` - Fixed group width logic: only action group fills container for buttons, validation/help groups use natural width
  - Key changes:
    - **Percentage width priority**: Button renderer now checks `isPercentageWidth` FIRST, before checking `actionWidthOverride`
    - **Validation group width**: For buttons in vertical layout, only the action object group gets `width: '100%'`, validation/help groups use natural width
    - **Enhanced logging**: Added `actionWidthOverrideProp` and `actionWidthOverrideFromProps` to button width calculation logs
- **Verification**:
  - Automated checks run: Linter check passed (no errors)
  - Result: **Partially Fixed** - UAT revealed issues persist
- **UAT Results**:
  - ❌ Panel percentage widths still have no effect
  - ❌ Resize preview still exactly the same (button not updating, validation shrinking)
  - ✅ SmartBorder works correctly
- **Root Cause Analysis (from logs)**:
  - **Panel issue**: Logs show `updates: { width: "50%" }` is sent, but component still has `componentWidth: "909px"` - update not reaching component OR being overwritten
  - **Resize issue**: `handleWidthChange` ALWAYS converts width to pixels (`${newWidth}px`) on line 1994, overwriting percentage widths
  - **Preview issue**: Button renderer logs show `actionWidthOverrideProp: undefined` (not shown but implied), meaning preview override not reaching renderer

---

#### Attempt 06 — Fix resize commit to preserve percentage widths and ensure undefined values reach store
- **Hypothesis tested**: Resize commit always converts to pixels (overwriting percentages), undefined values not reaching store
- **Change summary**:
  - Files:
    - `frontend/src/features/builder/components/SortableComponent.tsx` - Fixed `handleWidthChange` to preserve percentage width format during resize commit
    - `frontend/src/features/builder/components/properties/AppearanceSection.tsx` - Enhanced updates object construction to ensure undefined values are included
  - Key changes:
    - **Preserve percentage on resize**: If component had percentage width before resize, keep it (resize only changes pixel values, not percentage)
    - **Delete actionWidthOverride for percentages**: When preserving percentage, set `actionWidthOverride: undefined` so store deletes it
    - **Enhanced logging**: Added logging to show if `actionWidthOverride` is in updates object and its value
- **Verification**:
  - Automated checks run: Linter check passed (no errors)
  - Result: **BROKEN** - Resize stopped working, percentage widths still don't work
- **UAT Results**:
  - ❌ Panel percentage widths still have no effect
  - ❌ E resize handle does nothing (broken by preserving percentage width)
- **Root Cause**: Preserving percentage width during resize prevents visual changes - resize must convert to pixels

---

#### Attempt 07 — Revert broken resize change and fix undefined value inclusion
- **Hypothesis tested**: Resize must convert to pixels (user drags to specific pixel width), undefined values not being included in updates object
- **Change summary**:
  - Files:
    - `frontend/src/features/builder/components/SortableComponent.tsx` - Reverted to always convert to pixels on resize (correct behavior)
    - `frontend/src/features/builder/components/properties/AppearanceSection.tsx` - Fixed to explicitly set `actionWidthOverride: undefined` using direct assignment (not Object.assign)
  - Key changes:
    - **Resize always converts to pixels**: User drags to specific pixel width, so always use pixels (reverted broken change)
    - **Explicit undefined assignment**: Use `(updates as any).actionWidthOverride = undefined` to ensure key exists with undefined value
    - **Enhanced logging**: Added `actualUpdatesKeys` and `hasActionWidthOverrideKey` to verify key exists
- **Verification**:
  - Automated checks run: Linter check passed (no errors)
  - Result: **Ready for UAT**

---
