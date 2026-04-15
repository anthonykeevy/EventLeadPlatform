import json
import logging
import math
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Literal, Optional

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
from modules.form_validate.service import (
    DEFAULT_HEIGHT_BY_TYPE,
    _parse_dimension,
    validate_definition_payload,
)

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
    min_height = _minimum_render_height(component_type, props, runtime_footprints)
    if component_type in ("dropdown", "select"):
        # Collision checks model the closed control footprint, not an expanded/open menu list.
        options = props.get("options")
        if isinstance(options, list):
            min_height -= max(0, len(options) - 3) * 20.0
    height = max(height_base, min_height)
    return width, height


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
    prompt: str,
    context_pack: str,
    runtime_context: Optional[Dict[str, Any]] = None,
    *,
    system_prompt_addendum: str | None = None,
) -> List[Dict[str, str]]:
    runtime_context_block = _build_runtime_context_block(runtime_context)
    system_body = (
        "You generate EventLead form DefinitionJSON for Story 6.2.\n"
        "Output a single JSON object only. No markdown or prose.\n"
        "Ensure schemaVersion is '1.0', include formId, theme, canvasSettings, and pages.\n"
        "Use only Story 6.2 MVP components and single-page constraints.\n\n"
        f"{context_pack}"
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
                "Generate a DefinitionJSON for this request.\n"
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


def generate_form_definition(
    prompt: str,
    model_override: str | None = None,
    runtime_context: Optional[Dict[str, Any]] = None,
    openai_transport: str = "auto",
    *,
    max_system_correction_attempts: int | None = None,
    system_prompt_addendum: str | None = None,
) -> FormAiGenerateResponse:
    trace_entries: List[AttemptTraceEntry] = []
    resolved_transport = _resolve_openai_transport(openai_transport)
    correction_cap = (
        max_system_correction_attempts
        if max_system_correction_attempts is not None
        else MAX_SYSTEM_CORRECTION_ATTEMPTS
    )
    correction_cap = max(0, min(correction_cap, 10))

    try:
        context_pack = _load_context_pack()
    except RuntimeError:
        trace = GenerationTraceMetadata(
            attemptCount=0,
            maxSystemCorrectionAttempts=correction_cap,
            systemCorrectionAttemptsUsed=0,
            terminalReason="context-pack-load-failed",
            attempts=[],
            validationSummary=None,
            resolvedOpenaiTransport=resolved_transport,
        )
        return FormAiGenerateResponse(
            status="failed",
            definitionJSON=None,
            trace=trace,
            userMessage=(
                "AI generation failed before execution. "
                "Please contact support and try again."
            ),
            draftHasValidationIssues=False,
        )

    messages = _build_initial_messages(
        prompt=prompt,
        context_pack=context_pack,
        runtime_context=runtime_context,
        system_prompt_addendum=system_prompt_addendum,
    )
    last_validation: AttemptValidationSummary | None = None
    last_valid_definition: Dict[str, Any] | None = None
    last_candidate: Dict[str, Any] | None = None

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
        try:
            provider_content = _request_chatgpt_completion(
                messages,
                model_override=model_override,
                openai_transport=resolved_transport,
            )
            candidate = _extract_json_candidate(provider_content)
            candidate = _normalize_display_component_props(candidate)
            candidate = _post_process_generated_definition(
                candidate, prompt, runtime_context
            )
            last_candidate = candidate
        except (httpx.HTTPError, RuntimeError, ValueError) as exc:
            LOGGER.exception(
                "form-ai generate failed before validation (attempt %s/%s): %s",
                attempt_number,
                max_attempts,
                exc,
            )
            trace = GenerationTraceMetadata(
                attemptCount=attempt_number,
                maxSystemCorrectionAttempts=correction_cap,
                systemCorrectionAttemptsUsed=max(0, attempt_number - 1),
                terminalReason="provider-error",
                attempts=trace_entries,
                validationSummary=last_validation,
                resolvedOpenaiTransport=resolved_transport,
            )
            has_draft = last_candidate is not None
            return FormAiGenerateResponse(
                status="failed",
                definitionJSON=last_candidate if has_draft else None,
                trace=trace,
                userMessage=(
                    "AI provider call failed before validation could finish. "
                    + (
                        "The last draft from the previous successful model response is included — "
                        "you can load it on the canvas to inspect layout."
                        if has_draft
                        else "Please try again."
                    )
                ),
                draftHasValidationIssues=has_draft,
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
                correctionIssued=(not summary.valid) and correction_issued,
                notes=None if summary.valid else "validator-retry-required",
                collisionDeltaFromPrevious=collision_delta,
                collisionTrendVsPrevious=collision_trend,
            )
        )
        last_validation = summary

        LOGGER.info(
            "form-ai generate attempt %s/%s validation valid=%s errors=%s collisions=%s "
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

        if attempt_number > correction_cap:
            break
        messages.append({"role": "assistant", "content": json.dumps(candidate)})
        messages.append(
            {
                "role": "user",
                "content": _build_correction_message(validation, candidate, runtime_context),
            }
        )

    if last_valid_definition is not None:
        trace = GenerationTraceMetadata(
            attemptCount=len(trace_entries),
            maxSystemCorrectionAttempts=correction_cap,
            systemCorrectionAttemptsUsed=max(0, len(trace_entries) - 1),
            terminalReason="validated-success",
            attempts=trace_entries,
            validationSummary=last_validation,
            resolvedOpenaiTransport=resolved_transport,
        )
        return FormAiGenerateResponse(
            status="completed",
            definitionJSON=last_valid_definition,
            trace=trace,
            userMessage=(
                "AI draft generated and validated successfully. "
                "The canvas has been updated."
            ),
            draftHasValidationIssues=False,
        )

    fail_reason = "first-shot-invalid" if correction_cap == 0 else "retry-cap-exhausted"
    trace = GenerationTraceMetadata(
        attemptCount=len(trace_entries),
        maxSystemCorrectionAttempts=correction_cap,
        systemCorrectionAttemptsUsed=max(0, len(trace_entries) - 1),
        terminalReason=fail_reason,
        attempts=trace_entries,
        validationSummary=last_validation,
        resolvedOpenaiTransport=resolved_transport,
    )
    has_draft = last_candidate is not None
    if correction_cap == 0:
        fail_msg = (
            "The first model response did not pass validation. "
            + (
                "The draft JSON is included so you can inspect layout. "
                if has_draft
                else ""
            )
            + "Tune system instructions (addendum) or the prompt and try again."
        )
    else:
        fail_msg = (
            f"AI generation could not produce a valid form within {correction_cap} correction attempt(s). "
            + (
                "The last draft is included so you can load it on the canvas to inspect collisions or layout. "
                if has_draft
                else ""
            )
            + "You may revise your prompt and try again."
        )
    return FormAiGenerateResponse(
        status="failed",
        definitionJSON=last_candidate if has_draft else None,
        trace=trace,
        userMessage=fail_msg,
        draftHasValidationIssues=has_draft,
    )
