"""
Story 6.3 benchmark harness: all 10 prompts from docs/stories/STORY-6.2-BENCHMARK-FORMS.md
with mocked LLM output. Asserts validator acceptance, expected component types, single-page rule.
"""

from __future__ import annotations

import json
from typing import Any, Dict, FrozenSet, List, Tuple

import pytest

from modules.form_ai import service

# --- builders ---

def _theme() -> Dict[str, str]:
    return {"primaryColor": "#0055FF", "backgroundColor": "#FFFFFF", "fontFamily": "Inter"}


def _form(canvas_h: int, components: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "schemaVersion": "1.0",
        "formId": "story-63-benchmark",
        "theme": _theme(),
        "canvasSettings": {"width": 1920, "height": canvas_h, "gridSize": 8},
        "pages": [{"id": "page-1", "title": "Benchmark", "components": components}],
    }


def _c(
    idx: int,
    ctype: str,
    y: int,
    props: Dict[str, Any],
    w: int = 1840,
    h: int = 120,
) -> Dict[str, Any]:
    return {
        "id": f"bm-c{idx}",
        "type": ctype,
        "props": props,
        "position": {"x": 40, "y": y},
        "style": {"width": w, "height": h},
    }


def _yseq(start: int, n: int, step: int = 140) -> List[int]:
    return [start + i * step for i in range(n)]


# --- benchmark fixtures (ideal/smoothed JSON) ---

def _bm01() -> Dict[str, Any]:
    ys = _yseq(40, 6)
    radio_opts = [{"label": "Yes", "value": "yes"}, {"label": "No", "value": "no"}]
    return _form(
        1100,
        [
            _c(0, "text", ys[0], {"label": "Full Name", "required": True}),
            _c(1, "phone", ys[1], {"label": "Phone Number", "required": False}),
            _c(2, "email", ys[2], {"label": "Email", "required": True}),
            _c(3, "radio", ys[3], {"label": "Will you be attending?", "required": True, "options": radio_opts}),
            _c(4, "number", ys[4], {"label": "How many guests?", "required": False}),
            _c(5, "submit-button", ys[5], {"buttonText": "Submit", "buttonAction": "submit"}, h=81, w=220),
        ],
    )


def _bm02() -> Dict[str, Any]:
    ys = _yseq(40, 8)
    return _form(
        1200,
        [
            _c(0, "text", ys[0], {"label": "First Name", "required": True}),
            _c(1, "text", ys[1], {"label": "Last Name", "required": True}),
            _c(2, "address", ys[2], {"label": "Address", "required": False}),
            _c(3, "phone", ys[3], {"label": "Phone", "required": False}),
            _c(4, "email", ys[4], {"label": "Email", "required": True}),
            _c(5, "text", ys[5], {"label": "Company Name", "required": False}),
            _c(6, "textarea", ys[6], {"label": "Comments or Questions", "required": False}, h=140),
            _c(7, "submit-button", ys[7], {"buttonText": "Submit", "buttonAction": "submit"}, h=81, w=220),
        ],
    )


def _bm03() -> Dict[str, Any]:
    countries = [
        {"label": "Australia", "value": "au"},
        {"label": "United States", "value": "us"},
        {"label": "United Kingdom", "value": "uk"},
        {"label": "Canada", "value": "ca"},
        {"label": "New Zealand", "value": "nz"},
        {"label": "Other", "value": "other"},
    ]
    ys = _yseq(40, 8)
    return _form(
        1200,
        [
            _c(0, "text", ys[0], {"label": "First Name", "required": True}),
            _c(1, "text", ys[1], {"label": "Last Name", "required": True}),
            _c(2, "email", ys[2], {"label": "Email Address", "required": True}),
            _c(3, "phone", ys[3], {"label": "Phone Number", "required": True}),
            _c(4, "text", ys[4], {"label": "Company", "required": True}),
            _c(5, "text", ys[5], {"label": "Job Title", "required": True}),
            _c(6, "dropdown", ys[6], {"label": "Country", "required": True, "options": countries}),
            _c(7, "submit-button", ys[7], {"buttonText": "Register", "buttonAction": "submit"}, h=81, w=220),
        ],
    )


def _bm04() -> Dict[str, Any]:
    hear = [
        {"label": "Company Website", "value": "web"},
        {"label": "LinkedIn", "value": "li"},
        {"label": "Facebook", "value": "fb"},
        {"label": "Referral", "value": "ref"},
        {"label": "Other", "value": "other"},
    ]
    ys = _yseq(40, 11, 130)
    return _form(
        1500,
        [
            _c(0, "text", ys[0], {"label": "First Name", "required": True}),
            _c(1, "text", ys[1], {"label": "Last Name", "required": True}),
            _c(2, "email", ys[2], {"label": "Email", "required": True}),
            _c(3, "phone", ys[3], {"label": "Phone", "required": False}),
            _c(4, "text", ys[4], {"label": "Location", "required": False}),
            _c(5, "url", ys[5], {"label": "LinkedIn Profile", "required": False}),
            _c(6, "textarea", ys[6], {"label": "Why are you interested?", "required": True}, h=140),
            _c(
                7,
                "file-upload",
                ys[7],
                {"label": "Upload Resume", "required": True, "acceptedFileTypes": ".pdf,.doc,.docx"},
                h=140,
            ),
            _c(8, "dropdown", ys[8], {"label": "How did you hear about us?", "required": False, "options": hear}),
            _c(9, "terms", ys[9], {"label": "I agree to the privacy policy", "required": True}),
            _c(10, "submit-button", ys[10], {"buttonText": "Apply Now", "buttonAction": "submit"}, h=81, w=220),
        ],
    )


def _bm05() -> Dict[str, Any]:
    find_us = [
        {"label": "Search Engine", "value": "se"},
        {"label": "Social Media", "value": "sm"},
        {"label": "Friend", "value": "fr"},
        {"label": "Advertisement", "value": "ad"},
        {"label": "Other", "value": "o"},
    ]
    ys = _yseq(40, 7, 135)
    return _form(
        1100,
        [
            _c(0, "header", ys[0], {"label": "Customer Feedback"}, h=52),
            _c(
                1,
                "rating",
                ys[1],
                {"label": "Overall Experience", "required": True, "ratingMax": 5, "ratingStyle": "stars"},
                h=96,
            ),
            _c(
                2,
                "rating",
                ys[2],
                {
                    "label": "Recommend Us",
                    "required": True,
                    "ratingMax": 10,
                    "ratingStyle": "numbers",
                    "ratingLabels": {"low": "Not likely", "high": "Very likely"},
                },
                h=120,
            ),
            _c(3, "textarea", ys[3], {"label": "What did you like most?", "required": False}, h=140),
            _c(4, "textarea", ys[4], {"label": "What could we improve?", "required": False}, h=140),
            _c(5, "dropdown", ys[5], {"label": "How did you find us?", "required": False, "options": find_us}),
            _c(6, "submit-button", ys[6], {"buttonText": "Submit", "buttonAction": "submit"}, h=81, w=220),
        ],
    )


def _bm06() -> Dict[str, Any]:
    opts = [
        {"label": "Facebook", "value": "fb"},
        {"label": "Instagram", "value": "ig"},
        {"label": "Twitter", "value": "tw"},
        {"label": "YouTube", "value": "yt"},
        {"label": "Television", "value": "tv"},
        {"label": "Internet Search", "value": "is"},
        {"label": "Referral", "value": "rf"},
        {"label": "Other", "value": "ot"},
    ]
    ys = _yseq(40, 8, 145)
    return _form(
        1300,
        [
            _c(0, "text", ys[0], {"label": "First Name", "required": True}),
            _c(1, "text", ys[1], {"label": "Last Name", "required": True}),
            _c(2, "email", ys[2], {"label": "Email", "required": True}),
            _c(3, "phone", ys[3], {"label": "Phone Number", "required": False}),
            _c(4, "address", ys[4], {"label": "Shipping Address", "required": True}),
            _c(5, "checkbox", ys[5], {"label": "How did you hear about us?", "required": False, "options": opts}, h=300),
            _c(6, "textarea", ys[6], {"label": "Special Instructions", "required": False}, h=140),
            _c(7, "submit-button", ys[7], {"buttonText": "Place Order", "buttonAction": "submit"}, h=81, w=220),
        ],
    )


def _bm07() -> Dict[str, Any]:
    ys = _yseq(40, 4, 130)
    return _form(
        700,
        [
            _c(0, "header", ys[0], {"label": "Stay in the loop"}, h=52),
            _c(1, "paragraph", ys[1], {"text": "Get the latest updates delivered to your inbox."}, h=88),
            _c(2, "email", ys[2], {"label": "Email Address", "required": True}),
            _c(3, "submit-button", ys[3], {"buttonText": "Subscribe", "buttonAction": "submit"}, h=81, w=220),
        ],
    )


def _bm08() -> Dict[str, Any]:
    ys = _yseq(40, 10, 135)
    return _form(
        1500,
        [
            _c(0, "text", ys[0], {"label": "First Name", "required": True}),
            _c(1, "text", ys[1], {"label": "Middle Name", "required": False}),
            _c(2, "text", ys[2], {"label": "Last Name", "required": True}),
            _c(3, "phone", ys[3], {"label": "Phone Number", "required": True}),
            _c(4, "email", ys[4], {"label": "Email", "required": True}),
            _c(5, "address", ys[5], {"label": "Delivery Address", "required": True}),
            _c(6, "date", ys[6], {"label": "Preferred Date", "required": True, "dateType": "date"}),
            _c(7, "date", ys[7], {"label": "Preferred Time", "required": False, "dateType": "time"}),
            _c(8, "textarea", ys[8], {"label": "Special Delivery Notes", "required": False}, h=140),
            _c(9, "submit-button", ys[9], {"buttonText": "Place Pre-Order", "buttonAction": "submit"}, h=81, w=220),
        ],
    )


def _bm09() -> Dict[str, Any]:
    cat = [
        {"label": "Billing", "value": "b"},
        {"label": "Technical", "value": "t"},
        {"label": "Account", "value": "a"},
        {"label": "Shipping", "value": "s"},
        {"label": "Other", "value": "o"},
    ]
    pri = [
        {"label": "Low", "value": "l"},
        {"label": "Medium", "value": "m"},
        {"label": "High", "value": "h"},
        {"label": "Urgent", "value": "u"},
    ]
    ys = _yseq(40, 10, 135)
    return _form(
        1500,
        [
            _c(0, "header", ys[0], {"label": "Submit a Support Request"}, h=52),
            _c(1, "text", ys[1], {"label": "Your Name", "required": True}),
            _c(2, "email", ys[2], {"label": "Email Address", "required": True}),
            _c(3, "text", ys[3], {"label": "Order / Reference Number", "required": False}),
            _c(4, "dropdown", ys[4], {"label": "Issue Category", "required": True, "options": cat}),
            _c(5, "dropdown", ys[5], {"label": "Priority", "required": True, "options": pri}),
            _c(6, "text", ys[6], {"label": "Subject", "required": True}),
            _c(7, "textarea", ys[7], {"label": "Describe Your Issue", "required": True}, h=160),
            _c(
                8,
                "file-upload",
                ys[8],
                {"label": "Attachments", "required": False, "acceptedFileTypes": ".pdf,.jpg,.png"},
                h=140,
            ),
            _c(9, "submit-button", ys[9], {"buttonText": "Submit Request", "buttonAction": "submit"}, h=81, w=220),
        ],
    )


def _bm10() -> Dict[str, Any]:
    sizes = [
        {"label": "1-10", "value": "1"},
        {"label": "11-50", "value": "2"},
        {"label": "51-200", "value": "3"},
        {"label": "201-500", "value": "4"},
        {"label": "500+", "value": "5"},
    ]
    ys = _yseq(40, 11, 135)
    return _form(
        1650,
        [
            _c(0, "header", ys[0], {"label": "Talk to Sales"}, h=52),
            _c(1, "text", ys[1], {"label": "First Name", "required": True}),
            _c(2, "text", ys[2], {"label": "Last Name", "required": True}),
            _c(3, "email", ys[3], {"label": "Work Email", "required": True}),
            _c(4, "phone", ys[4], {"label": "Phone Number", "required": False}),
            _c(5, "text", ys[5], {"label": "Company Name", "required": True}),
            _c(6, "dropdown", ys[6], {"label": "Company Size", "required": True, "options": sizes}),
            _c(
                7,
                "rating",
                ys[7],
                {"label": "How interested are you?", "required": False, "ratingMax": 5, "ratingStyle": "stars"},
                h=96,
            ),
            _c(8, "textarea", ys[8], {"label": "Message", "required": False}, h=140),
            _c(
                9,
                "terms",
                ys[9],
                {"label": "I consent to receiving marketing communications", "required": True},
            ),
            _c(10, "submit-button", ys[10], {"buttonText": "Get in Touch", "buttonAction": "submit"}, h=81, w=220),
        ],
    )


BENCHMARK_CASES: List[Tuple[int, str, Dict[str, Any], FrozenSet[str]]] = [
    (
        1,
        (
            "Create an RSVP form for a party. I need the guest's full name, phone, email, "
            "Yes/No radio, guest count number, and submit."
        ),
        _bm01(),
        frozenset({"text", "phone", "email", "radio", "number", "submit-button"}),
    ),
    (
        2,
        (
            "Create a contact form with first and last name, address, phone, email required, "
            "company, comments textarea, submit button."
        ),
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
        (
            "Create a job application form with resume file upload, url, terms, dropdown, "
            "textarea and Apply Now button."
        ),
        _bm04(),
        frozenset({"text", "email", "phone", "url", "textarea", "file-upload", "dropdown", "terms", "submit-button"}),
    ),
    (
        5,
        (
            "Build customer feedback with heading Customer Feedback, two ratings, textareas, "
            "dropdown and submit."
        ),
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


@pytest.mark.parametrize("bm_id,prompt,fixture,expected_types", BENCHMARK_CASES, ids=[f"bm{c[0]:02d}" for c in BENCHMARK_CASES])
def test_story_63_benchmark_passes_validator_and_types(
    monkeypatch: pytest.MonkeyPatch,
    bm_id: int,
    prompt: str,
    fixture: Dict[str, Any],
    expected_types: FrozenSet[str],
) -> None:
    monkeypatch.setattr(
        service,
        "_request_chatgpt_completion",
        lambda _messages, model_override=None: json.dumps(fixture),
    )

    result = service.generate_form_definition(prompt, runtime_context=None)
    assert result.status == "completed", (bm_id, result.trace.terminalReason, result.userMessage)
    assert result.definitionJSON is not None
    pages = result.definitionJSON.get("pages")
    assert isinstance(pages, list) and len(pages) == 1

    def walk_types(items: List[Any], acc: List[str]) -> None:
        for item in items:
            if not isinstance(item, dict):
                continue
            t = str(item.get("type", "")).strip()
            if t:
                acc.append(t)
            ch = item.get("children")
            if isinstance(ch, list):
                walk_types(ch, acc)

    comps = pages[0].get("components")
    assert isinstance(comps, list)
    found: List[str] = []
    walk_types(comps, found)
    assert expected_types == frozenset(found), (bm_id, found)
