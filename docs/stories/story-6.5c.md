# Story 6.5c — Capability Catalog Cutover

**Epic:** 6 — AI Generation & Monetization Engine  
**Story ID:** 6.5c  
**Title:** Capability Catalog Cutover — `resolve_allowed_components` authoritative + Block F registry + `ref.BrandPosture` + toolbox alignment  
**Status:** Ready for Dev  
**Branch:** `story/epic6-6.5c-capability-catalog-cutover`  
**PR:** [#106](https://github.com/anthonykeevy/EventLeadPlatform/pull/106) — Draft → `develop`  
**Created:** 2026-05-20  
**Depends On:**
- Story 6.5b merged to `develop` (PR #104 + housekeeping PR #105) — Prompt Assembly Registry foundation, migrations `078`–`083`
- Architecture docs:
  - `docs/architecture/prompt-assembly-registry-architecture.md` — **§2.5** (toolbox–prompt alignment), **§2.6** (country-scoped capability), **§2.7** (Blocks A/F/I sources)
  - `docs/architecture/decision-6.5a-clarification-options-data-model.md` — companion

**Unblocks:**
- Story 6.5d — Clarification Data Plane (Block E + dropdowns; benefits from `ref.BrandPosture` precedent)

---

## 1) Goal

Make **one catalog resolver** the only source of truth for which component types exist for a given `CompanyID` + `CountryID`. Wire that resolver into **four consumers** so they always agree:

1. **Form Builder toolbox** (`POST /api/form-builder/init` → `components[]`)
2. **Form AI Block F** (capability guidance prose)
3. **Form AI Blocks A / I** (allowed `componentType` contract fragments)
4. **Semantic validator** (reject unknown types against the same set)

Additionally:
- Migrate **Block F** into the Prompt Assembly Registry as a `GENERATED` / `DynamicComponentCatalog` section (prose shell in DB; list filled at render time).
- Introduce **`ref.BrandPosture`** and re-wire Block C variant selection (replacing the Python `brandPosture` enum string path).
- Optionally reconcile naming: architecture `PromptAssemblyProfile*` vs implementation `PromptAssemblyRegistry*` (see 6.5b closeout) — **document the decision**; full rename only if low-risk.

**What this story does NOT do** (Story 6.5d):
- Clarification dropdowns, Block E, `ref.AudienceLocale` / `FormPurpose` / `RespondentType` APIs.
- Block D migration into registry (may land here only if trivial; otherwise defer to 6.5d).

---

## 2) In Scope

### 2.1 `resolve_allowed_components` (authoritative catalog service)

- Implement `resolve_allowed_components(db, company_id, country_id) -> ResolvedComponentCatalog` in a dedicated module (e.g. `backend/modules/form_builder/component_catalog.py` or `backend/modules/form_ai/component_catalog.py`).
- **Behaviour:** Same query semantics as today's `get_allowed_components()` in `backend/modules/form_builder/service.py` (Global ∪ Country ∪ Company). Refactor so `get_allowed_components` is a thin wrapper or alias — **one implementation**.
- Return shape must include everything consumers need:
  - `componentCode`, `displayName`, width-class metadata for prompt rendering, and fields required by init payload / validator.
  - Stable sorted order (match current `SortOrder`, `DisplayName`).
- Add unit tests proving country scoping (e.g. AU-only `address-lookup-au` appears only when `country_id` is AU).

### 2.2 Form AI — retire `ComponentCapabilitySnapshot` as allowed-type source

- `_build_initial_messages` / `_resolve_rendered_assembly` must call `resolve_allowed_components` instead of loading `config.ComponentCapabilitySnapshot` for the allowed-type list.
- `_build_capability_prompt_block` accepts catalog output from the resolver (not snapshot JSON blob).
- Semantic validator uses the **same** resolved catalog object in the request path (no third list).
- `GenerationRun.ComponentCapabilitySnapshotID` — **deprecate for new runs** or populate only for audit backward-compat; document in closeout. Prefer storing resolved catalog hash or JSON on existing `PromptVariantSnapshot` extension / new optional column only if needed for replay (minimize scope).

### 2.3 Prompt registry — Block F (+ dynamic fragments for A / I)

- Add `PromptSection` row: `SectionCode = 'COMPONENT_CAPABILITY'` (Block F), `DataStructureType = 'DynamicComponentCatalog'` (or architecture-equivalent enum value).
- Seed a **prose shell** variant (static instructions; dynamic list injected at render time).
- Extend `render_prompt_assembly` / renderer to:
  - Call `resolve_allowed_components` when hydrating Block F and Blocks A/I sections marked `DynamicComponentCatalog`.
  - Inject allowed `componentType` list into contract fragments (Block A tail / Block I per current assembly order in `service.py`).
- Preserve **byte-equivalence or explicit improvement** vs 6.5b for AU default inputs — run an equivalence-style diff or focused integration test (see AC-15).

### 2.4 `ref.BrandPosture` + Block C re-wire

- Create `ref.BrandPosture` (Code, DisplayName, SortOrder, IsActive) seeded with `local`, `heritage`, `neutral`, `transcreate`.
- Migrate `dbo.Company.BrandPosture` from free-text / enum string to FK → `ref.BrandPosture` (or add `BrandPostureID` column — follow existing ref-table patterns).
- API request field: accept `brandPosture` code; resolve via ref table for Block C variant selection in registry resolver.
- Update frontend AI panel posture picker to load from API/ref (not hardcoded enum) if the picker exists in scope; otherwise backend-only with follow-up noted in closeout.

### 2.5 Frontend toolbox alignment (mandatory)

- On Form Builder load, toolbox palette is built **only** from `POST /api/form-builder/init` `components[]`.
- Hide component types not returned by init (no static `ComponentRegistry.tsx` superset for palette).
- Re-fetch init when company/event context changes.
- Map `componentCode` → existing renderer entries; unknown codes fail gracefully (hidden + log).

### 2.6 Tests & evidence

- Backend: resolver tests, prompt block tests, validator alignment tests, migration static tests.
- Frontend: unit test(s) for toolbox filtering from init mock.
- `STORY-6.5c-GATE-EVIDENCE.md` with pytest summaries.
- Optional: catalog-alignment script (toolbox codes vs prompt ALLOWED list vs validator) for Tony UAT.

---

## 3) Out of Scope

- Block E clarification plane (6.5d).
- Full `PromptAssemblyRegistry` → `PromptAssemblyProfile` table rename (unless trivial; else document + 6.5d/tech-debt).
- Eval harness prompt-candidate sweeps.
- Production deploy / Story 6.11.

---

## 4) Acceptance Criteria

| ID | Criterion |
|----|-----------|
| AC-1 | `resolve_allowed_components(db, company_id, country_id)` exists and is the **only** implementation of the Global∪Country∪Company component query. |
| AC-2 | `get_allowed_components` / `build_init_payload` call the resolver (no duplicate SQL). |
| AC-3 | `POST /api/form-builder/init` `components[]` matches resolver output for the same inputs. |
| AC-4 | Form AI generation does **not** read `ComponentCapabilitySnapshot` for allowed types; uses resolver output. |
| AC-5 | Block F rendered via registry (`COMPONENT_CAPABILITY` section) with dynamic catalog injection. |
| AC-6 | Blocks A/I include allowed `componentType` list from the **same** resolver call as Block F. |
| AC-7 | Semantic validator rejects unknown `componentType` against resolver set (integration test). |
| AC-8 | `ref.BrandPosture` seeded; Company + generation path resolve posture through ref table. |
| AC-9 | Block C registry resolver selects variant by `ref.BrandPosture.Code` (not hardcoded enum-only path). |
| AC-10 | Frontend toolbox shows only init-returned components (test or UAT evidence). |
| AC-11 | Alembic migrations `084+` authored (reversible); Tony executes — agent does not run Alembic. |
| AC-12 | Country-scoped component test: AU-only code appears in all four consumers for AU, absent for non-AU. |
| AC-13 | Existing 6.5b registry tests remain green; new 6.5c focused suite green. |
| AC-14 | `STORY-6.5c-CLOSEOUT-REPORT.md` (mandatory — API + migrations). |
| AC-15 | Catalog alignment verification documented (script output or test) — toolbox = prompt = validator for representative AU input. |

---

## 5) Local Validation Flow

1. `alembic upgrade head` (Tony) — migrations `084+`.
2. `uvicorn` + `npm run dev` in worktree.
3. Open Form Builder for AU event — confirm toolbox matches DB catalog (no extra types).
4. AI Generate Form Draft — confirm ALLOWED types in trace match toolbox; no `unknown-component-type` for allowed palette types.
5. Change event to non-AU country — re-init; confirm AU-only types disappear from toolbox and prompt.

---

## 6) Planned Migration Set (preview)

| Rev | Purpose |
|-----|---------|
| `084` | `ref.BrandPosture` table + seed |
| `085` | `Company.BrandPostureID` (or FK migration from string) |
| `086` | Block F `PromptSection` + prose-shell variant |
| `087+` | As needed for data fixes / snapshot deprecation markers |

Dev confirms exact numbering against current alembic head (`083`) at implementation time.

---

## 7) Carry-Forward / Tech Debt

- `ComponentCapabilitySnapshot` table may remain for historical `GenerationRun` rows; document read-only status.
- `PromptAssemblyRegistry*` vs `PromptAssemblyProfile*` naming reconciliation.
- Block D into registry (6.5d or follow-up).
- Pre-existing form_ai mock test failures (see 6.5b gate evidence).

---

## 8) References

- `docs/stories/STORY-6.5b-CLOSEOUT-REPORT.md` — what 6.5b delivered  
- `backend/modules/form_builder/service.py` — `get_allowed_components` (today's query)  
- `backend/modules/form_ai/service.py` — `_build_capability_prompt_block`, snapshot load path  
- `backend/tests/test_form_ai_prompt_capabilities.py` — capability block tests to extend  
