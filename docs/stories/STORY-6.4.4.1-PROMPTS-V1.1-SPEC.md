# Story 6.4.4.1 — Benchmark `prompts-v1.1` Spec

**Story:** 6.4.4.1 — Locale Architecture: Wire the Registry.
**Status:** Spec accepted (D7 locked).
**Supersedes:** `prompts-v1.0` (10 prompts × 1 rep × no explicit locale = unmeasurable for locale fidelity).
**File on master after this story merges:** `backend/tests/form_ai_eval/prompts.yaml`.

---

## 1. Shape

| Slice | Count | Detail |
|---|---|---|
| Prompt categories | **15** | 10 inherited from `prompts-v1.0` + 5 new (see §3) |
| Locale conditioning per prompt | **6 explicit** | `AU`, `NZ`, `UK`, `US`, `INTL_ONLINE`, `EU` |
| Within-prompt variants | **3** | `neutral`, `ambiguous`, `adversarial` (see §4) |
| Repetitions per cell | **3** | Surface temperature variance; report median + p10 |
| **Total cells per eval run** | **15 × 6 × 3 = 270 generations** | |

Per Memo 3 cost projection: ~$2/run for LLM judging on the LLM-judged subset, plus generation cost (~$3–4 per full 270-cell generation pass at current pricing). Total ~$5–6 per full eval run. **Run on every prompt change, on model upgrades, and nightly on master.**

---

## 2. Schema (`prompts.yaml` row shape)

```yaml
- id: "p15-au-neutral-1"           # <prompt-id>-<locale>-<variant>-<rep>
  prompt_category: "intl-online-event"
  prompt_text: |
    A short stand-alone prompt the form generator will receive.
    Two-three sentences max.
  audience_locale: "AU"            # one of: AU NZ UK US CA IE DE INTL_ONLINE APAC EU NEUTRAL
  variant: "neutral"               # one of: neutral ambiguous adversarial
  repetition_index: 1              # 1..3
  expected_signals:                # for deterministic items 1, 2, 3, 5, 6, 9
    date_format: "DD/MM/YYYY"
    phone_country_code: "+61"
    address_field_pattern: "Suburb/State/Postcode"
    currency: "AUD"
    name_convention: ["First name|Given name", "Last name|Surname"]
    cross_locale_leakage_forbidden:
      - "ZIP"
      - "MM/DD/YYYY"
      - "+1 (555)"
  llm_judge_focus:                 # cues for items 4, 7, 8 (used in judge prompt)
    consent_anchor: "Privacy Act 1988"
    tone_register: "low PDI casual"
    mandatory_strictness: "low UAI relaxed"
```

The 270 rows of the YAML are produced by the cross-product (15 prompts × 6 locales × 3 variants) deduped against the rep dimension; reps are emitted as 3 generation calls per cell at run time, not 3 YAML rows.

---

## 3. Prompt categories (15 total)

### 3.1 Inherited from `prompts-v1.0` (10) — augmented with explicit `audience_locale`

| # | Prompt category | Notes |
|---|---|---|
| p01 | Event registration (basic) | Inherited; remove any embedded locale assumption from prompt text — locale is now a parameter |
| p02 | Conference RSVP with dietary | Inherited; same |
| p03 | Workshop signup with skill level | Inherited |
| p04 | Webinar registration | Inherited |
| p05 | Wedding RSVP | Inherited |
| p06 | Volunteer signup | Inherited |
| p07 | Membership application | Inherited |
| p08 | Trade show booth visit log | Inherited |
| p09 | Newsletter subscription | Inherited |
| p10 | Charity donation pledge | Inherited |

For each: review the v1.0 wording, strip any "Australian audience" / "AU customers" hint, replace with neutral phrasing. The locale is conditioned **via the parameter**, not the prompt text (except in the `adversarial` variant — see §4).

### 3.2 New (5) — added to cover international and policy-heavy use cases

| # | Prompt category | Why |
|---|---|---|
| p11 | International online event registration | Stress-tests INTL_ONLINE locale; ISO 8601 dates + E.164 phone + Country field required |
| p12 | EU GDPR-required event registration | Stress-tests `policy` sub-block: GDPR consent text, lawful-basis checkbox, data-handling notice |
| p13 | US PII-heavy onboarding | Stress-tests US conventions (TIN/SSN guidance — system **must refuse to invent** these); ZIP code, MM/DD/YYYY, "+1" |
| p14 | UK NHS waiver | Stress-tests UK conventions; NHS-specific consent language; UK postcode pattern |
| p15 | NZ-specific RSVP | Stress-tests NZ vs AU divergence; NZ phone (`+64`), NZ regions vs AU states |

---

## 4. Within-prompt variants (3 per prompt × locale)

For each (prompt, locale) pair, 3 variant rows are emitted:

| Variant | Description | Purpose |
|---|---|---|
| `neutral` | Locale conveyed only via `audienceLocale` parameter; prompt text contains no geographic/cultural cue | Baseline — does the locale block alone steer the model correctly? |
| `ambiguous` | Prompt text mentions a city or place name (e.g. "...for our Sydney conference...") that may or may not align with `audienceLocale` | Tests resolution robustness — does the model trust the parameter or the prompt cue? |
| `adversarial` | Prompt uses conventions of a different locale than `audienceLocale` (e.g. `audienceLocale=AU` but prompt mentions "ZIP code" or "+1") | Stress-tests cross-locale leakage (rubric item 9) |

Examples for prompt p01 (Event registration) × locale `AU`:

```yaml
- id: "p01-au-neutral-1"
  prompt_text: "I need a registration form for our annual sales conference. Capture name, email, phone, dietary requirements, t-shirt size."
  audience_locale: "AU"
  variant: "neutral"

- id: "p01-au-ambiguous-1"
  prompt_text: "I need a registration form for our Sydney sales conference. Capture name, email, phone, dietary requirements, t-shirt size."
  audience_locale: "AU"
  variant: "ambiguous"

- id: "p01-au-adversarial-1"
  prompt_text: "I need a registration form for our sales conference. Capture name, email, phone with ZIP code, dietary requirements, t-shirt size."
  audience_locale: "AU"
  variant: "adversarial"
```

The adversarial cell tests whether the registry-rendered locale block successfully overrides the in-prompt counter-cue.

---

## 5. Coverage matrix

| Locale | Prompts that have a strong "native" fit | Prompts that test cross-locale fidelity |
|---|---|---|
| AU | p01–p10 (all inherited), p15 (NZ-specific tests AU-NZ divergence) | p11 (INTL_ONLINE), p13 (US adversarial-style) |
| NZ | p15 (native), p01–p10 (close cousin) | p11, p13 |
| UK | p14 (NHS waiver native), p01–p10 | p11, p13 |
| US | p13 (PII-heavy native), p01–p10 | p11, p12 (EU GDPR adversarial-style for US-default models) |
| INTL_ONLINE | p11 (native), all others adapted | All — INTL_ONLINE is the universal compatibility test |
| EU | p12 (GDPR native), p01–p10 | p13, p14 (UK is post-Brexit; tests EU vs UK divergence) |

`CA` and `IE` are seeded in the registry but **not** in this benchmark — they roll into Story 6.4.4.2 or a successor (avoid combinatorial explosion at MVP).

---

## 6. Cost & runtime projection

| Item | Value |
|---|---|
| Cells per run | 270 (15 × 6 × 3) |
| Reps per cell | 3 (emitted at run time, not in YAML) |
| Total generations per run | 810 |
| Generation cost (avg) | ~$3–4 per run (GPT-5 mini at current pricing) |
| Judge cost (Cursor, 3 judges, ~270 LLM-judged items × 3 LLM-judged rubric elements) | ~$2 per run |
| Wall-clock per run (sequential generations) | ~30–45 min |
| Wall-clock per run (parallel batches of 10) | ~5–8 min |
| Tonyk-time per Cursor judge session | ~30 min × 3 judges = 1.5 hr per full eval |

**Cadence:**

- **On every prompt change** (any commit touching `service.py` system prompt or `prompts.yaml`): full eval.
- **On model upgrade** (form generator or any judge): full eval; bump `judge_model_version` in JSONs.
- **Nightly on `master`**: full eval; results land in `_bmad-output/eval-runs/nightly-<date>/` for trend tracking. (Nightly automation is a future story — not in 6.4.4.1 scope.)

---

## 7. Migration from `prompts-v1.0`

Documented in `docs/FORM-AI-EVAL-HARNESS.md` as part of AC-11. Salient points:

- v1.0 results (10 prompts × 1 rep × no locale) are not directly comparable to v1.1 (15 × 6 × 3 with explicit locale). Treat as separate measurement frames.
- The Story 6.4.3a/c diff/stats tooling continues to work; it diffs by prompt id + repetition + variant identity, which now includes the `audience_locale` and `variant` axes natively.
- Existing v1.0 baselines are preserved in `_bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline/` and `story-6.4.4-live-baseline/` for historical reference; cross-comparison to v1.1 results is disallowed (same boundary as the rubric_v1 → v2 transition).

---

## 8. AC-10 baseline run uses this spec

The AC-10 gate for Story 6.4.4.1 is:

> Re-judge baseline under rubric_v2 — gate to consider story complete: Grok 4 mean drops below 5.00 AND each judge scores ≥1 cell below 4 across the baseline.

That baseline is a fresh run of `prompts-v1.1` against the new registry-rendered prompt assembly. The 270-cell run gives substantial sample size for the judges to differentiate; if they still ceiling-lock, the AC-10 escape clause routes to a P0 carry-forward (per the rubric v2 ADR §7).

---

## 9. Future expansion (carry-forward)

| Item | Future home |
|---|---|
| `CA` and `IE` added to the locale axis (becomes 8 locales × 15 × 3 = 360 cells) | Story 6.4.4.2 or successor |
| `DE`, `JP`, `FR` after native-speaker calibration | Pre-Epic 7 |
| `prompts-v1.2` with brand-posture variants (4 brand postures × 15 prompts × locale subset) | Story 6.5b-style or successor |
| Multi-language prompt support (currently English-only) | Far-future; out of MVP |
| Image-derived prompts (from Story 6.5 Image-to-Form) | Story 6.5 closeout or successor |

---

## 10. Spec acceptance

| Item | Owner | Status |
|---|---|---|
| 15 prompts identified (10 inherited + 5 new) | SM (Bob) | Drafted in this spec |
| 6 locales selected for MVP | PM (John) + Tonyk | Locked (D2/D3) |
| Adversarial variant design | Memo 3 + SM | Drafted in this spec |
| Cost projection vetted | PM (John) | Within budget |
| YAML template approved | Dev (at implementation) | Pending implementation |
| `expected_signals` deterministic regex coverage | Dev (at implementation) | Pending implementation; reference `config.ValidationRule` for phone/postcode patterns |

Spec is ready for Dev implementation as part of Story 6.4.4.1 AC-6 / AC-11.

---

*End of spec. This document defines the structure and content of `backend/tests/form_ai_eval/prompts.yaml` v1.1; the actual YAML is produced by Dev as part of the story implementation.*
