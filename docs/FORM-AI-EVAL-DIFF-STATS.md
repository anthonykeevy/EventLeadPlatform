# Form AI Eval Diff And Statistics

Story 6.4.3c adds the comparison layer used by Story 6.4.4 prompt shrink experiments. It compares two eval run folders, applies deterministic structural gates, includes judge-score deltas when judge summaries exist, and writes Markdown, CSV, and JSON evidence.

## Compare Baseline Vs Variant

From the repo root:

```powershell
python -m backend.tests.form_ai_eval.diff `
  --baseline-run "_bmad-output/eval-runs/<baseline-run-id>" `
  --variant-run "_bmad-output/eval-runs/<variant-run-id>" `
  --output-dir "_bmad-output/eval-runs/<comparison-id>"
```

The output directory contains:

- `diff-report.md` for PM/SM review,
- `diff-details.csv` for row and metric inspection,
- `diff-summary.json` for machine-readable handoff.

If `--output-dir` is omitted, the tool writes under `_bmad-output/eval-runs/<baseline>-vs-<variant>-diff/`.

## Blocking Vs Advisory Outcomes

Blocking outcomes stop a ship decision until investigated:

- `schema_valid` regression: baseline row was valid and variant row is invalid.
- `boundary_violation_count > 0`: variant produced any boundary violation.

All other deltas are advisory in 6.4.3c. Component count, collision count, attempt count, duration, token/cost fields, judge scores, agreement, and GPT-5 mini bias deltas should be reviewed by PM/SM with the report context.

## Statistics

`backend/tests/form_ai_eval/stats.py` intentionally uses the Python standard library only.

- Welch t-test compares continuous metric samples without assuming equal variance.
- Cohen's `d` reports effect-size magnitude for continuous metric deltas.
- Fisher exact compares binary outcomes such as valid vs invalid rows.

For continuous metrics, a statistically useful win requires `p < 0.05` and effect size at least `0.3`. For Category B judge metrics, `p > 0.05` is inconclusive and the report recommends rerunning at `n=15`.

## Story 6.4.4 Usage

For each H1/H2/H4 or combined prompt variant:

1. Run the baseline and variant eval folders through the same benchmark set.
2. Generate and ingest judge packages when semantic Category B evidence is needed.
3. Run the diff tool with baseline as `--baseline-run` and the experiment as `--variant-run`.
4. Attach `diff-report.md`, `diff-summary.json`, and focused notes to the PM/SM ship/revert decision.

The tool recommends; it does not make product decisions. PM/SM should treat blockers as hard stops and advisory deltas as evidence for review.

## Out Of Scope

CI PR-comment automation is intentionally deferred until the report format stabilizes. The tool also does not run prompt sweeps, mutate prompt content, call live judge APIs, or change the judge rubric.
