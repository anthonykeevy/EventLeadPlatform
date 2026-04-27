# Story 6.4.4.1 ADR — Rubric v2 Governance

**Status:** Accepted for `rubric_v2`. Supersedes `rubric_v1` (governed by [`STORY-6.4.3b-RUBRIC-ADR.md`](./STORY-6.4.3b-RUBRIC-ADR.md), which now carries a supersession footer).
**Story:** 6.4.4.1 — Locale Architecture: Wire the Registry.
**Decision Owner:** SM + Dev; Architect review required for any subsequent rubric version change.
**Date:** 2026-04-27

---

## Context

`rubric_v1` was governed by `STORY-6.4.3b-RUBRIC-ADR.md` and used by Story 6.4.4 in the prompt-shrink sweep evaluation. PM/Tonyk review of the Story 6.4.4 results surfaced two structural problems with the v1 measurement architecture (full reasoning in [`STORY-6.4.4-CLOSEOUT-AMENDMENT.md`](./STORY-6.4.4-CLOSEOUT-AMENDMENT.md) §1):

1. **Two of three judges flatlined.** Across 5 runs × 60 cells × 3 judges = 900 cells, **Gemini 2.5 Flash and GPT-5 mini both gave 60/60 perfect 5/5 in every variant**. Claude was the only judge that moved. The Claude+Gemini "primary mean" was Gemini-flatline-dominated; every Claude-detected regression was exactly halved. "Rerun-at-n=15" cannot fix this — Gemini's variance was structurally zero.
2. **`locale_fidelity` had no ground truth.** None of the 10 v1 benchmark prompts specified a target locale. The judge package contained no locale anchor. Claude inferred AU strictness from output context clues (`+61`, "organisation") and applied its own model-internal AU-pedantry. Tonyk's lived AU experience confirmed several of Claude's downscores were false positives ("First name / Last name" is fine in AU; mandatory `+61` prefix on a domestic AU form is over-specification, not a fidelity bonus).

Four parallel research agents converged on a 9-element rubric with deterministic + LLM-judged scoring; Tonyk's lived-AU calibration anchors became the new ground truth.

---

## Decision

### 1. Replace the single-anchor `locale_fidelity` metric with a 9-element rubric

| # | Element | Method | Anchor scale |
|---|---|---|---|
| 1 | Date format matches `audienceLocale` | **Deterministic** (regex) | 0=wrong, 1=mixed, 2=correct |
| 2 | Phone format & country code matches | **Deterministic** (regex; consults `config.ValidationRule.ValidationPattern` per CountryID) | 0=mandates wrong/foreign code, 1=ambiguous, 2=correct + appropriate |
| 3 | Address schema matches | **Deterministic** (field-name presence) | 0=wrong (e.g. ZIP in AU), 1=partial, 2=correct |
| 4 | Consent/privacy citation correct | **LLM-judged** | 0=wrong Act, 1=generic, 2=correct |
| 5 | Currency / number format matches | **Deterministic** (regex) | 0=wrong, 1=ambiguous, 2=correct |
| 6 | Name-field convention matches | **Deterministic** (label list) | 0=wrong (mandatory honorifics in low-PDI), 1=partial, 2=correct |
| 7 | Tone register matches Hofstede PDI/UAI | **LLM-judged** | 0=clash, 1=neutral, 2=appropriate |
| 8 | Mandatory-field strictness matches UAI | **LLM-judged** | 0=clash, 1=neutral, 2=appropriate |
| 9 | Cross-locale leakage absent | **Deterministic** | 0=US conventions present in non-US locale, 2=clean |

**Origin note (per Tonyk Q8):** the rubric fuses Memo 2's 8-element design with Memo 3's cross-locale-leakage (item 9) addition. Anyone reading Memo 2 standalone will see "8 elements"; Memo 3 introduces the 9th. The rubric_v2 file (`backend/tests/form_ai_eval/rubric_v2.md`) and this ADR are the canonical 9-element source.

**Score range per item:** 0/1/2 (replaces v1's 0/1/2/3/4/5 wider range). Total score = sum across all 9 items, range 0–18.

### 2. Methodology split (deterministic + LLM-judged)

- **Items 1, 2, 3, 5, 6, 9 (deterministic):** computed in code, free per generation, run on every cell.
- **Items 4, 7, 8 (LLM-judged):** scored via the manual Cursor judge flow, run on whichever subset survives deterministic gates (or the full set, depending on the eval run configuration).

Deterministic items can produce a fast verdict before incurring LLM-judge cost. The Story 6.4.3c diff/stats tooling already handles deterministic Category A blocking; v2 extends it to deterministic locale items by treating them as Category A-style blocking when configured.

### 3. Calibration anchors — Tonyk's lived AU experience (must be in `rubric_v2.md`)

These anchors resolve the v1 false-positive issue (Claude's AU-pedantry without ground-truth):

| Item | Anchor | Score |
|---|---|---|
| 6 (name-field) | "First name / Last name" labels (AU) | 2 |
| 6 (name-field) | "Given name / Surname" labels (AU) | 2 (also acceptable) |
| 2 (phone) | Mandatory `+61` prefix in placeholder on AU domestic form | 0 |
| 2 (phone) | Phone helpText "Include country code if overseas" (AU) | 2 |
| 1 (date) | DD/MM/YYYY (AU) | 2 |
| 1 (date) | MM/DD/YYYY (AU) | 0 |
| 3 (address) | "Suburb / State / Postcode" (AU) | 2 |
| 3 (address) | "ZIP code" in non-US locale | 0 |
| 4 (consent) | "Privacy Act 1988" citation (AU) | 2 |
| 4 (consent) | Generic GDPR copy in AU | 1 |

Future calibration anchors per market are a carry-forward for native-speaker review (DE/JP/FR/EU).

### 4. Required JSON shape changes

| Change | v1 → v2 |
|---|---|
| `rubric_version` top-level | `'rubric_v1'` → `'rubric_v2'` |
| `judge_model` | unchanged (`'gpt5mini'`, `'claude'`, `'gemini'`) → `'gpt5mini'`, `'claude'`, `'grok'` (Gemini path retired) |
| **`judge_model_version` (new, required)** | _(not present)_ → `'claude-4.7-sonnet-20260315'`, `'grok-4-...'`, `'gpt-5-mini-...'` (full model version pinned per Cursor session) |
| `scores` map keys | 6 keys (`field_coverage_recall`, `field_label_f1`, `validation_intent_accuracy`, `row_group_agreement`, `locale_fidelity`, `copy_quality_score`) → 9 keys (`item_1_date_format`, `item_2_phone_format`, `item_3_address_schema`, `item_4_consent_citation`, `item_5_currency_number`, `item_6_name_convention`, `item_7_tone_register`, `item_8_mandatory_strictness`, `item_9_cross_locale_leakage`) |
| `scores` value range per metric | 0–5 → 0/1/2 |
| `rationale` per row | unchanged (free-text rationale per row) |
| **Calibration nudge in prompt** | _(not present)_ → "Identify at least one weakness per row before scoring" (must appear verbatim in all three judge prompts) |

### 5. Judge swap

| Slot | v1 | v2 | Why |
|---|---|---|---|
| Primary 1 | Claude (4.x — model version unspecified) | **Claude 4.7 (model version pinned)** | Memo 3 + Tonyk: 4.x ≠ 4.7. Pin in every Cursor judge chat; record in `judge_model_version` field. |
| Primary 2 | Gemini 2.5 Flash | **Grok 4** | Different model family from Claude/GPT — genuinely independent bias profile. Gemini's structural zero-variance disqualifies it. |
| Self-judging control | GPT-5 mini | **GPT-5 mini (unchanged; version pinned)** | Architectural invariant: control judge MUST be the same model as the form generator, so self-bias deltas are measurable. Version pin matters; size doesn't. |

GPT-5.7 vs GPT-5 mini swap was considered and rejected: keeping GPT-5 mini as control is architecturally necessary because it's the same model as the form generator. If the form generator upgrades to GPT-5.7, the control judge follows; the version pinning is what matters.

**Critical caveat from Memo 3:** within-family upgrades matter. Pin model version in every Cursor judge chat. Add `judge_model_version` field to `judge-output-*.json` and validate at ingest.

### 6. Primary aggregation

- **Primary metric value** = `(claude_score + grok_score) / 2` per cell, summed across the 9 items per row.
- **GPT-5 mini self-bias delta** = `gpt5mini_score - primary_mean` per metric per row.
- **Row-level inter-judge agreement** = computed from `|claude_score - grok_score|` distance across the 9 items.
- Bias delta calculation pattern unchanged from v1; only the inputs change (Grok replaces Gemini).

### 7. AC-10 escape clause (Tonyk Q6)

The story-completion gate (AC-10) requires Grok 4 mean drops below 5.00 AND each judge scores ≥1 cell below 4 across the baseline.

If after a single retry round (one calibration tweak — typically rubric anchor sharpening — followed by a re-run) all three judges still ceiling-lock under v2 + nudge, **the story is closed with `JUDGE-ARCHITECTURE-RE-INVESTIGATION` registered as a P0 carry-forward, and the architecture work itself is not blocked.**

This is the explicit fallback to prevent indefinite story holdback on a judging-method outcome that's structurally separate from the architecture work.

---

## Rationale

- **Single-anchor `locale_fidelity` had no ground truth.** Replacing it with 9 anchored elements + lived-AU calibration directly resolves the v1 false-positive issue.
- **Judge variance is now structurally non-zero.** Grok 4's distinct bias profile (different model family) breaks the family-correlation problem Gemini had with Claude (both Anthropic-adjacent training data signals).
- **Deterministic items make 6 of 9 elements free per generation.** The eval harness can run them on every cell of a 270-cell run without LLM-judging cost; LLM-judging budget is reserved for the 3 items that genuinely need judgment.
- **Calibration nudge is a known fix for ceiling-locking.** "Name one weakness per row before scoring" forces the judge to engage critically before assigning a score.
- **`judge_model_version` is reproducibility infrastructure.** v1's silent model drift (Claude 4.0 → 4.5 → 4.7 in the same calibration window) compromised year-on-year comparability. v2 prevents recurrence.
- **AC-10 escape clause prevents architectural work blocked by methodology.** The architecture is shipping value (registry, format/policy/tone split, brand posture, persistent resolution chain). If the judging method needs another iteration, that should not block the architecture from landing.

---

## Consequences

### Positive

- Locale fidelity is now measurable with ground truth; AU-pedantry false positives can no longer slip through.
- Deterministic items make eval cost-efficient (full 270-cell runs nightly are feasible).
- Pinned model versions make the judge architecture reproducible across model upgrades.
- The escape clause prevents future stories from getting stuck on judge-method calibration debt.

### Negative

- Score range collapse (0–5 → 0/1/2) reduces granularity — borderline cases are forced into a 3-step ladder. Mitigated by 9 elements summed (max 18) giving similar resolution to a single 0–5 metric in the limit.
- Gemini outputs from v1 (Story 6.4.4) become historical-only. Cannot be cross-compared to v2.
- Three new schema requirements on judge JSONs (`rubric_version: rubric_v2`, `judge_model_version`, 9-key `scores` map) — manual judge chats need explicit instruction; ingest must validate.
- 9 elements per row × 270 cells × 3 judges = 7,290 individual scorings per eval run — the manual Cursor flow is heavier; budget Tonyk-time accordingly.

### Neutral

- v1 governance ADR (`STORY-6.4.3b-RUBRIC-ADR.md`) remains authoritative for any v1 historical comparison; the supersession footer (added in PR #74) clarifies the boundary.
- v1 metric keys (`field_coverage_recall`, `field_label_f1`, etc.) are dropped from v2 — these were never locale-specific and were proxy metrics for layout / structural quality which the deterministic Category A harness already covers more directly.

---

## Implementation evidence

To be filled at closeout:

- Rubric file: `backend/tests/form_ai_eval/rubric_v2.md` (with calibration anchor table embedded).
- Judge prompt template: `docs/stories/STORY-6.4.4.1-JUDGE-PROMPTS.md` (Claude 4.7 + Grok 4 + GPT-5 mini, all with calibration nudge).
- Ingest schema bump: `backend/tests/form_ai_eval/judge_ingest.py` (rubric_v2 path; v1 backwards-compat preserved).
- Ingest tests: `backend/tests/test_eval_judge_ingest_v2.py`.
- Required JSON shape examples: in `judge_pack.py` package generator.

---

## Baseline re-snapshot policy (inherited from `STORY-6.4.3b-RUBRIC-ADR.md`, applied)

- v1 judge outputs (including all Story 6.4.4 historical files) **remain valid only for v1 comparisons**.
- Cross-comparison of v1 and v2 scores is **explicitly disallowed** by the v1 ADR's existing "Baseline re-snapshot policy" section.
- The v2 baseline is established by Story 6.4.4.1 AC-10 (re-judge `prompts-v1.1` baseline under rubric_v2). All future variant comparisons are against this v2 baseline.
- Future rubric versions (v3+) require their own ADR and re-snapshotting; the same boundary applies.

---

## Review questions (PM/Architect/SM)

1. Is 0/1/2 the right anchor scale, or should we use 0/1/2/3 to give an explicit "gap" score (between "wrong" and "partial")?
2. Are deterministic items 1–6 + 9 reliable enough that the LLM-judged items can be sampled (e.g. judge only 30% of cells) rather than judged on every cell?
3. Should `judge_model_version` validation be a hard ingest rejection (current decision) or a warning that allows ingest but flags the row?
4. When does a v3 rubric become inevitable, and what should trigger it (a new market launch? a model family change?)?
5. Should we keep a `copy_quality_score` proxy from v1 as item 10 (LLM-judged), or trust `prompts-v1.1` adversarial variants (item 9) to surface copy issues?

---

## Carry-forward

| Item | Suggested home |
|---|---|
| Native-speaker calibration anchors for NZ/UK/US/CA/IE/INTL_ONLINE/EU/DE/JP/FR | Pre-Epic 7 (international launch) |
| (Conditional) Judge architecture re-investigation if AC-10 escape clause invoked | New micro-story, P0 if invoked |
| Baseline distribution analysis for cross-locale leakage (item 9) | After 6.4.4.1 baseline establishes a real distribution |
| Promotion of cross-locale leakage from advisory to blocking | Post-distribution analysis |
| Rubric v3 trigger conditions document | When v2 calibration rounds reveal systematic gaps |

---

*End of ADR. This document is the authoritative source of truth for `rubric_v2` measurement architecture for Story 6.4.4.1 and beyond, until a v3 ADR supersedes it.*
