# UAT Checklist: T08

**Story:** 3.11  
**Task:** Client Context - Compatibility + Device/Browser Signals  
**Generated:** 2026-02-05

---

## Pre-conditions

- [ ] Backend server is running
- [ ] Frontend is running
- [ ] A public form link exists with at least one required field
- [ ] DB access available for querying `dbo.FormSubmission`

## Test Steps

### AC1: Compatibility signals captured on successful submission

- [ ] Step 1: Submit a valid public form response  
  → Verify: `FormSubmission.ContextJSON` includes core context plus compatibility fields when supported (e.g., `clientOnlineAtSubmit`, `effectiveConnectionType`, `maxTouchPoints`, `prefersReducedMotion`, `hardwareConcurrency`, `supportsIndexedDB`, `storageQuotaMb`, `appVersion`).
- [ ] Step 2: Verify unsupported fields are absent (no nulls/empties stored)  
  → Verify: Fields are omitted when the browser does not provide them.

### AC2: Outbox stores the same context when offline

- [ ] Step 1: Simulate offline mode, submit a valid response  
  → Verify: Public outbox item in IndexedDB includes the same context fields in `request.context`.
- [ ] Step 2: Return online and allow upload  
  → Verify: Submission succeeds and context fields are preserved in `FormSubmission.ContextJSON`.

### AC3: Server-derived country code captured when available

- [ ] Step 1: Submit a request where `CF-IPCountry` header is present (e.g., via reverse proxy)  
  → Verify: `FormSubmission.ContextJSON.ipCountryCode` exists and is a 2-letter code.

## Regression Check

- [ ] Submissions still succeed online
- [ ] Offline submissions still queue and sync
- [ ] No new console errors in the browser
- [ ] No new backend errors in logs

## Post-conditions

- [ ] Context payload remains privacy-safe (no raw IP values stored)

---

**Instructions for Human Tester:**
1. Execute each step in order  
2. Mark ✅ or ❌ for each item  
3. Add notes for any failures  
4. When complete, run `@ralf-uat *record-uat` with your results
