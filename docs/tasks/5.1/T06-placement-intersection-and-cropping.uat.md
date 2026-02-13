# UAT Checklist: T06 Placement + Intersection + Cropping

**Story:** 5.1 - Background Asset Management  
**Task:** T06 - Placement + Intersection + Cropping  
**Generated:** 2026-02-11

---

## Pre-conditions

- [ ] Backend server is running (http://127.0.0.1:8000)
- [ ] Frontend is running (http://localhost:3000)
- [ ] User is logged in
- [ ] At least one form exists with a background image (asset or external URL)

---

## Test Steps

### AC1: Background placement is persisted and applied correctly

- [ ] Step 1: Open form builder, select a form, ensure Background layer has an image
- [ ] Step 2: In Background Properties, adjust X, Y, Width, Height (placement values)
- [ ] Step 3: Verify the builder canvas displays the background at the new position/size
- [ ] Step 4: Switch to public preview or open the form via public link
- [ ] Step 5: Verify the same placement is applied in the renderer

### AC2: Fully off-canvas backgrounds are removed from canvas

- [ ] Step 1: With an image background, set X to a large negative value (e.g. -2000) or move Width/Position so the entire image is off-canvas
- [ ] Step 2: Verify the background disappears from the canvas
- [ ] Step 3: Verify the background is cleared from the page (no image on canvas)

### AC3: Asset remains in the library after auto-removal

- [ ] Step 1: After moving background off-canvas and auto-removal
- [ ] Step 2: Open the asset library (Select from Library)
- [ ] Step 3: Verify the previously used asset still appears in the library

### Regression Check

- [ ] Color-only backgrounds still render in builder and public form
- [ ] External URL backgrounds work in both contexts
- [ ] No console errors when loading forms with backgrounds
- [ ] Form submission still works

---

## Post-conditions

- [ ] Builder and renderer show placement correctly when applied
- [ ] Off-canvas auto-removal works; asset stays in library

---

**Instructions for Human Tester:**
1. Execute each step in order
2. Mark ✅ or ❌ for each item
3. Add notes for any failures
4. When complete, run `@ralf-uat *record-uat` with your results
