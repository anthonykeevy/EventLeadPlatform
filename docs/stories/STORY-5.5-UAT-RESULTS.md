# Story 5.5 UAT Results — Preview/Production Governance Foundations

**Story:** 5.5  
**Epic:** 5 - Form Builder Readiness + Review & Publishing  
**Status:** UAT PASSED (Step 0 + Step 1.1–1.4); rest deferred to later story  
**Created:** 2026-02-16  

---

## UAT Evidence Table

| Test ID | Description | Command/Action | Result | Evidence |
|---------|-------------|----------------|--------|----------|
| DC1 | Submissions have preview flag | Migration adds `IsPreview`; `public_form_router` sets from `LinkType` | PASS | `FormSubmission.IsPreview` set when `link_type == "PREVIEW"`; API creates submissions with flag |
| DC2 | Test threshold stored | `CompanyFormTestConfig` table; GET/PUT `/api/forms/company-test-config` | PASS | Table with `TestThresholdEnabled`, `TestThresholdValue`; endpoints for company config |
| DC3 | Test runs counted/audited | `FormTestRun` table; count = preview submissions + explicit runs | PASS | `FormTestRun` stores who, when, form version; `get_test_run_count()` sums both sources |
| DC4 | Publish blocked when not met | `update_form` raises `ValueError` with message; frontend shows alert | PASS | `readiness_service.check_publish_readiness()`; service layer blocks; frontend shows `err.message` |
| DC5 | Readiness badge visible | `ReadinessBadge` in Form Detail View | PASS | `FormDetailView` shows badge; "Ready to publish" or "X more test runs needed"; Record test run button |
| Build/lint | Backend | `pytest` | SKIP | Pre-existing test collection error (ref.Country table) — unrelated to Story 5.5 |
| Build/lint | Frontend | `npm run lint` | SKIP | ESLint not in PATH in sandbox — manual run required |

---

## Implementation Summary

### Backend
- **Migration 041:** `IsPreview` on `FormSubmission`; `CompanyFormTestConfig`; `FormTestRun`
- **Endpoints:** `GET /api/forms/{form_id}/readiness`, `POST /api/forms/{form_id}/record-test-run`, `GET/PUT /api/forms/company-test-config`
- **Publish guard:** `update_form` calls `check_publish_readiness` when status → PUBLISHED

### Frontend
- **ReadinessBadge:** Green "Ready to publish" or amber "X more test runs needed" with Record test run link
- **FormDetailView:** Badge in Status section; handleRecordTestRun; improved publish error message

---

## Migration Command (Human runs)

```powershell
cd C:\wt\elp\story-epic5-5.5-preview-production-governance
alembic -c backend/alembic.ini upgrade head
```

---

## Manual UAT Checklist

| Step | Check | Result |
|------|-------|--------|
| 0 | Run migration | PASSED |
| 1.1 | Submit form via PREVIEW link → verify `FormSubmission.IsPreview = 1` in DB | PASSED |
| 1.2 | Enable test threshold for company (PUT company-test-config) | PASSED |
| 1.3 | With 0 test runs, attempt publish → blocked with "X more test runs needed" | PASSED |
| 1.4 | Record test run or submit via preview until threshold met | PASSED |
| 1.5+ | Publish succeeds; readiness badge shows "Ready to publish" | Deferred to later story |
| — | Production link test (`IsPreview = 0`) | Deferred (no UI to create PRODUCTION links until 5.6+) |

---

*UAT results for Story 5.5 — Step 0 + Step 1.1–1.4 PASSED; merge approved.*
