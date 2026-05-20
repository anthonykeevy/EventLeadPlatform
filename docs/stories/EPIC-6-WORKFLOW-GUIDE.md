# Epic 6 Workflow Guide — BMAD Method (No Ralf)

**Workflow:** BMAD method only. **SM** prepares Story artifacts, **runs `./scripts/git/new-story.ps1`**, creates the **Git worktree**, opens the **Draft PR** *(now targeting `develop`)*, and hands the path to Dev; Dev implements via the single-session prompt. No Ralf decomposition or task cycle.

**🚀 Environment Promotion (adopted 2026-05-19):** Worktree (Dev) → `develop` (Azure Test slot, auto-deploy) → `master` (Production, future via Story 6.11). See **§ Environment Promotion Workflow** below for the full rules. **Story PRs now target `develop`, not `master`.**

**Current Focus (updated 2026-05-20 — Story 6.5b Complete):** **(1)** **Story 6.5c — Capability Catalog Cutover** (Up next; depends on 6.5b — `resolve_allowed_components` becomes authoritative for Blocks A/F/I + toolbox; `ref.BrandPosture` replaces enum; reconciles registry table naming `PromptAssemblyRegistry` ↔ architecture's `PromptAssemblyProfile`). **(3)** **Story 6.5d — Clarification Data Plane** (Pending; the original 6.5a content — three `ref.*` tables + Block E + dropdowns + `AudienceLocale` enum elimination — now plugs into the registry from 6.5b). **(4)** Targeted AU production-context eval verification (pending Tony's eval slice). **(5)** **Story 6.11 — Production Environment + CI/CD** — blueprint approved (see § Production Deployment Blueprint below); scheduled post-6.10 so production opens with billing live.
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
**Story 6.4.4.2 Status:** ✅ **Complete** (merged 2026-04-28, PR #79) — H2-only and H4-only ablations completed under `rubric_v2`; both failed the ship bar, so current `master` behavior remains unchanged.
**Story 6.4.5 Status:** ✅ **Measured/no-change** (merged 2026-04-29, PR #81) — H3 measured against AC10 `rubric_v2` baseline; no-go as-is due material `field_label_f1` regression and locale/context-conflict noise. Prompt changes reverted; evidence preserved.
**Story 6.4.6 Status:** ✅ **Complete** (merged 2026-04-30, PR #82) — AU-only diagnostic eval framework, current-state AU baseline, judge ingest, and `AU-000` handoff complete; no candidate prompt improvements in this story.
**Story 6.4.7 Status:** ✅ **Complete** (merged 2026-05-06, PR #84) — Analyst-owned AU-001 through AU-006 loop complete; AU-005 is the strongest behavioural target, AU-006 supplies lint-clean wording lessons for the follow-up production prompt implementation story.
**Story 6.4.8 Status:** ✅ **Complete** (merged 2026-05-07, PR #85) — AU-005 behaviour promoted via migration 072 (PR #86 added downgrade review note). Next step: targeted AU eval verification before resuming 6.5a / image-to-form path.
**Story 6.5a Status:** ✅ **Closed (Architecture Phase)** (2026-05-20) — data model (`decision-6.5a-clarification-options-data-model.md`) + prompt-assembly registry (`prompt-assembly-registry-architecture.md`) approved; implementation decomposed into 6.5b / 6.5c / 6.5d. PR #87 closed-as-superseded; merged via PR #103.
**Story 6.5b Status:** ✅ **Complete** (2026-05-20, PR #104 merged to `develop`) — Prompt Assembly Registry foundation; **R6 closed** on Azure Test. Evidence: `STORY-6.5b-UAT-RESULTS.md`, `STORY-6.5b-PROMPT-EQUIVALENCE-DIFF.md` (AC-19 PASS, Tony sign-off).
**Story 6.11 Status:** ⏳ **Scheduled** (post-6.10) — Production Environment + CI/CD + Manual Approval Gate. Scope per `docs/architecture/azure-infrastructure-architecture.md` §4 + §7. Sequenced last so production opens with billing live (6.6–6.10).
**Test Environment Status:** ✅ **Live** since 2026-05-14 — Azure App Service test slot `signalplatforms-test`, `develop` branch auto-deploys via `.github/workflows/deploy-to-test.yml`. ACS Email + ODBC URL translator + SPA-from-FastAPI + Alembic-on-startup all validated. **29 commits** (PRs #92–#96 + direct fixes) currently exist only on `develop` and must back-merge to `master` via the one-time reconciliation release PR.

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

**Rules (updated 2026-05-19 for Environment Promotion):**
- **Never work directly on `master`** or `develop`.
- **One Draft PR per Story** (opened immediately) → **`develop`** *(was `master`; flipped 2026-05-19 — see Environment Promotion Workflow below)*
- **Bugfix PRs** also target **`develop`**. The only branch that may target `master` is `develop` itself, via a **release PR**.
- **Release PRs** (`develop` → `master`) are **SM-drafted, Tony-approved**, opened after per-story QA in the Azure Test environment passes.
- **Implementation on Story branch** — no task branches.
- **Push daily:** no multi-day local-only changes.

---

## 🚀 Environment Promotion Workflow (Worktree → Test → Production)

**Adopted:** 2026-05-19. **Mandatory for all stories from this point forward.**

Epic 6 now runs against three environments with explicit promotion gates. This replaces the previous "story PR → master" model, which left Azure-specific bugs (port binding, ODBC URL format, missing deps, broken email) undetected until they hit a real deployment.

### Environment map

| Environment | Branch | Deploy target | Auto-deploy? | Trigger |
|------|--------|---------------|--------------|---------|
| **Dev** | `story/epicX-X.X-slug` (worktree) | Local dev (your machine) | Manual | Dev agent runs the app locally |
| **Test** | `develop` | Azure App Service test slot (`signalplatforms-test`) | ✅ Yes | Push to `develop` → `.github/workflows/deploy-to-test.yml` |
| **Production** | `master` | Azure App Service production (provisioned by Story 6.11) | 🔜 After Story 6.11 | Push to `master` → `deploy-to-prod.yml` with manual-approval gate on the `production` GitHub Environment |

### Promotion flow

```mermaid
flowchart LR
    A["Worktree<br/>story/epicX-X.X-slug<br/>(Dev)"] -->|Story PR| B["develop<br/>(Test slot, Azure)"]
    B -->|Auto-deploy via<br/>deploy-to-test.yml| T[("Test environment<br/>signalplatforms-test")]
    T -->|QA passes UAT<br/>against TEST URL| C["Release PR<br/>develop --> master"]
    C -->|Tony approves| D["master<br/>(Prod, future)"]
    D -.->|After Story 6.11:<br/>deploy-to-prod.yml<br/>(manual approval gate)| P[("Production environment")]
```

### Where QA fits (per-story cadence, decided 2026-05-19)

| Phase | Where | Who | What is validated |
|---|---|---|---|
| Dev | Worktree (local) | Dev agent | Green CI/CD (unit + integration tests + lint) per existing §🛑 Green CI/CD Rule |
| Story PR → develop | GitHub | SM + Dev | Branch hygiene, evidence package, scope correctness |
| Auto-deploy | Azure Test slot | GitHub Actions | Build + deploy success (no manual step) |
| **🆕 QA in Test (per-story)** | `https://signalplatforms-test.azurewebsites.net` (or the test custom domain when configured) | **Tony + SM** | Run `STORY-6.x-UAT-TEST-GUIDE.md` against the **deployed** Test environment. This is the **only place** we catch deployment-only bugs: env vars, secrets, real ACS email delivery, real Azure SQL, CSP/headers, custom domain TLS, cold-start, real OAuth callbacks. |
| Release PR `develop` → `master` | GitHub | SM (drafts) → Tony (approves) | Confirms QA-pass evidence; promotes the merged-and-tested code to the production branch |
| Prod deploy (future, Story 6.11+) | Azure prod | GitHub Actions + manual approval gate | Final cutover with rollback runbook |

### Release PR procedure (SM-owned)

1. **After per-story QA passes** in the Test environment:
   - Confirm `gh pr view <story-PR-N> --json mergedAt` shows the story PR is merged into `develop`.
   - Confirm the Test deploy workflow run for that merge is green: `gh run list --workflow=deploy-to-test.yml --branch develop --limit 5`.
   - Confirm `STORY-6.x-UAT-RESULTS.md` records the QA pass against the **Test URL** (not local dev).
2. **Open the release PR** (Draft):
   ```powershell
   gh pr create --draft --base master --head develop `
     --title "release: <stories bundled> via Test environment QA" `
     --body "<release notes — see template below>"
   ```
3. **Release PR body must include:**
   - Bundled stories with PR numbers and one-line scope each.
   - Link to each `STORY-6.x-UAT-RESULTS.md` confirming QA pass against Test.
   - New migrations / new Python or npm deps / changed env vars (for Production preflight).
   - Any one-off scripts environments downstream must run (e.g., when a prior migration was modified retroactively).
   - Rollback plan: previous master SHA tag (`pre-release-YYYY-MM-DD`).
4. **SM tags master before merge:** `git tag pre-release-YYYY-MM-DD && git push origin pre-release-YYYY-MM-DD` — known-good rollback point.
5. **Tony approves and merges via GitHub UI** (preserves audit trail). Master is now caught up. From Story 6.11 onwards, this triggers production deploy.
6. **Post-merge sync:** SM runs `git fetch origin` in every active worktree and `git switch develop && git pull` on the main checkout so Dev work continues from the latest base. Master and develop should be identical at this moment.

### Hotfix exception (rare)

If a critical production bug needs to bypass Test (e.g., security CVE, P0 outage):
1. Branch from `master`: `git switch -c bugfix/<date>-<slug>`.
2. PR → `master` directly with the `-BaseBranch master` override on `new-story.ps1` (or `gh pr create --base master`).
3. **Immediately cherry-pick or back-merge into `develop`** to prevent re-divergence: `git switch develop; git cherry-pick <commit>; git push`.
4. Document the bypass reason in the bugfix PR body. Hotfixes should be exceptional, not routine — if you find yourself hotfixing weekly, the QA process needs revisiting.

### Production Deployment Blueprint (Story 6.11)

**Status:** ⏳ Blueprint only. Implementation scheduled post-6.10 so production opens with billing live. This subsection captures the design so the Story 6.11 implementer (Tony + Dev) starts with a finished architecture and can spend the cycle on plumbing, not decisions. Authoritative reference is `EPIC-6-STATUS.md` row 6.11.

#### Design goals

1. **Zero-downtime deploys** via slot-swap (not in-place overwrite — the Test slot's restart-during-deploy pattern is acceptable for Test but not for paying customers).
2. **Mandatory manual approval** before any code touches live traffic.
3. **Same smoke gate as Test** (PR #99 pattern), extended with **feature-readiness probes** that run against the deployed slot before the swap.
4. **<5 min rollback** via slot re-swap (Azure keeps the previous code on the now-idle slot).
5. **Auditable trail per release**: GitHub Environments + Azure Activity Log + Application Insights deployment markers.

#### Infrastructure to provision

Refer to `docs/architecture/azure-infrastructure-architecture.md` §4 (resource topology) + §7 (CI/CD pipeline). Net-new resources for Story 6.11:

- App Service Plan + Web App `signalplatforms-prod` (P1V3 minimum for prod traffic and slot swap support)
- **Two deployment slots** under `signalplatforms-prod`: default `production` (serves live traffic) + `staging` (deploy target)
- Azure SQL DB `EventLeadPlatformProd` on a separate logical server (isolates prod backups, perf, and blast radius from Test)
- Key Vault `kv-eventlead-prod` with App Service managed identity granted `get` on secrets
- ACS Email verified sender domain `signalplatforms.com.au` with prod-grade MailFrom configured
- Application Insights bound to both slots (separate connection strings)
- Custom domain `app.signalplatforms.io` bound to **production slot only** (Cloudflare DNS + App Service-managed cert)

#### Slot architecture (zero-downtime)

```
            ┌────────────────────────────────────────┐
            │   App Service: signalplatforms-prod    │
            │                                        │
   USERS ──>│   ┌──────────────┐    ┌─────────────┐  │
            │   │  production  │    │   staging   │  │
            │   │ slot (live)  │<──>│ slot (idle) │  │
            │   │              │swap│             │  │
            │   └──────────────┘    └─────────────┘  │
            │           ▲                  ▲         │
            └───────────│──────────────────│─────────┘
                        │                  │
              after manual                 │
              approval, slot           deploy-to-prod
              swap promotes            .yml deploys
              staging → prod           here FIRST
```

The swap operation is atomic at the Azure load balancer level (~30s). Azure pre-warms the staging slot before the swap, so the first request hitting the newly-promoted code is never a cold-start request.

#### `deploy-to-prod.yml` workflow

Triggers:
- `on: push: branches: [master]` — normal release flow (release PR `develop` → `master` lands, this fires)
- `on: workflow_dispatch:` with `ref` input — hotfix promotion or rollback re-deploy

GitHub Environment: `production` (configured at repo Settings → Environments) with **required reviewer = Tony** and **deployment branches restricted to `master`** (prevents accidental prod deploys from feature branches).

Step sequence (mirrors `deploy-to-test.yml` from PRs #98/#99 with key prod-only additions in **bold**):

1. Checkout `master` HEAD (or `workflow_dispatch` input ref).
2. Setup Python 3.12, build Linux `antenv` (identical to Test).
3. Build frontend (`npx vite build`, identical to Test).
4. Prepare deployment package (`backend/` with `static/frontend/`; identical to Test).
5. **Pre-deploy smoke test** on CI runner — identical to Test (PR #99). Catches deploy-shape bugs in <60s before any Azure resources are touched.
6. Deploy to **`staging` slot** (NOT `production` directly):
   ```yaml
   - uses: azure/webapps-deploy@v3
     with:
       app-name: signalplatforms-prod
       slot-name: staging
       package: backend
   ```
7. **Wait for staging slot to be healthy**: poll `https://signalplatforms-prod-staging.azurewebsites.net/api/health` until 200 (max 5 min).
8. **Post-deploy smoke against the staging slot's real URL** — proves Azure-side init succeeded (env vars, secrets, prod DB connection, ACS, custom-domain bindings on prod slot didn't break staging). This is the first time the code touches a prod-like environment.
9. **Run feature-readiness probes against staging slot** (`/api/internal/readiness/<feature>` — see pattern below). Any 5xx or feature-not-ready response fails the workflow before any traffic shift.
10. **🛑 MANUAL APPROVAL GATE** — GitHub Environment `production` pauses the workflow. Tony receives a notification with a link to the run, reviews the smoke + readiness output in the workflow log, clicks ✅ Approve (or ❌ Reject). This is the irrevocable "ship to live traffic" decision.
11. **Atomic slot swap** (~30s):
    ```yaml
    - run: az webapp deployment slot swap
            --resource-group <rg>
            --name signalplatforms-prod
            --slot staging
            --target-slot production
    ```
12. **Post-swap verify**: hit `https://app.signalplatforms.io/api/health`, assert response includes the deployed SHA matching this workflow run (Application Insights deployment marker is also emitted at this point).

#### Smoke-test extension: feature-readiness probes

PR #99 proved the local-runner smoke pattern in Test. Story 6.11 extends it with **internal readiness endpoints** that the workflow probes against the staging slot before the swap:

- **`/api/internal/readiness/ai-context`** — returns 200 only if the Story 6.5a prompt registry is loaded and contains rows. (Resolves R6 from the 2026-05-19 release PR — the `context-pack-load-failed` AI bug would have been caught here before any prod swap.)
- **`/api/internal/readiness/stripe`** — confirms `STRIPE_SECRET_KEY` is present and `stripe.PaymentIntent.list(limit=1)` returns without auth error (added during the billing stories 6.6–6.10).
- **`/api/internal/readiness/email`** — confirms `EMAIL_PROVIDER=acs` resolves, the ACS connection string is valid, and the sender domain matches `EMAIL_FROM` (uses ACS's send-status endpoint, not a real email).

These probes are **internal only** — bind to a workflow-token header or restrict by source IP. They are NOT public health checks.

The pattern: **every story that adds a feature gated by external config adds a readiness probe in the same PR.** This way the prod smoke gate grows naturally and catches "I forgot to set the env var" bugs in CI instead of after the swap.

#### Manual approval gate

Configure at repo level (GitHub Settings → Environments → `production`):

- **Required reviewers:** Tony (initially); add a deputy when available so prod deploys aren't blocked by holidays.
- **Wait timer:** 0 — the human approval is the only gate.
- **Deployment branches:** `master` only.

When step 10 fires, the workflow shows "Waiting for approval from <reviewer>" in the Actions UI. The approver gets a GitHub notification + email. They open the run, scroll through smoke output + readiness probes + post-deploy smoke results, then approve or reject in the workflow UI. Approving unblocks step 11; rejecting aborts (staging slot keeps the new code but production stays untouched).

#### Rollback strategy

| Scenario | Action | Recovery time |
|---|---|---|
| Post-swap regression noticed within minutes (staging still holds previous prod code) | Re-swap: `az webapp deployment slot swap --slot production --target-slot staging` | <2 min |
| Post-swap regression noticed AFTER staging has been overwritten by a later deploy | `workflow_dispatch` deploy-to-prod with `ref = <previous-master-tag>`, then approve + swap | 20-30 min (full deploy cycle) |
| Catastrophic data corruption | Azure SQL point-in-time restore (DB) + slot re-swap (code) | 30-60 min |

The `Release PR procedure` (above) already tags `pre-release-YYYY-MM-DD` on master before each merge. For production cutovers, that tag becomes the rollback target. **Story 6.11 must add `docs/runbooks/PROD-ROLLBACK-RUNBOOK.md`** with the exact commands and a Tony-tested dry-run.

#### Slot-sticky vs swappable app settings

When configuring app settings on the prod slot, mark them according to whether they should swap with code:

| Setting type | Slot-sticky? | Examples |
|---|---|---|
| **Slot-bound** (do NOT swap with code) | ✅ Yes | `WEBSITES_PORT`, `EMAIL_FROM`, custom domain hostnames, slot-specific Application Insights connection string |
| **Code-bound** (SWAP with code) | ❌ No | Deployed SHA, code version stamp, feature flags |
| **Secrets** (do NOT swap; come from Key Vault) | ✅ Yes | DB connection, ACS connection string, Stripe secret key, JWT signing key |

Misconfiguring this category is the #1 source of "swap broke prod" Azure horror stories; Story 6.11's ACs should explicitly call out a slot-stickiness audit step.

#### Story 6.11 task list (preview)

- [ ] Provision App Service Plan + Web App `signalplatforms-prod` (P1V3+)
- [ ] Add `staging` deployment slot
- [ ] Provision Azure SQL DB `EventLeadPlatformProd` (separate logical server)
- [ ] Set up Key Vault + managed-identity access
- [ ] Configure prod slot app settings as `@Microsoft.KeyVault(...)` references (no plain-text secrets in App Service config)
- [ ] Configure slot-stickiness per the table above
- [ ] Bind `app.signalplatforms.io` to production slot only
- [ ] Verify ACS sender domain (SPF/DKIM) + configure prod MailFrom
- [ ] Bind Application Insights to both slots
- [ ] Create GitHub Environment `production` (required reviewer = Tony, deployment branches = `master`)
- [ ] Add GitHub secrets: `AZURE_WEBAPP_PUBLISH_PROFILE_PROD`, `AZURE_CREDENTIALS_PROD`
- [ ] Write `.github/workflows/deploy-to-prod.yml` (start from `deploy-to-test.yml`; add steps 7–12 above)
- [ ] Implement `/api/internal/readiness/{ai-context, stripe, email}` endpoints
- [ ] **Dry-run**: deploy a no-op commit to staging, run all gates, approve, swap, verify, then re-swap back. Validates the entire pipeline before first real release.
- [ ] Publish `docs/runbooks/PROD-ROLLBACK-RUNBOOK.md`
- [ ] First production cutover: release PR carries the billing-complete code; SM publishes go-live checklist

#### Acceptance criteria preview

Full ACs land in `docs/stories/story-6.11.md` when the story opens. Preview:

1. Push to `master` triggers `deploy-to-prod.yml`; deploy lands on staging slot only.
2. Pre-deploy CI smoke gates the Azure deploy (same as Test).
3. Post-deploy smoke + readiness probes against the staging slot gate the swap.
4. Workflow pauses for manual approval on the `production` GitHub Environment.
5. Swap is atomic; the production URL serves no 5xx during the swap window (measured via Application Insights synthetic monitor).
6. Rollback via slot re-swap completes in <2 min and is documented in the run summary.
7. App Insights records the deployed SHA as a custom property for both slots.
8. `docs/runbooks/PROD-ROLLBACK-RUNBOOK.md` exists and has been dry-run validated.

#### What Test taught us that Production inherits

| Lesson learned in Test (2026-05) | Inherited by Prod (Story 6.11) |
|---|---|
| Bare `python` in startup scripts fails when Oryx skips venv activation (PR #98) | Prod's `startup.txt` + `startup.sh` use `antenv/bin/python` from day one |
| Long Azure deploy/validate cycles hide deploy-shape bugs (PR #99) | Prod inherits the pre-deploy smoke step + adds a second post-deploy smoke against the deployed slot |
| File-system path resolution differs between local dev and Azure (R6 / context-pack bug) | Story 6.5a moves prompt context to DB; readiness probe gates the prod swap if the registry isn't loaded |
| `from_name` cross-provider contract is fragile under different SDK shapes (PR #100) | Email readiness probe verifies ACS resource config before swap, not just env-var presence |
| Slot test environment uses single in-place deploy → restart downtime is acceptable for Test but not Prod | Prod uses two-slot architecture and atomic swap |

### One-time reconciliation (May 2026 — historical record)

The first release PR through this process is a **bulk catch-up** to recover the 29 commits currently only on `develop`:

- **PRs:** #92 (ACS Email), #93 (Vite same-origin), #94 (aiohttp dep), #95 (password reset URL fix), #96 (platform owner seed)
- **Direct commits:** ~10 Azure startup fixes (uvicorn port, ODBC URL, Alembic subprocess, SPA-from-FastAPI, python-multipart, antenv bundling)
- **New migrations:** 073 (platform owner seed) + 074 (onboarding-complete flag)
- **Modified migration:** 015 (retroactive User-row insert — environments that already ran 015 need a one-off fix script; see release PR body)
- **New deps:** `aiohttp==3.13.5`, `python-multipart==0.0.20`
- **New files:** `backend/common/database_url.py`, `backend/services/email_providers/acs.py`, tests for both, `backend/startup.sh`, `database/seeds/signal-platforms-seed.sql`

Tony will prepare this release PR separately (see discussion record 2026-05-19). After this catch-up, master and develop are aligned and the per-story cadence begins. **PR #87 (Story 6.5a) must be re-targeted from `master` to `develop` (`gh pr edit 87 --base develop`) before its next push, so 6.5a becomes the first story to ship under the new flow.**

---

## 🇦🇺 AU-First Prompt Evaluation Reset (Mandatory after Story 6.4.5)

Story 6.4.5 showed that the six-locale prompt-candidate sweep creates too much context noise for the launch goal. From this point, prompt-candidate work is AU-first until the diagnostic framework proves changes are clean.

Rules:

- Do not continue prompt-candidate stories using the existing six-locale sweep approach.
- Defer H5/style and H6/font prompt-candidate sweeps until the AU diagnostic framework exists.
- Story 6.4.6 is Dev-owned and may change framework/harness code. It must produce the first current-state AU baseline and must not test prompt improvements.
- Story 6.4.7 is BMAD Analyst-owned and may update version-managed prompt/context artifacts and tracking documents only. It must not modify application, harness, judge-ingest, frontend, or backend code.
- If the Analyst loop discovers a needed code change, stop and raise a Dev-owned framework fix story.
- Tony approves continue/stop after every Analyst loop.
- The Analyst must present the top 5 candidate prompt/context improvements after each result review, advise which can safely be bundled without distorting causality, then wait for Tony approval before applying changes.
- Only one controlled change set is tested per iteration.
- Judge conflict findings must be reviewed before changing prompt text.

Persistent process document:

- `docs/stories/STORY-6-AU-EVAL-ANALYST-LOOP.md`

Tracking sheet:

- `docs/stories/STORY-6-AU-EVAL-ITERATION-TRACKING.md`

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
| **2026-05-19 (amendment)** | **Story 6.11 Production Deployment Blueprint added** to § Environment Promotion Workflow, between "Hotfix exception" and "One-time reconciliation". Captures the production design end-to-end so Story 6.11 implementation is plumbing, not decisions: design goals (zero-downtime, manual approval, smoke gate parity with Test, <5 min rollback), two-slot architecture diagram, `deploy-to-prod.yml` 12-step sequence (with prod-only post-deploy smoke + readiness probes against the staging slot before the swap), manual-approval-gate config, rollback strategy table, slot-stickiness rules for app settings, task-list preview, AC preview, and a "What Test taught us that Production inherits" table that maps each lesson from PRs #98/#99/#100/R6 to the prod design. `EPIC-6-STATUS.md` row 6.11 amended to point at this subsection as the authoritative blueprint. | Today's release-PR work and Tony's CI-check question in Stage D made clear that Story 6.11 needs a written-down design before the cycle opens — otherwise it will replay the same "discover by failing in Azure" pattern that cost two weeks during Test bring-up. Capture the lessons-learned while they're fresh and have the Story 6.11 implementer (Tony + Dev) inherit them by reference. |
| **2026-05-19** | **Environment Promotion Workflow adopted.** Story PRs now target **`develop`** (Test slot), promoted to **`master`** (Production) only via SM-drafted release PRs after per-story QA passes against the deployed Azure Test environment. `scripts/git/new-story.ps1` default `-BaseBranch` flipped from `master` to `develop`. New § Environment Promotion Workflow section added with mermaid, QA-in-Test table, release PR procedure, hotfix exception, and a historical record of the one-time reconciliation needed in May 2026 (29 commits stranded on `develop`). Added **Story 6.11 — Production Environment + CI/CD + Manual Approval Gate** to Phase B (post-6.10, so production opens with billing live). Updated **Story 6.5a Status:** architecture phase complete (Dimitri Rev 9, 2026-05-09) — first story to ship under the new flow. **`docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`** PR-naming rules updated in lockstep. | Two parallel tracks (Epic 6 story PRs → `master`; Azure infra fix PRs → `develop`) had silently diverged: master was missing all the fixes that actually make the app run on Azure (ACS Email, port binding, ODBC URL, SPA-from-FastAPI, dependencies). Tony surfaced the concern after deploying `develop` to Azure Test. The new model guarantees nothing reaches `master` without first passing QA against a real Azure deployment, which is the only place deployment-shaped bugs (env vars, secrets, real DB, real email) surface. Per-story cadence chosen over batched releases to match Epic 6's one-story-per-few-days rhythm. |
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
| 2026-04-29 | **Prompt-evaluation reset approved after Story 6.4.5.** Pause remaining prompt-candidate stories that continue the six-locale sweep approach. New sequence: Story 6.4.6 Dev-owned AU-only diagnostic framework + current-state AU baseline, then Story 6.4.7 BMAD Analyst-owned iterative loop over version-managed prompt/context artifacts. Analyst must present top 5 candidate improvements, advise safe bundleability, get Tony approval, apply one controlled change set, rerun eval/judges, update tracking, and stop for Tony continue/stop. | 6.4.4.2 and 6.4.5 showed the six-locale benchmark is too noisy for launch prompt decisions. AU is the launch market, so measurement must isolate AU prompt/context weaknesses before more prompt candidate sweeps. |
