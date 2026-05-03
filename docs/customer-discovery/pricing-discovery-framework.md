# Pricing Discovery Framework

**Why this is its own document:** Pricing is the question most likely to produce false signals. Direct questions ("would you pay $X?") get polite-but-meaningless answers. This document gives you indirect tactics that surface real willingness-to-pay through behaviour, anchors, and budget envelopes.

**Read before every interview.**

---

## Core principles

1. **Don't anchor first.** Once you say "$99", every answer they give is relative to that. Let them anchor you. Their first number is more honest than any number they react to.
2. **Past behaviour beats hypothetical.** "What did you pay last time" tells you more than "what would you pay."
3. **The unit they think in matters more than the price.** SMBs think per-event. Enterprises think per-year envelope. Pricing the wrong unit loses both.
4. **Pricing is a downstream output of value framing, not the input.** If pain is mild and tooling cheap, no price works. If pain is severe and the alternative is a $2k contractor, $99 sells itself.

---

## Persona A — SMB pricing discovery

### The three lenses (use in order)

**Lens 1 — Event budget envelope (asked early, in Section 2 of the guide)**

> "What did your last event cost you all-in — stand fees, travel, staff, swag, tools — roughly?"

This frames lead capture as a sliver of a much larger spend. If their event costs $15k all-in, a $99 form fee is rounding error. If it costs $1k, $99 is 10% — different conversation.

**Lens 2 — Current tooling spend (asked in Section 3)**

> "What does [current tool] cost you — per event, monthly, or annually? Roughly?"

This gives you the **alternative anchor** — what they already accept paying. If they're paying Jotform $39/month and rarely run events, your $99/event is steeper than it looks. If they're paying a contractor $500–$2k per event for a custom form, you're a bargain.

**Lens 3 — Reaction to your model (asked in Section 5, AFTER context)**

Don't start with the price. Start with the model.

> "We charge per published form per event — no subscription. Does that pricing model fit how you think about event spend?"

Listen for: "we'd prefer a subscription" (signals high event volume), "that's perfect, we don't run enough events to justify a subscription" (your sweet spot), "we'd want to know it's predictable" (signals procurement concerns even at SMB level).

*Only if* the model resonates: ask the price reaction.

> "If a published form was around $99 — including hosting, custom backgrounds, lead export — what's your gut?"

Listen for the *type* of objection, not yes/no:
- "That's reasonable" — weak. Probably polite.
- "That's cheaper than I expected" — concerning. May undervalue you, may signal you're below trust threshold.
- "That feels expensive for what it is" — investigate why. Their reference point matters.
- "That's fine but I'd want to know what 'published' covers" — strong. They're already mentally buying.
- "I'd want a multi-event discount" — strong. Signals frequency + commitment.

### What you're really learning

You're not learning whether $99 is right. You're learning:
- **The annual ceiling** — events/year × event-spend × tool-budget-fraction
- **The packaging objection** — per-form vs. per-event vs. per-seat vs. subscription
- **The trust threshold** — too cheap = "must be junk," too expensive = "rather use Jotform"

---

## Persona B — Enterprise pricing discovery

### Forget per-form. The unit is annual program spend.

Enterprises don't think "$99 per form." They think:
- "$X per year for the platform that supports our event program"
- "$Y included in the contract, $Z if we exceed volume"
- "$W per region or per BU"

Asking them about $99/form gets you a polite shrug. Ask about envelopes.

### The three lenses for enterprise

**Lens 1 — Annual envelope (asked in Section 6)**

> "Without committing to anything — what's the rough envelope your team has for lead-capture tooling per year?"

Many will say "I can't share that." Fine — try this:

> "Range, then. Are we talking under $25k, $25–$100k, $100k+? Just to calibrate what 'expensive' and 'cheap' mean to you."

**Lens 2 — Existing tool spend benchmarks**

> "What do you pay for your top three marketing tools today, ballpark?"

This gives you their reference points. If they pay $80k/year for Marketo, $40k for 6sense, $20k for Drift — they're not going to flinch at $30–60k for an event lead platform that does the job. If their entire stack is $40k they're a different buyer.

**Lens 3 — Pricing-model preference**

> "How do you typically prefer to be charged for tools like this — flat platform fee, per seat, per event, per region, usage-based?"

Listen for:
- **Flat platform fee** — predictability matters most. They want a number procurement can sign off and forget.
- **Per event** — they want costs to track usage. Common in agencies and event-heavy orgs.
- **Per seat** — common in marketing ops, less common for event tools.
- **Usage tiers (volume bands)** — they want to be rewarded for commitment. Common for enterprise SaaS.
- **"Whatever's simplest"** — they're not really thinking. Press: "what would your CFO want to see?"

### Three indirect questions worth more than any direct price ask

These three, asked late in the call, surface more pricing intelligence than any direct question:

1. > "Of the tools in your stack today, which one do you wish you paid less for, and which one would you happily pay more for if it was better?"

   *Why this works:* Reveals which categories are commoditised vs. valued. If they say "we'd pay more for a lead capture tool that actually integrated cleanly," you've found the value lever.

2. > "If a tool exactly like this came in at half the price of [closest competitor they've named], what would the conversation with procurement look like?"

   *Why this works:* Forces them to walk through the procurement process out loud — exposing approval thresholds, MSA requirements, and budget gates.

3. > "What would 'too cheap to be credible' look like for a tool in this category?"

   *Why this works:* Surfaces the floor. If they say "anything under $20k/year I'd assume isn't enterprise-grade," your floor is set. (This is a real dynamic — pricing too low actively kills enterprise deals.)

### The enterprise pricing trap

A repeated pattern from founders selling SMB tools into enterprises:

> SMB pricing: $99/form → multiplied by 50 forms/year for an enterprise = $4,950/year.
> Enterprise reaction: "That's not a real product. Why is your price so low?"
> Result: deal lost not because of price, but because of *credibility*.

Enterprises will often pay 5–10x more for the same software, packaged as an annual contract with SLAs and a CSM, than they'd pay metered. **Don't assume your SMB unit price scales linearly.** Discovery should reveal whether you need a *separate* enterprise pricing tier (likely yes).

---

## Persona C — Agency / service provider pricing discovery

### The unit is per-client economics + agency margin

Agencies don't think "$99 per form" or "annual platform fee" — they think:
- "How much does each client cost me to support on this tool, and what margin can I add?"
- "Can I rebill the client invisibly, or do they see the tool's price?"
- "What's my break-even client count for buying a higher tier?"

There are two distinct pricing models agencies want, and which one they prefer maps closely to their sub-model:

- **Project agencies** lean toward **pass-through** — each client pays directly, agency takes a referral commission or marks up implementation time.
- **Managed-service agencies** lean toward **agency-master billing** — single invoice to the agency, agency rebills clients at their own margin (often opaque to client).
- **MarTech consultancies** rarely buy themselves; they recommend, client buys.

### The three lenses for agencies

**Lens 1 — Current tooling cost across the client base**

> "Roughly how much do you spend on form / lead-capture tooling across your whole client base in a year? And how is that structured — one big licence, per-client subscriptions, client-paid?"

Reveals whether they currently buy at scale or per-client. If they're paying 12 separate Jotform subscriptions, they're a managed-service candidate frustrated with current state. If they only pay when a client engagement requires it, they're project-leaning.

**Lens 2 — Margin expectations**

> "When you include tooling in a client engagement, what kind of margin do you typically need on it?"

Industry rough range:
- Project agencies: bundle tool cost into project fee, 20–40% margin on direct costs
- Managed-service agencies: 30–50% on rebilled tooling
- White-label resellers: sometimes 100%+ (client never knows the underlying tool cost)

If they say "we don't mark up tooling, we just pass through," they're a low-margin agency — you'll need to ensure your reseller pricing leaves enough room.

**Lens 3 — Packaging preference**

> "If you were buying this for use across clients, what packaging would work best — flat agency licence, per-client workspace, per-seat across your team, or pass-through where each client pays?"

Listen for which model they pick *and* what they reject. The rejection is often more revealing.

### Three indirect questions worth more than direct asks

1. > "If we offered a white-label tier where you could fully rebrand and rebill clients at your own price, what would 'fair value' for that tier look like to you?"

   *Why this works:* Surfaces willingness-to-pay for the agency-platform value, not the per-form value.

2. > "How many concurrent clients would you need to be running on the platform before a higher tier started paying for itself?"

   *Why this works:* Reveals their volume ceiling and gives you a tier-pricing target.

3. > "Of the SaaS tools you currently use across your client base, which one's pricing model do you wish other vendors would copy?"

   *Why this works:* Hands you the packaging template they already endorse.

### The agency pricing trap

A common founder mistake: pricing agencies the same as SMBs ("they're just a small business buying our tool"). They aren't — they're a *channel*. Treating an agency as a single-customer SMB ignores that:

- They onboard *N* paying clients onto your platform per year
- They drive marketing for you (every client engagement is a demo)
- They absorb support burden you'd otherwise have

Healthy agency pricing reflects this — a small premium over SMB per-form is fine if it's offset by white-label, multi-client management, and reseller margin. Pricing agencies *too high* loses you the channel; pricing them like SMBs loses you the leverage.

---

## What to capture in your notes

For every interview:

| Field | Persona A | Persona B | Persona C |
|---|---|---|---|
| Event/campaign spend, all-in | yes | n/a | n/a |
| Annual volume (events / forms / clients) | yes | yes | yes |
| Current tooling spend | yes | yes | yes (across clients) |
| Closest tool comparison they named | yes | yes | yes |
| Stated envelope (if any) | optional | yes | yes (margin) |
| Pricing-model preference | yes | yes | yes |
| Reaction to $99/form (if reached) | yes | n/a | optional |
| "Pay less for" / "pay more for" answers | optional | yes | yes |
| Procurement-process detail | n/a | yes | n/a |
| Agency sub-model | n/a | n/a | yes |
| White-label appetite | n/a | n/a | yes |
| Concurrent client count | n/a | n/a | yes |
| Pass-through vs. master-billing preference | n/a | n/a | yes |

After 8–10 interviews per persona, you'll have enough to draft a defensible pricing model — not before.

---

## Red flags during pricing conversations

- **"We don't really have a budget for that"** — usually means they have one, but you're not their priority. Investigate alternative spend.
- **"Whatever it costs, if it works"** — almost always polite-but-meaningless. Try: "give me a range that would feel painful but doable."
- **They give a price they'd pay before you ask** — strong signal. Capture verbatim.
- **They flinch at the model, not the number** — model objection > price objection. Solve packaging first.
- **They start negotiating in the discovery call** — they're either buying (great, but careful — discovery isn't done) or testing how desperate you are. If desperate-test, hold the line: "I'm not pricing yet, just learning."

---

## What pricing answers also reveal — security, approval, and dashboard intent

Pricing isn't just about price. The questions you ask about *who decides spend, who pays, who needs to know, who approves* are the same questions that drive RBAC, approval flows, and dashboard design. While running pricing discovery, listen for these adjacent signals — they should land in the same notes and feed [tenancy-sharing-and-dashboards.md](tenancy-sharing-and-dashboards.md).

### Listen-with-both-ears mapping

| What they say in the pricing conversation | What it tells you about security / approval / dashboards |
|---|---|
| "I sign off, but my CFO needs to see total spend monthly" | Need: senior-level dashboard with at-a-glance spend rollup |
| "Each region has its own budget" | Need: per-company / per-group budget enforcement; group dashboard rollup |
| "Anyone on the team can build a form, only I publish" | Need: approval workflow with publish-only-admin; matches what's shipped |
| "We had a junior team member spend $5k unintentionally last quarter" | Need: hard cost cap / budget gate / per-user cost ceiling |
| "Procurement caps tool spend at $X/year" | Need: visible spend tracking + early-warning notifications + alternative governance to avoid blocking work |
| "I wouldn't want my agency to see my other suppliers' work" | Need: agency-scoped tenancy isolation (which we have) + visibility controls |
| "We rebill clients individually" | Need: per-client cost attribution + statement / invoice export |
| "Our compliance team needs to see who approved what" | Need: audit trail + approval-history surfacing in dashboard |
| "I don't want to know about every form, just the high-value ones" | Need: dashboard filtering / threshold-based notifications |

### Light probes to drop into the pricing conversation

These don't need their own section — they fold naturally into the pricing flow:

1. *"Other than you, who else needs to see what your team is spending — your manager, finance, procurement?"*
2. *"How would you want to be alerted if spend got close to a budget — email, dashboard, blocker before publish?"*
3. *"If a junior team member could publish a form that costs money, what controls do you want in place?"*
4. *"Today, when something gets published — does anyone get notified, or does it just happen quietly?"*
5. *"What would you want a senior-level dashboard to show at a glance? Forms active, leads this period, spend, pending approvals, something else?"*

These five questions take ~3 minutes total and produce design-grade input for the dashboard, approval-flow, and notification work.

---

## What this framework gives you

After 10+ Persona A interviews, 6+ Persona B interviews, and 6+ Persona C interviews, you'll have:

1. A defensible **per-form SMB price** (likely a range like $79–$129) with packaging logic.
2. A defensible **annual enterprise envelope** — almost certainly multiple tiers, almost certainly not "$99/form × N forms."
3. A defensible **agency / reseller tier** with white-label pricing and margin structure that protects the channel without losing the leverage.
4. **Multi-event / multi-client discount logic** — surface from the "we'd want a volume deal" signals.
5. **A "no" segment** — companies for whom no realistic price works. Mark them as not-our-buyer and stop pursuing.
