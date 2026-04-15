"""Form definition accepts optional aiAgentSettings (Story 6.3)."""

from schemas.form_definition import FormDefinition


def _minimal_pages():
    return [
        {
            "id": "page-1",
            "title": "P",
            "components": [
                {
                    "id": "a",
                    "type": "text",
                    "props": {"label": "x"},
                    "position": {"x": 0, "y": 0},
                }
            ],
        }
    ]


def test_form_definition_accepts_ai_agent_settings():
    raw = {
        "schemaVersion": "1.0",
        "formId": "402",
        "theme": {"primaryColor": "#000", "backgroundColor": "#fff", "fontFamily": "Inter"},
        "pages": _minimal_pages(),
        "aiAgentSettings": {
            "lastPrompt": "Create an RSVP form.",
            "includeEventInformation": True,
        },
    }
    m = FormDefinition.model_validate(raw)
    assert m.aiAgentSettings is not None
    assert m.aiAgentSettings.lastPrompt == "Create an RSVP form."
    assert m.aiAgentSettings.includeEventInformation is True


def test_form_definition_omits_ai_agent_settings():
    raw = {
        "schemaVersion": "1.0",
        "formId": "402",
        "theme": {"primaryColor": "#000", "backgroundColor": "#fff", "fontFamily": "Inter"},
        "pages": _minimal_pages(),
    }
    m = FormDefinition.model_validate(raw)
    assert m.aiAgentSettings is None