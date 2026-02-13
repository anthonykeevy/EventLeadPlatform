# UAT Results: T06 - Placement + Intersection + Cropping

**Story:** 5.1 - Background Asset Management  
**Task:** T06  
**Tester:** Anthony Keevy  
**Date:** 2026-02-13  
**Status:** ✅ PASSED

---

## Summary

| Area | Result |
|------|--------|
| AC1: Placement persisted and applied | ✅ Pass |
| AC2: Off-canvas auto-remove | ✅ Pass |
| AC3: Asset stays in library | ✅ Pass |
| Regression Check | ✅ Pass |

---

## Step Results

### AC1: Background placement is persisted and applied correctly

| Step | Action | Expected Result | Pass/Fail | Evidence |
|------|--------|-----------------|-----------|----------|
| 1.1 | Open form builder, select form with image background | Background visible | Pass | Tester verified |
| 1.2 | Adjust X, Y, Width, Height in Background Properties | Canvas updates live | Pass | Tester verified |
| 1.3 | Switch to public preview | Same placement in renderer | Pass | Tester verified |

### AC2: Fully off-canvas backgrounds are removed from canvas

| Step | Action | Expected Result | Pass/Fail | Evidence |
|------|--------|-----------------|-----------|----------|
| 2.1 | Set X to large negative (e.g. -2000) or move fully off-canvas | Background disappears | Pass | Tester verified |
| 2.2 | Verify canvas | No image on canvas | Pass | Tester verified |

### AC3: Asset remains in library after auto-removal

| Step | Action | Expected Result | Pass/Fail | Evidence |
|------|--------|-----------------|-----------|----------|
| 3.1 | Open asset library after off-canvas auto-removal | Asset still in library | Pass | Tester verified |

### Regression Check

| Step | Action | Expected Result | Pass/Fail | Evidence |
|------|--------|-----------------|-----------|----------|
| R1 | Color-only backgrounds | Renders in builder and public | Pass | Tester verified |
| R2 | External URL backgrounds | Works in both contexts | Pass | Tester verified |
| R3 | Forms with backgrounds | No console errors | Pass | Tester verified |
| R4 | Form submission | Still works | Pass | Tester verified |

---

## Defects

None.

---

## Out-of-Scope Items

None.

---

## Conclusion

All acceptance criteria and regression checks passed. Task T06 is ready for retrospective and closeout.
