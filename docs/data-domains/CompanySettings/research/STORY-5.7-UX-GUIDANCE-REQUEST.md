# Story 5.7 — UX Guidance Request

**For:** @ux-expert (Sally)  
**From:** Product Manager / Dev Team  
**Story:** 5.7 Company Settings Hub — Foundation  
**Created:** 2026-02-17  
**PM Decisions (Resolved):** `STORY-5.7-PM-DECISIONS.md` — use for implementation; many questions below are now resolved.

---

## Purpose

We are implementing Story 5.7: a central **Company Settings** area for Company Admins. We requested UX guidance on layout, interaction patterns, and edge cases. **PM has resolved most questions**; see STORY-5.7-PM-DECISIONS.md. This document retains the original questions for context; remaining open items are in the PM decisions doc.

---

## Story Summary

**User story:** As a Company Admin, I want a central Company Settings area where I can manage company details (for invoicing), form workflow thresholds, and company assets (images and Terms of Agreement), so that I have one place to configure properties and defaults.

**Screens / areas:**

1. **Company Settings Hub** — New route (e.g. `/settings` or `/company/settings`) with tabbed or sectioned navigation.
2. **Company Details** — Edit company name, ABN, contact (phone, email); billing address (BillingContactName, BillingEmail, BillingAddressLine1/2, City, State, PostalCode, Country). Validation: ABN 11 digits (Australian).
3. **Form Workflow** — Toggle and values: Demo test threshold (enabled, runs 0–100), Require publish approval. Help text for each setting.
4. **Form Branding** — Existing page (FormBrandingDefaultsPage); will be surfaced as a tab/section in the hub.
5. **Assets** — Two sub-sections:
   - **Images:** List, upload, delete, set display name.
   - **Terms of Agreement:** Upload PDF, list, delete. Used for consent checkboxes in forms (future story).

**Audience:** Company Admin only. Company User: no access or read-only.

---

## Existing Patterns

- **Form Branding** page exists at FormBrandingDefaultsPage — has version history, change summary, save flow. Can serve as a pattern for layout and save behaviour.
- **Asset picker** (Story 5.1) — used in Form Builder for background images; we need a management view (list, upload, delete) in addition to picker.
- **Dashboard** — Company Settings will likely live under Dashboard or a profile/company menu.

---

## UX Questions for Guidance

### 1. Hub structure and navigation

- Tabbed layout (Company Details | Form Workflow | Form Branding | Assets) vs sidebar/card navigation?
- How many levels of hierarchy? (e.g. Assets → Images | Terms as sub-tabs?)
- Entry point: Dashboard link, profile dropdown, or both?
- Mobile / responsive: tabs vs accordion vs stacked cards?

### 2. Company Details

- Single long form vs sections (Company info | Billing)?
- Inline validation for ABN (11 digits) — when to show error (on blur, on submit)?
- Required-field indication and error states for invoicing readiness.
- Any progressive disclosure (e.g. "Advanced" for optional fields)?

### 3. Form Workflow

- Simple form with toggles + number input; help text placement (tooltip, inline, help panel)?
- Should "Require publish approval" have a short explainer for Company Admins who may not know the workflow?

### 4. Assets — Images

- Grid vs list view for images?
- Upload: drag-and-drop zone, or file picker, or both?
- Delete: confirmation modal vs inline undo?
- Display name: inline edit or modal?

### 5. Assets — Terms of Agreement

- Separate section from Images, or combined list with type filter?
- Upload: PDF only; any size/limit messaging?
- When customer provides **Terms URL** (external link) vs **uploaded document** — same UI or different flows? (We support both; URL can be validated for iframe embeddability.)
- Display of Terms in "View terms" — embed in modal when possible, new tab fallback; any UX preference?

### 6. Platform default assets

- **Default images:** A few platform-provided images for new customers. How to present in picker? ("Platform images" vs "Your images" sections?)
- **Default Terms:** Platform Terms that companies can use; requires acceptance before use. Flow: show Terms + "I have read and agree to use these" checkbox. Where does this live — Assets tab, or separate onboarding/acceptance step?

### 7. Save / audit behaviour

- Form Branding uses explicit Save; version history visible. Apply same pattern to Company Details and Form Workflow?
- Unsaved changes warning when navigating away?
- Success feedback: toast, inline message, or both?

### 8. Empty and loading states

- New company: empty Assets, default Form Workflow values. Any onboarding hints?
- Loading: skeleton vs spinner for each section?
- Error states: validation errors vs API errors — consistent messaging pattern?

---

## Technical Constraints (for reference)

- Backend: Company, CompanyBillingDetails, CompanyFormTestConfig, Asset; version tables for audit.
- Terms: PDF only for MVP; support URL or uploaded asset; URL embeddability validated server-side.
- Form Branding already has version history UI — can reuse pattern.
- Company Admin only; RBAC already in place.

---

## References

- Story: `docs/stories/story-5.7.md`
- Data model: `docs/data-domains/CompanySettings/research/data-model-analysis.md`
- Document display: `docs/data-domains/CompanySettings/research/document-display-and-platform-defaults.md`
- Asset review: `docs/data-domains/CompanySettings/research/asset-management-platform-review.md`
- Existing: `frontend/src/features/dashboard/pages/FormBrandingDefaultsPage.tsx`

---

## How to Use This With UX Expert

Start a new chat and include:

```
@ux-expert 

Please provide UX guidance for Story 5.7 Company Settings Hub. I've attached the UX Guidance Request document that summarizes the screens, user flows, and specific questions we need help with.

[Attach or paste: docs/data-domains/CompanySettings/research/STORY-5.7-UX-GUIDANCE-REQUEST.md]
```

Or run the *create-design* workflow (if available) with this document as context.

---

*Request prepared for UX Expert review*
