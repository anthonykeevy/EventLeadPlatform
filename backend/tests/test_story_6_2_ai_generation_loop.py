import json

from modules.form_ai import service


def _base_definition() -> dict:
    return {
        "schemaVersion": "1.0",
        "formId": "ai-generated-form",
        "theme": {
            "primaryColor": "#0055FF",
            "backgroundColor": "#FFFFFF",
            "fontFamily": "Inter",
        },
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


def test_story_6_2_retry_loop_converges_within_cap(monkeypatch):
    invalid = _base_definition()
    invalid["pages"][0]["components"][0]["position"]["x"] = -10
    valid = _base_definition()

    responses = iter([json.dumps(invalid), json.dumps(valid)])
    monkeypatch.setattr(
        service,
        "_request_chatgpt_completion",
        lambda _messages, model_override=None, **kwargs: next(responses),
    )

    result = service.generate_form_definition(
        "Generate a contact form with a header title"
    )

    assert result.status == "completed"
    assert result.definitionJSON is not None
    assert result.trace.attemptCount == 2
    assert result.trace.systemCorrectionAttemptsUsed == 1
    assert result.trace.terminalReason == "validated-success"
    assert result.trace.attempts[0].validation.valid is False
    assert result.trace.attempts[1].validation.valid is True
    assert result.trace.attempts[0].collisionTrendVsPrevious == "n_a"
    assert result.trace.attempts[0].collisionDeltaFromPrevious is None
    assert result.trace.attempts[1].collisionDeltaFromPrevious is not None


def test_story_6_2_retry_cap_exhausted_after_three_corrections(monkeypatch):
    invalid = _base_definition()
    invalid["pages"][0]["components"][0]["position"]["x"] = -20

    responses = iter([json.dumps(invalid)] * 4)  # initial + 3 corrections
    monkeypatch.setattr(
        service,
        "_request_chatgpt_completion",
        lambda _messages, model_override=None, **kwargs: next(responses),
    )

    result = service.generate_form_definition("Generate a form that keeps failing")

    assert result.status == "failed"
    assert result.definitionJSON is not None
    assert result.draftHasValidationIssues is True
    assert result.trace.attemptCount == 4
    assert result.trace.maxSystemCorrectionAttempts == 3
    assert result.trace.systemCorrectionAttemptsUsed == 3
    assert result.trace.terminalReason == "retry-cap-exhausted"
    assert all(not entry.validation.valid for entry in result.trace.attempts)


def test_story_6_2_single_page_guardrail_enforced(monkeypatch):
    multi_page = _base_definition()
    multi_page["pages"].append(
        {
            "id": "page-2",
            "title": "Page 2",
            "components": [],
        }
    )

    responses = iter([json.dumps(multi_page)] * 4)
    monkeypatch.setattr(
        service,
        "_request_chatgpt_completion",
        lambda _messages, model_override=None, **kwargs: next(responses),
    )

    result = service.generate_form_definition("Generate a two page form")

    assert result.status == "failed"
    assert result.trace.attemptCount == 4
    assert result.trace.validationSummary is not None
    assert result.trace.validationSummary.schemaErrorCount >= 1


def test_story_6_2_side_by_side_fields_do_not_trigger_false_collision(monkeypatch):
    """Regression: collision boxes must not inflate width to footprint (~560px)."""
    side_by_side = _base_definition()
    side_by_side["canvasSettings"] = {"width": 1920, "height": 980, "gridSize": 32}
    side_by_side["pages"][0]["components"] = [
        {
            "id": "first-name",
            "type": "first-name",
            "props": {"label": "First"},
            "position": {"x": 40, "y": 40},
            "style": {"width": 400, "height": 100},
        },
        {
            "id": "last-name",
            "type": "text",
            "props": {"label": "Last"},
            "position": {"x": 480, "y": 40},
            "style": {"width": 400, "height": 100},
        },
    ]

    monkeypatch.setattr(
        service,
        "_request_chatgpt_completion",
        lambda _messages, model_override=None, **kwargs: json.dumps(side_by_side),
    )

    runtime_context = {
        "canvas": {"width": 1920, "height": 980, "gridSize": 32},
        "componentFootprints": [
            {"componentType": "first-name", "width": 560, "height": 110, "recommendedGapAfter": 24},
            {"componentType": "text", "width": 560, "height": 110, "recommendedGapAfter": 24},
        ],
    }

    result = service.generate_form_definition(
        "Build a form with first and last name side by side",
        runtime_context=runtime_context,
    )

    assert result.status == "completed"
    assert result.trace.validationSummary is not None
    assert result.trace.validationSummary.collisionCount == 0


def test_story_6_2_visual_overlap_heuristic_triggers_retry_failure(monkeypatch):
    visually_overlapping = _base_definition()
    visually_overlapping["pages"][0]["components"] = [
        {
            "id": "name-field",
            "type": "text",
            "props": {"label": "Full Name"},
            "position": {"x": 20, "y": 20},
            "style": {"width": 460, "height": 72},
        },
        {
            "id": "email-field",
            "type": "email",
            "props": {"label": "Email"},
            "position": {"x": 120, "y": 100},
            "style": {"width": 460, "height": 72},
        },
    ]

    responses = iter([json.dumps(visually_overlapping)] * 4)
    monkeypatch.setattr(
        service,
        "_request_chatgpt_completion",
        lambda _messages, model_override=None, **kwargs: next(responses),
    )

    result = service.generate_form_definition("Generate a compact contact form")

    assert result.status == "failed"
    assert result.trace.terminalReason == "retry-cap-exhausted"
    assert result.trace.validationSummary is not None
    assert result.trace.validationSummary.collisionCount >= 1


def test_story_6_2_visual_boundary_heuristic_triggers_retry_failure(monkeypatch):
    visually_off_canvas = _base_definition()
    visually_off_canvas["pages"][0]["components"] = [
        {
            "id": "right-edge-field",
            "type": "text",
            "props": {"label": "Name"},
            "position": {"x": 450, "y": 20},
            "style": {"width": 20, "height": 72},
        }
    ]

    responses = iter([json.dumps(visually_off_canvas)] * 4)
    monkeypatch.setattr(
        service,
        "_request_chatgpt_completion",
        lambda _messages, model_override=None, **kwargs: next(responses),
    )

    result = service.generate_form_definition("Generate a contact form near right edge")

    assert result.status == "failed"
    assert result.trace.terminalReason == "retry-cap-exhausted"
    assert result.trace.validationSummary is not None
    assert result.trace.validationSummary.boundaryViolationCount >= 1


def test_story_6_2_runtime_footprint_budget_applied_to_boundary_checks(monkeypatch):
    candidate = _base_definition()
    candidate["pages"][0]["components"] = [
        {
            "id": "name-field",
            "type": "text",
            "props": {"label": "Name"},
            "position": {"x": 40, "y": 20},
            "style": {"width": 20, "height": 40},
        }
    ]

    responses = iter([json.dumps(candidate)] * 4)
    monkeypatch.setattr(
        service,
        "_request_chatgpt_completion",
        lambda _messages, model_override=None, **kwargs: next(responses),
    )

    runtime_context = {
        "canvas": {"width": 500, "height": 700, "gridSize": 8},
        "componentFootprints": [
            {
                "componentType": "text",
                "width": 480,
                "height": 110,
                "recommendedGapAfter": 24,
            }
        ],
    }

    result = service.generate_form_definition(
        "Generate a contact form",
        runtime_context=runtime_context,
    )

    assert result.status == "failed"
    assert result.trace.terminalReason == "retry-cap-exhausted"
    assert result.trace.validationSummary is not None
    assert result.trace.validationSummary.boundaryViolationCount >= 1


def test_story_6_2_normalizes_header_text_prop_to_label(monkeypatch):
    candidate = _base_definition()
    candidate["pages"][0]["components"] = [
        {
            "id": "header-1",
            "type": "header",
            "props": {"text": "Contact Us"},
            "position": {"x": 20, "y": 20},
            "style": {"width": 460, "height": 48},
        },
        {
            "id": "name-field",
            "type": "text",
            "props": {"label": "Full Name"},
            "position": {"x": 20, "y": 90},
            "style": {"width": 460, "height": 72},
        },
    ]

    monkeypatch.setattr(
        service,
        "_request_chatgpt_completion",
        lambda _messages, model_override=None, **kwargs: json.dumps(candidate),
    )

    result = service.generate_form_definition(
        "Generate a contact form with a header title"
    )

    assert result.status == "completed"
    assert result.definitionJSON is not None
    header = result.definitionJSON["pages"][0]["components"][0]
    assert header["type"] == "header"
    assert header["props"]["label"] == "Contact Us"


def test_story_6_2_removes_unrequested_header_and_assigns_tab_order(monkeypatch):
    candidate = _base_definition()
    candidate["pages"][0]["components"] = [
        {
            "id": "header-1",
            "type": "header",
            "props": {"label": "Automotive Spare Parts - Lead Capture"},
            "position": {"x": 20, "y": 20},
            "style": {"width": 460, "height": 48},
        },
        {
            "id": "name-field",
            "type": "text",
            "props": {"label": "Full Name"},
            "position": {"x": 20, "y": 90},
            "style": {"width": 460, "height": 72},
        },
        {
            "id": "email-field",
            "type": "email",
            "props": {"label": "Email"},
            "position": {"x": 20, "y": 220},
            "style": {"width": 460, "height": 72},
        },
    ]

    monkeypatch.setattr(
        service,
        "_request_chatgpt_completion",
        lambda _messages, model_override=None, **kwargs: json.dumps(candidate),
    )

    result = service.generate_form_definition(
        "Build a lead capture form with name and email fields"
    )

    assert result.status == "completed"
    assert result.definitionJSON is not None
    components = result.definitionJSON["pages"][0]["components"]
    assert len(components) == 2
    assert [component["type"] for component in components] == ["text", "email"]
    assert [component["props"]["tabOrder"] for component in components] == [1, 2]


def test_story_6_2_rebalances_single_column_spacing_from_effective_heights(monkeypatch):
    candidate = _base_definition()
    candidate["canvasSettings"] = {"width": 1920, "height": 980, "gridSize": 32}
    candidate["pages"][0]["components"] = [
        {
            "id": "full-name",
            "type": "text",
            "props": {"label": "Full Name"},
            "position": {"x": 20, "y": 10},
            "style": {"width": 1880, "height": 130},
        },
        {
            "id": "email",
            "type": "email",
            "props": {"label": "Email Address"},
            "position": {"x": 20, "y": 40},
            "style": {"width": 1880, "height": 130},
        },
        {
            "id": "phone",
            "type": "phone",
            "props": {"label": "Phone Number"},
            "position": {"x": 20, "y": 70},
            "style": {"width": 1880, "height": 130},
        },
        {
            "id": "products",
            "type": "checkbox",
            "props": {
                "label": "Products",
                "options": [
                    {"label": "A", "value": "a"},
                    {"label": "B", "value": "b"},
                    {"label": "C", "value": "c"},
                    {"label": "D", "value": "d"},
                    {"label": "E", "value": "e"},
                    {"label": "F", "value": "f"},
                    {"label": "G", "value": "g"},
                    {"label": "H", "value": "h"},
                ],
            },
            "position": {"x": 20, "y": 100},
            "style": {"width": 1880, "height": 131},
        },
        {
            "id": "terms",
            "type": "terms",
            "props": {"label": "I agree", "required": True},
            "position": {"x": 20, "y": 130},
            "style": {"width": 1880, "height": 120},
        },
        {
            "id": "submit",
            "type": "submit-button",
            "props": {"label": "Submit"},
            "position": {"x": 20, "y": 160},
            "style": {"width": 220, "height": 81},
        },
    ]

    monkeypatch.setattr(
        service,
        "_request_chatgpt_completion",
        lambda _messages, model_override=None, **kwargs: json.dumps(candidate),
    )

    result = service.generate_form_definition("Build a lead capture form")

    assert result.status == "completed"
    assert result.definitionJSON is not None
    components = result.definitionJSON["pages"][0]["components"]

    expected_y = [25, 181, 336, 492, 737, 883]
    actual_y = [component["position"]["y"] for component in components]
    assert actual_y == expected_y
    assert components[-1]["style"]["height"] == 72
    assert components[-1]["props"]["height"] == 72


def test_story_6_2_runtime_footprint_plus_options_growth_affects_spacing(monkeypatch):
    candidate = _base_definition()
    candidate["canvasSettings"] = {"width": 1920, "height": 980, "gridSize": 32}
    candidate["pages"][0]["components"] = [
        {
            "id": "full-name",
            "type": "text",
            "props": {"label": "Full Name"},
            "position": {"x": 20, "y": 10},
            "style": {"width": 1880, "height": 130},
        },
        {
            "id": "products",
            "type": "checkbox",
            "props": {
                "label": "Products",
                "options": [{"label": str(i), "value": str(i)} for i in range(1, 9)],
            },
            "position": {"x": 20, "y": 40},
            "style": {"width": 1880, "height": 131},
        },
        {
            "id": "submit",
            "type": "submit-button",
            "props": {"label": "Submit"},
            "position": {"x": 20, "y": 70},
            "style": {"width": 220, "height": 81},
        },
    ]

    runtime_context = {
        "canvas": {"width": 1920, "height": 980, "gridSize": 32},
        "componentFootprints": [
            {"componentType": "checkbox", "width": 1880, "height": 131, "recommendedGapAfter": 24}
        ],
    }

    monkeypatch.setattr(
        service,
        "_request_chatgpt_completion",
        lambda _messages, model_override=None, **kwargs: json.dumps(candidate),
    )

    result = service.generate_form_definition(
        "Build a lead capture form",
        runtime_context=runtime_context,
    )

    assert result.status == "completed"
    assert result.definitionJSON is not None
    components = result.definitionJSON["pages"][0]["components"]

    # Checkbox: baseline 131 + options growth (8 options => +100) => effective 231.
    # Submit height clamped 81 -> 72: total 130 + 231 + 72 = 433; available 547; spaces 4
    assert [component["position"]["y"] for component in components] == [137, 404, 771]
    assert components[1]["style"]["height"] == 231
    assert components[1]["props"]["height"] == 231
    assert components[2]["style"]["height"] == 72


def test_story_6_2_syncs_style_dimensions_to_props_for_builder(monkeypatch):
    candidate = _base_definition()
    candidate["canvasSettings"] = {"width": 1920, "height": 980, "gridSize": 32}
    candidate["pages"][0]["components"] = [
        {
            "id": "name-field",
            "type": "text",
            "props": {"label": "Full Name"},
            "position": {"x": 20, "y": 20},
            "style": {"width": 1880, "height": 130},
        }
    ]

    monkeypatch.setattr(
        service,
        "_request_chatgpt_completion",
        lambda _messages, model_override=None, **kwargs: json.dumps(candidate),
    )

    result = service.generate_form_definition("Build a lead capture form")

    assert result.status == "completed"
    assert result.definitionJSON is not None
    component = result.definitionJSON["pages"][0]["components"][0]
    assert component["props"]["width"] == "1880px"
    assert component["props"]["height"] == 130


def test_story_6_2_collision_correction_includes_geometry_and_hints():
    from modules.form_validate.schemas import CollisionViolation, FormValidationResponse, ValidationSummary

    definition = {
        "schemaVersion": "1.0",
        "formId": "overlap-test",
        "theme": {},
        "canvasSettings": {"width": 500, "height": 700, "gridSize": 8},
        "pages": [
            {
                "id": "page-1",
                "title": "T",
                "components": [
                    {
                        "id": "a",
                        "type": "text",
                        "props": {"label": "A"},
                        "position": {"x": 20, "y": 20},
                        "style": {"width": 300, "height": 100},
                    },
                    {
                        "id": "b",
                        "type": "email",
                        "props": {"label": "B"},
                        "position": {"x": 20, "y": 80},
                        "style": {"width": 300, "height": 100},
                    },
                ],
            }
        ],
    }
    collisions = [
        CollisionViolation(
            componentAId="a",
            componentBId="b",
            pageId="page-1",
            layout="pages",
            overlapArea=120.0,
        )
    ]
    validation = FormValidationResponse(
        valid=False,
        schemaErrors=[],
        boundaryViolations=[],
        collisions=collisions,
        summary=ValidationSummary(errorCount=1, warningCount=0),
        meta={},
    )
    msg = service._build_correction_message(validation, definition, None)
    assert "Layout snapshot" in msg
    assert "Reported overlaps" in msg
    assert "| a |" in msg and "| b |" in msg
    assert "Vertical overlap" in msg or "position.y" in msg
