# Story 6.5d — Clarification Data Plane + Component Catalog Completion

**Epic:** 6 — AI Generation & Monetization Engine  
**Story ID:** 6.5d  
**Title:** Clarification dropdowns + Block E registry + catalog backlog + AU address-lookup + component registration process  
**Status:** Ready for Dev  
**Branch:** `story/epic6-6.5d-clarification-component-platform`  
**PR:** [#109](https://github.com/anthonykeevy/EventLeadPlatform/pull/109) — Draft → `develop`  
**Created:** 2026-05-21  
**Size:** L–XL (two tracks; single story per product decision)

**Depends On:**
- Story 6.5b ✅ — Prompt Assembly Registry (`PromptAssemblyRegistry*`, resolver/renderer)
- Story 6.5c ✅ — `resolve_allowed_components`, init-only toolbox, Block F registry, `ref.BrandPosture`
- Architecture: `docs/architecture/decision-6.5a-clarification-options-data-model.md` (Rev 9)
- Architecture: `docs/architecture/prompt-assembly-registry-architecture.md` (§2.7 Block E)
- Architecture: **`docs/architecture/decision-external-data-feed-components.md`** — **Tony + architect sign-off before Track A code**

**Unblocks:** Epic 6 clarification-aware generation at scale; clean catalog for AI + builder; Story 6.5e+ without ghost types.

---

## 1) Goal

Deliver **two related outcomes** in one story (Tony-approved):

### Track A — Component catalog completion (closes 6.5c §3 tech debt)

1. **Seed missing `FormBuilderComponent` rows** so toolbox, AI, and validator agree with historical capability/context vocabulary.
2. **Add AU online address component** (`address-lookup-au`, Country-scoped) as the reference implementation of country-specific catalog entries.
3. **Publish and enforce** `docs/workflows/ADD-COMPONENT-TO-PLATFORM-CHECKLIST.md` plus automation (`verify_component_catalog_alignment.py`).
4. Align Block G / prompt prose so the LLM is not instructed to emit types that are not in the catalog.

### Track B — Clarification data plane (original 6.5a implementation)

1. Three `ref.*` tables + seeds: `AudienceLocale`, `FormPurpose`, `RespondentType`.
2. Three read APIs: list + resolved default for AI Agent panel.
3. Block **E** (E1/E2/E3) in Prompt Assembly Registry; injected via renderer.
4. `Company` / `Form` / `GenerationRun` persistence + audit.
5. **Delete** `AudienceLocale` TypeScript/Python enums from the generation path; panel loads from APIs only.

---

## 2) Track A — Component catalog (detailed scope)

### 2.1 Missing global components (seed into `FormBuilderComponent`)

Restore types that exist in **renderer** and/or historical `ComponentCapabilitySnapshot` JSON but were **never** in migration 039 seeds (see `STORY-6.5c-CLOSEOUT-REPORT.md` §3):

| ComponentCode | Scope | Notes |
|---------------|-------|-------|
| `rating` | Global | Stars/numbers; align with registry renderer |
| `url` | Global | URL input |
| `file-upload` | Global | Story 6.2.2 attachment contract |
| `paragraph` | Global | Display-only content block |
| `address` | Global | Generic address field (existing renderer) |

**Explicitly out of scope unless Tony requests:** `last-name` (dropped in migration 057 — no frontend renderer parity; use `text` with name labels).

### 2.2 AU online address (`address-lookup-au`)

| Property | Value |
|----------|--------|
| `ComponentCode` | `address-lookup-au` (or `address-lookup` + country scope — Dev picks one canonical code; document in closeout) |
| Scope | **Country** — AU `CountryID` only |
| Behaviour | Online autocomplete via **GeoScape/PSMA** (see `docs/architecture/au-address-lookup-geoscape-handoff.md`; working reference in JobTrackerDB) |
| Proof | Appears in init for AU event; **absent** for non-AU country fixture |
| **Offline forms** | **First network-dependent component.** When customer requires form to run **offline**, exclude from catalog/resolver/AI/validator; keep manual `address` as fallback. |

**Dev handoff:** `docs/architecture/au-address-lookup-geoscape-handoff.md` (API base `https://api.psma.com.au`, env `GEOSCAPE_API_KEY`).

### 2.2b ABR company lookup (`company-lookup-abr`) — mandatory with address

| Property | Value |
|----------|--------|
| `ComponentCode` | `company-lookup-abr` |
| Scope | **Country** — AU |
| Behaviour | Same **EDF pattern** as address; reuse onboarding ABR (`abr_client.py`, `companies/router.py`) — `docs/architecture/abr-company-lookup-builder-handoff.md` |
| **Offline forms** | Same exclusion rule as `address-lookup-au` |
| **Why same story** | One shared design for `RequiresNetwork`, proxy APIs, init metadata, toolbox badge, offline filter |

### 2.3 Formal process + automation

| Deliverable | Path |
|-------------|------|
| Checklist (SM-authored, Dev validates in UAT) | `docs/workflows/ADD-COMPONENT-TO-PLATFORM-CHECKLIST.md` |
| Alignment script | `backend/scripts/verify_component_catalog_alignment.py` |
| SM registry entry | `docs/stories/EPIC-6-SM-TOOLS-REGISTRY.md` |
| Tests | `backend/tests/test_story_6_5d_catalog_alignment.py` |

Script must exit non-zero on mismatch and print diff of code sets (init vs resolver vs prompt fragment vs validator).

### 2.4 Prompt prose hygiene

- Update registry Block G variant (new migration) or `PromptSectionData` so FEW_SHOT prose only references **catalog-resident** types for AU and global fixtures.
- No requirement to change LLM behaviour for types that remain unseeded (e.g. `last-name`).

---

## 3) Track B — Clarification data plane (detailed scope)

Per `decision-6.5a-clarification-options-data-model.md` §11 seeds and §12 schema:

### 3.1 Reference tables + APIs

| Table | API (suggested) |
|-------|-----------------|
| `ref.AudienceLocale` | `GET /api/ref/audience-locales` |
| `ref.FormPurpose` | `GET /api/ref/form-purposes` |
| `ref.RespondentType` | `GET /api/ref/respondent-types` |

Each API returns: `{ items: [...], defaultCode, resolvedDefault }` using Company → Form → request override chain per architecture.

### 3.2 Schema

- `Company`: `DefaultAudienceLocaleCode`, `DefaultFormPurposeCode`, `DefaultRespondentTypeCode` (or FK IDs — follow existing ref patterns from 6.5c `BrandPostureID`).
- `Form`: persist selected clarification codes for panel restore.
- `GenerationRun`: store resolved clarification codes / FKs for replay.

### 3.3 Prompt registry — Block E

- Add `PromptSection` `CLARIFICATION_*` rows (E1 audience, E2 purpose, E3 respondent) per architecture §2.7.
- `DataStructureType` = clarification / prose injection pattern from architecture.
- Renderer loads text from resolved ref rows (not hardcoded enums).

### 3.4 Frontend — AI Agent panel

- Three dropdowns populated **only** from ref APIs.
- Remove `AudienceLocale` enum imports from generation client types where feasible.
- Pass selected codes on generate request; backend resolves defaults when null.

**Out of scope:** Fourth "Industry" dropdown (§16 architecture); Company Settings brand posture UI (`g-6441` carry-forward).

---

## 4) Acceptance criteria

| ID | Criterion |
|----|-----------|
| **Catalog** |
| AC-1 | Migration seeds global components: `rating`, `url`, `file-upload`, `paragraph`, `address` (minimum set above). |
| AC-2 | Migration seeds **Country-scoped** `address-lookup-au` (AU only); verified absent for non-AU fixture. |
| AC-2b | Offline-capable form context **excludes** `address-lookup-au` (and any `RequiresNetwork` types); manual `address` remains available. |
| AC-2c | `company-lookup-abr` seeded + wired under same EDF pattern as `address-lookup-au`. |
| AC-2d | `decision-external-data-feed-components.md` approved; framework GUIDE + REFERENCE + checklist updated. |
| AC-3 | `verify_component_catalog_alignment.py` passes for AU + global fixtures; registered in `EPIC-6-SM-TOOLS-REGISTRY.md`. |
| AC-4 | `ADD-COMPONENT-TO-PLATFORM-CHECKLIST.md` reviewed; closeout confirms each new component satisfied checklist §1–7. |
| AC-5 | Block G / context prose does not instruct disallowed ghost types for seeded markets. |
| **Clarification** |
| AC-6 | `ref.AudienceLocale`, `ref.FormPurpose`, `ref.RespondentType` exist with §11 seed data. |
| AC-7 | Three ref APIs return sorted active rows + resolved default. |
| AC-8 | Block E injected via registry renderer using resolved clarification text. |
| AC-9 | `Company` / `Form` / `GenerationRun` extended; values persisted on generate. |
| AC-10 | AI Agent panel uses API-driven dropdowns; no frontend enum for audience locale. |
| AC-11 | Alembic migrations `087+` (reversible); Tony executes — agent does not run Alembic. |
| **Quality** |
| AC-12 | Focused 6.5d tests green; 6.5b/6.5c regression tests still pass. |
| AC-13 | `STORY-6.5d-IMPLEMENTATION-FRICTION-LOG.md` completed by Dev. |
| AC-14 | `STORY-6.5d-CLOSEOUT-REPORT.md` (mandatory — APIs + migrations + catalog). |
| AC-15 | Local UAT: toolbox shows new types; AU address only on AU context; clarification dropdowns work; AI generate succeeds. |

---

## 4b) Recommended chat workflow (Tony clarity)

| Phase | Chat | Actor | Outcome |
|-------|------|-------|---------|
| **A — Architecture** | **Separate** chat (optional: Dimitri + architect agents) | Tony + data/architect | Approve `decision-external-data-feed-components.md` v2 (§9 closed); **no implementation** |
| **B — Implementation** | **New** chat in worktree `C:\wt\elp\story-epic6-6.5d-clarification-component-platform` | `@bmad-agent-bmm-dev` | Track A + B per dev prompt |

**Not recommended:** one chat that both finalizes architecture and implements — context drift, mixed roles, and harder review. SM default: **sign-off doc first, then Dev chat.**

---

## 5) Local validation flow

1. Tony: `alembic upgrade head` (from `086` → new head).
2. `python backend/scripts/verify_component_catalog_alignment.py` (params for AU company/event).
3. Local uvicorn + frontend: builder init, toolbox, AI panel dropdowns, generate form.
4. Do **not** wait for Azure for iteration; Test verifies after merge.

---

## 6) Planned migrations (preview; confirm head `086`)

| Rev | Purpose |
|-----|---------|
| `087` | Seed global catalog backlog (`rating`, `url`, `file-upload`, `paragraph`, `address`) |
| `088` | Seed AU `address-lookup-au` + `ref.ComponentType` if missing |
| `089`–`091` | `ref.AudienceLocale`, `ref.FormPurpose`, `ref.RespondentType` + seeds |
| `092` | Company/Form clarification columns |
| `093` | GenerationRun clarification audit columns |
| `094` | Block E registry sections + variants |
| `095` | Block G prose trim (catalog-aligned) — optional combine with 087 |

---

## 7) Dev closeout artifacts

| Artifact | Owner |
|----------|-------|
| `STORY-6.5d-GATE-EVIDENCE.md` | Dev |
| `STORY-6.5d-UAT-RESULTS.md` | Tony |
| `STORY-6.5d-IMPLEMENTATION-FRICTION-LOG.md` | Dev |
| `STORY-6.5d-CLOSEOUT-REPORT.md` | Dev |
| SM updates `EPIC-6-STATUS.md`, `EPIC-6-WORKFLOW-GUIDE.md`, carry-forward | SM |

---

## 8) References

- `STORY-6.5c-CLOSEOUT-REPORT.md` §3 — catalog drift rationale  
- `docs/workflows/ADD-COMPONENT-TO-PLATFORM-CHECKLIST.md`  
- `docs/stories/EPIC-6-SM-TOOLS-REGISTRY.md`  
- `backend/modules/form_builder/component_catalog.py` — resolver to extend, not duplicate  
