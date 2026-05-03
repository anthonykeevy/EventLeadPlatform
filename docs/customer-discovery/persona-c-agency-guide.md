# Persona C — Agency / Service Provider Interview Guide

**Length:** 25 minutes hard cap.
**Mode:** Video call. Recording with permission.
**Prerequisites:** Read [README.md](README.md) ground rules. Read [pricing-discovery-framework.md](pricing-discovery-framework.md). Skim [industry-pain-research.md](industry-pain-research.md).

---

## Why this persona is separate

Agencies are not enterprise buyers and not SMB buyers. They **deliver forms on behalf of *their* clients** — which gives them different jobs-to-be-done, different success criteria, different feature priorities, and different pricing logic.

Critically: agencies running their service on top of our platform is the **strongest possible signal that we're a platform, not a tool**. If discovery surfaces zero agencies actually willing to *operate* on us (vs. recommend us), we're a tool — and that changes our positioning entirely.

**JTBD note** — Jobs-To-Be-Done. Agencies are hired to make a client look good without them lifting a finger. The form tool gets hired by the *agency*, to (a) deliver fast across many clients, (b) protect the agency's margin, (c) keep the client in the dark about the tool stack, (d) avoid client-IT review burdens. Listen for which of those jobs is dominant.

---

## Three sub-models — let them self-classify

Agencies cluster into three models with materially different needs. **Don't pre-classify.** Section 1 has self-classifying questions; the cluster will reveal itself.

| | (a) Project agency | (b) Managed service | (c) MarTech consultancy |
|---|---|---|---|
| Engagement | One-off campaign / event / launch | Ongoing retainer | Implementation only |
| Form ownership after delivery | Hand back to client (or doesn't) | Agency runs continuously | Client owns from day one |
| Revenue model | Project fee | Monthly retainer + per-form | One-time implementation fee |
| Their key question to us | "Can I deliver fast and make my client look good?" | "Can I run this efficiently across N clients?" | "Is this a tool I can confidently recommend to enterprise?" |
| Platform usage | Build + deliver, leave | **Heavy** — multi-client, multi-form, ongoing | Setup, then exit |
| Strongest signal of platform-ness | Moderate | **Strong** | Weak |

If discovery surfaces lots of (a) and (c) but no (b), that's a finding: we're a tool agencies use, not a platform they run their service on.

---

## Goals of this conversation

1. **Self-classify the agency** into project / managed-service / consultancy, or hybrid.
2. Understand **how they currently deliver forms for clients** — tool stack, who owns what, what breaks.
3. Surface **switching signals** in our agency-relevant features (multi-tenant client separation, scoped agency role, white-label, embed, custom branding per client, kiosk for client physical spaces).
4. Discover the **client-handoff mechanics** — what happens at project end, who has access, who pays.
5. Understand **agency pricing logic** — how they buy tools to resell as a service, what margin they need, what packaging works.
6. Test the **platform-vs-tool signal** — would they actually run their service on top of us, or just use us when a client asks?

---

## What you do NOT do

- Don't push the white-label angle if they don't bring it up — let them tell you it matters.
- Don't assume their "client" is the buyer. The agency is your buyer; the client is their buyer.
- Don't pitch competitor displacement directly — agencies often have multi-tool stacks for different clients; "replace tool X" is the wrong framing.
- Don't read the unlock prompts as a list.

---

## The 25-minute structure

| Minutes | Section | Goal |
|---|---|---|
| 0–3 | Warm-up & self-classifying | Understand which agency model; permission to record |
| 3–10 | Last client form project (past behaviour) | Real workflow, what broke, client-handoff reality |
| 10–15 | Tool stack & multi-client mechanics | What's currently used, why, pain at the multi-client layer |
| 15–19 | Pain ranking & wishful thinking | Surface unprompted feature asks |
| 19–22 | Brief context + reaction (with platform-vs-tool probe) | Plant seed, gauge fit |
| 22–24 | Agency pricing logic | How they'd buy and resell |
| 24–25 | Commitment & close | Design partner, intros |

---

## Section 1 — Warm-up & self-classifying questions (3 min)

> "Thanks for the time. I'll keep us to 25 minutes. I'm doing customer research — trying to understand how agencies like yours deliver forms and customer-engagement tooling for clients. Mind if I record?"

> "Briefly — what's your role at [agency], and what kinds of clients do you typically work with?"

Then ask the **five self-classifying questions** in order. Don't telegraph what you're listening for.

1. **"When you deliver a form for a client, who owns it after delivery — you or the client?"**
2. **"How are you typically paid for this kind of work — project fee, monthly retainer, implementation fee, or commission?"**
3. **"How many clients do you currently have live forms running for, right now?"**
4. **"Do you build inside the client's existing tool stack, or do you bring your own tools and integrate?"**
5. **"What happens to the form and the data at the end of a project?"**

*Decode their answers:*
- **Project agency:** "client owns it" + "project fee" + few live clients + "use whatever client has" + "we hand it over and step away"
- **Managed service:** "we own and run it" + "retainer or retainer + per-form" + many concurrent clients + "we bring our own tools" + "keeps running until they cancel"
- **Consultancy:** "client always owns it" + "implementation fee, no ongoing" + low concurrent live count + "we set up in client's stack" + "we exit; client takes over"

Hybrid is common — note where they sit and which model dominates.

---

## Section 2 — Last client form project (7 min)

Open broadly.

> "Tell me about the most recent project where you built or ran a form for a client — what was it, who was the client, what were they trying to achieve?"

Drill in. Don't move on until vivid.

- "Walk me through it — who built it, what tool, what was the timeline?"
- "How was the form delivered to end-users — public link on the client's site, embedded into their pages, on a tablet at an event or reception, paper, QR code?"
- "What did the branding situation look like — did your tool show up anywhere on the form, or was it fully white-labeled to the client?"
- "What happened at handoff? Did the client get access to the form / data, or did you keep running it?"
- "What went wrong, or what was painful that you'd want to fix next time?"
- "Did you have to build any custom features for this client that off-the-shelf tools couldn't do — address validation, payment, custom logic?"
- **"Has there been a recent project where you ended up using paper / a Google Form / something embarrassingly basic because the proper tooling was too painful or too expensive for that engagement?"**

*Listen for:* Multi-client data leak risks, "Powered by [tool]" branding embarrassment, client-IT review delays, login sharing, scope creep on custom features, AU address validation pain, kiosk delivery, embed friction, **the moment they had to choose between paying for a heavy enterprise tool for a small client or using something cheap and limited**.

### If they're vague — unlock prompts

From [industry-pain-research.md](industry-pain-research.md):

- *"Some agencies have told me about awkward moments when 'Powered by [Tool]' showed up on a client form and the client noticed. Has that ever happened to you?"*
- *"I've heard about agencies losing access to a client's form data after the project ended because the licence was in someone's personal email. Anything like that?"*
- *"Some agencies describe a per-client login bottleneck where one person ends up holding access for half their accounts. Familiar?"*

---

## Section 3 — Tool stack & multi-client mechanics (5 min)

> "What tools do you use for forms and lead capture across your client base today?"

- "Same tool for every client, or different per client?"
- "How do you handle keeping each client's data and branding separate?"
- "Who pays for the tool — you or each client? How does that work?"
- "What about user access — your team, the client's team, or both?"
- "What's the pain point when you take on a new client — how long does it take to get them set up?"
- "What's the pain point when you offboard a client — what do you have to do?"

*Listen for:* Multi-tenant pain, login sharing, client branding mix-ups, billing complexity (rebilling clients), onboarding time per client, **"we wish we had a single platform for all clients but X stops us"**.

---

## Section 4 — Pain ranking & wishful thinking (4 min)

> "If I gave you a magic wand for delivering forms on behalf of clients — anything at all — what would you fix first?"

> "What about second?"

> "Have you or your team built workarounds — spreadsheets, scripts, processes — to fix things tools didn't do?"

### Optional probes if not surfaced

- *"How important is white-labeling — your client only ever sees their own brand, never yours or the tool's?"* (white-label switching-signal)
- *"What about a kiosk mode for clients running things like reception desks, retail activations, museum sign-in — does that come up?"* (kiosk switching-signal)
- *"Drag-and-drop AU address validation — how often does a client ask you for accurate Australian addresses, and how do you currently solve that?"* (AU address switching-signal)
- *"For a client paying you to manage their forms, is having a senior-level dashboard you can show them — leads collected per form/event, status of pending approvals, spend to date — important to your service?"* (platform-lens / visibility switching-signal)
- *"In effect, you're running an informal SDLC for the client's customer-engagement forms — design, build, validate, rework, approve, publish, distribute, support — across multiple clients. How do you currently keep track of where every client's forms are in that lifecycle, and is that something you'd want to expose to clients?"* (platform-lens / SDLC probe — strong managed-service signal if it lands)
- *"How do clients control their spend on tools you provide? Hard caps, monthly budget, ad-hoc approval, or trust-the-agency?"* (cost-governance design probe)
- *"When a client engagement ends, what should happen to the form, the data, and any future submissions? Who keeps access?"* (off-boarding / ownership probe — feeds open design question for sharing model)

---

## Section 5 — Brief context + platform-vs-tool probe (3 min)

> "Quick context. We've built a forms platform with custom-branded forms, AI form generation, AU address validation, embed-anywhere delivery (public URL or iframe), kiosk mode with auto-reset, and — most relevant for you — multi-tenant company workspaces with a scoped agency role: you can build and run forms inside a client's workspace without seeing other clients, and onboarding a new client is configured rather than rebuilt."

> "Two questions. First gut reaction — what stands out? Second, and be honest: would you see this as a tool you'd use when a client asked, or a platform you'd actually run your service on top of?"

*This second question is the platform-vs-tool signal.* Listen carefully:

- **"A platform I'd run my service on"** + concrete description of how → strong platform signal. Ask why and what would have to be true.
- **"A tool I'd use when a client asked"** → tool-only signal. Note this; if dominant across multiple agency interviews, we're not a platform play.
- **"Maybe — depends on…"** → probe what they'd need to see. Often surfaces the missing platform feature (white-label depth, billing, client offboarding).

Tag every feature reaction as **switching signal / retention / table stakes**.

---

## Section 6 — Agency pricing logic (3 min)

Agencies don't price like SMBs or enterprises — they buy to resell. See [pricing-discovery-framework.md](pricing-discovery-framework.md).

> "How do agencies like yours typically buy tools that you use across multiple clients — per-seat, per-client workspace, flat agency licence, or pass-through to the client?"

> "What margin do you typically need on tooling that you resell or include in client engagements?"

> "If we offered a white-label tier where you could run multiple clients under your own branding, what would 'fair value' look like?"

> "Of the tools you have today, which is the one you wish you paid less for, and which would you happily pay more for if it had better multi-client support?"

*Listen for:* Per-client seat economics, white-label tier willingness-to-pay, pass-through-to-client billing preferences, margin expectations (typically 30–50% for managed-service agencies).

---

## Section 7 — Commitment & close (1 min)

> "I'm running a small design-partner program — agencies who get early access in exchange for shaping the agency-side roadmap. Would that be interesting for [agency]?"

> "Who else should I talk to — peer agencies, your own clients who'd benefit, anyone in your network?"

> "Survey afterwards — 5 minutes, has built and planned features. Useful?"

**Commitment ladder for Persona C:**
1. Generic interest → weak.
2. Fills out the scorecard → moderate.
3. Refers a peer agency → strong.
4. Volunteers a current or recent client who'd be a good design-partner co-pilot → very strong.
5. Asks about white-label or reseller terms unprompted → very strong.
6. Books a follow-up to bring a colleague (account director, ops lead) → strongest.

---

## After the call (within 2 hours)

1. **Notes** — Persona A/B template plus:
   - **Agency sub-model:** project / managed-service / consultancy / hybrid
   - Concurrent live clients (rough)
   - Tool stack across clients
   - White-label appetite (high / medium / low / not relevant)
   - **Platform-vs-tool signal:** "platform I'd run on" / "tool I'd use" / "maybe with X"
   - Pricing-model preference (per-seat / per-client / flat / pass-through)
   - **Feature reaction tags:** switching signal / retention / table stakes
   - Design-partner interest
2. **Send [feature-resonance-scorecard.md](feature-resonance-scorecard.md)** with an agency-flavoured intro.
3. **Update [kill-criteria.md](kill-criteria.md)** Persona C tracker — especially the platform-vs-tool tally.
4. **Add unprompted asks** to gap list.

---

## Red flags during the call

- They describe their work entirely as "we recommend tools" with no implementation depth → consultancy-only; valuable input but unlikely buyer.
- They describe forms as a small incidental part of their service (not core) → won't drive revenue for us.
- They consistently push the "client should own the tool" line → they're consultancy-leaning; not a platform user.
- They want to white-label everything but won't pay above their current per-seat tool spend → margin expectations may not work; investigate.
- They keep redirecting to "well, I'd need to ask my clients" → they're not a decision-maker for tooling; get an intro to whoever is.
