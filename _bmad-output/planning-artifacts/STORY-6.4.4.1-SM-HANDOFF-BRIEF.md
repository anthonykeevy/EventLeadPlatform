# Story 6.4.4.1 — SM Handoff Brief

**Document type:** PM → SM handoff brief
**PM:** John (PM agent)
**Date:** 2026-04-27
**Successor to:** Story 6.4.4 (closeout amendment also required)
**Predecessor to:** Story 6.4.4.2 (conditional re-run), Story 6.4.5 (H3 cheat sheet), Story 6.5b-style (style intent)

---

## 1. Why this story exists (strategic context)

Story 6.4.4 ran prompt-shrink sweeps H1/H2/H4 plus combined and produced a closeout report on PR #72 saying "do not merge as-is". On PM/Tonyk review, three deeper findings emerged that turn this from a calibration patch into an architectural foundation story:

1. **The judging method is structurally broken.** Across 5 runs × 60 cells per judge × 3 judges = 900 cells, **Gemini 2.5 Flash and GPT-5 mini both gave 60/60 perfect 5/5 scores in every variant**. Claude was the only judge that moved. The Claude+Gemini "primary mean" is therefore Gemini-flatline-dominated; every Claude-detected regression is exactly halved by averaging with Gemini's constant 5.0. The "rerun-at-n15" recommendation is the wrong remedy — Gemini's variance is structurally zero.

2. **The `locale_fidelity` metric has no ground truth.** None of the 10 benchmark prompts in `prompts-v1.0` specify a target locale. The judge package contains no locale anchor. The form generator's system prompt has the AU/NZ block, but that information doesn't propagate to the judge. Claude inferred AU strictness from output context clues (`+61`, "organisation") and applied its own model-internal AU-pedantry. Tonyk's lived AU experience confirmed several of Claude's locale downscores were false positives ("First name/Last name" is fine in AU; mandatory `+61` prefix on a domestic AU form is over-specification, not a locale fidelity bonus).

3. **The product needs an internationalisation architecture, not just a bigger AU block.** The product launches in AU but expands to NZ, UK, US, CA, EU within 12 months. Online events with global audiences are a major use case. The brand-posture axis (American company in AU wanting US-flavoured copy) is orthogonal to audience locale. Four parallel research agents converged on an architecture combining a structured data layer, format/policy sub-block split, and a separate `brandPosture` parameter.

**The good news** (discovered late in PM analysis): Tonyk built **most of the data layer for this architecture during Epic 1-2** and drifted away from it during the form-builder work. `ref.Country`, `config.ValidationRule`, `config.PromptTemplate(Version)`, `config.PromptAssemblyProfile`, `config.CapabilityPolicyVersion`, and `config.ComponentCapabilitySnapshot` already exist with seed data. **This story is wiring an existing registry, not building Option C from scratch.**

---

## 2. Reference materials (Bob: read all of these in order)

### Primary planning artefacts (must read)

| # | File | Purpose |
|---|---|---|
| 1 | `_bmad-output/planning-artifacts/EPIC-6-PROMPT-ENGINEERING-IDEATION-BRIEF.md` (v2) | Original epic ideation; Stories 6.4.2–6.5d defined; judge architecture lock |
| 2 | `_bmad-output/planning-artifacts/STORY-6.4.4.1-SM-HANDOFF-BRIEF.md` | **This document** |
| 3 | `_bmad-output/research/locale-strategy/00-CONSOLIDATED-RECOMMENDATION.md` | Consolidated PM recommendation across 4 research memos (D1-D12 source) |
| 4 | `_bmad-output/research/locale-strategy/01-saas-localisation-pm-memo.md` | Stripe-style registry pattern, B-lite recommendation |
| 5 | `_bmad-output/research/locale-strategy/02-cross-cultural-ux-research-memo.md` | Hofstede dimensions (PDI/UAI/IDV), 8-element rubric design |
| 6 | `_bmad-output/research/locale-strategy/03-ai-prompt-engineering-memo.md` | Format vs policy split, token-cost projections, eval pattern |
| 7 | `_bmad-output/research/locale-strategy/04-brand-strategy-transcreation-memo.md` | `brandPosture` enum design, audienceLocale × brandPosture matrix |

### Story 6.4.4 artefacts (must read for closeout amendment context)

| # | File | Purpose |
|---|---|---|
| 8 | `docs/stories/STORY-6.4.4-CLOSEOUT-REPORT.md` | Original closeout; says "PM/SM ship decision required before merge" |
| 9 | `docs/stories/STORY-6.4.4-HYPOTHESIS-EVIDENCE.md` | Per-hypothesis evidence with diff stats |
| 10 | `docs/stories/STORY-6.4.4-JUDGE-PROMPTS.md` | Cursor judge prompts used; identical across 3 judges |
| 11 | `docs/stories/STORY-6.4.4-GATE-EVIDENCE.md` | Gate evidence |
| 12 | `_bmad-output/eval-runs/story-6.4.4-live-baseline-vs-{h1,h2,h4,combined}/diff-report.md` | Diff reports per hypothesis |

### Schema discovery files (must read to plan the wiring)

| # | File | Purpose |
|---|---|---|
| 13 | `backend/migrations/versions/053_story_631_form_ai_governance_tables.py` | Original `config.PromptTemplate*`, `CapabilityPolicyVersion`, `WidthClassPolicyVersion`, `PromptAssemblyProfile` migration |
| 14 | `backend/migrations/versions/054_story_631_seed_governance_baseline.py` | Initial seed of `FORM_AI_STEP1_BASE` template + `FORM_AI_DEFAULT_STEP1` profile |
| 15 | `backend/migrations/versions/055_story_631_form_ai_capability_rating_fileupload.py` | Capability snapshot evolution pattern (precedent for the new locale-block linkage migrations) |
| 16 | Earlier migrations seeding `ref.Country` and `config.ValidationRule` (search `^seed.*country` and `^seed.*validation_rule`) | Country and per-country regex seed data |

### Service code (must read before refactoring)

| # | File | Purpose |
|---|---|---|
| 17 | `backend/modules/form_ai/service.py` | Current Python-string locale block (lines ~1370 `_LOCALE_PROMPT_BLOCKS["AU"]`); `_build_initial_messages` at ~1545 |
| 18 | `backend/modules/form_ai/system_prompt_sections_1_6.py` | (Already deleted in 6.4.2 cleanup; verify gone) |
| 19 | `backend/tests/form_ai_eval/run.py` | Eval harness entry point |
| 20 | `backend/tests/form_ai_eval/judge_pack.py` | Judge package generator |
| 21 | `backend/tests/form_ai_eval/judge_ingest.py` | Judge result ingest with bias-delta logic |
| 22 | `backend/tests/form_ai_eval/prompts.yaml` | `prompts-v1.0` benchmark — needs to be replaced with v1.1 |
| 23 | `backend/tests/form_ai_eval/rubric_v1.md` | Current single-anchor rubric — being replaced with v2 |

### Workflow guide & general reference

| # | File | Purpose |
|---|---|---|
| 24 | `docs/stories/EPIC-6-WORKFLOW-GUIDE.md` | Multi-Round UAT Protocol, Capability Snapshot Rule, Green CI/CD Rule, RequestID lineage |
| 25 | `docs/stories/EPIC-6-STATUS.md` | Epic 6 status — needs Story 6.4.4.1 added |
| 26 | `docs/AGENT-LOGGING-GUIDE.md` | `log.ApiRequest` outbound payloads diagnostic pattern |
| 27 | `docs/FORM-AI-EVAL-JUDGE-WORKFLOW.md` | How the manual Cursor judge flow runs |
| 28 | `docs/stories/STORY-6.4.3b-RUBRIC-ADR.md` | Current rubric ADR — needs amendment for v2 |

---

## 3. Closeout amendment for Story 6.4.4 (must be drafted first)

Create `docs/stories/STORY-6.4.4-CLOSEOUT-AMENDMENT.md` with:

| Section | Content |
|---|---|
| Disposition | **Option 3 from original closeout**: revert prompt changes; keep harness, tests, and judge-prompt scaffolding; mark as "measured-only learning" |
| Reason | Judge architecture flatline (Gemini + GPT-5 mini ceiling-locked at 60/60); `locale_fidelity` metric has no ground truth in `prompts-v1.0`; locale_fidelity findings are a mix of real regressions and AU-pedantry noise that cannot be cleanly separated under the current rubric |
| Code reverts required in PR #72 | Locale block (~2.4 KB), consent decision-table block, operational-trim changes — all in `backend/modules/form_ai/service.py` |
| Code retained in PR #72 | Eval harness updates (`backend/tests/form_ai_eval/run.py` parsing for variant labels), tests, judge prompt scaffolding |
| Live judge JSONs | **Must be committed to PR #72 before merge** — currently only diff reports are in git; raw `judge-output-{claude,gemini,gpt5mini}.json` files for H1/H2/H4/combined live in OneDrive master folder. Audit trail requires they're tracked. |
| Carry-forward | Locale architecture work moves to Story 6.4.4.1; H1/H2/H4 hypothesis evidence preserved as input to optional Story 6.4.4.2 re-run under v2 rubric |
| ADR amendment | `docs/stories/STORY-6.4.3b-RUBRIC-ADR.md` gets a "v2 in progress" footer noting rubric_v1 is being superseded; baseline judge outputs under v1 remain valid for v1 comparisons only |

---

## 4. Story 6.4.4.1 — Locale Architecture: Wire the Registry

### 4.1 Objective

Wire the existing `ref.Country` + `config.ValidationRule` + `config.PromptTemplate(Version)` + `config.PromptAssemblyProfile` registry into the form-AI service so that locale-aware prompt blocks are rendered at request time from data, not from Python string constants. Add `audienceLocale` and `brandPosture` API parameters. Replace `rubric_v1` with `rubric_v2` (9 elements; deterministic + LLM-judged). Replace `prompts-v1.0` with `prompts-v1.1` (15 × 6 × 3 = 270 generations per eval run). Swap Gemini judge for Grok 4; pin Claude 4.7. Re-judge baseline as the gate to proceed.

### 4.2 Architectural decisions (from D1-D12, locked)

| ID | Decision | Implementation locus |
|---|---|---|
| D1 | Render-at-request-time from existing registry; format/policy sub-block split; forward-compatible to tool-use Option C | Service refactor + new join table |
| D2 | Locale enum: `AU \| NZ \| UK \| US \| CA \| IE \| DE \| INTL_ONLINE \| APAC \| EU \| NEUTRAL` | API + benchmark + registry |
| D3 | MVP fully-populated rows: AU, NZ, UK, US, CA, IE, INTL_ONLINE; rest as stubs | Seed migration |
| D4 | `brandPosture: local \| heritage \| neutral \| transcreate` + `heritageOrigin` | API + GenerationRun column |
| D5 | `brandIdentity` (logo/colour/font) deferred post-MVP | Out of scope |
| D6 | `locale_fidelity` rubric v2 (9 elements; 6 deterministic + 3 LLM-judged) | New rubric file + judge_ingest extension |
| D7 | `prompts-v1.1` benchmark (15 × 6 × 3 = 270/run) | New benchmark file |
| D8 | Judge swap: Claude 4.7 + Grok 4 + GPT-5 mini control | Judge prompt updates + ingest validation |
| D9 | Add `judge_model_version` field | Schema extension to judge JSON + ingest |
| D10 | Story 6.4.4 disposition: revert (closeout amendment) | Section 3 above |
| **D11(b)** | New join table `config.PromptTemplateLocaleBlock(PromptTemplateID, CountryID, BlockType, BlockBody, IsActive, ...)` where `BlockType ∈ {format, policy, tone}` | New migration (~063) |
| **D12(b)** | New sidecar `ref.CountryCulturalDimensions(CountryID, PowerDistanceIndex, UncertaintyAvoidanceIndex, IndividualismIndex, MasculinityIndex, LongTermOrientation, IndulgenceIndex, Source, ...)` | New migration (~064) |

### 4.3 Migrations (in order)

| # | File | Purpose |
|---|---|---|
| 063 | `063_story_6441_prompt_template_locale_block.py` | Create `config.PromptTemplateLocaleBlock` join table per D11(b). Columns: `PromptTemplateLocaleBlockID` (PK), `PromptTemplateID` (FK), `CountryID` (FK nullable — null = NEUTRAL fallback), `BlockType` (varchar 20: 'format', 'policy', 'tone'), `BlockBody` (nvarchar(max)), `ContentHash`, `IsActive`, audit columns, soft-delete. Unique constraint on (`PromptTemplateID`, `CountryID`, `BlockType`, `IsActive`=1) |
| 064 | `064_story_6441_country_cultural_dimensions.py` | Create `ref.CountryCulturalDimensions` sidecar per D12(b). One row per CountryID. Source field tracks attribution ("Hofstede 6D 2010" for now; future GLOBE/Trompenaars). Audit columns standard. |
| 065 | `065_story_6441_seed_locale_blocks_au.py` | Seed AU format block (~150 chars, references `config.ValidationRule` regex via documentation), AU policy block (~250 chars, Privacy Act 1988 + Spam Act 2003 wording), AU tone block (~100 chars, Hofstede-anchored: low PDI casual register) |
| 066 | `066_story_6441_seed_locale_blocks_nz_uk_us_ca_ie.py` | Seed equivalent blocks for NZ, UK, US, CA, IE |
| 067 | `067_story_6441_seed_locale_blocks_intl_online.py` | Seed INTL_ONLINE block: ISO 8601 dates, E.164 phone, single-line address, Country field required, English-neutral spelling |
| 068 | `068_story_6441_seed_country_cultural_dimensions.py` | Seed Hofstede 6D values for AU, NZ, UK, US, CA, IE (and stub rows for DE, JP, FR with `Source = 'Hofstede 6D 2010, requires native review'`) |
| 069 | `069_story_6441_generation_run_brand_posture.py` | Add `BrandPosture` (varchar 40 nullable), `BrandHeritageOrigin` (varchar 5 nullable) columns to `dbo.GenerationRun` |
| 070 | `070_story_6441_app_settings_locale_defaults.py` | Seed app settings: `form_ai.default_audience_locale = AU`, `form_ai.default_brand_posture = local`, `form_ai.locale_block_render_strategy = registry` (vs `python_constant` legacy) |

**Capability Snapshot Rule note (per `EPIC-6-WORKFLOW-GUIDE.md`):** none of these migrations touch component renderer manifests, so no capability snapshot bump is required. If `brandPosture` is later exposed in `FormSemanticPlan`, that's a Story 6.5b-style concern, not this story.

### 4.4 Service refactor

In `backend/modules/form_ai/service.py`:

1. **Replace `_LOCALE_PROMPT_BLOCKS["AU"]` Python constant** with a registry-lookup function `_assemble_locale_block(audience_locale: str, brand_posture: str | None, db_session) -> str`.
2. **Inside `_assemble_locale_block`**: query active `PromptTemplateLocaleBlock` rows for the active template + country, joined to `ref.Country` and `ref.CountryCulturalDimensions`. Concatenate format + policy + tone sub-blocks in that order. Cache per-process for 5 minutes (registry rarely changes; eliminates per-request DB hit).
3. **Update `_build_initial_messages`** at line ~1545 to:
   - Accept new parameters from the request: `audience_locale`, `brand_posture`, `brand_heritage_origin`
   - Call `_assemble_locale_block` and inject the assembled block in place of the current Python-constant location
   - Place the block **last in the cacheable system-prompt prefix** (Memo 3) so prompt caching hits the stable portion
   - Store `BrandPosture` and `BrandHeritageOrigin` on `dbo.GenerationRun`
4. **Add fallback**: if `audience_locale` is unknown or no rows exist for that country, render NEUTRAL block + log a `log.ApplicationError` with severity `info` (not `error` — neutral fallback is by design).
5. **Backward compatibility**: existing `dbo.GenerationRun` rows have no `BrandPosture`. Service treats null as `local`.

### 4.5 Rubric v2 (`backend/tests/form_ai_eval/rubric_v2.md`)

9-element scoring (per Memo 2 + Memo 3):

| # | Element | Method | Anchors |
|---|---|---|---|
| 1 | Date format matches `audienceLocale` | Deterministic regex | 0/1/2 |
| 2 | Phone format & country code matches | Deterministic regex (consults `config.ValidationRule.ValidationPattern` for the country) | 0/1/2 |
| 3 | Address schema matches | Deterministic field-name presence | 0/1/2 |
| 4 | Consent/privacy citation correct | LLM-judged (Cursor) | 0/1/2 |
| 5 | Currency / number format matches | Deterministic regex | 0/1/2 |
| 6 | Name-field convention matches | Deterministic | 0/1/2 |
| 7 | Tone register matches PDI/UAI | LLM-judged | 0/1/2 |
| 8 | Mandatory-field strictness matches UAI | LLM-judged | 0/1/2 |
| 9 | Cross-locale leakage absent | Deterministic | 0=US convention in non-US locale, 2=clean |

**Tonyk's lived-AU calibration anchors (must be in rubric_v2.md):**
- "First name / Last name" labels → score 2 on item 6 (NOT a regression vs "Given name/Surname")
- "Given name / Surname" labels → also score 2 on item 6
- Mandatory `+61` prefix in placeholder on AU domestic form → score 0 on item 2
- Phone helpText "Include country code if overseas" → score 2 on item 2
- DD/MM/YYYY → score 2 on item 1; MM/DD/YYYY → score 0 on item 1
- "Suburb/State/Postcode" → score 2 on item 3; "ZIP code" in non-US → score 0 on item 3
- "Privacy Act 1988" citation in AU → score 2 on item 4; generic GDPR copy in AU → score 1 on item 4

**ADR amendment**: `STORY-6.4.3b-RUBRIC-ADR.md` becomes the v1 ADR; new `STORY-6.4.4.1-RUBRIC-V2-ADR.md` documents v2 supersession with re-snapshotting policy unchanged from v1.

### 4.6 Benchmark `prompts-v1.1`

15 prompts × 6 locales × 3 reps = 270 generations per eval run.

| Slice | Detail |
|---|---|
| 10 prompts inherited | Same as `prompts-v1.0` but with explicit `audienceLocale` field added |
| 5 new prompts | (a) International online event registration, (b) EU GDPR-required event registration, (c) US PII-heavy onboarding (with TIN/SSN guidance — system must refuse to invent), (d) UK NHS waiver, (e) NZ-specific RSVP |
| 6 explicit locales per prompt | AU, NZ, UK, US, INTL_ONLINE, EU |
| 3 within-prompt variants | "neutral" (locale only in parameter), "ambiguous" (mentions a city), "adversarial" (prompt uses US conventions but locale=AU) |
| 3 repetitions | Surface temperature variance; report median + p10 |

Cost: ~$2/run for LLM judging plus generation cost (~$5-6 per full eval). **Run on every prompt change, on model upgrades, and nightly on master.**

### 4.7 Judge swap implementation

| Judge slot | Action | File changes |
|---|---|---|
| Primary 1: Claude | Pin to `Claude 4.7` explicitly in judge prompts | `STORY-6.4.4.1-JUDGE-PROMPTS.md` (new) replaces 6.4.4 version |
| Primary 2: Gemini | **Replace with Grok 4** | Same file — Gemini-specific prompt removed, Grok prompt added |
| Control: GPT-5 mini | Unchanged (same model as form generator; self-bias delta is the architectural intent) | Same file — version explicitly pinned |
| All judges | "Identify at least one weakness per row before scoring" instruction added to judge prompt template | Calibration nudge for ceiling-locked models |
| All judge JSON outputs | Add required `judge_model_version` field (e.g., `"claude-4.7-sonnet-20260315"`); ingest validates | `judge_ingest.py` schema bump |

**Ingest validation update**: `backend/tests/form_ai_eval/judge_ingest.py` rejects judge outputs missing `judge_model_version`. The Claude+Gemini primary mean becomes Claude+Grok primary mean. GPT-5 mini bias delta calculation unchanged.

### 4.8 Acceptance criteria

| AC | Status gate |
|---|---|
| AC-1 | `config.PromptTemplateLocaleBlock` migration applied; 7 fully-populated countries (AU/NZ/UK/US/CA/IE/INTL_ONLINE) seeded for format + policy + tone block types |
| AC-2 | `ref.CountryCulturalDimensions` migration applied; 6 Hofstede dimensions seeded for the 7 MVP countries |
| AC-3 | `dbo.GenerationRun` has `BrandPosture` and `BrandHeritageOrigin` columns; backfilled to null on existing rows |
| AC-4 | `service.py` uses registry-rendered locale block; Python `_LOCALE_PROMPT_BLOCKS` constant deleted; `_assemble_locale_block` function tested |
| AC-5 | `audienceLocale` and `brandPosture` accepted as request parameters; default `audienceLocale = AU`, `brandPosture = local` when unspecified |
| AC-6 | `prompts-v1.1` checked in; 15 × 6 × 3 = 270 rows; locale set per row |
| AC-7 | `rubric_v2.md` checked in with Tonyk's lived-AU calibration anchors |
| AC-8 | `judge_ingest.py` accepts `rubric_version: rubric_v2` and `judge_model_version` field; rejects missing or malformed |
| AC-9 | `STORY-6.4.4.1-JUDGE-PROMPTS.md` checked in: Claude 4.7 + Grok 4 + GPT-5 mini, all with "name one weakness" instruction |
| AC-10 | Re-judge baseline under rubric_v2: **gate to consider story complete** — Grok 4 must drop below 5.00 average AND each judge must score ≥1 cell below 4 across the baseline |
| AC-11 | Eval harness regression: existing 6.4.3a/c tests still pass; benchmark v1.0 → v1.1 migration documented |
| AC-12 | Backend regression: `pytest backend/tests` passes (excluding skipped) |
| AC-13 | Frontend pass-through: AI Agent panel sends `audienceLocale` (default from event/company) and `brandPosture` (default `local`); no UI redesign required, but new params visible in network tab |
| AC-14 | Story 6.4.4 closeout amendment merged separately; PR #72 reverts (per section 3) committed before this story merges |
| AC-15 | New ADR `STORY-6.4.4.1-RUBRIC-V2-ADR.md` checked in |
| AC-16 | New ADR `STORY-6.4.4.1-LOCALE-ARCHITECTURE-ADR.md` checked in (registry pattern, format/policy split, brand posture parameter) |

### 4.9 Out of scope

- Frontend UI redesign for `audienceLocale`/`brandPosture` — defaults from event/company/sensible defaults; UX polish in a follow-up
- `brandIdentity` (logo/colour/font) — post-MVP per D5
- Native-speaker review of DE/JP/FR/non-Anglophone locale blocks — those rows ship as stubs flagged for review
- H1/H2/H4 re-evaluation under v2 — that's Story 6.4.4.2 (conditional)
- Tool-use (Option C) access pattern — current architecture is forward-compatible, no rework required when we adopt later
- Style intent / `themeIntent` — Story 6.5b-style concern (note: `brandPosture` is a new prompt input that 6.5b-style resolver must accept)

---

## 5. Story 6.4.4.2 — Conditional re-run of H1/H2/H4 under v2

May not be needed. The locale architecture in 6.4.4.1 delivers structural prompt-shrink (the AU/NZ block goes from a 2.4 KB Python constant to ~500 chars rendered from a 3-row registry lookup). That's larger than H1's saving and more architecturally sound. H2 (consent decision-table) and H4 (operational trim) may still be valuable individually but the urgency is lower.

**SM decision point**: after 6.4.4.1 ships and we have v2-rubric baseline numbers, hold a 30-min review with Tonyk to decide whether 6.4.4.2 is worth running or whether we skip directly to 6.4.5 (H3 component cheat sheet).

---

## 6. Note for Story 6.5b-style

`brandPosture` is a new prompt input parameter introduced in 6.4.4.1. The style-intent resolver designed in 6.5b-style must accept it as part of the resolver contract:

```
StyleIntent = (themeIntent, brandPosture, audienceLocale) → ResolvedStyle
```

The resolver design ADR for 6.5b-style should reference Story 6.4.4.1's `STORY-6.4.4.1-LOCALE-ARCHITECTURE-ADR.md` and the `brandPosture` enum.

---

## 7. Carry-forward (post-6.4.4.1)

| Item | Suggested home | Notes |
|---|---|---|
| Native-speaker review of DE/JP/FR locale blocks before populating | Pre-Epic 7 (international launch) | Stubs ship in 6.4.4.1; flagged via `Source = 'Hofstede 6D 2010, requires native review'` |
| `config.CompanyValidationRule` overrides exposed in admin UI | Epic 7 admin tooling | Schema exists; just needs UI |
| `brandIdentity` (logo/colour/font) parameter | Post-MVP | Memo 4 recommends as separate parameter |
| Tool-use access pattern (Option C) | When latency budget allows / batched tool-use mature | Forward-compatible architecture; no rework cost |
| Cross-locale leakage metric promotion to blocking | After baseline establishes distribution | Currently advisory in v2 |

---

## 8. Hand-off package the SM should produce

Per the BMAD workflow guide:

| Artefact | Path |
|---|---|
| Story file | `docs/stories/story-6.4.4.1.md` |
| Story context XML | `docs/stories/story-context-6.4.4.1.xml` |
| Single-session dev prompt | `docs/stories/STORY-6.4.4.1-SINGLE-SESSION-DEV-PROMPT.md` |
| UAT test guide | `docs/stories/STORY-6.4.4.1-UAT-TEST-GUIDE.md` |
| Preflight | `docs/stories/STORY-6.4.4.1-PREFLIGHT.md` |
| Locale architecture ADR | `docs/stories/STORY-6.4.4.1-LOCALE-ARCHITECTURE-ADR.md` |
| Rubric v2 ADR | `docs/stories/STORY-6.4.4.1-RUBRIC-V2-ADR.md` |
| Benchmark v1.1 spec | `docs/stories/STORY-6.4.4.1-PROMPTS-V1.1-SPEC.md` |
| Closeout amendment for 6.4.4 | `docs/stories/STORY-6.4.4-CLOSEOUT-AMENDMENT.md` |

Then SM runs:

```powershell
./scripts/git/new-story.ps1 -Epic 6 -Story "6.4.4.1" -Slug "locale-architecture-wire-registry" -CreateWorktree -DraftPR
```

Worktree will land at `C:\wt\elp\story-epic6-6.4.4.1-locale-architecture-wire-registry\` per `$env:ELP_WORKTREE_ROOT`.

SM reports back to PM with: worktree path + branch name + Draft PR URL for Tonyk to open in Claude/Cursor for the Dev agent.

---

## 9. Estimated story size

**5-6 dev days** (down from initial 5-7 estimate because data layer is mostly built):

| Block | Days |
|---|---|
| Migrations (063-070) + reviews | 1.0 |
| Seed content (locale blocks for 7 markets, Hofstede dimensions) | 1.0 |
| Service refactor (`_assemble_locale_block`, `_build_initial_messages`, GenerationRun persistence) | 1.5 |
| API surface + minimal frontend pass-through | 0.5 |
| Rubric v2 + benchmark v1.1 + judge prompt templates | 1.0 |
| `judge_ingest.py` schema bump + ingest tests | 0.5 |
| ADRs (locale architecture + rubric v2) | 0.5 |
| Re-judge baseline under v2 + AC-10 gate | 0.5 (mostly Tonyk-time in Cursor) |
| **Total** | **~6 days** |

Plus closeout amendment for 6.4.4 (~0.5 day, separate PR before this story merges).

---

*End of brief. Bob: please confirm understanding before drafting `story-6.4.4.1.md`. Any scope question, raise with PM (John) before drafting.*
