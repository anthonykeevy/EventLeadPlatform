# Customer Discovery — EventLead Platform

**Owner:** Anthony Keevy
**Started:** 2026-05-01
**Goal:** Validate that what's been built (and what's planned) is what customers will actually pay for, before scaling sales effort. Surface critical features that haven't been considered.

---

## Why this exists

Six months of build has produced an enterprise-shaped platform: multi-tenant, RBAC, audit, AI form generation, offline capture, approval workflows, agency role, kiosk capture, AU address validation, custom backgrounds, embed delivery. Before investing in sales/marketing, we need to confirm:

1. **The pains we built for are real and frequent enough to pay for.**
2. **The features that consumed the most build effort are the ones that resonate** — not just polite-nod features. Especially: which features are *switching signals* that would cause someone to leave their current tool.
3. **The gaps for true enterprise sale** (SSO, integrations, custom domains, DSAR, data residency) are real dealbreakers vs. "roadmap-acceptable" — we don't want to build the wrong thing next.
4. **Pricing reality** — what an SMB will actually swipe a card for, what an enterprise budget envelope looks like, and how an agency reseller would price across their clients.
5. **Whether agencies use the platform to run their service**, not just as a tool they recommend. That's the platform-ness signal.
6. **What we haven't thought of** — features customers ask for unprompted that competitors don't have.

This is **discovery**, not sales. The goal of every conversation is to learn, not to close.

---

## Scope reframe — it's not just events

Initial framing was "event lead capture." Reality: the platform serves **any customer-engagement form** with multiple delivery channels.

**Use cases the platform supports:**
- Event lead capture (the original wedge — and one of many)
- Surveys / NPS / post-engagement feedback
- Registration / RSVP
- Product info / contact / inquiry forms
- Lead-gen forms embedded in marketing sites
- Application / intake forms
- Kiosk-based capture (retail, reception, healthcare, gym, museum, lobby)

**Delivery channels:**
- Public form URL
- Embed snippet / iframe (drop into marketing site or CRM-rendered page)
- Kiosk mode with auto-reset after timeout (built and tested; UI toggle not yet exposed)
- QR code on print / signage / business cards (works with public URL)

The unit of value isn't "event" — it's **the form and how it's delivered**. The interview guides reflect this.

---

## Two key vocab terms

**JTBD = Jobs-To-Be-Done.** A framework that says people don't buy products, they "hire" them to do a job. Useful in interviews because asking "what job were you trying to get done?" reveals real motivation, while "what features do you want?" reveals opinions about features. We use this lens throughout.

**Switching signal vs. retention feature vs. table stakes.** Every feature reaction in an interview gets tagged with one of these:

- **Switching signal** = a feature that would make someone leave their current tool. Rare and gold. Probable switching candidates: AU address validation drag-and-drop, branded forms with custom backgrounds, AI form gen, offline capture, kiosk auto-reset, agency multi-client RBAC.
- **Retention feature** = matters once you're in, doesn't drive the switch. (Audit trail. Versioning.)
- **Table stakes** = everyone's expected to have it; absence kills you, presence doesn't help. (CSV export. Email validation.)

This taxonomy drives both our build priorities and our positioning.

---

## Two lenses for talking about the product

A subtle but important distinction that should colour how interviews are framed and how features are positioned:

- **Platform lens (enterprise value)** — what senior buyers care about. Visibility across the whole program (forms × events × companies × spend × leads × approvals), automation of the *full* process — what amounts to an **informal SDLC for customer-engagement forms**: design → build → validate → rework → approve → publish → distribute (email link, copy embed, etc.) → support. Many people, manual handoffs, no system of record. The platform replaces that whole process, not just one tool inside it. SDLC is vocabulary Persona B already lives with from their software org and recognises immediately. **The process varies per company** — exact stages and roles will differ — but the shape is universally recognisable. This is the enterprise sale.
- **Operational lens (day-to-day value)** — what hands-on users care about. Easier form design, custom branding, AI assistance, AU address validation as a drag-and-drop, kiosk auto-reset, offline capture, drag-and-drop component library. This is the SMB sale and the day-to-day "do I want to use this" check for any user.

**Both lenses matter.** Persona A buys mostly on operational pain. Persona B buys mostly on platform value. Persona C is split — operational pain is what makes them recommend it; platform value is what makes them run their service on it.

Discovery should explicitly probe both. The new [tenancy-sharing-and-dashboards.md](tenancy-sharing-and-dashboards.md) doc anchors the platform-lens story; the [persona guides](persona-a-smb-guide.md) cover both with operational-lens probes leading.

---

## Three personas, three guides

We're validating three distinct buyers with different jobs-to-be-done, decision processes, and pricing logic.

| | **Persona A — SMB User** | **Persona B — Enterprise** | **Persona C — Agency / Service Provider** |
|---|---|---|---|
| Who | Marketing manager, event coord, business owner | Field marketing director, marketing ops, procurement | Marketing/event/experiential agency, MarTech consultancy |
| Org size | 5–200 staff | 200+ staff | Any — but defined by *delivering forms on behalf of clients* |
| Decision speed | Days, credit card | Months, procurement + security review | Days–weeks; agency principal decides |
| Pricing logic | Per-form / per-event, alternative-tool anchor | Annual contract, budget envelope, volume discount | Per-client seats, white-label tier, reseller margin |
| Interview length | **20 minutes** | **30 minutes** (45 only as design-partner upgrade) | **25 minutes** |
| Guide | [persona-a-smb-guide.md](persona-a-smb-guide.md) | [persona-b-enterprise-guide.md](persona-b-enterprise-guide.md) | [persona-c-agency-guide.md](persona-c-agency-guide.md) |

**Why agencies are a separate persona.** They don't just *use* the platform — they *resell* it as part of their service. The buying logic, success criteria, and feature priorities are different enough that lumping them in with B would muddy both. They also test our deepest signal: **is this a tool, or a platform people run their business on?**

Within agencies there are three sub-models (one-off project / managed service / MarTech consultancy). We don't pre-classify — Section 1 of the Persona C guide has self-classifying questions and lets the data tell us.

---

## Documents in this folder

| File | Purpose | When to use |
|---|---|---|
| [README.md](README.md) | This file — orientation, ground rules, program plan | Before starting |
| [persona-a-smb-guide.md](persona-a-smb-guide.md) | 20-minute SMB script | Every Persona A call |
| [persona-b-enterprise-guide.md](persona-b-enterprise-guide.md) | 30-minute enterprise script | Every Persona B call |
| [persona-c-agency-guide.md](persona-c-agency-guide.md) | 25-minute agency script with sub-model classifier | Every Persona C call |
| [feature-resonance-scorecard.md](feature-resonance-scorecard.md) | Async follow-up survey — built + planned features, scored 1–5 | Send within 24h of every interview |
| [pricing-discovery-framework.md](pricing-discovery-framework.md) | How to surface willingness-to-pay without anchoring; also surfaces security/approval/dashboard intent | Reference before every call |
| [tenancy-sharing-and-dashboards.md](tenancy-sharing-and-dashboards.md) | Platform-lens reference — the User → Company → Event → Form model, sharing primitives, hierarchy, dashboard lenses by persona, open design questions | Reference + use to frame the "platform value" conversation |
| [mvp-scope-fix-candidates.md](mvp-scope-fix-candidates.md) | Pre-launch fix candidates surfaced during discovery prep — feeds your project plan | Reference; sync with project plan as items resolve |
| [industry-pain-research.md](industry-pain-research.md) | Documented pain patterns + unlock prompts | Reference; never read aloud |
| [kill-criteria.md](kill-criteria.md) | Pre-decided thresholds for pivot/persevere/kill per persona | Review weekly |
| [targeting-and-outreach.md](targeting-and-outreach.md) | Job titles, channels, LinkedIn templates | Daily, while sourcing |

---

## How to run the discovery program

**Phase 1 — Persona A (Weeks 1–3)**
- Target: 12–15 completed interviews. Cheaper, faster cycle. Builds your interview muscle and exposes which built features actually resonate.
- Source: LinkedIn, AU exhibitor lists, industry Slack/Reddit, warm intros.

**Phase 2 — Persona B (Weeks 3–6, overlapping A)**
- Target: 6–10 completed interviews. Slower to schedule. Use Persona A learnings to sharpen the enterprise guide.
- Source: Sales Navigator, EEAA/MEA membership, warm intros from advisor network.

**Phase 3 — Persona C (Weeks 2–6, runs alongside)**
- Target: 6–8 completed interviews. Often easiest to source if you have agency contacts already.
- Source: Mumbrella/AdNews community, agency LinkedIn groups, warm intros, AU agency directories.

**Weekly cadence**
- Mondays: review last week's notes, update [kill-criteria.md](kill-criteria.md) tracker, decide if any signals warrant pivoting.
- Fridays: tally response rates by channel, refine outreach templates.

**After every call**
1. Write up notes within 2 hours (memory decays fast).
2. Send the [feature-resonance-scorecard.md](feature-resonance-scorecard.md) survey + a personal thank-you.
3. Tag every feature reaction in your notes as **switching signal / retention / table stakes**.
4. Tag the interview against [kill-criteria.md](kill-criteria.md) signals.
5. Capture unprompted feature asks verbatim in a running gap list — these are the most valuable output of discovery.

---

## Ground rules (the Mom Test)

1. **Talk about their life, not your idea.** First 60% of every call is past behaviour and current pain. No pitching.
2. **Ask about specifics in the past, not generics or opinions about the future.** "Tell me about the last form your team built" beats "would you use a tool that..."
3. **Talk less, listen more.** Aim for ~20% you / ~80% them.
4. **Don't react to compliments.** "That sounds great" tells you nothing — follow with "what would actually have to be true for you to buy it?"
5. **Watch for commitment signals.** Real signals = intros, time, money, a follow-up meeting. Words are not signals.
6. **Don't sell when you should be learning.** If they ask "when can I buy it?", note it and redirect to learning before promising.
7. **Use unlock prompts only when they're being vague**, never as a checklist. See [industry-pain-research.md](industry-pain-research.md).

---

## What we're explicitly NOT doing

- Not running a survey-only program. Surveys without behavioural context produce noise.
- Not anchoring with our $99 price. We let them anchor first.
- Not demoing the product in early calls. Demos turn discovery into sales.
- Not over-investing in any one persona until kill-criteria signal we should.
- Not pre-classifying agency interviewees as project / managed-service / consultancy — letting their answers reveal it.
