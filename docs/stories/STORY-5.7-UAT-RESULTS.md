# Story 5.7 UAT Results — Company Settings Hub

**Story:** 5.7  
**Epic:** 5 - Form Builder Readiness + Review & Publishing  
**Date:** 2026-02-18  
**Status:** ✅ UAT Passed  

---

## UAT Evidence Table

| Test ID | Description | Command/Action | Result | Evidence |
|---------|-------------|----------------|--------|----------|
| DC1 | Hub nav; cog + Profile; hide if not admin | Manual | ✅ Pass | Navigate via cog and Profile; Company Settings hidden when not admin |
| DC2 | Company Details; ABR popup; manual entry | Manual | ✅ Pass | AU company: ABR modal; select company; form populates |
| DC3 | Form Approval Workflow; help text | Manual | ✅ Pass | Toggles and help icons visible |
| DC4 | Assets Images; grid/list; swap rules | Manual | ✅ Pass | Grid/list, DnD, swap, forms usage |
| DC5 | Terms auto-mapping | Manual | ✅ Pass | Terms component uses company Terms when defined; "We will use your company terms" in builder |
| DC6 | Save; unsaved warning | Manual | ✅ Pass | Save toast; beforeunload when dirty |
| Build/lint | Backend + frontend | pytest; npm run build | ✅ Pass | Build and tests successful |

---

## Build Verification Commands

**Backend (pytest):**
```powershell
cd backend ; python -m pytest -x -q 2>&1 | Select-Object -First 50
```

**Frontend (build):**
```powershell
cd frontend ; npm run build
```

**Migration (human runs):**
```powershell
cd backend ; alembic upgrade head
```
Migration file: `backend/migrations/versions/043_story_57_asset_types_width_height_nullable.py`

---

## Implementation Summary

### Phase 1: Hub + Navigation ✅
- CompanySettingsLayout: Company Details | Form Approval Workflow | Form Branding | Assets (Images | Terms | Documents | Video)
- Mobile: Hamburger + slide-over nav (<768px)
- UserMenu: "Company Settings" link when admin for active company; hidden when not admin
- Entry points: cog on company header; Profile dropdown

### Phase 2: Company Details ✅
- Company Details page with display name, legal name, ABN, billing
- ABR popup: "Search Australian Business Register" button → modal with SmartCompanySearch
- "Enter manually" in modal and on form (link to close modal)
- Backend: GET/PUT `/api/companies/{id}/details` for Company + CompanyBillingDetails
- Unsaved changes: beforeunload warning

### Phase 3: Form Approval Workflow ✅
- Form Approval Workflow page with test threshold and Require publish approval
- Uses existing GET/PUT `/api/forms/company-test-config`
- Help text and help icons per PM decisions

### Phase 4: Assets ✅
- Migration 043: ref.AssetType TERMS, DOCUMENT, VIDEO; Asset.WidthPx/HeightPx nullable
- AssetsImagesPage, AssetsTermsPage, AssetsDocumentsPage, AssetsVideoPage
- Images: grid/list, DnD, file picker, swap (same dims/ratio allow; different ratio block)
- Terms: PDF upload, URL add, validation, pop-up vs new-tab, default asset selection
- Forms-using-image search; Terms component shows "We will use your company terms" when company has terms

### Out of Scope (per story)
- Onboarding refactor (remove Step 2) — separate story

---

*UAT completed 2026-02-18 — all criteria PASSED. See STORY-5.7-RETROSPECTIVE.md for lessons learned.*
