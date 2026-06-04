# Story 6.5e-vision — Component Platform Hardening + Image-to-Form Vision Path

**Epic:** 6 — AI Generation & Monetization Engine  
**Story ID:** 6.5e-vision *(was 6.5b-vision — renamed 2026-05-20)*  
**Title:** Track 0 — component platform hardening (6.5d follow-through) + Track 1 — screenshot/photo → `FormSemanticPlan`  
**Status:** ⏸️ **Deferred** (worktree not opened)  
**Branch:** `story/epic6-6.5e-vision-image-to-form` *(planned)*  
**PR:** TBD — Draft → `develop`  
**Created:** 2026-05-28  
**Size:** L (Track 0: S · Track 1: M per ideation brief)

**Pause note (2026-06-03):** Deferred while customer discovery is active. The next Epic 6 story is `story-6.5e-landing-page.md`, which supports customer discovery and beta account creation before more Form Builder / image-to-form investment.

**Depends On:**
- Story 6.5d ✅ — catalog alignment, EDF reference pair, clarification plane, `ADD-COMPONENT-TO-PLATFORM-CHECKLIST.md`
- Story 6.5b ✅ — Prompt Assembly Registry
- Story 6.5c ✅ — `resolve_allowed_components` cutover
- Architecture: `docs/architecture/prompt-assembly-registry-architecture.md`
- Planning: `_bmad-output/planning-artifacts/EPIC-6-PROMPT-ENGINEERING-IDEATION-BRIEF.md` (6.5b-vision scope)

**Unblocks:** 6.5f-style (style intent rides on vision path per ideation brief); cleaner component additions after 6.5d lessons.

---

## 1) Goal

Deliver **two tracks** in one story (Tony-approved pattern from 6.5d):

### Track 0 — Component platform hardening *(6.5d SM closeout — do first)*

Close the process gaps exposed when EDF components shipped with catalog/registry parity but incomplete runtime UAT surfaces.

| # | Deliverable | Source |
|---|-------------|--------|
| T0-1 | **Checklist v1.3** — ship §0c (global-component submit smoke + per-component AC-4 matrix); bump doc version | `g-65e-checklist-v13` |
| T0-2 | **`verify_edf_props_wired.py`** — fail if `PropertiesSchemaJSON` key not read in runtime for EDF codes | `g-65e-props-wiring-script`, friction log #3 |
| T0-3 | **Closeout template** — `STORY-6.x-COMPONENT-CHECKLIST-AUDIT.md` or table in closeout report (one row per `ComponentCode` × §1–7) | AC-4 gap from 6.5d |
| T0-4 | **CI / gate hook** — document or wire `verify_component_catalog_alignment.py` after migration apply on Test | friction log #13 |
| T0-5 *(stretch P3)* | Address manual-entry UI for `address-lookup-au` (company pattern) | `g-65d-address-manual-fallback` |
| T0-6 *(stretch P3)* | `editableLegalNameAfterResolve` on `company-lookup-abr` | `g-65d-editable-legal-name` |
| T0-7 *(stretch P2)* | AI panel hint/chip for AU EDF types in generate prompt | `g-65e-ai-edf-prompt-ux` |

**Exit gate for Track 0:** Checklist v1.3 published; props-wiring script runs green on `address-lookup-au` + `company-lookup-abr`; SM tools registry updated.

### Track 1 — Image-to-Form Vision Path *(product differentiator)*

Per ideation brief: screenshot/photo input → vision model → `FormSemanticPlan` → existing deterministic compiler.

| Area | Scope (preview — refine in SM pack) |
|------|-------------------------------------|
| Backend | Vision call path; Tier Map prompt section; low-confidence → clarification recovery (uses 6.5d Block E) |
| Frontend | Image upload UX in AI Agent panel; preserve canvas contract |
| Prompt | Registry-backed vision block (not hardcoded constants) |
| Tests | `test_image_to_form.py` (per ideation brief) |
| Docs | Start/extend `STORY-6.5b-CANVAS-PRESERVATION-CONTRACT.md` |

**Out of scope Track 1:** Style Intent resolver (6.5f-style); PII layers (6.5g-PII); Google Fonts (6.5h-fonts).

---

## 2) Acceptance criteria

### Track 0 — Platform hardening

| ID | Criterion |
|----|-----------|
| AC-T0-1 | `ADD-COMPONENT-TO-PLATFORM-CHECKLIST.md` at **v1.3** with §0c; Epic 6 workflow references v1.3. |
| AC-T0-2 | `backend/scripts/verify_edf_props_wired.py` exits non-zero on unwired property; registered in `EPIC-6-SM-TOOLS-REGISTRY.md`. |
| AC-T0-3 | Story closeout template requires per-component §1–7 matrix when any `FormBuilderComponent` changes. |
| AC-T0-4 | Focused tests for new script green; existing `verify_component_catalog_alignment.py` still passes (21 codes AU fixture). |

### Track 1 — Vision path

| ID | Criterion |
|----|-----------|
| AC-V1 | User can attach screenshot/photo in AI Agent panel and trigger generate. |
| AC-V2 | Backend produces valid `FormSemanticPlan` from vision output; semantic validator accepts plan. |
| AC-V3 | Compiled form renders in builder without `unknown-component-type`; uses catalog-resident types only. |
| AC-V4 | Low-confidence path surfaces clarification dropdowns (6.5d) rather than silent failure. |
| AC-V5 | Canvas preservation contract documented and UAT'd (no destructive overwrite without user consent). |
| AC-V6 | Focused vision tests green; 6.5d regression tests still pass. |

---

## 3) Recommended chat workflow

| Phase | Chat | Actor | Outcome |
|-------|------|-------|---------|
| **A — SM pack** | Main repo / SM | `@bmad-agent-bmm-sm` | `story-context-6.5e-vision.xml`, UAT guide, dev prompt; `new-story.ps1` |
| **B — Track 0** | Worktree | `@bmad-agent-bmm-dev` | Checklist v1.3 + props script + templates *(1–2 days)* |
| **C — Track 1** | Same worktree | `@bmad-agent-bmm-dev` | Vision path per dev prompt *(ideation: 5–6 d)* |

**Order:** Track 0 **before** Track 1 — prevents vision work from adding components without hardened process.

---

## 4) References

- `STORY-6.5d-CLOSEOUT-REPORT.md` §6 — checklist improvements  
- `STORY-6.5d-IMPLEMENTATION-FRICTION-LOG.md` — automation candidates  
- `docs/workflows/ADD-COMPONENT-TO-PLATFORM-CHECKLIST.md`  
- `EPIC-6-CARRY-FORWARD-BACKLOG.md` — `g-65e-*` items  
- `_bmad-output/planning-artifacts/EPIC-6-PROMPT-ENGINEERING-IDEATION-BRIEF.md` — original 6.5b-vision sizing

---

*SM draft — 2026-05-28 — absorbs 6.5d platform follow-through before vision implementation.*
