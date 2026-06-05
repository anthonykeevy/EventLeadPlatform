# Story 6.5e — Customer-Facing Beta Landing Page

**Epic:** 6 — AI Generation & Monetization Engine  
**Story ID:** 6.5e-landing  
**Title:** Replace the developer-friendly test-system homepage with a customer-facing beta landing page  
**Status:** ✅ **Complete** (2026-06-04) — local + Azure Test UAT pass; see `STORY-6.5e-LANDING-CLOSEOUT-REPORT.md`  
**Branch:** `story/epic6-6.5e-landing-page`  
**PR:** [#117](https://github.com/anthonykeevy/EventLeadPlatform/pull/117) (docs) · [#118](https://github.com/anthonykeevy/EventLeadPlatform/pull/118) (implementation) → `develop`  
**Created:** 2026-06-03  
**Size:** M  

---

## 1) Product Decision

Pause the previously planned **6.5e image-to-form / Form Builder vision path** until customer discovery produces clearer signal. The next customer-visible investment is the Test system landing page because Anthony needs a credible URL for discovery, follow-up, and beta account creation.

This story promotes `docs/LANDING-PAGE-BRIEF.md` into the active Epic 6 project plan.

**Why now:**

- Customer discovery is active, but completed interview volume is still low.
- The current `/` homepage exposes developer/test details and does not help prospects understand the product.
- A customer-facing beta landing page supports outreach without committing to speculative Form Builder work.
- The page can test positioning language while staying honest about beta readiness and partial features.

---

## 2) Discovery Alignment

The landing page brief aligns with `docs/customer-discovery/` on the core positioning:

| Discovery source | Alignment in landing page |
|---|---|
| `README.md` scope reframe | Uses **customer engagement forms**, not only event lead capture. |
| Operational/platform lenses | Separates hands-on form-building value from governance, approval, teams, and visibility. |
| Persona A | Speaks to marketing managers, event coordinators, demand gen, and small business users who build/run forms. |
| Persona B | Speaks to marketing operations and enterprise leaders who care about governed workflows. |
| Persona C | Includes agency/client campaign forms and repeatable branded workspaces. |
| `feature-resonance-scorecard.md` | Reuses built/planned feature language and avoids claiming partial features as fully shipped. |
| `tenancy-sharing-and-dashboards.md` | Positions workspaces, roles, approvals, sharing, and dashboards as platform value without overpromising enterprise readiness. |
| `mvp-scope-fix-candidates.md` | Keeps beta and production-critical warnings visible before external use. |

### Messaging Guardrails

- Lead with customer outcomes: faster form launch, branded capture, approval workflow, follow-up visibility.
- Do not lead with developer stack, APIs, multi-tenant architecture, RBAC, or internal test status.
- Do not imply production maturity, enterprise compliance, automatic migration, SSO, SOC 2, DPA, data residency, or custom domains.
- Mark experimental or planned capabilities carefully.
- Use honest beta trust: free beta, suitable for testing and pilots, talk to Signal Platforms before production-critical workflows or sensitive data.

---

## 3) Implementation Scope

### In Scope

- Replace or bypass the existing `/` developer homepage in `frontend/src/App.tsx`.
- Add a customer-facing landing page component, preferably under a dedicated feature area such as `frontend/src/features/marketing/`.
- Add customer-facing copy from `docs/LANDING-PAGE-BRIEF.md` with responsive layout and accessible semantic headings.
- Route primary CTA **Create an account** to `/signup`.
- Route secondary CTA **See example forms** to an in-page examples/use-cases section unless safe public example forms are available.
- Add SEO metadata support for page title, meta description, canonical basics if the app supports it.
- Add crawlable FAQ content and JSON-LD if practical within current frontend architecture.
- Remove developer-only homepage links from the public root route, including API docs, database test, MailHog, environment package versions, and backend health status.
- Add footer links/placeholders for Privacy and Terms only if working pages/URLs exist; otherwise include this as a required follow-up before external promotion.

### Out of Scope

- Building new Form Builder capabilities.
- Image-to-form / vision upload.
- Billing, pricing gates, Stripe, or production migration promises.
- Enterprise procurement features such as SSO, DPA, data residency commitments, custom domains, SOC 2, or formal accessibility reports.
- Real testimonials unless Anthony supplies approved quotes.

---

## 4) Developer Task Plan

| Task | Owner | Deliverable | Notes |
|---|---|---|---|
| T1 | SM | Story pack | Created: `story-context-6.5e-landing.xml`, UAT guide, dev prompt, gate evidence template, friction log template. |
| T2 | Dev | Landing page component | New customer-facing page replacing `HomePage` in `frontend/src/App.tsx` or extracting it into `frontend/src/features/marketing/`. |
| T3 | Dev | CTA routing | Primary CTA to `/signup`; login link available but secondary to account creation. |
| T4 | Dev | SEO/AEO pass | Page title, meta description, one H1, crawlable FAQ, useful image alt text; JSON-LD if feasible. |
| T5 | Dev + Anthony | Safe visuals/examples | Use safe mock UI or approved fake example forms only. No internal/test records. |
| T6 | Dev | Beta trust/footer | Free beta wording, production-critical warning, company name, support/contact, privacy/terms handling. |
| T7 | Dev | Tests/checks | Frontend typecheck/build and targeted tests for routing/rendering if existing test setup supports it. |
| T8 | SM + Anthony | UAT | 10-second comprehension, mobile, CTA route, no dev-only exposure, beta warning visible. |

---

## 5) Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-1 | The root route `/` no longer shows developer environment readiness, package versions, backend health, API docs, database test, MailHog, or local-only instructions. |
| AC-2 | A non-technical visitor can understand within 10 seconds that EventLead helps teams create branded customer engagement forms for events, campaigns, registrations, feedback, and follow-up. |
| AC-3 | The primary CTA **Create an account** is visible above the fold and routes to `/signup`. |
| AC-4 | The secondary CTA **See example forms** scrolls to examples/use cases or routes to a safe public example page if one exists. |
| AC-5 | The page includes operational lens content for hands-on users and platform lens content for managers/agencies without creating separate persona pages. |
| AC-6 | Beta trust wording is visible before account creation and does not promise production readiness or automatic migration. |
| AC-7 | Product claims distinguish shipped, partial, experimental, and planned capabilities where relevant. |
| AC-8 | The page has one H1, logical H2s, page title, meta description, crawlable FAQ content, and useful alt text for visuals. |
| AC-9 | The page works on mobile and passes basic accessibility checks: semantic headings, keyboard navigation, sufficient contrast, and no image-only text. |
| AC-10 | Footer includes Signal Platforms Pty Ltd and either working Privacy/Terms links or an explicit blocker noted before external promotion. |
| AC-11 | No secrets, internal environment details, dev-only links, real customer data, or test records are exposed. |
| AC-12 | Frontend build/typecheck passes, and any existing relevant frontend tests remain green. |

---

## 6) UAT Checklist

- Open the Test system root URL as an unauthenticated visitor.
- Confirm the first screen answers: what it is, who it is for, why it matters, and what to click.
- Click **Create an account** and confirm `/signup` loads.
- Click **See example forms** and confirm the user lands on examples/use cases, not developer docs.
- Scan for overclaims against `feature-resonance-scorecard.md` and `tenancy-sharing-and-dashboards.md`.
- Check mobile layout at narrow width.
- Confirm no developer-only links or environment diagnostics are visible.
- Confirm beta warning is visible and understandable.

---

## 7) Follow-Up Decisions

These do not block starting the story, but they should be tracked before using the URL broadly in outbound:

1. **Brand/name:** Keep `EventLead` as placeholder until Anthony finalises naming.
2. **Privacy and terms:** Decide whether to add simple public pages now or link existing policy documents.
3. **Safe examples:** Decide whether v1 uses stylised mock panels, screenshots from fake forms, or public sample form links.
4. **Contact path:** Decide support/contact email or route.
5. **Production language:** Confirm whether the Test URL can be shared externally as a beta/pilot environment and whether any data-entry restrictions need stronger wording.

---

## 8) References

- `docs/LANDING-PAGE-BRIEF.md`
- `docs/stories/story-context-6.5e-landing.xml`
- `docs/stories/STORY-6.5e-LANDING-SINGLE-SESSION-DEV-PROMPT.md`
- `docs/stories/STORY-6.5e-LANDING-UAT-TEST-GUIDE.md`
- `docs/stories/STORY-6.5e-LANDING-GATE-EVIDENCE.md`
- `docs/stories/STORY-6.5e-LANDING-IMPLEMENTATION-FRICTION-LOG.md`
- `docs/customer-discovery/README.md`
- `docs/customer-discovery/PROGRAM-STATUS.md`
- `docs/customer-discovery/targeting-and-outreach.md`
- `docs/customer-discovery/feature-resonance-scorecard.md`
- `docs/customer-discovery/tenancy-sharing-and-dashboards.md`
- `docs/customer-discovery/mvp-scope-fix-candidates.md`
- `frontend/src/App.tsx`

---

*PM/SM draft — 2026-06-03 — created to support customer discovery and beta account creation while Form Builder vision work waits for customer feedback.*
