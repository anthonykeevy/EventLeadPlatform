"""Story 6.3.1 UAT spot-check: deterministic compiler against 10 benchmark prompts.

Mirrors the prompts catalogued in docs/stories/STORY-6.3-BENCHMARK-PROMPTS-AND-OUTCOMES.md
by hand-building the semantic plan a well-behaved LLM should now emit for each
prompt (no coordinates, only intent). Runs the deterministic compiler and
reports geometry, overlap detection, off-canvas detection, and the headline
compileSummary fields.

This is a *layout* spot-check, not a prompt-engineering test. It deliberately
bypasses the LLM so we can pin the compiler under controlled inputs and prove
that items 1-3 of the close-uat-compiler-gap plan generalise across prompt
diversity (not just prompts 3 and 5 we manually tested).

Run from backend/:
    python scripts/story_631_uat_spotcheck.py

Exit code 0 = all 10 prompts pass (no overlaps, no off-canvas).
Exit code 1 = at least one prompt has a layout failure.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# backend/ (parent of scripts/) needs to be on sys.path so this script runs
# from any working directory.
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from modules.form_ai.compiler import (  # noqa: E402
    DEFAULT_MARGIN_X,
    compile_semantic_plan_to_definition,
)
from modules.form_ai.schemas import FormSemanticPlan  # noqa: E402


# --- Governance config -------------------------------------------------------
# Mirrors backend/tests/test_story_631_deterministic_compiler.py::_governance_payload()
# but expanded to cover every component type the 10 benchmark prompts emit.

GOVERNANCE: Dict[str, Any] = {
    "capabilityPolicyJson": {
        "step1": {"allowSemanticOnly": True, "allowGeometry": False},
        "step2": {"gridOnly": True, "allowNonGrid": False},
    },
    "widthClassPolicyJson": {
        "classes": {
            "compact": {"minSpan": 3, "targetSpan": 4, "maxSpan": 5},
            "half": {"minSpan": 5, "targetSpan": 6, "maxSpan": 7},
            "full": {"minSpan": 10, "targetSpan": 12, "maxSpan": 12},
        },
        "downgradeRules": [
            {"if": "canvasWidth<1200", "from": "half", "to": "full"},
        ],
    },
    "componentCapabilitySnapshotJson": {
        "components": [
            {"type": "header", "widthClasses": ["full"]},
            {"type": "paragraph", "widthClasses": ["full"]},
            {"type": "text", "widthClasses": ["compact", "half", "full"]},
            {"type": "email", "widthClasses": ["compact", "half", "full"]},
            {"type": "phone", "widthClasses": ["compact", "half", "full"]},
            {"type": "number", "widthClasses": ["compact", "half", "full"]},
            {"type": "url", "widthClasses": ["half", "full"]},
            {"type": "date", "widthClasses": ["compact", "half"]},
            {"type": "address", "widthClasses": ["full"]},
            {"type": "dropdown", "widthClasses": ["compact", "half", "full"]},
            {"type": "radio", "widthClasses": ["half", "full"]},
            {"type": "checkbox", "widthClasses": ["half", "full"]},
            {"type": "rating", "widthClasses": ["half", "full"]},
            {"type": "textarea", "widthClasses": ["half", "full"]},
            {"type": "file-upload", "widthClasses": ["full"]},
            {"type": "terms", "widthClasses": ["full"]},
            {"type": "submit-button", "widthClasses": ["compact", "half"]},
        ]
    },
    "validationContracts": [
        {"componentType": "text", "allowedRules": ["required", "maxLength"]},
        {"componentType": "email", "allowedRules": ["required", "email", "maxLength"]},
        {"componentType": "phone", "allowedRules": ["required", "phone", "maxLength"]},
        {"componentType": "number", "allowedRules": ["required", "min", "max"]},
        {"componentType": "url", "allowedRules": ["required", "url", "maxLength"]},
        {"componentType": "date", "allowedRules": ["required"]},
        {"componentType": "address", "allowedRules": ["required"]},
        {"componentType": "dropdown", "allowedRules": ["required"]},
        {"componentType": "radio", "allowedRules": ["required"]},
        {"componentType": "checkbox", "allowedRules": ["required"]},
        {"componentType": "rating", "allowedRules": ["required", "min", "max"]},
        {"componentType": "textarea", "allowedRules": ["required", "minLength", "maxLength"]},
        {"componentType": "file-upload", "allowedRules": ["required"]},
        {"componentType": "terms", "allowedRules": ["required"]},
        {"componentType": "submit-button", "allowedRules": []},
        {"componentType": "header", "allowedRules": []},
        {"componentType": "paragraph", "allowedRules": []},
    ],
}

CANVAS = {"width": 1920, "height": 980, "gridSize": 8}


# --- Component shorthand -----------------------------------------------------


def _yes_no() -> List[Dict[str, str]]:
    return [{"label": "Yes", "value": "yes"}, {"label": "No", "value": "no"}]


def _opts(*labels: str) -> List[Dict[str, str]]:
    return [{"label": lbl, "value": lbl.lower().replace(" ", "-")} for lbl in labels]


def _v(**kwargs: Any) -> Dict[str, Any]:
    """Concise validationIntent literal."""
    return {k: v for k, v in kwargs.items() if v is not None}


# --- 10 benchmark prompts as semantic plans ---------------------------------
# Each plan mirrors what a compliant LLM should emit per the Story 6.3.1
# contract: no coordinates, only semantic intent (componentType, label,
# widthIntent, validationIntent, section, rowGroup, options, actionAlignment).


def _bm01_party_rsvp() -> FormSemanticPlan:
    return FormSemanticPlan.model_validate({
        "semanticPlanVersion": "1.0",
        "formId": "bm01-party-rsvp",
        "title": "Party RSVP",
        "components": [
            {"componentType": "text",  "label": "Full name",         "widthIntent": "full",   "section": "guest",     "rowGroup": "name",     "validationIntent": _v(required=True, maxLength=80)},
            {"componentType": "phone", "label": "Phone number",      "widthIntent": "half",   "section": "guest",     "rowGroup": "contact",  "validationIntent": _v(required=True, phone=True, maxLength=20)},
            {"componentType": "email", "label": "Email",             "widthIntent": "half",   "section": "guest",     "rowGroup": "contact",  "validationIntent": _v(required=True, email=True, maxLength=80)},
            {"componentType": "radio", "label": "Will you attend?",  "widthIntent": "full",   "section": "rsvp",      "rowGroup": "attend",   "options": _yes_no(), "validationIntent": _v(required=True)},
            {"componentType": "number","label": "How many guests?",  "widthIntent": "compact","section": "rsvp",      "rowGroup": "guests",   "validationIntent": _v(required=False, min=0, max=20)},
            {"componentType": "submit-button", "label": "Submit",     "widthIntent": "compact","actionAlignment": "center", "section": "action"},
        ],
    })


def _bm02_contact_address() -> FormSemanticPlan:
    return FormSemanticPlan.model_validate({
        "semanticPlanVersion": "1.0",
        "formId": "bm02-contact-address",
        "title": "Contact",
        "components": [
            {"componentType": "text",     "label": "First name",   "widthIntent": "half", "section": "person",  "rowGroup": "name",    "validationIntent": _v(required=True, maxLength=40)},
            {"componentType": "text",     "label": "Last name",    "widthIntent": "half", "section": "person",  "rowGroup": "name",    "validationIntent": _v(required=True, maxLength=40)},
            {"componentType": "address",  "label": "Address",      "widthIntent": "full", "section": "address"},
            {"componentType": "phone",    "label": "Phone",        "widthIntent": "half", "section": "person",  "rowGroup": "contact", "validationIntent": _v(phone=True, maxLength=20)},
            {"componentType": "email",    "label": "Email",        "widthIntent": "half", "section": "person",  "rowGroup": "contact", "validationIntent": _v(required=True, email=True, maxLength=80)},
            {"componentType": "text",     "label": "Company name", "widthIntent": "full", "section": "company",                      "validationIntent": _v(maxLength=120)},
            {"componentType": "textarea", "label": "Comments",     "widthIntent": "full", "section": "comments",                     "validationIntent": _v(maxLength=2000)},
            {"componentType": "submit-button", "label": "Submit",  "widthIntent": "compact", "actionAlignment": "center", "section": "action"},
        ],
    })


def _bm03_event_registration() -> FormSemanticPlan:
    return FormSemanticPlan.model_validate({
        "semanticPlanVersion": "1.0",
        "formId": "bm03-event-registration",
        "title": "Tech Conference Registration",
        "components": [
            {"componentType": "header",   "label": "Tech Conference Registration", "widthIntent": "full", "section": "intro"},
            {"componentType": "text",     "label": "First name",     "widthIntent": "half", "section": "attendee", "rowGroup": "name",    "validationIntent": _v(required=True, maxLength=40)},
            {"componentType": "text",     "label": "Last name",      "widthIntent": "half", "section": "attendee", "rowGroup": "name",    "validationIntent": _v(required=True, maxLength=40)},
            {"componentType": "email",    "label": "Email address",  "widthIntent": "half", "section": "attendee", "rowGroup": "contact", "validationIntent": _v(required=True, email=True, maxLength=80)},
            {"componentType": "phone",    "label": "Phone number",   "widthIntent": "half", "section": "attendee", "rowGroup": "contact", "validationIntent": _v(required=True, phone=True, maxLength=20)},
            {"componentType": "text",     "label": "Company name",   "widthIntent": "half", "section": "work",     "rowGroup": "company", "validationIntent": _v(maxLength=120)},
            {"componentType": "text",     "label": "Job title",      "widthIntent": "half", "section": "work",     "rowGroup": "company", "validationIntent": _v(maxLength=80)},
            {"componentType": "dropdown", "label": "Country",        "widthIntent": "half", "section": "work",     "options": _opts("Australia", "United States", "United Kingdom", "Canada", "New Zealand", "Other"), "validationIntent": _v(required=True)},
            {"componentType": "submit-button", "label": "Register",   "widthIntent": "compact", "actionAlignment": "center", "section": "action"},
        ],
    })


def _bm04_job_application() -> FormSemanticPlan:
    return FormSemanticPlan.model_validate({
        "semanticPlanVersion": "1.0",
        "formId": "bm04-job-application",
        "title": "Job Application",
        "components": [
            {"componentType": "text",        "label": "First name",    "widthIntent": "half", "section": "applicant", "rowGroup": "name",    "validationIntent": _v(required=True, maxLength=40)},
            {"componentType": "text",        "label": "Last name",     "widthIntent": "half", "section": "applicant", "rowGroup": "name",    "validationIntent": _v(required=True, maxLength=40)},
            {"componentType": "email",       "label": "Email",         "widthIntent": "half", "section": "applicant", "rowGroup": "contact", "validationIntent": _v(required=True, email=True, maxLength=80)},
            {"componentType": "phone",       "label": "Phone",         "widthIntent": "half", "section": "applicant", "rowGroup": "contact", "validationIntent": _v(required=True, phone=True, maxLength=20)},
            {"componentType": "text",        "label": "Location",      "widthIntent": "half", "section": "applicant", "rowGroup": "where",   "validationIntent": _v(maxLength=80)},
            {"componentType": "url",         "label": "LinkedIn URL",  "widthIntent": "half", "section": "applicant", "rowGroup": "where",   "validationIntent": _v(url=True, maxLength=200)},
            {"componentType": "textarea",    "label": "Why are you interested?", "widthIntent": "full", "section": "interest",  "validationIntent": _v(required=True, maxLength=2000)},
            {"componentType": "file-upload", "label": "Resume",        "widthIntent": "full", "section": "attachments", "validationIntent": _v(required=True)},
            {"componentType": "dropdown",    "label": "How did you hear about us?", "widthIntent": "half", "section": "attribution", "options": _opts("Company Website", "LinkedIn", "Facebook", "Referral", "Other")},
            {"componentType": "terms",       "label": "I agree to the privacy policy", "widthIntent": "full", "section": "consent", "validationIntent": _v(required=True)},
            {"componentType": "submit-button","label": "Apply Now",     "widthIntent": "compact", "actionAlignment": "center", "section": "action"},
        ],
    })


def _bm05_customer_feedback() -> FormSemanticPlan:
    return FormSemanticPlan.model_validate({
        "semanticPlanVersion": "1.0",
        "formId": "bm05-customer-feedback",
        "title": "Customer Feedback",
        "components": [
            {"componentType": "header",   "label": "Customer Feedback",                       "widthIntent": "full",   "section": "intro"},
            {"componentType": "rating",   "label": "How would you rate your overall experience?", "widthIntent": "half", "section": "satisfaction", "rowGroup": "ratings", "validationIntent": _v(required=True, min=1, max=5)},
            {"componentType": "rating",   "label": "How likely are you to recommend us?",     "widthIntent": "half",   "section": "satisfaction", "rowGroup": "ratings", "validationIntent": _v(required=True, min=0, max=10)},
            {"componentType": "textarea", "label": "What did you like most?",                 "widthIntent": "full",   "section": "comments", "validationIntent": _v(maxLength=2000)},
            {"componentType": "textarea", "label": "What could we improve?",                  "widthIntent": "full",   "section": "comments", "validationIntent": _v(maxLength=2000)},
            {"componentType": "dropdown", "label": "How did you find us?",                    "widthIntent": "half",   "section": "attribution", "options": _opts("Search Engine", "Social Media", "Friend", "Advertisement", "Other")},
            {"componentType": "submit-button", "label": "Submit",                              "widthIntent": "compact","actionAlignment": "center", "section": "action"},
        ],
    })


def _bm06_merchandise_order() -> FormSemanticPlan:
    return FormSemanticPlan.model_validate({
        "semanticPlanVersion": "1.0",
        "formId": "bm06-merch-order",
        "title": "Merchandise Order",
        "components": [
            {"componentType": "text",     "label": "First name",      "widthIntent": "half", "section": "customer", "rowGroup": "name",    "validationIntent": _v(required=True, maxLength=40)},
            {"componentType": "text",     "label": "Last name",       "widthIntent": "half", "section": "customer", "rowGroup": "name",    "validationIntent": _v(required=True, maxLength=40)},
            {"componentType": "email",    "label": "Email",           "widthIntent": "half", "section": "customer", "rowGroup": "contact", "validationIntent": _v(required=True, email=True, maxLength=80)},
            {"componentType": "phone",    "label": "Phone number",    "widthIntent": "half", "section": "customer", "rowGroup": "contact", "validationIntent": _v(required=True, phone=True, maxLength=20)},
            {"componentType": "address",  "label": "Shipping address","widthIntent": "full", "section": "shipping"},
            {"componentType": "checkbox", "label": "How did you hear about us?", "widthIntent": "full", "section": "attribution", "options": _opts("Facebook", "Instagram", "Twitter", "YouTube", "Television", "Internet Search", "Referral", "Other")},
            {"componentType": "textarea", "label": "Special instructions", "widthIntent": "full", "section": "notes", "validationIntent": _v(maxLength=1000)},
            {"componentType": "submit-button", "label": "Place Order",  "widthIntent": "compact", "actionAlignment": "center", "section": "action"},
        ],
    })


def _bm07_newsletter() -> FormSemanticPlan:
    return FormSemanticPlan.model_validate({
        "semanticPlanVersion": "1.0",
        "formId": "bm07-newsletter",
        "title": "Stay in the loop",
        "components": [
            {"componentType": "header",    "label": "Stay in the loop",                                              "widthIntent": "full", "section": "intro"},
            {"componentType": "paragraph", "label": "Get the latest updates delivered to your inbox.",               "widthIntent": "full", "section": "intro"},
            {"componentType": "email",     "label": "Email address",                                                  "widthIntent": "full", "section": "signup", "validationIntent": _v(required=True, email=True, maxLength=80)},
            {"componentType": "submit-button", "label": "Subscribe",  "widthIntent": "compact", "actionAlignment": "center", "section": "action"},
        ],
    })


def _bm08_pre_order() -> FormSemanticPlan:
    return FormSemanticPlan.model_validate({
        "semanticPlanVersion": "1.0",
        "formId": "bm08-pre-order",
        "title": "Pre-Order",
        "components": [
            {"componentType": "text",     "label": "First name",   "widthIntent": "half",    "section": "customer", "rowGroup": "name",    "validationIntent": _v(required=True, maxLength=40)},
            {"componentType": "text",     "label": "Middle name",  "widthIntent": "compact", "section": "customer", "rowGroup": "name",    "validationIntent": _v(maxLength=40)},
            {"componentType": "text",     "label": "Last name",    "widthIntent": "half",    "section": "customer", "rowGroup": "name",    "validationIntent": _v(required=True, maxLength=40)},
            {"componentType": "phone",    "label": "Phone",        "widthIntent": "half",    "section": "customer", "rowGroup": "contact", "validationIntent": _v(required=True, phone=True, maxLength=20)},
            {"componentType": "email",    "label": "Email",        "widthIntent": "half",    "section": "customer", "rowGroup": "contact", "validationIntent": _v(required=True, email=True, maxLength=80)},
            {"componentType": "address",  "label": "Delivery address", "widthIntent": "full", "section": "delivery"},
            {"componentType": "date",     "label": "Preferred delivery date", "widthIntent": "half", "section": "delivery", "rowGroup": "schedule"},
            {"componentType": "date",     "label": "Preferred delivery time", "widthIntent": "half", "section": "delivery", "rowGroup": "schedule"},
            {"componentType": "textarea", "label": "Special delivery notes",   "widthIntent": "full", "section": "delivery", "validationIntent": _v(maxLength=1000)},
            {"componentType": "submit-button", "label": "Place Pre-Order",     "widthIntent": "compact", "actionAlignment": "center", "section": "action"},
        ],
    })


def _bm09_support_ticket() -> FormSemanticPlan:
    return FormSemanticPlan.model_validate({
        "semanticPlanVersion": "1.0",
        "formId": "bm09-support-ticket",
        "title": "Submit a Support Request",
        "components": [
            {"componentType": "header",      "label": "Submit a Support Request", "widthIntent": "full", "section": "intro"},
            {"componentType": "text",        "label": "Name",         "widthIntent": "half", "section": "requester", "rowGroup": "identity", "validationIntent": _v(required=True, maxLength=80)},
            {"componentType": "email",       "label": "Email address","widthIntent": "half", "section": "requester", "rowGroup": "identity", "validationIntent": _v(required=True, email=True, maxLength=80)},
            {"componentType": "text",        "label": "Order/reference number (optional)", "widthIntent": "half", "section": "ticket", "rowGroup": "ref", "validationIntent": _v(maxLength=40)},
            {"componentType": "text",        "label": "Subject line", "widthIntent": "half", "section": "ticket", "rowGroup": "ref", "validationIntent": _v(required=True, maxLength=120)},
            {"componentType": "dropdown",    "label": "Issue category", "widthIntent": "half", "section": "ticket", "rowGroup": "category", "options": _opts("Billing", "Technical", "Account", "Shipping", "Other"), "validationIntent": _v(required=True)},
            {"componentType": "dropdown",    "label": "Priority",     "widthIntent": "half", "section": "ticket", "rowGroup": "category", "options": _opts("Low", "Medium", "High", "Urgent"),               "validationIntent": _v(required=True)},
            {"componentType": "textarea",    "label": "Describe your issue", "widthIntent": "full", "section": "details", "validationIntent": _v(required=True, maxLength=4000)},
            {"componentType": "file-upload", "label": "Attachments",  "widthIntent": "full", "section": "attachments"},
            {"componentType": "submit-button","label": "Submit Request","widthIntent": "compact", "actionAlignment": "center", "section": "action"},
        ],
    })


def _bm10_sales_lead() -> FormSemanticPlan:
    return FormSemanticPlan.model_validate({
        "semanticPlanVersion": "1.0",
        "formId": "bm10-sales-lead",
        "title": "Talk to Sales",
        "components": [
            {"componentType": "header",   "label": "Talk to Sales",   "widthIntent": "full", "section": "intro"},
            {"componentType": "text",     "label": "First name",      "widthIntent": "half", "section": "lead",    "rowGroup": "name",    "validationIntent": _v(required=True, maxLength=40)},
            {"componentType": "text",     "label": "Last name",       "widthIntent": "half", "section": "lead",    "rowGroup": "name",    "validationIntent": _v(required=True, maxLength=40)},
            {"componentType": "email",    "label": "Work email",      "widthIntent": "half", "section": "lead",    "rowGroup": "contact", "validationIntent": _v(required=True, email=True, maxLength=80)},
            {"componentType": "phone",    "label": "Phone number",    "widthIntent": "half", "section": "lead",    "rowGroup": "contact", "validationIntent": _v(phone=True, maxLength=20)},
            {"componentType": "text",     "label": "Company name",    "widthIntent": "half", "section": "company", "rowGroup": "co",      "validationIntent": _v(required=True, maxLength=120)},
            {"componentType": "dropdown", "label": "Company size",    "widthIntent": "half", "section": "company", "rowGroup": "co",      "options": _opts("1-10", "11-50", "51-200", "201-500", "500+"), "validationIntent": _v(required=True)},
            {"componentType": "rating",   "label": "How interested are you?", "widthIntent": "half", "section": "interest", "validationIntent": _v(min=1, max=5)},
            {"componentType": "textarea", "label": "Message",         "widthIntent": "full", "section": "message", "validationIntent": _v(maxLength=2000)},
            {"componentType": "terms",    "label": "I consent to receiving marketing communications", "widthIntent": "full", "section": "consent", "validationIntent": _v(required=True)},
            {"componentType": "submit-button", "label": "Get in Touch", "widthIntent": "compact", "actionAlignment": "center", "section": "action"},
        ],
    })


def _bm11_overpacked_row() -> FormSemanticPlan:
    """Stress: 4 ``half`` inputs in a single rowGroup. At target tier widths
    they won't all fit; the Phase 2 solver must shrink (and possibly reflow)
    rather than overlap or push the last column off-canvas."""
    return FormSemanticPlan.model_validate({
        "semanticPlanVersion": "1.0",
        "formId": "bm11-overpacked-row",
        "title": "Quad column stress",
        "components": [
            {"componentType": "text",  "label": "First name",  "widthIntent": "half", "section": "person", "rowGroup": "quad", "validationIntent": _v(required=True, maxLength=40)},
            {"componentType": "text",  "label": "Middle name", "widthIntent": "half", "section": "person", "rowGroup": "quad", "validationIntent": _v(maxLength=40)},
            {"componentType": "text",  "label": "Last name",   "widthIntent": "half", "section": "person", "rowGroup": "quad", "validationIntent": _v(required=True, maxLength=40)},
            {"componentType": "text",  "label": "Suffix",      "widthIntent": "half", "section": "person", "rowGroup": "quad", "validationIntent": _v(maxLength=10)},
            {"componentType": "email", "label": "Email",       "widthIntent": "half", "section": "person", "rowGroup": "contact", "validationIntent": _v(required=True, email=True, maxLength=80)},
            {"componentType": "phone", "label": "Phone",       "widthIntent": "half", "section": "person", "rowGroup": "contact", "validationIntent": _v(phone=True, maxLength=20)},
            {"componentType": "submit-button", "label": "Save", "widthIntent": "compact", "actionAlignment": "center", "section": "action"},
        ],
    })


def _bm12_long_labels_and_helptext() -> FormSemanticPlan:
    """Stress: very long header / paragraph text + verbose textarea help text.
    Catches height-measurement regressions and confirms full-row banner
    components still isolate to their own row even when paired with a
    same-section input that has rowGroup=None."""
    long_help = (
        "Please describe in as much detail as you can the issue you are "
        "experiencing, including the steps to reproduce, the expected "
        "behavior, the actual behavior, any error messages or screenshots, "
        "and the device, browser, and operating system you are using."
    )
    return FormSemanticPlan.model_validate({
        "semanticPlanVersion": "1.0",
        "formId": "bm12-long-labels",
        "title": "Bug report — please be thorough",
        "components": [
            {"componentType": "header",    "label": "Bug report — please be as thorough as possible so we can resolve it quickly", "widthIntent": "full", "section": "intro"},
            {"componentType": "paragraph", "label": "Tell us everything: what you tried, what happened, and what you expected. The more we know up front, the faster we can fix it.", "widthIntent": "full", "section": "intro"},
            {"componentType": "text",     "label": "Your name",   "widthIntent": "half", "section": "reporter", "rowGroup": "id", "validationIntent": _v(required=True, maxLength=80)},
            {"componentType": "email",    "label": "Email",       "widthIntent": "half", "section": "reporter", "rowGroup": "id", "validationIntent": _v(required=True, email=True, maxLength=80)},
            {"componentType": "textarea", "label": "Describe the issue", "placeholder": long_help, "widthIntent": "full", "section": "details", "validationIntent": _v(required=True, maxLength=8000)},
            {"componentType": "file-upload", "label": "Screenshots or logs", "widthIntent": "full", "section": "attachments"},
            {"componentType": "terms",    "label": "I confirm the information above is accurate", "widthIntent": "full", "section": "consent", "validationIntent": _v(required=True)},
            {"componentType": "submit-button", "label": "Submit Report", "widthIntent": "compact", "actionAlignment": "center", "section": "action"},
        ],
    })


def _bm13_wide_dropdowns_and_many_rows() -> FormSemanticPlan:
    """Stress: many sequential rowGroups with wide dropdowns + a paired
    rowGroup whose items both want ``full`` widthIntent (forces the solver
    into shrink, then potentially reflow)."""
    return FormSemanticPlan.model_validate({
        "semanticPlanVersion": "1.0",
        "formId": "bm13-wide-dropdowns",
        "title": "Logistics intake",
        "components": [
            {"componentType": "header",   "label": "Logistics intake",                                                "widthIntent": "full", "section": "intro"},
            {"componentType": "dropdown", "label": "Origin warehouse (long names like 'Sydney - Eastern Creek 03')",  "widthIntent": "full", "section": "route", "rowGroup": "warehouses", "options": _opts("Sydney - Eastern Creek 03", "Melbourne - Truganina 12", "Brisbane - Larapinta 04", "Perth - Kewdale 02"), "validationIntent": _v(required=True)},
            {"componentType": "dropdown", "label": "Destination warehouse (also long)",                               "widthIntent": "full", "section": "route", "rowGroup": "warehouses", "options": _opts("Adelaide - Wingfield 07", "Hobart - Glenorchy 01", "Darwin - Berrimah 05", "Canberra - Hume 03"), "validationIntent": _v(required=True)},
            {"componentType": "date",     "label": "Pickup date", "widthIntent": "half", "section": "schedule", "rowGroup": "dates"},
            {"componentType": "date",     "label": "Delivery date", "widthIntent": "half", "section": "schedule", "rowGroup": "dates"},
            {"componentType": "number",   "label": "Quantity",   "widthIntent": "compact", "section": "cargo", "rowGroup": "cargo", "validationIntent": _v(required=True, min=1, max=10000)},
            {"componentType": "dropdown", "label": "Unit",        "widthIntent": "compact", "section": "cargo", "rowGroup": "cargo", "options": _opts("Pallets", "Cartons", "Pieces"), "validationIntent": _v(required=True)},
            {"componentType": "number",   "label": "Weight (kg)","widthIntent": "compact", "section": "cargo", "rowGroup": "cargo", "validationIntent": _v(min=0, max=50000)},
            {"componentType": "textarea", "label": "Special instructions", "widthIntent": "full", "section": "notes", "validationIntent": _v(maxLength=2000)},
            {"componentType": "submit-button", "label": "Book Shipment",  "widthIntent": "compact", "actionAlignment": "center", "section": "action"},
        ],
    })


BENCHMARKS: List[Tuple[str, FormSemanticPlan]] = [
    ("01 — Party RSVP",              _bm01_party_rsvp()),
    ("02 — Contact + address",       _bm02_contact_address()),
    ("03 — Event registration",      _bm03_event_registration()),
    ("04 — Job application",         _bm04_job_application()),
    ("05 — Customer feedback",       _bm05_customer_feedback()),
    ("06 — Merchandise order",       _bm06_merchandise_order()),
    ("07 — Newsletter minimal",      _bm07_newsletter()),
    ("08 — Pre-order date/time",     _bm08_pre_order()),
    ("09 — Support ticket",          _bm09_support_ticket()),
    ("10 — Sales lead",              _bm10_sales_lead()),
    # Phase 2 stress prompts — exercise the solver under inputs the LLM
    # would emit when it over-packs a row, attaches verbose copy, or asks
    # for two full-width dropdowns side-by-side.
    ("11 — Over-packed row (stress)",       _bm11_overpacked_row()),
    ("12 — Long labels + helpText (stress)", _bm12_long_labels_and_helptext()),
    ("13 — Wide dropdowns x N rows (stress)", _bm13_wide_dropdowns_and_many_rows()),
]


# --- Reporting ---------------------------------------------------------------


@dataclass
class PromptResult:
    label: str
    input_count: int
    output_count: int
    canvas_w: int
    canvas_h: int
    summary: Dict[str, Any]
    components: List[Dict[str, Any]] = field(default_factory=list)
    overlaps: List[Tuple[str, str]] = field(default_factory=list)
    off_canvas: List[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return (
            self.output_count == self.input_count
            and not self.overlaps
            and not self.off_canvas
        )


def _detect_overlaps(items: List[Dict[str, Any]]) -> List[Tuple[str, str]]:
    overlaps: List[Tuple[str, str]] = []
    for i, a in enumerate(items):
        ay1 = a["position"]["y"]
        ay2 = ay1 + a["style"]["height"]
        ax1 = a["position"]["x"]
        ax2 = ax1 + a["style"]["width"]
        for b in items[i + 1:]:
            by1 = b["position"]["y"]
            by2 = by1 + b["style"]["height"]
            bx1 = b["position"]["x"]
            bx2 = bx1 + b["style"]["width"]
            if ay1 < by2 and by1 < ay2 and ax1 < bx2 and bx1 < ax2:
                overlaps.append((a["id"], b["id"]))
    return overlaps


def _detect_off_canvas(
    items: List[Dict[str, Any]], canvas_w: int, canvas_h: int
) -> List[str]:
    out: List[str] = []
    # content_right uses DEFAULT_MARGIN_X as the right margin so we surface
    # anything that touches or exceeds the editable content area.
    content_right = canvas_w - DEFAULT_MARGIN_X
    for c in items:
        right = c["position"]["x"] + c["style"]["width"]
        bottom = c["position"]["y"] + c["style"]["height"]
        if right > content_right or bottom > canvas_h or c["position"]["x"] < 0 or c["position"]["y"] < 0:
            out.append(c["id"])
    return out


def run_prompt(label: str, plan: FormSemanticPlan) -> PromptResult:
    definition, summary = compile_semantic_plan_to_definition(
        plan,
        runtime_context={"canvas": dict(CANVAS)},
        capability_policy_json=GOVERNANCE["capabilityPolicyJson"],
        width_policy_json=GOVERNANCE["widthClassPolicyJson"],
        capability_snapshot_json=GOVERNANCE["componentCapabilitySnapshotJson"],
        validation_contracts=GOVERNANCE["validationContracts"],
    )
    items = definition["pages"][0]["components"]
    canvas_w = definition["canvasSettings"]["width"]
    canvas_h = definition["canvasSettings"]["height"]
    return PromptResult(
        label=label,
        input_count=len(plan.components),
        output_count=len(items),
        canvas_w=canvas_w,
        canvas_h=canvas_h,
        summary=summary,
        components=items,
        overlaps=_detect_overlaps(items),
        off_canvas=_detect_off_canvas(items, canvas_w, canvas_h),
    )


def print_per_prompt(result: PromptResult, *, verbose: bool) -> None:
    status = "PASS" if result.passed else "FAIL"
    s = result.summary
    print(
        f"[{status}] {result.label}  "
        f"in={result.input_count} out={result.output_count}  "
        f"canvas={result.canvas_w}x{result.canvas_h}  "
        f"sections={s.get('sectionCount', 0)} rowGroups={s.get('rowGroupCount', 0)}  "
        f"fallbackCount={s.get('fallbackCount', 0)}  "
        f"submitClamped={s.get('submitButtonClamped', False)}"
    )
    if not result.passed:
        if result.overlaps:
            print(f"    overlaps ({len(result.overlaps)}):")
            for a, b in result.overlaps:
                print(f"      {a} <-> {b}")
        if result.off_canvas:
            print(f"    off-canvas: {', '.join(result.off_canvas)}")
        if result.output_count != result.input_count:
            print(
                f"    component count mismatch: input {result.input_count}, "
                f"output {result.output_count}"
            )
    if verbose:
        for c in result.components:
            x, y = c["position"]["x"], c["position"]["y"]
            w, h = c["style"]["width"], c["style"]["height"]
            print(
                f"    {c['type']:<14} y={y:>4} x={x:>4} w={w:>4} h={h:>3}"
                f"  right={x + w:>4}"
            )


def main(argv: Optional[List[str]] = None) -> int:
    argv = list(argv or sys.argv[1:])
    verbose = "--verbose" in argv or "-v" in argv

    print(f"Story 6.3.1 UAT spot-check — {len(BENCHMARKS)} benchmark prompts")
    print(f"Canvas: {CANVAS['width']} x {CANVAS['height']}, gridSize {CANVAS['gridSize']}")
    print()

    results: List[PromptResult] = []
    for label, plan in BENCHMARKS:
        result = run_prompt(label, plan)
        results.append(result)
        print_per_prompt(result, verbose=verbose)

    passed = sum(1 for r in results if r.passed)
    failed = len(results) - passed
    print()
    print(f"Summary: {passed}/{len(results)} prompts pass")
    if failed:
        print("Failed prompts:")
        for r in results:
            if not r.passed:
                reasons: List[str] = []
                if r.overlaps:
                    reasons.append(f"{len(r.overlaps)} overlap(s)")
                if r.off_canvas:
                    reasons.append(f"{len(r.off_canvas)} off-canvas")
                if r.output_count != r.input_count:
                    reasons.append("component count mismatch")
                print(f"  - {r.label}: {', '.join(reasons)}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
