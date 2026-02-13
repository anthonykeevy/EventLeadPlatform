# Epic 5 Workflow Guide — Changelog

**Scope policy:** This workflow is **Epic 5 specific** and **not shared** outside Epic 5.

This file tracks **incremental process changes** (workflow evolution), so we can study history and avoid fixing the same thing repeatedly.

**Current process (authoritative):** `docs/stories/EPIC-5-WORKFLOW-GUIDE.md`

---

## How to add an entry

Add a new section with:
- **Trigger** (what pain/confusion happened)
- **Change** (what we changed in the workflow)
- **Why** (expected impact)
- **Follow-ups** (what to revisit later)
- **Evidence** (optional: transcript/doc pointers)

---

## 2026-02-07 — Epic 5 workflow baseline

- **Trigger:** Epic 5 kickoff needed a repeatable Git + agent workflow.
- **Change:**
  - Established Epic 5 workflow guide structure and roles (Human vs AI).
  - Defined the core Epic kickoff phases (Story bootstrap → artifacts → decomposition → task loop).
- **Why:** Start Epic 5 with a clear, agent-owned loop and reduce ad-hoc work.
- **Follow-ups:** Iterate after first real task execution.

---

## 2026-02-09 — Removed cross-epic dependency (Epic 3) and made Epic 5 self-contained

- **Trigger:** Workflow drift/confusion caused by referencing Epic 3 workflow.
- **Change:**
  - Replaced Epic 3 references with the full explicit Epic 5 task execution loop inside the Epic 5 guide.
  - Added “Epic 5 specific / not shared” policy.
- **Why:** Prevent cross-epic drift and keep the process readable from one document.
- **Follow-ups:** Keep Epic 5 workflow improvements isolated to Epic 5.

---

## 2026-02-09 — T01 learnings: reduce confirmations, correct build context, standardize filenames, and prevent duplicate artifacts

- **Trigger:** During Task T01:
  - Dev flow asked the human to re-confirm already-approved task scope/ACs.
  - Build verification was attempted from the wrong directory (repo root vs `frontend/`), causing misleading “no build script” feedback.
  - Task artifacts were auto-generated with generic names (`T01.uat.md`, `T01.completion.md`), creating merge/duplication risk.
- **Change:**
  - **Approval rule:** Task spec is the approval artifact; dev proceeds end-to-end without re-confirm prompts.
  - **Build rule:** Frontend checks run from `frontend/` inside the correct worktree.
  - **Artifact naming rule:** Task artifacts must be renamed to `${TaskBase}.*` before commit/merge.
  - **Baseline-broken rule:** If repo baseline build/typecheck is already failing, record baseline evidence and run scoped verification; don’t claim a regression without proof.
- **Why:** Reduce human friction, avoid duplicated task artifacts, and ensure evidence is accurate/repeatable.
- **Follow-ups:** After frontend build stabilization, add a reliable scoped typecheck command for builder contract changes.
- **Evidence:** Task T01 transcript under `docs/Transcripts/` in the T01 task worktree / story branch.

---

## 2026-02-09 — Workflow updates live on the Story branch (not task branches)

- **Trigger:** Updating workflow docs inside task branches creates avoidable conflicts and “extra” commits every task.
- **Change:**
  - Workflow guide + workflow changelog are maintained and committed **only on the Story branch** (as a dedicated story-level commit when needed).
  - Task PRs should not include workflow doc edits.
- **Why:** Keep task PRs focused and reduce merge churn.
- **Follow-ups:** If a workflow change is required mid-task, record the note and apply the doc update after the task is merged (story-level commit).

---

## 2026-02-09 — T02 learnings: DB migration sequencing across worktrees, PR bootstrap, and non-interactive retro

- **Trigger:** During Task T02 (DB migration):
  - Migration was first executed from the wrong checkout (`OneDrive\Projects\EventLeadPlatform`) instead of the task worktree, so tables weren’t created where expected.
  - Local DB had already been upgraded to KB revision `037`, but the task worktree (branched from the Story) did not contain the KB migration chain (`036/037`), causing Alembic “missing revision” failures.
  - Retro flow asked for “continue?” confirmations at every step, creating friction and encouraging premature conclusions (“Alembic issue” vs “workflow timing issue”).
- **Change:**
  - **PR bootstrap commit (mandatory):** update task spec status → commit/push → create PR (so PR exists before real work).
  - **DB migration sequencing:** never run `alembic upgrade head` until the migration files exist in the *current task worktree* and the worktree contains the full revision chain already applied to the DB.
  - **Preflight check:** verify DB `alembic_version.version_num` exists as a migration file in the current worktree before attempting upgrades.
  - **Retro automation:** use `#yolo` mode for BMAD workflows to avoid per-step confirmations; add a PM sanity-check step to correct misattributed root causes.
- **Why:** Prevent cross-worktree migration drift, reduce Alembic dead-ends, keep PRs visible early, and make retro fast + accurate.
- **Follow-ups:**
  - Add an automated preflight script to compare DB head vs migration files (optional future task).
  - Ensure KB migration PR(s) are merged into the shared trunk before upgrading DB environments (so new worktrees don’t miss applied revisions).
- **Evidence:** T02 transcript: `docs/Transcripts/cursor_epic_5_story_5_1_task_t02.md`

---

## 2026-02-09 — T03 learnings: tracker closeout + scriptable PR bootstrap (cost/efficiency)

- **Trigger:** Task T03 completed successfully end-to-end in one prompt, but:
  - Total token usage was high (process overhead + tool friction is expensive at scale).
  - Story trackers drifted (e.g., task completed/merged but `STATUS.md` didn’t reflect it).
  - PR bootstrap is a repeatable mechanical step that should be scriptable.
- **Change:**
  - **Tracker closeout step:** make tracker updates an explicit mandatory post-merge step (task spec + `TASK-PLAN.md` + `STATUS.md` + next task readiness).
  - **Git automation:** update `scripts/git/new-task.ps1` to support `-BootstrapPR` so PRs can be created immediately without manual micro-steps.
  - **Commit guidance:** accept 2–4 commits when isolating artifacts keeps reviews clean.
- **Why:** Reduce “workflow tax” tokens, prevent tracker drift, and make PR creation a one-command operation.
- **Follow-ups:**
  - Consider adding a lightweight “tracker consistency check” (fails if task spec / task plan / status disagree).
  - Add a short “browser automation smoke steps” template for UI-heavy tasks (T04+).
- **Evidence:** T03 transcript: `docs/Transcripts/cursor_epic_5_story_5_1_task_t03.md`

