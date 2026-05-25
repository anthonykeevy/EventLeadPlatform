# Story 6.5d — UAT Test Guide

**Story:** Clarification Data Plane + Component Catalog Completion  
**PR:** [#109](https://github.com/anthonykeevy/EventLeadPlatform/pull/109)  
**Tester:** Tony  
**Environment:** LocalDB first; Azure Test after merge to `develop`

---

## Prerequisites

1. Dev marks PR Ready; `STORY-6.5d-GATE-EVIDENCE.md` shows focused + full pytest green.
2. **Tony:** `alembic upgrade head` from revision **086** → new head (Dev lists exact revisions in closeout).
3. Backend + frontend running (usual local stack).
4. AU company/event fixture Dev documents in closeout (company id, event id, country).

---

## Track A — Component catalog

| # | Step | Pass? |
|---|------|-------|
| A1 | Open Form Builder on **AU** event. Toolbox includes: `rating`, `url`, `file-upload`, `paragraph`, `address`, and **AU address lookup** (label per UI). | |
| A2 | Open builder on **non-AU** context (if available). AU-only `address-lookup-au` **not** in toolbox. | |
| A3 | Drag new types to canvas; preview/runtime render without console errors. | |
| A4 | AI generate: prompt uses new types when appropriate; no `unknown-component-type` / validator rejection. | |
| A5 | Dev runs `python backend/scripts/verify_component_catalog_alignment.py` — paste PASS output in `STORY-6.5d-UAT-RESULTS.md`. | |

---

## Track B — Clarification dropdowns

| # | Step | Pass? |
|---|------|-------|
| B1 | AI Agent panel shows **Audience**, **Form purpose**, **Respondent** dropdowns populated from API (not hardcoded enum labels only). | |
| B2 | Change each dropdown; generate form — request succeeds; no 422 on clarification fields. | |
| B3 | Reload form / panel — selections restore from Form persistence where implemented. | |
| B4 | Company defaults apply when form fields null (Dev documents test company). | |
| B5 | Inspect `GenerationRun` row after generate — clarification codes/FKs stored (Dev provides query or admin note). | |

---

## Regression

| # | Step | Pass? |
|---|------|-------|
| R1 | Toolbox still init-only (no static ghost palette). | |
| R2 | Brand posture / Block C still works (6.5c). | |
| R3 | Registry path still generates on Azure-equivalent config (local smoke). | |

---

## Azure Test (post-merge)

Repeat A1–B2 on `signalplatforms-test` after PR merges to `develop` and deploy completes.

---

## Sign-off

Record in `docs/stories/STORY-6.5d-UAT-RESULTS.md`:

- Date, environment, pass/fail per section
- Migration head applied
- Any defects → new fix task + task PR (not local-only patches)

---

*SM pack — 2026-05-21.*
