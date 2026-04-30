# Story 6 AU Eval Iteration Tracking

This sheet is initialised by Story 6.4.6 and maintained by the BMAD Analyst loop in Story 6.4.7.

## Analyst Iteration Design

Story 6.4.6 establishes the frozen AU baseline and harness evidence. Story 6.4.7 uses that baseline to test Analyst-authored prompt/context improvements without requiring the Analyst to edit tooling or production code.

The baseline is the stable control. It should only change at an explicit promotion gate after a candidate has passed deterministic checks, judge scoring, and Tony/SM review. Candidate variants are temporary experiment arms compared back to the frozen baseline.

Use the variant dimension according to the improvement goal:

- Locale robustness: `neutral`, `ambiguous`, `adversarial`.
- General prompt improvement: `candidate-a`, `candidate-b`, `candidate-c`.
- Focused target areas: candidate labels may describe the tested change, for example `explicit-validation`, `sectioned-flow`, or `concise-copy`.

Each Analyst iteration should record one improvement goal, target metrics, the changed prompt/context section, the exact candidate change, expected metric movement, actual metric movement, judge feedback, regressions, and the decision. Keep the scenario slice stable across candidates so row-by-row comparison remains meaningful.

| Iteration ID | Date/time | Baseline run ID | Candidate run ID | Prompt/context section changed | Change tested | Hypothesis | Expected metric movement | Actual metric movement | Metrics improved | Metrics regressed | Individual prompt rows improved/regressed | Judge conflict findings | Deterministic AU check failures | Judge-suggested correction | Decision | Reason | Follow-up action | Evidence links |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AU-000 | 2026-04-30 21:25 AEST | `story-6.4.6-au-baseline-current` | N/A | N/A | Current prompt state AU baseline | Establish clean AU-only baseline before prompt changes | N/A | Baseline captured: 45/45 schema-valid; judge mean agreement 0.817; mean locale fidelity 3.344; mean cross-locale leakage 3.522; mean format accuracy 3.344 | N/A - baseline | N/A - baseline | Judge scoring found conflicts in 45/45 rows; deterministic failures in 25/45 rows | Top likely responsible sections: `au_locale_block` (51 mentions), `system_prompt_output_contract` (24), `candidate_prompt_block` (22), `consent_legal_guidance` (12). Dominant issue: neutral/international prompt context conflicts with AU-only locale contract. | 130 generated-output findings across 25 prompts: 33 ZIP/Postcode, 56 foreign phone-code, 1 MM/DD/YYYY, 3 GDPR/CCPA-only privacy, 37 NHS/NZ-region; 0 prompt-context findings | Remove the neutral preamble from `au_locale_block`; make AU locale guidance explicit; add an `audience_locale`-wins rule for adversarial cross-locale cues; strengthen AU consent/legal guidance. | baseline captured | Story 6.4.6 initialises the diagnostic framework and records the current-state AU baseline without candidate prompt changes. | Analyst reviews AU-000 in Story 6.4.7 and defines candidate prompt/context experiments against this frozen baseline. | `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/`; `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/aggregate-summary.json`; `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/au-deterministic-checks.json`; `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/judge-package/`; `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/judge-package/judge-ingest-summary.json`; `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/judge-package/judge-ingest-summary.csv`; `docs/stories/STORY-6.4.6-AU-BASELINE-EVIDENCE.md` |

