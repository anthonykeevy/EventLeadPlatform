from __future__ import annotations

from itertools import combinations
from typing import Any, Dict, Iterable, List, Tuple

from pydantic import ValidationError

from schemas.form_definition import FormComponent, FormDefinition, FormPage

from .schemas import (
    BoundaryViolation,
    CollisionViolation,
    FormValidationResponse,
    SchemaError,
    ValidationSummary,
)


DEFAULT_CANVAS_WIDTH = 1920.0
DEFAULT_CANVAS_HEIGHT = 980.0


DEFAULT_HEIGHT_BY_TYPE: Dict[str, float] = {
    "divider": 20.0,
    "header": 40.0,
    "submit-button": 60.0,
    "first-name": 100.0,
    "text": 100.0,
    "email": 100.0,
    "phone": 100.0,
    "number": 100.0,
    "date": 100.0,
    "dropdown": 200.0,
    "checkbox": 60.0,
    "radio": 80.0,
    "textarea": 150.0,
    "address": 100.0,
    "terms": 60.0,
    "file-upload": 120.0,
}

# Builder vertical fields often render label + validation below `style.height` suggests.
# Without this, deterministic collision checks underestimate tall fields (e.g. textarea vs submit).
_TEXTAREA_COLLISION_EXTRA = 60.0


def _error_path(loc: Iterable[Any]) -> str:
    return ".".join(str(item) for item in loc) if loc else "root"


def _parse_dimension(value: Any, fallback: float) -> float:
    if isinstance(value, (int, float)):
        return float(value) if float(value) > 0 else fallback
    if isinstance(value, str):
        cleaned = value.strip().lower()
        if cleaned.endswith("px"):
            cleaned = cleaned[:-2]
        try:
            parsed = float(cleaned)
            return parsed if parsed > 0 else fallback
        except ValueError:
            return fallback
    return fallback


def _inflate_height_for_collision(component_type: str, height: float) -> float:
    if component_type == "textarea":
        return max(height, 140.0) + _TEXTAREA_COLLISION_EXTRA
    return height


def _component_size(component: FormComponent) -> Tuple[float, float]:
    style_w = component.style.width if component.style else None
    style_h = component.style.height if component.style else None
    props = component.props
    props_w = getattr(props, "width", None) if props else None
    props_h = getattr(props, "height", None) if props else None

    fallback_width = 300.0
    fallback_height = DEFAULT_HEIGHT_BY_TYPE.get(component.type, 100.0)

    parsed_sw = _parse_dimension(style_w, 0.0)
    parsed_pw = _parse_dimension(props_w, 0.0)
    parsed_sh = _parse_dimension(style_h, 0.0)
    parsed_ph = _parse_dimension(props_h, 0.0)

    # Width: prefer authored `style.width`, then props (do not max both — stale props can be full-bleed).
    if parsed_sw > 0:
        width = parsed_sw
    elif parsed_pw > 0:
        width = parsed_pw
    else:
        width = fallback_width

    # Height: max of style vs props catches builder sync drift; inflate textarea for label/validation chrome.
    height = max(parsed_sh, parsed_ph)
    if height <= 0:
        height = fallback_height
    height = _inflate_height_for_collision(component.type, height)

    return width, height


def _flatten_components(
    components: List[FormComponent], page_id: str, layout: str
) -> List[Dict[str, Any]]:
    flattened: List[Dict[str, Any]] = []

    def walk(items: List[FormComponent]) -> None:
        for comp in items:
            if comp.position is not None:
                width, height = _component_size(comp)
                flattened.append(
                    {
                        "componentId": comp.id,
                        "pageId": page_id,
                        "layout": layout,
                        "x": float(comp.position.x),
                        "y": float(comp.position.y),
                        "width": width,
                        "height": height,
                    }
                )
            if comp.children:
                walk(comp.children)

    walk(components)
    return flattened


def _pages_for_layout(definition: FormDefinition, layout: str) -> List[FormPage]:
    if layout == "pages":
        return definition.pages
    if layout == "desktopPages":
        return definition.desktopPages or []
    if layout == "tabletPages":
        return definition.tabletPages or []
    if layout == "mobilePages":
        return definition.mobilePages or []
    return []


def _collect_boundary_violations(
    items: List[Dict[str, Any]], canvas_width: float, canvas_height: float
) -> List[BoundaryViolation]:
    violations: List[BoundaryViolation] = []
    for item in items:
        left = item["x"] < 0
        top = item["y"] < 0
        right = item["x"] + item["width"] > canvas_width
        bottom = item["y"] + item["height"] > canvas_height

        if left or right or top or bottom:
            violations.append(
                BoundaryViolation(
                    componentId=item["componentId"],
                    pageId=item["pageId"],
                    layout=item["layout"],
                    position={"x": item["x"], "y": item["y"]},
                    size={"width": item["width"], "height": item["height"]},
                    canvas={"width": canvas_width, "height": canvas_height},
                    violations={
                        "left": left,
                        "right": right,
                        "top": top,
                        "bottom": bottom,
                    },
                )
            )

    violations.sort(key=lambda v: (v.layout, v.pageId, v.componentId))
    return violations


def _overlap_area(a: Dict[str, Any], b: Dict[str, Any]) -> float:
    left = max(a["x"], b["x"])
    right = min(a["x"] + a["width"], b["x"] + b["width"])
    top = max(a["y"], b["y"])
    bottom = min(a["y"] + a["height"], b["y"] + b["height"])

    if right <= left or bottom <= top:
        return 0.0
    return float((right - left) * (bottom - top))


def _collect_collisions(items: List[Dict[str, Any]]) -> List[CollisionViolation]:
    collisions: List[CollisionViolation] = []

    grouped: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
    for item in items:
        key = (item["layout"], item["pageId"])
        grouped.setdefault(key, []).append(item)

    for (layout, page_id), group_items in grouped.items():
        sorted_items = sorted(group_items, key=lambda i: i["componentId"])
        for left_item, right_item in combinations(sorted_items, 2):
            overlap = _overlap_area(left_item, right_item)
            if overlap > 0:
                collisions.append(
                    CollisionViolation(
                        componentAId=left_item["componentId"],
                        componentBId=right_item["componentId"],
                        pageId=page_id,
                        layout=layout,
                        overlapArea=overlap,
                    )
                )

    collisions.sort(key=lambda c: (c.layout, c.pageId, c.componentAId, c.componentBId))
    return collisions


def validate_definition_payload(payload: Dict[str, Any]) -> FormValidationResponse:
    definition_candidate: Any = payload.get("definition", payload)
    if not isinstance(definition_candidate, dict):
        schema_errors = [
            SchemaError(
                path="definition",
                message="definition must be a JSON object",
                code="type_error.object",
            )
        ]
        return FormValidationResponse(
            valid=False,
            schemaErrors=schema_errors,
            boundaryViolations=[],
            collisions=[],
            summary=ValidationSummary(errorCount=len(schema_errors), warningCount=0),
            meta={"deterministic": True},
        )

    try:
        definition = FormDefinition.model_validate(definition_candidate)
    except ValidationError as exc:
        schema_errors = [
            SchemaError(path=_error_path(err["loc"]), message=err["msg"], code=err["type"])
            for err in exc.errors()
        ]
        schema_errors.sort(key=lambda err: (err.path, err.code, err.message))
        return FormValidationResponse(
            valid=False,
            schemaErrors=schema_errors,
            boundaryViolations=[],
            collisions=[],
            summary=ValidationSummary(errorCount=len(schema_errors), warningCount=0),
            meta={"deterministic": True},
        )

    canvas_width = float(definition.canvasSettings.width) if definition.canvasSettings else DEFAULT_CANVAS_WIDTH
    canvas_height = float(definition.canvasSettings.height) if definition.canvasSettings else DEFAULT_CANVAS_HEIGHT

    flattened: List[Dict[str, Any]] = []
    for layout_name in ("pages", "desktopPages", "tabletPages", "mobilePages"):
        for page in _pages_for_layout(definition, layout_name):
            flattened.extend(_flatten_components(page.components, page.id, layout_name))

    boundary_violations = _collect_boundary_violations(flattened, canvas_width, canvas_height)
    collisions = _collect_collisions(flattened)
    error_count = len(boundary_violations) + len(collisions)

    return FormValidationResponse(
        valid=error_count == 0,
        schemaErrors=[],
        boundaryViolations=boundary_violations,
        collisions=collisions,
        summary=ValidationSummary(errorCount=error_count, warningCount=0),
        meta={"deterministic": True},
    )
