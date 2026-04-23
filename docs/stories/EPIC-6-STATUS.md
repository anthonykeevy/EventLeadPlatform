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
| **6.4** | AI Iteration on Existing Designs | Allow users to refine/modify an existing form via AI; "change the layout", "add a field", etc. | ⏳ Pending (foundation in place — ready for SM to plan) |

### Phase B: Platform Billing & Monetization (deferred)

| Story | Title | Goal | Status |
|------|-------|------|--------|
| **6.5** | Platform Billing Infrastructure | Set up Stripe Direct, webhooks, and the database schema for Payments and Invoices. | ⏳ Pending |
| **6.6** | Unified Publish & Payment Gate | Integrate the Stripe Checkout into the Epic 5 Admin Review & Publish flow. | ⏳ Pending |
| **6.7** | Australian GST Invoicing | Auto-generate compliant PDF invoices and email them upon successful payment. | ⏳ Pending |
| **6.8** | Stripe Connect Infrastructure | Allow companies to securely link their Stripe accounts via OAuth in Company Settings. | ⏳ Pending |
| **6.9** | Form Payment Component | Add a Payment component to the builder and upgrade the submission API to handle B2B2C checkout. | ⏳ Pending |

---

*Epic 6 Status Document*  
*Last Updated: 2026-04-15 (Story 6.3.1 complete via PR #64 — deterministic compiler foundation in place; Story 6.4 is next)*