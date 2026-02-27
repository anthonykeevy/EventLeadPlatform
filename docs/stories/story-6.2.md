# Story 6.2: AI Form Builder UI and Agent Loop

**Epic:** Epic 6 - AI Generation and Monetization Engine  
**Domain:** Builder UX, AI orchestration loop, validator-driven retries  
**Status:** Draft for PM Review  
**Priority:** High  
**Created:** 2026-02-27  
**Owner:** PM Agent  
**Prerequisite:** Story 6.1 complete and merged (`POST /api/form-validate` available)
**Context:** `docs/stories/story-context-6.2.xml`  
**UAT Guide:** `docs/stories/STORY-6.2-UAT-TEST-GUIDE.md`  
**AI Context Pack:** `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md`  
**SM Readiness:** `docs/stories/STORY-6.2-SM-READINESS-SUMMARY.md`
**PM Decisions:** Single-page locked; retry cap = 3 system attempts; start provider = ChatGPT API; Global Properties menu switcher (`AI Agent`/`Inspector`/`Logic`)

---

## User Story

**As a** Company User building a form,  
**I want** to describe a form in natural language and have AI generate a valid initial form layout,  
**So that** I can start from a useful draft and then refine it manually in the Builder.

**As a** Product/Engineering team,  
**I want** AI generation to run through a deterministic validation-retry loop before loading to canvas,  
**So that** generated output is structurally valid and less likely to break the Builder UX.

---

## Story Objective

Deliver an MVP AI generation workflow inside the Builder that:
1. accepts user prompt input,
2. calls the AI generation service,
3. injects a versioned LLM context pack (product usage guidance, component rules, and generation constraints),
4. validates candidate `DefinitionJSON` via Story 6.1 endpoint,
5. retries with structured feedback when invalid,
6. loads successful output onto the canvas with clear user messaging.

---

## In Scope

1. Add Builder UI entry point for AI generation in Global Properties panel with three-way menu switch:
   - `AI Agent`
   - `Inspector`
   - `Logic`
   (AI Agent tab hosts prompt/generation controls; Inspector and Logic remain accessible)
2. Add generation request handling and progress state (`idle`, `generating`, `validating`, `retrying`, `completed`, `failed`).
3. Create an initial **LLM Context Pack** used on every generation attempt:
   - product behavior context (how users build/refine forms in EventLead),
   - allowed component taxonomy + required/optional props,
   - layout and canvas rules (single-page MVP constraints),
   - strict JSON-only output contract (no prose, no markdown),
   - deterministic correction instructions for validator-driven retries,
   - examples (one good generation + one corrected-from-errors flow).
4. Implement AI retry loop contract:
   - submit prompt,
   - receive candidate `DefinitionJSON`,
   - call `POST /api/form-validate`,
   - if invalid, build correction prompt from structured errors and retry up to configured max attempts.
5. Load validated `DefinitionJSON` into Builder state and render on canvas.
6. Show user-facing feedback:
   - generation status,
   - success summary,
   - failure reason when retries exhausted.
7. Add audit-style trace metadata for troubleshooting (attempt count, validator result summary, terminal failure reason).
8. Guardrails for MVP:
   - single-page generation only,
   - no direct persistence to production until user saves through existing flow.
9. Provider configuration support:
   - initial provider integration uses ChatGPT API,
   - read provider key from backend environment configuration (for example `OPENAI_API_KEY`),
   - do not expose provider secrets in logs, API responses, or committed files.
10. Retry policy lock for Story 6.2:
   - maximum **3** automatic correction retries per generation request,
   - if still invalid after retry 3, show structured failure outcome to user.

---

## Out of Scope

1. Payment-related components/flows (Stories 6.3+).
2. Multi-page AI generation orchestration.
3. Advanced semantic refinement chat memory across sessions.
4. Automatic publish flow integration.
5. Replacing manual Builder editing patterns.
6. Fine-tuning/model-training pipeline work.

---

## Dependencies (Story 6.1 Contract)

Story 6.2 depends on Story 6.1 validator response contract:
- Endpoint: `POST /api/form-validate`
- Response fields used by loop:
  - `valid`
  - `schemaErrors`
  - `boundaryViolations`
  - `collisions`
  - `summary`

If response shape changes, Story 6.2 loop and prompt-builder logic must be updated in lockstep.

Additional dependency:
- LLM provider credentials are configured in local environment (for example `OPENAI_API_KEY` in `backend/.env`, untracked by git).

---

## Acceptance Criteria / Done Criteria

- [ ] AC1: AI generation UI is available in Builder Global Properties menu under `AI Agent`, with `Inspector` and `Logic` still switchable.
- [ ] AC2: A versioned LLM Context Pack is defined and used for every generation attempt.
- [ ] AC3: System calls AI generation backend and receives candidate `DefinitionJSON`.
- [ ] AC4: Each candidate is validated using Story 6.1 endpoint before canvas load.
- [ ] AC5: Invalid candidates trigger retry loop with structured validator feedback.
- [ ] AC6: Retry loop honors max attempts (**3**) and exits deterministically.
- [ ] AC7: Successful validated output loads into Builder canvas without crash.
- [ ] AC8: Failure states are clearly shown to user with actionable guidance.
- [ ] AC9: Attempt trace metadata is captured for debugging and support.
- [ ] AC10: Initial provider uses ChatGPT API, with key consumed from environment configuration and never emitted in logs/responses.
- [ ] AC11: Green CI/CD evidence produced per Epic 6 workflow.
- [ ] AC12: Tool usage feedback captured via workflow tooling log.

---

## Risks and Mitigations

1. **Risk:** Prompt/validator loop oscillates and never converges.  
   **Mitigation:** enforce max retries, deterministic correction template, and explicit user fallback path.

2. **Risk:** Validator feedback too verbose for effective retries.  
   **Mitigation:** normalize to concise error payload before constructing correction prompt.

3. **Risk:** Builder state corruption on generated payload load.  
   **Mitigation:** load into isolated candidate state first; apply only after validation pass.

4. **Risk:** Performance degradation from repeated calls.  
   **Mitigation:** cap retries, show progress, log latency per attempt for tuning.

5. **Risk:** Test/runtime DB drift affects CI reliability again.  
   **Mitigation:** mandatory workflow preflight script and DB parity rule from Epic 6 workflow guide.

6. **Risk:** LLM output quality varies due to under-specified instructions.  
   **Mitigation:** require versioned context pack with explicit component/rule constraints and correction examples.

---

## Test Ownership Split (Explicit)

### Agent-owned (default for this story)
1. Backend/API tests for AI loop orchestration and validator integration.
2. Automated frontend unit/integration tests for state transitions and error handling.
3. Green gate execution via workflow scripts:
   - `scripts/workflow/preflight-story.ps1`
   - `scripts/workflow/run-green-gate.ps1`
   - `scripts/workflow/generate-story-evidence.ps1`

### Human-owned (only where needed)
1. UX acceptance on prompt usability and messaging quality.
2. Exploratory manual validation of generated layout usefulness.
3. Any external credential-dependent integration verification the agent cannot execute.

Escalate to human only with blocker evidence per Epic 6 workflow policy.

---

## PM Review Checklist

- [ ] Scope is limited to AI UI + loop behavior, not payments or publish flow.
- [ ] Single-page scope is explicitly locked for Story 6.2.
- [ ] LLM Context Pack clearly defines product usage guidance, components, and generation rules.
- [ ] Story 6.1 validator dependency is explicit and correct.
- [ ] Retry cap is locked to 3 system attempts (not a user usage cap).
- [ ] Global Properties switcher pattern (`AI Agent`/`Inspector`/`Logic`) is reflected in scope and ACs.
- [ ] Acceptance criteria are testable and deterministic.
- [ ] Test ownership split is clear and aligned with workflow policy.
- [ ] Risks are captured with practical mitigations.
- [ ] Story is implementation-ready for SM context/UAT artifact generation.

---

*Story 6.2 draft prepared for PM review*  
*Last Updated: 2026-02-27*
