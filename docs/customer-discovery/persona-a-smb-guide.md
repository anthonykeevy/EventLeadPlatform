# Persona A — SMB User Interview Guide

**Length:** 20 minutes hard cap. Treat this as a budget — if you're at minute 15 with topics left, drop the lowest-priority section, don't run over.
**Mode:** Video call (Zoom/Meet/Teams). Recording with permission strongly preferred.
**Prerequisites:** Read [README.md](README.md) ground rules. Read [pricing-discovery-framework.md](pricing-discovery-framework.md). Skim [industry-pain-research.md](industry-pain-research.md) for unlock prompts.

---

## Who Persona A is

A person at a 5–200-staff company who is responsible (at least partly) for collecting information from customers via forms — for events, campaigns, surveys, registrations, lead gen, kiosk-based reception, or a mix. They might exhibit at trade shows, run webinars or in-person customer engagements, embed forms on their website, or all of the above.

They almost certainly use one of: paper / business cards / clipboard, a generic form tool (Jotform, Google Forms, Typeform, Microsoft Forms), a CRM-bundled form (HubSpot, Mailchimp), an event-specific tool, or asked a developer to build something custom.

**JTBD note** — Jobs-To-Be-Done framework. Don't ask "what features do you want?" — ask "what job were you trying to get done at your last [event/campaign/launch], and what did you hire to do it?" That reveals real motivation; feature questions reveal opinions.

---

## Goals of this conversation

1. Confirm the **pain is frequent and expensive** — not a once-a-year nuisance.
2. Discover **what they actually pay today** (event/campaign budget envelope and per-tool spend).
3. Surface **which built differentiators** (offline capture, AI form gen, branded backgrounds, AU address validation, kiosk auto-reset, embed delivery, approval workflows) are **switching signals** vs. retention features vs. don't-care.
4. Identify **features we haven't built that they ask for unprompted.**
5. Get **commitment signals** (intro to peers, willingness to pilot, willingness to follow up).

---

## What you do NOT do

- Don't pitch the product in the first 15 minutes.
- Don't say the price.
- Don't argue with their pain ("oh but our tool handles that") — capture and move on.
- Don't ask "would you use…" or "would you pay…" — ask about past behaviour instead.
- Don't read the unlock prompts as a list. Use them only when they're vague.

---

## The 20-minute structure

| Minutes | Section | Goal |
|---|---|---|
| 0–2 | Warm-up & framing | Set them at ease, get permission to record |
| 2–8 | The last form they used (past behaviour) | Real workflow, real costs, real pains |
| 8–13 | Current tools & alternatives | What they use, what they paid, what they swap between |
| 13–17 | Pain ranking & wishful thinking | Surface unprompted feature asks |
| 17–19 | Brief context on what we do (NOT a demo) | Plant a seed, gauge reaction, tag features |
| 19–20 | Commitment signals & close | Intros, follow-up, scorecard survey |

---

## Section 1 — Warm-up & framing (2 min)

> "Thanks for the time — I'll keep us to 20 minutes. I'm doing customer research, not selling — I'm trying to understand how companies like yours collect information from customers. Forms for events, surveys, registrations, contact, anything where someone fills something in. Mind if I record so I don't have to scribble?"

> "Quickly — what's your role, and what kinds of customer engagements does your team run that involve collecting information from people?"

*Listen for:* Events vs. surveys vs. lead gen vs. registration vs. mixed. Are forms a small or big part of their work? Do they own the budget or recommend?

---

## Section 2 — The last form they used (6 min) ← most important section

Open broadly. Don't pre-suppose it's an event.

> "Tell me about the most recent time your team needed to collect information from customers — what was it, and what were you trying to achieve?"

If they're vague, prompt with concrete examples: *"event, survey, sign-up form, feedback request, application, contact form on the website — whatever was most recent."*

Then drill in. Don't move on until you have a vivid picture.

- "Walk me through how it actually worked — who built the form, who shared it, who collected the data?"
- "How was the form delivered to people — public link, embed on your site, on a tablet at a venue, QR code, paper, something else?"
- "How many responses did you come back with? How did that compare to what you hoped?"
- "What happened to those responses afterwards — where did they end up, how long until follow-up?"
- "Anything go wrong? What's the moment you'd most want to do differently?"
- **"Or — was there a recent time when you skipped digital capture altogether and used paper / business cards / a clipboard because the digital options were too painful or too slow to set up?"**

*Listen for:* Manual data entry afterwards, lost paper forms, illegible handwriting, leads not followed up because of delay, Wi-Fi failures at venues, branded vs. generic look, who validated the data, kiosk/tablet vs. mobile use, integration with their CRM, address fields entered wrong, consent/opt-in confusion.

> "What did that whole engagement cost you all-in — staff time, tools, anything else? Roughly?"

*Listen for:* The "envelope" their form work sits inside. If a campaign costs $20k and the form is "the cheap bit they wing," that tells you pricing tolerance.

### If they're vague — unlock prompts (use sparingly)

Drawn from [industry-pain-research.md](industry-pain-research.md):

- *"Some teams I've spoken to said venue Wi-Fi at events drops out and their offline fallback either didn't exist or didn't sync. Has that ever bitten you?"*
- *"When you go through last quarter's responses, what proportion turn out to be unusable — illegible, fake email, junk?"*
- *"Some teams describe leads sitting in a spreadsheet for days before reaching the CRM, then sales calling a cold prospect. Does that pattern sound familiar?"*

**Drop the prompt and shut up. Listen for whether they latch on with a real story.** A polite nod is not a signal.

---

## Section 3 — Current tools & alternatives (5 min)

> "When you need to collect data from customers, what's your current go-to? Walk me through what you used last time and why."

- "How did you set it up? Who built it? How long did it take?"
- "What did it cost — per form, per event, or as a subscription?"
- "Have you ever used something else? Why did you switch?"
- "If you couldn't use [X] anymore tomorrow, what would you do?" *(reveals true alternative — often "back to paper" or "ask the developer")*
- "Has anyone on your team or a customer ever asked for something the tool couldn't do?"

*Listen for:* Custom branding asks, offline failures, integration with their CRM (Salesforce, HubSpot, Pipedrive, Mailchimp, Zoho), team handoffs (someone built it, someone else needed to edit it day-of), AU-specific address validation pain, consent tracking, **a developer being asked to build something marketing came up with**.

### Developer-handoff probe (if relevant)

> "Has there ever been a time where marketing asked for a form feature, but it had to go to a developer because the off-the-shelf tool couldn't do it? What was that?"

*Why this matters:* Surfaces hard-feature asks (AU address validation via G-NAF/Geoscape, payment fields, conditional logic, custom CRM mapping, save-progress, file upload). These are switching signals — features that took weeks to build manually become drag-and-drop in our platform.

---

## Section 4 — Pain ranking & wishful thinking (4 min)

> "If I gave you a magic wand for customer-engagement forms — anything at all — what would you fix first?"

*Don't fill the silence. Let them think.*

> "What about second?"

> "Have you or anyone on your team ever built a workaround — a spreadsheet, a script, a manual process — to fix something the tool didn't do?"

*Listen for:* Workarounds = real pain. People only build workarounds for problems they couldn't ignore. **This section is where unbuilt features surface** — write down every wishful-thinking item verbatim, even if it sounds out of scope.

### Optional probes if you have time and they haven't surfaced naturally

- *"Have you ever wished a form could just sit on a tablet at reception and reset itself between people?"* (kiosk auto-reset switching-signal probe)
- *"How important is it that addresses your customers enter are valid — actual, deliverable Australian addresses?"* (AU address validation switching-signal probe)
- *"What about embedding forms directly into your website or a CRM page rather than sending people to a separate URL?"* (delivery-channel probe)

---

## Section 5 — Brief context (2 min, NOT a demo)

Only after the above. Two sentences max.

> "Quick context on what I'm building, then I want your gut reaction. We're building a forms platform with a few specific things — branded forms with custom backgrounds, the form works offline so Wi-Fi doesn't matter, an AI assistant that generates the form from a description, drag-and-drop AU address validation, embed-anywhere delivery, and a kiosk mode for tablets at receptions or events. You pay per published form — not a subscription."

> "What's your gut reaction — what stands out, and what would stop you using it?"

*Listen carefully and tag what they react to:*
- **Genuine excitement** that interrupts you ("wait, can it…") → likely **switching signal**. Note which feature.
- **Polite nod** ("yeah that's nice") → **retention or table stakes**.
- **Specific objection** ("but does it integrate with Salesforce?") → gold — that's the real buying criterion.

Tag every feature reaction in your post-call notes as **switching signal / retention / table stakes**.

---

## Section 6 — Commitment signals & close (1 min)

> "I'm going to send you a 5-minute survey afterwards with a list of features — built and planned — to get your reaction. Useful?"
> "Who else in your world should I talk to about this? Anyone in your team, or at peer companies?"
> "If this existed today and worked, would you want to be among the first to try it at your next form/event/campaign?"

**Commitment ladder (in order of strength):**
1. Says "interesting" → weak. Score 1.
2. Fills out the scorecard survey → moderate. Score 2.
3. Refers a peer by name → strong. Score 3.
4. Asks about pricing or pilot terms unprompted → strong. Score 4.
5. Books a follow-up call or asks for a demo → very strong. Score 5.

---

## After the call (within 2 hours)

1. **Write up notes** using this template:
   - Their role, company size, types of forms they run
   - Last form/engagement story (in their words where possible)
   - Tools used + spend
   - Top 2 wishful-thinking items (verbatim)
   - **Feature reaction tags:** switching signal / retention / table stakes (per feature mentioned)
   - Their reaction to our context (excitement / nod / objection)
   - Commitment score (1–5)
   - Verbatim quote worth remembering
2. **Send the [feature-resonance-scorecard.md](feature-resonance-scorecard.md)** as a Google Form / Typeform link with a thank-you note.
3. **Tag the interview** in [kill-criteria.md](kill-criteria.md) tracker.
4. **Add unprompted feature asks** to a running gap list.

---

## Red flags during the call

- They keep agreeing politely with everything → you're talking too much. Shut up; let silence work.
- They can't remember specifics → too senior or too removed from the work. Ask if there's a hands-on colleague you should also talk to.
- They start asking detailed product questions in minute 5 → they want to buy, not be discovered. Note it, redirect once, and if it persists, accept it's a sales call now — but capture pricing reactions carefully.
- They say "we're happy with what we have" → don't disagree. Ask "what would have to change for you to even look at something else?" — that's the real switching trigger.
- All their pain is around one tool you don't intend to compete with → they're not your buyer; finish politely.
