import json
from typing import Any, Dict

from modules.form_ai import service
from modules.form_ai.compiler import (
    LAYOUT_MODE_HORIZONTAL_STACKED,
    LAYOUT_MODE_VERTICAL_PACKED,
    compile_semantic_plan_to_definition,
    resolve_layout_mode,
)
from modules.form_ai.schemas import FormSemanticPlan, SemanticComponentIntent


def _governance_payload() -> dict:
    return {
        "capabilityPolicyJson": {
            "step1": {"allowSemanticOnly": True, "allowGeometry": False},
            "step2": {"gridOnly": True, "allowNonGrid": False},
        },
        "widthClassPolicyJson": {
            "classes": {
                "compact": {"minSpan": 3, "targetSpan": 4, "maxSpan": 5},
                "half": {"minSpan": 5, "targetSpan": 6, "maxSpan": 7},
                "full": {"minSpan": 10, "targetSpan": 12, "maxSpan": 12},
            },
            "downgradeRules": [{"if": "canvasWidth<1200", "from": "half", "to": "full"}],
        },
        "componentCapabilitySnapshotJson": {
            "components": [
                {"type": "header", "widthClasses": ["full"]},
                {"type": "rating", "widthClasses": ["half", "full"]},
                {"type": "textarea", "widthClasses": ["half", "full"]},
                {"type": "dropdown", "widthClasses": ["compact", "half", "full"]},
                {"type": "submit-button", "widthClasses": ["compact", "half"]},
            ]
        },
        "validationContracts": [
            {"componentType": "textarea", "allowedRules": ["required", "minLength", "maxLength"]},
            {"componentType": "dropdown", "allowedRules": ["required"]},
            {"componentType": "rating", "allowedRules": ["required", "min", "max"]},
            {"componentType": "submit-button", "allowedRules": []},
            {"componentType": "header", "allowedRules": []},
        ],
    }


def test_story_631_compiler_accepts_semantic_plan_without_coordinates():
    semantic = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "formId": "feedback-1",
            "title": "Customer Feedback",
            "components": [
                {"componentType": "header", "label": "Customer Feedback", "widthIntent": "full"},
                {
                    "componentType": "rating",
                    "label": "Overall experience",
                    "widthIntent": "half",
                    "validationIntent": {"required": True, "min": 1, "max": 5},
                },
                {
                    "componentType": "rating",
                    "label": "Recommendation likelihood",
                    "widthIntent": "half",
                    "validationIntent": {"required": True, "min": 0, "max": 10},
                },
                {"componentType": "textarea", "label": "What did you like most?", "widthIntent": "full"},
                {"componentType": "textarea", "label": "What could we improve?", "widthIntent": "full"},
                {
                    "componentType": "dropdown",
                    "label": "How did you find us?",
                    "widthIntent": "half",
                    "options": [
                        {"label": "Search Engine", "value": "search"},
                        {"label": "Social Media", "value": "social"},
                        {"label": "Friend", "value": "friend"},
                    ],
                },
                {
                    "componentType": "submit-button",
                    "label": "Submit",
                    "widthIntent": "compact",
                    "actionAlignment": "center",
                },
            ],
        }
    )
    governance = _governance_payload()

    definition, compile_summary = compile_semantic_plan_to_definition(
        semantic,
        runtime_context={"canvas": {"width": 1920, "height": 980, "gridSize": 8}},
        capability_policy_json=governance["capabilityPolicyJson"],
        width_policy_json=governance["widthClassPolicyJson"],
        capability_snapshot_json=governance["componentCapabilitySnapshotJson"],
        validation_contracts=governance["validationContracts"],
    )

    assert definition["schemaVersion"] == "1.0"
    assert definition["pages"][0]["components"]
    assert compile_summary["compilerMode"] == "deterministic-grid"
    assert compile_summary["outputComponentCount"] == len(semantic.components)
    submit = next(item for item in definition["pages"][0]["components"] if item["type"] == "submit-button")
    assert submit["position"]["x"] >= 0
    assert submit["position"]["y"] + submit["style"]["height"] <= definition["canvasSettings"]["height"]


def test_story_631_compiler_is_deterministic_for_same_semantic_input():
    semantic = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "formId": "deterministic-1",
            "components": [
                {"componentType": "header", "label": "Talk to Sales", "widthIntent": "full"},
                {"componentType": "rating", "label": "Interest", "widthIntent": "half"},
                {"componentType": "dropdown", "label": "Company size", "widthIntent": "half"},
                {"componentType": "textarea", "label": "Message", "widthIntent": "full"},
                {"componentType": "submit-button", "label": "Send", "widthIntent": "compact"},
            ],
        }
    )
    governance = _governance_payload()
    runtime_context = {"canvas": {"width": 1366, "height": 768, "gridSize": 8}}

    first_definition, _ = compile_semantic_plan_to_definition(
        semantic,
        runtime_context=runtime_context,
        capability_policy_json=governance["capabilityPolicyJson"],
        width_policy_json=governance["widthClassPolicyJson"],
        capability_snapshot_json=governance["componentCapabilitySnapshotJson"],
        validation_contracts=governance["validationContracts"],
    )
    second_definition, _ = compile_semantic_plan_to_definition(
        semantic,
        runtime_context=runtime_context,
        capability_policy_json=governance["capabilityPolicyJson"],
        width_policy_json=governance["widthClassPolicyJson"],
        capability_snapshot_json=governance["componentCapabilitySnapshotJson"],
        validation_contracts=governance["validationContracts"],
    )

    assert first_definition == second_definition


def test_story_631_service_ignores_legacy_coordinates_and_compiles_layout(monkeypatch):
    # Legacy-shaped output with impossible coordinates must be transformed into compiler-owned layout.
    legacy_definition = {
        "schemaVersion": "1.0",
        "formId": "legacy-1",
        "theme": {"primaryColor": "#000", "backgroundColor": "#fff", "fontFamily": "Inter"},
        "canvasSettings": {"width": 500, "height": 400, "gridSize": 8},
        "pages": [
            {
                "id": "page-1",
                "title": "Legacy",
                "components": [
                    {
                        "id": "txt-1",
                        "type": "textarea",
                        "props": {"label": "Feedback"},
                        "position": {"x": 9999, "y": 9999},
                        "style": {"width": 9999, "height": 200},
                    },
                    {
                        "id": "submit-1",
                        "type": "submit-button",
                        "props": {"label": "Submit"},
                        "position": {"x": 9999, "y": 9999},
                        "style": {"width": 9999, "height": 72},
                    },
                ],
            }
        ],
    }

    monkeypatch.setattr(service, "_request_chatgpt_completion", lambda *args, **kwargs: json.dumps(legacy_definition))
    monkeypatch.setattr(
        service,
        "_resolve_runtime_governance_versions",
        lambda _db: {
            **_governance_payload(),
            "promptTemplateVersionId": 1,
            "promptTemplateVersionRef": "1:v1",
            "promptAssemblyProfileId": 1,
            "promptAssemblyProfileRef": "default:semantic-plan",
            "capabilityPolicyVersionId": 1,
            "capabilityPolicyVersionRef": "baseline:v1",
            "componentCapabilitySnapshotId": 1,
            "componentCapabilitySnapshotRef": "snapshot-v1",
            "widthClassPolicyVersionId": 1,
            "widthClassPolicyVersionRef": "width:v1",
            "validationContractVersion": "contracts-test",
            "governanceResolutionSource": "db-active",
        },
    )

    result = service.generate_form_definition(
        "Build feedback form",
        runtime_context={"canvas": {"width": 500, "height": 400, "gridSize": 8}},
        max_system_correction_attempts=0,
        db_session=None,
    )

    # Result should be a successful, deterministic-grid compilation. The
    # compiler legitimately grows the canvas vertically to fit the
    # textarea + submit (with rendered-footprint heights), and the boundary
    # validator now respects the compiled canvas height — so what used to
    # fail with a phantom out-of-bounds is now a genuine pass.
    assert result.status == "completed"
    assert result.trace.compilerMode == "deterministic-grid"
    assert result.definitionJSON is not None
    components = result.definitionJSON["pages"][0]["components"]
    assert all(component["position"]["x"] < 1000 for component in components)
    assert all(component["position"]["y"] < 1000 for component in components)


def test_story_631_semantic_plan_tolerates_story_version_and_validation_list_shape():
    # Reproduces the exact LLM payload from UAT request 0cfa6871: semanticPlanVersion="6.3.1"
    # and validationIntent emitted as a list of strings. Both must be coerced into the schema.
    plan = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "6.3.1",
            "formId": "tech-conference-registration",
            "title": "Tech Conference Registration",
            "components": [
                {
                    "componentType": "first-name",
                    "label": "First name",
                    "widthIntent": "half",
                    "validationIntent": ["required"],
                },
                {
                    "componentType": "email",
                    "label": "Email address",
                    "widthIntent": "half",
                    "validationIntent": ["required", "email"],
                },
                {
                    "componentType": "phone",
                    "label": "Phone number",
                    "widthIntent": "half",
                    "validationIntent": {"required": True, "format": "phone"},
                },
            ],
        }
    )

    assert plan.semanticPlanVersion == "1.0"
    first_name = plan.components[0].validationIntent
    email = plan.components[1].validationIntent
    phone = plan.components[2].validationIntent
    assert first_name is not None and first_name.required is True
    assert email is not None and email.required is True and email.email is True
    assert phone is not None and phone.required is True and phone.phone is True


def test_story_631_service_rebrands_parse_failure_and_invokes_correction_loop(monkeypatch):
    # First model reply returns a non-JSON payload. Story 6.3.1 (failure-mode
    # separation) routes this to the dedicated json-parse phase with its own
    # correction prompt and terminalReason="json-parse-failed" rather than
    # the catch-all semantic-plan-invalid that used to swallow it.
    call_count = {"n": 0}

    def fake_provider(messages, *args, **kwargs):
        call_count["n"] += 1
        if call_count["n"] == 1:
            # Not JSON at all → triggers ValueError from _extract_json_candidate
            return "this is not json at all"
        # Second attempt: still broken so we land on terminal json-parse-failed.
        return "still not json"

    monkeypatch.setattr(service, "_request_chatgpt_completion", fake_provider)
    monkeypatch.setattr(
        service,
        "_resolve_runtime_governance_versions",
        lambda _db: {
            **_governance_payload(),
            "promptTemplateVersionId": 1,
            "promptTemplateVersionRef": "1:v1",
            "promptAssemblyProfileId": 1,
            "promptAssemblyProfileRef": "default:semantic-plan",
            "capabilityPolicyVersionId": 1,
            "capabilityPolicyVersionRef": "baseline:v1",
            "componentCapabilitySnapshotId": 1,
            "componentCapabilitySnapshotRef": "snapshot-v1",
            "widthClassPolicyVersionId": 1,
            "widthClassPolicyVersionRef": "width:v1",
            "validationContractVersion": "contracts-test",
            "governanceResolutionSource": "db-active",
        },
    )

    result = service.generate_form_definition(
        "Build a feedback form",
        runtime_context={"canvas": {"width": 1280, "height": 800, "gridSize": 8}},
        max_system_correction_attempts=1,
        db_session=None,
    )

    assert result.status == "failed"
    assert result.trace.terminalReason == "json-parse-failed"
    assert result.trace.failureClass == "llm-fault"
    assert call_count["n"] == 2, "correction loop should have called the provider twice"
    assert len(result.trace.attempts) == 2
    for attempt in result.trace.attempts:
        assert attempt.notes is not None and attempt.notes.startswith("json-parse-failed:")
        assert attempt.failedAt == "json-parse"
        assert attempt.compileDiagnostics is not None
        assert "jsonParseError" in attempt.compileDiagnostics


# --- Story 6.3.1 UAT compiler-gap close (items 1-3) ---


def _governance_payload_with_max_length() -> dict:
    """Variant governance payload that allows maxLength on text/email/phone.

    The base _governance_payload() does not list these component types, so the
    compiler would not normalize a maxLength rule into props.validation. The
    width-cap test needs a concrete maxLength to exercise the content path.
    """
    payload = _governance_payload()
    payload["validationContracts"] = list(payload["validationContracts"]) + [
        {"componentType": "text", "allowedRules": ["required", "maxLength"]},
        {"componentType": "email", "allowedRules": ["required", "email", "maxLength"]},
        {"componentType": "phone", "allowedRules": ["required", "phone", "maxLength"]},
    ]
    payload["componentCapabilitySnapshotJson"]["components"].extend(
        [
            {"type": "text", "widthClasses": ["compact", "half", "full"]},
            {"type": "email", "widthClasses": ["compact", "half", "full"]},
            {"type": "phone", "widthClasses": ["compact", "half", "full"]},
        ]
    )
    return payload


def test_story_631_post_processing_skipped_for_deterministic_grid(monkeypatch):
    """When compilerMode == 'deterministic-grid' the destructive post-processing
    transforms (rebalance + sync-style-into-props) must be skipped by default,
    and the trace must record that decision through compileSummary.postProcessingApplied."""
    semantic_plan_payload = {
        "semanticPlanVersion": "1.0",
        "formId": "pp-skip-1",
        "title": "Post-Processing Skip",
        "components": [
            {"componentType": "header", "label": "Welcome", "widthIntent": "full"},
            {"componentType": "textarea", "label": "Notes", "widthIntent": "full"},
            {
                "componentType": "submit-button",
                "label": "Submit",
                "widthIntent": "compact",
                "actionAlignment": "center",
            },
        ],
    }
    monkeypatch.setattr(
        service,
        "_request_chatgpt_completion",
        lambda *args, **kwargs: json.dumps(semantic_plan_payload),
    )
    monkeypatch.setattr(
        service,
        "_resolve_runtime_governance_versions",
        lambda _db: {
            **_governance_payload(),
            "promptTemplateVersionId": 1,
            "promptTemplateVersionRef": "1:v1",
            "promptAssemblyProfileId": 1,
            "promptAssemblyProfileRef": "default:semantic-plan",
            "capabilityPolicyVersionId": 1,
            "capabilityPolicyVersionRef": "baseline:v1",
            "componentCapabilitySnapshotId": 1,
            "componentCapabilitySnapshotRef": "snapshot-v1",
            "widthClassPolicyVersionId": 1,
            "widthClassPolicyVersionRef": "width:v1",
            "validationContractVersion": "contracts-test",
            "governanceResolutionSource": "db-active",
        },
    )

    # Ensure no env override forces the destructive transforms back on for this test.
    monkeypatch.delenv("FORM_AI_PP_REBALANCE", raising=False)
    monkeypatch.delenv("FORM_AI_PP_SYNC_STYLE_PROPS", raising=False)

    # Compute the geometry the compiler will produce so we can assert the
    # post-processed output is byte-equal (no rebalance/y-shuffle).
    plan = FormSemanticPlan.model_validate(semantic_plan_payload)
    governance = _governance_payload()
    expected_definition, expected_summary = compile_semantic_plan_to_definition(
        plan,
        runtime_context={"canvas": {"width": 1920, "height": 980, "gridSize": 8}},
        capability_policy_json=governance["capabilityPolicyJson"],
        width_policy_json=governance["widthClassPolicyJson"],
        capability_snapshot_json=governance["componentCapabilitySnapshotJson"],
        validation_contracts=governance["validationContracts"],
    )

    # Prompt deliberately mentions "heading" so the always-on heading filter
    # keeps the header component; this isolates the assertion to the rebalance
    # behavior we actually want to verify.
    result = service.generate_form_definition(
        "Build a welcome form with a heading and a notes section.",
        runtime_context={"canvas": {"width": 1920, "height": 980, "gridSize": 8}},
        max_system_correction_attempts=0,
        db_session=None,
    )

    assert result.definitionJSON is not None
    expected_components = expected_definition["pages"][0]["components"]
    actual_components = result.definitionJSON["pages"][0]["components"]
    expected_y = {c["id"]: c["position"]["y"] for c in expected_components}
    actual_y = {c["id"]: c["position"]["y"] for c in actual_components}
    assert actual_y == expected_y, "rebalance must not move compiler-set y positions"

    # Heights must also match: rebalance would normally rewrite style.height.
    expected_h = {c["id"]: c["style"]["height"] for c in expected_components}
    actual_h = {c["id"]: c["style"]["height"] for c in actual_components}
    assert actual_h == expected_h

    summary = result.trace.compileSummary or {}
    applied = summary.get("postProcessingApplied")
    assert applied is not None, "compileSummary must surface postProcessingApplied"
    assert applied["rebalance"] is False
    assert applied["syncStyleProps"] is False
    # Heading filter + tab order remain on by default.
    assert applied["headingFilter"] is True
    assert applied["tabOrder"] is True
    # Sanity: confirm we exercised the same compiler input both times.
    assert summary.get("inputComponentCount") == expected_summary["inputComponentCount"]


def test_story_631_compiler_honors_section_and_row_group():
    """Two components sharing rowGroup must land on the same y; a third
    component in a different rowGroup AND a different section must start a
    new y. Phase 1 W2 rule: section-gap multiplier only fires when the
    *previous* section had 2+ rows — single-row sections add base gap only."""
    semantic = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "formId": "grouping-1",
            "components": [
                {
                    "componentType": "text",
                    "label": "First name",
                    "widthIntent": "half",
                    "section": "contact",
                    "rowGroup": "name",
                },
                {
                    "componentType": "text",
                    "label": "Last name",
                    "widthIntent": "half",
                    "section": "contact",
                    "rowGroup": "name",
                },
                {
                    "componentType": "text",
                    "label": "Street address",
                    "widthIntent": "full",
                    "section": "shipping",
                    "rowGroup": "address",
                },
            ],
        }
    )
    governance = _governance_payload_with_max_length()
    definition, compile_summary = compile_semantic_plan_to_definition(
        semantic,
        runtime_context={"canvas": {"width": 1920, "height": 980, "gridSize": 8}},
        capability_policy_json=governance["capabilityPolicyJson"],
        width_policy_json=governance["widthClassPolicyJson"],
        capability_snapshot_json=governance["componentCapabilitySnapshotJson"],
        validation_contracts=governance["validationContracts"],
    )

    components = {c["props"]["label"]: c for c in definition["pages"][0]["components"]}
    first_name = components["First name"]
    last_name = components["Last name"]
    address = components["Street address"]

    # Same rowGroup -> same y.
    assert first_name["position"]["y"] == last_name["position"]["y"]
    # Different x: side-by-side packing inside the row.
    assert first_name["position"]["x"] != last_name["position"]["x"]

    # Previous section ('contact') had only 1 row (name pair on same y), so
    # the W2 section-gap multiplier must NOT fire when crossing into 'shipping'.
    # Address y should be exactly name_row_bottom + DEFAULT_ROW_GAP.
    name_row_bottom = first_name["position"]["y"] + first_name["style"]["height"]
    expected_address_y = name_row_bottom + 24
    assert address["position"]["y"] == expected_address_y, (
        f"single-row section transition must use base gap only; got "
        f"address.y={address['position']['y']}, expected {expected_address_y}"
    )

    assert compile_summary["sectionCount"] == 2
    assert compile_summary["rowGroupCount"] == 2


def test_story_631_section_gap_does_not_fire_after_multi_row_section():
    """UAT round 5 (run 40) reversed the W2 rule: the user explicitly
    requested uniform inter-row gaps:

      "Based on our calculation method the gap at the top and inbetween should
       be identical?"

    ``SECTION_GAP_MULTIPLIER`` is now ``1.0`` so a section change after a
    multi-row section no longer adds extra leading space — every gap is
    exactly ``DEFAULT_ROW_GAP``. This test pins that behaviour against
    accidental reverts to the old 2.0 multiplier (which produced 48 px gaps
    between sections while the rest of the form used 24 px)."""
    semantic = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "formId": "section-multi-row",
            "components": [
                # 'contact' section: 2 rows of name+name, then phone+email.
                {"componentType": "text", "label": "First name",
                 "widthIntent": "half", "section": "contact", "rowGroup": "name",
                 "validationIntent": {"required": True, "maxLength": 40}},
                {"componentType": "text", "label": "Last name",
                 "widthIntent": "half", "section": "contact", "rowGroup": "name",
                 "validationIntent": {"required": True, "maxLength": 40}},
                {"componentType": "phone", "label": "Phone",
                 "widthIntent": "half", "section": "contact", "rowGroup": "ct",
                 "validationIntent": {"required": True, "phone": True, "maxLength": 20}},
                {"componentType": "email", "label": "Email",
                 "widthIntent": "half", "section": "contact", "rowGroup": "ct",
                 "validationIntent": {"required": True, "email": True, "maxLength": 80}},
                # 'address' section: a single textarea — extra section gap fires
                # before this because the *previous* section had 2 rows.
                {"componentType": "textarea", "label": "Notes",
                 "widthIntent": "full", "section": "notes",
                 "validationIntent": {"maxLength": 1000}},
            ],
        }
    )
    governance = _governance_payload_with_max_length()
    definition, _summary = compile_semantic_plan_to_definition(
        semantic,
        runtime_context={"canvas": {"width": 1920, "height": 980, "gridSize": 8}},
        capability_policy_json=governance["capabilityPolicyJson"],
        width_policy_json=governance["widthClassPolicyJson"],
        capability_snapshot_json=governance["componentCapabilitySnapshotJson"],
        validation_contracts=governance["validationContracts"],
    )

    by_label = {c["props"]["label"]: c for c in definition["pages"][0]["components"]}
    phone = by_label["Phone"]
    notes = by_label["Notes"]
    contact_row_bottom = phone["position"]["y"] + phone["style"]["height"]
    # Uniform-gap policy: only DEFAULT_ROW_GAP separates section boundaries.
    expected_notes_y = contact_row_bottom + 24
    assert notes["position"]["y"] == expected_notes_y, (
        f"section change after a multi-row section must use DEFAULT_ROW_GAP "
        f"(uniform-gap policy); got notes.y={notes['position']['y']}, "
        f"expected {expected_notes_y}"
    )


def test_story_631_compiler_caps_width_by_max_length():
    """A small ``maxLength`` content hint (well below the type's tier target)
    must shrink the resolved width and surface ``widthSource='content-cap'``
    in stage diagnostics. Phase 1 W1 behavior: the tier owns the natural
    width; ``validationIntent.maxLength`` shrinks (never grows) the target."""
    semantic = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "formId": "width-cap-1",
            "components": [
                {
                    # 15-char maxLength field (e.g. a short product code) —
                    # content_hint ~ 15*9 + 32 = 167 px. Well below the email
                    # tier target of 360 so content-cap must fire.
                    "componentType": "email",
                    "label": "Code",
                    "widthIntent": "half",
                    "validationIntent": {"required": True, "email": True, "maxLength": 15},
                }
            ],
        }
    )
    governance = _governance_payload_with_max_length()
    definition, compile_summary = compile_semantic_plan_to_definition(
        semantic,
        runtime_context={"canvas": {"width": 1920, "height": 980, "gridSize": 8}},
        capability_policy_json=governance["capabilityPolicyJson"],
        width_policy_json=governance["widthClassPolicyJson"],
        capability_snapshot_json=governance["componentCapabilitySnapshotJson"],
        validation_contracts=governance["validationContracts"],
    )

    email_component = definition["pages"][0]["components"][0]
    assert email_component["type"] == "email"
    # tier_target=360, content_hint~167 so target shrinks below 360.
    assert email_component["style"]["width"] < 360
    # Floor enforcement: must remain at or above email tier_min (240). The
    # content_hint is below tier_min but min_px clamps target up.
    assert email_component["style"]["width"] >= 167

    diag = compile_summary["stageDiagnostics"][0]
    assert diag["widthSource"] == "content-cap"
    assert diag["maxLengthHint"] == 15
    # New tier-derived diagnostics fields surfaced for ops triage.
    assert diag["widthMinPx"] >= 167
    assert diag["widthTargetPx"] == diag["widthPx"]


def test_story_631_width_floor_inflation_does_not_overlap_neighbour():
    """Regression: when content-cap shrinks span (e.g. phone with maxLength=20
    snaps to span=2 ~287px) but the component's width_floor (default 320px for
    non-submit) inflates the *visual* width past the span-derived width, the
    next item in the same rowGroup must not start inside the inflated tail.

    Surfaced by the 10-prompt UAT spot-check: phone+email sharing rowGroup
    ('contact') overlapped by ~9px on a 1920 canvas because email's x was
    computed from col_width*used_span (using the phone's pre-floor span)
    instead of the post-floor visual width.
    """
    semantic = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "formId": "floor-vs-span-1",
            "components": [
                {
                    "componentType": "phone",
                    "label": "Phone number",
                    "widthIntent": "half",
                    "section": "contact",
                    "rowGroup": "contact",
                    "validationIntent": {"required": True, "phone": True, "maxLength": 20},
                },
                {
                    "componentType": "email",
                    "label": "Email address",
                    "widthIntent": "half",
                    "section": "contact",
                    "rowGroup": "contact",
                    "validationIntent": {"required": True, "email": True, "maxLength": 80},
                },
            ],
        }
    )
    governance = _governance_payload_with_max_length()
    definition, _summary = compile_semantic_plan_to_definition(
        semantic,
        runtime_context={"canvas": {"width": 1920, "height": 980, "gridSize": 8}},
        capability_policy_json=governance["capabilityPolicyJson"],
        width_policy_json=governance["widthClassPolicyJson"],
        capability_snapshot_json=governance["componentCapabilitySnapshotJson"],
        validation_contracts=governance["validationContracts"],
    )

    components = definition["pages"][0]["components"]
    phone = next(c for c in components if c["type"] == "phone")
    email = next(c for c in components if c["type"] == "email")

    assert phone["position"]["y"] == email["position"]["y"], (
        "phone and email share rowGroup='contact' so they must land on the same y"
    )
    phone_right = phone["position"]["x"] + phone["style"]["width"]
    assert email["position"]["x"] >= phone_right, (
        f"email left edge {email['position']['x']} must not start before "
        f"phone right edge {phone_right} (visual overlap)"
    )


def test_story_631_submit_button_stays_within_canvas():
    """On a narrow canvas, the tier-based width resolver shrinks the submit
    button's max_px to ``content_width`` (=170 on a 250-canvas), so the
    button fits naturally without needing the constraint-pass clamp. The
    button must render fully inside the canvas regardless of how the cap is
    achieved."""
    semantic = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "formId": "submit-clamp-1",
            "components": [
                {
                    "componentType": "submit-button",
                    "label": "Submit",
                    "widthIntent": "compact",
                    "actionAlignment": "center",
                }
            ],
        }
    )
    governance = _governance_payload()
    definition, compile_summary = compile_semantic_plan_to_definition(
        semantic,
        # Narrow canvas: content area is 250 - 2*40 = 170, smaller than the
        # submit tier target of 280. The Phase 1 tier resolver caps max_px at
        # content_width and target_px collapses to 170 — no overflow ever
        # reaches the constraint pass.
        runtime_context={"canvas": {"width": 250, "height": 400, "gridSize": 8}},
        capability_policy_json=governance["capabilityPolicyJson"],
        width_policy_json=governance["widthClassPolicyJson"],
        capability_snapshot_json=governance["componentCapabilitySnapshotJson"],
        validation_contracts=governance["validationContracts"],
    )

    canvas_width = definition["canvasSettings"]["width"]
    submit = definition["pages"][0]["components"][0]
    right_edge = submit["position"]["x"] + submit["style"]["width"]
    assert right_edge <= canvas_width - 40, (
        f"submit-button right edge {right_edge} must not exceed content_right "
        f"{canvas_width - 40}"
    )
    assert submit["position"]["x"] >= 40
    # With the tier resolver the width fits naturally; no clamp needs to fire.
    assert compile_summary["submitButtonClamped"] is False


# Story 6.3.1 UAT round 5 — render-then-measure (two-phase compile) tests.
#
# These exercise the new ``measured_heights`` argument on
# ``compile_semantic_plan_to_definition``. The flow they protect:
#
#   1. /generate compiles with per-type estimates → first-pass DefinitionJSON.
#   2. Frontend renders that JSON, measures each component's actual DOM
#      height, and POSTs the measurements to /remeasure.
#   3. /remeasure recompiles with the same semantic plan + measured_heights,
#      so the layout solver places rows using ground-truth heights instead
#      of estimates that disagree with the renderer.
#
# Failures these tests catch:
#   * Compiler ignores the measurement and falls back to the estimate.
#   * Compiler trusts garbage (zero / negative) measurements.
#   * compileSummary.heightsSource doesn't reflect what actually happened
#     (estimated vs measured vs mixed) — the trace would lose the audit
#     trail that distinguishes a first-pass run from a remeasure pass.


def test_story_631_compiler_uses_measured_height_when_provided():
    """Ground-truth measurements override per-type estimates.

    Repro of Prompt 6: an 8-option checkbox is estimated at ~131 px but the
    visual validator sees ~220 px once rendered, causing a downstream
    collision with the next row. ``measured_heights`` must win so the
    layout solver reserves the real height.
    """
    # Distinct rowGroups so the layout solver keeps them on separate rows
    # (the wide test canvas would otherwise pack them side-by-side, which
    # hides the vertical-stacking effect we're trying to assert).
    semantic = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "formId": "remeasure-checkbox-1",
            "title": "Checkbox remeasure",
            "components": [
                {
                    "componentType": "checkbox",
                    "label": "Pick interests",
                    "widthIntent": "full",
                    "rowGroup": "row-a",
                    "options": [
                        {"label": f"Option {i}", "value": f"opt{i}"} for i in range(8)
                    ],
                },
                {
                    "componentType": "textarea",
                    "label": "Anything else?",
                    "widthIntent": "full",
                    "rowGroup": "row-b",
                },
            ],
        }
    )
    governance = _governance_payload()
    governance["componentCapabilitySnapshotJson"]["components"].append(
        {"type": "checkbox", "widthClasses": ["full"]}
    )
    governance["validationContracts"].append(
        {"componentType": "checkbox", "allowedRules": ["required"]}
    )

    # First pass: no measurements → per-type estimate.
    estimated_def, estimated_summary = compile_semantic_plan_to_definition(
        semantic,
        runtime_context={"canvas": {"width": 1920, "height": 980, "gridSize": 8}},
        capability_policy_json=governance["capabilityPolicyJson"],
        width_policy_json=governance["widthClassPolicyJson"],
        capability_snapshot_json=governance["componentCapabilitySnapshotJson"],
        validation_contracts=governance["validationContracts"],
    )
    estimated_checkbox = next(
        c for c in estimated_def["pages"][0]["components"] if c["type"] == "checkbox"
    )
    estimated_textarea = next(
        c for c in estimated_def["pages"][0]["components"] if c["type"] == "textarea"
    )
    estimated_height = estimated_checkbox["style"]["height"]
    estimated_textarea_y = estimated_textarea["position"]["y"]

    # Second pass: simulate the frontend reporting "checkbox actually rendered
    # at 320px" (well above the per-type estimate). Textarea uses an estimate.
    measured_height = 320
    refined_def, refined_summary = compile_semantic_plan_to_definition(
        semantic,
        runtime_context={"canvas": {"width": 1920, "height": 980, "gridSize": 8}},
        capability_policy_json=governance["capabilityPolicyJson"],
        width_policy_json=governance["widthClassPolicyJson"],
        capability_snapshot_json=governance["componentCapabilitySnapshotJson"],
        validation_contracts=governance["validationContracts"],
        measured_heights={estimated_checkbox["id"]: measured_height},
    )
    refined_checkbox = next(
        c for c in refined_def["pages"][0]["components"] if c["type"] == "checkbox"
    )
    refined_textarea = next(
        c for c in refined_def["pages"][0]["components"] if c["type"] == "textarea"
    )

    assert refined_checkbox["style"]["height"] == measured_height, (
        "checkbox height must come from the measured value, not the estimate"
    )
    assert refined_checkbox["style"]["height"] > estimated_height, (
        "sanity: the measured height in this test should be larger than the estimate"
    )
    # Crucial: the next row must shift down to make room for the taller
    # checkbox — this is the collision fix.
    assert refined_textarea["position"]["y"] > estimated_textarea_y, (
        f"textarea must be pushed down once checkbox is taller; "
        f"estimated_y={estimated_textarea_y} refined_y={refined_textarea['position']['y']}"
    )

    # Trace fields must distinguish the two passes.
    assert estimated_summary["heightsSource"] == "estimated"
    assert estimated_summary["measuredComponentCount"] == 0
    assert estimated_summary["estimatedComponentCount"] >= 2

    # Mixed: only the checkbox was measured; textarea + submit-button etc.
    # remain estimated. ``"mixed"`` is the right label, not ``"measured"``.
    assert refined_summary["heightsSource"] == "mixed"
    assert refined_summary["measuredComponentCount"] == 1
    assert refined_summary["estimatedComponentCount"] >= 1


def test_story_631_compiler_ignores_invalid_measured_heights():
    """Zero/negative measurements must fall back to the per-type estimate.

    The ``/remeasure`` schema ``gt=0`` validator already rejects bad
    payloads at the API edge, but the compiler must also be defensive:
    nothing downstream should ever produce a 0-height component just
    because a frontend rounding bug fed in junk.
    """
    semantic = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "formId": "remeasure-junk-1",
            "title": "Junk measurements",
            "components": [
                {"componentType": "header", "label": "Hi", "widthIntent": "full"},
                {
                    "componentType": "textarea",
                    "label": "Tell us more",
                    "widthIntent": "full",
                },
            ],
        }
    )
    governance = _governance_payload()

    baseline_def, _baseline_summary = compile_semantic_plan_to_definition(
        semantic,
        runtime_context={"canvas": {"width": 1200, "height": 800, "gridSize": 8}},
        capability_policy_json=governance["capabilityPolicyJson"],
        width_policy_json=governance["widthClassPolicyJson"],
        capability_snapshot_json=governance["componentCapabilitySnapshotJson"],
        validation_contracts=governance["validationContracts"],
    )
    baseline_textarea = next(
        c for c in baseline_def["pages"][0]["components"] if c["type"] == "textarea"
    )
    baseline_height = baseline_textarea["style"]["height"]

    # Feed the compiler garbage: 0, negative, NaN-string. None of these
    # should override the per-type estimate.
    refined_def, refined_summary = compile_semantic_plan_to_definition(
        semantic,
        runtime_context={"canvas": {"width": 1200, "height": 800, "gridSize": 8}},
        capability_policy_json=governance["capabilityPolicyJson"],
        width_policy_json=governance["widthClassPolicyJson"],
        capability_snapshot_json=governance["componentCapabilitySnapshotJson"],
        validation_contracts=governance["validationContracts"],
        measured_heights={
            baseline_textarea["id"]: 0,
            "non-existent-id": 999,
        },
    )
    refined_textarea = next(
        c for c in refined_def["pages"][0]["components"] if c["type"] == "textarea"
    )

    assert refined_textarea["style"]["height"] == baseline_height, (
        "0-height measurement must be ignored; estimate must win"
    )
    # Nothing was actually measured (0 is rejected, unknown id is irrelevant)
    # → trace must say ``estimated``, not ``mixed``.
    assert refined_summary["heightsSource"] == "estimated"
    assert refined_summary["measuredComponentCount"] == 0


def test_story_631_compile_summary_reports_measured_when_all_measured():
    """When every output component has a measurement, the trace must say
    ``"measured"`` (not ``"mixed"``). This is the happy-path label for a
    successful /remeasure round-trip and what the UAT replay tool keys off
    of when comparing first-pass vs second-pass diagnostics."""
    semantic = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "formId": "remeasure-allmeasured-1",
            "title": "All measured",
            "components": [
                {"componentType": "header", "label": "Hi", "widthIntent": "full"},
                {
                    "componentType": "submit-button",
                    "label": "Submit",
                    "widthIntent": "compact",
                    "actionAlignment": "center",
                },
            ],
        }
    )
    governance = _governance_payload()

    # First do a dry compile so we know the synthesised component ids
    # (header + submit-button get auto-ids in this fixture).
    pre_def, _ = compile_semantic_plan_to_definition(
        semantic,
        runtime_context={"canvas": {"width": 1200, "height": 800, "gridSize": 8}},
        capability_policy_json=governance["capabilityPolicyJson"],
        width_policy_json=governance["widthClassPolicyJson"],
        capability_snapshot_json=governance["componentCapabilitySnapshotJson"],
        validation_contracts=governance["validationContracts"],
    )
    measurements = {c["id"]: 90 for c in pre_def["pages"][0]["components"]}

    _refined_def, refined_summary = compile_semantic_plan_to_definition(
        semantic,
        runtime_context={"canvas": {"width": 1200, "height": 800, "gridSize": 8}},
        capability_policy_json=governance["capabilityPolicyJson"],
        width_policy_json=governance["widthClassPolicyJson"],
        capability_snapshot_json=governance["componentCapabilitySnapshotJson"],
        validation_contracts=governance["validationContracts"],
        measured_heights=measurements,
    )

    assert refined_summary["heightsSource"] == "measured"
    assert refined_summary["measuredComponentCount"] == len(measurements)
    assert refined_summary["estimatedComponentCount"] == 0


# ---------------------------------------------------------------------------
# Story 6.3.1 (UAT round 6) — Phase 2 layout-mode detection.
#
# These tests pin down the public contract of ``resolve_layout_mode`` and the
# new ``compileSummary.layoutMode`` field. The compiler still routes both
# modes to the same packed-rows code path for now (Phase 3 will branch on
# this); the only invariant we care about here is that the *trace* records
# what the runtime asked for so unimplemented branches are obvious.
# ---------------------------------------------------------------------------


def _trivial_semantic_plan() -> FormSemanticPlan:
    """Smallest plan that compiles cleanly. Used by layout-mode tests where
    we only care about ``compileSummary.layoutMode``, not the geometry."""
    return FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "formId": "layout-mode-test",
            "title": "Layout mode probe",
            "components": [
                {"componentType": "header", "label": "Hi", "widthIntent": "full"},
                {
                    "componentType": "submit-button",
                    "label": "Submit",
                    "widthIntent": "compact",
                    "actionAlignment": "center",
                },
            ],
        }
    )


def test_story_631_resolve_layout_mode_defaults_to_vertical_packed():
    """No runtime context, no globalStyles, junk values — all default to
    ``vertical-packed`` so a typo in stored config can never accidentally
    route to an unimplemented branch."""
    assert resolve_layout_mode(None) == LAYOUT_MODE_VERTICAL_PACKED
    assert resolve_layout_mode({}) == LAYOUT_MODE_VERTICAL_PACKED
    assert (
        resolve_layout_mode({"lockedGlobals": None}) == LAYOUT_MODE_VERTICAL_PACKED
    )
    assert (
        resolve_layout_mode({"lockedGlobals": {"globalStyles": None}})
        == LAYOUT_MODE_VERTICAL_PACKED
    )
    assert (
        resolve_layout_mode(
            {"lockedGlobals": {"globalStyles": {"defaultObjectLayout": "vertical"}}}
        )
        == LAYOUT_MODE_VERTICAL_PACKED
    )
    assert (
        resolve_layout_mode(
            {"lockedGlobals": {"globalStyles": {"defaultObjectLayout": "mixed"}}}
        )
        == LAYOUT_MODE_VERTICAL_PACKED
    )
    assert (
        resolve_layout_mode(
            {"lockedGlobals": {"globalStyles": {"defaultObjectLayout": None}}}
        )
        == LAYOUT_MODE_VERTICAL_PACKED
    )
    # Non-string token (defensive): a future config bug should not flip mode.
    assert (
        resolve_layout_mode(
            {"lockedGlobals": {"globalStyles": {"defaultObjectLayout": 1}}}
        )
        == LAYOUT_MODE_VERTICAL_PACKED
    )


def test_story_631_resolve_layout_mode_recognises_horizontal():
    """The literal string ``"horizontal"`` (case-insensitive, trimmed) is
    the only value that opts into ``horizontal-stacked``."""
    assert (
        resolve_layout_mode(
            {"lockedGlobals": {"globalStyles": {"defaultObjectLayout": "horizontal"}}}
        )
        == LAYOUT_MODE_HORIZONTAL_STACKED
    )
    assert (
        resolve_layout_mode(
            {"lockedGlobals": {"globalStyles": {"defaultObjectLayout": "HORIZONTAL"}}}
        )
        == LAYOUT_MODE_HORIZONTAL_STACKED
    )
    assert (
        resolve_layout_mode(
            {
                "lockedGlobals": {
                    "globalStyles": {"defaultObjectLayout": "  horizontal  "}
                }
            }
        )
        == LAYOUT_MODE_HORIZONTAL_STACKED
    )


def test_story_631_compile_summary_reports_vertical_packed_by_default():
    """Fresh runtime context with no layout signal must surface
    ``layoutMode = "vertical-packed"`` in the compile summary so the
    field is always present (downstream consumers can rely on it)."""
    semantic = _trivial_semantic_plan()
    governance = _governance_payload()

    _, compile_summary = compile_semantic_plan_to_definition(
        semantic,
        runtime_context={"canvas": {"width": 1920, "height": 980, "gridSize": 8}},
        capability_policy_json=governance["capabilityPolicyJson"],
        width_policy_json=governance["widthClassPolicyJson"],
        capability_snapshot_json=governance["componentCapabilitySnapshotJson"],
        validation_contracts=governance["validationContracts"],
    )
    assert compile_summary["layoutMode"] == LAYOUT_MODE_VERTICAL_PACKED


def test_story_631_compile_summary_reports_horizontal_stacked_when_requested():
    """When the runtime context ships ``defaultObjectLayout = "horizontal"``,
    ``compileSummary.layoutMode`` must reflect that — even though the
    geometry still falls back to the packed-rows path in Phase 2."""
    semantic = _trivial_semantic_plan()
    governance = _governance_payload()

    _, compile_summary = compile_semantic_plan_to_definition(
        semantic,
        runtime_context={
            "canvas": {"width": 1920, "height": 980, "gridSize": 8},
            "lockedGlobals": {
                "globalStyles": {"defaultObjectLayout": "horizontal"},
            },
        },
        capability_policy_json=governance["capabilityPolicyJson"],
        width_policy_json=governance["widthClassPolicyJson"],
        capability_snapshot_json=governance["componentCapabilitySnapshotJson"],
        validation_contracts=governance["validationContracts"],
    )
    assert compile_summary["layoutMode"] == LAYOUT_MODE_HORIZONTAL_STACKED


# ---------------------------------------------------------------------------
# Story 6.3.1 (UAT round 6) — Phase 2 *completion*: real horizontal-stacked
# compiler branch.
#
# The earlier Phase 2 invariant (``geometry must be byte-identical to
# vertical mode``) was a deliberately temporary scaffold so detection +
# LLM nudge could land first. Phase 2 *completion* implements the actual
# geometry, so the new invariant is the OPPOSITE: horizontal-mode geometry
# must DIFFER from vertical-mode geometry, in the specific shape we
# documented to the user (per-component full-row bounding boxes, single
# column, banner / submit special-cased).
# ---------------------------------------------------------------------------


def _horizontal_input_plan() -> FormSemanticPlan:
    """Plan with multiple INPUT components plus banner + submit so the
    horizontal-stacked branch's three code paths (banner, standard input,
    submit-button) all execute. Includes a ``rowGroup`` to verify that
    horizontal mode IGNORES grouping (each input still gets its own row).
    """
    return FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "formId": "horizontal-fixture",
            "title": "Horizontal layout probe",
            "components": [
                {
                    "componentType": "header",
                    "label": "Contact us",
                    "widthIntent": "full",
                },
                {
                    "componentType": "first-name",
                    "label": "First name",
                    "widthIntent": "compact",
                    # Both name fields share a rowGroup — a horizontal-mode
                    # compile must IGNORE that and put each on its own row.
                    "rowGroup": "name",
                },
                {
                    "componentType": "last-name",
                    "label": "Last name",
                    "widthIntent": "compact",
                    "rowGroup": "name",
                },
                {
                    "componentType": "email",
                    "label": "Email",
                    "widthIntent": "half",
                },
                {
                    "componentType": "submit-button",
                    "label": "Submit",
                    "widthIntent": "compact",
                    "actionAlignment": "left",
                },
            ],
        }
    )


def _compile(semantic, runtime_context):
    governance = _governance_payload()
    return compile_semantic_plan_to_definition(
        semantic,
        runtime_context=runtime_context,
        capability_policy_json=governance["capabilityPolicyJson"],
        width_policy_json=governance["widthClassPolicyJson"],
        capability_snapshot_json=governance["componentCapabilitySnapshotJson"],
        validation_contracts=governance["validationContracts"],
    )


_DESKTOP_RUNTIME = {"canvas": {"width": 1920, "height": 980, "gridSize": 8}}
_DESKTOP_RUNTIME_HORIZONTAL = {
    **_DESKTOP_RUNTIME,
    "lockedGlobals": {"globalStyles": {"defaultObjectLayout": "horizontal"}},
}


def test_story_631_horizontal_mode_changes_geometry_vs_vertical_mode():
    """Phase 2 *completion* invariant: horizontal mode produces a different
    layout than vertical mode for the same plan. (Replaces the earlier
    Phase-2-detection-only invariant which asserted byte-identical
    geometry; that scaffold has been retired.)"""
    semantic = _horizontal_input_plan()

    vertical_def, _ = _compile(semantic, _DESKTOP_RUNTIME)
    horizontal_def, _ = _compile(semantic, _DESKTOP_RUNTIME_HORIZONTAL)

    assert json.dumps(vertical_def["pages"], sort_keys=True) != json.dumps(
        horizontal_def["pages"], sort_keys=True
    ), "Horizontal mode must produce different geometry than vertical mode"


def test_story_631_horizontal_mode_places_each_input_on_its_own_row():
    """Single-column ordering: the two name fields share ``rowGroup="name"``
    in the plan, but horizontal-stacked mode ignores that and gives each
    input its own row. Verified by every standard input having a unique
    ``y`` coordinate (banner + submit-button are special-cased and may or
    may not share rows with other components — we exclude them)."""
    semantic = _horizontal_input_plan()
    horizontal_def, _ = _compile(semantic, _DESKTOP_RUNTIME_HORIZONTAL)
    components = horizontal_def["pages"][0]["components"]

    standard_inputs = [
        c for c in components
        if c["type"] not in {"header", "paragraph", "divider", "terms", "submit-button"}
    ]
    ys = [c["position"]["y"] for c in standard_inputs]
    assert len(ys) == len(set(ys)), (
        f"Inputs must each have their own row; got duplicate y values: {ys}"
    )


def test_story_631_horizontal_mode_standard_inputs_use_just_wide_enough_box():
    """Story 6.3.1 (UAT round 6) — Fix D: standard inputs in horizontal
    mode no longer span the full content row. They get a "just-wide-enough"
    bounding box equal to ``label_band + intra_gap + input_band + intra_gap
    + assumed_validation_band``, which is materially narrower than the
    content row on a wide canvas (desktop 1920) — that's the whole point
    of Fix D, since the previous full-row policy made the input column
    look squashed when the renderer's auto-split decided to stretch label
    + validation. Banner-style components (``header``, ``terms``) and the
    submit-button keep their special policies and are excluded.
    """
    from modules.form_ai.compiler import DEFAULT_MARGIN_X

    semantic = _horizontal_input_plan()
    horizontal_def, _ = _compile(semantic, _DESKTOP_RUNTIME_HORIZONTAL)
    canvas_width = horizontal_def["canvasSettings"]["width"]
    content_width = canvas_width - 2 * DEFAULT_MARGIN_X

    components = horizontal_def["pages"][0]["components"]
    for c in components:
        if c["type"] in {"submit-button", "header", "paragraph", "divider", "terms"}:
            continue
        assert c["style"]["width"] < content_width, (
            f"{c['type']!r} should use a just-wide-enough bounding box "
            f"(<{content_width}px), got {c['style']['width']}px — Fix D "
            f"removed the full-row policy for standard inputs."
        )
        assert c["position"]["x"] == DEFAULT_MARGIN_X, (
            f"{c['type']!r} should still pin to the left margin"
        )


def test_story_631_horizontal_mode_records_per_row_decisions_in_summary():
    """``rowSolverDecisions`` must include a horizontal-mode entry per
    component, with the documented ``decision`` strings + the new
    ``validationDroppedBelow`` and ``layoutMode`` fields. This is what
    powers the trace / replay tooling."""
    semantic = _horizontal_input_plan()
    _, summary = _compile(semantic, _DESKTOP_RUNTIME_HORIZONTAL)

    decisions = summary["rowSolverDecisions"]
    assert len(decisions) == len(semantic.components), (
        "One row decision per component in horizontal mode"
    )
    valid_decisions = {
        "horizontal-banner",
        "horizontal-submit",
        "horizontal-inline-validation",
        "horizontal-validation-below",
    }
    for d in decisions:
        assert d["decision"] in valid_decisions, f"Unknown decision: {d['decision']}"
        assert d["layoutMode"] == LAYOUT_MODE_HORIZONTAL_STACKED
        assert isinstance(d["validationDroppedBelow"], bool)


def test_story_631_horizontal_mode_drops_validation_below_on_narrow_canvas():
    """At the lower end of the supported horizontal-mode canvas width
    (just above the 600 px mobile threshold), there isn't room to fit
    ``[ Label ][ Input ][ Validation ]`` inline — the compiler must
    detect this and reserve extra height so the renderer can wrap
    validation below without colliding with the next row."""
    semantic = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "formId": "narrow-horizontal",
            "title": "Narrow horizontal probe",
            "components": [
                {"componentType": "email", "label": "Email", "widthIntent": "half"},
            ],
        }
    )
    runtime = {
        "canvas": {"width": 640, "height": 800, "gridSize": 8},
        "lockedGlobals": {"globalStyles": {"defaultObjectLayout": "horizontal"}},
    }
    _, summary = _compile(semantic, runtime)
    decisions = summary["rowSolverDecisions"]
    assert len(decisions) == 1
    assert decisions[0]["decision"] == "horizontal-validation-below", (
        "640px canvas should not have room for inline validation"
    )
    assert decisions[0]["validationDroppedBelow"] is True


def test_story_631_horizontal_mode_keeps_validation_inline_on_wide_canvas():
    """At desktop width (1920), every standard input has plenty of room
    for inline validation. None of the rows should drop validation below."""
    semantic = _horizontal_input_plan()
    _, summary = _compile(semantic, _DESKTOP_RUNTIME_HORIZONTAL)

    standard_decisions = [
        d for d in summary["rowSolverDecisions"]
        if d["decision"] not in {"horizontal-banner", "horizontal-submit"}
    ]
    for d in standard_decisions:
        assert d["decision"] == "horizontal-inline-validation", (
            f"Desktop width should keep validation inline; got {d['decision']}"
        )
        assert d["validationDroppedBelow"] is False


def test_story_631_fix_e_horizontal_mode_terms_uses_tight_box_not_full_row():
    """Story 6.3.1 (UAT round 7) — Fix E item 5: terms in horizontal mode
    used to render at the full content width (UAT round 6 routed it through
    the banner branch). The renderer's auto-tracked grid then spread the
    checkbox to the far left of the canvas, the consent text to the far
    right, and the validation message even further right — visually the
    consent looked like 3 unrelated controls.

    The new policy is a tight bounding box:
      box_width = checkbox_band + intra_gap + label_band + intra_gap + validation_band

    where the label band is sized to the consent text (label + link) instead
    of the form-wide ``horizontalLabelBandPx``. The terms branch also stamps
    ``inputWidthOverride``, ``labelWidthOverride`` and ``helpWidthOverride``
    so the renderer pins each column track and the 3 sub-objects pack
    together left-aligned at ``DEFAULT_MARGIN_X``.
    """
    from modules.form_ai.compiler import (
        DEFAULT_MARGIN_X,
        TERMS_CHECKBOX_BAND_PX,
        HORIZONTAL_INTRA_GAP_PX,
        HORIZONTAL_VALIDATION_MIN_PX,
    )

    semantic = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "formId": "terms-fixture",
            "title": "Marketing consent",
            "components": [
                {"componentType": "email", "label": "Email", "widthIntent": "half"},
                {
                    "componentType": "terms",
                    "label": "I agree to receive marketing emails",
                    "widthIntent": "full",
                    # Default registry termsLinkText is "Terms of Service" — the
                    # consent label band has to fit "label + link + space + *".
                },
                {
                    "componentType": "submit-button",
                    "label": "Sign up",
                    "widthIntent": "compact",
                },
            ],
        }
    )
    horizontal_def, summary = _compile(semantic, _DESKTOP_RUNTIME_HORIZONTAL)
    components = horizontal_def["pages"][0]["components"]
    content_width = horizontal_def["canvasSettings"]["width"] - 2 * DEFAULT_MARGIN_X

    terms = next(c for c in components if c["type"] == "terms")

    # Tight bounding box — must be < the full content width on a desktop
    # canvas (~1840 px), because the entire point of Fix E item 5 is to
    # avoid the 1000+ px of dead space that the old full-row policy created
    # between the checkbox and the consent text.
    assert terms["style"]["width"] < content_width, (
        f"Terms should now use a tight bounding box, not the full row; "
        f"got width={terms['style']['width']}, content_width={content_width}"
    )

    # Story 6.3.1 (UAT round 9) — Fix G item 3: bounding box is now
    # ``checkbox + gap + consent label + gap + validation column`` (inline,
    # not dropped below). Width is wider than F4 but still well below the
    # full content_width so the consent visually reads as a single grouped
    # control rather than spreading across the canvas.
    expected_minimum = (
        TERMS_CHECKBOX_BAND_PX
        + HORIZONTAL_INTRA_GAP_PX
        + 200  # consent-text band
        + HORIZONTAL_INTRA_GAP_PX
        + 200  # validation band (HORIZONTAL_VALIDATION_MIN_PX floor)
    )
    assert terms["style"]["width"] >= expected_minimum, (
        f"Terms box should be wide enough for "
        f"checkbox + consent label + inline validation; got "
        f"{terms['style']['width']}, expected at least {expected_minimum}"
    )

    # Left-aligned with the rest of the form so the column-of-checkboxes
    # visual stays consistent.
    assert terms["position"]["x"] == DEFAULT_MARGIN_X

    # Story 6.3.1 (UAT round 9) — Fix G item 3: terms still keeps its two
    # *structural* overrides because the renderer's flexColumnSet would
    # otherwise stretch the 32 px checkbox to fill the row and the
    # form-wide ``horizontalLabelBandPx`` would force the consent label
    # to wrap. ``helpWidthOverride`` is intentionally NOT stamped — the
    # validation column auto-grows to fit the message inside the wider
    # bounding box.
    assert terms["props"]["inputWidthOverride"] == TERMS_CHECKBOX_BAND_PX
    assert terms["props"]["labelWidthOverride"] > 0
    assert "helpWidthOverride" not in terms["props"], (
        "Fix G item 3: terms helpWidthOverride must NOT be pinned — the "
        "validation column auto-grows naturally inside the inline-validation "
        "bounding box."
    )

    # ``props.width`` is synced to the tight bounding box so the renderer's
    # ``hasExplicitWidth`` branch lays out the inline-grid at the correct
    # wrapper width.
    assert terms["props"].get("width") == f"{terms['style']['width']}px", (
        f"Terms props.width should match style.width; "
        f"got props.width={terms['props'].get('width')}, "
        f"style.width={terms['style']['width']}px"
    )

    # Decision string: Fix G reverts F4 — terms is inline-validation by
    # default and only switches to wrapped-validation when the inline
    # bounding box would exceed content_width.
    terms_decision = next(
        d for d in summary["rowSolverDecisions"]
        if "terms" in d["componentIds"][0]
    )
    assert terms_decision["decision"] == "horizontal-terms-inline-validation"
    assert terms_decision["validationDroppedBelow"] is False


def test_story_631_horizontal_mode_submit_button_respects_alignment():
    """Submit-button keeps its actionAlignment policy (left/right/center) in
    horizontal mode just like vertical mode — the user called this out as
    "special consideration" since it's the form's call-to-action."""
    from modules.form_ai.compiler import DEFAULT_MARGIN_X

    for alignment, expected_predicate in [
        ("left", lambda x, w, cw: x == DEFAULT_MARGIN_X),
        ("right", lambda x, w, cw: x + w == DEFAULT_MARGIN_X + cw),
        # Center alignment: midpoint of the button equals the midpoint of
        # the content row (within rounding).
        ("center", lambda x, w, cw: abs((x + w / 2) - (DEFAULT_MARGIN_X + cw / 2)) <= 1),
    ]:
        semantic = FormSemanticPlan.model_validate(
            {
                "semanticPlanVersion": "1.0",
                "formId": f"submit-{alignment}",
                "title": "Submit alignment probe",
                "components": [
                    {
                        "componentType": "submit-button",
                        "label": "Submit",
                        "widthIntent": "compact",
                        "actionAlignment": alignment,
                    },
                ],
            }
        )
        definition, _ = _compile(semantic, _DESKTOP_RUNTIME_HORIZONTAL)
        canvas_width = definition["canvasSettings"]["width"]
        content_width = canvas_width - 2 * DEFAULT_MARGIN_X
        submit = definition["pages"][0]["components"][0]
        assert expected_predicate(
            submit["position"]["x"], submit["style"]["width"], content_width
        ), f"submit alignment={alignment!r} placed at x={submit['position']['x']}"


def test_story_631_horizontal_mode_stamps_form_wide_label_band_on_global_styles():
    """Story 6.3.1 (UAT round 6) — Fix C: horizontal-stacked compiles must
    publish a single form-wide ``globalStyles.horizontalLabelBandPx`` so the
    renderer can align every label across all components at the same input
    left-edge. The value must be a positive int within the documented clamp
    bounds and must also be surfaced on ``compileSummary.horizontalLabelBandPx``
    for trace consumers.
    """
    from modules.form_ai.compiler import (
        HORIZONTAL_LABEL_BAND_MAX_PX,
        HORIZONTAL_LABEL_BAND_MIN_PX,
    )

    semantic = _horizontal_input_plan()
    definition, summary = _compile(semantic, _DESKTOP_RUNTIME_HORIZONTAL)

    global_styles = definition.get("globalStyles")
    assert isinstance(global_styles, dict), (
        "Horizontal mode must emit a globalStyles object on the definition"
    )
    band_px = global_styles.get("horizontalLabelBandPx")
    assert isinstance(band_px, int) and band_px > 0, (
        f"horizontalLabelBandPx must be a positive int; got {band_px!r}"
    )
    assert HORIZONTAL_LABEL_BAND_MIN_PX <= band_px <= HORIZONTAL_LABEL_BAND_MAX_PX, (
        f"horizontalLabelBandPx must be clamped to "
        f"[{HORIZONTAL_LABEL_BAND_MIN_PX}, {HORIZONTAL_LABEL_BAND_MAX_PX}]; "
        f"got {band_px}"
    )

    assert summary.get("horizontalLabelBandPx") == band_px, (
        "compileSummary.horizontalLabelBandPx must mirror the value stamped "
        "on the definition so the trace and the form agree"
    )


def test_story_631_vertical_mode_does_not_stamp_horizontal_label_band():
    """Vertical-packed mode must NOT author ``globalStyles.horizontalLabelBandPx``
    — the band is a horizontal-mode-only knob and stamping it on a vertical
    form would (a) leak nonsense into ``definition.globalStyles`` and
    (b) confuse the frontend's reducer which only patches when the value is
    present. ``compileSummary.horizontalLabelBandPx`` must be ``None`` so the
    trace makes the skip explicit.
    """
    semantic = _horizontal_input_plan()
    definition, summary = _compile(semantic, _DESKTOP_RUNTIME)

    # Either no globalStyles key at all, or the key exists without the
    # horizontal-only knob — both are acceptable.
    global_styles = definition.get("globalStyles") or {}
    assert "horizontalLabelBandPx" not in global_styles, (
        "Vertical-packed mode must not stamp horizontalLabelBandPx; got "
        f"{global_styles.get('horizontalLabelBandPx')!r}"
    )
    assert summary.get("horizontalLabelBandPx") is None, (
        "compileSummary.horizontalLabelBandPx must be None in vertical mode"
    )


def test_story_631_horizontal_label_band_grows_with_longer_labels():
    """Sanity check on the estimator: a plan with a long label must produce
    a wider band than a plan with only short labels (within the clamp)."""
    short_plan = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "formId": "short-labels",
            "title": "Short labels",
            "components": [
                {"componentType": "first-name", "label": "Name", "widthIntent": "compact"},
                {"componentType": "email", "label": "Email", "widthIntent": "compact"},
            ],
        }
    )
    long_plan = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "formId": "long-labels",
            "title": "Long labels",
            "components": [
                {
                    "componentType": "first-name",
                    "label": "What is your full preferred display name?",
                    "widthIntent": "compact",
                },
                {"componentType": "email", "label": "Email", "widthIntent": "compact"},
            ],
        }
    )
    short_def, _ = _compile(short_plan, _DESKTOP_RUNTIME_HORIZONTAL)
    long_def, _ = _compile(long_plan, _DESKTOP_RUNTIME_HORIZONTAL)
    short_band = short_def["globalStyles"]["horizontalLabelBandPx"]
    long_band = long_def["globalStyles"]["horizontalLabelBandPx"]
    assert long_band >= short_band, (
        f"Longer-label plan should produce >= band width; got short={short_band}, long={long_band}"
    )


# ---------------------------------------------------------------------------
# Story 6.3.1 (UAT round 6) — Fix D: content-aware input bands in horizontal
# mode. The compiler must derive a per-component "comfortable" input width
# from the chars table + LLM ``validationIntent.maxLength``, stamp it on
# ``component.props.inputWidthOverride`` so the renderer's Fix B plumbing
# pins the input column to that pixel value, and shrink the bounding box
# to ``label_band + 2*intra_gap + input_band + assumed_validation_band``
# so the canvas right side is naturally empty (matches a designer's manual
# layout instead of the compiler's previous full-row policy).
# ---------------------------------------------------------------------------


def test_story_631_fix_d_input_band_estimator_uses_comfortable_chars_when_no_max_length():
    """When the LLM does not supply ``validationIntent.maxLength``, the
    estimator falls back to the per-type ``comfortable`` chars value and
    converts to pixels via ``chars * AVG_CHAR_PX + INPUT_BAND_PADDING_PX``.
    For ``email`` (comfortable=32, tier=(240, 360, 520)) this should land
    inside the tier — i.e. the tier clamp doesn't fire and we get exactly
    ``32 * 9 + 24 = 312 px``."""
    from modules.form_ai.compiler import (
        AVG_CHAR_PX,
        COMPONENT_WIDTH_TIERS,
        INPUT_BAND_PADDING_PX,
        INPUT_COMFORTABLE_CHARS,
        _estimate_horizontal_input_band_px,
    )

    comfortable, _ = INPUT_COMFORTABLE_CHARS["email"]
    tier = COMPONENT_WIDTH_TIERS["email"]
    expected = int(round(comfortable * AVG_CHAR_PX + INPUT_BAND_PADDING_PX))

    band = _estimate_horizontal_input_band_px("email", None, tier)
    assert band == expected, f"Email default band should be {expected}px, got {band}px"
    assert tier[0] <= band <= tier[2], "Default band should already sit inside the tier"


def test_story_631_fix_d_input_band_caps_at_hard_max_for_silly_max_length():
    """RFC 5321 lets emails be 254 chars. Rendering that wide would dominate
    the row, so the compiler caps at ``hard_max=80`` even when the LLM
    parrots back the spec maximum. After the cap the math is
    ``80 * 9 + 24 = 744 px`` which the email tier (max 520) clamps to 520
    — both clamps in series MUST kick in for the user's "80 char cap"
    requirement to actually bite."""
    from modules.form_ai.compiler import (
        COMPONENT_WIDTH_TIERS,
        _estimate_horizontal_input_band_px,
    )

    tier = COMPONENT_WIDTH_TIERS["email"]
    band_silly = _estimate_horizontal_input_band_px("email", 254, tier)
    band_at_cap = _estimate_horizontal_input_band_px("email", 80, tier)

    assert band_silly == band_at_cap, (
        "maxLength=254 should resolve to the same band as maxLength=80 "
        f"because hard_max caps at 80 chars; got 254→{band_silly}, 80→{band_at_cap}"
    )
    assert band_silly == int(round(tier[2])), (
        f"After the chars-cap the px-cap (tier max {tier[2]}) should also "
        f"fire and pin the band at the tier max, got {band_silly}px"
    )


def test_story_631_fix_d_input_band_honours_small_max_length_then_tier_min():
    """When the LLM supplies a small maxLength (e.g. 20 chars for an
    internal-code email field), the estimator uses it — but the tier's
    ``min`` still acts as a floor so the input control never collapses
    below a usable size. Email tier min is 240 px, and 20 chars = 204 px,
    so the resolved band must equal the tier min (240), not 204."""
    from modules.form_ai.compiler import (
        COMPONENT_WIDTH_TIERS,
        _estimate_horizontal_input_band_px,
    )

    tier = COMPONENT_WIDTH_TIERS["email"]
    band = _estimate_horizontal_input_band_px("email", 20, tier)
    assert band == int(round(tier[0])), (
        f"Tiny maxLength should be clamped UP to tier min ({tier[0]}px), "
        f"got {band}px"
    )


def test_story_631_fix_d_unknown_component_type_falls_back_to_tier_target():
    """Component types not in ``INPUT_COMFORTABLE_CHARS`` (e.g. checkbox,
    file-upload) — and not the rating special case — must defer to the
    tier's natural ``target`` rather than throwing or returning 0.

    Note: rating used to be the example here but Fix E item 4 added rating
    to the chars table (with a special icon-row sizing path), so we
    deliberately probe with a truly-unknown type instead.
    """
    from modules.form_ai.compiler import (
        COMPONENT_WIDTH_TIERS,
        _estimate_horizontal_input_band_px,
        INPUT_COMFORTABLE_CHARS,
    )

    # Pick a type that's known to the tier table but NOT in the chars
    # table — checkbox/file-upload are good probes because they're real
    # components the LLM can emit.
    candidate = "checkbox"
    assert candidate not in INPUT_COMFORTABLE_CHARS, (
        f"Test fixture assumes {candidate!r} stays out of INPUT_COMFORTABLE_CHARS"
    )
    tier = COMPONENT_WIDTH_TIERS.get(candidate, COMPONENT_WIDTH_TIERS["first-name"])
    band = _estimate_horizontal_input_band_px(candidate, None, tier)
    assert band == int(round(tier[1])), (
        f"Unknown type should fall back to tier.target ({tier[1]}px), "
        f"got {band}px"
    )


def test_story_631_fix_g_compiler_does_not_stamp_input_width_override_on_props():
    """Story 6.3.1 (UAT round 9) — Fix G "framework-first": standard inputs
    in horizontal mode must NOT have ``component.props.inputWidthOverride``
    stamped. The renderer's CSS Grid resolves the input column as
    ``minmax(0, 1fr)`` so users can drag-resize it via the standard
    Properties Panel without fighting a compiler-set pin (which had no
    panel affordance to clear).

    Terms is the one structural exception: its 32 px checkbox would be
    stretched to ``1fr`` if not pinned, so the override stays for terms.
    """
    semantic = _horizontal_input_plan()
    definition, _ = _compile(semantic, _DESKTOP_RUNTIME_HORIZONTAL)
    components = definition["pages"][0]["components"]

    for c in components:
        props = c.get("props", {}) or {}
        if c["type"] == "terms":
            # Structural pin: see Fix G item 3 commentary in compiler.py.
            assert "inputWidthOverride" in props, (
                "terms must keep its structural inputWidthOverride (32 px "
                "checkbox) so the renderer doesn't stretch the checkbox to "
                "fill the row"
            )
            continue
        assert "inputWidthOverride" not in props, (
            f"Fix G framework-first: {c['type']!r} must NOT have "
            f"inputWidthOverride stamped (got {props.get('inputWidthOverride')!r}). "
            "The input column is resolved via CSS Grid auto/1fr in the renderer "
            "so users can adjust via Appearance \u2192 Dimensions afterwards."
        )


def test_story_631_fix_g_box_width_includes_label_input_validation_budget():
    """The bounding box width that ships in ``style.width`` must STILL be
    sized as ``label_band + intra_gap + input_band + intra_gap +
    validation_band`` so the inline-grid renders without horizontal scroll
    even though we no longer stamp per-object pins. Verified by checking
    the box width is within a reasonable envelope of the budget — exact
    arithmetic is encapsulated by the internal estimators.
    """
    from modules.form_ai.compiler import (
        HORIZONTAL_INTRA_GAP_PX,
        HORIZONTAL_VALIDATION_MIN_PX,
        HORIZONTAL_VALIDATION_MAX_PX,
        COMPONENT_WIDTH_TIERS,
    )

    semantic = _horizontal_input_plan()
    definition, _ = _compile(semantic, _DESKTOP_RUNTIME_HORIZONTAL)
    components = definition["pages"][0]["components"]
    label_band = definition["globalStyles"]["horizontalLabelBandPx"]

    for c in components:
        if c["type"] in {"submit-button", "header", "paragraph", "divider", "terms"}:
            continue
        tier = COMPONENT_WIDTH_TIERS.get(c["type"])
        if tier is None:
            continue
        # Lower bound: label + gap + tier.min + gap + min validation
        floor = (
            label_band
            + HORIZONTAL_INTRA_GAP_PX
            + tier[0]
            + HORIZONTAL_INTRA_GAP_PX
            + HORIZONTAL_VALIDATION_MIN_PX
        )
        # Upper bound: label + gap + tier.max + gap + max validation
        ceiling = (
            label_band
            + HORIZONTAL_INTRA_GAP_PX
            + tier[2]
            + HORIZONTAL_INTRA_GAP_PX
            + HORIZONTAL_VALIDATION_MAX_PX
        )
        # textarea uses a wider tier so its ceiling can exceed normal —
        # widen the window for it.
        if c["type"] == "textarea":
            ceiling += 200
        assert floor - 5 <= c["style"]["width"] <= ceiling + 5, (
            f"{c['type']!r} box_width {c['style']['width']}px must sit "
            f"inside [{floor}, {ceiling}] (label {label_band} + gap "
            f"+ tier {tier} + gap + validation [MIN, MAX])"
        )


def test_story_631_fix_g_props_width_matches_style_width_for_standard_inputs():
    """Story 6.3.1 (UAT round 9) — Fix G2 props.width sync.

    The frontend canvas wrapper (``SortableComponent.displayWidth``) reads
    ``component.props.width`` to size the absolutely-positioned shell that
    contains the universal grid. Pre-Fix-G the wrapper width was kept in
    step with the bounding box by the ``inputWidthOverride`` expansion
    branch; with that override removed the compiler must instead sync
    ``props.width`` directly so the shell matches ``style.width``. Without
    this sync the renderer paints the inline-grid inside the earlier
    tier-based ``props.width`` (e.g. ``"359px"``), squeezing label+input+
    validation into a band narrower than the collision footprint.
    """
    semantic = _horizontal_input_plan()
    definition, _ = _compile(semantic, _DESKTOP_RUNTIME_HORIZONTAL)
    components = definition["pages"][0]["components"]

    for c in components:
        # Submit/header/paragraph/divider follow their own width contracts;
        # this guarantee covers the standard input row that benefits from
        # the bounding-box budget.
        if c["type"] in {"submit-button", "header", "paragraph", "divider"}:
            continue
        props_width = (c.get("props") or {}).get("width")
        assert isinstance(props_width, str) and props_width.endswith("px"), (
            f"{c['type']!r} should expose props.width as a px string for "
            f"the canvas wrapper, got {props_width!r}"
        )
        props_width_px = int(props_width.removesuffix("px"))
        assert props_width_px == c["style"]["width"], (
            f"{c['type']!r} props.width {props_width_px}px should equal "
            f"style.width {c['style']['width']}px so the canvas wrapper "
            f"matches the bounding box reserved for the inline grid"
        )


def test_story_631_fix_d_input_band_preset_compact_shrinks_inputs():
    """Story 6.3.1 (UAT round 6) — Fix D item 4: a "compact" preset on
    ``globalStyles.horizontalInputBandPreset`` must shrink the resolved
    input bands compared to "standard". The shrink stops at tier.min so
    a "compact" email never collapses below the email tier minimum."""
    semantic = _horizontal_input_plan()
    runtime_compact = {
        **_DESKTOP_RUNTIME,
        "lockedGlobals": {
            "globalStyles": {
                "defaultObjectLayout": "horizontal",
                "horizontalInputBandPreset": "compact",
            }
        },
    }
    runtime_standard = {
        **_DESKTOP_RUNTIME,
        "lockedGlobals": {
            "globalStyles": {
                "defaultObjectLayout": "horizontal",
                "horizontalInputBandPreset": "standard",
            }
        },
    }

    compact_def, _ = _compile(semantic, runtime_compact)
    standard_def, _ = _compile(semantic, runtime_standard)

    compact_email = next(
        c for c in compact_def["pages"][0]["components"] if c["type"] == "email"
    )
    standard_email = next(
        c for c in standard_def["pages"][0]["components"] if c["type"] == "email"
    )

    # Story 6.3.1 (UAT round 9) — Fix G: per-object overrides are no
    # longer stamped. Verify the preset effect via the bounding box
    # ``style.width`` (which still uses the preset multiplier internally
    # to compute the input band budget).
    assert compact_email["style"]["width"] <= standard_email["style"]["width"], (
        "Compact preset must produce smaller bounding boxes than standard; got "
        f"compact={compact_email['style']['width']}, "
        f"standard={standard_email['style']['width']}"
    )


def test_story_631_fix_d_input_band_preset_spacious_grows_inputs():
    """Story 6.3.1 (UAT round 6) — Fix D item 4: "spacious" preset must
    enlarge the input bands relative to "standard", capped at tier.max
    so even a spacious email cannot exceed the email tier maximum."""
    from modules.form_ai.compiler import COMPONENT_WIDTH_TIERS

    semantic = _horizontal_input_plan()
    runtime_spacious = {
        **_DESKTOP_RUNTIME,
        "lockedGlobals": {
            "globalStyles": {
                "defaultObjectLayout": "horizontal",
                "horizontalInputBandPreset": "spacious",
            }
        },
    }
    runtime_standard = {
        **_DESKTOP_RUNTIME,
        "lockedGlobals": {
            "globalStyles": {
                "defaultObjectLayout": "horizontal",
                "horizontalInputBandPreset": "standard",
            }
        },
    }

    spacious_def, _ = _compile(semantic, runtime_spacious)
    standard_def, _ = _compile(semantic, runtime_standard)

    spacious_email = next(
        c for c in spacious_def["pages"][0]["components"] if c["type"] == "email"
    )
    standard_email = next(
        c for c in standard_def["pages"][0]["components"] if c["type"] == "email"
    )
    email_tier_max = int(round(COMPONENT_WIDTH_TIERS["email"][2]))

    # Story 6.3.1 (UAT round 9) — Fix G: assert via style.width (input
    # override no longer stamped on props).
    assert spacious_email["style"]["width"] >= standard_email["style"]["width"], (
        "Spacious preset must produce larger bounding boxes than standard; got "
        f"spacious={spacious_email['style']['width']}, "
        f"standard={standard_email['style']['width']}"
    )
    # Tier-max clamp still applies internally; box width should be no
    # more than label_band + gaps + tier.max + validation.MAX.
    from modules.form_ai.compiler import (
        HORIZONTAL_INTRA_GAP_PX,
        HORIZONTAL_VALIDATION_MAX_PX,
    )
    label_band = spacious_def["globalStyles"]["horizontalLabelBandPx"]
    ceiling = (
        label_band
        + HORIZONTAL_INTRA_GAP_PX
        + email_tier_max
        + HORIZONTAL_INTRA_GAP_PX
        + HORIZONTAL_VALIDATION_MAX_PX
    )
    assert spacious_email["style"]["width"] <= ceiling, (
        "Spacious bounding box must respect tier.max + validation.MAX ceiling; "
        f"got {spacious_email['style']['width']}, ceiling {ceiling}"
    )


def test_story_631_fix_d_unknown_preset_falls_back_to_standard_multiplier():
    """A typo or future preset value in the form JSON must not produce
    degenerate widths — the resolver falls back to the 1.0 multiplier so
    bands match the "standard" preset."""
    semantic = _horizontal_input_plan()
    runtime_typo = {
        **_DESKTOP_RUNTIME,
        "lockedGlobals": {
            "globalStyles": {
                "defaultObjectLayout": "horizontal",
                "horizontalInputBandPreset": "ULTRA_WIDE_42",  # not a valid preset
            }
        },
    }
    runtime_standard = {
        **_DESKTOP_RUNTIME,
        "lockedGlobals": {
            "globalStyles": {
                "defaultObjectLayout": "horizontal",
                "horizontalInputBandPreset": "standard",
            }
        },
    }

    typo_def, _ = _compile(semantic, runtime_typo)
    standard_def, _ = _compile(semantic, runtime_standard)

    # Story 6.3.1 (UAT round 9) — Fix G: per-object overrides are no
    # longer stamped. Verify preset fallback via style.width.
    for ttypo, tstd in zip(typo_def["pages"][0]["components"], standard_def["pages"][0]["components"]):
        if ttypo["type"] in {"submit-button", "header", "paragraph", "divider", "terms"}:
            continue
        assert ttypo["style"]["width"] == tstd["style"]["width"], (
            f"Unknown preset must fall back to standard; got "
            f"typo={ttypo['style']['width']}, standard={tstd['style']['width']} "
            f"for type {ttypo['type']!r}"
        )


def test_story_631_fix_d_drop_below_recomputes_box_without_validation():
    """When the canvas can't fit ``[Label][Input][Validation]`` inline
    (narrow-tablet 640 with an email tier ≈ 312 px wide), the compiler
    drops validation below the input AND recomputes ``style.width`` so it
    no longer reserves space for the validation column. Without this
    second recompute we'd ship a box that's wider than necessary, which
    is exactly the bug Fix D's bounding-box policy is meant to remove.
    """
    from modules.form_ai.compiler import (
        HORIZONTAL_INTRA_GAP_PX,
        HORIZONTAL_VALIDATION_MIN_PX,
    )

    semantic = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "formId": "narrow-fix-d",
            "title": "Narrow Fix D probe",
            "components": [
                {"componentType": "email", "label": "Email", "widthIntent": "half"},
            ],
        }
    )
    runtime = {
        "canvas": {"width": 640, "height": 800, "gridSize": 8},
        "lockedGlobals": {"globalStyles": {"defaultObjectLayout": "horizontal"}},
    }
    definition, summary = _compile(semantic, runtime)
    assert summary["rowSolverDecisions"][0]["decision"] == "horizontal-validation-below"

    component = definition["pages"][0]["components"][0]
    label_band = definition["globalStyles"]["horizontalLabelBandPx"]
    # Story 6.3.1 (UAT round 9) — Fix G: input override no longer stamped.
    # Compute the expected input band from the internal estimator instead.
    from modules.form_ai.compiler import (
        COMPONENT_WIDTH_TIERS,
        _estimate_horizontal_input_band_px,
    )
    tier = COMPONENT_WIDTH_TIERS["email"]
    input_band = _estimate_horizontal_input_band_px(
        "email", max_length=None, tier=tier, chars_multiplier=1.0,
    )
    expected_no_validation = label_band + HORIZONTAL_INTRA_GAP_PX + input_band

    # Drop-below path may also have shrunk the input band to fit the
    # narrow canvas (the compiler clamps when even no-validation overflows).
    # So allow the box to be at most ``expected_no_validation``.
    assert component["style"]["width"] <= expected_no_validation + 1, (
        "When validation drops below, box_width must NOT include validation "
        f"reservation; got {component['style']['width']}px, "
        f"expected at most ~{int(expected_no_validation)}px"
    )
    # And the box must NOT include the validation band, otherwise drop-
    # below is just adding extra height for nothing.
    expected_with_validation = (
        expected_no_validation + HORIZONTAL_INTRA_GAP_PX + HORIZONTAL_VALIDATION_MIN_PX
    )
    assert component["style"]["width"] < expected_with_validation, (
        "Drop-below box_width should be narrower than the inline-validation "
        "box_width; otherwise Fix D's bounding-box recompute is missing"
    )


# -----------------------------------------------------------------------
# Story 6.3.1 (UAT round 7) — Fix E tests
#
# Six issues raised by the user after Fix D landed:
#   1. Label-input gap was too wide (label band over-padded).
#   2. Validation column was wrapping (auto-tracked, was getting < 200 px).
#   3. Dropdowns weren't sized to their longest option.
#   4. Rating wasn't sized to its icon row.
#   5. Terms component was spreading checkbox + text + validation across
#      the full canvas with huge dead space between them.
#
# Each test below is named ``fix_e_<item>_*`` so the connection back to
# the user feedback is obvious from the failure message alone.
# -----------------------------------------------------------------------


def test_story_631_fix_e1_label_band_uses_tighter_padding_than_vertical():
    """Fix E item 1: the horizontal label band must use the new
    ``HORIZONTAL_LABEL_BAND_PADDING_PX`` (16 px) — not the general
    ``LABEL_PADDING_PX`` (32 px). The user's UAT round 7 feedback was that
    the label-input gap was visually too wide; the fix is to halve the
    right-side padding inside the label band so the band hugs the longest
    label more tightly.
    """
    from modules.form_ai.compiler import (
        AVG_CHAR_PX,
        HORIZONTAL_LABEL_BAND_PADDING_PX,
        LABEL_PADDING_PX,
        _estimate_horizontal_label_band_px,
    )

    # Sanity check: the constant we just introduced really is tighter
    # than the legacy padding. If someone bumps it back to 32, the test
    # fails with a clear hint pointing back at the regression.
    assert HORIZONTAL_LABEL_BAND_PADDING_PX < LABEL_PADDING_PX

    # 16-char label exactly (count: "Sixteen char lbl" = S-i-x-t-e-e-n-(sp)-
    # c-h-a-r-(sp)-l-b-l = 16). No required marker, so width is exactly:
    # 16 * 9 + 16 = 160 px (well within the [120, 280] clamp).
    label_text = "Sixteen char lbl"
    assert len(label_text) == 16, "test fixture invariant: label must be 16 chars"
    plan = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "components": [
                {"componentType": "text", "label": label_text},
            ],
        }
    )
    band = _estimate_horizontal_label_band_px(plan, content_width=1024.0)
    expected = int(round(len(label_text) * AVG_CHAR_PX + HORIZONTAL_LABEL_BAND_PADDING_PX))
    assert band == expected, (
        f"Label band should be ``len(label) * AVG_CHAR_PX + "
        f"HORIZONTAL_LABEL_BAND_PADDING_PX`` = {expected} px, got {band}"
    )


def test_story_631_fix_e1_label_band_includes_required_marker_chars():
    """Fix E item 1: required-marker " *" appended to the label by the
    renderer must be counted when sizing the band, otherwise required
    fields with the longest label get their asterisk cropped off the
    right edge of the band.
    """
    from modules.form_ai.compiler import _estimate_horizontal_label_band_px

    optional_plan = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "components": [{"componentType": "text", "label": "How interested are you?"}],
        }
    )
    required_plan = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "components": [
                {
                    "componentType": "text",
                    "label": "How interested are you?",
                    "validationIntent": {"required": True},
                },
            ],
        }
    )
    optional_band = _estimate_horizontal_label_band_px(optional_plan, 1024.0)
    required_band = _estimate_horizontal_label_band_px(required_plan, 1024.0)
    assert required_band > optional_band, (
        f"Required label should reserve space for the ' *' marker; "
        f"got required={required_band}, optional={optional_band}"
    )


def test_story_631_fix_g_validation_column_not_pinned_for_standard_inputs():
    """Story 6.3.1 (UAT round 9) — Fix G: the validation column must NOT
    be pinned via ``props.helpWidthOverride`` for standard inputs. Fix E
    pinned it; Fix F2 made the pin content-aware. Fix G removes the pin
    entirely so the renderer's CSS Grid (``minmax(0, max-content)``) can
    auto-grow the validation column to fit whatever message the runtime
    emits — and crucially, so the user can still resize it via the
    Appearance panel without fighting a stamped pixel pin (see
    COMPONENT-FRAMEWORK-REFERENCE.md).
    """
    semantic = _horizontal_input_plan()
    definition, summary = _compile(semantic, _DESKTOP_RUNTIME_HORIZONTAL)
    components = definition["pages"][0]["components"]

    for component, decision in zip(components, summary["rowSolverDecisions"]):
        # ``terms`` is the only structural exception — its inline
        # validation budget is reserved by the bounding box, but
        # ``helpWidthOverride`` is still NOT stamped (column auto-grows).
        if component["type"] == "terms":
            assert "helpWidthOverride" not in component["props"], (
                "terms must not pin helpWidthOverride either; bounding "
                "box already reserves the validation budget"
            )
            continue
        assert "helpWidthOverride" not in component["props"], (
            f"{component['type']} (decision={decision['decision']}) "
            "must NOT stamp helpWidthOverride; framework auto-grows the "
            "validation column via minmax(0, max-content)"
        )


def test_story_631_fix_e2_validation_pin_skipped_when_dropped_below():
    """Fix E item 2: when validation drops below the input (narrow canvas)
    pinning the validation column would leave dead space to the right of
    the message. The compiler must therefore SKIP the helpWidthOverride
    stamp in that case.
    """
    semantic = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "components": [
                {"componentType": "email", "label": "Email", "widthIntent": "half"},
            ],
        }
    )
    runtime = {
        "canvas": {"width": 640, "height": 800, "gridSize": 8},
        "lockedGlobals": {"globalStyles": {"defaultObjectLayout": "horizontal"}},
    }
    definition, summary = _compile(semantic, runtime)
    assert summary["rowSolverDecisions"][0]["decision"] == "horizontal-validation-below"
    component = definition["pages"][0]["components"][0]
    assert "helpWidthOverride" not in component["props"], (
        "When validation drops below, helpWidthOverride must not be "
        "stamped; got "
        f"{component['props'].get('helpWidthOverride')!r}"
    )


def test_story_631_fix_e3_dropdown_sized_to_longest_option_label():
    """Fix E item 3 (refined by Fix F item 1): dropdown/select width must
    be driven by the longest option label (e.g. "Enterprise" in a
    Company-size dropdown) rather than the generic 22-char default.

    Story 6.3.1 (UAT round 8) — Fix F item 1: options-driven dropdowns
    now skip the ``tier[0]`` floor (which was the vertical-mode input
    minimum) and use a narrow chrome floor instead, so a 10-char
    "Enterprise" dropdown renders at ~114 px in horizontal mode rather
    than being inflated to the 220+ px tier minimum.
    """
    from modules.form_ai.compiler import (
        AVG_CHAR_PX,
        COMPONENT_WIDTH_TIERS,
        INPUT_BAND_PADDING_PX,
        _estimate_horizontal_input_band_px,
    )

    tier = COMPONENT_WIDTH_TIERS["dropdown"]
    band = _estimate_horizontal_input_band_px(
        "dropdown",
        max_length=None,
        tier=tier,
        options_max_chars=10,  # "Enterprise" = 10 chars
    )
    # Expected: 10 chars wins over the comfortable 22 chars; the narrow
    # chrome floor (~33 px) is below the chars math, so the natural
    # chars-driven width survives and the tier max is the only ceiling.
    raw_px = float(10) * AVG_CHAR_PX + INPUT_BAND_PADDING_PX
    narrow_floor_px = AVG_CHAR_PX + INPUT_BAND_PADDING_PX
    expected = int(round(max(narrow_floor_px, min(raw_px, tier[2]))))
    assert band == expected, (
        f"Dropdown should size to longest option (10 chars → "
        f"{expected} px after narrow-floor clamp), got {band} px"
    )


def test_story_631_fix_e3_dropdown_caps_long_option_at_hard_max():
    """Fix E item 3: a dropdown with a silly-long option ("Some really
    long enterprise category description that goes on") must still be
    capped at ``hard_max`` — same policy as ``maxLength`` capping for
    text inputs. Otherwise one verbose option would balloon the column.
    """
    from modules.form_ai.compiler import (
        COMPONENT_WIDTH_TIERS,
        INPUT_COMFORTABLE_CHARS,
        _estimate_horizontal_input_band_px,
    )

    _, hard_max = INPUT_COMFORTABLE_CHARS["dropdown"]
    tier = COMPONENT_WIDTH_TIERS["dropdown"]
    band_capped = _estimate_horizontal_input_band_px(
        "dropdown", max_length=None, tier=tier, options_max_chars=200
    )
    band_at_max = _estimate_horizontal_input_band_px(
        "dropdown", max_length=None, tier=tier, options_max_chars=hard_max
    )
    assert band_capped == band_at_max, (
        f"Option-driven width should be capped at hard_max={hard_max} chars; "
        f"got {band_capped} (capped) vs {band_at_max} (at hard_max)"
    )


def test_story_631_fix_e3_longest_option_chars_handles_label_value_strings():
    """Fix E item 3 helper test: ``_longest_option_chars`` must accept
    the three option shapes the LLM commonly emits — dict with ``label``,
    dict with only ``value``, and plain string — without crashing.
    """
    from modules.form_ai.compiler import _longest_option_chars

    assert _longest_option_chars(
        [{"label": "Small", "value": "S"}, {"label": "Enterprise", "value": "XL"}]
    ) == len("Enterprise")
    assert _longest_option_chars(
        [{"value": "201-500"}, {"value": "1001-5000"}]
    ) == len("1001-5000")
    assert _longest_option_chars(["Yes", "No", "Maybe later"]) == len("Maybe later")
    # Empty / missing options return None so the estimator falls back to
    # the comfortable default cleanly.
    assert _longest_option_chars(None) is None
    assert _longest_option_chars([]) is None


def test_story_631_fix_e4_rating_sized_from_validation_intent_max():
    """Fix E item 4: a rating with ``validationIntent.max = 5`` (5-star)
    must size to the icon row, not to the generic chars table value.
    Width is ``5 * RATING_ICON_PX + INPUT_BAND_PADDING_PX``.
    """
    from modules.form_ai.compiler import (
        COMPONENT_WIDTH_TIERS,
        INPUT_BAND_PADDING_PX,
        RATING_ICON_PX,
        _estimate_horizontal_input_band_px,
    )

    tier = COMPONENT_WIDTH_TIERS["rating"]
    band = _estimate_horizontal_input_band_px(
        "rating", max_length=None, tier=tier, rating_count=5
    )
    expected = int(round(5 * RATING_ICON_PX + INPUT_BAND_PADDING_PX))
    # Tier max is the only ceiling — the rating special path skips the
    # tier-min floor because narrow rating widgets are visually correct.
    expected = min(expected, int(round(tier[2])))
    assert band == expected, (
        f"5-star rating should be {expected} px (5 icons + padding), "
        f"got {band}"
    )


def test_story_631_fix_e4_rating_resolves_count_from_extras_or_options():
    """Fix E item 4 helper: ``_resolve_rating_count`` must read the count
    from ``validationIntent.max``, fall back to LLM extras like
    ``maxRating`` / ``ratingScale``, and finally fall back to
    ``len(options)`` for labelled scales.
    """
    from modules.form_ai.compiler import _resolve_rating_count

    via_validation = SemanticComponentIntent.model_validate(
        {
            "componentType": "rating",
            "label": "How likely?",
            "validationIntent": {"max": 5},
        }
    )
    assert _resolve_rating_count(via_validation) == 5

    via_extra = SemanticComponentIntent.model_validate(
        {"componentType": "rating", "label": "NPS", "maxRating": 10}
    )
    assert _resolve_rating_count(via_extra) == 10

    via_options = SemanticComponentIntent.model_validate(
        {
            "componentType": "rating",
            "label": "Rate us",
            "options": [
                {"label": "Bad"},
                {"label": "OK"},
                {"label": "Good"},
            ],
        }
    )
    assert _resolve_rating_count(via_options) == 3

    # Story 6.3.1 (UAT round 8) — Fix F item 1b: when the LLM omits
    # ``validationIntent.max`` and any extra/options hints, the resolver
    # now defaults to a 5-star scale rather than returning ``None``.
    # ``None`` would push the rating component back onto the chars-driven
    # path, which then gets clamped to the (~220 px) text-input tier
    # minimum — the very regression UAT round 8 (item 5) reported.
    none_intent = SemanticComponentIntent.model_validate(
        {"componentType": "rating", "label": "Rate"}
    )
    assert _resolve_rating_count(none_intent) == 5

    # Out-of-range extras (e.g. the LLM emits ``max: 100`` because it
    # confused ``rating`` with a numeric input) also snap back to the
    # 5-star default rather than degrading to the chars-driven path.
    out_of_range_intent = SemanticComponentIntent.model_validate(
        {
            "componentType": "rating",
            "label": "Rate",
            "validationIntent": {"max": 100},
        }
    )
    assert _resolve_rating_count(out_of_range_intent) == 5


def test_story_631_fix_g_rating_box_width_includes_icon_row_budget():
    """Story 6.3.1 (UAT round 9) — Fix G: per-object overrides are no
    longer stamped on rating either. The bounding ``style.width`` MUST
    still include the icon-row budget (5 * RATING_ICON_PX +
    INPUT_BAND_PADDING_PX) plus label-band + validation-band so the
    placement loop reserves enough horizontal real estate, but the
    inner column sizing is left to the framework's CSS Grid (so the
    user can resize it via the Appearance panel without fighting a
    stamped pixel pin).
    """
    from modules.form_ai.compiler import (
        HORIZONTAL_INTRA_GAP_PX,
        HORIZONTAL_VALIDATION_MIN_PX,
        INPUT_BAND_PADDING_PX,
        RATING_ICON_PX,
    )

    semantic = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "components": [
                {
                    "componentType": "rating",
                    "label": "How likely are you to recommend us?",
                    "validationIntent": {"max": 5},
                },
            ],
        }
    )
    definition, _summary = _compile(semantic, _DESKTOP_RUNTIME_HORIZONTAL)
    component = definition["pages"][0]["components"][0]
    assert "inputWidthOverride" not in component["props"], (
        "Fix G: rating must not stamp inputWidthOverride; the framework "
        "auto-grows the input column so the user can edit star count / "
        "icon symbols without the input wrapping."
    )
    label_band = definition["globalStyles"]["horizontalLabelBandPx"]
    icon_band = int(round(5 * RATING_ICON_PX + INPUT_BAND_PADDING_PX))
    floor = (
        label_band
        + HORIZONTAL_INTRA_GAP_PX
        + icon_band
        + HORIZONTAL_INTRA_GAP_PX
        + HORIZONTAL_VALIDATION_MIN_PX
    )
    assert component["style"]["width"] >= floor - 2, (
        f"Rating bounding box must reserve label + icon + validation "
        f"budget (>= {floor} px); got {component['style']['width']}px"
    )


def test_story_631_fix_e5_terms_left_aligned_at_default_margin():
    """Fix E item 5: the terms component must left-align with the rest of
    the form (``DEFAULT_MARGIN_X``) so the visual column of inputs stays
    consistent. Pre-Fix-E the terms branch went through the banner code
    which gave it ``x = DEFAULT_MARGIN_X`` and ``width = content_width``;
    we still want the left-align but no longer the full width.
    """
    from modules.form_ai.compiler import DEFAULT_MARGIN_X

    semantic = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "components": [
                {"componentType": "email", "label": "Email", "widthIntent": "half"},
                {
                    "componentType": "terms",
                    "label": "I consent to receiving marketing communications",
                },
            ],
        }
    )
    definition, _summary = _compile(semantic, _DESKTOP_RUNTIME_HORIZONTAL)
    components = definition["pages"][0]["components"]
    terms = next(c for c in components if c["type"] == "terms")
    email = next(c for c in components if c["type"] == "email")
    assert terms["position"]["x"] == DEFAULT_MARGIN_X
    assert email["position"]["x"] == DEFAULT_MARGIN_X


# ---------------------------------------------------------------------------
# Story 6.3.1 (UAT round 8) — Fix F: regression repair for the symptoms the
# user reported after Fix E (item-by-item):
#   1. "Input width was not suppose to change but now all inputs are the same
#      width" — caused by the runtime-supplied ``componentFootprints`` (DOM
#      measurements of toolbox tiles, uniformly ~359 px wide) being treated as
#      a hard floor by ``_resolve_component_widths``. The horizontal-mode
#      placement loop now bypasses those inflated solver values and feeds the
#      ORIGINAL ``COMPONENT_WIDTH_TIERS`` to the input-band estimator so
#      content-aware widths survive.
#   3. "validation object … allow it to auto grow … if … causes a collision …
#      reduced in width to avoid collisions" — Fix E item 2's hard pin to
#      ``HORIZONTAL_VALIDATION_MIN_PX`` (200 px) is replaced with a per-rule
#      auto-grown width clamped to ``[MIN, MAX]`` and to the remaining row
#      width.
#   5. "Rating … same issue as 1" — when the LLM omits ``validationIntent.max``
#      (very common on minimal plans) ``_resolve_rating_count`` returned
#      ``None`` and the rating fell back to chars-driven sizing → tier-min
#      clamp → 220+ px tile. Fix F item 1b defaults to a 5-star scale.
#   6. "Terms is looking much better but the validation message needs to be
#      next to the input" — terms validation now ALWAYS drops below the
#      consent line in horizontal mode so the renderer renders it on its own
#      auto track directly under the checkbox + label, instead of pushed off
#      to the far right of a wide row.
# ---------------------------------------------------------------------------


# Footprint dictionary that mimics the production payload that triggered the
# uniform-input regression: every toolbox tile measures exactly 359 px wide
# (the default ``UniversalFieldShell`` tile width on a 1920-px canvas), so
# every component's solver-resolved floor / target / max collapses to 359.
_UNIFORM_359_FOOTPRINTS = {
    component_type: {
        "width": 359,
        "height": 96,
        "minWidth": 359,
        "maxWidth": 359,
    }
    for component_type in (
        "first-name",
        "last-name",
        "email",
        "text",
        "dropdown",
        "rating",
        "textarea",
        "phone",
        "submit-button",
        "header",
        "terms",
    )
}


def _desktop_runtime_horizontal_with_uniform_footprints() -> Dict[str, Any]:
    return {
        **_DESKTOP_RUNTIME_HORIZONTAL,
        "componentFootprints": _UNIFORM_359_FOOTPRINTS,
    }


def test_story_631_fix_f1_input_widths_vary_under_uniform_footprints():
    """Fix F item 1 (re-asserted under Fix G via style.width): when the
    runtime sends uniform 359-px componentFootprints (the production
    payload that caused the UAT-round-8 regression), the horizontal-mode
    placement loop must STILL produce per-component bounding boxes
    derived from the chars table — not collapse every input to the same
    footprint-driven floor.

    Story 6.3.1 (UAT round 9) — Fix G: per-object overrides are no
    longer stamped, so we assert via ``style.width`` (which still
    reflects label + chars-driven input + validation budget).
    """
    semantic = _horizontal_input_plan()
    runtime = _desktop_runtime_horizontal_with_uniform_footprints()
    definition, _ = _compile(semantic, runtime)
    components = definition["pages"][0]["components"]

    boxes_by_type = {c["type"]: c["style"]["width"] for c in components}
    assert {"first-name", "last-name", "email"}.issubset(boxes_by_type.keys())

    distinct_widths = {
        boxes_by_type["first-name"],
        boxes_by_type["last-name"],
        boxes_by_type["email"],
    }
    assert len(distinct_widths) >= 2, (
        f"Fix F item 1: under uniform 359-px footprints the bounding "
        f"boxes must still differ (chars-driven), not collapse to the "
        f"footprint floor; got {boxes_by_type!r}"
    )


def test_story_631_fix_f1b_rating_default_count_survives_uniform_footprints():
    """Fix F item 1b (re-asserted under Fix G via style.width): a rating
    component whose plan omits ``validationIntent.max`` must still
    reserve an icon-row-sized budget (~5 * 28 + 16 = 156 px) inside its
    bounding box under the uniform-footprint runtime, not get inflated
    to the 359-px tile floor.

    Story 6.3.1 (UAT round 9) — Fix G: ``inputWidthOverride`` is no
    longer stamped, but the compiler still feeds the rating budget into
    ``box_width``. Verify the bounding box is well below 359 px + label
    band — it should sit at roughly ``label + gap + ~156 + gap +
    validation`` (≈ ``label + 380``-ish), much less than ``label + 359 +
    validation`` would be.
    """
    semantic = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "components": [
                {"componentType": "rating", "label": "Rate us"},
            ],
        }
    )
    runtime = _desktop_runtime_horizontal_with_uniform_footprints()
    definition, _ = _compile(semantic, runtime)
    component = definition["pages"][0]["components"][0]

    assert "inputWidthOverride" not in component["props"], (
        "Fix G: rating must not stamp inputWidthOverride; the framework "
        "auto-grows the input column to the icon row at render time."
    )
    label_band = definition["globalStyles"]["horizontalLabelBandPx"]
    # Compare against a rough chars-only baseline that uses 22 chars
    # (the comfortable default for inputs without an option list) — the
    # rating box should be smaller than that, because the rating budget
    # (~156 px) is well below 22 * 9 + 16 = 214 px.
    from modules.form_ai.compiler import (
        AVG_CHAR_PX,
        HORIZONTAL_INTRA_GAP_PX,
        HORIZONTAL_VALIDATION_MIN_PX,
        INPUT_BAND_PADDING_PX,
    )
    chars_baseline_input = 22 * AVG_CHAR_PX + INPUT_BAND_PADDING_PX
    chars_baseline_box = (
        label_band
        + HORIZONTAL_INTRA_GAP_PX
        + chars_baseline_input
        + HORIZONTAL_INTRA_GAP_PX
        + HORIZONTAL_VALIDATION_MIN_PX
    )
    assert component["style"]["width"] < chars_baseline_box, (
        f"Fix F item 1b: rating bounding box must be narrower than the "
        f"chars-baseline (~{int(chars_baseline_box)} px); got "
        f"{component['style']['width']}px — looks like the icon-row "
        f"budget regressed to a chars/footprint floor."
    )


def test_story_631_fix_f2_validation_band_auto_grows_for_long_messages():
    """Fix F item 2: a validator with a long synthesized message must
    produce a wider ``helpWidthOverride`` than a validator with a short
    message — the column auto-grows to the longest message the runtime
    ``validationEngine`` would render rather than being pinned at 200 px.

    Uses ``textarea`` because the test governance payload's
    ``validationContracts`` allows ``maxLength`` for textarea (so the
    flat normalized validation block actually contains ``maxLength``,
    triggering the synthesized-message path in
    ``_estimate_validation_band_px``).
    """
    from modules.form_ai.compiler import HORIZONTAL_VALIDATION_MIN_PX

    short_plan = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "components": [
                {
                    "componentType": "textarea",
                    "label": "Comments",
                    "validationIntent": {"required": True},
                },
            ],
        }
    )
    long_plan = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "components": [
                {
                    "componentType": "textarea",
                    "label": "Comments",
                    "validationIntent": {
                        "required": True,
                        "maxLength": 5000,
                    },
                },
            ],
        }
    )
    short_def, _ = _compile(short_plan, _DESKTOP_RUNTIME_HORIZONTAL)
    long_def, _ = _compile(long_plan, _DESKTOP_RUNTIME_HORIZONTAL)
    # Story 6.3.1 (UAT round 9) — Fix G: helpWidthOverride is no longer
    # stamped (the renderer auto-grows the validation column via
    # ``minmax(0, max-content)``). Instead the bounding ``style.width``
    # must reserve the validation budget — verify that path by asserting
    # the box for the long-message plan is wider than for the short one.
    short_comp = short_def["pages"][0]["components"][0]
    long_comp = long_def["pages"][0]["components"][0]
    assert "helpWidthOverride" not in short_comp["props"]
    assert "helpWidthOverride" not in long_comp["props"]
    assert long_comp["style"]["width"] > short_comp["style"]["width"], (
        f"Fix F item 2 (re-asserted under Fix G): long ``maxLength`` "
        f"plan must reserve a wider bounding box than short ``required`` "
        f"plan; got long={long_comp['style']['width']}px, "
        f"short={short_comp['style']['width']}px"
    )
    # And the short box must still reserve at least the validation MIN.
    short_def_label = short_def["globalStyles"]["horizontalLabelBandPx"]
    from modules.form_ai.compiler import HORIZONTAL_INTRA_GAP_PX
    assert (
        short_comp["style"]["width"]
        >= short_def_label + HORIZONTAL_INTRA_GAP_PX + HORIZONTAL_VALIDATION_MIN_PX
    )


def test_story_631_fix_f2_validation_band_capped_at_max():
    """Fix F item 2: the auto-grown validation column must hard-cap at
    ``HORIZONTAL_VALIDATION_MAX_PX`` so a paragraph-length validator
    message can't dominate the row.
    """
    from modules.form_ai.compiler import (
        DEFAULT_VALIDATION_PLACEHOLDER_CHARS,
        HORIZONTAL_VALIDATION_MAX_PX,
        _estimate_validation_band_px,
    )

    # 200-char message (way beyond the cap) — must clamp to the max.
    long_message_props = {
        "validation": {
            "rules": [
                {"type": "required", "message": "x" * 200},
            ]
        }
    }
    band = _estimate_validation_band_px(
        long_message_props,
        min_px=200.0,
        max_px=HORIZONTAL_VALIDATION_MAX_PX,
    )
    assert band == int(round(HORIZONTAL_VALIDATION_MAX_PX)), (
        f"Fix F item 2: validation band must cap at "
        f"HORIZONTAL_VALIDATION_MAX_PX ({HORIZONTAL_VALIDATION_MAX_PX}), "
        f"got {band}"
    )

    # Empty rules → fall back to the placeholder length, but still respect
    # the min floor.
    placeholder_band = _estimate_validation_band_px(
        {}, min_px=200.0, max_px=HORIZONTAL_VALIDATION_MAX_PX
    )
    assert placeholder_band >= 200, (
        f"Fix F item 2: empty rules must still reserve at least the "
        f"placeholder room; got {placeholder_band}"
    )
    assert placeholder_band <= int(round(HORIZONTAL_VALIDATION_MAX_PX))
    # And it should reflect the placeholder character count, not just blow
    # past the floor — sanity check that ``DEFAULT_VALIDATION_PLACEHOLDER_CHARS``
    # is honoured.
    assert DEFAULT_VALIDATION_PLACEHOLDER_CHARS > 0


def test_story_631_fix_f3_label_band_excludes_terms_consent_label():
    """Fix F item 3: the very long ``terms`` consent label
    ("I consent to receiving marketing communications" ≈ 49 chars) must
    NOT inflate the form-wide ``horizontalLabelBandPx`` — otherwise every
    other row's label-input gap widens to accommodate a label that has
    its own per-row width override.
    """
    from modules.form_ai.compiler import _estimate_horizontal_label_band_px

    no_terms = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "components": [
                {"componentType": "first-name", "label": "First name"},
                {"componentType": "last-name", "label": "Last name"},
                {"componentType": "email", "label": "Work email"},
            ],
        }
    )
    with_terms = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "components": [
                {"componentType": "first-name", "label": "First name"},
                {"componentType": "last-name", "label": "Last name"},
                {"componentType": "email", "label": "Work email"},
                {
                    "componentType": "terms",
                    "label": "I consent to receiving marketing communications",
                },
            ],
        }
    )
    band_no_terms = _estimate_horizontal_label_band_px(no_terms, 1024.0)
    band_with_terms = _estimate_horizontal_label_band_px(with_terms, 1024.0)
    assert band_no_terms == band_with_terms, (
        f"Fix F item 3: adding terms must NOT widen the form-wide label "
        f"band; got {band_no_terms} (no terms) vs {band_with_terms} "
        f"(with terms)"
    )


def test_story_631_fix_g3_terms_validation_inline_with_autogrow():
    """Story 6.3.1 (UAT round 9) — Fix G item 3: revert Fix F4. In
    horizontal mode the ``terms`` validation must render INLINE (next to
    the consent link, not below) on canvases wide enough to fit it.
    The bounding ``style.width`` is widened to include the validation
    column, but ``helpWidthOverride`` is NOT stamped — the validation
    column auto-grows via the framework's CSS Grid track. Structural
    pins (32-px checkbox via ``inputWidthOverride``, consent text via
    ``labelWidthOverride``) are retained because the framework would
    otherwise stretch them.

    Per the user: "we are not following the COMPONENT-FRAMEWORK-
    REFERENCE.md … all controls continue to work and allow the user to
    make the changes they want."
    """
    from modules.form_ai.compiler import (
        HORIZONTAL_INTRA_GAP_PX,
        HORIZONTAL_VALIDATION_MIN_PX,
        TERMS_CHECKBOX_BAND_PX,
    )

    semantic = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "components": [
                {"componentType": "email", "label": "Email"},
                {
                    "componentType": "terms",
                    "label": "I consent to receiving marketing communications",
                },
            ],
        }
    )
    definition, summary = _compile(semantic, _DESKTOP_RUNTIME_HORIZONTAL)
    terms = next(
        c for c in definition["pages"][0]["components"] if c["type"] == "terms"
    )
    terms_decision = next(
        d
        for d in summary["rowSolverDecisions"]
        if "terms" in d["componentIds"][0]
    )
    assert terms_decision["decision"] == "horizontal-terms-inline-validation", (
        f"Fix G3: terms must default to inline validation on a desktop "
        f"canvas, got {terms_decision['decision']!r}"
    )
    assert terms_decision["validationDroppedBelow"] is False

    # Structural pins survive (framework would otherwise stretch them).
    assert terms["props"].get("inputWidthOverride") == TERMS_CHECKBOX_BAND_PX, (
        "Fix G3: terms must keep the 32-px checkbox pin so the input "
        "column doesn't stretch."
    )
    assert "labelWidthOverride" in terms["props"], (
        "Fix G3: terms must keep the consent-text label pin so the "
        "long consent label doesn't squeeze the input column."
    )

    # ``helpWidthOverride`` must NOT be stamped — the column auto-grows.
    assert "helpWidthOverride" not in terms["props"], (
        "Fix G3: terms validation column must auto-grow via the "
        "framework's CSS Grid; helpWidthOverride must not be stamped."
    )

    # Bounding box must include the validation budget so the placement
    # loop reserves enough horizontal real estate for the inline column.
    label_pin = terms["props"]["labelWidthOverride"]
    inline_floor = (
        TERMS_CHECKBOX_BAND_PX
        + HORIZONTAL_INTRA_GAP_PX
        + label_pin
        + HORIZONTAL_INTRA_GAP_PX
        + HORIZONTAL_VALIDATION_MIN_PX
    )
    assert terms["style"]["width"] >= inline_floor - 2, (
        f"Fix G3: terms bounding box must reserve label + checkbox + "
        f"validation budget (>= {inline_floor} px); got "
        f"{terms['style']['width']}px"
    )

    # props.width is still synced to style.width.
    assert terms["props"].get("width") == f"{terms['style']['width']}px"


def test_story_631_fix_g4a_horizontal_rows_are_tighter_than_vertical():
    """Story 6.3.1 (UAT round 9) — Fix G4a: horizontal mode now reserves
    ~50 px per text input row (label + input + validation share one
    row) instead of the ~110 px the vertical-packed table reserves
    (label-above-input). Without this carve-out the canvas inflates to
    fit phantom vertical chrome that doesn't exist in horizontal mode —
    the "huge gaps between components" symptom from UAT round 9.

    Asserts BOTH halves of the fix:
      * ``style.height`` for a standard text input shrinks from ~110 to
        ~52 px in horizontal mode.
      * ``_row_chrome`` returns 0 in horizontal mode for ALL component
        types (label and validation are inline columns, not vertical
        slots), so textarea/submit-button/file-upload don't double-pay
        for chrome that only exists in vertical mode.
    """
    from modules.form_ai.compiler import (
        DEFAULT_COMPONENT_HEIGHTS,
        DEFAULT_COMPONENT_HEIGHTS_HORIZONTAL,
        LAYOUT_MODE_HORIZONTAL_STACKED,
        LAYOUT_MODE_VERTICAL_PACKED,
        _row_chrome,
    )

    # Tight standard-input row: 52 px in horizontal vs 110 px vertical
    # (the vertical default for unlisted text-like inputs).
    horizontal_text = DEFAULT_COMPONENT_HEIGHTS_HORIZONTAL["text"]
    vertical_text_fallback = DEFAULT_COMPONENT_HEIGHTS.get("text", 110)
    assert horizontal_text < vertical_text_fallback, (
        f"Fix G4a: horizontal text-input row ({horizontal_text}) must "
        f"be tighter than the vertical-mode fallback "
        f"({vertical_text_fallback})"
    )
    assert horizontal_text <= 60, (
        f"Fix G4a: horizontal text-input row should be ~50 px (got "
        f"{horizontal_text})"
    )

    # No vertical chrome in horizontal mode: every component type that
    # has a non-zero chrome budget vertically must report 0 chrome
    # horizontally (label/validation are inline columns).
    for component_type in ("textarea", "submit-button", "file-upload", "text"):
        assert _row_chrome(
            component_type, layout_mode=LAYOUT_MODE_HORIZONTAL_STACKED
        ) == 0.0, (
            f"Fix G4a: {component_type} must report 0 row chrome in "
            "horizontal mode (label and validation render inline)"
        )

    # Vertical mode behaviour preserved — textarea still pays for its
    # 80 px label/validation chrome stack so the next row doesn't
    # collide.
    assert (
        _row_chrome("textarea", layout_mode=LAYOUT_MODE_VERTICAL_PACKED) == 80.0
    )


def test_story_631_fix_g4a_canvas_does_not_inflate_a_typical_horizontal_form():
    """Story 6.3.1 (UAT round 9) — Fix G4a end-to-end: a typical contact
    form (8 inputs + textarea + terms + submit, ~10 components) compiled
    in horizontal mode on a 980-px-tall desktop canvas must FIT the
    components inside the 980 px floor instead of inflating the canvas.
    User feedback: "I created a new form where the canvas was 980px high
    and used the same prompt after changing the componenet to horizontal
    and it automatically increased the height of the canvas to the same
    with huge gaps between."
    """
    semantic = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "components": [
                {"componentType": "first-name", "label": "Given name"},
                {"componentType": "last-name", "label": "Surname"},
                {"componentType": "email", "label": "Work email"},
                {"componentType": "phone", "label": "Mobile"},
                {"componentType": "text", "label": "Company name"},
                {
                    "componentType": "dropdown",
                    "label": "Company size",
                    "options": [
                        {"label": "1-10"},
                        {"label": "11-50"},
                        {"label": "51-200"},
                    ],
                },
                {"componentType": "rating", "label": "How interested are you?"},
                {"componentType": "submit-button", "label": "Submit"},
            ],
        }
    )
    definition, summary = _compile(semantic, _DESKTOP_RUNTIME_HORIZONTAL)
    canvas_height = definition["canvasSettings"]["height"]
    assert canvas_height == 980, (
        f"Fix G4a: a typical 8-component horizontal form must FIT the "
        f"runtime 980-px canvas without growing; got {canvas_height}px "
        f"(canvasHeightGrew={summary['canvasHeightGrew']})"
    )
    # And the bottom-most component must sit comfortably inside the
    # canvas — not crammed against the bottom edge.
    components = definition["pages"][0]["components"]
    max_bottom = max(
        c["position"]["y"] + c["style"]["height"] for c in components
    )
    assert max_bottom <= canvas_height, (
        f"Fix G4a: components must fit inside the canvas; got "
        f"max_bottom={max_bottom}, canvas_height={canvas_height}"
    )


def test_story_631_vertical_mode_geometry_is_unchanged_by_phase_2_completion():
    """Regression guard: any plan compiled in vertical mode must produce
    the same geometry as before the horizontal-stacked branch was added.
    Verified by re-running the original ``_trivial_semantic_plan`` in
    pure vertical mode and asserting it still works (existing tests pin
    the exact byte-level shape — this just verifies no exception)."""
    semantic = _trivial_semantic_plan()
    definition, summary = _compile(semantic, _DESKTOP_RUNTIME)
    assert summary["layoutMode"] == LAYOUT_MODE_VERTICAL_PACKED
    assert len(definition["pages"][0]["components"]) > 0


# ---------------------------------------------------------------------------
# Story 6.3.1 (UAT round 6) — Phase 2 LLM nudge gating.
#
# ``_build_initial_messages`` injects ``_HORIZONTAL_STACKED_LAYOUT_NUDGE`` if
# and only if the resolved layout mode is ``horizontal-stacked``. These
# tests make sure the gate is correct in both directions so vertical-mode
# generations don't see noise and horizontal-mode generations do see
# guidance.
# ---------------------------------------------------------------------------


def _system_message_text(messages: list) -> str:
    system = next(m for m in messages if m["role"] == "system")
    return system["content"]


def test_story_631_horizontal_layout_nudge_omitted_in_vertical_mode():
    """No layout signal → no nudge in the system prompt."""
    messages = service._build_initial_messages(
        prompt="Build a contact form.",
        context_pack="",
        runtime_context={"canvas": {"width": 1920, "height": 980, "gridSize": 8}},
    )
    body = _system_message_text(messages)
    assert "LAYOUT MODE — HORIZONTAL STACKED" not in body


def test_story_631_horizontal_layout_nudge_included_when_horizontal():
    """``defaultObjectLayout = "horizontal"`` → nudge appears in the system
    prompt with the documented headline + the rowGroup-suppression rule."""
    messages = service._build_initial_messages(
        prompt="Build a contact form.",
        context_pack="",
        runtime_context={
            "canvas": {"width": 1920, "height": 980, "gridSize": 8},
            "lockedGlobals": {
                "globalStyles": {"defaultObjectLayout": "horizontal"},
            },
        },
    )
    body = _system_message_text(messages)
    assert "LAYOUT MODE — HORIZONTAL STACKED" in body
    # The nudge's most important rule: don't pack via rowGroup in horizontal.
    assert "Do NOT use ``rowGroup``" in body


def test_story_631_horizontal_layout_nudge_omitted_for_vertical_string():
    """An explicit ``"vertical"`` value must not trigger the nudge — only
    the literal ``"horizontal"`` opts in."""
    messages = service._build_initial_messages(
        prompt="Build a contact form.",
        context_pack="",
        runtime_context={
            "canvas": {"width": 1920, "height": 980, "gridSize": 8},
            "lockedGlobals": {
                "globalStyles": {"defaultObjectLayout": "vertical"},
            },
        },
    )
    body = _system_message_text(messages)
    assert "LAYOUT MODE — HORIZONTAL STACKED" not in body
