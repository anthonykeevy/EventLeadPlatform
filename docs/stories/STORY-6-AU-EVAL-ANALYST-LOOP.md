# Story 6 AU Eval Analyst Loop

## Purpose

The AU-only evaluation loop exists to improve individual Form AI generation results for the Australian launch market. The goal is not simply a higher aggregate score. The goal is to understand which prompt/context section caused each weakness, test one controlled change at a time, and preserve evidence about what improved or regressed so failed changes are not repeated.

This document is the persistent process anchor for the BMAD Analyst. If chat context is summarised or lost, resume from this document plus the tracking sheet, not from memory.

## Current Benchmark Scope

The launch benchmark is Australia-first.

- Audience/event context should be clearly AU unless a row is explicitly marked as an adversarial source-market adaptation test.
- Non-AU concepts such as NHS, UK GDPR, NZ regions, ZIP/+1, EU lawful basis, US/UK/NZ-specific language, and foreign-market compliance cues are failures unless explicitly tagged as intentional adversarial source-market inputs.
- AU locale contract includes +61 phone guidance, DD/MM/YYYY dates, Suburb/State/Postcode address shape, AUD, Privacy Act 1988, Spam Act 2003, Australian English, and practical/plain-English tone.

## Artifact Locations

Baseline and candidate runs:

- `_bmad-output/eval-runs/<au-run-id>/`

Judge packages:

- `_bmad-output/eval-runs/<au-run-id>/judge-package/`

Tracking sheet:

- `docs/stories/STORY-6-AU-EVAL-ITERATION-TRACKING.md`

Framework instructions:

- Story 6.4.6 story pack and gate evidence once created.

## Required Shared Context Package

Each judge package must include the complete prompt context efficiently:

- One shared sectioned context bundle per run.
- Stable section IDs for every prompt/context area.
- Content hash for each shared section.
- Per-case user prompt, generation output, expected AU signals, and references to shared section IDs.

Shared sections must include:

- System prompt / output contract.
- AU locale block.
- Brand posture block.
- Component capability block.
- Component property cheat sheet if active.
- Consent/legal guidance.
- Context pack excerpt.
- Candidate prompt block if active.

## Judge Diagnostics

Judge outputs must include:

- Metric scores.
- Rationale.
- Whether conflicting data exists in the complete prompt.
- Conflict description.
- Likely prompt/context section responsible for the low score.
- Suggested correction.
- Confidence level.

The Analyst must review judge conflict findings before changing prompt text.

## Iteration Tracking Fields

Every loop must update the tracking sheet with:

- Iteration ID.
- Date/time.
- Baseline run ID.
- Candidate run ID.
- Prompt/context section changed.
- Change tested.
- Hypothesis.
- Expected metric movement.
- Actual metric movement.
- Metrics improved.
- Metrics regressed.
- Individual prompt rows improved/regressed.
- Judge conflict findings.
- Deterministic AU check failures.
- Judge-suggested correction.
- Decision: keep / reject / revise.
- Reason.
- Follow-up action.
- Evidence links.

## Analyst Loop Steps

1. Read this process document, the current tracking sheet, and the latest AU framework instructions.
2. Review the latest AU baseline/candidate results.
3. Analyse metric movement, low-scoring individual prompt rows, deterministic AU failures, judge disagreement, judge-identified conflicting prompt/context data, and judge suggestions.
4. Present Tony with the top 5 candidate prompt/context improvements.
5. For each candidate, explain:
   - target prompt/context section,
   - expected metric movement,
   - risk,
   - whether it can be safely bundled with any other candidate without distorting causality.
6. Recommend one controlled change or one tightly related change set.
7. Stop for Tony approval.
8. After Tony approves, update only version-managed prompt/context artifacts and the tracking sheet. Do not modify application, harness, judge-ingest, frontend, or backend code.
9. Run the AU eval as a background task.
10. Run the three judge evaluations as background tasks until all three complete.
11. Ingest judge outputs.
12. Compare the candidate result against the prior baseline/candidate.
13. Summarise what changed, what was expected, what actually happened, why it differed, whether to keep/reject/revise, and the suggested next change.
14. Stop and ask Tony for continue/stop before the next loop.

## Hard Rules

- Tony approves continue/stop after every loop.
- Only one controlled change set is tested per iteration.
- Do not make multiple unrelated prompt/context changes in one loop.
- Judge conflict findings must be reviewed before changing prompt text.
- Story 2 / Analyst loop may update version-managed prompt/context files and tracking documents only.
- If code changes are needed, stop and raise a Dev-owned framework fix story.
- If context is summarised, resume from this document and the tracking sheet.

