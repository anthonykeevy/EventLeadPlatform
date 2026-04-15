"""Story 6.3: system/user prompt assembly for AI generation."""

from modules.form_ai import service
from modules.form_ai.system_prompt_sections_1_6 import SYSTEM_PROMPT_SECTIONS_1_TO_6


def test_build_initial_messages_uses_static_system_prompt():
    messages = service._build_initial_messages(
        prompt="Build a contact form",
        runtime_context=None,
    )
    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == SYSTEM_PROMPT_SECTIONS_1_TO_6
    assert messages[1]["role"] == "user"


def test_build_user_message_prompt_is_last_line():
    user_message = service._build_user_message(
        prompt="Keep this prompt unchanged.",
        runtime_context={},
    )
    assert "## User Request" in user_message
    assert user_message.rstrip().endswith("Keep this prompt unchanged.")


def test_build_user_message_contains_lock_state_and_runtime_context():
    user_message = service._build_user_message(
        prompt="Generate",
        runtime_context={
            "formId": "form-403",
            "canvasSettings": {"width": 1200, "height": 900, "gridSize": 8},
            "globalStylesLocked": True,
            "globalStyles": {"inputBackgroundColor": "#ffffff"},
            "theme": {"primaryColor": "#7c3aed", "fontFamily": "Inter"},
            "componentFootprints": [{"componentType": "text", "width": 560, "height": 117}],
            "eventInformation": {"name": "Summit 2026"},
        },
    )
    assert "### Global Styles Lock State" in user_message
    assert "\nlocked\n" in user_message
    assert "### Current Global Styles" in user_message
    assert '"inputBackgroundColor": "#ffffff"' in user_message


def test_generate_uses_system_user_message_split(monkeypatch):
    import json

    candidate = {
        "schemaVersion": "1.0",
        "formId": "x",
        "theme": {"primaryColor": "#000", "backgroundColor": "#fff", "fontFamily": "Inter"},
        "canvasSettings": {"width": 500, "height": 700, "gridSize": 8},
        "pages": [
            {
                "id": "page-1",
                "title": "P",
                "components": [
                    {
                        "id": "a",
                        "type": "text",
                        "props": {"label": "A"},
                        "position": {"x": 20, "y": 20},
                        "style": {"width": 460, "height": 72},
                    }
                ],
            }
        ],
    }
    monkeypatch.setattr(
        service,
        "_request_chatgpt_completion",
        lambda _messages, model_override=None: json.dumps(candidate),
    )

    result = service.generate_form_definition("hello", runtime_context=None)
    assert result.status == "completed"
    assert result.definitionJSON is not None


def test_submit_button_guardrail_keeps_submit_within_canvas_and_avoids_overlap():
    definition = {
        "schemaVersion": "1.0",
        "formId": "403",
        "theme": {"primaryColor": "#000", "fontFamily": "Inter"},
        "canvasSettings": {"width": 1920, "height": 980, "gridSize": 32},
        "pages": [
            {
                "id": "page-1",
                "components": [
                    {
                        "id": "country-1",
                        "type": "dropdown",
                        "position": {"x": 736, "y": 800},
                        "props": {"width": "544px"},
                    },
                    {
                        "id": "submit-button-1",
                        "type": "submit-button",
                        "position": {"x": 864, "y": 960},
                        "props": {"width": "224px", "buttonText": "Register"},
                    },
                ],
            }
        ],
    }
    runtime_context = {
        "canvasSettings": {"width": 1920, "height": 980, "gridSize": 32},
        "componentFootprints": [
            {"componentType": "dropdown", "width": 560, "height": 131},
            {"componentType": "submit-button", "width": 220, "height": 72},
        ],
    }

    adjusted = service._guardrail_submit_button_placement(definition, runtime_context)
    components = adjusted["pages"][0]["components"]
    submit = next(item for item in components if item["id"] == "submit-button-1")

    # 980 canvas height - 72 submit height = max Y 908; with 32px grid, submit should snap to 896.
    assert submit["position"]["y"] <= 908

    collisions = service._collect_visual_collisions(adjusted, runtime_context)
    boundaries = service._collect_visual_boundary_violations(adjusted, runtime_context)
    assert len(collisions) == 0
    assert len(boundaries) == 0


def test_column_flow_guardrail_expands_canvas_for_tall_forms():
    definition = {
        "schemaVersion": "1.0",
        "formId": "405",
        "theme": {"primaryColor": "#000", "fontFamily": "Inter"},
        "canvasSettings": {"width": 1920, "height": 980, "gridSize": 32},
        "pages": [
            {
                "id": "page-1",
                "components": [
                    {"id": "a", "type": "text", "position": {"x": 96, "y": 160}, "props": {"width": "560px"}},
                    {"id": "b", "type": "text", "position": {"x": 96, "y": 320}, "props": {"width": "560px"}},
                    {"id": "c", "type": "textarea", "position": {"x": 96, "y": 768}, "props": {"width": "720px", "height": 200}},
                    {"id": "d", "type": "file-upload", "position": {"x": 96, "y": 1008}, "props": {"width": "560px"}},
                    {"id": "e", "type": "dropdown", "position": {"x": 96, "y": 1184}, "props": {"width": "560px"}},
                    {"id": "f", "type": "terms", "position": {"x": 720, "y": 1184}, "props": {"width": "560px"}},
                ],
            }
        ],
    }
    runtime_context = {
        "canvasSettings": {"width": 1920, "height": 980, "gridSize": 32},
        "componentFootprints": [
            {"componentType": "text", "width": 560, "height": 110},
            {"componentType": "textarea", "width": 720, "height": 200},
            {"componentType": "file-upload", "width": 560, "height": 132},
            {"componentType": "dropdown", "width": 560, "height": 120},
            {"componentType": "terms", "width": 560, "height": 120},
        ],
    }

    adjusted = service._enforce_column_flow_and_canvas_fit(definition, runtime_context)
    canvas_height = adjusted["canvasSettings"]["height"]
    assert canvas_height > 980

    collisions = service._collect_visual_collisions(adjusted, runtime_context)
    boundaries = service._collect_visual_boundary_violations(adjusted, runtime_context)
    assert len(collisions) == 0
    assert len(boundaries) == 0


def test_column_flow_places_submit_after_content_and_resolves_bottom_row_overlap():
    definition = {
        "schemaVersion": "1.0",
        "formId": "405",
        "theme": {"primaryColor": "#000", "fontFamily": "Inter"},
        "canvasSettings": {"width": 1920, "height": 980, "gridSize": 32},
        "pages": [
            {
                "id": "page-1",
                "components": [
                    {"id": "why-1", "type": "textarea", "position": {"x": 64, "y": 864}, "props": {"width": "1152px", "height": 338}},
                    {"id": "heard-about-1", "type": "dropdown", "position": {"x": 640, "y": 1312}, "props": {"width": "560px"}},
                    {"id": "terms-privacy-1", "type": "terms", "position": {"x": 64, "y": 1312}, "props": {"width": "1152px"}},
                    {"id": "submit-1", "type": "submit-button", "position": {"x": 1632, "y": 896}, "props": {"width": "220px"}},
                ],
            }
        ],
    }
    runtime_context = {
        "canvasSettings": {"width": 1920, "height": 980, "gridSize": 32},
        "componentFootprints": [
            {"componentType": "textarea", "width": 720, "height": 338},
            {"componentType": "dropdown", "width": 560, "height": 120},
            {"componentType": "terms", "width": 560, "height": 120},
            {"componentType": "submit-button", "width": 220, "height": 72},
        ],
    }

    adjusted = service._enforce_column_flow_and_canvas_fit(definition, runtime_context)
    components = adjusted["pages"][0]["components"]
    by_id = {item["id"]: item for item in components}

    submit_y = by_id["submit-1"]["position"]["y"]
    heard_y = by_id["heard-about-1"]["position"]["y"]
    terms_y = by_id["terms-privacy-1"]["position"]["y"]
    assert submit_y > max(heard_y, terms_y)

    collisions = service._collect_visual_collisions(adjusted, runtime_context)
    boundaries = service._collect_visual_boundary_violations(adjusted, runtime_context)
    assert len(collisions) == 0
    assert len(boundaries) == 0


def test_trace_includes_post_processing_position_deltas(monkeypatch):
    import json

    monkeypatch.setattr(service, "ENABLE_POST_PROCESSING", True)

    candidate = {
        "schemaVersion": "1.0",
        "formId": "405",
        "theme": {"primaryColor": "#0055FF", "fontFamily": "Inter"},
        "canvasSettings": {"width": 1920, "height": 980, "gridSize": 32},
        "pages": [
            {
                "id": "page-1",
                "components": [
                    {
                        "id": "field-a",
                        "type": "text",
                        "position": {"x": 64, "y": 864},
                        "props": {"label": "A", "width": "560px"},
                    },
                    {
                        "id": "field-b",
                        "type": "text",
                        "position": {"x": 64, "y": 1024},
                        "props": {"label": "B", "width": "560px"},
                    },
                    {
                        "id": "submit-1",
                        "type": "submit-button",
                        "position": {"x": 1800, "y": 960},
                        "props": {"buttonText": "Submit", "width": "220px"},
                    },
                ],
            }
        ],
    }
    monkeypatch.setattr(
        service,
        "_request_chatgpt_completion",
        lambda _messages, model_override=None: json.dumps(candidate),
    )

    result = service.generate_form_definition(
        "Build a form",
        runtime_context={
            "canvasSettings": {"width": 1920, "height": 980, "gridSize": 32},
            "componentFootprints": [
                {"componentType": "text", "width": 560, "height": 110},
                {"componentType": "submit-button", "width": 220, "height": 72},
            ],
        },
    )
    assert result.trace.attempts
    attempt_post = result.trace.attempts[0].postProcessing
    assert attempt_post is not None
    assert attempt_post.changedComponentCount >= 1
    changed_ids = {item.componentId for item in attempt_post.changedComponents}
    assert "submit-1" in changed_ids or "field-b" in changed_ids
    assert result.trace.postProcessingSummary is not None
