# UAT Results: T03 - Backend Public Submission Endpoint + Idempotency

**Story:** 3.11 - Dynamic Submission (Outbox)  
**Task:** T03 - Backend: Public Submission Endpoint + Idempotency  
**Tester:** Anthony Keevy  
**Date:** 2026-02-03  
**Overall Result:** ✅ PASS  

---

## Step Results

| AC | Result | Evidence |
|----|--------|----------|
| AC1 | ✅ PASS | Invalid token returns `404` |
| AC2 | ✅ PASS | Valid submission returns `submissionId` and `status="ACCEPTED"` |
| AC3 | ✅ PASS | Duplicate submission returns `status="DUPLICATE"` with same `submissionId` |
| AC4 | ✅ PASS | Counters updated only for accepted submission |

---

## Defects

None.

---

## Out-of-Scope Requests

None.

---

## Automation Opportunities

None identified during this UAT.
