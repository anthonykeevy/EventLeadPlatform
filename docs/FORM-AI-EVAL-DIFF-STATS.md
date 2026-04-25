# Form AI Eval Diff + Statistics

**Status:** Template ready; Dev completes during Story 6.4.3c  
**Audience:** Dev, SM, PM reviewing prompt experiment evidence  
**Scope:** Compare eval runs and interpret structural/judge deltas. Prompt sweeps begin in Story 6.4.4.

---

## Purpose

Story 6.4.3c adds the decision-support layer for the Form AI eval harness:

- compare two eval run folders,
- identify structural blockers,
- summarise advisory deltas,
- include judge metrics when available,
- calculate statistical evidence,
- produce Markdown/CSV/JSON outputs for review.

---

## Example Command

Dev fills the exact final command after implementation.

```powershell
python -m backend.tests.form_ai_eval.diff `
  --baseline-run "_bmad-output/eval-runs/story-6.4.3a-live-full-10row-baseline" `
  --variant-run "_bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline" `
  --output-dir "_bmad-output/eval-runs/story-6.4.3c-sample-diff"
```

Expected outputs:

- `diff-report.md`
- `diff-details.csv`
- `diff-summary.json`

---

## Blocking Outcomes

These block a prompt change unless explicitly overruled by SM/PM:

- `schema_valid` regression of one or more rows,
- any `boundary_violation_count > 0`.

---

## Advisory Outcomes

These are reported for human review:

- component count changes,
- collision count changes,
- attempt count changes,
- duration changes,
- token/cost changes,
- judge metric deltas,
- GPT-5 mini self-bias deltas,
- judge agreement changes.

---

## Statistical Rules

Continuous metrics:

- Welch's t-test for p-value.
- Cohen's `d` for effect size.
- A win requires `p < 0.05` and `d >= 0.3`.

Binary metrics:

- Fisher exact test.
- Used for `schema_valid` and similar pass/fail outcomes.

Inconclusive Category B:

- If `p > 0.05`, recommend rerun at n=15 before declaring a final verdict.

---

## How Story 6.4.4 Uses This

For H1/H2/H4 and combined variants:

1. Run baseline and variant generations through the eval harness.
2. Generate judge packages and ingest scores where semantic metrics are required.
3. Run this diff tool baseline vs variant.
4. Review blockers first.
5. Review statistical/advisory evidence.
6. PM/SM decide ship, revert, or rerun.

---

## Out Of Scope

- Running prompt sweeps.
- Choosing H1/H2/H4 winners.
- PR comment automation.
- Changing judge rubric.
- Live model API calls.
