# Task Retrospective: T07 — Builder Defaults on New Form + Save to Company Defaults

**Story:** 5.2 - Company Form Defaults (Brand System)  
**Task:** T07 - Builder Defaults on New Form + Save to Company Defaults  
**Final Status:** ✅ HumanDone  
**Date:** 2026-02-16  

---

## What Went Well

| What Went Well | Evidence |
|----------------|----------|
| All ACs passed on first UAT run | T07-builder-defaults-new-form-save-company.uat-results.md — AC1, AC2, AC3, Regression all Pass |
| T07 scope was minimal: formContext gap only | T07-builder-defaults-new-form-save-company.completion.md — single file change in useBuilderStore.ts |
| T05 had already implemented Save button and Init API | Completion note: "Save button and Init API integration were already wired in T05" |
| formContext fix enabled eventId=null forms | useBuilderStore.ts: formContext set whenever companyId exists; Init API only when eventId present |
| Logic rules bug discovered and fixed during UAT | evaluateRules.ts: extractLogicalValue added for radio/dropdown/checkbox compound values |

---

## What Went Wrong

| Issue | Root Cause | Evidence |
|-------|------------|----------|
| Logic rules (show/hide, require/unrequire) not working for radio in Preview | evaluateRules used JSON.stringify on `{value, extraTextByValue}`; rule compared "yes" vs `'{"value":"yes",...}'` | UAT-results Out of Scope: "Logic rules fix (radio/dropdown value extraction)" |
| None | — | No UAT defects; all ACs passed |

---

## Prevention Actions

| Issue | Prevention Action | Owner |
|-------|-------------------|-------|
| Logic rules regression | Add unit tests for evaluateRules with `{value}`, `{values}` payloads | ralf-dev |
| Logic rules regression | Add UAT regression step: "Form with radio/dropdown + logic rules — verify rules apply in Preview" | ralf-uat |
| Integration-task scope | When prior task (T05) delivers core UX, integration task (T07) focuses on edge cases (eventId=null) — keep that pattern | ralf-sm |

---

## Test Improvements

### Automated Tests to Add

| Test Type | Description | Location | Command |
|-----------|-------------|----------|---------|
| unit | evaluateRules: equals/notEquals/contains with `{value:"yes"}`, `{values:["a"]}` | `frontend/src/features/logic-engine/evaluateRules.test.ts` | `npm test evaluateRules` |
| unit | extractLogicalValue: radio, dropdown, checkbox-with-options | same | same |

### UAT Automation Candidates

- Logic rules verification (radio/dropdown) — add as standard regression for forms with logic; currently manual.
- Init API call verification — Network tab check; could add E2E or Cypress intercept assertion.

---

## Process Improvements

### For ralf-sm (Decomposition)
- T07 as "Integration + UAT" task was correctly scoped: fix gaps + validate. Minimal code change expected when T05 delivered bulk of work.
- AC for "formContext when eventId=null" could be explicit in similar tasks to avoid ambiguity.

### For ralf-dev (Execution)
- When touching form builder state (formContext, Init flow), consider logic-engine as dependent surface — logic rules consume form values.
- extractLogicalValue pattern: document in COMPONENT-FRAMEWORK-REFERENCE or logic-engine README so future component value shapes are handled.

### For ralf-uat (Validation)
- Add optional regression: "Form with radio/dropdown and logic rules — change selection, verify target (required/disabled) updates."
- Checklist already covered eventId=null (R1); this proved valuable.

---

## Scope Creep Discovered

| Item | Classification | Routing |
|------|----------------|---------|
| Logic rules fix (evaluateRules: extract value from radio/dropdown objects) | ENHANCEMENT | Resolved in-session; no routing needed |

---

## If We Ran This Again

1. **Explicit formContext AC for eventId=null** — Add to Task Spec: "formContext set when companyId present even if eventId null" to avoid implicit behavior.
2. **Logic rules as standard regression** — Include logic-rule verification (radio → require/unrequire) in UAT checklist for any task that touches form values or preview.
3. **Unit tests before UAT** — Add evaluateRules tests for compound value types when logic-engine is in scope; would have caught the bug earlier.

---

*Retrospective by Ralf-Retro — 2026-02-16*
