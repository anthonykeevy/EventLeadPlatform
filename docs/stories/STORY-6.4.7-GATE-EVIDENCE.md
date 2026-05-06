# Story 6.4.7 Gate Evidence

## Preflight

- Preflight command: `.\scripts\workflow\preflight-story.ps1 -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.4.7-au-baseline-analyst-loop" -ExpectedBranch "story/epic6-6.4.7-au-baseline-analyst-loop" -ReportFile "docs/stories/STORY-6.4.7-PREFLIGHT.md"`
- Result: PASS.
- PR #84: open draft PR from `story/epic6-6.4.7-au-baseline-analyst-loop` to `master`.
- Story 6.4.6 PR #82: merged.

## Baseline Evidence Reviewed

- Baseline run: `story-6.4.6-au-baseline-current`
- Tracking row: `AU-000`
- Aggregate baseline: 45/45 schema-valid rows.
- Deterministic AU findings: 130 generated-output findings across 25 prompts; 0 prompt-context findings.
- Finding breakdown: 33 ZIP/Postcode, 56 foreign phone-code, 1 MM/DD/YYYY, 3 GDPR/CCPA-only privacy, 37 NHS/NZ-region.
- Judge conflict findings: at least one judge reported conflicting data for 45/45 rows.
- Top likely responsible sections: `au_locale_block`, `system_prompt_output_contract`, `candidate_prompt_block`, `consent_legal_guidance`.
- Key prompt-context conflict: `au_locale_block` includes neutral/international guidance before the AU contract facts.

## Candidate Proposal Gate

Five candidates were presented to Tony before experiment config creation:

1. Correct `au_locale_block` by replacing neutral/international framing with strict AU locale guidance and precedence.
2. Add a `system_prompt_output_contract` precedence rule for conflicting user-requested locale tokens.
3. Add AU-specific Privacy Act 1988 and Spam Act 2003 consent/legal guidance.
4. Add AU field/property examples for phone, date, address, currency, and name labels.
5. Add a foreign-themed prompt adaptation rule for EU/UK/NZ/US-themed prompts that still target an AU audience.

Recommendation: run candidate 1 first as a controlled eval-only overlay, because it targets the highest-evidence root cause while preserving causal clarity.

Tony approved the recommended `AU-001` change set on 2026-05-05.

## Approved Experiment Config

- Config: `docs/stories/experiments/story-6.4.7-au-001.json`
- Overlay: `docs/stories/experiments/story-6.4.7-au-001-candidate-a.md`
- Experiment ID: `story-6.4.7-au-001`
- Candidate run ID: `story-6.4.7-au-001-candidate-a`
- Baseline run ID: `story-6.4.6-au-baseline-current`
- Prompt set: `backend/tests/form_ai_eval/prompts_au_v1.yaml`
- Scenario slice: `au-all`
- AU context conflict override: enabled for this controlled experiment because the frozen baseline prompt context contains the known neutral/international `au_locale_block` conflict being tested.
- Changed section: `candidate_prompt_block`
- Target metrics: `locale_fidelity`, `cross_locale_leakage`, `format_pattern_accuracy`, `policy_compliance`
- Known risk metrics: `field_coverage_recall`, `field_label_f1`, `copy_quality_score`

## Candidate Eval Run

- Command: `python -m backend.tests.form_ai_eval.experiment "docs\stories\experiments\story-6.4.7-au-001.json"`
- Result: completed.
- Candidate completed count: 45/45 rows.
- Candidate artifacts: `_bmad-output/eval-runs/story-6.4.7-au-001/`
- Candidate run folder: `_bmad-output/eval-runs/story-6.4.7-au-001/story-6.4.7-au-001-candidate-a/`
- Judge package: `_bmad-output/eval-runs/story-6.4.7-au-001/story-6.4.7-au-001-candidate-a/judge-package/`
- Diff artifacts: `_bmad-output/eval-runs/story-6.4.7-au-001/diffs/candidate-a/`
- Runtime notes: provider returned one transient 502 and one semantic-rules retry message; the harness completed the run. Repeated API logging mapper warnings appeared but did not halt generation.

## Early Deterministic And Diff Findings

- Generated-output deterministic AU findings moved from 130 baseline findings across 25 prompts to 9 candidate findings.
- Candidate prompt-context deterministic findings: 8 findings in `candidate_prompt_block`, caused by the overlay naming forbidden foreign tokens while instructing the model not to emit them.
- Remaining generated-output findings:
  - `p07-au-adversarial-r1`: 2 ZIP/Postcode findings and 2 foreign phone-code findings.
  - `p14-au-neutral-r1`: 4 NHS/NZ-region findings.
  - `p14-au-ambiguous-r1`: 1 NHS/NZ-region finding.
- Structural diff: blocked by `schema_valid_regression` for `p13-au-adversarial-r1`; candidate row has `schema_valid=False`, `terminal_reason=provider-error`, `failure_class=provider-fault`.
- Judge comparison: completed and ingested. Note: the Claude output was produced before the later "Sonnet 4.6 going forward" model preference; it remains the AU-001 evidence for this closed iteration.

## Judge Ingest And Final Comparison

- Ingest command: `python -m backend.tests.form_ai_eval.judge_ingest "_bmad-output\eval-runs\story-6.4.7-au-001\story-6.4.7-au-001-candidate-a\judge-package"`
- Ingest result: PASS after normalising Grok confidence values from percentage style to `0..1` and repairing the JSON newline suffix.
- Judge rows ingested: 45.
- Primary judges: Claude and Grok.
- Control judge: GPT-5 mini.
- Refreshed diff command: `python -m backend.tests.form_ai_eval.diff --baseline-run "_bmad-output\eval-runs\story-6.4.6-au-baseline-current" --variant-run "_bmad-output\eval-runs\story-6.4.7-au-001\story-6.4.7-au-001-candidate-a" --output-dir "_bmad-output\eval-runs\story-6.4.7-au-001\diffs\candidate-a"`

Metric movement:

- Improved: `locale_fidelity` 3.344 -> 4.678, `cross_locale_leakage` 3.522 -> 4.711, `format_pattern_accuracy` 3.344 -> 4.689, `policy_compliance` 3.789 -> 4.589, `row_group_agreement` 4.356 -> 4.478.
- Regressed: `field_coverage_recall` 4.433 -> 4.067, `validation_intent_accuracy` 3.767 -> 3.489, `copy_quality_score` 4.122 -> 3.956.
- Inconclusive/flat: `field_label_f1` 4.044 -> 4.078, `cultural_register` 3.900 -> 3.911.
- Blocking structural issue: `p13-au-adversarial-r1` schema-valid regression due to provider-fault row.

Decision:

- AU-001 is a useful measured change but is not promoted as-is.
- Reason: the strict AU direction clearly works for locale leakage, but the candidate is too narrow and introduces/retains issues: prompt-context lint findings, one schema-invalid row, lower field coverage, lower validation intent, and slightly worse copy quality.
- Tony direction on 2026-05-05: close this issue off and use Sonnet 4.6 for Claude-family judging going forward because it is cheaper.

Next recommended candidate:

- Move away from AU-only locale hardening and test a broader form-builder prompt improvement focused on field coverage, validation intent, and cleaner component planning across all form types.

## AU-002 Approved Experiment Config

- Tony approved the next round on 2026-05-05, aiming to retain AU-001's strong score lift while pushing the candidate into the 90s.
- Config: `docs/stories/experiments/story-6.4.7-au-002.json`
- Overlay: `docs/stories/experiments/story-6.4.7-au-002-candidate-a.md`
- Experiment ID: `story-6.4.7-au-002`
- Candidate run ID: `story-6.4.7-au-002-candidate-a`
- Baseline run ID: `story-6.4.6-au-baseline-current`
- Prompt set: `backend/tests/form_ai_eval/prompts_au_v1.yaml`
- Scenario slice: `au-all`
- Changed section: `candidate_prompt_block`
- Intent: cleaned AU-001 successor that avoids forbidden-token examples and adds form completeness, validation-intent, and copy-quality guards.
- Target metrics: `locale_fidelity`, `cross_locale_leakage`, `format_pattern_accuracy`, `policy_compliance`, `field_coverage_recall`, `validation_intent_accuracy`, `copy_quality_score`
- Known risk metrics: `field_label_f1`, `row_group_agreement`, `cultural_register`

## AU-003 Approved Experiment Config

- Tony requested AU-003 on 2026-05-06 to measure the combined effect of AU-001 and AU-002.
- Config: `docs/stories/experiments/story-6.4.7-au-003.json`
- Overlay: `docs/stories/experiments/story-6.4.7-au-003-candidate-a.md`
- Experiment ID: `story-6.4.7-au-003`
- Candidate run ID: `story-6.4.7-au-003-candidate-a`
- Baseline run ID: `story-6.4.6-au-baseline-current`
- Prompt set: `backend/tests/form_ai_eval/prompts_au_v1.yaml`
- Scenario slice: `au-all`
- Changed section: `candidate_prompt_block`
- Intent: direct combination of AU-001's explicit strict AU locale enforcement and AU-002's form completeness, validation-intent, and copy-quality guard.
- Target metrics: `locale_fidelity`, `cross_locale_leakage`, `format_pattern_accuracy`, `policy_compliance`, `field_coverage_recall`, `validation_intent_accuracy`, `copy_quality_score`
- Known risk metrics: `field_label_f1`, `row_group_agreement`, `cultural_register`

## AU-003 Run And Judge Results

- Generation run: completed 45/45 rows.
- Judge sessions: completed for Claude-family Sonnet 4.6, Grok, and GPT-5 mini control.
- Judge ingest: passed after normalising Grok percent-style confidence values and GPT-5 mini null confidence values.
- Diff refresh: completed against frozen baseline `story-6.4.6-au-baseline-current`.
- Average Category B score: baseline `3.862 / 5` (`77.2%`) -> AU-003 `4.344 / 5` (`86.9%`), net `+9.6` percentage points.
- AU-003 is the best judged candidate so far: AU-001 `4.264 / 5` (`85.3%`), AU-002 `3.914 / 5` (`78.3%`), AU-003 `4.344 / 5` (`86.9%`).
- Metric wins over baseline: `locale_fidelity` `3.344 -> 4.900`, `cross_locale_leakage` `3.522 -> 4.889`, `format_pattern_accuracy` `3.344 -> 4.889`, `policy_compliance` `3.789 -> 4.444`, `validation_intent_accuracy` `3.767 -> 3.944`, `field_coverage_recall` `4.433 -> 4.467`, `cultural_register` `3.900 -> 3.978`.
- Metric regressions: `row_group_agreement` `4.356 -> 4.011`, `copy_quality_score` `4.122 -> 3.922`, `field_label_f1` `4.044 -> 4.000`.
- Deterministic AU checks: AU-003 has 25 total findings, including 8 prompt-context findings and 17 generated-output findings across 6 rows. This is much better than AU-002's 122 generated-output findings, but worse than AU-001's 17 total findings / 9 generated-output findings.
- Recommendation: keep AU-003 as the winning direction, but do not promote the literal overlay as-is. The next step should be a cleaned AU-004 or production prompt patch that moves the combined rules into the base AU prompt sections without explicit forbidden-token examples, resolves the neutral-vs-strict AU context conflict, and adds a "silently substitute AU equivalents" rule for adversarial foreign cues.
- Evidence: `_bmad-output/eval-runs/story-6.4.7-au-003/`, `_bmad-output/eval-runs/story-6.4.7-au-003/story-6.4.7-au-003-candidate-a/judge-package/judge-ingest-summary.json`, `_bmad-output/eval-runs/story-6.4.7-au-003/diffs/candidate-a/diff-summary.json`, `docs/stories/STORY-6-AU-EVAL-ITERATION-TRACKING.md`, `au-candidate-metrics.canvas.tsx`.

## AU-004 Approved Experiment Config

- Tony approved AU-004 on 2026-05-06 after reviewing that AU-003 outperformed AU-001 and AU-002 individually.
- Config: `docs/stories/experiments/story-6.4.7-au-004.json`
- Overlay: `docs/stories/experiments/story-6.4.7-au-004-candidate-a.md`
- Experiment ID: `story-6.4.7-au-004`
- Candidate run ID: `story-6.4.7-au-004-candidate-a`
- Baseline run ID: `story-6.4.6-au-baseline-current`
- Prompt set: `backend/tests/form_ai_eval/prompts_au_v1.yaml`
- Scenario slice: `au-all`
- Changed section: `candidate_prompt_block`
- Intent: use AU-003 as the behavioural base, but remove explicit forbidden examples, require silent AU substitution, and retain the form completeness / validation / copy-quality guard.
- Target metrics: `locale_fidelity`, `cross_locale_leakage`, `format_pattern_accuracy`, `policy_compliance`, `field_coverage_recall`, `validation_intent_accuracy`, `copy_quality_score`, `row_group_agreement`
- Known risk metrics: `field_label_f1`, `cultural_register`

## AU-004 Run And Judge Results

- Generation run: completed 45/45 rows.
- Prompt-context lint: passed with 0 findings.
- Judge sessions: completed for Claude-family Sonnet 4.6, Grok, and GPT-5 mini control.
- Judge ingest: passed after normalising Grok percent-style confidence values.
- Diff refresh: completed against frozen baseline `story-6.4.6-au-baseline-current`.
- Average Category B score: baseline `3.862 / 5` (`77.2%`) -> AU-004 `4.094 / 5` (`81.9%`), net `+4.6` percentage points.
- Comparison to prior candidates: AU-001 `4.264 / 5` (`85.3%`), AU-002 `3.914 / 5` (`78.3%`), AU-003 `4.344 / 5` (`86.9%`), AU-004 `4.094 / 5` (`81.9%`).
- Metric wins over baseline: `locale_fidelity` `3.344 -> 4.600`, `cross_locale_leakage` `3.522 -> 4.500`, `format_pattern_accuracy` `3.344 -> 4.478`, `policy_compliance` `3.789 -> 3.967`.
- Metric regressions: `field_coverage_recall` `4.433 -> 4.056`, `validation_intent_accuracy` `3.767 -> 3.578`, `row_group_agreement` `4.356 -> 3.944`, `cultural_register` `3.900 -> 3.767`, `copy_quality_score` `4.122 -> 4.044`, `field_label_f1` `4.044 -> 4.011`.
- Deterministic AU checks: AU-004 has 44 generated-output findings across 10 rows and 0 prompt-context findings. This confirms the cleaned wording fixed AU-003's prompt lint but weakened generated-output resistance.
- Recommendation: do not promote AU-004. Keep AU-003 as the behavioural base. The next improvement should preserve AU-003's strong enforcement and solve lint through prompt architecture/section placement rather than softening the rule language.
- Evidence: `_bmad-output/eval-runs/story-6.4.7-au-004/`, `_bmad-output/eval-runs/story-6.4.7-au-004/story-6.4.7-au-004-candidate-a/judge-package/judge-ingest-summary.json`, `_bmad-output/eval-runs/story-6.4.7-au-004/diffs/candidate-a/diff-summary.json`, `docs/stories/STORY-6-AU-EVAL-ITERATION-TRACKING.md`, `au-candidate-metrics.canvas.tsx`.

## AU-005 Approved Experiment Config

- Tony approved AU-005 on 2026-05-06 after reviewing variant, form-type, and judge "why not 5" lenses.
- Config: `docs/stories/experiments/story-6.4.7-au-005.json`
- Overlay: `docs/stories/experiments/story-6.4.7-au-005-candidate-a.md`
- Experiment ID: `story-6.4.7-au-005`
- Candidate run ID: `story-6.4.7-au-005-candidate-a`
- Baseline run ID: `story-6.4.6-au-baseline-current`
- Prompt set: `backend/tests/form_ai_eval/prompts_au_v1.yaml`
- Scenario slice: `au-all`
- Changed section: `candidate_prompt_block`
- Intent: keep AU-003's strict AU behavioural base and add a narrow publish-ready polish pass for consent/legal specificity, validation intent, section ordering, over-scoping, and copy quality.
- Target metrics: `locale_fidelity`, `cross_locale_leakage`, `format_pattern_accuracy`, `policy_compliance`, `field_coverage_recall`, `validation_intent_accuracy`, `copy_quality_score`, `row_group_agreement`
- Known risk metrics: `field_label_f1`, `cultural_register`

## AU-005 Run And Judge Results

- Generation run: completed 45/45 rows.
- Judge sessions: completed for Claude-family Sonnet 4.6, Grok, and GPT-5 mini control.
- Judge ingest: passed after normalising GPT-5 mini null confidence values.
- Diff refresh: completed against frozen baseline `story-6.4.6-au-baseline-current`.
- Average Category B score: baseline `3.862 / 5` (`77.2%`) -> AU-005 `4.471 / 5` (`89.4%`), net `+12.2` percentage points.
- Comparison to prior candidates: AU-001 `4.264 / 5` (`85.3%`), AU-002 `3.914 / 5` (`78.3%`), AU-003 `4.344 / 5` (`86.9%`), AU-004 `4.094 / 5` (`81.9%`), AU-005 `4.471 / 5` (`89.4%`).
- Variant averages: neutral `4.277 -> 4.553`, ambiguous `4.253 -> 4.490`, adversarial `3.057 -> 4.370`. AU-005 improves all three variants and edges AU-003 on judged adversarial average.
- Metric wins over baseline: `field_coverage_recall` `4.433 -> 4.833`, `validation_intent_accuracy` `3.767 -> 4.244`, `row_group_agreement` `4.356 -> 4.533`, `locale_fidelity` `3.344 -> 4.733`, `policy_compliance` `3.789 -> 4.389`, `cultural_register` `3.900 -> 4.300`, `cross_locale_leakage` `3.522 -> 4.744`, `format_pattern_accuracy` `3.344 -> 4.678`, `copy_quality_score` `4.122 -> 4.344`.
- Metric weakness: `field_label_f1` `4.044 -> 3.911`, statistically inconclusive but still below baseline and below AU-003.
- Deterministic AU checks: AU-005 has 24 total findings, including 8 prompt-context findings and 16 generated-output findings across 5 rows. This is slightly better than AU-003's 25 total / 17 generated-output findings, but still not clean enough to promote as a literal overlay.
- Form-type readout: AU-005 is best on 11 of 15 prompt families. AU-003 remains best for `p01` event registration, `p14` UK/NHS waiver, and `p15` NZ RSVP; AU-001 remains best for `p13` US PII onboarding.
- Recommendation: AU-005 is the strongest candidate direction so far and should become the promotion target, subject to converting the eval-only overlay into production prompt sections that remove explicit forbidden-token prompt-context lint while preserving AU-005's strict behavioural force.
- Evidence: `_bmad-output/eval-runs/story-6.4.7-au-005/`, `_bmad-output/eval-runs/story-6.4.7-au-005/story-6.4.7-au-005-candidate-a/judge-package/judge-ingest-summary.json`, `_bmad-output/eval-runs/story-6.4.7-au-005/diffs/candidate-a/diff-summary.json`, `docs/stories/STORY-6-AU-EVAL-ITERATION-TRACKING.md`, `au-candidate-metrics.canvas.tsx`.

## AU-006 Approved Experiment Config

- Tony approved AU-006 on 2026-05-06 after AU-005 became the strongest judged candidate but retained prompt-context lint from explicit enforcement.
- Config: `docs/stories/experiments/story-6.4.7-au-006.json`
- Overlay: `docs/stories/experiments/story-6.4.7-au-006-candidate-a.md`
- Experiment ID: `story-6.4.7-au-006`
- Candidate run ID: `story-6.4.7-au-006-candidate-a`
- Baseline run ID: `story-6.4.6-au-baseline-current`
- Prompt set: `backend/tests/form_ai_eval/prompts_au_v1.yaml`
- Scenario slice: `au-all`
- Changed section: `candidate_prompt_block`
- Intent: production-style rewrite of AU-005 that avoids literal forbidden examples while preserving hard AU output constraints and publish-ready polish.
- Target metrics: `locale_fidelity`, `cross_locale_leakage`, `format_pattern_accuracy`, `policy_compliance`, `field_coverage_recall`, `validation_intent_accuracy`, `copy_quality_score`, `row_group_agreement`, `field_label_f1`
- Known risk metrics: `cultural_register`

## AU-006 Run And Judge Results

- Generation run: completed 45/45 rows.
- Prompt-context lint: passed with 0 findings. This achieves the main production-rewrite objective that AU-005 could not meet as a literal overlay.
- Deterministic AU checks: 3 generated-output findings and 0 prompt-context findings. Remaining leakage is isolated to `p11`: one foreign phone-code match in `p11-au-neutral-r1`, plus two Auckland matches in `p11-au-ambiguous-r1`.
- Judge sessions: completed for Claude-family Sonnet 4.6, Grok, and GPT-5 mini control.
- Judge ingest: passed after completing the Grok output file to include all 45 expected rows.
- Diff refresh: completed against frozen baseline `story-6.4.6-au-baseline-current`.
- Average Category B score: baseline `3.862 / 5` (`77.2%`) -> AU-006 `4.214 / 5` (`84.3%`), net `+7.0` percentage points.
- Comparison to prior candidates: AU-001 `4.264 / 5` (`85.3%`), AU-002 `3.914 / 5` (`78.3%`), AU-003 `4.344 / 5` (`86.9%`), AU-004 `4.094 / 5` (`81.9%`), AU-005 `4.471 / 5` (`89.4%`), AU-006 `4.214 / 5` (`84.3%`).
- Metric wins over baseline: `locale_fidelity` `3.344 -> 4.656`, `cross_locale_leakage` `3.522 -> 4.867`, `format_pattern_accuracy` `3.344 -> 4.567`, `cultural_register` `3.900 -> 4.411`, `field_coverage_recall` `4.433 -> 4.544`.
- Metric regressions: `policy_compliance` `3.789 -> 3.567`, `validation_intent_accuracy` `3.767 -> 3.433`, `copy_quality_score` `4.122 -> 3.878`; `field_label_f1` and `row_group_agreement` are slightly below baseline / inconclusive.
- Recommendation: do not promote AU-006 over AU-005. Keep AU-006's lint-clean locale-conflict wording, but reintroduce AU-005's explicit AU policy/consent specificity, validation-intent guard, and publish-ready copy quality in a non-lint-triggering way.
- Evidence: `_bmad-output/eval-runs/story-6.4.7-au-006/`, `_bmad-output/eval-runs/story-6.4.7-au-006/story-6.4.7-au-006-candidate-a/judge-package/judge-ingest-summary.json`, `_bmad-output/eval-runs/story-6.4.7-au-006/story-6.4.7-au-006-candidate-a/prompt-context-lint.json`, `_bmad-output/eval-runs/story-6.4.7-au-006/story-6.4.7-au-006-candidate-a/au-deterministic-checks.json`, `_bmad-output/eval-runs/story-6.4.7-au-006/diffs/candidate-a/diff-summary.json`, `docs/stories/experiments/story-6.4.7-au-006.json`, `au-candidate-metrics.canvas.tsx`.

## Story Closeout

- Tony requested Story 6.4.7 closeout on 2026-05-06.
- Closeout report: `docs/stories/STORY-6.4.7-CLOSEOUT-REPORT.md`
- Final decision: close Story 6.4.7 as complete. It is an Analyst-owned evidence/decision story, not the production prompt implementation story.
- Top performer: `AU-005` with `4.471 / 5` (`89.4%`), net `+12.2` percentage points over baseline.
- Production note: the follow-up implementation should promote AU-005's strict AU + publish-ready behaviour into production prompt/context sections, using AU-006's lint-clean conflict wording lessons while restoring AU-005's policy, validation, and copy-quality strength.
