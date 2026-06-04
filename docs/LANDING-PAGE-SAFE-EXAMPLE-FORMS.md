# Landing Page Safe Example Forms

## Purpose

Create a set of safe, Australian-focused example forms on the EventLead test platform. These forms should be published so landing-page visitors can click an example, complete the form and submit it. This proves the product promise with the real form builder, public renderer and submission flow.

Use fictional brands only. Do not copy real company names, logos, events, vehicle models, venue names, government marks, AFL/NRL/team names, universities or recognisable brand colour systems.

## Demo Event To Create

**Event name:** EventLead Public Demo Showcase 2026

**Event description:** A fictional demonstration event used to host public sample forms for EventLead. The event contains realistic but fake Australian campaign, event, inquiry, feedback, kiosk and agency workflows. It is safe for screenshots, public demos and landing-page links.

**Internal note:** All data, brands and submissions are test/demo only. Do not use real customer names, production prospects or private business data.

## Device And Routing Decision

Do not create separate desktop, tablet and mobile versions for every form. Start with one responsive form per use case and test each form across desktop, tablet and mobile viewports.

Create separate device-specific forms only where the actual workflow changes:

- **Kiosk/reception capture:** tablet-first, very short, large touch targets, reset-friendly wording.
- **Mobile-first requests:** shorter fields, fewer open-text questions, prominent phone/email fields.
- **Desktop-heavy briefs:** longer campaign or product inquiry forms where users need space to type.

For landing-page routing, use explicit links first, for example "View mobile demo", "View kiosk demo" or "View campaign brief demo". Do not rely on automatic device detection until the platform has a tested routing feature for mapping visitor device to the correct published form.

## Image Guidance

Best option: create our own fictional brand images and abstract backgrounds. This avoids copyright, trademark and brand-safety issues.

Use AI-generated or internally created images with these constraints:

- No real logos, badges, venue names, car badges, number plates, faces of real people or copyrighted mascots.
- Use Australian context through scenery, colours and generic cues: eucalyptus, coastal light, city skyline silhouettes, exhibition booths, tablets, QR signage, coffee carts, EV charging shapes.
- Store images as demo assets and label them as fictional.

If using online images, use only images with clear commercial-use permissions, record the source URL and licence, and avoid recognisable people or brands.

## Primary workflow — build in the Form Builder (required for demo)

These examples must be created **through the product Form Builder**, not by injecting JSON from a script. That is what we are demoing: AI-assisted generation, manual review, branding, publish, and public submit.

For each form (sections below):

1. Log in as Signal Platforms (platform owner).
2. Create or open event **EventLead Public Demo Showcase 2026**.
3. **New form** → open **Form Builder**.
4. Paste the section’s **AI Form Builder prompt** into the AI panel → generate.
5. **Review in the builder:** add missing components (especially Address Lookup AU, Company Lookup ABR, rating, file upload where listed), fix labels, spacing, colours.
6. **Publish** from the builder workflow.
7. Open the public link; submit one valid + one validation test entry.
8. Record Form ID and public URL in the tracking table below.
9. **Images / backgrounds:** upload in the builder (separate task).

Do not inject full form JSON from scripts — that bypasses the Form Builder demo.

### Database shells — migration `096` (run once per environment)

Migration `backend/migrations/versions/096_story_6_5e_landing_demo_event_and_form_shells.py` creates:

| Object | State |
|--------|--------|
| Event **EventLead Public Demo Showcase 2026** | `PUBLISHED`, CompanyID **1** (Signal Platforms) |
| Eight **Form** headers | `DRAFT`, `NO_APPROVAL`, linked to the event |
| **FormVersion** v1 each | Empty canvas + `aiAgentSettings.lastPrompt` (opens pre-filled in AI Agent panel) |

**You run Alembic** (agent does not):

```powershell
cd backend
alembic upgrade 096
# or: alembic upgrade head
```

Then open each form in the Form Builder, run AI generate from the pre-loaded prompt, add backgrounds, test, publish when ready.

### Published URL tracking (fill after you publish in the builder)

| Landing label | Form name | Form ID | Public URL | Screenshot |
|---------------|-----------|---------|------------|------------|
| Event lead capture demo | Rivergum Expo Lead Capture | | | |
| Demo drive request demo | Harbour EV Demo Drive Request | | | |
| RSVP form demo | Wattle Room Business Breakfast RSVP | | | |
| Feedback survey demo | Coastal Home Expo Feedback | | | |
| Product inquiry demo | Banksia Outdoor Living Product Inquiry | | | |
| Kiosk check-in demo | Eucalypt Workspace Visitor Check-In | | | |
| Agency campaign brief demo | Northstar Creative Campaign Brief | | | |
| Outreach campaign request demo | Ironbark Outreach Campaign Request | | | |

Record Form IDs from the dashboard and public URLs after publish (share with integrator for landing-page links).

## Build And Publish Workflow

For each form:

1. Create it under **EventLead Public Demo Showcase 2026**.
2. Use the AI Form Builder prompt from the relevant section below.
3. Manually review the generated fields and add missing components if the AI builder skips them.
4. Apply brand styling and a safe image/background where appropriate.
5. Publish the form.
6. Open the public form link in a fresh browser session.
7. Submit at least two test entries:
   - one complete valid entry
   - one validation-path entry where a required field is missed first
8. Confirm the submission is stored and can be viewed/exported.
9. Capture a screenshot suitable for the landing page.
10. Record the public form URL and screenshot path in this document or a follow-up implementation note.

## Component Coverage Target

Collectively, the demo set should show:

- Display: header, paragraph, divider.
- Core inputs: first name, text, number, email, URL, textarea.
- Choices: dropdown, radio, checkbox.
- Date/time: date picker.
- Australian data components: **Address Lookup (AU)** and **Company Lookup (ABR)**.
- Engagement: rating/NPS-style question.
- Trust/legal: terms checkbox.
- Upload: file upload on a desktop-heavy form.
- Action: submit button with validation.

Prefer **Address Lookup (AU)** over the older generic Address component unless testing the legacy address field is specifically required.

## Form 1 — Event Lead Capture

**Form name:** Rivergum Expo Lead Capture

**Fictional brand:** Rivergum Events Collective

**Description:** Captures leads at a fictional Australian trade expo booth, including company details, contact information, product interest and follow-up consent.

**Primary device target:** Tablet and desktop.

**Landing-page use:** Shows EventLead for event lead capture and booth follow-up.

**Components to include:** Header, paragraph, first name, text, email, phone, Company Lookup (ABR), dropdown, checkbox, textarea, terms, submit.

**Image/background idea:** Abstract Australian expo hall with eucalyptus green accents, generic booth lighting and no visible real logos.

**AI Form Builder prompt:**

```text
Create a branded Australian event lead capture form for a fictional company called Rivergum Events Collective at the "EventLead Public Demo Showcase 2026".

Goal: capture qualified booth leads and follow-up consent after a trade expo conversation.

Design: clean professional tablet-friendly layout, eucalyptus green and deep navy accents, short sections with dividers, suitable for a staff member to complete while talking to a visitor.

Fields:
- Header: Rivergum Expo Lead Capture
- Paragraph: Thanks for visiting our demo stand. Leave your details and we will send the relevant information after the event.
- First name, required
- Last name, required
- Email address, required
- Mobile number, required, Australian format placeholder
- Company using Company Lookup (ABR), optional manual fallback
- Role/title, optional text input
- Main area of interest, required dropdown: Event lead capture, Registration forms, Customer feedback, Kiosk capture, Agency/client forms
- Lead temperature, required radio: Just researching, Interested in a pilot, Ready to discuss
- Follow-up preferences, checkbox group: Email me information, Call me this week, Send pricing when available, Invite me to future demos
- Notes from the conversation, long text, optional
- Terms checkbox: I agree to be contacted about this demo inquiry
- Submit button text: Send lead details

Use realistic fake Australian examples only. Do not mention or copy real brands.
```

## Form 2 — Test-Drive / Demo Request

**Form name:** Harbour EV Demo Drive Request

**Fictional brand:** Harbour EV Studio

**Description:** A mobile-first request form for booking a demo drive with a fictional Australian electric vehicle studio.

**Primary device target:** Mobile.

**Landing-page use:** Shows mobile lead capture for high-intent booking workflows.

**Components to include:** Header, paragraph, first name, email, phone, Address Lookup (AU), date, dropdown, radio, terms, submit.

**Image/background idea:** Generic modern EV silhouette beside Sydney harbour-inspired water and gum trees, with no badge or real model styling.

**AI Form Builder prompt:**

```text
Create a mobile-first demo drive request form for a fictional Australian brand called Harbour EV Studio.

Goal: let a prospective customer request a demo drive appointment.

Design: mobile-first, short, high-conversion, blue and teal styling, large touch targets, no real vehicle brands or model names.

Fields:
- Header: Book a Harbour EV demo drive
- Paragraph: Tell us where and when you would like to try a fictional Harbour EV. This is a demo form using fake brand content.
- First name, required
- Email address, required
- Mobile number, required with Australian placeholder
- Preferred demo location using Address Lookup (AU), required, allow manual fallback
- Preferred date, required, future dates only if supported
- Preferred time window, required dropdown: Morning, Lunch time, Afternoon, After work, Weekend
- Vehicle interest, required radio: City hatch, Family SUV, Fleet vehicle, Not sure yet
- Would you like charging information?, checkbox
- Terms checkbox: I agree to be contacted about this demo request
- Submit button text: Request demo drive

Keep the form concise for mobile. Use only fictional Australian content.
```

## Form 3 — Registration / RSVP

**Form name:** Wattle Room Business Breakfast RSVP

**Fictional brand:** Wattle Room Events

**Description:** Event registration and RSVP form for a fictional business breakfast in Brisbane.

**Primary device target:** Desktop and mobile.

**Landing-page use:** Shows registrations, RSVP, dietary needs and attendee counts.

**Components to include:** Header, paragraph, first name, email, phone, number, dropdown, checkbox, textarea, terms, submit.

**Image/background idea:** Warm cafe/conference breakfast scene with wattles, coffee cups and neutral signage.

**AI Form Builder prompt:**

```text
Create an Australian RSVP and registration form for a fictional event brand called Wattle Room Events.

Event: Brisbane Business Growth Breakfast, hosted under the EventLead Public Demo Showcase 2026.

Goal: capture attendee registration details, dietary needs and optional guest count.

Design: friendly, warm, professional, suitable for desktop and mobile. Use gold, cream and charcoal colours inspired by wattle flowers, without copying any real venue branding.

Fields:
- Header: Brisbane Business Growth Breakfast RSVP
- Paragraph: Reserve your place for a fictional breakfast session for Australian small business operators.
- First name, required
- Last name, required
- Email address, required
- Mobile number, optional
- Organisation, text input, optional
- Number of attendees, number field, required, min 1 if supported
- Attendance type, required dropdown: Attending in person, Joining waitlist, Unable to attend but send notes
- Dietary requirements, checkbox group: Vegetarian, Vegan, Gluten free, Dairy free, Nut allergy, No special requirements
- Accessibility or seating notes, long text, optional
- Terms checkbox: I confirm these details are accurate for this demo RSVP
- Submit button text: Submit RSVP

Use realistic but fake Australian event wording.
```

## Form 4 — Customer Feedback / NPS

**Form name:** Coastal Home Expo Feedback

**Fictional brand:** Coastal Home Expo

**Description:** Post-event feedback form with rating and NPS-style questions for a fictional home and lifestyle expo.

**Primary device target:** Mobile.

**Landing-page use:** Shows customer feedback, ratings and short survey workflows.

**Components to include:** Header, paragraph, rating, radio, checkbox, textarea, email optional, submit.

**Image/background idea:** Generic coastal lifestyle expo palette with soft sand, teal and white; no real venue names.

**AI Form Builder prompt:**

```text
Create a mobile-friendly customer feedback and NPS-style form for a fictional Australian event called Coastal Home Expo.

Goal: collect quick feedback after a visitor attends a home and lifestyle expo.

Design: short, friendly, mobile-first, coastal colours, easy to complete in under two minutes.

Fields:
- Header: Coastal Home Expo Feedback
- Paragraph: Thanks for visiting our fictional expo. Your feedback helps us improve the next event.
- Overall event rating, required rating component, 5 stars
- How likely are you to recommend the expo?, required radio: 0-3 Unlikely, 4-6 Maybe, 7-8 Likely, 9-10 Very likely
- What interested you most?, checkbox group: Renovation ideas, Outdoor living, Solar and energy, Furniture and styling, Builders and suppliers, Food and entertainment
- What could be improved?, long text, optional
- Would you like updates about the next event?, radio: Yes, No
- Email address, optional, shown for follow-up
- Submit button text: Send feedback

Use fictional Australian content and avoid real venue or exhibitor names.
```

## Form 5 — Product Inquiry

**Form name:** Banksia Outdoor Living Product Inquiry

**Fictional brand:** Banksia Outdoor Living

**Description:** Product inquiry form for a fictional Australian outdoor furniture and shade company, including project details, address and attachment upload.

**Primary device target:** Desktop.

**Landing-page use:** Shows richer inquiry workflows, file upload and address capture.

**Components to include:** Header, paragraph, first name, email, phone, Address Lookup (AU), dropdown, number, URL, file upload, textarea, terms, submit.

**Image/background idea:** AI-generated outdoor patio scene with banksia-inspired colours, no real furniture brands.

**AI Form Builder prompt:**

```text
Create a desktop-friendly product inquiry form for a fictional Australian brand called Banksia Outdoor Living.

Goal: capture a detailed inquiry about outdoor furniture, shade or event activation products.

Design: premium but approachable, earthy Australian colours, enough space for detailed project notes. Include a safe fictional brand feel.

Fields:
- Header: Banksia Outdoor Living Product Inquiry
- Paragraph: Tell us about your outdoor project and we will suggest suitable product options. This is a demo form using fictional brand content.
- First name, required
- Last name, required
- Email address, required
- Mobile number, required
- Project address using Address Lookup (AU), required, allow manual fallback
- Product category, required dropdown: Outdoor seating, Shade structure, Event activation furniture, Planters and styling, Not sure yet
- Approximate budget, number field, optional, label in AUD
- Project timing, required radio: This month, 1-3 months, 3-6 months, Just researching
- Website or inspiration link, URL field, optional
- Upload site photo or sketch, file upload, optional, allow image or PDF if supported
- Project notes, long text, optional
- Terms checkbox: I agree to be contacted about this inquiry
- Submit button text: Send product inquiry

Keep all brand and product names fictional and Australian focused.
```

## Form 6 — Kiosk / Reception Capture

**Form name:** Eucalypt Workspace Visitor Check-In

**Fictional brand:** Eucalypt Workspace

**Description:** Tablet kiosk check-in form for visitors arriving at a fictional co-working space.

**Primary device target:** Tablet kiosk.

**Landing-page use:** Shows tablet-friendly reception and kiosk capture.

**Components to include:** Header, paragraph, first name, phone, email, Company Lookup (ABR), dropdown, checkbox, submit.

**Image/background idea:** Simple abstract reception background with eucalyptus green shapes. Avoid real building photos or identifiable locations.

**AI Form Builder prompt:**

```text
Create a tablet kiosk visitor check-in form for a fictional Australian co-working brand called Eucalypt Workspace.

Goal: allow reception visitors to check in quickly on a tablet.

Design: kiosk-first, large touch targets, very short form, high contrast, eucalyptus green and white. The form should feel quick and reset-friendly.

Fields:
- Header: Eucalypt Workspace Visitor Check-In
- Paragraph: Welcome. Please check in before entering the workspace. This is a fictional demo form.
- First name, required
- Last name, required
- Mobile number, required
- Email address, optional
- Company using Company Lookup (ABR), optional, allow manual fallback
- Who are you visiting?, required dropdown: Community manager, Meeting room booking, Event host, Workspace member, Other
- Visitor type, required radio: Meeting guest, Event attendee, Contractor, Delivery, Other
- Safety acknowledgement checkbox: I agree to follow reception and visitor instructions while onsite
- Submit button text: Check in

Keep wording short and suitable for a public tablet.
```

## Form 7 — Agency / Client Campaign Form

**Form name:** Northstar Creative Campaign Brief

**Fictional brand:** Northstar Creative Co.

**Description:** Desktop-heavy campaign intake form for a fictional Australian agency collecting client campaign requirements.

**Primary device target:** Desktop.

**Landing-page use:** Shows agency/client workflows, approval prep, long text, company details and file upload.

**Components to include:** Header, paragraph, Company Lookup (ABR), first name, email, phone, URL, date, dropdown, checkbox, textarea, file upload, terms, submit.

**Image/background idea:** Abstract creative studio desk with campaign boards, generic devices and Australian colour accents; no real campaign logos.

**AI Form Builder prompt:**

```text
Create a detailed client campaign brief form for a fictional Australian agency called Northstar Creative Co.

Goal: collect enough information from a client to brief a campaign landing page or event lead form.

Design: desktop-first, structured sections with dividers, professional agency style, navy and orange accents, clear instructions.

Fields:
- Header: Northstar Creative Campaign Brief
- Paragraph: Share the campaign details we need to prepare a branded form or landing page. This is fictional demo content.
- Client company using Company Lookup (ABR), required, allow manual fallback
- Contact first name, required
- Contact last name, required
- Contact email, required
- Contact phone, optional
- Client website, URL field, optional
- Campaign name, text input, required
- Desired launch date, date picker, required
- Campaign type, required dropdown: Event lead capture, Product launch, Registration or RSVP, Customer feedback, Competition or giveaway, Other
- Channels required, checkbox group: Public link, Website embed, QR code, Kiosk/tablet, Email campaign, Social campaign
- Target audience, long text, required
- Required fields or data to collect, long text, required
- Brand notes, long text, optional
- Upload brand guide or campaign brief, file upload, optional, PDF/image accepted if supported
- Approval contact, text input, optional
- Terms checkbox: I confirm this fictional campaign brief can be used for demo purposes
- Submit button text: Submit campaign brief

Use only fictional Australian brands and safe placeholder content.
```

## Form 8 — Outreach Campaign Request

**Form name:** Ironbark Outreach Campaign Request

**Fictional brand:** Ironbark Growth Studio

**Description:** Campaign intake form for a fictional Australian growth team planning a compliant outreach campaign, including audience, offer, consent basis, channel preference and follow-up goals.

**Primary device target:** Desktop and tablet.

**Landing-page use:** Shows EventLead for outreach planning, campaign intake and structured handoff before follow-up activity starts.

**Components to include:** Header, paragraph, Company Lookup (ABR), first name, email, phone, URL, dropdown, radio, checkbox, number, textarea, terms, submit.

**Image/background idea:** Abstract Australian growth/connection visual with ironbark green, warm clay and navy; no real LinkedIn, email provider, CRM or social platform logos.

**AI Form Builder prompt:**

```text
Create an Australian outreach campaign request form for a fictional agency called Ironbark Growth Studio.

Goal: collect a structured brief for a compliant outreach campaign before the team drafts messages or starts follow-up.

Design: professional desktop/tablet layout, clear sections, ironbark green, warm clay and navy colours. The form should feel like a responsible campaign planning workflow, not a spam tool.

Fields:
- Header: Ironbark Outreach Campaign Request
- Paragraph: Share the campaign goals, audience and consent context so the team can prepare a safe outreach plan. This is fictional demo content.
- Requesting company using Company Lookup (ABR), required, allow manual fallback
- Contact first name, required
- Contact last name, required
- Contact email, required
- Contact phone, optional, Australian placeholder
- Company website, URL field, optional
- Campaign objective, required dropdown: Customer discovery, Event invitation, Product demo request, Partner outreach, Re-engagement, Other
- Primary audience, required dropdown: Existing customers, Warm prospects, Event attendees, Partners, Local businesses, Industry contacts
- Estimated audience size, number field, optional
- Preferred outreach channel, required radio: Email, Phone, LinkedIn-style professional network, SMS, Mixed channels
- Consent or relationship basis, required checkbox group: Existing customer relationship, Event registration, Opt-in list, Referral introduction, Public business contact, Needs review
- Personalisation inputs available, checkbox group: Name, Company, Role/title, Industry, Prior event attended, Pain point or interest, None yet
- Key message or offer, long text, required
- Follow-up outcome wanted, required dropdown: Book a meeting, Collect feedback, Confirm attendance, Send resources, Qualify interest
- Risks or exclusions, long text, optional, placeholder: "e.g. do not contact competitors, no sensitive industries, avoid weekends"
- Terms checkbox: I confirm this fictional outreach request is for demo purposes and should be reviewed before any real outreach
- Submit button text: Submit outreach request

Use only fictional Australian content. Do not mention real social networks by logo or brand styling, and do not imply automated spam or scraping.
```

## Landing Page Link Labels

Once published, use labels like:

- Event lead capture demo
- Demo drive request demo
- RSVP form demo
- Feedback survey demo
- Product inquiry demo
- Kiosk check-in demo
- Agency campaign brief demo
- Outreach campaign request demo

Avoid calling them "templates" unless users can actually copy them.

## What May Still Be Missing

Before external use, confirm:

- Public form URLs remain stable after edits or republishing.
- The public renderer can submit every component used here, especially file upload, Address Lookup (AU) and Company Lookup (ABR).
- Submitted data is visible in the admin/dashboard flow and can be exported or inspected.
- Thank-you/success states are presentable after submission.
- The landing page has a place to link examples without implying the fictional brands are real customers.
- Demo submissions are periodically cleared or clearly marked as test data.
- Any generated images have documented ownership/licensing.
- The support/contact mailbox shown publicly is real and monitored.

