# UAT Checklist: T10

**Story:** 3.11
**Task:** Frontend Build Stabilization (lint + build clean)
**Generated:** 2026-02-06

---

## Pre-conditions

- [ ] Node dependencies installed in `frontend/` (`npm install`)

## Test Steps

### AC1: `npm run lint` passes

- [ ] Step 1: `cd frontend; npm run lint` → Verify: exits 0 (warnings ok).

### AC2: `npm run build` passes

- [ ] Step 1: `cd frontend; npm run build` → Verify: build succeeds.

### AC3: Any remaining warnings are documented

- [ ] Step 1: Review lint output → Verify: only warnings reported, no errors.
- [ ] Step 2: Review build output → Verify: any warnings are captured in notes.

### AC4: Fixes are committed on a task branch with a PR to the story branch

- [ ] Step 1: Open PR https://github.com/anthonykeevy/EventLeadPlatform/pull/18 → Verify: base branch is `story/epic3-3.11-dynamic-submission`.

## Regression Check

- [ ] Verify no additional errors when re-running `npm run lint`.
- [ ] Verify no additional errors when re-running `npm run build`.

## Post-conditions

- [ ] Lint/build baseline remains green for the task branch.

---

**Instructions for Human Tester:**
1. Execute each step in order
2. Mark ✅ or ❌ for each item
3. Add notes for any failures
4. When complete, run `@ralf-uat *record-uat` with your results
