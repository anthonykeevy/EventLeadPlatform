# Persona B — Enterprise Interview Guide

**Length:** 30 minutes hard cap. Optional 15-minute extension only if they self-identify as wanting to be a design partner.
**Mode:** Video call. Recording with permission.
**Prerequisites:** Read [README.md](README.md) ground rules. Read [pricing-discovery-framework.md](pricing-discovery-framework.md). Skim [industry-pain-research.md](industry-pain-research.md). Be familiar with our enterprise gaps (SSO, webhooks, custom domains, DSAR, data residency, SLA).

---

## Who Persona B is

Someone at a 200+ staff company who runs (or owns budget for) marketing programs that involve substantial customer-engagement form work — field marketing, trade-show, events, surveys, lead-gen campaigns, webinar registrations, customer-feedback programs — often across multiple business units, regions, or product lines.

They have a team, work alongside marketing ops and brand, and any tool they buy goes through procurement and a security review. They sign annual contracts, not credit-card subscriptions.

**JTBD note** — Jobs-To-Be-Done. People don't buy a form-builder; they hire one to (a) make their team faster, (b) make leads land cleanly in the CRM, (c) keep brand and compliance happy, (d) survive a procurement review. Listen for which job is dominant — the answer changes the pitch.

---

## Goals of this conversation

1. Confirm the **job-to-be-done at scale** — forms across an integrated program, not one-off tactics.
2. Discover the **buying process**: who decides, who blocks, what procurement asks for.
3. Surface **which enterprise gaps** (SSO, webhooks, custom domains, DSAR, data residency, SLA, SOC2) are dealbreakers vs. roadmap-acceptable for *their* company.
4. Discover the **integration reality** — which CRM/MAP they use and how data flows today.
5. Understand the **annual budget envelope** for forms / lead-capture tooling — the unit isn't $99/form, it's "what's a tool like this worth across our program?"
6. Find **switching signals** vs. retention features in our differentiators (offline capture, AI form gen, AU address validation, kiosk auto-reset, agency role, embed delivery, audit trail, approval workflows).
7. Find features we haven't considered that procurement, security, or brand will demand.

---

## What you do NOT do

- Don't position as cheap. Enterprise buyers distrust cheap. Position as fit-for-purpose.
- Don't promise gaps will be closed by a specific date unless you've decided to commit.
- Don't show product before minute 20.
- Don't skip the procurement / security questions even if they feel awkward — that's where deals die.
- Don't read unlock prompts as a list. Use only when they're being vague.

---

## The 30-minute structure

| Minutes | Section | Goal |
|---|---|---|
| 0–3 | Warm-up & framing | Permission to record, set context |
| 3–10 | Their program (past behaviour) | Understand scale, structure, complexity, mix of form types |
| 10–16 | Tooling stack & integrations | What's in place, what's painful, what's mandatory |
| 16–22 | Procurement & security reality | Surface true gating requirements |
| 22–26 | Brief context + reaction (with feature tagging) | Plant seed, gauge fit, identify switching signals |
| 26–29 | Pricing discovery (envelope, not per-unit) | Understand budget mechanics |
| 29–30 | Commitment & close | Design partner offer, intros |

---

## Section 1 — Warm-up & framing (3 min)

> "Thanks for the time. I'll keep us to 30 minutes. I'm doing customer research, not selling — trying to understand how enterprise marketing teams actually run customer-engagement form work across their program. Mind if I record?"

> "Briefly — your role, your team's scope, and roughly how many customer-facing forms or engagements your team runs in a year? Could be events, surveys, registrations, lead campaigns — anything where customers fill something in."

*Listen for:* Volume per year, mix of form types, regions/BUs covered, team size, who they report to. This calibrates everything.

---

## Section 2 — Their program (7 min)

Open broadly. Don't pre-suppose it's events. **Lead with the platform-lens probe** — enterprises don't buy "a form builder," they buy *the elimination of a process*. Frame it as the **SDLC for customer-engagement forms** — Persona B will recognise the language immediately from their software org.

> "I think of customer-engagement forms as having their own SDLC — someone identifies a need, design, build, validate, rework, approval, publishing, distribution (email link, embed in site, kiosk), and ongoing support. Walk me through how that actually plays out at [company]. Who's involved at each stage? Where does it stall? How many tools and handoffs are involved?"

That whole chain is what the platform replaces — many people, manual handoffs, often no system of record. Listen for which stages are most painful, who owns each, and how visible it is to senior leadership.

The exact SDLC shape will vary per company — that's expected. The pain pattern (handoffs, stalls, lack of visibility) is what you're listening for, not a specific stage list.

Drill into the messy bits.

- "What kinds of forms does your team build most often — registrations, surveys, lead gen, contact, kiosk-based, embedded on the website?"
- "Who designs and builds them — internal team, marketing ops, agency, or developers?"
- "How does the data get to where it needs to go? Same way every time, or different per region/product?"
- "Once data comes in, what's the average time before it's usable in [CRM / data warehouse]?"
- "Tell me about the worst form/engagement project your team ran in the last 12 months. What happened?"
- **"Has there been a recent case where the team gave up and used paper / a Google Form / a spreadsheet because the proper tooling was too painful?"**

*Listen for:* Agency relationships (this is why our agency role might matter), regional variance, attribution gaps, manual rekey, compliance flags, **developer-handoff stories** (marketing asks for X, dev has to build it because the form tool can't), **AU address validation pain** (Geoscape / G-NAF / Australia Post API).

### If they're vague — unlock prompts

From [industry-pain-research.md](industry-pain-research.md):
- *"Some teams describe leads sitting in spreadsheets for days before reaching the CRM, by which time sales is calling cold prospects. Does that pattern happen at [company]?"*
- *"Some marketing teams have told me about being stuck with one tool admin who becomes a bottleneck for the whole team on event/launch day. Has that happened to you?"*
- *"I've heard developers complain about being asked to build forms manually because the marketing tool couldn't do conditional logic, address validation, or payment fields. Anything like that at [company]?"*

---

## Section 3 — Tooling stack & integrations (6 min)

> "What tools are in your stack today for forms / lead capture, and the systems they feed into?"

- "Which ones do you love, which ones do you tolerate?"
- "How does data flow from form-capture into [CRM]? Real-time integration, batch upload, manual?"
- "What's the procurement story on those tools — annual contracts, MSA in place, who owns the relationship?"
- "Is there anything you've evaluated and rejected? Why?"
- "If a new tool came in, what would have to be true about its integrations on day one?"

*Listen for:* **Day-one integration requirements** — Salesforce, Marketo, HubSpot, Eloqua, Pardot, MS Dynamics. Real-time vs. batch. Webhook vs. native connector vs. Zapier-acceptable. **This is a hard gating dimension.**

---

### Platform-lens probes (drop one or two in if not surfaced naturally)

These probe whether they value *visibility and process replacement* — the real enterprise platform sale, not the operational tool sale.

- *"At a senior level today, do you have a single view of how many forms are active across the team, how many leads they've collected this quarter, and what's pending approval? Or is that pieced together from spreadsheets / individual tool logins / asking around?"*
- *"How important is it that the head of marketing / global team can see what every region or BU is doing on customer-engagement forms, in one place?"*
- *"If a form went live today that someone in another region built, how long would it take you to know it existed?"*
- *"How are you currently handling the design → build → validate → rework → approve → publish → distribute process? How many people, how many tools, how long?"*

Listen for: visibility gaps as a pain point, "we just don't know what marketing is doing across regions," approval/governance friction, multiple tools for one workflow. These are the platform-lens switching signals.

---

## Section 4 — Procurement & security reality (6 min) ← critical for enterprise

This is where enterprise deals die. Don't skip.

> "If you wanted to bring in a new tool tomorrow, walk me through what that actually involves at [company]. Who has to approve? What does the security review look like?"

- "Do you have a vendor questionnaire you typically send? Could I see one to make sure I'm meeting the bar?"
- "Is SSO mandatory? Which provider — Okta, Azure AD, Google Workspace, Ping?"
- "Are there data residency requirements? Must data stay in Australia / EU / US?"
- "Do you require a DPA, sub-processor list, SOC 2 / ISO 27001, pen test report?"
- "Privacy Act / GDPR side — how do you handle data subject deletion or access requests today? Do you require self-serve from your tools?" *(Note: AU Privacy Act tranche-one reforms passed Dec 2024. New consent definition is likely to land in 2025–26 — worth probing whether they're ready.)*
- "What about audit logging — does security require audit log export to your SIEM?"
- "What's procurement's typical contract length and minimum spend?"
- "When a junior or regional team member commissions a customer-engagement form that costs money to publish, how do you control spend today? Hard caps, budget per region, manager approval, no controls?" *(open design question for our cost-governance feature — see scorecard Q4)*

*Listen for:* Which gates are **hard mandatory** vs. **roadmap-acceptable with commitment** vs. **nice-to-have**. The distinction is the entire point of this section.

---

## Section 5 — Brief context & reaction (4 min)

Three sentences max. Then shut up.

> "Quick context. We've built a customer-engagement forms platform with branded drag-and-drop forms, offline capture, AI form generation, drag-and-drop AU address validation, embed-anywhere delivery (public URL or iframe in your site/CRM), kiosk mode with auto-reset, multi-tenant team collaboration including agency partners with scoped access, configurable approval workflows, and a full audit trail. We're missing some enterprise pieces today — SSO, webhooks to CRM, custom domains, self-serve DSAR — and figuring out which of those are real blockers for companies like yours."

> "Setting price and contract aside — what stands out as relevant, what's missing, and which of those gaps would be a hard no for [company]?"

*Listen for and tag every feature reaction:*
- **Switching signal** — they interrupt you, ask "wait, can it…", describe a specific scenario where this would make them switch. Note which feature.
- **Retention** — "yeah that's nice" / polite engagement.
- **Table stakes** — "of course, everyone has that."

Common unprompted enterprise asks worth listening for:
- Lead deduplication / enrichment (ZoomInfo, Clearbit, 6sense)
- Real-time CRM push with field mapping
- Multi-language / multi-region forms
- Consent management & lawful-basis tracking per submission *(particularly relevant given AU Privacy Act reforms)*
- Field-level encryption / PII masking
- VPAT / accessibility certificate
- White-label custom domain
- IP allowlisting on admin
- Bring-your-own storage / S3
- A/B testing of forms
- E-signature for waivers / consent
- Scheduled exports to data warehouse
- Embed delivery with preserved branding
- Agency partner access without full seat cost

---

## Section 6 — Pricing envelope (3 min)

The unit is annual program spend, not per-form. See [pricing-discovery-framework.md](pricing-discovery-framework.md).

> "Without committing to anything — what's the rough envelope your team has for forms / lead-capture tooling per year? And how do you typically think about that — per event, per seat, per region, flat platform fee?"

> "What does 'expensive' look like for a tool in this category? What does 'too cheap to be credible' look like?"

> "Of the tools you have today, which is the one you wish you paid less for, and which is the one you'd happily pay more for if it was better?"

*Listen for:* Annual envelope, preferred pricing model, signals of budget elasticity ("we'd pay more for X").

---

## Section 7 — Commitment & close (1 min)

> "I'm running a small design-partner program — companies who get early access in exchange for shaping the roadmap. Would that be interesting for [company]?"

> "Who else inside [company] should I talk to — security, procurement, marketing ops, or your CRM admin?"

> "I'll send you a short survey with our feature list — both built and planned — to get a written reaction. Useful?"

**Commitment ladder for Persona B:**
1. Generic interest → weak.
2. Fills out the scorecard → moderate.
3. Refers a colleague (esp. marketing ops / security / procurement) → strong.
4. Shares their vendor questionnaire → very strong.
5. Asks about design-partner terms or pilot → very strong.
6. Books a follow-up that includes someone else from their team → strongest.

---

## After the call (within 2 hours)

1. **Notes** — same template as Persona A plus:
   - Org size, volume of form work per year, regions/BUs covered
   - CRM/MAP stack
   - Procurement gates ranked: hard mandatory / roadmap-acceptable / nice-to-have
   - Annual budget envelope (if surfaced)
   - **Feature reaction tags:** switching signal / retention / table stakes (per feature mentioned)
   - Unprompted enterprise feature asks (verbatim)
   - Design-partner interest (yes / maybe / no)
2. **Send [feature-resonance-scorecard.md](feature-resonance-scorecard.md)** with an enterprise-flavoured intro (the survey has a Persona B section).
3. **Update gap-priority list** based on what they ranked as hard mandatory.
4. **Update [kill-criteria.md](kill-criteria.md)** tracker.

---

## Red flags during the call

- They speak only in generalities, never specifics → either too senior or politely deflecting. Ask "could you give me an example from a specific project in the last quarter?"
- They keep saying "we'd need to check with [X]" → you're talking to a champion, not a decision-maker. That's fine, but get an intro to X.
- Procurement section gets brushed off ("oh we can probably make it work") → they don't actually know. Ask "have you brought a new SaaS tool in the last 6 months — what did that process look like?"
- They show high product interest with low procurement clarity → champion without budget. Useful for design-partner, not for revenue.
