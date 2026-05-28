# Story 6.5e-vision — UAT Test Guide

**Story:** Component Platform Hardening + Image-to-Form Vision Path  
**PR:** *(link when Dev marks Ready)*  
**Tester:** Tony  
**Environment:** LocalDB first; Azure Test after merge to `develop`

---

## Prerequisites

1. Dev marks PR Ready; `STORY-6.5e-vision-GATE-EVIDENCE.md` shows focused pytest green.
2. **Tony:** `alembic upgrade head` from **095** → new head (Dev lists revisions in closeout).
3. Backend + frontend running (usual local stack).
4. Sample images prepared:
   - Clean **screenshot** of a competitor/web form (PNG, readable text).
   - **Photo** of a paper form (optional — expect lower quality).
   - **Non-form** image (optional negative test).

---

## Track 0 — Platform hardening

| # | Step | Pass? |
|---|------|-------|
| T0-1 | Open `ADD-COMPONENT-TO-PLATFORM-CHECKLIST.md` — version **1.3**, §0c present. | |
| T0-2 | Dev runs `python backend/scripts/verify_edf_props_wired.py` — paste PASS in `STORY-6.5e-vision-UAT-RESULTS.md`. | |
| T0-3 | Dev runs `python backend/scripts/verify_component_catalog_alignment.py` — still **21 codes** PASS. | |
| T0-4 | *(Stretch)* Address manual fallback on `address-lookup-au` — search → manual path → submit → JSON. | |
| T0-5 | *(Stretch)* AI panel shows hint/chip to request AU EDF types in text generate. | |

---

## Track 1 — Image-to-form

| # | Step | Pass? |
|---|------|-------|
| V1 | AI Agent panel: attach image (screenshot) + optional text hint → **Generate**. Request succeeds (no 422). | |
| V2 | Generated form appears on canvas; fields match visible structure (labels/types plausible). | |
| V3 | No `unknown-component-type` in UI/console; toolbox types are catalog-resident only. | |
| V4 | **Canvas preservation:** Set non-default canvas width, add one field, generate from image on non-empty canvas — **canvas width unchanged**. | |
| V5 | Empty canvas + image generate — uses default canvas (not image pixel dimensions). | |
| V6 | Replace-form warning shows when canvas non-empty (image + text paths). | |
| V7 | `GenerationRun` row shows `generation_source` = image (Dev provides query). | |
| V8 | Text-only generate still works (regression smoke). | |
| V9 | Clarification dropdowns still populate from ref APIs when panel used with image mode. | |
| V10 | *(Negative)* Non-form image → clear error or empty-plan message, no crash. | |

### Vision quality bar (feasibility §3.1)

Use **≥4 of 5** fixture images producing usable forms to keep GPT-5 mini. If below bar, document in UAT results and whether Dev enabled image-only model fallback.

| Fixture | Usable form? | Notes |
|---------|--------------|-------|
| 1 Web form screenshot | | |
| 2 Lead-gen screenshot | | |
| 3 Survey screenshot | | |
| 4 Paper photo | | |
| 5 Dense registration form | | |

---

## Regression

| # | Step | Pass? |
|---|------|-------|
| R1 | 6.5d clarification dropdowns + generate with codes. | |
| R2 | EDF company + address on published AU form (portal layering). | |
| R3 | Init-only toolbox (no ghost palette). | |

---

## Azure Test (post-merge)

Repeat **T0-2**, **T0-3**, **V1–V4**, **R1–R3** on `signalplatforms-test` after deploy.

---

## Results doc

Record outcomes in `docs/stories/STORY-6.5e-vision-UAT-RESULTS.md`.

---

*SM pack — 2026-05-28*
