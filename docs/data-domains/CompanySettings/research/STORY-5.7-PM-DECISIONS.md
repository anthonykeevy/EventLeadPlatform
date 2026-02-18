# Story 5.7 — PM Decisions (Post Sally UX Review)

**For:** Dev team, UX, Story implementation  
**From:** Product Manager  
**Story:** 5.7 Company Settings Hub — Foundation  
**Created:** 2026-02-17  
**Status:** Resolved — use these decisions during development  

---

## Purpose

This document captures PM decisions made after reviewing Sally's UX guidance. Use it as the source of truth to avoid agents guessing during development.

---

## 1. Asset Types and Infrastructure

| Decision | Detail |
|----------|--------|
| **Asset types** | Build infrastructure for **Images**, **Terms**, **Documents**, and **Video** (all four from the start). |
| **Terms auto-mapping** | When a Terms asset is defined in Company Settings, the Terms component **automatically uses** the company's terms. No manual "Use company terms" choice — it's automatic. |

**Existing:** `TermsPropertiesSection.tsx` — link text, URL, or HTML content. Add `assetRef` support; when company has Terms asset configured, Terms component auto-uses it.

---

## 2. Company Details and Onboarding

| Decision | Detail |
|----------|--------|
| **Remove company from onboarding** | Remove Company setup from the onboarding flow. Onboarding = User details only (Step 1). Create a **placeholder company** at signup. Company details setup happens later when usage develops. |
| **Placeholder company** | Platform creates a minimal company named **"Your Company"** so the data model stays company-based. |
| **Display name vs legal name** | ABR search populates **legal name**. Companies often have different **trading names**. Provide a **Display Name** field (used throughout the platform). DB: `Company.CustomDisplayName`, `DisplayNameSource` (Legal, Business, Custom, User) — already exist. |
| **Non-AU and individuals** | Support companies outside Australia and individuals (no registered company). Placeholder company + manual entry. ABR search only for AU. |
| **ABR search in popup** | **Popup/modal.** Add "Search Australian Business Register" button; on click, open modal with SmartCompanySearch; on selection, close and populate form. Include "Enter manually" in modal and on form. |
| **Billing gate** | Before enabling billing, require company details to be updated — even if "no company" (individual). |

**Existing:** `OnboardingStep2.tsx` — Company Setup with ABR search (AU only), manual entry toggle. Story 5.7: refactor onboarding to remove Step 2; move company setup to Company Settings.

---

## 3. Form Workflow (Renamed)

| Decision | Detail |
|----------|--------|
| **Name** | Rename "Form Workflow" → **Form Approval Workflow**. |
| **Layout** | Two levels. Use Form Branding page layout as reference (sidebar nav, sectioned content). |
| **Entry points** | Both: (a) **cog icon** on company header, (b) **Profile dropdown** — add "Company Settings" alongside Theme Settings, Account Settings. |
| **Mobile/responsive** | **Hamburger + slide-over** for mobile (<768px); keep sidebar for tablet and desktop. Horizontal tabs as fallback if scope is tight. |

**Existing:** `CompanyContainer.tsx` — Settings cog for admins; `UserMenu.tsx` — Theme Settings, Account Settings.

**Profile dropdown behaviour:** Link goes to **whatever the active company is** when the user is on the dashboard. **If the user is not an admin for that active company, the "Company Settings" menu item does not display** (hide it).

---

## 4. Help and Descriptions

| Decision | Detail |
|----------|--------|
| **Page header** | Every page has a **description in the header** explaining the menu overall and how it will help users. |
| **Second-level menu** | Each second-level menu item has a short description. |
| **Property help** | Help buttons next to properties (same pattern as Form Builder Global and Component Properties). |
| **Standard pattern** | Ensure a **common approach** across the platform for help and information. |

**Existing:** `GlobalStylesPanel.tsx` — `helpText` on `PropertySelect`, `PropertyTextInput`, etc.; sections like "Help & Validation", "Default Object Layout" with `helpText="Default object layout for components..."`. Reuse this pattern.

---

## 5. Assets — Images

| Decision | Detail |
|----------|--------|
| **View toggle** | Button to switch between **grid** and **list** view. |
| **Upload** | Both **drag-and-drop** and **file picker**. |
| **Delete** | **Confirmation modal** before delete. |
| **Display name** | User selects image → **properties panel** appears showing metadata. User can set an **alternative/display name**. |
| **Audit trail** | Show audit trail (where image came from, upload timestamp, etc.). **No full AssetVersion table** — we don't edit images, so basic CreatedDate/CreatedBy is sufficient. |
| **Forms using image** | Show a list of **forms** the image is used on, with **form status** (Draft, Published, etc.). **Yes — search the database** for the unique asset reference in every form (DefinitionJSON in FormVersion; search for assetId/assetKey). |
| **Image swap** | Use case: company changes logo and wants to update it on all forms. Support **swap/replace** image A with image B across all forms. **Rules:** Allow when dimensions **or** aspect ratio match. If aspect ratio differs: **block** with message "Use an image with the same dimensions (or aspect ratio) to avoid layout changes." If swapping PNG→JPG (transparency loss): show warning; allow. |

---

## 6. Assets — Terms (Separate Section)

| Decision | Detail |
|----------|--------|
| **Separate from Images** | Yes — separate section/sub-tab. |
| **Formats** | Support **PDF upload** and **URL**. Validate URL server-side; inform customer if validation passed. |
| **URL caveat** | If URL is not under our control (external), warn: "Works when tested but may stop working later if their company changes policy." |
| **Inline fallback** | If inline (iframe) does not work, **automatically switch to new page** for display. |
| **Production simulation** | Provide a simulation showing exactly how the **production form** will display Terms to the customer. |

---

## 7. Platform Defaults

| Decision | Detail |
|----------|--------|
| **Platform images** | Option to **turn off** platform-provided default images from displaying (company can hide them in picker). |
| **Platform Terms** | Default Terms per country. Companies must **read and accept** platform Terms before they can enable their own company Terms. Force read/accept flow first. |
| **Platform Terms format** | **Create a form on our own platform** for the Terms for each country. This allows us to prepare it to be formatted perfectly (using Form Builder / form definition for layout control, rather than external PDFs or generic HTML). |

---

## 8. Save, Feedback, and Consistency

| Decision | Detail |
|----------|--------|
| **Save pattern** | Same as Form Branding: explicit Save, version history, audit. Apply to Company Details, Form Approval Workflow, Assets. |
| **Unsaved changes** | Yes — warning when navigating away with unsaved changes. |
| **Success feedback** | Must be **consistent** across the platform. Review how success feedback is done elsewhere and use the same. |

**Existing:** `useToastNotifications()` from `features/ux` — `toast.success(message, title)`, `toast.error(message, title)`. Used in FormBrandingDefaultsPage, FormReviewPage, EditFormModal, DashboardLayout. Form Branding: `toast.success('Form branding defaults saved', 'Success')`. Use this pattern.

---

## 9. Empty States and Value Communication

| Decision | Detail |
|----------|--------|
| **Explain benefits** | Make it clear what the **benefits** are to the user; allow them to use or not use features. |
| **Billing gate** | Before billing: insist they update company details (even if "no company"). |

---

## 10. Onboarding Integration

| Decision | Detail |
|----------|--------|
| **Reuse existing onboarding** | Review the current onboarding process and **include previous work**. |
| **Current flow** | Step 1: User details (name, phone, country). Step 2: Company setup (ABR search for AU, manual for others, billing address). Creates company via `/api/companies` (onboarding). |
| **New flow** | Step 1: User details only. Create placeholder company. Step 2 removed. Company Details moved to Company Settings. |

**Reference:** `frontend/src/features/onboarding/`, `DashboardLayout.tsx` (OnboardingModal, handleOnboardingComplete).

---

## Remaining Questions (Resolved)

| # | Question | PM Decision |
|---|----------|-------------|
| 3 | Placeholder company naming | **"Your Company"** |
| 4 | Company Settings in Profile dropdown | Link goes to **active company** on dashboard. **Hide menu item** if user is not admin for that company. |
| 5 | Terms component assetRef | **Automatically** use company Terms when defined — no manual choice. |
| 6 | Platform Terms per country | **Create a form on our platform** for each country's Terms (Form Builder); allows perfect formatting. |
| 7 | Audit trail / AssetVersion | **No full AssetVersion** — can't edit images. Basic CreatedDate/CreatedBy. Add **image swap** use case: replace image A with B across all forms (same dimensions, or document alignment rules). |
| 8 | Forms using image | **Yes — search DB** for unique asset reference in every form. DefinitionJSON in FormVersion contains assetId/assetKey; search across FormVersion.DefinitionJSON. |

**Implementation note (Forms using image):** DefinitionJSON stores `asset: { assetId, assetKey, ... }` in page backgrounds (and possibly future component refs). Use SQL Server JSON functions (e.g. `LIKE '%"assetId":123%'` or `JSON_VALUE`) or parse in app layer. Consider Form + FormVersion (active version) join to get forms where asset appears; include Form status (Draft/Published) from FormVersion.Status.

## Resolved (Final PM Decisions)

| # | Question | PM Decision |
|---|----------|-------------|
| **Mobile/responsive** | Company Settings on mobile | Hamburger + slide-over for mobile (<768px); sidebar for tablet and desktop. Horizontal tabs as fallback if scope is tight. |
| **ABR search** | Popup vs inline | Popup. "Search Australian Business Register" button → modal with SmartCompanySearch → on selection, close and populate form. "Enter manually" in modal and on form. |
| **Image swap alignment** | Rules for safe swap | Allow when dimensions or aspect ratio match. Block if aspect ratio differs (show message). Warn if PNG→JPG (transparency loss); allow. |

---

## References

- **Consultation feedback:** `docs/data-domains/CompanySettings/research/STORY-5.7-CONSULTATION-FEEDBACK.md` (UX/BA input; PM decisions above)
- Story: `docs/stories/story-5.7.md`
- UX request: `docs/data-domains/CompanySettings/research/STORY-5.7-UX-GUIDANCE-REQUEST.md`
- Onboarding: `frontend/src/features/onboarding/`, `OnboardingStep2.tsx`
- Form Branding: `frontend/src/features/dashboard/pages/FormBrandingDefaultsPage.tsx`
- Company model: `backend/models/company.py` (CustomDisplayName, DisplayNameSource)
- Toast: `frontend/src/features/ux/components/ToastProvider.tsx` (`useToastNotifications`)

---

*PM decisions — use as source of truth for Story 5.7 implementation*
