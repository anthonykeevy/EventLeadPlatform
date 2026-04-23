# Story 6.3.1 — Simplified AI Output + Deterministic Layout Foundation

**Epic:** 6 — AI Generation & Monetization Engine  
**Story ID:** 6.3.1  
**Title:** Simplified AI Output + Deterministic Layout Foundation  
**Status:** ✅ **Complete** (2026-04-15)  
**Branch:** `story/epic6-6.3.1-simplified-ai-deterministic-layout`  
**PR:** [#64](https://github.com/anthonykeevy/EventLeadPlatform/pull/64)  
**Depends On:** Story 6.3 (✅ Closed as learning)  
**Unblocks:** Story 6.4 (AI Iteration on Existing Designs)  
**Created:** 2026-04-15  
**Completed:** 2026-04-15

---

## 1) Goal

Improve first-shot UAT reliability by splitting responsibilities:

1. AI returns a **simplified intent contract** (fields, labels, options, grouping hints, priority), not precision geometry math.
2. Backend/frontend apply a **deterministic layout planner** and post-processing rules for spacing, alignment, bounds, and collision prevention.
3. Trace/logs preserve **raw AI output vs transformed final definition** so tuning remains observable.

This story is the architectural bridge between Story 6.3 learning outcomes and Story 6.4 conversational edits.

---

## 2) In Scope

### 2.1 Simplified generation contract (AI output)

| Area | Requirement |
|------|-------------|
| **Contract shape** | Define a reduced schema for AI output focused on structure and intent: component list, semantic groups/sections, required flags, options, and optional relative ordering hints. |
| **No hard coordinates** | AI should not be responsible for final `x`, `y`, or pixel-perfect width/height math in this mode. |
| **Validation** | Add schema validation for simplified payload and deterministic conversion errors. |
| **Fallback behavior** | If simplified payload fails contract validation, return clear user-facing failure plus trace details. |

### 2.2 Deterministic layout planner

| Area | Requirement |
|------|-------------|
| **Planner stage** | Add a dedicated planner that converts simplified AI payload into valid `DefinitionJSON` with deterministic geometry. |
| **Geometry source** | Use one canonical footprint source for component min sizes and spacing defaults. |
| **Rules** | Enforce single-page bounds, non-overlap, deterministic tab order, and consistent vertical rhythm. |
| **Extensibility** | Planner logic must be modular so Story 6.4 can request scoped changes without re-generating entire forms. |

### 2.3 Post-processing rationalization

| Area | Requirement |
|------|-------------|
| **Explicit transforms** | Keep post-processing steps explicit and flag-driven, with defaults documented. |
| **Mutation visibility** | Every transform applied must be reflected in trace metadata/log output. |
| **Raw vs final** | Return/store both raw simplified payload and final transformed definition in trace context (or equivalent debug artifact). |

### 2.4 Quality and benchmark evidence

| Area | Requirement |
|------|-------------|
| **Benchmark rerun** | Re-run 10-benchmark mocked harness against new planner pipeline. |
| **First-shot emphasis** | Add explicit first-shot score summary (before correction retries) in baseline evidence. |
| **UAT criterion** | Human UAT requires stable, visible canvas output on at least two benchmark prompts without manual patching. |

### 2.5 Logging, extraction, and single-change tuning discipline

| Area | Requirement |
|------|-------------|
| **Canonical logging workflow** | Use `docs/AGENT-LOGGING-GUIDE.md` as canonical diagnosis workflow for Form AI traces and failures. |
| **Correlation extraction** | For each benchmark/tuning run, capture inbound `RequestID` and correlated outbound chain evidence from `log.ApiRequest` (including `:outbound:` rows) and trace terminal reason. |
| **Single-variable changes** | During tuning, only one meaningful variable is changed per run (prompt section/policy flag/layout rule/validation mapping) so causality is measurable. |
| **Run ledger** | Maintain an experiment ledger linking: run ID, changed variable, expected effect, observed metrics (first-shot + final), and decision (keep/revert). |

### 2.6 Story pack requirements for SM delivery

| Area | Requirement |
|------|-------------|
| **Context artifact** | SM delivery includes `docs/stories/story-context-6.3.1.xml` as the implementation map for Dev. |
| **Prompt artifact** | SM delivery includes `docs/stories/STORY-6.3.1-SINGLE-SESSION-DEV-PROMPT.md` with explicit Step 0 preflight and logging workflow references. |
| **UAT artifact** | SM delivery includes `docs/stories/STORY-6.3.1-UAT-TEST-GUIDE.md` including RequestID/correlation capture steps. |

---

## 3) Out of Scope

| Item | Reason |
|------|--------|
| Story 6.4 conversational edit commands | Separate story; relies on this foundation |
| Multi-page generation | Remains out of scope for this phase |
| New model providers | Not needed for architectural split |

---

## 4) Acceptance Criteria

1. **AC-1 (Simplified contract):** `/api/form-ai/generate` supports simplified AI output mode where model response is schema-valid without requiring explicit pixel geometry.
2. **AC-2 (Deterministic planner):** Planner deterministically maps simplified output to valid `DefinitionJSON` with no collisions/boundary violations on benchmark fixtures that are expected to pass.
3. **AC-3 (Trace clarity):** Trace/logs include raw AI payload summary plus final transformed definition summary, including transform steps applied.
4. **AC-4 (Post-processing flags):** Key post-processing steps are individually toggleable via config/env and documented in `docs/FORM-AI-POST-PROCESSING-GUIDE.md`.
5. **AC-5 (Benchmark evidence):** Updated baseline file records first-shot + final outcomes for all 10 benchmarks.
6. **AC-6 (Builder visibility):** In-app Generate still applies result onto builder canvas and remains selectable/editable.
7. **AC-7 (Regression safety):** Existing Story 6.2/6.3 tests remain green or are intentionally updated with rationale.
8. **AC-8 (Capability auto-ingestion):** Capability registry data used by Step 1/Step 2 is produced from a versioned machine-readable snapshot pipeline sourced from component framework metadata (registry/capability sources), not ad-hoc manual duplication.
9. **AC-9 (Per-component validation contract):** Compiler validation normalization is driven by structured per-component contracts (allowed rules, parameter schema, compatibility constraints, and message policy) and rejects unsupported rule/component combinations deterministically.
10. **AC-10 (Canvas-responsive width classes):** Width intents (`compact`, `half`, `full`) are resolved against current canvas settings (width/grid), with deterministic class-to-span/px mapping, per-component bounds enforcement, and documented fallback/downgrade rules.
11. **AC-11 (Version traceability):** Every generation run records prompt/template version IDs, capability snapshot version, validation contract version, and width policy version so runs are replayable/auditable.
12. **AC-12 (Framework-driven capability coverage):** Capability snapshot generation is explicitly derived from component framework sources and validated against `docs/COMPONENT-FRAMEWORK-REFERENCE.md` so new components/features are included without manual drift.
13. **AC-13 (Single-change evidence discipline):** Gate evidence demonstrates at least one controlled tuning sequence where each run changes only one variable and includes correlated logging evidence (`RequestID` chain + terminal reason + validation counts) per `docs/AGENT-LOGGING-GUIDE.md`.
14. **AC-14 (SM context pack completeness):** Story cannot move to Dev execution until SM artifacts exist for `story-context-6.3.1.xml`, `STORY-6.3.1-SINGLE-SESSION-DEV-PROMPT.md`, and `STORY-6.3.1-UAT-TEST-GUIDE.md`.

---

## 5) Definition of Done

- [x] Story ACs met with evidence in `STORY-6.3.1-GATE-EVIDENCE.md`
- [x] `python -m pytest --tb=short` green (705 passed, 26 skipped, 0 failed — 2026-04-15)
- [x] `npm run lint` and `npm run test:unit -- --watch=false` green (0 lint warnings; 272 tests passed)
- [x] Human UAT pass recorded in `STORY-6.3.1-UAT-RESULTS.md` against `STORY-6.3.1-UAT-TEST-GUIDE.md` (rounds 1–11; final disposition PASS)
- [x] Evidence includes capability snapshot artifact (migrations 053–057) and trace example showing all version IDs (`FORM_AI_CAPABILITY_POLICY:v1`, `FORM_AI_WIDTH_POLICY:v1`, validation contracts active, prompt template versions)
- [x] Evidence includes correlated log extraction (`RequestID` + outbound chain) and one-variable-at-a-time tuning sequence (UAT rounds 4–11)
- [x] SM story pack artifacts exist: `story-context-6.3.1.xml`, `STORY-6.3.1-SINGLE-SESSION-DEV-PROMPT.md`, `STORY-6.3.1-UAT-TEST-GUIDE.md`
- [x] Story closeout updates in `EPIC-6-STATUS.md` and `EPIC-6-WORKFLOW-GUIDE.md`

---

## 6) References

- `docs/stories/STORY-6.3-CLOSEOUT-REPORT.md`
- `docs/stories/STORY-6.3.1-CLOSEOUT-REPORT.md`
- `docs/stories/STORY-6.3.1-GATE-EVIDENCE.md`
- `docs/stories/STORY-6.3.1-UAT-TEST-GUIDE.md`
- `docs/stories/STORY-6.3.1-UAT-RESULTS.md`
- `docs/stories/story-6.3.md`
- `docs/COMPONENT-FRAMEWORK-REFERENCE.md`
- `docs/AGENT-LOGGING-GUIDE.md`
- `docs/FORM-AI-POST-PROCESSING-GUIDE.md`
- `backend/modules/form_ai/service.py`
- `backend/modules/form_ai/compiler.py`
- `backend/modules/form_ai/semantic_validator.py`
- `frontend/src/features/builder/components/ai/AIAgentPanel.tsx`

---

## 7) Dev Agent Record

**Agent:** `@bmad-agent-bmm-dev` (Amelia)
**Sessions:** Single multi-day session, UAT rounds 1–11.
**Start:** 2026-04-15 (worktree + Draft PR #64 created by SM)
**Closeout:** 2026-04-15

### What was implemented

1. **Semantic plan + deterministic compiler split**
   - `backend/modules/form_ai/semantic_validator.py` — coordinate-free `FormSemanticPlan` schema and validation.
   - `backend/modules/form_ai/compiler.py` — deterministic Python compiler that converts semantic plans into pixel-perfect single-page `DefinitionJSON`.
   - `backend/modules/form_ai/service.py` — orchestrator updated to call validator → compiler → light post-processing (header filter + tab order); legacy guardrails (`_guardrail_submit_button_placement`, `_enforce_column_flow_and_canvas_fit`, `ENABLE_POST_PROCESSING`) removed.
   - `backend/modules/form_ai/router.py` + `schemas.py` — exposed `/generate`, `/remeasure`; trace surfaces `compileSummary` (layoutMode, heightsSource, governanceVersions).

2. **Render-then-measure round-trip (UAT round 5)**
   - Frontend measures rendered component heights and posts them back to `/api/form-ai/remeasure`.
   - Compiler re-runs with measured heights and the frontend swaps the refined definition; failures fall back to first pass without blanking the canvas.

3. **Governance + persistence**
   - New tables: `ComponentCapabilitySnapshot`, `CapabilityPolicyVersion`, `WidthClassPolicyVersion`, `ComponentValidationContract`, `PromptTemplate(+Version)`, `PromptAssemblyProfile`, `GenerationRun`, `GenerationArtifact`.
   - Migrations 053 → 057 (Anthony ran each per workspace rule):
     - 053 governance tables
     - 054 seed `FORM_AI_CAPABILITY_POLICY:v1` + `FORM_AI_WIDTH_POLICY:v1`
     - 055 capability snapshot extension (`rating`, `file-upload`, `address`, `url`)
     - 056 capability snapshot extension (`first-name`, `last-name`)
     - 057 drop `last-name` until frontend `ComponentRegistry` ships matching renderer

4. **Layout-mode selection (UAT round 6)**
   - `frontend/src/features/builder/utils/layoutMode.ts` and `resolveLayoutModeForRequest.ts` — 600 px threshold; horizontal-stacked nudge gated by canvas width.

5. **Validator parity (UAT round 11)**
   - `backend/modules/form_ai/service.py` — `MIN_PLAUSIBLE_RENDER_HEIGHT_PX = 32.0` lets `_collision_component_width_height` and `_flatten_boundary_visual_components` trust compiler-stamped heights, eliminating phantom desktop/tablet collisions.

6. **Test rebuild**
   - 7 new Story 6.3.1 test files (semantic validator, compiler, layout solver, content widths, failure-mode separation, governance persistence, governance API).
   - 6 legacy Story 6.2 / 6.3 test files rewritten to assert against the new contract (no coordinate guessing in fixtures, no obsolete guardrails).
   - Total backend suite: **705 passed, 26 skipped** (was 515 pass at end of 6.2.1).
   - Frontend `layoutMode.test.ts` added; suite now **272 passed**.

7. **Tooling + docs**
   - `backend/scripts/story_631_replay.py` — reproduces compiled definitions for any `GenerationRun` across desktop / tablet / mobile.
   - `backend/scripts/story_631_uat_spotcheck.py` — one-off compiler probe.
   - `docs/analysis/eventlead_form_ai_workflow.md` and `docs/FORM-AI-POST-PROCESSING-GUIDE.md` updated to describe the new pipeline.
   - `STORY-6.3.1-UAT-TEST-GUIDE.md` extended with §10–§15 covering locale, layout-mode, validator parity, framework parity, canvas growth, edit-after-AI parity.

### Decisions / deviations

- **Submit-button validation parity** (`g-frontend-submit-parity`) carried forward to Story 6.4 backlog rather than expanded scope here. It does not block Definition of Done because both surfaces still surface validation errors — the gap is purely visual parity.
- **Last-name component** intentionally removed from the active capability snapshot (migration 057) until the frontend `ComponentRegistry` renderer ships. First-name remains active.
- **Geometry rebalancing** (`_sync_style_dimensions_into_props`, `_rebalance_single_column_vertical_spacing`) is now owned by the compiler at generation time; runtime re-layout is no longer attempted on legacy definitions.

### File List

**Backend — added**
- `backend/migrations/versions/053_story_631_form_ai_governance_tables.py`
- `backend/migrations/versions/054_story_631_seed_governance_baseline.py`
- `backend/migrations/versions/055_story_631_form_ai_capability_rating_fileupload.py`
- `backend/migrations/versions/056_story_631_form_ai_capability_first_last_name.py`
- `backend/migrations/versions/057_story_631_form_ai_capability_drop_last_name.py`
- `backend/models/config/capability_policy_version.py`
- `backend/models/config/component_capability_snapshot.py`
- `backend/models/config/component_validation_contract.py`
- `backend/models/config/prompt_assembly_profile.py`
- `backend/models/config/prompt_template.py`
- `backend/models/config/prompt_template_version.py`
- `backend/models/config/width_class_policy_version.py`
- `backend/models/generation_artifact.py`
- `backend/models/generation_run.py`
- `backend/modules/form_ai/compiler.py`
- `backend/modules/form_ai/semantic_validator.py`
- `backend/scripts/story_631_replay.py`
- `backend/scripts/story_631_uat_spotcheck.py`
- `backend/tests/test_story_631_content_widths.py`
- `backend/tests/test_story_631_deterministic_compiler.py`
- `backend/tests/test_story_631_failure_mode_separation.py`
- `backend/tests/test_story_631_form_ai_governance_api.py`
- `backend/tests/test_story_631_governance_persistence.py`
- `backend/tests/test_story_631_layout_solver.py`
- `backend/tests/test_story_631_semantic_validator.py`

**Backend — modified**
- `backend/models/__init__.py`
- `backend/models/config/__init__.py`
- `backend/models/log/__init__.py`
- `backend/modules/form_ai/router.py`
- `backend/modules/form_ai/schemas.py`
- `backend/modules/form_ai/service.py`
- `backend/modules/form_validate/service.py`
- `backend/tests/test_form_ai_first_shot.py`
- `backend/tests/test_form_ai_prompt_capabilities.py`
- `backend/tests/test_story_63_benchmark_harness.py`
- `backend/tests/test_story_63_context_pack_path.py`
- `backend/tests/test_story_63_event_context_post_process.py`
- `backend/tests/test_story_6_2_ai_generation_loop.py`

**Frontend — added**
- `frontend/src/features/builder/components/ai/resolveLayoutModeForRequest.ts`
- `frontend/src/features/builder/utils/layoutMode.ts`
- `frontend/src/features/builder/utils/__tests__/layoutMode.test.ts`

**Frontend — modified**
- `frontend/src/features/builder/api/aiFormGenerationApi.ts`
- `frontend/src/features/builder/components/FormBuilderCanvas.tsx`
- `frontend/src/features/builder/components/SortableComponent.tsx`
- `frontend/src/features/builder/components/UniversalFieldShell.tsx`
- `frontend/src/features/builder/components/ai/AIAgentPanel.tsx`
- `frontend/src/features/builder/components/ai/sectionedPromptArchitecture.ts`
- `frontend/src/features/builder/components/properties/GlobalStylesPanel.tsx`
- `frontend/src/features/builder/pages/BuilderPage.tsx`
- `frontend/src/features/builder/stores/useBuilderStore.ts`
- `frontend/src/features/builder/types/builder.types.ts`
- `frontend/src/features/builder/utils/objectRenderers.tsx`

**Docs — added / modified**
- `docs/stories/STORY-6.3.1-PREFLIGHT.md` (added)
- `docs/stories/STORY-6.3.1-GATE-EVIDENCE.md` (added)
- `docs/stories/STORY-6.3.1-UAT-RESULTS.md` (added)
- `docs/stories/STORY-6.3.1-CLOSEOUT-REPORT.md` (added)
- `docs/stories/STORY-6.3.1-UAT-TEST-GUIDE.md` (modified — §10–§15 added)
- `docs/FORM-AI-POST-PROCESSING-GUIDE.md` (modified)
- `docs/analysis/eventlead_form_ai_workflow.md` (modified)
- `docs/stories/EPIC-6-STATUS.md` (modified — 6.3.1 marked complete, 6.4 next)
- `docs/stories/EPIC-6-WORKFLOW-GUIDE.md` (modified — Current Focus → 6.4)
- `docs/stories/story-6.3.1.md` (modified — Status → Complete + this Dev Agent Record)
