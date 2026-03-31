# Epic 6 Workflow Guide — BMAD Method (No Ralf)

**Workflow:** BMAD method only. SM agent prepares Story, context, and UAT; SM reviews artifacts; Dev agent builds via single-session prompt. No Ralf decomposition or task cycle.

**Current Focus:** Story 6.3 - AI Context Uplift & Benchmark Baseline (Epic 6)  
**Story 6.2.1 Status:** ✅ Complete (merged 2026-03-30, PR #54)  
**Story 6.2.2 Status:** ✅ Complete (merged 2026-03-31, PR #55)  
**Story 6.3 Status:** ⏳ Pending (next — unblocked)  

---

## ⚡ Epic 6 Story Workflow (BMAD)

This is the streamlined workflow established at the end of Epic 5.

| Step | Actor | Action |
|------|-------|--------|
| 0 | **Human** | Confirm PR closed, `git pull origin master` in main repo |
| 1 | **@bmad-agent-bmm-pm** | Approves scope; finalizes PM decisions doc (`docs/stories/story-6.x.md`) |
| 2 | **@bmad-agent-bmm-sm** | Prepares context (`story-context-6.x.xml`) & UAT guide (`STORY-6.x-UAT-TEST-GUIDE.md`) |
| 3 | **@bmad-agent-bmm-sm** | Uses `Shell` tool to run `./scripts/git/new-story.ps1` and set up the Git worktree & Draft PR |
| 4 | **Human** | Switch Cursor window to the newly created worktree (`C:\wt\elp\...`) |
| 5 | **@bmad-agent-bmm-dev** | Implements the story end-to-end. Runs `pytest` & `npm test`. Fixes issues. Creates final commit & PR. |
| 6 | **Human** | Manual UAT per `STORY-6.x-UAT-TEST-GUIDE.md` and merge PR via GitHub/gh |

**Artifacts:** `story-6.x.md`, `story-context-6.x.xml`, `STORY-6.x-UAT-TEST-GUIDE.md`, `STORY-6.x-SINGLE-SESSION-DEV-PROMPT.md`

---

## 🔧 Git + PR Discipline (Mandatory)

This workflow follows the platform-wide Git rules in:
- `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`

**Rules:**
- **Never work directly on `master`.**
- **One Draft PR per Story** (opened immediately) → `master`
- **Implementation on Story branch** — no task branches
- **Push daily:** no multi-day local-only changes

## 🛑 The "Green CI/CD" Rule (Mandatory for Epic 6+)
To prevent technical debt accumulation and AI Hallucinations regarding test status, the Dev agent is strictly bound by the Green CI/CD Rule:
1. Before creating the final closeout commit, the Dev agent **MUST** run:
   - Frontend: `npm run lint` and `npm run test:unit -- --watch=false`
   - Backend: `python -m pytest --tb=short`
2. **ANTI-HALLUCINATION PROTOCOL:** The agent MUST read the exact output of the test run. If the test process times out, hangs, or the output is truncated before showing the final `=== X passed, Y failed ===` summary, the agent MUST treat the test as **FAILED**.
3. The agent is **NOT** allowed to end its turn or close the story until all tests demonstrably pass and **0** linting errors/warnings remain in the touched files.
4. If the test suites or linters fail, the Dev agent must fix them as part of the story implementation loop before asking the human for help.

---

## 🧰 Workflow Automation Toolkit (Mandatory for Epic 6+)

Use the workflow scripts to reduce repetitive agent overhead and keep evidence consistent:

1. **Preflight** (worktree + branch + DB resolution parity):
   - `.\scripts\workflow\preflight-story.ps1 -ExpectedWorktreePath "C:\wt\elp\<story-worktree>" -ExpectedBranch "story/epicX-X.X-<slug>" -ReportFile "docs/stories/STORY-X.X-PREFLIGHT.md"`
2. **Green gate execution** (anti-truncation summary enforcement):
   - `.\scripts\workflow\run-green-gate.ps1 -StoryId "X.X" -FocusedTestCommand "python -m pytest tests/test_story_x_x.py --tb=short" -BackendGateCommand "python -m pytest --tb=short" -EvidenceFile "docs/stories/STORY-X.X-GATE-EVIDENCE.md"`
3. **Evidence sync** (append gate evidence into UAT results):
   - `.\scripts\workflow\generate-story-evidence.ps1 -StoryId "X.X" -GateEvidenceFile "docs/stories/STORY-X.X-GATE-EVIDENCE.md" -UatResultsFile "docs/stories/STORY-X.X-UAT-RESULTS.md"`
4. **Tool feedback capture** (continuous process improvement):
   - `.\scripts\workflow\collect-tool-feedback.ps1 -StoryId "X.X" -ToolName "run-green-gate.ps1" -Rating 4 -Feedback "What worked and what should improve"`

---

## 🗄️ Database Connection Consistency Rule (Mandatory)

To prevent test/runtime drift:

1. All backend code paths that connect to the DB must resolve connection settings from a common source.
2. Test harness DB resolution must align with runtime DB resolution (no independent fallback logic that diverges).
3. During preflight, always capture both:
   - `os.getenv("DATABASE_URL")`
   - runtime-resolved DB URL from `common.database`.
4. Any mismatch that changes selected DB backend (for example SQL Server vs SQLite) must be treated as a gate-risk and corrected before closeout.

---

## 🚀 Epic Kickoff (Start Here)

The Epic 6 kickoff path leverages the newly updated **BMAD v6** commands (`@bmad-agent-bmm-sm.md`, etc.).

- Phase 0: Agentic Story bootstrap (branch/worktree + Draft PR) for 6.1
- Phase 1: Story artifacts (SM prepares Story, context, UAT)
- Phase 2: Dev single-session implementation

### 📋 Phase 0 & 1: Agentic Setup for Story 6.1 (Main Chat)

**Prompt for `@bmad-agent-bmm-sm.md`:**

```markdown
@bmad-agent-bmm-sm.md Please act as Scrum Master and orchestrate Phase 0 and Phase 1 for Story 6.1: AI Foundation: Static Validator.

Git discipline:
1. Use the Shell tool to run: `./scripts/git/new-story.ps1 -Epic 6 -Story "6.1" -Slug "ai-foundation-static-validator" -CreateWorktree -DraftPR -WorktreeRoot "C:\wt\elp"`
2. Wait for the script to finish successfully.

Context:
- Epic scope/roadmap: `docs/stories/EPIC-6-STATUS.md`
- Concept: `docs/AI-FORM-BUILDING-IDEA.md`
- Goal: Build a static backend validator API (`POST /api/form-validate`) that accepts `DefinitionJSON` and returns schema + collision/boundary errors without needing a DOM.

Requirements:
1. Create `docs/stories/story-6.1.md` focusing purely on the backend validation API.
2. Create `docs/stories/story-context-6.1.xml` highlighting that this leverages existing collision logic.
3. Create `docs/stories/STORY-6.1-UAT-TEST-GUIDE.md` with Postman/Swagger test instructions.
4. Create `docs/stories/STORY-6.1-SINGLE-SESSION-DEV-PROMPT.md` containing the strict Green CI/CD instructions for the Dev agent.
```

---

## ✅ Phase 2: Dev Single-Session Implementation (Execution Contract)

**Owner:** `@bmad-agent-bmm-dev`  
**Goal:** Implement the full story in one execution loop without weakening quality gates.

### Required run order (before requesting human UAT)
1. Run preflight script and resolve any failures:
   - `.\scripts\workflow\preflight-story.ps1 ...`
2. Implement story scope only (respect in-scope/out-of-scope from `story-6.x.md`).
3. Run Green CI/CD via toolkit script:
   - `.\scripts\workflow\run-green-gate.ps1 ...`
4. If any check fails, fix and re-run until fully green.
5. Produce story evidence artifacts using toolkit script:
   - `.\scripts\workflow\generate-story-evidence.ps1 ...`
6. Commit and push only when checks are demonstrably green.

### Why this gate is strict
Epic 6 adopts TEA-informed quality enforcement because high error volume was previously normalized and important failures were ignored over time. Current TEA baseline is **94/100**, and this workflow preserves that baseline by requiring green verification at the end of **every** story.

---

## 📦 Story Evidence Contract (Mandatory Before Human UAT)

Before the human runs manual UAT, the Dev agent must provide all of the following in the story PR comment or closeout note:

1. Commands run (exact command and working directory).
2. Final test/lint summaries copied from terminal output.
3. Pass/fail table for frontend and backend checks.
4. List of checks not run (if any) with explicit reason.
5. Suggested manual-only checks for the human UAT pass.

If summaries are missing, truncated, or non-final, the story is treated as **NOT READY FOR UAT**.

---

## 🧪 Phase 3: Human UAT + Merge Gate

**Owner:** Human  
**Goal:** Validate behavior the agent cannot fully validate and enforce release quality.

### Required checklist
1. Run manual UAT from `STORY-6.x-UAT-TEST-GUIDE.md`.
2. Verify the Dev agent evidence package is complete and consistent with PR changes.
3. Confirm no unresolved P0/P1 defects remain.
4. Merge Story PR only when:
   - Green CI/CD evidence is complete,
   - Manual UAT passes,
   - Scope boundaries are preserved.

---

## 🔄 Phase 4: Story Closeout + Next Story Reset

**Owner:** `@bmad-agent-bmm-pm` or `@bmad-agent-bmm-sm`  
**Goal:** Keep epic flow deterministic after each story merge.

### Required closeout actions
1. Update story completion status in `docs/stories/EPIC-6-STATUS.md`.
2. Record lessons/process adjustments in this workflow changelog section.
3. In main repo, confirm PR merged and run `git pull origin master`.
4. Confirm next story focus and regenerate the next story prompt pack.
5. Record developer-agent feedback on script/tool usage:
   - `.\scripts\workflow\collect-tool-feedback.ps1 ...`

---

## 🚨 Failure Routing Policy (Green Gate Protection)

If Green CI/CD does not pass after reasonable fix attempts:

1. Stop broad implementation.
2. Classify issue:
   - **Defect in current story scope** -> continue in same story until fixed.
   - **Cross-cutting debt/blocker** -> create a micro-fix follow-up story and link it.
3. Do not claim story complete with unresolved gate failures.
4. Escalate to TEA review when failures indicate systemic test instability or unclear assertions.

---

## ☁️ Cloud Co-Developer Worktree Model (Epic 6)

Epic 6 supports adding a second developer agent (cloud) while preserving branch hygiene.

### Operating model
1. One active implementation owner per story branch.
2. If cloud agent is used in parallel:
   - use a separate branch/worktree for cloud work,
   - open a PR into the active story branch,
   - integrate only after Green CI/CD evidence is provided.
3. Never have two agents pushing directly to the same branch concurrently.

### Recommended usage pattern
- Local dev agent: primary story implementation and stabilization.
- Cloud dev agent: bounded sub-problem (refactor slice, isolated test fix, analysis spike).
- Integrate cloud contribution through PR review into story branch, then rerun full Green CI/CD.

This preserves your learning objective (multi-agent experience) without weakening release controls.

---

## 📒 Workflow Changelog (Epic 6)

| Date | Change | Why |
|------|--------|-----|
| 2026-02-26 | Added explicit Phase 2 execution contract, Phase 3 human merge gate, and Phase 4 reset process | Epic 6 was latest but not final; needed closeout and reset mechanics to avoid drift |
| 2026-02-26 | Added Story Evidence Contract tied to Green CI/CD output quality | Prevent false-green/hallucinated completion and preserve per-story quality gate |
| 2026-02-26 | Added Failure Routing Policy with TEA escalation path | Ensure failing gates are routed deterministically instead of deferred silently |
| 2026-02-26 | Added Cloud Co-Developer Worktree Model | Enable second developer agent usage while maintaining branch integrity and quality control |
| 2026-02-26 | Added workflow automation scripts + mandatory tool feedback logging | Reduce repetitive agent effort and create continuous improvement loop |
| 2026-02-26 | Added database connection consistency rule for test/runtime parity | Prevent recurring SQL backend drift between app runtime and pytest harness |
