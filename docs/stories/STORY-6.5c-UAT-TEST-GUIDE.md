# Story 6.5c — UAT Test Guide

**Story:** 6.5c — Capability Catalog Cutover  
**UAT owner:** Tony + SM  
**Environment:** LocalDB first, then Azure Test after merge to `develop`

---

## Section 1 — Migration & ref.BrandPosture

Pass criteria:

- Migrations `084+` applied (`alembic upgrade head`).
- `ref.BrandPosture` has four active rows (`local`, `heritage`, `neutral`, `transcreate`).
- Company posture resolves through ref table (spot-check in SSMS).

**Section 1 Final:** Pass / Fail

---

## Section 2 — Toolbox ↔ Init alignment

Pass criteria:

- Open Form Builder for an **AU** company/event.
- Toolbox shows only component types returned by init (no extra static types).
- Note `componentCode` list from browser network tab (`POST /api/form-builder/init`).

**Section 2 Final:** Pass / Fail

---

## Section 3 — AI prompt ↔ toolbox alignment

Pass criteria:

- Same AU context: run **Generate Form Draft** with a prompt that needs address/email/phone.
- AI panel trace shows ALLOWED COMPONENT TYPES matching Section 2 toolbox codes.
- Generation succeeds without `unknown-component-type` for types visible in toolbox.
- No regression: no `context-pack-load-failed` / `prompt-assembly-resolution-failed`.

**Section 3 Final:** Pass / Fail

---

## Section 4 — Country scope change

Pass criteria:

- Switch to a non-AU event (or company) where AU-only components should not apply.
- Re-load builder: AU-only codes (e.g. `address-lookup-au` if applicable) **absent** from toolbox and from a new generation trace.

**Section 4 Final:** Pass / Fail

---

## Section 5 — Brand posture

Pass criteria:

- Change brand posture (if UI exposed) or via API; generation uses correct Block C variant prose.
- `GenerationRun` / snapshot records posture resolution source.

**Section 5 Final:** Pass / Fail / N/A

---

## Section 6 — Automated gates

Review `STORY-6.5c-GATE-EVIDENCE.md` — focused + full pytest summaries.

**Section 6 Final:** Pass / Fail

---

## Section 7 — Test environment (post-merge)

After merge to `develop` and deploy:

- Repeat Sections 2–3 on `signalplatforms-test`.
- Confirm catalog alignment holds in deployed Test.

**Section 7 Final:** Pass / Fail

---

## UAT Result Summary

| Section | Result | Notes |
|---|---|---|
| 1 Migrations / ref.BrandPosture | _Pending_ | |
| 2 Toolbox ↔ init | _Pending_ | |
| 3 AI prompt ↔ toolbox | _Pending_ | |
| 4 Country scope | _Pending_ | |
| 5 Brand posture | _Pending_ | |
| 6 Automated gates | _Pending_ | |
| 7 Azure Test | _Pending_ | |

**Final:** _Pending_
