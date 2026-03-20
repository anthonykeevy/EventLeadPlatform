import json
import logging
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx

from middleware.outbound_request_logger import timed_log_outbound_http_request
from modules.form_validate.schemas import (
    BoundaryDirectionFlags,
    BoundaryViolation,
    CollisionViolation,
    FormValidationResponse,
    SchemaError,
    ValidationSummary,
)
from modules.form_validate.service import validate_definition_payload

from .schemas import (
    AttemptTraceEntry,
    AttemptValidationSummary,
    FormAiGenerateResponse,
    GenerationTraceMetadata,
)

MAX_SYSTEM_CORRECTION_ATTEMPTS = 3
_ROOT_PATH = Path(__file__).resolve().parents[3]
CONTEXT_PACK_PATH = _ROOT_PATH / "docs" / "stories" / "STORY-6.2-AI-CONTEXT-PACK.md"
LOGGER = logging.getLogger(__name__)


def _load_context_pack() -> str:
    try:
        return CONTEXT_PACK_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError("context-pack-load-failed") from exc


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
    definition: Dict[str, Any], prompt: str, runtime_context: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    pages = definition.get("pages")
    if not isinstance(pages, list):
        return definition

    allow_heading = _prompt_requests_heading(prompt)
    for page in pages:
        if not isinstance(page, dict):
            continue
        components = page.get("components")
        if not isinstance(components, list):
            continue

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

        # Always produce deterministic, contiguous tab order values for generated output.
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

        page["components"] = filtered_components

    definition = _sync_style_dimensions_into_props(definition)
    return _rebalance_single_column_vertical_spacing(definition, runtime_context)


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
        "textarea": 140.0,
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


def _flatten_visual_components(
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
                style = item.get("style") if isinstance(item.get("style"), dict) else {}
                props = item.get("props") if isinstance(item.get("props"), dict) else {}
                component_type = str(item.get("type", "text"))
                minimum_width = _minimum_render_width(component_type, runtime_footprints)
                stated_width = _parse_positive_dimension(
                    style.get("width", props.get("width")), minimum_width
                )
                width = max(stated_width, minimum_width)
                stated_height = _parse_positive_dimension(style.get("height"), 0.0)
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


def _collect_visual_collisions(
    definition: Dict[str, Any], runtime_context: Optional[Dict[str, Any]] = None
) -> List[CollisionViolation]:
    page_id, flattened = _flatten_visual_components(definition, runtime_context)
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
    page_id, flattened = _flatten_visual_components(definition, runtime_context)
    if not flattened:
        return []

    canvas = definition.get("canvasSettings")
    canvas_width = 1920.0
    canvas_height = 980.0
    if isinstance(canvas, dict):
        canvas_width = _parse_positive_dimension(canvas.get("width"), 1920.0)
        canvas_height = _parse_positive_dimension(canvas.get("height"), 980.0)
    runtime_canvas = (runtime_context or {}).get("canvas")
    if isinstance(runtime_canvas, dict):
        canvas_width = _parse_positive_dimension(runtime_canvas.get("width"), canvas_width)
        canvas_height = _parse_positive_dimension(
            runtime_canvas.get("height"), canvas_height
        )

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


def _build_initial_messages(
    prompt: str, context_pack: str, runtime_context: Optional[Dict[str, Any]] = None
) -> List[Dict[str, str]]:
    runtime_context_block = _build_runtime_context_block(runtime_context)
    return [
        {
            "role": "system",
            "content": (
                "You generate EventLead form DefinitionJSON for Story 6.2.\n"
                "Output a single JSON object only. No markdown or prose.\n"
                "Ensure schemaVersion is '1.0', include formId, theme, canvasSettings, and pages.\n"
                "Use only Story 6.2 MVP components and single-page constraints.\n\n"
                f"{context_pack}"
                + ("\n\n" + runtime_context_block if runtime_context_block else "")
            ),
        },
        {
            "role": "user",
            "content": (
                "Generate a DefinitionJSON for this request.\n"
                f"Prompt: {prompt}\n"
                "Return only valid JSON."
            ),
        },
    ]


def _build_correction_message(validation: FormValidationResponse) -> str:
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
    collision_lines = [
        (
            f"- {item.componentAId} overlaps {item.componentBId} "
            f"on {item.pageId} (area={item.overlapArea})"
        )
        for item in validation.collisions
    ]

    segments: List[str] = []
    if schema_lines:
        segments.append("Schema errors:\n" + "\n".join(schema_lines))
    if boundary_lines:
        segments.append("Boundary violations:\n" + "\n".join(boundary_lines))
    if collision_lines:
        segments.append("Collisions:\n" + "\n".join(collision_lines))

    return (
        "Your previous JSON failed validation. Correct it deterministically.\n"
        "Keep user intent while fixing all errors.\n"
        "Return only one valid JSON object.\n\n"
        + "\n\n".join(segments)
    )


def _request_chatgpt_completion(
    messages: List[Dict[str, str]], model_override: str | None = None
) -> str:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("missing-openai-api-key")

    if model_override and model_override.strip():
        model = model_override.strip()
    else:
        model = os.getenv("OPENAI_MODEL", "gpt-5-mini").strip() or "gpt-5-mini"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    timeout_seconds = 120.0
    timeout_raw = os.getenv("OPENAI_TIMEOUT_SECONDS", "").strip()
    if timeout_raw:
        try:
            parsed_timeout = float(timeout_raw)
            if parsed_timeout > 0:
                timeout_seconds = parsed_timeout
        except ValueError:
            pass

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

    def call_responses_api(client: httpx.Client) -> str:
        def _responses_content_type(role: str) -> str:
            # Responses API requires assistant history content as output_text.
            return "output_text" if role == "assistant" else "input_text"

        responses_payload = {
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

    # GPT-5 family is more reliable on Responses API than Chat Completions.
    model_lower = model.lower()
    prefer_responses_api = model_lower.startswith("gpt-5")

    with httpx.Client(timeout=timeout_seconds) as client:
        if prefer_responses_api:
            return call_responses_api(client)

        payload = {
            "model": model,
            "temperature": 0.2,
            "response_format": {"type": "json_object"},
            "messages": messages,
        }
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
            # Fall through to Responses API fallback.
            pass

        return call_responses_api(client)


def generate_form_definition(
    prompt: str,
    model_override: str | None = None,
    runtime_context: Optional[Dict[str, Any]] = None,
) -> FormAiGenerateResponse:
    trace_entries: List[AttemptTraceEntry] = []

    try:
        context_pack = _load_context_pack()
    except RuntimeError:
        trace = GenerationTraceMetadata(
            attemptCount=0,
            maxSystemCorrectionAttempts=MAX_SYSTEM_CORRECTION_ATTEMPTS,
            systemCorrectionAttemptsUsed=0,
            terminalReason="context-pack-load-failed",
            attempts=[],
            validationSummary=None,
        )
        return FormAiGenerateResponse(
            status="failed",
            definitionJSON=None,
            trace=trace,
            userMessage=(
                "AI generation failed before execution. "
                "Please contact support and try again."
            ),
        )

    messages = _build_initial_messages(
        prompt=prompt, context_pack=context_pack, runtime_context=runtime_context
    )
    last_validation: AttemptValidationSummary | None = None
    last_valid_definition: Dict[str, Any] | None = None

    for attempt_number in range(1, MAX_SYSTEM_CORRECTION_ATTEMPTS + 2):
        phase = "initial" if attempt_number == 1 else "correction"
        correction_issued = attempt_number <= MAX_SYSTEM_CORRECTION_ATTEMPTS

        try:
            provider_content = _request_chatgpt_completion(
                messages, model_override=model_override
            )
            candidate = _extract_json_candidate(provider_content)
            candidate = _normalize_display_component_props(candidate)
            candidate = _post_process_generated_definition(
                candidate, prompt, runtime_context
            )
        except (httpx.HTTPError, RuntimeError, ValueError):
            trace = GenerationTraceMetadata(
                attemptCount=attempt_number,
                maxSystemCorrectionAttempts=MAX_SYSTEM_CORRECTION_ATTEMPTS,
                systemCorrectionAttemptsUsed=max(0, attempt_number - 1),
                terminalReason="provider-error",
                attempts=trace_entries,
                validationSummary=last_validation,
            )
            return FormAiGenerateResponse(
                status="failed",
                definitionJSON=None,
                trace=trace,
                userMessage=(
                    "AI generation could not be completed right now. "
                    "Please try again."
                ),
            )

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
        trace_entries.append(
            AttemptTraceEntry(
                attemptNumber=attempt_number,
                phase=phase,
                validation=summary,
                correctionIssued=(not summary.valid) and correction_issued,
                notes=None if summary.valid else "validator-retry-required",
            )
        )
        last_validation = summary

        if validation.valid:
            last_valid_definition = candidate
            break

        if attempt_number > MAX_SYSTEM_CORRECTION_ATTEMPTS:
            break
        messages.append({"role": "assistant", "content": json.dumps(candidate)})
        messages.append({"role": "user", "content": _build_correction_message(validation)})

    if last_valid_definition is not None:
        trace = GenerationTraceMetadata(
            attemptCount=len(trace_entries),
            maxSystemCorrectionAttempts=MAX_SYSTEM_CORRECTION_ATTEMPTS,
            systemCorrectionAttemptsUsed=max(0, len(trace_entries) - 1),
            terminalReason="validated-success",
            attempts=trace_entries,
            validationSummary=last_validation,
        )
        return FormAiGenerateResponse(
            status="completed",
            definitionJSON=last_valid_definition,
            trace=trace,
            userMessage=(
                "AI draft generated and validated successfully. "
                "The canvas has been updated."
            ),
        )

    trace = GenerationTraceMetadata(
        attemptCount=len(trace_entries),
        maxSystemCorrectionAttempts=MAX_SYSTEM_CORRECTION_ATTEMPTS,
        systemCorrectionAttemptsUsed=max(0, len(trace_entries) - 1),
        terminalReason="retry-cap-exhausted",
        attempts=trace_entries,
        validationSummary=last_validation,
    )
    return FormAiGenerateResponse(
        status="failed",
        definitionJSON=None,
        trace=trace,
        userMessage=(
            "AI generation could not produce a valid form within 3 correction attempts. "
            "Please revise your prompt and try again."
        ),
    )
