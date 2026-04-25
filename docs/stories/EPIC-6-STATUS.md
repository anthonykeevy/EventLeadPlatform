# Epic 6 Status - AI Generation & Monetization Engine

**Epic ID:** Epic 6  
**Status:** 🔄 In Progress  
**Created:** 2026-02-23  
**Product Manager:** John (PM Agent)  

---

## 🎯 Epic 6 Overview

**Objective:** Transform the platform into a revenue-generating engine by introducing two massive value drivers: **AI-Assisted Form Building** to drastically reduce time-to-value, and a **Dual-Tier Payment Architecture** that handles both our own platform billing (SaaS revenue) and allows our customers to charge their end-users (B2B2C).

Epic 6 bridges the gap between a free tool and a commercial enterprise. We are fulfilling the core business model from the PRD ("Create Free, Pay to Publish") while immediately adding a high-demand feature (form payments) for our customers.

---

## 🧠 Architectural Pivot: The "Dual-Tier" Stripe Strategy

During planning, a major strategic requirement was introduced: *We don't just want to charge our customers; we want our customers to be able to add a payment component to their forms to charge their attendees/leads.*

This fundamentally changes the payment architecture. We must implement two different Stripe patterns simultaneously:

1. **Stripe Direct (Platform Billing):** 
   - **Use Case:** EventLeadPlatform charging the Company Admin the $99 fee to publish a form.
   - **Architecture:** Standard Stripe Checkout. Money flows directly from the Company Admin's credit card into your EventLeadPlatform Stripe account.

2. **Stripe Connect (Customer Monetization):**
   - **Use Case:** A Company User adds a "Payment Component" to their form (e.g., "$50 Event Registration Fee"). The end-user fills out the form and pays.
   - **Architecture:** We must use **Stripe Connect (Standard)**. 
     - *Step 1:* In Company Settings, the Admin clicks "Connect Stripe" and goes through an OAuth flow to link their own business Stripe account to our platform.
     - *Step 2:* The Form Builder gets a new `Payment` component.
     - *Step 3:* When an end-user submits the form, the payment is routed directly to the *Customer's* connected Stripe account. (Optional: We can configure this to take an application fee/cut of the transaction in the future).

---

## 🧭 Scope Boundary

### Phase A: AI-Assisted Generation
- **Static Collision Validator:** A backend endpoint that validates `DefinitionJSON` for schema correctness, canvas boundaries, and component overlaps without needing a browser DOM.
- **AI Loop & Prompt Pack:** Engineering the precise instructions so an AI agent can reliably generate compliant `DefinitionJSON` from a natural language prompt.
- **Builder UI Integration:** A chat/prompt interface where the user describes the form, the AI generates it, and it instantly loads onto the canvas for manual refinement.

### Phase B: Platform Billing & Invoicing (The MVP $99 Gate)
**Design Constraint:** While the MVP is a flat $99 publish fee, the underlying architecture MUST be extensible to support future complexity (subscriptions, tiered usage, add-ons). We will use Stripe Checkout Sessions and a flexible `LineItems` database model to ensure we aren't painted into a corner.
- **Stripe Direct Integration:** Checkout sessions for the $99 publish fee.
- **Unified Approval Workflow:** Modifying the Epic 5 Publish Request flow so that if a form is approved, it lands in a "Pending Payment" state until the Admin checks out.
- **GST Invoicing:** Generating an Australian GST-compliant PDF invoice post-payment and emailing it to the Admin.

### Phase C: Form Monetization (Stripe Connect)
- **Company Stripe Linking:** An OAuth flow in Company Settings allowing customers to link their existing Stripe accounts.
- **Payment Component:** A new builder component representing a fixed or variable price.
- **Submission Gateway:** Upgrading the public form renderer to process a Stripe Elements payment before successfully recording the form submission.

### Out of Scope
- Subscription billing (we are sticking to one-time per-publish fees).
- AI generation of multi-page forms (MVP AI will stick to single-page layouts to control collision complexity).
- **AI iteration on existing designs** (deferred post-MVP per 2026-04-23 PM/SM scope review). Iteration is a high-risk novel capability; MVP differentiator shifts to **Image-to-Form** instead. Edit/refine actions in MVP are handled by direct builder tools (Properties Panel, drag/drop, undo). See `EPIC-6-WORKFLOW-GUIDE.md` changelog for rationale.

---

## 🗺️ Story Roadmap

### Phase A: AI-Assisted Generation

| Story | Title | Goal | Status |
|------|-------|------|--------|
| **6.1** | AI Foundation: Static Validator | Build the backend API that takes `DefinitionJSON` and returns schema/collision errors. | ✅ **Complete** (2026-02-26, PR #52) |
| **6.2** | AI Form Builder UI & Agent Loop (POC) | End-to-end POC: chat UI, AI generation endpoint, retry loop, context pack v1, model comparison. | ✅ **Complete** (2026-03-20, PR #53) |
| **6.2.1** | Component Library Expansion | Add `url`, `rating`, promote `paragraph`; update COMPONENT-FRAMEWORK docs; Properties Panel controls; frontend UAT for all new components on toolbox/canvas/runtime surfaces. | ✅ **Complete** (2026-03-30, PR #54) |
| **6.2.2** | File Upload Component (Full Stack) | `file-upload` builder component + public upload endpoint + SubmissionAttachment model + secure download API for company (`GET .../attachments/.../content`). In-product download UX → **Epic 8**. Submission-scoped attachment IDs ensure no cross-contamination. | ✅ **Complete** (2026-03-31, PR #55) |
| **6.3** | AI Context Uplift & Benchmark Baseline | Delivered benchmark/logging uplift and tuning controls, but closed as a learning story after UAT quality gap findings. See `STORY-6.3-CLOSEOUT-REPORT.md`. | ✅ **Closed (Learning)** (2026-04-15) |
| **6.3.1** | Simplified AI Output + Deterministic Layout Foundation | Bridge story: AI emits coordinate-free `FormSemanticPlan`, deterministic Python compiler owns geometry; render-then-measure round-trip; governance (capability snapshot, validation contracts, prompt versioning, generation runs); UAT rounds 1–11 PASS. See `STORY-6.3.1-CLOSEOUT-REPORT.md`. | ✅ **Complete** (2026-04-15, PR #64) |
| **6.4** | **AI Agent Panel Production Polish + User Preferences Architecture Foundation** *(rescoped 2026-04-23; expanded same day to include foundational user-preferences architecture per Tonyk's request for "aligned database architecture to support this level of managing User preferences")* | Tactical polish (last prompt persistence, replace-form warning with "don't show again", hide transport selector, retry default in `config.AppSetting`, silent soft-validation autoload) **plus** foundational `dbo.UserPreference` + `ref.UserPreferenceCategory` + `ref.UserPreferenceKey` architecture mirroring the `config.AppSetting` pattern, dynamic Notifications UI, and `GET/PATCH/DELETE /api/me/preferences`. Final size: M-L (4 migrations, 19 ACs, 41 new backend tests). See `STORY-6.4-CLOSEOUT-REPORT.md`. | ✅ **Complete** (2026-04-24, PR #66) |
| **6.4.1** | *(Optional micro-story — only if surfaced during 6.4)* Submit-button validation parity (design pill ↔ preview summary) — `g-frontend-submit-parity` from 6.3.1 carry-forward backlog. | Did not surface during 6.4 polish work; remains tracked in `EPIC-6-CARRY-FORWARD-BACKLOG.md` (P2). Suggested home: Story 6.5 frontend pass. | ⏳ Carry-forward (not promoted) |
| **6.4.3a** | **AI Eval Harness Bones** | Frozen `prompts-v1.0` benchmark set, CLI runner, `log.FormAiEvalRun` migration, Category A structural metrics, and full 10-row live baseline for later zero-behavioural-change checks. | ✅ **Complete** (2026-04-25, PR #68) |
| **6.4.2** | **Capability Snapshot Prompt Cleanup** | Delete orphan prompt-section bundle, complete Capability Parity Audit, lock/verify always-pass capability snapshot prompt behavior, document `FormSemanticPlan` backward compatibility, and re-capture post-flip baseline. | ✅ **Complete** (2026-04-25, PR #69) |
| **6.4.3b** | **Eval Judge Package + Rubric ADR** | Generate Cursor judge packages, ingest judge JSON, lock rubric v1, and document the manual cross-model judge workflow. | ✅ **Complete** (2026-04-25, PR #70) |
| **6.4.3c** | **Eval Diff + Statistics Tooling** | Add Welch/Fisher statistics, diff reports, and public harness docs for prompt-change decisions. | ⏳ Pending |
| **6.4.4** | **Prompt Shrink Sweeps H1/H2/H4** | Run H1/H2/H4 plus combined sweeps through the harness, ship winners, and document hypothesis evidence. | ⏳ Pending |
| **6.4.5** | **Component Property Cheat Sheet H3** | Add component property cheat sheet under measurement and ship only if the harness evidence wins. | ⏳ Pending |
| **6.5a** | **Clarification Questions** | Text-only clarification flow with schema additions and AI Agent panel UX for low-confidence cases. | ⏳ Pending |
| **6.5b-vision** | **Image-to-Form Vision Path** | Screenshot/photo input to `FormSemanticPlan`, reusing deterministic compiler architecture. | ⏳ Pending |
| **6.5b-style** | **Style Intent Resolver** | Add semantic `themeIntent`/`styleIntent`, resolver boundary, canvas-preservation contract, and H5 sweep. | ⏳ Pending |
| **6.5c** | **PII Detection Layers** | PII detection, user-assertion clarification hook, and PII-heavy benchmark subset. | ⏳ Pending |
| **6.5d** | **Google Fonts Directive** *(conditional)* | Add "Use only Google Fonts" directive and font-nomination validity check if H6 wins. | ⏳ Conditional |

### Phase B: Platform Billing & Monetization (deferred — renumbered 2026-04-23)

| Story | Title | Goal | Status |
|------|-------|------|--------|
| **6.6** | Platform Billing Infrastructure | Set up Stripe Direct, webhooks, and the database schema for Payments and Invoices. | ⏳ Pending |
| **6.7** | Unified Publish & Payment Gate | Integrate the Stripe Checkout into the Epic 5 Admin Review & Publish flow. | ⏳ Pending |
| **6.8** | Australian GST Invoicing | Auto-generate compliant PDF invoices and email them upon successful payment. | ⏳ Pending |
| **6.9** | Stripe Connect Infrastructure | Allow companies to securely link their Stripe accounts via OAuth in Company Settings. | ⏳ Pending |
| **6.10** | Form Payment Component | Add a Payment component to the builder and upgrade the submission API to handle B2B2C checkout. | ⏳ Pending |

### 🛑 Deferred Post-MVP

| Item | Reason |
|------|--------|
| **AI Iteration on Existing Designs** (was Story 6.4) | High-risk novel capability requiring same architectural-discovery pattern that consumed Story 6.3 + 6.3.1. PM/SM joint review on 2026-04-23 concluded value-vs-effort doesn't justify shipping in MVP. Image-to-form (6.5) gives a sharper differentiator at lower architectural risk. Revisit post-revenue. |

---

*Epic 6 Status Document*  
*Last Updated: 2026-04-25 (Prompt-engineering ideation brief v2: AI track reordered to 6.4.3a → 6.4.2 → 6.4.3b/c → measured prompt sweeps before Image-to-Form/style additions.)*