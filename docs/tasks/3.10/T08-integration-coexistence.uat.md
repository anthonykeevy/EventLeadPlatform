# UAT Checklist: T08

**Story:** 3.10  
**Task:** Integration & Coexistence  
**Generated:** 2026-01-15

---

## Pre-conditions

- [ ] Backend server is running
- [ ] Frontend is running
- [ ] User is logged in
- [ ] Builder is open to a form with at least two components

## Test Steps

### AC1: Layout Switching Preserves Objects

- [ ] Step 1: Select a component using Object Layout with layoutGroups populated  
  → Verify: layoutGroups visible in Object Layout editor
- [ ] Step 2: Switch to Grid Layout and assign objects to grid cells  
  → Verify: assignments appear in grid editor
- [ ] Step 3: Switch back to Object Layout  
  → Verify: layoutGroups remain intact
- [ ] Step 4: Switch back to Grid Layout  
  → Verify: gridLayout config is re-created per defaults and no stale merged assignments remain

### AC2: Object Layout Regression Check

- [ ] Step 1: Use Object Layout drag-and-drop to reorder objects  
  → Verify: row order updates and persists
- [ ] Step 2: Open runtime preview  
  → Verify: Object Layout renders correctly

### AC3: Grid and Object Layout Coexist in Same Form

- [ ] Step 1: Component A → Grid Layout (2×2), assign objects  
  → Verify: grid renders correctly on canvas
- [ ] Step 2: Component B → Object Layout (vertical or mixed)  
  → Verify: object layout renders correctly on canvas
- [ ] Step 3: Open runtime preview  
  → Verify: both components render correctly
- [ ] Step 4: Switch between components in builder  
  → Verify: no console errors

### AC4: Canvas vs Runtime Parity

- [ ] Step 1: Configure merged cells and individual row/column gaps  
  → Verify: grid preview reflects merges and gaps
- [ ] Step 2: Open runtime preview  
  → Verify: grid structure, spans, and gaps match canvas

### AC5: Story Done Criteria (DC1–DC5)

- [ ] DC1: Grid Layout modal opens and saves configuration correctly  
  → Verify: reopening shows saved settings
- [ ] DC2: Objects can be assigned to grid cells via drag-and-drop  
  → Verify: assignments persist
- [ ] DC3: Grid renders correctly on canvas and runtime preview  
  → Verify: parity confirmed
- [ ] DC4: Component overrides work independently of global defaults  
  → Verify: component override changes do not affect others
- [ ] DC5: Grid Layout does NOT break existing Object Layout functionality  
  → Verify: Object Layout works as before

## Regression Check

- [ ] Verify Object Layout drag-and-drop still works
- [ ] Verify no console errors in browser
- [ ] Verify runtime preview opens without errors

## Post-conditions

- [ ] Builder state is stable; no objects lost during layout switching

## Edge Cases (if applicable)

- [ ] Switch Object ↔ Grid repeatedly (3+ times)  
  → Verify: no data loss, no console errors

---

**Instructions for Human Tester:**
1. Execute each step in order
2. Mark ✅ or ❌ for each item
3. Add notes for any failures
4. When complete, run `@ralf-uat *record-uat` with your results
