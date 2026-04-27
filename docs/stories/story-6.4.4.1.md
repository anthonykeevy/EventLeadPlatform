# Story 6.4.4.1 — Locale Architecture: Wire the Registry

**Epic:** 6 — AI Generation & Monetization Engine
**Story ID:** 6.4.4.1
**Title:** Locale Architecture: Wire the Registry (+ rubric v2 + prompts v1.1 + judge swap)
**Status:** Draft (SM pack)
**Branch:** `story/epic6-6.4.4.1-locale-architecture-wire-registry` (to be created)
**PR:** TBD on `new-story.ps1` execution
**Created:** 2026-04-27
**Depends On:** Story 6.4.4 closeout amendment ([PR #74](https://github.com/anthonykeevy/EventLeadPlatform/pull/74)) merged + Story 6.4.4 ([PR #72](https://github.com/anthonykeevy/EventLeadPlatform/pull/72)) merged with judge JSONs.
**Successor To:** Story 6.4.4 (measured-only learning under rubric_v1).
**Predecessor Of:** Story 6.4.4.2 (conditional H2/H4 re-run under rubric_v2), Story 6.4.5 (H3 component cheat sheet), Story 6.5b-style (style-intent resolver — must accept `brandPosture`).

---

## 1) Goal

Wire the existing `ref.Country` + `config.ValidationRule` + `config.PromptTemplate(Version)` + `config.PromptAssemblyProfile` registry into the form-AI service so that locale-aware prompt blocks are **rendered at request time from data**, not from Python string constants. Add `audienceLocale` and `brandPosture` API parameters with a clean default-resolution chain. Replace `rubric_v1` with `rubric_v2` (9 elements; 6 deterministic + 3 LLM-judged). Replace `prompts-v1.0` with `prompts-v1.1` (15 prompts × 6 locales × 3 reps = 270 cells per eval run). Swap Gemini judge for Grok 4; pin Claude 4.7. Re-judge baseline as the gate to proceed.

Success means the locale block is data-driven (deletable in 6 lines when format guidance becomes obsolete), the new audience-locale and brand-posture parameters are persisted on `dbo.GenerationRun` for replay, the rubric has ground truth (Tonyk's lived-AU calibration anchors are encoded), and the judge architecture has a fallback if Grok 4 also ceiling-locks.

This story is **wiring an existing registry**, not building a greenfield architecture. Database discovery during PM analysis confirmed ~70% of the data layer (`ref.Country`, `config.ValidationRule` with 27 country-linked patterns, `config.PromptTemplate(Version)`, `config.PromptAssemblyProfile`, `config.CapabilityPolicyVersion`, `config.ComponentCapabilitySnapshot`) is already built and seeded.

---

## 2) In Scope

### 2.1 Migrations (063–071, in order)

| # | File | Purpose |
|---|---|---|
| 063 | `063_story_6441_prompt_template_locale_block.py` | Create `config.PromptTemplateLocaleBlock` join table per D11(b). Columns: `PromptTemplateLocaleBlockID` (PK), `PromptTemplateID` (FK to `config.PromptTemplate`), `CountryID` (FK to `ref.Country`, nullable — null = NEUTRAL fallback row), `BlockType` (varchar 20, check constraint `IN ('format', 'policy', 'tone')`), `BlockBody` (`nvarchar(max)`), `ContentHash` (varchar 64), `IsActive` (bit), audit columns (`CreatedDate`, `CreatedBy`, `UpdatedDate`, `UpdatedBy`, `IsDeleted`). Unique constraint on (`PromptTemplateID`, `CountryID`, `BlockType`) where `IsActive = 1`. |
| 064 | `064_story_6441_country_cultural_dimensions.py` | Create `ref.CountryCulturalDimensions` sidecar per D12(b). One row per CountryID. Columns: `CountryCulturalDimensionsID` (PK), `CountryID` (FK, unique), `PowerDistanceIndex`, `UncertaintyAvoidanceIndex`, `IndividualismIndex`, `MasculinityIndex`, `LongTermOrientation`, `IndulgenceIndex` (each `int` nullable), `Source` (`varchar 200`), `SourceYear` (`int` nullable), audit columns. |
| 065 | `065_story_6441_seed_locale_blocks_au.py` | Seed AU format block (~150 chars; references `config.ValidationRule.ValidationPattern` per CountryID via documentation), AU policy block (~250 chars; Privacy Act 1988 + Spam Act 2003), AU tone block (~100 chars; Hofstede-anchored low-PDI casual register). |
| 066 | `066_story_6441_seed_locale_blocks_nz_uk_us_ca_ie.py` | Seed equivalent format/policy/tone blocks for NZ, UK, US, CA, IE — **pre-reviewed quality** per Tonyk's instruction (LLM-drafted, Tonyk-skim before merge). |
| 067 | `067_story_6441_seed_locale_blocks_intl_online.py` | Seed INTL_ONLINE block: ISO 8601 dates (YYYY-MM-DD), E.164 phone, single-line address, Country field required, English-neutral spelling. |
| 068 | `068_story_6441_seed_country_cultural_dimensions.py` | Seed Hofstede 6D values for the 7 MVP markets (AU, NZ, UK, US, CA, IE, INTL_ONLINE — INTL_ONLINE seeded with neutral midpoint values where applicable, source = "neutral midpoint"); stub rows for DE, JP, FR with `Source = 'Hofstede 6D 2010, requires native review'`. |
| 069 | `069_story_6441_generation_run_brand_posture.py` | Add `BrandPosture` (`varchar 40` nullable, check constraint `IN ('local', 'heritage', 'neutral', 'transcreate')`) and `BrandHeritageOrigin` (`varchar 5` nullable, ISO-3166-1 alpha-2) columns to `dbo.GenerationRun`. Backfill null on existing rows. |
| 070 | `070_story_6441_company_brand_posture.py` | **(Added per Tonyk Q7)** Add `BrandPosture` (`varchar 40` nullable) and `BrandHeritageOrigin` (`varchar 5` nullable) columns to `dbo.Company` — same check constraints as `dbo.GenerationRun`. These persist per-company defaults; no UI in this story (deferred to follow-up). |
| 071 | `071_story_6441_app_settings_locale_defaults.py` | Seed `config.AppSetting` rows: `form_ai.default_audience_locale = 'AU'`, `form_ai.default_brand_posture = 'local'`, `form_ai.locale_block_render_strategy = 'registry'` (alternative `'python_constant'` retained as legacy escape hatch — defaults to `registry`). |

**Capability Snapshot Rule (per `EPIC-6-WORKFLOW-GUIDE.md`):** none of these migrations touches component renderer manifests, so no capability snapshot bump is required. If `brandPosture` is later exposed in `FormSemanticPlan`, that's a Story 6.5b-style concern.

### 2.2 Service refactor (`backend/modules/form_ai/service.py`)

1. **Replace `_LOCALE_PROMPT_BLOCKS["AU"]` Python constant** with a registry-lookup function `_assemble_locale_block(audience_locale: str, brand_posture: str | None, db_session) -> str`.
2. **Inside `_assemble_locale_block`:** query active `PromptTemplateLocaleBlock` rows for the active template + `CountryID` resolved from `audience_locale`, joined to `ref.Country` and `ref.CountryCulturalDimensions`. Concatenate format + policy + tone sub-blocks in that order. Cache per-process for 5 minutes (registry rarely changes; eliminates per-request DB hit).
3. **Update `_build_initial_messages` (~line 1545)** to:
   - Accept new parameters: `audience_locale: str | None`, `brand_posture: str | None`, `brand_heritage_origin: str | None`.
   - Call `_assemble_locale_block` and inject the assembled block in place of the current Python-constant location.
   - Place the block **last in the cacheable system-prompt prefix** (Memo 3) so prompt caching hits the stable portion.
   - Persist `BrandPosture` and `BrandHeritageOrigin` on `dbo.GenerationRun` at run-creation time.
4. **Default-resolution chain** (encoded in a new helper `_resolve_audience_locale` / `_resolve_brand_posture`):
   - `audienceLocale`: explicit request param → `Event.CountryID` (if event scope) → `Company.CountryID` → `User.CountryID` → `app_setting.form_ai.default_audience_locale` (default `'AU'`). All `CountryID` values map via `ref.Country.ISO2Code` → enum `AU | NZ | UK | US | CA | IE | DE | INTL_ONLINE | APAC | EU | NEUTRAL`.
   - `brandPosture`: explicit request param → `Company.BrandPosture` → `app_setting.form_ai.default_brand_posture` (default `'local'`).
   - `brandHeritageOrigin`: explicit request param → `Company.BrandHeritageOrigin` → null.
   - Future story (6.5b-style or successor): per-form dropdown override.
5. **Fallback:** if `audience_locale` is unknown or no rows exist for that country, render NEUTRAL block + log a `log.ApplicationError` with severity `info` (not `error` — neutral fallback is by design).
6. **Backward compatibility:** existing `dbo.GenerationRun` rows have no `BrandPosture`. Service treats null as `'local'`.
7. **Delete `backend/modules/form_ai/system_prompt_sections_1_6.py`** if any traces remain (already deleted in 6.4.2 cleanup; verify).

### 2.3 API surface

`backend/modules/form_ai/router.py` (or wherever the AI panel endpoints live):

- Form-AI generation request schema gains optional `audienceLocale` (enum), `brandPosture` (enum), `brandHeritageOrigin` (string) fields.
- Defaults applied via the resolution chain above when fields omitted.
- Response unchanged in shape; resolved values surfaced under `meta.locale = { resolved: 'AU', source: 'Event.CountryID' }` for debuggability (small addition; schema audit will be needed in PR review).

### 2.4 Frontend pass-through (`frontend/src/.../FormAiPanel`)

**No UI redesign in this story.** AI Agent panel sends `audienceLocale` and `brandPosture` derived from event/company defaults via the existing `/api/me` + `/api/companies/{id}` data already loaded in app context. Network tab must show the new params on every form-AI generation call. Future story owns the per-form override dropdown.

### 2.5 Rubric v2 (`backend/tests/form_ai_eval/rubric_v2.md`)

9-element scoring (per Memo 2 + Memo 3; full anchor table in `STORY-6.4.4.1-RUBRIC-V2-ADR.md`):

| # | Element | Method |
|---|---|---|
| 1 | Date format matches `audienceLocale` | Deterministic regex |
| 2 | Phone format & country code matches | Deterministic regex (consults `config.ValidationRule.ValidationPattern`) |
| 3 | Address schema matches | Deterministic field-name presence |
| 4 | Consent/privacy citation correct | LLM-judged |
| 5 | Currency / number format matches | Deterministic regex |
| 6 | Name-field convention matches | Deterministic |
| 7 | Tone register matches PDI/UAI | LLM-judged |
| 8 | Mandatory-field strictness matches UAI | LLM-judged |
| 9 | Cross-locale leakage absent | Deterministic |

Tonyk's lived-AU calibration anchors encoded in the rubric (full list in the Rubric v2 ADR §4).

### 2.6 Benchmark `prompts-v1.1` (`backend/tests/form_ai_eval/prompts.yaml`)

15 prompts × 6 locales × 3 reps = 270 cells per eval run. Detailed spec in `STORY-6.4.4.1-PROMPTS-V1.1-SPEC.md`.

### 2.7 Judge swap

Update `STORY-6.4.4.1-JUDGE-PROMPTS.md` (replaces 6.4.4 version):

- **Primary 1:** Claude 4.7 (model version pinned, e.g. `claude-4.7-sonnet-20260315`).
- **Primary 2:** Grok 4 (replaces Gemini 2.5 Flash — different model family for genuine bias independence).
- **Control:** GPT-5 mini (unchanged — same model as form generator; self-bias delta is the architectural intent).
- **Calibration nudge in all three judge prompts:** "Identify at least one weakness per row before scoring" — to break ceiling-locking.
- **All judge JSON outputs:** add required `judge_model_version` field (e.g. `"claude-4.7-sonnet-20260315"`).

### 2.8 Ingest schema bump (`backend/tests/form_ai_eval/judge_ingest.py`)

- Reject judge outputs missing `judge_model_version`.
- Accept `rubric_version: rubric_v2`.
- Validate the 9 new metric keys in the `scores` map (replaces v1's 6 keys).
- Validate score ranges per metric (deterministic items 0/1/2; LLM-judged items 0/1/2; cross-locale leakage 0/2).
- Compute primary mean as **Claude + Grok mean** (Gemini gone); GPT-5 mini bias delta computation unchanged in shape.
- Backwards compatibility: v1 ingest still works for v1 files (existing 6.4.4 JSONs once committed in PR #72) — version-gated path.

### 2.9 ADRs

- `STORY-6.4.4.1-LOCALE-ARCHITECTURE-ADR.md` (new) — registry pattern, format/policy/tone split, brand posture parameter, resolution chain.
- `STORY-6.4.4.1-RUBRIC-V2-ADR.md` (new) — supersedes `STORY-6.4.3b-RUBRIC-ADR.md` (which already has the supersession footer from PR #74).

### 2.10 Tests

- Unit tests for `_assemble_locale_block` (registry hit, NEUTRAL fallback, missing template).
- Unit tests for `_resolve_audience_locale` / `_resolve_brand_posture` resolution chain order.
- Migration round-trip tests (063–071 up + down).
- `judge_ingest.py` new schema-bump tests (rubric_v2 happy path; rejection on missing `judge_model_version`; rejection on wrong metric keys; v1 backwards-compat).
- Eval harness regression: existing 6.4.3a/c tests still pass; v1.0 → v1.1 benchmark migration documented.

### 2.11 Re-judge baseline under rubric_v2 (AC-10 gate)

Generate a fresh baseline run on `prompts-v1.1` with the new prompt assembly, package judge inputs under `rubric_v2.md`, run all three judges via Cursor (Tonyk-time), ingest, and verify the AC-10 gate (Grok 4 mean drops below 5.00 AND each judge scores ≥1 cell below 4 — see AC-10 escape clause).

---

## 3) Out of Scope

| Item | Reason / future home |
|---|---|
| Frontend UI redesign for `audienceLocale` / `brandPosture` (per-form dropdown) | Defaults-only in 6.4.4.1; per-form override is a future story (Tonyk Q7). |
| Company settings UI for `BrandPosture` / `BrandHeritageOrigin` | DB columns persist in this story (migration 070); UI deferred to a follow-up. |
| `brandIdentity` (logo / colour / font) | Post-MVP per D5; voice ≠ visual (Memo 4). |
| Native-speaker review of DE / JP / FR / non-Anglophone locale blocks | Stub rows ship with `Source = 'requires native review'`; carry-forward pre-Epic 7. |
| H1/H2/H4 re-evaluation under rubric_v2 | Story 6.4.4.2 (conditional). |
| Tool-use (Option C) access pattern | Forward-compatible architecture; no rework when adopted later. |
| Style intent / `themeIntent` resolver | Story 6.5b-style (must accept `brandPosture` in resolver contract). |
| Image-to-Form integration | Story 6.5 (separate track). |
| `config.CompanyValidationRule` overrides exposed in admin UI | Epic 7 admin tooling (schema exists, just needs UI). |
| Cross-locale leakage metric promotion to blocking | Advisory in v2; promote after baseline establishes a real distribution. |

---

## 4) Acceptance Criteria

(AC-1 through AC-16 preserved verbatim from `STORY-6.4.4.1-SM-HANDOFF-BRIEF.md` §4.8 with the AC-10 escape clause Tonyk approved.)

1. **AC-1 PromptTemplateLocaleBlock migrated and seeded:** `config.PromptTemplateLocaleBlock` migration applied; 7 fully-populated countries (AU/NZ/UK/US/CA/IE/INTL_ONLINE) seeded for format + policy + tone block types (21 rows minimum).
2. **AC-2 CountryCulturalDimensions migrated and seeded:** `ref.CountryCulturalDimensions` migration applied; 6 Hofstede dimensions seeded for the 7 MVP countries; stub rows for DE/JP/FR with `requires native review` flag.
3. **AC-3 GenerationRun brand columns migrated:** `dbo.GenerationRun` has `BrandPosture` and `BrandHeritageOrigin` columns; backfilled to null on existing rows.
4. **AC-4 Service uses registry:** `service.py` uses registry-rendered locale block; Python `_LOCALE_PROMPT_BLOCKS` constant deleted; `_assemble_locale_block` function tested.
5. **AC-5 API accepts new params:** `audienceLocale` and `brandPosture` accepted as request parameters; default `audienceLocale = AU`, `brandPosture = local` when unspecified (resolution chain per §2.2.4).
6. **AC-6 Benchmark v1.1 checked in:** `prompts-v1.1` checked in; 15 × 6 × 3 = 270 cells; locale set per cell.
7. **AC-7 Rubric v2 checked in:** `rubric_v2.md` checked in with Tonyk's lived-AU calibration anchors and the 9-element scoring table.
8. **AC-8 Ingest rubric_v2 schema:** `judge_ingest.py` accepts `rubric_version: rubric_v2` and `judge_model_version` field; rejects missing or malformed; v1 backwards-compat preserved for 6.4.4 baseline.
9. **AC-9 Judge prompts checked in:** `STORY-6.4.4.1-JUDGE-PROMPTS.md` committed: Claude 4.7 + Grok 4 + GPT-5 mini, all with "name one weakness" calibration nudge.
10. **AC-10 Re-judge baseline under rubric_v2 (gate to consider story complete):** Grok 4 mean drops below 5.00 AND each judge scores ≥1 cell below 4 across the baseline. **Escape clause (Tonyk Q6):** if after a single retry round (one calibration tweak — typically rubric anchor sharpening — followed by a re-run) all three judges still ceiling-lock, the story is closed with `JUDGE-ARCHITECTURE-RE-INVESTIGATION` registered as a P0 carry-forward and the architecture work itself is not blocked.
11. **AC-11 Eval harness regression:** existing 6.4.3a/c tests still pass; benchmark v1.0 → v1.1 migration documented in `docs/FORM-AI-EVAL-HARNESS.md`.
12. **AC-12 Backend regression:** `pytest backend/tests` passes (excluding skipped).
13. **AC-13 Frontend pass-through:** AI Agent panel sends `audienceLocale` (default from event/company resolution chain) and `brandPosture` (default `local` after Company fallback); no UI redesign required, but new params visible in network tab.
14. **AC-14 Story 6.4.4 prerequisite:** Closeout amendment ([PR #74](https://github.com/anthonykeevy/EventLeadPlatform/pull/74)) merged; PR #72 merged with 12 live judge JSONs committed (per amendment §3.1).
15. **AC-15 Rubric v2 ADR checked in:** `STORY-6.4.4.1-RUBRIC-V2-ADR.md` committed.
16. **AC-16 Locale architecture ADR checked in:** `STORY-6.4.4.1-LOCALE-ARCHITECTURE-ADR.md` committed (registry pattern, format/policy/tone split, brand posture parameter, resolution chain).

---

## 5) Definition of Done

- All ACs mapped to `STORY-6.4.4.1-GATE-EVIDENCE.md` (Dev creates at closeout).
- Focused tests (unit + ingest + migration) and backend gate green.
- Frontend lint + unit tests green.
- Manual UAT per `STORY-6.4.4.1-UAT-TEST-GUIDE.md` complete.
- Both ADRs committed.
- `docs/stories/EPIC-6-STATUS.md` updated; `docs/stories/EPIC-6-WORKFLOW-GUIDE.md` Current Focus advanced.
- `STORY-6.4.4.1-CLOSEOUT-REPORT.md` written (mandatory: this story ships migrations + new public API params).
- AC-10 re-judge baseline complete under rubric_v2 (or escape clause invoked with carry-forward registered).
- SM stale-field audit clean.

---

## 6) Estimated Size

**~7–9 dev days** (revised up from PM brief's 6 days, per Tonyk Q5/Q7 — pre-reviewed non-AU locale content + Company brand columns):

| Block | Days |
|---|---|
| Migrations 063–071 + reviews | 1.5 |
| Pre-reviewed seed content (7 markets × 3 sub-blocks = 21 prose blocks, Hofstede dimensions) | 1.5 |
| Service refactor (`_assemble_locale_block`, resolution helpers, `_build_initial_messages`, GenerationRun persistence) | 1.5 |
| API surface + frontend pass-through + Company brand columns | 1.0 |
| Rubric v2 + benchmark v1.1 + judge prompt templates | 1.0 |
| `judge_ingest.py` schema bump + tests | 0.5 |
| ADRs (locale architecture + rubric v2) | 0.5 |
| Re-judge baseline under v2 + AC-10 gate (Tonyk Cursor time) | 0.5 |
| **Total** | **~8 days** |

Risk: AC-10 calibration round (escape clause) could add 0.5 days if all three judges initially ceiling-lock and a rubric anchor tweak + re-run is needed.

---

## 7) Dependencies on other stories

- **Story 6.4.4 closeout amendment** ([PR #74](https://github.com/anthonykeevy/EventLeadPlatform/pull/74)) — must merge first so rubric_v1 supersession status is on master.
- **Story 6.4.4 (PR #72)** — must merge with 12 live judge JSONs (audit trail) before this story merges, per AM-AC-3 / AM-AC-4 of the closeout amendment.
- **Story 6.4.3b rubric ADR** — already on master; gets the v2 supersession reference added in PR #74.

---

## 8) Successor stories enabled

| Story | What this story unlocks |
|---|---|
| 6.4.4.2 (conditional) | Re-evaluation of H2/H4 under rubric_v2 (H1 deleted; combined moot). |
| 6.4.5 (H3 component cheat sheet) | Locale-aware component selection guidance can leverage the new registry. |
| 6.5b-style (style intent) | `brandPosture` parameter is now a first-class request input the resolver must accept. |
| 6.5 (Image-to-Form) | Locale parameters propagate identically through image-derived form generation. |
| Future Epic 7 international launch | DE/JP/FR/EU rows already provisioned in registry with `requires native review` flag. |

---

## Dev Agent Record

### Implementation Notes

_(filled by Dev during implementation)_

### Debug Log

_(filled by Dev)_

### Test Results

_(filled by Dev — preflight, focused gate, backend gate, frontend gate, AC-10 re-judge result)_

### File List

_(filled by Dev at closeout — all files added/modified)_

### Change Log

_(filled by Dev — date-stamped)_
