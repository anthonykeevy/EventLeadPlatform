"""AI Form Builder prompts for Story 6.5e landing demo shells (migration 096)."""

from __future__ import annotations

from dataclasses import dataclass

DEMO_EVENT_NAME = "EventLead Public Demo Showcase 2026"
DEMO_EVENT_DESCRIPTION = (
    "A fictional demonstration event used to host public sample forms for EventLead. "
    "The event contains realistic but fake Australian campaign, event, inquiry, feedback, "
    "kiosk and agency workflows. It is safe for screenshots, public demos and landing-page links."
)
DEMO_EVENT_SHORT = "Public demo forms for EventLead landing page and customer discovery."
DEMO_TAG = "story-6.5e-landing-demo"

COMPANY_ID = 1
SEED_USER_ID = 1


@dataclass(frozen=True)
class LandingDemoFormRow:
    slug: str
    form_name: str
    form_description: str
    ai_prompt: str


PROMPT_RIVERGUM = """Create a branded Australian event lead capture form for a fictional company called Rivergum Events Collective at the "EventLead Public Demo Showcase 2026".

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

Use realistic fake Australian examples only. Do not mention or copy real brands."""

PROMPT_HARBOUR = """Create a mobile-first demo drive request form for a fictional Australian brand called Harbour EV Studio.

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

Keep the form concise for mobile. Use only fictional Australian content."""

PROMPT_WATTLE = """Create an Australian RSVP and registration form for a fictional event brand called Wattle Room Events.

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

Use realistic but fake Australian event wording."""

PROMPT_COASTAL = """Create a mobile-friendly customer feedback and NPS-style form for a fictional Australian event called Coastal Home Expo.

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

Use fictional Australian content and avoid real venue or exhibitor names."""

PROMPT_BANKSIA = """Create a desktop-friendly product inquiry form for a fictional Australian brand called Banksia Outdoor Living.

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

Keep all brand and product names fictional and Australian focused."""

PROMPT_EUCALYPT = """Create a tablet kiosk visitor check-in form for a fictional Australian co-working brand called Eucalypt Workspace.

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

Keep wording short and suitable for a public tablet."""

PROMPT_NORTHSTAR = """Create a detailed client campaign brief form for a fictional Australian agency called Northstar Creative Co.

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

Use only fictional Australian brands and safe placeholder content."""

PROMPT_IRONBARK = """Create an Australian outreach campaign request form for a fictional agency called Ironbark Growth Studio.

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

Use only fictional Australian content. Do not mention real social networks by logo or brand styling, and do not imply automated spam or scraping."""

LANDING_DEMO_FORM_ROWS: list[LandingDemoFormRow] = [
    LandingDemoFormRow(
        "rivergum-expo-lead",
        "Rivergum Expo Lead Capture",
        "Captures leads at a fictional Australian trade expo booth (Rivergum Events Collective).",
        PROMPT_RIVERGUM,
    ),
    LandingDemoFormRow(
        "harbour-ev-demo-drive",
        "Harbour EV Demo Drive Request",
        "Mobile-first demo drive request for fictional Harbour EV Studio.",
        PROMPT_HARBOUR,
    ),
    LandingDemoFormRow(
        "wattle-room-rsvp",
        "Wattle Room Business Breakfast RSVP",
        "RSVP for a fictional Brisbane business breakfast (Wattle Room Events).",
        PROMPT_WATTLE,
    ),
    LandingDemoFormRow(
        "coastal-home-feedback",
        "Coastal Home Expo Feedback",
        "Post-event feedback and NPS-style questions (Coastal Home Expo).",
        PROMPT_COASTAL,
    ),
    LandingDemoFormRow(
        "banksia-product-inquiry",
        "Banksia Outdoor Living Product Inquiry",
        "Detailed product inquiry with address and file upload (Banksia Outdoor Living).",
        PROMPT_BANKSIA,
    ),
    LandingDemoFormRow(
        "eucalypt-kiosk-checkin",
        "Eucalypt Workspace Visitor Check-In",
        "Tablet kiosk visitor check-in (Eucalypt Workspace).",
        PROMPT_EUCALYPT,
    ),
    LandingDemoFormRow(
        "northstar-campaign-brief",
        "Northstar Creative Campaign Brief",
        "Agency client campaign intake (Northstar Creative Co.).",
        PROMPT_NORTHSTAR,
    ),
    LandingDemoFormRow(
        "ironbark-outreach-request",
        "Ironbark Outreach Campaign Request",
        "Compliant outreach campaign planning brief (Ironbark Growth Studio).",
        PROMPT_IRONBARK,
    ),
]
