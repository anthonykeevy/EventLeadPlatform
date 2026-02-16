# Epic 5 Workflow Guide - BMAD + Ralf Integration

**Current Focus:** Story 5.4 - Shared Resolver Parity (Epic 5)  
**Story 5.1 Status:** ✅ Complete (2026-02-13) — Merged to master  
**Story 5.2 Status:** ✅ Complete (2026-02-16) — Merged to master (#32)  
**Story 5.3 Status:** ✅ Complete (2026-02-16) — Single-session; UAT passed; retro done; merge pending  

---

## ⚡ Single-Session Story Workflow (Story 5.3 validated)

**When:** Backend-heavy stories with clear DCs; schema/API/tests; limited or no frontend. Story 5.3 proved this path works.

| Step | Human | Agent |
|------|-------|-------|
| 1 | Run `new-story.ps1`; open Story worktree in Cursor | — |
| 2 | Paste single-session Dev prompt (see `docs/stories/STORY-5.3-SINGLE-SESSION-DEV-PROMPT.md`) | @dev implements full story; runs automated UAT; records evidence in STORY-5.x-UAT-RESULTS.md |
| 3 | Run migration (`alembic upgrade head`) if migration created | — |
| 4 | Manual UAT (Form Builder save/load, etc.); verify evidence | — |
| 5 | Run retro; update EPIC-5-WORKFLOW-GUIDE | — |
| 6 | Merge Story PR to master | — |

**Artifacts:** `docs/stories/STORY-5.x-SINGLE-SESSION-DEV-PROMPT.md` (copy from 5.3, adapt scope). Human runs migrations only. See `docs/stories/STORY-5.3-RETRO.md` and `docs/tasks/5.3/LESSONS-LEARNED.md`.

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

Epic 3’s workflow guide (`docs/stories/EPIC-3-WORKFLOW-GUIDE_UPDATED.md`) is the **final, human-heavy reference** for Epic 3 and should remain unchanged.

Epic 5’s goal is to **remove the human from the loop where not needed** by shifting repeatable mechanics to agents (Git/PR hygiene, status consistency, routine checks), while keeping humans for true blockers only.

**After each Story** in Epic 5, we will:
- Run a short “workflow retro” and update **this file** (streamline prompts/steps).
- Record the change in the “Workflow Change Log” at the bottom.

---

## 👤🧑 vs 🤖 Responsibilities (Epic 5 default)

### 🧑 Human (only where required)
- Open the correct worktree folder in Cursor (agents operate in the folder you opened).
- Execute **manual UAT** and report results.
- Execute **DB migrations** (agents prepare; humans run).
- Provide product decisions and approvals (scope, UX trade-offs, “good enough” thresholds).
- Enter any secrets/credentials (never in chat output).

### 🤖 AI (default owner)
- Create Story/Task branches + worktrees + PRs (and verify PR base).
- Keep task/status docs consistent (task header + `TASK-PLAN.md` + `STATUS.md`).
- Commit + push at least once per session; keep PRs updating reliably.
- Run **as many automated checks as possible** and capture evidence (commands + pass/fail + gaps).
- Merge Task PRs into Story (integrator step) when UAT is ✅ PASS.
- Clean up task branches/worktrees (when safe).

---

## 🚀 Epic Kickoff (start here)

The Epic 5 kickoff path is:

- (Optional) Phase -1 UX Ideation → output: `docs/stories/EPIC-5-UX-IDEATION.md`
- Phase 0 Story bootstrap (branch/worktree + Draft PR)
- Phase 1 Story artifacts (SM)
- Phase 2 Decompose into tasks (Ralf-SM)
- Phase 3 Execute tasks (Ralf-dev/uat/retro + integrator merges)

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

## 📋 Phase 0: Git Setup for Story 5.2

**When:** Before starting Story 5.2 implementation.  
**Goal:** Create Story 5.2 branch + Draft PR.

- **Story 5.2:** Company Form Defaults (Brand System)
- **Branch:** `story/epic5-5.2-company-form-defaults`

```powershell
./scripts/git/new-story.ps1 -Epic 5 -Story "5.2" -Slug "company-form-defaults" -CreateWorktree -DraftPR -WorktreeRoot "C:\wt\elp"
```

🧑 **Human checkpoint:** If the script creates a worktree, open it in Cursor: `C:\wt\elp\story-epic5-5.2-company-form-defaults`

---

## 📋 Phase 1: Story 5.2 Artifacts (Ready)

Story 5.2 artifacts are **already created** (scope finalized 2026-02-13):

- `docs/stories/story-5.2.md` — Full scope including Form Builder Init API, component catalog, single payload
- `docs/stories/story-context-5.2.xml` — Context file for ralf-sm decomposition (directive: ralf-sm creates full task breakdown; database first)
- `docs/tasks/5.2/TASK-PLAN.md` — Draft; ralf-sm will create/replace during Phase 2 decomposition
- `docs/tasks/5.2/T00-*.md`, `T06-*.md` — Design-reference specs; ralf-sm uses as input, creates own task specs

**Optional:** If SM updates are needed, use:

```markdown
@sm.mdc Please create/update Story 5.2 artifacts. Story file and context file exist at docs/stories/story-5.2.md and docs/stories/story-context-5.2.xml. Add or refine STORY-5.2-UAT-TEST-GUIDE.md if needed. Scope is finalized per docs/stories/STORY-5.2-FORM-BUILDER-INIT-API.md and docs/stories/COMPONENT-CATALOG-SCHEMA-DESIGN.md.
```

---

## 📋 Phase 2: Story Decomposition (Ralf-SM - Main Chat)

**⚠️ CRITICAL — Worktree / Branch requirement (2026-02-13):**

Decomposition outputs (`TASK-PLAN.md`, `Txx-*.md`, `STATUS.md`, `LESSONS-LEARNED.md`) **must** be created in the **Story worktree** on the **Story branch**. If Ralf-SM runs in the main repo on `master` or another branch (e.g. `chore/lint-resolution`), task worktrees created from the story branch will **not** see the task specs.

**Before invoking Ralf-SM:**
1. Open the Story worktree in Cursor (e.g. `C:\wt\elp\story-epic5-5.2-company-form-defaults`).
2. Confirm branch: `git branch --show-current` → Story branch (e.g. `story/epic5-5.2-company-form-defaults`).
3. Run `@ralf-sm *decompose-story` in that window.
4. Commit and push the decomposition from the Story worktree **before** creating task branches/worktrees.

**If decomposition was written to the wrong branch:** Copy the `docs/tasks/<story>/` files to the Story worktree, remove any obsolete task specs, `git add`, commit, push. Do **not** merge from the wrong branch into story (it mixes unrelated changes).

---

### Story 5.1 Prompt (`@ralf-sm`)

```markdown
@ralf-sm

*decompose-story

Git discipline (mandatory):
- **Run in the Story worktree** with Story branch checked out. Do NOT run in main repo on master/chore branches — task worktrees would miss the specs.
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

### Story 5.2 Prompt (`@ralf-sm`)

```markdown
@ralf-sm

*decompose-story

Git discipline (mandatory):
- **Run in the Story worktree** (e.g. C:\wt\elp\story-epic5-5.2-company-form-defaults) with Story branch checked out. Do NOT run in main repo on master/chore branches — task worktrees would miss the specs.
- Confirm the active Story branch exists and is pushed (do not work on `master`).
- Each task MUST be implemented on a `task/5.2/Txx-<slug>` branch with a PR into the Story branch.
- Follow: `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`

Inputs:
- Story ID: 5.2
- Story file: `docs/stories/story-5.2.md`
- Context file: `docs/stories/story-context-5.2.xml`
- References:
  - `docs/prd.md`
  - `docs/stories/EPIC-5-STATUS.md`
  - `docs/stories/STORY-5.2-DATA-SCHEMA.md`
  - `docs/stories/COMPONENT-CATALOG-SCHEMA-DESIGN.md`
  - `docs/stories/STORY-5.2-FORM-BUILDER-INIT-API.md`

**Critical:** Ralf-SM creates the full task breakdown from the story and context. Do NOT feel constrained by any pre-existing TASK-PLAN or task specs. The context file defines: (1) database task must be first (schema + seeds for defaults + component catalog), (2) reference docs describe approved design — use them to inform tasks but you decide structure, granularity, and dependencies.

Output requirements:
1. Create `docs/tasks/5.2/TASK-PLAN.md` from scratch (your decomposition)
2. Create full task specs for each task in your plan (first task = database). Use naming: `T{id}-{slug}.md` (e.g. T03-form-builder-init-api.md).
3. Initialize `docs/tasks/5.2/LESSONS-LEARNED.md` if missing
4. Create/update `docs/tasks/5.2/STATUS.md` (current task = your first task — database)

**Task doc naming:** All task docs follow `T{id}-{slug}.{type}.md` (see Phase 3 "Task document naming").
```

---

## ✅ Phase 3: Task Execution Cycle

### Task document naming (mandatory)

Task-related docs MUST use the pattern `T{id}-{slug}.{type}.md`:

| Document | Filename pattern | Example |
|----------|------------------|---------|
| Spec | `T{id}-{slug}.md` | `T02-defaults-api-crud-merge-resolver.md` |
| UAT checklist | `T{id}-{slug}.uat.md` | `T02-defaults-api-crud-merge-resolver.uat.md` |
| UAT results | `T{id}-{slug}.uat-results.md` | `T02-defaults-api-crud-merge-resolver.uat-results.md` |
| Retro | `T{id}-{slug}.retro.md` | `T02-defaults-api-crud-merge-resolver.retro.md` |

**Do not use:** `T02-uat-results.md`, `T02.retro.md`, or any variant missing the task slug.

---

Use the hardened task cycle (worktrees + PR base checks + UAT + retro + push discipline) from:
- `docs/stories/EPIC-3-WORKFLOW-GUIDE_UPDATED.md` (Phase 3 section)

### Task kickoff (after worktree creation) — MANDATORY

After running `new-task.ps1` to create the task branch and worktree, **before** starting implementation or creating the PR:

1. **Open the task worktree** in Cursor (e.g. `C:\wt\elp\task-5.1-T07-data-url-guard-and-cleanup`).

2. **Update the task spec** to In Progress:
   - Edit `docs/tasks/<story>/<Txx>-<slug>.md`
   - Set `**Status:**` from `⏸️ Pending` to `🔄 In Progress`

3. **Update STATUS.md**:
   - Edit `docs/tasks/<story>/STATUS.md`
   - Set `**Current Task:**` to `Txx (<task-title>)`

4. **Commit + push** these doc updates:
   ```powershell
   git add docs/tasks/<story>/<Txx>-<slug>.md docs/tasks/<story>/STATUS.md
   git commit -m "docs: Txx kickoff - status In Progress"
   git push origin task/<story>/<Txx>-<slug>
   ```

5. **Create the PR** (GitHub requires at least one commit):
   ```powershell
   gh pr create --base "story/epic5-5.1-background-asset-management" --head "task/5.1/<Txx>-<slug>" --title "<StoryId>: <Txx> - <slug>" --body "Implements <Txx> for story <StoryId>. See docs/tasks/<StoryId>/ for completion + UAT."
   ```
   Or re-run: `./scripts/git/new-task.ps1 ... -CreateWorktree -CreatePR` (idempotent; will create PR when commits exist).

**Why:** The PR cannot be created with zero commits. Updating status creates the first commit; the PR then has a meaningful base for the implementation diff.

### Single-prompt full cycle (T05 learning – recommended)

After T05, the agent stopped after retro without attempting UAT, closeout commit, or merge. Use this **single prompt** to run the full Phase 3 cycle in one go:

```markdown
@ralf-dev

*run-task

**FULL CYCLE (do not stop until complete):** Implement → Automated verification → UAT attempt → Retro → Commit all → Push → Merge PR.

Scope + ACs are pre-approved; proceed end-to-end without waiting for interactive confirmations.

Task Spec: docs/tasks/<story>/<TaskBase>.md

**Mandatory steps (in order):**
1. Implement per task spec.
2. Automated verification: run lint/build/tests for touched areas; record evidence in completion note.
3. UAT: Open `${TaskBase}.uat.md` (e.g. T05-shared-resolver-parity.uat.md). For each step:
   - If automatable (e.g. file existence check, API call, DevTools/browser automation): execute it and record result.
   - If manual-only: record "Human verification: [step] – not executed by agent."
   - Create/update `${TaskBase}.uat-results.md` with PASS/FAIL and evidence.
4. Retro: Run @ralf-retro *run-retro (or equivalent); update `${TaskBase}.retro.md` and LESSONS-LEARNED.md.
5. Commit: Run `git status`. Commit implementation first (feat(Txx): ...), then closeout (docs: completion, uat-results, retro, Txx-*.md status, TASK-PLAN.md, STATUS.md). Push.
6. Merge: In the task worktree, run `gh pr merge --squash` (merges the PR for the current branch). If merge fails (e.g. "review required"), output the exact command for the human to run.

**Rules:** PR must target Story branch. Before closeout: working tree clean (implementation committed). Cap long build output.
```

**Example (T05):**
```markdown
Task Spec: docs/tasks/5.1/T05-shared-resolver-parity.md
```
*(Replace with your task's spec path.)*

**Caveat:** If the task spec explicitly requires **human UAT** (e.g. DB migration, high-risk UI flow), complete through step 5 (push), then output: "Human: execute `${TaskBase}.uat.md`, then run `gh pr merge --squash` to merge."

### Epic 5 automation deltas (reduce human steps)

- Add a **pre-UAT automated verification step**:
  - Before the human runs UAT, the dev agent must run **all relevant automated checks** it can (based on touched areas) and write evidence.
  - The human then reviews evidence and decides what to **retest manually** or what the agent couldn’t test.
  - Evidence must include:
    - Commands run (and working directory)
    - Pass/fail summary
    - What could not be run (and why)
    - Any follow-up manual checks recommended
  - **Prompt snippet (paste into each task’s `@ralf-dev *run-task` message):**

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
    - `npm run lint`
    - `npm run build`
  - Backend (if touched):
    - `python -m pytest` (if tests exist/configured)
    - else minimum: `python -m compileall backend`
```
- Prefer **agent-owned** Git actions:
  - Create branches/worktrees with `./scripts/git/new-task.ps1 ... -CreateWorktree -WorktreeRoot "C:\wt\elp"`
  - **After worktree creation:** Update task spec Status to In Progress + STATUS.md; commit + push; then create PR (or re-run with `-CreatePR`). See "Task kickoff" section above.
  - Fix PR base via `gh pr edit ... --base <story-branch>` if needed
  - Commit + push after retro output files are created (so PR always updates)
- Prefer **agent-owned integrator merges** (Task PR → Story) after human UAT is ✅ PASS.
- Keep humans for:
  - UAT execution
  - DB migration execution (if any)

### Commit discipline (T04 learning – mandatory)

After T04, the closeout sometimes committed only **docs** (UAT/retro/status) and left **implementation** uncommitted, so the merged PR did not contain the code.

**Rules for the dev agent:**

1. **Implementation commits first.** Before creating the closeout commit (UAT passed, retro, HumanDone):
   - Run `git status` in the task worktree.
   - If any implementation files (backend/ or frontend/ code, or new task-specific files) are modified or untracked, commit them in one or more commits with a clear message (e.g. `feat(T04): ... implementation`). Do not rely on a single "closeout" commit to carry code.
2. **Closeout commit = docs only.** The final commit that updates status/retro/UAT docs should not be the only commit containing code. If the working tree had code changes, they must already be committed.
3. **Verify before push.** Before `git push` and "Merge PR": run `git status` again. Working tree should be clean (or only intentionally untracked, e.g. `backend/storage/`). If not, commit remaining changes and then push.

**Asset storage + worktrees (T08 learning):** Asset files live in directories excluded from git (e.g. `backend/storage/`). Each worktree has its own working tree; untracked files from one worktree are not present in another. For UAT requiring real background images: run from the story worktree where assets were uploaded, or re-upload a test image in the current worktree before verifying display.
4. **Build/lint output.** Long `npm run build` or similar output can crash sessions. Prefer: run from the task worktree, cap output (e.g. PowerShell `Select-Object -First 100`), or redirect to a file and report pass/fail + first/last lines only.

**Prompt snippet to add to task run instructions (optional but recommended):**

```markdown
Before closeout: run `git status`. If implementation files are uncommitted, commit them first (feat(Txx): ...), then create the closeout commit (docs only). Push only when working tree is clean.
```

### Scope boundary (T04 learning)

If the task spec says "Frontend-only" (or similar) but backend changes become necessary during implementation:
- Document the scope expansion in the completion note (why backend was touched).
- Ensure both frontend and backend changes are committed; do not leave backend changes uncommitted because the spec said "frontend-only."

### Story branch sync with master (2026-02-09 learning – recommended)

When `master` receives significant merges **after** the Story branch was created (e.g. lint-resolution, other stories), merge `master` into the Story branch **early** rather than at the end.

**Why:** A Story branch created before (e.g.) lint fixes will diverge from master. Merging Story → master at closeout then surfaces many conflicts. Resolving them early keeps the story branch up to date and makes the final merge trivial.

**When:** After a substantial merge to master (chore/lint-resolution, another story PR), or when starting a new task if the story branch is behind.

**How:**
```powershell
# In the Story worktree
git fetch origin master
git merge origin/master
# Resolve conflicts; keep both lint fixes from master and story changes
git push origin <story-branch>
```

---

*Epic 5 Workflow Guide - created for Epic 5 cycle start*  
*Last Updated: 2026-02-13*

---

## 📓 Workflow Change Log (Epic 5)

| Date | Change | Why |
|------|--------|-----|
| 2026-02-07 | Added “Workflow Evolution Goal” + Human/AI responsibilities + Epic kickoff + automation deltas | Start Epic 5 with a streamlined, agent-owned loop and iteratively remove unnecessary human steps |
| 2026-02-07 | Inserted “pre-UAT automated verification” requirement (dev agent runs what it can; human reviews evidence and retests selectively) | Reduce manual retesting time and make UAT focus on what automation can’t cover |
| 2026-02-10 | Added "Commit discipline (T04 learning)" and "Scope boundary (T04 learning)" under Phase 3 | T04 closeout committed only docs; implementation was left uncommitted. Rules: implementation commits first, closeout = docs only, verify clean tree before push; cap build/lint output to avoid session crashes; document scope expansion if backend touched despite frontend-only spec |
| 2026-02-09 | Added "Story branch sync with master" (merge master into story branch early when master has parallel work) | Story 5.1 was branched before lint-resolution merged to master; merging master in early avoided painful conflict resolution at closeout |
| 2026-02-11 | Added "Single-prompt full cycle" (implement → UAT attempt → retro → commit → push → merge in one prompt) | T05: agent stopped after retro; no UAT attempt, no closeout commit, no merge. One prompt now mandates the full cycle |
| 2026-02-13 | Added "Task kickoff" (after worktree: update task spec to In Progress, STATUS.md, commit+push, then create PR) | T07: PR creation was skipped (0 commits). Status update creates first commit so PR can be created before implementation |
| 2026-02-13 | Added "CRITICAL — Worktree/Branch requirement" for Phase 2 (Ralf-SM decomposition) | Ralf-SM ran in main repo on chore branch; decomposition was not on story branch; task worktrees lacked specs. Fix: run decomposition in Story worktree, commit there before creating task branches |
| 2026-02-16 | Added "Single-Session Story Workflow" (Story 5.3 validated) | Story 5.3 delivered in one chat without Ralf decomposition. Backend-heavy stories with clear DCs can use single-session prompt; human runs migrations, manual UAT, retro, merge. See STORY-5.3-RETRO, docs/tasks/5.3/LESSONS-LEARNED |

