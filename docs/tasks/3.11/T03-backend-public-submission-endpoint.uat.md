# UAT Checklist: T03

**Story:** 3.11  
**Task:** Backend - Public Submission Endpoint + Idempotency  
**Generated:** 2026-02-03  

---

## Pre-conditions

- [ ] Backend server is running.
- [ ] DB migration `035` is applied (`dbo.FormSubmission` exists).
- [ ] You have a valid public form token for PREVIEW or PRODUCTION.

## Test Steps

### AC1: Endpoint exists and is token-gated

- [ ] Step 1: POST an invalid payload to an invalid token  
  ```powershell
  $ac1Body = @{
    idempotencyKey   = 123
    submittedAtClient = "not-a-date"
  } | ConvertTo-Json -Depth 5

  Invoke-RestMethod -Method Post `
    -Uri "http://localhost:8000/api/public/forms/INVALID_TOKEN/submissions" `
    -ContentType "application/json" `
    -Body $ac1Body
  ```
  → Verify: `404` with a safe generic message.

### AC2: Persists to `dbo.FormSubmission`

- [ ] Step 1: POST a valid payload using the provided token  
  ```powershell
  $ac2Body = @{
    idempotencyKey = "test-123"
    submittedAtClient = "2026-02-03T12:00:00Z"
    answersByComponentId = @{
      firstName = "A"
    }
    context = @{
      clientDeviceId = "device-1"
      clientSessionId = "session-1"
      submitAttemptId = "attempt-1"
    }
  } | ConvertTo-Json -Depth 5

  Invoke-RestMethod -Method Post `
    -Uri "http://localhost:8000/api/public/forms/an_sN5Q3ewF9gXxhGS126hoLzZndBQwlHiwuT8zfkrs/submissions" `
    -ContentType "application/json" `
    -Body $ac2Body
  ```
  → Verify: response `status="ACCEPTED"` and a numeric `submissionId`.
- [ ] Step 2: Query `dbo.FormSubmission` by `submissionId`  
  → Verify: `FormID`, `FormVersionID`, `FormPublicLinkID`, `AnswersJSON`, `ContextJSON` are populated.

### AC3: Idempotency works and is stable

- [ ] Step 1: Re-submit the same payload with the same `idempotencyKey`  
  → Verify: response `status="DUPLICATE"` and the same `submissionId`.
- [ ] Step 2: Query `dbo.FormSubmission`  
  → Verify: only one row exists for `(FormPublicLinkID, IdempotencyKey)`.

### AC4: Counters update correctly (accepted only)

- [ ] Step 1: Capture `dbo.Form.TotalSubmissions` before submit.  
  → Verify: value increments by 1 only on `ACCEPTED`.
- [ ] Step 2: Confirm `LastSubmissionDate` updates on `ACCEPTED` and does not change on `DUPLICATE`.

## Regression Check

- [ ] `GET /api/public/forms/{token}` still returns the form definition.
- [ ] No new backend errors appear in logs during submission tests.

## Post-conditions

- [ ] Test submission data is cleaned up if required by the environment.

## Edge Cases (if applicable)

- [ ] Submit with `submittedAtClient` in a local timezone offset (`+10:00`)  
  → Verify: stored `SubmittedAtClient` is normalized to UTC.

---

**Instructions for Human Tester:**
1. Execute each step in order
2. Mark ✅ or ❌ for each item
3. Add notes for any failures
4. When complete, run `@ralf-uat *record-uat` with your results
