# UAT Checklist: T02 - Grid CSS Rendering

**Story:** 3.10 - Grid Layout System  
**Task:** T02 - Grid CSS Rendering  
**Prepared:** 2026-01-14

---

## Environment Setup

- [ ] Frontend dev server is running (`npm run dev` in frontend folder)
- [ ] Form builder is accessible at localhost

---

## Verification Steps

### AC1: Components with `gridLayout` render as CSS Grid

**Test Setup:**
To test grid layout rendering, you need to manually add a `gridLayout` config to a component. This can be done via browser DevTools or by temporarily editing the form definition.

**Option A: DevTools Test (Recommended)**

1. Open the form builder in browser
2. Add a text field to the canvas
3. Open browser DevTools → Console
4. Run this code to add grid layout to the component:

```javascript
// Find the builder store
const store = window.__BUILDER_STORE__;
// Or access via React DevTools and find useBuilderStore

// Add gridLayout to first component
const components = store.getState().pages[0].components;
if (components.length > 0) {
  const comp = components[0];
  comp.props.gridLayout = {
    rows: 3,
    columns: 1,
    columnGap: 8,
    rowGap: 8,
    cellAssignments: {
      "0-0": "label",
      "1-0": "input",
      "2-0": "validation"
    }
  };
  // Force re-render
  store.setState({ pages: [...store.getState().pages] });
}
```

5. Inspect the component in DevTools Elements panel

- [ ] **Verify:** Component has a container with `display: grid`
- [ ] **Verify:** Container has `gridTemplateRows` with values like `1fr 8px 1fr 8px 1fr`
- [ ] **Verify:** Container has `gridTemplateColumns: 1fr`

**Option B: Code Modification Test**

1. In `frontend/src/features/builder/utils/gridLayoutUtils.ts`, add a test log:
   ```typescript
   // In generateGridStyles(), add:
   console.log('Grid styles generated:', styles);
   ```
2. Add gridLayout to a component in form definition
3. Check console for log output

---

### AC2: Objects appear in assigned cells

**Prerequisites:** Complete AC1 setup with grid layout

- [ ] **Verify:** Label object appears in row 1 (gridRow: "1 / 2")
- [ ] **Verify:** Input object appears in row 3 (gridRow: "3 / 4", accounting for gap track)
- [ ] **Verify:** Validation object appears in row 5 (gridRow: "5 / 6", accounting for gap tracks)
- [ ] **Verify:** Objects not in cellAssignments are NOT rendered

**Negative Test:**
1. Remove an object from cellAssignments (e.g., remove "validation")
2. **Verify:** That object is not visible in the component

---

### AC3: Default gaps render correctly

**Prerequisites:** Complete AC1 setup with grid layout

1. Inspect the grid container in DevTools
2. Check the `gridTemplateRows` value

- [ ] **Verify:** Format is `1fr 8px 1fr 8px 1fr` (content tracks separated by 8px gap tracks)
- [ ] **Verify:** Visual gap between label and input is visible (~8px)
- [ ] **Verify:** Visual gap between input and validation is visible (~8px)

**Custom Gap Test:**
1. Modify the gridLayout to use custom gaps:
   ```javascript
   comp.props.gridLayout = {
     ...comp.props.gridLayout,
     rowGap: 16,
     rowGaps: { 0: 24 }  // Custom gap after first row
   };
   ```
2. **Verify:** First gap (label→input) is larger (24px)
3. **Verify:** Second gap (input→validation) is 16px

---

### AC4: Rendering works on canvas surface

**Prerequisites:** Complete AC1 setup

1. View the component on the canvas (builder mode)
2. Select the component

- [ ] **Verify:** SmartBorder appears around the component
- [ ] **Verify:** Grid layout renders correctly inside SmartBorder
- [ ] **Verify:** Resize handles still appear (if applicable)
- [ ] **Verify:** Component can be selected and dragged

---

### AC5: Rendering works on runtime surface

**Test Setup:**
1. Add a component with gridLayout configuration
2. Navigate to the form preview/runtime mode (if available)

OR

3. Test via PublicFormRendererPage if a form with grid layout is published

- [ ] **Verify:** Grid layout renders correctly in runtime mode
- [ ] **Verify:** Input fields are functional (can type, focus, etc.)
- [ ] **Verify:** Validation errors display in correct grid position
- [ ] **Verify:** No SmartBorder or builder chrome visible

---

## Regression Check

- [ ] **Verify:** Components WITHOUT gridLayout still render using Object Layout
- [ ] **Verify:** Vertical layout (label above input) works correctly
- [ ] **Verify:** Horizontal layout (label beside input) works correctly
- [ ] **Verify:** Mixed layouts work correctly
- [ ] **Verify:** No console errors related to grid layout when using Object Layout

---

## Code Inspection (Optional)

For thorough verification:

1. [ ] Open `frontend/src/features/builder/components/UniversalFieldShell.tsx`
2. [ ] Verify `getEffectiveGridLayout()` function exists (~line 117)
3. [ ] Verify `renderWithGridLayout()` function exists (~line 396)
4. [ ] Verify `content` useMemo checks `effectiveGridLayout` first (~line 653)

---

## Pass/Fail Summary

| AC | Description | Status |
|----|-------------|--------|
| AC1 | Components with `gridLayout` render as CSS Grid | ⬜ |
| AC2 | Objects appear in assigned cells | ⬜ |
| AC3 | Default gaps render correctly | ⬜ |
| AC4 | Rendering works on canvas surface | ⬜ |
| AC5 | Rendering works on runtime surface | ⬜ |
| Regression | Object Layout still works | ⬜ |

---

## UAT Result

- [ ] **PASS** - All acceptance criteria verified
- [ ] **FAIL** - Issues found (document below)

### Issues Found (if any)

_None documented_

---

*UAT checklist generated by Ralf-Dev*  
*Generated: 2026-01-14*
