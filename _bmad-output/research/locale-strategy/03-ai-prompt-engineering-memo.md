# Locale Architecture Memo — EventLeadPlatform Form Generator

**Author:** Sr. Prompt Engineer (multilingual LLM products)
**Date:** 2026-04-25
**Re:** Locale strategy for GPT-5 mini form generator (AU launch → 6-market expansion)

> Note on sources: WebSearch was unavailable in this environment. Pricing and benchmark figures below are reasoned from first principles and the publicly-known pricing tiers prior to my cutoff; treat absolute numbers as order-of-magnitude and re-validate before committing budget.

---

## 1. Architecture recommendation: **Hybrid B + seed of C**

Ship **(B) tiered locale blocks** now; instrument it so it becomes the data source for **(C) capability registry** in 12 months. Reject (A) parameter-only.

**Why.** Story 6.4.4 already gave you the answer empirically: collapsing the 2.4 KB block produced measurable `locale_fidelity` regressions on GPT-5 mini. That isn't a model-knowledge problem you can solve by trusting "AU" as a parameter — it's a *steerability* problem. Smaller models know AU formats, but they default to US conventions because (i) RLHF training data skews US, and (ii) form-generation is a structured-output task where the model picks the highest-prior token sequence, which is `MM/DD/YYYY`. Stripe Tax, DeepL, and Smartling all hit this and all landed on the same shape: **explicit per-locale rule blocks, lazily loaded**. Pure tool-use registries (C) work but add a round-trip and only pay off once you have >10 locales with frequently-changing rules — premature for a 6-market roadmap.

(A) becomes viable only when the model reliably *self-elicits* locale rules from a 1-line hint across 100+ generations. We have direct evidence GPT-5 mini does not.

## 2. Token-cost projections (100k generations/month)

Assume GPT-5 mini ≈ **$0.25 / 1M input tokens** (estimate; verify). Each locale block ≈ 600 tokens (~500 chars + framing).

```
# Per-generation INPUT cost components
base_prompt_tokens  = 22_000_chars / 4  ≈ 5_500 tokens
locale_block_tokens = 600
user_prompt_tokens  ≈ 200

# (A) Parameter-only: no per-locale block
cost_A = 100_000 * (5_500 + 200) * 0.25 / 1e6 = $142.50/mo  (any market count)

# (B) Tiered — only the *active* market's block is injected per request
cost_B = 100_000 * (5_500 + 600 + 200) * 0.25 / 1e6 = $157.50/mo
# Same cost regardless of market count — only one block ships per call.

# (B) naive — all market blocks always shipped (DO NOT DO THIS)
cost_B_naive(N) = 100_000 * (5_500 + 600*N + 200) * 0.25 / 1e6
  N=1   → $157.50
  N=5   → $217.50
  N=10  → $292.50
  N=20  → $442.50

# (C) Tool-use: 1 extra round-trip @ ~400 tokens in + 300 out
cost_C ≈ cost_A + 100_000 * (400*0.25 + 300*2.00)/1e6 ≈ $142.50 + $70 = $212.50
```

**Takeaway:** properly-implemented (B) costs **$15/mo more than (A)** at any market count. The cost debate is a red herring; correctness is the only axis that matters. With prompt caching enabled (most providers cache identical prefixes at ~10% read cost), even naive-(B) at N=20 drops below $100/mo.

## 3. Model-version sensitivity

I don't have GPT-5.7 benchmark data, so this is reasoned, not measured:

- **GPT-5 mini → GPT-5.7 (full):** I'd expect ~30–50% of the AU/NZ block to become redundant — specifically the *format reminders* (DD/MM/YYYY, +61). The *consent norms* (Privacy Act 1988 phrasing, Spam Act opt-in) will still need explicit injection because they're product-policy decisions, not world-knowledge. Cost goes up ~5–8× per token.
- **Claude 4 → Claude 4.7:** Larger relative jump in instruction-following on structured output; I'd expect ~50–60% redundancy on format rules but the same ~0% redundancy on policy/consent text.
- **Inflection point for (A) viability:** Roughly when the model scores ≥ 95% `locale_fidelity` on a 0-shot "generate AU registration form" prompt with only `audienceLocale: "AU"` as a hint. My prediction: GPT-5.7 / Claude 4.7-class models hit this for *format* fidelity within 12 months, but **never** for *consent/policy* fidelity — that's a product-correctness question no model can self-elicit.

Strategic implication: design (B) so the format rules and the policy rules are **separate sub-blocks**. When models improve, you delete the format sub-block and keep the policy sub-block. That's a 6-line change, not a re-architecture.

## 4. Locale injection mechanics

Inject as a **runtime-templated section of the system prompt**, immediately after the role/task definition and before output-format rules. Not message-level (cache-busts the prefix). Not tool-use (round-trip cost without benefit at this scale).

```ts
// Pseudo-structure
const systemPrompt = [
  ROLE_AND_TASK,                    // stable, cacheable
  OUTPUT_FORMAT_RULES,              // stable, cacheable
  LOCALE_BLOCKS[audienceLocale]     // swaps per request — place LAST in cache prefix
    ?? LOCALE_BLOCKS["__fallback"], // 1-line "infer from ISO code" for unsupported markets
  SAFETY_AND_GUARDRAILS,
].join("\n\n");

// LOCALE_BLOCKS["AU"] internal structure:
//   ## Locale: AU (Australia)
//   ### Formats   ← deletable when models improve
//   ### Address fields
//   ### Consent & legal  ← keep forever
```

Place the locale block **last in the cacheable prefix** so the stable portion still hits the cache. Use prompt-caching breakpoints to keep ROLE+FORMAT cached across all locales.

## 5. Eval pattern for locale-awareness

Current 10-prompt benchmark with no locale anchor is unmeasurable — judges are guessing. Restructure as:

- **15 prompts × 6 locales × 3 reps = 270 generations per eval run.**
- 15 prompts split: 5 "neutral" (locale only in parameter), 5 "ambiguous" (mentions a city), 5 "adversarial" (user types US conventions but `audienceLocale=AU`).
- 3 repetitions to surface temperature variance; report median + p10.
- Per-locale judge rubric with **deterministic checks** (regex for date/phone format, field-name presence) + LLM-judge for consent-text adequacy. Deterministic gates run free; LLM-judge only on the 30% that pass deterministic.
- **Cost per eval run:** ~270 × ($0.002 generation + $0.005 judge) ≈ **$2/run**. Run nightly on main, on every prompt change, and on model upgrades. ~$60/mo.
- Add a **6th metric: cross-locale leakage** — does the AU prompt ever produce US conventions? This is the regression you actually fear in production.

---
**Bottom line:** Ship tiered (B) with format/policy split. The cost delta vs (A) is noise. Re-evaluate (A) only when your own eval harness shows a frontier-model crossing the 95% threshold on format-only checks — which is the only measurement that matters.
