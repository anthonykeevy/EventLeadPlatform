# Story 5.7 Retrospective — Company Settings Hub

**Story:** 5.7 Company Settings Hub — Foundation  
**Epic:** 5 - Form Builder Readiness + Review & Publishing  
**Date:** 2026-02-18  
**Status:** UAT Passed  
**Facilitator:** Scrum Master (Retrospective)  

---

## 1. Summary

Story 5.7 delivered a central **Company Settings Hub** for Company Admins with:

- **Navigation & entry points:** Cog icon, Profile dropdown (hidden when not admin), mobile hamburger + slide-over
- **Company Details:** Display name, legal name, ABN, billing; ABR search popup (AU); manual entry
- **Form Approval Workflow:** Test threshold, Require publish approval; help text
- **Assets:** Images (grid/list, DnD, swap, forms usage); Terms (PDF, URL, validation, default selection)
- **Terms auto-mapping:** Form Builder Terms component shows "We will use your company terms" when company has Terms configured
- **Save pattern:** Explicit Save, version history, unsaved-changes warning

All UAT criteria passed.

---

## 2. What Went Well

| Area | Observation |
|------|-------------|
| **PM decisions upfront** | STORY-5.7-PM-DECISIONS.md and STORY-5.7-CONSULTATION-FEEDBACK.md provided clear direction on ABR popup vs inline, image swap rules, mobile layout, and Terms auto-mapping. Reduced ambiguity during implementation. |
| **Reuse of existing patterns** | Form Branding page, useToastNotifications, GlobalStylesPanel help pattern, and asset picker (Story 5.1) were reused. Kept UI and behaviour consistent. |
| **Incremental delivery** | Phased approach (Hub → Company Details → Form Approval Workflow → Assets) allowed validation at each step. |
| **Mobile-first consideration** | Hamburger + slide-over for <768px was specified early; implementation followed UX guidance. |
| **ABR popup UX** | Modal flow with "Enter manually" escape hatch kept Company Details form clean and aligned with PM preference. |
| **Terms infrastructure** | Asset types (IMAGE, TERMS, DOCUMENT, VIDEO), Terms URL validation, and company Terms integration laid a solid foundation for future document categories (backlog). |
| **UAT guide** | STORY-5.7-UAT-TEST-GUIDE.md gave a clear checklist; DC1–DC6 mapped directly to done criteria. |

---

## 3. What Could Improve

| Area | Observation |
|------|-------------|
| **Scope creep risk** | Story combined hub, company details, workflow, and assets. Breaking into smaller stories (e.g. Hub+Details first, Assets as follow-on) might have reduced iteration time. |
| **Terms runtime resolution** | Form Builder UI shows "We will use your company terms" when company has Terms, but runtime (TermsField, public form) must resolve company default Terms. This handoff needed explicit verification. |
| **URL blockers documentation** | TERMS-URL-BLOCKERS-AND-MITIGATIONS.md and validation UX (403/401 messaging) evolved during implementation. Capturing these earlier would have reduced rework. |
| **Migration sequencing** | Multiple migrations (Asset types, DefaultTermsAssetID, TermsDisplayMode) — batching into a single migration for related schema changes could simplify rollout. |
| **Profile dropdown behaviour** | "Hide Company Settings when not admin" required careful RBAC/UI coordination. Documenting the exact rules in the story helped. |

---

## 4. Lessons Learned

| Lesson | Apply to Future Stories |
|--------|-------------------------|
| **PM + UX consultation before dev** | STORY-5.7-CONSULTATION-FEEDBACK.md and PM decisions doc reduced back-and-forth. Use this pattern for multi-faceted UX stories. |
| **Asset type taxonomy upfront** | Defining IMAGE, TERMS, DOCUMENT, VIDEO early avoided mid-story schema surprises. |
| **Terms: URL vs popup vs new tab** | Two-path URL add (pop-up vs new tab) and TermsDisplayMode improved flexibility. Consider similar "mode" options for other document types. |
| **Default asset selection** | Radio buttons for preferred Terms when 2+ assets improved clarity. Reuse for future multi-asset scenarios. |
| **Form Builder ↔ Company Settings** | TermsPropertiesSection needed `companyId` from formContext. Cross-feature data flow (builder ↔ dashboard) should be designed explicitly. |
| **Lint hygiene** | Any files modified during a story must be reviewed and all lint issues (including @typescript-eslint/no-explicit-any) must be resolved before story closure. |

---

## 5. Action Items

| # | Action | Owner | Notes |
|---|--------|-------|------|
| 1 | Document Terms runtime resolution flow (Form Builder → public form) in technical docs | Dev | Ensures assetRef/defaultTermsAssetId resolution is traceable |
| 2 | Consider PDF.js for Terms display (backlog) | PM | Better rotation/controls; see PDF-ROTATION-AND-VIEW-OPTIONS.md |
| 3 | Plan document categories backlog item | PM | Multiple document types + category selection in Terms component |
| 4 | Merge Story 5.7 PR to master | Dev | DC8 remaining |
| 5 | **Process:** Any files modified during a story must be reviewed and all lint issues resolved | Team | Add to story-done checklist; prevents lint debt accumulation |

---

## 6. Metrics

| Metric | Value |
|--------|-------|
| UAT pass rate | 100% (DC1–DC6 + build) |
| Migrations added | 043 (asset types), 046 (TermsDisplayMode), 047 (DefaultTermsAssetID) |
| Key deliverables | CompanySettingsLayout, CompanyDetailsPage, FormApprovalWorkflowPage, AssetsImagesPage, AssetsTermsPage, TermsPropertiesSection update |

---

## 7. References

- Story: `docs/stories/story-5.7.md`
- UAT guide: `docs/stories/STORY-5.7-UAT-TEST-GUIDE.md`
- UAT results: `docs/stories/STORY-5.7-UAT-RESULTS.md`
- PM decisions: `docs/data-domains/CompanySettings/research/STORY-5.7-PM-DECISIONS.md`
- UX consultation: `docs/data-domains/CompanySettings/research/STORY-5.7-CONSULTATION-FEEDBACK.md`

---

*Story 5.7 Retrospective — 2026-02-18*
