# Epic 3 Workflow Guide - BMAD + Ralf Integration

**Current Focus:** Story 3.11 - Dynamic Submission (Outbox)  
**Status:** 🔄 In Progress  

---

## 🚨 **PM MAINTENANCE INSTRUCTIONS**
**FOR THE PM AGENT:**
At the end of every story or UAT cycle, you **MUST** update this document.
1. Identify the **Next Focus** from `EPIC-3-STATUS.md`.
2. **REWRITE** the prompts in Phases 0-4 below to be specific to that focus.
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
- Treat `master` as the **restored baseline**.
- Start Story 3.11 as **new implementation work** on top of that baseline.
- If any regressions in completed stories (3.8/3.9/3.10) are discovered during 3.11 work, route them as **fix tasks** (each with its own branch + PR), per the workflow below.

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

**Default for current focus:** Mode A (Next Story Creation + implementation tasks for Story 3.11).

```
┌─────────────────────────────────────────────────────────────────────┐
│  MAIN CHAT (persistent throughout story)                            │
│                                                                     │
│  Phase 0: Git setup (create Story branch + Draft PR)                │
│                    ↓                                                │
│  Phase 1: @sm.mdc creates Story 3.11 artifacts                      │
│                    ↓                                                │
│  Phase 2: @ralf-sm *decompose-story → TASK-PLAN + T01 spec          │
│                    ↓                                                │
│  [User opens Task Chat for T01]                                     │
│                    ↓                                                │
│  Phase 3: Task cycle + Integrator merges (repeat)                   │
│                    ↓                                                │
│  Human executes Story 3.11 UAT (from story UAT guide)               │
│                    ↓                                                │
│  Phase 4: @dev.mdc finalizes Story 3.11 + merges Story PR to master │
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

**When:** Before you start Story 3.11 implementation work (so nothing can be “local-only”).  
**Goal:** Create a single Story branch + Draft PR for Story 3.11.

**Recommended branch for Story 3.11:**
- `story/epic3-3.11-dynamic-submission`

**Fast path:** use the helper script (recommended: short worktree root on Windows):
```powershell
$env:ELP_WORKTREE_ROOT = "C:\wt\elp"
./scripts/git/new-story.ps1 -Epic 3 -Story "3.11" -Slug "dynamic-submission" -CreateWorktree -DraftPR
```

Then create a Draft PR to `master` (manual if `gh` is not installed).

### **Agent-owned Git setup (recommended for Git novices)**

If you want the agent to do Phase 0 for you (recommended), copy/paste in the **Main Chat**:

```markdown
@dev.mdc

Please run **Phase 0 Git setup** for Story 3.11.

Requirements:
- Use a short worktree root: set `$env:ELP_WORKTREE_ROOT = "C:\wt\elp"` for this session.
- Run: `./scripts/git/new-story.ps1 -Epic 3 -Story "3.11" -Slug "dynamic-submission" -CreateWorktree -DraftPR`
- If `gh` is not installed, provide the manual steps to create the Draft PR on GitHub UI.

Outputs:
- Confirm the story branch exists and is pushed
- Provide the story worktree path that was created
- Provide the Draft PR link (or the manual GitHub steps)
```

---

## 📋 **Phase 1: Story Artifact Creation (SM - Main Chat)**

**Current Target:** Story 3.11 - Dynamic Submission (Outbox)  
**Goal:** Create/validate the Story 3.11 story artifact(s) (story file + context XML + initial UAT plan) so the story can be decomposed into tasks.

### **Copy/Paste this Prompt for the Scrum Master Agent (@sm.mdc)**
```markdown
@sm.mdc Please create the Story 3.11 artifacts for Epic 3: Dynamic Submission (Outbox).

Git discipline (mandatory):
- Work must happen on a Story branch (not `master`).
- A Draft PR must exist from the Story branch → `master` before implementation begins.
- All implementation will occur via Task branches/PRs into the Story branch.
- Follow: `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`
- If the Story branch/worktree/Draft PR does not exist yet, STOP and run Phase 0 (agent-owned) using `./scripts/git/new-story.ps1 ... -CreateWorktree -DraftPR` (use `$env:ELP_WORKTREE_ROOT = "C:\wt\elp"`).

Context:
- Stories 3.8–3.10 are complete; the next planned story is **3.11 - Dynamic Submission**.
- Story 3.11 delivers **The Outbox**: offline-capable submission queue + sync.

Requirements:
1. Read `docs/stories/EPIC-3-STATUS.md` and confirm the next focus is Story 3.11.
2. Create/Update these artifacts:
   - `docs/stories/story-3.11.md` (Done Criteria + scope boundaries + dependencies + risks)
   - `docs/stories/story-context-3.11.xml` (context + forbidden zones + acceptance criteria)
   - `docs/stories/STORY-3.11-UAT-TEST-GUIDE.md` (initial UAT plan; can be refined during tasks)
3. Ensure the story explicitly states:
   - **In scope**: renderer submission UX + offline outbox queue + sync behavior (as defined by Epic 3)
   - **Out of scope** (if applicable): advanced conflict resolution, back-office workflows, analytics, etc.
4. Confirm Git discipline for this story:
   - A Story branch exists and is pushed
   - A Draft PR exists from the Story branch → `master`

Deliverables:
- Story 3.11 story + context artifacts created/updated
- Initial UAT guide stub created/updated
- Ready handoff to @ralf-sm for decomposition
```

---

## 📋 **Phase 2: Story Decomposition (Ralf-SM - Main Chat)**

**When:** After Story 3.11 artifacts exist and are approved.  
**Goal:** Decompose Story 3.11 into implementable tasks with minimal scope creep.

### **Copy/Paste this Prompt (@ralf-sm)**
```markdown
@ralf-sm

*decompose-story

Git discipline (mandatory):
- Confirm the active Story branch exists and is pushed (do not work on `master`).
- Each task MUST be implemented on a `task/<story>/<Txx>-<slug>` branch with a PR into the Story branch.
- Follow: `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`

Inputs:
- Story ID: 3.11
- Story file: `docs/stories/story-3.11.md`
- Context file: `docs/stories/story-context-3.11.xml`
- References: 
  - `docs/solution-architecture.md`
  - `docs/COMPONENT-FRAMEWORK-REFERENCE.md` (renderer + component framework context)
  - `docs/AGENT-LOGGING-GUIDE.md` (UI evidence expectations if bugs arise)
  - Any UX/product notes for submission/outbox

Output requirements:
1. Create `docs/tasks/3.11/TASK-PLAN.md` with:
   - Full task skeleton (all task titles with dependencies)
   - Done Criteria from story
   - Dependency graph
2. Create first task spec: `docs/tasks/3.11/T01-*.md` (fully detailed)
3. Create placeholder specs for remaining tasks (title + brief scope only)
4. Initialize `docs/tasks/3.11/LESSONS-LEARNED.md`
5. **Phase 3 readiness sweep (required):**
   - Create/update `docs/tasks/3.11/STATUS.md` (current task = **T01** initially)
   - Ensure **ALL** Phase 3 task specs exist (`docs/tasks/3.11/Txx-*.md`)
   - Ensure each task spec header is consistent with `TASK-PLAN.md` (Status + Dependencies)

Task decomposition guidance:
- Each task should be completable in ONE chat session
- Prefer smaller tasks over larger ones
- First task should establish foundation (types, API contracts, data model, queue storage strategy)
- Last task(s) should be integration + UAT polish
- Each task must include the Git/PR expectation:
  - Task branch + PR → into the Story branch

Important constraints:
- If DB migrations are required, the agent must PREPARE the exact commands/files, but a human executes migrations.
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
4. **Git:** create a task branch + PR into the Story branch before coding.
5. Implement + verify (`@ralf-dev *run-task`) → UAT checklist → human UAT → record results → retro.
6. Integrator merges the task PR into the Story branch, then re-run the failing UAT scenario.

### Skill shortcut (recommended)

Start a new chat and run the project skill **`uat-bugfix`** to execute this entire loop (intake → branch → fix → UAT → finalize) with Git discipline baked in.

## ✅ **Phase 3: Task Execution Cycle (Implementation Tasks)**

For **each task**, follow this cycle:

### **Step 3a: Open New Task Chat**

🧑 **Human**
1. If you created a task worktree: **open that task worktree folder** in Cursor (recommended: a separate window)
2. Create a new Cursor chat
3. Name it: `Epic3-3.11-Txx <slug>`

✅ **Human check (quick):**
- Confirm the chat name matches the task spec filename.
- In the integrated terminal **in the same Cursor window**, run `git branch --show-current` and confirm you are on the expected `task/...` branch. (Agents can’t switch worktrees; they operate in whatever folder you opened.)

### **Step 3b0: Git Setup for Task (Branch + PR)**

**Goal:** Ensure the task work is safely tracked and mergeable before any long build/debug/UAT loop begins.

1. Create a task branch named: `task/<story>/<Txx>-<slug>`
2. Push it immediately
3. Open a PR **into the story branch** (not `master`)
4. Use a task worktree if desired (recommended for isolation)

**If GitHub won’t let you open the PR yet (common):**

- If you see `No commits between ...` when creating the PR, it means the branch has no unique commits yet.
- Fix: make a tiny “start task” commit (example: set the task spec `**Status:** 🔄 In Progress`), then push and create the PR.

🧑 **Human checkpoint (required, 60 seconds):**

Run these commands in the **task worktree** and confirm the output makes sense before coding:

```powershell
git status -sb
git branch --show-current
git rev-parse --short HEAD
```

Confirm on GitHub (UI or `gh`) that:
- The **Task PR base** is the **Story branch** (NOT `master`)
- A **Draft Story PR** exists from **Story → `master`** (re-create it if it was merged/closed)

**Avoid the #1 PR mistake (wrong base branch):**
- Do **not** click GitHub’s “Compare & pull request” banner (it defaults base to `master`).
- Always create the Task PR with either:
  - `./scripts/git/new-task.ps1 ... -CreatePR` (preferred), or
  - `gh pr create --base "<story-branch>" --head "<task-branch>" ...`

**If the Task PR base is wrong (e.g., it targets `master`):**
- Fix it immediately (recommended via CLI):

```powershell
& "C:\Program Files\GitHub CLI\gh.exe" pr edit <PR_NUMBER> --base "<story-branch>"
```

- If GitHub UI won’t let you change base: it’s usually because the branch has **no unique commits yet**. Make the tiny “start task” commit, push, then edit the PR base.

**Helper script (prints commands with `-DryRun`):**
```powershell
./scripts/git/new-task.ps1 -StoryBranch "<story-branch>" -StoryId "3.11" -TaskId "T03" -Slug "<slug>" -CreateWorktree -CreatePR -DryRun
```

**Agent-owned Git setup (recommended for Git novices):**

If you want the agent to create the task branch + worktree + PR for you, copy/paste in the **Main Chat** (or at the start of the Task Chat):

```markdown
@dev.mdc

Please create the Git setup for the next task (agent-owned).

Inputs:
- Story branch: <story-branch>
- Story ID: 3.11
- Task ID: Txx
- Slug: <slug>

Requirements:
- Use a short worktree root: set `$env:ELP_WORKTREE_ROOT = "C:\wt\elp"` for this session.
- Run: `./scripts/git/new-task.ps1 -StoryBranch "<story-branch>" -StoryId "3.11" -TaskId "Txx" -Slug "<slug>" -CreateWorktree -CreatePR`
- If `gh` is not installed, provide manual PR creation steps (task PR → story branch).

Outputs:
- Confirm the task branch exists and is pushed
- Provide the task worktree path that was created
- Provide the Task PR link (or the manual GitHub steps)
```

#### Runtime / worktree preflight (prevents “endpoint missing” confusion)

Before you start services (backend/frontend) or run UAT, verify the runtime folder is **the right branch** and **up-to-date**.

- In the folder you will run the backend from (usually the **Story worktree**), run:

```powershell
git status -sb
git branch --show-current
git rev-parse --short HEAD
```

- If you see `[behind N]` → `git pull` before testing.
- If you have local edits (`git status --porcelain` not empty) → commit them to the correct **task branch**, or stash them. Keep the **Story worktree clean**.

**GH CLI note (Windows):**
- If `gh` is not on PATH, you can run it with:

```powershell
& "C:\Program Files\GitHub CLI\gh.exe" --version
```

#### Worktrees: `EventLeadPlatform` vs worktree root (read this if you feel “lost”)

- `EventLeadPlatform/` is your **main worktree** (one local clone + the main `.git` store).
- Your **worktree root** contains **additional worktrees** (extra checkouts) created by the helper scripts:
  - Default: `..\EventLeadPlatform.wt` (relative to repo root)
  - Recommended on Windows: `C:\wt\elp` (set `$env:ELP_WORKTREE_ROOT = "C:\wt\elp"`)
- Each worktree is checked out to **one specific branch**. This lets you work on multiple branches at once without constant switching.
- **Agents do not “switch workspaces” automatically.** They operate in **whatever folder you opened in Cursor**:
  - If you open `EventLeadPlatform/`, the agent is working in the main worktree.
  - If you open the worktree folder (e.g. `C:\wt\elp\<some-branch-worktree>`), the agent is working in that branch’s worktree.

**If you hit “path too long” issues (Windows):**
- Prefer a **short worktree root** outside OneDrive (example: `C:\wt\elp`)
- Set `$env:ELP_WORKTREE_ROOT = "C:\wt\elp"` (per machine), or pass `-WorktreeRoot` to the helper scripts.

### **Step 3b: Execute Task (@ralf-dev)**

Paste in the new Task Chat:

```markdown
@ralf-dev

IMPORTANT (do not ask me twice):
- If my message already contains a menu trigger (like `*run-task`), execute it immediately (do NOT show a menu and wait).
- First, state the current git branch (`git branch --show-current`). If you are not on the expected `task/...` branch, STOP and tell me exactly which worktree folder to open in Cursor.

Git discipline (mandatory):
- Ensure you are on the task branch (NOT `master`).
- Push at least once per session so nothing is local-only.
- This task PR must target the Story branch.
- If the task branch/worktree/PR does not exist yet, STOP and create it using `./scripts/git/new-task.ps1 ... -CreateWorktree -CreatePR` (use `$env:ELP_WORKTREE_ROOT = "C:\wt\elp"`), then proceed.

*run-task

Task Spec: docs/tasks/3.11/Txx-<slug>.md

Rules:
- Do not expand scope.
- If anything is out-of-scope, stop and route it.
- Follow the Story 3.11 Done Criteria and forbidden zones.

Outputs:
- docs/tasks/3.11/Txx-<slug>.completion.md
- docs/tasks/3.11/Txx-<slug>.uat.md (auto-generated)
```

**If you see a menu instead of execution:** reply with `*run-task` (only) and the task spec path (if requested). The goal is one message → execution, not a two-step handshake.

**ralf-dev will:**
1. Implement the task
2. Generate completion note with evidence
3. **Auto-generate UAT checklist** (new feature!)

### **Step 3c: Human UAT**

1. Open the UAT checklist at `docs/tasks/3.11/Txx-<slug>.uat.md`
2. Execute each test step manually
3. Mark ✅ or ❌ for each item
4. Note any issues

### **Step 3d: Record UAT Results (@ralf-uat)**

In the **same Task Chat**, paste:

```markdown
@ralf-uat

IMPORTANT (do not ask me twice):
- If my message already contains a menu trigger (like `*record-uat`), execute it immediately (do NOT show a menu and wait).

*record-uat

Inputs:
- Task Spec: docs/tasks/3.11/Txx-<slug>.md
- UAT Checklist: docs/tasks/3.11/Txx-<slug>.uat.md
- Your results: 
  [Paste your pass/fail results per step]

Outputs:
- docs/tasks/3.11/Txx-<slug>.uat-results.md
- Update STATUS.md
```

**If you see a menu instead of execution:** reply with `*record-uat` (only) and paste your results again.

### **Step 3e: Run Retrospective (@ralf-retro)**

In the **same Task Chat**, paste:

```markdown
@ralf-retro

*run-retro

Inputs:
- Task Spec: docs/tasks/3.11/Txx-<slug>.md
- Completion Note: docs/tasks/3.11/Txx-<slug>.completion.md
- UAT Results: docs/tasks/3.11/Txx-<slug>.uat-results.md

Outputs:
- docs/tasks/3.11/Txx-<slug>.retro.md
- Append to docs/tasks/3.11/LESSONS-LEARNED.md
```

### **Step 3e1: Final Commit + Push (Agent-owned)**

After retro output files are created, ensure nothing is “local-only” (this is what makes the PR reliably appear/update in GitHub):

```powershell
git status --porcelain
git add -A
git commit -m "<storyId>: <TaskId> - record UAT + retro"
git push
```

- If `git status --porcelain` is empty: still confirm the branch is pushed and the PR shows the latest commit.

### **Step 3f: Return to Main Chat (@ralf-sm)**

Close the Task Chat. In the **Main Chat**, paste:

```markdown
@ralf-sm

*next-task

Story ID: 3.11
Completed Task: Txx

This will:
1. Verify task completion status
2. Update TASK-PLAN.md
3. Check if story is complete (all tasks done + Done Criteria met)
4. If not complete: Create/refine next task spec
5. Provide new Task Chat instructions
6. Ensure Phase 3 task specs remain consistent (update Status/Dependencies headers + `docs/tasks/3.11/STATUS.md`)
```

### **Step 3g: Integrator Merge (Task PR → Story Branch)**

This is the “integrator” step: it’s where the task becomes **officially part of the story** (and where conflicts are handled on purpose, not by accident).

After UAT passes, retro is recorded, and Step 3e1 push is done:
- Merge the **Task PR** into the **Story branch**
- Resolve conflicts (expected when multiple tasks touch the same files)
- Run integration checks (frontend typecheck/build, backend tests as applicable)
- Delete the task worktree (if used)

🧑 **Human checkpoint (required):**
- Before clicking “Merge”, confirm the PR base is the **Story branch** (not `master`).
- After merge, `git pull` in the **Story worktree** and confirm your changes landed (then continue to the next task).
- If anything looks “missing”, verify you are running services from the **Story worktree** (see “Runtime / worktree preflight”).

**Repeat Steps 3a-3g for each task until all tasks are complete.**

---

## 📊 **Phase 4: Story Completion (Main Chat)**

**When:** Story 3.11 tasks are complete and Story 3.11 UAT passes.

### **Copy/Paste this Prompt for the Developer (@dev.mdc)**
```markdown
@dev.mdc Please finalize Story 3.11 (Dynamic Submission / Outbox).

Git discipline (mandatory):
- Do not do this work on `master` without a Story PR.
- Confirm all task PRs were merged into the Story branch before merging the Story PR to `master`.
- Follow: `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`

Requirements:
1. Update `docs/stories/story-3.11.md` and `docs/stories/story-context-3.11.xml` with completion + evidence.
2. Update `docs/stories/STORY-3.11-UAT-TEST-GUIDE.md` with final pass/fail results.
3. Update `docs/stories/EPIC-3-STATUS.md` (mark 3.11 as Complete, identify next focus).
4. Confirm Story 3.11 Done Criteria are met and document any residual issues.
5. Confirm all task PRs have been merged into the Story branch (Integrator step complete).
6. Merge the **Story Draft PR** into `master` (per `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`).

Deliverables:
- Finalized Story artifacts
- Updated status documentation
- Confirmation that Dynamic Submission (Outbox) is working end-to-end
```

---

## 🔄 **Phase 5: Cycle Reset (PM Agent)**

**When:** Story 3.11 is finalized (merged to `master`).  
**Goal:** Prepare this document for the next story.

### **Copy/Paste this Prompt for the PM Agent (@pm.mdc)**
```markdown
@pm.mdc Please reset the cycle for the next story.

Requirements:
1. Read `docs/stories/EPIC-3-STATUS.md` to identify the next story focus.
2. Update `docs/stories/EPIC-3-WORKFLOW-GUIDE_UPDATED.md`:
   - Update "Current Focus" to the next story.
   - Rewrite Phases 0-4 prompts to be specific to the new story.
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
