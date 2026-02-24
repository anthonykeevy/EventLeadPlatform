# Epic 6 Workflow Guide — BMAD Method (No Ralf)

**Workflow:** BMAD method only. SM agent prepares Story, context, and UAT; SM reviews artifacts; Dev agent builds via single-session prompt. No Ralf decomposition or task cycle.

**Current Focus:** Story 6.1 - AI Foundation: Static Validator (Epic 6)  

---

## ⚡ Epic 6 Story Workflow (BMAD)

This is the streamlined workflow established at the end of Epic 5.

| Step | Human | Agent |
|------|-------|-------|
| 0 | **Before new story:** Confirm PR closed, `git pull origin master` in main repo | — |
| 1 | PM approves scope; PM decisions doc finalized | — |
| 2 | — | **@sm** prepares Story, context (XML), UAT guide; SM reviews and suggests improvements |
| 3 | Run `new-story.ps1`; open Story worktree in Cursor | — |
| 4 | Create STORY-6.x-SINGLE-SESSION-DEV-PROMPT.md | — |
| 5 | Paste Dev prompt into new chat | **@dev** implements full story; **MUST achieve 100% green tests & 0 lint warnings before closeout** |
| 6 | Run migration (`alembic upgrade head`) if created | — |
| 7 | Manual UAT per STORY-6.x-UAT-TEST-GUIDE.md | — |
| 8 | Merge Story PR to master | — |

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
To prevent technical debt accumulation, the Dev agent is strictly bound by the Green CI/CD Rule:
1. Before creating the final closeout commit, the Dev agent **MUST** run:
   - Frontend: `npm run lint` and `npm run test:unit`
   - Backend: `python -m pytest`
2. The agent is **NOT** allowed to end its turn or close the story until all tests pass and **0** linting errors/warnings remain in the touched files.
3. If the test suites or linters fail, the Dev agent must fix them as part of the story implementation.

---

## 🚀 Epic Kickoff (Start Here)

The Epic 6 kickoff path is:

- Phase 0: Story bootstrap (branch/worktree + Draft PR) for 6.1
- Phase 1: Story artifacts (SM prepares Story, context, UAT)
- Phase 2: Dev single-session prompt

### 📋 Phase 0: Git Setup for Story 6.1

**When:** Before starting Story 6.1 implementation.  
**Goal:** Create Story 6.1 branch + Draft PR.

```powershell
./scripts/git/new-story.ps1 -Epic 6 -Story "6.1" -Slug "ai-foundation-static-validator" -CreateWorktree -DraftPR -WorktreeRoot "C:\wt\elp"
```

🧑 **Human checkpoint:** Open the new worktree in Cursor: `C:\wt\elp\story-epic6-6.1-ai-foundation-static-validator`

---

### 📋 Phase 1: Story 6.1 Artifact Creation (SM - Main Chat)

**Prompt for `@sm.mdc`:**

```markdown
@sm.mdc Please create the Story 6.1 artifacts for Epic 6: AI Generation & Monetization Engine.

Git discipline:
- If the Story branch/worktree/Draft PR does not exist yet, STOP and run Phase 0 using:
  `./scripts/git/new-story.ps1 -Epic 6 -Story "6.1" -Slug "ai-foundation-static-validator" -CreateWorktree -DraftPR -WorktreeRoot "C:\wt\elp"`

Context:
- Epic scope/roadmap: `docs/stories/EPIC-6-STATUS.md`
- Concept: `docs/AI-FORM-BUILDING-IDEA.md`
- Goal: Build a static backend validator API (`POST /api/form-validate`) that accepts `DefinitionJSON` and returns schema + collision/boundary errors without needing a DOM. This provides the feedback loop the AI agent will use to correct itself in Story 6.2.

Requirements:
1. Create `docs/stories/story-6.1.md` focusing purely on the backend validation API.
2. Create `docs/stories/story-context-6.1.xml` highlighting that this leverages our existing collision logic (`checkCanvasBoundary`, `checkCollision`) ported to Python, or exposing a Node.js utility, but the end result is a structured JSON feedback response for the AI.
3. Create `docs/stories/STORY-6.1-UAT-TEST-GUIDE.md` with instructions on how to test the API via Postman or Swagger by sending good/bad `DefinitionJSON`.
```
