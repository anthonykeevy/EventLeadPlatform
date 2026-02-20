# Story 5.7 UAT Test Guide — Company Settings Hub

**Story:** 5.7  
**Epic:** 5 - Form Builder Readiness + Review & Publishing  
**Status:** ✅ UAT Passed (2026-02-18)
**Created:** 2026-02-17  
**PM Decisions:** `docs/data-domains/CompanySettings/research/STORY-5.7-PM-DECISIONS.md`  

---

## Scope (UAT Coverage)

Story 5.7 UAT verifies:

1. **DC1:** Company Settings hub exists with navigation; entry points (cog + Profile dropdown)
2. **DC2:** Company Details page: display name, legal name, ABN, billing; ABR popup (AU); manual entry; non-AU/individuals
3. **DC3:** Form Approval Workflow: test threshold, Require publish approval; help text
4. **DC4:** Assets: Images (grid/list, upload, delete, display name, audit trail, forms usage, image swap); Terms (separate, PDF+URL, validation, simulation)
5. **DC5:** Terms component auto-maps to company Terms when defined
6. **DC6:** Save/feedback pattern; unsaved-changes warning

---

## Pre-conditions

- Stories 5.1, 5.2, 5.5, 5.6 complete
- Backend running with Company, CompanyBillingDetails, CompanyFormTestConfig, Asset APIs
- ref.AssetType: IMAGE, TERMS, DOCUMENT, VIDEO
- Test company with Company Admin user

---

## UAT Steps

### DC1: Company Settings Hub — Navigation & Entry Points

| Step | Action | Expected |
|------|--------|----------|
| 1.1 | Login as Company Admin; select a company on dashboard | Dashboard loads |
| 1.2 | Click cog icon on company header | Navigate to Company Settings |
| 1.3 | Verify nav: Company Details, Form Approval Workflow, Form Branding, Assets | All sections visible |
| 1.4 | Click Profile dropdown | "Company Settings" visible |
| 1.5 | Click "Company Settings" from Profile | Navigate to active company's settings |
| 1.6 | Switch to company where user is NOT admin; open Profile dropdown | "Company Settings" does NOT display |
| 1.7 | Resize to &lt;768px (mobile) | Hamburger menu; slide-over nav; or horizontal tabs |

---

### DC2: Company Details Page

| Step | Action | Expected |
|------|--------|----------|
| 2.1 | Open Company Details section | Form with display name, legal name, ABN, billing fields |
| 2.2 | (AU company) Click "Search Australian Business Register" | Modal opens with SmartCompanySearch |
| 2.3 | Search by ABN; select company | Modal closes; form populated |
| 2.4 | Verify "Enter manually" in modal and on form | Can bypass ABR |
| 2.5 | Edit Display name; save | Success toast; display name used platform-wide |
| 2.6 | (Non-AU or individual) Verify no ABR; manual entry only | Form accepts manual entry |
| 2.7 | Navigate away with unsaved changes | Warning modal |

---

### DC3: Form Approval Workflow Page

| Step | Action | Expected |
|------|--------|----------|
| 3.1 | Open Form Approval Workflow section | Page description in header |
| 3.2 | Verify test threshold toggle and value (0–100) | Editable |
| 3.3 | Verify Require publish approval toggle | Editable |
| 3.4 | Verify help text / help buttons beside properties | Form Builder pattern |
| 3.5 | Change values; save | Success toast; version recorded |

---

### DC4: Assets — Images

| Step | Action | Expected |
|------|--------|----------|
| 4.1 | Open Assets → Images | Grid or list view |
| 4.2 | Toggle grid/list view | View switches |
| 4.3 | Upload via drag-and-drop | Image appears |
| 4.4 | Upload via file picker | Image appears |
| 4.5 | Select image → properties panel | Metadata, display name, audit trail |
| 4.6 | Set display name; save | Updated |
| 4.7 | Verify "Forms using this image" | List of forms + status (Draft/Published) |
| 4.8 | Use image swap: replace with same-dimensions image | Swap succeeds |
| 4.9 | Use image swap: replace with different-aspect-ratio image | Blocked with message |
| 4.10 | Delete image | Confirmation modal; then deleted |

---

### DC4: Assets — Terms

| Step | Action | Expected |
|------|--------|----------|
| 4.11 | Open Assets → Terms (separate from Images) | Terms section |
| 4.12 | Upload PDF | Stored; listed |
| 4.13 | Add Terms URL; validate | URL validated; pass/fail message |
| 4.14 | View production simulation | Mirrors how form displays Terms |
| 4.15 | (If iframe fails) Verify fallback to new page | Opens in new tab |

---

### DC5: Terms Component Auto-mapping

| Step | Action | Expected |
|------|--------|----------|
| 5.1 | Define company Terms asset in Company Settings | Terms asset exists |
| 5.2 | Add Terms component to form in Form Builder | Terms component uses company Terms automatically |

---

### DC6: Save & Feedback

| Step | Action | Expected |
|------|--------|----------|
| 6.1 | Edit any settings section; click Save | Toast: "… saved", "Success" |
| 6.2 | Edit; navigate away without saving | Unsaved-changes warning |
| 6.3 | Verify version history (Company Details, Form Approval Workflow) | Audit trail visible |

---

## Pass Criteria

- [x] All DC1–DC6 manual checks pass
- [x] Mobile (&lt;768px): hamburger + slide-over (or tabs) works
- [x] Profile dropdown hides Company Settings when not admin
- [x] ABR popup flow complete; "Enter manually" available
- [x] Image swap: allow same dims/ratio; block different ratio; warn PNG→JPG
- [x] Forms-using-image search returns correct forms + status

---

## References

- Story: `docs/stories/story-5.7.md`
- PM decisions: `docs/data-domains/CompanySettings/research/STORY-5.7-PM-DECISIONS.md`
- Data model: `docs/data-domains/CompanySettings/research/data-model-analysis.md`

---

*UAT completed 2026-02-18 — all criteria PASSED. See STORY-5.7-UAT-RESULTS.md for evidence.*
