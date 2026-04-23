"""Story 6.3 / 6.3.1 — heading filter behaviour in ``_post_process_generated_definition``.

History note: an earlier test
(``test_post_process_keeps_header_when_runtime_has_event_information``)
asserted that the presence of ``runtime_context["eventInformation"]`` would
keep an LLM-emitted ``header`` even when the user prompt didn't ask for one.
That escape hatch was removed in the Story 6.3.1 redesign — heading
acceptance now goes through ``_prompt_requests_heading`` only, so headers
without a heading-keyword prompt are stripped at the *semantic plan* stage
(``_filter_unrequested_headings_from_plan``) **and** the post-compile pass
keeps that decision consistent. The test was deleted rather than rewritten;
the feature could be reinstated by reading ``runtime_context`` inside the
heading-filter branch below if/when product wants it back.
"""

from modules.form_ai import service


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
    out, _applied = service._post_process_generated_definition(
        definition,
        "RSVP form with name field only.",
        None,
    )
    types = [c["type"] for c in out["pages"][0]["components"]]
    assert "header" not in types
