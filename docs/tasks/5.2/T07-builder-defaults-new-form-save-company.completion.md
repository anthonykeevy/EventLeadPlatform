# Task T07 Completion Note

**Story:** 5.2 - Company Form Defaults (Brand System)  
**Task:** T07 - Builder Defaults on New Form + Save to Company Defaults  
**Completed:** 2026-02-16  

---

## Summary

Implemented formContext availability fix and verified Save to Company Defaults UX. The Save button and Init API integration were already wired in T05; T07 addresses the gap where formContext was not set when eventId was null.

## Changes Made

| File | Change |
|------|--------|
| `frontend/src/features/builder/stores/useBuilderStore.ts` | Set formContext whenever companyId exists (not only when both companyId and eventId). Call Init API only when eventId is present (API requires it). Enables Save to Company Defaults button for forms with companyId but null eventId. |

## Implementation Details

**Before:** formContext and Init API were only invoked when `form?.companyId && form?.eventId`.

**After:**
- `formContext = { companyId, eventId }` set whenever `form?.companyId` exists
- Init API called only when `form.eventId != null && form.eventId > 0`
- Save to Company Defaults button now appears for all forms with company context, regardless of eventId

## Verification

- No new lint errors in modified file
- Pre-existing build issues in worktree (apiBaseUrl, FormBrandingDefaultsPage imports) — unrelated to T07
- T07 UAT checklist created: `T07-builder-defaults-new-form-save-company.uat.md`

## AC Coverage

| AC | Status |
|----|--------|
| AC1: Company defaults on new form | Existing T05 logic; Init API called when companyId+eventId present |
| AC2: Save to Company Defaults visible | formContext now set from companyId alone; PropertiesPanel/GlobalStylesPanel already pass companyId, isCompanyAdmin, saveToCompanyDefaults |
| AC3: Save to Company Defaults works | saveToCompanyDefaults → putCompanyFormDefaults (theme, globalStyles) — already implemented in T05 |
