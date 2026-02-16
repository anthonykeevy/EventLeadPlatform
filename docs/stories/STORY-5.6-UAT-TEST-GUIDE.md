# Story 5.6 UAT Test Guide — Publish Request Workflow

**Story:** 5.6  
**Epic:** 5 - Form Builder Readiness + Review & Publishing  
**Status:** Skeleton — expand per implementation  
**Created:** 2026-02-16  

---

## Scope (UAT Coverage)

Story 5.6 UAT verifies:

1. **DC1:** Company-level RequirePublishApproval config; Company User sees "Request Publish" when enabled
2. **DC2:** FormPublishRequest table + API; create request; validate readiness; form status → Pending Review
3. **DC3:** Request Publish modal in Builder: select admin(s), optional message; success shows Pending Admin Review
4. **DC4:** Admin Dashboard: pending publish requests queue; deep link to Review and Publish
5. **DC5:** Duplicate requests handled (idempotent or "already pending" message)

---

## Pre-conditions

- Stories 5.1–5.5 complete (assets, company defaults, schema, shared resolver, preview/production governance)
- Backend and frontend running
- At least one company with multiple users (Company User + Company Admin)
- Company has RequirePublishApproval enabled
- At least one form in Draft with readiness met (or threshold disabled)

---

## UAT Steps

| DC | Focus | Key verification |
|----|-------|------------------|
| DC1 | Approval config | Enable RequirePublishApproval for company → Company User sees "Request Publish"; disable → Company User sees "Publish" (subject to test threshold) |
| DC2 | Create request | Company User creates publish request via API or UI → FormPublishRequest record created; form status = Pending Review; readiness validated before create |
| DC3 | Request modal | Builder: Company User clicks Request Publish → modal opens; select admin(s), optional message; submit → success; Builder shows "Pending Admin Review" |
| DC4 | Admin queue | Company Admin opens Dashboard → sees pending publish requests; each row has form name, requester, date; deep link to Review and Publish |
| DC5 | Duplicates | Create second request for same form while first pending → idempotent (no duplicate) or clear "Already pending" message |

---

## Manual UAT Checklist

### Company User flow

- [ ] Log in as Company User (company with RequirePublishApproval enabled)
- [ ] Open form in Builder; ensure readiness met (or threshold disabled)
- [ ] Verify CTA shows "Request Publish" (not "Publish")
- [ ] Click Request Publish → modal opens
- [ ] Select admin(s), add optional message, submit
- [ ] Verify success: Builder shows "Pending Admin Review"
- [ ] Verify Event Dashboard shows "Pending Review" badge

### Admin queue

- [ ] Log in as Company Admin (same company)
- [ ] Open Dashboard / Event Dashboard
- [ ] Verify pending publish requests visible (queue or embedded list)
- [ ] Verify each row: form name, requester, requested date
- [ ] Click deep link → navigates to Review and Publish route (page may be minimal in 5.6)

### Config and duplicates

- [ ] Disable RequirePublishApproval → Company User sees "Publish" (subject to test threshold)
- [ ] Attempt duplicate request for same form → handled (no duplicate row or clear message)

---

## Pass Criteria

- [ ] All DC1–DC5 checks pass
- [ ] No regressions in form save/load, readiness display, or publish flow (Company Admin)

---

*Refine during implementation. UAT results feed into final PASS/FAIL.*
