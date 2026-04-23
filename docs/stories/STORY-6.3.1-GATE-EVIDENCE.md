# Story 6.3.1 Gate Evidence

- Generated: 2026-04-15 (closeout run, post UAT Round 11)
- Repository root: `C:\wt\elp\story-epic6-6.3.1-simplified-ai-deterministic-layout`
- Branch: `story/epic6-6.3.1-simplified-ai-deterministic-layout`
- Draft PR: [#64](https://github.com/anthonykeevy/EventLeadPlatform/pull/64)

| Command | Working Directory | Exit | Summary detected | Status |
|---------|-------------------|------|------------------|--------|
| `npm run lint` | `...\frontend` | 0 | yes | PASS |
| `npm run test:unit -- --watch=false` | `...\frontend` | 0 | yes | PASS |
| `python -m pytest --tb=short` | `...\backend` | 0 | yes | PASS |

---

## `npm run lint`

- Working dir: `C:\wt\elp\story-epic6-6.3.1-simplified-ai-deterministic-layout\frontend`
- Exit code: 0
- Command: `eslint src --ext ts,tsx --max-warnings 0`
- Final summary: clean exit, **no errors and no warnings** (`--max-warnings 0` enforced).

## `npm run test:unit -- --watch=false`

- Working dir: `C:\wt\elp\story-epic6-6.3.1-simplified-ai-deterministic-layout\frontend`
- Exit code: 0
- Final summary: **Test Files 27 passed (27), Tests 272 passed (272)** in 33.73s (Vitest, jsdom).
- New file under test exercised here: `src/features/builder/utils/__tests__/layoutMode.test.ts` (canvas-driven layout-mode resolver).

## `python -m pytest --tb=short`

- Working dir: `C:\wt\elp\story-epic6-6.3.1-simplified-ai-deterministic-layout\backend`
- Exit code: 0
- Final summary: **705 passed, 26 skipped, 5711 warnings in 96.51s** (Windows, Python 3.13, MSSQL).
- New Story 6.3.1 test files included in the run:
  - `tests/test_story_631_semantic_validator.py`
  - `tests/test_story_631_deterministic_compiler.py`
  - `tests/test_story_631_layout_solver.py`
  - `tests/test_story_631_content_widths.py`
  - `tests/test_story_631_failure_mode_separation.py`
  - `tests/test_story_631_governance_persistence.py`
  - `tests/test_story_631_form_ai_governance_api.py`
- Rewritten Story 6.2 / 6.3 tests now exercising the deterministic-compiler contract:
  - `tests/test_story_6_2_ai_generation_loop.py`
  - `tests/test_story_63_context_pack_path.py`
  - `tests/test_story_63_benchmark_harness.py`
  - `tests/test_story_63_event_context_post_process.py`
  - `tests/test_form_ai_prompt_capabilities.py`
  - `tests/test_form_ai_first_shot.py`

---

## Database / migration evidence

- Alembic migrations introduced this story (run by Anthony per workspace rule):
  - `053_story_631_form_ai_governance_tables.py` — capability/validation/width/prompt governance tables.
  - `054_story_631_seed_governance_baseline.py` — seed `FORM_AI_CAPABILITY_POLICY:v1` and `FORM_AI_WIDTH_POLICY:v1`.
  - `055_story_631_form_ai_capability_rating_fileupload.py` — capability snapshot extension for `rating`, `file-upload`, `address`, `url` (UAT Round 4 fix).
  - `056_story_631_form_ai_capability_first_last_name.py` — capability snapshot extension for `first-name` / `last-name` (UAT Round 5).
  - `057_story_631_form_ai_capability_drop_last_name.py` — drop `last-name` until frontend `ComponentRegistry` ships matching renderer (UAT Round 5 follow-up).
- Replay tooling: `backend/scripts/story_631_replay.py` reproduces compiled `DefinitionJSON` for a stored `GenerationRun` across desktop / tablet / mobile canvas profiles.
- Spot-check tooling: `backend/scripts/story_631_uat_spotcheck.py` for one-off compiler probes.

---

## Closeout sanity checks

- `git status` clean of scratch artefacts: `_uat_diag*.txt`, `_ai_log_recent.txt`, `backend/_probe_*.py`, `replay-output/` removed before commit.
- Unrelated `EPIC-5-STATUS.md` / `EPIC-5-WORKFLOW-GUIDE.md` working-tree edits (PowerShell encoding noise) reverted via `git checkout --`.
- `.\scripts\workflow\preflight-story.ps1` PASS recorded in `STORY-6.3.1-PREFLIGHT.md` (worktree, branch, DB resolution parity all green).

---

## Anti-hallucination compliance

Per `EPIC-6-WORKFLOW-GUIDE.md` "Green CI/CD Rule": all three commands above ran to **explicit final summary lines** (no truncation, no timeout) and exit code `0`. The summary lines are quoted verbatim in this file.
