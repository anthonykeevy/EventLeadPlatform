# Story 6.4.4 Gate Evidence

## Acceptance Criteria Mapping

| AC | Evidence |
|---|---|
| AC-1 H1 measured | Live run `story-6.4.4-live-h1-locale-one-line`; diff in `_bmad-output/eval-runs/story-6.4.4-live-baseline-vs-h1/` |
| AC-2 H2 measured | Live run `story-6.4.4-live-h2-consent-decision-table`; diff in `_bmad-output/eval-runs/story-6.4.4-live-baseline-vs-h2/` |
| AC-3 H4 measured | Live run `story-6.4.4-live-h4-operational-trim`; diff in `_bmad-output/eval-runs/story-6.4.4-live-baseline-vs-h4/` |
| AC-4 Combined measured | Live run `story-6.4.4-live-h1-h2-h4-combined`; diff in `_bmad-output/eval-runs/story-6.4.4-live-baseline-vs-combined/` |
| AC-5 Structural gates pass | All live diffs show `blocked = false`, no blocking reasons, and 10/10 matched rows |
| AC-6 Semantic evidence recorded | Baseline plus H1/H2/H4/combined judged by GPT-5 mini, Claude, and Gemini |
| AC-7 Statistical outputs recorded | Live diff summaries include Category B p-values/effect sizes and recommendations |
| AC-8 Revert losers | PM/SM decision pending; combined should not ship as-is due significant locale regression |
| AC-9 Prompt size delta documented | See `STORY-6.4.4-HYPOTHESIS-EVIDENCE.md` |
| AC-10 Hypothesis evidence complete | See `STORY-6.4.4-HYPOTHESIS-EVIDENCE.md` |
| AC-11 No unrelated capability work | No H3/H5/H6/Image-to-Form work; `prompts.yaml` and `rubric_v1.md` untouched |
| AC-12 Closeout complete | See `STORY-6.4.4-CLOSEOUT-REPORT.md` |

## Commands Run

### Preflight

```powershell
python scripts/agent/preflight.py -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.4.4-prompt-shrink-sweeps" -ExpectedBranch "story/epic6-6.4.4-prompt-shrink-sweeps" -Story "6.4.4"
```

Result: failed with exit code 2 because `scripts/agent/preflight.py` was not present in this worktree. Recorded in `STORY-6.4.4-PREFLIGHT.md`.

### Red Phase

```powershell
python -m pytest backend/tests/test_form_ai_prompt_capabilities.py backend/tests/test_form_ai_eval_harness.py --tb=short
```

Result before implementation: failed expected tests for H1/H2/H4 prompt contracts and non-baseline variant parsing.

### Focused Gate

```powershell
python -m pytest backend/tests/test_story_631_content_widths.py::test_locale_block_au_uses_story_644_one_line_directive backend/tests/test_story_631_content_widths.py::test_initial_messages_default_to_au_locale backend/tests/test_form_ai_prompt_capabilities.py backend/tests/test_form_ai_eval_harness.py backend/tests/test_eval_diff.py backend/tests/test_eval_stats.py --tb=short
```

Result: 31 passed, 116 warnings.

### Full Backend Gate

```powershell
cd backend
python -m pytest --tb=short
```

Initial result: 2 failures in older Story 6.3.1 locale tests that asserted the pre-shrink detailed AU/NZ block.

Final result after updating those tests to the Story 6.4.4 contract:

- 784 passed
- 26 skipped
- 5711 warnings
- duration: 95.54s

### Live Category B Evidence

Live baseline and variant runs were generated for:

- `story-6.4.2-post-cleanup-baseline`
- `story-6.4.4-live-h1-locale-one-line`
- `story-6.4.4-live-h2-consent-decision-table`
- `story-6.4.4-live-h4-operational-trim`
- `story-6.4.4-live-h1-h2-h4-combined`

Judge packages were generated and judged by GPT-5 mini, Claude, and Gemini. Judge outputs were ingested successfully for each package.

### Live Diff Reports

```powershell
python -m backend.tests.form_ai_eval.diff --baseline-run <baseline> --variant-run <variant> --output-dir <diff-output>
```

Generated outputs:

- `_bmad-output/eval-runs/story-6.4.4-live-baseline-vs-h1/`
- `_bmad-output/eval-runs/story-6.4.4-live-baseline-vs-h2/`
- `_bmad-output/eval-runs/story-6.4.4-live-baseline-vs-h4/`
- `_bmad-output/eval-runs/story-6.4.4-live-baseline-vs-combined/`

### Lint Diagnostics

Read IDE lints for touched files after implementation edits.

Result: no linter errors.

## Quality Notes

- No Alembic commands were run.
- No benchmark prompts or judge rubric files were modified.
- Combined H1+H2+H4 has a statistically significant `locale_fidelity` regression and should not be merged as-is.
- H1, H2, and H4 individual runs are inconclusive at n=10 and should either be explicitly accepted by PM/SM or rerun at n=15.
