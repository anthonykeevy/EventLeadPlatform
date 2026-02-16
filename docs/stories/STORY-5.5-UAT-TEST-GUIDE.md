# Story 5.5 UAT Test Guide — Preview/Production Governance Foundations

**Story:** 5.5  
**Epic:** 5 - Form Builder Readiness + Review & Publishing  
**Status:** Skeleton — expand per implementation  
**Created:** 2026-02-16  

---

## Scope (UAT Coverage)

Story 5.5 UAT verifies:

1. **DC1:** Submissions store preview vs production flag; backend and API support filtering by mode
2. **DC2:** Test threshold configurable per company (enabled/disabled, threshold value)
3. **DC3:** Test runs (preview + "Record test run") counted and audited
4. **DC4:** Publish blocked when threshold enabled and not met; clear UI message
5. **DC5:** Readiness badge visible in Builder or Dashboard

---

## Pre-conditions

- Stories 5.1–5.4 complete (assets, company defaults, schema, shared resolver)
- Backend and frontend running
- At least one company with a form

---

## UAT Steps

| DC | Focus | Key verification |
|----|-------|------------------|
| DC1 | Preview/production flag | Submit form in preview mode → submission has is_preview=true; submit in production → is_preview=false. API/list supports filter by mode. |
| DC2 | Test threshold | Company settings: enable test threshold, set value (e.g. 3). Verify stored in DB/config. Disable → threshold not enforced. |
| DC3 | Test run audit | Perform preview submission and "Record test run". Verify count increments; audit shows who + when. |
| DC4 | Publish block | With threshold enabled and count below threshold: attempt publish → blocked with message (e.g. "3 more test runs needed"). |
| DC5 | Readiness badge | Builder or Dashboard shows readiness (e.g. "Ready to publish" when threshold met, "X more test runs needed" when not). |

---

## Manual UAT Checklist

### Preview vs production

- [ ] Open form in preview mode; submit → submission flagged as preview
- [ ] Open form in production mode; submit → submission flagged as production
- [ ] Filter submissions by mode (API or UI)

### Test threshold

- [ ] Enable test threshold for company; set value (e.g. 3)
- [ ] Verify storage (DB or config)
- [ ] Disable threshold → publish not blocked by test count

### Publish block + readiness

- [ ] With threshold enabled and 0 test runs: publish blocked, message visible
- [ ] Perform test runs (preview submit or Record test run) until threshold met
- [ ] Readiness badge updates; publish allowed when threshold met

---

## Pass Criteria

- [ ] All DC1–DC5 checks pass
- [ ] No regressions in form submission or public form render

---

*Refine during implementation. UAT results feed into final PASS/FAIL.*
