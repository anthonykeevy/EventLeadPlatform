# Epic 6 Status - AI Generation & Monetization Engine

**Epic ID:** Epic 6  
**Status:** 📝 Draft / Planning  
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

## 🗺️ Proposed Story Roadmap

| Story | Title | Goal |
|------|-------|------|
| **6.1** | AI Foundation: Static Validator | Build the backend API that takes `DefinitionJSON` and returns schema/collision errors. |
| **6.2** | AI Form Builder UI & Agent Loop | Build the chat interface and the AI retry loop to generate forms onto the canvas. |
| **6.3** | Platform Billing Infrastructure | Set up Stripe Direct, webhooks, and the database schema for Payments and Invoices. |
| **6.4** | Unified Publish & Payment Gate | Integrate the Stripe Checkout into the Epic 5 Admin Review & Publish flow. |
| **6.5** | Australian GST Invoicing | Auto-generate compliant PDF invoices and email them upon successful payment. |
| **6.6** | Stripe Connect Infrastructure | Allow companies to securely link their Stripe accounts via OAuth in Company Settings. |
| **6.7** | Form Payment Component | Add a Payment component to the builder and upgrade the submission API to handle B2B2C checkout. |

---

*Epic 6 Status Document - Drafted for approval*  
*Last Updated: 2026-02-23*