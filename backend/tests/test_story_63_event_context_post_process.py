"""Story 6.3: eventInformation must not cause event headers to be stripped in post-process."""

from modules.form_ai import service


def test_post_process_keeps_header_when_runtime_has_event_information():
    definition = {
        "schemaVersion": "1.0",
        "formId": "x",
        "theme": {},
        "canvasSettings": {"width": 1920, "height": 980, "gridSize": 8},
        "pages": [
            {
                "id": "page-1",
                "title": "P1",
                "components": [
                    {
                        "id": "evh",
                        "type": "header",
                        "props": {"label": "Spring Gala 2026 — Acme Hall"},
                        "position": {"x": 20, "y": 10},
                        "style": {"width": 560, "height": 52},
                    },
                    {
                        "id": "name",
                        "type": "text",
                        "props": {"label": "Name"},
                        "position": {"x": 20, "y": 80},
                        "style": {"width": 560, "height": 110},
                    },
                ],
            }
        ],
    }
    runtime = {"eventInformation": {"eventId": 1, "name": "Spring Gala 2026"}}
    # Prompt must lack heading keywords so we prove eventInformation alone allows the header.
    out = service._post_process_generated_definition(
        definition,
        "RSVP form with name field only.",
        runtime,
    )
    types = [c["type"] for c in out["pages"][0]["components"]]
    assert types[0] == "header"


def test_post_process_still_strips_header_without_prompt_or_event():
    definition = {
        "schemaVersion": "1.0",
        "formId": "x",
        "theme": {},
        "canvasSettings": {"width": 1920, "height": 980, "gridSize": 8},
        "pages": [
            {
                "id": "page-1",
                "title": "P1",
                "components": [
                    {
                        "id": "evh",
                        "type": "header",
                        "props": {"label": "Unwanted"},
                        "position": {"x": 20, "y": 10},
                        "style": {"width": 560, "height": 52},
                    },
                    {
                        "id": "name",
                        "type": "text",
                        "props": {"label": "Name"},
                        "position": {"x": 20, "y": 80},
                        "style": {"width": 560, "height": 110},
                    },
                ],
            }
        ],
    }
    out = service._post_process_generated_definition(
        definition,
        "RSVP form with name field only.",
        None,
    )
    types = [c["type"] for c in out["pages"][0]["components"]]
    assert "header" not in types
