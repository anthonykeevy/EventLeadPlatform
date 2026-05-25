# Story 6.5d — Closeout Report

**Story:** Clarification Data Plane + Component Catalog Completion  
**Date:** 2026-05-25  
**Status:** ✅ **Dev complete — Ready for SM review / merge** (PR [#109](https://github.com/anthonykeevy/EventLeadPlatform/pull/109) Draft → `develop`)  
**Dev complete:** 2026-05-25 · **Merged:** pending PR #109  
**Worktree:** `C:\wt\elp\story-epic6-6.5d-clarification-component-platform`

---

## 1. Story outcome

Story 6.5d delivered **two tracks** in one PR:

### Track A — Component catalog + EDF reference pair

- Seeded global catalog backlog: `rating`, `url`, `file-upload`, `paragraph`, `address`
- Seeded AU country-scoped EDF pair: `address-lookup-au`, `company-lookup-abr`
- `RequiresNetwork` + offline resolver filter; GeoScape + ABR proxy APIs
- `ADD-COMPONENT-TO-PLATFORM-CHECKLIST.md` + `verify_component_catalog_alignment.py` (21 codes aligned)
- **Full EDF runtime UX** for both AU components (not registry stubs — see §4)

### Track B — Clarification data plane

- `ref.AudienceLocale`, `ref.FormPurpose`, `ref.RespondentType` + seeds
- Ref APIs with Company → Form → request resolution chain
- Block E (E1/E2/E3) in Prompt Assembly Registry
- AI Agent panel API-driven dropdowns; `AudienceLocale` enum removed from generation path
- `Company` / `Form` / `GenerationRun` clarification persistence + audit

**Key achievement:** Catalog, AI, validator, and toolbox agree on 21 component codes for AU fixture; clarification dropdowns are data-driven end-to-end with audit on `GenerationRun`.

---

## 2. Evidence summary

| Artefact | Path | Result |
|----------|------|--------|
| Preflight | `STORY-6.5d-PREFLIGHT.md` | PASS |
| Migrations | `087`–`095` | Tony applied LocalDB (UAT executed) |
| Focused pytest | 6.5d + 6.5c regression | **11/11 PASS** (2026-05-25) |
| Catalog alignment | `verify_component_catalog_alignment.py` | **PASS** — 21 codes |
| Gate evidence | `STORY-6.5d-GATE-EVIDENCE.md` | Updated |
| UAT | `STORY-6.5d-UAT-RESULTS.md` | Track A, Track B, Regression **Pass** (local) |
| Friction log | `STORY-6.5d-IMPLEMENTATION-FRICTION-LOG.md` | Complete |

---

## 3. Migrations (Tony executes)

| Rev | File | Purpose |
|-----|------|---------|
| 087 | `087_story_6_5d_seed_global_catalog_backlog.py` | Global seeds: `rating`, `url`, `file-upload`, `paragraph`, `address` |
| 088 | `088_story_6_5d_edf_schema_and_au_components.py` | `RequiresNetwork`, `Form.RequiresOfflineCapable`, `cache.AddressSearch`, AU EDF pair |
| 089 | `089_story_6_5d_ref_audience_locale.py` | `ref.AudienceLocale` + 11 seeds |
| 090 | `090_story_6_5d_ref_form_purpose.py` | `ref.FormPurpose` + 10 seeds |
| 091 | `091_story_6_5d_ref_respondent_type.py` | `ref.RespondentType` + 9 seeds |
| 092 | `092_story_6_5d_clarification_company_form_columns.py` | Company defaults + Form persist codes |
| 093 | `093_story_6_5d_generation_run_clarification_audit.py` | GenerationRun audit columns |
| 094 | `094_story_6_5d_block_e_clarification_registry.py` | Block E1/E2/E3 (`Refs`) |
| 095 | `095_story_6_5d_block_g_catalog_aligned_note.py` | Block G catalog-alignment note |

```powershell
cd backend
alembic upgrade head
```

---

## 4. APIs

| Endpoint | Purpose |
|----------|---------|
| `GET /api/ref/audience-locales?formId=` | Clarification dropdown + resolved default |
| `GET /api/ref/form-purposes?formId=` | Form purpose list + default |
| `GET /api/ref/respondent-types?formId=` | Respondent type list + default |
| `GET /api/external-feed/address-au/search?q=` | GeoScape proxy (requires `GEOSCAPE_API_KEY`) |
| `POST /api/external-feed/address-au/resolve` | PSMA id → structured lines + cache |
| `POST /api/external-feed/company-abr/search` | ABR smart-search proxy |

---

## 5. EDF components — scope delivered vs UAT follow-on work

Initial implementation landed catalog seeds, proxy APIs, and registry runtimes. **UAT exposed that EDF components need substantially more than checklist §1–4 (DB + registry stub).** The following was required to reach production-quality behaviour for `company-lookup-abr` and `address-lookup-au`:

### Shared EDF infrastructure

| Item | What we had to do |
|------|-------------------|
| Floating UI layering | Published forms use absolute positioning; inline dropdowns/panels were painted over by later fields. Generalized **`EdfAnchorPortal`** (portaled to `document.body`, z-index 10000) for all EDF overlays. |
| Scaled preview/runtime | `PublicFormArtboard` applies `transform: scale()`; portaled UI rendered at browser 1:1 scale. Added **`artboardScale`** prop + **auto-detect scale** from anchor `offsetWidth` vs `getBoundingClientRect()`. |
| Validation display | Runtime rendered `helpText` with error styling by default. Errors now only via `error` prop after submit trigger; **`edfFieldValue` / `validationEngine`** empty checks for lookup types. |
| Form reset | Company field repopulated after submit reset (auto-select). **`skipAutoSelectRef`** + **`key={componentId-sessionId}`** remount on session rotate. |
| Typography parity | Manual panel initially used Tailwind `rem` spacing + input typography for labels. Aligned to **`fieldStyles.labelStyle`** and theme-derived inline spacing. |

### `company-lookup-abr` specific

| Item | What we had to do |
|------|-------------------|
| Manual fallback | `allowManualFallback` saved in properties but **not read** in runtime; zero-result state did not open panel. Wired **`CompanyManualEntryPanel`**, no-results/API-error links, **`buildManualCompanyValue()`**. |
| Manual entry loop | Typing in Trading as caused **Maximum update depth exceeded** (`useEffect` → `onChange` on every keystroke). Replaced with handler-driven updates + **`skipExternalSyncRef`**. |
| Manual capture UX | Back-to-search cleared values; no confirm step. Added **“Use this company”** button; committed manual value shows in main input with edit link. |
| ABR result richness | Backend extended for **`business_names`**, **`matched_name`**, **`match_type`**; frontend subtitles + status badges. |
| Inactive ABN | **`warnOnInactiveAbn`** badges + post-select banner; **`blockOnInactiveAbn`** submit validation in `PublicFormArtboard`. |
| Phone co-testing | National `0412345678` failed without `+61`; default **`countryCode: 'AU'`** when `countryCodeRequired !== true`. |

### `address-lookup-au` specific

| Item | What we had to do |
|------|-------------------|
| Portal parity | Address dropdown moved to **`EdfAnchorPortal`** with `contentScale` (same scale fix as company). |
| Manual fallback | **Not implemented** — only company has manual-entry UI. Fallback remains plain `address` component per architecture. |

### Submission proof (Tony UAT)

Form submission **#322** captured manual company as structured JSON:

```json
{
  "displayText": "Western Groceries Pty Ltd",
  "validationSource": "manual",
  "legalEntityName": "Western Groceries Pty Ltd",
  "abn": null,
  "matchType": "manual",
  "tradingAs": "Western Supplies"
}
```

Address resolved via Geoscape with `validationSource: "geoscape"` and `psmaAddressId`.

---

## 6. Component checklist improvements (recommended)

See **`docs/workflows/ADD-COMPONENT-TO-PLATFORM-CHECKLIST.md` §0b** (added in this closeout). Summary:

1. **Properties ↔ runtime wiring audit** — grep every prop in `PropertiesSchemaJSON` against runtime reads (manual fallback was saved but unused).
2. **EDF floating UI rule** — any overlay beyond the field box must use `EdfAnchorPortal`; verify on scaled `PublicFormArtboard`.
3. **End-to-end UAT script** — search → select → manual fallback (if applicable) → submit → inspect `FormSubmission.AnswersJSON` structured payload.
4. **Validation matrix** — empty, invalid, inactive/block flags, reset-after-submit, error-only-after-trigger.
5. **No `useEffect` → `onChange` sync loops** for controlled lookup state.
6. **AI prompt note** — AU EDF types must be **explicitly requested** in generate prompt or LLM defaults to plain `text` fields (UAT A4).

---

## 7. Tony / UAT record

| Section | Result | Notes |
|---------|--------|-------|
| Track A A1–A5 | **Pass** | Catalog + alignment script; A4 needs explicit AU component prompt |
| Track B B1–B5 | **Pass** | GenerationRun 170–171 store clarification codes |
| Regression R1–R3 | **Pass** | Init-only toolbox; Block C; registry generate |
| Azure Test | Pending | Post-merge to `develop` |

Full detail: `STORY-6.5d-UAT-RESULTS.md`.

---

## 8. Carry-forward backlog

| ID | Description | Severity | Suggested home |
|----|-------------|----------|----------------|
| `g-65d-address-manual-fallback` | Address lookup manual entry UI (company pattern exists; address still uses plain `address` fallback only). | P3 | Future EDF story or 6.5d follow-up task |
| `g-65d-editable-legal-name` | `editableLegalNameAfterResolve` property not implemented on `company-lookup-abr`. | P3 | EDF polish task |
| `g-65d-azure-uat` | Repeat A1–B2 on `signalplatforms-test` after merge. | P1 pre-prod | Tony post-merge |

**Resolved this story:** `g-65-catalog-drift` (absorbed by 6.5d Track A).

---

## 9. Risks & mitigations

| Risk | Mitigation |
|------|------------|
| EDF components underestimated vs checklist | §0b EDF runtime parity added to checklist; friction log documents pattern |
| AI omits AU EDF types without explicit prompt | Document in generate UX / few-shot examples; Block G already catalog-aligned |
| Portaled UI scale regressions | Auto-detect anchor scale in `EdfAnchorPortal` |
| Full pytest not re-run post-UAT fixes | CI on PR #109; recommend full `pytest` before merge |

---

## 10. Definition of done status

- [x] Track A catalog seeds + EDF pair + alignment automation
- [x] Track B ref tables, APIs, Block E, panel dropdowns, persistence
- [x] EDF runtime UX UAT green (company + address; manual company submit verified)
- [x] Migrations 087–095 authored; Tony applied LocalDB
- [x] Focused tests 11/11 green
- [x] Local UAT sign-off (`STORY-6.5d-UAT-RESULTS.md`)
- [x] Gate evidence + friction log + closeout report (this document)
- [x] Checklist §0b EDF runtime parity amendment
- [ ] PR #109 merged to `develop`
- [ ] Azure Test UAT (post-merge)

---

*Dev closeout — Story 6.5d — 2026-05-25.*
