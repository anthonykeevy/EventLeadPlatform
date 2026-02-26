# Epic 6 Workflow Guide — BMAD Method (No Ralf)

**Workflow:** BMAD method only. SM agent prepares Story, context, and UAT; SM reviews artifacts; Dev agent builds via single-session prompt. No Ralf decomposition or task cycle.

**Current Focus:** Story 6.1 - AI Foundation: Static Validator (Epic 6)  

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
