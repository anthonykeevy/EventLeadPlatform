# Story 6.5b — Gate Evidence

**Date:** 2026-05-20  
**Branch:** `story/epic6-6.5b-registry-foundation` (worktree `C:\wt\elp\story-epic6-6.5b-registry-foundation`)  
**PR:** [#104](https://github.com/SignalPlatforms/EventLeadPlatform/pull/104) — **merged to `develop`** (2026-05-20T04:30:52Z)  
**Base commit:** `cb339ed` (origin/develop at story start)  
**Merge commit on `develop`:** `1375e72`

---

## Section 1 — AC mapping

| AC | Statement | Evidence |
|----|-----------|----------|
| AC-1 | Migration creates `config.PromptAssemblyRegistry`, `PromptAssemblyRegistryVersion`, `PromptSection`, `PromptSectionVariant`, `PromptSectionData`. | `backend/migrations/versions/078_story_6_5b_prompt_assembly_registry_schema.py` |
| AC-2 | `FORM_AI_V1` registry seeded with active VersionNumber=1 and 5 sections (A, B, C, G, I). | `backend/migrations/versions/079_story_6_5b_seed_form_ai_v1_profile.py` |
| AC-3 | Block A (`ROLE_CONTRACT`), B (`SAFETY`), I (`JSON_OUTPUT`), and four Block C variants (`local`/`heritage`/`neutral`/`transcreate`) seeded; `local` IsDefault=1. | `backend/migrations/versions/080_story_6_5b_seed_variants_a_b_c_i.py` |
| AC-4 | Block G (`FEW_SHOT`) seeded from inlined trimmed `STORY-6.2-AI-CONTEXT-PACK.md` content; migration self-contained (no on-disk file read at runtime). | `backend/migrations/versions/081_story_6_5b_seed_block_g_context_pack.py` |
| AC-5 | `dbo.GenerationRun` extended with nullable `PromptAssemblyRegistryVersionID BIGINT` (FK) and `PromptVariantSnapshot NVARCHAR(MAX)`. | `backend/migrations/versions/082_story_6_5b_generation_run_assembly_audit.py` |
| AC-6 | `resolve_prompt_assembly()` selects active version, picks Block C variant by `brand_posture`, falls back to `IsDefault`. | `backend/modules/form_ai/prompt_assembly/resolver.py` + `tests/test_story_6_5b_registry_resolver.py` (7/7 PASS) |
| AC-7 | `render_prompt_assembly()` substitutes only declared placeholders (`{heritageOrigin}`); leaves unrelated braces untouched. | `backend/modules/form_ai/prompt_assembly/renderer.py` + `tests/test_story_6_5b_renderer.py` (8/8 PASS) |
| AC-8 | `_build_initial_messages` consumes `RenderedAssembly` and emits Block A/B/C/G/I from registry; falls back to canonical seeds when no DB session is provided (test compatibility). | `backend/modules/form_ai/service.py` (`_build_initial_messages`, `_resolve_rendered_assembly`, `_build_canonical_rendered_assembly`) |
| AC-9 | `_load_context_pack()` removed; runtime no longer reads `STORY-6.2-AI-CONTEXT-PACK.md` from disk. | service.py diff vs cb339ed (function gone, constants gone, `from pathlib import Path` removed) + `tests/test_story_6_5b_equivalence.py::test_assembly_does_not_read_context_pack_from_disk` (PASS) |
| AC-10 | `generate_form_definition()` resolves the assembly once per run and persists `PromptAssemblyRegistryVersionID` + `PromptVariantSnapshot` JSON onto `dbo.GenerationRun`. | service.py (`_resolve_rendered_assembly`, `_persist_generation_run_and_artifacts`, `_build_prompt_variant_snapshot`) |
| AC-11 | Resolver raises `LookupError` when no active registry version exists; service maps it to `prompt-assembly-resolution-failed` terminal reason. | resolver.py + service.py + `tests/test_story_6_5b_registry_resolver.py::test_resolver_raises_lookup_error_when_registry_inactive` (PASS) |
| AC-12 | `PromptVariantSnapshot` payload contains the resolved variant IDs for every emitted section, keyed by `SectionCode`. | `_build_prompt_variant_snapshot` (service.py) + handoff doc verification SELECT |
| AC-13 | Resolver test fixture is dialect-agnostic (SQLite in-memory) and isolates the suite from the live database. | `tests/test_story_6_5b_registry_resolver.py::registry_db` fixture |
| AC-14 | Migration set has working `downgrade()` chain back to `074`. | `tests/test_story_6_5b_migrations_static.py` (15/15 PASS, including `test_migration_chain_links_in_order`) |
| AC-15 | Eval harness updated to call resolver/renderer the same way runtime does (no direct context-pack import). | `backend/tests/form_ai_eval/au_diagnostics.py` diff |
| AC-16 | Historical Story 6.2 prompt-eval helper neutralised (R6 obsoletes its file-based context-pack tightening). | `backend/scripts/story_6_2_prompt_eval.py::_tighten_context_pack` returns `RuntimeError` shim |
| AC-17 | `STORY-6.2-AI-CONTEXT-PACK.md` carries a "documentation only" banner pointing at the registry. | `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md` (banner at top) |
| AC-18 | `EPIC-6-STATUS.md` row 6.5b moved to "Ready for UAT"; `EPIC-6-WORKFLOW-GUIDE.md` Current Focus updated; R6 marked "Resolved by 6.5b" pending Test verification. | `docs/stories/EPIC-6-STATUS.md`, `docs/stories/EPIC-6-WORKFLOW-GUIDE.md` |
| **AC-19** | **Prompt-equivalence diff is byte-identical for unchanged inputs across all four brand postures.** | **`docs/stories/STORY-6.5b-PROMPT-EQUIVALENCE-DIFF.md` — verdict: PASS (20/20 IDENTICAL).** Tony sign-off **done** (2026-05-20). |

---

## Section 2 — Test execution

### 2.1 Story 6.5b focused suite (39/39 PASS)

```
$env:PYTHONPATH = "C:\wt\elp\story-epic6-6.5b-registry-foundation\backend"
cd C:\wt\elp\story-epic6-6.5b-registry-foundation\backend
pytest tests/test_story_6_5b_registry_resolver.py `
       tests/test_story_6_5b_renderer.py `
       tests/test_story_6_5b_equivalence.py `
       tests/test_story_6_5b_migrations_static.py -q
```

Result:

```
============================ 39 passed, 177 warnings in 1.55s ============================
```

Breakdown:

| File | Tests | Passed |
|------|-------|--------|
| `test_story_6_5b_registry_resolver.py` | 7 | 7 |
| `test_story_6_5b_renderer.py` | 8 | 8 |
| `test_story_6_5b_equivalence.py` | 8 | 8 |
| `test_story_6_5b_migrations_static.py` | 16 | 16 |
| **Total** | **39** | **39** |

### 2.2 form_ai regression suite (26 pass, 7 pre-existing fail — see § 2.3)

```
pytest tests/test_form_ai_first_shot.py `
       tests/test_form_ai_locale_assembly.py `
       tests/test_form_ai_locale_resolution.py `
       tests/test_form_ai_prompt_capabilities.py `
       tests/test_story_63_context_pack_path.py -q
```

Result: `26 passed, 7 failed`. **All 7 failures are pre-existing.**

### 2.3 Pre-existing baseline failures (not introduced by 6.5b)

All seven failures share signature `AttributeError: 'str' object has no attribute 'content'` at `service.py:4041`:

```python
provider_content = provider_completion.content
```

The tests monkeypatch `_request_chatgpt_completion` to return a bare `str` (e.g. `"this is not json at all"` or `json.dumps(valid)`), but production code expects a `ProviderCompletion` dataclass with a `.content` attribute. The mismatch exists at base commit `cb339ed` — verified by:

```powershell
git show cb339ed:backend/modules/form_ai/service.py | Select-String "provider_completion\.content"
# returns: provider_content = provider_completion.content
git show cb339ed:backend/tests/test_form_ai_first_shot.py | Select-String "_request_chatgpt_completion" -Context 2
# returns: same monkeypatch returning bare str
```

Affected tests (all pre-existing on `develop`):

- `test_form_ai_first_shot.py::test_max_correction_zero_issues_only_one_provider_call`
- `test_form_ai_first_shot.py::test_system_prompt_addendum_in_system_message`
- `test_story_63_context_pack_path.py::test_generate_uses_system_user_message_split`
- `test_story_63_context_pack_path.py::test_compiler_keeps_submit_button_within_canvas`
- `test_story_63_context_pack_path.py::test_compiler_grows_canvas_for_tall_forms`
- `test_story_63_context_pack_path.py::test_compiler_places_submit_after_content_block`
- `test_story_63_context_pack_path.py::test_post_process_position_deltas_recorded_in_trace`

**Decision:** Out of scope for 6.5b. Suggest spinning a small follow-up story to update these test mocks to return a `ProviderCompletion` instance (or fixture). Equivalence diff (AC-19) confirms behaviour for the production path is unchanged.

---

## Section 3 — AC-19 prompt-equivalence diff (gate artefact)

### 3.1 Generator script

```
backend/scripts/story_6_5b_prompt_equivalence_diff.py
```

Inlines the legacy `_build_initial_messages_legacy` (the pre-6.5b literal-based assembly), runs both old and new for all four brand postures, slices each system message into Blocks A / B / C / G / I / D_HEADER, and reports `IDENTICAL` / `WHITESPACE` / `CONTENT` per block.

Run command:

```powershell
$env:PYTHONPATH = "C:\wt\elp\story-epic6-6.5b-registry-foundation\backend"
cd C:\wt\elp\story-epic6-6.5b-registry-foundation\backend
python scripts/story_6_5b_prompt_equivalence_diff.py `
  --output ../docs/stories/STORY-6.5b-PROMPT-EQUIVALENCE-DIFF.md
```

### 3.2 Result summary

From `docs/stories/STORY-6.5b-PROMPT-EQUIVALENCE-DIFF.md` (commit `e1d9fbb`, generated 2026-05-20T03:01:57Z):

| Posture | A | B | I | G | C |
|---------|---|---|---|---|---|
| local | IDENTICAL | IDENTICAL | IDENTICAL | IDENTICAL | IDENTICAL |
| heritage | IDENTICAL | IDENTICAL | IDENTICAL | IDENTICAL | IDENTICAL |
| neutral | IDENTICAL | IDENTICAL | IDENTICAL | IDENTICAL | IDENTICAL |
| transcreate | IDENTICAL | IDENTICAL | IDENTICAL | IDENTICAL | IDENTICAL |

**Verdict: PASS.** No `WHITESPACE` and no `CONTENT` deltas in any in-scope block across any posture. `D_HEADER` is also `IDENTICAL` for all four postures (Block D moves into the registry in 6.5c, so equivalence here is incidental but reassuring).

### 3.3 Tony sign-off (complete)

All three checkboxes at the top of `STORY-6.5b-PROMPT-EQUIVALENCE-DIFF.md` are ticked (2026-05-20). PR #104 merged to `develop`.

---

## Section 4 — R6 closure evidence

R6 was opened on PR #101 ("`context-pack-load-failed` on Azure Test environment due to read of `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md` outside the deployed package").

After 6.5b:

- `_load_context_pack()` and the module-level `CONTEXT_PACK_PATH` / `_ROOT_PATH` constants are deleted from `service.py`. Verified by `tests/test_story_6_5b_equivalence.py::test_assembly_does_not_read_context_pack_from_disk`.
- Block G prose is sourced from `config.PromptSectionVariant.PromptSnippet` seeded by migration `081_story_6_5b_seed_block_g_context_pack.py`. The migration body inlines the trimmed prose as a Python string literal computed offline at base commit `cb339ed`.
- `tests/test_story_6_5b_equivalence.py::test_block_g_migration_081_does_not_read_context_pack_at_runtime` AST-parses the migration and asserts no executable code path reads the markdown file from disk.
- `STORY-6.2-AI-CONTEXT-PACK.md` carries a banner declaring it documentation-only.
- `backend/scripts/story_6_2_prompt_eval.py::_tighten_context_pack` raises `RuntimeError` to surface obsolete callsites.

R6 is **functionally closed**. The status flips ✅ on `EPIC-6-STATUS.md` only after Tony deploys to Azure Test and confirms the `context-pack-load-failed` terminal reason no longer appears.

---

## Section 5 — Migration handoff

See `docs/stories/STORY-6.5b-MIGRATION-HANDOFF.md` for:

- Migration list (078 → 082) with rows-affected counts.
- Step-by-step `alembic upgrade head` procedure.
- Per-migration verification SELECTs for LocalDB.
- Post-migration smoke test (uvicorn + frontend) and `dbo.GenerationRun` audit-column verification.
- Rollback plan (`alembic downgrade 074`).

---

## Section 6 — Unfinished / Tony to execute

| Item | Owner | Status |
|------|-------|--------|
| Run `alembic upgrade head` against LocalDB (072 → 083) | Tony | **Done** (2026-05-20, head `083` incl. Block A trim) |
| Run verification SELECTs from migration handoff doc | Tony | Partial — agent confirmed 8 variants + resolver OK; Tony to confirm Block G len/marker in SSMS |
| Local smoke test: uvicorn + frontend, generate form draft, confirm no `context-pack-load-failed` | Tony | **Done** (2026-05-20; GenerationRunID **163**, `validated-success`) |
| Confirm `dbo.GenerationRun.PromptAssemblyRegistryVersionID` populated post-generation | Tony | **Done** (`PromptAssemblyRegistryVersionID`=1, `SnapshotLen`=130) |
| Tick three sign-off checkboxes on `STORY-6.5b-PROMPT-EQUIVALENCE-DIFF.md` | Tony | **Done** |
| Merge PR #104 into `develop`; CI/CD deploys to Azure Test | Tony | **Done** (2026-05-20) |
| Verify R6 resolved on deployed Test environment (no `context-pack-load-failed`) | Tony | **Done** — `validated-success` on Test |
| Flip `EPIC-6-STATUS.md` row 6.5b → ✅ Complete | Tony | **Done** |

---

## Section 7 — Open follow-ups for Story 6.5c

- **Naming reconciliation:** Architecture doc uses `PromptAssemblyProfile*`; implementation uses `PromptAssemblyRegistry*` to avoid collision with existing `config.PromptAssemblyProfile` (Story 6.3.1 governance step profile, FK'd from `dbo.GenerationRun.PromptAssemblyProfileID`). 6.5c is the natural place to choose a final name.
- **Capability cutover:** 6.5c will make `resolve_allowed_components` authoritative for Block A/F/I and toolbox; Block A's seeded prose may shrink as a result.
- **Block D into registry:** Architecture envisions Block D living in the registry too. Currently `_assemble_locale_block` produces it in `service.py`; 6.5c can land that.

---

## Section 8 — Appendix: file inventory

### 8.1 New files

```
backend/migrations/versions/078_story_6_5b_prompt_assembly_registry_schema.py
backend/migrations/versions/079_story_6_5b_seed_form_ai_v1_profile.py
backend/migrations/versions/080_story_6_5b_seed_variants_a_b_c_i.py
backend/migrations/versions/081_story_6_5b_seed_block_g_context_pack.py
backend/migrations/versions/082_story_6_5b_generation_run_assembly_audit.py
backend/migrations/versions/083_story_6_5b_trim_block_a_role_contract.py
backend/models/config/prompt_assembly_registry.py
backend/models/config/prompt_assembly_registry_version.py
backend/models/config/prompt_section.py
backend/models/config/prompt_section_data.py
backend/models/config/prompt_section_variant.py
backend/modules/form_ai/prompt_assembly/__init__.py
backend/modules/form_ai/prompt_assembly/canonical_seeds.py
backend/modules/form_ai/prompt_assembly/renderer.py
backend/modules/form_ai/prompt_assembly/resolver.py
backend/scripts/story_6_5b_prompt_equivalence_diff.py
backend/tests/test_story_6_5b_equivalence.py
backend/tests/test_story_6_5b_migrations_static.py
backend/tests/test_story_6_5b_registry_resolver.py
backend/tests/test_story_6_5b_renderer.py
docs/stories/STORY-6.5b-MIGRATION-HANDOFF.md
docs/stories/STORY-6.5b-PROMPT-EQUIVALENCE-DIFF.md
docs/stories/STORY-6.5b-GATE-EVIDENCE.md          # this file
```

### 8.2 Modified files

```
backend/models/__init__.py
backend/models/config/__init__.py
backend/models/generation_run.py
backend/modules/form_ai/service.py
backend/scripts/story_6_2_prompt_eval.py
backend/tests/form_ai_eval/au_diagnostics.py
backend/tests/form_ai_eval/au_locale_contract_v1.json
docs/stories/EPIC-6-STATUS.md
docs/stories/EPIC-6-WORKFLOW-GUIDE.md
docs/stories/STORY-6.2-AI-CONTEXT-PACK.md
```
