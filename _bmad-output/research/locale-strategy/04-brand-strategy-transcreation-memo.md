# Brand Posture in AI Form Generation — A Transcreation Lens

**To:** EventLeadPlatform PM
**From:** Senior Brand Strategist (transcreation practice)
**Date:** 25 April 2026
**Re:** Designing the `brandPosture` parameter

> Note on sources: WebSearch was unavailable in this session. Citations below draw on well-documented public case histories (McDonald's "Macca's" 2013 DDB Sydney rebrand; IKEA's founder-mandated Swedish naming convention; Netflix localization scale-up; Apple's globally-uniform product nomenclature; Coca-Cola "Share a Coke" 2011-onwards; Spotify Wrapped's localized-data-global-template model). Established theory is flagged as such; everything else is my recommendation.

## 1. Translation vs. Localisation vs. Transcreation — and why forms care

**Established theory.** Translation moves *meaning* between languages literally. Localisation adapts *artefacts* to a market — dates, currency, units, legal copy, idiom. Transcreation re-*creates* an idea so it lands with the same emotional payload in a new culture, often discarding the source words entirely (the canonical example: Haribo's "Kids und Erwachsene" jingle becoming "Kids and grown-ups love it so" in English — same feeling, different words).

Forms look like the boring end of this spectrum, but they aren't. A submit button reading "Get Started" vs. "Sign me up, mate" vs. "Join the waitlist" vs. "Request demo" carries enormous voice signal. Helper text, error states, consent wording and microcopy on a registration form are the *only* brand surface many leads will touch before the event. Treating them as pure localisation (just swap dates and phone format) strips heritage. Treating them as full transcreation overshoots — you don't want a German enterprise brand suddenly sounding ocker because the event is in Brisbane.

## 2. Patterns: who localises, who preserves, who transcreates

**Established case patterns:**

- **Preserve heritage (high):** Apple, IKEA, Tesla, Rolex, Louis Vuitton. Premium / design-led / country-of-origin-as-asset brands. IKEA *never* translates "Billy" or "Kallax"; the Swedishness is the product. Apple keeps "iPhone Pro Max" globally — naming consistency is identity.
- **Localise heavily, preserve voice spine:** Netflix, Spotify, Airbnb. Platform brands. Netflix dubs aggressively and commissions local originals, but the wordmark, UI tone ("Top 10 in Australia today") and product vocabulary are globally uniform. Spotify Wrapped is a global template with locally-personalised data — the format is the brand.
- **Transcreate per market:** Coca-Cola, Nike, McDonald's. FMCG / lifestyle brands where emotional resonance beats consistency. "Share a Coke" launched in Australia in 2011 with local first names, then re-transcreated in 80+ markets — same mechanic, different names, sometimes different scripts. McDonald's Australia formally adopted "Macca's" on signage in 2013 (DDB Sydney) after research showed 55% of Australians used the nickname — heritage *plus* deep localisation.
- **Hybrid (most global B2B):** Microsoft, Salesforce, Atlassian. US/AU heritage preserved in voice and naming; dates, currency, compliance localised. This is the modal pattern for SaaS.

**Industry tilts.** Luxury, design, tech-hardware → preserve. Streaming, hospitality, B2B SaaS → hybrid. FMCG, QSR, sport, telco → transcreate.

## 3. `brandPosture` enum — recommendation

```
brandPosture: 'local' | 'heritage' | 'neutral' | 'transcreate'
heritageOrigin?: 'US' | 'UK' | 'AU' | 'NZ' | 'JP' | 'DE' | 'FR' | 'SE' | 'other'
```

Four values, not six. `heritage:US` collapses into `heritage` + `heritageOrigin: 'US'` — cleaner, extensible, and avoids a combinatorial enum.

- `local` — voice matches `audienceLocale` (default for AU SMB customers running AU events).
- `heritage` — voice anchored to `heritageOrigin`; locale-sensitive fields still localise.
- `neutral` — international-English, no idiom, no slang. Default for unknown / multi-market brands.
- `transcreate` — preserve heritage *concept*, regenerate idiom for audience. Premium tier; needs human review.

**Default:** `local` when `companyCountry === audienceLocale`, otherwise `neutral`. Never silently assume heritage — it's the riskiest wrong guess.

## 4. `audienceLocale` × `brandPosture` matrix

| Audience | Posture | Dates / Phone / Consent | Spelling | Tone & Idiom | Flag? |
|---|---|---|---|---|---|
| AU | local | AU | AU English | "G'day", "mate" allowed | — |
| AU | heritage:US | AU | US English | US-flavoured, no Aussie slang | — |
| AU | heritage:UK | AU | UK English | Reserved, British register | — |
| AU | neutral | AU | International EN | Plain, no idiom | — |
| AU | transcreate (US source) | AU | AU English | US energy, AU idiom | Human review |
| DE | heritage:JP | DE | n/a (German) | Formal Japanese register in German | **Warn — likely uncanny** |
| JP | heritage:US | JP | Japanese | Casual US energy in Japanese | **Warn — register clash** |
| Any | local + non-matching companyCountry | — | — | — | **Warn — heritage may be lost** |

The warnings matter. Cross-script heritage transplants (JP→DE, US→JP-casual) are where transcreation agencies earn their fees; an LLM will produce confidently wrong output.

## 5. Visual identity — separate parameter, post-MVP

**Opinion.** Logo, colour, typography are a *different axis* — `brandIdentity`, not `brandPosture`. Voice and visual diverge constantly (Coca-Cola: globally uniform red/script visual, locally transcreated copy). Conflating them forces false choices.

**MVP:** `brandPosture` + `heritageOrigin` only. Ship voice control; let customers upload a logo as a static asset.
**Post-MVP:** `brandIdentity` object (logoUrl, primaryColor, fontFamily, optional brand-guidelines URL for RAG-grounded tone extraction). That's where the real moat is — but it's a six-month build, not a sprint.

---
*~610 words.*
