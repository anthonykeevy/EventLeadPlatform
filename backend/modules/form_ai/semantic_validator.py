"""Story 6.3.1 semantic-validation gate.

Pure, deterministic gate that runs AFTER FormSemanticPlan parses (so the
shape/Pydantic types are already valid) and BEFORE the deterministic compiler.

Catches LLM faults that the Pydantic schema cannot express:
    * empty plan (no components)
    * componentType not registered in the resolved capability snapshot
    * widthIntent not in this component's allowed widthClasses
    * dropdown/radio/checkbox missing or with empty options
    * validationIntent rule not in this component's allowed rules (per the
      validation contract)
    * componentId reused across components

Each violation carries a stable ``code`` and a human-readable ``message`` +
``suggestion`` that the LLM-correction message renders verbatim. The gate is
binary: if ``violations`` is non-empty, ``valid`` is False and the caller is
expected to either (a) feed a correction prompt to the LLM and retry, or
(b) terminate with terminalReason="semantic-rules-violated".

The gate is intentionally read-only with respect to the plan; it never mutates
the input. All inputs (capability snapshot, validation contracts) follow the
same shape the compiler accepts in :func:`compile_semantic_plan_to_definition`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

from .schemas import FormSemanticPlan, SemanticPlanViolation

# Components that REQUIRE non-empty options to be meaningful in the form. If
# the LLM picks one of these without options, the user is shown a control with
# nothing to choose from.
_CHOICE_COMPONENT_TYPES: Set[str] = {"dropdown", "radio", "checkbox", "select"}


@dataclass
class SemanticPlanValidationResult:
    """Outcome of the semantic-validation gate.

    ``valid`` is True only when ``violations`` is empty. Callers should treat
    this as a binary gate: do not run the compiler when ``valid`` is False.
    """

    valid: bool
    violations: List[SemanticPlanViolation] = field(default_factory=list)


def validate_semantic_plan(
    plan: FormSemanticPlan,
    *,
    capability_snapshot_json: Optional[Dict[str, Any]],
    validation_contracts: Optional[List[Dict[str, Any]]],
) -> SemanticPlanValidationResult:
    """Run the six-rule pre-compile gate.

    Parameters mirror the corresponding arguments on
    :func:`modules.form_ai.compiler.compile_semantic_plan_to_definition` so the
    same governance payload can be passed through both stages without
    transformation.

    Returns a :class:`SemanticPlanValidationResult`. The function never raises
    on validation problems; it raises only on programmer bugs (e.g. ``plan``
    is not a ``FormSemanticPlan``).
    """
    violations: List[SemanticPlanViolation] = []

    if not plan.components:
        violations.append(
            SemanticPlanViolation(
                code="empty-plan",
                message="The semantic plan has no components.",
                suggestion=(
                    "Return at least one component covering the user's prompt, "
                    "and a submit-button at the end if it is a submittable form."
                ),
            )
        )
        # No point in checking per-component rules when the plan is empty.
        return SemanticPlanValidationResult(valid=False, violations=violations)

    known_types = _build_known_types(capability_snapshot_json)
    width_classes_by_type = _build_width_classes_by_type(capability_snapshot_json)
    allowed_rules_by_type = _build_allowed_rules_by_type(validation_contracts)

    seen_component_ids: Dict[str, int] = {}

    for index, component in enumerate(plan.components):
        component_type = (component.componentType or "").strip()
        component_id = component.componentId

        # Rule: unknown-component-type. We only flag when we *have* a snapshot
        # to compare against. An empty/missing snapshot means we trust the LLM
        # (gate is permissive when policy is undefined).
        if known_types is not None and component_type and component_type not in known_types:
            violations.append(
                SemanticPlanViolation(
                    code="unknown-component-type",
                    componentIndex=index,
                    componentId=component_id,
                    componentType=component_type,
                    message=(
                        f"componentType '{component_type}' is not registered in the "
                        "current capability snapshot."
                    ),
                    suggestion=(
                        "Choose one of: "
                        + ", ".join(sorted(known_types))
                        + "."
                        if known_types
                        else "No component types are registered; contact ops."
                    ),
                )
            )
            # Subsequent rules need a known type to look up policies; skip them
            # for this component when the type itself is invalid.
            continue

        # Rule: width-intent-not-allowed. Compare the requested widthIntent
        # against this type's allowed widthClasses (if the snapshot defines
        # them). A None widthIntent is acceptable - the compiler will pick a
        # deterministic default.
        if component.widthIntent is not None and component_type:
            allowed_widths = width_classes_by_type.get(component_type)
            if allowed_widths is not None and component.widthIntent not in allowed_widths:
                violations.append(
                    SemanticPlanViolation(
                        code="width-intent-not-allowed",
                        componentIndex=index,
                        componentId=component_id,
                        componentType=component_type,
                        message=(
                            f"widthIntent '{component.widthIntent}' is not allowed for "
                            f"componentType '{component_type}'."
                        ),
                        suggestion=(
                            "Use one of: " + ", ".join(allowed_widths) + "."
                            if allowed_widths
                            else (
                                "This component type has no allowed widthClasses in the "
                                "current snapshot; contact ops."
                            )
                        ),
                    )
                )

        # Rule: missing-options-for-choice. dropdown/radio/checkbox/select must
        # carry at least one usable option.
        if component_type in _CHOICE_COMPONENT_TYPES:
            options = component.options
            if not isinstance(options, list) or not options:
                violations.append(
                    SemanticPlanViolation(
                        code="missing-options-for-choice",
                        componentIndex=index,
                        componentId=component_id,
                        componentType=component_type,
                        message=(
                            f"componentType '{component_type}' requires a non-empty "
                            "options array."
                        ),
                        suggestion=(
                            "Add options as an array of {label, value} objects "
                            "covering every choice the user can make."
                        ),
                    )
                )

        # Rule: invalid-validation-rule. Only flag rule keys actually set by
        # the LLM (we ignore None values that Pydantic carries as defaults).
        if component.validationIntent is not None and component_type:
            allowed_rules = allowed_rules_by_type.get(component_type)
            if allowed_rules is not None:
                requested_rules = component.validationIntent.model_dump(exclude_none=True)
                disallowed = sorted(
                    rule for rule in requested_rules.keys() if rule not in allowed_rules
                )
                if disallowed:
                    violations.append(
                        SemanticPlanViolation(
                            code="invalid-validation-rule",
                            componentIndex=index,
                            componentId=component_id,
                            componentType=component_type,
                            message=(
                                f"validationIntent for '{component_type}' uses "
                                f"disallowed rule(s): {', '.join(disallowed)}."
                            ),
                            suggestion=(
                                "Allowed rules for this componentType: "
                                + (", ".join(sorted(allowed_rules)) if allowed_rules else "(none)")
                                + "."
                            ),
                        )
                    )

        # Rule: duplicate-component-id. Only enforced when the LLM explicitly
        # set componentId (otherwise the compiler synthesises a unique one).
        if component_id:
            if component_id in seen_component_ids:
                violations.append(
                    SemanticPlanViolation(
                        code="duplicate-component-id",
                        componentIndex=index,
                        componentId=component_id,
                        componentType=component_type or None,
                        message=(
                            f"componentId '{component_id}' is reused (first seen at index "
                            f"{seen_component_ids[component_id]})."
                        ),
                        suggestion=(
                            "Give every component a unique componentId, or omit "
                            "componentId entirely and let the compiler synthesise one."
                        ),
                    )
                )
            else:
                seen_component_ids[component_id] = index

    return SemanticPlanValidationResult(valid=not violations, violations=violations)


# --- internal helpers --------------------------------------------------------


def _build_known_types(
    capability_snapshot_json: Optional[Dict[str, Any]],
) -> Optional[Set[str]]:
    """Return the set of registered componentTypes, or None when no snapshot.

    None means "no opinion" - the gate becomes permissive for the
    unknown-component-type rule. An empty set means "snapshot present but
    declares zero types" which is itself an ops misconfiguration; the gate
    will still flag every type as unknown in that case (intentional - it
    surfaces the misconfig instead of silently passing it through).
    """
    if not isinstance(capability_snapshot_json, dict):
        return None
    components = capability_snapshot_json.get("components")
    if not isinstance(components, list):
        return None
    types: Set[str] = set()
    for row in components:
        if not isinstance(row, dict):
            continue
        type_name = str(row.get("type", "")).strip()
        if type_name:
            types.add(type_name)
    return types


def _build_width_classes_by_type(
    capability_snapshot_json: Optional[Dict[str, Any]],
) -> Dict[str, List[str]]:
    """Map componentType -> allowed widthClasses list (preserving snapshot order).

    Returns an empty dict when no snapshot or when no row carries
    widthClasses. The gate treats absence as "no opinion" (skips the
    width-intent-not-allowed rule for that type).
    """
    mapped: Dict[str, List[str]] = {}
    if not isinstance(capability_snapshot_json, dict):
        return mapped
    components = capability_snapshot_json.get("components")
    if not isinstance(components, list):
        return mapped
    for row in components:
        if not isinstance(row, dict):
            continue
        type_name = str(row.get("type", "")).strip()
        if not type_name:
            continue
        width_classes = row.get("widthClasses")
        if isinstance(width_classes, list):
            normalised = [str(item).strip() for item in width_classes if str(item).strip()]
            mapped[type_name] = normalised
    return mapped


def _build_allowed_rules_by_type(
    validation_contracts: Optional[List[Dict[str, Any]]],
) -> Dict[str, Set[str]]:
    """Map componentType -> set of allowed validationIntent rule keys.

    Mirrors :func:`modules.form_ai.compiler._build_allowed_rules` shape but
    returns sets for O(1) membership checks. Absence (no contract row) means
    the gate skips the invalid-validation-rule check for that type.
    """
    mapped: Dict[str, Set[str]] = {}
    if not isinstance(validation_contracts, list):
        return mapped
    for row in validation_contracts:
        if not isinstance(row, dict):
            continue
        type_name = str(row.get("componentType", "")).strip()
        if not type_name:
            continue
        allowed = row.get("allowedRules")
        if isinstance(allowed, list):
            mapped[type_name] = {str(rule).strip() for rule in allowed if str(rule).strip()}
    return mapped
