"""
Story 6.3.1 benchmark harness: all 10 prompts from
``docs/stories/STORY-6.3-BENCHMARK-PROMPTS-AND-OUTCOMES.md`` run end-to-end
through the deterministic compiler with mocked LLM output.

History note: pre-Story-6.3.1, the LLM mock returned a full
``DefinitionJSON`` (with x/y/style stamped by the model) and the test
asserted validator acceptance. With the deterministic-grid compiler the
LLM now returns a ``FormSemanticPlan`` (no coordinates) and the compiler
owns geometry. Each ``_bm0X`` fixture has been rewritten as a semantic
plan; the asserted contract is:

* ``status == "completed"`` (compiler accepted the plan)
* single-page rule still holds
* the rendered component-type set is consistent with the plan, after the
  heading-filter post-process which strips ``header``/``paragraph``
  intents whose label is a placeholder OR whose owning prompt does not
  mention any heading keyword (``header``, ``heading``, ``title``, etc.).
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict, FrozenSet, List, Tuple

import pytest

from modules.form_ai import service


# --- builders ---------------------------------------------------------------

def _plan(components: List[Dict[str, Any]], *, form_id: str = "story-631-benchmark", title: str = "Benchmark") -> Dict[str, Any]:
    return {
        "semanticPlanVersion": "1.0",
        "formId": form_id,
        "title": title,
        "components": components,
    }


def _i(component_type: str, label: str, *, intent: str = "full", required: bool = False, **extra: Any) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "componentType": component_type,
        "label": label,
        "widthIntent": intent,
    }
    if required:
        out["validationIntent"] = {"required": True}
    out.update(extra)
    return out


def _opts(*pairs: Tuple[str, str]) -> List[Dict[str, str]]:
    return [{"label": label, "value": value} for label, value in pairs]


# --- semantic-plan fixtures (one per benchmark prompt) ---------------------

def _bm01() -> Dict[str, Any]:
    radio_opts = _opts(("Yes", "yes"), ("No", "no"))
    return _plan(
        [
            _i("text", "Full Name", required=True),
            _i("phone", "Phone Number", intent="half"),
            _i("email", "Email", intent="half", required=True),
            _i("radio", "Will you be attending?", required=True, options=radio_opts),
            _i("number", "How many guests?", intent="compact"),
            _i("submit-button", "Submit", intent="compact"),
        ],
    )


def _bm02() -> Dict[str, Any]:
    return _plan(
        [
            _i("text", "First Name", intent="half", required=True),
            _i("text", "Last Name", intent="half", required=True),
            _i("address", "Address"),
            _i("phone", "Phone", intent="half"),
            _i("email", "Email", intent="half", required=True),
            _i("text", "Company Name"),
            _i("textarea", "Comments or Questions"),
            _i("submit-button", "Submit", intent="compact"),
        ],
    )


def _bm03() -> Dict[str, Any]:
    countries = _opts(
        ("Australia", "au"), ("United States", "us"), ("United Kingdom", "uk"),
        ("Canada", "ca"), ("New Zealand", "nz"), ("Other", "other"),
    )
    return _plan(
        [
            _i("text", "First Name", intent="half", required=True),
            _i("text", "Last Name", intent="half", required=True),
            _i("email", "Email Address", intent="half", required=True),
            _i("phone", "Phone Number", intent="half", required=True),
            _i("text", "Company", intent="half", required=True),
            _i("text", "Job Title", intent="half", required=True),
            _i("dropdown", "Country", required=True, options=countries),
            _i("submit-button", "Register", intent="compact"),
        ],
    )


def _bm04() -> Dict[str, Any]:
    hear = _opts(
        ("Company Website", "web"), ("LinkedIn", "li"), ("Facebook", "fb"),
        ("Referral", "ref"), ("Other", "other"),
    )
    return _plan(
        [
            _i("text", "First Name", intent="half", required=True),
            _i("text", "Last Name", intent="half", required=True),
            _i("email", "Email", intent="half", required=True),
            _i("phone", "Phone", intent="half"),
            _i("text", "Location"),
            _i("url", "LinkedIn Profile"),
            _i("textarea", "Why are you interested?", required=True),
            _i("file-upload", "Upload Resume", required=True, acceptedFileTypes=".pdf,.doc,.docx"),
            _i("dropdown", "How did you hear about us?", options=hear),
            _i("terms", "I agree to the privacy policy", required=True),
            _i("submit-button", "Apply Now", intent="compact"),
        ],
    )


def _bm05() -> Dict[str, Any]:
    find_us = _opts(
        ("Search Engine", "se"), ("Social Media", "sm"), ("Friend", "fr"),
        ("Advertisement", "ad"), ("Other", "o"),
    )
    return _plan(
        [
            _i("header", "Customer Feedback"),
            _i("rating", "Overall Experience", intent="half", required=True, ratingMax=5, ratingStyle="stars"),
            _i("rating", "Recommend Us", intent="half", required=True, ratingMax=10, ratingStyle="numbers",
               ratingLabels={"low": "Not likely", "high": "Very likely"}),
            _i("textarea", "What did you like most?"),
            _i("textarea", "What could we improve?"),
            _i("dropdown", "How did you find us?", options=find_us),
            _i("submit-button", "Submit", intent="compact"),
        ],
    )


def _bm06() -> Dict[str, Any]:
    opts = _opts(
        ("Facebook", "fb"), ("Instagram", "ig"), ("Twitter", "tw"),
        ("YouTube", "yt"), ("Television", "tv"), ("Internet Search", "is"),
        ("Referral", "rf"), ("Other", "ot"),
    )
    return _plan(
        [
            _i("text", "First Name", intent="half", required=True),
            _i("text", "Last Name", intent="half", required=True),
            _i("email", "Email", intent="half", required=True),
            _i("phone", "Phone Number", intent="half"),
            _i("address", "Shipping Address", required=True),
            _i("checkbox", "How did you hear about us?", options=opts),
            _i("textarea", "Special Instructions"),
            _i("submit-button", "Place Order", intent="compact"),
        ],
    )


def _bm07() -> Dict[str, Any]:
    # Prompt explicitly mentions "heading" and "paragraph" so heading filter keeps both.
    return _plan(
        [
            _i("header", "Stay in the loop"),
            _i("paragraph", "Get the latest updates delivered to your inbox."),
            _i("email", "Email Address", required=True),
            _i("submit-button", "Subscribe", intent="compact"),
        ],
    )


def _bm08() -> Dict[str, Any]:
    return _plan(
        [
            _i("text", "First Name", intent="half", required=True),
            _i("text", "Middle Name", intent="half"),
            _i("text", "Last Name", intent="half", required=True),
            _i("phone", "Phone Number", intent="half", required=True),
            _i("email", "Email", intent="half", required=True),
            _i("address", "Delivery Address", required=True),
            _i("date", "Preferred Date", intent="half", required=True, dateType="date"),
            _i("date", "Preferred Time", intent="half", dateType="time"),
            _i("textarea", "Special Delivery Notes"),
            _i("submit-button", "Place Pre-Order", intent="compact"),
        ],
    )


def _bm09() -> Dict[str, Any]:
    cat = _opts(("Billing", "b"), ("Technical", "t"), ("Account", "a"), ("Shipping", "s"), ("Other", "o"))
    pri = _opts(("Low", "l"), ("Medium", "m"), ("High", "h"), ("Urgent", "u"))
    return _plan(
        [
            _i("header", "Submit a Support Request"),
            _i("text", "Your Name", intent="half", required=True),
            _i("email", "Email Address", intent="half", required=True),
            _i("text", "Order / Reference Number"),
            _i("dropdown", "Issue Category", intent="half", required=True, options=cat),
            _i("dropdown", "Priority", intent="half", required=True, options=pri),
            _i("text", "Subject", required=True),
            _i("textarea", "Describe Your Issue", required=True),
            _i("file-upload", "Attachments", acceptedFileTypes=".pdf,.jpg,.png"),
            _i("submit-button", "Submit Request", intent="compact"),
        ],
    )


def _bm10() -> Dict[str, Any]:
    sizes = _opts(
        ("1-10", "1"), ("11-50", "2"), ("51-200", "3"),
        ("201-500", "4"), ("500+", "5"),
    )
    return _plan(
        [
            _i("header", "Talk to Sales"),
            _i("text", "First Name", intent="half", required=True),
            _i("text", "Last Name", intent="half", required=True),
            _i("email", "Work Email", intent="half", required=True),
            _i("phone", "Phone Number", intent="half"),
            _i("text", "Company Name", required=True),
            _i("dropdown", "Company Size", intent="half", required=True, options=sizes),
            _i("rating", "How interested are you?", intent="half", ratingMax=5, ratingStyle="stars"),
            _i("textarea", "Message"),
            _i("terms", "I consent to receiving marketing communications", required=True),
            _i("submit-button", "Get in Touch", intent="compact"),
        ],
    )


# Each tuple: (id, prompt, semantic plan, expected component types after compile).
# ``expected_types`` is the *plan* set minus heading/paragraph intents that the
# heading-filter strips when the prompt has no heading-keyword (see
# ``_prompt_requests_heading``).
BENCHMARK_CASES: List[Tuple[int, str, Dict[str, Any], FrozenSet[str]]] = [
    (
        1,
        "Create an RSVP form for a party. I need the guest's full name, phone, email, "
        "Yes/No radio, guest count number, and submit.",
        _bm01(),
        frozenset({"text", "phone", "email", "radio", "number", "submit-button"}),
    ),
    (
        2,
        "Create a contact form with first and last name, address, phone, email required, "
        "company, comments textarea, submit button.",
        _bm02(),
        frozenset({"text", "address", "phone", "email", "textarea", "submit-button"}),
    ),
    (
        3,
        "Build a registration form for a tech conference with country dropdown and Register submit.",
        _bm03(),
        frozenset({"text", "email", "phone", "dropdown", "submit-button"}),
    ),
    (
        4,
        "Create a job application form with resume file upload, url, terms, dropdown, "
        "textarea and Apply Now button.",
        _bm04(),
        frozenset({"text", "email", "phone", "url", "textarea", "file-upload", "dropdown", "terms", "submit-button"}),
    ),
    (
        5,
        "Build customer feedback with heading Customer Feedback, two ratings, textareas, "
        "dropdown and submit.",
        _bm05(),
        frozenset({"header", "rating", "textarea", "dropdown", "submit-button"}),
    ),
    (
        6,
        "Create merchandise order form with checkbox channel options, address, Place Order button.",
        _bm06(),
        frozenset({"text", "email", "phone", "address", "checkbox", "textarea", "submit-button"}),
    ),
    (
        7,
        "Create minimal newsletter signup with heading Stay in the loop, paragraph, email, Subscribe.",
        _bm07(),
        frozenset({"header", "paragraph", "email", "submit-button"}),
    ),
    (
        8,
        "Create pre-order form with three name fields, delivery date and time pickers, Place Pre-Order.",
        _bm08(),
        frozenset({"text", "phone", "email", "address", "date", "textarea", "submit-button"}),
    ),
    (
        9,
        "Create support ticket form with heading, two dropdowns, file upload attachments, Submit Request.",
        _bm09(),
        frozenset({"header", "text", "email", "dropdown", "textarea", "file-upload", "submit-button"}),
    ),
    (
        10,
        "Build sales lead form with heading Talk to Sales, rating, terms, Get in Touch submit.",
        _bm10(),
        frozenset({"header", "text", "email", "phone", "dropdown", "rating", "textarea", "terms", "submit-button"}),
    ),
]


def _walk_types(items: List[Any], acc: List[str]) -> None:
    for item in items:
        if not isinstance(item, dict):
            continue
        t = str(item.get("type", "")).strip()
        if t:
            acc.append(t)
        ch = item.get("children")
        if isinstance(ch, list):
            _walk_types(ch, acc)


@pytest.mark.parametrize(
    "bm_id,prompt,plan,expected_types",
    BENCHMARK_CASES,
    ids=[f"bm{c[0]:02d}" for c in BENCHMARK_CASES],
)
def test_story_631_benchmark_compiles_semantic_plan_into_valid_definition(
    monkeypatch: pytest.MonkeyPatch,
    bm_id: int,
    prompt: str,
    plan: Dict[str, Any],
    expected_types: FrozenSet[str],
) -> None:
    monkeypatch.setattr(
        service,
        "_request_chatgpt_completion",
        lambda *_args, **_kwargs: json.dumps(plan),
    )

    result = service.generate_form_definition(
        prompt,
        runtime_context={"canvas": {"width": 1920, "height": 980, "gridSize": 8}},
        max_system_correction_attempts=0,
        db_session=None,
    )

    assert result.status == "completed", (
        bm_id, result.trace.terminalReason, result.userMessage,
    )
    assert result.definitionJSON is not None
    assert result.trace.compilerMode == "deterministic-grid"

    pages = result.definitionJSON.get("pages")
    assert isinstance(pages, list) and len(pages) == 1, (bm_id, pages)

    components = pages[0].get("components")
    assert isinstance(components, list)
    found: List[str] = []
    _walk_types(components, found)
    assert frozenset(found) == expected_types, (bm_id, found)

    # Compiler is the single source of geometry; no component should have a
    # negative position or stray off the bottom of the (possibly grown) canvas.
    canvas = result.definitionJSON["canvasSettings"]
    canvas_h = canvas["height"]
    canvas_w = canvas["width"]
    for component in components:
        x = component["position"]["x"]
        y = component["position"]["y"]
        w = component["style"]["width"]
        h = component["style"]["height"]
        assert x >= 0 and y >= 0, (bm_id, component["id"], x, y)
        assert x + w <= canvas_w + 1, (bm_id, component["id"], x + w, canvas_w)
        assert y + h <= canvas_h + 1, (bm_id, component["id"], y + h, canvas_h)


def test_story_631_benchmark_prompt_keywords_match_expected_heading_policy():
    """Documents the contract behind ``expected_types``: any benchmark
    case that *includes* ``header``/``paragraph`` in expected types must
    have a heading-keyword in its prompt; cases that *exclude* them must
    not. If this drifts, the heading filter or the keyword list moved.
    """
    keyword_re = re.compile(r"\b(header|heading|title|banner|intro|introduction)\b", re.IGNORECASE)
    for bm_id, prompt, _plan_payload, expected_types in BENCHMARK_CASES:
        wants_heading = bool(keyword_re.search(prompt))
        has_heading_in_expected = "header" in expected_types or "paragraph" in expected_types
        assert wants_heading == has_heading_in_expected, (bm_id, prompt, expected_types)
