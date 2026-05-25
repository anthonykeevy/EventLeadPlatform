# Story 6.5d — Gate Evidence

**Date:** 2026-05-25  
**Branch:** `story/epic6-6.5d-clarification-component-platform`  
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
| `STORY-6.5d-UAT-RESULTS.md` | Tony sign-off recorded |
| Azure Test | Pending post-merge |

## Architecture gate

- `decision-external-data-feed-components.md` — **Approved**, §9 resolved
- Preflight — `STORY-6.5d-PREFLIGHT.md` PASS

## Notes

- Full `pytest` suite not re-run after EDF UAT fixes — recommend CI on PR #109 before merge.
- EDF runtime UAT (portal scale, manual ABR, submit payload) validated manually; not in automated suite yet.
