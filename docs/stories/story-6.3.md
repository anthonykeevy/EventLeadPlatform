# Story 6.3 — AI Context Uplift & Benchmark Baseline

**Epic:** 6 — AI Generation & Monetization Engine  
**Story ID:** 6.3  
**Title:** AI Context Uplift & Benchmark Baseline  
**Status:** 🟨 **Closed (learning capture)** — UAT not satisfactory; redesign required before release  
**Branch:** `story/epic6-6.3-ai-context-benchmark-baseline` (expected; confirm in worktree)  
**PR:** _TBD_  
**Depends On:** Story 6.2.2 (✅ Complete, PR #55)  
**Blocks:** Story 6.4 (AI Iteration on Existing Designs)  
**Created:** 2026-03-31  
**Closed:** 2026-04-02  
**Sources:** `EPIC-6-STATUS.md`, `STORY-6.2-CLOSEOUT-REPORT.md` §2, `STORY-6.2-BENCHMARK-FORMS.md`, `STORY-6.2-AI-CONTEXT-PACK.md`, `backend/modules/form_ai/service.py`

---

## 1) Goal

Raise **AI form-generation quality** and **operational reliability** by:

1. Shipping **AI Context Pack v2** (richer, benchmark-informed instructions aligned with post-6.2.1/6.2.2 component reality), including **canvas-scale default width/height guidance per component type** so the model can place `position` + `style` without guessing.  
2. Aligning **`runtimeContext.componentFootprints`** with **builder truth**: toolbox tiles are visually compact (~order-of-magnitude smaller than canvas); footprints sent to `/api/form-ai/generate` must reflect **100% canvas** sizing/heuristics (same policy the builder uses for new drops), not raw toolbox `getBoundingClientRect` alone on an empty form.  
3. **Hardening** the generation pipeline (errors, configurability, testability) without changing product UX flows.  
4. Implementing a **repeatable automated harness** over the **10 benchmarks** in `STORY-6.2-BENCHMARK-FORMS.md`.  
5. Establishing a **documented quality baseline** (pass/fail + rubric dimensions) so Story **6.4** and future tuning can compare against a fixed reference.

---

## 2) In Scope

### 2.1 AI Context Pack v2

| Area | Requirement |
|------|-------------|
| **Primary artifact** | Evolve `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md` to **Context Pack v2.0** (update title block version + **Last Updated**). Add a short **“Changes from v1.1”** section so reviewers see deltas. |
| **Content** | Incorporate lessons from 6.2.1/6.2.2: full **MVP component catalog** parity with registry; **`first-name`** and other supported types as needed; **`file-upload`** rules (attachment IDs, `allowMultiple` / `maxFiles`, no paths); **`terms`**, **`date`** modes, **`dropdown`/`radio`/`checkbox`** option shapes; pointer to **`docs/COMPONENT-FRAMEWORK-GUIDE.md`** / **REFERENCE** for authoritative prop names. |
| **Component dimensions** | Add a **“Default canvas footprints”** section: for each generation-safe component type, document **recommended default `style.width` / `style.height` (px)** (and notes: options-count height growth, `rating` / `url` / `paragraph` / `file-upload`, submit-button vs inputs). Numbers must **match** the chosen single source of truth in code (see §2.5) — no orphan magic numbers that drift from the builder. Explicitly state that **toolbox thumbnails are not 1:1 canvas size**; the model must use this table (and/or `componentFootprints` in runtime JSON) for layout math. |
| **Contract** | Preserve strict JSON-only output rules, validator feedback mapping, single-page constraint, and disclaimer for disallowed features (payments, multi-page). |
| **Loader** | `backend/modules/form_ai/service.py` continues to load this path unless Dev introduces an env override (optional AC below). |

### 2.2 Pipeline hardening

| Area | Requirement |
|------|-------------|
| **Context pack load** | If file missing or unreadable: structured error (`RuntimeError` today) remains; ensure API/response surfaces a **clear client-facing message** (no stack traces to end users). |
| **Config (optional but recommended)** | Support **`FORM_AI_CONTEXT_PACK_PATH`** (or agreed name) env var: when set, load that file instead of the default path; enables future split packs without code churn. Default remains repo-relative `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md`. |
| **Tests** | Add/extend tests so harness + unit tests can point at a **temporary context file** or fixture path where env is set (avoid coupling all tests to the full v2 doc length if needed). |
| **Observability** | Preserve existing outbound HTTP timing logs; document in gate evidence any **new** log fields or trace fields added for benchmark runs. |
| **No scope creep** | Do not add Story **6.4** conversational edit loop; do not add new LLM providers unless required to fix a hardening bug (default: stay on current integration). |

### 2.3 Ten-benchmark automated harness

| Area | Requirement |
|------|-------------|
| **Source of truth** | `docs/stories/STORY-6.2-BENCHMARK-FORMS.md` — all **10** benchmarks. |
| **Implementation** | New test module (e.g. `backend/tests/test_story_63_benchmark_harness.py`) that exercises **`generate_form_definition`** (and/or validation path) per benchmark. |
| **Mocking** | **Default CI path:** mock `_request_chatgpt_completion` (or the single outbound call boundary) so tests do not require API keys. Use **curated JSON fixtures** per benchmark that represent “ideal” or “runner-smoothed” model output where needed. |
| **Assertions** | Minimum per benchmark: **schema validity** via existing validator; **expected component types** or **field count** checks derived from the benchmark table; **single-page** guard. Optional: collision/boundary counts where the benchmark implies layout constraints. |
| **Parametrization** | Prefer `@pytest.mark.parametrize` over copy-paste. |
| **Docs** | Short header in test file pointing to `STORY-6.2-BENCHMARK-FORMS.md` and this story. |

### 2.4 Quality baseline document

| Area | Requirement |
|------|-------------|
| **New file** | `docs/stories/STORY-6.3-BENCHMARK-BASELINE.md` |
| **Content** | Table: Benchmark #, Title, **pass/fail** (or score if rubric automated), notes (e.g. which AC failed). Record **commit SHA**, **date**, and **model** (or `mocked-ci` if only fixture path). |
| **Rubric** | Reuse the five dimensions from **STORY-6.2-BENCHMARK-FORMS.md** where human scoring is still manual; automation focuses on **schema + structural** checks first. |

### 2.5 Canvas-faithful `componentFootprints` (builder integration)

| Area | Requirement |
|------|-------------|
| **Problem** | `frontend/.../ai/AIAgentPanel.tsx` `buildRuntimeContext` currently seeds `componentFootprints` from **`[data-toolbox-component-type]`** DOM bounds. Toolbox previews use **compact** rendering (`surface="toolbox"` — see `componentSurfaceCapabilities.ts`); those pixel sizes are **not** the same as **canvas** placement sizes. On a **new empty form**, only these small measurements may be sent, while `backend/modules/form_ai/service.py` treats footprints as **minimum render width/height** — causing weak or wrong collision/boundary heuristics. |
| **Direction** | Prefer **one policy** shared with “user dropped a new component from toolbox” sizing: e.g. synthetic **`FormComponent` per registry type** with the same default props/structure the builder uses for a new drop, then **`getComponentDimensions(component, null, 100)`** and/or reuse **`estimateConfiguredFootprint`** (extract to a shared module if needed so frontend does not duplicate). Cover **all** toolbox-eligible AI types. |
| **Fallback order** | (1) Measured canvas DOM for types already on the form (if reliable); (2) synthetic defaults for missing types; (3) do **not** rely on toolbox thumbnail pixels as sole source for min width/height. |
| **Tests** | Frontend unit test(s): for an empty definition, runtime context footprints for `text` (and 1–2 other types) match expected **canvas-scale** ranges, not sub-50px thumbnail sizes. |
| **Docs** | Short comment in `AIAgentPanel.tsx` at `buildRuntimeContext` explaining why toolbox bounds are insufficient. |

### 2.6 Builder-visible delivery (Anthony must see results on canvas)

| Area | Requirement |
|------|-------------|
| **Product path** | Story 6.3 changes must **not** break the existing flow: user opens **Form Builder** on a form → **AI** panel (Global Properties workflow) → enters prompt → **Generate** → on success the app calls **`applyValidatedDefinition`** so the draft loads onto the **canvas** (components selectable, editable, same as a manual build). |
| **Regression guard** | If implementation touches `AIAgentPanel.tsx` / `applyValidatedDefinition` / generation API wiring, Dev verifies in browser (or documents agent-browser evidence) that **at least one** benchmark-style prompt produces a **visible** multi-field layout on canvas after generate — not only a 200 JSON response or passing pytest. |
| **Scope note** | Automated pytest does **not** replace this; it validates contracts. **Human UAT §5** in `STORY-6.3-UAT-TEST-GUIDE.md` is **mandatory** for sign-off so Anthony can judge layout quality for 6.3 vs future work. |

---

## 3) Out of Scope

| Item | Reason |
|------|--------|
| Story **6.4** “edit existing form with AI” | Separate story |
| Full visual/UI screenshot regression | Too heavy for 6.3 |
| Live multi-model leaderboard in product | `STORY-6.2-MODEL-COMPARISON.md` is reference only unless PM expands |
| Changing Epic 5/7 publish or billing | Epic boundary |

---

## 4) Acceptance Criteria

1. **AC-1 (Context Pack v2):** `STORY-6.2-AI-CONTEXT-PACK.md` reads as **v2.0** with changelog from v1.1; content covers all **builder-registered** generation-safe component types relevant to benchmarks (including **`file-upload`**, **`url`**, **`rating`**, **`paragraph`**, **`first-name`** as applicable).  
2. **AC-2 (Loader / env):** Optional env var documented in `backend` README or `env.example` (one line OK) — if implemented, tests prove both default path and override path behavior.  
3. **AC-3 (Harness):** Automated tests cover **all 10** benchmarks with **deterministic** mocks; `python -m pytest` passes in CI without secrets.  
4. **AC-4 (Baseline):** `STORY-6.3-BENCHMARK-BASELINE.md` exists and is filled for the **mocked** CI run at merge time (and leaves room for a future “live model” row).  
5. **AC-5 (Regressions):** Existing Story 6.2 tests (`test_story_6_2_ai_generation_loop.py`) still pass unless story explicitly updates behavior with documented rationale.  
6. **AC-6 (Docs):** `EPIC-6-WORKFLOW-GUIDE.md` **Current Focus** / 6.3 status updated at story closeout per checklist; `EPIC-6-STATUS.md` row for 6.3 gets PR # and Complete when merged.  
7. **AC-7 (Dimensions in Context Pack v2):** `STORY-6.2-AI-CONTEXT-PACK.md` includes a **default canvas footprint** subsection per §2.1; values stay in sync with §2.5 implementation (same numbers or generated from one exported JSON — document which).  
8. **AC-8 (Runtime footprints):** `buildRuntimeContext` (or successor) supplies **canvas-scale** `componentFootprints` for AI generation on **new** and **existing** forms per §2.5; frontend test proves thumbnails are not the only source for empty forms.  
9. **AC-9 (Builder canvas):** Successful **Generate** from the in-app AI panel **applies** the definition to the **builder canvas** per §2.6; components are visible and interactable. **No** closeout if the only proof is backend tests — **§5** of the UAT guide must be **PASS** (or documented blocker with follow-up task).

---

## 5) Definition of Done

- [ ] All AC satisfied; gate evidence in `STORY-6.3-GATE-EVIDENCE.md`  
- [ ] `npm run lint` + `npm run test:unit -- --watch=false` green  
- [ ] `python -m pytest --tb=short` green  
- [ ] Human UAT per `STORY-6.3-UAT-TEST-GUIDE.md` (includes **§5** builder canvas visibility)  
- [ ] Story PR merged via GitHub; closeout checklist in workflow guide applied  

**Closeout note:** This story was intentionally closed for learning capture and redesign planning. Human UAT did not reach satisfactory quality; see `STORY-6.3-CLOSEOUT-REPORT.md`.

---

## 6) References

- `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md`  
- `docs/stories/STORY-6.2-BENCHMARK-FORMS.md`  
- `docs/stories/STORY-6.2-CLOSEOUT-REPORT.md`  
- `docs/stories/STORY-6.3-CLOSEOUT-REPORT.md`
- `docs/FORM-AI-POST-PROCESSING-GUIDE.md`
- `backend/modules/form_ai/service.py` (`CONTEXT_PACK_PATH`, `generate_form_definition`)  
- `backend/tests/test_story_6_2_ai_generation_loop.py`  
- `docs/COMPONENT-FRAMEWORK-GUIDE.md`  
- `frontend/src/features/builder/components/ai/AIAgentPanel.tsx` — `buildRuntimeContext`, `estimateConfiguredFootprint`  
- `frontend/src/features/builder/utils/collisionDetection.ts` — `getComponentDimensions`  
- `frontend/src/features/builder/utils/componentSurfaceCapabilities.ts` — toolbox vs canvas surface behavior  
- `frontend/src/features/builder/registry/ComponentRegistry.tsx` — default props / structure for synthetic components  

---

## 7) Dev Agent Record

### Agent Model Used

Cursor agent (Amelia dev prompt / single-session Story 6.3 instructions).

### Completion Notes List

- Context Pack v2.0 in `STORY-6.2-AI-CONTEXT-PACK.md` with changelog + default canvas footprints (aligned with `buildAiRuntimeFootprints.ts`).
- `FORM_AI_CONTEXT_PACK_PATH` + `get_context_pack_path()` in `backend/modules/form_ai/service.py`; tests in `test_story_63_context_pack_path.py`.
- Canvas-faithful `componentFootprints` via `buildAiRuntimeFootprints.ts` + `AIAgentPanel` (`initComponents` filter parity with sidebar).
- Benchmark harness `test_story_63_benchmark_harness.py` (10 parametrized cases, mocked `_request_chatgpt_completion`).
- Baseline `STORY-6.3-BENCHMARK-BASELINE.md`; gate log `STORY-6.3-GATE-EVIDENCE.md`.
- AC-9: `applyValidatedDefinition` on completed generate unchanged; browser UAT still required.
- UAT feedback ledger: `STORY-6.3-BENCHMARK-UAT-FEEDBACK-LOG.md` (BM01: vertical margin fix, context-only width/label guidance; benchmark prompts unchanged for baseline).
- Story closeout decision recorded in `STORY-6.3-CLOSEOUT-REPORT.md` (learning captured, redesign required; no release-ready claim).
- Post-processing usage guidance documented in `docs/FORM-AI-POST-PROCESSING-GUIDE.md`.

### File List

- `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md`
- `docs/stories/STORY-6.3-BENCHMARK-BASELINE.md`
- `docs/stories/STORY-6.3-BENCHMARK-UAT-FEEDBACK-LOG.md`
- `docs/stories/STORY-6.3-GATE-EVIDENCE.md`
- `docs/stories/story-6.3.md`
- `.env.example`
- `backend/modules/form_ai/service.py`
- `backend/tests/test_story_63_benchmark_harness.py`
- `backend/tests/test_story_63_context_pack_path.py`
- `frontend/src/features/builder/components/ai/buildAiRuntimeFootprints.ts`
- `frontend/src/features/builder/components/ai/AIAgentPanel.tsx`
- `frontend/src/features/builder/components/ai/__tests__/buildAiRuntimeFootprints.test.ts`
- `docs/stories/STORY-6.3-BENCHMARK-PROMPTS-AND-OUTCOMES.md`
- `docs/stories/STORY-6.3-CLOSEOUT-REPORT.md`
- `docs/stories/STORY-6.2-BENCHMARK-FORMS.md` (baseline prompts frozen)
- `backend/tests/test_story_6_2_ai_generation_loop.py` (rebalance expected `y` after float gap)
- `docs/FORM-AI-POST-PROCESSING-GUIDE.md`
