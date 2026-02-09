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
- **Evidence:** Task T01 transcript under `docs/Transcript/` in the T01 task worktree / story branch.

---

## 2026-02-09 — Workflow updates live on the Story branch (not task branches)

- **Trigger:** Updating workflow docs inside task branches creates avoidable conflicts and “extra” commits every task.
- **Change:**
  - Workflow guide + workflow changelog are maintained and committed **only on the Story branch** (as a dedicated story-level commit when needed).
  - Task PRs should not include workflow doc edits.
- **Why:** Keep task PRs focused and reduce merge churn.
- **Follow-ups:** If a workflow change is required mid-task, record the note and apply the doc update after the task is merged (story-level commit).

