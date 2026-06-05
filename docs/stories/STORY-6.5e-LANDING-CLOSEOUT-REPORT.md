# Story 6.5e Landing — Closeout Report

**Story:** 6.5e — Customer-Facing Beta Landing Page  
**Date:** 2026-06-04  
**Status:** ✅ **Complete** — Local + Azure Test UAT pass; Tony sign-off  
**PRs:** [#117](https://github.com/anthonykeevy/EventLeadPlatform/pull/117) (story pack/docs) · [#118](https://github.com/anthonykeevy/EventLeadPlatform/pull/118) (implementation) → `develop`

---

## 1. Story outcome

The public root route `/` on the Test system is now a **customer-facing beta landing page** (`BetaLandingPage` in `frontend/src/features/marketing/`). Developer diagnostics (API health, Swagger, MailHog, package versions, local start commands) are no longer shown to unauthenticated visitors.

Primary and secondary CTAs route correctly; interim **Privacy** and **Terms** pages are linked from the footer; SEO/AEO basics (title, meta, H1, FAQ, JSON-LD) are in place. Safe **mock use-case tiles** ship in v1; eight live builder demo forms remain deferred follow-up (`docs/LANDING-PAGE-SAFE-EXAMPLE-FORMS.md`).

---

## 2. Evidence summary

| Artefact | Path | Result |
|----------|------|--------|
| Story pack | `story-6.5e-landing-page.md`, `story-context-6.5e-landing.xml` | Complete |
| Dev prompt | `STORY-6.5e-LANDING-SINGLE-SESSION-DEV-PROMPT.md` | Followed |
| Preflight | `STORY-6.5e-LANDING-PREFLIGHT.md` | PASS |
| Gate evidence | `STORY-6.5e-LANDING-GATE-EVIDENCE.md` | Complete |
| UAT guide | `STORY-6.5e-LANDING-UAT-TEST-GUIDE.md` | Used for local + Azure Test |
| Friction log | `STORY-6.5e-LANDING-IMPLEMENTATION-FRICTION-LOG.md` | PR #117 docs-only merge noted |
| Targeted tests | `npx vitest run src/features/marketing src/features/auth/utils/__tests__` | **13/13 PASS** |
| Vite bundle | `npx vite build` | **PASS** |

---

## 3. UAT results

### Local (2026-06-04)

| Section | Result |
|---------|--------|
| A — First impression | **Pass** |
| B — CTA flow | **Pass** |
| C — Discovery/claims | **Pass** |
| D — SEO/AEO/accessibility | **Pass** |
| E — Safety scan | **Pass** |

### Azure Test — https://test.signalplatforms.com.au/ (2026-06-04)

| Section | Result | Notes |
|---------|--------|-------|
| A — First impression | **Pass** | Customer-facing root; no dev diagnostics |
| B — CTA flow | **Pass** | Create account → `/signup`; signup and login CTAs work |
| C — Discovery/claims | **Pass** | |
| D — SEO/AEO/accessibility | Not re-run on Azure | Covered in local UAT |
| E — Safety scan | **Pass** | |

**Decision:** **Pass** — story acceptance criteria met for landing scope.

---

## 4. Out-of-scope issue observed on Azure Test (carry-forward)

| ID | Issue | Environment | In 6.5e scope? | Recommended follow-up |
|----|-------|-------------|----------------|---------------------|
| **CF-1** | **Background image cannot be uploaded** (builder/form background asset upload fails) | Azure Test | **No** — not part of landing ACs; observed during broader smoke only | Open a **fix task + PR** (likely company assets / blob storage / test slot config). Do not block 6.5e closeout. |

**CF-1 notes (Tony):** Reproduced on Test after landing deploy. Not investigated in this story. Suspect Azure Blob / `STORAGE_*` app settings, CORS, or upload API path on the test slot — confirm via API logs and `enhanced_diagnostic_logs.py` on a dedicated fix branch.

---

## 5. Deferred follow-ups (non-blocking)

| Item | Rationale |
|------|-----------|
| Eight safe public example forms + screenshots | `LANDING-PAGE-SAFE-EXAMPLE-FORMS.md`; v1 uses mock tiles only |
| Migration `096` + demo seed on Test | Optional; not required for landing UAT |
| Privacy/Terms legal review | Interim beta notices; review before broad external promotion |
| Repo-wide `npm run build` (`tsc`) failures | Pre-existing; unrelated to marketing feature |
| **CF-1** background image upload on Test | See §4 |

---

## 6. Sign-off

| Role | Name | Date | Decision |
|------|------|------|----------|
| UAT | Anthony | 2026-06-04 | **Pass** (landing); CF-1 logged out-of-scope |
| Dev closeout | Agent session | 2026-06-04 | Story complete on `develop` after PR #118 |

---

*Story 6.5e Landing closeout — 2026-06-04.*
