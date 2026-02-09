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

## ✅ Phase 3: Task Execution Cycle

Use the hardened task cycle (worktrees + PR base checks + UAT + retro + push discipline) from:
- `docs/stories/EPIC-3-WORKFLOW-GUIDE_UPDATED.md` (Phase 3 section)

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
  - Create branches/worktrees/PRs with `./scripts/git/new-task.ps1 ... -CreateWorktree -CreatePR`
  - Fix PR base via `gh pr edit ... --base <story-branch>` if needed
  - Commit + push after retro output files are created (so PR always updates)
- Prefer **agent-owned integrator merges** (Task PR → Story) after human UAT is ✅ PASS.
- Keep humans for:
  - UAT execution
  - DB migration execution (if any)

---

*Epic 5 Workflow Guide - created for Epic 5 cycle start*  
*Last Updated: 2026-02-07*

---

## 📓 Workflow Change Log (Epic 5)

| Date | Change | Why |
|------|--------|-----|
| 2026-02-07 | Added “Workflow Evolution Goal” + Human/AI responsibilities + Epic kickoff + automation deltas | Start Epic 5 with a streamlined, agent-owned loop and iteratively remove unnecessary human steps |
| 2026-02-07 | Inserted “pre-UAT automated verification” requirement (dev agent runs what it can; human reviews evidence and retests selectively) | Reduce manual retesting time and make UAT focus on what automation can’t cover |

