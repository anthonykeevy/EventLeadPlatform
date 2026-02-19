# Epic 5 Status - Form Builder Readiness + Review & Publishing

**Epic ID:** Epic 5  
**Status:** ✅ Approved (2026-02-07) · 🔄 In Progress  
**Created:** 2026-02-06  
**Product Manager:** John (PM Agent)  
**Developer:** Developer Agent  

---

## 🎯 Epic 5 Overview

**Objective:** Make the **form builder production-ready** (assets + defaults + schema parity) and then deliver a **governed review/publish workflow** so customers can reliably move a form from **draft → tested (preview) → published (production)** with stable public URLs and safe operational controls.

Epic 5 is driven directly by the PRD sections:
- **4A. Preview & Testing System** (preview/production modes, test thresholds, audit)
- **7. Form Publishing & Hosting** (publish/unpublish, public URL generation, hosting guarantees)
- **Publish Request Flow** (Company User requests publish; Company Admin reviews + publishes)

**Primary UX references:**
- `docs/stories/EPIC-5-UX-IDEATION.md` (screen map + journeys; evolves during Epic 5)
- `docs/stories/UNIFIED-FORM-WORKSPACE-SPECIFICATION.md`  
  (Optional UX improvement concept; implement only minimal subset needed to ship Epic 5.)

---

## 🚦 Direction Change (2026-02-07): Form Builder Readiness First

**Problem:** “Preview/test/publish governance” only creates customer value if the builder is already reliable for real customers. Today, we have **high-risk technical debt** that will force rework and can block real-world publishing:

- **Background images are embedded as base64 Data URLs in the form JSON** (builder reads file → `readAsDataURL` and stores it in the definition).  
  This bloats `FormVersion.DefinitionJSON` (NVARCHAR MAX), makes saves/loads slower, inflates version history, and prevents asset reuse/lifecycle control.
- **Brand defaults are per-form, not per-company.** The builder has a strong `globalStyles` model, but it lives inside each form definition; there is no “set once, inherit everywhere” company-level defaults capability.
- **Backend validation only partially models the builder definition.** `backend/schemas/form_definition.py` is minimal compared to what the builder produces, so we aren’t validating what we’re actually shipping (drift risk).
- **Preview/production parity is not guaranteed** if defaults/assets are resolved differently between surfaces.

**Decision:** Epic 5 will be delivered in two phases:

1. **Form Builder Readiness tranche (foundation, must ship first)**
2. **Review/Test/Publish governance tranche (builds on the foundation)**

### “No rework” constraints from PRD (Enterprise direction)

Per `docs/prd.md` (“Enterprise Onboarding, Domains, SSO, and Internal vs External Usage”), Epic 5 must avoid design decisions that block future enterprise work:

- **Domains = branding/routing, not security boundary**: do not implement security by “which host you used”.
- **Security = auth + access policy**: keep access checks centralized (public tokens today; company-only audiences later).
- **SSO authenticates identity, not tenant membership**: do not assume “logged in via SSO” implies access to a company without explicit policy.

**Practical implications for Epic 5 readiness work:**
- Asset URLs should be **generated at runtime** (avoid persisting absolute hosts) so custom domains can be introduced later.
- Introduce/retain an explicit “audience/access policy” concept in publish metadata design (even if Epic 5 ships Public-only).

---

## ✅ PRD Anchors (What “Review & Publishing” means)

Per `docs/prd.md`:

### Preview & Testing
- Toggle **Preview** vs **Production** mode in the builder
- Preview URL uses the same runtime as production (`?preview=true` concept)
- Preview leads are flagged separately (preview vs production)
- **Minimum preview tests** required before publish (default 5; admin override per company)
- Audit who ran tests + when

### Publish workflow
- Company User cannot publish directly → must **request admin to publish**
- Admin receives “Review and Publish” link → reviews form → runs required tests (if needed) → publishes

### Publishing & hosting
- Publish generates a stable public URL
- Unpublish takes the form offline
- Activation windows (event-based) control when forms are active

---

## 🧑‍💼 Customer Value (What Epic 5 delivers)

Epic 5 delivers **production-ready form creation** plus a **managed publishing workflow** so customers can answer:

- **Can we reliably create and brand forms at scale?** (company defaults + reusable assets; no JSON bloat)
- **Is this form ready to go live?** (tests completed vs required threshold)
- **Who tested it and when?** (basic audit trail)
- **What’s the production link?** (stable URL/token for published forms)
- **If I can’t publish (role), how do I get it published?** (publish request → admin review)

### Form lifecycle (customer-facing)

Minimum customer-facing lifecycle we will support:

- **Draft** → **Preview Tested** (≥ threshold) → **Pending Admin Review** → **Published** → **Unpublished**

> Note: This is a *UX lifecycle* (badges + gating). The underlying data model can evolve, but the customer must always see a clear “where am I” state.

### Builder vs Dashboard (what goes where)

**Builder = creation + testing actions.**  
**Dashboard = management + visibility + approvals.**

#### Builder enhancements (Epic 5 in scope)
- **Preview vs Production toggle** (and clear visual state in the builder header)
- **Test counter visibility** (e.g., “Preview tests: 2/5”)
- **Publish gating messaging** (why publish is blocked and what to do next)
- **Publish request UX for Company User** (modal: select admin(s) + optional message)
- **Admin review entry point** that reuses the preview runtime (read-only “review” mode is acceptable)

#### Dashboard enhancements (Epic 5 in scope)
- **Form status badges** on Event Dashboard (Draft / Pending Review / Published / Unpublished)
- **Readiness visibility** on form cards (Preview tests \(X/Y\), last tested timestamp/user)
- **Admin review queue** (pending publish requests, deep-link to “Review and Publish”)
- **Published link visibility** (copy link, show activation window status)
- **Preview vs production lead hygiene surfaces (minimal)**:
  - Filter preview vs production in submissions list (and ability to clear preview submissions if required)

#### Notification / entry points (Epic 5 in scope)
- Minimum viable: **in-app queue** for admins (Dashboard)
- Optional (nice-to-have): email notifications for publish requested / changes requested / published

### Surface map (capability → location)

| Capability | Builder | Dashboard |
|-----------|---------|-----------|
| Build/edit form content + styling | ✅ | - |
| Switch Preview vs Production mode | ✅ | - |
| Run preview tests / record test runs | ✅ | - |
| See test progress \(X/Y\) | ✅ | ✅ |
| Request publish (Company User) | ✅ | ✅ (optional shortcut) |
| Review publish requests (Admin) | - | ✅ |
| Review form (Admin) | ✅ (review mode) | ✅ (deep-link) |
| Publish / Unpublish (Admin) | ✅ (review/publish screen) | ✅ |
| See stable production URL | - | ✅ |
| Configure activation window status (event-based) | - | ✅ |

---

## 🎨 UX Ideation (Required before Story 5.1 implementation)

To reduce long UAT loops, Epic 5 should start with a lightweight UX ideation output that answers:
- What screens exist (and which live in Dashboard vs Builder)?
- What are the happy paths for **Company User** and **Company Admin**?
- What does the user see when publish is blocked (threshold, role, missing tests)?
- What does “Review and Publish” look like (minimum viable)?

**Artifact:** `docs/stories/EPIC-5-UX-IDEATION.md` (draft UX notes + screen map).

---

## 🧭 Scope Boundary (Epic 5)

### In Scope

#### Phase A: Form Builder Readiness (Foundation)

- **Background asset management (no base64 in `DefinitionJSON`)**
  - Upload/store/reuse background images as **assets** and reference them from the form definition
  - **Limits are configuration-backed**: any upload/runtime limits MUST be stored in `config.AppSetting` (loaded via `ConfigurationService`)
    - Suggested keys (draft; finalize in Story 5.1):
      - `forms.assets.images.max_upload_bytes`
      - `forms.assets.images.max_width_px`
      - `forms.assets.images.max_height_px`
      - `forms.assets.images.allowed_mime_types` (JSON)
      - (Later) `forms.assets.images.max_total_bytes_per_company` (quota)
      - (Later) `forms.assets.images.max_count_per_company` (quota)
  - **Provider swap is painless**: build a storage provider abstraction (Local dev → Azure Blob prod) and switch by config (no definition/schema change)
  - **Placement supports cropping**: store background positioning in canvas coordinates (allow negative offsets) and clip at render time
    - Enforce an **intersection rule**: if the image is fully off-canvas, it is **auto-removed from the canvas** (asset remains in library so user can re-add)
  - Asset lifecycle: dedup (hash), soft-delete, cleanup policy, and rename (`displayName` separate from `originalFilename`)
  - Migration: **not expected** (background images weren’t functional in existing forms as of 2026-02-07), but keep a defensive guard against embedded Data URLs
- **Company-level form defaults (brand system)**
  - Persist defaults once per company (fonts/colors/spacing/typography)
  - Inheritance model: company defaults → form overrides → component overrides
  - UI to manage defaults (Dashboard preferred; builder shows “inherited vs overridden”)
- **Schema + validation alignment**
  - Backend validates the real builder output (structure + key invariants) instead of ignoring unknown keys
  - Schema versioning + compatibility/migration strategy
- **Preview/production parity via a shared resolver**
  - The same resolution rules for defaults and assets apply across:
    - Builder preview
    - Public renderer
    - “Review and Publish” (admin)

#### Phase B: Review/Test/Publish Governance (Workflow)

- **Preview vs Production mode**
  - Clear separation in UI and in stored submissions (flags/metadata)
  - Ability to filter/delete preview submissions (hygiene)
- **Test threshold gating**
  - **Optional per company** (enabled/disabled)
  - Threshold is **adjustable** (default + company override)
  - Block publish **only when enabled** and threshold is not met (with clear UI)
  - Define what counts as a “test”:
    - Preview submission **or**
    - Explicit “Record test run” action (supports static/no-input forms)
  - Audit trail of test runs (who + when)
- **Publish request + review flow**
  - **Optional per company** (separation-of-duties toggle)
  - If enabled: Company User requests publish → Admin review queue + “Review and Publish” entry point
  - If disabled: Company Users may publish directly (without forcing “admin approval” for small single-user companies)
- **Publish/unpublish**
  - Form status model supports draft/pending review/published/unpublished
  - Production link/token generation and persistence
- **Public URL + activation windows**
  - Stable public URL per published form
  - Event-based activation/deactivation rules (show “event ended” message)
- **UX consolidation for review/publish (allowed)**
  - If the Unified Form Workspace helps achieve review/publish goals, implement **only the minimal subset** needed for Epic 5 (avoid boiling the ocean).

### Out of Scope (Explicit)

- Real-time multi-user co-editing (concurrent editing, live cursors) → Epic 4 (advanced)
- Payments/billing/invoicing (Stripe + GST invoices) → Epic 6
- Full analytics dashboards beyond basic preview/production filtering → Epic 7
- Enterprise onboarding: custom domains + SSO + join policy/approvals UI → later (see PRD “Post‑MVP Direction”)
- Internal-only forms (Company-only audience) and restricted audience policies → later (Enterprise tier)

---

## ✅ Epic 5 Done Criteria (Draft)

Epic 5 is complete when:
- [ ] Background images are managed as reusable assets (no embedded base64 Data URLs in `FormVersion.DefinitionJSON`)
- [ ] Image upload/runtime limits are enforced via settings stored in `config.AppSetting` (not hard-coded)
- [ ] Company-level form defaults exist and are applied consistently (inheritance model documented + implemented)
- [ ] Backend validation aligns with the builder definition (schema drift prevented; versioning/migration strategy exists)
- [ ] Preview/production parity is guaranteed by a shared defaults/assets resolver
- [ ] Preview vs production is clearly supported end-to-end (UI + persistence)
- [ ] Preview testing gate is configurable per company (enabled/disabled + adjustable threshold) and supports static/no-input forms
- [ ] Publish approval workflow is configurable per company (direct publish vs request/review), without blocking single-user companies
- [ ] Published forms have stable public URL/token behavior and activation windows
- [ ] Dashboard provides management visibility (status + readiness + review queue) without requiring opening the builder
- [ ] UAT proves the end-to-end path works for both roles (Company User + Company Admin)

---

## 🗺️ Proposed Story Roadmap (Draft for Approval)

| Story | Title | Goal | Notes / Dependencies |
|------|-------|------|----------------------|
| **5.1** | Background Asset Management | Replace embedded base64 backgrounds with asset upload/store/reference (local → Azure ready) | ✅ **Complete 2026-02-13** — T01–T08 HumanDone; merged to master 2026-02-13. |
| **5.2** | Company Form Defaults (Brand System) | Persist company-level defaults and apply inheritance across forms | ✅ **Complete 2026-02-16** — T01–T08 HumanDone; merged to master (#32). |
| **5.3** | Schema + Validation Alignment | Bring backend definition schema in line with builder output; prevent drift | ✅ **Complete 2026-02-16** — Single-session; merged to master (#42). |
| **5.4** | Shared Resolver Parity | Single resolver for defaults/assets used by preview + public + review | ✅ **Complete 2026-02-16** — Single-session; merged to master (#43). |
| **5.5** | Preview/Production Governance Foundations | Toggle preview vs production + test counter + readiness badges | ✅ **Complete 2026-02-16** — Single-session; merged to master. |
| **5.6** | Publish Request Workflow | Company User requests publish; admin receives review queue/link | ✅ **Complete 2026-02-17** — Merged to master; FormReviewPage, approve/reject. |
| **5.7** | Company Settings Hub | Company details, Form Approval Workflow, assets (images, terms) | ✅ **Complete 2026-02-18** — Merged to master. |
| **5.8** | Admin Review & Publish + Activation | Stable URL on publish, unpublish, published link visibility, activation windows | **Next** — Builds on 5.6 review screen. |
| **5.9** | Hardening + UAT | End-to-end UAT across roles + regressions | Includes fix stories as needed. |
| **5.10** | UX Consolidation (optional) | Minimal “workspace” consolidation to reduce navigation friction | Only if needed to ship Epic 5 goals. |

---

## 📋 Backlog (Future Work)

Items added during Epic 5 planning; not in current story scope.

| Item | Description | Source |
|------|-------------|--------|
| **Global Defaults screen** | Administration Settings page for Global Form Defaults — mirror of Company Defaults page (Global Properties controls + Toolbox visual guide). System Admin only. | PM review 2026-02-13 (Story 5.2) |
| **AI-Assisted Form Building** | AI agent generates DefinitionJSON from natural-language prompt; static validator (schema + collision/boundary) returns feedback; user refines in Form Builder. See `docs/AI-FORM-BUILDING-IDEA.md`. | PM assessment 2026-02-18 — consider after Epic 5 |
| **User Preference Centre (Communication)** | Platform-wide page for notification and communication preferences. Communication is essential for engagement; handle notification fatigue delicately. **MVP:** In-app notifications. Add page to Profile dropdown; build incrementally as we add processes (publish requested, published, unpublish reminders, team invites, etc.). **Email:** Platform already uses email (login, onboarding, approval requests). Use Mailhog until launch to avoid paid email service; then switch to SendGrid/Azure. Cross-epic: relevant to Epic 4 (Team Collaboration), Epic 5 (publish flow), and future features. | PM 2026-02-18 — Story 5.8 notification research |

**Note:** APIs for Form Builder defaults and Component Catalog (multi-country, multi-company) are now **in scope** for Story 5.2. Form Builder Init API delivers single payload (defaults + components + DefinitionJSON skeleton) per `docs/stories/STORY-5.2-FORM-BUILDER-INIT-API.md`.

---

## 🔗 Key References

- Product requirements: `docs/prd.md`
- UX ideation: `docs/stories/EPIC-5-UX-IDEATION.md`
- Unified workspace concept: `docs/stories/UNIFIED-FORM-WORKSPACE-SPECIFICATION.md`
- Access control foundations: `docs/ACCESS-CONTROL-MATRIX.md`, `docs/stories/story-2.9.md`
- Submission foundations: `docs/stories/story-3.11.md`, `docs/tasks/3.11/TASK-PLAN.md`

---

*Epic 5 Status Document - Drafted for approval*  
*Last Updated: 2026-02-18 — Stories 5.6, 5.7 complete; 5.8 next*

