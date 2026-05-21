"""Capability prompt block helpers shared by Form AI and the registry renderer."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from modules.form_builder.component_catalog import ResolvedComponentCatalog


def capability_type_summary(
    capability_json: Optional[Dict[str, Any]],
) -> List[Tuple[str, List[str]]]:
    """Return [(componentType, [allowed width classes])] from capability JSON."""
    if not isinstance(capability_json, dict):
        return []
    components = capability_json.get("components")
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


def build_capability_prompt_block(
    capability_json: Optional[Dict[str, Any]],
    *,
    header: str = (
        "ALLOWED COMPONENT TYPES (catalog-authoritative; do NOT invent others):"
    ),
    footer: str = (
        "If the user asks for a feature that isn't in this list "
        "(e.g. signature capture, payment collection), use the closest registered type "
        "and put a brief explanation in helpText."
    ),
) -> str:
    """Render the Block F capability list from resolved catalog JSON."""
    summary = capability_type_summary(capability_json)
    if not summary:
        return ""
    lines = [header]
    for component_type, widths in summary:
        if widths:
            lines.append(
                f"  - {component_type} (allowed widthIntent hints: {', '.join(widths)})"
            )
        else:
            lines.append(f"  - {component_type}")
    lines.append(footer)
    return "\n".join(lines)


def build_capability_prompt_block_from_catalog(
    catalog: Optional[ResolvedComponentCatalog],
) -> str:
    if catalog is None or not catalog.components:
        return ""
    return build_capability_prompt_block(catalog.to_capability_json())
