# Locale & Brand Strategy Recommendation (Consolidated)

**Document type:** PM consolidation of 4 parallel research memos
**Author:** John (PM agent), consolidating
**Date:** 2026-04-26
**Status:** Awaiting Tonyk decisions before SM hand-off
**Purpose:** Inform calibration micro-story (Story 6.4.4.1) and locale architecture for Epic 6 + beyond

---

## Source memos (all in `_bmad-output/research/locale-strategy/`)

| # | Persona | Memo | Citations confirmed? |
|---|---|---|---|
| 1 | International SaaS Localisation PM | `01-saas-localisation-pm-memo.md` | No (WebSearch unavailable; flagged) |
| 2 | Cross-cultural UX researcher | `02-cross-cultural-ux-research-memo.md` | No (WebSearch unavailable; canonical sources flagged) |
| 3 | AI Prompt Engineer | `03-ai-prompt-engineering-memo.md` | No (pricing reasoned from first principles; flagged) |
| 4 | Brand strategist (transcreation) | `04-brand-strategy-transcreation-memo.md` | No (canonical case histories; flagged) |

**Caveat to bear in mind:** none of the four agents had live WebSearch. All flagged this honestly. The frameworks they invoke (Hofstede, GLOBE, Stripe registry pattern, IKEA/McDonald's case histories, transcreation theory) are well-established and stand on their own; specific numbers and figures should be re-validated before external citation. The strategic recommendations don't depend on the unverified figures.

---

## 1. Where the four memos converge

| Question | Memo 1 (SaaS PM) | Memo 2 (UX) | Memo 3 (Prompt Eng) | Memo 4 (Brand) | Convergence |
|---|---|---|---|---|---|
| Architecture choice | Hybrid B→C, "B-lite" | (out of scope) | Hybrid B + seed of C | (out of scope) | **Strong** |
| Brand posture is separate from audience locale | Yes | Yes | (implicit) | Yes | **Unanimous** |
| Pure parameter-only (A) is wrong now | Yes | (implicit) | Yes — empirically disproven by 6.4.4 | (implicit) | **Strong** |
| Locale rules belong in structured data, not prose | Yes (Stripe pattern) | Yes (8-element rubric is data) | Yes (registry seed) | (implicit) | **Strong** |
| Cost is not the architecture lever | Implicit | (out of scope) | Yes — only $15/mo delta | (out of scope) | **Strong on Memo 3 evidence** |
| Inflection point exists where (A) becomes viable | Implicit | (out of scope) | Yes — for *format* rules; *never* for *policy* rules | (out of scope) | **Memo 3 is the new architectural insight** |

The recommendation across all four is the same shape: **start with tiered locale blocks rendered from a structured data source, separate brand posture from audience locale, design for graceful evolution as models improve.**

---

## 2. Recommended architecture (consolidated)

### 2.1 Locale architecture: "B-lite" with format/policy split

A single recommendation combining Memo 1's "B-lite from a registry" with Memo 3's "format vs. policy sub-blocks":

```
LocaleRegistry (structured data, source of truth)
    └─ row per locale: AU, NZ, UK, US, CA, IE, DE, INTL_ONLINE, APAC, EU, NEUTRAL
        ├─ format rules (DD/MM/YYYY, +61, postcode shape, currency...)
        ├─ address schema (Suburb/State/Postcode vs City/State/ZIP vs ...)
        ├─ name conventions (single vs given/family; honorifics)
        ├─ consent/legal rules (Privacy Act 1988, GDPR, CCPA, ...)
        └─ tone defaults (Hofstede-derived: PDI, UAI, IDV cues)

Renderer
    └─ produces a ~500-char system-prompt block per request
        ├─ ## Locale: <code>
        ├─ ### Formats           ← deletable when models reach format viability
        ├─ ### Address fields
        ├─ ### Consent & legal   ← keep forever (product-policy, not world-knowledge)
        └─ ### Tone defaults     ← Hofstede-anchored

System prompt assembly (Memo 3 pattern)
    ROLE_AND_TASK              ← stable, cacheable
    OUTPUT_FORMAT_RULES        ← stable, cacheable
    LOCALE_BLOCKS[audienceLocale] ?? LOCALE_BLOCKS["NEUTRAL"]
                               ← swaps per request, placed LAST in cacheable prefix
    SAFETY_AND_GUARDRAILS
    + user prompt at message level
```

**Why this shape:**

- **Token discipline:** one ~500-char block per request regardless of how many markets we support (Memo 3: $157.50/mo at 100k generations vs $142.50/mo for parameter-only; the architecture cost is noise).
- **Auditability:** legal/compliance review the registry row, not 8 prose variants that drift.
- **Future-proof:** when GPT-5.7+ reliably handles formats from a 1-line hint (Memo 3 predicts ~12 months for format rules; never for policy), delete the format sub-block — six lines change, not a re-architecture.
- **Cache friendly:** stable prefix + per-request locale block = cache hits on the bulk of the prompt, only the locale tail busts.
- **Graceful degradation:** unsupported markets fall back to `NEUTRAL`, which is a real first-class locale, not silence.

### 2.2 Locale enum (first-class non-country values included)

Memo 1 proposed: `AU | NZ | UK | US | CA | IE | DE | INTL_ONLINE | APAC | EU | NEUTRAL`. Memo 3 didn't object. I recommend this verbatim for `prompts-v1.1` benchmark categories.

For MVP launch, **the registry needs only 7 fully-populated rows**: AU, NZ, UK, US, CA, IE, INTL_ONLINE. EU and DE can ship as stubs (refer to NEUTRAL + GDPR consent appendix). APAC can ship as a NEUTRAL alias with phone-formatting addendum.

### 2.3 Brand posture: separate parameter (Memo 4 is decisive)

```
brandPosture: 'local' | 'heritage' | 'neutral' | 'transcreate'
heritageOrigin?: 'US' | 'UK' | 'AU' | 'NZ' | 'JP' | 'DE' | 'FR' | 'SE' | 'other'
```

Memo 4's argument for collapsing `heritage:US` into `heritage` + `heritageOrigin` is sound — it avoids combinatorial enum explosion and is extensible.

**Interaction rule (canonical):**
> *`audienceLocale` controls field shape and compliance. `brandPosture` controls voice and copy register.*

**Defaults:**
- `local` when company country == audience locale (the modal AU SMB case).
- `neutral` when unknown / multi-market.
- **Never silently assume `heritage`** — it's the riskiest wrong guess.

**Warning cases** (LLM produces confidently wrong output):
- Cross-script heritage transplants: `heritageOrigin: JP` × `audienceLocale: DE`
- Register clashes: `heritageOrigin: US` (casual) × `audienceLocale: JP` (formal)
- Loss-of-heritage warning: `local` set when company country differs from audience locale

These deserve human-review tags in the AI Agent panel, not silent generation.

### 2.4 Visual identity is a separate axis (Memo 4)

`brandIdentity` (logo, colours, typography) is post-MVP. Voice and visual diverge constantly in real brand strategy (Coca-Cola: globally uniform visual, transcreated copy). Conflating them forces false choices. **MVP scope: voice via `brandPosture` only; logo upload as static asset.**

---

## 3. Recommended `locale_fidelity` rubric v2 (Memo 2 + Memo 3)

The current v1 metric "*locale_fidelity 0-5*" with a single anchor sentence has no ground truth (the 6.4.4 finding). Memo 2 proposes 8 measurable elements; Memo 3 proposes a deterministic-vs-judged split. **Combined recommendation:**

| # | Element | Scoring approach | 0 / 1 / 2 anchors |
|---|---|---|---|
| 1 | Date format matches `audienceLocale` | **Deterministic** (regex) | 0=wrong, 1=mixed, 2=correct |
| 2 | Phone format & country code matches | **Deterministic** (regex) | 0=mandates wrong/foreign code, 1=ambiguous, 2=correct + appropriate |
| 3 | Address schema matches | **Deterministic** (field-name presence) | 0=wrong (e.g. ZIP in AU), 1=partial, 2=correct |
| 4 | Consent/privacy citation correct | **LLM-judged** | 0=wrong Act, 1=generic, 2=correct |
| 5 | Currency / number format matches | **Deterministic** | 0=wrong, 1=ambiguous, 2=correct |
| 6 | Name-field convention matches | **Deterministic** | 0=wrong (mandatory honorifics in low-PDI), 1=partial, 2=correct |
| 7 | Tone register matches Hofstede PDI/UAI | **LLM-judged** | 0=clash, 1=neutral, 2=appropriate |
| 8 | Mandatory-field strictness matches UAI | **LLM-judged** | 0=clash, 1=neutral, 2=appropriate |
| 9 | **Cross-locale leakage** (Memo 3) | **Deterministic** | 0=US conventions present in non-US locale form, 2=clean |

Items 1-6 + 9 are deterministic (free to compute, run on every generation). Items 4, 7, 8 are LLM-judged on whichever subset survives deterministic gates.

**Calibration anchors** (from Tonyk's lived AU experience, captured during this session):
- "First name / Last name" labels = full marks AU (item 6)
- "Given name / Surname" labels = also full marks AU (item 6)
- Mandatory `+61` prefix in placeholder on a domestic AU form = score 0 (item 2)
- Phone helpText "Include country code if overseas" = full marks AU (item 2)
- DD/MM/YYYY = full marks AU (item 1); MM/DD/YYYY = score 0
- "Suburb/State/Postcode" address pattern = full marks AU (item 3); "ZIP code" = score 0
- "Privacy Act 1988" citation = full marks AU consent (item 4); generic GDPR copy = score 1

These directly resolve the 6.4.4 false-positive issue (Claude marking down "First name/Last name" was AU-pedantry without ground-truth anchor).

---

## 4. Eval pattern for measuring locale-awareness (Memo 3)

Current `prompts-v1.0` benchmark: 10 prompts × 1 rep × no explicit locale = unmeasurable. **Replace with `prompts-v1.1`:**

| Slice | Count | Description |
|---|---|---|
| Prompt categories | 15 (was 10) | Add 5: international online event, EU GDPR-required event, US PII-heavy onboarding, UK NHS waiver, NZ-specific RSVP |
| Locale conditioning per prompt | 6 explicit | AU, NZ, UK, US, INTL_ONLINE, EU |
| Within-prompt variants | 3 | "neutral" (locale only in parameter), "ambiguous" (mentions a city), "adversarial" (prompt uses US conventions but locale=AU) |
| Repetitions | 3 | To surface temperature variance; report median + p10 |

**Total per eval run: 15 × 6 × 3 = 270 generations.**

Memo 3's projected cost: ~$2/run for the LLM judging, plus generation cost. Run on every prompt change, on model upgrades, and nightly on master.

---

## 5. Judge architecture (responding to Tonyk's "replace Gemini or GPT-5 mini" decision)

The 6.4.4 evidence: Gemini 2.5 Flash and GPT-5 mini both gave 60/60 perfect 5/5 across 5 runs. They flatlined. Claude was the only judge that moved.

**Recommendation:**

| Judge slot | Current | Proposed | Rationale |
|---|---|---|---|
| Primary judge 1 | Claude (4.x) | **Claude 4.7** explicitly | Memo 3 + Tonyk: 4.x ≠ 4.7. Pin the model version in the Cursor chat. |
| Primary judge 2 | Gemini 2.5 Flash | **Grok 4** | Different model family from Claude/GPT — genuinely independent bias profile. Memo 3 supports model-family diversity. |
| Self-judging control | GPT-5 mini | **GPT-5 mini** (unchanged) | Architectural invariant: the control judge MUST be the same model as the form generator, so self-bias deltas are measurable. |

**Critical caveat from Memo 3 + Tonyk's point:** within-family upgrades matter. Pin model version in every Cursor judge chat (e.g., "Claude 4.7", not "Claude") so the judge architecture is reproducible. Add `judge_model_version` field to `judge-output-*.json` and validate at ingest.

GPT-5.7 vs GPT-5 mini swap was considered and rejected: keeping GPT-5 mini as control is architecturally necessary because it's the same model as the form generator. If the form generator upgrades to GPT-5.7, the control judge follows; the version pinning is what matters, not the size.

**Calibration prerequisite (from earlier in this conversation):** even with Grok replacing Gemini, the rubric needs the v2 redesign above and the "name at least one weakness per row" instruction. Otherwise Grok will ceiling-lock too. Model swap alone doesn't fix calibration.

---

## 6. Decisions Tonyk needs to make

| # | Decision | Recommended | Why |
|---|---|---|---|
| **D1** | Locale architecture: B-lite with format/policy split? | **Yes** | Convergent recommendation across 3 of 4 memos; cost delta vs (A) is $15/mo at scale; future-proof via format-block deletion |
| **D2** | Locale enum (11 values incl. INTL_ONLINE / APAC / EU / NEUTRAL)? | **Yes** | Memo 1; required to ship `prompts-v1.1` |
| **D3** | Registry rows fully populated for MVP: AU, NZ, UK, US, CA, IE, INTL_ONLINE? | **Yes** | Smallest viable; EU/DE/APAC ship as stubs |
| **D4** | `brandPosture` enum (`local`/`heritage`/`neutral`/`transcreate`) + `heritageOrigin`? | **Yes** | Memo 4's collapsed enum; default `local` when company country == audience locale, else `neutral` |
| **D5** | `brandIdentity` (logo/colour/font) — post-MVP? | **Yes** | Memo 4; voice ≠ visual |
| **D6** | `locale_fidelity` rubric v2 — 9-element, deterministic + LLM-judged? | **Yes** | Memo 2 + Memo 3; replaces single-anchor v1 that has no ground truth |
| **D7** | Eval benchmark `prompts-v1.1` — 15 prompts × 6 locales × 3 reps = 270/run? | **Yes** | Memo 3; ~$2/run is in budget |
| **D8** | Judge swap: keep Claude (pin to 4.7) + replace Gemini with Grok 4 + keep GPT-5 mini control? | **Yes** | Convergent on independence + version pinning |
| **D9** | Add `judge_model_version` field to judge outputs and ingest validation? | **Yes** | Reproducibility |
| **D10** | Story 6.4.4 disposition: revert prompt changes (keep harness/tests); fold into 6.4.4.1 calibration? | **Yes** | Closeout report option 3; safest path before re-evaluation under v1.1 rubric |

If you sign off on D1-D10 (or counter), I write the SM brief.

---

## 7. What goes to Bob (SM) after Tonyk decisions

A single SM brief covering the 6.4.4.1 calibration + locale-architecture micro-story pack:

1. **Closeout amendment for Story 6.4.4** — disposition = revert prompt changes; mark as measured-only learning; document `STORY-6.4.4-CLOSEOUT-AMENDMENT.md` referencing this consolidation.

2. **Story 6.4.4.1 — Locale Architecture Foundation + Rubric v2 + Judge Swap** — single story covering:
   - `LocaleRegistry` data structure + 7 fully-populated rows (AU/NZ/UK/US/CA/IE/INTL_ONLINE) + 4 stub rows (EU/DE/APAC/NEUTRAL)
   - System-prompt renderer (format/policy split)
   - `prompts-v1.1` benchmark (15 × 6 × 3)
   - `rubric_v2.md` with 9 elements + Tonyk's calibration anchors
   - Judge swap: Grok in for Gemini; pin Claude 4.7; add `judge_model_version`
   - Re-judge new baseline under v2 rubric; gate to proceed: judge averages must drop below 5.00 AND each judge must score ≥1 cell below 4 across the baseline
   - Adds `audienceLocale` and `brandPosture` parameters to the AI Agent panel API surface (frontend may be deferred to follow-up story)

3. **Story 6.4.4.2 — Re-run H1/H2/H4/Combined under v2** — *only if* H1/H2/H4 still appear desirable after the architecture change. May become unnecessary because locale shrinkage is what the new architecture delivers structurally.

4. **Story 6.5b-style impact note** — `brandPosture` is new prompt input; style-intent resolver design must accept it.

5. **Carry-forward** — Hofstede dimensions for non-Anglophone markets (DE/JP/FR/...) are research-grounded; the registry rows for those need a reviewer with native cultural fluency before populating. Flag in the registry seed.

---

## 8. Open risks to call out

| Risk | Mitigation |
|---|---|
| Registry rows for non-AU markets need native-speaker review before populating | Stub markers; explicit reviewer list per market; do not ship a market until reviewed |
| Memo citations were not WebSearch-verified in this round | Re-validate any external claims (CSA Research figures, Stripe Tax patterns, etc.) before quoting in a public-facing doc |
| Within-model variance not measured | First-shot calibration run under v2 rubric on the existing baseline tells us whether the issue is methodology or model diversity |
| Cross-locale leakage metric is new and untested | Treat as advisory in v2; promote to blocking only after baseline establishes a real distribution |
| Brand-posture warnings (cross-script heritage) need UX surface | AI Agent panel needs a "Confirm intent" prompt for warning cases |

---

## 9. Bottom line

The locale_fidelity issue you raised in Story 6.4.4 wasn't a calibration tweak — it was the symptom of an architectural assumption the harness inherited. **The fix is to redesign locale as data, not prose; redesign brand-posture as a separate parameter; and redesign the rubric around 9 measurable elements with your AU lived-experience as calibration anchor.** The four research memos converge on this and add three pieces of value the conversation did not previously have:

1. **Stripe's "registry, not prose" pattern** — the canonical playbook for this problem
2. **Format vs policy sub-blocks** — the future-proofing insight that lets us delete sections gracefully as models improve
3. **The 9-element rubric** — the missing ground truth for `locale_fidelity`

This is also enough work that 6.4.4.1 should be its own story, not a fold-in. Estimated size: **5-7 dev days** (registry + renderer + rubric v2 + benchmark v1.1 + judge-output schema bump + 1-2 days re-judging in Cursor).

If you sign off on D1-D10, I'll draft Bob's brief next.

— John

---

*End of consolidation. Source memos in this folder.*
