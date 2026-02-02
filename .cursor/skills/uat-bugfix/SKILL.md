---
name: uat-bugfix
description: Runs an end-to-end UAT bugfix loop (intake → evidence → fix task spec → git branch/PR → implement → verify → UAT checklist → record results → retro/lessons). Use when a UAT step fails, a regression is found, or the user asks to fix a bug discovered during UAT.
disable-model-invocation: true
---

# UAT Bugfix (End-to-End Task Loop)

## Purpose
Turn any UAT failure into **tracked work** that is **committed, pushed, and mergeable**, with clear evidence and a deterministic retest path.

This skill is designed to work with BMAD/Ralf artifacts, but it can run standalone.

Authoritative Git workflow:
- `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`

---

## Roles (how this skill expects to operate)
- **Anthony (human):** UAT gate. Executes UAT checklist steps and reports pass/fail + notes.
- **Agent:** implementation + verification + documentation. Creates branches/PRs, updates task artifacts, and prepares the next UAT checklist.

**Logging guidance:** `docs/AGENT-LOGGING-GUIDE.md` is for the agent. The agent may ask the human to download/attach evidence (e.g. Dev Logs JSON) but should not require the human to read the guide.

---

## Intake (ask only what’s missing)
Collect:
- **Story ID** (e.g. `3.8`, `3.9`) and whether this is a combined UAT cycle
- **Failing UAT step(s)**: paste the exact step text (or section) from the UAT guide
- **Expected vs actual**
- **Repro steps** (minimum viable)
- **Scope**: `frontend` | `backend` | `mixed`
- **Constraints** (forbidden zones, must-not-change files, performance, backwards compatibility)
- **Branch context**:
  - Story/UAT integration branch name (e.g. `story/epic3-3.8-3.9-uat-completion`)
  - Whether a Story/UAT Draft PR to `master` already exists

If the user can’t provide everything, proceed with best-effort evidence capture first.

---

## Rules (non-negotiable)
- **No work on `master`**: create or switch to the correct branch before implementing.
- **Push daily**: no multi-day local-only work.
- **One defect per task** where possible (small blast radius).
- **Evidence-first**: baseline evidence before changing code.
- **No secrets**: never paste credentials/tokens; redact if encountered.
- **Never run Alembic commands** (upgrade/downgrade/revision/history/current). Provide commands for the human to run.

---

## Workflow (execute in order)

### 1) Confirm classification (defect vs enhancement)
Using the story acceptance criteria / UAT guide:
- **DEFECT**: violates an explicit expected behavior
- **ENHANCEMENT / OUT OF SCOPE**: desirable improvement not required by ACs

Only defects proceed as UAT bugfix tasks. Enhancements get routed to backlog.

### 2) Capture baseline evidence (fast + cheap)
Depending on scope:
- **Frontend/UI**:
  - Agent uses `docs/AGENT-LOGGING-GUIDE.md` (Dev Logs bundle + snapshot evidence)
  - Prefer: ask the human to download and attach the **Dev Logs JSON** rather than pasting huge logs into chat
  - Capture: screenshot + console errors + key event logs (if builder/resize)
- **Backend/API/auth**:
  - Run: `python backend/enhanced_diagnostic_logs.py --limit 20`
  - Save output to a file if large; quote only key excerpts

### 3) Create (or append) a fix task spec in `docs/tasks/<story-id>/`
If `docs/tasks/<story-id>/TASK-PLAN.md` exists:
- Create the next `Txx-<slug>.md` fix task (small, testable)
- Update `TASK-PLAN.md` to include it

If it does not exist:
- Create:
  - `docs/tasks/<story-id>/TASK-PLAN.md` (minimal skeleton)
  - `docs/tasks/<story-id>/T01-<slug>.md` (detailed fix task)

Task spec must include:
- Scope In / Scope Out / Forbidden zones
- Acceptance criteria (binary, observable)
- Required verification (commands + manual checks)

### 4) Git setup (branch + PR)
Create a task branch off the Story/UAT branch:
- Branch: `task/<story-id>/<Txx>-<slug>`
- PR: task branch → Story/UAT branch

Preferred: use `scripts/git/new-task.ps1`.
If `gh` is not installed, instruct the user to create the PR via GitHub UI.

### 5) Implement minimal fix + verify
Implement the smallest change that satisfies the failing UAT step(s).

Verification requirements:
- Run the most relevant automated checks for the touched area(s)
- Re-run the same evidence capture that demonstrated the failure

### 6) Write completion note + generate UAT checklist
Create:
- `docs/tasks/<story-id>/<Txx>-<slug>.completion.md`
- `docs/tasks/<story-id>/<Txx>-<slug>.uat.md`

### 7) Human UAT (gate)
Ask the user to run the checklist and return results.

### 8) Record UAT results + retro + finalize
On PASS:
- Create `docs/tasks/<story-id>/<Txx>-<slug>.uat-results.md`
- Update `TASK-PLAN.md` status
- Add short retro notes (or run the Ralf retro flow) and update lessons/memory if applicable
- Ensure the task branch is pushed and PR is ready to merge

On FAIL:
- Extract defects clearly
- Create a new fix task (or refine the existing one if the scope stays identical)

---

## Escalation (when to switch to `bug-session`)
Switch to the `bug-session` skill when:
- 2+ failed fix attempts, or repeated regressions
- Non-deterministic repro (timing/layout measurement)
- Cross-cutting issue (frontend + backend + state persistence)
- High severity (data loss, auth/security)

