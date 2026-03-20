# Story 6.2: AI Generation Pipeline, Test Harness & Benchmark Baseline

**Epic:** Epic 6 - AI Generation and Monetization Engine  
**Domain:** Builder UX, AI orchestration loop, validator-driven retries, quality measurement  
**Status:** 🔄 In Progress (reshaping from POC → production pipeline + test harness)  
**Priority:** High  
**Created:** 2026-02-27  
**Reshaped:** 2026-03-20  
**Owner:** PM Agent  
**Prerequisite:** Story 6.1 complete and merged (`POST /api/form-validate` available)  
**Context:** `docs/stories/story-context-6.2.xml`  
**UAT Guide:** `docs/stories/STORY-6.2-UAT-TEST-GUIDE.md`  
**AI Context Pack:** `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md`  
**Benchmark Forms:** `docs/stories/STORY-6.2-BENCHMARK-FORMS.md`  
**SM Readiness:** `docs/stories/STORY-6.2-SM-READINESS-SUMMARY.md`  
**PM Decisions:** Single-page locked; retry cap = 3 system attempts; start provider = ChatGPT API; Global Properties menu switcher (`AI Agent`/`Inspector`/`Logic`); 10 real-world benchmark forms for quality measurement

---

## User Story

**As a** Company User building a form,  
**I want** to describe a form in natural language and have AI generate a valid initial form layout,  
**So that** I can start from a useful draft and then refine it manually in the Builder.

**As a** Product/Engineering team,  
**I want** a measurable quality baseline for AI generation using real-world form benchmarks,  
**So that** we can systematically improve AI output quality and detect regressions.

---

## Story Objective

Deliver a production-ready AI generation pipeline with a measurable quality framework:

1. **Harden the POC pipeline** — the chat UI, AI generation endpoint, retry loop, and canvas
   loading built during the POC phase become production-grade with proper tests and error handling.
2. **Build a test harness** — an automated/semi-automated system that runs the 10 benchmark
   prompts through the pipeline, scores the output, and produces a results matrix.
3. **Establish the quality baseline** — run all 10 benchmarks, record scores, and document
   the starting point for future context pack improvements (Story 6.3).

### What already exists (POC)
- Chat UI in Global Properties panel (`AI Agent` / `Inspector` / `Logic` tabs)
- Backend AI generation endpoint (`/api/form-ai/generate`)
- AI retry loop with validator feedback (max 3 retries)
- LLM Context Pack v1 (`STORY-6.2-AI-CONTEXT-PACK.md`)
- Frontend state management for generation lifecycle
- Model comparison evaluation script

### What this story adds
- Production hardening of the above (tests, edge cases, error paths)
- Benchmark forms document with 10 real-world-inspired prompts
- Automated test harness to run benchmarks and score output
- Scoring rubric (5 dimensions × 10 forms = 500 max score)
- Baseline results matrix (first full run)

---

## In Scope

### Phase A: Pipeline Hardening
1. Review and harden existing POC code for the AI generation loop:
   - Backend endpoint, service layer, retry logic, error handling
   - Frontend chat UI, state transitions, canvas loading
   - Ensure proper test coverage for happy path and failure paths
2. Versioned LLM Context Pack (already exists, verify completeness):
   - Product behavior context
   - Component taxonomy + required/optional props
   - Layout and canvas rules (single-page MVP)
   - JSON-only output contract
   - Deterministic correction instructions for retries
   - Examples (good generation + corrected-from-errors flow)
3. Provider configuration:
   - ChatGPT API via `OPENAI_API_KEY` in backend `.env`
   - No secrets in logs, responses, or committed files
4. Retry policy: max **3** automatic correction retries per request
5. Green CI/CD gates pass with all new code

### Phase B: Test Harness & Benchmark Evaluation
6. Create test harness script that:
   - Feeds each of the 10 benchmark prompts through the AI pipeline
   - Captures raw AI output per attempt (including retries)
   - Records validator pass/fail per attempt
   - Calculates scores across 5 dimensions per benchmark
   - Produces a summary results matrix (CSV or markdown)
7. Define scoring rubric (see `STORY-6.2-BENCHMARK-FORMS.md`):
   - **Field Completeness** (0-10): all expected fields present with correct types
   - **Layout Quality** (0-10): logical grouping, no overlaps, readable flow
   - **Schema Validity** (0-10): passes validator on first attempt (10) or after retries (partial)
   - **Prompt Fidelity** (0-10): output matches user intent, no hallucinated extras
   - **Visual Polish** (0-10): reasonable sizing, spacing, alignment
8. Run full benchmark suite and document baseline scores
9. Audit-style trace metadata captured per generation (attempt count, validator results, latency)

### Phase C: Documentation & Closeout
10. Update story artifacts with final results
11. Produce green gate evidence per Epic 6 workflow

---

## Out of Scope

1. Context pack improvements to raise scores (that is Story 6.3).
2. AI iteration on existing designs / user refinement (that is Story 6.4).
3. Payment-related components/flows (Stories 6.5+).
4. Multi-page AI generation orchestration.
5. Advanced semantic refinement or chat memory across sessions.
6. Fine-tuning or model-training work.

---

## Dependencies (Story 6.1 Contract)

Story 6.2 depends on Story 6.1 validator response contract:
- Endpoint: `POST /api/form-validate`
- Response fields used by loop: `valid`, `schemaErrors`, `boundaryViolations`, `collisions`, `summary`

If response shape changes, Story 6.2 loop and prompt-builder logic must be updated in lockstep.

Additional dependency:
- LLM provider credentials configured in local environment (`OPENAI_API_KEY` in `backend/.env`, untracked by git).

---

## Acceptance Criteria / Done Criteria

### Pipeline (carried from POC, verify complete)
- [ ] AC1: AI generation UI available in Builder Global Properties under `AI Agent`, with `Inspector` and `Logic` switchable.
- [ ] AC2: Versioned LLM Context Pack defined and used for every generation attempt.
- [ ] AC3: System calls AI generation backend and receives candidate `DefinitionJSON`.
- [ ] AC4: Each candidate validated via Story 6.1 endpoint before canvas load.
- [ ] AC5: Invalid candidates trigger retry loop with structured validator feedback.
- [ ] AC6: Retry loop honors max attempts (**3**) and exits deterministically.
- [ ] AC7: Successful validated output loads into Builder canvas without crash.
- [ ] AC8: Failure states clearly shown to user with actionable guidance.
- [ ] AC9: Attempt trace metadata captured for debugging.
- [ ] AC10: ChatGPT API key consumed from env config and never emitted in logs/responses.

### Test Harness & Benchmarks (new)
- [ ] AC11: 10 benchmark forms documented with prompts, expected fields, and layout expectations.
- [ ] AC12: Test harness script runs all 10 benchmarks and produces scored results matrix.
- [ ] AC13: Scoring rubric covers 5 dimensions (Field Completeness, Layout Quality, Schema Validity, Prompt Fidelity, Visual Polish).
- [ ] AC14: Baseline results matrix documented with scores and commentary.
- [ ] AC15: Harness is re-runnable — supports before/after comparison for context pack changes.

### Quality Gates
- [ ] AC16: Green CI/CD evidence produced per Epic 6 workflow.
- [ ] AC17: Tool usage feedback captured via workflow tooling log.

---

## Benchmark Forms (Summary)

Full details in `STORY-6.2-BENCHMARK-FORMS.md`. Ten real-world-inspired forms:

| # | Category | Fields | Key challenge |
|---|----------|--------|---------------|
| 1 | Simple Contact | 6 | Two-column name row |
| 2 | Sales Lead Capture | 10 | Dense form, multiple dropdowns |
| 3 | Event Registration | 7 | Checkbox + dropdown mix |
| 4 | Customer Feedback | 6 | Heading + dropdowns + text areas |
| 5 | Booking / Reservation | 8 | Date/time pairing, many dropdowns |
| 6 | Job Application | 9 | Mid-density, qualification dropdowns |
| 7 | Newsletter Signup | 4 | Minimal — should not over-engineer |
| 8 | Multi-Section Registration | 9 | Grouped fields, two-column pairs |
| 9 | Event RSVP | 8 | Multiple related dropdowns |
| 10 | Support Ticket | 9 | Category/priority pairing, large text area |

---

## Risks and Mitigations

1. **Risk:** Prompt/validator loop oscillates and never converges.  
   **Mitigation:** enforce max retries, deterministic correction template, explicit user fallback.

2. **Risk:** Validator feedback too verbose for effective retries.  
   **Mitigation:** normalize to concise error payload before correction prompt.

3. **Risk:** Builder state corruption on generated payload load.  
   **Mitigation:** load into isolated candidate state; apply only after validation pass.

4. **Risk:** Benchmark scores are subjective (Layout Quality, Visual Polish).  
   **Mitigation:** document scoring criteria explicitly; same scorer for baseline and deltas.

5. **Risk:** LLM output quality varies between runs (non-determinism).  
   **Mitigation:** run each benchmark 2-3 times and record best/average; set temperature low.

6. **Risk:** Test harness requires live API key (cost per run).  
   **Mitigation:** cache successful outputs; only re-run when context pack changes.

---

## Test Ownership Split

### Agent-owned
1. Backend/API tests for AI loop orchestration and validator integration.
2. Frontend unit/integration tests for state transitions and error handling.
3. Test harness execution and scoring.
4. Green gate execution via workflow scripts.

### Human-owned
1. UX acceptance on prompt usability and messaging quality.
2. Subjective scoring validation (Layout Quality, Visual Polish dimensions).
3. Any credential-dependent integration verification the agent cannot execute.
4. Final review of benchmark baseline before Story 6.3 proceeds.

---

## PM Review Checklist

- [ ] Scope split is clear: 6.2 = pipeline + harness, 6.3 = context uplift, 6.4 = iteration.
- [ ] POC work is acknowledged and being hardened, not rebuilt.
- [ ] 10 benchmark forms are documented and cover diverse form types.
- [ ] Scoring rubric is defined with 5 measurable dimensions.
- [ ] Test harness is re-runnable for regression detection.
- [ ] Story 6.1 validator dependency is explicit and correct.
- [ ] Retry cap locked to 3 system attempts.
- [ ] Acceptance criteria are testable and deterministic.
- [ ] Risks include benchmark subjectivity and LLM non-determinism.

---

*Story 6.2 reshaped from POC → production pipeline + test harness*  
*Last Updated: 2026-03-20*
