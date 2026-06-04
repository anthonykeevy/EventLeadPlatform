"""Definition builders for the eight landing-page safe demo forms."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from seed_data.landing_demo.definition_builder import VerticalLayout, build_definition

DEMO_EVENT_NAME = "EventLead Public Demo Showcase 2026"
DEMO_EVENT_DESCRIPTION = (
    "A fictional demonstration event used to host public sample forms for EventLead. "
    "The event contains realistic but fake Australian campaign, event, inquiry, feedback, "
    "kiosk and agency workflows. Safe for screenshots, public demos and landing-page links."
)


@dataclass(frozen=True)
class LandingDemoFormSpec:
    slug: str
    form_name: str
    form_description: str
    primary_color: str
    builder: Callable[[], dict[str, Any]]


def _opts(pairs: list[tuple[str, str]]) -> list[dict[str, str]]:
    return [{"label": label, "value": value} for label, value in pairs]


def _terms(label: str) -> dict[str, Any]:
    return {"label": label, "required": True, "exportName": "terms_accepted"}


def _submit(text: str) -> dict[str, Any]:
    return {"buttonText": text, "required": False}


def build_rivergum_expo_lead() -> dict[str, Any]:
    ly = VerticalLayout()
    comps = [
        ly.header("Rivergum Expo Lead Capture"),
        ly.paragraph(
            "Thanks for visiting our demo stand. Leave your details and we will send "
            "the relevant information after the event."
        ),
        ly.place("first-name", label="First name", props={"required": True, "exportName": "first_name"}),
        ly.place("text", label="Last name", props={"required": True, "placeholder": "Last name", "exportName": "last_name"}),
        ly.place("email", label="Email address", props={"required": True, "placeholder": "name@example.com"}),
        ly.place(
            "phone",
            label="Mobile number",
            props={"required": True, "placeholder": "04xx xxx xxx", "exportName": "mobile"},
        ),
        ly.place(
            "company-lookup-abr",
            label="Company",
            props={"required": False, "allowManualFallback": True, "exportName": "company"},
        ),
        ly.place("text", label="Role / title", props={"required": False, "exportName": "role"}),
        ly.place(
            "dropdown",
            label="Main area of interest",
            props={
                "required": True,
                "options": _opts(
                    [
                        ("Event lead capture", "event_lead"),
                        ("Registration forms", "registration"),
                        ("Customer feedback", "feedback"),
                        ("Kiosk capture", "kiosk"),
                        ("Agency / client forms", "agency"),
                    ]
                ),
            },
        ),
        ly.place(
            "radio",
            label="Lead temperature",
            props={
                "required": True,
                "options": _opts(
                    [
                        ("Just researching", "researching"),
                        ("Interested in a pilot", "pilot"),
                        ("Ready to discuss", "ready"),
                    ]
                ),
            },
        ),
        ly.place(
            "checkbox",
            label="Follow-up preferences",
            props={
                "required": False,
                "options": _opts(
                    [
                        ("Email me information", "email_info"),
                        ("Call me this week", "call_week"),
                        ("Send pricing when available", "pricing"),
                        ("Invite me to future demos", "future_demos"),
                    ]
                ),
            },
            height=120,
        ),
        ly.place(
            "textarea",
            label="Notes from the conversation",
            props={"required": False, "placeholder": "Optional notes"},
            height=120,
        ),
        ly.place("terms", props=_terms("I agree to be contacted about this demo inquiry")),
        ly.place("submit-button", props=_submit("Send lead details"), height=64),
    ]
    return build_definition(comps, primary_color="#0F766E", form_id_suffix="rivergum-expo-lead")


def build_harbour_ev_demo_drive() -> dict[str, Any]:
    ly = VerticalLayout()
    comps = [
        ly.header("Book a Harbour EV demo drive"),
        ly.paragraph(
            "Tell us where and when you would like to try a fictional Harbour EV. "
            "This is a demo form using fake brand content."
        ),
        ly.place("first-name", label="First name", props={"required": True}),
        ly.place("email", label="Email address", props={"required": True}),
        ly.place("phone", label="Mobile number", props={"required": True, "placeholder": "04xx xxx xxx"}),
        ly.place(
            "address-lookup-au",
            label="Preferred demo location",
            props={"required": True, "allowManualFallback": True, "exportName": "demo_location"},
        ),
        ly.place("date", label="Preferred date", props={"required": True}),
        ly.place(
            "dropdown",
            label="Preferred time window",
            props={
                "required": True,
                "options": _opts(
                    [
                        ("Morning", "morning"),
                        ("Lunch time", "lunch"),
                        ("Afternoon", "afternoon"),
                        ("After work", "after_work"),
                        ("Weekend", "weekend"),
                    ]
                ),
            },
        ),
        ly.place(
            "radio",
            label="Vehicle interest",
            props={
                "required": True,
                "options": _opts(
                    [
                        ("City hatch", "hatch"),
                        ("Family SUV", "suv"),
                        ("Fleet vehicle", "fleet"),
                        ("Not sure yet", "unsure"),
                    ]
                ),
            },
        ),
        ly.place(
            "checkbox",
            label="Would you like charging information?",
            props={"required": False, "options": _opts([("Yes, send charging information", "charging_yes")])},
        ),
        ly.place("terms", props=_terms("I agree to be contacted about this demo request")),
        ly.place("submit-button", props=_submit("Request demo drive"), height=64),
    ]
    return build_definition(comps, primary_color="#0369A1", form_id_suffix="harbour-ev-demo")


def build_wattle_room_rsvp() -> dict[str, Any]:
    ly = VerticalLayout()
    comps = [
        ly.header("Brisbane Business Growth Breakfast RSVP"),
        ly.paragraph(
            "Reserve your place for a fictional breakfast session for Australian small business operators."
        ),
        ly.place("first-name", label="First name", props={"required": True}),
        ly.place("text", label="Last name", props={"required": True}),
        ly.place("email", label="Email address", props={"required": True}),
        ly.place("phone", label="Mobile number", props={"required": False, "placeholder": "04xx xxx xxx"}),
        ly.place("text", label="Organisation", props={"required": False}),
        ly.place("number", label="Number of attendees", props={"required": True, "min": 1}),
        ly.place(
            "dropdown",
            label="Attendance type",
            props={
                "required": True,
                "options": _opts(
                    [
                        ("Attending in person", "in_person"),
                        ("Joining waitlist", "waitlist"),
                        ("Unable to attend but send notes", "notes_only"),
                    ]
                ),
            },
        ),
        ly.place(
            "checkbox",
            label="Dietary requirements",
            props={
                "required": False,
                "options": _opts(
                    [
                        ("Vegetarian", "veg"),
                        ("Vegan", "vegan"),
                        ("Gluten free", "gf"),
                        ("Dairy free", "df"),
                        ("Nut allergy", "nuts"),
                        ("No special requirements", "none"),
                    ]
                ),
            },
            height=140,
        ),
        ly.place(
            "textarea",
            label="Accessibility or seating notes",
            props={"required": False},
            height=100,
        ),
        ly.place("terms", props=_terms("I confirm these details are accurate for this demo RSVP")),
        ly.place("submit-button", props=_submit("Submit RSVP"), height=64),
    ]
    return build_definition(comps, primary_color="#B45309", form_id_suffix="wattle-room-rsvp")


def build_coastal_home_feedback() -> dict[str, Any]:
    ly = VerticalLayout()
    comps = [
        ly.header("Coastal Home Expo Feedback"),
        ly.paragraph(
            "Thanks for visiting our fictional expo. Your feedback helps us improve the next event."
        ),
        ly.place(
            "rating",
            label="Overall event rating",
            props={"required": True, "ratingMax": 5, "ratingStyle": "stars"},
        ),
        ly.place(
            "radio",
            label="How likely are you to recommend the expo?",
            props={
                "required": True,
                "options": _opts(
                    [
                        ("0-3 Unlikely", "unlikely"),
                        ("4-6 Maybe", "maybe"),
                        ("7-8 Likely", "likely"),
                        ("9-10 Very likely", "very_likely"),
                    ]
                ),
            },
            height=120,
        ),
        ly.place(
            "checkbox",
            label="What interested you most?",
            props={
                "required": False,
                "options": _opts(
                    [
                        ("Renovation ideas", "reno"),
                        ("Outdoor living", "outdoor"),
                        ("Solar and energy", "solar"),
                        ("Furniture and styling", "furniture"),
                        ("Builders and suppliers", "builders"),
                        ("Food and entertainment", "food"),
                    ]
                ),
            },
            height=140,
        ),
        ly.place("textarea", label="What could be improved?", props={"required": False}, height=100),
        ly.place(
            "radio",
            label="Would you like updates about the next event?",
            props={"required": True, "options": _opts([("Yes", "yes"), ("No", "no")])},
        ),
        ly.place("email", label="Email address (optional)", props={"required": False}),
        ly.place("submit-button", props=_submit("Send feedback"), height=64),
    ]
    return build_definition(comps, primary_color="#0D9488", form_id_suffix="coastal-feedback")


def build_banksia_product_inquiry() -> dict[str, Any]:
    ly = VerticalLayout()
    comps = [
        ly.header("Banksia Outdoor Living Product Inquiry"),
        ly.paragraph(
            "Tell us about your outdoor project and we will suggest suitable product options. "
            "This is a demo form using fictional brand content."
        ),
        ly.place("first-name", label="First name", props={"required": True}),
        ly.place("text", label="Last name", props={"required": True}),
        ly.place("email", label="Email address", props={"required": True}),
        ly.place("phone", label="Mobile number", props={"required": True}),
        ly.place(
            "address-lookup-au",
            label="Project address",
            props={"required": True, "allowManualFallback": True, "exportName": "project_address"},
        ),
        ly.place(
            "dropdown",
            label="Product category",
            props={
                "required": True,
                "options": _opts(
                    [
                        ("Outdoor seating", "seating"),
                        ("Shade structure", "shade"),
                        ("Event activation furniture", "activation"),
                        ("Planters and styling", "planters"),
                        ("Not sure yet", "unsure"),
                    ]
                ),
            },
        ),
        ly.place("number", label="Approximate budget (AUD)", props={"required": False}),
        ly.place(
            "radio",
            label="Project timing",
            props={
                "required": True,
                "options": _opts(
                    [
                        ("This month", "this_month"),
                        ("1-3 months", "one_three"),
                        ("3-6 months", "three_six"),
                        ("Just researching", "research"),
                    ]
                ),
            },
        ),
        ly.place("url", label="Website or inspiration link", props={"required": False}),
        ly.place(
            "file-upload",
            label="Upload site photo or sketch",
            props={"required": False, "accept": "image/*,.pdf", "maxFileSizeMb": 10},
            height=96,
        ),
        ly.place("textarea", label="Project notes", props={"required": False}, height=120),
        ly.place("terms", props=_terms("I agree to be contacted about this inquiry")),
        ly.place("submit-button", props=_submit("Send product inquiry"), height=64),
    ]
    return build_definition(comps, primary_color="#78350F", form_id_suffix="banksia-inquiry")


def build_eucalypt_kiosk_checkin() -> dict[str, Any]:
    ly = VerticalLayout(step=92)
    comps = [
        ly.header("Eucalypt Workspace Visitor Check-In", height=64),
        ly.paragraph(
            "Welcome. Please check in before entering the workspace. This is a fictional demo form.",
            height=88,
        ),
        ly.place("first-name", label="First name", props={"required": True}, height=80),
        ly.place("text", label="Last name", props={"required": True}, height=80),
        ly.place("phone", label="Mobile number", props={"required": True, "placeholder": "04xx xxx xxx"}, height=80),
        ly.place("email", label="Email address", props={"required": False}, height=80),
        ly.place(
            "company-lookup-abr",
            label="Company",
            props={"required": False, "allowManualFallback": True},
            height=88,
        ),
        ly.place(
            "dropdown",
            label="Who are you visiting?",
            props={
                "required": True,
                "options": _opts(
                    [
                        ("Community manager", "community"),
                        ("Meeting room booking", "meeting"),
                        ("Event host", "event_host"),
                        ("Workspace member", "member"),
                        ("Other", "other"),
                    ]
                ),
            },
            height=88,
        ),
        ly.place(
            "radio",
            label="Visitor type",
            props={
                "required": True,
                "options": _opts(
                    [
                        ("Meeting guest", "guest"),
                        ("Event attendee", "attendee"),
                        ("Contractor", "contractor"),
                        ("Delivery", "delivery"),
                        ("Other", "other"),
                    ]
                ),
            },
            height=120,
        ),
        ly.place(
            "checkbox",
            label="Safety acknowledgement",
            props={
                "required": True,
                "options": _opts(
                    [("I agree to follow reception and visitor instructions while onsite", "safety_ok")]
                ),
            },
            height=88,
        ),
        ly.place("submit-button", props=_submit("Check in"), height=72),
    ]
    return build_definition(comps, primary_color="#15803D", form_id_suffix="eucalypt-kiosk")


def build_northstar_campaign_brief() -> dict[str, Any]:
    ly = VerticalLayout()
    comps = [
        ly.header("Northstar Creative Campaign Brief"),
        ly.paragraph(
            "Share the campaign details we need to prepare a branded form or landing page. "
            "This is fictional demo content."
        ),
        ly.divider(),
        ly.place(
            "company-lookup-abr",
            label="Client company",
            props={"required": True, "allowManualFallback": True},
        ),
        ly.place("first-name", label="Contact first name", props={"required": True}),
        ly.place("text", label="Contact last name", props={"required": True}),
        ly.place("email", label="Contact email", props={"required": True}),
        ly.place("phone", label="Contact phone", props={"required": False}),
        ly.place("url", label="Client website", props={"required": False}),
        ly.place("text", label="Campaign name", props={"required": True}),
        ly.place("date", label="Desired launch date", props={"required": True}),
        ly.place(
            "dropdown",
            label="Campaign type",
            props={
                "required": True,
                "options": _opts(
                    [
                        ("Event lead capture", "event_lead"),
                        ("Product launch", "launch"),
                        ("Registration or RSVP", "rsvp"),
                        ("Customer feedback", "feedback"),
                        ("Competition or giveaway", "competition"),
                        ("Other", "other"),
                    ]
                ),
            },
        ),
        ly.place(
            "checkbox",
            label="Channels required",
            props={
                "required": False,
                "options": _opts(
                    [
                        ("Public link", "link"),
                        ("Website embed", "embed"),
                        ("QR code", "qr"),
                        ("Kiosk / tablet", "kiosk"),
                        ("Email campaign", "email"),
                        ("Social campaign", "social"),
                    ]
                ),
            },
            height=140,
        ),
        ly.place("textarea", label="Target audience", props={"required": True}, height=100),
        ly.place("textarea", label="Required fields or data to collect", props={"required": True}, height=100),
        ly.place("textarea", label="Brand notes", props={"required": False}, height=100),
        ly.place(
            "file-upload",
            label="Upload brand guide or campaign brief",
            props={"required": False, "accept": "image/*,.pdf", "maxFileSizeMb": 15},
            height=96,
        ),
        ly.place("text", label="Approval contact", props={"required": False}),
        ly.place(
            "terms",
            props=_terms("I confirm this fictional campaign brief can be used for demo purposes"),
        ),
        ly.place("submit-button", props=_submit("Submit campaign brief"), height=64),
    ]
    return build_definition(comps, primary_color="#1E3A8A", form_id_suffix="northstar-brief")


def build_ironbark_outreach_request() -> dict[str, Any]:
    ly = VerticalLayout()
    comps = [
        ly.header("Ironbark Outreach Campaign Request"),
        ly.paragraph(
            "Share the campaign goals, audience and consent context so the team can prepare "
            "a safe outreach plan. This is fictional demo content."
        ),
        ly.place(
            "company-lookup-abr",
            label="Requesting company",
            props={"required": True, "allowManualFallback": True},
        ),
        ly.place("first-name", label="Contact first name", props={"required": True}),
        ly.place("text", label="Contact last name", props={"required": True}),
        ly.place("email", label="Contact email", props={"required": True}),
        ly.place("phone", label="Contact phone", props={"required": False, "placeholder": "04xx xxx xxx"}),
        ly.place("url", label="Company website", props={"required": False}),
        ly.place(
            "dropdown",
            label="Campaign objective",
            props={
                "required": True,
                "options": _opts(
                    [
                        ("Customer discovery", "discovery"),
                        ("Event invitation", "event"),
                        ("Product demo request", "demo"),
                        ("Partner outreach", "partner"),
                        ("Re-engagement", "reengage"),
                        ("Other", "other"),
                    ]
                ),
            },
        ),
        ly.place(
            "dropdown",
            label="Primary audience",
            props={
                "required": True,
                "options": _opts(
                    [
                        ("Existing customers", "customers"),
                        ("Warm prospects", "prospects"),
                        ("Event attendees", "attendees"),
                        ("Partners", "partners"),
                        ("Local businesses", "local"),
                        ("Industry contacts", "industry"),
                    ]
                ),
            },
        ),
        ly.place("number", label="Estimated audience size", props={"required": False}),
        ly.place(
            "radio",
            label="Preferred outreach channel",
            props={
                "required": True,
                "options": _opts(
                    [
                        ("Email", "email"),
                        ("Phone", "phone"),
                        ("Professional network", "network"),
                        ("SMS", "sms"),
                        ("Mixed channels", "mixed"),
                    ]
                ),
            },
        ),
        ly.place(
            "checkbox",
            label="Consent or relationship basis",
            props={
                "required": True,
                "options": _opts(
                    [
                        ("Existing customer relationship", "customer"),
                        ("Event registration", "event_reg"),
                        ("Opt-in list", "optin"),
                        ("Referral introduction", "referral"),
                        ("Public business contact", "public"),
                        ("Needs review", "review"),
                    ]
                ),
            },
            height=140,
        ),
        ly.place(
            "checkbox",
            label="Personalisation inputs available",
            props={
                "required": False,
                "options": _opts(
                    [
                        ("Name", "name"),
                        ("Company", "company"),
                        ("Role / title", "role"),
                        ("Industry", "industry"),
                        ("Prior event attended", "prior_event"),
                        ("Pain point or interest", "pain"),
                        ("None yet", "none"),
                    ]
                ),
            },
            height=140,
        ),
        ly.place("textarea", label="Key message or offer", props={"required": True}, height=120),
        ly.place(
            "dropdown",
            label="Follow-up outcome wanted",
            props={
                "required": True,
                "options": _opts(
                    [
                        ("Book a meeting", "meeting"),
                        ("Collect feedback", "feedback"),
                        ("Confirm attendance", "attendance"),
                        ("Send resources", "resources"),
                        ("Qualify interest", "qualify"),
                    ]
                ),
            },
        ),
        ly.place(
            "textarea",
            label="Risks or exclusions",
            props={
                "required": False,
                "placeholder": "e.g. do not contact competitors, no sensitive industries, avoid weekends",
            },
            height=100,
        ),
        ly.place(
            "terms",
            props=_terms(
                "I confirm this fictional outreach request is for demo purposes and "
                "should be reviewed before any real outreach"
            ),
        ),
        ly.place("submit-button", props=_submit("Submit outreach request"), height=64),
    ]
    return build_definition(comps, primary_color="#365314", form_id_suffix="ironbark-outreach")


LANDING_DEMO_FORMS: list[LandingDemoFormSpec] = [
    LandingDemoFormSpec(
        "rivergum-expo-lead",
        "Rivergum Expo Lead Capture",
        "Captures leads at a fictional Australian trade expo booth (Rivergum Events Collective).",
        "#0F766E",
        build_rivergum_expo_lead,
    ),
    LandingDemoFormSpec(
        "harbour-ev-demo-drive",
        "Harbour EV Demo Drive Request",
        "Mobile-first demo drive request for fictional Harbour EV Studio.",
        "#0369A1",
        build_harbour_ev_demo_drive,
    ),
    LandingDemoFormSpec(
        "wattle-room-rsvp",
        "Wattle Room Business Breakfast RSVP",
        "RSVP for a fictional Brisbane business breakfast (Wattle Room Events).",
        "#B45309",
        build_wattle_room_rsvp,
    ),
    LandingDemoFormSpec(
        "coastal-home-feedback",
        "Coastal Home Expo Feedback",
        "Post-event feedback and NPS-style questions (Coastal Home Expo).",
        "#0D9488",
        build_coastal_home_feedback,
    ),
    LandingDemoFormSpec(
        "banksia-product-inquiry",
        "Banksia Outdoor Living Product Inquiry",
        "Detailed product inquiry with address and file upload (Banksia Outdoor Living).",
        "#78350F",
        build_banksia_product_inquiry,
    ),
    LandingDemoFormSpec(
        "eucalypt-kiosk-checkin",
        "Eucalypt Workspace Visitor Check-In",
        "Tablet kiosk visitor check-in (Eucalypt Workspace).",
        "#15803D",
        build_eucalypt_kiosk_checkin,
    ),
    LandingDemoFormSpec(
        "northstar-campaign-brief",
        "Northstar Creative Campaign Brief",
        "Agency client campaign intake (Northstar Creative Co.).",
        "#1E3A8A",
        build_northstar_campaign_brief,
    ),
    LandingDemoFormSpec(
        "ironbark-outreach-request",
        "Ironbark Outreach Campaign Request",
        "Compliant outreach campaign planning brief (Ironbark Growth Studio).",
        "#365314",
        build_ironbark_outreach_request,
    ),
]
