# Story 6.5e Landing — UAT Test Guide

**Story:** Customer-Facing Beta Landing Page  
**PR:** [#117](https://github.com/anthonykeevy/EventLeadPlatform/pull/117) — Draft -> `develop`  
**Tester:** Tony  
**Environment:** Local first; Azure Test after merge to `develop`

---

## Prerequisites

1. Dev marks PR Ready for UAT.
2. `STORY-6.5e-LANDING-GATE-EVIDENCE.md` shows frontend build/lint/test status.
3. Backend and frontend are running locally, or Azure Test deployment is complete.
4. Use an unauthenticated browser session first.

No Alembic migration should be required for this story.

---

## A. First Impression

| # | Step | Pass? |
|---|------|-------|
| A1 | Open `/` as an unauthenticated visitor. The page looks like a real customer-facing product page, not an internal development status page. | |
| A2 | Within 10 seconds, confirm the first screen answers: what EventLead is, who it is for, why it matters, and what to click next. | |
| A3 | Hero copy uses customer language around branded customer engagement forms, events, campaigns, approvals, and follow-up. | |
| A4 | No developer stack wording is prominent above the fold: no FastAPI, SQL Server, MailHog, Swagger, health checks, package versions, or local start commands. | |

---

## B. CTA Flow

| # | Step | Pass? |
|---|------|-------|
| B1 | Click **Create an account** in the hero. It routes to `/signup`. | |
| B2 | Return to `/`. Click the bottom CTA if present. It also routes to `/signup`. | |
| B3 | Click **See example forms**. It scrolls/routes to safe examples or use cases, not developer docs. | |
| B4 | Login remains available but does not compete with the primary account-creation CTA. | |

---

## C. Discovery And Claims Alignment

| # | Step | Pass? |
|---|------|-------|
| C1 | Page says "customer engagement forms" or equivalent category language, not only "event lead form builder." | |
| C2 | Page speaks to Persona A hands-on users: build branded forms without developer delays. | |
| C3 | Page speaks to Persona B managers/operations: governance, approval, teams, visibility, follow-up. | |
| C4 | Page speaks to Persona C agencies/service providers: client campaign forms or repeatable branded workspaces. | |
| C5 | Claims do not overstate partial/planned capabilities from `feature-resonance-scorecard.md` and `tenancy-sharing-and-dashboards.md`. | |
| C6 | Beta wording is visible before account creation and does not promise production readiness, enterprise compliance, or automatic migration. | |

---

## D. SEO / AEO / Accessibility

| # | Step | Pass? |
|---|------|-------|
| D1 | Browser title and/or metadata identify EventLead as customer engagement forms for marketing/events. | |
| D2 | Page has exactly one visible H1 and logical H2 sections. | |
| D3 | FAQ content is present in crawlable text and answers: what EventLead is, who it is for, use cases, generic-form-tool difference, beta readiness. | |
| D4 | Product visuals have useful alt text, not generic "screenshot" labels. | |
| D5 | Keyboard navigation reaches CTAs and key links in a sensible order. | |
| D6 | Mobile/narrow viewport remains readable; CTAs are accessible without horizontal scrolling. | |

---

## E. Safety Scan

| # | Step | Pass? |
|---|------|-------|
| E1 | No secrets, internal environment details, local URLs, test user data, or real customer records are visible. | |
| E2 | Footer includes Signal Platforms Pty Ltd and contact/support path if available. | |
| E3 | Privacy/Terms links are present if working pages/URLs exist; otherwise the missing links are recorded as an external-promotion blocker. | |
| E4 | Example visuals/forms use realistic fake data only. | |

---

## Azure Test

After merge to `develop` and Azure Test deployment:

1. Repeat sections A, B, C, and E on the Azure Test root URL.
2. Confirm `/signup` works from Azure Test.
3. Confirm no local-only links or localhost assumptions appear.

---

## Sign-Off Record

Record UAT results in chat and, if failures are found, create follow-up fix tasks/PRs rather than patching locally without tracking.

Suggested result format:

```text
Story 6.5e Landing UAT
Date:
Environment:
A First Impression:
B CTA Flow:
C Discovery/Claims:
D SEO/AEO/Accessibility:
E Safety:
Decision: Pass / Fail
Notes:
```

---

*SM pack — 2026-06-03.*
