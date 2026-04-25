"""Story 6.3.1 semantic-validation gate: one test per rule + happy path.

Pinned behaviours:
    * each rule fires only when its specific condition is met,
    * the gate is permissive when no governance is supplied (no false positives),
    * violations carry the right code/index so the LLM-correction message can
      point at the right component.
"""

from __future__ import annotations

from typing import Any, Dict, List

from modules.form_ai.schemas import FormSemanticPlan
from modules.form_ai.semantic_validator import validate_semantic_plan


def _capability_snapshot() -> Dict[str, Any]:
    return {
        "components": [
            {"type": "text", "widthClasses": ["compact", "half", "full"]},
            {"type": "email", "widthClasses": ["half", "full"]},
            {"type": "phone", "widthClasses": ["compact", "half"]},
            {"type": "dropdown", "widthClasses": ["half", "full"]},
            {"type": "radio", "widthClasses": ["full"]},
            {"type": "checkbox", "widthClasses": ["full"]},
            {"type": "submit-button", "widthClasses": ["compact", "half"]},
        ]
    }


def _validation_contracts() -> List[Dict[str, Any]]:
    return [
        {"componentType": "text", "allowedRules": ["required", "maxLength"]},
        {"componentType": "email", "allowedRules": ["required", "email", "maxLength"]},
        {"componentType": "phone", "allowedRules": ["required", "phone", "maxLength"]},
        {"componentType": "dropdown", "allowedRules": ["required"]},
        {"componentType": "radio", "allowedRules": ["required"]},
        {"componentType": "checkbox", "allowedRules": ["required"]},
        {"componentType": "submit-button", "allowedRules": []},
    ]


def _plan(*components: Dict[str, Any]) -> FormSemanticPlan:
    return FormSemanticPlan.model_validate(
        {"semanticPlanVersion": "1.0", "components": list(components)}
    )


# --- happy path -------------------------------------------------------------


def test_story_631_validator_passes_well_formed_plan():
    plan = _plan(
        {
            "componentType": "text",
            "label": "Full name",
            "widthIntent": "full",
            "validationIntent": {"required": True, "maxLength": 80},
        },
        {
            "componentType": "email",
            "label": "Email",
            "widthIntent": "half",
            "validationIntent": {"required": True, "email": True},
        },
        {
            "componentType": "dropdown",
            "label": "Country",
            "widthIntent": "half",
            "options": [{"label": "AU", "value": "au"}],
            "validationIntent": {"required": True},
        },
        {"componentType": "submit-button", "widthIntent": "compact"},
    )

    result = validate_semantic_plan(
        plan,
        capability_snapshot_json=_capability_snapshot(),
        validation_contracts=_validation_contracts(),
    )

    assert result.valid is True
    assert result.violations == []


# --- empty-plan -------------------------------------------------------------


def test_story_631_validator_flags_empty_plan():
    plan = _plan()

    result = validate_semantic_plan(
        plan,
        capability_snapshot_json=_capability_snapshot(),
        validation_contracts=_validation_contracts(),
    )

    assert result.valid is False
    assert len(result.violations) == 1
    assert result.violations[0].code == "empty-plan"
    assert result.violations[0].componentIndex is None


def test_story_631_validator_skips_per_component_rules_when_plan_empty():
    """empty-plan must short-circuit: do not also emit per-component noise."""
    plan = _plan()

    result = validate_semantic_plan(
        plan,
        capability_snapshot_json=_capability_snapshot(),
        validation_contracts=_validation_contracts(),
    )

    assert [v.code for v in result.violations] == ["empty-plan"]


# --- unknown-component-type -------------------------------------------------


def test_story_631_validator_flags_unknown_component_type():
    plan = _plan(
        {"componentType": "alien-widget", "label": "Whatever", "widthIntent": "half"},
        {"componentType": "text", "label": "Name", "widthIntent": "half"},
    )

    result = validate_semantic_plan(
        plan,
        capability_snapshot_json=_capability_snapshot(),
        validation_contracts=_validation_contracts(),
    )

    assert result.valid is False
    codes = [v.code for v in result.violations]
    assert codes == ["unknown-component-type"]
    violation = result.violations[0]
    assert violation.componentIndex == 0
    assert violation.componentType == "alien-widget"
    assert "alien-widget" in violation.message
    assert violation.suggestion is not None and "text" in violation.suggestion


def test_story_631_validator_skips_subsequent_rules_on_unknown_type():
    """An unknown type cannot meaningfully be checked against width/validation
    contracts, so we skip to the next component instead of piling on noise."""
    plan = _plan(
        {
            "componentType": "alien-widget",
            "widthIntent": "compact",
            "validationIntent": {"required": True, "email": True},
        }
    )

    result = validate_semantic_plan(
        plan,
        capability_snapshot_json=_capability_snapshot(),
        validation_contracts=_validation_contracts(),
    )

    assert [v.code for v in result.violations] == ["unknown-component-type"]


def test_story_631_validator_permissive_when_no_capability_snapshot():
    """Story 6.3.1 (governance-resolution): when ops have not configured a
    capability snapshot, the gate must not block. Otherwise a fresh install
    would be unable to generate any form."""
    plan = _plan(
        {"componentType": "alien-widget", "label": "Whatever", "widthIntent": "half"},
    )

    result = validate_semantic_plan(
        plan, capability_snapshot_json=None, validation_contracts=None
    )

    assert result.valid is True


# --- width-intent-not-allowed -----------------------------------------------


def test_story_631_validator_flags_disallowed_width_intent():
    plan = _plan(
        {"componentType": "phone", "label": "Phone", "widthIntent": "full"},
    )

    result = validate_semantic_plan(
        plan,
        capability_snapshot_json=_capability_snapshot(),
        validation_contracts=_validation_contracts(),
    )

    codes = [v.code for v in result.violations]
    assert codes == ["width-intent-not-allowed"]
    violation = result.violations[0]
    assert violation.componentIndex == 0
    assert violation.componentType == "phone"
    assert violation.suggestion is not None
    assert "compact" in violation.suggestion and "half" in violation.suggestion


def test_story_631_validator_allows_missing_width_intent():
    """widthIntent=None is acceptable; the compiler will pick a default."""
    plan = _plan({"componentType": "phone", "label": "Phone"})

    result = validate_semantic_plan(
        plan,
        capability_snapshot_json=_capability_snapshot(),
        validation_contracts=_validation_contracts(),
    )

    assert result.valid is True


# --- missing-options-for-choice ---------------------------------------------


def test_story_631_validator_flags_dropdown_without_options():
    plan = _plan(
        {"componentType": "dropdown", "label": "Country", "widthIntent": "half"}
    )

    result = validate_semantic_plan(
        plan,
        capability_snapshot_json=_capability_snapshot(),
        validation_contracts=_validation_contracts(),
    )

    codes = [v.code for v in result.violations]
    assert codes == ["missing-options-for-choice"]


def test_story_631_validator_flags_radio_with_empty_options():
    plan = _plan(
        {
            "componentType": "radio",
            "label": "Pick one",
            "widthIntent": "full",
            "options": [],
        }
    )

    result = validate_semantic_plan(
        plan,
        capability_snapshot_json=_capability_snapshot(),
        validation_contracts=_validation_contracts(),
    )

    assert [v.code for v in result.violations] == ["missing-options-for-choice"]


def test_story_631_validator_flags_checkbox_without_options():
    plan = _plan(
        {"componentType": "checkbox", "label": "Topics", "widthIntent": "full"}
    )

    result = validate_semantic_plan(
        plan,
        capability_snapshot_json=_capability_snapshot(),
        validation_contracts=_validation_contracts(),
    )

    assert [v.code for v in result.violations] == ["missing-options-for-choice"]


# --- invalid-validation-rule ------------------------------------------------


def test_story_631_validator_flags_disallowed_validation_rule():
    plan = _plan(
        {
            "componentType": "phone",
            "label": "Phone",
            "widthIntent": "half",
            "validationIntent": {"required": True, "email": True},
        }
    )

    result = validate_semantic_plan(
        plan,
        capability_snapshot_json=_capability_snapshot(),
        validation_contracts=_validation_contracts(),
    )

    codes = [v.code for v in result.violations]
    assert codes == ["invalid-validation-rule"]
    violation = result.violations[0]
    assert "email" in violation.message
    assert violation.suggestion is not None
    assert "phone" in violation.suggestion


def test_story_631_validator_lists_all_disallowed_rules_per_component():
    plan = _plan(
        {
            "componentType": "phone",
            "label": "Phone",
            "widthIntent": "half",
            "validationIntent": {"required": True, "email": True, "url": True},
        }
    )

    result = validate_semantic_plan(
        plan,
        capability_snapshot_json=_capability_snapshot(),
        validation_contracts=_validation_contracts(),
    )

    assert len(result.violations) == 1
    msg = result.violations[0].message
    assert "email" in msg and "url" in msg


# --- duplicate-component-id -------------------------------------------------


def test_story_631_validator_flags_duplicate_component_id():
    plan = _plan(
        {"componentType": "text", "label": "First", "componentId": "shared"},
        {"componentType": "text", "label": "Second", "componentId": "shared"},
    )

    result = validate_semantic_plan(
        plan,
        capability_snapshot_json=_capability_snapshot(),
        validation_contracts=_validation_contracts(),
    )

    codes = [v.code for v in result.violations]
    assert codes == ["duplicate-component-id"]
    violation = result.violations[0]
    assert violation.componentIndex == 1
    assert violation.componentId == "shared"


def test_story_631_validator_does_not_flag_unset_component_ids():
    plan = _plan(
        {"componentType": "text", "label": "First"},
        {"componentType": "text", "label": "Second"},
    )

    result = validate_semantic_plan(
        plan,
        capability_snapshot_json=_capability_snapshot(),
        validation_contracts=_validation_contracts(),
    )

    assert result.valid is True


# --- FormSemanticPlan compatibility -----------------------------------------


def test_form_semantic_plan_normalizes_non_10_version():
    plan = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "6.3.1",
            "components": [{"componentType": "text"}],
        }
    )

    assert plan.semanticPlanVersion == "1.0"


def test_form_semantic_plan_normalizes_missing_version():
    plan = FormSemanticPlan.model_validate({"components": [{"componentType": "text"}]})

    assert plan.semanticPlanVersion == "1.0"


def test_form_semantic_plan_accepts_fields_alias():
    plan = FormSemanticPlan.model_validate({"fields": [{"componentType": "text"}]})

    assert [component.componentType for component in plan.components] == ["text"]


def test_form_semantic_plan_accepts_items_alias():
    plan = FormSemanticPlan.model_validate({"items": [{"componentType": "email"}]})

    assert [component.componentType for component in plan.components] == ["email"]


def test_form_semantic_plan_accepts_elements_alias():
    plan = FormSemanticPlan.model_validate({"elements": [{"componentType": "phone"}]})

    assert [component.componentType for component in plan.components] == ["phone"]


def test_form_semantic_plan_ignores_extra_root_keys():
    plan = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "components": [{"componentType": "text"}],
            "layout": {"unexpected": True},
        }
    )

    assert plan.model_extra is None
    assert [component.componentType for component in plan.components] == ["text"]


def test_form_semantic_plan_alias_does_not_bypass_active_capability_snapshot():
    plan = FormSemanticPlan.model_validate(
        {"fields": [{"componentType": "alien-widget", "label": "Whatever"}]}
    )

    result = validate_semantic_plan(
        plan,
        capability_snapshot_json=_capability_snapshot(),
        validation_contracts=_validation_contracts(),
    )

    assert result.valid is False
    assert [violation.code for violation in result.violations] == [
        "unknown-component-type"
    ]


# --- multiple violations across components ----------------------------------


def test_story_631_validator_collects_violations_from_multiple_components():
    plan = _plan(
        {"componentType": "phone", "label": "Phone", "widthIntent": "full"},  # width
        {"componentType": "dropdown", "label": "Country", "widthIntent": "half"},  # missing options
        {
            "componentType": "text",
            "label": "Name",
            "widthIntent": "half",
            "validationIntent": {"required": True, "email": True},  # invalid rule
        },
    )

    result = validate_semantic_plan(
        plan,
        capability_snapshot_json=_capability_snapshot(),
        validation_contracts=_validation_contracts(),
    )

    codes = [v.code for v in result.violations]
    assert codes == [
        "width-intent-not-allowed",
        "missing-options-for-choice",
        "invalid-validation-rule",
    ]
    assert [v.componentIndex for v in result.violations] == [0, 1, 2]
