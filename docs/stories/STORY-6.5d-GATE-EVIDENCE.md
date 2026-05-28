# Story 6.5d — Gate Evidence

**Date:** 2026-05-26  
**Branch:** `develop` (merged via PRs #109, #111, #112)  
**Alembic (Tony executes):** `086` → `095`

## Automated checks

| Command | Result |
|---------|--------|
| `python -m pytest tests/test_story_6_5d_migrations_static.py tests/test_story_6_5d_clarification_refs.py tests/test_story_6_5d_catalog_alignment.py tests/test_story_6_5d_block_e_renderer.py tests/test_story_6_5c_component_catalog.py tests/test_story_6_5c_catalog_alignment.py --tb=short -q` | **11/11 PASS** (2026-05-25) |
| `python scripts/verify_component_catalog_alignment.py` | **PASS** — 21 codes (company=1, country=1) |

## UAT

| Guide | Result |
|-------|--------|
| `STORY-6.5d-UAT-TEST-GUIDE.md` | Track A, Track B, Regression **Pass** (local, 2026-05-25) |
| `STORY-6.5d-UAT-RESULTS.md` | **Pass** — local + Azure Test (2026-05-26) |
| Azure Test | **Pass** — deploy [#111](https://github.com/anthonykeevy/EventLeadPlatform/pull/111), UAT fixes [#112](https://github.com/anthonykeevy/EventLeadPlatform/pull/112) |

## Architecture gate

- `decision-external-data-feed-components.md` — **Approved**, §9 resolved
- Preflight — `STORY-6.5d-PREFLIGHT.md` PASS

## Notes

- EDF runtime UAT (portal layering, dark theme, GeoScape on Test) validated manually on Azure Test 2026-05-26.
- Checklist §0b (EDF runtime parity + portaled theme contrast) updated in T02.
- Story ready for SM sign-off; production promotion via `develop` → `master` release PR when scheduled.
