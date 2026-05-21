# Story 6.5c — Gate Evidence



**Date:** 2026-05-20  

**Branch:** `story/epic6-6.5c-capability-catalog-cutover`  

**Alembic head (pre-migration):** `083` → new revisions `084`–`086`



## Preflight



- `scripts/workflow/preflight-story.ps1` — **PASS** (`docs/stories/STORY-6.5c-PREFLIGHT.md`)

- PR [#106](https://github.com/anthonykeevy/EventLeadPlatform/pull/106) — Draft → `develop`

- Worktree: `C:\wt\elp\story-epic6-6.5c-capability-catalog-cutover`



## Targeted pytest (Story 6.5c + 6.5b regression)



```powershell

cd backend

python -m pytest tests/test_story_6_5c_component_catalog.py tests/test_story_6_5c_catalog_alignment.py tests/test_story_6_5c_migrations_static.py tests/test_story_6_5c_prompt_renderer.py tests/test_form_ai_prompt_capabilities.py tests/test_story_6_5b_registry_resolver.py tests/test_story_6_5b_equivalence.py --tb=short -q

```



**Result:** 35 passed



## AC-15 catalog alignment



`tests/test_story_6_5c_catalog_alignment.py::test_catalog_alignment_init_prompt_validator_codes_match` asserts set equality for AU fixture:



- `get_allowed_components` / init shape

- `resolve_allowed_components` codes

- Block F rendered list (`build_capability_prompt_block_from_catalog`)

- Semantic validator accepts only catalog codes



## Migrations (Tony executes)



```powershell

cd backend

alembic upgrade head

```



Expected new head: `086`



| Rev | Purpose |

|-----|---------|

| 084 | `ref.BrandPosture` + seed |

| 085 | `Company.BrandPostureID` FK + backfill |

| 086 | Block F `COMPONENT_CAPABILITY` / `DynamicComponentCatalog` |



### Migrations executed (Tony, LocalDB)



```

alembic upgrade head

INFO  [alembic.runtime.migration] Context impl MSSQLImpl.

INFO  [alembic.runtime.migration] Will assume transactional DDL.

INFO  [alembic.runtime.migration] Running upgrade 083 -> 084, Story 6.5c: ref.BrandPosture table + seed.

INFO  [alembic.runtime.migration] Running upgrade 084 -> 085, Story 6.5c: Company.BrandPostureID FK to ref.BrandPosture.

INFO  [alembic.runtime.migration] Running upgrade 085 -> 086, Story 6.5c: Block F COMPONENT_CAPABILITY registry section + prose shell.

```



**Head after apply:** `086`



## Full suite



Background run (~18 min): **712 passed**, 74 failed, 107 errors (exit 1).



Failures cluster in MSSQL integration tests (`test_story_1_11_*`, `test_story_622_*`) with `42S22 Invalid column name` — likely test DB/fixture schema drift after `Company.BrandPostureID` model addition, not Story 6.5c catalog logic. **Story 6.5c + 6.5b regression: 35/35 passed** (re-run after migration fix).



## UAT



See `STORY-6.5c-UAT-TEST-GUIDE.md` — **All sections Pass** (LocalDB + Azure Test, Tony sign-off 2026-05-21).



Key UAT evidence:



- Country scope: `divider` scoped Country/AU — absent UK toolbox (form 813), present AU (form 504); reverted to Global.

- Brand posture API: GenerationRuns **168** (neutral), **169** (heritage/US) — Block C variants match request.

