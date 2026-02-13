# UAT Checklist: T05 Shared Resolver Parity

**Story:** 5.1 - Background Asset Management  
**Task:** T05 - Shared Resolver Parity  
**Generated:** 2026-02-11

---

## Pre-conditions

- [ ] Backend server is running (http://127.0.0.1:8000)
- [ ] Frontend is running (http://localhost:3000)
- [ ] User is logged in
- [ ] At least one form exists with a background image (asset or external URL)

---

## Test Steps

### AC1: Builder preview and renderer display the same background asset

- [ ] Step 1: Open form builder, select a form, add a background image (upload or select from library)
- [ ] Step 2: Verify the builder canvas displays the background image (cover/contain/size matches)
- [ ] Step 3: Switch to public preview (or open the form via public link)
- [ ] Step 4: Verify the same background image displays in the renderer with matching size/position

### AC2: Resolver logic is centralized

- [ ] Step 1: Confirm only one resolver module exists: `frontend/src/features/builder/utils/backgroundAssetResolver.ts`
- [ ] Step 2: Confirm both FormBuilderCanvas and PublicFormArtboard use `useBackgroundImageUrl`

### Regression Check

- [ ] Color-only backgrounds still render in builder and public form
- [ ] External URL backgrounds work in both contexts
- [ ] No console errors when loading forms with backgrounds
- [ ] Form submission still works

---

## Post-conditions

- [ ] Builder and renderer show identical background for the same form definition

---

**Instructions for Human Tester:**
1. Execute each step in order
2. Mark ✅ or ❌ for each item
3. Add notes for any failures
4. When complete, run `@ralf-uat *record-uat` with your results
