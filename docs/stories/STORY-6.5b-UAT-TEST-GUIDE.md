# Story 6.5b — UAT Test Guide

**Story:** 6.5b — Prompt Assembly Registry Foundation (Closes R6)
**UAT owner:** Tony + SM
**Mode:** Evidence review + R6-resolution verification in deployed Test environment

This story shifts the five "stored prose" prompt blocks (A ROLE_CONTRACT, B SAFETY, C BRAND_POSTURE, G FEW_SHOT, I JSON_OUTPUT) from Python literals / on-disk markdown into versioned DB rows. The assembled prompt must remain functionally equivalent to today's output (AC-9). Block G migration closes R6 (the `context-pack-load-failed` failure on Azure).

Two sign-off gates: **(a)** AC-19 prompt-equivalence diff (Tony reviews locally — pre-merge), and **(b)** R6-resolved verification against the deployed Test environment after merge.

---

## Section 1 — Schema & Migration Review

Review the new migration files (`073_…` through whatever Dev produced).

Pass criteria:

- Migrations exist for: registry schema, FORM_AI_V1 profile + version, sections A/B/C/G/I, variants for each section (Block C = 4 variants), `GenerationRun` audit columns.
- Each migration has a working `downgrade()`.
- No existing migration was modified (latest pre-existing head: `072_story_648_au_production_prompt_context.py`).
- No Alembic command was executed by the agent.
- Tony has executed the migrations locally; alembic head is at the new tip.

**Section 1 Final:** Pass / Fail

---

## Section 2 — Block A/B/C/G/I Variant Content Review

Spot-check the seeded variant text against the current code path.

Pass criteria:

- Block A `ROLE_CONTRACT` variant content matches today's system role prose (verbatim, including `FormSemanticPlan` instructions).
- Block B `SAFETY` variant content matches today's PII / brand-safety prose.
- Block C `BRAND_POSTURE` has **four** variants keyed by `VariantCode` matching the enum values (`local`, `heritage`, `neutral`, `transcreate`). Each variant contains the correct prose for its posture.
- Block G `FEW_SHOT` variant contains the current `STORY-6.2-AI-CONTEXT-PACK.md` content (post-trim — `_trim_context_pack_for_prompt` semantics preserved at seed time or in the renderer).
- Block I `JSON_OUTPUT` variant contains today's JSON-tail prose.
- `STORY-6.2-AI-CONTEXT-PACK.md` has the documentation-only banner referencing the seeding migration.

**Section 2 Final:** Pass / Fail

---

## Section 3 — Renderer / Resolver Behaviour

Review `resolve_prompt_assembly()` and `render_prompt_assembly()` against architecture §4 + §5.

Pass criteria:

- Resolver returns sections in correct `SortOrder`.
- Resolver picks the active `PromptAssemblyProfileVersion` (only one active at a time).
- For Block C, resolver selects the variant whose `VariantCode` matches the current `brandPosture` enum value (passed as input).
- Renderer hydrates `Prose` `DataStructureType` verbatim from `PromptSectionVariant.PromptSnippet`.
- Renderer applies `{heritageOrigin}` placeholder substitution for Block C `heritage` variant (architecture §2.7 Block C).
- Backend tests for the resolver / renderer pass (see Section 6).

**Section 3 Final:** Pass / Fail

---

## Section 4 — Pre-Merge Prompt-Equivalence Diff (AC-19) — Tony Sign-off Gate

This is the **most important gate** for this story since there is no frontend to eyeball.

Review `docs/stories/STORY-6.5b-PROMPT-EQUIVALENCE-DIFF.md` produced by Dev's helper script (`backend/scripts/story_6_5b_prompt_equivalence_diff.py`).

Pass criteria:

- Report header shows: `GenerationRunID`, recovered inputs (audienceLocale, brandPosture, user prompt excerpt), commit SHA, local run timestamp.
- Per-block panel exists for each of A–I:
  - `OLD` snippet from current `_build_initial_messages` path.
  - `NEW` snippet from new `render_prompt_assembly()`.
  - Source-change one-liner (e.g., "A: code literal → `PromptSectionVariant.PromptSnippet` ID 5").
  - Diff verdict: ✅ Identical / ⚠️ Whitespace-only / 🔴 Content delta.
- Summary table: 9 rows (A–I), each with verdict and source-change one-liner.
- Top-level verdict: ✅ No behavioural regression (target) or explicit Tony-accepted delta.
- Blocks D, E, F, H verdict = ✅ Identical (they are not touched this story).
- Block G verdict = ✅ Identical (the content is the same prose, just from DB instead of file).
- **Tony explicitly approves "no behavioural degradation"** — recorded in the report and in this UAT guide.

If the verdict is 🔴 or ⚠️ for any block with non-trivial content delta, Dev investigates and re-runs the script until verdict is ✅ (or Tony explicitly accepts the delta with reason).

**Section 4 Final:** Pass / Fail
**Tony sign-off:** ☐ Approved "no behavioural degradation" / ☐ Approved with documented delta / ☐ Rejected — see notes

---

## Section 5 — `_load_context_pack()` Removal

Pass criteria:

- `_load_context_pack()` is deleted (or replaced with a deprecation-raising shim that clearly directs readers to the registry).
- No runtime call site reads `STORY-6.2-AI-CONTEXT-PACK.md` from disk. Confirm via:
  ```powershell
  rg -n "STORY-6.2-AI-CONTEXT-PACK|_load_context_pack|CONTEXT_PACK_PATH" backend/
  ```
  All hits should be in tests / comments / the deprecation shim message only.
- `_ROOT_PATH` and `CONTEXT_PACK_PATH` constants removed from `backend/modules/form_ai/service.py` if no longer used.

**Section 5 Final:** Pass / Fail

---

## Section 6 — Automated Green Gate

Review `STORY-6.5b-GATE-EVIDENCE.md`.

Pass criteria:

- Full `python -m pytest --tb=short` summary line is recorded (e.g., `=== N passed, 0 failed in Xs ===`). Anti-hallucination protocol applies — no truncated runs.
- New backend tests added cover:
  - Registry resolver (active version selection, variant selection by `BrandPosture`, fallback to `DEFAULT`).
  - Renderer hydration of `Prose` `DataStructureType`.
  - Equivalence test: assembled prompt for representative input contains every key phrase / section header from the current `_build_initial_messages` output.
  - `_load_context_pack` removal (no test depends on the file read).
- Existing form-AI eval baseline still green (no behavioural regression in the harness).
- Frontend checks are NOT required (no frontend touched).

Suggested minimum focused checks:

```powershell
python -m pytest backend/tests/test_form_ai_prompt_assembly.py backend/tests/test_form_ai_prompt_capabilities.py backend/tests/test_form_ai_locale_assembly.py backend/tests/test_form_ai_locale_resolution.py backend/tests/test_story_6_5b_*.py --tb=short
```

Then full backend regression:

```powershell
python -m pytest --tb=short
```

**Section 6 Final:** Pass / Fail

---

## Section 7 — Deploy & R6 Verification in Test (Post-Merge)

After PR merges to `develop`, `.github/workflows/deploy-to-test.yml` auto-deploys to the Azure test slot.

Pass criteria:

- GitHub Actions deploy run for the merge commit completes green:
  ```powershell
  gh run list --workflow=deploy-to-test.yml --branch develop --limit 5
  ```
- App Service is healthy: `https://signalplatforms-test.azurewebsites.net/api/health` returns 200.
- Tony logs in to the deployed Test environment and runs **UAT prompt 1** from story-6.5b spec context (e.g., "Create a registration form for a tech conference in Sydney"):
  - AI Generate Form Draft button is clicked.
  - **Generation succeeds** (status: Success, components rendered).
  - **No `context-pack-load-failed`** in the AI panel terminal output (AC-13).
- SQL check (Tony or SM runs against Azure Test DB):
  ```sql
  SELECT TOP 1
    GenerationRunID,
    PromptAssemblyProfileVersionID,
    <variant-id-columns-or-json-snapshot>
  FROM dbo.GenerationRun
  WHERE TerminalReason IS NULL
  ORDER BY CreatedUtc DESC;
  ```
  - `PromptAssemblyProfileVersionID` is non-null.
  - Variant IDs / snapshot contain entries for Blocks A, B, C, G, I (AC-14).

**Section 7 Final:** Pass / Fail
**R6 Verified Resolved:** ☐ Yes / ☐ No (notes if no)

---

## Section 8 — Migration Handoff

If a migration was added (it will be — at least 6 of them), Tony reviews migration instructions.

Pass criteria:

- Exact Alembic command for Tony is listed in `STORY-6.5b-GATE-EVIDENCE.md` (or closeout report):
  ```powershell
  cd backend
  alembic upgrade head
  ```
- Each migration ID listed with one-line purpose (per story-6.5b.md §7 planned set).
- Downgrade behaviour documented for each migration.
- How to verify seeded rows after Tony applies it (representative `SELECT` queries).
- Agent did NOT execute Alembic.

**Section 8 Final:** Pass / Fail / N/A

---

## Section 9 — Closeout & Stale-Field Audit

Review story closeout. SM runs the stale-field audit per EPIC-6-WORKFLOW-GUIDE.md.

Pass criteria:

- `docs/stories/story-6.5b.md` — Status `Complete`, Completed date matches `mergedAt` UTC date for PR #104, PR # is correct.
- `docs/stories/EPIC-6-STATUS.md` — row 6.5b flipped to ✅, R6 entry marked **Resolved by 6.5b**.
- `docs/stories/EPIC-6-WORKFLOW-GUIDE.md` — Current Focus updated to next story (likely 6.5c — Capability Catalog Cutover).
- `STORY-6.5b-CLOSEOUT-REPORT.md` exists and covers: TL;DR, AC matrix (19/19), architecture sketch (renderer hand-off), what this unlocks (6.5c, 6.5d), carry-forward backlog, risks, green gates, hygiene, decision.
- Worktree retirement plan recorded (`git worktree remove "C:\wt\elp\story-epic6-6.5b-registry-foundation"`).
- Production promotion decision is explicit (next: 6.5c).

**Section 9 Final:** Pass / Fail

---

## UAT Result Summary

| Section | Result | Notes |
|---|---|---|
| Section 1 Schema & Migration Review | _Pending_ | |
| Section 2 Block A/B/C/G/I Variant Content Review | _Pending_ | |
| Section 3 Renderer / Resolver Behaviour | _Pending_ | |
| Section 4 Pre-Merge Equivalence Diff (Tony sign-off) | _Pending_ | |
| Section 5 `_load_context_pack()` Removal | _Pending_ | |
| Section 6 Automated Green Gate | _Pending_ | |
| Section 7 Deploy & R6 Verification in Test | _Pending_ | |
| Section 8 Migration Handoff | _Pending_ | |
| Section 9 Closeout & Stale-Field Audit | _Pending_ | |

**Final UAT Decision:** _Pending_ — PASS / PARTIAL / FAIL
