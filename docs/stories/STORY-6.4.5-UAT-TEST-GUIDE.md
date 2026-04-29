# Story 6.4.5 — UAT Test Guide

**Story:** 6.4.5 — Component Property Cheat Sheet H3  
**UAT owner:** Human (Tonyk) + SM  
**Mode:** Evidence review + Cursor judge sessions

This story validates whether a concise component-property cheat sheet improves or safely preserves Form AI quality under `prompts-v1.1` / `rubric_v2`.

---

## §1 Prompt Contract Review

Review the H3 prompt block in `backend/modules/form_ai/service.py`.

Pass criteria:

- H3 is concise and semantic-plan oriented.
- It is filtered to active capability snapshot component types.
- It does not mention unsupported/future components.
- It does not ask the model to emit unsupported props.
- It is omitted when no capability snapshot exists.

**Section §1 Final:** Pass / Fail

---

## §2 Focused Test Review

Review `STORY-6.4.5-GATE-EVIDENCE.md`.

Pass criteria:

- Focused prompt contract tests pass.
- Tests cover snapshot filtering and unsupported-component exclusion.

**Section §2 Final:** Pass / Fail

---

## §3 H3 Eval Evidence

Review `STORY-6.4.5-HYPOTHESIS-EVIDENCE.md`.

Pass criteria:

- H3 run uses `prompts-v1.1` and `rubric_v2`.
- Run id and output paths are recorded.
- Generated definitions are available for all rows, or any failure is explicitly documented.
- Judge package contains explicit output paths.

**Section §3 Final:** Pass / Fail

---

## §4 Cursor Judge Sessions

For the H3 judge package:

1. Run one Cursor judge session each for Claude 4.7, Grok 4, and GPT-5 mini.
2. Save each output to the path embedded in the prompt.
3. Confirm ingest succeeds.

Pass criteria:

- Each output has `rubric_version: "rubric_v2"`.
- Each output has `judge_model` and `judge_model_version`.
- Ingest summary JSON/CSV exists.

**Section §4 Final:** Pass / Fail

---

## §5 Diff/Stats Decision

Review the diff/statistics output against `story-6.4.4.1-ac10-baseline-v2`.

Pass criteria:

- No structural blockers.
- No material Category B regression.
- Any improvement/win claims are backed by p-value/effect-size or clearly marked advisory.
- If evidence is inconclusive, closeout says whether Tonyk/PM accepted safe-neutral or reverted.

**Section §5 Final:** Pass / Fail

---

## §6 Green Gate Review

Pass criteria:

- Focused backend tests are green.
- Backend regression final summary is recorded.
- Frontend lint/unit checks are recorded if frontend files were touched; otherwise marked not applicable.
- No truncated output is treated as green.

**Section §6 Final:** Pass / Fail

---

## §7 Final Decision

Review `STORY-6.4.5-CLOSEOUT-REPORT.md`.

Pass criteria:

- H3 final state is explicit: shipped or reverted/no-change.
- Final code state matches the verdict.
- Carry-forward items are listed.
- Next recommended story is recorded.

**Section §7 Final:** Pass / Fail

---

## UAT Result Summary

| Section | Result | Notes |
|---|---|---|
| §1 Prompt contract | Pass for measurement | H3 was bounded/snapshot-filtered during evaluation, then reverted for no-change closeout. |
| §2 Focused tests | Pass | Focused tests passed before evaluation and after no-change revert. |
| §3 H3 eval evidence | Pass | H3 generated 270/270 definitions. |
| §4 Cursor judge sessions | Pass | Claude, Grok, and repaired GPT-5 mini outputs ingested. |
| §5 Diff/stats decision | Fail to ship | Material `field_label_f1` regression plus locale/context-conflict noise. |
| §6 Green gate | Pass | Focused and backend regression gates passed. |
| §7 Final decision | Measured/no-change | H3 no-go as-is; prompt changes reverted. |

