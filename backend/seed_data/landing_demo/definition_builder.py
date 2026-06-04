"""Build valid FormDefinition JSON for landing-page demo forms."""
from __future__ import annotations

from typing import Any
from uuid import uuid4


def _cid() -> str:
    return f"c-{uuid4().hex[:8]}"


def _theme(primary: str, background: str = "#FFFFFF", font: str = "Inter") -> dict[str, Any]:
    return {
        "primaryColor": primary,
        "backgroundColor": background,
        "fontFamily": font,
    }


def _base_canvas(width: int = 960, height: int = 1400) -> dict[str, Any]:
    return {
        "schemaVersion": "1.0",
        "formId": f"landing-demo-{uuid4().hex[:8]}",
        "theme": _theme("#0F766E"),
        "globalStyles": {
            "fontFamily": "Inter",
            "fontSize": 14,
            "fontWeight": 400,
            "labelFontFamily": "Inter",
            "defaultLayout": "vertical",
            "primaryColor": "#0F766E",
            "placeholderColor": "#9CA3AF",
            "backgroundColor": "#FFFFFF",
            "borderColor": "#D1D5DB",
            "errorColor": "#DC2626",
            "baseSpacing": 8,
            "labelGap": 1,
            "inputHelpGap": 0.5,
            "objectRowGapPx": 8,
            "objectColumnGapPx": 8,
            "dividerBorderColor": "#E5E7EB",
            "dividerBorderWidth": 1,
            "dividerWidth": "100%",
        },
        "canvasSettings": {
            "width": width,
            "height": height,
            "gridSize": 8,
            "backgroundColor": "#F8FAFC",
        },
        "logic": {"rules": []},
    }


def _comp(
    comp_type: str,
    *,
    label: str | None = None,
    props: dict[str, Any] | None = None,
    y: int,
    width: int = 880,
    height: int = 72,
) -> dict[str, Any]:
    merged: dict[str, Any] = dict(props or {})
    if label is not None:
        merged["label"] = label
    return {
        "id": _cid(),
        "type": comp_type,
        "props": merged,
        "position": {"x": 40, "y": y},
        "style": {"width": width, "height": height},
    }


def build_definition(components: list[dict[str, Any]], *, primary_color: str, form_id_suffix: str) -> dict[str, Any]:
    doc = _base_canvas()
    doc["formId"] = f"landing-demo-{form_id_suffix}"
    doc["theme"] = _theme(primary_color)
    doc["globalStyles"]["primaryColor"] = primary_color
    page = {"id": "page-1", "title": "Page 1", "components": components}
    doc["pages"] = [page]
    doc["desktopPages"] = [page]
    return doc


class VerticalLayout:
    """Simple y-stack for demo form components."""

    def __init__(self, start_y: int = 32, step: int = 84) -> None:
        self._y = start_y
        self._step = step

    def place(
        self,
        comp_type: str,
        *,
        label: str | None = None,
        props: dict[str, Any] | None = None,
        height: int = 72,
        width: int = 880,
    ) -> dict[str, Any]:
        comp = _comp(comp_type, label=label, props=props, y=self._y, height=height, width=width)
        self._y += max(height, self._step)
        return comp

    def header(self, text: str, *, height: int = 56) -> dict[str, Any]:
        return self.place("header", props={"text": text}, height=height)

    def paragraph(self, text: str, *, height: int = 96) -> dict[str, Any]:
        return self.place("paragraph", props={"text": text, "label": text}, height=height)

    def divider(self) -> dict[str, Any]:
        return self.place("divider", props={}, height=24)
