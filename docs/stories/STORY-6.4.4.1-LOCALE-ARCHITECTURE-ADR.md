# Story 6.4.4.1 ADR — Locale Architecture: Wire the Registry

**Status:** Accepted (D1–D5, D11(b), D12(b) locked by PM/Tonyk; Architect review required for any change to the registry data model or resolution chain).
**Story:** 6.4.4.1 — Locale Architecture: Wire the Registry.
**Decision Owner:** PM (John) + SM (Bob) + Tonyk (final disposition).
**Date:** 2026-04-27
**Supersedes:** N/A (first ADR for the locale architecture).
**Related:** [`STORY-6.4.4.1-RUBRIC-V2-ADR.md`](./STORY-6.4.4.1-RUBRIC-V2-ADR.md), [`STORY-6.4.4-CLOSEOUT-AMENDMENT.md`](./STORY-6.4.4-CLOSEOUT-AMENDMENT.md), [`STORY-6.4.3b-RUBRIC-ADR.md`](./STORY-6.4.3b-RUBRIC-ADR.md) (now superseded by rubric_v2).

---

## Context

Story 6.4.4 attempted prompt-shrink sweeps (H1/H2/H4) and uncovered three deeper findings on PM/Tonyk review (full reasoning in [`STORY-6.4.4-CLOSEOUT-AMENDMENT.md`](./STORY-6.4.4-CLOSEOUT-AMENDMENT.md) §1):

1. **The judging method was structurally broken at rubric_v1.** Two of three judges flatlined at 60/60 perfect 5/5 across 5 runs.
2. **`locale_fidelity` had no ground truth.** No benchmark prompt specified a target locale; Claude inferred AU strictness from output context clues and applied AU-pedantry false positives.
3. **The product needs an internationalisation architecture.** Launches AU but expands to NZ/UK/US/CA/EU within 12 months. Online events with global audiences are a major use case. Brand posture (e.g. American company in AU wanting US-flavoured copy) is orthogonal to audience locale.

Four parallel research agents (SaaS localisation PM, cross-cultural UX, AI prompt engineering, brand strategy / transcreation) converged on a tiered locale architecture rendered from a structured registry, with format/policy split, brand posture as a separate parameter, and a 9-element rubric with deterministic + LLM-judged elements.

**The good news:** Tonyk built ~70% of the data layer for this architecture during Epic 1–2 and drifted away from it during the form-builder work. `ref.Country`, `config.ValidationRule` (27 country-linked patterns), `config.PromptTemplate(Version)`, `config.PromptAssemblyProfile`, `config.CapabilityPolicyVersion`, and `config.ComponentCapabilitySnapshot` already exist with seed data. **This story wires the existing registry; it does not build greenfield.**

---

## Decision

### D1 — Render-at-request-time from existing registry; format/policy/tone sub-block split

The locale prompt block is **rendered at request time** from `config.PromptTemplateLocaleBlock` (new join table) joined to `ref.Country` and `ref.CountryCulturalDimensions` (new sidecar). The block is split into three sub-blocks concatenated in fixed order:

| Sub-block | Content | When deletable |
|---|---|---|
| **format** | Date, phone, address, currency, name conventions; references `config.ValidationRule.ValidationPattern` per CountryID for regex authority | When LLMs reliably handle formats from a one-line locale hint (Memo 3 estimates ~12 months for top-tier models). Delete this sub-block; keep policy and tone. |
| **policy** | Privacy Act / GDPR / CCPA / regulatory consent text; data handling notice templates | **Never deletable** — product policy, not world knowledge. Always required. |
| **tone** | Hofstede-anchored register cues (PDI, UAI, IDV); formality defaults | Deletable when style-intent (Story 6.5b-style) supersedes per-locale tone defaults — but tone block remains a useful fallback. |

Forward-compatible to tool-use Option C (LLM calls a `getLocaleRules(country)` tool instead of receiving a rendered block) — no schema rework required when adopted; only the renderer changes.

### D2 — Locale enum

```
audienceLocale: AU | NZ | UK | US | CA | IE | DE | INTL_ONLINE | APAC | EU | NEUTRAL
```

INTL_ONLINE / APAC / EU / NEUTRAL are first-class non-country values (Memo 1). NEUTRAL is the explicit fallback when an unknown locale is requested or no rows exist for the resolved country — it is **not** silence.

### D3 — MVP populated rows

7 fully-populated registry rows: AU, NZ, UK, US, CA, IE, INTL_ONLINE. EU and DE ship as **stubs** (registry rows present but flagged for native-speaker review). APAC ships as a NEUTRAL alias with phone-formatting addendum.

Per Tonyk Q5 (PM/SM joint review 2026-04-27): all 7 MVP rows ship **pre-reviewed quality** — LLM-drafted, Tonyk-skim before merge. DE/JP/FR stubs flagged `Source = 'requires native review'`.

### D4 — Brand posture parameter (separate from audience locale)

```
brandPosture: 'local' | 'heritage' | 'neutral' | 'transcreate'
brandHeritageOrigin: ISO-3166-1 alpha-2 string (nullable; only used when brandPosture = 'heritage')
```

Memo 4's collapsed enum: `heritage:US`, `heritage:UK`, etc. flatten to `heritage` + `heritageOrigin`, avoiding combinatorial explosion. Defaults:

- `local` when company country == audience locale (modal AU SMB case).
- `neutral` when unknown / multi-market.
- **Never silently assume `heritage`** — it's the riskiest wrong guess.

**Interaction rule (canonical):**
> `audienceLocale` controls field shape and compliance. `brandPosture` controls voice and copy register.

Warning cases (LLM produces confidently wrong output) get human-review tags in the AI Agent panel (out of scope for this story; future):

- Cross-script heritage transplants: `heritageOrigin: JP` × `audienceLocale: DE`.
- Register clashes: `heritageOrigin: US` (casual) × `audienceLocale: JP` (formal).

### D5 — `brandIdentity` (logo / colour / font) deferred post-MVP

Voice ≠ visual. Brands routinely diverge on voice and visual (Coca-Cola: globally uniform visual, transcreated copy). MVP scope: voice via `brandPosture` only; logo upload remains a static asset workflow.

### D11(b) — Schema: `config.PromptTemplateLocaleBlock` join table

| Column | Type | Notes |
|---|---|---|
| `PromptTemplateLocaleBlockID` | bigint identity PK | |
| `PromptTemplateID` | bigint FK → `config.PromptTemplate(PromptTemplateID)` | The active template (e.g. `FORM_AI_STEP1_BASE`) |
| `CountryID` | bigint FK → `ref.Country(CountryID)`, **nullable** | Null = NEUTRAL fallback row |
| `BlockType` | varchar(20) check `IN ('format', 'policy', 'tone')` | |
| `BlockBody` | nvarchar(max) | Block prose; ~150–250 chars typical |
| `ContentHash` | varchar(64) | SHA-256 of `BlockBody`; for change detection |
| `IsActive` | bit default 1 | |
| audit | `CreatedDate`, `CreatedBy`, `UpdatedDate`, `UpdatedBy`, `IsDeleted` | Standard pattern |

Unique constraint: `(PromptTemplateID, CountryID, BlockType)` where `IsActive = 1`.

### D12(b) — Schema: `ref.CountryCulturalDimensions` sidecar

| Column | Type | Notes |
|---|---|---|
| `CountryCulturalDimensionsID` | bigint identity PK | |
| `CountryID` | bigint FK → `ref.Country(CountryID)` unique | One row per country |
| `PowerDistanceIndex` | int nullable (0–100) | Hofstede 6D |
| `UncertaintyAvoidanceIndex` | int nullable | |
| `IndividualismIndex` | int nullable | |
| `MasculinityIndex` | int nullable | |
| `LongTermOrientation` | int nullable | |
| `IndulgenceIndex` | int nullable | |
| `Source` | varchar(200) | Citation/attribution; e.g. `'Hofstede 6D 2010'`, `'Hofstede 6D 2010, requires native review'` |
| `SourceYear` | int nullable | |
| audit | _(standard)_ | |

Future-extensible to GLOBE / Trompenaars by adding columns without schema rework.

---

## Resolution chain (Tonyk Q7)

The service resolves `audienceLocale` and `brandPosture` per request via a deterministic chain. Each step falls through to the next on null/missing.

### `audienceLocale` resolution

1. **Explicit request param** — `body.audienceLocale` (validated against enum). If invalid → reject with `400`.
2. **Event country** — `Event.CountryID` mapped via `ref.Country.ISO2Code` to enum (when the form belongs to an event scope).
3. **Company country** — `Company.CountryID` mapped via `ref.Country.ISO2Code` to enum.
4. **User country** — `User.CountryID` mapped via `ref.Country.ISO2Code` to enum (per the existing `dbo.User` schema; nullable).
5. **App setting** — `config.AppSetting('form_ai.default_audience_locale')` (seeded `'AU'`).
6. **Hardcoded fallback** — `'AU'` (defensive; should never trigger if app_setting seeded).

If the resolved value maps to a CountryID with no `PromptTemplateLocaleBlock` rows: render NEUTRAL block + log `log.ApplicationError` severity `info`. NEUTRAL is by design; not an error.

### `brandPosture` resolution

1. **Explicit request param** — `body.brandPosture` (validated against enum).
2. **Company default** — `Company.BrandPosture` (new column, migration 070).
3. **App setting** — `config.AppSetting('form_ai.default_brand_posture')` (seeded `'local'`).
4. **Hardcoded fallback** — `'local'`.

### `brandHeritageOrigin` resolution

1. **Explicit request param** — `body.brandHeritageOrigin` (ISO-3166-1 alpha-2 validated).
2. **Company default** — `Company.BrandHeritageOrigin`.
3. **null** — only meaningful when `brandPosture = 'heritage'`; otherwise ignored.

### Future per-form override

Per Tonyk Q7: a future story (probably 6.5b-style or successor) adds a per-form dropdown allowing the user to override `audienceLocale` (and `brandPosture`) at form-builder time. This story persists the resolution path so the future override has a clean precedence position (between explicit-request-param and Event).

---

## Persistence

Every `dbo.GenerationRun` row records the resolved `BrandPosture` and `BrandHeritageOrigin` at run-creation time (migration 069). The resolved `audienceLocale` is **not** added as a new column — it's recoverable from the system prompt logged via `log.ApiRequest` and the `RequestID` lineage. (Adding a column for it is deferred until we have a concrete use case.)

`dbo.Company` gains the new brand-posture columns (migration 070) so per-company defaults persist. UI for editing these defaults is **deferred** to a follow-up story; this story persists the schema only. Tonyk explicitly chose this scope (Q7).

---

## Rationale

- **Token discipline:** one ~500-char block per request regardless of how many markets we support. Memo 3 projects $157.50/mo at 100k generations vs $142.50/mo for parameter-only — the architecture cost is noise.
- **Auditability:** legal/compliance review the registry rows, not 8 prose variants drifting in source files.
- **Future-proof:** when GPT-5.7+ reliably handles formats from a 1-line hint (~12 months for format rules; never for policy), delete the format sub-block — six lines change, not a re-architecture.
- **Cache friendly:** stable prefix (role/output-format/safety) + per-request locale tail = cache hits on the bulk of the prompt.
- **Graceful degradation:** unsupported markets fall back to NEUTRAL, a real first-class locale, not silence.
- **Decoupled from voice:** `brandPosture` is orthogonal to `audienceLocale`. Memo 4's collapsed enum (`heritage` + `heritageOrigin`) is extensible without enum explosion.
- **Replayable:** every generation has its `BrandPosture` + `BrandHeritageOrigin` persisted on `GenerationRun`; the registry version is implicit via `PromptTemplateVersion`.
- **Aligned with existing patterns:** `config.AppSetting` for global defaults, `dbo.Company` columns for per-company overrides, future per-form dropdown — same precedence pattern Epic 6 has used elsewhere (e.g. Story 6.4 `UserPreference` architecture).

---

## Consequences

### Positive

- The Python `_LOCALE_PROMPT_BLOCKS` constant is **deleted** in this story. No more drift between prose-in-code and prose-in-registry.
- Adding a new market is a **seed migration**, not a code change.
- Blocks can be A/B-tested by flipping `IsActive` on registry rows (pattern available; not exercised in MVP).
- The brand-posture decision is now **explicit and auditable** — no more implicit "the LLM will figure it out".
- Closeout amendment for Story 6.4.4 unblocks itself naturally: H1's locale block deletion is the architectural intent, not a regression to fix.

### Negative

- One additional DB hit per request unless cached (mitigated by 5-min process-local cache).
- Seven markets × three sub-blocks = 21 prose rows that need writing, each pre-reviewed (Tonyk Q5). Real localisation work.
- Adds two new tables (`config.PromptTemplateLocaleBlock`, `ref.CountryCulturalDimensions`) and two new columns each on `dbo.GenerationRun` and `dbo.Company` — non-trivial schema surface area for one story.
- Resolution chain has 6 fallback steps for `audienceLocale` — must be tested at every level.
- DE/JP/FR stubs ship without native-speaker review; carry-forward must be explicit.

### Neutral

- Forward-compatibility to tool-use Option C is preserved but not exercised. No upgrade pressure.
- Frontend pass-through is defaults-only; no UX regression risk because there's no new UI.

---

## Implementation evidence

To be filled at closeout:

- Migration files: `backend/migrations/versions/063_…` through `071_…`.
- Service entry points: `_assemble_locale_block`, `_resolve_audience_locale`, `_resolve_brand_posture`, `_build_initial_messages` (~line 1545).
- Tests: `backend/tests/test_form_ai_locale_assembly.py`, `backend/tests/test_form_ai_locale_resolution.py`.
- Public docs: `docs/FORM-AI-EVAL-HARNESS.md` v1.0 → v1.1 migration note.

---

## Review questions (PM/Architect/SM)

1. Is the format/policy/tone sub-block split the right axis, or should we collapse to format/policy only and treat tone as a `brandPosture`-derived overlay?
2. Should `app_setting.form_ai.locale_block_render_strategy` actually offer a `python_constant` legacy escape hatch, or should we delete that path entirely (no fallback to the deleted constant)?
3. Should the resolution chain include User country at all, given that User country is a person-level fact and forms are organisation-level artefacts? (Decision in this ADR: yes, as a backstop only — Event > Company > User.)
4. Should `ref.CountryCulturalDimensions` be exposed as a public domain in the API or kept internal to the service? (Decision: internal — not part of the API surface in MVP.)
5. Should the LLM call a tool to fetch the locale block (Option C) instead of receiving it inline, and if so when? (Decision: not now; forward-compatible architecture preserves the option.)

---

## Carry-forward

| Item | Suggested home |
|---|---|
| Company brand settings UI (admin page exposing `BrandPosture` / `BrandHeritageOrigin`) | Future story (post-6.4.4.1; possibly bundled with 6.5b-style). |
| Per-form locale dropdown (override at form-builder time) | Future story (6.5b-style or successor). |
| Native-speaker review of DE / JP / FR / EU locale blocks | Pre-Epic 7 (international launch). |
| Tool-use access pattern (Option C) | When latency budget allows / batched tool-use mature. |
| Cross-script heritage warning UI (e.g. JP × DE) | Future story; warnings logged in the meantime. |
| GLOBE / Trompenaars dimensions in `ref.CountryCulturalDimensions` | Add columns when needed; schema is extensible. |

---

*End of ADR. This document is the authoritative source of truth for the Story 6.4.4.1 locale architecture decisions.*
