# Task Retrospective: T06 - Placement + Intersection + Cropping

**Story:** 5.1 - Background Asset Management  
**Task:** T06 - Placement + Intersection + Cropping  
**Final Status:** ✅ HumanDone  
**Date:** 2026-02-13

---

## What Went Well

| What Went Well | Evidence |
|----------------|----------|
| All ACs and regression checks passed on human UAT | `T06-placement-intersection-and-cropping.uat-results.md` — AC1, AC2, AC3, R1–R4 all Pass |
| Foundation from T01 (contracts) and T05 (resolver) enabled clean implementation | Completion Note § Changes; `backgroundPlacementUtils.ts` created; FormBuilderCanvas + PublicFormArtboard use placement consistently |
| Placement utils isolated and reusable | `backgroundPlacementUtils.ts`: `isBackgroundFullyOffCanvas`, `createDefaultPlacement` |
| Off-canvas auto-remove clears page but not library | AC3 verified: asset remains in library after auto-removal (`T06-placement-intersection-and-cropping.uat-results.md`) |
| Explicit regression checklist in UAT | R1 (color-only), R2 (external URL), R3 (no console errors), R4 (form submission) — per T05 learning |
| Build passed before human UAT | Completion Note § Test Evidence: `npm run build` passed in T06 worktree |
| Scope boundary respected | Crop UI out of scope; crop supported in rendering; can be added later |

---

## What Went Wrong

| Issue | Root Cause | Evidence |
|-------|------------|----------|
| Crop UI not implemented | Explicitly out of scope; crop supported programmatically in rendering | Completion Note § Out-of-scope: "Crop UI not added (crop can be set programmatically)" |
| Worktree needed npm install before build | Standard for fresh worktrees | Common across Epic 5 tasks |

---

## Prevention Actions

| Issue | Prevention Action | Owner |
|-------|-------------------|-------|
| (None critical) | — | — |
| Placement/intersection tasks | Continue explicit regression checklist (color-only, external URL, console, form submit) | ralf-uat |

---

## Test Improvements

### Automated Tests to Add

| Test Type | Description | Location | Command |
|-----------|-------------|----------|---------|
| Unit | `isBackgroundFullyOffCanvas` — fully on, fully off, partial overlap | `backgroundPlacementUtils.test.ts` | `npm test backgroundPlacementUtils` |
| Unit | `createDefaultPlacement` returns valid placement object | `backgroundPlacementUtils.test.ts` | `npm test backgroundPlacementUtils` |
| Integration | Placement round-trip: builder → definition → renderer shows same position/size | Builder/renderer integration | `npm run test:int` (if configured) |

### UAT Automation Candidates

- **Console check:** `list_console_messages` when loading form with placement — no errors
- **Definition check:** Verify `page.background.placement` is present after adjusting X/Y/W/H

---

## Process Improvements

### For ralf-sm (Decomposition)
- Placement/cropping tasks: scope "crop UI" explicitly (in vs out) to avoid ambiguity.

### For ralf-dev (Execution)
- Run build after placement/utils changes; canvas rendering is sensitive to type/shape of placement object.
- When adding intersection logic: test edge cases (fully on, fully off, partial) in isolation.

### For ralf-uat (Validation)
- Keep explicit regression items (color-only, external URL, console, form submit) for canvas/rendering tasks.

---

## Scope Creep Discovered

| Item | Classification | Routing |
|------|----------------|---------|
| Crop UI | OUT_OF_SCOPE | Documented; future task if needed |
| None | — | — |

---

## If We Ran This Again

1. **Add unit tests for placement utils early** — `isBackgroundFullyOffCanvas` and `createDefaultPlacement` are pure functions; easy to test edge cases before integration.
2. **Explicit scope on crop** — Spec already noted crop is supported in rendering but UI is out of scope; this prevented scope creep.
3. **Regression checklist pattern works** — T05 learning (explicit Pass/Fail per regression item) applied; human UAT had clear R1–R4 to verify.

---

*Retro completed 2026-02-13*
