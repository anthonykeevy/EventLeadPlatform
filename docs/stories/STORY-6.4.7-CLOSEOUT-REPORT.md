# Story 6.4.7 Closeout Report

## Story Outcome

Story 6.4.7 is closed as an Analyst-owned AU prompt evaluation and decision story.

The story met its purpose: it used the frozen `AU-000` baseline from Story 6.4.6 to run controlled AU prompt/context experiments, compare deterministic and judge evidence, and identify the strongest promotion direction for production prompt work.

## Decision

- Close Story 6.4.7 as complete.
- Do not promote any eval-only overlay literally into production from this story.
- Treat `AU-005` as the top-performing candidate and the production implementation target.
- Use `AU-006` as supporting evidence for how to remove prompt-context lint, not as the winning prompt behaviour.

## Top Performer: AU-005

`AU-005` was the strongest judged candidate.

- Average score: baseline `3.862 / 5` (`77.2%`) -> AU-005 `4.471 / 5` (`89.4%`).
- Net improvement: `+12.2` percentage points.
- Variant averages improved across all variants:
  - Neutral: `4.277 -> 4.553`
  - Ambiguous: `4.253 -> 4.490`
  - Adversarial: `3.057 -> 4.370`
- AU-005 was best on 11 of 15 prompt families.
- AU-005 improved the key production-quality dimensions that matter for the form builder:
  - `field_coverage_recall`
  - `validation_intent_accuracy`
  - `row_group_agreement`
  - `locale_fidelity`
  - `policy_compliance`
  - `cultural_register`
  - `cross_locale_leakage`
  - `format_pattern_accuracy`
  - `copy_quality_score`

AU-005 should not be copied into production as-is because it still produced prompt-context lint findings from explicit forbidden-token language. Its behaviour is the target; its eval-only wording is not the production patch.

## Production Prompt Improvements To Implement

The follow-up production prompt work should preserve AU-005's behavioural gains while avoiding AU-005's literal overlay lint issue.

Recommended production changes:

- Make `audienceLocale = AU` the authoritative output contract for all generated form copy and component configuration.
- Use Australian English and AU conventions for phone, dates, address labels, currency, privacy, marketing-message consent, waivers, terms, and acknowledgements.
- Preserve AU-005's strict locale-conflict behaviour: when the user prompt includes a foreign-market cue that conflicts with AU, generate the Australian equivalent unless the field is explicitly collecting an external destination/source-market value.
- Use AU-006's lint-clean style for conflict handling: describe categories of conflicting cues and substitution behaviour without embedding long lists of forbidden foreign examples in prompt text.
- Reintroduce AU-005's AU legal/policy specificity in production wording:
  - Privacy Act 1988
  - Spam Act 2003
  - AU Privacy Principles where appropriate
  - concise AU-appropriate consent, terms, acknowledgement, waiver, and marketing-update wording
- Keep AU-005's form completeness and validation guard:
  - include every material field group requested by the user
  - make required/optional intent explicit through `validationIntent`
  - use the most specific supported component type
  - preserve requested sections, validation rules, and key options while applying AU localisation
- Keep AU-005's publish-ready polish guard:
  - identity/contact first
  - form-specific choices next
  - operational notes/preferences after that
  - consent/terms near the end
  - avoid adding address, organisation, role, or extra context fields unless requested or clearly necessary
  - prefer checkbox or terms acknowledgement patterns over typed signatures unless a signature is explicitly requested

Special attention for the follow-up implementation:

- Preserve AU-006's prompt-context lint win: `0` prompt-context findings.
- Do not repeat AU-006's quality regression: generic privacy/marketing wording, weak validation intent, and weaker copy polish.
- Add a targeted rule for `p11`-style international event/timezone prompts: avoid generated timezone options or labels that introduce foreign phone-code-like strings or overseas region names unless the form is explicitly collecting an external value.
- Watch `field_label_f1`, `p01`, `p14`, and `p15`, where earlier candidates showed trade-offs.

## Evidence Summary

- Baseline: `story-6.4.6-au-baseline-current`
- Top performer: `story-6.4.7-au-005-candidate-a`
- Lint-clean lesson candidate: `story-6.4.7-au-006-candidate-a`
- Metrics canvas: `au-candidate-metrics.canvas.tsx`
- Iteration tracking: `docs/stories/STORY-6-AU-EVAL-ITERATION-TRACKING.md`
- Gate evidence: `docs/stories/STORY-6.4.7-GATE-EVIDENCE.md`
- AU-005 evidence:
  - `_bmad-output/eval-runs/story-6.4.7-au-005/`
  - `_bmad-output/eval-runs/story-6.4.7-au-005/story-6.4.7-au-005-candidate-a/judge-package/judge-ingest-summary.json`
  - `_bmad-output/eval-runs/story-6.4.7-au-005/diffs/candidate-a/diff-summary.json`
- AU-006 evidence:
  - `_bmad-output/eval-runs/story-6.4.7-au-006/`
  - `_bmad-output/eval-runs/story-6.4.7-au-006/story-6.4.7-au-006-candidate-a/judge-package/judge-ingest-summary.json`
  - `_bmad-output/eval-runs/story-6.4.7-au-006/story-6.4.7-au-006-candidate-a/prompt-context-lint.json`
  - `_bmad-output/eval-runs/story-6.4.7-au-006/story-6.4.7-au-006-candidate-a/au-deterministic-checks.json`

## Follow-Up Story Recommendation

Create a separate production implementation story:

**Promote AU-005 prompt improvements into production AU prompt sections**

Suggested goal:

Convert AU-005's winning strict AU + publish-ready behaviour into the production prompt/context path, using AU-006's lint-clean conflict wording and preserving AU-005's explicit AU legal, validation, and copy-quality strength.

Suggested acceptance criteria:

- Production prompt/context artifacts implement the AU-005 behaviour without eval-only overlays.
- Prompt-context lint remains at `0` findings.
- AU deterministic generated-output findings stay close to AU-006's `3` findings and materially below AU-005's `16`.
- Judge score remains close to AU-005's `4.471 / 5` and does not repeat AU-006's regressions in `policy_compliance`, `validation_intent_accuracy`, or `copy_quality_score`.
- The `p11` timezone/international-event leakage case is specifically addressed.
- Focused harness tests and an AU eval slice are run before promotion.

## Verification

Focused Analyst green gate passed on 2026-05-06:

```powershell
python -m pytest backend/tests/test_form_ai_eval_experiment.py backend/tests/test_judge_pack.py backend/tests/test_judge_ingest.py backend/tests/test_eval_diff.py --tb=short
```

Result: `18 passed`, `116 warnings`.
