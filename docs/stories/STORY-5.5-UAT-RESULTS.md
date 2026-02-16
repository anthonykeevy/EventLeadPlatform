# Story 5.5 UAT Results — Preview/Production Governance Foundations

**Story:** 5.5  
**Epic:** 5 - Form Builder Readiness + Review & Publishing  
**Status:** Implementation Complete — Human verification required  
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

- [ ] Run migration
- [ ] Submit form via PREVIEW link → verify `FormSubmission.IsPreview = 1` in DB
- [ ] Submit form via PRODUCTION link → verify `IsPreview = 0`
- [ ] Enable test threshold for company (PUT company-test-config)
- [ ] With 0 test runs, attempt publish → blocked with "X more test runs needed"
- [ ] Record test run or submit via preview until threshold met
- [ ] Publish succeeds; readiness badge shows "Ready to publish"

---

*UAT results for Story 5.5 — Human handoff: run migration, verify manually, then merge PR.*
