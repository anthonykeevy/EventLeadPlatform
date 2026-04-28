# Story 6.4.4.2 — UAT Test Guide

**Story:** 6.4.4.2 — Re-evaluate H2/H4 under rubric_v2  
**UAT owner:** Human (Tonyk) + SM  
**Mode:** Evidence review + Cursor judge sessions

This story is UAT-heavy because the key question is whether H2 and/or H4 are safe prompt-shrink changes under the calibrated `rubric_v2` judge panel.

---

## §1 Baseline Control Verification

Confirm the story uses the regenerated AC10 baseline as control:

```powershell
Test-Path "_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-v2/judge-package/judge-ingest-summary.json"
```

Pass criteria:

- Baseline path exists.
- Summary reports 270 rows.
- Claude, Grok, and GPT-5 mini are present.
- Generated definitions are available for all rows.

**Section §1 Final:** Pass / Fail

---

## §2 H2 Variant Evidence

Review `STORY-6.4.4.2-HYPOTHESIS-EVIDENCE.md` for the H2 row.

Pass criteria:

- H2 was run as a single-variable variant.
- The variant uses `prompts-v1.1` and `rubric_v2`.
- Judge package includes explicit output paths.
- Ingest summary exists for Claude, Grok, and GPT-5 mini.
- Diff/stat output compares H2 against `story-6.4.4.1-ac10-baseline-v2`.
- Any terms/checkbox/required-acknowledgement regressions are absent or explicitly accepted.

**Section §2 Final:** Pass / Fail

---

## §3 H4 Variant Evidence

Review `STORY-6.4.4.2-HYPOTHESIS-EVIDENCE.md` for the H4 row.

Pass criteria:

- H4 was run as a single-variable variant.
- The variant uses `prompts-v1.1` and `rubric_v2`.
- Judge package includes explicit output paths.
- Ingest summary exists for Claude, Grok, and GPT-5 mini.
- Diff/stat output compares H4 against `story-6.4.4.1-ac10-baseline-v2`.
- Any row-grouping, tab-order, collision, or catalog regressions are absent or explicitly accepted.

**Section §3 Final:** Pass / Fail

---

## §4 Cursor Judge Sessions

For each variant requiring semantic judging:

1. Open the three emitted judge prompt files.
2. Run one Cursor session each for Claude, Grok, and GPT-5 mini.
3. Ensure each session writes to the output path embedded in its prompt.
4. Confirm the result files are well-formed JSON.

Pass criteria:

- Each output has `rubric_version: "rubric_v2"`.
- Each output has `judge_model` and `judge_model_version`.
- Each scored row has all rubric_v2 metrics.
- Scores are valid and non-empty.

**Section §4 Final:** Pass / Fail

---

## §5 Accepted-Subset Interaction Check

Only run this section if both H2 and H4 individually pass.

Pass criteria:

- The accepted H2+H4 subset run exists.
- It excludes H1.
- Diff/stat output shows no material interaction regression.
- If an interaction regression appears, the closeout records which candidate was reverted.

**Section §5 Final:** Pass / Fail / Not Applicable

---

## §6 Green Gate Review

Review `STORY-6.4.4.2-GATE-EVIDENCE.md`.

Pass criteria:

- Focused tests for touched prompt/eval code are green.
- Backend regression final summary is recorded, or a CI-backed exception is explicit.
- Frontend lint/unit checks are recorded if frontend files were touched; otherwise frontend is marked not applicable.
- No output is treated as green if the final summary was truncated.

**Section §6 Final:** Pass / Fail

---

## §7 Final Decision

Review `STORY-6.4.4.2-CLOSEOUT-REPORT.md`.

Pass criteria:

- H2 verdict is explicit: ship / revert / no-change.
- H4 verdict is explicit: ship / revert / no-change.
- Final retained code state matches the verdicts.
- Carry-forward items are listed with severity.
- Next recommended story is recorded.

**Section §7 Final:** Pass / Fail

---

## UAT Result Summary

| Section | Result | Notes |
|---|---|---|
| §1 Baseline control | TBD | |
| §2 H2 evidence | TBD | |
| §3 H4 evidence | TBD | |
| §4 Cursor judge sessions | TBD | |
| §5 Accepted-subset interaction | TBD | |
| §6 Green gate | TBD | |
| §7 Final decision | TBD | |

