# Story 6.5c — Single-Session Dev Prompt

You are implementing **Story 6.5c — Capability Catalog Cutover**.

**Worktree:** `C:\wt\elp\story-epic6-6.5c-capability-catalog-cutover`  
**Branch:** `story/epic6-6.5c-capability-catalog-cutover`  
**PR:** [#106](https://github.com/anthonykeevy/EventLeadPlatform/pull/106) — Draft → `develop`  
**Base:** `develop` at or after merge commit `2a88fd8` (PR #105 — 6.5b closeout)

---

## Mission

One catalog resolver. Four consumers. They must always match.

1. Implement **`resolve_allowed_components`** as the single source of truth (refactor today's `get_allowed_components` SQL in `backend/modules/form_builder/service.py`).
2. Wire Form AI Blocks **F**, **A**, **I** and the **semantic validator** to that resolver — stop using `ComponentCapabilitySnapshot` for allowed types.
3. Migrate **Block F** into the Prompt Assembly Registry (`COMPONENT_CAPABILITY`, dynamic catalog hydration).
4. Add **`ref.BrandPosture`** and re-wire Block **C** variant selection.
5. **Frontend:** toolbox palette only from `POST /api/form-builder/init` `components[]`.

---

## Read First

1. `docs/stories/story-6.5c.md`
2. `docs/stories/story-context-6.5c.xml`
3. `docs/architecture/prompt-assembly-registry-architecture.md` — §2.5, §2.6, §2.7, §8.3
4. `docs/stories/STORY-6.5b-CLOSEOUT-REPORT.md` — registry naming note
5. `backend/modules/form_builder/service.py` — `get_allowed_components`
6. `backend/modules/form_ai/service.py` — snapshot load + `_build_capability_prompt_block`
7. `backend/modules/form_ai/prompt_assembly/` — resolver + renderer from 6.5b
8. `backend/tests/test_form_ai_prompt_capabilities.py`

---

## Step 0 — Preflight

```powershell
.\scripts\workflow\preflight-story.ps1 `
  -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.5c-capability-catalog-cutover" `
  -ExpectedBranch "story/epic6-6.5c-capability-catalog-cutover" `
  -ReportFile "docs/stories/STORY-6.5c-PREFLIGHT.md"
```

Verify PR #106, alembic head `083`, worktree path correct.

---

## Step 1 — Plan (chat, 5–10 bullets)

Cover: module location for resolver, migration list (`084+`), Block F registry row, renderer changes, frontend files for toolbox, snapshot deprecation strategy, AC-15 alignment test approach.

---

## Step 2 — `resolve_allowed_components`

- Extract/refactor catalog query from `get_allowed_components` into shared module.
- Return typed structure (dataclass) with codes + width metadata + init payload fields.
- `get_allowed_components` and `build_init_payload` call resolver only.

---

## Step 3 — Form AI cutover

- Replace snapshot-based allowed list with resolver output in generation path.
- Extend renderer for `DynamicComponentCatalog` — Block F prose shell + injected list.
- Inject same codes into Blocks A/I contract fragments (match current `_build_initial_messages` insertion order).
- Validator uses same object — add test proving mismatch is impossible for fixture catalog.

---

## Step 4 — Registry Block F + migrations

- Seed `PromptSection` `COMPONENT_CAPABILITY` on active `FORM_AI_V1` version.
- Migrations `084+`; Tony runs Alembic — you do not.

---

## Step 5 — `ref.BrandPosture`

- Seed ref table; migrate Company FK; update resolver Block C selection.
- Update API/schemas as needed; frontend picker if in scope.

---

## Step 6 — Frontend toolbox

- Find toolbox palette source; gate on init `components[]` only.
- Re-fetch on context change.

---

## Step 7 — Tests & AC-15

```powershell
python -m pytest backend/tests/test_story_6_5c_*.py backend/tests/test_form_ai_prompt_capabilities.py backend/tests/test_form_ai_prompt_assembly.py --tb=short
python -m pytest --tb=short
```

Add **catalog alignment** test or script: export codes from resolver, from init API, from rendered Block F — assert set equality for AU fixture.

Record in `STORY-6.5c-GATE-EVIDENCE.md`.

---

## Step 8 — Closeout

- `STORY-6.5c-CLOSEOUT-REPORT.md` (mandatory)
- `STORY-6.5c-UAT-RESULTS.md` template pre-filled where possible
- Update `story-6.5c.md` → Ready for UAT (not Complete)
- Do **not** mark PR Ready until Tony UAT

---

## Do NOT

- Run Alembic
- Implement Block E (6.5d)
- Break 6.5b Block G registry / R6 fix
- Use `&&` in PowerShell
