# Epic 3 Workflow Guide - BMAD + Ralf Integration

**Current Focus:** Stories 3.8 & 3.9 - UAT Completion  
**Status:** 🧪 In UAT  

---

## 🚨 **PM MAINTENANCE INSTRUCTIONS**
**FOR THE PM AGENT:**
At the end of every story or UAT cycle, you **MUST** update this document.
1. Identify the **Next Focus** from `EPIC-3-STATUS.md`.
2. **REWRITE** the prompts in Phases 1-4 below to be specific to that focus.
3. Ensure the "Current Focus" header above reflects the new focus.
4. Only then is the story considered "Closed".

---

## 🔧 **Git + PR Discipline (Mandatory)**

This Epic workflow follows the platform-wide Git rules in:
- `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`

**Rules:**
- **Never work directly on `master`.**
- **One Draft PR per Story** (opened immediately) → `master`
- **One PR per Task (Txx)** → into the Story branch
- **Push daily:** no multi-day local-only changes
- **Integrator step is required:** task PR merges + conflict resolution + integration checks are explicit work (not an afterthought)

---

## 🧭 **Recovery Merge Notice (Current Reality)**

On **2026-02-02**, a recovery PR was merged into `master` to restore missing Epic 3 work (builder framework, grid layout system, renderer scaffolding, docs, BMAD assets).

**How to proceed after recovery:**
- Do **not** re-implement Story 3.8/3.9/3.10 from scratch.
- Treat `master` as the **restored baseline**.
- Run UAT; any failures become **fix tasks** (each with its own branch + PR), per the workflow below.

---

## 👥 **Roles & responsibilities (how you want to work)**

- **Anthony (you / human gate):**
  - Provide direction and approvals via this workflow + story artifacts
  - Execute the UAT steps and report pass/fail + notes
  - Decide when the story is acceptable to close
- **Agent(s):**
  - Implement fixes, update documentation, and keep Git/PR discipline
  - Update UAT documents with results once you report them
  - Use logging/diagnostics tooling to troubleshoot and to prove fixes

**Important:** `docs/AGENT-LOGGING-GUIDE.md` is an **agent reference**. You only need to download/attach the requested evidence (e.g. Dev Logs JSON) when asked.

---

## 🧱 **Mode A: Next Story Creation (PM → SM → Ralf-SM)**

Use this mode when you are starting a **brand-new story** (new scope, not just UAT fixes):

1. **PM**: review epic status + prior story feedback, then define the next story focus and boundaries.
2. **SM**: create the story file + story-context XML (with Done Criteria + forbidden zones + placeholder UAT section).
3. **Ralf-SM**: decompose the story into `TASK-PLAN.md` + task specs (`T01...`).

Then execute tasks and return to Mode B for UAT completion.

---

## 📋 **Workflow Architecture**

This workflow uses a **Main Chat + Task Chats** pattern.

**Default for current focus:** Mode B (UAT completion + fix tasks for Stories 3.8/3.9).

```
┌─────────────────────────────────────────────────────────────────────┐
│  MAIN CHAT (persistent throughout story)                            │
│                                                                     │
│  Phase 0: Git setup (create Story/UAT branch + Draft PR)            │
│                    ↓                                                │
│  Phase 1: @pm.mdc kicks off UAT (order + evidence expectations)     │
│                    ↓                                                │
│  Human executes UAT (capture failures as notes + evidence)          │
│                    ↓                                                │
│  Phase 2: @ralf-sm *decompose-story → TASK-PLAN + T01 fix spec      │
│                    ↓                                                │
│  [User opens Task Chat for T01 fix]                                 │
│                    ↓                                                │
│  Phase 3: Fix task cycle + Integrator merges (repeat)               │
│                    ↓                                                │
│  Phase 4: @dev.mdc finalizes UAT + merges Story PR to master        │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  TASK CHAT (one per task, isolated)                                 │
│                                                                     │
│  @ralf-dev *run-task → implements + auto-generates UAT checklist   │
│                    ↓                                                │
│  Human tests using UAT checklist                                   │
│                    ↓                                                │
│  @ralf-uat *record-uat → records results                           │
│                    ↓                                                │
│  @ralf-retro *run-retro → extracts lessons                         │
│                    ↓                                                │
│  Close chat, return to Main Chat                                   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📋 **Phase 0: Git Setup (Main Chat)**

**When:** Before you start any UAT fix work (so nothing can be “local-only”).  
**Goal:** Create a single integration branch + Draft PR for this UAT cycle.

**Recommended branch for this combined UAT cycle:**
- `story/epic3-3.8-3.9-uat-completion`

**Fast path:** use the helper script:
```powershell
./scripts/git/new-story.ps1 -Epic 3 -Story "3.8-3.9" -Slug "uat-completion" -CreateWorktree
```

Then create a Draft PR to `master` (manual if `gh` is not installed).

---

## 📋 **Phase 1: UAT Kickoff (Main Chat)**

**Current Target:** Stories 3.8 & 3.9  
**Goal:** Complete UAT for Story 3.8 (Public Form Renderer) and Story 3.9 (Builder Persistence) now that Grid Layout is complete.

### **Copy/Paste this Prompt for the PM Agent (@pm.mdc)**
```markdown
@pm.mdc Please initiate UAT completion for Story 3.8 and Story 3.9.

Git discipline (mandatory):
- Work must happen on a Story/UAT branch (not `master`).
- A Draft PR must exist from the Story/UAT branch → `master` before any fix work begins.
- Any fixes found during UAT will be implemented as Task branches/PRs into the Story/UAT branch.
- Follow: `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`

Context:
- Story 3.10 (Grid Layout) is complete and unblocks UAT.
- Stories 3.8 and 3.9 were previously blocked.

Requirements:
1. Confirm UAT readiness from `docs/stories/EPIC-3-STATUS.md`
2. Identify current UAT guides:
   - docs/stories/STORY-3.8-UAT-TEST-GUIDE.md
   - docs/stories/STORY-3.8-3.9-UAT-TEST-GUIDE.md
3. Provide UAT execution order and checklist expectations
4. Confirm that any UAT failures will be routed into fix tasks via @ralf-sm
5. Confirm Git discipline for this UAT cycle:
   - A Story/UAT branch exists and is pushed
   - A Draft PR exists from the Story/UAT branch → `master`

Deliverables:
- UAT readiness confirmation
- UAT execution order
- Clear handoff to task creation if failures occur
```

---

## 📋 **Phase 2: UAT Failure Triage (Ralf-SM - Main Chat)**

**When:** After UAT failures are identified for Story 3.8 or 3.9.  
**Goal:** Create targeted fix tasks and keep scope minimal.

### **Copy/Paste this Prompt (@ralf-sm)**
```markdown
@ralf-sm

*decompose-story

Git discipline (mandatory):
- Confirm the active Story/UAT branch exists and is pushed (do not work on `master`).
- Each fix task MUST be implemented on a `task/<story>/<Txx>-<slug>` branch with a PR into the Story/UAT branch.
- Follow: `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`

Inputs:
- Story ID: 3.8 or 3.9
- Story file: docs/stories/story-3.8.md or docs/stories/story-3.9.md
- References: 
  - docs/stories/STORY-3.8-UAT-TEST-GUIDE.md and docs/stories/STORY-3.8-3.9-UAT-TEST-GUIDE.md
  - docs/COMPONENT-FRAMEWORK-REFERENCE.md
  - docs/solution-architecture.md
  - UAT failure notes

Output requirements:
1. Create docs/tasks/3.8/ or docs/tasks/3.9/ TASK-PLAN.md with:
   - Full task skeleton (all task titles with dependencies)
   - Done Criteria from story
   - Dependency graph
2. Create first fix task spec: docs/tasks/3.8/T01-*.md or docs/tasks/3.9/T01-*.md (fully detailed)
3. Create placeholder specs for remaining tasks (title + brief scope only)
4. Initialize docs/tasks/3.8/LESSONS-LEARNED.md or docs/tasks/3.9/LESSONS-LEARNED.md

Task decomposition guidance:
- Each task should be completable in ONE chat session
- Prefer smaller tasks over larger ones
- First task should establish foundation (types, interfaces)
- Last task(s) should be integration/polish
- Each fix task must include the Git/PR expectation:
  - Task branch + PR → into the Story/UAT branch
```

---

## 🐛 **UAT Bugfix Loop (Explicit)**

When a UAT check fails:

1. **Capture evidence** (fast, minimal):
   - Use `docs/AGENT-LOGGING-GUIDE.md` for UI issues (snapshot/log bundle)
   - Use `python backend/enhanced_diagnostic_logs.py --limit 20` for backend/auth/API context
2. **Classify**: defect vs enhancement vs out-of-scope (only AC violations are defects).
3. **Create a fix task** (via `@ralf-sm *decompose-story` or `*refine-task`) with:
   - clear acceptance criteria
   - required verification
   - forbidden zones / scope boundaries
4. **Git:** create a task branch + PR into the Story/UAT branch before coding.
5. Implement + verify (`@ralf-dev *run-task`) → UAT checklist → human UAT → record results → retro.
6. Integrator merges the task PR into the Story/UAT branch, then re-run the failing UAT scenario.

### Skill shortcut (recommended)

Start a new chat and run the project skill **`uat-bugfix`** to execute this entire loop (intake → branch → fix → UAT → finalize) with Git discipline baked in.

## ✅ **Phase 3: Task Execution Cycle (Fix Tasks)**

For **each task**, follow this cycle:

### **Step 3a: Open New Task Chat**

1. Create a new Cursor chat
2. Name it: `Epic3-3.8-Txx <slug>` or `Epic3-3.9-Txx <slug>`

### **Step 3b0: Git Setup for Task (Branch + PR)**

**Goal:** Ensure the task work is safely tracked and mergeable before any long debugging/UAT loop begins.

1. Create a task branch named: `task/<story>/<Txx>-<slug>`
2. Push it immediately
3. Open a PR **into the story branch** (not `master`)
4. Use a task worktree if desired (recommended for isolation)

**Helper script (prints commands with `-DryRun`):**
```powershell
./scripts/git/new-task.ps1 -StoryBranch "<story-branch>" -StoryId "3.8" -TaskId "T01" -Slug "<slug>" -CreateWorktree -CreatePR -DryRun
```

### **Step 3b: Execute Task (@ralf-dev)**

Paste in the new Task Chat:

```markdown
@ralf-dev

Git discipline (mandatory):
- Ensure you are on the task branch (NOT `master`).
- Push at least once per session so nothing is local-only.
- This task PR must target the Story/UAT branch.

*run-task

Task Spec: docs/tasks/3.8/Txx-<slug>.md or docs/tasks/3.9/Txx-<slug>.md

Rules:
- Do not expand scope.
- If anything is out-of-scope, stop and route it.
- Reference docs/GRID-LAYOUT-GUIDE.md for specifications.

Outputs:
- docs/tasks/3.8/Txx-<slug>.completion.md or docs/tasks/3.9/Txx-<slug>.completion.md
- docs/tasks/3.8/Txx-<slug>.uat.md or docs/tasks/3.9/Txx-<slug>.uat.md (auto-generated)
```

**ralf-dev will:**
1. Implement the task
2. Generate completion note with evidence
3. **Auto-generate UAT checklist** (new feature!)

### **Step 3c: Human UAT**

1. Open the UAT checklist at `docs/tasks/3.8/Txx-<slug>.uat.md` or `docs/tasks/3.9/Txx-<slug>.uat.md`
2. Execute each test step manually
3. Mark ✅ or ❌ for each item
4. Note any issues

### **Step 3d: Record UAT Results (@ralf-uat)**

In the **same Task Chat**, paste:

```markdown
@ralf-uat

*record-uat

Inputs:
- Task Spec: docs/tasks/3.8/Txx-<slug>.md or docs/tasks/3.9/Txx-<slug>.md
- UAT Checklist: docs/tasks/3.8/Txx-<slug>.uat.md or docs/tasks/3.9/Txx-<slug>.uat.md
- Your results: 
  [Paste your pass/fail results per step]

Outputs:
- docs/tasks/3.8/Txx-<slug>.uat-results.md or docs/tasks/3.9/Txx-<slug>.uat-results.md
- Update STATUS.md
```

### **Step 3e: Run Retrospective (@ralf-retro)**

In the **same Task Chat**, paste:

```markdown
@ralf-retro

*run-retro

Inputs:
- Task Spec: docs/tasks/3.8/Txx-<slug>.md or docs/tasks/3.9/Txx-<slug>.md
- Completion Note: docs/tasks/3.8/Txx-<slug>.completion.md or docs/tasks/3.9/Txx-<slug>.completion.md
- UAT Results: docs/tasks/3.8/Txx-<slug>.uat-results.md or docs/tasks/3.9/Txx-<slug>.uat-results.md

Outputs:
- docs/tasks/3.8/Txx-<slug>.retro.md or docs/tasks/3.9/Txx-<slug>.retro.md
- Append to docs/tasks/3.8/LESSONS-LEARNED.md or docs/tasks/3.9/LESSONS-LEARNED.md
```

### **Step 3f: Return to Main Chat (@ralf-sm)**

Close the Task Chat. In the **Main Chat**, paste:

```markdown
@ralf-sm

*next-task

Story ID: 3.8 or 3.9
Completed Task: Txx

This will:
1. Verify task completion status
2. Update TASK-PLAN.md
3. Check if story is complete (all tasks done + Done Criteria met)
4. If not complete: Create/refine next task spec
5. Provide new Task Chat instructions
```

### **Step 3g: Integrator Merge (Task PR → Story Branch)**

After UAT passes and retro is recorded for the task:
- Merge the **Task PR** into the **Story branch**
- Resolve conflicts (expected when multiple tasks touch the same files)
- Run integration checks (frontend typecheck/build, backend tests as applicable)
- Delete the task worktree (if used)

**Repeat Steps 3a-3g for each task until all tasks are complete.**

---

## 📊 **Phase 4: UAT Completion (Main Chat)**

**When:** UAT passes for Story 3.8 and Story 3.9, and any fix tasks are complete.

### **Copy/Paste this Prompt for the Developer (@dev.mdc)**
```markdown
@dev.mdc Please finalize UAT for Story 3.8 and Story 3.9.

Git discipline (mandatory):
- Do not do this work on `master` without a Story/UAT PR.
- Confirm all fix task PRs were merged into the Story/UAT branch before merging the Story/UAT PR to `master`.
- Follow: `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`

Requirements:
1. Update `docs/stories/story-3.8.md` and `docs/stories/story-3.9.md` with UAT results.
2. Update `docs/stories/EPIC-3-STATUS.md` (mark 3.8/3.9 as Complete, identify next story).
3. Confirm UAT blockers are resolved and document any residual issues.
4. Confirm all fix task PRs have been merged into the story branch (Integrator step complete).
5. **GIT COMMIT (targeted):**
   ```powershell
   git add docs/stories/story-3.8.md docs/stories/story-3.9.md docs/stories/EPIC-3-STATUS.md
   git commit -m "docs(epic3): complete Story 3.8/3.9 UAT"
   ```
6. Merge the **Story Draft PR** into `master` (per `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`).

Deliverables:
- Finalized Story artifacts
- Updated status documentation
- Confirmation that Component Framework issues are resolved
- Git commit
```

---

## 🔄 **Phase 5: Cycle Reset (PM Agent)**

**When:** Story 3.8/3.9 UAT is finalized.  
**Goal:** Prepare this document for the next story.

### **Copy/Paste this Prompt for the PM Agent (@pm.mdc)**
```markdown
@pm.mdc Please reset the cycle for the next story.

Requirements:
1. Read `docs/stories/EPIC-3-STATUS.md` to identify the next story focus.
2. Update `docs/stories/EPIC-3-WORKFLOW-GUIDE_UPDATED.md`:
   - Update "Current Focus" to the next story.
   - Rewrite Phases 1-4 prompts to be specific to the new story.
   - Ensure goals and context match the new story.
3. Confirm ready for execution.
```

---

## 📁 **Output Artifacts Reference**

### Per Story (created by @ralf-sm)
```
docs/tasks/{story-id}/
├── TASK-PLAN.md           # Task skeleton + dependencies + Done Criteria
├── T01-{slug}.md          # Task spec (fully detailed)
├── T02-{slug}.md          # Task spec
├── ...
└── LESSONS-LEARNED.md     # Accumulated lessons
```

### Per Task (created by @ralf-dev, @ralf-uat, @ralf-retro)
```
docs/tasks/{story-id}/
├── Txx-{slug}.completion.md   # What was done + evidence
├── Txx-{slug}.uat.md          # UAT checklist (auto-generated)
├── Txx-{slug}.uat-results.md  # Human test results
├── Txx-{slug}.retro.md        # Retrospective summary
└── STATUS.md                  # Overall progress tracker
```

### Memory Updates (by @ralf-retro)
```
bmad/ralf-taskflow/memory/
├── dev-patterns.yaml          # Implementation patterns
├── common-failures.yaml       # Failure patterns
├── test-gap-patterns.yaml     # Testing gaps
└── process-improvements.yaml  # Process refinements

docs/learning/
└── testing-playbook.md        # Reusable test patterns
```

---

## ⚡ **Quick Reference: Agent Commands**

| Agent | Command | Purpose |
|-------|---------|---------|
| @ralf-sm | `*decompose-story` | Story → TASK-PLAN + Task Specs |
| @ralf-sm | `*next-task` | Review completed task, prepare next |
| @ralf-sm | `*refine-task` | Update task spec based on feedback |
| @ralf-dev | `*run-task` | Execute task (impl + completion + UAT checklist) |
| @ralf-uat | `*record-uat` | Record human UAT results |
| @ralf-retro | `*run-retro` | Extract lessons, update memory |

---

## 🔧 **Troubleshooting**

### Task is too large
- @ralf-dev will STOP and propose a split
- Return to Main Chat, @ralf-sm creates new sub-tasks

### UAT fails
- @ralf-uat marks as FailedUAT
- @ralf-retro documents root cause
- Return to Main Chat, @ralf-sm creates fix task

### Scope creep discovered
- @ralf-dev flags as OUT OF SCOPE
- @ralf-retro routes to BACKLOG-ITEMS.md
- @ralf-sm reviews before next task

### All tasks done but Done Criteria fail
- @ralf-sm identifies gap
- Creates additional task to address
- Continue task cycle
