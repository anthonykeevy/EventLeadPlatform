# UAT Checklist: T07

**Story:** 3.11  
**Task:** Validation Telemetry - Events + Storage + Resolved vs Abandoned  
**Generated:** 2026-02-05

---

## Pre-conditions

- [ ] Backend server is running
- [ ] Frontend is running
- [ ] A public form link exists with at least one required field
- [ ] DB access available for querying `log.FrontendEvent` and `dbo.FormSubmission`

## Test Steps

### AC1: Emit `validation_failed_submit` when submit is blocked by validation

- [ ] Step 1: Open the public form and click Submit with a required field empty  
  → Verify: Validation UI appears and a `POST /api/public/forms/{token}/telemetry/validation` request is sent.
- [ ] Step 2: Repeat with another invalid field (e.g., email pattern)  
  → Verify: A telemetry request is sent again for the blocked submit attempt.

### AC2: Telemetry includes rule/component identity + value diagnostics (no raw values)

- [ ] Step 1: Query `log.FrontendEvent` for the latest `validation_failed_submit` event  
  → Verify: Payload contains `componentId`, `componentType`, `ruleType`, `ruleCode`, `errorCategory`, and `valueDiagnostics`.
- [ ] Step 2: Inspect `valueDiagnostics`  
  → Verify: It contains only type/length/shape info (no raw field values).

### AC3: Telemetry stored in queryable backend table

- [ ] Step 1: Run  
  `SELECT TOP 5 * FROM log.FrontendEvent WHERE EventType = 'validation_failed_submit' ORDER BY CreatedDate DESC;`  
  → Verify: A row exists for each blocked submit attempt with `SessionID` populated.

### AC4: Resolved vs abandoned correlation via `clientSessionId`

- [ ] Step 1: Submit a valid response after a failed validation attempt  
  → Verify: A new row appears in `dbo.FormSubmission`.
- [ ] Step 2: Compare `log.FrontendEvent.SessionID` to `FormSubmission.ContextJSON.clientSessionId`  
  → Verify: They match, enabling correlation of resolved vs abandoned sessions.

## Regression Check

- [ ] Successful submission still works when validation passes
- [ ] No new console errors in the browser
- [ ] No new backend errors in logs

## Post-conditions

- [ ] Validation telemetry rows present only for blocked submit attempts

## Edge Cases (if applicable)

- [ ] Required checkbox/terms unchecked → telemetry recorded with `errorCategory=required`
- [ ] Pattern rule (email/phone) invalid → telemetry recorded with `errorCategory=pattern`

---

**Instructions for Human Tester:**
1. Execute each step in order  
2. Mark ✅ or ❌ for each item  
3. Add notes for any failures  
4. When complete, run `@ralf-uat *record-uat` with your results
