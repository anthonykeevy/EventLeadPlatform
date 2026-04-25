# Story 6.4.3a — Benchmark Baseline

**Story:** 6.4.3a — AI Eval Harness Bones  
**Benchmark Set Version:** `prompts-v1.0`  
**Status:** Template ready; Dev completes after harness smoke/formal run  
**Data classification:** PII-adjacent synthetic eval data. Do not share raw generations externally.

---

## 1) Run Metadata

| Field | Value |
|-------|-------|
| Run ID | `<fill after run>` |
| Git SHA | `<fill after run>` |
| Branch | `story/epic6-6.4.3a-ai-eval-harness-bones` |
| Command | `<exact command>` |
| Working directory | `<repo/worktree path>` |
| Output folder | `_bmad-output/eval-runs/<run-id>/` |
| DB persistence | `<enabled/disabled; migration applied by Anthony: yes/no>` |
| Model/config snapshot | `<model, prompt version, capability snapshot version, relevant env/config names only>` |
| Started at UTC | `<timestamp>` |
| Completed at UTC | `<timestamp>` |

---

## 2) Benchmark Coverage

| Prompt ID | Type | Included | Repetitions | Notes |
|-----------|------|----------|-------------|-------|
| `p-01-event-registration-conference` | Event registration | `<yes/no>` | `<n>` | Multi-consent, payment placeholder, t-shirt size |
| `p-02-lead-gen-saas-demo` | Lead-gen | `<yes/no>` | `<n>` | Minimal one-liner |
| `p-03-survey-nps` | Survey | `<yes/no>` | `<n>` | Rating + long textarea |
| `p-04-waiver-gym-membership` | Waiver | `<yes/no>` | `<n>` | Mandatory acknowledgement, terms popup |
| `p-05-rsvp-wedding` | RSVP | `<yes/no>` | `<n>` | +1 names, meal choice, dietary notes |
| `p-06-feedback-post-event` | Feedback | `<yes/no>` | `<n>` | Minimal emergent structure |
| `p-07-booking-consultation` | Booking | `<yes/no>` | `<n>` | Calendar + slots, conditional reminder |
| `p-08-onboarding-new-employee` | Onboarding | `<yes/no>` | `<n>` | PII-heavy synthetic fields |
| `p-09-application-scholarship` | Application | `<yes/no>` | `<n>` | Essays, file upload, terms |
| `p-10-donation-charity` | Donation | `<yes/no>` | `<n>` | Amount, gift-aid, recurring toggle |

---

## 3) Structural Summary

| Metric | Value | Notes |
|--------|-------|-------|
| Total generations attempted | `<n>` | Prompt rows x repetitions |
| Successful generations | `<n>` | |
| Failed generations | `<n>` | Include failure classes below |
| `schema_valid` failures | `<n>` | |
| Collision count total | `<n>` | |
| Boundary violation count total | `<n>` | Must be 0 for future blocking gate |
| Mean component count | `<value>` | |
| Mean attempt count | `<value>` | |
| Mean duration ms | `<value>` | |
| Input tokens total | `<value>` | |
| Output tokens total | `<value>` | |
| Total cost USD | `<value>` | |
| Retry count total | `<n>` | |

---

## 4) Failure Classes

| Failure Class | Count | Prompt IDs | Notes |
|---------------|-------|------------|-------|
| `<class>` | `<n>` | `<ids>` | `<notes>` |

If no failures occurred, state: `No failures observed in this run.`

---

## 5) Output Files

| File | Purpose |
|------|---------|
| `_bmad-output/eval-runs/<run-id>/metrics.jsonl` | Per-generation metrics |
| `_bmad-output/eval-runs/<run-id>/summary.csv` | Tabular summary |
| `_bmad-output/eval-runs/<run-id>/checkpoint.json` | Present only if halted/resumed |
| `_bmad-output/eval-runs/<run-id>/run-metadata.json` | Run configuration snapshot |

---

## 6) DB Evidence

| Check | Result |
|-------|--------|
| `log.FormAiEvalRun` migration applied by Anthony | `<yes/no>` |
| Rows inserted | `<n>` |
| BenchmarkSetVersion | `prompts-v1.0` |
| HypothesisCode | `baseline` |
| BaselineExpiresAt populated | `<yes/no>` |
| Judge fields nullable/empty | `<yes/no>` |

---

## 7) Limitations

- Category B semantic judge scores are not available until Story 6.4.3b.
- Rubric governance and judge JSON ingest are not available until Story 6.4.3b.
- Welch/Fisher statistics and diff tooling are not available until Story 6.4.3c.
- This baseline is structurally useful for Story 6.4.2 zero-behavioural-change checks, but it is not a final prompt-quality verdict.

---

## 8) Decision

Baseline is considered usable for Story 6.4.2 when:

- all 10 prompt rows are included or excluded rows are explicitly justified,
- run metadata is complete,
- Category A metrics are recorded,
- DB persistence is verified if migration has been applied,
- limitations are acknowledged.
