# Story 6.3 — AI Context Uplift & Benchmark Baseline

**Epic:** 6 — AI Generation & Monetization Engine  
**Story ID:** 6.3  
**Title:** AI Context Uplift & Benchmark Baseline  
**Status:** 📋 **Prepared** — awaiting `./scripts/git/new-story.ps1` + Draft PR + Dev implementation  
**Branch:** `story/epic6-6.3-ai-context-benchmark-baseline` (expected; confirm in worktree)  
**PR:** _TBD_  
**Depends On:** Story 6.2.2 (✅ Complete, PR #55)  
**Blocks:** Story 6.4 (AI Iteration on Existing Designs)  
**Created:** 2026-03-31  
**Sources:** `EPIC-6-STATUS.md`, `STORY-6.2-CLOSEOUT-REPORT.md` §2, `STORY-6.2-BENCHMARK-FORMS.md`, `STORY-6.2-AI-CONTEXT-PACK.md`, `backend/modules/form_ai/service.py`

---

## 1) Goal

Raise **AI form-generation quality** and **operational reliability** by:

1. Shipping **AI Context Pack v2** (richer, benchmark-informed instructions aligned with post-6.2.1/6.2.2 component reality).  
2. **Hardening** the generation pipeline (errors, configurability, testability) without changing product UX flows.  
3. Implementing a **repeatable automated harness** over the **10 benchmarks** in `STORY-6.2-BENCHMARK-FORMS.md`.  
4. Establishing a **documented quality baseline** (pass/fail + rubric dimensions) so Story **6.4** and future tuning can compare against a fixed reference.

---

## 2) In Scope

### 2.1 AI Context Pack v2

| Area | Requirement |
|------|-------------|
| **Primary artifact** | Evolve `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md` to **Context Pack v2.0** (update title block version + **Last Updated**). Add a short **“Changes from v1.1”** section so reviewers see deltas. |
| **Content** | Incorporate lessons from 6.2.1/6.2.2: full **MVP component catalog** parity with registry; **`first-name`** and other supported types as needed; **`file-upload`** rules (attachment IDs, `allowMultiple` / `maxFiles`, no paths); **`terms`**, **`date`** modes, **`dropdown`/`radio`/`checkbox`** option shapes; pointer to **`docs/COMPONENT-FRAMEWORK-GUIDE.md`** / **REFERENCE** for authoritative prop names. |
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

---

## 5) Definition of Done

- [ ] All AC satisfied; gate evidence in `STORY-6.3-GATE-EVIDENCE.md`  
- [ ] `npm run lint` + `npm run test:unit -- --watch=false` green  
- [ ] `python -m pytest --tb=short` green  
- [ ] Human UAT per `STORY-6.3-UAT-TEST-GUIDE.md`  
- [ ] Story PR merged via GitHub; closeout checklist in workflow guide applied  

---

## 6) References

- `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md`  
- `docs/stories/STORY-6.2-BENCHMARK-FORMS.md`  
- `docs/stories/STORY-6.2-CLOSEOUT-REPORT.md`  
- `backend/modules/form_ai/service.py` (`CONTEXT_PACK_PATH`, `generate_form_definition`)  
- `backend/tests/test_story_6_2_ai_generation_loop.py`  
- `docs/COMPONENT-FRAMEWORK-GUIDE.md`  

---

## 7) Dev Agent Record

### Agent Model Used

_TBD_

### Completion Notes List

_TBD_

### File List

_TBD_
