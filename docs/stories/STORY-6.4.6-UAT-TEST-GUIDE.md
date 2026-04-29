# Story 6.4.6 - UAT Test Guide

**Story:** 6.4.6 - AU-Only Diagnostic Evaluation Framework + Baseline  
**UAT owner:** Human (Tony) + SM  
**Mode:** Evidence review + Cursor judge sessions

This story validates that the AU diagnostic framework exists, produces a clean current-state AU baseline, and hands Story 6.4.7 enough structured evidence for controlled prompt iteration.

---

## Section 1 - AU Prompt Set Review

Review the AU benchmark prompt set and evidence notes.

Pass criteria:

- Prompt rows are AU launch-market focused.
- Stable row IDs and metadata support row-level comparison.
- Non-AU concepts are removed unless explicitly tagged as adversarial source-market adaptation tests.
- Form-type variety is preserved.

**Section 1 Final:** Pass / Fail

---

## Section 2 - AU Locale Contract Review

Review the AU contract artifact and source notes.

Pass criteria:

- Contract includes +61, DD/MM/YYYY, Suburb/State/Postcode, AUD, Privacy Act 1988, Spam Act 2003, Australian English, and practical/plain-English tone.
- Any assumptions are documented.
- Tests cover the contract shape and required facts.

**Section 2 Final:** Pass / Fail

---

## Section 3 - Context Preflight And Shared Bundle

Review prompt-context artifacts from the AU baseline run.

Pass criteria:

- Complete prompt context is represented by stable section IDs.
- Shared sections have content hashes.
- Per-case rows reference section IDs/hashes.
- Preflight/linter output identifies conflicts with responsible sections.
- Artifacts are available under the baseline run folder.

**Section 3 Final:** Pass / Fail

---

## Section 4 - Deterministic AU Checks

Review deterministic AU check output.

Pass criteria:

- Checks cover ZIP/Postcode, +1/+44/+64, MM/DD/YYYY, GDPR/CCPA-only wording, NHS/NZ-region/foreign leakage, and adversarial tags.
- Machine-readable and human-readable reports exist.
- Failures are linked to prompt IDs and likely sections.

**Section 4 Final:** Pass / Fail

---

## Section 5 - Current-State AU Baseline

Review `STORY-6.4.6-AU-BASELINE-EVIDENCE.md`.

Pass criteria:

- Baseline uses current prompt behavior only.
- No candidate prompt/context improvement was applied.
- Run ID and output paths are recorded.
- Generated definitions exist for all intended AU rows, or retry/failure outcome is documented.

**Section 5 Final:** Pass / Fail

---

## Section 6 - Cursor Judge Sessions

For the AU baseline judge package:

1. Run one Cursor judge session each for Claude, Grok, and GPT-5 mini.
2. Save each output to the path embedded in its judge prompt.
3. Confirm ingest succeeds.

Pass criteria:

- Each output has `rubric_version: "rubric_v2"`.
- Each output has `judge_model` and `judge_model_version`.
- Each row includes metric scores, rationale, conflict flag, conflict description, likely responsible section IDs, suggested correction, and confidence.
- Ingest summary JSON/CSV exists and includes diagnostic fields.

**Section 6 Final:** Pass / Fail

---

## Section 7 - Tracking Sheet Handoff

Review `STORY-6-AU-EVAL-ITERATION-TRACKING.md`.

Pass criteria:

- Row `AU-000` has the baseline run ID.
- Candidate run ID is `N/A`.
- Prompt/context section changed is `N/A`.
- Judge conflict findings and deterministic AU failures are summarized.
- Evidence links point to the baseline run, judge package, ingest outputs, and Story 6.4.6 evidence docs.

**Section 7 Final:** Pass / Fail

---

## Section 8 - Green Gate Review

Review `STORY-6.4.6-GATE-EVIDENCE.md`.

Pass criteria:

- Focused eval/judge tests are green.
- Backend regression final summary is recorded.
- Frontend lint/unit checks are recorded if frontend files were touched; otherwise marked not applicable.
- No truncated output is treated as green.

**Section 8 Final:** Pass / Fail

---

## Section 9 - Final Decision

Review `STORY-6.4.6-CLOSEOUT-REPORT.md`.

Pass criteria:

- Framework final state is explicit.
- Baseline completeness is explicit.
- No prompt improvement leakage occurred.
- Carry-forward items are listed.
- Next recommended story is Story 6.4.7 unless a framework blocker remains.

**Section 9 Final:** Pass / Fail

---

## UAT Result Summary

| Section | Result | Notes |
|---|---|---|
| Section 1 AU prompt set | TBD |  |
| Section 2 AU locale contract | TBD |  |
| Section 3 Context preflight/shared bundle | TBD |  |
| Section 4 Deterministic AU checks | TBD |  |
| Section 5 Current-state AU baseline | TBD |  |
| Section 6 Cursor judge sessions | TBD |  |
| Section 7 Tracking sheet handoff | TBD |  |
| Section 8 Green gate | TBD |  |
| Section 9 Final decision | TBD |  |
