"""Blank builder canvas + pre-loaded AI prompt (matches createEmptyFormDefinition)."""
from __future__ import annotations

import json
from typing import Any


def build_blank_definition_with_prompt(form_id: int, prompt: str) -> str:
    """Return DefinitionJSON string for an empty canvas with aiAgentSettings.lastPrompt set."""
    definition: dict[str, Any] = {
        "schemaVersion": "1.0",
        "formId": str(form_id),
        "theme": {
            "primaryColor": "#0055FF",
            "backgroundColor": "#FFFFFF",
            "fontFamily": "Inter",
        },
        "globalStyles": {
            "fontFamily": "Inter",
            "fontSize": 14,
            "fontWeight": 400,
            "labelFontFamily": "Inter",
            "defaultLayout": "vertical",
            "primaryColor": "#0055FF",
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
        "logic": {"rules": []},
        "canvasSettings": {
            "width": 1920,
            "height": 980,
            "gridSize": 8,
        },
        "pages": [
            {
                "id": "page-1",
                "title": "Page 1",
                "components": [],
            }
        ],
        "aiAgentSettings": {
            "lastPrompt": prompt,
            "includeEventInformation": True,
        },
    }
    return json.dumps(definition, ensure_ascii=False)
