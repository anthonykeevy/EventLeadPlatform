# Epic 6 Workflow Guide — BMAD Method (No Ralf)

**Workflow:** BMAD method only. **SM** prepares Story artifacts, **runs `./scripts/git/new-story.ps1`**, creates the **Git worktree**, opens the **Draft PR**, and hands the path to Dev; Dev implements via the single-session prompt. No Ralf decomposition or task cycle.

**Current Focus:** Story 6.4.5 — **Component Property Cheat Sheet H3** (after Story 6.4.4.2 measured/no-change ablation).
**Story 6.2.1 Status:** ✅ Complete (merged 2026-03-30, PR #54)  
**Story 6.2.2 Status:** ✅ Complete (merged 2026-03-31, PR #55)  
**Story 6.3 Status:** ✅ **Closed (Learning)** — closed after UAT findings; see `STORY-6.3-CLOSEOUT-REPORT.md` (2026-04-15)  
**Story 6.3.1 Status:** ✅ **Complete** (merged 2026-04-15, PR #64) — deterministic compiler + governance foundation; UAT rounds 1–11 PASS. See `STORY-6.3.1-CLOSEOUT-REPORT.md`.  
**Story 6.4 Status:** ✅ **Complete** (PR #66, UAT Rounds 1–3 PASS 2026-04-24; merge date to land via parity-check post-merge) — User Preferences architecture foundation + AI Agent panel polish; 19 ACs, 4 migrations. See `STORY-6.4-CLOSEOUT-REPORT.md`.  
**Story 6.4.3a Status:** ✅ **Complete** (merged 2026-04-25, PR #68) — eval harness bones, `log.FormAiEvalRun`, and full 10-row live baseline. See `STORY-6.4.3a-CLOSEOUT-REPORT.md`.  
**Story 6.4.2 Status:** ✅ **Complete** (2026-04-25, PR #69) — capability snapshot prompt cleanup, parity audit, `FormSemanticPlan` ADR, active prompt tests, and post-cleanup baseline. See `STORY-6.4.2-CLOSEOUT-REPORT.md`.  
**Story 6.4.3b Status:** ✅ **Complete** (2026-04-25, PR #70) — eval judge package generator, rubric v1, DB-backed judge ingest, and Cursor judge workflow.  
**Story 6.4.3c Status:** ✅ **Complete** (2026-04-25, PR #71) — eval diff reports, Welch/Fisher statistics, and 6.4.4 handoff docs.  
**Story 6.4.4 Status:** ✅ **Complete** (merged 2026-04-27, PR #72) — H1/H2/H4 prompt shrink sweeps; combined H1+H2+H4 evidence fed Story 6.4.4.1 locale registry work.
**Story 6.4.4.1 Status:** ✅ **Complete** (merged 2026-04-27, PR #75) — locale registry wiring, audience locale/brand posture API pass-through, prompts-v1.1/rubric_v2 judge bump. Company Settings brand posture UI deferred to `g-6441-company-brand-settings-ui`.
**Story 6.4.4.1-ac10 Status:** ✅ **Complete** (merged 2026-04-27, PR #77) — AC-10 baseline re-judge passed; next recommended story is 6.4.4.2.
**Story 6.4.4.2 Status:** ✅ **Review / measured no-change** (PR #79) — H2-only and H4-only ablations completed under `rubric_v2`; both failed the ship bar, so current `master` behavior remains unchanged.

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
| 6 | **Human + SM** | Manual UAT per `STORY-6.x-UAT-TEST-GUIDE.md`; SM performs the **pre-merge stale-field audit** below; **merge story PR via GitHub** only after sign-off; then SM performs the **post-merge reset** before opening the next story. |

**Artifacts:** `story-6.x.md`, `story-context-6.x.xml`, `STORY-6.x-UAT-TEST-GUIDE.md`, `STORY-6.x-SINGLE-SESSION-DEV-PROMPT.md`

**`STORY-6.x-CLOSEOUT-REPORT.md` is MANDATORY** when a story (a) introduces or modifies a **public API surface** — defined as: a new or changed HTTP endpoint, a new or changed Pydantic schema returned to clients, or a new or changed exported TypeScript type/interface in `frontend/src/.../types/*` consumed across feature boundaries — (b) ships ≥1 schema migration, or (c) defers in-scope work to a future story. Otherwise optional but strongly recommended (see Story 6.3.1 closeout report for the canonical template — TL;DR, AC matrix, architecture sketch, "what this unlocks", carry-forward backlog, risks, green gates, hygiene, decision).

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
| 6 | `STORY-6.x-CLOSEOUT-REPORT.md` present per the mandatory criteria above (API change / migration / deferred scope); otherwise optional but recommended for audit trail. | Dev |
| 7 | **Date-stamp parity** — Both **`Completed`** in `story-6.x.md` and the merge date in `EPIC-6-STATUS.md` must equal the GitHub **`mergedAt`** date (UTC) for the story PR. Confirm via `gh pr view <N> --json mergedAt,state` before stamping. If "dev complete" and "merged" dates differ, record both explicitly (e.g. *Dev complete: 2026-04-15 / Merged: 2026-04-23 (PR #64)*) — never quietly use the dev-complete date as the merge date. | Dev |
| 8 | **Worktree retired** — After PR merge confirmed and any local artefacts harvested, prune the merged worktree: `git worktree remove "<path>"`. Keeps `git worktree list` clean and avoids stale-DB-pointing IDE windows from previous stories. | Dev / Human |

**Merge discipline:** Prefer **merge via GitHub** (or `gh pr merge`) so the PR shows **merged** and history matches `master`. Local fast-forward-only merges without updating the PR confuse “is PR #N closed?” checks.

### SM stale-field audit (mandatory before merge)

Before merge sign-off, SM must run an explicit stale-field pass against the story branch and fix any misses in a final housekeeping commit:

1. `gh pr view <N> --json state,isDraft,mergedAt,headRefName,baseRefName,url` — verify the PR number and target branch.
2. `rg -n "Draft|Ready for UAT|Ready for UAT/SM review|Keep PR .* open|Current Focus" docs/stories/story-6.x.md docs/stories/STORY-6.x-CLOSEOUT-REPORT.md docs/stories/EPIC-6-STATUS.md docs/stories/EPIC-6-WORKFLOW-GUIDE.md` — every hit must be intentional for the current phase.
3. Confirm `story-6.x.md`, `STORY-6.x-CLOSEOUT-REPORT.md`, `EPIC-6-STATUS.md`, and this guide agree on: status, PR number, next focus, and carry-forward items.
4. Confirm mandatory evidence artifacts exist for the story type (baseline, capability audit, rubric ADR, hypothesis evidence, canvas contract, etc.).
5. Only after the stale-field pass is clean should SM say "merge-ready".

### SM post-merge reset (mandatory before next story)

After the PR is merged and before running `new-story.ps1` for the next story:

1. Pull `master` in the main checkout.
2. Re-run `gh pr view <N> --json state,mergedAt,mergeCommit,url` and stamp the UTC merge date into story/status docs if the merge date differs from dev-complete date.
3. Re-run the stale-field scan above on `master`. If stale fields remain, fix them on the next story branch before Dev starts implementation.
4. Attempt `git worktree remove "<merged-story-path>"`. If Windows denies deletion, record the path and retry after any IDE/terminal handles are closed.
5. Only then prepare the next story pack and open the next Draft PR.

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

- **Strongly recommended:** Run `git worktree list` and `git worktree remove "<merged-story-path>"` for any **merged** story worktrees before SM runs `new-story.ps1` for the next story (see closeout checklist row 8). This prevents stale IDE windows pointing at deleted branches and keeps the worktree root tidy. Retain only worktrees whose PR is still open or in active triage. See `AGENTIC-GIT-WORKTREE-WORKFLOW.md` for the full retirement procedure.
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

### 🧬 Capability Snapshot Rule (AI Form Generation)

Established post Story 6.3.1 (migrations 056 → 057 round-trip):

1. When a story adds an AI capability that depends on a frontend `ComponentRegistry` renderer (e.g. via `ComponentCapabilitySnapshot`), the **matching renderer must already exist on `master`** before the capability migration is applied in CI/UAT environments.
2. If a capability slips through without a renderer, ship an **immediate follow-up migration to drop it** in the same story (canonical example: migration `057_story_631_form_ai_capability_drop_last_name.py` cleaned up `056`).
3. Do **not** close a story with an active capability snapshot whose target renderer is missing — the LLM will silently substitute (e.g. `radio` for `rating`) and silently regress UAT prompts in the next story.
4. Capability snapshot version (`FORM_AI_CAPABILITY_POLICY:vN`) must be referenced in `STORY-6.x-GATE-EVIDENCE.md` whenever a story adds or removes capabilities.

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

## 🔁 Multi-Round UAT Protocol (recommended for tuning-heavy stories)

Established post Story 6.3.1 (which executed 11 UAT rounds with one-variable-at-a-time tuning). When a story is expected to need **more than two** UAT rounds (typical for AI generation, layout solver, or prompt-tuning work), Dev should adopt this protocol from **Round 1**:

1. Open `STORY-6.x-UAT-RESULTS.md` early with two tables:
   - **§9 Final result** — section-by-section pass/fail (updated after each round, never overwritten between rounds).
   - **Round-by-round summary (chronological)** — one row per round capturing: focus, **single variable changed**, `RequestID` chain (per `docs/AGENT-LOGGING-GUIDE.md`), outcome (Pass / Partial / Fail / Pass-with-caveat), follow-up.
2. **One meaningful variable per round.** Prompt section, policy flag, layout rule, validation contract, capability snapshot — change only one so causality is measurable. If two variables must move together, document the coupling rationale in the round row.
3. Each round's `RequestID` (and `generationRunId` when relevant) must be referenced in the round row so the run is replayable via the story's replay tooling.
4. Carry-forward items discovered during rounds go into the round row **and** are mirrored to the `STORY-6.x-CLOSEOUT-REPORT.md` carry-forward backlog at closeout.

**Canonical example:** `STORY-6.3.1-UAT-RESULTS.md` (11 rounds, single-variable per round, full RequestID lineage).

---

## 🧪 Phase 3: Human UAT + Merge Gate

**Owner:** Human  
**Goal:** Validate behavior the agent cannot fully validate and enforce release quality.

### Required checklist
1. Run manual UAT from `STORY-6.x-UAT-TEST-GUIDE.md`.
2. Verify the Dev agent evidence package is complete and consistent with PR changes.
3. Confirm no unresolved P0/P1 defects remain.
4. **SM closeout audit (mandatory pre-merge gate)** — before clicking Merge, ask `@bmad-agent-bmm-sm` to run the closeout audit. SM walks the closeout checklist (rows 1–6) against the story branch, confirms `STORY-6.x-CLOSEOUT-REPORT.md` reflects reality, lands a final SM **housekeeping commit** if any of rows 1–3 (story status field, `EPIC-6-STATUS.md` row, this guide's Current Focus) need updating, merges any new carry-forward items into `EPIC-6-CARRY-FORWARD-BACKLOG.md`, and gives the explicit "merge-ready" sign-off. *Added 2026-04-24 after Story 6.4 closeout exposed that Dev consistently misses housekeeping rows when fully focused on UAT pass + closeout report.*
5. Merge Story PR only when:
   - Green CI/CD evidence is complete,
   - Manual UAT passes,
   - Scope boundaries are preserved,
   - SM closeout audit signed off.
6. **Post-merge (rows 7–8 of closeout checklist):** SM verifies date-stamp parity (story `Completed:` ↔ `EPIC-6-STATUS.md` ↔ `gh pr view --json mergedAt`) and prunes the worktree (`git worktree remove "<path>"`).

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
| 2026-04-15 | Story 6.3.1 complete (PR #64). Architectural shift: **AI emits semantic intent only**, deterministic Python compiler owns geometry, render-then-measure provides ground-truth heights, governance tables (capability/validation/width/prompt) make every run replayable. Carry-forward follow-ups (`g-frontend-submit-parity`, `g4b-second-pass-rows`, `g-doc`, `g-backlog-dropdown-font`) tracked into Story 6.4 backlog. | Establish the foundation Story 6.4 (AI iteration on existing designs) was waiting on; next SM cycle starts on this baseline. |
| 2026-04-23 | Post-6.3.1 SM review. Workflow improvements: **(1)** Closeout checklist rows 7–8 added (date-stamp parity vs `gh pr view --json mergedAt`; mandatory worktree retirement). **(2)** `STORY-6.x-CLOSEOUT-REPORT.md` upgraded from "optional" to **mandatory** when API surface changes / migrations ship / scope is deferred (with "public API surface" defined inline). **(3)** New **Multi-Round UAT Protocol** section codifying single-variable-per-round + RequestID lineage (canonical example: `STORY-6.3.1-UAT-RESULTS.md`). **(4)** New **Capability Snapshot Rule** under DB Consistency (renderer must exist before capability migration; immediate drop-migration if it slips). | 6.3.1 closeout exposed three drift patterns (date stamps, stale worktrees, capability/renderer skew) the team had to discover the hard way; fold lessons into the guide before opening the next story so the next cycle inherits them. |
| 2026-04-23 | **Epic 6 scope pivot (PM/SM joint review)**. Story 6.4 originally framed as "AI Iteration on Existing Designs" was **deferred post-MVP** after PM analysis: iteration is a high-risk novel capability whose value-vs-effort doesn't justify shipping in MVP. Replacement: **Story 6.4 = AI Agent Panel Production Polish** (XS-S, ships clean) and **new Story 6.5 = Image-to-Form** (M, key differentiator: snap a screenshot of an existing form, get a working form). Image-to-form leverages the 6.3.1 deterministic-compiler architecture unchanged — only the input transport (multimodal LLM) is new. Billing stories renumbered to 6.6–6.10. See `EPIC-6-STATUS.md` for the updated roadmap. | After 6.3 + 6.3.1 cost ~3 weeks of architecture discovery, the team needs a fast clean shipment to rebuild momentum. Iteration would have repeated the discovery pattern; image-to-form is well-trodden multimodal territory with a much sharper user value proposition (one-screenshot conversion from competing tools). Aligns with Tonyk's *"AI gets you 80%, builder tools get the last 20%"* differentiator. |
| 2026-04-23 | **Story 6.4 in-flight scope expansion (Tonyk decision)**. Polish work needed a place to store "don't show again" preferences. Discussion evolved from `localStorage` → `User` JSON column → **net-new `UserPreference` architecture** mirroring `config.AppSetting`. Story 6.4 expanded from XS-S to M-L (4 migrations, 19 ACs, 3 new tables, new `/api/me/preferences` surface, dynamic Notifications UI). Tonyk explicitly chose the foundational path over the tactical shortcut so all future per-user toggles can ship via DB seed alone. | Doing the foundation work once at the right moment (when the first real consumer needed it) is far cheaper than retrofitting a `User` JSON column under three downstream consumers. The pattern is now established for billing email prefs, theme keys, image-handling defaults (6.5), etc. |
| 2026-04-24 | **Story 6.4 closed Complete (PR #66 merge-ready).** Closeout audit by SM caught 3 housekeeping gaps (story status field, `EPIC-6-STATUS.md` row, workflow guide Current Focus) and one outstanding PR-#65 commitment (`EPIC-6-CARRY-FORWARD-BACKLOG.md` had never been created). All 4 fixed in a final SM housekeeping commit before the merge gate. **Lesson:** the closeout-checklist housekeeping rows (1–3) are owned by Dev but consistently get missed because Dev's focus is on UAT pass + closeout report. **New rule:** the SM closeout audit (this exact pass) is now an explicit gate before the human merges any story PR — added as workflow step in §⚡ Epic 6 Story Workflow. | Trust the process: a 5-minute audit catches what a tired Dev forgets at end-of-story. Better to surface the gap pre-merge than to chase reconciliation drift later (cf. 2026-04-23 row 1 about date-stamp parity, which exists for the same reason). |
| 2026-04-25 | **Story 6.4.3a merged (PR #68), but stale closeout fields survived the merge.** `story-6.4.3a.md` still said "Ready for UAT/SM review" and PR "Draft"; closeout still said "Keep PR #68 open"; `EPIC-6-STATUS.md` and this guide still pointed to the older 6.5 flow. Added explicit SM stale-field audit and post-merge reset sections with exact `gh pr view` + `rg` checks before the next story opens. | Convert a repeated human-memory step into a checklist with observable commands. The next round should fail visibly before merge if story/status/current-focus fields drift. |
