# Story 6.5b — Prompt Assembly Registry Foundation (Closes R6)

**Epic:** 6 — AI Generation & Monetization Engine
**Story ID:** 6.5b
**Title:** Prompt Assembly Registry Foundation — `PromptAssemblyProfile*` schema + renderer + migrate stored-prose Blocks A/B/C/G/I to DB
**Status:** Ready for Dev
**Branch:** *(to be created — suggest `story/epic6-6.5b-registry-foundation` off `develop`)*
**PR:** *(to be opened to `develop` once branch is created)*
**Created:** 2026-05-20
**Depends On:**
- Story 6.5a Architecture Phase merged to `develop` (architecture docs + roadmap update)
- Release PR #101 reconciliation merged (already complete)
- Architecture docs (authoritative):
  - `docs/architecture/decision-6.5a-clarification-options-data-model.md` (Rev 9 — Approved)
  - `docs/architecture/prompt-assembly-registry-architecture.md` — companion (**§2.7** post-implementation per-block sources, **§3** registry schema, **§8** variant versioning, **§10** sequencing)

**Unblocks:**
- Story 6.5c — Capability Catalog Cutover (Blocks F/A-tail/I-tail authoritative resolver, `ref.BrandPosture`, toolbox alignment)
- Story 6.5d — Clarification Data Plane (Block E plugs into the registry built here)
- Story 6.11 Production Deployment Blueprint — `/api/internal/readiness/ai-context` probe (PR #102) becomes meaningful once Block G is DB-resident

**Resolves:**
- **R6** from PR #101 release notes — `context-pack-load-failed` on AI "Generate Form Draft" in Test environment. Block G (FEW_SHOT) migration moves the context-pack content from the on-disk markdown file (`docs/stories/STORY-6.2-AI-CONTEXT-PACK.md`) into `PromptSectionVariant.PromptSnippet`, eliminating the Azure path-resolution failure described in `backend/modules/form_ai/service.py:_load_context_pack`.

---

## 1) Goal

Stand up the **Prompt Assembly Registry** so that the five "stored prose" prompt blocks (A, B, C, G, I) live in versioned DB rows instead of Python string literals or on-disk markdown. This is the foundation that:

1. Closes **R6** (Block G context-pack is no longer a file).
2. Lets Story 6.5d plug Block E into a working `PromptSection*` framework instead of inventing its own injection path.
3. Lets Story 6.5c cut over capability generation without also having to invent the registry.

The renderer continues to assemble the prompt in the same order (A→I) and produces an output that is **functionally equivalent** to today's `_build_initial_messages` path for unchanged inputs — verified by regression tests.

**What this story does NOT do** (handled in 6.5c / 6.5d):
- Does **not** make `resolve_allowed_components` authoritative for Blocks A/F/I or the frontend toolbox (Story 6.5c).
- Does **not** replace the `brandPosture` enum with `ref.BrandPosture` — Block C prose is migrated, but the *picker* is still the existing enum (Story 6.5c).
- Does **not** touch Blocks D (locale) or E (clarification). D keeps its existing `PromptTemplateLocaleBlock` path; E remains in code until Story 6.5d.

---

## 2) In Scope

### 2.1 Registry Schema (per architecture §3 + §8)

Confirm/extend the existing `backend/models/config/prompt_assembly_profile.py` to match the architecture §3 schema. Target tables:

| Table | Purpose |
|-------|---------|
| `config.PromptAssemblyProfile` | Top-level named assembly (e.g., `FORM_AI_V1`) |
| `config.PromptAssemblyProfileVersion` | Versioned activation (one `IsActive` per profile at a time) |
| `config.PromptSection` | Ordered sections within a profile (one per block A/B/C/G/I in this story); `DataStructureType` tells the renderer how to hydrate |
| `config.PromptSectionVariant` | One or more variants per section; **variant-level versioning** per §8 (`VersionNumber`, `IsActive`, `ValidFromUtc`, `ValidToUtc`, optional `ExperimentFlag` / `RolloutPercent`) |
| `config.PromptSectionData` | Optional structured side-data per variant (e.g., `PROHIBITED_TOPICS` JSON list for Block B) |

If the existing `prompt_assembly_profile.py` model is partial, extend it; the migration set in §8 must produce a schema that exactly matches the architecture §3 definitions.

### 2.2 Resolver + Renderer (per architecture §4 + §5)

- **Resolver (Python):** `resolve_prompt_assembly(profile_code, company_id, country_id, audience_locale_code, brand_posture, …) → ordered list of (PromptSection, winning PromptSectionVariant)`.
- **Renderer (Python):** `render_prompt_assembly(resolved_sections, runtime_context) → list of OpenAI ChatCompletion messages` (or string blocks, depending on current message shape).
- The renderer hydrates each section's `DataStructureType`:
  - `Prose` → `PromptSectionVariant.PromptSnippet` (verbatim, with optional `{placeholder}` substitution from runtime context — Block C's `{heritageOrigin}`).
  - `LocaleBlock` → existing `PromptTemplateLocaleBlock` lookup (Block D — no change to the data source for this story).
  - Other `DataStructureType` enums per architecture §3 as needed by Blocks A/B/C/G/I.
- **No SP required for this story.** Architecture §5.4 endorses a hybrid Python-first approach; we can add `usp_ResolvePromptAssembly` later as an optimisation if profiling shows it's needed.
- The renderer is **invoked from** `_build_initial_messages` (in `backend/modules/form_ai/service.py`) — wraps existing inline string construction for the in-scope blocks; out-of-scope blocks (D/E/F/H) continue along their current paths in the same function.

### 2.3 Migrate Stored-Prose Blocks A, B, C, G, I from Code → Registry

| Block | Section code | What gets seeded | Source today |
|-------|--------------|------------------|--------------|
| **A** ROLE_CONTRACT | `ROLE_CONTRACT` | System role prose ("You are an expert semantic form designer…") + `FormSemanticPlan` instructions + consent/layout nudges | Python string literals in `_build_initial_messages` and adjacent helpers |
| **B** SAFETY | `SAFETY` | PII / brand-safety / no-illegal-content prose | Python string literals |
| **C** BRAND_POSTURE | `BRAND_POSTURE` | **Four variants**, one per `VariantCode` matching the four `brandPosture` enum values (`local`, `heritage`, `neutral`, `transcreate`). Renderer selects by current enum value. | Python string literals keyed by enum |
| **G** FEW_SHOT | `FEW_SHOT` | **The current context-pack content from `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md`** seeded into `PromptSectionVariant.PromptSnippet`. This is the change that closes R6. | `_load_context_pack()` reading the MD file from disk |
| **I** JSON_OUTPUT | `JSON_OUTPUT` | "Return a single valid JSON object…" / schema tail prose | Python string literals |

**Block G specifics (R6 fix):**
- The current MD file content is copied verbatim into the seed (preserves behaviour).
- `_load_context_pack()` is **removed** (or kept as a thin deprecation shim that raises a clear error directing readers to the registry — Dev's call; cleaner to delete).
- `_trim_context_pack_for_prompt()` either moves into the renderer or is dropped if the registry variant is already trimmed at seed time. Dev to decide based on what reads simplest.
- The on-disk file `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md` is **kept in the repo** as documentation reference but is no longer read at runtime; add a banner at the top of the MD file noting "Source of truth: `config.PromptSectionVariant` where `SectionCode='FEW_SHOT'` — see migration N3."

**Blocks D, E, F, H out of scope:** their wiring in `_build_initial_messages` is unchanged in this story.

### 2.4 Equivalence Guarantee

For the same inputs (same `companyId`, `countryId`, `audienceLocale`, `brandPosture`, user prompt, etc.), the assembled prompt produced via the new renderer must be **functionally equivalent** to the current `_build_initial_messages` output. "Functionally equivalent" is verified by:

- A regression test that snapshots the current `_build_initial_messages` output for a representative input, then asserts the new renderer produces a string that contains all the same key phrases / section headers / context-pack body.
- Existing form-AI eval harness (`scripts/story_6_2_prompt_eval.py` and related) continues to pass at the previous baseline.
- A single live UAT generation (UAT prompt 1 from 6.5a §7) produces a sensible form (no `context-pack-load-failed`).

### 2.5 Audit / Trace

- `dbo.GenerationRun` records the **variant IDs** used per generation for at minimum Blocks A, B, C, G, I (one column per block, or a JSON snapshot column). This makes "what the LLM actually saw" fully replayable.
- A new audit field on `GenerationRun` named `PromptAssemblyProfileVersionID` records which version of the profile was active at generation time (per §8.2 versioning model).
- `log.ApiRequest` lineage continues unchanged.

### 2.6 Frontend

**No frontend changes in this story.** The AI Agent panel calls the same backend endpoint and receives the same response shape; the renderer change is invisible to the panel.

---

## 3) Out of Scope

| Item | Future home |
|------|-------------|
| Block D (LOCALE) migration into `PromptSectionVariant` | Optional later; existing `PromptTemplateLocaleBlock` path is fine for now and is the architecture's intended source |
| Block E (CLARIFICATION) | **Story 6.5d** |
| Block F (COMPONENT_CAPABILITY) — full GENERATED rewrite via `resolve_allowed_components` | **Story 6.5c** |
| `resolve_allowed_components` authoritative for the frontend toolbox | **Story 6.5c** |
| `ref.BrandPosture` table + replace `brandPosture` enum | **Story 6.5c** |
| `ref.CountryDataType` / `ref.CountryDataTypeValue` | Post-MVP (companion §9) |
| SP `usp_ResolvePromptAssembly` (performance optimisation) | Optional later — only if profiling shows a need |
| Removal of the MD file `STORY-6.2-AI-CONTEXT-PACK.md` from the repo | Out — keep as reference doc with banner |
| Running Alembic | **Tony executes** — agent prepares commands |

---

## 4) Acceptance Criteria

### Schema & Migrations
1. **AC-1** Registry tables exist per architecture §3 with variant-level versioning columns per §8.1 (`VersionNumber`, `IsActive`, `ValidFromUtc`, `ValidToUtc`, optional `ExperimentFlag`, `RolloutPercent`). Where the existing `prompt_assembly_profile.py` model is short of this, it is extended.
2. **AC-2** A single `PromptAssemblyProfile` row seeded (e.g., `Code='FORM_AI_V1'`) with one active `PromptAssemblyProfileVersion`.
3. **AC-3** Five `PromptSection` rows seeded under the profile in the correct `SortOrder`: `ROLE_CONTRACT` (A), `SAFETY` (B), `BRAND_POSTURE` (C), `FEW_SHOT` (G), `JSON_OUTPUT` (I). (Sections for D/E/F sit between but are placeholders or unused this story — Dev's call on whether to seed empty rows or skip.)
4. **AC-4** Each in-scope section has at least one `PromptSectionVariant` row seeded with the current production prose. Block C has **four** variants (`local`, `heritage`, `neutral`, `transcreate`).
5. **AC-5** Block G's variant `PromptSnippet` exactly matches the current `STORY-6.2-AI-CONTEXT-PACK.md` content (after the existing trim — `_trim_context_pack_for_prompt` semantics preserved either at seed time or in the renderer).
6. **AC-6** `GenerationRun` extended with `PromptAssemblyProfileVersionID` and variant-ID columns (or JSON snapshot column) per §2.5.
7. **AC-7** Alembic migrations authored by agent (starting at `073_`), executed by Tony; each migration is reversible (downgrade works) and ordered.

### Resolver & Renderer
8. **AC-8** `resolve_prompt_assembly()` returns the ordered (section, winning-variant) list for given inputs; honours `IsActive` + the variant-versioning rules in §8.2.
9. **AC-9** `render_prompt_assembly()` produces a prompt string (or message list) that for unchanged inputs is functionally equivalent to today's `_build_initial_messages` output for Blocks A, B, C, G, I.
10. **AC-10** `_build_initial_messages` in `backend/modules/form_ai/service.py` invokes the renderer for the in-scope blocks; Blocks D, E, F, H continue along their existing paths unchanged.
11. **AC-11** `_load_context_pack()` is deleted (or replaced with a clear deprecation shim that raises) — no runtime file reads for the context pack.

### Behaviour & R6
12. **AC-12** Existing form-AI eval baseline continues to pass at the previous threshold (no behavioural regression in the harness).
13. **AC-13** **R6 is verified resolved in Test:** UAT prompt 1 (AU + simple registration form) executed via the deployed Test environment produces a successful generation with no `context-pack-load-failed` terminal state.
14. **AC-14** A `GenerationRun` row produced by the UAT contains non-null `PromptAssemblyProfileVersionID` and the expected variant IDs for Blocks A, B, C, G, I — verifiable by SQL.

### Tests & Documentation
15. **AC-15** Backend tests cover:
    - Registry resolver (active version selection, variant selection by `BrandPosture`, fallback to `DEFAULT`).
    - Renderer hydration of `Prose` `DataStructureType`.
    - **Equivalence test**: assembled prompt for representative input contains every key phrase / section header from the current `_build_initial_messages` output.
    - `_load_context_pack` removal — no test that depends on the file read remains.
16. **AC-16** `STORY-6.2-AI-CONTEXT-PACK.md` gets a banner at the top noting it is documentation-only and the runtime source is the registry seed in migration `N3` (whatever number Dev assigns).
17. **AC-17** Closeout report committed at `docs/stories/STORY-6.5b-CLOSEOUT-REPORT.md` covering migration log, R6 verification evidence, and the equivalence-test result.
18. **AC-18** `EPIC-6-STATUS.md` row 6.5b flipped to ✅; R6 row marked **Resolved by 6.5b**.

### Pre-Merge Prompt-Equivalence Diff (Tony Sign-off Gate)
19. **AC-19** **Prompt-equivalence diff produced and signed off before PR Ready-for-Review.**

    Rationale: 6.5b has no frontend change, so Tony cannot eyeball the AI Agent panel for regressions. Instead, Dev produces a deterministic side-by-side diff that proves the new assembled prompt is functionally equivalent to today's.

    **Implementation:**

    1. Dev writes a small helper script `backend/scripts/story_6_5b_prompt_equivalence_diff.py` (or `.ps1` / TS — Dev's call) that:
       - Selects the **most recent successful generation** from the current system. Suggested query (Dev confirms exact column names):
         ```sql
         SELECT TOP 1 GenerationRunID, CompanyID, CountryID, AudienceLocale, BrandPosture, RequestPayload
         FROM dbo.GenerationRun
         WHERE TerminalReason IS NULL  -- successful
         ORDER BY CreatedUtc DESC;
         ```
       - Recovers the inputs (audienceLocale, brandPosture, user prompt, eventId/companyId context) from that row plus the linked `log.ApiRequest` payload.
       - **Path A — Old prompt**: re-assembles via the current `_build_initial_messages` code path (pre-renderer) for the same inputs. Captures the resulting prompt string verbatim.
       - **Path B — New prompt**: re-assembles via the new `render_prompt_assembly()` for the same inputs against the seeded registry. Captures the resulting prompt string verbatim.
       - **Does not call the LLM** in either path — pure assembly only.
       - Produces a structured Markdown report `docs/stories/STORY-6.5b-PROMPT-EQUIVALENCE-DIFF.md` with:
         - **Header**: `GenerationRunID`, inputs (audienceLocale, brandPosture, user prompt excerpt), commit SHA, run timestamp.
         - **Per-block panel** for each block A–I:
           - Block name + section code.
           - `OLD` snippet (from Path A).
           - `NEW` snippet (from Path B).
           - **Source change**: e.g., "A: code literal → `PromptSectionVariant.PromptSnippet` (ID 5)", or "D: unchanged (still `PromptTemplateLocaleBlock`)", or "G: file read → `PromptSectionVariant.PromptSnippet` (ID 9) — **R6 fix point**".
           - **Diff verdict**: ✅ Identical / ⚠️ Whitespace-only / 🔴 Content delta (with the exact diff if 🔴).
         - **Summary table**: 9 rows (blocks A–I), each with verdict and source-change one-liner.
         - **Top-level verdict**: ✅ No behavioural regression / ⚠️ Cosmetic only / 🔴 Investigation required.

    2. Dev runs the script against a local environment with the new migrations applied, commits the resulting Markdown to the story branch, and pings Tony for sign-off.

    3. **Tony reviews the diff and approves "no behavioural degradation" before the PR is moved from Draft → Ready for Review.** If the verdict is 🔴 or ⚠️ with non-trivial content delta, Dev investigates and re-runs until the verdict is ✅ (or Tony explicitly accepts the delta).

    4. The same script is re-run **after** UAT prompt 1 succeeds in Test (AC-13) to confirm Test-environment behaviour matches local — diff file updated with both rows in the header.

---

## 5) Definition of Done

- Story branch pushed; new Draft PR (→ `develop`) marked **Ready for Review** **only after Tony signs off the prompt-equivalence diff (AC-19)**.
- All 19 ACs met and verified.
- Migration files prepared, executed by Tony, recorded in the migration log; downgrades verified locally.
- CI pre-deploy smoke (PR #99 pattern) green on the PR; auto-deploy to Test succeeds.
- **R6 verified resolved in Test** (UAT prompt 1 produces successful generation).
- Equivalence test green; eval harness baseline still green.
- Prompt-equivalence diff report (`docs/stories/STORY-6.5b-PROMPT-EQUIVALENCE-DIFF.md`) committed with Tony's sign-off recorded.
- `EPIC-6-STATUS.md` updated; closeout report committed.
- No Alembic commands run by the agent (Tony executes; agent provides exact commands).

---

## 5a) Local Validation Flow (Avoid Azure Cycle Time)

6.5b has no frontend change, which means **every iteration can be validated locally without waiting for an Azure deploy**. This is critical for the prompt-equivalence diff (AC-19) where Tony may want multiple iterations before sign-off.

### Local stack required

| Component | Local equivalent | Notes |
|-----------|------------------|-------|
| Backend | `uvicorn backend.main:app --reload` | Same `/api/form-ai/generate` Azure exposes |
| Database | SQL Server LocalDB (or whichever the project uses for dev) | Apply migrations 073→078 locally first; Tony executes Alembic |
| AI provider | OpenAI / Azure OpenAI via `.env` | Real generation responses, billable to dev key |
| Email | MailHog (already wired) | Not exercised by 6.5b |
| Frontend (optional) | `cd frontend && npm run dev` against local backend | Only needed if Dev wants UI to drive the API; not required for AC-19 since the equivalence script runs headless |

### Iteration loop (no Azure)

```
1. Edit code in worktree
2. Restart uvicorn (or rely on --reload)
3. Run the equivalence script: python backend/scripts/story_6_5b_prompt_equivalence_diff.py
4. Review the generated docs/stories/STORY-6.5b-PROMPT-EQUIVALENCE-DIFF.md
5. If diff verdict is 🔴 or ⚠️ unexpected, fix and go back to step 1
6. When verdict is ✅, commit + push → Tony reviews diff in GitHub
7. After Tony signs off, mark PR Ready for Review → CI smoke → auto-deploy to Test
8. Re-run equivalence script against Test (or smoke-check UAT prompt 1) for AC-13 / AC-14
```

### What you do NOT need Azure for

- Schema correctness (Alembic upgrade + downgrade locally)
- Resolver / renderer behaviour
- Block-by-block equivalence to the current `_build_initial_messages` output
- R6 conceptual fix (no file read remains)
- Eval harness regression baseline

### What you DO need Azure for (final gate only)

- Verifying R6 is gone in the **actual** Test environment (AC-13) — proves the deploy package no longer needs the MD file
- UAT against the deployed Test infrastructure (release blocker)
- App Insights / log lineage check in production-equivalent infra

**Net effect:** Azure deploy becomes a release gate, not an iteration tool. If Dev needs N iterations to land the renderer cleanly, all N happen locally in seconds-to-minutes rather than 20-minute Azure round-trips.

---

## 6) Evidence & References

**Architecture (authoritative):**
- `docs/architecture/prompt-assembly-registry-architecture.md` — §2.7 (post-impl block sources), §3 (registry schema), §5 (renderer contract), §8 (variant versioning), §10 (sequencing)
- `docs/architecture/decision-6.5a-clarification-options-data-model.md` — §4.1 (all-blocks-DB-driven platform rule)

**Code touch points:**
- `backend/modules/form_ai/service.py` — `_build_initial_messages`, `_load_context_pack` (delete), `_trim_context_pack_for_prompt` (move or delete)
- `backend/models/config/prompt_assembly_profile.py` — verify/extend
- `backend/models/config/prompt_template.py`, `prompt_template_version.py` — referenced, not changed in this story
- `backend/migrations/versions/` — new migrations starting at `073_`
- `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md` — add documentation-only banner

**Prior story context:**
- Story 6.5a — Architecture Phase (closed) — `docs/stories/story-6.5a.md`
- Story 6.4.4.1 — Locale Architecture ADR (Block D still uses this path)
- Story 6.4.8 — AU production prompt context (migration 072)
- PR #101 — release reconciliation (R6 carry-forward — resolved by this story)
- PR #102 — Story 6.11 Production Deployment Blueprint

---

## 7) Planned Migration Set (agent prepares, Tony executes)

Suggested decomposition starting at `073_` (Dev may consolidate; each must be reversible):

| # | Migration | Description |
|---|-----------|-------------|
| 073 | `story_65b_prompt_assembly_registry_schema` | Create/extend `PromptAssemblyProfile`, `PromptAssemblyProfileVersion`, `PromptSection`, `PromptSectionVariant`, `PromptSectionData` per architecture §3 + §8.1 |
| 074 | `story_65b_seed_form_ai_v1_profile` | Seed `PromptAssemblyProfile` (`FORM_AI_V1`) + one active `PromptAssemblyProfileVersion` + five `PromptSection` rows (A, B, C, G, I) |
| 075 | `story_65b_seed_variants_a_b_i` | Seed `PromptSectionVariant` rows for Blocks A, B, I (each one default variant) |
| 076 | `story_65b_seed_brand_posture_variants_c` | Seed four `PromptSectionVariant` rows for Block C (one per `brandPosture` enum value) |
| 077 | `story_65b_seed_few_shot_variant_g` | Seed Block G variant from current `STORY-6.2-AI-CONTEXT-PACK.md` content (**this is the R6 fix migration**) |
| 078 | `story_65b_generation_run_assembly_audit` | Add `PromptAssemblyProfileVersionID` and variant-ID columns (or JSON snapshot) to `dbo.GenerationRun` |

May be consolidated; downgrade paths required.

---

## 8) Carry-forward Backlog Triggered or Confirmed by This Story

| Item | Trigger story |
|------|---------------|
| Block F (COMPONENT_CAPABILITY) full GENERATED rewrite | **Story 6.5c** |
| `resolve_allowed_components` authoritative for toolbox + Blocks A/F/I | **Story 6.5c** |
| `ref.BrandPosture` + retire `brandPosture` enum | **Story 6.5c** |
| Block E (CLARIFICATION) + `ref.AudienceLocale` / `ref.FormPurpose` / `ref.RespondentType` + APIs + dropdowns | **Story 6.5d** |
| Block D (LOCALE) migration into `PromptSectionVariant` (currently fine via existing `PromptTemplateLocaleBlock`) | Optional later |
| SP `usp_ResolvePromptAssembly` | Optional — perf optimisation only |
| `ref.CountryDataType` / `ref.CountryDataTypeValue` | Post-MVP |
| Multi-locale form snapshots, 4th clarification dropdown, browser `Accept-Language` detection | Post-MVP |

---

**Next:** Once 6.5b ships and R6 is verified resolved in Test, draft `story-6.5c.md` (Capability Catalog Cutover).
