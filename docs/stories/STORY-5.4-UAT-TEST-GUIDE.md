# Story 5.4 UAT Test Guide — Shared Resolver Parity

**Story:** 5.4  
**Epic:** 5 - Form Builder Readiness + Review & Publishing  
**Status:** Skeleton — expand per implementation  
**Created:** 2026-02-16  

---

## Scope (UAT Coverage)

Story 5.4 UAT verifies:

1. **DC1:** Backend and frontend defaults resolution produce identical theme, globalStyles, canvasSettings for the same inputs (parity tests pass)
2. **DC2:** Parity tests in backend/tests/ with shared fixtures
3. **DC3:** `docs/stories/STORY-5.4-RESOLUTION-RULES.md` documents merge algorithm and asset resolution
4. **DC4:** Builder preview and public renderer use same asset resolution path; audit confirms no divergence
5. **DC5:** Future Review and Publish integration documented

---

## Pre-conditions

- Stories 5.1, 5.2, 5.3 complete (assets, company defaults, Init API, schema validation)
- Backend and frontend running
- Test fixtures for merged defaults + form overrides available

---

## UAT Steps

| DC | Focus | Key verification |
|----|-------|-------------------|
| DC1 | Defaults parity | Parity test: given fixture (merged defaults + form overrides), Python and TypeScript output identical theme, globalStyles, canvasSettings |
| DC2 | Parity tests | pytest runs; fixtures in backend/tests/ or shared; tests pass in CI |
| DC3 | Documentation | STORY-5.4-RESOLUTION-RULES.md exists; describes merge order (Global → Company → Form); asset resolution rules |
| DC4 | Asset audit | FormBuilderCanvas and PublicFormArtboard both use useBackgroundImageUrl; no duplicate/divergent logic |
| DC5 | Review prep | Doc section: future Story 5.6 Review UI must use resolve_definition_for_render (backend) or verified frontend parity |

---

## Manual UAT Checklist

### Defaults parity

- [ ] Run parity tests: `python -m pytest backend/tests/ -k parity` (or equivalent)
- [ ] All parity tests pass
- [ ] Manually: create form with company defaults; builder preview and public form (with token) render same theme/colors

### Asset resolution

- [ ] Form with background image (asset ref): builder inline preview shows image
- [ ] Same form in public renderer (token): background image displays correctly
- [ ] No console errors; both use same resolution path

### Documentation

- [ ] STORY-5.4-RESOLUTION-RULES.md complete
- [ ] Review and Publish section documents resolver contract for Story 5.6

---

## Pass Criteria

- [ ] All DC1–DC5 checks pass
- [ ] Parity tests pass in CI
- [ ] No regressions in Form Builder save/load or public form render

---

*Refine during implementation. UAT results feed into final PASS/FAIL.*
