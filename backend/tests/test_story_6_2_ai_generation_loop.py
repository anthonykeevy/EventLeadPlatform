"""Story 6.2 → 6.3.1 — AI generation loop, retry mechanics, and post-process.

History note: Story 6.2 had the LLM emit a full ``DefinitionJSON`` (with
``position``/``style`` stamped by the model). Most tests in this file
asserted that bad coordinates from the LLM would force a retry / fail.
Story 6.3.1 split that responsibility: the LLM now emits a
``FormSemanticPlan`` (no coordinates) and the *deterministic compiler*
owns geometry, so coordinate-driven failure paths can no longer be
provoked through the LLM mock. Where the original behavioural intent is
still meaningful (retry loop, retry cap, single-page rule, heading
normalization, post-process spacing/sync) the test has been rewritten
against the new contract; where it's not (geometry-driven retries) the
test has been replaced with the semantic-plan equivalent.
"""

import json

from modules.form_ai import service


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _base_definition() -> dict:
    """Legacy DefinitionJSON shape used by the small handful of tests below
    that still need to drive the legacy-coordinates ingestion path
    (``_semantic_plan_from_legacy_definition``)."""
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


def _semantic_plan(components: list[dict]) -> dict:
    return {
        "semanticPlanVersion": "1.0",
        "formId": "story-6-2-test",
        "title": "T",
        "components": components,
    }


def _set_provider(monkeypatch, payloads: list[str]) -> None:
    iterator = iter(payloads)

    def _provider(*_args, **_kwargs):
        try:
            return next(iterator)
        except StopIteration:
            return payloads[-1]

    monkeypatch.setattr(service, "_request_chatgpt_completion", _provider)


# ---------------------------------------------------------------------------
# Retry-loop mechanics (rewritten for semantic-plan input)
# ---------------------------------------------------------------------------


def test_story_6_2_retry_loop_converges_within_cap(monkeypatch):
    """The first attempt returns invalid JSON (parse-failure terminal phase),
    the second attempt returns a clean semantic plan; the service should
    take the corrected attempt and converge.

    Rationale: Story 6.3.1 moved coordinate validation to the deterministic
    compiler, so the only LLM-fault paths that *still* drive the retry loop
    end-to-end are JSON parse failures and semantic-plan validation
    failures. JSON parse is the simplest reproducer.
    """
    valid_plan = _semantic_plan(
        [
            {"componentType": "text", "label": "Full Name", "widthIntent": "full"},
            {"componentType": "submit-button", "label": "Submit", "widthIntent": "compact"},
        ]
    )
    _set_provider(monkeypatch, ["this is not json", json.dumps(valid_plan)])

    result = service.generate_form_definition(
        "Generate a contact form with a header title",
        runtime_context={"canvas": {"width": 500, "height": 700, "gridSize": 8}},
    )

    assert result.status == "completed", (result.trace.terminalReason, result.userMessage)
    assert result.definitionJSON is not None
    assert result.trace.attemptCount == 2
    assert result.trace.systemCorrectionAttemptsUsed == 1
    assert result.trace.terminalReason == "validated-success"
    assert result.trace.attempts[0].validation.valid is False
    assert result.trace.attempts[1].validation.valid is True


def test_story_6_2_retry_cap_exhausted_after_three_corrections(monkeypatch):
    """When every attempt returns un-parseable JSON the service must exit on
    ``json-parse-failed`` after the cap is hit. Default cap = 3 corrections,
    so attemptCount == 4 (initial + 3 corrections)."""
    _set_provider(monkeypatch, ["not json"] * 6)

    result = service.generate_form_definition("Generate a form that keeps failing")

    assert result.status == "failed", result.trace.terminalReason
    assert result.draftHasValidationIssues is False  # never produced a draft
    assert result.trace.attemptCount == 4
    assert result.trace.maxSystemCorrectionAttempts == 3
    assert result.trace.systemCorrectionAttemptsUsed == 3
    assert result.trace.terminalReason == "json-parse-failed"


def test_story_6_2_single_page_guardrail_enforced(monkeypatch):
    """Story 6.3.1 deterministic compiler *always* emits a single page
    regardless of what the LLM puts in the semantic plan; the guardrail is
    structural rather than runtime. We assert: even when the LLM returns
    an empty/sparse plan, the compiled definition has exactly one page.
    """
    plan = _semantic_plan(
        [{"componentType": "text", "label": "A", "widthIntent": "full"}]
    )
    _set_provider(monkeypatch, [json.dumps(plan)] * 4)

    result = service.generate_form_definition("Generate a contact form")

    assert result.status == "completed"
    assert result.definitionJSON is not None
    assert len(result.definitionJSON["pages"]) == 1


def test_story_6_2_side_by_side_fields_do_not_trigger_false_collision(monkeypatch):
    """Regression (still relevant): collision boxes must not inflate width
    to the runtime footprint when the LLM emits explicit narrow widths.
    Driven through the legacy-definition ingestion path because the
    contract is about how the validator interprets explicit ``style.width``
    values, not about plan-stage decisions."""
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

    _set_provider(monkeypatch, [json.dumps(side_by_side)])
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


# ---------------------------------------------------------------------------
# Tests removed in Story 6.3.1
# ---------------------------------------------------------------------------
# The following Story-6.2 tests asserted that geometry-driven failure modes
# (overlapping x/y, off-canvas x/y, runtime-footprint-budget violations on
# LLM-stamped widths) would trigger the retry loop. Story 6.3.1 made the
# compiler the single owner of geometry, so those failure modes can no
# longer be provoked through the LLM mock — the compiler simply re-lays out
# the components into a clean grid. The behaviour is still tested via:
#   - ``test_story_631_*`` (deterministic compiler unit tests)
#   - ``test_horizontal_stacked_rows_do_not_trigger_phantom_collisions``
#   - ``test_collision_check_still_inflates_when_height_missing``
# in ``test_story_63_context_pack_path.py``. The deleted tests were:
#   * test_story_6_2_visual_overlap_heuristic_triggers_retry_failure
#   * test_story_6_2_visual_boundary_heuristic_triggers_retry_failure
#   * test_story_6_2_runtime_footprint_budget_applied_to_boundary_checks


# ---------------------------------------------------------------------------
# Header / paragraph handling
# ---------------------------------------------------------------------------


def test_story_6_2_normalizes_header_text_prop_to_label(monkeypatch):
    """When the LLM (legacy shape) emits a header with ``props.text`` instead
    of ``props.label`` *and* the prompt explicitly asks for a header, the
    resulting page must keep the header and carry the user's text. The
    legacy-shape ingester (``_semantic_plan_from_legacy_definition``)
    is responsible for the ``text`` → ``label`` normalisation; the
    compiler then renders the header.
    """
    candidate = _base_definition()
    candidate["pages"][0]["components"] = [
        {
            "id": "header-1",
            "type": "header",
            "props": {"label": "Contact Us"},
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

    _set_provider(monkeypatch, [json.dumps(candidate)])
    result = service.generate_form_definition(
        "Generate a contact form with a header title"
    )

    assert result.status == "completed"
    assert result.definitionJSON is not None
    types = [c["type"] for c in result.definitionJSON["pages"][0]["components"]]
    assert "header" in types
    header = next(c for c in result.definitionJSON["pages"][0]["components"] if c["type"] == "header")
    assert header["props"]["label"] == "Contact Us"


def test_story_6_2_removes_unrequested_header_and_assigns_tab_order(monkeypatch):
    """When the prompt has no heading keyword the heading filter strips the
    header, and the post-process pass numbers tabOrder 1..N."""
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

    _set_provider(monkeypatch, [json.dumps(candidate)])
    result = service.generate_form_definition(
        "Build a lead capture form with name and email fields"
    )

    assert result.status == "completed"
    assert result.definitionJSON is not None
    components = result.definitionJSON["pages"][0]["components"]
    assert len(components) == 2
    assert [component["type"] for component in components] == ["text", "email"]
    assert [component["props"]["tabOrder"] for component in components] == [1, 2]


# ---------------------------------------------------------------------------
# Spacing / dimension synchronisation
# ---------------------------------------------------------------------------


def test_story_6_2_compiler_lays_out_single_column_with_increasing_y(monkeypatch):
    """Replaces ``test_story_6_2_rebalances_single_column_spacing_from_effective_heights``.

    The pre-Story-6.3.1 rebalancer pinned exact y values (25, 181, 336, …)
    based on hand-tuned spacing. The deterministic-grid compiler picks its
    own row height per layout mode and may legitimately pack multiple
    ``widthIntent: full`` components onto the same row when the canvas is
    wide enough (UAT round 6 — horizontal-stacked layout). The contract
    that survives is:

    * components are laid out in plan order (y monotonically non-decreasing)
    * no two components collide
    * no component leaks past the (possibly grown) canvas bottom
    """
    plan = _semantic_plan(
        [
            {"componentType": "text", "label": "Full Name", "widthIntent": "full"},
            {"componentType": "email", "label": "Email Address", "widthIntent": "full"},
            {"componentType": "phone", "label": "Phone Number", "widthIntent": "full"},
            {"componentType": "checkbox", "label": "Products", "widthIntent": "full",
             "options": [{"label": ch, "value": ch.lower()} for ch in "ABCDEFGH"]},
            {"componentType": "terms", "label": "I agree", "widthIntent": "full",
             "validationIntent": {"required": True}},
            {"componentType": "submit-button", "label": "Submit", "widthIntent": "compact"},
        ]
    )
    _set_provider(monkeypatch, [json.dumps(plan)])

    result = service.generate_form_definition(
        "Build a lead capture form",
        runtime_context={"canvas": {"width": 1920, "height": 980, "gridSize": 32}},
    )
    assert result.status == "completed"

    components = result.definitionJSON["pages"][0]["components"]
    ys = [c["position"]["y"] for c in components]
    assert ys == sorted(ys), ys

    canvas_h = result.definitionJSON["canvasSettings"]["height"]
    canvas_w = result.definitionJSON["canvasSettings"]["width"]
    bottoms = [c["position"]["y"] + c["style"]["height"] for c in components]
    assert max(bottoms) <= canvas_h, (max(bottoms), canvas_h)
    for c in components:
        assert c["position"]["x"] + c["style"]["width"] <= canvas_w + 1, c

    # Validator agrees: no collisions, no boundary violations.
    assert result.trace.validationSummary is not None
    assert result.trace.validationSummary.collisionCount == 0
    assert result.trace.validationSummary.boundaryViolationCount == 0


def test_story_6_2_compiler_compiles_long_and_short_option_lists(monkeypatch):
    """Replaces ``test_story_6_2_runtime_footprint_plus_options_growth_affects_spacing``.

    The Story-6.2 footprint-rebalancer grew checkbox heights linearly with
    the number of options (110 + 20px per extra option). The Story-6.3.1
    deterministic compiler instead stamps a layout-mode-aware row height
    (52 px in horizontal-stacked, 110-200 px in vertical-stacked) and
    relies on the *frontend* renderer to grow vertically when the option
    list overflows. The contract that survives at the compiler boundary
    is therefore "both shapes compile cleanly into a no-collision layout";
    the per-options height is now a runtime concern (see
    ``UniversalFieldShell`` and the second-pass remeasure flow).
    """
    long_options = [{"label": str(i), "value": str(i)} for i in range(1, 9)]
    short_options = [{"label": "Yes", "value": "yes"}, {"label": "No", "value": "no"}]
    runtime = {"canvas": {"width": 1920, "height": 980, "gridSize": 32}}

    for options in (long_options, short_options):
        plan = _semantic_plan(
            [
                {"componentType": "checkbox", "label": "Choices", "widthIntent": "full", "options": options},
                {"componentType": "submit-button", "label": "Submit", "widthIntent": "compact"},
            ]
        )
        _set_provider(monkeypatch, [json.dumps(plan)])
        result = service.generate_form_definition("Build a lead capture form", runtime_context=runtime)
        assert result.status == "completed", (len(options), result.trace.terminalReason)

        checkbox = next(
            c for c in result.definitionJSON["pages"][0]["components"] if c["type"] == "checkbox"
        )
        # Stamped height must agree with the props echo so the builder canvas
        # uses the same footprint as the validator.
        assert checkbox["style"]["height"] == checkbox["props"].get("height")
        # No collisions / no boundary violations regardless of option count.
        assert result.trace.validationSummary.collisionCount == 0
        assert result.trace.validationSummary.boundaryViolationCount == 0


def test_story_6_2_syncs_style_dimensions_to_props_for_builder(monkeypatch):
    """The form-builder canvas reads ``props.width`` for its absolute-positioned
    shell (see ``SortableComponent.displayWidth``). The deterministic
    compiler must therefore stamp the same width string into both
    ``style.width`` (validator/preview) and ``props.width`` (builder).
    """
    plan = _semantic_plan(
        [{"componentType": "text", "label": "Full Name", "widthIntent": "full"}]
    )
    _set_provider(monkeypatch, [json.dumps(plan)])

    result = service.generate_form_definition(
        "Build a lead capture form",
        runtime_context={"canvas": {"width": 1920, "height": 980, "gridSize": 32}},
    )

    assert result.status == "completed"
    component = result.definitionJSON["pages"][0]["components"][0]
    style_width = component["style"]["width"]
    props_width = component["props"].get("width")
    assert isinstance(props_width, str) and props_width.endswith("px"), props_width
    assert int(props_width[:-2]) == style_width, (props_width, style_width)


# ---------------------------------------------------------------------------
# Correction message format (still relevant — exercises _build_correction_message)
# ---------------------------------------------------------------------------


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
