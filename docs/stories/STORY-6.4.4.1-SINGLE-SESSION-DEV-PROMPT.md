# Story 6.4.4.1 Single-Session Dev Prompt

You are implementing **Story 6.4.4.1 — Locale Architecture: Wire the Registry**.

**Worktree:** `C:\wt\elp\story-epic6-6.4.4.1-locale-architecture-wire-registry`
**Branch:** `story/epic6-6.4.4.1-locale-architecture-wire-registry`
**PR:** TBD (Draft PR opened by SM via `new-story.ps1`)
**Base:** `master` (must include the merged closeout amendment from PR #74 and the merged Story 6.4.4 PR #72 with judge JSONs)

---

## Mission

Wire the existing `ref.Country` + `config.ValidationRule` + `config.PromptTemplate(Version)` + `config.PromptAssemblyProfile` registry into the form-AI service. Replace the Python `_LOCALE_PROMPT_BLOCKS` constant with a registry-rendered locale block per request. Add `audienceLocale` + `brandPosture` API parameters with the resolution chain (Event → Company → User → app_setting). Add per-company brand-posture columns. Replace rubric_v1 with rubric_v2 (9 elements; deterministic + LLM-judged). Replace prompts-v1.0 with prompts-v1.1 (270 cells). Swap Gemini judge for Grok 4; pin Claude 4.7. Re-judge baseline as the AC-10 gate.

This is **wiring an existing registry**, not building greenfield. ~70% of the data layer is already built.

---

## Read First (in order)

1. `docs/stories/story-6.4.4.1.md` — story spec + AC-1..16.
2. `docs/stories/story-context-6.4.4.1.xml` — implementation context, dependencies, primary code paths.
3. `docs/stories/STORY-6.4.4.1-LOCALE-ARCHITECTURE-ADR.md` — registry, format/policy/tone split, brand posture, resolution chain rationale.
4. `docs/stories/STORY-6.4.4.1-RUBRIC-V2-ADR.md` — 9-element rubric, calibration anchors, judge swap, AC-10 escape clause.
5. `docs/stories/STORY-6.4.4.1-PROMPTS-V1.1-SPEC.md` — benchmark spec.
6. `_bmad-output/planning-artifacts/STORY-6.4.4.1-SM-HANDOFF-BRIEF.md` — PM authoritative brief (D1-D12).
7. `_bmad-output/research/locale-strategy/00-CONSOLIDATED-RECOMMENDATION.md` — research consolidation.
8. `docs/stories/STORY-6.4.4-CLOSEOUT-AMENDMENT.md` — context for what 6.4.4 left on master.
9. `backend/migrations/versions/053_story_631_form_ai_governance_tables.py` — original `config.PromptTemplate*` schema (FK target).
10. `backend/migrations/versions/054_story_631_seed_governance_baseline.py` — seed pattern reference.
11. `backend/migrations/versions/055_story_631_form_ai_capability_rating_fileupload.py` — capability snapshot evolution pattern (precedent).
12. `backend/modules/form_ai/service.py` — current `_LOCALE_PROMPT_BLOCKS` (~line 1370) and `_build_initial_messages` (~line 1545).
13. `backend/tests/form_ai_eval/run.py` + `judge_pack.py` + `judge_ingest.py` + `prompts.yaml` + `rubric_v1.md` — eval harness.
14. `docs/stories/EPIC-6-WORKFLOW-GUIDE.md` — Multi-Round UAT, Capability Snapshot Rule, Green CI/CD Rule, RequestID lineage.
15. `docs/AGENT-LOGGING-GUIDE.md` — `log.ApiRequest` outbound payloads diagnostic pattern.
16. `docs/FORM-AI-EVAL-JUDGE-WORKFLOW.md` — Cursor judge flow.
17. `docs/FORM-AI-EVAL-DIFF-STATS.md` — diff/statistics tooling for the AC-10 baseline comparison.

---

## Step 0 — Preflight

Run:

```powershell
.\scripts\workflow\preflight-story.ps1 `
  -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.4.4.1-locale-architecture-wire-registry" `
  -ExpectedBranch "story/epic6-6.4.4.1-locale-architecture-wire-registry" `
  -ReportFile "docs/stories/STORY-6.4.4.1-PREFLIGHT.md"
```

Capture: `os.getenv("DATABASE_URL")`, runtime-resolved DB URL, alembic head, branch + worktree parity.

Verify pre-conditions are met **before any code changes**:

- `master` includes commit from PR #74 (closeout amendment + rubric_v1 supersession footer).
- `master` includes commit from PR #72 merged (with the 12 live judge JSONs under `_bmad-output/eval-runs/story-6.4.4-live-baseline-vs-{h1,h2,h4,combined}/`).
- `gh pr view 74 --json state,mergedAt` shows `MERGED`.
- `gh pr view 72 --json state,mergedAt` shows `MERGED`.
- `git log --oneline master | head -5` includes both merge commits.

If any of these fails, STOP and notify Human. Do not proceed.

---

## Step 1 — Migrations 063–071 (apply in order)

Implement **9 alembic migrations** (template style: copy `054_story_631_seed_governance_baseline.py` for seeds; `053_story_631_form_ai_governance_tables.py` for new tables).

| # | File | What |
|---|---|---|
| 063 | `063_story_6441_prompt_template_locale_block.py` | Create `config.PromptTemplateLocaleBlock` table per ADR D11(b). PK, FKs to `config.PromptTemplate` and `ref.Country` (nullable for NEUTRAL fallback), `BlockType` (check constraint `IN ('format','policy','tone')`), `BlockBody` (`nvarchar(max)`), `ContentHash` (varchar 64), `IsActive`, audit columns. Unique constraint on `(PromptTemplateID, CountryID, BlockType)` where `IsActive = 1`. Down: drop. |
| 064 | `064_story_6441_country_cultural_dimensions.py` | Create `ref.CountryCulturalDimensions` per ADR D12(b). One row per CountryID. Six Hofstede dimension columns nullable, `Source`, `SourceYear`, audit. Down: drop. |
| 065 | `065_story_6441_seed_locale_blocks_au.py` | Insert AU format + policy + tone rows for `FORM_AI_STEP1_BASE` template (CountryID = AU). Reference current AU prompt block (deleted in step 2 below). Tonyk-reviewed. Down: delete by `(PromptTemplateID, CountryID, BlockType)`. |
| 066 | `066_story_6441_seed_locale_blocks_nz_uk_us_ca_ie.py` | Same shape, NZ/UK/US/CA/IE — pre-reviewed quality (LLM-drafted; Tonyk-skim before merge). Down: delete by composite key. |
| 067 | `067_story_6441_seed_locale_blocks_intl_online.py` | INTL_ONLINE: ISO 8601 dates, E.164 phone, single-line address with required Country, English-neutral spelling. CountryID null is acceptable; create a synthetic INTL_ONLINE Country row first if needed (or use `null` CountryID). Down: delete. |
| 068 | `068_story_6441_seed_country_cultural_dimensions.py` | Hofstede 6D for 7 MVP markets; DE/JP/FR stubs with `Source = 'Hofstede 6D 2010, requires native review'`. Use canonical published values (cite source in migration docstring). Down: delete. |
| 069 | `069_story_6441_generation_run_brand_posture.py` | `ALTER TABLE dbo.GenerationRun ADD BrandPosture VARCHAR(40) NULL`, `BrandHeritageOrigin VARCHAR(5) NULL`. Add check constraint on BrandPosture. Down: drop columns. |
| 070 | `070_story_6441_company_brand_posture.py` | `ALTER TABLE dbo.Company ADD BrandPosture VARCHAR(40) NULL`, `BrandHeritageOrigin VARCHAR(5) NULL`. Same check. Down: drop columns. |
| 071 | `071_story_6441_app_settings_locale_defaults.py` | Insert 3 `config.AppSetting` rows: `form_ai.default_audience_locale = 'AU'`, `form_ai.default_brand_posture = 'local'`, `form_ai.locale_block_render_strategy = 'registry'`. Down: delete by key. |

After migrations:

- Run `python -m alembic upgrade head` and `python -m alembic downgrade -1` round-trip for each migration in turn (or use the migration test harness if present).
- Confirm head matches expected revision in preflight report.

---

## Step 2 — Service refactor (`backend/modules/form_ai/service.py`)

1. **Delete** `_LOCALE_PROMPT_BLOCKS["AU"]` constant (~line 1370). Delete `_build_locale_prompt_block` if it was only the AU lookup.
2. **Add** `_assemble_locale_block(audience_locale: str, brand_posture: str | None, db_session) -> str`:
   - Resolve `audience_locale` → `CountryID` via `ref.Country.ISO2Code` (handle `INTL_ONLINE` / `EU` / `APAC` / `NEUTRAL` synthetic values explicitly — see ADR §3.2).
   - Query active `config.PromptTemplateLocaleBlock` rows for `(active template, CountryID, IsActive=1)` — three rows expected (`format`, `policy`, `tone`).
   - Concatenate in order `format → policy → tone`.
   - Cache by `(template_version, country_id)` for 5 minutes via process-local dict + monotonic clock. Invalidate on test setup.
   - Fallback: if no rows found → render NEUTRAL block (CountryID null) → `log.ApplicationError` severity `info`.
3. **Add** `_resolve_audience_locale(request, current_user, event_id, db_session) -> str`:
   - Order: `request.audienceLocale` (validated against enum) → `Event.CountryID` (when `event_id` present) → `Company.CountryID` (current user's company) → `User.CountryID` → `app_setting('form_ai.default_audience_locale')` → `'AU'`.
   - Return ISO2 enum value.
4. **Add** `_resolve_brand_posture(request, current_user, db_session) -> tuple[str, str | None]`:
   - Order: `request.brandPosture / brandHeritageOrigin` → `Company.BrandPosture / Company.BrandHeritageOrigin` → `('local', None)`.
   - Validate enum.
5. **Update** `_build_initial_messages` (~line 1545):
   - Accept `audience_locale`, `brand_posture`, `brand_heritage_origin` parameters.
   - Call `_assemble_locale_block` and inject the block in place of the deleted Python constant.
   - Position block **last in the cacheable system-prompt prefix** (per Memo 3 — preserves cache hit on stable portion).
6. **Update** `dbo.GenerationRun` create flow to persist `BrandPosture` and `BrandHeritageOrigin`.

---

## Step 3 — API surface

`backend/modules/form_ai/router.py` (or equivalent endpoint module):

- Form-AI generation request schema gains optional `audienceLocale: AudienceLocaleEnum`, `brandPosture: BrandPostureEnum`, `brandHeritageOrigin: str | None`.
- Endpoint resolves via `_resolve_*` helpers, passes to service.
- Add `meta.locale = { resolved: 'AU', source: 'Event.CountryID' }` to the response for debuggability (small addition; check schema test impact).

`backend/models/generation_run.py` and `backend/models/company.py` get the new attributes mirroring migrations 069 and 070.

---

## Step 4 — Frontend pass-through

`frontend/src/.../FormAiPanel.tsx` (or wherever the AI panel currently calls `/api/form-ai/*`):

- Forward `audienceLocale` and `brandPosture` from app context (existing `/api/me` + company data) on every form-AI generation request.
- **No UI redesign** — defaults-only pass-through. Do not add a dropdown in this story.
- Verify network tab shows the new params on every call.

---

## Step 5 — Rubric v2

- Create `backend/tests/form_ai_eval/rubric_v2.md` per the ADR §4 anchor table (9 elements).
- Embed Tonyk's lived-AU calibration anchors verbatim from ADR §5.
- Update `judge_pack.py` to package `rubric_v2.md` instead of v1, and to inject the "name at least one weakness per row before scoring" calibration nudge into the per-judge prompt template.

---

## Step 6 — Benchmark v1.1

- Replace `backend/tests/form_ai_eval/prompts.yaml` with the v1.1 spec from `STORY-6.4.4.1-PROMPTS-V1.1-SPEC.md`.
- 15 prompts × 6 locales × 3 reps = 270 rows; each row carries explicit `audienceLocale` field.
- Document the v1.0 → v1.1 migration in `docs/FORM-AI-EVAL-HARNESS.md`.

---

## Step 7 — Judge swap + ingest schema bump

`backend/tests/form_ai_eval/judge_ingest.py`:

- Add `rubric_v2` path: 9 metric keys; deterministic items 0/1/2; LLM-judged items 0/1/2; cross-locale leakage 0/2.
- Require `judge_model_version` field on every judge output; reject otherwise.
- Compute primary mean as **Claude + Grok mean** (Gemini path retired).
- GPT-5 mini bias delta computation unchanged in shape.
- Preserve v1 path for the 6.4.4 historical files (version-gated).

`docs/stories/STORY-6.4.4.1-JUDGE-PROMPTS.md`:

- Pin Claude 4.7 explicitly (e.g. `claude-4.7-sonnet-20260315`).
- Add Grok 4 prompt (replaces Gemini's prompt).
- Pin GPT-5 mini version.
- Embed the calibration nudge in all three prompts.
- Clarify required JSON shape including the new `judge_model_version` field.

---

## Step 8 — Tests

Add focused tests:

- `backend/tests/test_form_ai_locale_assembly.py`:
  - `_assemble_locale_block` registry hit (AU, NZ, INTL_ONLINE).
  - Cache hit (second call within 5 min returns cached value).
  - NEUTRAL fallback when CountryID has no rows.
  - Mock `log.ApplicationError` to verify info-severity log.
- `backend/tests/test_form_ai_locale_resolution.py`:
  - Resolution chain order: explicit > event > company > user > app_setting > 'AU'.
  - Invalid enum → `ValidationError`.
- `backend/tests/test_eval_judge_ingest_v2.py`:
  - Happy path: rubric_v2 + judge_model_version present → ingest succeeds.
  - Missing `judge_model_version` → reject.
  - Unknown metric key → reject.
  - Out-of-range score → reject.
  - v1 backwards-compat: existing v1 file still ingests via v1 path.
- Migration round-trip tests: `tests/test_migration_063_071_round_trip.py` (or harness equivalent).

Run focused tests; if any fail, fix and re-run.

---

## Step 9 — AC-10 baseline re-judge under rubric_v2

This is partly Tonyk-time (Cursor judge runs):

1. Run a fresh baseline eval on `prompts-v1.1` against the new prompt assembly (registry-rendered): `python -m backend.tests.form_ai_eval.run --benchmark prompts-v1.1 --variant rubric-v2-baseline`.
2. Generate the judge package via `judge_pack.py` (which now embeds `rubric_v2.md` and the calibration nudge).
3. Tonyk runs three Cursor judge sessions (Claude 4.7, Grok 4, GPT-5 mini); JSON outputs land in `_bmad-output/eval-runs/<run-id>/judge-package/results/`.
4. `python -m backend.tests.form_ai_eval.judge_ingest --run-id <run-id>`.
5. Inspect ingest summary against AC-10 gate:
   - **Pass:** Grok 4 mean drops below 5.00 AND each judge scores ≥1 cell below 4 → AC-10 met. Continue to closeout.
   - **Fail (ceiling-lock):** all three judges still produce 5/5 across every cell → AC-10 escape clause:
     - One calibration tweak round (rubric anchor sharpening — change one anchor to a sharper threshold) per Multi-Round UAT Protocol; one variable per round; RequestID lineage in `STORY-6.4.4.1-UAT-RESULTS.md`.
     - Re-run; re-judge.
     - If still ceiling-locked: register `JUDGE-ARCHITECTURE-RE-INVESTIGATION` as a P0 carry-forward in `EPIC-6-CARRY-FORWARD-BACKLOG.md`; close the story (architecture work is not blocked); move on.

Document outcome in `STORY-6.4.4.1-UAT-RESULTS.md` (round-by-round table; single variable per round).

---

## Step 10 — Green CI/CD gate

```powershell
.\scripts\workflow\run-green-gate.ps1 `
  -StoryId "6.4.4.1" `
  -FocusedTestCommand "python -m pytest backend/tests/test_form_ai_locale_assembly.py backend/tests/test_form_ai_locale_resolution.py backend/tests/test_eval_judge_ingest_v2.py --tb=short" `
  -BackendGateCommand "python -m pytest backend/tests --tb=short" `
  -EvidenceFile "docs/stories/STORY-6.4.4.1-GATE-EVIDENCE.md"
```

Frontend:

```powershell
cd frontend; npm run lint; npm run test:unit -- --watch=false; cd ..
```

**Anti-Hallucination Protocol** (per Workflow Guide §🛑): if test output is truncated or hangs, treat as FAILED. Don't end the turn until you can read `=== X passed, Y failed ===` in full.

---

## Step 11 — Closeout artefacts

- `STORY-6.4.4.1-CLOSEOUT-REPORT.md` — mandatory (migrations + new public API surface). Use Story 6.3.1 closeout as the canonical template.
- `STORY-6.4.4.1-GATE-EVIDENCE.md` — AC-by-AC mapping + gate outputs.
- `STORY-6.4.4.1-UAT-RESULTS.md` — round-by-round table.
- Update `docs/stories/EPIC-6-STATUS.md` — add Story 6.4.4.1 row.
- Update `docs/stories/EPIC-6-WORKFLOW-GUIDE.md` — Current Focus = next story (6.4.4.2 conditional or 6.4.5 H3).
- Update `docs/stories/EPIC-6-CARRY-FORWARD-BACKLOG.md` — register: company brand settings UI; native-speaker review of DE/JP/FR; per-form locale dropdown; (conditional) judge architecture re-investigation if AC-10 escape invoked.

---

## Step 12 — Stale-field audit + push

Per Workflow Guide §🔍 SM stale-field audit:

```powershell
gh pr view <PR#> --json state,isDraft,mergedAt,headRefName,baseRefName,url
rg -n "Draft|Ready for UAT|Keep PR .* open|Current Focus" docs/stories/story-6.4.4.1.md docs/stories/STORY-6.4.4.1-CLOSEOUT-REPORT.md docs/stories/EPIC-6-STATUS.md docs/stories/EPIC-6-WORKFLOW-GUIDE.md
```

Fix any drift in a final SM housekeeping commit. Push. Mark PR Ready for review (un-Draft).

---

## Constraints (do NOT break)

- **No mocking the database in migration tests.** Real SQL Server (or test SQLite if that's the harness convention).
- **No cross-comparison of rubric_v1 and rubric_v2 scores anywhere.** They are different measurements.
- **No re-introducing Gemini to the judge panel.** Grok 4 replaces it permanently.
- **No UI redesign for `audienceLocale`/`brandPosture`.** Pass-through only; per-form override is a future story.
- **No skipping pre-review of NZ/UK/US/CA/IE/INTL_ONLINE locale blocks.** Tonyk requires pre-reviewed quality for all 7 MVP markets.
- **No new dependencies for caching.** Process-local dict + monotonic clock is enough.
- **No capability snapshot bump.** Renderer manifests are unchanged.
- **No AC-10 indefinite block.** If escape clause invoked, register carry-forward and close.

---

## Done when

- All 16 ACs green or escape-clause-documented (AC-10).
- Both ADRs committed.
- Migrations 063–071 applied in order; round-trip tested.
- Service refactor complete; `_LOCALE_PROMPT_BLOCKS` deleted.
- Frontend pass-through visible in network tab.
- Rubric v2 + benchmark v1.1 + judge prompts committed.
- Ingest schema bump tested.
- Green CI/CD evidence in `STORY-6.4.4.1-GATE-EVIDENCE.md`.
- AC-10 baseline re-judged or escape clause carry-forward registered.
- Closeout report + status/workflow doc updates committed.
- SM stale-field audit clean.
- PR un-Drafted.
