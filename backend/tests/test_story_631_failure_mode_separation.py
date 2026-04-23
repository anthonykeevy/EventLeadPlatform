"""Story 6.3.1 failure-mode separation: each pipeline stage maps to its own
terminalReason and failureClass, and compiler-fault paths NEVER feed back
to the LLM.

Coverage matrix:

    stage failure              | terminalReason            | failureClass     | extra LLM call?
    --------------------------- | ------------------------- | ---------------- | ---------------
    json-parse                  | json-parse-failed         | llm-fault        | yes (until cap)
    semantic-plan (Pydantic)    | semantic-plan-invalid     | llm-fault        | yes (until cap)
    semantic-rules (gate)       | semantic-rules-violated   | llm-fault        | yes (until cap)
    compile (compiler exception)| compiler-error            | compiler-fault   | NEVER
    compile-validation (self-check) | compiler-validation-failed | compiler-fault | NEVER
    happy path                  | validated-success         | none             | n/a
"""

from __future__ import annotations

import json
from typing import Any, Dict, List

from modules.form_ai import service
from modules.form_ai.compiler import compile_semantic_plan_to_definition
from modules.form_ai.schemas import FormSemanticPlan


def _governance_payload() -> Dict[str, Any]:
    """Minimal but complete governance payload that matches the prompts below."""
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
        },
        "componentCapabilitySnapshotJson": {
            "components": [
                {"type": "header", "widthClasses": ["full"]},
                {"type": "text", "widthClasses": ["compact", "half", "full"]},
                {"type": "submit-button", "widthClasses": ["compact", "half"]},
            ]
        },
        "validationContracts": [
            {"componentType": "text", "allowedRules": ["required", "maxLength"]},
            {"componentType": "submit-button", "allowedRules": []},
            {"componentType": "header", "allowedRules": []},
        ],
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
    }


def _patch_governance(monkeypatch, payload: Dict[str, Any] | None = None) -> None:
    monkeypatch.setattr(
        service,
        "_resolve_runtime_governance_versions",
        lambda _db: payload or _governance_payload(),
    )


def _patch_provider(monkeypatch, responses: List[str]) -> Dict[str, int]:
    """Return a counter dict so the test can assert how many times the provider
    was actually called (proves compiler-fault paths do NOT retry)."""
    state = {"count": 0}

    def fake_provider(messages, *args, **kwargs):
        idx = state["count"]
        state["count"] += 1
        if idx < len(responses):
            return responses[idx]
        return responses[-1]

    monkeypatch.setattr(service, "_request_chatgpt_completion", fake_provider)
    return state


def _runtime() -> Dict[str, Any]:
    return {"canvas": {"width": 1280, "height": 800, "gridSize": 8}}


def _well_formed_plan_json(width_intent: str = "full") -> str:
    return json.dumps(
        {
            "semanticPlanVersion": "1.0",
            "formId": "fm-test",
            "title": "Test",
            "components": [
                {
                    "componentType": "text",
                    "label": "Name",
                    "widthIntent": width_intent,
                    "validationIntent": {"required": True},
                },
                {"componentType": "submit-button", "widthIntent": "compact"},
            ],
        }
    )


# --- json-parse-failed ------------------------------------------------------


def test_failure_mode_json_parse_routes_to_dedicated_terminal(monkeypatch):
    counter = _patch_provider(monkeypatch, ["not json"])
    _patch_governance(monkeypatch)

    result = service.generate_form_definition(
        "any prompt",
        runtime_context=_runtime(),
        max_system_correction_attempts=0,
        db_session=None,
    )

    assert result.status == "failed"
    assert result.trace.terminalReason == "json-parse-failed"
    assert result.trace.failureClass == "llm-fault"
    assert counter["count"] == 1
    assert result.trace.attempts[0].failedAt == "json-parse"
    assert result.trace.attempts[0].compileDiagnostics is not None
    assert "jsonParseError" in result.trace.attempts[0].compileDiagnostics


def test_failure_mode_json_parse_uses_dedicated_correction_prompt(monkeypatch):
    """The correction prompt fed back to the LLM after json-parse failure must
    be the json-parse-specific one, not the semantic-plan one. We assert this
    by checking the messages list captured on the second provider call."""
    captured: List[List[Dict[str, Any]]] = []

    def fake_provider(messages, *args, **kwargs):
        captured.append([dict(m) for m in messages])
        return "still not json" if len(captured) > 1 else "first reply not json"

    monkeypatch.setattr(service, "_request_chatgpt_completion", fake_provider)
    _patch_governance(monkeypatch)

    service.generate_form_definition(
        "any prompt",
        runtime_context=_runtime(),
        max_system_correction_attempts=1,
        db_session=None,
    )

    assert len(captured) == 2
    correction = captured[1][-1]["content"]
    assert "not parseable JSON" in correction
    # Negative: must NOT use the semantic-plan correction text.
    assert "FormSemanticPlan validation" not in correction


# --- semantic-plan-invalid (Pydantic shape) ---------------------------------


def test_failure_mode_semantic_plan_routes_to_dedicated_terminal(monkeypatch):
    # JSON is valid but components is the wrong shape (string, not list).
    bad_plan = json.dumps(
        {"semanticPlanVersion": "1.0", "formId": "x", "components": "broken"}
    )
    counter = _patch_provider(monkeypatch, [bad_plan])
    _patch_governance(monkeypatch)

    result = service.generate_form_definition(
        "any prompt",
        runtime_context=_runtime(),
        max_system_correction_attempts=0,
        db_session=None,
    )

    assert result.status == "failed"
    assert result.trace.terminalReason == "semantic-plan-invalid"
    assert result.trace.failureClass == "llm-fault"
    assert counter["count"] == 1
    assert result.trace.attempts[0].failedAt == "semantic-plan"


# --- semantic-rules-violated (NEW gate) -------------------------------------


def test_failure_mode_semantic_rules_routes_to_dedicated_terminal(monkeypatch):
    # widthIntent="full" is not allowed for submit-button in the test snapshot.
    bad_plan = json.dumps(
        {
            "semanticPlanVersion": "1.0",
            "formId": "x",
            "components": [
                {"componentType": "text", "label": "Name", "widthIntent": "half"},
                {"componentType": "submit-button", "widthIntent": "full"},
            ],
        }
    )
    counter = _patch_provider(monkeypatch, [bad_plan])
    _patch_governance(monkeypatch)

    result = service.generate_form_definition(
        "any prompt",
        runtime_context=_runtime(),
        max_system_correction_attempts=0,
        db_session=None,
    )

    assert result.status == "failed"
    assert result.trace.terminalReason == "semantic-rules-violated"
    assert result.trace.failureClass == "llm-fault"
    assert counter["count"] == 1
    assert result.trace.attempts[0].failedAt == "semantic-rules"
    # Last-attempt violations surfaced for triage
    assert result.trace.semanticValidationViolations is not None
    assert len(result.trace.semanticValidationViolations) == 1
    assert (
        result.trace.semanticValidationViolations[0].code
        == "width-intent-not-allowed"
    )


def test_failure_mode_semantic_rules_uses_dedicated_correction_prompt(monkeypatch):
    """Gate violations must use the rules-specific correction prompt (with
    rule codes), not the semantic-plan-shape correction prompt."""
    captured: List[List[Dict[str, Any]]] = []

    bad_plan = json.dumps(
        {
            "semanticPlanVersion": "1.0",
            "formId": "x",
            "components": [
                {"componentType": "text", "label": "Name", "widthIntent": "half"},
                {"componentType": "submit-button", "widthIntent": "full"},
            ],
        }
    )

    def fake_provider(messages, *args, **kwargs):
        captured.append([dict(m) for m in messages])
        return bad_plan  # repeat the same broken plan to exhaust the cap

    monkeypatch.setattr(service, "_request_chatgpt_completion", fake_provider)
    _patch_governance(monkeypatch)

    service.generate_form_definition(
        "any prompt",
        runtime_context=_runtime(),
        max_system_correction_attempts=1,
        db_session=None,
    )

    assert len(captured) == 2
    correction = captured[1][-1]["content"]
    assert "policy gate" in correction
    assert "[width-intent-not-allowed]" in correction


# --- compiler-error (compiler exception) ------------------------------------


def test_failure_mode_compiler_exception_terminates_without_llm_retry(monkeypatch):
    counter = _patch_provider(monkeypatch, [_well_formed_plan_json()])
    _patch_governance(monkeypatch)

    def explode(*args, **kwargs):
        raise RuntimeError("kaboom: compiler bug under test")

    monkeypatch.setattr(
        service, "compile_semantic_plan_to_definition", explode
    )

    result = service.generate_form_definition(
        "any prompt",
        runtime_context=_runtime(),
        max_system_correction_attempts=3,  # cap is generous; we expect zero retries
        db_session=None,
    )

    assert result.status == "failed"
    assert result.trace.terminalReason == "compiler-error"
    assert result.trace.failureClass == "compiler-fault"
    # CRITICAL: compiler exception must NOT trigger another LLM call.
    assert counter["count"] == 1
    assert result.trace.attempts[-1].failedAt == "compile"
    diagnostics = result.trace.attempts[-1].compileDiagnostics
    assert diagnostics is not None
    assert diagnostics["errorType"] == "RuntimeError"
    assert "kaboom" in diagnostics["compilerError"]


def test_failure_mode_compiler_drop_post_gate_is_compiler_error(monkeypatch):
    """If the gate passes but the compiler still drops a component, that is a
    compiler bug (the gate should have caught it). Surface it as compiler-error."""
    counter = _patch_provider(monkeypatch, [_well_formed_plan_json()])
    _patch_governance(monkeypatch)

    real_compile = compile_semantic_plan_to_definition

    def compile_with_drop(plan, **kwargs):
        candidate, summary = real_compile(plan, **kwargs)
        summary["droppedComponentCount"] = 2
        summary["droppedComponentReasons"] = [
            {"componentIndex": 0, "componentType": "text", "reason": "test-injected"},
        ]
        return candidate, summary

    monkeypatch.setattr(
        service, "compile_semantic_plan_to_definition", compile_with_drop
    )

    result = service.generate_form_definition(
        "any prompt",
        runtime_context=_runtime(),
        max_system_correction_attempts=2,
        db_session=None,
    )

    assert result.status == "failed"
    assert result.trace.terminalReason == "compiler-error"
    assert result.trace.failureClass == "compiler-fault"
    assert counter["count"] == 1, "compiler-fault must not trigger LLM retries"
    # Draft must be returned so user/ops can inspect.
    assert result.definitionJSON is not None
    assert result.draftHasValidationIssues is True


# --- compiler-validation-failed (self-check) --------------------------------


def test_failure_mode_compiler_validation_failure_terminates_without_llm_retry(
    monkeypatch,
):
    counter = _patch_provider(monkeypatch, [_well_formed_plan_json()])
    _patch_governance(monkeypatch)

    # Force the post-compile self-check to report invalid output.
    real_validate = service.validate_definition_payload

    def fake_validate(payload):
        result = real_validate(payload)
        # Return a clone with valid=False so the self-check terminates.
        return result.model_copy(update={"valid": False})

    monkeypatch.setattr(service, "validate_definition_payload", fake_validate)

    result = service.generate_form_definition(
        "any prompt",
        runtime_context=_runtime(),
        max_system_correction_attempts=3,
        db_session=None,
    )

    assert result.status == "failed"
    assert result.trace.terminalReason == "compiler-validation-failed"
    assert result.trace.failureClass == "compiler-fault"
    assert counter["count"] == 1, "compiler-fault must not trigger LLM retries"
    assert result.trace.attempts[-1].failedAt == "compile-validation"
    # Draft must be returned so user/ops can inspect.
    assert result.definitionJSON is not None
    assert result.draftHasValidationIssues is True


# --- happy path -------------------------------------------------------------


def test_failure_mode_happy_path_marks_failure_class_none(monkeypatch):
    counter = _patch_provider(monkeypatch, [_well_formed_plan_json()])
    _patch_governance(monkeypatch)

    result = service.generate_form_definition(
        "any prompt",
        runtime_context=_runtime(),
        max_system_correction_attempts=0,
        db_session=None,
    )

    assert result.status == "completed"
    assert result.trace.terminalReason == "validated-success"
    assert result.trace.failureClass == "none"
    assert counter["count"] == 1
    assert result.trace.attempts[-1].failedAt == "none"
    assert result.trace.semanticValidationViolations is None
