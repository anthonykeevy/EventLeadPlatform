# Story 6.4.6 - AU-Only Diagnostic Evaluation Framework + Baseline

**Epic:** 6 - AI Generation & Monetization Engine  
**Story ID:** 6.4.6  
**Title:** AU-Only Diagnostic Evaluation Framework + Baseline  
**Status:** Complete  
**Branch:** `story/epic6-6.4.6-au-diagnostic-eval-framework`  
**PR:** [#82](https://github.com/anthonykeevy/EventLeadPlatform/pull/82) - Merged 2026-04-30  
**Created:** 2026-04-29  
**Depends On:** Story 6.4.5 ([PR #81](https://github.com/anthonykeevy/EventLeadPlatform/pull/81)) merged.  
**Unblocks:** Story 6.4.7 - AU Baseline Analysis And Iterative Prompt Improvement Loop.

---

## 1) Goal

Build the AU-only diagnostic evaluation framework and prove it works by producing the first current-state AU baseline result set.

This story is a framework and baseline story. It must not test or ship prompt improvements. Success means the next BMAD Analyst story can review a clean AU baseline, trace weaknesses to prompt/context sections, propose controlled changes to Tony, and iterate without relying on chat memory.

---

## 2) In Scope

### 2.1 AU benchmark prompt set

Create an AU launch benchmark prompt set focused on Australian use cases.

Requirements:

- Keep broad form-type variety across event registration, lead capture, surveys, RSVPs, applications, bookings, onboarding, donations, waivers, feedback, and consent-heavy forms.
- Make audience/event context clearly Australian unless a row is explicitly tagged as an adversarial source-market adaptation test.
- Replace or rewrite existing non-AU market rows where they add launch noise.
- Remove accidental foreign-market concepts such as NHS, UK GDPR, NZ regions, ZIP/+1, +44/+64, EU lawful basis, CCPA-only privacy wording, and US/UK/NZ-specific address cues unless the row is intentionally adversarial.
- Use stable row IDs and metadata that make row-level comparison easy in Story 6.4.7.
- Preserve enough repetitions to identify row-level instability without returning to the previous six-locale sweep.

### 2.2 AU locale contract

Create a version-managed AU locale contract from existing DB/config facts and the approved launch requirements.

The contract must cover:

- +61 phone guidance.
- DD/MM/YYYY dates.
- Suburb, State, Postcode address shape.
- AUD currency.
- Privacy Act 1988.
- Spam Act 2003.
- Australian English.
- Practical/plain-English tone.

Do not invent new product policy. If a contract fact cannot be traced to existing config/DB facts or the approved story text, document the source/assumption in the evidence file.

### 2.3 Prompt-context consistency preflight/linter

Add a deterministic preflight that checks the complete LLM prompt context before generation.

The preflight must:

- Inspect the complete prompt context sent to the LLM for each AU eval row.
- Report conflicting prompt/context data before the eval run proceeds.
- Use stable section IDs for each prompt/context area.
- Include content hashes for shared context sections.
- Identify the likely section responsible for each deterministic conflict.
- Write machine-readable and human-readable artifacts into the eval run folder.

### 2.4 Shared context bundle for judge packages

Ensure the judge package includes complete prompt context efficiently.

Each run must include:

- One shared sectioned context bundle per run.
- Stable section IDs for every prompt/context area.
- Content hashes for each shared section.
- Per-case user prompt, generation output, expected AU signals, deterministic AU findings, and references to shared section IDs.

Shared sections must include:

- System prompt / output contract.
- AU locale block.
- Brand posture block.
- Component capability block.
- Component property cheat sheet if active.
- Consent/legal guidance.
- Context pack excerpt.
- Candidate prompt block if active.

### 2.5 Judge diagnostics

Extend judge prompts/templates/ingest so judge output includes:

- Metric scores.
- Rationale.
- Whether conflicting data exists in the complete prompt.
- Conflict description.
- Likely prompt/context section responsible for the low score.
- Suggested correction.
- Confidence level.

The diagnostics must be validated by automated tests and included in the ingested summary artifacts.

### 2.6 Deterministic AU checks

Add deterministic AU checks for common failures:

- ZIP where Postcode is expected.
- +1, +44, or +64 where +61 or neutral AU guidance is expected.
- MM/DD/YYYY where DD/MM/YYYY is expected.
- GDPR/CCPA-only privacy wording where AU privacy wording is expected.
- NHS, NZ-region, or other foreign-market leakage unless explicitly marked as intentional.

Checks should run against the complete prompt context and generated output where applicable.

### 2.7 Current-state AU baseline

Run the current-state AU baseline after the framework is implemented.

The baseline must:

- Use the new AU benchmark prompt set.
- Use current `master` prompt behavior only.
- Not include candidate prompt improvements.
- Generate the judge package.
- Produce three judge prompt files for Claude, Grok, and GPT-5 mini.
- Ingest judge outputs after Tony saves them.
- Record baseline evidence and update the AU iteration tracking row `AU-000`.

---

## 3) Out of Scope


| Item                                                | Reason / future home                                                    |
| --------------------------------------------------- | ----------------------------------------------------------------------- |
| Prompt/context improvements                         | Story 6.4.7 Analyst loop after Tony approval.                           |
| H5/style, H6/font, or other prompt-candidate sweeps | Deferred until AU diagnostic framework exists and baseline is reviewed. |
| Six-locale benchmark continuation                   | Explicitly paused by the AU-first reset.                                |
| Application API changes                             | This story is eval framework/test tooling, not product API.             |
| Frontend UI changes                                 | No UI surface expected.                                                 |
| Alembic migrations                                  | Not expected; agents must not run Alembic commands.                     |
| Judge model API automation                          | Cursor/manual judge flow remains in place.                              |
| Declaring a prompt winner                           | Baseline only; Story 6.4.7 decides candidate changes.                   |


---

## 4) Acceptance Criteria

1. **AC-1 AU prompt set exists:** An AU-only benchmark prompt set exists with stable IDs, AU launch contexts, and explicit adversarial tags where foreign-market source material is intentional.
2. **AC-2 Foreign noise reviewed:** Accidental NHS, UK GDPR, NZ regions, ZIP/+1, EU lawful basis, CCPA-only, and similar foreign-market cues are removed or tagged as intentional adversarial inputs.
3. **AC-3 AU contract exists:** A version-managed AU locale contract records +61, DD/MM/YYYY, Suburb/State/Postcode, AUD, Privacy Act 1988, Spam Act 2003, Australian English, and practical/plain-English tone.
4. **AC-4 Context preflight exists:** The complete LLM prompt context can be assembled into stable sections and linted before generation.
5. **AC-5 Shared context bundle packaged:** Judge packages include one shared context bundle with section IDs/content hashes plus per-case references.
6. **AC-6 Judge diagnostics extended:** Judge prompt/template/ingest support conflict flags, conflict descriptions, likely responsible sections, suggested corrections, and confidence.
7. **AC-7 Deterministic AU checks implemented:** Deterministic AU checks report common AU failures in machine-readable and human-readable artifacts.
8. **AC-8 Current-state AU baseline complete:** The baseline run uses current prompt behavior only and records run IDs/output paths.
9. **AC-9 Judge outputs ingested:** Claude, Grok, and GPT-5 mini judge outputs are saved, validated, ingested, and summarized.
10. **AC-10 Tracking sheet updated:** `STORY-6-AU-EVAL-ITERATION-TRACKING.md` row `AU-000` is updated with baseline run ID, judge/diagnostic findings, deterministic AU failures, decision, and evidence links.
11. **AC-11 Evidence docs complete:** `STORY-6.4.6-AU-BASELINE-EVIDENCE.md`, gate evidence, UAT results, and closeout report are filled.
12. **AC-12 Green gates recorded:** Focused tests and backend regression evidence are recorded; frontend checks are only required if frontend files are touched.
13. **AC-13 No prompt improvement leakage:** No candidate prompt/context improvement is applied or tested in this story.

---

## 5) Definition of Done

- All ACs are mapped to evidence.
- Story branch is pushed to PR #82.
- AU baseline artifacts are preserved under `_bmad-output/eval-runs/`.
- `AU-000` tracking row is filled for Story 6.4.7 handoff.
- No untracked scratch artifacts are committed.
- Stale-field audit passes before merge.
- Closeout report recommends Story 6.4.7 as the next story.