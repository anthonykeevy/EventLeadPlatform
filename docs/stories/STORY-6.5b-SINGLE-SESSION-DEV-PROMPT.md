# Story 6.5b — Single-Session Dev Prompt

You are implementing **Story 6.5b — Prompt Assembly Registry Foundation (Closes R6)**.

**Worktree:** `C:\wt\elp\story-epic6-6.5b-registry-foundation`
**Branch:** `story/epic6-6.5b-registry-foundation`
**PR:** [#104](https://github.com/anthonykeevy/EventLeadPlatform/pull/104) — Draft PR to `develop`
**Base:** `develop` at or after merge commit `cb339ed` (PR #103 — Architecture Closeout + 6.5b Draft)

---

## Mission

Stand up the **Prompt Assembly Registry** (`config.PromptAssemblyProfile*`, `config.PromptSection*`, `config.PromptSectionVariant*`, `config.PromptSectionData`) per `docs/architecture/prompt-assembly-registry-architecture.md`. Migrate the five "stored prose" blocks **A, B, C, G, I** out of Python literals and the on-disk markdown file into seeded DB variants. Wire the renderer into `_build_initial_messages` so the assembled prompt is functionally equivalent to today's output for unchanged inputs.

**This is the change that closes R6** (`context-pack-load-failed` in the deployed Test environment). Block G migration moves `STORY-6.2-AI-CONTEXT-PACK.md` content into the DB and deletes `_load_context_pack()`, removing the on-disk file dependency that Azure can't satisfy.

**Hard rule — no behavioural regression.** AC-19 (prompt-equivalence diff) is **Tony's pre-merge sign-off gate**. Do not move the PR Draft → Ready until Tony approves the diff report.

---

## Read First (in this order)

1. `docs/stories/story-6.5b.md` — 19 ACs, §5a Local Validation Flow, §7 Planned Migration Set.
2. `docs/stories/story-context-6.5b.xml` — critical objectives, constraints, paths.
3. `docs/architecture/prompt-assembly-registry-architecture.md` — **authoritative**:
   - §2.7 (post-impl per-block sources)
   - §3 (registry schema)
   - §4 (catalog resolver)
   - §5 (renderer contract)
   - §5.4 (Python-first hybrid — no SP this story)
   - §8 (variant-level versioning)
   - §10 (sequencing — confirms 6.5b is Stage 1)
4. `docs/architecture/decision-6.5a-clarification-options-data-model.md` — §4.1 (all-blocks-DB-driven platform rule). E (clarification) is **out of scope** this story.
5. `docs/stories/STORY-6.5b-UAT-TEST-GUIDE.md` — what Tony + SM will check post-implementation. Build to this.
6. `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md` — source of Block G seed content.
7. `backend/modules/form_ai/service.py` — current `_build_initial_messages`, `_load_context_pack`, `_trim_context_pack_for_prompt`.
8. `backend/models/config/prompt_assembly_profile.py` (verify what already exists).
9. `backend/migrations/versions/072_story_648_au_production_prompt_context.py` — most recent migration; your numbering starts at `073_`.
10. `docs/stories/EPIC-6-WORKFLOW-GUIDE.md` — §⚡, the Green CI/CD Rule, Story Evidence Contract, Database Connection Consistency Rule.

---

## Step 0 — Preflight

Run the workflow preflight script:

```powershell
.\scripts\workflow\preflight-story.ps1 `
  -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.5b-registry-foundation" `
  -ExpectedBranch "story/epic6-6.5b-registry-foundation" `
  -ReportFile "docs/stories/STORY-6.5b-PREFLIGHT.md"
```

Verify:

- PR #104 exists and targets `develop`.
- PR #103 is merged at `cb339ed`.
- You are in the worktree at `C:\wt\elp\story-epic6-6.5b-registry-foundation` (not the main checkout).
- LocalDB is reachable and `os.getenv("DATABASE_URL")` matches the runtime-resolved URL from `common.database` (Database Connection Consistency Rule).
- Architecture docs `decision-6.5a-clarification-options-data-model.md` and `prompt-assembly-registry-architecture.md` exist under `docs/architecture/`.

If any precondition fails, **stop and report** before touching code.

---

## Step 1 — Implementation Plan (Think Before You Type)

Before editing, write a short plan into chat (5–10 bullets max) covering:

1. Order of migrations (matches story-6.5b.md §7).
2. Which existing `backend/models/config/prompt_assembly_profile.py` rows already exist (vs need adding).
3. Where the resolver + renderer modules will live (suggest `backend/modules/form_ai/prompt_assembly/{resolver.py, renderer.py, __init__.py}`).
4. Which call sites in `_build_initial_messages` will be replaced.
5. What `_load_context_pack` becomes (deleted vs deprecation shim).
6. Tests to add (resolver, renderer, equivalence, no-file-read).
7. Shape of the AC-19 helper script (`backend/scripts/story_6_5b_prompt_equivalence_diff.py`).
8. Schema choice for `GenerationRun` audit: discrete `PromptAssemblyProfileVersionID` + per-block FK columns (5 nullable INT columns), OR a single JSON snapshot column. **Recommendation:** combo — `PromptAssemblyProfileVersionID INT NULL` (FK) + `PromptVariantSnapshot NVARCHAR(MAX) NULL` (JSON: `{"A": <id>, "B": <id>, "C": <id>, "G": <id>, "I": <id>}`). Discrete FK gives audit joins; snapshot gives forward-compat as blocks are added in 6.5c/6.5d.

Pause for ~30 seconds and re-read the plan against AC-1..AC-19. Adjust if you spot a gap.

---

## Step 2 — Registry Schema + Variant Versioning Migration (AC-1, AC-7)

Authoritative reference: `prompt-assembly-registry-architecture.md` §3 + §8.1.

Create migration `073_story_6_5b_prompt_assembly_registry_schema.py`:

- `config.PromptAssemblyProfile` (Code UQ, Description, IsActive, audit cols).
- `config.PromptAssemblyProfileVersion` (FK Profile, VersionNumber, IsActive — only one active per Profile via partial UQ or trigger, IsLockedForEdits, ReleaseNotes, ActivatedUtc).
- `config.PromptSection` (FK ProfileVersion, SectionCode A/B/C/D/E/F/G/H/I, DisplayName, SortOrder, IsRequired, DataStructureType ENUM `Prose|Json|Snapshot|Refs`).
- `config.PromptSectionVariant` (FK PromptSection, VariantCode UQ within section, DisplayName, Description, IsDefault, PromptSnippet NVARCHAR(MAX), SchemaJson NVARCHAR(MAX) NULL, VariantVersion INT, IsLockedForEdits, ActivatedUtc).
- `config.PromptSectionData` (FK PromptSectionVariant, DataKey, DataValue, DataType, SortOrder).

Each table: audit columns (`CreatedUtc`, `CreatedBy`, `LastUpdatedUtc`, `LastUpdatedBy`) matching the rest of the codebase.

Working `downgrade()` that drops in reverse FK order.

Add SQLAlchemy models in `backend/models/config/` for the new tables and register them in `backend/models/__init__.py`.

---

## Step 3 — Seed FORM_AI_V1 Profile + Sections + Variants (AC-2, AC-3, AC-4, AC-5)

Create migration `074_story_6_5b_seed_form_ai_v1_profile.py`:

- `PromptAssemblyProfile` row: `Code='FORM_AI_V1'`, `Description='Form AI generation prompt assembly — initial migration of stored prose blocks'`, `IsActive=1`.
- `PromptAssemblyProfileVersion` row: VersionNumber=1, IsActive=1, ReleaseNotes='Initial registry — A/B/C/G/I migration; D/E/F/H remain on existing paths'.
- `PromptSection` rows (SortOrder 1..5 — leave gaps for D/E/F/H to slot in later in 6.5c/6.5d):

| Code | DisplayName | SortOrder | DataStructureType | IsRequired |
|---|---|---|---|---|
| A | ROLE_CONTRACT | 1 | Prose | 1 |
| B | SAFETY | 2 | Prose | 1 |
| C | BRAND_POSTURE | 5 | Prose | 1 |
| G | FEW_SHOT | 7 | Prose | 1 |
| I | JSON_OUTPUT | 9 | Prose | 1 |

(SortOrder gaps mirror the full A–I tree from architecture §2; sections D=3, E=4, F=6, H=8 will be inserted by 6.5c / 6.5d.)

Create migration `075_story_6_5b_seed_variants_abci.py`:

- Block A: 1 variant `VariantCode='DEFAULT'`, `IsDefault=1`, `PromptSnippet` = current Block A prose from `backend/modules/form_ai/service.py`.
- Block B: 1 variant `DEFAULT`, snippet = current Block B prose.
- Block C: **4 variants** keyed by `VariantCode IN ('local', 'heritage', 'neutral', 'transcreate')` matching the `brandPosture` enum values. Use the existing `BRAND_POSTURE_PROMPTS` dict in `service.py` as the source. `IsDefault=1` for `neutral`.
- Block I: 1 variant `DEFAULT`, snippet = current Block I JSON-output prose.

Create migration `076_story_6_5b_seed_block_g_context_pack.py`:

- Block G: 1 variant `VariantCode='DEFAULT'`, `IsDefault=1`, `PromptSnippet` = the **post-trim** content of `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md`.
- Decide: trim at seed time, or store full file and let renderer call `_trim_context_pack_for_prompt`. **Recommendation:** trim at seed time (simpler, no runtime trim cost; trim is deterministic). Document the choice in the migration docstring + closeout report.

Each migration should `INSERT` via raw SQL or `sa.text` against `op.get_bind()` for cross-dialect safety. Mirror existing seed patterns (e.g., `065_story_6441_seed_locale_blocks_au.py`).

---

## Step 4 — Resolver + Renderer (AC-8, AC-9)

Reference: architecture §4 + §5.

Create `backend/modules/form_ai/prompt_assembly/__init__.py` exporting `resolve_prompt_assembly` and `render_prompt_assembly`.

`resolver.py`:

```python
def resolve_prompt_assembly(
    db: Session,
    profile_code: str,
    *,
    brand_posture: BrandPosture,
    audience_locale: str,  # accepted for future use; not consumed by 6.5b blocks
) -> list[ResolvedSection]:
    """Return sections in SortOrder with the chosen variant for each.

    For 6.5b in-scope blocks (A, B, C, G, I):
      - Picks the active PromptAssemblyProfileVersion for `profile_code`.
      - For each PromptSection, picks the variant whose VariantCode matches the
        runtime axis (Block C: brand_posture); otherwise picks IsDefault=1.

    Returns ResolvedSection(code, sort_order, variant_id, snippet, data_structure_type).
    """
```

`renderer.py`:

```python
def render_prompt_assembly(
    resolved: list[ResolvedSection],
    *,
    placeholders: dict[str, str],  # {"heritageOrigin": "Australia"} etc.
) -> str:
    """Concatenate snippets in SortOrder; substitute {placeholder} tokens.

    Only Prose DataStructureType is handled this story; Json/Snapshot/Refs raise
    NotImplementedError (lights up in 6.5c).
    """
```

Acceptance:

- Resolver returns sections in `SortOrder`.
- Block C variant is picked by `VariantCode == brand_posture.value`. If no match, fall back to `IsDefault=1`.
- Renderer hydrates `Prose` verbatim, then runs `str.format_map` (or equivalent) for `{heritageOrigin}` only when Block C variant is `heritage`.
- Whitespace between blocks matches the current `\n\n` join in `_build_initial_messages`.

---

## Step 5 — Wire Renderer Into `_build_initial_messages` (AC-10, AC-11)

In `backend/modules/form_ai/service.py`:

1. Call `resolve_prompt_assembly(db, "FORM_AI_V1", brand_posture=..., audience_locale=...)`.
2. Call `render_prompt_assembly(resolved, placeholders={...})`.
3. The returned string **replaces** the current literal blocks A/B/C/G/I in the system-message construction. Keep D (`_assemble_locale_block`), E (clarification context — not yet present at runtime), F (`_build_capability_block`), H (user message) on their existing paths.
4. **Delete `_load_context_pack()`** (or replace with a single line: `raise RuntimeError("Replaced by registry — see Story 6.5b. Block G now seeds from config.PromptSectionVariant.")`).
5. Delete `_ROOT_PATH` and `CONTEXT_PACK_PATH` if no longer referenced.
6. Capture variant IDs from `resolved` and persist into the new `GenerationRun` columns (see Step 6).

Acceptance check via grep:

```powershell
rg -n "STORY-6.2-AI-CONTEXT-PACK|_load_context_pack|CONTEXT_PACK_PATH" backend/
```

Only hits allowed: test files, the deprecation shim string, and `docs/` references.

---

## Step 6 — Extend `dbo.GenerationRun` for Replayability (AC-6, AC-14)

Create migration `077_story_6_5b_generation_run_assembly_audit.py`:

- Add column `PromptAssemblyProfileVersionID INT NULL` with FK to `config.PromptAssemblyProfileVersion(PromptAssemblyProfileVersionID)`.
- Add column `PromptVariantSnapshot NVARCHAR(MAX) NULL` — JSON `{"A": <id>, "B": <id>, "C": <id>, "G": <id>, "I": <id>}`.
- Working `downgrade()` that drops the FK then both columns.

In `service.py`, populate these two columns when persisting a `GenerationRun` row. JSON serialise with `json.dumps(..., sort_keys=True)`.

---

## Step 7 — Backend Tests (AC-12, AC-15)

Add under `backend/tests/`:

- `test_story_6_5b_registry_resolver.py` — covers:
  - Active version selection.
  - Variant selection by `BrandPosture` (each of 4 values picks the correct variant).
  - Fallback to `IsDefault=1` when no `VariantCode` match.
  - SortOrder is preserved.
- `test_story_6_5b_renderer.py` — covers:
  - `Prose` hydration is verbatim.
  - `{heritageOrigin}` substitution works for Block C `heritage` variant.
  - Block separator matches the current `\n\n` convention.
- `test_story_6_5b_equivalence.py` — the **key** functional test:
  - Build a representative GenerationRun input (single `brandPosture` value, simple user prompt).
  - Capture the system message produced by `_build_initial_messages` post-implementation.
  - Assert it contains every key marker phrase from the current production prose (sample 6–10 stable phrases per block).
  - Assert no `STORY-6.2-AI-CONTEXT-PACK.md` file is opened during the assembly (monkeypatch `pathlib.Path.open` to raise; renderer must not call it).
- `test_story_6_5b_migrations_static.py` — verifies migration files exist, have a `revision` and `down_revision`, and `downgrade()` is not a no-op.

Run the focused suite then the full suite:

```powershell
python -m pytest `
  backend/tests/test_story_6_5b_registry_resolver.py `
  backend/tests/test_story_6_5b_renderer.py `
  backend/tests/test_story_6_5b_equivalence.py `
  backend/tests/test_story_6_5b_migrations_static.py `
  backend/tests/test_form_ai_prompt_assembly.py `
  backend/tests/test_form_ai_prompt_capabilities.py `
  backend/tests/test_form_ai_locale_assembly.py `
  backend/tests/test_form_ai_locale_resolution.py `
  --tb=short

python -m pytest --tb=short
```

Anti-hallucination protocol: copy the **exact** final summary line into `STORY-6.5b-GATE-EVIDENCE.md`. If pytest is truncated, treat as FAIL.

---

## Step 8 — AC-19 Prompt-Equivalence Diff Helper (THE GATE)

This is the most important artifact you produce — it's Tony's pre-merge sign-off.

Create `backend/scripts/story_6_5b_prompt_equivalence_diff.py`. It must:

1. Accept `--generation-run-id <int>` (defaults to "most recent successful run on LocalDB").
2. Recover the inputs from `dbo.GenerationRun`: `BrandPosture`, `AudienceLocale`, the user prompt.
3. Build the system message via:
   - **OLD path:** the pre-Story-6.5b `_build_initial_messages` logic (you can keep a copy of the old function as `_build_initial_messages_legacy` in the script for diff purposes — do not leave it in `service.py`).
   - **NEW path:** the new `_build_initial_messages` calling the renderer.
4. Per-block diff (split both system messages at `\n\n` boundaries; tag splits A..I using stable header phrases):
   - Verdict: ✅ Identical / ⚠️ Whitespace-only / 🔴 Content delta.
   - Source-change one-liner ("A: code literal → PromptSectionVariant ID <n>").
5. Emit `docs/stories/STORY-6.5b-PROMPT-EQUIVALENCE-DIFF.md` with:
   - Header: GenerationRunID, recovered inputs, commit SHA (`git rev-parse HEAD`), local timestamp.
   - Per-block fenced code panels (`OLD` then `NEW`) with verdict.
   - Summary table at the bottom (9 rows A–I).
   - Top-level verdict and a "Tony sign-off" checkbox block to be ticked manually.

Run it locally and commit the generated report. If the verdict is 🔴 or ⚠️ for in-scope blocks (A/B/C/G/I) with non-trivial deltas, **fix it before asking for sign-off** (likely cause: whitespace drift in the seed migration).

Expected outcome: D/E/F/H = ✅ (you didn't touch them). A/B/I = ✅ (literal copy from code → DB). C = ✅ for each of the 4 postures (with the matching variant selected). G = ✅ (same prose, just from DB).

---

## Step 9 — Documentation Banner on STORY-6.2-AI-CONTEXT-PACK.md (AC-16)

Edit `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md`. Add a banner at the **top** of the file (before the existing H1):

```markdown
> **📋 Documentation only — runtime source moved 2026-05-XX (Story 6.5b)**
>
> This file is preserved for reference. The runtime source for the AI form-generation
> few-shot context pack (Block G in the prompt assembly tree) is now
> `config.PromptSectionVariant` seeded by migration `076_story_6_5b_seed_block_g_context_pack.py`.
> Update the registry via a new variant version migration; do not edit this file expecting
> a runtime effect.
```

Do **not** delete the file.

---

## Step 10 — EPIC-6-STATUS.md + EPIC-6-WORKFLOW-GUIDE.md Updates (AC-18)

These get the final pass during closeout, but draft the changes now so the closeout commit is small:

- `EPIC-6-STATUS.md` — row 6.5b flips to ✅; R6 entry marked **Resolved by 6.5b** with link to this story.
- `EPIC-6-WORKFLOW-GUIDE.md` — Current Focus advances to Story 6.5c (Capability Catalog Cutover). Move 6.5b to a completed-status line.

Do not commit these until UAT passes and Tony signs off the equivalence diff.

---

## Step 11 — Local Validation Flow (per story-6.5b.md §5a)

While iterating (Steps 4–8), use the local-stack loop, NOT Azure:

```powershell
cd backend
uvicorn main:app --reload --port 8000
```

Frontend: `npm run dev` in `frontend/`. Hit the AI Agent panel locally.

Validate end-to-end locally **before** pushing:

- Generate a form for "tech conference in Sydney" (or any AU prompt).
- Confirm: success, components render, no `context-pack-load-failed`.
- Open LocalDB and confirm the new `GenerationRun` row has `PromptAssemblyProfileVersionID` and `PromptVariantSnapshot` populated.

Only push to PR #104 once local validation + equivalence diff are clean. Azure deploy is the **verification** step (post-merge UAT Section 7), not the iteration step.

---

## Step 12 — Migration Handoff to Tony

You will create six migration files: 073, 074, 075, 076, 077 (and any small follow-ups). **Do not run Alembic yourself.**

In `STORY-6.5b-GATE-EVIDENCE.md`, list:

```powershell
# Tony runs:
cd backend
alembic upgrade head
```

For each migration file:

- File name.
- One-line purpose.
- Rows inserted/updated (with row counts where deterministic).
- Downgrade behaviour.
- Verification `SELECT` after Tony applies (e.g., `SELECT COUNT(*) FROM config.PromptSectionVariant WHERE PromptSectionID IN (SELECT PromptSectionID FROM config.PromptSection WHERE SectionCode='C');` should return 4).

---

## Step 13 — Closeout (AC-17, AC-18)

Before requesting UAT:

1. Fill `docs/stories/STORY-6.5b-GATE-EVIDENCE.md`:
   - Commands run + working directory.
   - Final pytest summary line(s).
   - Equivalence-diff verdict summary (link to the report).
   - `_load_context_pack` removal grep evidence.
   - Migration list with Tony's run command.
   - Pass/fail table for backend checks.
2. Fill `docs/stories/STORY-6.5b-UAT-RESULTS.md` (pre-fill sections you can verify locally — Tony fills the rest post-deploy).
3. Fill `docs/stories/STORY-6.5b-CLOSEOUT-REPORT.md` (mandatory per workflow — schema migrations + API surface change). Use the Story 6.3.1 closeout report as the template. Required content:
   - TL;DR.
   - AC matrix (19/19 with one-liner evidence per AC).
   - Architecture sketch: registry tables + renderer hand-off diagram.
   - "What this unlocks": Stories 6.5c (Capability Catalog Cutover) + 6.5d (Clarification Data Plane).
   - Carry-forward backlog (anything you find that's outside 6.5b/c/d).
   - Risks: variant content drift, GenerationRun snapshot column growth, etc.
   - Green gates: pytest summary + equivalence-diff verdict.
   - Hygiene: stale-field scan output, banner on STORY-6.2-AI-CONTEXT-PACK.md confirmed.
   - Decision: production-ready / merge-recommended / next story = 6.5c.
4. Update `docs/stories/story-6.5b.md` Status to `Ready for UAT` (NOT `Complete` yet — Tony stamps `Complete` after merge per the date-stamp parity rule).
5. Run the SM stale-field audit (`rg` per EPIC-6-WORKFLOW-GUIDE.md §SM stale-field audit).

Then ping Tony (back in the SM chat) with:

- Equivalence-diff report path.
- Gate-evidence path.
- Tony's review checklist: (a) sign off equivalence diff, (b) run alembic upgrade head, (c) verify local generation, (d) flip PR #104 to Ready and merge to develop, (e) wait for Test deploy and run UAT Section 7.

---

## Expected Next-Story Routing

- If 6.5b passes UAT and R6 is verified resolved in Test → SM opens **Story 6.5c — Capability Catalog Cutover** (Block F migration + `ref.BrandPosture` swap-in + `resolve_allowed_components` authoritative).
- If equivalence diff exposes a behavioural delta in A/B/G/I that's hard to reconcile → stop, escalate to SM with the report. Do not merge.
- If R6 reproduces in Test post-deploy → bug fix in same story branch; re-deploy; re-run UAT Section 7. R6 must be closed for 6.5b to be Complete.

---

## What NOT To Do

- Do NOT touch the frontend.
- Do NOT introduce `ref.BrandPosture` or replace the `brandPosture` enum (Story 6.5c).
- Do NOT migrate Block D (locale), E (clarification), F (capability), or H (user prompt) — they stay on existing paths.
- Do NOT run Alembic. Migration files only.
- Do NOT mutate existing migrations. New ones start at 073.
- Do NOT delete `STORY-6.2-AI-CONTEXT-PACK.md` from the repo. Banner only.
- Do NOT push the equivalence-diff report empty or with ⚠️/🔴 verdicts unresolved. The PR cannot move Draft → Ready until Tony signs it off.
- Do NOT chain commands with `&&` in PowerShell. Use `;` if you must chain.
- Do NOT skip the full `python -m pytest` summary capture. Anti-hallucination protocol: if truncated, FAIL.
