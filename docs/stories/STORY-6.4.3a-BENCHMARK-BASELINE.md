# Story 6.4.3a — Benchmark Baseline

**Story:** 6.4.3a — AI Eval Harness Bones  
**Benchmark Set Version:** `prompts-v1.0`  
**Status:** Full 10-row live provider baseline complete with DB persistence verified
**Data classification:** PII-adjacent synthetic eval data. Do not share raw generations externally.

---

## 1) Run Metadata

| Field | Value |
|-------|-------|
| Run ID | `story-6.4.3a-live-full-10row-baseline` |
| Git SHA | `0dfebd84f4387295ebf0cf05c722bd0c71e474b5` |
| Branch | `story/epic6-6.4.3a-ai-eval-harness-bones` |
| Command | `python -m backend.tests.form_ai_eval.run --variant baseline --hypothesis-code baseline --repetitions 1 --max-cost-usd 1 --persist-db --run-id story-6.4.3a-live-full-10row-baseline` |
| Working directory | `C:\wt\elp\story-epic6-6.4.3a-ai-eval-harness-bones` |
| Output folder | `_bmad-output/eval-runs/story-6.4.3a-live-full-10row-baseline/` |
| DB persistence | Enabled; `EvalRunID=3..12` verified in `log.FormAiEvalRun` |
| Model/config snapshot | Existing Form AI provider configuration; `prompts-v1.0`; frozen runtime contexts declare `FORM_AI_CAPABILITY_POLICY:v1` |
| Started at UTC | `2026-04-25T03:15:27.067164+00:00` |
| Completed at UTC | `2026-04-25T03:27:28.371735+00:00` |

---

## 2) Benchmark Coverage

| Prompt ID | Type | Included | Repetitions | Notes |
|-----------|------|----------|-------------|-------|
| `p-01-event-registration-conference` | Event registration | yes | 1 | Multi-consent, payment placeholder, t-shirt size |
| `p-02-lead-gen-saas-demo` | Lead-gen | yes | 1 | Minimal one-liner |
| `p-03-survey-nps` | Survey | yes | 1 | Rating + long textarea |
| `p-04-waiver-gym-membership` | Waiver | yes | 1 | Mandatory acknowledgement, terms popup |
| `p-05-rsvp-wedding` | RSVP | yes | 1 | +1 names, meal choice, dietary notes |
| `p-06-feedback-post-event` | Feedback | yes | 1 | Minimal emergent structure |
| `p-07-booking-consultation` | Booking | yes | 1 | Calendar + slots, conditional reminder |
| `p-08-onboarding-new-employee` | Onboarding | yes | 1 | PII-heavy synthetic fields |
| `p-09-application-scholarship` | Application | yes | 1 | Essays, file upload, terms |
| `p-10-donation-charity` | Donation | yes | 1 | Amount, gift-aid, recurring toggle |

---

## 3) Structural Summary

| Metric | Value | Notes |
|--------|-------|-------|
| Total generations attempted | 10 | Prompt rows x repetitions |
| Successful generations | 10 | Live provider path |
| Failed generations | 0 | |
| `schema_valid` failures | 0 | |
| Collision count total | 0 | |
| Boundary violation count total | 0 | Must be 0 for future blocking gate |
| Mean component count | 14.1 | Component counts ranged from 6 to 20 |
| Mean attempt count | 1.2 | Two prompts required one correction attempt |
| Mean duration ms | 72127.6 | Total run elapsed about 12 minutes |
| Input tokens total | 0 | Existing service response does not expose provider usage yet |
| Output tokens total | 0 | Existing service response does not expose provider usage yet |
| Total cost USD | 0.0 | Cost fields are placeholders until provider usage is surfaced |
| Retry count total | 0 | |

---

## 4) Failure Classes

| Failure Class | Count | Prompt IDs | Notes |
|---------------|-------|------------|-------|
| `none` | 10 | all included prompt IDs | No failures observed in full live provider baseline |

If no failures occurred, state: `No failures observed in this run.`

---

## 5) Output Files

| File | Purpose |
|------|---------|
| `_bmad-output/eval-runs/story-6.4.3a-live-full-10row-baseline/metrics.jsonl` | Per-generation metrics |
| `_bmad-output/eval-runs/story-6.4.3a-live-full-10row-baseline/summary.csv` | Tabular summary |
| `_bmad-output/eval-runs/story-6.4.3a-live-full-10row-baseline/checkpoint.json` | Not present; run did not halt/resume |
| `_bmad-output/eval-runs/story-6.4.3a-live-full-10row-baseline/run-metadata.json` | Run configuration snapshot |

---

## 6) DB Evidence

| Check | Result |
|-------|--------|
| `log.FormAiEvalRun` migration applied by Anthony | yes; `061 -> 062` applied 2026-04-25 |
| Rows inserted | 10 full-baseline rows verified: `EvalRunID=3..12`, `GenerationRunID=97..106` |
| BenchmarkSetVersion | `prompts-v1.0` |
| HypothesisCode | `baseline` |
| BaselineExpiresAt populated | yes; `CreatedDate + 30 days` verified |
| Judge fields nullable/empty | yes; `JudgeRubricVersion`, `JudgeAgreementScore`, `BiasDeltaJSON` are null |

DB persistence command:

```powershell
python -m backend.tests.form_ai_eval.run --variant baseline --hypothesis-code baseline --repetitions 1 --max-cost-usd 1 --persist-db --run-id story-6.4.3a-live-full-10row-baseline
```

Full live provider result: all 10 prompt rows persisted with `schema_valid=true`, `collision_count=0`, `boundary_violation_count=0`, `terminal_reason=validated-success`, `failure_class=none`, judge fields null, and `BaselineExpiresAt = CreatedDate + 30 days`.

---

## 7) Limitations

- Category B semantic judge scores are not available until Story 6.4.3b.
- Rubric governance and judge JSON ingest are not available until Story 6.4.3b.
- Welch/Fisher statistics and diff tooling are not available until Story 6.4.3c.
- This baseline is structurally useful for Story 6.4.2 zero-behavioural-change checks, but it is not a final prompt-quality verdict.
- Token and cost fields remain `0` until provider usage is surfaced by the existing Form AI service response.

---

## 8) Decision

Baseline is considered usable for Story 6.4.2 when:

- all 10 prompt rows are included or excluded rows are explicitly justified,
- run metadata is complete,
- Category A metrics are recorded,
- DB persistence is verified if migration has been applied,
- limitations are acknowledged.
