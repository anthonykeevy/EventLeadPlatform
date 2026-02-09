# Epic 5 Workflow Guide - BMAD + Ralf Integration

**Current Focus:** Story 5.1 - Background Asset Management (Epic 5 kickoff)  
**Status:** ✅ Approved (2026-02-07) · 🔄 In Progress  

---

## 🔧 Git + PR Discipline (Mandatory)

This workflow follows the platform-wide Git rules in:
- `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`

**Rules:**
- **Never work directly on `master`.**
- **One Draft PR per Story** (opened immediately) → `master`
- **One PR per Task (Txx)** → into the Story branch
- **Push daily:** no multi-day local-only changes
- **Integrator step is required:** task PR merges + conflict resolution + integration checks are explicit work (not an afterthought)

---

## 🎯 Epic 5 Reference (PM-owned)

- Epic scope + proposed story roadmap: `docs/stories/EPIC-5-STATUS.md`
- PRD anchors: `docs/prd.md` (Preview/Testing + Publishing + Publish Request flow)
- Optional UX concept: `docs/stories/UNIFIED-FORM-WORKSPACE-SPECIFICATION.md`

---

## 🧭 Workflow Evolution Goal (Epic 5)

Epic 5’s goal is to **remove the human from the loop where not needed** by shifting repeatable mechanics to agents (Git/PR hygiene, status consistency, routine checks), while keeping humans for true blockers only.

**After each Task** in Epic 5, we will:
- Run a short **workflow review** (what worked / what slowed us down).
- Record the incremental change in: `docs/stories/EPIC-5-WORKFLOW-GUIDE-CHANGELOG.md`
- If the workflow itself needs an update, apply it as a **Story-branch-only** change (do not include workflow edits inside Task PRs).

**Scope + sharing policy (important):**
- This workflow is **Epic 5 specific** and **not shared** outside Epic 5.
- It will change often; avoid copying it into other epics to prevent drift and confusion.

---

## 👤🧑 vs 🤖 Responsibilities (Epic 5 default)

### 🧑 Human (only where required)
- Open the correct worktree folder in Cursor (agents operate in the folder you opened).
- Execute **manual UAT only when required** (UI/flow validation, high‑risk changes, or when explicitly requested).
- Execute **final Story UAT** before merging the Story PR → `master`.
- Execute **DB migrations** (agents prepare; humans run).
- Provide product decisions and approvals (scope, UX trade-offs, “good enough” thresholds).
- Enter any secrets/credentials (never in chat output).

### 🤖 AI (default owner)
- Create Story/Task branches + worktrees + PRs (and verify PR base).
- Keep task/status docs consistent (task header + `TASK-PLAN.md` + `STATUS.md`).
- Commit + push at least once per session; keep PRs updating reliably.
- Run **as many automated checks as possible** and capture evidence (commands + pass/fail + gaps).
- If automated verification sufficiently covers the task’s acceptance criteria, **record UAT PASS with evidence** (agent-owned) and proceed to retro without blocking on a human checkpoint.
- Merge Task PRs into Story (integrator step) when UAT is ✅ PASS.
- Maintain `EPIC-5-WORKFLOW-GUIDE.md` + `EPIC-5-WORKFLOW-GUIDE-CHANGELOG.md` on the **Story branch** (never in Task PRs).
- Clean up task branches/worktrees (when safe).

---

## 🧠 BMAD / Ralf Agent Map (who does what)

| Stage | Agent / Tool | Owner | Output |
|------|--------------|-------|--------|
| Create story artifacts | `@sm.mdc` | AI (prompted by human) | `docs/stories/story-<id>.md`, `story-context-<id>.xml`, `STORY-<id>-UAT-TEST-GUIDE.md` |
| Decompose story into tasks | `@ralf-sm *decompose-story` | AI | `docs/tasks/<story>/TASK-PLAN.md`, `STATUS.md`, `LESSONS-LEARNED.md`, `T01-*.md` + placeholders |
| Implement a task | `@ralf-dev *run-task` | AI | Code changes + task artifacts (completion/uat/uat-results/retro) |
| Record human UAT (only when required) | `@ralf-uat *record-uat` | Human executes UAT; AI records | `${TaskBase}.uat-results.md` |
| Retro | `@ralf-retro *run-retro` | AI | `${TaskBase}.retro.md` + updates to `LESSONS-LEARNED.md` (story branch) |
| Git automation | `scripts/git/new-story.ps1`, `scripts/git/new-task.ps1`, `gh` | AI | Branch/worktree/PR creation, merges |

**Rule:** Workflow doc updates are committed on the **Story branch** only (not in Task PRs).

---

## 🚀 Epic Kickoff (start here)

The Epic 5 kickoff path is:

- (Optional) Phase -1 UX Ideation → output: `docs/stories/EPIC-5-UX-IDEATION.md`
- Phase 0 Story bootstrap (branch/worktree + Draft PR)
- Phase 1 Story artifacts (SM)
- Phase 2 Decompose into tasks (Ralf-SM)
- Phase 3 Execute tasks (Ralf-dev/uat/retro + integrator merges)
- Phase 4 Story closeout (final Story UAT + merge Story PR → `master`)
- Phase 5 Epic closeout (after all Epic 5 stories merged)

---

## 🎨 Phase -1: UX Ideation (UX Expert / UX Designer) — RECOMMENDED

**When:** Before Story 5.1 branch creation (reduces long UAT loops).  
**Goal:** Align **Dashboard vs Builder** responsibilities and define the minimal set of screens/flows needed for customer value.

**Primary artifact (owned by this phase):**
- `docs/stories/EPIC-5-UX-IDEATION.md`

### Copy/Paste this Prompt for the UX Designer Agent (`@ux-designer.mdc`)

> Note: the UX agents show a menu first; after they greet you, reply with `*create-design`.

```markdown
@ux-designer.mdc

We are starting Epic 5: Form Builder Readiness + Review & Publishing.

Goal: produce a lightweight UX ideation/spec so we can ship Epic 5 with minimal UAT thrash.

Inputs:
- Epic scope: `docs/stories/EPIC-5-STATUS.md`
- PRD publish request flow (Company User → Admin): `docs/prd.md` (User Flows section “Create Form & Request Publish”)
- Unified workspace concept (optional): `docs/stories/UNIFIED-FORM-WORKSPACE-SPECIFICATION.md`

Output requirements:
1. Clarify **Builder vs Dashboard** responsibilities for Epic 5 (what lives where, and why).
2. Provide a minimal **screen map** and **happy-path journeys** for:
   - Company User (build → preview test → request publish → handle feedback)
   - Company Admin (review queue → review → test if needed → publish/unpublish)
3. Include the **Form Builder Readiness tranche** UX implications:
   - Background asset upload/picker UX (no embedded base64; assets are reusable)
   - Company-level brand defaults UX (set once, inherit everywhere; show “inherited vs overridden”)
4. Define key UX copy for gating states (threshold not met, role cannot publish, pending admin review).
5. Capture edge cases (request changes, decline, unpublished, activation window ended).
6. Write the results into: `docs/stories/EPIC-5-UX-IDEATION.md`

Constraints:
- Payments are out of scope (Epic 6). Do not require Stripe in the UX.
- Analytics dashboards are out of scope (Epic 7). Keep “visibility” focused on readiness + publishing state.
```

### Alternate: UX Expert Agent (`@ux-expert.mdc`)

If you prefer a broader ideation/website-planning workflow, use `@ux-expert.mdc` then select `*plan-project`.

---

## 📋 Phase 0: Git Setup (Main Chat)

**When:** Before you start Story 5.1 implementation work.  
**Goal:** Create a Story branch + Draft PR for Story 5.1.

**Recommended first story (per Epic 5 draft roadmap):**
- **Story 5.1:** Background Asset Management
- **Branch:** `story/epic5-5.1-background-asset-management`

```powershell
./scripts/git/new-story.ps1 -Epic 5 -Story "5.1" -Slug "background-asset-management" -CreateWorktree -DraftPR -WorktreeRoot "C:\wt\elp"
```

🧑 **Human checkpoint (only if needed):**
- If the script creates a worktree folder, open it in Cursor (new window recommended): `C:\wt\elp\story-epic5-5.1-background-asset-management`

---

## 📋 Phase 1: Story Artifact Creation (SM - Main Chat)

### Copy/Paste this Prompt for the Scrum Master Agent (`@sm.mdc`)

```markdown
@sm.mdc Please create the Story 5.1 artifacts for Epic 5: Form Builder Readiness + Review & Publishing.

Git discipline (mandatory):
- Work must happen on a Story branch (not `master`).
- A Draft PR must exist from the Story branch → `master` before implementation begins.
- All implementation will occur via Task branches/PRs into the Story branch.
- Follow: `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`
- If the Story branch/worktree/Draft PR does not exist yet, STOP and run Phase 0 using:
  `./scripts/git/new-story.ps1 -Epic 5 -Story "5.1" -Slug "background-asset-management" -CreateWorktree -DraftPR -WorktreeRoot "C:\wt\elp"`

Context:
- Epic 3 is complete (builder + renderer + submission/outbox).
- Epic 5 goal: **Form Builder Readiness first** (assets + defaults + schema parity), then preview/production + publish governance.
- Epic scope/roadmap: `docs/stories/EPIC-5-STATUS.md`
- PRD: `docs/prd.md` sections 4A + 7 + Publish Request flow.

Requirements:
1. Read `docs/stories/EPIC-5-STATUS.md` and confirm Story 5.1 is the next focus.
2. Create/Update these artifacts:
   - `docs/stories/story-5.1.md`
   - `docs/stories/story-context-5.1.xml`
   - `docs/stories/STORY-5.1-UAT-TEST-GUIDE.md`
3. Story 5.1 should establish **background asset management**:
   - Replace embedded base64 Data URLs with asset references in form definitions
   - Backend persistence model for assets (DB/storage + lifecycle)
   - Renderer + builder parity plan for resolving assets consistently
   - **Limits must be config-backed**: any upload/runtime limits must be stored in `config.AppSetting` (loaded via `ConfigurationService`)
     - Include proposed `SettingKey` list in the story (draft keys ok; finalize during decomposition)
   - Storage provider abstraction to allow a **painless swap** (Local dev → Azure Blob prod) via config (no schema redesign)
   - **No migration expected** (background images weren’t functional/used in existing forms as of 2026-02-07), but add a defensive guard against embedded Data URLs
4. Explicitly defer:
   - Company-level defaults (Story 5.2)
   - Schema/validation alignment (Story 5.3)
   - Governance workflow (preview/prod + publish request + admin review) (Story 5.5+)
   - Payments/invoicing (Epic 6)

Deliverables:
- Story 5.1 artifacts created/updated
- Ready handoff to @ralf-sm for decomposition
```

---

## 📋 Phase 2: Story Decomposition (Ralf-SM - Main Chat)

### Copy/Paste this Prompt (`@ralf-sm`)

```markdown
@ralf-sm

*decompose-story

Git discipline (mandatory):
- Confirm the active Story branch exists and is pushed (do not work on `master`).
- Each task MUST be implemented on a `task/<story>/<Txx>-<slug>` branch with a PR into the Story branch.
- Follow: `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`

Inputs:
- Story ID: 5.1
- Story file: `docs/stories/story-5.1.md`
- Context file: `docs/stories/story-context-5.1.xml`
- References:
  - `docs/prd.md`
  - `docs/stories/EPIC-5-STATUS.md`

Output requirements:
1. Create `docs/tasks/5.1/TASK-PLAN.md`
2. Create first task spec `docs/tasks/5.1/T01-*.md`
3. Create placeholder specs for remaining tasks
4. Initialize `docs/tasks/5.1/LESSONS-LEARNED.md`
5. Create/update `docs/tasks/5.1/STATUS.md` (current task = **T01** initially)
```

---

## 📌 Phase 2.5: Commit the Story Artifacts (MANDATORY)

**Goal:** Ensure every task branch contains the story/task specs to prevent drift and duplicate artifacts.

After Phase 1 + Phase 2 outputs are created/updated:
- Commit the updated Story artifacts and decomposed task files on the **Story branch**
- Push the Story branch
- Only then create Task branches from that Story branch

---

## ✅ Phase 3: Task Execution Cycle (Epic 5 Full Workflow)

Each task follows this explicit loop. Do not skip steps.

### Step 1: Create task branch + worktree + PR (agent-owned)

```powershell
scripts/git/new-task.ps1 -StoryBranch "story/epic5-5.1-background-asset-management" -StoryId 5.1 -TaskId T01 -Slug "asset-contracts-and-config-foundations" -CreateWorktree
```

#### Step 1A: PR bootstrap commit (mandatory)

**Goal:** Ensure a PR can be created immediately (avoids “no commits between base/head”).

- Edit the task spec `docs/tasks/<story>/<TaskBase>.md`
  - Update **Status** to: `🔄 In Progress (Approved)`
- Commit + push that single doc change

**Commit cadence (avoid micro-commits):**
- Target 2–3 commits per task:
  - PR bootstrap commit (status → In Progress)
  - Implementation (+ artifacts)
  - Closeout updates (if needed)
- Only do extra commits when they materially reduce risk (e.g., large refactors, checkpoints before risky steps).

#### Step 1B: Create the PR (after bootstrap commit)

Option A (preferred): re-run the task script to create the PR (safe to re-run):

```powershell
scripts/git/new-task.ps1 -StoryBranch "story/epic5-5.1-background-asset-management" -StoryId 5.1 -TaskId T01 -Slug "asset-contracts-and-config-foundations" -CreatePR
```

Option B: create the PR directly:

```powershell
gh pr create --base "story/epic5-5.1-background-asset-management" --head "task/5.1/T01-asset-contracts-and-config-foundations" --title "5.1: T01 - asset-contracts-and-config-foundations"
```

**PR safety check (mandatory):** verify base/head **before** doing any real work.

### Step 2: Implement the task (Ralf-Dev)

Use `@ralf-dev *run-task` with the task spec path. Keep changes scoped to the task spec.

**Do not re-confirm work that is already approved:**
- The task spec is the approval artifact. Once a task is approved, the dev agent should **not** ask the human to “confirm scope/ACs again”.
- In the `*run-task` prompt, explicitly state: “Scope + ACs are pre‑approved; proceed end‑to‑end without waiting for interactive confirmations.”
- If your internal taskflow normally pauses for `y/n` at each step, **assume yes** and continue (do not block on the human repeating approvals).

**Canonical task artifact filenames (to avoid duplicates):**
- Let `TaskBase = <task spec filename without .md>` (example: `T01-asset-contracts-and-config-foundations`)
- Store task artifacts under `docs/tasks/<story>/` using:
  - `${TaskBase}.completion.md`
  - `${TaskBase}.uat.md` (checklist)
  - `${TaskBase}.uat-results.md` (evidence + PASS/FAIL)
  - `${TaskBase}.retro.md`
- **Important:** Ralf taskflow may auto-generate generic names like `T01.uat.md` / `T01.completion.md`.
  - Before committing/merging, **rename** them to `${TaskBase}.*` and update any links.
  - Do **not** commit the generic `T01.*` artifact filenames (they will collide or duplicate later).

### Step 3: Automated verification (required, before UAT decision)

Before deciding whether human UAT is required, the dev agent must run **all relevant automated checks** and record evidence:
- Commands run (with working directory)
- Pass/fail summary
- What could not be run (and why)
- What the human should re-test manually

**If the baseline is already broken:**
- If a standard check fails due to **pre-existing baseline issues**, capture evidence (error count + short summary) and explicitly label it as baseline.
- Then run the most **scoped** verification you can for the touched area (and document what you did).
- Do not claim the task “broke the build” unless you can show a new regression.

**Prompt snippet (paste into each task’s `@ralf-dev *run-task` message):**

```markdown
Automated verification (must do before I run manual UAT):
- Run as many automated checks as possible for the areas you touched and record evidence in the completion note:
  - Commands run (with working directory)
  - Pass/fail summary
  - What you could not run (and why)
  - What I should re-test manually
- Suggested defaults:
  - Frontend (if touched):
    - `cd frontend`
    - `npm install` (only if needed)
    - `npm run lint`
    - `npm run build`
  - Backend (if touched):
    - `python -m pytest` (if tests exist/configured)
    - else minimum: `python -m compileall backend`
```

### Step 4: UAT (default agent-owned; human only when required)

**Default (Epic 5):** If Step 3 passes and the task’s acceptance criteria are verifiable via automated checks + deterministic inspection, the dev agent should:
- Create/update `${TaskBase}.uat-results.md` with evidence and mark ✅ PASS  
  - Preferred: hand results to `@ralf-uat *record-uat` with **Tester = AI/Agent** so the UAT file format + task-plan updates stay consistent.
- Update `docs/tasks/<story>/TASK-PLAN.md` and `docs/tasks/<story>/STATUS.md`
- Proceed directly to retro (Step 5)

**Human UAT is required only when:**
- The task spec explicitly says “Human UAT required”, or
- The task changes UI/UX flows that need human validation, or
- The task includes manual-only steps (DB migrations, credentials), or
- Automated verification cannot reasonably cover the acceptance criteria

When human UAT is required:
- Execute the task’s UAT guide (`${TaskBase}.uat.md`)
- Record results via `@ralf-uat *record-uat`

**Agent-owned UAT recording (copy/paste snippet):**

```markdown
#yolo
@ralf-uat *record-uat
Tester: AI/Agent
Results:
- AC1: PASS — <evidence>
- AC2: PASS — <evidence>
```

#### DB migration tasks (special sequencing — prevents Alembic/worktree mismatch)

**Rule:** Never ask a human to run `alembic upgrade head` until the migration files exist in the *current worktree* and the worktree contains **every revision already applied to the DB**.

- **Trunk rule:** Don’t upgrade a shared/dev DB from “temporary” migrations that aren’t merged into your working trunk (Story branch). If you apply a migration from a task branch, merge that task PR into the Story before starting another DB task/worktree.

- **Always run Alembic from the task worktree** (not the OneDrive repo, not another worktree):

```powershell
cd C:\wt\elp\<task-worktree>\backend
alembic upgrade head
```

- **Preflight (prevents “missing revision” errors):**
  - Human runs: `SELECT version_num FROM alembic_version;`
  - AI verifies: the file `backend/migrations/versions/<version_num>_*.py` exists in the task worktree
  - If it does **not** exist: STOP. Fix the branch/worktree first (sync/merge the missing migration chain) before creating/applying any new migration.

- **UAT for DB-only tasks:** migration output + deterministic verification queries count as the UAT evidence. If those pass, AI records ✅ PASS and proceeds (no extra human “checkbox UAT” loop needed).

### Step 5: Retro (required after UAT pass)

After UAT is ✅ PASS (agent-owned or human):
- Run `@ralf-retro *run-retro`
- Ensure story-level learning is captured in `docs/tasks/<story>/LESSONS-LEARNED.md`

**BMAD workflow automation tip:** Use `#yolo` mode when running workflows to avoid per-step “continue?” confirmations (especially for retro):

```markdown
#yolo
@ralf-retro *run-retro
Task: T02
Story: 5.1
```

**Epic 5 note:** The retro workflow’s “update memory files” step is treated as optional. In Epic 5, prefer skipping memory-file updates and capture improvements in:
- `docs/tasks/<story>/LESSONS-LEARNED.md`
- `docs/stories/EPIC-5-WORKFLOW-GUIDE-CHANGELOG.md`

#### PM sanity-check (prevents wrong root-cause writeups)

After retro, PM (or AI acting as PM) does a quick check:
- Confirm the retro’s “root cause” matches the transcript/evidence (tool issue vs workflow timing issue).
- If misattributed, capture the corrected prevention action in:
  - `docs/tasks/<story>/LESSONS-LEARNED.md` (story learning), and
  - `docs/stories/EPIC-5-WORKFLOW-GUIDE-CHANGELOG.md` (process change history)

**Epic 5 non-sharing rule (important):**
- Do **not** commit changes under `bmad/ralf-taskflow/memory/` as part of Epic 5 tasks.
- Workflow/process improvements must be captured in:
  - `docs/stories/EPIC-5-WORKFLOW-GUIDE.md` (this file), and
  - `docs/tasks/<story>/LESSONS-LEARNED.md`

### Step 6: Integrator merge (agent-owned after UAT pass + retro)

- Merge Task PR → Story branch
- Resolve conflicts and run integration checks if needed
- Update task/status docs as required

### Step 7: Workflow review (required after each task)

At the end of each task (on the Story branch, after the task PR is merged):
- Run a **workflow review** (what worked / what slowed us down).
- If needed, update **this file** (**Story branch only**; do not include workflow edits inside Task PRs).
- Append an entry to `docs/stories/EPIC-5-WORKFLOW-GUIDE-CHANGELOG.md`.

---

## ✅ Phase 4: Story Closeout (after all tasks are merged)

**Goal:** Merge the Story PR → `master` with end-to-end evidence.

### Step 1: Confirm story is ready to close
- All task PRs are merged into the Story branch.
- `docs/tasks/<story>/TASK-PLAN.md` shows all tasks ✅ Done / ✅ HumanDone.
- `docs/tasks/<story>/STATUS.md` is up to date.

### Step 2: Final Story UAT (required)
- Human runs the story UAT guide: `docs/stories/STORY-<id>-UAT-TEST-GUIDE.md`
- Record results (recommended): `docs/stories/STORY-<id>-UAT-RESULTS.md`
- If UAT fails: create a fix task branch/PR (do not patch on the Story branch without a task).

### Step 3: Merge Story PR → `master` (integrator)
- Ensure Story PR base is `master`
- Merge (no force push; resolve conflicts; run integration checks if needed)

### Step 4: Update epic tracking
- Update `docs/stories/EPIC-5-STATUS.md` (mark the story ✅ complete)

---

## ✅ Phase 5: Epic Closeout (after all Epic 5 stories are merged)

**Goal:** Close Epic 5 cleanly and move to the next epic.

- Confirm all Epic 5 stories are merged to `master` and reflected in `docs/stories/EPIC-5-STATUS.md`.
- Update the overall epic tracker (if used): `docs/epic-status.md`
- Run an Epic retro (recommended) and capture learnings (file name is flexible; keep it under `docs/stories/`).

---

*Epic 5 Workflow Guide - created for Epic 5 cycle start*  
*Last Updated: 2026-02-09*

---

## 📓 Workflow change history (Epic 5)

See `docs/stories/EPIC-5-WORKFLOW-GUIDE-CHANGELOG.md`.

