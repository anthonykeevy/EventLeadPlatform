import json
import logging
import math
import os
import re
import time
import uuid
import hashlib
from pathlib import Path
from typing import Any, Dict, Iterable, List, Literal, Optional, Tuple

import httpx
from pydantic import ValidationError
from sqlalchemy import text
from sqlalchemy.orm import Session

from common.request_context import get_current_request_context

from middleware.outbound_request_logger import timed_log_outbound_http_request
from modules.form_validate.schemas import (
    BoundaryDirectionFlags,
    BoundaryViolation,
    CollisionViolation,
    FormValidationResponse,
    SchemaError,
    ValidationSummary,
)
from modules.form_validate.service import (
    DEFAULT_HEIGHT_BY_TYPE,
    _parse_dimension,
    validate_definition_payload,
)

from .schemas import (
    AttemptTraceEntry,
    AttemptValidationSummary,
    FormSemanticPlan,
    FormAiGenerateResponse,
    FormAiRemeasureRequest,
    FormAiRemeasureResponse,
    GenerationTraceMetadata,
    SemanticComponentIntent,
    SemanticPlanViolation,
)
from .compiler import (
    LAYOUT_MODE_HORIZONTAL_STACKED,
    compile_semantic_plan_to_definition,
    resolve_layout_mode,
)
from .semantic_validator import (
    SemanticPlanValidationResult,
    validate_semantic_plan,
)

# Fallback used when AppSetting row is absent or DB is unreachable on startup.
_DEFAULT_RETRIES_FALLBACK = 2
# Module-level cache for form_ai.default_retries AppSetting value.
# Set to None to force a reload on next call to _get_default_retries().
_cached_default_retries: Optional[int] = None

MAX_SYSTEM_CORRECTION_ATTEMPTS = _DEFAULT_RETRIES_FALLBACK  # kept for backward compat
_ROOT_PATH = Path(__file__).resolve().parents[3]
CONTEXT_PACK_PATH = _ROOT_PATH / "docs" / "stories" / "STORY-6.2-AI-CONTEXT-PACK.md"
LOGGER = logging.getLogger(__name__)


def _load_context_pack() -> str:
    try:
        return CONTEXT_PACK_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError("context-pack-load-failed") from exc


def _env_flag(name: str, default: bool) -> bool:
    """Read a boolean env flag. Falls back to ``default`` when unset/empty/invalid.

    Truthy values: 1, true, yes, on. Falsy values: 0, false, no, off.
    Used by Story 6.3.1 to gate post-processing transforms in the deterministic-grid
    compiler path so the compiler stays the single owner of layout by default.
    """
    raw = os.getenv(name, "").strip().lower()
    if raw in {"1", "true", "yes", "on"}:
        return True
    if raw in {"0", "false", "no", "off"}:
        return False
    return default


def _get_default_retries(db_session: Optional[Session] = None) -> int:
    """Return the default system correction attempt count from config.AppSetting.

    Value is module-level cached after the first successful read.
    Falls back to ``_DEFAULT_RETRIES_FALLBACK`` (2) when:
      - The AppSetting row does not exist yet (pre-migration environment)
      - No db_session is supplied
      - Any DB error occurs

    Call ``_invalidate_default_retries_cache()`` to force a reload (e.g. from an
    ops endpoint after updating the AppSetting row).
    """
    global _cached_default_retries
    if _cached_default_retries is not None:
        return _cached_default_retries

    if db_session is None:
        return _DEFAULT_RETRIES_FALLBACK

    try:
        from sqlalchemy import text as _text
        row = db_session.execute(
            _text(
                "SELECT TOP 1 [SettingValue] FROM [config].[AppSetting] "
                "WHERE [SettingKey] = N'form_ai.default_retries' AND [IsDeleted] = 0"
            )
        ).fetchone()
        if row and row[0] is not None:
            value = max(0, min(10, int(row[0])))
            _cached_default_retries = value
            return value
    except Exception as exc:
        LOGGER.warning("form_ai.default_retries: AppSetting read failed (%s), using fallback %d", exc, _DEFAULT_RETRIES_FALLBACK)

    return _DEFAULT_RETRIES_FALLBACK


def _invalidate_default_retries_cache() -> None:
    """Reset the module-level cache so the next call re-reads from AppSetting."""
    global _cached_default_retries
    _cached_default_retries = None


def _summarise_semantic_plan_error(exc: BaseException) -> str:
    """Compact, model-friendly summary of why FormSemanticPlan parsing failed."""
    if isinstance(exc, ValidationError):
        parts: List[str] = []
        for err in exc.errors()[:6]:
            loc = ".".join(str(p) for p in err.get("loc", ())) or "<root>"
            msg = err.get("msg", "invalid")
            parts.append(f"{loc}: {msg}")
        more = max(0, len(exc.errors()) - 6)
        if more:
            parts.append(f"...and {more} more")
        return " | ".join(parts) or str(exc)
    return str(exc)


def _build_semantic_plan_correction_message(error_summary: str) -> str:
    return (
        "Your previous JSON failed FormSemanticPlan validation. Errors:\n"
        f"  {error_summary}\n\n"
        "Return a corrected JSON object that strictly matches FormSemanticPlan:\n"
        "  - semanticPlanVersion MUST be the string \"1.0\".\n"
        "  - Root keys: semanticPlanVersion, formId, title, components.\n"
        "  - Each component: componentType (required), label, optional placeholder/helpText, "
        "widthIntent in {compact|half|full}, optional options (array of {label,value}), "
        "optional validationIntent.\n"
        "  - validationIntent MUST be an OBJECT with boolean keys "
        "(required, email, phone, url) or numeric keys (minLength, maxLength, min, max). "
        "Do NOT use a list of strings.\n"
        "Return only valid JSON. No markdown, no prose."
    )


def _correction_message_for_json_parse(error_summary: str) -> str:
    """Story 6.3.1 (failure-mode separation): correction prompt for the
    json-parse stage.

    Distinct from the semantic-plan correction message because the LLM has not
    even produced parseable JSON at this point, so listing FormSemanticPlan
    field rules adds noise. Keep this short and focused on the JSON shape.
    """
    return (
        "Your previous response was not parseable JSON.\n"
        f"Parser said: {error_summary}\n\n"
        "Return a single JSON object (no markdown fences, no prose, no comments) "
        "that conforms to FormSemanticPlan. Re-emit the entire object."
    )


def _correction_message_for_semantic_rules(
    violations: List[SemanticPlanViolation],
) -> str:
    """Story 6.3.1 (failure-mode separation): correction prompt for the
    semantic-validation gate (LLM-fault rules that run before compile).

    Renders the violation list with stable rule codes the LLM can act on. Each
    line names the offending component (by id when present, else by index) so
    the model can target the fix instead of regenerating the entire plan.
    """
    lines: List[str] = []
    for violation in violations:
        target = violation.componentId or (
            f"components[{violation.componentIndex}]"
            if violation.componentIndex is not None
            else "(plan)"
        )
        suffix = (
            f" Suggestion: {violation.suggestion}" if violation.suggestion else ""
        )
        lines.append(
            f"- [{violation.code}] {target}: {violation.message}{suffix}"
        )

    return (
        "Your previous semantic plan parsed but failed the policy gate "
        "(componentType registry, widthClasses, options, validation contract, "
        "or unique componentIds). Fix every issue below and re-emit the "
        "entire FormSemanticPlan as one JSON object:\n"
        + "\n".join(lines)
        + "\n\nKeep the user's original intent. Only change what is necessary "
        "to clear these violations."
    )


# Story 6.3.1 (failure-mode separation): map terminalReason -> coarse failure
# class for dashboards. New reasons added by this slice are listed first; the
# legacy reasons keep their existing semantics.
_FAILURE_CLASS_BY_REASON: Dict[str, str] = {
    "validated-success": "none",
    "provider-error": "provider-fault",
    "context-pack-load-failed": "infrastructure-fault",
    "json-parse-failed": "llm-fault",
    "semantic-plan-invalid": "llm-fault",
    "semantic-rules-violated": "llm-fault",
    "compiler-error": "compiler-fault",
    "compiler-validation-failed": "compiler-fault",
    "retry-cap-exhausted": "llm-fault",
    "first-shot-invalid": "llm-fault",
}


def _classify_failure(terminal_reason: str) -> str:
    """Return the failure-class label for a terminalReason value.

    Defaults to ``"llm-fault"`` for unknown reasons rather than ``"none"``
    because an unknown terminal reason means we have a non-success outcome we
    forgot to map; surfacing it as an llm-fault is the safer dashboard
    default (it shows up in the same bucket as retry-cap-exhausted).
    """
    if not terminal_reason:
        return "llm-fault"
    return _FAILURE_CLASS_BY_REASON.get(terminal_reason, "llm-fault")


def _extract_json_candidate(raw_content: str) -> Dict[str, Any]:
    cleaned = raw_content.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.replace("json", "", 1).strip()

    try:
        parsed = json.loads(cleaned)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("json-parse-failed")

    sliced = cleaned[start : end + 1]
    parsed = json.loads(sliced)
    if not isinstance(parsed, dict):
        raise ValueError("json-parse-failed")
    return parsed


def _infer_width_intent_from_component(
    component: Dict[str, Any], canvas_width: float
) -> str:
    # Story 6.3.1 (semantic gate compatibility): submit-button is universally
    # compact/half in registered snapshots. Mapping a legacy 9999-px style.width
    # to "full" trips the new semantic-validation gate even though the legacy
    # input was clearly broken. Clamp here so the legacy bridge always emits a
    # gate-safe intent for submit-button.
    component_type = str(component.get("type", "")).strip()
    if component_type == "submit-button":
        return "compact"
    style = component.get("style") if isinstance(component.get("style"), dict) else {}
    props = component.get("props") if isinstance(component.get("props"), dict) else {}
    width = _parse_positive_dimension(style.get("width", props.get("width")), 0.0)
    if width <= 0:
        return "half"
    full_threshold = canvas_width * 0.72
    compact_threshold = canvas_width * 0.28
    if width >= full_threshold:
        return "full"
    if width <= compact_threshold:
        return "compact"
    return "half"


def _semantic_plan_from_legacy_definition(
    definition_candidate: Dict[str, Any]
) -> FormSemanticPlan:
    pages = definition_candidate.get("pages")
    if not isinstance(pages, list) or not pages:
        raise ValueError("semantic-plan-missing-components")
    first_page = pages[0] if isinstance(pages[0], dict) else {}
    components = first_page.get("components")
    if not isinstance(components, list):
        raise ValueError("semantic-plan-missing-components")

    canvas = definition_candidate.get("canvasSettings")
    canvas_width = 1920.0
    if isinstance(canvas, dict):
        canvas_width = _parse_positive_dimension(canvas.get("width"), 1920.0)

    semantic_components: List[Dict[str, Any]] = []
    for component in components:
        if not isinstance(component, dict):
            continue
        component_type = str(component.get("type", "")).strip()
        if not component_type:
            continue
        props = component.get("props") if isinstance(component.get("props"), dict) else {}
        label = props.get("label")
        # Story 6.3.1 (semantic gate compatibility): only carry a
        # validationIntent into the plan when the legacy props supplied an
        # explicit validation dict OR required=True. Synthesising a default
        # {"required": False} would trip the new invalid-validation-rule check
        # for component types whose contract allows no rules (submit-button,
        # header, paragraph, divider, ...).
        validation_intent: Optional[Dict[str, Any]]
        if isinstance(props.get("validation"), dict):
            validation_intent = props.get("validation")
        elif bool(props.get("required")):
            validation_intent = {"required": True}
        else:
            validation_intent = None
        semantic_components.append(
            {
                "componentId": component.get("id"),
                "componentType": component_type,
                "label": label if isinstance(label, str) else None,
                "placeholder": props.get("placeholder")
                if isinstance(props.get("placeholder"), str)
                else None,
                "helpText": props.get("helpText")
                if isinstance(props.get("helpText"), str)
                else None,
                "widthIntent": _infer_width_intent_from_component(component, canvas_width),
                "actionAlignment": (
                    "center" if component_type == "submit-button" else None
                ),
                "options": props.get("options")
                if isinstance(props.get("options"), list)
                else None,
                "validationIntent": validation_intent,
            }
        )

    return FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "formId": str(definition_candidate.get("formId", "ai-generated-form")),
            "title": first_page.get("title")
            if isinstance(first_page.get("title"), str)
            else "Page 1",
            "components": semantic_components,
        }
    )


def _extract_semantic_plan_candidate(raw_candidate: Dict[str, Any]) -> FormSemanticPlan:
    if "components" in raw_candidate and "semanticPlanVersion" in raw_candidate:
        return FormSemanticPlan.model_validate(raw_candidate)
    if "components" in raw_candidate and "pages" not in raw_candidate:
        candidate = dict(raw_candidate)
        candidate.setdefault("semanticPlanVersion", "1.0")
        return FormSemanticPlan.model_validate(candidate)
    if "pages" in raw_candidate:
        return _semantic_plan_from_legacy_definition(raw_candidate)
    raise ValueError("semantic-plan-parse-failed")


def _normalize_display_component_props(definition: Dict[str, Any]) -> Dict[str, Any]:
    pages = definition.get("pages")
    if not isinstance(pages, list):
        return definition

    def walk(items: List[Any]) -> None:
        for item in items:
            if not isinstance(item, dict):
                continue
            component_type = str(item.get("type", "")).strip()
            props = item.get("props")
            if isinstance(props, dict) and component_type in {"header", "paragraph"}:
                label = props.get("label")
                text = props.get("text")
                if (not isinstance(label, str) or not label.strip()) and isinstance(text, str):
                    if text.strip():
                        props["label"] = text.strip()
            children = item.get("children")
            if isinstance(children, list):
                walk(children)

    for page in pages:
        if not isinstance(page, dict):
            continue
        components = page.get("components")
        if isinstance(components, list):
            walk(components)
    return definition


def _prompt_requests_heading(prompt: str) -> bool:
    lowered = prompt.lower()
    heading_markers = (
        "header",
        "heading",
        "title",
        "banner",
        "intro",
        "introduction",
    )
    return any(re.search(rf"\b{re.escape(marker)}\b", lowered) for marker in heading_markers)


def _is_placeholder_heading_text(value: Any) -> bool:
    if not isinstance(value, str):
        return True
    text = value.strip()
    if not text:
        return True
    if text in {"-", "--", "---", "_", ".", "|", "~"}:
        return True
    return False


def _filter_unrequested_headings_from_plan(
    semantic_plan: FormSemanticPlan, prompt: str
) -> Tuple[FormSemanticPlan, int]:
    """Strip ``header``/``paragraph`` intents from the semantic plan when the
    user prompt didn't ask for one.

    Background: The LLM frequently emits a courtesy ``header`` intent ("Contact
    Form" etc.) even when the prompt has no heading-related keyword. The
    *post-compile* heading filter then drops the rendered header from the page,
    but the compiler has already laid out the rest of the form *below* that
    header — so first-name ends up at ``y = margin + header_height + row_gap``
    (~104 px) and a ghost gap is left at the top of the canvas (UAT round 5
    reproduced this on prompt 1: the live canvas had ~80 px of empty space
    above First name).

    Filtering at the *plan* stage instead means the compiler never reserves
    that vertical real estate, so the first real component sits exactly at
    ``DEFAULT_MARGIN_Y`` and the top gap matches every other inter-row gap.

    Placeholder-text headings (``"-"``, ``""``, etc.) are still dropped here
    too — there's no point laying them out and then removing them, regardless
    of what the prompt says.

    Returns the (possibly new) plan and the count of intents removed so we can
    surface the diagnostic via ``compileSummary``.
    """
    if not semantic_plan.components:
        return semantic_plan, 0
    allow_heading = _prompt_requests_heading(prompt)
    kept: List[SemanticComponentIntent] = []
    dropped = 0
    for component in semantic_plan.components:
        component_type = (component.componentType or "").strip().lower()
        if component_type in {"header", "paragraph"}:
            label = component.label
            if _is_placeholder_heading_text(label):
                dropped += 1
                continue
            if component_type == "header" and not allow_heading:
                dropped += 1
                continue
        kept.append(component)
    if dropped == 0:
        return semantic_plan, 0
    filtered = semantic_plan.model_copy(update={"components": kept})
    return filtered, dropped


def _sort_index_for_tab_order(component: Dict[str, Any], fallback_index: int) -> tuple[float, float, int]:
    position = component.get("position")
    x_val = 0.0
    y_val = 0.0
    if isinstance(position, dict):
        y_val = _parse_number(position.get("y"), 0.0)
        x_val = _parse_number(position.get("x"), 0.0)
    return (y_val, x_val, fallback_index)


def _resolve_canvas_height(
    definition: Dict[str, Any], runtime_context: Optional[Dict[str, Any]]
) -> float:
    runtime_canvas = runtime_context.get("canvas") if runtime_context else None
    if isinstance(runtime_canvas, dict):
        runtime_height = _parse_positive_dimension(runtime_canvas.get("height"), 0.0)
        if runtime_height > 0:
            return runtime_height
    canvas = definition.get("canvasSettings")
    if isinstance(canvas, dict):
        canvas_height = _parse_positive_dimension(canvas.get("height"), 0.0)
        if canvas_height > 0:
            return canvas_height
    return 0.0


def _effective_component_height(
    component: Dict[str, Any], runtime_footprints: Dict[str, Dict[str, float]]
) -> float:
    component_type = str(component.get("type", "")).strip()
    props = component.get("props")
    if not isinstance(props, dict):
        props = {}
    style = component.get("style")
    style_height = 0.0
    if isinstance(style, dict):
        style_height = _parse_positive_dimension(style.get("height"), 0.0)
    min_height = _minimum_render_height(component_type, props, runtime_footprints)
    return max(style_height, min_height)


def _sync_style_dimensions_into_props(definition: Dict[str, Any]) -> Dict[str, Any]:
    pages = definition.get("pages")
    if not isinstance(pages, list):
        return definition

    def walk(items: List[Any]) -> None:
        for item in items:
            if not isinstance(item, dict):
                continue
            props = item.get("props")
            if not isinstance(props, dict):
                props = {}
                item["props"] = props
            style = item.get("style")
            if isinstance(style, dict):
                width = _parse_positive_dimension(style.get("width"), 0.0)
                height = _parse_positive_dimension(style.get("height"), 0.0)
                if width > 0:
                    props["width"] = f"{int(round(width))}px"
                if height > 0:
                    props["height"] = int(round(height))
            children = item.get("children")
            if isinstance(children, list):
                walk(children)

    for page in pages:
        if not isinstance(page, dict):
            continue
        components = page.get("components")
        if isinstance(components, list):
            walk(components)

    return definition


def _single_column_layout_detected(
    components: List[Dict[str, Any]], grid_size: float
) -> bool:
    x_values: List[float] = []
    for component in components:
        position = component.get("position")
        if not isinstance(position, dict):
            return False
        x_values.append(_parse_number(position.get("x"), 0.0))
    if not x_values:
        return False
    tolerance = max(32.0, grid_size * 2.0)
    return (max(x_values) - min(x_values)) <= tolerance


def _rebalance_single_column_vertical_spacing(
    definition: Dict[str, Any], runtime_context: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    pages = definition.get("pages")
    if not isinstance(pages, list) or not pages:
        return definition

    canvas_height = _resolve_canvas_height(definition, runtime_context)
    if canvas_height <= 0:
        return definition

    runtime_footprints = _build_runtime_footprint_map(runtime_context)
    grid_size = 0.0
    runtime_canvas = runtime_context.get("canvas") if runtime_context else None
    if isinstance(runtime_canvas, dict):
        grid_size = _parse_positive_dimension(runtime_canvas.get("gridSize"), 0.0)

    for page in pages:
        if not isinstance(page, dict):
            continue
        components = page.get("components")
        if not isinstance(components, list) or len(components) < 2:
            continue
        normalized_components = [item for item in components if isinstance(item, dict)]
        if len(normalized_components) < 2:
            continue
        if not _single_column_layout_detected(normalized_components, grid_size):
            continue

        sorted_components = sorted(
            enumerate(normalized_components),
            key=lambda pair: _sort_index_for_tab_order(pair[1], pair[0]),
        )
        heights: List[float] = []
        for _, component in sorted_components:
            height = _effective_component_height(component, runtime_footprints)
            heights.append(height)

            style = component.get("style")
            if not isinstance(style, dict):
                style = {}
                component["style"] = style
            style["height"] = int(round(height))

            props = component.get("props")
            if not isinstance(props, dict):
                props = {}
                component["props"] = props
            props["height"] = int(round(height))

        total_height = sum(heights)
        if total_height <= 0:
            continue

        available_space = canvas_height - total_height
        if available_space <= 0:
            continue

        spaces = len(sorted_components) + 1
        gap = float(int(available_space // spaces))
        if gap < 0:
            gap = 0.0

        y_cursor = gap
        for idx, (_, component) in enumerate(sorted_components):
            position = component.get("position")
            if not isinstance(position, dict):
                position = {}
                component["position"] = position
            position["y"] = int(round(y_cursor))
            y_cursor += heights[idx] + gap

    return definition


def _post_process_generated_definition(
    definition: Dict[str, Any],
    prompt: str,
    runtime_context: Optional[Dict[str, Any]],
    *,
    compiler_mode: str = "legacy",
) -> tuple[Dict[str, Any], Dict[str, bool]]:
    """Run flag-gated post-processing transforms on a generated definition.

    Returns the (possibly mutated) definition together with a record of which
    transforms actually ran, so AC-3 (transform visibility) can surface the
    decision through ``compileSummary.postProcessingApplied``.

    Defaults change per ``compiler_mode``:
    - ``deterministic-grid``: destructive geometry transforms (sync-style-into-props,
      single-column rebalance) default OFF so the compiler stays the single owner
      of layout. Heading filter and tab order rewrite stay ON.
    - ``legacy``: all transforms default ON to preserve pre-Story-6.3.1 behaviour.

    Each transform can still be force-toggled via env var:
      FORM_AI_PP_HEADING_FILTER, FORM_AI_PP_TAB_ORDER,
      FORM_AI_PP_SYNC_STYLE_PROPS, FORM_AI_PP_REBALANCE.
    """
    is_deterministic = compiler_mode == "deterministic-grid"
    apply_heading_filter = _env_flag("FORM_AI_PP_HEADING_FILTER", default=True)
    apply_tab_order = _env_flag("FORM_AI_PP_TAB_ORDER", default=True)
    apply_sync_style_props = _env_flag(
        "FORM_AI_PP_SYNC_STYLE_PROPS", default=not is_deterministic
    )
    apply_rebalance = _env_flag(
        "FORM_AI_PP_REBALANCE", default=not is_deterministic
    )

    applied: Dict[str, bool] = {
        "headingFilter": False,
        "tabOrder": False,
        "syncStyleProps": False,
        "rebalance": False,
    }

    pages = definition.get("pages")
    if not isinstance(pages, list):
        return definition, applied

    allow_heading = _prompt_requests_heading(prompt)
    for page in pages:
        if not isinstance(page, dict):
            continue
        components = page.get("components")
        if not isinstance(components, list):
            continue

        if apply_heading_filter:
            filtered_components: List[Dict[str, Any]] = []
            for component in components:
                if not isinstance(component, dict):
                    continue
                component_type = str(component.get("type", "")).strip()
                props = component.get("props")
                if not isinstance(props, dict):
                    props = {}
                    component["props"] = props

                if component_type in {"header", "paragraph"}:
                    label = props.get("label")
                    if _is_placeholder_heading_text(label):
                        continue
                    if component_type == "header" and not allow_heading:
                        continue
                filtered_components.append(component)
            applied["headingFilter"] = True
        else:
            filtered_components = [c for c in components if isinstance(c, dict)]

        if apply_tab_order:
            sorted_pairs = sorted(
                enumerate(filtered_components),
                key=lambda pair: _sort_index_for_tab_order(pair[1], pair[0]),
            )
            for tab_order, (_, component) in enumerate(sorted_pairs, start=1):
                props = component.get("props")
                if not isinstance(props, dict):
                    props = {}
                    component["props"] = props
                props["tabOrder"] = tab_order
            applied["tabOrder"] = True

        page["components"] = filtered_components

    if apply_sync_style_props:
        definition = _sync_style_dimensions_into_props(definition)
        applied["syncStyleProps"] = True
    if apply_rebalance:
        definition = _rebalance_single_column_vertical_spacing(definition, runtime_context)
        applied["rebalance"] = True
    return definition, applied


def _validate_single_page_guardrail(definition: Dict[str, Any]) -> List[SchemaError]:
    errors: List[SchemaError] = []
    pages = definition.get("pages")
    if not isinstance(pages, list):
        return errors
    if len(pages) != 1:
        errors.append(
            SchemaError(
                path="pages",
                message="Story 6.2 supports single-page generation only",
                code="story6_2.single_page_only",
            )
        )
    return errors


def _merge_guardrail_errors(
    base_validation: FormValidationResponse, guardrail_errors: List[SchemaError]
) -> FormValidationResponse:
    if not guardrail_errors:
        return base_validation

    schema_errors = list(base_validation.schemaErrors) + guardrail_errors
    error_count = (
        len(schema_errors)
        + len(base_validation.boundaryViolations)
        + len(base_validation.collisions)
    )
    return FormValidationResponse(
        valid=False,
        schemaErrors=schema_errors,
        boundaryViolations=base_validation.boundaryViolations,
        collisions=base_validation.collisions,
        summary=ValidationSummary(errorCount=error_count, warningCount=0),
        meta=base_validation.meta,
    )


def _validation_summary(validation: FormValidationResponse) -> AttemptValidationSummary:
    return AttemptValidationSummary(
        valid=validation.valid,
        schemaErrorCount=len(validation.schemaErrors),
        boundaryViolationCount=len(validation.boundaryViolations),
        collisionCount=len(validation.collisions),
        errorCount=validation.summary.errorCount,
    )


def _build_runtime_footprint_map(
    runtime_context: Optional[Dict[str, Any]],
) -> Dict[str, Dict[str, float]]:
    if not runtime_context:
        return {}
    raw = runtime_context.get("componentFootprints")
    if not isinstance(raw, list):
        return {}
    mapped: Dict[str, Dict[str, float]] = {}
    for item in raw:
        if not isinstance(item, dict):
            continue
        component_type = str(item.get("componentType", "")).strip()
        if not component_type:
            continue
        width = _parse_positive_dimension(item.get("width"), 0.0)
        height = _parse_positive_dimension(item.get("height"), 0.0)
        gap = _parse_positive_dimension(item.get("recommendedGapAfter"), 0.0)
        if width <= 0 or height <= 0:
            continue
        mapped[component_type] = {
            "width": width,
            "height": height,
            "recommendedGapAfter": gap,
        }
    return mapped


def _capability_type_summary(
    capability_snapshot_json: Optional[Dict[str, Any]],
) -> List[Tuple[str, List[str]]]:
    """Return [(componentType, [allowed width classes])] from the active snapshot.

    Empty list when the snapshot is missing or malformed; callers should treat
    that as "no allow-list known" (e.g. legacy DB-empty governance) and fall
    back to permissive behaviour.
    """
    if not isinstance(capability_snapshot_json, dict):
        return []
    components = capability_snapshot_json.get("components")
    if not isinstance(components, list):
        return []
    summary: List[Tuple[str, List[str]]] = []
    for row in components:
        if not isinstance(row, dict):
            continue
        component_type = str(row.get("type", "")).strip()
        if not component_type:
            continue
        width_classes_raw = row.get("widthClasses")
        if isinstance(width_classes_raw, list):
            widths = [
                str(item).strip()
                for item in width_classes_raw
                if isinstance(item, (str, int, float)) and str(item).strip()
            ]
        else:
            widths = []
        summary.append((component_type, widths))
    summary.sort(key=lambda pair: pair[0])
    return summary


def _filter_runtime_context_to_capability(
    runtime_context: Optional[Dict[str, Any]],
    capability_snapshot_json: Optional[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    """Drop ``componentFootprints`` entries the active snapshot doesn't register.

    The frontend builds ``componentFootprints`` from the live toolbox DOM,
    which can advertise types (``rating``, ``file-upload``, ``first-name``...)
    that are not registered in the current capability snapshot. Sending those
    to the LLM led the model to emit unregistered components, which the
    semantic-validation gate then rejected as ``unknown-component-type`` — and
    the only correction round-trip was wasted relabelling them. Filtering up
    front gives the LLM a faithful palette of what the compiler actually
    accepts.

    Behaviour:
      * No snapshot known → return ``runtime_context`` unchanged (permissive).
      * Snapshot present → keep only footprints whose ``componentType`` is in
        the snapshot's ``components[].type`` set.
      * No ``runtime_context`` → return ``None`` unchanged.
    """
    if runtime_context is None:
        return None
    summary = _capability_type_summary(capability_snapshot_json)
    if not summary:
        return runtime_context
    allowed_types = {component_type for component_type, _ in summary}
    footprints = runtime_context.get("componentFootprints")
    if not isinstance(footprints, list):
        return runtime_context
    filtered: List[Any] = []
    for entry in footprints:
        if not isinstance(entry, dict):
            continue
        component_type = str(entry.get("componentType", "")).strip()
        if component_type and component_type in allowed_types:
            filtered.append(entry)
    if filtered == footprints:
        return runtime_context
    next_context = dict(runtime_context)
    next_context["componentFootprints"] = filtered
    return next_context


def _build_capability_prompt_block(
    capability_snapshot_json: Optional[Dict[str, Any]],
) -> str:
    """Render an "ALLOWED COMPONENT TYPES" block for the system prompt.

    Lists each registered ``componentType`` with its allowed ``widthIntent``
    values so the LLM can self-constrain on the first attempt — eliminating
    the most common cause of correction-loop usage observed in UAT. The widths
    here are the *vocabulary* the compiler will accept as a hint; the final
    pixel width is decided by the deterministic compiler's tier table.
    """
    summary = _capability_type_summary(capability_snapshot_json)
    if not summary:
        return ""
    lines = ["ALLOWED COMPONENT TYPES (snapshot-authoritative; do NOT invent others):"]
    for component_type, widths in summary:
        if widths:
            lines.append(
                f"  - {component_type} (allowed widthIntent hints: {', '.join(widths)})"
            )
        else:
            lines.append(f"  - {component_type}")
    lines.append(
        "If the user asks for a feature that isn't in this list "
        "(e.g. signature capture, payment collection), use the closest registered type "
        "and put a brief explanation in helpText."
    )
    return "\n".join(lines)


def _build_runtime_context_block(runtime_context: Optional[Dict[str, Any]]) -> str:
    if not runtime_context:
        return ""
    try:
        safe_payload = json.dumps(runtime_context, ensure_ascii=True)
    except (TypeError, ValueError):
        return ""
    terms_defaults = runtime_context.get("termsDefaults")
    terms_rules = ""
    if isinstance(terms_defaults, dict) and terms_defaults.get("hasCompanyTerms") is True:
        link_text = terms_defaults.get("termsLinkText")
        terms_rules = (
            "\nTerms defaults rule: company-managed terms are available. "
            "Use a `terms` component for consent, keep `props.termsUrl` and `props.termsContent` empty "
            "unless user explicitly asks to replace legal source, and preserve company link behavior."
        )
        if isinstance(link_text, str) and link_text.strip():
            terms_rules += f" Prefer `props.termsLinkText` = \"{link_text.strip()}\"."
    return (
        "Runtime layout context (authoritative, measured from toolbox/canvas):\n"
        + safe_payload
        + "\n\n"
        + "Use runtime context as hard constraints. Do not change lockedGlobals values. "
        + "Generate pages/components placement that stays fully within canvas."
        + terms_rules
    )


def _parse_positive_dimension(value: Any, fallback: float) -> float:
    if isinstance(value, (int, float)):
        number = float(value)
        return number if number > 0 else fallback
    if isinstance(value, str):
        candidate = value.strip().lower()
        if candidate.endswith("px"):
            candidate = candidate[:-2]
        try:
            number = float(candidate)
            return number if number > 0 else fallback
        except ValueError:
            return fallback
    return fallback


def _parse_number(value: Any, fallback: float) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        candidate = value.strip().lower()
        if candidate.endswith("px"):
            candidate = candidate[:-2]
        try:
            return float(candidate)
        except ValueError:
            return fallback
    return fallback


def _minimum_render_height(
    component_type: str,
    component_props: Dict[str, Any],
    runtime_footprints: Optional[Dict[str, Dict[str, float]]] = None,
) -> float:
    base_by_type = {
        "header": 52.0,
        "divider": 20.0,
        "submit-button": 60.0,
        "text": 110.0,
        "email": 110.0,
        "phone": 110.0,
        "number": 110.0,
        "date": 110.0,
        "address": 120.0,
        "dropdown": 120.0,
        "select": 120.0,
        "checkbox": 120.0,
        "radio": 120.0,
        # Aligned with STORY-6.2-AI-CONTEXT-PACK / runtime footprints (~200): label + control + validation band.
        "textarea": 200.0,
        "terms": 120.0,
    }
    minimum_height = base_by_type.get(component_type, 110.0)
    if runtime_footprints and component_type in runtime_footprints:
        minimum_height = max(minimum_height, runtime_footprints[component_type]["height"])
    if component_type in ("checkbox", "radio", "dropdown", "select"):
        options = component_props.get("options")
        if isinstance(options, list):
            minimum_height += max(0, len(options) - 3) * 20.0
    return minimum_height


def _minimum_render_width(
    component_type: str,
    runtime_footprints: Optional[Dict[str, Dict[str, float]]] = None,
) -> float:
    if runtime_footprints and component_type in runtime_footprints:
        return runtime_footprints[component_type]["width"]
    width_by_type = {
        "header": 460.0,
        "divider": 460.0,
        "submit-button": 180.0,
        "text": 460.0,
        "email": 460.0,
        "phone": 460.0,
        "number": 460.0,
        "date": 460.0,
        "address": 460.0,
        "textarea": 460.0,
        "dropdown": 460.0,
        "select": 460.0,
        "checkbox": 460.0,
        "radio": 460.0,
    }
    return width_by_type.get(component_type, 420.0)


def _collision_component_width_height(
    item: Dict[str, Any],
    runtime_footprints: Dict[str, Dict[str, float]],
) -> tuple[float, float]:
    """
    Geometry for pairwise collision checks.

    Width matches ``form_validate.service._component_size`` (no footprint minimum).
    Inflating every field to ~560px from runtime footprints made side-by-side rows
    look like massive overlaps even when x positions were valid for narrow widths.

    Height still uses ``max(stated, minimum_render_height)`` so under-stated
    vertical sizes cannot hide real overlaps (same as prior visual collision intent).
    """
    style = item.get("style") if isinstance(item.get("style"), dict) else {}
    props = item.get("props") if isinstance(item.get("props"), dict) else {}
    component_type = str(item.get("type", "text"))

    width_raw = style.get("width")
    height_raw = style.get("height")
    if width_raw is None and props.get("width") is not None:
        width_raw = props.get("width")

    fallback_width = 300.0
    fallback_height = DEFAULT_HEIGHT_BY_TYPE.get(component_type, 100.0)
    width = _parse_dimension(width_raw, fallback_width)
    height_base = _parse_dimension(height_raw, fallback_height)
    # UAT round 11 — trust compiler-stamped heights when they look plausible
    # (see ``MIN_PLAUSIBLE_RENDER_HEIGHT_PX`` comment). Falling back to the
    # ``_minimum_render_height`` inflation only when the stated height is
    # missing/degenerate keeps legacy tests (which omit ``style.height``) and
    # vertical-stacked layouts safe, while fixing the horizontal-stacked
    # phantom-collision bug where compiler heights of 52 px were inflated to
    # 110-120 px and crashed into the next row.
    if height_base >= MIN_PLAUSIBLE_RENDER_HEIGHT_PX:
        height = height_base
    else:
        min_height = _minimum_render_height(component_type, props, runtime_footprints)
        if component_type in ("dropdown", "select"):
            # Collision checks model the closed control footprint, not an expanded/open menu list.
            options = props.get("options")
            if isinstance(options, list):
                min_height -= max(0, len(options) - 3) * 20.0
        height = max(height_base, min_height)
    return width, height


# UAT round 5 (run 42) — anything below this is treated as "the LLM emitted a
# nonsense width" (e.g. ``"width": 10`` or stripped ``"width": "0px"``) and
# falls back to ``_minimum_render_width``. Above the floor we trust whatever
# the deterministic compiler placed there — its tier table already accounts
# for the canvas size and would never legitimately produce <60 px inputs.
MIN_PLAUSIBLE_RENDER_WIDTH_PX = 60.0

# UAT round 11 — same trust-the-compiler escape hatch for height. The legacy
# ``_minimum_render_height`` table assumed every component renders the
# vertical-stacked footprint (label on top, input below, validation below) and
# inflated short stated heights to 110-120 px. That made horizontal-stacked
# rows (label/input/validation in a single 52 px row) overlap the next row in
# the validator even though the canvas had a clean 24 px vertical gap between
# them. The deterministic compiler now stamps a layout-mode-aware height on
# every component (``_component_height(layout_mode=...)`` + ``_row_chrome``),
# so as long as the stated height looks plausible (>= floor) we trust it.
# Mobile/vertical-stacked forms still pass through the inflation path because
# the compiler stamps the full vertical footprint there.
MIN_PLAUSIBLE_RENDER_HEIGHT_PX = 32.0


def _flatten_boundary_visual_components(
    definition: Dict[str, Any],
    runtime_context: Optional[Dict[str, Any]] = None,
) -> tuple[str, List[Dict[str, Any]]]:
    """
    Footprint-inflated boxes for boundary checks (narrow JSON width vs rendered width).
    """
    pages = definition.get("pages")
    if not isinstance(pages, list) or len(pages) == 0:
        return ("page-1", [])
    page = pages[0]
    page_id = page.get("id", "page-1")
    components = page.get("components")
    if not isinstance(components, list):
        return (str(page_id), [])

    flattened: List[Dict[str, Any]] = []
    runtime_footprints = _build_runtime_footprint_map(runtime_context)

    def walk(items: List[Any]) -> None:
        for item in items:
            if not isinstance(item, dict):
                continue
            position = item.get("position")
            if isinstance(position, dict):
                x = _parse_number(position.get("x"), 0.0)
                y = _parse_number(position.get("y"), 0.0)
                style = item.get("style") if isinstance(item.get("style"), dict) else {}
                props = item.get("props") if isinstance(item.get("props"), dict) else {}
                component_type = str(item.get("type", "text"))
                # UAT round 5 (run 42) — width: trust the deterministic
                # compiler's emitted ``style.width`` whenever it's a positive
                # number. The legacy ``max(stated, minimum)`` rule was a guard
                # against early LLM-emitted geometry that often reported tiny
                # 100 px inputs; the deterministic compiler now emits widths
                # that are sized for the actual canvas (e.g. 295 px on a
                # 375 px mobile screen), so inflating to the 460 px desktop
                # toolbox footprint creates phantom boundary failures on
                # narrow canvases. We keep ``MIN_PLAUSIBLE_RENDER_WIDTH_PX``
                # as a hard safety net for genuinely degenerate widths
                # (sub-60 px is never a real input on any canvas).
                stated_width = _parse_positive_dimension(
                    style.get("width", props.get("width")), 0.0
                )
                if stated_width >= MIN_PLAUSIBLE_RENDER_WIDTH_PX:
                    width = stated_width
                else:
                    minimum_width = _minimum_render_width(
                        component_type, runtime_footprints
                    )
                    width = max(stated_width, minimum_width)
                stated_height = _parse_positive_dimension(style.get("height"), 0.0)
                # UAT round 11 — same trust-the-compiler escape hatch as width.
                # Compiler-stamped heights >= the plausibility floor are taken
                # at face value; only short/missing values get inflated by the
                # vertical-stacked ``_minimum_render_height`` table, which
                # otherwise creates phantom bottom-edge boundary failures on
                # horizontal-stacked rows.
                if stated_height >= MIN_PLAUSIBLE_RENDER_HEIGHT_PX:
                    height = stated_height
                else:
                    min_height = _minimum_render_height(
                        component_type, props, runtime_footprints
                    )
                    height = max(stated_height, min_height)
                flattened.append(
                    {
                        "id": str(item.get("id", "")),
                        "x": x,
                        "y": y,
                        "width": width,
                        "height": height,
                    }
                )
            children = item.get("children")
            if isinstance(children, list):
                walk(children)

    walk(components)
    return (str(page_id), flattened)


def _flatten_collision_visual_components(
    definition: Dict[str, Any],
    runtime_context: Optional[Dict[str, Any]] = None,
) -> tuple[str, List[Dict[str, Any]]]:
    pages = definition.get("pages")
    if not isinstance(pages, list) or len(pages) == 0:
        return ("page-1", [])
    page = pages[0]
    page_id = page.get("id", "page-1")
    components = page.get("components")
    if not isinstance(components, list):
        return (str(page_id), [])

    flattened: List[Dict[str, Any]] = []
    runtime_footprints = _build_runtime_footprint_map(runtime_context)

    def walk(items: List[Any]) -> None:
        for item in items:
            if not isinstance(item, dict):
                continue
            position = item.get("position")
            if isinstance(position, dict):
                x = _parse_number(position.get("x"), 0.0)
                y = _parse_number(position.get("y"), 0.0)
                width, height = _collision_component_width_height(item, runtime_footprints)
                flattened.append(
                    {
                        "id": str(item.get("id", "")),
                        "type": str(item.get("type", "text")),
                        "x": x,
                        "y": y,
                        "width": width,
                        "height": height,
                    }
                )
            children = item.get("children")
            if isinstance(children, list):
                walk(children)

    walk(components)
    return (str(page_id), flattened)


def _collect_visual_collisions(
    definition: Dict[str, Any], runtime_context: Optional[Dict[str, Any]] = None
) -> List[CollisionViolation]:
    page_id, flattened = _flatten_collision_visual_components(definition, runtime_context)
    if not flattened:
        return []

    collisions: List[CollisionViolation] = []
    for index in range(len(flattened)):
        left = flattened[index]
        for right in flattened[index + 1 :]:
            x_overlap = min(left["x"] + left["width"], right["x"] + right["width"]) - max(
                left["x"], right["x"]
            )
            y_overlap = min(
                left["y"] + left["height"], right["y"] + right["height"]
            ) - max(left["y"], right["y"])
            if x_overlap > 0 and y_overlap > 0:
                collisions.append(
                    CollisionViolation(
                        componentAId=left["id"],
                        componentBId=right["id"],
                        pageId=page_id,
                        layout="pages",
                        overlapArea=float(x_overlap * y_overlap),
                    )
                )
    collisions.sort(key=lambda item: (item.pageId, item.componentAId, item.componentBId))
    return collisions


def _collect_visual_boundary_violations(
    definition: Dict[str, Any], runtime_context: Optional[Dict[str, Any]] = None
) -> List[BoundaryViolation]:
    page_id, flattened = _flatten_boundary_visual_components(definition, runtime_context)
    if not flattened:
        return []

    # The compiled ``definition.canvasSettings`` is authoritative for boundary
    # checks: the deterministic compiler is allowed to grow the canvas
    # vertically when the form needs more space (canvasHeightGrew=true in
    # compileSummary). The runtime context only carries the *initial* canvas
    # the user opened the builder with, so using it would falsely flag every
    # component placed past row N+1 of a tall form. We therefore take the
    # max of (definition, runtime) so the runtime can only act as a floor.
    canvas = definition.get("canvasSettings")
    canvas_width = 1920.0
    canvas_height = 980.0
    if isinstance(canvas, dict):
        canvas_width = _parse_positive_dimension(canvas.get("width"), 1920.0)
        canvas_height = _parse_positive_dimension(canvas.get("height"), 980.0)
    runtime_canvas = (runtime_context or {}).get("canvas")
    if isinstance(runtime_canvas, dict):
        runtime_width = _parse_positive_dimension(
            runtime_canvas.get("width"), canvas_width
        )
        runtime_height = _parse_positive_dimension(
            runtime_canvas.get("height"), canvas_height
        )
        canvas_width = max(canvas_width, runtime_width)
        canvas_height = max(canvas_height, runtime_height)

    violations: List[BoundaryViolation] = []
    for item in flattened:
        left = item["x"] < 0
        right = item["x"] + item["width"] > canvas_width
        top = item["y"] < 0
        bottom = item["y"] + item["height"] > canvas_height
        if not (left or right or top or bottom):
            continue
        violations.append(
            BoundaryViolation(
                componentId=item["id"],
                pageId=page_id,
                layout="pages",
                position={"x": item["x"], "y": item["y"]},
                size={"width": item["width"], "height": item["height"]},
                canvas={"width": canvas_width, "height": canvas_height},
                violations=BoundaryDirectionFlags(
                    left=left, right=right, top=top, bottom=bottom
                ),
            )
        )
    violations.sort(key=lambda item: (item.pageId, item.componentId))
    return violations


def _merge_visual_boundaries(
    base_validation: FormValidationResponse, visual_boundaries: List[BoundaryViolation]
) -> FormValidationResponse:
    if not visual_boundaries:
        return base_validation

    existing_keys = {
        (item.layout, item.pageId, item.componentId)
        for item in base_validation.boundaryViolations
    }
    merged_boundaries = list(base_validation.boundaryViolations)
    for item in visual_boundaries:
        key = (item.layout, item.pageId, item.componentId)
        if key in existing_keys:
            continue
        merged_boundaries.append(item)
        existing_keys.add(key)

    if len(merged_boundaries) == len(base_validation.boundaryViolations):
        return base_validation

    error_count = (
        len(base_validation.schemaErrors)
        + len(merged_boundaries)
        + len(base_validation.collisions)
    )
    return FormValidationResponse(
        valid=False,
        schemaErrors=base_validation.schemaErrors,
        boundaryViolations=merged_boundaries,
        collisions=base_validation.collisions,
        summary=ValidationSummary(errorCount=error_count, warningCount=0),
        meta=base_validation.meta,
    )


def _merge_visual_collisions(
    base_validation: FormValidationResponse, visual_collisions: List[CollisionViolation]
) -> FormValidationResponse:
    if not visual_collisions:
        return base_validation

    existing_keys = {
        (item.layout, item.pageId, item.componentAId, item.componentBId)
        for item in base_validation.collisions
    }
    merged_collisions = list(base_validation.collisions)
    for item in visual_collisions:
        key = (item.layout, item.pageId, item.componentAId, item.componentBId)
        reverse_key = (item.layout, item.pageId, item.componentBId, item.componentAId)
        if key in existing_keys or reverse_key in existing_keys:
            continue
        merged_collisions.append(item)
        existing_keys.add(key)

    if len(merged_collisions) == len(base_validation.collisions):
        return base_validation

    error_count = (
        len(base_validation.schemaErrors)
        + len(base_validation.boundaryViolations)
        + len(merged_collisions)
    )
    return FormValidationResponse(
        valid=False,
        schemaErrors=base_validation.schemaErrors,
        boundaryViolations=base_validation.boundaryViolations,
        collisions=merged_collisions,
        summary=ValidationSummary(errorCount=error_count, warningCount=0),
        meta=base_validation.meta,
    )


# Story 6.3.1 UAT round 5 (run 42 follow-up) — locale-aware terminology block.
#
# EventLead is launching in Australia first, with most early users authoring
# forms for the Australian / New Zealand market. The default LLM voice is
# American English (zip code, organization, cell phone, color), which produces
# forms that read awkwardly to AU/NZ end-users and require manual relabelling.
#
# This map is a small, deliberately narrow set of high-traffic terminology
# swaps that materially affect form labels, placeholders, and helpText. We
# intentionally do NOT try to do full en-AU/en-NZ spelling normalisation —
# that's the LLM's job once it knows the convention; trying to enforce it via
# explicit lists would be brittle and miss edge cases.
#
# Wiring guidance for future extension:
#   - Today this is a hard-coded "AU/NZ" default applied to every request.
#   - When the user/event country is plumbed into ``run_form_ai_generation``,
#     replace the hard-coded ``"AU"`` in ``_build_locale_prompt_block`` with
#     the resolved ISO code and add new entries here keyed by region.
#   - The block is opt-out via ``locale_code=None`` so we can always disable
#     for tests / specific tenants.
_LOCALE_PROMPT_BLOCKS: Dict[str, str] = {
    "AU": "Form audience: Australia/New Zealand. Use AU/NZ spelling, address, phone, date conventions.",
}


# Story 6.3.1 UAT round 5 (Prompts 9/10 follow-up) — consent / legal-
# acknowledgement guidance.
#
# Background: when prompts asked for "Marketing consent" / "I agree to receive
# updates" / "GDPR opt-in" / "I have read the privacy policy", the model was
# emitting a plain ``checkbox`` with the consent sentence as the label. That
# renders, but it loses the value the ``terms`` component adds for
# legal/consent intent specifically:
#
#   * ``terms`` exposes ``props.termsLinkText`` + a clickable link the
#     end-user can open to read the full document before agreeing — required
#     for GDPR/CCPA/AU Privacy Act enforceability ("evidence of informed
#     consent"). Plain checkbox has nowhere to put that link.
#   * When company-managed terms are uploaded (see ``termsDefaults`` in
#     runtime context), ``terms`` auto-wires the company doc, so the form
#     stays consistent across the customer's whole event suite without the
#     LLM having to fabricate copy.
#   * ``terms`` is rendered with consent-specific affordances (label
#     emphasis, link styling, required-by-default semantics).
#
# This block is locale-independent — the AU/NZ locale rules already cover
# spelling/terminology; consent semantics are universal.
#
# Wiring guidance:
#   * Block is always-on in ``_build_initial_messages`` (no opt-out flag);
#     the rules are conservative and won't fire unless the prompt actually
#     mentions consent/agreement language.
#   * Pairs with the existing ``terms_rules`` block in
#     ``_build_runtime_context_block``: that block adds *runtime* context
#     ("company terms exist, here's the link text"); this block adds
#     *semantic* guidance ("which component type to pick").
_CONSENT_GUIDANCE_BLOCK = (
    "## CONSENT & LEGAL ACKNOWLEDGEMENTS\n"
    "| User intent | Component | Required guidance |\n"
    "|---|---|---|\n"
    "| Marketing consent, terms acceptance, privacy acknowledgement, data/cookie consent, waiver, release, code-of-conduct or indemnity acknowledgement | ``terms`` | Set ``validationIntent.required = true`` unless explicitly optional. Use company-managed terms when runtime context provides them. |\n"
    "| Consent text but no company-managed terms | ``terms`` | Keep the acknowledgement sentence in ``label`` or ``props.termsContent``. Do not invent legal URLs or policy content. |\n"
    "| Interests, preferences, dietary choices, availability, feature toggles or other non-legal multi-select | ``checkbox`` | Treat as ordinary choices, not legal acknowledgement. |\n"
)


# Story 6.3.1 (UAT round 6) — Phase 2 LLM nudge for horizontal-stacked
# layout. Only injected when ``compiler.resolve_layout_mode`` reports
# ``"horizontal-stacked"`` for the current request; otherwise the prompt is
# unchanged so vertical-mode generations don't see any new instructions.
#
# Why a separate block?
#   * In horizontal-stacked mode every input renders as
#     ``[ Label ][ Input ][ Validation ]`` on a single row, so the rowGroup
#     packing the LLM normally uses to put two fields side-by-side
#     (first-name + last-name, city + state) actively *hurts* the layout —
#     the row solver would have to fit two label/input/validation triplets
#     in the same horizontal band.
#   * The compiler's Phase 3 horizontal-stacked branch will ignore rowGroup
#     entirely (one input per row, period), but that branch isn't built yet.
#     For Phase 2 we still route to the packed-rows code path; this addendum
#     just steers the LLM toward output that *also* works once Phase 3 lands
#     (and looks better today on a horizontal-mode form).
_HORIZONTAL_STACKED_LAYOUT_NUDGE = (
    "## LAYOUT MODE — HORIZONTAL STACKED (active for this request)\n"
    "The form's Global Styles set ``defaultObjectLayout = \"horizontal\"``: "
    "every input will render as ``[ Label ][ Input ][ Validation ]`` on its "
    "own row. The compiler enforces a single-column ordering, so:\n"
    "  - Do NOT use ``rowGroup`` to pack two fields side-by-side. Each "
    "    component gets its own row regardless of what you set, and using "
    "    rowGroup just makes the trace noisier. Leave ``rowGroup`` empty "
    "    (or omit it) for every standard input.\n"
    "  - Order components by reading order — natural top-to-bottom flow "
    "    (contact details → address → message → consent → submit), not by "
    "    visual columns.\n"
    "  - ``widthIntent`` still influences the *input column* width (the "
    "    middle of the three columns), so keep using ``\"compact\"`` for "
    "    short fields (zip / age / state code), ``\"full\"`` for long-form "
    "    fields (textarea / description), and the default for everything "
    "    else. The compiler picks the actual pixel widths and keeps the "
    "    label and validation columns aligned across the form.\n"
    "  - ``terms`` and ``submit-button`` are special: the compiler renders "
    "    them edge-to-edge (terms) and left-aligned with their own width "
    "    (submit), regardless of the label/input grid. You don't need to "
    "    do anything special — just include them in the natural reading "
    "    order.\n"
)


def _build_locale_prompt_block(locale_code: Optional[str] = "AU") -> str:
    """Return the locale-specific terminology block for ``locale_code``.

    Currently only ``"AU"`` is wired (covers AU + NZ — the early-access
    market). Returns an empty string when ``locale_code`` is None or unknown
    so test fixtures can opt out cleanly.

    Wiring note (future): when company / event country is plumbed through
    ``run_form_ai_generation``, pass the ISO-3166 code here. Map e.g.
    ``"AU"`` and ``"NZ"`` → the ``"AU"`` block (shared AU/NZ market), and
    add fresh blocks for ``"US"`` / ``"GB"`` / etc. as we expand.
    """
    if not locale_code:
        return ""
    return _LOCALE_PROMPT_BLOCKS.get(locale_code.upper(), "")


def _trim_context_pack_for_prompt(context_pack: str) -> str:
    """Remove non-generation operational notes before sending context to the LLM."""
    marker = "\n## Operational Notes"
    index = context_pack.find(marker)
    if index == -1:
        return context_pack
    return context_pack[:index].rstrip()


def _build_initial_messages(
    prompt: str,
    context_pack: str,
    runtime_context: Optional[Dict[str, Any]] = None,
    *,
    system_prompt_addendum: str | None = None,
    capability_snapshot_json: Optional[Dict[str, Any]] = None,
    locale_code: Optional[str] = "AU",
) -> List[Dict[str, str]]:
    runtime_context_block = _build_runtime_context_block(runtime_context)
    capability_block = _build_capability_prompt_block(capability_snapshot_json)
    locale_block = _build_locale_prompt_block(locale_code)
    prompt_context_pack = _trim_context_pack_for_prompt(context_pack)

    # Story 6.3.1 (UAT round 6) — Phase 2 LLM nudge for horizontal-stacked
    # layout. ``resolve_layout_mode`` returns the legacy
    # ``"vertical-packed"`` for any non-horizontal request, in which case
    # ``layout_mode_block`` is empty and the prompt is unchanged.
    layout_mode = resolve_layout_mode(runtime_context)
    layout_mode_block = (
        _HORIZONTAL_STACKED_LAYOUT_NUDGE
        if layout_mode == LAYOUT_MODE_HORIZONTAL_STACKED
        else ""
    )

    system_body = (
        "You generate an EventLead semantic form plan for Story 6.3.1.\n"
        "Output a single JSON object only. No markdown or prose.\n"
        "Return FormSemanticPlan only; do not output any coordinates, pixel widths, x/y positions, style blocks, or final DefinitionJSON.\n"
        "\n"
        + (locale_block + "\n" if locale_block else "")
        + _CONSENT_GUIDANCE_BLOCK
        + (layout_mode_block + "\n" if layout_mode_block else "")
        + "\n"
        + "REQUIRED ROOT KEYS (exact, case-sensitive):\n"
        "  - semanticPlanVersion: must be the string \"1.0\" (do NOT use the story number).\n"
        "  - formId: short slug or id (string).\n"
        "  - title: form title (string).\n"
        "  - components: array of component intents (see below).\n"
        "Do NOT add any other root keys.\n"
        "\n"
        "EACH COMPONENT (object):\n"
        "  - componentType (required), label, placeholder, helpText, section, rowGroup,\n"
        "  - widthIntent: one of \"compact\" | \"half\" | \"full\".\n"
        "    This is a HINT, not a final width. The deterministic compiler picks\n"
        "    the actual pixel width from a per-type tier table and may shrink the\n"
        "    component further (or wrap it onto its own row) so the layout fits\n"
        "    the canvas. Treat widthIntent as a maximum cap: use \"compact\" when\n"
        "    the field's content is short (e.g. zip, age, state code), \"full\"\n"
        "    only when you genuinely want the field to span the row.\n"
        "    Use rowGroup to indicate which fields you'd like packed side-by-side;\n"
        "    the compiler decides whether they actually fit.\n"
        "  - options: array of {label,value} for dropdown/radio,\n"
        "  - validationIntent: an OBJECT (not an array) with any of these boolean/number keys:\n"
        "      required, email, phone, url, minLength, maxLength, min, max, pattern.\n"
        "    Example: \"validationIntent\": { \"required\": true, \"email\": true }.\n"
        "    NEVER emit validationIntent as a list of strings (e.g. [\"required\",\"email\"]).\n"
        "\n"
        "Use only Story 6.2/6.3.1 supported component catalog and single-page constraints.\n\n"
        + (capability_block + "\n\n" if capability_block else "")
        + f"{prompt_context_pack}"
        + ("\n\n" + runtime_context_block if runtime_context_block else "")
    )
    if system_prompt_addendum and system_prompt_addendum.strip():
        system_body += (
            "\n\n## Instruction addendum (follow strictly; user-facing prompt unchanged)\n"
            + system_prompt_addendum.strip()
        )
    return [
        {
            "role": "system",
            "content": system_body,
        },
        {
            "role": "user",
            "content": (
                "Generate a semantic plan for this request.\n"
                f"Prompt: {prompt}\n"
                "Return only valid JSON."
            ),
        },
    ]


def _collision_pair_hint(
    a: Dict[str, Any], b: Dict[str, Any], x_ov: float, y_ov: float
) -> str:
    """Deterministic, LLM-readable fix hints from pairwise geometry."""
    xa, ya, wa, ha = float(a["x"]), float(a["y"]), float(a["width"]), float(a["height"])
    xb, yb, wb, hb = float(b["x"]), float(b["y"]), float(b["width"]), float(b["height"])
    row_tol = 56.0
    same_row = abs(ya - yb) <= row_tol
    if same_row and x_ov >= y_ov * 0.55:
        left, right = (a, b) if xa <= xb else (b, a)
        xl = float(left["x"])
        wl = float(left["width"])
        xr = float(right["x"])
        min_x = xl + wl + 56.0
        if xr < min_x - 1e-6:
            return (
                f"Same-row overlap: narrow `style.width` or set `{right['id']}.position.x` "
                f"≥ {math.ceil(min_x)} (or use a single column stack)."
            )
        return (
            "Same-row overlap: reduce both `style.width` values or increase horizontal gap "
            "between columns (~56–96px)."
        )
    upper, lower = (a, b) if ya <= yb else (b, a)
    u_y = float(upper["y"])
    u_h = float(upper["height"])
    l_y = float(lower["y"])
    min_y = u_y + u_h + 8.0
    if l_y + 1e-6 < min_y:
        ut = str(upper.get("type", "?"))
        lt = str(lower.get("type", "?"))
        extra = ""
        if "textarea" in (ut, lt) and "submit-button" in (ut, lt):
            extra = (
                " For textarea+submit, also ensure `textarea.style.height` reserves space for "
                "label/validation chrome above the button."
            )
        return (
            f"Vertical overlap: set `{lower['id']}.position.y` ≥ {math.ceil(min_y)} "
            f"(fully below `{upper['id']}`).{extra}"
        )
    return ""


def _build_collision_truth_feedback(
    definition: Dict[str, Any],
    runtime_context: Optional[Dict[str, Any]],
    collisions: List[CollisionViolation],
) -> str:
    """
    Markdown-style tables for the LLM: full layout snapshot (validator collision boxes)
    plus one row per reported pair with recomputed overlap vs validator area and fix hints.

    Geometry matches ``_flatten_collision_visual_components`` (DefinitionJSON), not SmartBorder.
    """
    if not collisions:
        return ""

    page_id, flat = _flatten_collision_visual_components(definition, runtime_context)
    if not flat:
        return ""

    sorted_flat = sorted(flat, key=lambda it: (float(it["y"]), float(it["x"]), str(it["id"])))
    by_id = {item["id"]: item for item in flat}

    lines: List[str] = [
        "Collision layout (DefinitionJSON boxes — same math as the validator; not SmartBorder pixels).",
        "",
        f"Layout snapshot (page {page_id}):",
        "| id | type | x | y | width | height |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for item in sorted_flat:
        lines.append(
            f"| {item['id']} | {item.get('type', '?')} | {float(item['x']):.0f} | "
            f"{float(item['y']):.0f} | {float(item['width']):.0f} | {float(item['height']):.0f} |"
        )

    lines.extend(
        [
            "",
            "Reported overlaps (recompute sanity-check vs validator `overlapArea`):",
            "| A | B | overlap W×H | area (validator) | area (recomputed) | Notes |",
            "| --- | --- | --- | ---: | ---: | --- |",
        ]
    )

    for item in collisions:
        a = by_id.get(item.componentAId)
        b = by_id.get(item.componentBId)
        if not a or not b:
            lines.append(
                f"| `{item.componentAId}` | `{item.componentBId}` | — | "
                f"{item.overlapArea:.0f} | — | Missing id in layout snapshot; verify JSON. |"
            )
            continue
        xa, ya, wa, ha = float(a["x"]), float(a["y"]), float(a["width"]), float(a["height"])
        xb, yb, wb, hb = float(b["x"]), float(b["y"]), float(b["width"]), float(b["height"])
        x_ov = min(xa + wa, xb + wb) - max(xa, xb)
        y_ov = min(ya + ha, yb + hb) - max(ya, yb)
        area_r = max(0.0, x_ov) * max(0.0, y_ov)
        wh = f"{x_ov:.0f}×{y_ov:.0f}px" if x_ov > 0 and y_ov > 0 else "0 (no overlap)"
        if x_ov <= 0 or y_ov <= 0:
            notes = (
                "**INCONSISTENT**: validator reported overlap but these boxes do not overlap "
                "when recomputed; do not invent layout changes for this pair."
            )
        else:
            hint = _collision_pair_hint(a, b, x_ov, y_ov)
            mismatch = abs(area_r - float(item.overlapArea)) > 1.0
            extra = (
                f" (area mismatch vs validator {item.overlapArea:.0f})"
                if mismatch
                else ""
            )
            notes = (hint + extra) if hint else f"Overlap area {area_r:.0f}px².{extra}"
        safe_notes = notes.replace("|", "/")
        lines.append(
            f"| `{item.componentAId}` | `{item.componentBId}` | {wh} | "
            f"{float(item.overlapArea):.0f} | {area_r:.0f} | {safe_notes} |"
        )

    return "\n".join(lines)


def _enrich_collision_feedback_lines(
    definition: Optional[Dict[str, Any]],
    runtime_context: Optional[Dict[str, Any]],
    collisions: List[CollisionViolation],
) -> List[str]:
    """Legacy bullet format; prefer :func:`_build_collision_truth_feedback` for LLM prompts."""
    if not definition or not collisions:
        return []
    _, flat = _flatten_collision_visual_components(definition, runtime_context)
    by_id = {item["id"]: item for item in flat}
    lines: List[str] = []
    for item in collisions:
        a = by_id.get(item.componentAId)
        b = by_id.get(item.componentBId)
        if not a or not b:
            lines.append(
                f"- {item.componentAId} overlaps {item.componentBId} "
                f"on {item.pageId} (area={item.overlapArea})"
            )
            continue
        xa, ya, wa, ha = float(a["x"]), float(a["y"]), float(a["width"]), float(a["height"])
        xb, yb, wb, hb = float(b["x"]), float(b["y"]), float(b["width"]), float(b["height"])
        x_ov = min(xa + wa, xb + wb) - max(xa, xb)
        y_ov = min(ya + ha, yb + hb) - max(ya, yb)
        if x_ov <= 0 or y_ov <= 0:
            lines.append(
                f"- {item.componentAId} overlaps {item.componentBId} "
                f"on {item.pageId} (area={item.overlapArea})"
            )
            continue
        ta = str(a.get("type", "?"))
        tb = str(b.get("type", "?"))
        head = (
            f"- `{item.componentAId}` ({ta}) box x={xa:.0f} y={ya:.0f} w={wa:.0f} h={ha:.0f} "
            f"vs `{item.componentBId}` ({tb}) x={xb:.0f} y={yb:.0f} w={wb:.0f} h={hb:.0f} — "
            f"overlap ~{x_ov:.0f}px × {y_ov:.0f}px (area={item.overlapArea:.0f})."
        )
        hint = _collision_pair_hint(a, b, x_ov, y_ov)
        lines.append(head + (" " + hint if hint else ""))
    return lines


def _build_correction_message(
    validation: FormValidationResponse,
    candidate_definition: Optional[Dict[str, Any]] = None,
    runtime_context: Optional[Dict[str, Any]] = None,
) -> str:
    schema_lines = [
        f"- {item.path}: {item.message} ({item.code})" for item in validation.schemaErrors
    ]
    boundary_lines = [
        (
            f"- {item.componentId} on {item.pageId}: "
            f"left={item.violations.left}, right={item.violations.right}, "
            f"top={item.violations.top}, bottom={item.violations.bottom}"
        )
        for item in validation.boundaryViolations
    ]
    collision_block = ""
    if validation.collisions and candidate_definition is not None:
        collision_block = _build_collision_truth_feedback(
            candidate_definition, runtime_context, list(validation.collisions)
        )
    elif validation.collisions:
        collision_block = "\n".join(
            (
                f"- {item.componentAId} overlaps {item.componentBId} "
                f"on {item.pageId} (area={item.overlapArea})"
            )
            for item in validation.collisions
        )

    segments: List[str] = []
    if schema_lines:
        segments.append("Schema errors:\n" + "\n".join(schema_lines))
    if boundary_lines:
        segments.append("Boundary violations:\n" + "\n".join(boundary_lines))
    if collision_block:
        footprint_note = (
            "\n\nNote: `runtimeContext.componentFootprints` are measured toolbox/canvas hints; "
            "collision uses your JSON `position`/`style` plus minimum heights per type. "
            "If a field renders taller than `style.height`, increase height or move components below."
            if runtime_context and isinstance(
                runtime_context.get("componentFootprints"), list
            )
            else ""
        )
        segments.append("Collisions:\n" + collision_block + footprint_note)

    return (
        "Your previous JSON failed validation. Correct it deterministically.\n"
        "Keep user intent while fixing all errors.\n"
        "Return only one valid JSON object.\n\n"
        + "\n\n".join(segments)
    )


def _resolve_openai_transport(explicit: str) -> Literal["sync", "stream"]:
    """Resolve request `auto|sync|stream` plus FORM_AI_OPENAI_TRANSPORT (for auto)."""
    mode = (explicit or "auto").strip().lower()
    if mode == "sync":
        return "sync"
    if mode == "stream":
        return "stream"
    env = os.getenv("FORM_AI_OPENAI_TRANSPORT", "").strip().lower()
    if env == "stream":
        return "stream"
    return "sync"


def _consume_openai_responses_sse_to_text(line_iter: Iterable[Any]) -> str:
    parts: List[str] = []
    for raw in line_iter:
        if raw is None:
            continue
        line = raw.decode("utf-8") if isinstance(raw, bytes) else raw
        line = line.strip()
        if not line or line.startswith(":"):
            continue
        if not line.startswith("data: "):
            continue
        data = line[6:].strip()
        if data == "[DONE]":
            break
        try:
            obj = json.loads(data)
        except json.JSONDecodeError:
            continue
        if not isinstance(obj, dict):
            continue
        evt_type = obj.get("type")
        if evt_type == "error":
            err = obj.get("error")
            msg = err if isinstance(err, str) else json.dumps(obj, ensure_ascii=True)[:500]
            raise RuntimeError(f"openai-responses-stream-error:{msg}")
        err_obj = obj.get("error")
        if isinstance(err_obj, dict) and err_obj.get("message"):
            raise RuntimeError(
                f"openai-responses-stream-error:{err_obj.get('message')}"
            )
        if evt_type == "response.output_text.delta":
            delta = obj.get("delta")
            if isinstance(delta, str):
                parts.append(delta)
    text = "".join(parts)
    if not text.strip():
        raise RuntimeError("empty-provider-response-stream")
    return text


def _consume_chat_completions_sse_to_text(line_iter: Iterable[Any]) -> str:
    parts: List[str] = []
    for raw in line_iter:
        if raw is None:
            continue
        line = raw.decode("utf-8") if isinstance(raw, bytes) else raw
        line = line.strip()
        if not line or line.startswith(":"):
            continue
        if not line.startswith("data: "):
            continue
        data = line[6:].strip()
        if data == "[DONE]":
            break
        try:
            chunk = json.loads(data)
        except json.JSONDecodeError:
            continue
        if not isinstance(chunk, dict):
            continue
        err = chunk.get("error")
        if isinstance(err, dict) and err.get("message"):
            raise RuntimeError(f"openai-chat-stream-error:{err.get('message')}")
        for choice in chunk.get("choices") or []:
            if not isinstance(choice, dict):
                continue
            delta = choice.get("delta") or {}
            if not isinstance(delta, dict):
                continue
            c = delta.get("content")
            if isinstance(c, str) and c:
                parts.append(c)
    text = "".join(parts)
    if not text.strip():
        raise RuntimeError("empty-provider-response-stream")
    return text


def _request_chatgpt_completion(
    messages: List[Dict[str, str]],
    model_override: str | None = None,
    *,
    openai_transport: Literal["sync", "stream"] = "sync",
) -> str:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("missing-openai-api-key")

    if model_override and model_override.strip():
        model = model_override.strip()
    else:
        model = os.getenv("OPENAI_MODEL", "gpt-5-mini").strip() or "gpt-5-mini"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    timeout_seconds = 180.0
    timeout_raw = os.getenv("OPENAI_TIMEOUT_SECONDS", "").strip()
    if timeout_raw:
        try:
            parsed_timeout = float(timeout_raw)
            if parsed_timeout > 0:
                timeout_seconds = parsed_timeout
        except ValueError:
            pass
    # Explicit read timeout (long Responses calls); connect capped so hung TCP fails fast.
    httpx_timeout = httpx.Timeout(
        connect=min(30.0, timeout_seconds),
        read=timeout_seconds,
        write=timeout_seconds,
        pool=timeout_seconds,
    )

    def _log_provider_http_error(exc: httpx.HTTPError, endpoint: str) -> None:
        payload: Dict[str, Any] = {
            "model": model,
            "endpoint": endpoint,
            "error_class": exc.__class__.__name__,
        }
        request = getattr(exc, "request", None)
        if request is not None:
            payload["method"] = request.method
            payload["url"] = str(request.url)
        response = getattr(exc, "response", None)
        if response is not None:
            payload["status_code"] = response.status_code
            try:
                body = response.json()
                if isinstance(body, dict) and isinstance(body.get("error"), dict):
                    error = body["error"]
                    payload["provider_error"] = {
                        "type": error.get("type"),
                        "code": error.get("code"),
                        "param": error.get("param"),
                        "message": error.get("message"),
                    }
                else:
                    payload["response_body_snippet"] = response.text[:500]
            except ValueError:
                payload["response_body_snippet"] = response.text[:500]
        LOGGER.warning("form-ai provider request failed: %s", payload)

    def _responses_content_type(role: str) -> str:
        # Responses API requires assistant history content as output_text.
        return "output_text" if role == "assistant" else "input_text"

    def build_responses_payload(*, stream: bool) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": model,
            "input": [
                {
                    "role": item["role"],
                    "content": [
                        {
                            "type": _responses_content_type(item["role"]),
                            "text": item["content"],
                        }
                    ],
                }
                for item in messages
            ],
            "text": {"format": {"type": "json_object"}},
        }
        if stream:
            payload["stream"] = True
        return payload

    def call_responses_api(client: httpx.Client) -> str:
        responses_payload = build_responses_payload(stream=False)
        started_at = time.monotonic()
        endpoint_url = "https://api.openai.com/v1/responses"
        try:
            responses = client.post(
                endpoint_url,
                headers=headers,
                json=responses_payload,
            )
            responses.raise_for_status()
            timed_log_outbound_http_request(
                provider="openai",
                method="POST",
                url=endpoint_url,
                started_at_monotonic=started_at,
                status_code=responses.status_code,
                request_payload=responses_payload,
                response_payload=responses.json(),
            )
        except httpx.HTTPError as exc:
            response = getattr(exc, "response", None)
            body_snippet: Optional[str] = None
            if response is not None:
                try:
                    body_snippet = response.text[:1000]
                except Exception:
                    body_snippet = None
            timed_log_outbound_http_request(
                provider="openai",
                method="POST",
                url=endpoint_url,
                started_at_monotonic=started_at,
                status_code=response.status_code if response is not None else 599,
                request_payload=responses_payload,
                response_payload={"error": exc.__class__.__name__, "body": body_snippet},
            )
            _log_provider_http_error(exc, "responses")
            raise
        responses_body = responses.json()

        output_text = responses_body.get("output_text")
        if isinstance(output_text, str) and output_text.strip():
            return output_text

        output = responses_body.get("output") or []
        for item in output:
            if item.get("type") != "message":
                continue
            for content_item in item.get("content") or []:
                if content_item.get("type") == "output_text":
                    text = content_item.get("text", "")
                    if isinstance(text, str) and text.strip():
                        return text

        raise RuntimeError("empty-provider-response")

    def call_responses_api_stream(client: httpx.Client) -> str:
        responses_payload = build_responses_payload(stream=True)
        started_at = time.monotonic()
        endpoint_url = "https://api.openai.com/v1/responses"
        try:
            with client.stream(
                "POST",
                endpoint_url,
                headers=headers,
                json=responses_payload,
            ) as responses:
                responses.raise_for_status()
                text = _consume_openai_responses_sse_to_text(responses.iter_lines())
            timed_log_outbound_http_request(
                provider="openai",
                method="POST",
                url=endpoint_url,
                started_at_monotonic=started_at,
                status_code=responses.status_code,
                request_payload=responses_payload,
                response_payload={
                    "stream": True,
                    "mode": "responses_sse",
                    "chars": len(text),
                },
            )
            return text
        except httpx.HTTPError as exc:
            response = getattr(exc, "response", None)
            body_snippet: Optional[str] = None
            if response is not None:
                try:
                    body_snippet = response.text[:1000]
                except Exception:
                    body_snippet = None
            timed_log_outbound_http_request(
                provider="openai",
                method="POST",
                url=endpoint_url,
                started_at_monotonic=started_at,
                status_code=response.status_code if response is not None else 599,
                request_payload=responses_payload,
                response_payload={"error": exc.__class__.__name__, "body": body_snippet},
            )
            _log_provider_http_error(exc, "responses-stream")
            raise

    def build_chat_payload(*, stream: bool) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": model,
            "temperature": 0.2,
            "response_format": {"type": "json_object"},
            "messages": messages,
        }
        if stream:
            payload["stream"] = True
        return payload

    def call_chat_completions_stream(client: httpx.Client) -> str:
        payload = build_chat_payload(stream=True)
        chat_endpoint_url = "https://api.openai.com/v1/chat/completions"
        started_at = time.monotonic()
        try:
            with client.stream(
                "POST",
                chat_endpoint_url,
                headers=headers,
                json=payload,
            ) as response:
                response.raise_for_status()
                text = _consume_chat_completions_sse_to_text(response.iter_lines())
            timed_log_outbound_http_request(
                provider="openai",
                method="POST",
                url=chat_endpoint_url,
                started_at_monotonic=started_at,
                status_code=response.status_code,
                request_payload=payload,
                response_payload={
                    "stream": True,
                    "mode": "chat_completions_sse",
                    "chars": len(text),
                },
            )
            return text
        except httpx.HTTPError as exc:
            error_response = getattr(exc, "response", None)
            body_snippet: Optional[str] = None
            if error_response is not None:
                try:
                    body_snippet = error_response.text[:1000]
                except Exception:
                    body_snippet = None
            timed_log_outbound_http_request(
                provider="openai",
                method="POST",
                url=chat_endpoint_url,
                started_at_monotonic=started_at,
                status_code=error_response.status_code if error_response is not None else 599,
                request_payload=payload,
                response_payload={"error": exc.__class__.__name__, "body": body_snippet},
            )
            _log_provider_http_error(exc, "chat.completions-stream")
            raise

    # GPT-5 family is more reliable on Responses API than Chat Completions.
    model_lower = model.lower()
    prefer_responses_api = model_lower.startswith("gpt-5")

    with httpx.Client(timeout=httpx_timeout) as client:
        if prefer_responses_api:
            if openai_transport == "stream":
                return call_responses_api_stream(client)
            return call_responses_api(client)

        if openai_transport == "stream":
            try:
                return call_chat_completions_stream(client)
            except httpx.HTTPError:
                # Chat streaming failed; fall back to synchronous Responses API.
                return call_responses_api(client)

        payload = build_chat_payload(stream=False)
        chat_endpoint_url = "https://api.openai.com/v1/chat/completions"
        started_at = time.monotonic()
        try:
            response = client.post(
                chat_endpoint_url,
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            body = response.json()
            timed_log_outbound_http_request(
                provider="openai",
                method="POST",
                url=chat_endpoint_url,
                started_at_monotonic=started_at,
                status_code=response.status_code,
                request_payload=payload,
                response_payload=body,
            )

            choices = body.get("choices") or []
            message = choices[0].get("message", {}) if choices else {}
            content = message.get("content", "")
            if isinstance(content, str) and content.strip():
                return content
        except httpx.HTTPError as exc:
            error_response = getattr(exc, "response", None)
            body_snippet: Optional[str] = None
            if error_response is not None:
                try:
                    body_snippet = error_response.text[:1000]
                except Exception:
                    body_snippet = None
            timed_log_outbound_http_request(
                provider="openai",
                method="POST",
                url=chat_endpoint_url,
                started_at_monotonic=started_at,
                status_code=error_response.status_code if error_response is not None else 599,
                request_payload=payload,
                response_payload={"error": exc.__class__.__name__, "body": body_snippet},
            )
            _log_provider_http_error(exc, "chat.completions")
            # Fall through to Responses API fallback (sync only).
            pass

        return call_responses_api(client)


def _safe_json_dumps(value: Any) -> str:
    try:
        return json.dumps(value, ensure_ascii=True, default=str)
    except Exception:
        return json.dumps({"serializationError": True}, ensure_ascii=True)


def _sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def _coerce_form_id(runtime_context: Optional[Dict[str, Any]]) -> Optional[int]:
    if not runtime_context or not isinstance(runtime_context, dict):
        return None
    raw = runtime_context.get("formId")
    if isinstance(raw, int):
        return raw
    if isinstance(raw, str):
        raw = raw.strip()
        if raw.isdigit():
            return int(raw)
    return None


def _build_request_id_fallback() -> str:
    return f"form-ai-{uuid.uuid4()}"


def _resolve_runtime_governance_versions(
    db_session: Optional[Session],
) -> Dict[str, Any]:
    default_payload: Dict[str, Any] = {
        "promptTemplateVersionId": None,
        "promptTemplateVersionRef": None,
        "promptAssemblyProfileId": None,
        "promptAssemblyProfileRef": None,
        "capabilityPolicyVersionId": None,
        "capabilityPolicyVersionRef": None,
        "componentCapabilitySnapshotId": None,
        "componentCapabilitySnapshotRef": None,
        "widthClassPolicyVersionId": None,
        "widthClassPolicyVersionRef": None,
        "validationContractVersion": None,
        "governanceResolutionSource": "no-db-session",
        "capabilityPolicyJson": None,
        "widthClassPolicyJson": None,
        "componentCapabilitySnapshotJson": None,
        "validationContracts": [],
    }
    if db_session is None:
        return default_payload

    payload = dict(default_payload)
    payload["governanceResolutionSource"] = "db-active"

    try:
        prompt_template_version = db_session.execute(
            text(
                """
                SELECT TOP 1
                    PromptTemplateVersionID,
                    PromptTemplateID,
                    VersionNumber
                FROM config.PromptTemplateVersion
                WHERE IsActive = 1 AND IsDeleted = 0
                ORDER BY ActivatedDate DESC, CreatedDate DESC, PromptTemplateVersionID DESC
                """
            )
        ).mappings().first()
        if prompt_template_version is not None:
            payload["promptTemplateVersionId"] = prompt_template_version["PromptTemplateVersionID"]
            payload["promptTemplateVersionRef"] = (
                f"{prompt_template_version['PromptTemplateID']}:v{prompt_template_version['VersionNumber']}"
            )

        prompt_assembly_profile = db_session.execute(
            text(
                """
                SELECT TOP 1
                    PromptAssemblyProfileID,
                    ProfileKey,
                    StepName
                FROM config.PromptAssemblyProfile
                WHERE IsActive = 1 AND IsDeleted = 0
                ORDER BY UpdatedDate DESC, CreatedDate DESC, PromptAssemblyProfileID DESC
                """
            )
        ).mappings().first()
        if prompt_assembly_profile is not None:
            payload["promptAssemblyProfileId"] = prompt_assembly_profile["PromptAssemblyProfileID"]
            payload["promptAssemblyProfileRef"] = (
                f"{prompt_assembly_profile['ProfileKey']}:{prompt_assembly_profile['StepName']}"
            )

        capability_policy_version = db_session.execute(
            text(
                """
                SELECT TOP 1
                    CapabilityPolicyVersionID,
                    PolicyKey,
                    VersionNumber,
                    PolicyJson
                FROM config.CapabilityPolicyVersion
                WHERE IsActive = 1 AND IsDeleted = 0
                ORDER BY ActivatedDate DESC, CreatedDate DESC, CapabilityPolicyVersionID DESC
                """
            )
        ).mappings().first()
        if capability_policy_version is not None:
            payload["capabilityPolicyVersionId"] = (
                capability_policy_version["CapabilityPolicyVersionID"]
            )
            payload["capabilityPolicyVersionRef"] = (
                f"{capability_policy_version['PolicyKey']}:v{capability_policy_version['VersionNumber']}"
            )
            if isinstance(capability_policy_version.get("PolicyJson"), str):
                try:
                    payload["capabilityPolicyJson"] = json.loads(
                        capability_policy_version["PolicyJson"]
                    )
                except json.JSONDecodeError:
                    payload["capabilityPolicyJson"] = None

        capability_snapshot = db_session.execute(
            text(
                """
                SELECT TOP 1
                    ComponentCapabilitySnapshotID,
                    SnapshotVersion,
                    SnapshotJson
                FROM config.ComponentCapabilitySnapshot
                WHERE IsActive = 1 AND IsDeleted = 0
                ORDER BY GeneratedDate DESC, ComponentCapabilitySnapshotID DESC
                """
            )
        ).mappings().first()
        if capability_snapshot is not None:
            payload["componentCapabilitySnapshotId"] = (
                capability_snapshot["ComponentCapabilitySnapshotID"]
            )
            payload["componentCapabilitySnapshotRef"] = capability_snapshot["SnapshotVersion"]
            if isinstance(capability_snapshot.get("SnapshotJson"), str):
                try:
                    payload["componentCapabilitySnapshotJson"] = json.loads(
                        capability_snapshot["SnapshotJson"]
                    )
                except json.JSONDecodeError:
                    payload["componentCapabilitySnapshotJson"] = None

        width_policy_version = db_session.execute(
            text(
                """
                SELECT TOP 1
                    WidthClassPolicyVersionID,
                    PolicyKey,
                    VersionNumber,
                    PolicyJson
                FROM config.WidthClassPolicyVersion
                WHERE IsActive = 1 AND IsDeleted = 0
                ORDER BY ActivatedDate DESC, CreatedDate DESC, WidthClassPolicyVersionID DESC
                """
            )
        ).mappings().first()
        if width_policy_version is not None:
            payload["widthClassPolicyVersionId"] = (
                width_policy_version["WidthClassPolicyVersionID"]
            )
            payload["widthClassPolicyVersionRef"] = (
                f"{width_policy_version['PolicyKey']}:v{width_policy_version['VersionNumber']}"
            )
            if isinstance(width_policy_version.get("PolicyJson"), str):
                try:
                    payload["widthClassPolicyJson"] = json.loads(
                        width_policy_version["PolicyJson"]
                    )
                except json.JSONDecodeError:
                    payload["widthClassPolicyJson"] = None

        contracts = db_session.execute(
            text(
                """
                SELECT
                    ComponentType,
                    ContractVersion,
                    AllowedRulesJson,
                    RuleParameterSchemaJson,
                    RuleCompatibilityJson,
                    MessagePolicyJson
                FROM config.ComponentValidationContract
                WHERE IsActive = 1 AND IsDeleted = 0
                ORDER BY ComponentType ASC, ContractVersion ASC
                """
            )
        ).mappings().all()
        if contracts:
            normalized_contracts: List[Dict[str, Any]] = []
            for row in contracts:
                allowed_rules: List[str] = []
                if isinstance(row.get("AllowedRulesJson"), str):
                    try:
                        parsed_rules = json.loads(row["AllowedRulesJson"])
                        if isinstance(parsed_rules, list):
                            allowed_rules = [
                                str(rule).strip() for rule in parsed_rules if str(rule).strip()
                            ]
                    except json.JSONDecodeError:
                        allowed_rules = []
                normalized_contracts.append(
                    {
                        "componentType": row.get("ComponentType"),
                        "contractVersion": row.get("ContractVersion"),
                        "allowedRules": allowed_rules,
                    }
                )
            payload["validationContracts"] = normalized_contracts
            signature = "|".join(
                f"{row['ComponentType']}:{row['ContractVersion']}" for row in contracts
            )
            payload["validationContractVersion"] = (
                f"contracts-{_sha256_hex(signature)[:12]}-{len(contracts)}"
            )

        if not any(
            payload[key] is not None
            for key in (
                "promptTemplateVersionId",
                "promptAssemblyProfileId",
                "capabilityPolicyVersionId",
                "componentCapabilitySnapshotId",
                "widthClassPolicyVersionId",
                "validationContractVersion",
            )
        ):
            payload["governanceResolutionSource"] = "db-empty"
        return payload
    except Exception:
        LOGGER.exception("form-ai governance resolution failed")
        payload["governanceResolutionSource"] = "db-resolution-error"
        return payload


def _persist_generation_run_and_artifacts(
    *,
    db_session: Optional[Session],
    actor_user_id: Optional[int],
    company_id: Optional[int],
    prompt: str,
    runtime_context: Optional[Dict[str, Any]],
    response: FormAiGenerateResponse,
    raw_attempt_payloads: List[Dict[str, Any]],
    semantic_attempt_payloads: List[Dict[str, Any]],
    compiled_attempt_payloads: List[Dict[str, Any]],
    governance_versions: Dict[str, Any],
    compile_input_plans: Optional[List[Dict[str, Any]]] = None,
) -> Optional[int]:
    """Persist a GenerationRun + its artifacts. Returns the GenerationRunID
    on success (or None if no DB session was available, or persistence
    failed). Story 6.3.1 UAT round 5: the id is needed by the response so
    the frontend can call ``/remeasure`` against the same run.
    """
    if db_session is None:
        return None

    try:
        context = get_current_request_context()
        request_id = (
            context.request_id if context and isinstance(context.request_id, str) and context.request_id else None
        ) or _build_request_id_fallback()

        resolved_company_id = company_id
        if resolved_company_id is None and context is not None:
            resolved_company_id = context.company_id

        prompt_hash = _sha256_hex(prompt)
        runtime_context_text = _safe_json_dumps(runtime_context or {})
        runtime_context_hash = _sha256_hex(runtime_context_text)
        form_id = _coerce_form_id(runtime_context)
        resolved_form_id = form_id
        if resolved_form_id is not None:
            form_exists = db_session.execute(
                text("SELECT TOP 1 FormID FROM dbo.Form WHERE FormID = :form_id"),
                {"form_id": resolved_form_id},
            ).scalar_one_or_none()
            if form_exists is None:
                resolved_form_id = None

        resolved_company_fk = resolved_company_id
        if resolved_company_fk is not None:
            company_exists = db_session.execute(
                text("SELECT TOP 1 CompanyID FROM dbo.Company WHERE CompanyID = :company_id"),
                {"company_id": resolved_company_fk},
            ).scalar_one_or_none()
            if company_exists is None:
                resolved_company_fk = None

        run_insert = db_session.execute(
            text(
                """
                INSERT INTO dbo.GenerationRun
                (
                    RequestID,
                    CompanyID,
                    FormID,
                    PromptTemplateVersionID,
                    PromptAssemblyProfileID,
                    CapabilityPolicyVersionID,
                    ComponentCapabilitySnapshotID,
                    WidthClassPolicyVersionID,
                    ValidationContractVersion,
                    PromptHash,
                    RuntimeContextHash,
                    Status,
                    TerminalReason,
                    AttemptCount,
                    FirstShotValid,
                    IsReplayable,
                    CreatedBy
                )
                OUTPUT inserted.GenerationRunID
                VALUES
                (
                    :request_id,
                    :company_id,
                    :form_id,
                    :prompt_template_version_id,
                    :prompt_assembly_profile_id,
                    :capability_policy_version_id,
                    :component_capability_snapshot_id,
                    :width_class_policy_version_id,
                    :validation_contract_version,
                    :prompt_hash,
                    :runtime_context_hash,
                    :status,
                    :terminal_reason,
                    :attempt_count,
                    :first_shot_valid,
                    :is_replayable,
                    :created_by
                )
                """
            ),
            {
                "request_id": request_id,
                "company_id": resolved_company_fk,
                "form_id": resolved_form_id,
                "prompt_template_version_id": governance_versions.get("promptTemplateVersionId"),
                "prompt_assembly_profile_id": governance_versions.get("promptAssemblyProfileId"),
                "capability_policy_version_id": governance_versions.get("capabilityPolicyVersionId"),
                "component_capability_snapshot_id": governance_versions.get(
                    "componentCapabilitySnapshotId"
                ),
                "width_class_policy_version_id": governance_versions.get("widthClassPolicyVersionId"),
                "validation_contract_version": governance_versions.get(
                    "validationContractVersion"
                ),
                "prompt_hash": prompt_hash,
                "runtime_context_hash": runtime_context_hash,
                "status": response.status,
                "terminal_reason": response.trace.terminalReason,
                "attempt_count": response.trace.attemptCount,
                "first_shot_valid": (
                    response.trace.attempts[0].validation.valid
                    if response.trace.attempts
                    else None
                ),
                "is_replayable": True,
                "created_by": actor_user_id,
            },
        )
        generation_run_id = run_insert.scalar_one()

        artifact_insert_stmt = text(
            """
            INSERT INTO dbo.GenerationArtifact
            (
                GenerationRunID,
                ArtifactType,
                SequenceNumber,
                ArtifactJson,
                ArtifactHash,
                IsCompressed,
                CreatedBy
            )
            VALUES
            (
                :generation_run_id,
                :artifact_type,
                :sequence_number,
                :artifact_json,
                :artifact_hash,
                :is_compressed,
                :created_by
            )
            """
        )
        artifact_rows: List[Dict[str, Any]] = []
        for payload in raw_attempt_payloads:
            payload_json = _safe_json_dumps(payload)
            artifact_rows.append(
                {
                    "generation_run_id": generation_run_id,
                    "artifact_type": "raw-semantic-attempt",
                    "sequence_number": int(payload.get("attemptNumber", 1)),
                    "artifact_json": payload_json,
                    "artifact_hash": _sha256_hex(payload_json),
                    "is_compressed": False,
                    "created_by": actor_user_id,
                }
            )
        for payload in semantic_attempt_payloads:
            payload_json = _safe_json_dumps(payload)
            artifact_rows.append(
                {
                    "generation_run_id": generation_run_id,
                    "artifact_type": "semantic-plan-attempt",
                    "sequence_number": int(payload.get("attemptNumber", 1)),
                    "artifact_json": payload_json,
                    "artifact_hash": _sha256_hex(payload_json),
                    "is_compressed": False,
                    "created_by": actor_user_id,
                }
            )
        for payload in compiled_attempt_payloads:
            payload_json = _safe_json_dumps(payload)
            artifact_rows.append(
                {
                    "generation_run_id": generation_run_id,
                    "artifact_type": "compiled-definition-attempt",
                    "sequence_number": int(payload.get("attemptNumber", 1)),
                    "artifact_json": payload_json,
                    "artifact_hash": _sha256_hex(payload_json),
                    "is_compressed": False,
                    "created_by": actor_user_id,
                }
            )
        # Story 6.3.1 UAT round 5 — render-then-measure: persist the exact
        # plan that was fed to the compiler (i.e. after heading-filter and
        # any other pre-compile transforms). The /remeasure endpoint loads
        # this artifact and feeds it straight back into the compiler with
        # measured heights, so the second pass is byte-identical to the
        # first except for the resolved height per component.
        for payload in compile_input_plans or []:
            payload_json = _safe_json_dumps(payload)
            artifact_rows.append(
                {
                    "generation_run_id": generation_run_id,
                    "artifact_type": "compile-input-plan",
                    "sequence_number": int(payload.get("attemptNumber", 1)),
                    "artifact_json": payload_json,
                    "artifact_hash": _sha256_hex(payload_json),
                    "is_compressed": False,
                    "created_by": actor_user_id,
                }
            )

        trace_json = _safe_json_dumps(response.trace.model_dump())
        artifact_rows.append(
            {
                "generation_run_id": generation_run_id,
                "artifact_type": "trace-metadata",
                "sequence_number": 1,
                "artifact_json": trace_json,
                "artifact_hash": _sha256_hex(trace_json),
                "is_compressed": False,
                "created_by": actor_user_id,
            }
        )
        if response.definitionJSON is not None:
            final_json = _safe_json_dumps(response.definitionJSON)
            artifact_rows.append(
                {
                    "generation_run_id": generation_run_id,
                    "artifact_type": "final-definition",
                    "sequence_number": 1,
                    "artifact_json": final_json,
                    "artifact_hash": _sha256_hex(final_json),
                    "is_compressed": False,
                    "created_by": actor_user_id,
                }
            )

        for row in artifact_rows:
            db_session.execute(artifact_insert_stmt, row)
        db_session.commit()
        return generation_run_id
    except Exception:
        db_session.rollback()
        LOGGER.exception("form-ai generation run/artifact persistence failed")
        return None


def _build_trace_metadata(
    *,
    terminal_reason: str,
    attempts: List[AttemptTraceEntry],
    correction_cap: int,
    last_validation: Optional[AttemptValidationSummary],
    resolved_transport: Literal["sync", "stream"],
    governance_versions: Dict[str, Any],
    last_compile_summary: Optional[Dict[str, Any]],
    last_violations: Optional[List[SemanticPlanViolation]] = None,
    attempt_count_override: Optional[int] = None,
) -> GenerationTraceMetadata:
    """Build a GenerationTraceMetadata from the live loop state.

    Centralises the (previously 4x duplicated) trace assembly so adding new
    governance/failure fields is one edit. ``attempt_count_override`` exists
    for the provider-error path which counts the in-flight attempt even
    though no AttemptTraceEntry was appended for it.
    """
    attempt_count = (
        attempt_count_override
        if attempt_count_override is not None
        else len(attempts)
    )
    return GenerationTraceMetadata(
        attemptCount=attempt_count,
        maxSystemCorrectionAttempts=correction_cap,
        systemCorrectionAttemptsUsed=max(0, attempt_count - 1),
        terminalReason=terminal_reason,
        attempts=attempts,
        validationSummary=last_validation,
        resolvedOpenaiTransport=resolved_transport,
        promptTemplateVersionId=governance_versions.get("promptTemplateVersionId"),
        promptTemplateVersionRef=governance_versions.get("promptTemplateVersionRef"),
        promptAssemblyProfileId=governance_versions.get("promptAssemblyProfileId"),
        promptAssemblyProfileRef=governance_versions.get("promptAssemblyProfileRef"),
        capabilityPolicyVersionId=governance_versions.get("capabilityPolicyVersionId"),
        capabilityPolicyVersionRef=governance_versions.get("capabilityPolicyVersionRef"),
        componentCapabilitySnapshotId=governance_versions.get("componentCapabilitySnapshotId"),
        componentCapabilitySnapshotRef=governance_versions.get("componentCapabilitySnapshotRef"),
        widthClassPolicyVersionId=governance_versions.get("widthClassPolicyVersionId"),
        widthClassPolicyVersionRef=governance_versions.get("widthClassPolicyVersionRef"),
        validationContractVersion=governance_versions.get("validationContractVersion"),
        governanceResolutionSource=governance_versions.get("governanceResolutionSource"),
        compilerMode="deterministic-grid",
        compileSummary=last_compile_summary,
        failureClass=_classify_failure(terminal_reason),
        semanticValidationViolations=last_violations,
    )


def remeasure_form_definition(
    body: FormAiRemeasureRequest,
    *,
    runtime_context: Optional[Dict[str, Any]],
    db_session: Session,
    actor_user_id: Optional[int] = None,
) -> FormAiRemeasureResponse:
    """Story 6.3.1 UAT round 5 — render-then-measure second pass.

    Loads the original ``compile-input-plan`` artifact for ``generationRunId``,
    re-runs the deterministic compiler with the supplied DOM heights, and
    returns a refined ``DefinitionJSON`` that exactly matches what the
    renderer is going to paint. The first pass is left untouched on the
    canvas while this runs; the frontend swaps to the refined definition
    on success and keeps the first pass on failure.

    The endpoint never calls the LLM, so retries / semantic violations /
    transport selection are all N/A. It does call the same compiler +
    post-processing + validation pipeline as ``/generate`` so the returned
    ``DefinitionJSON`` is governed exactly the same way.
    """
    # ----- 1. Load the persisted compile-input-plan ----------------------
    plan_row = db_session.execute(
        text(
            """
            SELECT TOP 1 ArtifactJson
            FROM dbo.GenerationArtifact
            WHERE GenerationRunID = :run_id
              AND ArtifactType = 'compile-input-plan'
            ORDER BY SequenceNumber DESC, GenerationArtifactID DESC
            """
        ),
        {"run_id": body.generationRunId},
    ).mappings().first()

    if plan_row is None:
        # No compile-input-plan persisted — almost always means the run is
        # from before UAT round 5 shipped. Fall back to "remeasure not
        # available" so the frontend keeps the first-pass definition.
        return FormAiRemeasureResponse(
            status="failed",
            definitionJSON=None,
            compileSummary=None,
            validationSummary=None,
            userMessage=(
                "Render-then-measure is unavailable for this generation. "
                "The first-pass layout will be used."
            ),
            generationRunId=body.generationRunId,
        )

    try:
        plan_envelope = json.loads(plan_row["ArtifactJson"])
        plan_dict = plan_envelope.get("plan") if isinstance(plan_envelope, dict) else None
        if not isinstance(plan_dict, dict):
            raise ValueError("compile-input-plan envelope missing 'plan'")
        semantic_plan = FormSemanticPlan.model_validate(plan_dict)
    except Exception:
        LOGGER.exception(
            "form-ai /remeasure: failed to load compile-input-plan for run %s",
            body.generationRunId,
        )
        return FormAiRemeasureResponse(
            status="failed",
            definitionJSON=None,
            compileSummary=None,
            validationSummary=None,
            userMessage=(
                "Render-then-measure could not load the original semantic plan. "
                "The first-pass layout will be used."
            ),
            generationRunId=body.generationRunId,
        )

    # ----- 2. Resolve governance the same way /generate does -------------
    # Same active versions snapshot. The first pass might have used a
    # different version if the policy changed between the two calls; this
    # is fine for the second pass because the compiler accepts the same
    # FormSemanticPlan shape across active versions and the validator is
    # version-stable. We still log when the snapshot id drifts.
    governance_versions = _resolve_runtime_governance_versions(db_session)

    # ----- 3. Build the measurement map ----------------------------------
    measured_heights: Dict[str, float] = {
        m.componentId: float(m.height) for m in body.measurements
    }

    # ----- 4. Recompile with measurements --------------------------------
    try:
        candidate, compile_summary = compile_semantic_plan_to_definition(
            semantic_plan,
            runtime_context=runtime_context,
            capability_policy_json=governance_versions.get("capabilityPolicyJson"),
            width_policy_json=governance_versions.get("widthClassPolicyJson"),
            capability_snapshot_json=governance_versions.get(
                "componentCapabilitySnapshotJson"
            ),
            validation_contracts=governance_versions.get("validationContracts"),
            measured_heights=measured_heights,
        )
        candidate = _normalize_display_component_props(candidate)
        compiler_mode = (
            str(compile_summary.get("compilerMode", "deterministic-grid"))
            if isinstance(compile_summary, dict)
            else "deterministic-grid"
        )
        # Use the prompt placeholder from the captured plan envelope when
        # available; otherwise pass an empty prompt — post-processing only
        # uses the prompt for heuristics that are no-ops on a remeasure
        # pass (e.g. heading dropping has already happened pre-compile).
        candidate, post_processing_applied = _post_process_generated_definition(
            candidate,
            "",
            runtime_context,
            compiler_mode=compiler_mode,
        )
        if isinstance(compile_summary, dict):
            compile_summary["postProcessingApplied"] = post_processing_applied
            compile_summary["remeasureRunId"] = body.generationRunId
    except Exception:
        LOGGER.exception(
            "form-ai /remeasure: compile failed for run %s",
            body.generationRunId,
        )
        return FormAiRemeasureResponse(
            status="failed",
            definitionJSON=None,
            compileSummary=None,
            validationSummary=None,
            userMessage=(
                "Render-then-measure recompile failed. "
                "The first-pass layout will be used."
            ),
            generationRunId=body.generationRunId,
        )

    # ----- 5. Validate the refined definition ----------------------------
    validation = validate_definition_payload({"definition": candidate})
    validation = _merge_guardrail_errors(
        validation, _validate_single_page_guardrail(candidate)
    )
    validation = _merge_visual_boundaries(
        validation, _collect_visual_boundary_violations(candidate, runtime_context)
    )
    validation = _merge_visual_collisions(
        validation, _collect_visual_collisions(candidate, runtime_context)
    )
    summary = _validation_summary(validation)

    # ----- 6. Persist remeasure artifacts on the same run ----------------
    try:
        artifact_insert_stmt = text(
            """
            INSERT INTO dbo.GenerationArtifact
            (GenerationRunID, ArtifactType, SequenceNumber, ArtifactJson,
             ArtifactHash, IsCompressed, CreatedBy)
            VALUES
            (:generation_run_id, :artifact_type, :sequence_number,
             :artifact_json, :artifact_hash, :is_compressed, :created_by)
            """
        )
        # Sequence number = 1 + existing remeasure-output rows so multiple
        # remeasure calls on the same run are tracked in order.
        existing = db_session.execute(
            text(
                """
                SELECT COUNT(*) AS n FROM dbo.GenerationArtifact
                WHERE GenerationRunID = :run_id
                  AND ArtifactType = 'remeasure-output'
                """
            ),
            {"run_id": body.generationRunId},
        ).scalar_one()
        next_sequence = int(existing) + 1

        input_json = _safe_json_dumps(
            {
                "measurements": [m.model_dump() for m in body.measurements],
                "runtimeContext": runtime_context,
            }
        )
        output_json = _safe_json_dumps(
            {
                "definition": candidate,
                "compileSummary": compile_summary,
                "validation": summary.model_dump(),
            }
        )
        db_session.execute(
            artifact_insert_stmt,
            {
                "generation_run_id": body.generationRunId,
                "artifact_type": "remeasure-input",
                "sequence_number": next_sequence,
                "artifact_json": input_json,
                "artifact_hash": _sha256_hex(input_json),
                "is_compressed": False,
                "created_by": actor_user_id,
            },
        )
        db_session.execute(
            artifact_insert_stmt,
            {
                "generation_run_id": body.generationRunId,
                "artifact_type": "remeasure-output",
                "sequence_number": next_sequence,
                "artifact_json": output_json,
                "artifact_hash": _sha256_hex(output_json),
                "is_compressed": False,
                "created_by": actor_user_id,
            },
        )
        db_session.commit()
    except Exception:
        db_session.rollback()
        LOGGER.exception(
            "form-ai /remeasure: artifact persistence failed for run %s",
            body.generationRunId,
        )

    # ----- 7. Build response -------------------------------------------------
    is_valid = bool(summary.valid)
    return FormAiRemeasureResponse(
        status="completed" if is_valid else "failed",
        definitionJSON=candidate if is_valid else None,
        compileSummary=compile_summary if isinstance(compile_summary, dict) else None,
        validationSummary=summary,
        userMessage=(
            "Layout refined using rendered measurements."
            if is_valid
            else (
                "Render-then-measure produced a layout with validation issues. "
                "The first-pass layout will be used."
            )
        ),
        generationRunId=body.generationRunId,
    )


def generate_form_definition(
    prompt: str,
    model_override: str | None = None,
    runtime_context: Optional[Dict[str, Any]] = None,
    openai_transport: str = "auto",
    *,
    max_system_correction_attempts: int | None = None,
    system_prompt_addendum: str | None = None,
    db_session: Optional[Session] = None,
    actor_user_id: Optional[int] = None,
    actor_company_id: Optional[int] = None,
) -> FormAiGenerateResponse:
    trace_entries: List[AttemptTraceEntry] = []
    raw_attempt_payloads: List[Dict[str, Any]] = []
    semantic_attempt_payloads: List[Dict[str, Any]] = []
    compiled_attempt_payloads: List[Dict[str, Any]] = []
    # Story 6.3.1 UAT round 5 — captured per-attempt for /remeasure replay.
    compile_input_plans: List[Dict[str, Any]] = []
    governance_versions = _resolve_runtime_governance_versions(db_session)
    resolved_transport = _resolve_openai_transport(openai_transport)
    correction_cap = (
        max_system_correction_attempts
        if max_system_correction_attempts is not None
        else _get_default_retries(db_session)
    )
    correction_cap = max(0, min(correction_cap, 10))

    def _finalize(response: FormAiGenerateResponse) -> FormAiGenerateResponse:
        run_id = _persist_generation_run_and_artifacts(
            db_session=db_session,
            actor_user_id=actor_user_id,
            company_id=actor_company_id,
            prompt=prompt,
            runtime_context=runtime_context,
            response=response,
            raw_attempt_payloads=raw_attempt_payloads,
            semantic_attempt_payloads=semantic_attempt_payloads,
            compiled_attempt_payloads=compiled_attempt_payloads,
            governance_versions=governance_versions,
            compile_input_plans=compile_input_plans,
        )
        # Story 6.3.1 UAT round 5 — surface the persisted run id so the
        # frontend can call ``/remeasure`` with DOM heights for a refined
        # second-pass layout. None when persistence is disabled (tests) or
        # the insert failed (caught and logged inside the persist helper).
        if run_id is not None:
            response.generationRunId = run_id
        return response

    try:
        context_pack = _load_context_pack()
    except RuntimeError:
        trace = _build_trace_metadata(
            terminal_reason="context-pack-load-failed",
            attempts=[],
            correction_cap=correction_cap,
            last_validation=None,
            resolved_transport=resolved_transport,
            governance_versions=governance_versions,
            last_compile_summary=None,
            attempt_count_override=0,
        )
        return _finalize(FormAiGenerateResponse(
            status="failed",
            definitionJSON=None,
            trace=trace,
            userMessage=(
                "AI generation failed before execution. "
                "Please contact support and try again."
            ),
            draftHasValidationIssues=False,
        ))

    # Filter the runtime palette to types the active capability snapshot
    # actually registers. The frontend builds ``componentFootprints`` from the
    # toolbox DOM, which can advertise types the snapshot doesn't accept; that
    # was the dominant cause of UAT failures (the LLM used ``rating`` /
    # ``file-upload`` / ``first-name``, the semantic gate rejected them, and
    # the only correction round-trip was wasted relabelling them).
    capability_snapshot_for_prompt = governance_versions.get(
        "componentCapabilitySnapshotJson"
    )
    runtime_context_for_prompt = _filter_runtime_context_to_capability(
        runtime_context, capability_snapshot_for_prompt
    )

    messages = _build_initial_messages(
        prompt=prompt,
        context_pack=context_pack,
        runtime_context=runtime_context_for_prompt,
        system_prompt_addendum=system_prompt_addendum,
        capability_snapshot_json=capability_snapshot_for_prompt,
    )
    last_validation: AttemptValidationSummary | None = None
    last_valid_definition: Dict[str, Any] | None = None
    last_candidate: Dict[str, Any] | None = None
    last_compile_summary: Dict[str, Any] | None = None
    # Story 6.3.1 (failure-mode separation): violations from the most recent
    # attempt that exercised the gate. Cleared on the next attempt that passes
    # the gate or fails before reaching it. Surfaced on terminal exit so the
    # UI/triage can show the LLM's last semantic mistakes.
    last_violations: Optional[List[SemanticPlanViolation]] = None

    def _llm_fault_summary() -> AttemptValidationSummary:
        """Single-error stub validation summary used for LLM-fault stages
        that fail before validate_definition_payload runs."""
        return AttemptValidationSummary(
            valid=False,
            schemaErrorCount=1,
            boundaryViolationCount=0,
            collisionCount=0,
            errorCount=1,
        )

    def _user_message_for_terminal(
        terminal_reason: str, *, has_draft: bool
    ) -> str:
        """Story 6.3.1: per-terminalReason user-facing message. Compiler-fault
        messages explicitly tell the user it is not their prompt's fault."""
        draft_suffix = (
            "The last draft is included so you can load it on the canvas to inspect."
            if has_draft
            else "Please try again."
        )
        if terminal_reason == "json-parse-failed":
            return (
                "The AI returned a response that was not valid JSON. "
                "Please try again or refine your prompt."
            )
        if terminal_reason == "semantic-plan-invalid":
            return (
                "The AI returned a response that did not match the semantic plan contract "
                "(JSON shape). Please try again or refine the prompt."
            )
        if terminal_reason == "semantic-rules-violated":
            return (
                "The AI's plan failed policy validation (component types, "
                "options, validation rules) within the retry budget. "
                "Please refine your prompt and try again."
            )
        if terminal_reason == "compiler-error":
            return (
                "Internal compiler error while building the form layout. "
                "This is not your prompt's fault. Please report this run to support. "
                + draft_suffix
            )
        if terminal_reason == "compiler-validation-failed":
            return (
                "The compiler produced a layout that did not pass our self-check "
                "(schema or geometry). This is not your prompt's fault; please report it. "
                + draft_suffix
            )
        # Unchanged messages for legacy terminal reasons:
        if terminal_reason == "provider-error":
            return (
                "AI provider call failed before validation could finish. "
                + (
                    "The last draft from the previous successful model response is included - "
                    "you can load it on the canvas to inspect layout."
                    if has_draft
                    else "Please try again."
                )
            )
        if terminal_reason == "first-shot-invalid":
            return (
                "The first model response did not pass validation. "
                + (
                    "The draft JSON is included so you can inspect layout. "
                    if has_draft
                    else ""
                )
                + "Tune system instructions (addendum) or the prompt and try again."
            )
        if terminal_reason == "retry-cap-exhausted":
            return (
                f"AI generation could not produce a valid form within "
                f"{correction_cap} correction attempt(s). "
                + (
                    "The last draft is included so you can load it on the canvas to inspect. "
                    if has_draft
                    else ""
                )
                + "You may revise your prompt and try again."
            )
        return "AI generation failed. Please try again."

    max_attempts = correction_cap + 1
    for attempt_number in range(1, correction_cap + 2):
        phase = "initial" if attempt_number == 1 else "correction"
        correction_issued = attempt_number <= correction_cap

        LOGGER.info(
            "form-ai generate attempt %s/%s phase=%s",
            attempt_number,
            max_attempts,
            phase,
        )

        # ============================================================
        # PROVIDER CALL. True provider failures exit immediately.
        # ============================================================
        try:
            provider_content = _request_chatgpt_completion(
                messages,
                model_override=model_override,
                openai_transport=resolved_transport,
            )
            raw_attempt_payloads.append(
                {
                    "attemptNumber": attempt_number,
                    "phase": phase,
                    "providerContent": provider_content,
                }
            )
        except (httpx.HTTPError, RuntimeError) as exc:
            LOGGER.exception(
                "form-ai provider call failed (attempt %s/%s): %s",
                attempt_number,
                max_attempts,
                exc,
            )
            trace = _build_trace_metadata(
                terminal_reason="provider-error",
                attempts=trace_entries,
                correction_cap=correction_cap,
                last_validation=last_validation,
                resolved_transport=resolved_transport,
                governance_versions=governance_versions,
                last_compile_summary=last_compile_summary,
                last_violations=last_violations,
                attempt_count_override=attempt_number,
            )
            has_draft = last_candidate is not None
            return _finalize(FormAiGenerateResponse(
                status="failed",
                definitionJSON=last_candidate if has_draft else None,
                trace=trace,
                userMessage=_user_message_for_terminal(
                    "provider-error", has_draft=has_draft
                ),
                draftHasValidationIssues=has_draft,
            ))

        # ============================================================
        # PHASE 1: JSON parse. LLM-fault: feeds back to LLM.
        # ============================================================
        try:
            semantic_raw = _extract_json_candidate(provider_content)
        except (ValueError, json.JSONDecodeError) as exc:
            error_summary = str(exc) or "json-parse-failed"
            LOGGER.warning(
                "form-ai json-parse failed (attempt %s/%s): %s",
                attempt_number,
                max_attempts,
                error_summary,
            )
            last_violations = None  # not a gate failure
            trace_entries.append(
                AttemptTraceEntry(
                    attemptNumber=attempt_number,
                    phase=phase,
                    validation=_llm_fault_summary(),
                    correctionIssued=correction_issued,
                    notes=f"json-parse-failed: {error_summary[:240]}",
                    collisionDeltaFromPrevious=None,
                    collisionTrendVsPrevious="n_a",
                    compileDiagnostics={"jsonParseError": error_summary},
                    failedAt="json-parse",
                )
            )
            last_validation = trace_entries[-1].validation
            if attempt_number > correction_cap:
                trace = _build_trace_metadata(
                    terminal_reason="json-parse-failed",
                    attempts=trace_entries,
                    correction_cap=correction_cap,
                    last_validation=last_validation,
                    resolved_transport=resolved_transport,
                    governance_versions=governance_versions,
                    last_compile_summary=last_compile_summary,
                    last_violations=last_violations,
                )
                has_draft = last_candidate is not None
                return _finalize(FormAiGenerateResponse(
                    status="failed",
                    definitionJSON=last_candidate if has_draft else None,
                    trace=trace,
                    userMessage=_user_message_for_terminal(
                        "json-parse-failed", has_draft=has_draft
                    ),
                    draftHasValidationIssues=has_draft,
                ))
            messages.append({"role": "assistant", "content": provider_content})
            messages.append(
                {
                    "role": "user",
                    "content": _correction_message_for_json_parse(error_summary),
                }
            )
            continue

        # ============================================================
        # PHASE 2: Semantic plan parse (Pydantic shape).
        # LLM-fault: feeds back to LLM.
        # ============================================================
        try:
            semantic_plan = _extract_semantic_plan_candidate(semantic_raw)
            semantic_attempt_payloads.append(
                {
                    "attemptNumber": attempt_number,
                    "phase": phase,
                    "semanticPlan": semantic_plan.model_dump(),
                }
            )
        except (ValidationError, ValueError) as exc:
            error_summary = _summarise_semantic_plan_error(exc)
            LOGGER.warning(
                "form-ai semantic-plan parse failed (attempt %s/%s): %s",
                attempt_number,
                max_attempts,
                error_summary,
            )
            last_violations = None  # not a gate failure
            trace_entries.append(
                AttemptTraceEntry(
                    attemptNumber=attempt_number,
                    phase=phase,
                    validation=_llm_fault_summary(),
                    correctionIssued=correction_issued,
                    notes=f"semantic-plan-invalid: {error_summary[:240]}",
                    collisionDeltaFromPrevious=None,
                    collisionTrendVsPrevious="n_a",
                    compileDiagnostics={
                        "semanticPlanError": error_summary,
                        "errorType": type(exc).__name__,
                    },
                    failedAt="semantic-plan",
                )
            )
            last_validation = trace_entries[-1].validation
            if attempt_number > correction_cap:
                trace = _build_trace_metadata(
                    terminal_reason="semantic-plan-invalid",
                    attempts=trace_entries,
                    correction_cap=correction_cap,
                    last_validation=last_validation,
                    resolved_transport=resolved_transport,
                    governance_versions=governance_versions,
                    last_compile_summary=last_compile_summary,
                    last_violations=last_violations,
                )
                has_draft = last_candidate is not None
                return _finalize(FormAiGenerateResponse(
                    status="failed",
                    definitionJSON=last_candidate if has_draft else None,
                    trace=trace,
                    userMessage=_user_message_for_terminal(
                        "semantic-plan-invalid", has_draft=has_draft
                    ),
                    draftHasValidationIssues=has_draft,
                ))
            messages.append({"role": "assistant", "content": provider_content})
            messages.append(
                {
                    "role": "user",
                    "content": _build_semantic_plan_correction_message(error_summary),
                }
            )
            continue

        # ============================================================
        # PHASE 3: Semantic-validation gate (NEW).
        # Catches LLM faults that the Pydantic shape parser cannot:
        # unknown component type, disallowed widthIntent, missing
        # options, disallowed validation rule, duplicate componentId.
        # LLM-fault: feeds back to LLM.
        # ============================================================
        gate_result: SemanticPlanValidationResult = validate_semantic_plan(
            semantic_plan,
            capability_snapshot_json=governance_versions.get(
                "componentCapabilitySnapshotJson"
            ),
            validation_contracts=governance_versions.get("validationContracts"),
        )
        if not gate_result.valid:
            last_violations = gate_result.violations
            LOGGER.warning(
                "form-ai semantic-rules failed (attempt %s/%s): %s violation(s)",
                attempt_number,
                max_attempts,
                len(gate_result.violations),
            )
            trace_entries.append(
                AttemptTraceEntry(
                    attemptNumber=attempt_number,
                    phase=phase,
                    validation=_llm_fault_summary(),
                    correctionIssued=correction_issued,
                    notes=(
                        f"semantic-rules-violated: {len(gate_result.violations)} "
                        "violation(s)"
                    ),
                    collisionDeltaFromPrevious=None,
                    collisionTrendVsPrevious="n_a",
                    compileDiagnostics={
                        "semanticGateViolations": [
                            v.model_dump() for v in gate_result.violations
                        ],
                    },
                    failedAt="semantic-rules",
                )
            )
            last_validation = trace_entries[-1].validation
            if attempt_number > correction_cap:
                trace = _build_trace_metadata(
                    terminal_reason="semantic-rules-violated",
                    attempts=trace_entries,
                    correction_cap=correction_cap,
                    last_validation=last_validation,
                    resolved_transport=resolved_transport,
                    governance_versions=governance_versions,
                    last_compile_summary=last_compile_summary,
                    last_violations=last_violations,
                )
                has_draft = last_candidate is not None
                return _finalize(FormAiGenerateResponse(
                    status="failed",
                    definitionJSON=last_candidate if has_draft else None,
                    trace=trace,
                    userMessage=_user_message_for_terminal(
                        "semantic-rules-violated", has_draft=has_draft
                    ),
                    draftHasValidationIssues=has_draft,
                ))
            messages.append({"role": "assistant", "content": provider_content})
            messages.append(
                {
                    "role": "user",
                    "content": _correction_message_for_semantic_rules(
                        gate_result.violations
                    ),
                }
            )
            continue

        # Plan passed the gate; clear last attempt's violations so the
        # terminal trace doesn't carry stale data.
        last_violations = None

        # ============================================================
        # PHASE 4: Compile + post-process.
        # COMPILER-FAULT: never feeds back to LLM. Terminate immediately.
        # ============================================================
        try:
            # UAT round 5 (run 40, prompt 1) — strip courtesy headers BEFORE
            # compile so the row solver doesn't reserve vertical space for a
            # component the post-compile filter is going to drop. Without this
            # the first real component lands at ~y=104 instead of y=24 and the
            # canvas appears to have a large blank band at the top.
            plan_for_compile, headings_dropped = _filter_unrequested_headings_from_plan(
                semantic_plan, prompt
            )
            # Story 6.3.1 UAT round 5 — capture the *exact* plan we hand to
            # the compiler so /remeasure can replay it byte-for-byte with
            # measured heights. The semantic-plan-attempt artifact is the
            # raw model output (pre-filter); this one is the post-filter
            # plan that matches the compiled-definition-attempt.
            compile_input_plans.append(
                {
                    "attemptNumber": attempt_number,
                    "phase": phase,
                    "plan": plan_for_compile.model_dump(),
                    "headingsDropped": headings_dropped,
                }
            )
            candidate, compile_summary = compile_semantic_plan_to_definition(
                plan_for_compile,
                runtime_context=runtime_context,
                capability_policy_json=governance_versions.get("capabilityPolicyJson"),
                width_policy_json=governance_versions.get("widthClassPolicyJson"),
                capability_snapshot_json=governance_versions.get(
                    "componentCapabilitySnapshotJson"
                ),
                validation_contracts=governance_versions.get("validationContracts"),
            )
            if isinstance(compile_summary, dict) and headings_dropped:
                compile_summary["preCompileHeadingsDropped"] = headings_dropped
            candidate = _normalize_display_component_props(candidate)
            compiler_mode = (
                str(compile_summary.get("compilerMode", "deterministic-grid"))
                if isinstance(compile_summary, dict)
                else "deterministic-grid"
            )
            candidate, post_processing_applied = _post_process_generated_definition(
                candidate,
                prompt,
                runtime_context,
                compiler_mode=compiler_mode,
            )
            if isinstance(compile_summary, dict):
                compile_summary["postProcessingApplied"] = post_processing_applied
            last_candidate = candidate
            last_compile_summary = compile_summary
            compiled_attempt_payloads.append(
                {
                    "attemptNumber": attempt_number,
                    "phase": phase,
                    "definition": candidate,
                    "compileSummary": compile_summary,
                }
            )
        except Exception as exc:  # broad: ANY compile/post-process failure is a compiler bug
            LOGGER.exception(
                "form-ai compiler/post-process failed (attempt %s/%s): %s",
                attempt_number,
                max_attempts,
                exc,
            )
            trace_entries.append(
                AttemptTraceEntry(
                    attemptNumber=attempt_number,
                    phase=phase,
                    validation=_llm_fault_summary(),  # validation slot is unused for compile faults
                    correctionIssued=False,
                    notes=f"compiler-error: {type(exc).__name__}: {str(exc)[:200]}",
                    collisionDeltaFromPrevious=None,
                    collisionTrendVsPrevious="n_a",
                    compileDiagnostics={
                        "compilerError": str(exc),
                        "errorType": type(exc).__name__,
                    },
                    failedAt="compile",
                )
            )
            last_validation = trace_entries[-1].validation
            trace = _build_trace_metadata(
                terminal_reason="compiler-error",
                attempts=trace_entries,
                correction_cap=correction_cap,
                last_validation=last_validation,
                resolved_transport=resolved_transport,
                governance_versions=governance_versions,
                last_compile_summary=last_compile_summary,
                last_violations=None,
            )
            has_draft = last_candidate is not None
            return _finalize(FormAiGenerateResponse(
                status="failed",
                definitionJSON=last_candidate if has_draft else None,
                trace=trace,
                userMessage=_user_message_for_terminal(
                    "compiler-error", has_draft=has_draft
                ),
                draftHasValidationIssues=has_draft,
            ))

        # Story 6.3.1 (compiler-drops self-check): the gate should have
        # rejected anything the compiler would silently drop. If we still see
        # drops, that is a compiler bug surfacing - terminate as compiler-fault
        # rather than swallowing the missing components into a "successful"
        # response.
        dropped_count = 0
        if isinstance(compile_summary, dict):
            dropped_count = int(compile_summary.get("droppedComponentCount", 0) or 0)
        if dropped_count > 0:
            LOGGER.error(
                "form-ai compiler dropped %s component(s) after gate passed (attempt %s/%s)",
                dropped_count,
                attempt_number,
                max_attempts,
            )
            trace_entries.append(
                AttemptTraceEntry(
                    attemptNumber=attempt_number,
                    phase=phase,
                    validation=_llm_fault_summary(),
                    correctionIssued=False,
                    notes=f"compiler-error: dropped {dropped_count} component(s) post-gate",
                    collisionDeltaFromPrevious=None,
                    collisionTrendVsPrevious="n_a",
                    compileDiagnostics=last_compile_summary,
                    failedAt="compile",
                )
            )
            last_validation = trace_entries[-1].validation
            trace = _build_trace_metadata(
                terminal_reason="compiler-error",
                attempts=trace_entries,
                correction_cap=correction_cap,
                last_validation=last_validation,
                resolved_transport=resolved_transport,
                governance_versions=governance_versions,
                last_compile_summary=last_compile_summary,
                last_violations=None,
            )
            return _finalize(FormAiGenerateResponse(
                status="failed",
                definitionJSON=last_candidate,
                trace=trace,
                userMessage=_user_message_for_terminal(
                    "compiler-error", has_draft=True
                ),
                draftHasValidationIssues=True,
            ))

        # ============================================================
        # PHASE 5: Definition self-check (was: LLM-correction loop).
        # Schema + visual collisions/boundaries on the COMPILER's output.
        # COMPILER-FAULT: terminate, return draft so user/ops can inspect.
        # NEVER feeds back to LLM (the LLM does not own these positions).
        # ============================================================
        validation = validate_definition_payload({"definition": candidate})
        validation = _merge_guardrail_errors(
            validation, _validate_single_page_guardrail(candidate)
        )
        validation = _merge_visual_boundaries(
            validation, _collect_visual_boundary_violations(candidate, runtime_context)
        )
        validation = _merge_visual_collisions(
            validation, _collect_visual_collisions(candidate, runtime_context)
        )
        summary = _validation_summary(validation)
        prev_collision: int | None = None
        if trace_entries:
            prev_collision = trace_entries[-1].validation.collisionCount
        collision_delta: int | None = None
        collision_trend: Literal["improved", "worse", "unchanged", "n_a"] | None = None
        if prev_collision is None:
            collision_trend = "n_a"
        else:
            collision_delta = summary.collisionCount - prev_collision
            if collision_delta < 0:
                collision_trend = "improved"
            elif collision_delta > 0:
                collision_trend = "worse"
            else:
                collision_trend = "unchanged"

        trace_entries.append(
            AttemptTraceEntry(
                attemptNumber=attempt_number,
                phase=phase,
                validation=summary,
                correctionIssued=False,  # compiler-fault path: no LLM correction
                notes=None if summary.valid else "compiler-validation-failed",
                collisionDeltaFromPrevious=collision_delta,
                collisionTrendVsPrevious=collision_trend,
                compileDiagnostics=last_compile_summary,
                failedAt="none" if summary.valid else "compile-validation",
            )
        )
        last_validation = summary

        LOGGER.info(
            "form-ai generate attempt %s/%s self-check valid=%s errors=%s collisions=%s "
            "boundaries=%s collision_trend=%s collision_delta=%s",
            attempt_number,
            max_attempts,
            summary.valid,
            summary.errorCount,
            summary.collisionCount,
            summary.boundaryViolationCount,
            collision_trend,
            collision_delta,
        )

        if validation.valid:
            last_valid_definition = candidate
            break

        # Self-check failed -> compiler-fault, terminate. The LLM cannot fix
        # geometry it did not produce; this is a bug in the compiler.
        trace = _build_trace_metadata(
            terminal_reason="compiler-validation-failed",
            attempts=trace_entries,
            correction_cap=correction_cap,
            last_validation=last_validation,
            resolved_transport=resolved_transport,
            governance_versions=governance_versions,
            last_compile_summary=last_compile_summary,
            last_violations=None,
        )
        return _finalize(FormAiGenerateResponse(
            status="failed",
            definitionJSON=last_candidate,
            trace=trace,
            userMessage=_user_message_for_terminal(
                "compiler-validation-failed", has_draft=True
            ),
            draftHasValidationIssues=True,
        ))

    if last_valid_definition is not None:
        trace = _build_trace_metadata(
            terminal_reason="validated-success",
            attempts=trace_entries,
            correction_cap=correction_cap,
            last_validation=last_validation,
            resolved_transport=resolved_transport,
            governance_versions=governance_versions,
            last_compile_summary=last_compile_summary,
            last_violations=None,
        )
        return _finalize(FormAiGenerateResponse(
            status="completed",
            definitionJSON=last_valid_definition,
            trace=trace,
            userMessage=(
                "AI draft generated and validated successfully. "
                "The canvas has been updated."
            ),
            draftHasValidationIssues=False,
        ))

    # Loop exited without success and without an explicit terminal return.
    # In the new pipeline this only happens when the LLM-fault correction
    # loop runs out of attempts AND the most recent failure was at the
    # semantic-rules gate (because json-parse and semantic-plan terminate
    # explicitly when the cap is exhausted). retry-cap-exhausted is kept for
    # back-compat with existing dashboards.
    fail_reason = "first-shot-invalid" if correction_cap == 0 else "retry-cap-exhausted"
    trace = _build_trace_metadata(
        terminal_reason=fail_reason,
        attempts=trace_entries,
        correction_cap=correction_cap,
        last_validation=last_validation,
        resolved_transport=resolved_transport,
        governance_versions=governance_versions,
        last_compile_summary=last_compile_summary,
        last_violations=last_violations,
    )
    has_draft = last_candidate is not None
    return _finalize(FormAiGenerateResponse(
        status="failed",
        definitionJSON=last_candidate if has_draft else None,
        trace=trace,
        userMessage=_user_message_for_terminal(fail_reason, has_draft=has_draft),
        draftHasValidationIssues=has_draft,
    ))
