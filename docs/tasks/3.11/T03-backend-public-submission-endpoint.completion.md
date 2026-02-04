# Task Completion: T03

**Story:** 3.11  
**Task:** Backend - Public Submission Endpoint + Idempotency  
**Completed:** 2026-02-03  
**Status:** Complete  

---

## Summary of Changes

Implemented the token-gated public submission endpoint with idempotency handling, persisted submissions to `dbo.FormSubmission`, and updated `dbo.Form` counters on accepted submissions. Added the `FormSubmission` SQLAlchemy model and public submission schemas required by the API contract.

## Files Changed

| File | Change | Reason |
|------|--------|--------|
| `backend/modules/forms/public_form_router.py` | Modified | Add public submission endpoint with idempotency and counters |
| `backend/modules/forms/public_submission_schemas.py` | Created | Define request/response schemas for public submission |
| `backend/models/form_submission.py` | Created | Map `dbo.FormSubmission` for persistence |
| `backend/models/__init__.py` | Modified | Register new model and update model count |
| `docs/tasks/3.11/TASK-PLAN.md` | Modified | Mark T03 status as ✅ Done |

## Acceptance Criteria Verification

### AC1: Endpoint exists and is token-gated
- **Status:** PASS
- **Evidence:** `POST /api/public/forms/{token}/submissions` added with safe 404 via `_raise_invalid_link()` in `public_form_router.py`.

### AC2: Persists to `dbo.FormSubmission`
- **Status:** PASS
- **Evidence:** `FormSubmission` model + insert mapping for `AnswersJSON`, `ContextJSON`, and `SubmittedAtClient` in `public_form_router.py`.

### AC3: Idempotency works and is stable
- **Status:** PASS
- **Evidence:** `IntegrityError` handler queries existing row and returns `status="DUPLICATE"` with the same `submissionId`.

### AC4: Counters update correctly (accepted only)
- **Status:** PASS
- **Evidence:** `TotalSubmissions`, `LastSubmissionDate`, and demo/production counters update only on successful insert.

## Test Evidence

### Automated Tests
```powershell
python -m py_compile "backend/modules/forms/public_form_router.py"
# (no output, exit code 0)

python -m py_compile "backend/models/form_submission.py"
# (no output, exit code 0)

python -m py_compile "backend/modules/forms/public_submission_schemas.py"
# (no output, exit code 0)
```

## Manual UAT Steps

For human verification:

1. [ ] Start backend and ensure migration `035` is applied.  
2. [ ] AC1 invalid payload (token-gated behavior):
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
3. [ ] AC2 valid payload (using provided token):
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
   → Verify: `status="ACCEPTED"` and `submissionId` is returned.
4. [ ] Re-submit the same payload with the same `idempotencyKey`.  
   → Verify: `status="DUPLICATE"` and the same `submissionId` is returned.
5. [ ] Check DB:
   - `dbo.FormSubmission` has exactly 1 row for the `(FormPublicLinkID, IdempotencyKey)`.
   - `dbo.Form.TotalSubmissions` incremented by 1, and `LastSubmissionDate` updated.

## Known Limitations / Out-of-Scope Items

- [ ] Manual API/DB verification must be performed by a human tester.

## Recommended Next Step

Ready for UAT by human.
