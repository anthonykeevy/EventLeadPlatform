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
| **6.4.3c** | **Eval Diff + Statistics Tooling** | Add Welch/Fisher statistics, diff reports, and public harness docs for prompt-change decisions. | ✅ **Complete** (2026-04-25, PR #71) |
| **6.4.4** | **Prompt Shrink Sweeps H1/H2/H4** | Run H1/H2/H4 plus combined sweeps through the harness, ship winners, and document hypothesis evidence. | ✅ **Complete** (2026-04-27, PR #72) |
| **6.4.4.1** | **Locale Architecture: Wire the Registry** | Replace hard-coded locale prompt constants with registry-backed locale blocks, add audience locale/brand posture resolution, and bump eval/judge to prompts-v1.1/rubric_v2. Company Settings brand posture UI deferred to `g-6441-company-brand-settings-ui`. | ✅ **Complete** (merged 2026-04-27, PR #75) |
| **6.4.4.1-ac10** | **AC-10 Baseline Re-Judge Execution** | Re-judged the `prompts-v1.1` baseline under `rubric_v2`; AC-10 passed and recommends Story 6.4.4.2 next. | ✅ **Complete** (merged 2026-04-27, PR #77) |
| **6.4.4.2** | **Re-evaluate H2/H4 under rubric_v2** | Ablation study: H2-only and H4-only re-run against the AC10 `rubric_v2` baseline; both failed the ship bar, so current `master` behavior remains unchanged. | ✅ **Complete** (merged 2026-04-28, PR #79) |
| **6.4.5** | **Component Property Cheat Sheet H3** | H3 was implemented and measured under `prompts-v1.1` / `rubric_v2`; useful signal but material `field_label_f1` regression and locale/context-conflict noise mean no-go as-is. Prompt changes reverted; artifacts preserved. | ✅ **Measured/no-change** (merged 2026-04-29, PR #81) |
| **6.4.6** | **AU-Only Diagnostic Evaluation Framework + Baseline** | Built the AU-only diagnostic framework, AU benchmark, prompt-context linter/shared context bundles, judge diagnostics, deterministic AU checks, Analyst experiment harness, and the first current-state AU baseline. | ✅ **Complete** (merged 2026-04-30, PR #82) |
| **6.4.7** | **AU Baseline Analysis And Iterative Prompt Improvement Loop** | BMAD Analyst loop completed AU-001 through AU-006 against the frozen AU-000 baseline. AU-005 is the strongest behavioural target (`4.471 / 5`, `89.4%`); AU-006 provides the lint-clean wording lesson. Follow-up should promote AU-005 behaviour into production prompt/context sections without literal eval overlay lint. | ✅ **Complete** (merged 2026-05-06, PR #84) |
| **6.4.8** | **Promote AU-005 Into Production Prompt Context** | Dev-owned production implementation story: convert AU-005's winning strict AU + publish-ready behaviour into production prompt/context storage, using AU-006's lint-clean conflict wording and targeted p11 leakage guard. | ✅ **Complete** (merged 2026-05-07, PR #85) — AU-005 behaviour promoted via migration 072 + downgrade review note (PR #86). |
| **6.5a** | **Architecture Phase — Clarification Data Plane + Prompt Assembly Registry Design** *(rescoped 2026-05-20)* | The original "add clarification dropdowns" brief expanded during Dimitri-led architecture work into a full data-plane redesign. Deliverable: two architecture docs (`decision-6.5a-clarification-options-data-model.md` Rev 9, and `prompt-assembly-registry-architecture.md`). Implementation decomposed into 6.5b / 6.5c / 6.5d. See `story-6.5a.md` for the closeout and decomposition rationale. | ✅ **Complete (Architecture Phase)** (2026-05-20) — PR #87 closed-as-superseded; merged via PR #103 (architecture closeout + 6.5b draft) |
| **6.5b** | **Prompt Assembly Registry Foundation** *(Closed R6)* | Stand up `PromptAssemblyRegistry*` / `PromptSection*` / `PromptSectionVariant*` / `PromptSectionData` schema + Python resolver/renderer (`backend/modules/form_ai/prompt_assembly/`). Migrated Blocks A/B/C/G/I from code/disk into seeded DB variants. Block G inlined via migration `081`; `_load_context_pack` removed. Migrations `078`–`083` (incl. Block A preamble trim). `dbo.GenerationRun` audit columns for replayability. AC-19 equivalence diff PASS + Tony sign-off. **R6 resolved** on Azure Test (2026-05-20). See `story-6.5b.md`, `STORY-6.5b-CLOSEOUT-REPORT.md`. | ✅ **Complete** (2026-05-20) — merged PR #104 to `develop`; Test deploy verified |
| **6.5c** | **Capability Catalog Cutover** | `resolve_allowed_components` authoritative for toolbox (`/api/form-builder/init`), Form AI Blocks A/F/I, and semantic validator. Block F in registry (`COMPONENT_CAPABILITY` / `DynamicComponentCatalog`). `ref.BrandPosture` + `Company.BrandPostureID`. Frontend toolbox init-only. Migrations `084`–`086`. AC-15 catalog alignment PASS. LocalDB + Azure Test UAT green (2026-05-21). See `story-6.5c.md`, `STORY-6.5c-CLOSEOUT-REPORT.md`. Catalog backlog absorbed into **6.5d**. | ✅ **Complete** (2026-05-21) — merged PR [#106](https://github.com/anthonykeevy/EventLeadPlatform/pull/106) + closeout [#107](https://github.com/anthonykeevy/EventLeadPlatform/pull/107) to `develop` |
| **6.5d** | **Clarification Data Plane + Component Catalog Completion** | **Track A:** Global catalog backlog + AU EDF pair with full runtime UX; `ADD-COMPONENT-TO-PLATFORM-CHECKLIST.md` v1.2 (§0b EDF parity); alignment script (21 codes). **Track B:** `ref.*` clarification tables + APIs; Block E; AI panel dropdowns; persistence + audit. Local + Azure Test UAT pass. PRs [#109](https://github.com/anthonykeevy/EventLeadPlatform/pull/109), [#111](https://github.com/anthonykeevy/EventLeadPlatform/pull/111), [#112](https://github.com/anthonykeevy/EventLeadPlatform/pull/112), [#113](https://github.com/anthonykeevy/EventLeadPlatform/pull/113). | ✅ **Complete** (2026-05-25 merged; Azure Test UAT 2026-05-26) |
| **6.5e-landing** | **Customer-Facing Beta Landing Page** — replace the developer-friendly Test system root page with customer-facing positioning, CTA to account creation, SEO/AEO-ready FAQ content, beta trust wording, and safe example/use-case sections. Promotes `docs/LANDING-PAGE-BRIEF.md` into the active project plan and supports customer discovery while avoiding speculative Form Builder work. See `story-6.5e-landing-page.md`. | 🧪 **Ready for UAT** — PR [#117](https://github.com/anthonykeevy/EventLeadPlatform/pull/117); Privacy/Terms + safe screenshots remain follow-ups |
| **6.5e-vision** *(was 6.5b-vision — renamed 2026-05-20)* | **Image-to-Form Vision Path** (+ **Track 0:** component platform hardening from 6.5d closeout — checklist v1.3, props-wiring script, optional EDF polish). Screenshot/photo input to `FormSemanticPlan`, reusing deterministic compiler architecture. See `story-6.5e-vision.md`. | ⏸️ **Deferred** — pause until customer discovery provides stronger signal on Form Builder / image-to-form priority |
| **6.5f-style** *(was 6.5b-style — renamed 2026-05-20)* | **Style Intent Resolver** | Add semantic `themeIntent`/`styleIntent`, resolver boundary, canvas-preservation contract, and H5 sweep. | ⏸️ Prompt-candidate sweep deferred pending AU-only diagnostic framework |
| **6.5g-PII** *(was 6.5c — renamed 2026-05-20)* | **PII Detection Layers** | PII detection, user-assertion clarification hook, and PII-heavy benchmark subset. | ⏳ Pending |
| **6.5h-fonts** *(was 6.5d — renamed 2026-05-20)* | **Google Fonts Directive** *(conditional)* | Add "Use only Google Fonts" directive and font-nomination validity check if H6 wins. | ⏸️ Prompt-candidate sweep deferred pending AU-only diagnostic framework |

### Phase B: Platform Billing & Monetization (deferred — renumbered 2026-04-23)

| Story | Title | Goal | Status |
|------|-------|------|--------|
| **6.6** | Platform Billing Infrastructure | Set up Stripe Direct, webhooks, and the database schema for Payments and Invoices. | ⏳ Pending |
| **6.7** | Unified Publish & Payment Gate | Integrate the Stripe Checkout into the Epic 5 Admin Review & Publish flow. | ⏳ Pending |
| **6.8** | Australian GST Invoicing | Auto-generate compliant PDF invoices and email them upon successful payment. | ⏳ Pending |
| **6.9** | Stripe Connect Infrastructure | Allow companies to securely link their Stripe accounts via OAuth in Company Settings. | ⏳ Pending |
| **6.10** | Form Payment Component | Add a Payment component to the builder and upgrade the submission API to handle B2B2C checkout. | ⏳ Pending |
| **6.11** | **Production Environment + CI/CD + Manual Approval Gate** | Provision the Azure production resources (App Service `signalplatforms-prod` with `production` + `staging` deployment slots, Azure SQL prod on a separate logical server, ACS verified sender domain, Application Insights, Key Vault) per `docs/architecture/azure-infrastructure-architecture.md` §4 + §7. Add `.github/workflows/deploy-to-prod.yml` triggered on push to `master` (and `workflow_dispatch` for hotfix promotion) that deploys to the **staging slot first**, runs the pre-deploy CI smoke gate (PR #99 pattern, inherited from Test) + post-deploy smoke + feature-readiness probes against the staging slot, then pauses for **manual approval on the `production` GitHub Environment** (required reviewer = Tony) before performing the atomic slot swap. Configure custom domain + Cloudflare DNS for `app.signalplatforms.io` bound to the production slot only. Validate Stripe production credentials end-to-end. Publish `docs/runbooks/PROD-ROLLBACK-RUNBOOK.md`. **Sequenced last so production opens with billing live (6.6–6.10).** Closes Phase D candidate D1 (production-side). **Architecture blueprint:** `EPIC-6-WORKFLOW-GUIDE.md` § "Production Deployment Blueprint (Story 6.11)" — design, slot diagram, workflow step sequence, readiness-probe pattern, rollback strategy, slot-stickiness audit, and task list are all pre-decided so the story executes plumbing only. | ⏳ Pending (scheduled post-6.10) |

### 🛑 Deferred Post-MVP

| Item | Reason |
|------|--------|
| **AI Iteration on Existing Designs** (was Story 6.4) | High-risk novel capability requiring same architectural-discovery pattern that consumed Story 6.3 + 6.3.1. PM/SM joint review on 2026-04-23 concluded value-vs-effort doesn't justify shipping in MVP. Image-to-form (6.5) gives a sharper differentiator at lower architectural risk. Revisit post-revenue. |

---

### Phase D: MVP Hardening — Discovery-Surfaced Fix Candidates (added 2026-05-03)

**Origin:** Customer discovery preparation (May 2026) included a deep verification pass against the codebase to confirm which features are shipped vs. partial vs. designed-only. The pass surfaced gaps between *design intent* and *shipped code*. These are tracked here so they can be promoted to formal stories within Epic 6 (or split out into a hardening epic) as triage decides.

**Source doc:** `docs/customer-discovery/mvp-scope-fix-candidates.md` — full context, risk-if-shipped-as-is, effort hints, and discovery dependencies for each item.

**Triage proposal (suggested order):**

| # | Candidate | Status proposal | Discovery dependency | Suggested promotion path |
|---|-----------|----------------|----------------------|--------------------------|
| **D1** | **Test & Production environment setup** | **Test: ✅ Done** (2026-05-12 → 2026-05-14). Azure App Service test slot live; `develop` branch auto-deploys via `.github/workflows/deploy-to-test.yml`; ACS Email + ODBC URL translator + SPA-from-FastAPI + Alembic-on-startup all working. **Production: promoted to Story 6.11** (sequenced post-6.10 so launch coincides with billing). | Test: none — done. Prod: scoped via `azure-infrastructure-architecture.md`. | Test: ✅. Prod: see **Story 6.11** in Phase B table above. |
| **D2** | **Production email infrastructure** (replace MailHog with SendGrid / SES / similar; DKIM/SPF/DMARC) | Build pre-MVP — couples to D1 | None | Sibling story to D1 |
| **D3** | **Email-share onboarding for non-tenant emails** | Build pre-MVP | Light — validates that user-initiated request-to-join is acceptable to enterprise IT (or whether enterprise mode disables it) | Story under Epic 6 (or a sharing-hardening sub-section); medium effort |
| **D4** | **Company-wide form access — UI/API alignment** | Build pre-MVP OR hide the UI radio button | Light if hiding; light-to-medium if implementing | Trivial story (hide UI) or medium story (implement). Hide UI immediately to remove customer-visible failure |
| **D5** | **Cost-gated approval — backend enforcement OR pivot to alternative governance** | Decide after discovery (lean Replace) | **Strong** — scorecard Q4 (multiple-choice) + Persona B procurement probe + Persona C visibility probe will determine right shape | Can't story this until discovery surfaces governance-shape preference; track here as blocked-on-discovery |
| **D6** | **Kiosk auto-reset — form-builder UI surface** | Defer unless discovery shows switching-signal | Strong — track scorecard #7 reactions and unprompted mentions | Promote only if ≥10–15% of Persona A/C interviewees rate ≥4 |
| **D7** | **"Shared by [Company / User]" tag — configurable / suppressible** | Decide after discovery | Strong — Persona C white-label appetite; check scorecard #30 + AG2 | Small story if promoted (admin setting + conditional render) |
| **D8** | **Group admin role + consolidated dashboard** | Out of MVP scope; collect signal | Strong — likely Persona B switching-signal | Post-MVP story or a separate epic if signal is strong |
| **D9** | **Self-signup → existing company → admin-approval flow** | Validate via discovery | Strong — security/IT-team posture varies by enterprise; may require "enterprise mode" toggle | Promote with D3 if security signal supports user-initiated; otherwise add IT-provisioned variant |

**Decision points & gates:**
- **D1 + D2** are launch-readiness blockers regardless of discovery outcomes — start when developer capacity allows; ~2–4 focused weeks expected.
- **D3 + D4** are pre-launch trust blockers — claiming features in interviews / collateral that fail in product is the worst customer experience. Hide-UI on D4 can ship today.
- **D5–D9** are deliberately discovery-blocked. Don't build governance, kiosk UI, or white-label features speculatively; the customer-discovery program is designed to surface preference before commitment.

**Cross-references:**
- Full context per candidate: `docs/customer-discovery/mvp-scope-fix-candidates.md`
- Open design questions feeding these: `docs/customer-discovery/tenancy-sharing-and-dashboards.md` (Open Design Questions section)
- Discovery scorecard items that will inform D5–D9: `docs/customer-discovery/feature-resonance-scorecard.md`
- Triage-feeder rationale: customer-discovery README `docs/customer-discovery/README.md`

---

*Epic 6 Status Document*  
*Last Updated: 2026-06-03 — Story 6.5d **Complete** (PRs #109–#113; Azure Test UAT 2026-05-26). **Current focus:** Story **6.5e-landing** UAT on PR [#117](https://github.com/anthonykeevy/EventLeadPlatform/pull/117); then `develop` → `master` reconciliation. Story **6.5e-vision** deferred until discovery signal improves.*  
*Prior 2026-05-19 — (1) Added Story 6.11 — Production Environment + CI/CD + Manual Approval Gate — at the end of Phase B (sequenced post-6.10 so production opens with billing live). (2) Phase D row D1 split: Test environment ✅ done (Azure + GitHub Actions `deploy-to-test.yml` on `develop`); Production work promoted to Story 6.11. (3) See `EPIC-6-WORKFLOW-GUIDE.md` for the new Environment Promotion Workflow (Worktree → develop → master). (4) Story 6.11 row references the "Production Deployment Blueprint (Story 6.11)" subsection in `EPIC-6-WORKFLOW-GUIDE.md` — design is pre-decided so the story executes plumbing only.*
