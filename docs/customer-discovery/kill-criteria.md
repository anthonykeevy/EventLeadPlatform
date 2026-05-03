# Kill Criteria & Decision Thresholds

**Purpose:** Pre-decide what signals would make us pivot, persevere, or kill — *before* we hear them. Without this, every founder rationalises mixed signals as positive. With it, we have a sober external check.

**Owner:** Anthony Keevy
**Review cadence:** Weekly during active discovery. Update only with deliberate intent — moving the goalposts after seeing data is exactly what this doc is designed to prevent.

---

## How to use this document

1. **Now (before any interviews):** Read the criteria below. Disagree, edit, lock it in. Note the date you locked it.
2. **After each interview:** Update the tracker at the bottom with the relevant signals.
3. **Weekly:** Compare cumulative signals against thresholds. Make a decision.
4. **Critically:** When you hit a kill or pivot threshold, *don't immediately argue with the data.* Sit with it for 24 hours. Then decide.

**Locked date:** 2026-05-01

---

## Switching-signal taxonomy (use to tag every feature reaction)

Tag every feature reaction in your interview notes and the survey responses as one of:

- **Switching signal** — would cause the interviewee to leave their current tool. *Score 5 on the survey, or interrupt-with-excitement on the call.* Rare and gold.
- **Retention feature** — matters once you're in, doesn't drive the switch. *Score 3–4 on survey, "yeah that's nice."*
- **Table stakes** — everyone has it; absence kills you, presence doesn't help. *Score 2–3, "of course."*

**Decision rule:** A feature scoring as a switching signal in ≥40% of interviewees in a given persona is a **lead-with feature** in marketing for that persona. A feature scoring as table stakes in ≥60% but switching-signal in <10% is a feature you must have but should not lead with.

---

## Persona A — SMB Field Marketer

### Persevere signals (continue investing)

After **10+ Persona A interviews**, all of these are true:

- [ ] At least **6 of 10** describe a specific, vivid pain at their last event (lost leads, manual rekey, Wi-Fi failure, branded form that wasn't, etc.) — i.e. pain is real and frequent.
- [ ] At least **5 of 10** are paying *something* today for lead capture (subscription, contractor, badge scan service) — confirms willingness-to-pay exists.
- [ ] At least **4 of 10** show unprompted excitement about one of: offline capture, AI form gen, or branded backgrounds.
- [ ] At least **3 of 10** give a strong commitment signal (refer a peer, ask about pilot, book a follow-up).
- [ ] Average pricing reaction to $99/form is "fair" or "cheap" (not "expensive").

### Pivot signals (something's wrong, change direction)

If any of these are true:

- [ ] **6+ of 10** say "we just use Jotform/Google Forms and it's fine" — differentiation isn't enough; rethink positioning or segment.
- [ ] **5+ of 10** flag the same unprompted feature gap (e.g. CRM integration) above all our existing features — feature priority is wrong.
- [ ] **5+ of 10** prefer subscription pricing over per-form — packaging is wrong.
- [ ] No one in 10 interviews describes a vivid pain — we've built a vitamin, not a painkiller.

### Kill signals (this segment isn't viable)

If after **15 Persona A interviews:**

- [ ] Fewer than **3** show any commitment signal beyond "interesting."
- [ ] Fewer than **3** can recall lead-capture as a specific problem they care about.
- [ ] No one offers an intro to a peer.
- [ ] Pricing reaction is consistently "no, this is what Jotform is for."

→ SMB segment is not the wedge. Reallocate effort to Persona B or reconsider the product entirely.

---

## Persona B — Enterprise

### Persevere signals (continue enterprise track)

After **6+ Persona B interviews**, all of these are true:

- [ ] At least **4 of 6** describe a specific event-program pain (regional inconsistency, attribution gap, manual rekey to CRM, agency coordination).
- [ ] At least **3 of 6** name a specific tool category they'd swap or augment — i.e. they're actively shopping mentally.
- [ ] At least **2 of 6** voluntarily share procurement/security context (vendor questionnaire, MSA terms, security requirements) — strong qualification signal.
- [ ] At least **2 of 6** express interest in being a design partner.
- [ ] The same **3 enterprise gaps** (out of our 7+) get flagged as "hard mandatory" by 50%+ of respondents — gives us a clear build-next list.

### Pivot signals

- [ ] **All 6** flag a single missing feature as a hard blocker (e.g. SSO) — that gap must move to top priority before more enterprise discovery.
- [ ] **5 of 6** say "we'd never buy from a startup at our scale" — credibility / trust gap is the real issue, not features. Need anchor customer or partner.
- [ ] **4 of 6** say their current tool meets their needs and they have no active project — discovery has caught them at the wrong moment in their buying cycle. Not a kill, but pause and re-engage in 6 months.

### Kill signals

After **10 Persona B interviews:**

- [ ] Fewer than **2** show concrete buying intent (design-partner offer, follow-up with colleagues, vendor questionnaire shared).
- [ ] Annual envelope responses are universally below what we'd need to charge to make enterprise tier viable.
- [ ] The procurement gates required (SOC2 Type II, IL4, FedRAMP etc.) are too far from what's achievable in 12 months.

→ Enterprise track is not viable in current form. Either drop to mid-market or change the product.

---

## Persona C — Agency / Service Provider

This persona has its own most-important signal: **the platform-vs-tool answer.** That overrides feature scores.

### Persevere signals (continue agency track)

After **6+ Persona C interviews**, all of these are true:

- [ ] At least **2 of 6** answer "platform I'd run my service on" to the explicit Section 5 question. Even one is a strong signal; two confirms the model.
- [ ] At least **3 of 6** describe vivid multi-client pain (data leak risks, "Powered by X" embarrassment, login bottleneck, slow onboarding/offboarding).
- [ ] At least **2 of 6** show unprompted excitement about white-label, agency-master billing, or scoped agency role.
- [ ] At least **2 of 6** ask about reseller terms, white-label tier, or design-partner program unprompted.
- [ ] The agency sub-model distribution shows at least one (b) managed-service interviewee — not 100% (a) project + (c) consultancy.

### Pivot signals

- [ ] **5 of 6** answer "tool I'd use when a client asks" — we're a tool not a platform; reposition the agency offering as a feature inside SMB/Enterprise tiers, not a separate motion.
- [ ] **All 6** are sub-model (a) project agencies — managed-service motion may not exist in market or we're targeting wrong agencies.
- [ ] **4 of 6** flag the same hard gap (e.g., "we'd never use this without full custom-domain white-label") — the agency offering needs that gap closed before more discovery.
- [ ] Pricing margin expectations are universally too high for our reseller tier to make sense — pricing model needs rework.

### Kill signals

After **10 Persona C interviews:**

- [ ] **Zero** "platform I'd run on" answers — agencies see us as a tool only, never a platform. Drop the dedicated agency motion.
- [ ] Fewer than **2** show concrete commitment (white-label questions, design-partner interest, peer agency referral).
- [ ] Feature scorecard responses for AG1–AG10 (agency-only section) show no feature scoring ≥4 on average — agency-specific build was wrong-headed.

→ Agency persona doesn't justify dedicated motion. Keep the agency role as a feature serving Persona A/B customers, drop the reseller/white-label investment.

---

## Cross-segment kill signals (whole-product red flags)

These would override anything above:

- [ ] After 20+ total interviews across both segments, no one has volunteered an intro to anyone else. (Conversion currency = referrals. Zero referrals = no real interest.)
- [ ] Multiple credible interviewees independently say "this overlaps with what [established competitor] already does for free / at the same price." Not differentiated.
- [ ] Common feedback: "this is a feature, not a product" — i.e. customers expect this inside their existing platform (Marketo, HubSpot etc.). Distribution will eat us.

---

## Tracker (update after each interview)

### Persona A tracker

| # | Date | Name (initials) | Vivid pain? | Paying for capture today? | Excitement on differentiator? | Commitment signal (1–5) | Price reaction | Notes / verbatim quote |
|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | |
| 2 | | | | | | | | |
| 3 | | | | | | | | |
| 4 | | | | | | | | |
| 5 | | | | | | | | |
| 6 | | | | | | | | |
| 7 | | | | | | | | |
| 8 | | | | | | | | |
| 9 | | | | | | | | |
| 10 | | | | | | | | |
| 11 | | | | | | | | |
| 12 | | | | | | | | |
| 13 | | | | | | | | |
| 14 | | | | | | | | |
| 15 | | | | | | | | |

### Persona B tracker

| # | Date | Name (initials) | Org size / events/yr | Vivid program pain? | Hard-mandatory gaps named | Procurement detail shared? | Design-partner interest? | Notes / verbatim quote |
|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | |
| 2 | | | | | | | | |
| 3 | | | | | | | | |
| 4 | | | | | | | | |
| 5 | | | | | | | | |
| 6 | | | | | | | | |
| 7 | | | | | | | | |
| 8 | | | | | | | | |
| 9 | | | | | | | | |
| 10 | | | | | | | | |

### Persona C tracker

| # | Date | Name (initials) | Agency / sub-model | Concurrent client count | Vivid multi-client pain? | Platform-vs-tool answer | White-label appetite | Commitment signal (1–6) | Notes / verbatim |
|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | | |
| 2 | | | | | | | | | |
| 3 | | | | | | | | | |
| 4 | | | | | | | | | |
| 5 | | | | | | | | | |
| 6 | | | | | | | | | |
| 7 | | | | | | | | | |
| 8 | | | | | | | | | |
| 9 | | | | | | | | | |
| 10 | | | | | | | | | |

### Platform-vs-tool tally (Persona C) — the single most important agency signal

| Answer | Count | Notes |
|---|---|---|
| "Platform I'd run my service on" | | |
| "Tool I'd use when a client asks" | | |
| "Maybe — depends on…" | | List the 'depends on' conditions |

### Gap-frequency tally (Persona B)

Update with a tick mark every time an enterprise gap is named as a hard requirement.

| Gap | Hard requirement count | Roadmap-acceptable count | Not relevant count |
|---|---|---|---|
| SSO / SAML / OIDC | | | |
| Webhooks / native CRM integration | | | |
| Custom domain | | | |
| Self-serve DSAR | | | |
| Data residency | | | |
| SOC 2 Type II | | | |
| DPA + sub-processor list | | | |
| Audit log to SIEM | | | |
| IP allowlisting | | | |
| VPAT / accessibility | | | |
| Lead dedup / enrichment | | | |
| Multi-language forms | | | |
| Field-level encryption | | | |
| Bring-your-own storage | | | |
| A/B testing | | | |
| E-signature | | | |
| Consent / lawful-basis | | | |
| Scheduled DW exports | | | |

---

## Decision log

Record decisions made based on this tracker. Date them.

| Date | Decision | Reasoning | Trigger (which threshold) |
|---|---|---|---|
| | | | |
