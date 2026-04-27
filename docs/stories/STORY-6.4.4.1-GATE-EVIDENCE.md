# Story 6.4.4.1 Gate Evidence

## Automated Checks

### Targeted Backend

Command:

```powershell
python -m py_compile backend\modules\form_ai\service.py backend\modules\form_ai\schemas.py backend\modules\form_ai\router.py backend\tests\form_ai_eval\run.py backend\tests\form_ai_eval\judge_pack.py backend\tests\form_ai_eval\judge_ingest.py backend\tests\form_ai_eval\diff.py backend\migrations\versions\063_story_6441_prompt_template_locale_block.py backend\migrations\versions\064_story_6441_country_cultural_dimensions.py backend\migrations\versions\065_story_6441_seed_locale_blocks_au.py backend\migrations\versions\066_story_6441_seed_locale_blocks_nz_uk_us_ca_ie.py backend\migrations\versions\067_story_6441_seed_locale_blocks_intl_online.py backend\migrations\versions\068_story_6441_seed_country_cultural_dimensions.py backend\migrations\versions\069_story_6441_generation_run_brand_posture.py backend\migrations\versions\070_story_6441_company_brand_posture.py backend\migrations\versions\071_story_6441_app_settings_locale_defaults.py
python -m pytest backend/tests/test_story_6441_migrations_static.py backend/tests/test_form_ai_locale_assembly.py backend/tests/test_form_ai_locale_resolution.py backend/tests/test_form_ai_prompt_capabilities.py backend/tests/test_story_631_form_ai_governance_api.py backend/tests/test_story_631_governance_persistence.py backend/tests/test_form_ai_eval_harness.py backend/tests/test_judge_pack.py backend/tests/test_judge_ingest.py --tb=short
```

Result: `44 passed`.

### Full Backend

Command:

```powershell
python -m pytest backend/tests --tb=short
```

Result after Anthony applied migrations `063`-`071` and stale Story 6.4.4 locale tests were updated for Story 6.4.4.1: `793 passed, 26 skipped`.

### Frontend

Command:

```powershell
cd frontend; npm run lint
npm run test:unit -- --watch=false
```

Result after `frontend/node_modules` was installed in the worktree:

- `npm run lint`: pass.
- `npm run test:unit -- --watch=false`: `283 passed`.

## AC Mapping

- Locale registry migrations 063-071: covered by static migration tests and Python compile.
- Runtime registry assembly/cache/fallback: covered by `test_form_ai_locale_assembly.py`.
- audienceLocale / brandPosture resolution: covered by `test_form_ai_locale_resolution.py`.
- API pass-through and persistence params: covered by governance API/persistence tests.
- Benchmark v1.1 and rubric v2 judge pipeline: covered by eval harness, judge pack, judge prompts doc, and judge ingest tests.

## Remaining Human Gates

- Manual browser/network UAT to confirm `audienceLocale`, `brandPosture`, and `brandHeritageOrigin` are present on `/api/form-ai/generate` requests.
- AC-10 live 270-cell baseline/judge execution remains pending.
