"""Story 6.3.1 — system/user prompt assembly + end-to-end compiler validation.

This file replaces the original Story 6.3 tests that referenced
``_build_user_message``, ``_guardrail_submit_button_placement`` and
``_enforce_column_flow_and_canvas_fit``. Those helpers were removed when
the Story 6.3.1 deterministic compiler took over: the LLM now returns a
``FormSemanticPlan`` (no coordinates), and the compiler is the single
owner of geometry, canvas growth and submit-button placement. The tests
below assert the *behaviour* those helpers used to guarantee, expressed
through the new public surface.
"""

import json
from typing import Any, Dict

from modules.form_ai import service


def _semantic_plan(components: list[dict[str, Any]], *, form_id: str = "ctx-test", title: str = "T") -> dict[str, Any]:
    return {
        "semanticPlanVersion": "1.0",
        "formId": form_id,
        "title": title,
        "components": components,
    }


def _generate_with_semantic_plan(plan: dict[str, Any], runtime_context: dict[str, Any] | None, monkeypatch) -> Any:
    monkeypatch.setattr(
        service,
        "_request_chatgpt_completion",
        lambda *_args, **_kwargs: json.dumps(plan),
    )
    return service.generate_form_definition(
        "Build a form",
        runtime_context=runtime_context,
        max_system_correction_attempts=0,
        db_session=None,
    )


# ---------------------------------------------------------------------------
# Prompt assembly
# ---------------------------------------------------------------------------


def test_build_initial_messages_returns_system_user_pair():
    """The two-message structure is part of the OpenAI contract; the system
    body must mention the FormSemanticPlan output schema, and the user body
    must repeat the prompt verbatim."""
    messages = service._build_initial_messages(
        prompt="Build a contact form",
        context_pack="<<context-pack>>",
        runtime_context=None,
    )
    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"
    assert "FormSemanticPlan" in messages[0]["content"]
    # Context pack is pasted into the system prompt so policy stays in one
    # place across attempts.
    assert "<<context-pack>>" in messages[0]["content"]
    assert "Build a contact form" in messages[1]["content"]


def test_build_initial_messages_carries_runtime_context_block():
    """Runtime context (canvas, locked globals, theme) must reach the LLM via
    the system prompt's runtime-context block."""
    messages = service._build_initial_messages(
        prompt="Generate",
        context_pack="<<context-pack>>",
        runtime_context={
            "formId": "form-403",
            "canvas": {"width": 1200, "height": 900, "gridSize": 8},
            "lockedGlobals": {"globalStyles": {"inputBackgroundColor": "#ffffff"}},
            "theme": {"primaryColor": "#7c3aed", "fontFamily": "Inter"},
        },
    )
    system_body = messages[0]["content"]
    assert "Runtime layout context" in system_body
    assert "form-403" in system_body
    assert "#7c3aed" in system_body


def test_build_initial_messages_emits_terms_defaults_rule_when_company_terms_present():
    """The runtime-context block injects an explicit instruction to prefer
    the `terms` component and reuse company-managed termsLinkText. This is
    what carries the AI Agent → terms-component nudge for §8.4 of the UAT
    guide; if it disappears the AI will start emitting raw checkboxes again.
    """
    messages = service._build_initial_messages(
        prompt="Generate",
        context_pack="<<context-pack>>",
        runtime_context={
            "termsDefaults": {
                "hasCompanyTerms": True,
                "termsLinkText": "Acme Privacy Policy",
            },
        },
    )
    system_body = messages[0]["content"]
    assert "Terms defaults rule" in system_body
    assert "Acme Privacy Policy" in system_body


# ---------------------------------------------------------------------------
# End-to-end: deterministic compiler owns geometry
# ---------------------------------------------------------------------------


def test_generate_uses_system_user_message_split(monkeypatch):
    """Smoke test that the new pipeline (semantic plan → compiler) returns
    a successful definition without coordinates leaking from the LLM."""
    plan = _semantic_plan(
        [
            {"componentType": "text", "label": "Name", "widthIntent": "full"},
            {"componentType": "submit-button", "label": "Send", "widthIntent": "compact"},
        ],
    )
    result = _generate_with_semantic_plan(
        plan,
        runtime_context={"canvas": {"width": 500, "height": 700, "gridSize": 8}},
        monkeypatch=monkeypatch,
    )

    assert result.status == "completed", (result.trace.terminalReason, result.userMessage)
    assert result.definitionJSON is not None
    assert result.trace.compilerMode == "deterministic-grid"


def test_compiler_keeps_submit_button_within_canvas(monkeypatch):
    """Replaces ``test_submit_button_guardrail_keeps_submit_within_canvas_and_avoids_overlap``.

    The deterministic compiler is the new owner of submit-button placement;
    the contract that survives is "submit must end up inside the (possibly
    grown) canvas".
    """
    plan = _semantic_plan(
        [
            {"componentType": "dropdown", "label": "Country", "widthIntent": "full",
             "options": [{"label": "AU", "value": "au"}, {"label": "NZ", "value": "nz"}]},
            {"componentType": "submit-button", "label": "Register", "widthIntent": "compact"},
        ],
    )
    result = _generate_with_semantic_plan(
        plan,
        runtime_context={"canvas": {"width": 1920, "height": 980, "gridSize": 32}},
        monkeypatch=monkeypatch,
    )
    assert result.status == "completed"

    canvas_height = result.definitionJSON["canvasSettings"]["height"]
    submit = next(
        c for c in result.definitionJSON["pages"][0]["components"]
        if c["type"] == "submit-button"
    )
    submit_bottom = submit["position"]["y"] + submit["style"]["height"]
    assert submit_bottom <= canvas_height, (submit_bottom, canvas_height)
    assert submit["position"]["x"] >= 0


def test_compiler_grows_canvas_for_tall_forms(monkeypatch):
    """Replaces ``test_column_flow_guardrail_expands_canvas_for_tall_forms``.

    When the semantic plan has more components than the initial canvas can
    hold vertically, the compiler is allowed to grow ``canvasSettings.height``
    (UAT round 4 policy change). The contract: compiled canvas height >=
    initial canvas height, and the resulting layout has zero phantom
    collisions / boundary violations.
    """
    plan = _semantic_plan(
        [
            {"componentType": "text", "label": "First name", "widthIntent": "full"},
            {"componentType": "text", "label": "Last name", "widthIntent": "full"},
            {"componentType": "textarea", "label": "Comments", "widthIntent": "full"},
            {"componentType": "file-upload", "label": "Attach", "widthIntent": "full"},
            {"componentType": "dropdown", "label": "Source", "widthIntent": "full",
             "options": [{"label": "Web", "value": "web"}]},
            {"componentType": "terms", "label": "I agree", "widthIntent": "full"},
            {"componentType": "submit-button", "label": "Send", "widthIntent": "compact"},
        ],
    )
    result = _generate_with_semantic_plan(
        plan,
        runtime_context={"canvas": {"width": 1920, "height": 600, "gridSize": 32}},
        monkeypatch=monkeypatch,
    )
    assert result.status == "completed"
    assert result.definitionJSON["canvasSettings"]["height"] >= 600

    collisions = service._collect_visual_collisions(
        result.definitionJSON,
        runtime_context={"canvas": {"width": 1920, "height": 600, "gridSize": 32}},
    )
    boundaries = service._collect_visual_boundary_violations(
        result.definitionJSON,
        runtime_context={"canvas": {"width": 1920, "height": 600, "gridSize": 32}},
    )
    assert collisions == [], collisions
    assert boundaries == [], boundaries


def test_compiler_places_submit_after_content_block(monkeypatch):
    """Replaces ``test_column_flow_places_submit_after_content_and_resolves_bottom_row_overlap``.

    The deterministic compiler honours the semantic plan's component order
    (no reordering by type — order is the LLM's responsibility, told via
    system-prompt rules). When submit is listed last, it must end up at the
    largest y. When the compiler-generated layout has zero collisions and
    zero boundary violations, the contract that survives is that submit's
    bottom edge sits below the bottom edge of every other component.
    """
    plan = _semantic_plan(
        [
            {"componentType": "textarea", "label": "Why", "widthIntent": "full"},
            {"componentType": "dropdown", "label": "Heard about us", "widthIntent": "full",
             "options": [{"label": "Web", "value": "web"}]},
            {"componentType": "terms", "label": "I agree", "widthIntent": "full"},
            {"componentType": "submit-button", "label": "Send", "widthIntent": "compact"},
        ],
    )
    result = _generate_with_semantic_plan(
        plan,
        runtime_context={"canvas": {"width": 1920, "height": 980, "gridSize": 32}},
        monkeypatch=monkeypatch,
    )
    assert result.status == "completed"

    components = result.definitionJSON["pages"][0]["components"]
    submit = next(c for c in components if c["type"] == "submit-button")
    submit_bottom = submit["position"]["y"] + submit["style"]["height"]
    other_bottoms = [
        c["position"]["y"] + c["style"]["height"]
        for c in components
        if c["type"] != "submit-button"
    ]
    assert submit_bottom >= max(other_bottoms), (submit_bottom, other_bottoms)


def test_post_process_position_deltas_recorded_in_trace(monkeypatch):
    """Replaces ``test_trace_includes_post_processing_position_deltas``.

    The trace surfaces ``compileSummary.postProcessingApplied`` so callers
    can audit which transforms ran. ``ENABLE_POST_PROCESSING`` no longer
    exists — heading filter + tab order always run for the deterministic
    grid path; this test pins that contract.
    """
    plan = _semantic_plan(
        [
            {"componentType": "text", "label": "A", "widthIntent": "full"},
            {"componentType": "text", "label": "B", "widthIntent": "full"},
            {"componentType": "submit-button", "label": "Submit", "widthIntent": "compact"},
        ],
    )
    result = _generate_with_semantic_plan(
        plan,
        runtime_context={"canvas": {"width": 1920, "height": 980, "gridSize": 32}},
        monkeypatch=monkeypatch,
    )
    assert result.status == "completed"
    assert result.trace.attempts
    attempt = result.trace.attempts[0]
    assert attempt.compileDiagnostics is not None
    pp_applied = attempt.compileDiagnostics.get("postProcessingApplied")
    assert isinstance(pp_applied, dict)
    assert pp_applied.get("headingFilter") is True
    assert pp_applied.get("tabOrder") is True

    # Components carry tabOrder = 1..N after the post-process pass.
    components = result.definitionJSON["pages"][0]["components"]
    tab_orders = [c["props"].get("tabOrder") for c in components]
    assert tab_orders == list(range(1, len(components) + 1))


# ---------------------------------------------------------------------------
# Validator parity (UAT round 11 — false-positive collision/boundary fix)
# ---------------------------------------------------------------------------


def test_horizontal_stacked_rows_do_not_trigger_phantom_collisions():
    """UAT round 11 regression — desktop/tablet horizontal-stacked layouts.

    Each component is on its own row at 24 px gaps with the compiler-stamped
    height of 52 px. The legacy ``_minimum_render_height`` table inflated
    those rows to 110-120 px (vertical-stacked footprint) and produced 8+
    phantom collisions even though the compiled positions are clean. This
    test mirrors the production trace for the "sales lead" prompt where the
    user observed false-positive collision warnings on desktop and tablet
    while the same form passed on mobile (which actually uses the inflated
    vertical heights).
    """

    definition = {
        "schemaVersion": "1.0",
        "formId": "411",
        "theme": {"primaryColor": "#0055FF", "fontFamily": "Inter"},
        "canvasSettings": {"width": 1920, "height": 1012, "gridSize": 32},
        "pages": [
            {
                "id": "page-1",
                "components": [
                    {"id": "header-1", "type": "header",
                     "position": {"x": 40, "y": 24},
                     "props": {"width": "1840px", "height": 56},
                     "style": {"width": 1840, "height": 56}},
                    {"id": "first-name-2", "type": "first-name",
                     "position": {"x": 40, "y": 104},
                     "props": {"width": "717px", "height": 52},
                     "style": {"width": 717, "height": 52}},
                    {"id": "text-3", "type": "text",
                     "position": {"x": 40, "y": 180},
                     "props": {"width": "834px", "height": 52},
                     "style": {"width": 834, "height": 52}},
                    {"id": "email-4", "type": "email",
                     "position": {"x": 40, "y": 256},
                     "props": {"width": "879px", "height": 52},
                     "style": {"width": 879, "height": 52}},
                    {"id": "phone-5", "type": "phone",
                     "position": {"x": 40, "y": 332},
                     "props": {"width": "767px", "height": 52},
                     "style": {"width": 767, "height": 52}},
                    {"id": "text-6", "type": "text",
                     "position": {"x": 40, "y": 408},
                     "props": {"width": "771px", "height": 52},
                     "style": {"width": 771, "height": 52}},
                    {"id": "dropdown-7", "type": "dropdown",
                     "position": {"x": 40, "y": 484},
                     "props": {
                         "width": "582px", "height": 52,
                         "options": [
                             {"label": "1-10", "value": "1-10"},
                             {"label": "11-50", "value": "11-50"},
                             {"label": "51-200", "value": "51-200"},
                             {"label": "201-500", "value": "201-500"},
                             {"label": "500+", "value": "500+"},
                         ],
                     },
                     "style": {"width": 582, "height": 52}},
                    {"id": "rating-8", "type": "rating",
                     "position": {"x": 40, "y": 560},
                     "props": {"width": "659px", "height": 52},
                     "style": {"width": 659, "height": 52}},
                    {"id": "textarea-9", "type": "textarea",
                     "position": {"x": 40, "y": 636},
                     "props": {"width": "993px", "height": 200},
                     "style": {"width": 993, "height": 200}},
                    {"id": "terms-10", "type": "terms",
                     "position": {"x": 40, "y": 860},
                     "props": {"width": "797px", "height": 52},
                     "style": {"width": 797, "height": 52}},
                    {"id": "submit-button-11", "type": "submit-button",
                     "position": {"x": 40, "y": 936},
                     "props": {"width": "280px", "height": 52},
                     "style": {"width": 280, "height": 52}},
                ],
            }
        ],
    }

    collisions = service._collect_visual_collisions(definition)
    boundaries = service._collect_visual_boundary_violations(definition)

    assert collisions == [], (
        f"Expected no phantom collisions; got {[(c.componentAId, c.componentBId) for c in collisions]}"
    )
    assert boundaries == [], (
        f"Expected no boundary violations; got {[b.componentId for b in boundaries]}"
    )


def test_collision_check_still_inflates_when_height_missing():
    """Safety net: legacy definitions without ``style.height`` (and tiny/zero
    heights) still pass through ``_minimum_render_height`` so we don't hide
    real overlaps in old fixtures or LLM-emitted JSON before the compiler
    stamps a height.
    """

    definition = {
        "schemaVersion": "1.0",
        "formId": "test",
        "theme": {"primaryColor": "#000", "fontFamily": "Inter"},
        "canvasSettings": {"width": 1920, "height": 980, "gridSize": 32},
        "pages": [
            {
                "id": "page-1",
                "components": [
                    {"id": "a", "type": "text",
                     "position": {"x": 40, "y": 100},
                     "props": {"width": "560px"}},
                    {"id": "b", "type": "text",
                     "position": {"x": 40, "y": 150},
                     "props": {"width": "560px"}},
                ],
            }
        ],
    }

    collisions = service._collect_visual_collisions(definition)
    assert len(collisions) == 1
    assert {collisions[0].componentAId, collisions[0].componentBId} == {"a", "b"}
