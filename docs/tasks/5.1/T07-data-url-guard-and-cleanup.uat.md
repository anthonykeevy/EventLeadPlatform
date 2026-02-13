# UAT Checklist: T07 Data URL Guard + Cleanup

**Story:** 5.1 - Background Asset Management  
**Task:** T07 - Data URL Guard + Cleanup  
**Generated:** 2026-02-13

---

## Pre-conditions

- [ ] Backend server is running (http://127.0.0.1:8000)
- [ ] Frontend is running (http://localhost:3000)
- [ ] User is logged in
- [ ] At least one form exists

---

## Test Steps

### AC1: Data URL backgrounds are rejected at input with clear error

- [ ] Step 1: Open form builder, select a form, switch to Background layer, choose Image
- [ ] Step 2: In "Or enter image URL", paste a Data URL (e.g. `data:image/png;base64,iVBORw0KGgo=`)
- [ ] Step 3: Verify the Data URL is NOT applied (background unchanged)
- [ ] Step 4: Verify a clear error message appears (e.g. "Data URLs are not supported...")

### AC2: Legacy Data URLs are stripped on definition load

- [ ] Step 1: (Setup) Manually create or edit a form definition (via API/DB or dev tools) to have a page background with `value: "data:image/png;base64,..."` and no asset reference
- [ ] Step 2: Load the form in the builder
- [ ] Step 3: Verify the background shows as cleared (no Data URL displayed)
- [ ] Step 4: Save the form and verify DefinitionJSON has no base64 in background

### AC3: No base64 blobs remain in DefinitionJSON after save

- [ ] Step 1: With any form in builder (asset background, external URL, or color-only)
- [ ] Step 2: Save the form
- [ ] Step 3: Inspect the saved definition (API response or network tab) for "data:" or "base64"
- [ ] Step 4: Verify no `background.value` contains Data URL

### Regression Check

- [ ] External URL backgrounds still work
- [ ] Asset-based backgrounds still work
- [ ] Color-only backgrounds still work
- [ ] No console errors when loading/saving forms

---

## Post-conditions

- [ ] Data URLs blocked at input with user-facing error
- [ ] Load path strips legacy Data URLs
- [ ] Save produces definitions with asset references only (no base64)

---

**Instructions for Human Tester:**
1. Execute each step in order
2. Mark ✅ or ❌ for each item
3. Add notes for any failures
4. When complete, run `@ralf-uat *record-uat` with your results
