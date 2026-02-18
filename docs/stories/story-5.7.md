# Story 5.7: Company Settings Hub — Foundation

**Epic:** Epic 5 - Form Builder Readiness + Review & Publishing  
**Domain:** Company Settings, Dashboard, Billing, Assets  
**Status:** In Progress
**Priority:** High (foundation for invoicing, governance, future settings)  
**Created:** 2026-02-17  
**Owner:** Developer Agent  
**PM Decisions:** `docs/data-domains/CompanySettings/research/STORY-5.7-PM-DECISIONS.md`  
**Context:** `docs/stories/story-context-5.7.xml`  
**UAT Guide:** `docs/stories/STORY-5.7-UAT-TEST-GUIDE.md`  

---

## 📖 User Story

**As a** Company Admin,  
**I want** a central Company Settings area where I can manage company details (for invoicing), form approval workflow, and company assets (images, terms, documents, video),  
**So that** I have one place to configure properties and defaults that the platform uses across forms, billing, and governance — and future settings can extend this foundation.

**Context & entry point:**  
- Stories 5.1–5.6 complete. Company Admins today have no UI to set RequirePublishApproval, test thresholds, or company invoicing details.  
- Company model has ABN, CustomDisplayName, DisplayNameSource; CompanyBillingDetails has billing address; CompanyFormTestConfig has form workflow settings.  
- Asset model supports images (Story 5.1); ref.AssetType extended for IMAGE, TERMS, DOCUMENT, VIDEO.  
- **Onboarding:** Company setup removed from onboarding; placeholder company "Your Company" at signup. Company Details in Settings. (Onboarding refactor = follow-on story.)  
- PRD: Company Admin can "Manage company details (name, billing address, ABN, contact info)" and "Company settings page". Invoice details require Company name (display name), billing address.

---

## 🧭 Scope Boundary

### In scope (Story 5.7)

- **Company Settings Hub (navigation)**
  - Route: `/dashboard/companies/:companyId/settings`.
  - **Form Approval Workflow** (renamed). Layout: two levels, Form Branding style (sidebar nav, sectioned content).
  - Entry points: **cog icon** on company header and **Profile dropdown** "Company Settings" (links to active company; **hide if user is not admin** for that company).
  - **Mobile (<768px):** Hamburger + slide-over nav; horizontal tabs as fallback if scope tight.
  - Sections: Company Details | Form Approval Workflow | Form Branding | Assets (Images | Terms | Documents | Video).
  - Company Admin only; Company User: read-only or no access.
- **Company Details page**
  - Edit: **Display name** (platform-wide), Legal entity name, ABN, contact (phone, email).
  - **ABR search (AU):** "Search Australian Business Register" button → modal with SmartCompanySearch → on selection, close and populate form. Include "Enter manually" in modal and on form.
  - Support non-AU and individuals (manual entry, placeholder company).
  - Edit: Billing details (CompanyBillingDetails).
  - Gate: Require company details before billing (even "no company").
- **Form Approval Workflow page**
  - Settings from `CompanyFormTestConfig`: Demo test threshold, Require publish approval.
  - API: GET/PUT `/api/forms/company-test-config`.
  - **Help:** Page description in header; second-level menu descriptions; help buttons beside properties (Form Builder pattern).
- **Assets page**
  - **Images:** Grid/list toggle, drag-and-drop + file picker, delete confirmation, display name in properties panel, audit trail, **forms using image** (search DefinitionJSON for assetId/assetKey) with form status. **Image swap:** Replace image A with B across forms — allow when dimensions or aspect ratio match; block if aspect ratio differs; warn if PNG→JPG (transparency loss).
  - **Terms:** Separate section. PDF + URL; URL validation; inline fallback to new page if iframe fails; production simulation.
  - **Documents, Video:** Infrastructure (asset types in place).
  - **Terms auto-mapping:** When company Terms asset defined, Form Builder Terms component auto-uses it.
- **Platform defaults:** Option to turn off platform images; Platform Terms = form per country, force read/accept before company terms.
- **Save/feedback:** Same pattern as Form Branding (explicit Save, version history, unsaved-changes warning). Success: `useToastNotifications` (consistent platform-wide).
- **Empty states:** Explain benefits; allow user to use or not.

### Out of scope (Story 5.7)

- Stripe/payment integration (Epic 6).
- Onboarding refactor (remove Company from Step 2) — separate story; PM decision documented.
- Global Defaults screen (System Admin) — backlog.

---

## 🎯 Done Criteria

- [ ] **DC1:** Company Settings hub with navigation. Entry points: cog + Profile dropdown (active company; hide if not admin). Mobile: hamburger + slide-over (<768px).
- [ ] **DC2:** Company Details: display name, legal name, ABN, billing; ABR popup (AU); "Enter manually" in modal and form; non-AU/individuals.
- [ ] **DC3:** Form Approval Workflow: test threshold, Require publish approval. Help text per PM decisions.
- [ ] **DC4:** Assets: Images (grid/list, DnD+picker, delete confirm, display name, audit trail, forms usage, image swap); Terms (separate, PDF+URL, validation, simulation); asset types IMAGE, TERMS, DOCUMENT, VIDEO.
- [ ] **DC5:** Terms component auto-maps to company Terms when defined.
- [ ] **DC6:** Save/feedback pattern consistent; unsaved-changes warning.
- [ ] **DC7:** UAT guide executed and marked PASSED.
- [ ] **DC8:** Story PR merged to `master`.

---

## 📐 Data Model Notes

- **Company:** Existing; CustomDisplayName, DisplayNameSource. Display name = primary name platform-wide.
- **CompanyBillingDetails:** Existing; GET/PUT for Company Admin.
- **CompanyFormTestConfig:** Existing; GET/PUT `/api/forms/company-test-config`; add version table for audit.
- **ref.AssetType:** IMAGE, TERMS, DOCUMENT, VIDEO (all four).
- **Asset:** WidthPx/HeightPx nullable for non-image assets (migration).

---

## 📚 References

- **PM decisions:** `docs/data-domains/CompanySettings/research/STORY-5.7-PM-DECISIONS.md`
- **Story context:** `docs/stories/story-context-5.7.xml`
- **UAT guide:** `docs/stories/STORY-5.7-UAT-TEST-GUIDE.md`
- Epic scope: `docs/stories/EPIC-5-STATUS.md`
- PRD: `docs/prd.md`
- Data model: `docs/data-domains/CompanySettings/research/data-model-analysis.md`
- Form Branding: `frontend/src/features/dashboard/pages/FormBrandingDefaultsPage.tsx`

---

*Story 5.7 - Company Settings Hub (Foundation)*  
*Last Updated: 2026-02-17*
