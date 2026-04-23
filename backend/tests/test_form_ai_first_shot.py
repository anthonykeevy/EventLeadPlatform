import json

from modules.form_ai import service
from modules.form_ai.first_shot_scoring import score_goal_coverage, score_layout


def _valid_definition() -> dict:
    return {
        "schemaVersion": "1.0",
        "formId": "t",
        "theme": {"primaryColor": "#0055FF", "backgroundColor": "#FFFFFF", "fontFamily": "Inter"},
        "canvasSettings": {"width": 500, "height": 700, "gridSize": 8},
        "pages": [
            {
                "id": "page-1",
                "title": "Page 1",
                "components": [
                    {
                        "id": "name-field",
                        "type": "text",
                        "props": {"label": "Full Name"},
                        "position": {"x": 20, "y": 20},
                        "style": {"width": 460, "height": 72},
                    }
                ],
            }
        ],
    }


def test_max_correction_zero_issues_only_one_provider_call(monkeypatch):
    """With max_system_correction_attempts=0, the provider must be called
    exactly once and no LLM-correction loop kicks in.

    Story 6.3.1 (failure-mode separation) note: a legacy-shaped definition
    with a negative position is now CORRECTED by the deterministic compiler,
    so the same scenario that used to fail with first-shot-invalid now
    succeeds. To preserve the test's original intent ("cap=0 means one call
    only, even when the response is broken"), use a non-JSON response that
    fails the json-parse phase deterministically.
    """
    calls: list[int] = []

    def fake(messages, model_override=None, **kwargs):
        calls.append(1)
        return "this is not json at all"

    monkeypatch.setattr(service, "_request_chatgpt_completion", fake)
    result = service.generate_form_definition(
        "test prompt", max_system_correction_attempts=0
    )

    assert len(calls) == 1
    assert result.trace.attemptCount == 1
    assert result.trace.terminalReason == "json-parse-failed"
    assert result.trace.failureClass == "llm-fault"
    assert result.status == "failed"


def test_system_prompt_addendum_in_system_message(monkeypatch):
    valid = _valid_definition()
    captured: list[list] = []

    def fake(messages, model_override=None, **kwargs):
        captured.append(messages)
        return json.dumps(valid)

    monkeypatch.setattr(service, "_request_chatgpt_completion", fake)
    result = service.generate_form_definition(
        "test prompt",
        max_system_correction_attempts=0,
        system_prompt_addendum="XYZZY_ADDENDUM_MARKER",
    )

    assert result.status == "completed"
    assert len(captured) == 1
    system_content = captured[0][0]["content"]
    assert "XYZZY_ADDENDUM_MARKER" in system_content
    assert "test prompt" in captured[0][1]["content"]


def test_score_layout_penalizes_collisions():
    assert score_layout(0, 0, 0) == 100.0
    assert score_layout(2, 0, 0) == 90.0
    assert score_layout(0, 1, 0) == 92.0


def test_score_goal_coverage_registration_prompt():
    definition = {
        "schemaVersion": "1.0",
        "formId": "x",
        "theme": {},
        "canvasSettings": {"width": 1920, "height": 980, "gridSize": 8},
        "pages": [
            {
                "id": "p1",
                "title": "T",
                "components": [
                    {
                        "id": "fn",
                        "type": "first-name",
                        "props": {"label": "First name"},
                        "position": {"x": 20, "y": 20},
                        "style": {"width": 400, "height": 100},
                    },
                    {
                        "id": "ln",
                        "type": "text",
                        "props": {"label": "Last name"},
                        "position": {"x": 20, "y": 140},
                        "style": {"width": 400, "height": 100},
                    },
                    {
                        "id": "em",
                        "type": "email",
                        "props": {"label": "Email"},
                        "position": {"x": 20, "y": 260},
                        "style": {"width": 400, "height": 100},
                    },
                    {
                        "id": "ph",
                        "type": "phone",
                        "props": {"label": "Phone"},
                        "position": {"x": 20, "y": 380},
                        "style": {"width": 400, "height": 100},
                    },
                    {
                        "id": "co",
                        "type": "text",
                        "props": {"label": "Company name"},
                        "position": {"x": 20, "y": 500},
                        "style": {"width": 400, "height": 100},
                    },
                    {
                        "id": "jt",
                        "type": "text",
                        "props": {"label": "Job title"},
                        "position": {"x": 20, "y": 620},
                        "style": {"width": 400, "height": 100},
                    },
                    {
                        "id": "ct",
                        "type": "dropdown",
                        "props": {
                            "label": "Country",
                            "options": [
                                {"label": "Australia", "value": "au"},
                                {"label": "United States", "value": "us"},
                                {"label": "United Kingdom", "value": "uk"},
                                {"label": "Canada", "value": "ca"},
                                {"label": "New Zealand", "value": "nz"},
                                {"label": "Other", "value": "other"},
                            ],
                        },
                        "position": {"x": 20, "y": 740},
                        "style": {"width": 400, "height": 100},
                    },
                    {
                        "id": "sub",
                        "type": "submit-button",
                        "props": {"label": "Register"},
                        "position": {"x": 20, "y": 860},
                        "style": {"width": 220, "height": 81},
                    },
                ],
            }
        ],
    }
    prompt = (
        "Build a registration form for a tech conference. Include first name, last name, "
        "email address, phone number, company name, job title, and a country dropdown with "
        "these options: Australia, United States, United Kingdom, Canada, New Zealand, Other. "
        "Add a submit button labeled 'Register'."
    )
    score, checks = score_goal_coverage(definition, prompt)
    assert score == 100.0
    assert all(c["ok"] for c in checks if c.get("id") != "_note")
