# Epic 5 Workflow Guide — BMAD Method (No Ralf)

**Workflow:** BMAD method only. SM agent prepares Story, context, and UAT; SM reviews artifacts; Dev agent builds via single-session prompt. No Ralf decomposition or task cycle.

**Current Focus:** Story 5.8 - Admin Review & Publish + Activation (Epic 5)  
**Story 5.1–5.5 Status:** ✅ Complete — Merged to master  
**Story 5.6 Status:** ✅ Complete (2026-02-17) — Publish Request Workflow  
**Story 5.7 Status:** ✅ Complete (2026-02-18) — Company Settings Hub  
**Story 5.8 Status:** ⏳ Ready — Context and UAT created; SM review pending  

---

## ⚡ Epic 5 Story Workflow (BMAD — Validated Stories 5.3–5.7)

**When:** All Epic 5 stories now use this path. No Ralf decomposition.

| Step | Human | Agent |
|------|-------|-------|
| 1 | PM approves scope; PM decisions doc finalized | — |
| 2 | — | **@sm** prepares Story, context (XML), UAT guide; SM reviews and suggests improvements |
| 3 | Run `new-story.ps1`; open Story worktree in Cursor | — |
| 4 | Create STORY-5.x-SINGLE-SESSION-DEV-PROMPT.md (copy from 5.7/5.8 template, adapt scope) | — |
| 5 | Paste Dev prompt into new chat | **@dev** implements full story; runs automated checks; records evidence |
| 6 | Run migration (`alembic upgrade head`) if migration created | — |
| 7 | Manual UAT per STORY-5.x-UAT-TEST-GUIDE.md; verify evidence | — |
| 8 | Merge Story PR to master | — |
| 9 | (Optional) Retro; update EPIC-5-WORKFLOW-GUIDE | — |

**Artifacts:** `story-5.x.md`, `story-context-5.x.xml`, `STORY-5.x-UAT-TEST-GUIDE.md`, `STORY-5.x-PM-DECISIONS.md`, `STORY-5.x-SINGLE-SESSION-DEV-PROMPT.md`

---

## 🔧 Git + PR Discipline (Mandatory)

This workflow follows the platform-wide Git rules in:
- `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`

**Rules:**
- **Never work directly on `master`.**
- **One Draft PR per Story** (opened immediately) → `master`
- **Implementation on Story branch** — no task branches; Dev works directly on story branch
- **Push daily:** no multi-day local-only changes

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
- Phase 1 Story artifacts (SM prepares Story, context, UAT — SM reviews and suggests)
- Phase 2 Dev single-session prompt (copy STORY-5.x-SINGLE-SESSION-DEV-PROMPT.md; paste into new chat with @dev)
- Phase 3 Human: migrations, UAT, merge PR

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
- Ready for Dev single-session prompt (no Ralf decomposition)
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

## 📋 Phase 1: Story 5.8 — SM Review (Current)

Story 5.8 artifacts are **ready** (PM approved 2026-02-18):

- `docs/stories/story-5.8.md` — Admin Review & Publish + Activation
- `docs/stories/story-context-5.8.xml` — Context for Dev
- `docs/stories/STORY-5.8-UAT-TEST-GUIDE.md` — UAT coverage
- `docs/stories/STORY-5.8-PM-DECISIONS.md` — PM decisions

**SM review complete:** See `docs/stories/STORY-5.8-SM-REVIEW-SUGGESTIONS.md` for suggestions. Incorporate as needed; then create STORY-5.8-SINGLE-SESSION-DEV-PROMPT.md and hand off to @dev.

---

## 📋 Phase 2: Dev Single-Session Prompt (No Ralf)

**Epic 5 uses BMAD method only.** No Ralf decomposition or task cycle. Dev implements the full story in one session.

**Steps:**
1. Create `docs/stories/STORY-5.x-SINGLE-SESSION-DEV-PROMPT.md` — copy from `STORY-5.7-SINGLE-SESSION-DEV-PROMPT.md` or `STORY-5.8` template, adapt scope.
2. Open Story worktree in Cursor (e.g. `C:\wt\elp\story-epic5-5.8-...`).
3. Paste the Dev prompt into a **new chat** with @dev.
4. Dev implements, runs checks, records evidence. Human runs migrations; manual UAT; merge PR.

**Template:** See `docs/stories/STORY-5.7-SINGLE-SESSION-DEV-PROMPT.md` for structure. Story 5.8 prompt to be created after SM review.

---

### Story 5.8 Dev Prompt (create after SM review)

Copy structure from `docs/stories/STORY-5.7-SINGLE-SESSION-DEV-PROMPT.md`. Adapt for Story 5.8 scope (approval options, unpublish modes, activation windows, hide approval UI). Paste into new chat with @dev.

---

## ✅ Phase 3: Human Follow-up (Migrations, UAT, Merge)

After @dev implements the story:

| Step | Human action |
|------|--------------|
| 1 | Run `alembic upgrade head` if migration created (agents prepare; human executes) |
| 2 | Run manual UAT per STORY-5.x-UAT-TEST-GUIDE.md; verify evidence in STORY-5.x-UAT-RESULTS.md |
| 3 | Merge Story PR to master |
| 4 | (Optional) Retro; update EPIC-5-WORKFLOW-GUIDE |

### Dev commit discipline (single-session)

The Dev prompt (STORY-5.7-SINGLE-SESSION-DEV-PROMPT.md) instructs @dev: implementation commits first; closeout (UAT results, docs) in separate commit; verify clean tree before push.

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
*Last Updated: 2026-02-18*

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
| 2026-02-16 | Stories 5.3, 5.4, 5.5 complete; focus → 5.6 | All single-session stories merged to master. Next: Publish Request Workflow |
| 2026-02-18 | **BMAD method only; no Ralf** | Stories 5.6, 5.7 delivered via SM prepare/review + Dev single-session prompt. Ralf decomposition and task cycle removed. SM prepares Story, context, UAT; SM reviews; Dev builds in one session. Create STORY-5.x-SINGLE-SESSION-DEV-PROMPT; paste into @dev. |

