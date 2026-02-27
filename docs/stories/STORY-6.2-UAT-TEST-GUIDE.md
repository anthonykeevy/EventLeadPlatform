# Story 6.2 UAT Test Guide - AI Form Builder UI and Agent Loop

**Story:** 6.2  
**Epic:** 6 - AI Generation and Monetization Engine  
**Updated:** 2026-02-27  
**UAT Status:** Draft

---

## Objective

Verify that the AI Builder flow can generate, validate, retry, and safely load form definitions using Story 6.1 validator feedback, while keeping ownership split explicit between agent and human tests.

PM-confirmed constraints:
- Single-page generation only.
- Retry cap is 3 system correction attempts per generation request.
- Global Properties menu switcher includes `AI Agent`, `Inspector`, and `Logic`.

---

## Test Ownership Split (Mandatory)

### Agent-owned tests (default)
1. Backend/API tests for generation + validator retry behavior.
2. Frontend automated tests for state transitions and non-crash behavior.
3. Green gate execution and evidence generation using workflow scripts.

### Human-owned tests (targeted only)
1. UX quality checks (prompt usability, status wording clarity).
2. Exploratory assessment of generation usefulness for real workflows.
3. Any provider/runtime checks that require credentials/access unavailable to the agent.

Escalation to human requires blocker evidence per Epic 6 workflow policy.

---

## Preflight (Agent-Owned)

Run before implementation/UAT:

```powershell
.\scripts\workflow\preflight-story.ps1 -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.2-ai-form-builder-ui-agent-loop" -ExpectedBranch "story/epic6-6.2-ai-form-builder-ui-agent-loop" -ReportFile "docs/stories/STORY-6.2-PREFLIGHT.md"
```

Expected:
- Worktree path and branch match.
- Runtime DB resolution check passes.
- No preflight FAIL rows.

---

## Agent-Owned UAT Cases

| Test ID | Type | Description | Owner | Expected |
|---------|------|-------------|-------|----------|
| A1 | Frontend auto | Prompt panel/modal renders and accepts input | Agent | Input accepted; state moves to generating |
| A2 | Backend/API | AI generation call returns candidate payload | Agent | Candidate `DefinitionJSON` received |
| A3 | Backend/API | Validator called on every candidate | Agent | `POST /api/form-validate` called before load |
| A4 | Backend/API | Invalid candidate triggers retry | Agent | Retry prompt built from structured errors |
| A5 | Backend/API | Max attempts enforced | Agent | Loop exits deterministically at configured cap |
| A6 | Frontend auto | Valid candidate loads to canvas | Agent | Canvas updates; no crash |
| A7 | Frontend auto | Failure state shown when retries exhausted | Agent | Clear user message with next action |
| A8 | Backend/API | Attempt trace metadata recorded | Agent | Attempt count + summary + terminal reason captured |
| A9 | Security/config | Provider secret handling | Agent | No key leakage in logs or responses |
| A10 | UX structure (auto) | Global Properties switcher behavior | Agent | `AI Agent`, `Inspector`, and `Logic` are switchable and stable |

---

## Human-Owned UAT Cases

| Test ID | Type | Description | Owner | Expected |
|---------|------|-------------|-------|----------|
| H1 | UX | Prompt guidance is understandable for non-technical users | Human | User can successfully describe desired form |
| H2 | UX | Status/progress wording is clear and non-ambiguous | Human | Users understand wait/retry/failure states |
| H3 | Exploratory | Generated form usefulness for real scenario | Human | Draft requires refinement but is meaningfully usable |
| H4 | Prompt quality loop | Evaluate generated output quality against agreed gates | Human + Agent | Meets acceptance threshold by <= configured cycle count |

---

## Green Gate Execution (Agent-Owned)

```powershell
.\scripts\workflow\run-green-gate.ps1 -StoryId "6.2" -FocusedTestCommand "python -m pytest tests/test_story_6_2_*.py --tb=short" -BackendGateCommand "python -m pytest --tb=short" -FrontendGateCommand "npm run lint; npm run test:unit -- --watch=false" -EvidenceFile "docs/stories/STORY-6.2-GATE-EVIDENCE.md"
.\scripts\workflow\generate-story-evidence.ps1 -StoryId "6.2" -GateEvidenceFile "docs/stories/STORY-6.2-GATE-EVIDENCE.md" -UatResultsFile "docs/stories/STORY-6.2-UAT-RESULTS.md"
```

---

## Tool Feedback Capture (Mandatory)

After execution, record feedback for iterative script improvement:

```powershell
.\scripts\workflow\collect-tool-feedback.ps1 -StoryId "6.2" -ToolName "preflight-story.ps1" -Rating 1 -Feedback "<feedback>"
.\scripts\workflow\collect-tool-feedback.ps1 -StoryId "6.2" -ToolName "run-green-gate.ps1" -Rating 1 -Feedback "<feedback>"
.\scripts\workflow\collect-tool-feedback.ps1 -StoryId "6.2" -ToolName "generate-story-evidence.ps1" -Rating 1 -Feedback "<feedback>"
```

Rating scale: 1 (poor) to 5 (excellent)

---

## Prompt Quality Evaluation Loop (Required)

Use a bounded improvement loop to avoid subjective "looks good" decisions.

### Quality gates per cycle
1. Structural validity rate (validator pass on first attempt).
2. Retry convergence rate (valid by retry <= 3).
3. Layout usability score (human quick rating 1-5).
4. Edit distance effort (how much manual correction is needed after load, low/med/high).

### Process
1. Run a fixed prompt set (minimum 10 representative prompts).
2. Record metrics for each prompt.
3. If gates not met, update context pack/rules only (not random tweaks), rerun next cycle.
4. Repeat for up to X cycles (recommended X=3 for Story 6.2).
5. Accept when thresholds are met for two consecutive cycles.

### Suggested initial thresholds
- >= 80% validator pass by retry <= 3
- >= 70% human usability score >= 4/5
- manual correction effort low/medium for >= 80% prompts

Document each cycle in `docs/stories/STORY-6.2-UAT-RESULTS.md`.

---

## Exit Criteria

- All agent-owned tests pass or have documented, valid blocker evidence.
- Human-owned tests completed with pass/fail notes.
- Green gate evidence file generated with explicit summaries.
- UAT results file updated.
- Tool feedback log entries recorded.

---

*Story 6.2 UAT Guide (SM draft)*  
*Last Updated: 2026-02-27*
