# Story 6.3 — UAT Test Guide

**Story:** 6.3 — AI Context Uplift & Benchmark Baseline  
**Owner:** Anthony (Human UAT)  
**Prep:** Dev provides `STORY-6.3-GATE-EVIDENCE.md` + merged PR link  

---

## Environment

- Branch: story branch containing 6.3 (or `master` post-merge for confirmation pass).  
- Backend: usual local API + DB.  
- **LLM:** Optional for UAT §2; core ACs are mock-driven in CI.

---

## §1 — Automated gates (witness)

| Step | Command | Expected |
|------|---------|----------|
| 1.1 | From `backend/`: `python -m pytest tests/test_story_6_2_ai_generation_loop.py tests/test_story_63_benchmark_harness.py --tb=short` | All pass |
| 1.2 | From `backend/`: `python -m pytest --tb=short` | All pass (or document skips) |
| 1.3 | From `frontend/`: `npm run lint` | Pass |
| 1.4 | From `frontend/`: `npm run test:unit -- --watch=false` | Pass |

**Record:** paste summary lines into UAT results / gate evidence.

---

## §2 — Context Pack sanity (spot check)

| Step | Action | Expected |
|------|--------|----------|
| 2.1 | Open `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md` | Version **2.0**, “Changes from v1.1” present |
| 2.2 | Skim component catalog | Includes **file-upload**, **url**, **rating**, **paragraph**, and other registered types used in benchmarks |
| 2.3 | If `FORM_AI_CONTEXT_PACK_PATH` (or final env name) exists: set to a temp copy, restart API, trigger one generation | Uses override file; restore default or unset after test |
| 2.4 | Open **Context Pack v2** § default canvas footprints + trigger **Generate** on a **new empty form**; capture request payload or backend log redaction of `runtimeContext.componentFootprints` | Widths/heights are **canvas-scale** (e.g. inputs ~hundreds of px wide on 1920 canvas), not tiny toolbox-thumb pixels only |

---

## §3 — Benchmark baseline document

| Step | Action | Expected |
|------|--------|----------|
| 3.1 | Open `docs/stories/STORY-6.3-BENCHMARK-BASELINE.md` | All **10** benchmarks listed with **PASS** (mocked CI) or noted partial with explanation |
| 3.2 | Confirm commit SHA / date recorded | Matches release under test |

---

## §4 — Optional live model smoke (non-blocking)

**Requires:** valid `OPENAI_API_KEY` (or project standard) in dev environment only.

| Step | Action | Expected |
|------|--------|----------|
| 4.1 | From Builder, run AI generate using **Benchmark 1** prompt (RSVP) | Completes or fails gracefully with visible error (no 500 without message) |
| 4.2 | Load result on canvas | Single page; no obvious overlap; validator path usable |

If not run, note **“Skipped — mock CI only”** in UAT results.

---

## §5 — Builder canvas visibility (**mandatory** — Story 6.3 AC-9)

**Goal:** Confirm that improvements from 6.3 are visible **in the Form Builder** (not only via API/pytest). The normal path is: **Builder** → open a form → **Global Properties / AI** entry point → **Generate** → definition **replaces** the canvas via `applyValidatedDefinition`.

| Step | Action | Expected |
|------|--------|----------|
| 5.1 | Open an existing draft form (or create new) in **Form Builder** | Canvas and AI panel load |
| 5.2 | Paste **Benchmark 1** prompt from `STORY-6.2-BENCHMARK-FORMS.md` → **Generate** | Status succeeds (or clear user-facing error if model/config missing) |
| 5.3 | **Without** leaving the builder, inspect **canvas** | **All** generated field types from the benchmark appear as components (RSVP: name, phone, email, radio, number, submit) — selectable, not empty canvas |
| 5.4 | Repeat **5.2–5.3** for **at least one** other benchmark (e.g. **2** or **3**) | Same: visible layout on canvas after success |
| 5.5 | Optional: click a component → **Properties** updates | Confirms store/canvas binding still works |

If §5 cannot run (no API key), record **FAIL for AC-9** and raise a follow-up task — **do not** mark Story 6.3 Complete on Human sign-off without Anthony seeing canvas output or an agreed exception.

---

## §6 — UAT Result

| Section | Pass / Fail / Skipped | Notes |
|---------|----------------------|-------|
| §1 Gates | | |
| §2 Context pack + runtime footprints (incl. 2.4) | | |
| §3 Baseline doc | | |
| §4 Live smoke | | |
| §5 Builder canvas (AC-9) | | |

**Sign-off:** _Name / date_
