# Epic 6 Workflow Guide — BMAD Method (No Ralf)

**Workflow:** BMAD method only. **SM** prepares Story artifacts, **runs `./scripts/git/new-story.ps1`**, creates the **Git worktree**, opens the **Draft PR**, and hands the path to Dev; Dev implements via the single-session prompt. No Ralf decomposition or task cycle.

**Current Focus:** Story 6.x redesign planning - AI generation architecture rethink (post-6.3 closeout)  
**Story 6.2.1 Status:** ✅ Complete (merged 2026-03-30, PR #54)  
**Story 6.2.2 Status:** ✅ Complete (merged 2026-03-31, PR #55)  
**Story 6.3 Status:** 🟨 **Closed (learning capture)** — implementation + diagnostics complete, but human UAT quality was not satisfactory; redesign required (see `STORY-6.3-CLOSEOUT-REPORT.md`)  

---

## ⚡ Epic 6 Story Workflow (BMAD)

This is the streamlined workflow established at the end of Epic 5.

| Step | Actor | Action |
|------|-------|--------|
| 0 | **Human** | **`git fetch origin`**, **`git pull origin master`** in main repo; confirm prior story merged on GitHub; note or remove stale worktrees (see **Pre-next-story sync**). You **do not** run `new-story.ps1` in the normal flow. |
| 1 | **@bmad-agent-bmm-pm** | Approves scope; signs off `docs/stories/story-6.x.md` (may be drafted by SM first — align in chat). |
| 2 | **@bmad-agent-bmm-sm** | Produces the story pack: `story-context-6.x.xml`, `STORY-6.x-UAT-TEST-GUIDE.md`, `STORY-6.x-SINGLE-SESSION-DEV-PROMPT.md`, and any templates (`STORY-6.x-BENCHMARK-BASELINE.md`, etc.); finalizes `story-6.x.md` wording with PM as needed. |
| 3 | **@bmad-agent-bmm-sm** | **Runs `./scripts/git/new-story.ps1`** via the **Shell** tool (`-CreateWorktree`, `-DraftPR`, `-Epic`, `-Story`, `-Slug`, `-WorktreeRoot` per machine, e.g. `$env:ELP_WORKTREE_ROOT = "C:\wt\elp"`). Confirms worktree path + branch + PR URL in chat and updates the dev prompt with **exact** paths. |
| 4 | **Human** | **Open the SM-created worktree** in Cursor (e.g. **File → Open Folder** → `C:\wt\elp\story-epic6-...`). Point **@bmad-agent-bmm-dev** at that window so all edits land on the story branch. |
| 5 | **@bmad-agent-bmm-dev** | Implements in the **worktree** only. Runs `pytest` & `npm test`. Pushes to the story branch (Draft PR already exists). |
| 6 | **Human** | Manual UAT per `STORY-6.x-UAT-TEST-GUIDE.md`; **merge story PR via GitHub** (preferred) or `gh pr merge`; then run **Story closeout checklist** below |

**Artifacts:** `story-6.x.md`, `story-context-6.x.xml`, `STORY-6.x-UAT-TEST-GUIDE.md`, `STORY-6.x-SINGLE-SESSION-DEV-PROMPT.md`

Optional parity: `STORY-6.x-CLOSEOUT-REPORT.md` (recommended for cross-cutting or release-grade stories).

---

## 📋 Story closeout checklist (Dev + Human — before marking **Complete**)

Use this to avoid stale roadmap/workflow docs and wrong PR numbers (common gap pattern).

| # | Check | Owner |
|---|--------|-------|
| 1 | `docs/stories/story-6.x.md` — **Status** Complete, **Completed** date, **PR #** matches the **story’s** GitHub PR (do not confuse with another row in `EPIC-6-STATUS.md`, e.g. 6.2 vs 6.2.2). | Dev |
| 2 | `docs/stories/EPIC-6-STATUS.md` — story row **Complete** + **correct PR #** + one-line scope note if deferred work moved. | Dev |
| 3 | **`docs/stories/EPIC-6-WORKFLOW-GUIDE.md` (this file)** — **Current Focus** = **next** story; completed story lines show ✅ + merge date/PR; **no** “in progress / blocked” for a story already on `master`. | Dev |
| 4 | `STORY-6.x-GATE-EVIDENCE.md` — **full** `python -m pytest --tb=short` summary line recorded **when policy requires it**; if only focused tests are run locally, state that explicitly and point to **CI** or follow-up full run so reviewers know. | Dev |
| 5 | Remove stray artifacts (`downloaded.bin`, `temp*.txt`, scratch logs) — **never commit**. | Dev |
| 6 | Optional: `STORY-6.x-CLOSEOUT-REPORT.md` for audit trail (esp. merges with deferrals like “UX → Epic 8”). | Dev |

**Merge discipline:** Prefer **merge via GitHub** (or `gh pr merge`) so the PR shows **merged** and history matches `master`. Local fast-forward-only merges without updating the PR confuse “is PR #N closed?” checks.

---

## 🔄 Pre-next-story sync (Human + SM — mandatory before `new-story.ps1`)

**Purpose:** `master` must match **`origin/master`** before the **SM agent** runs **`new-story.ps1`** (the script branches from local `master`).

**Human** — from **main repo** (`EventLeadPlatform` checkout, not a story worktree):

```powershell
git fetch origin
git switch master
git pull origin master
gh pr list --state open
```

Then:

- **Optional:** `git worktree list` — remove or retire old story worktrees per `AGENTIC-GIT-WORKTREE-WORKFLOW.md`.
- Tell **`@bmad-agent-bmm-sm`** that sync is done (or SM runs **fetch/pull** via Shell on wrap-up).

**SM agent** — after a green base:

- Run **`./scripts/git/new-story.ps1 ... -CreateWorktree -DraftPR`** (Human does not run this in the normal Epic 6 loop).
- If the script fails (permissions, path length, `gh` auth), SM diagnoses; Human assists with environment fixes only.

**@bmad-agent-bmm-sm** on “prepare next story” / Phase 0: sync **or** confirm with Human, **then** run `new-story.ps1`.

Agents taking a “wrap-up” or “start next story” task should run the same **fetch + pull** (or ask Human to confirm) before SM runs `new-story.ps1`.

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
To prevent technical debt accumulation and AI Hallucinations regarding test status, the Dev agent is strictly bound by the Green CI/CD Rule:
1. Before creating the final closeout commit, the Dev agent **MUST** run:
   - Frontend: `npm run lint` and `npm run test:unit -- --watch=false`
   - Backend: `python -m pytest --tb=short` (**full** suite unless risk is negligible—if only a **focused** file ran locally, say so in `STORY-X.X-GATE-EVIDENCE.md` and ensure CI or Human confirms full green)
2. **ANTI-HALLUCINATION PROTOCOL:** The agent MUST read the exact output of the test run. If the test process times out, hangs, or the output is truncated before showing the final `=== X passed, Y failed ===` summary, the agent MUST treat the test as **FAILED**.
3. The agent is **NOT** allowed to end its turn or close the story until all tests demonstrably pass and **0** linting errors/warnings remain in the touched files.
4. If the test suites or linters fail, the Dev agent must fix them as part of the story implementation loop before asking the human for help.

---

## 🧰 Workflow Automation Toolkit (Mandatory for Epic 6+)

Use the workflow scripts to reduce repetitive agent overhead and keep evidence consistent:

1. **Preflight** (worktree + branch + DB resolution parity):
   - `.\scripts\workflow\preflight-story.ps1 -ExpectedWorktreePath "C:\wt\elp\<story-worktree>" -ExpectedBranch "story/epicX-X.X-<slug>" -ReportFile "docs/stories/STORY-X.X-PREFLIGHT.md"`
2. **Green gate execution** (anti-truncation summary enforcement):
   - `.\scripts\workflow\run-green-gate.ps1 -StoryId "X.X" -FocusedTestCommand "python -m pytest tests/test_story_x_x.py --tb=short" -BackendGateCommand "python -m pytest --tb=short" -EvidenceFile "docs/stories/STORY-X.X-GATE-EVIDENCE.md"`
3. **Evidence sync** (append gate evidence into UAT results):
   - `.\scripts\workflow\generate-story-evidence.ps1 -StoryId "X.X" -GateEvidenceFile "docs/stories/STORY-X.X-GATE-EVIDENCE.md" -UatResultsFile "docs/stories/STORY-X.X-UAT-RESULTS.md"`
4. **Tool feedback capture** (continuous process improvement):
   - `.\scripts\workflow\collect-tool-feedback.ps1 -StoryId "X.X" -ToolName "run-green-gate.ps1" -Rating 4 -Feedback "What worked and what should improve"`

---

## 🗄️ Database Connection Consistency Rule (Mandatory)

To prevent test/runtime drift:

1. All backend code paths that connect to the DB must resolve connection settings from a common source.
2. Test harness DB resolution must align with runtime DB resolution (no independent fallback logic that diverges).
3. During preflight, always capture both:
   - `os.getenv("DATABASE_URL")`
   - runtime-resolved DB URL from `common.database`.
4. Any mismatch that changes selected DB backend (for example SQL Server vs SQLite) must be treated as a gate-risk and corrected before closeout.

---

## 🚀 Epic Kickoff (Start Here)

The Epic 6 kickoff path leverages the newly updated **BMAD v6** commands (`@bmad-agent-bmm-sm.md`, etc.).

- Phase 0: Agentic Story bootstrap (branch/worktree + Draft PR) for 6.1
- Phase 1: Story artifacts (SM prepares Story, context, UAT)
- Phase 2: Dev single-session implementation

### 📋 Phase 0 & 1: Agentic Setup (SM owns `new-story.ps1` + worktree)

**Pattern:** Human pulls **`master`**; **`@bmad-agent-bmm-sm`** prepares artifacts on **`master`** (or a short-lived docs PR if policy requires), then **runs `new-story.ps1` from the main repo** so the story branch and worktree are created **before** Dev starts.

**Example prompt — Story 6.3 (current):**

```markdown
@bmad-agent-bmm-sm.md After Human has `git pull origin master`, please:
1. Confirm story pack exists: `docs/stories/story-6.3.md`, `story-context-6.3.xml`, `STORY-6.3-UAT-TEST-GUIDE.md`, `STORY-6.3-SINGLE-SESSION-DEV-PROMPT.md`.
2. Use Shell to run (adjust WorktreeRoot if needed):
   `./scripts/git/new-story.ps1 -Epic 6 -Story "6.3" -Slug "ai-context-benchmark-baseline" -CreateWorktree -DraftPR`
   (If you use ELP_WORKTREE_ROOT, the script picks it up; otherwise pass `-WorktreeRoot "C:\wt\elp"`.)
3. Paste the worktree path, branch name, and Draft PR URL into chat; update `STORY-6.3-SINGLE-SESSION-DEV-PROMPT.md` Step 0 preflight paths if they differ from the template.
4. Tell Human to open that folder in Cursor for `@bmad-agent-bmm-dev`.
```

**Historical example — Story 6.1:**

```markdown
@bmad-agent-bmm-sm.md Orchestrate Phase 0–1 for Story 6.1. After Human syncs `master`, run:
`./scripts/git/new-story.ps1 -Epic 6 -Story "6.1" -Slug "ai-foundation-static-validator" -CreateWorktree -DraftPR`
then ensure `story-6.1.md`, `story-context-6.1.xml`, `STORY-6.1-UAT-TEST-GUIDE.md`, `STORY-6.1-SINGLE-SESSION-DEV-PROMPT.md` are ready and dev prompt paths match the created worktree.
```

---

## ✅ Phase 2: Dev Single-Session Implementation (Execution Contract)

**Owner:** `@bmad-agent-bmm-dev`  
**Goal:** Implement the full story in one execution loop without weakening quality gates.

### Required run order (before requesting human UAT)
1. Run preflight script and resolve any failures:
   - `.\scripts\workflow\preflight-story.ps1 ...`
2. Implement story scope only (respect in-scope/out-of-scope from `story-6.x.md`).
3. Run Green CI/CD via toolkit script:
   - `.\scripts\workflow\run-green-gate.ps1 ...`
4. If any check fails, fix and re-run until fully green.
5. Produce story evidence artifacts using toolkit script:
   - `.\scripts\workflow\generate-story-evidence.ps1 ...`
6. Commit and push only when checks are demonstrably green.

### Why this gate is strict
Epic 6 adopts TEA-informed quality enforcement because high error volume was previously normalized and important failures were ignored over time. Current TEA baseline is **94/100**, and this workflow preserves that baseline by requiring green verification at the end of **every** story.

---

## 📦 Story Evidence Contract (Mandatory Before Human UAT)

Before the human runs manual UAT, the Dev agent must provide all of the following in the story PR comment or closeout note:

1. Commands run (exact command and working directory).
2. Final test/lint summaries copied from terminal output.
3. Pass/fail table for frontend and backend checks.
4. List of checks not run (if any) with explicit reason.
5. Suggested manual-only checks for the human UAT pass.

If summaries are missing, truncated, or non-final, the story is treated as **NOT READY FOR UAT**.

---

## 🧪 Phase 3: Human UAT + Merge Gate

**Owner:** Human  
**Goal:** Validate behavior the agent cannot fully validate and enforce release quality.

### Required checklist
1. Run manual UAT from `STORY-6.x-UAT-TEST-GUIDE.md`.
2. Verify the Dev agent evidence package is complete and consistent with PR changes.
3. Confirm no unresolved P0/P1 defects remain.
4. Merge Story PR only when:
   - Green CI/CD evidence is complete,
   - Manual UAT passes,
   - Scope boundaries are preserved.

---

## 🔄 Phase 4: Story Closeout + Next Story Reset

**Owner:** `@bmad-agent-bmm-pm` or `@bmad-agent-bmm-sm`  
**Goal:** Keep epic flow deterministic after each story merge.

### Required closeout actions
1. Update story completion status in `docs/stories/EPIC-6-STATUS.md`.
2. Record lessons/process adjustments in this workflow changelog section.
3. In main repo, confirm PR merged and run `git pull origin master`.
4. Confirm next story focus; **`@bmad-agent-bmm-sm`** prepares the next story pack **and** runs **`new-story.ps1`** for the next worktree (Human opens the folder for Dev).
5. Record developer-agent feedback on script/tool usage:
   - `.\scripts\workflow\collect-tool-feedback.ps1 ...`

---

## 🚨 Failure Routing Policy (Green Gate Protection)

If Green CI/CD does not pass after reasonable fix attempts:

1. Stop broad implementation.
2. Classify issue:
   - **Defect in current story scope** -> continue in same story until fixed.
   - **Cross-cutting debt/blocker** -> create a micro-fix follow-up story and link it.
3. Do not claim story complete with unresolved gate failures.
4. Escalate to TEA review when failures indicate systemic test instability or unclear assertions.

---

## ☁️ Cloud Co-Developer Worktree Model (Epic 6)

Epic 6 supports adding a second developer agent (cloud) while preserving branch hygiene.

### Operating model
1. One active implementation owner per story branch.
2. If cloud agent is used in parallel:
   - use a separate branch/worktree for cloud work,
   - open a PR into the active story branch,
   - integrate only after Green CI/CD evidence is provided.
3. Never have two agents pushing directly to the same branch concurrently.

### Recommended usage pattern
- Local dev agent: primary story implementation and stabilization.
- Cloud dev agent: bounded sub-problem (refactor slice, isolated test fix, analysis spike).
- Integrate cloud contribution through PR review into story branch, then rerun full Green CI/CD.

This preserves your learning objective (multi-agent experience) without weakening release controls.

---

## 📒 Workflow Changelog (Epic 6)

| Date | Change | Why |
|------|--------|-----|
| 2026-02-26 | Added explicit Phase 2 execution contract, Phase 3 human merge gate, and Phase 4 reset process | Epic 6 was latest but not final; needed closeout and reset mechanics to avoid drift |
| 2026-02-26 | Added Story Evidence Contract tied to Green CI/CD output quality | Prevent false-green/hallucinated completion and preserve per-story quality gate |
| 2026-02-26 | Added Failure Routing Policy with TEA escalation path | Ensure failing gates are routed deterministically instead of deferred silently |
| 2026-02-26 | Added Cloud Co-Developer Worktree Model | Enable second developer agent usage while maintaining branch integrity and quality control |
| 2026-02-26 | Added workflow automation scripts + mandatory tool feedback logging | Reduce repetitive agent effort and create continuous improvement loop |
| 2026-02-26 | Added database connection consistency rule for test/runtime parity | Prevent recurring SQL backend drift between app runtime and pytest harness |
| 2026-03-31 | Clarified **SM owns `new-story.ps1` + worktree + Draft PR**; Human syncs `master` and opens worktree for Dev | Match practiced flow; Human was not expected to run the script in normal Epic 6 loop |
| 2026-04-02 | Story 6.3 closed as learning capture (not release-ready); next focus shifted to architecture redesign planning | Preserve learnings and avoid forcing incremental tuning on a foundation that needs redesign |
