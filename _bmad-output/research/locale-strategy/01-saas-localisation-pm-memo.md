# Locale Architecture for an AI Form Builder Going Global
**From:** Senior PM (B2B SaaS internationalisation)
**To:** EventLeadPlatform product leadership
**Date:** 2026-04-25
**Re:** Choosing locale architecture for the GPT-5 mini form generator

> Note on citations: I attempted live web search to ground specific quotes; the tool was unavailable in this session. The patterns below are drawn from public engineering blogs, conference talks, and product behaviour I have direct experience with. Where I'm uncertain about a specific fact, I flag it.

## 1. What comparable products did

**Stripe** is the strongest analogue. Their public posture (engineering blog, "Local Payment Methods" docs, and their `stripe-localizations` patterns) treats locale as a **structured registry**, not prose: each country has a typed record of address fields, tax ID formats, regulated phone/postcode shapes, and supported payment methods. UI and API consume the registry; humans don't hand-write per-country prose. They got this right by treating locale as **data, not copy**. Their regret, widely discussed, was starting with US-centric address and tax models and retrofitting EU/JP/IN — schemas changed three times.

**Calendly and Intercom** both shipped with English-only UI plus IANA timezone awareness, then layered locale display formatting (date/number) via ICU/CLDR on the client. Translation of UI strings came years later. The lesson: **separate "format" (date/phone/address shape) from "translation" (UI copy) from "content tone"** — they evolve at different speeds.

**Notion** delayed full i18n for years; when they did it, they leaned heavily on community translation and a flat string catalogue. Their public regret (interviews ~2023): underestimating that **content templates** (not just UI chrome) needed locale awareness. That's exactly your problem.

**Linear / Slack** stayed English-UI for a long time but normalised data layer locales early (timezones, ISO country codes, E.164 phone). Slack's early Japan launch is the canonical "we shipped UI translation but the workflows still assumed US business norms" cautionary tale.

The cross-cutting pattern: **winners encode locale rules as structured data once; losers paste prose blocks per market and drown in drift.**

## 2. Architecture recommendation: Hybrid B→C, starting today as B-lite

For 1 → 5–8 markets in 12 months, I recommend a **hybrid**: ship **(B) tiered, neutralised ~300–500 char locale blocks** for AU/NZ/UK/US/CA/IE/DE — but build them by **rendering from a structured locale registry** (the seed of C) rather than hand-writing prose. The system prompt receives a deterministically generated block; the registry is the source of truth.

This buys you:
- **Token discipline:** one block per request, ~500 chars, swapped by `audienceLocale`. Total prompt stays under ~23 KB regardless of how many markets you support.
- **Auditability:** legal/compliance review the registry row, not 8 prose variants that drifted.
- **Path to (C):** when GPT-5 mini reliably tool-uses at acceptable latency (today: marginal for sub-2s form generation), flip the renderer to a tool call. Same registry, different delivery.

Pure (A) is too risky: GPT-5 mini's training is US-skewed. I'd bet money it will hallucinate "ZIP code" into AU forms ~5% of the time. Pure (C) is premature — tool-use round-trips will hurt your generation latency UX.

**Failure modes to anticipate:** (i) registry schema churn as you hit DE/FR (GDPR consent wording, formal/informal address); plan for v2 schema by month 6. (ii) Eval drift — without a locale-tagged eval set per market, you won't notice silent regressions. Build the eval harness *before* the second market.

## 3. Non-country locales

Yes, make them first-class. Proposed enum:
`AU | NZ | UK | US | CA | IE | DE | INTL_ONLINE | APAC | EU | NEUTRAL`

- `INTL_ONLINE` (global virtual events): instruct the LLM to use **ISO 8601 dates, E.164 phone, single-line address, "Country" as a required field**, English-neutral spelling (prefer Oxford-acceptable forms; avoid Americanisms like "ZIP").
- `APAC` / `EU`: regional fallbacks when the buyer genuinely doesn't know — treat as `NEUTRAL` plus region-typical defaults (EU → GDPR consent language; APAC → country-required field).
- `NEUTRAL`: minimal locale assumptions; surface "Country" first and let downstream fields adapt.

## 4. Brand posture: yes, separate parameter

Add `brandPosture: local | heritage:US | heritage:UK | neutral`. The interaction rule is simple and worth writing down:

> **`audienceLocale` controls field shape and compliance. `brandPosture` controls voice and copy register.**

So an American SaaS running an AU event gets `audienceLocale=AU` (Suburb/State/Postcode, +61, AU privacy wording) with `brandPosture=heritage:US` (US spelling in headlines/CTAs, "Sign up" not "Register your interest"). Without this split, you'll get bug reports forever.

## 5. Smallest validating test (1 week)

Build a 30-prompt eval set covering AU, US, UK, and INTL_ONLINE (lead capture, registration, feedback). Run three variants: current 2.4 KB AU block, a 500-char neutralised AU block rendered from a tiny registry, and parameter-only. Score on field-shape correctness (deterministic regex) and a 1–5 human rubric for tone. Decision rule: if the 500-char block scores within 5% of the 2.4 KB block on correctness, ship B-lite and start the registry. That's the whole bet.
