# Story 6.3 — Gate evidence

**Date:** 2026-03-31 (local run)  
**Worktree:** `story-epic6-6.3-ai-context-benchmark-baseline`

## Backend

```text
python -m pytest --tb=short -q
# 535 passed, 26 skipped
```

Notable new/extended modules: `tests/test_story_63_benchmark_harness.py` (10/10 benchmarks, mocked LLM), `tests/test_story_63_context_pack_path.py` (`FORM_AI_CONTEXT_PACK_PATH`).

## Frontend

```text
npm run lint
# ESLint clean (--max-warnings 0)

npm run test:unit -- --watch=false
# Vitest: all files passed (includes buildAiRuntimeFootprints.test.ts)
```

## Builder apply path (AC-9)

`frontend/src/features/builder/components/ai/AIAgentPanel.tsx` — on `response.status === "completed"` with `definitionJSON`, `applyValidatedDefinition` is still called, then optional `relayoutFromRenderedHeights` re-apply. **Human UAT §5** (`STORY-6.3-UAT-TEST-GUIDE.md`) still required for sign-off.

## Preflight

SM-supplied `preflight-story.ps1` not re-run in this session; CI/local gates above executed from repo root as listed.

## Human UAT status (closeout)

- Human UAT did not reach satisfactory AI layout quality for Story 6.3 acceptance.
- Story 6.3 is therefore closed as learning capture and baseline consolidation, not as release-ready completion.
- See `docs/stories/STORY-6.3-CLOSEOUT-REPORT.md` for blockers, learnings, and redesign direction.
