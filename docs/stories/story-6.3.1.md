# Story 6.3.1 — Simplified AI Output + Deterministic Layout Foundation

**Epic:** 6 — AI Generation & Monetization Engine  
**Story ID:** 6.3.1  
**Title:** Simplified AI Output + Deterministic Layout Foundation  
**Status:** 📋 **Prepared** — required bridge after Story 6.3 learning closeout  
**Branch:** `story/epic6-6.3.1-simplified-ai-deterministic-layout` (expected)  
**PR:** _TBD_  
**Depends On:** Story 6.3 (✅ Closed as learning)  
**Blocks:** Story 6.4 (AI Iteration on Existing Designs)  
**Created:** 2026-04-15

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

- [ ] Story ACs met with evidence in `STORY-6.3.1-GATE-EVIDENCE.md`
- [ ] `python -m pytest --tb=short` green
- [ ] `npm run lint` and `npm run test:unit -- --watch=false` green
- [ ] Human UAT pass recorded using a new `STORY-6.3.1-UAT-TEST-GUIDE.md`
- [ ] Evidence includes one capability snapshot artifact and one trace example showing all version IDs (prompt/capability/validation/width policy)
- [ ] Evidence includes correlated log extraction (`RequestID` + outbound chain) and at least one one-variable-at-a-time tuning sequence
- [ ] SM story pack artifacts exist: `story-context-6.3.1.xml`, `STORY-6.3.1-SINGLE-SESSION-DEV-PROMPT.md`, `STORY-6.3.1-UAT-TEST-GUIDE.md`
- [ ] Story closeout updates in `EPIC-6-STATUS.md` and `EPIC-6-WORKFLOW-GUIDE.md`

---

## 6) References

- `docs/stories/STORY-6.3-CLOSEOUT-REPORT.md`
- `docs/stories/story-6.3.md`
- `docs/COMPONENT-FRAMEWORK-REFERENCE.md`
- `docs/AGENT-LOGGING-GUIDE.md`
- `docs/FORM-AI-POST-PROCESSING-GUIDE.md`
- `backend/modules/form_ai/service.py`
- `frontend/src/features/builder/components/ai/AIAgentPanel.tsx`
