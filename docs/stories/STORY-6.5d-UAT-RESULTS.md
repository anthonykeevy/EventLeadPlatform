# Story 6.5d — UAT Results

**Story:** Clarification Data Plane + Component Catalog Completion  
**Tester:** Tony  
**Environment:** Local (LocalDB)  
**Date:** 2026-05-25  
**PR:** [#109](https://github.com/anthonykeevy/EventLeadPlatform/pull/109)

---

## Migration head applied

Tony applied migrations **086 → 095** (UAT executed 2026-05-25).

---

## Track A — Component catalog

| # | Result | Notes |
|---|--------|-------|
| A1 | **Passed** | AU Form Builder toolbox includes backlog types (`rating`, `url`, `file-upload`, `paragraph`, `address`) plus AU EDF components (`address-lookup-au`, `company-lookup-abr`). |
| A2 | **Passed** | Non-AU context excludes AU-only `address-lookup-au` / `company-lookup-abr`. |
| A3 | **Passed** | New types drag to canvas; preview/runtime render without console errors. |
| A4 | **Passed** | AI generate accepts new component types when appropriate. **Note:** prompt must explicitly request AU-specific components (e.g. address lookup, ABR company lookup); otherwise the model tends to propose plain text fields instead. |
| A5 | **Passed** | Catalog alignment gate — see output below. |

### A5 — `verify_component_catalog_alignment.py` output

```text
CATALOG ALIGNMENT OK — 21 codes (company=1, country=1, form=None)
  codes: address, address-lookup-au, checkbox, company-lookup-abr, date, divider, dropdown, email, file-upload, first-name, header, number, paragraph, phone, radio, rating, submit-button, terms, text, textarea, url
```

Command:

```powershell
cd backend
python scripts/verify_component_catalog_alignment.py
```

Script: `backend/scripts/verify_component_catalog_alignment.py` (Story 6.5d AC-3 four-consumer alignment gate).

---

## Track B — Clarification dropdowns

| # | Result | Notes |
|---|--------|-------|
| B1 | **Passed** | AI Agent panel shows Audience, Form purpose, and Respondent dropdowns populated from ref APIs. |
| B2 | **Passed** | Changed each dropdown; generate succeeded; no 422 on clarification fields. |
| B3 | **Passed** | Reload form / panel — selections restore from Form persistence. |
| B4 | **Passed** | Company defaults apply when form clarification columns are NULL. |
| B5 | **Passed** | GenerationRun audit columns populated after generate — see query output below. |

### B5 — `GenerationRun` query output (Tony)

```text
GenerationRunID  FormID  CreatedDate                      AudienceLocaleCode  FormPurposeCode        RespondentTypeCode
171              504     2026-05-21 12:00:12.5466667      AU                  EVENT_REGISTRATION     ATTENDEE
170              504     2026-05-21 11:41:37.0066667      AU                  TRAINING_PROFESSIONAL  PARTICIPANT
169              504     2026-05-21 00:50:24.2200000      NULL                NULL                   NULL
168              504     2026-05-21 00:50:04.4000000      NULL                NULL                   NULL
167              813     2026-05-20 05:42:31.4566667      NULL                NULL                   NULL
```

Runs **170–171** store clarification codes matching B2 panel selections. Runs **167–169** are pre-fix baseline (NULL codes).

---

## Regression

| # | Result | Notes |
|---|--------|-------|
| R1 | **Passed** | Toolbox still init-only (no static ghost palette). |
| R2 | **Passed** | Brand posture / Block C still works (6.5c). |
| R3 | **Passed** | Registry path still generates (local smoke). |

---

## Azure Test (post-merge)

Not yet run.

---

## Defects / follow-ups

None recorded — Track A, Track B, and Regression all passed (local).

---

*Updated 2026-05-25 — Full local UAT sign-off (Track A, Track B, Regression).*
