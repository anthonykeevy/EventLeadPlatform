# Task T08: Integration & Coexistence

**Story:** 3.10 - Grid Layout System  
**Task ID:** T08  
**Status:** ✅ Complete  
**Dependencies:** T02 ✅, T03 ✅, T04 ✅, T05 ✅, T06 ✅, T07 ✅  
**Estimated Time:** 2-3 hours  
**Completed:** 2026-01-15  

---

## 📋 Task Overview

**Objective:** Final integration task to verify Grid Layout works end-to-end and coexists properly with Object Layout, including layout switching, canvas/runtime parity, and Story Done Criteria validation.

**User Story:** As a form builder user, I want Grid Layout and Object Layout to both work reliably in the same form without regressions, so I can choose the best layout per component.

---

## ✅ Scope (In)

- [ ] Verify layout switching (Object ↔ Grid) preserves object definitions and assignments
- [ ] Verify Grid Layout does not break Object Layout (regression)
- [ ] Verify both layout types can coexist in same form (different components)
- [ ] Verify canvas and runtime render parity for both layout types
- [ ] Verify all Story Done Criteria are met
- [ ] Fix integration bugs discovered in this verification scope
- [ ] Add minimal UX polish if required to pass Done Criteria

---

## ❌ Scope (Out)

- New features beyond the Grid Layout story
- Refactoring unrelated builder systems
- Backend changes
- Performance optimizations (unless blocking parity)
- New UI controls beyond what was scoped in T01–T07

---

## 🚫 Forbidden Zones

| Zone | Reason |
|------|--------|
| `backend/` | No backend changes |
| `database/` | No schema changes |
| `frontend/src/features/auth/` | Unrelated |
| `frontend/src/features/invitations/` | Unrelated |
| `frontend/src/features/forms/` | Unrelated |
| `frontend/src/features/events/` | Unrelated |

---

## 🎯 Acceptance Criteria

### AC1: Layout Switching Preserves Objects

**Criterion:** Switching a component between Object Layout and Grid Layout does not delete or lose object data. Object assignments are preserved appropriately per layout.

**Verification:**
- Start with Object Layout component (with layoutGroups populated)
- Switch to Grid Layout (creates gridLayout config)
- Assign objects in gridLayout
- Switch back to Object Layout (gridLayout cleared)
- Verify layoutGroups still intact
- Switch back to Grid Layout
- Verify gridLayout config restored or re-created per spec (global defaults or system defaults)

**Implementation Notes:**
- Grid takes precedence when `gridLayout` is set
- Object Layout uses `objectLayout` + `layoutGroups`
- Switching to Object Layout clears `gridLayout` (existing behavior)

---

### AC2: Object Layout Regression Check

**Criterion:** Existing Object Layout behavior still works as before.

**Verification:**
- Pick a component using Object Layout
- Verify drag-and-drop layout groups still function
- Verify object order changes reflect in preview
- Verify runtime preview renders correctly

---

### AC3: Grid and Object Layout Coexist in Same Form

**Criterion:** In a single form, one component can use Grid Layout and another can use Object Layout without interference.

**Verification:**
- Component A: Grid Layout (2×2 with assignments)
- Component B: Object Layout (vertical or mixed)
- Verify both render correctly on canvas
- Verify both render correctly in runtime preview
- No console errors when switching between components

---

### AC4: Canvas vs Runtime Parity

**Criterion:** Grid Layout renders identically on canvas and runtime preview (structure, gaps, spanning, assignments).

**Verification:**
- Use grid with merged cells + individual gaps
- Verify canvas preview matches runtime output
- Verify object spans and gaps are consistent

---

### AC5: Story Done Criteria Pass

**Criterion:** All Story Done Criteria (DC1–DC5) are satisfied with evidence.

**Verification:**
- DC1: Grid Layout modal opens and saves configuration correctly
- DC2: Objects can be assigned to grid cells via drag-and-drop
- DC3: Grid renders correctly on canvas and in runtime preview
- DC4: Component overrides work independently of global defaults
- DC5: Grid Layout does NOT break existing Object Layout functionality

---

## 🔧 Implementation Details

### Files to Modify

| File | Change Type | Description |
|------|-------------|-------------|
| `GridLayoutSection.tsx` | Modify | Fix integration bugs if found |
| `GridLayoutEditor.tsx` | Modify | Fix preview parity issues if found |
| `GlobalStylesPanel.tsx` | Modify | Fix global defaults integration issues if found |
| `gridLayoutUtils.ts` | Modify | Fix resolution or validation issues if found |
| `ObjectLayoutSection.tsx` | Modify | Only if regression found |

---

## 🧪 Required Tests

### Manual Verification (Integration Checklist)

1. **Global Defaults + Grid Layout**
   - Set global default grid layout (rows/columns/gaps)
   - Create component with no override
   - Verify it uses global grid defaults

2. **Component Override**
   - Click \"Override Global\" for a component
   - Modify rows/columns
   - Verify component uses override while others still use global

3. **Switch Layout Modes**
   - Toggle component from Object Layout → Grid Layout
   - Assign grid objects
   - Toggle back to Object Layout and verify layoutGroups intact

4. **Grid Merging + Spacing**
   - Merge a 2×1 cell group
   - Set individual row/column gaps
   - Verify span and gaps on canvas

5. **Canvas vs Runtime**
   - Open runtime preview
   - Verify grid structure, gaps, and assignments match canvas

6. **Regression: Object Layout**
   - Use Object Layout drag-and-drop (rows/groups)
   - Verify no regressions or errors

### DevTools MCP Verification

Use DevTools MCP to validate runtime state:

1. `navigate_page` to builder
2. `list_console_messages` → No errors
3. `evaluate_script` → verify gridLayout on selected component

Example script:
```javascript
const store = window.__ZUSTAND_DEVTOOLS__;
const selected = store.getState().selectedComponentId;
const comp = store.getState().components.find(c => c.id === selected);
console.log(comp.props.gridLayout);
```

### Build Verification

```bash
ReadLints: GridLayoutSection.tsx, GridLayoutEditor.tsx, GlobalStylesPanel.tsx, gridLayoutUtils.ts
```

---

## 📚 References

- Story Done Criteria: `docs/stories/story-3.10.md`
- Grid Layout Guide: `docs/GRID-LAYOUT-GUIDE.md` (Resolution Order, Coexistence)
- Component Framework: `docs/COMPONENT-FRAMEWORK-REFERENCE.md`

---

## ⚠️ Edge Cases

| Case | Expected Behavior |
|------|-------------------|
| Component has gridLayout + objectLayout | Grid Layout takes precedence |
| Global default set, component override cleared | Component uses global values |
| Global default removed | Component falls back to system defaults |
| Switching layouts repeatedly | No data loss, no console errors |

---

## 📝 Handoff Requirements

On completion, provide:
1. `T08-integration-coexistence.completion.md` with:
   - Files changed
   - AC verification evidence
   - Regression results
2. `T08-integration-coexistence.uat.md` with:
   - Step-by-step manual test instructions
   - DevTools MCP verification steps

---

*Task Spec created by Ralf-SM*  
*Date: 2026-01-15*
