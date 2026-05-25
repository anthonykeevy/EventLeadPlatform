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
| A1 | Open Form Builder on **AU** event. Toolbox includes: `rating`, `url`, `file-upload`, `paragraph`, `address`, and **AU address lookup** (label per UI). | **Pass** |
| A2 | Open builder on **non-AU** context (if available). AU-only `address-lookup-au` **not** in toolbox. | **Pass** |
| A3 | Drag new types to canvas; preview/runtime render without console errors. | **Pass** |
| A4 | AI generate: prompt uses new types when appropriate; no `unknown-component-type` / validator rejection. | **Pass** — prompt must explicitly request AU-specific components or AI defaults to text fields |
| A5 | Dev runs `python backend/scripts/verify_component_catalog_alignment.py` — paste PASS output in `STORY-6.5d-UAT-RESULTS.md`. | **Pass** — see results doc |

---

## Track B — Clarification dropdowns

| # | Step | Pass? |
|---|------|-------|
| B1 | AI Agent panel shows **Audience**, **Form purpose**, **Respondent** dropdowns populated from API (not hardcoded enum labels only). | **Pass** |
| B2 | Change each dropdown; generate form — request succeeds; no 422 on clarification fields. | **Pass** |
| B3 | Reload form / panel — selections restore from Form persistence where implemented. | **Pass** |
| B4 | Company defaults apply when form fields null (Dev documents test company). | **Pass** |
| B5 | Inspect `GenerationRun` row after generate — clarification codes/FKs stored (Dev provides query or admin note). | **Pass** — see results doc |

---

## Regression

| # | Step | Pass? |
|---|------|-------|
| R1 | Toolbox still init-only (no static ghost palette). | **Pass** |
| R2 | Brand posture / Block C still works (6.5c). | **Pass** |
| R3 | Registry path still generates on Azure-equivalent config (local smoke). | **Pass** |

---

## B4 / B5 how-to

These are backend-persistence checks. B1–B3 already prove the UI + generate path works; B4/B5 confirm **where** the selected values land in SQL.

### B4 — Company defaults when form fields are null

**What it tests:** If a form has no saved clarification codes (`Form.AudienceLocaleCode` etc. are NULL), the AI panel should pre-select the **company** defaults — not only the hardcoded fallbacks (`AU`, `EVENT_REGISTRATION`, `ATTENDEE`).

**Resolution order:** request (panel selection) → form snapshot → **company defaults** → fallback.

**Steps:**

1. Pick a test company (local fixture: **CompanyID = 1**, Signal Platforms).
2. Set company defaults (SSMS or one-off SQL):

```sql
UPDATE dbo.Company
SET DefaultAudienceLocaleCode = N'AU',
    DefaultFormPurposeCode = N'LEAD_CAPTURE',
    DefaultRespondentTypeCode = N'PROSPECT'
WHERE CompanyID = 1 AND IsDeleted = 0;
```

3. Open a form under that company where clarification columns are NULL (e.g. Form 504 after reset, or a new form).
4. Open the AI Agent panel **without** changing dropdowns first.
5. **Pass if:** Audience / Form purpose / Respondent default to `AU` / `Lead capture` / `Prospect` (or whatever you set), not only generic fallbacks.
6. Optional API check:

```http
GET /api/ref/form-purposes?formId=504
```

Response `defaultCode` should reflect company default when form snapshot is null.

**Note:** At UAT time CompanyID 1 had **NULL** company defaults, so this scenario was not exercised in the UI yet.

### B5 — GenerationRun audit columns

**What it tests:** Each successful generate writes the three clarification codes to `dbo.GenerationRun` for audit/replay.

**Steps:**

1. Run a generate from the AI panel with known selections (you already did this for B2).
2. Note the `generationRunId` from the network response, **or** query the latest row:

```sql
SELECT TOP 5
    GenerationRunID,
    FormID,
    CreatedDate,
    AudienceLocaleCode,
    FormPurposeCode,
    RespondentTypeCode
FROM dbo.GenerationRun
ORDER BY GenerationRunID DESC;
```

3. **Pass if:** the row for your run has non-NULL codes matching what you selected in the panel.

**Agent spot-check (2026-05-25):** Runs **170** and **171** (Form 504) show stored codes, e.g. `TRAINING_PROFESSIONAL` / `PARTICIPANT` and `EVENT_REGISTRATION` / `ATTENDEE`. Run **169** (pre-migration / older path) has NULLs — useful baseline comparison.

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
