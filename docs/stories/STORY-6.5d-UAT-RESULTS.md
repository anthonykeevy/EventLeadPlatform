# Story 6.5d — UAT Results

**Story:** Clarification Data Plane + Component Catalog Completion  
**Tester:** Tony

---

## Local UAT (LocalDB)

**Environment:** Local (LocalDB)  
**Date:** 2026-05-25  
**PR:** [#109](https://github.com/anthonykeevy/EventLeadPlatform/pull/109) (docs/story scope)

### Migration head applied

Tony applied migrations **086 → 095** (UAT executed 2026-05-25).

### Track A — Component catalog

| # | Result | Notes |
|---|--------|-------|
| A1 | **Passed** | AU Form Builder toolbox includes backlog types (`rating`, `url`, `file-upload`, `paragraph`, `address`) plus AU EDF components (`address-lookup-au`, `company-lookup-abr`). |
| A2 | **Passed** | Non-AU context excludes AU-only `address-lookup-au` / `company-lookup-abr`. |
| A3 | **Passed** | New types drag to canvas; preview/runtime render without console errors. |
| A4 | **Passed** | AI generate accepts new component types when appropriate. **Note:** prompt must explicitly request AU-specific components (e.g. address lookup, ABR company lookup); otherwise the model tends to propose plain text fields instead. |
| A5 | **Passed** | Catalog alignment gate — see output below. |

#### A5 — `verify_component_catalog_alignment.py` output

```text
CATALOG ALIGNMENT OK — 21 codes (company=1, country=1, form=None)
  codes: address, address-lookup-au, checkbox, company-lookup-abr, date, divider, dropdown, email, file-upload, first-name, header, number, paragraph, phone, radio, rating, submit-button, terms, text, textarea, url
```

```powershell
cd backend
python scripts/verify_component_catalog_alignment.py
```

### Track B — Clarification dropdowns

| # | Result | Notes |
|---|--------|-------|
| B1 | **Passed** | AI Agent panel shows Audience, Form purpose, and Respondent dropdowns populated from ref APIs. |
| B2 | **Passed** | Changed each dropdown; generate succeeded; no 422 on clarification fields. |
| B3 | **Passed** | Reload form / panel — selections restore from Form persistence. |
| B4 | **Passed** | Company defaults apply when form clarification columns are NULL. |
| B5 | **Passed** | GenerationRun audit columns populated after generate — see query output below. |

#### B5 — `GenerationRun` query output (Tony)

```text
GenerationRunID  FormID  CreatedDate                      AudienceLocaleCode  FormPurposeCode        RespondentTypeCode
171              504     2026-05-21 12:00:12.5466667      AU                  EVENT_REGISTRATION     ATTENDEE
170              504     2026-05-21 11:41:37.0066667      AU                  TRAINING_PROFESSIONAL  PARTICIPANT
169              504     2026-05-21 00:50:24.2200000      NULL                NULL                   NULL
```

Runs **170–171** store clarification codes matching B2 panel selections.

### Regression (local)

| # | Result | Notes |
|---|--------|-------|
| R1 | **Passed** | Toolbox still init-only (no static ghost palette). |
| R2 | **Passed** | Brand posture / Block C still works (6.5c). |
| R3 | **Passed** | Registry path still generates (local smoke). |

---

## Azure Test UAT

**Environment:** `signalplatforms-test` (Test slot)  
**Date:** 2026-05-26  
**Deploy PRs:** [#111](https://github.com/anthonykeevy/EventLeadPlatform/pull/111) (T01 implementation), [#112](https://github.com/anthonykeevy/EventLeadPlatform/pull/112) (T02 EDF overlay / dark theme / GeoScape UAT)

### Preconditions verified

| Item | Result | Notes |
|------|--------|-------|
| Alembic head **095** on Test DB | **OK** | After T01 deploy + app restart (was stuck at 086 before T01). |
| `GEOSCAPE_API_KEY` in App Service Configuration | **OK** | Address search works after key saved + restart. |
| Catalog toolbox (21 codes) | **OK** | AU EDF components visible in builder. |

### Track A / B (Test)

| Area | Result | Notes |
|------|--------|-------|
| Track A (catalog + EDF on Test) | **Passed** | Toolbox, drag/drop, published form render for AU EDF pair. |
| Track B (clarification dropdowns) | **Passed** | Ref APIs + AI panel dropdowns on Test. |
| Regression (init-only toolbox, generate) | **Passed** | No regressions observed on Test. |

### EDF UAT fixes (T02 — [#112](https://github.com/anthonykeevy/EventLeadPlatform/pull/112))

| # | Result | Notes |
|---|--------|-------|
| E1 | **Passed** | Company lookup dropdown appears **above** address field on published form (overlay root + field z-index lift). |
| E2 | **Passed** | Address lookup readable with account **Dark Theme** (`dark:text` on result rows via `edfLookupStyles.ts`). |
| E3 | **Passed** | GeoScape address search + resolve on Test after `GEOSCAPE_API_KEY` configured. |
| E4 | **Passed** | Company lookup dark-theme contrast unchanged (shared result-row styles). |

### Defects / follow-ups (Test)

None — full Test sign-off after T02 deploy.

---

## Summary

| Environment | Date | Result |
|-------------|------|--------|
| Local (LocalDB) | 2026-05-25 | **Pass** — Track A, Track B, Regression |
| Azure Test | 2026-05-26 | **Pass** — Track A/B, Regression, EDF overlay + dark theme (T02) |

---

*Updated 2026-05-26 — Local + Azure Test UAT sign-off.*
