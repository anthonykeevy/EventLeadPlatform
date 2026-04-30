# Story 6.4.6 AU Baseline Evidence

## Summary

Story 6.4.6 builds the AU-only diagnostic evaluation framework and produces the first current-state AU baseline.

This evidence file must remain baseline-only. Do not record candidate prompt/context improvements here.

## AU Prompt Set

| Item | Result |
|---|---|
| Prompt file | `backend/tests/form_ai_eval/prompts_au_v1.yaml` |
| Benchmark version | `prompts-au-v1` |
| Row count | 45 rows |
| Repetition strategy | One frozen row per AU prompt/variant; runner `--repetitions` remains available for repeated live runs. |
| Adversarial source-market rows | 15 existing AU adversarial variant rows retained; each row carries `metadata.source_market_adaptation = false` until a row is explicitly converted to source-market adaptation. |
| Foreign-noise audit result | AU-only prompt loader enforces `audience_locale = AU`; focused tests validate the file and metadata. |

Notes:

- Source file is derived from the AU slice of `prompts-v1.1`, with non-AU locale rows removed rather than carried into the AU diagnostic benchmark.

## AU Locale Contract

| Contract fact | Source / evidence | Result |
|---|---|---|
| +61 phone guidance | Story AC-3 / `au_locale_contract_v1.json` | Recorded |
| DD/MM/YYYY dates | Story AC-3 / `au_locale_contract_v1.json` | Recorded |
| Suburb/State/Postcode | Story AC-3 / `au_locale_contract_v1.json` | Recorded |
| AUD | Story AC-3 / `au_locale_contract_v1.json` | Recorded |
| Privacy Act 1988 | Story AC-3 / `au_locale_contract_v1.json` | Recorded |
| Spam Act 2003 | Story AC-3 / `au_locale_contract_v1.json` | Recorded |
| Australian English | Story AC-3 / `au_locale_contract_v1.json` | Recorded |
| Practical/plain-English tone | Story AC-3 / `au_locale_contract_v1.json` | Recorded |

Assumptions:

- The contract is version-managed at `backend/tests/form_ai_eval/au_locale_contract_v1.json`. It records story-approved launch facts and notes that DB-backed `config.PromptTemplateLocaleBlock` remains the runtime source when a DB session is available.

## Prompt Context Preflight

| Artifact | Path | Result |
|---|---|---|
| Shared context bundle | `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/shared-context-bundle.json` | Live aggregate artifact produced |
| Prompt-context lint JSON | `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/prompt-context-lint.json` | Live aggregate artifact produced; 0 prompt-context findings |
| Prompt-context lint markdown | `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/prompt-context-lint.md` | Live aggregate artifact produced |
| Deterministic AU checks JSON | `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/au-deterministic-checks.json` | Live aggregate artifact produced; 130 generated-output findings |
| Deterministic AU checks markdown | `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/au-deterministic-checks.md` | Live aggregate artifact produced |

Preflight summary:

- Live aggregate run completed from controlled one-row slices with max four concurrent subprocesses. Prompt context lint found 0 prompt-context conflicts.

## Baseline Run

| Item | Result |
|---|---|
| Run ID | `story-6.4.6-au-baseline-current` |
| Variant label | `story-6.4.6-au-baseline-current` |
| Prompt behavior | Current state / no candidate prompt improvements |
| Output folder | `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/` |
| Generated rows | 45/45 live rows aggregated under `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/`. |
| Failures/retries | 45/45 rows completed with `schema_valid=true` and `terminal_reason=validated-success`. Initial full 45-row run was stopped after producing no artifacts, then completed in controlled slices. |

Live proof run summary:

| Run ID | Prompt ID | Duration | Result |
|---|---|---:|---|
| `story-6.4.6-au-baseline-current-single` | `p01-au-neutral-r1` | 42.968s | `schema_valid=true`; no deterministic AU findings |
| `story-6.4.6-au-baseline-current-parallel-p02` | `p02-au-neutral-r1` | 51.557s | `schema_valid=true`; no deterministic AU findings |
| `story-6.4.6-au-baseline-current-parallel-p03` | `p03-au-neutral-r1` | 56.855s | `schema_valid=true`; no deterministic AU findings |
| `story-6.4.6-au-baseline-current-parallel-p04` | `p04-au-neutral-r1` | 48.757s | `schema_valid=true`; no deterministic AU findings |

Aggregate baseline summary:

| Item | Result |
|---|---|
| Aggregate summary | `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/aggregate-summary.json` |
| Schema-valid rows | 45/45 |
| Min / max row duration | 33.996s / 133.696s |
| Prompt-context deterministic findings | 0 |
| Generated-output deterministic findings | 130 findings across 25 prompts |
| Finding breakdown | 33 ZIP/Postcode, 56 foreign phone-code, 1 MM/DD/YYYY, 3 GDPR/CCPA-only privacy, 37 NHS/NZ-region |
| Token/cost fields | This aggregate artifact was produced from earlier controlled one-row runs before provider usage capture was wired through, so `input_tokens`, `output_tokens`, and `total_cost_usd` remain placeholders here. The runner/service now capture provider token usage for new runs when returned by the provider; provider cost is still not returned by OpenAI and remains a harness-side placeholder. |
| Parallel execution evidence | `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/parallel-execution-summary.json`; max observed concurrent runs = 4. |

## Judge Package

| Item | Path / Result |
|---|---|
| Judge package | `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/judge-package/` |
| Shared context bundle included | `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/judge-package/shared-context-bundle.json` |
| Claude prompt | `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/judge-package/judge-prompt-claude.md` |
| Grok prompt | `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/judge-package/judge-prompt-grok.md` |
| GPT-5 mini prompt | `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/judge-package/judge-prompt-gpt5mini.md` |
| Judge output template | `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/judge-package/judge-output-template.json`; includes diagnostic fields |
| Judge metadata | `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/judge-package/judge-package-metadata.json`; 45 rows |

## Judge Ingest

| Item | Result |
|---|---|
| Claude output saved | `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/judge-package/results/judge-output-claude.json` |
| Grok output saved | `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/judge-package/results/judge-output-grok.json` |
| GPT-5 mini output saved | `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/judge-package/results/judge-output-gpt5mini.json` |
| Ingest summary JSON | `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/judge-package/judge-ingest-summary.json` |
| Ingest summary CSV | `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/judge-package/judge-ingest-summary.csv` |
| Diagnostic fields validated | PASS. Ingest completed for 45 rows across Claude, Grok, and GPT-5 mini after normalising GPT-5 mini null diagnostic placeholders to empty values and Grok percentage-style confidence values to `0..1`. |

## Baseline Diagnostic Summary

| Diagnostic area | Summary |
|---|---|
| Lowest-scoring rows | Judge agreement min 0.60; weakest metric means are locale fidelity 3.344, format pattern accuracy 3.344, and cross-locale leakage 3.522. |
| Judge conflict findings | At least one judge reported conflicting data for 45/45 rows. Dominant finding: current prompt context contains neutral/international guidance that conflicts with the AU-only locale contract, especially on adversarial rows. |
| Likely responsible sections | Top section mentions: `au_locale_block` 51, `system_prompt_output_contract` 24, `candidate_prompt_block` 22, `consent_legal_guidance` 12. |
| Deterministic AU failures | 130 generated-output findings across 25 prompts; 0 prompt-context findings |
| Judge-suggested corrections | Remove neutral preamble from `au_locale_block`; make AU guidance explicit; add `audience_locale`-wins rule for cross-locale/adversarial cues; strengthen AU privacy/Spam Act consent guidance. |
| Analyst handoff notes | `AU-000` updated. Story 6.4.7 should start from this frozen baseline and test candidate prompt/context improvements without overwriting the baseline run folder. |

## Tracking Sheet Update

| Item | Result |
|---|---|
| `AU-000` row updated | Updated with baseline run ID, deterministic findings, judge means, conflict findings, suggested corrections, and follow-up action |
| Baseline run ID recorded | `story-6.4.6-au-baseline-current` |
| Evidence links recorded | Baseline folder, aggregate summary, deterministic checks, judge package |

## Final Baseline Verdict

Live current-state AU baseline, judge package, and judge ingest are complete. The baseline is intentionally diagnostic, not passing quality: it records systematic AU-locale weaknesses for the Analyst loop to address in Story 6.4.7.
