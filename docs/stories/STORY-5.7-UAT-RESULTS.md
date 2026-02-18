# Story 5.7 UAT Results — Company Settings Hub

**Story:** 5.7  
**Epic:** 5 - Form Builder Readiness + Review & Publishing  
**Date:** 2026-02-18  
**Status:** Pending manual UAT  

---

## UAT Evidence Table

| Test ID | Description | Command/Action | Result | Evidence |
|---------|-------------|----------------|--------|----------|
| DC1 | Hub nav; cog + Profile; hide if not admin | Manual | Pending | Navigate via cog and Profile; verify Company Settings hidden when not admin |
| DC2 | Company Details; ABR popup; manual entry | Manual | Pending | AU company: ABR modal; select company; form populates |
| DC3 | Form Approval Workflow; help text | Manual | Pending | Toggles and help icons visible |
| DC4 | Assets Images; grid/list; swap rules | Manual | Pending | Placeholder in place; full DnD/swap deferred |
| DC5 | Terms auto-mapping | Manual | Pending | Terms component assetRef — placeholder |
| DC6 | Save; unsaved warning | Manual | Pending | Save toast; beforeunload when dirty |
| Build/lint | Backend + frontend | pytest; npm run build | TBD | See commands below |

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

### Phase 4: Assets (Infrastructure) ✅
- Migration 043: ref.AssetType TERMS, DOCUMENT, VIDEO; Asset.WidthPx/HeightPx nullable
- Placeholder pages: AssetsImagesPage, AssetsTermsPage, AssetsDocumentsPage, AssetsVideoPage
- Full Images/Terms DnD, swap, forms-using-image — deferred (foundation in place)

### Out of Scope (per story)
- Onboarding refactor (remove Step 2) — separate story
- Full Assets Images/Terms implementation — foundation ready
- Terms component assetRef auto-mapping — placeholder

---

*Complete manual UAT per STORY-5.7-UAT-TEST-GUIDE.md and update results above.*
