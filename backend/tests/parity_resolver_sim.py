"""
Story 5.4: Python simulation of frontend resolveDefinitionForRender / deepMerge.
Used by parity tests to compare backend output with frontend logic without invoking Node.
Logic must stay in sync with frontend/src/features/builder/utils/definitionResolver.ts
"""
from typing import Any, Dict


def _deep_merge_ts_style(
    base: Dict[str, Any], override: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Mirror of TypeScript deepMerge: override recursively overrides base.
    Nested dicts merged; arrays and scalars replaced.
    Uses object/!Array checks like TS.
    """
    result = dict(base)
    for key, override_val in override.items():
        base_val = result.get(key)
        if (
            base_val is not None
            and override_val is not None
            and isinstance(base_val, dict)
            and not isinstance(base_val, list)
            and isinstance(override_val, dict)
            and not isinstance(override_val, list)
        ):
            result[key] = _deep_merge_ts_style(base_val, override_val)
        else:
            result[key] = override_val
    return result


def resolve_definition_for_render_frontend_equiv(
    defaults: Dict[str, Any] | None,
    form_definition: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Python equivalent of frontend resolveDefinitionForRender.
    If defaults is None, return form_definition as-is (matches TS).
    """
    if defaults is None:
        return dict(form_definition)

    result = dict(form_definition)

    base_theme: Dict[str, Any] = (
        defaults["theme"] if isinstance(defaults.get("theme"), dict) else {}
    )
    form_theme = form_definition.get("theme")
    result["theme"] = (
        _deep_merge_ts_style(base_theme, form_theme)
        if form_theme is not None and isinstance(form_theme, dict)
        else base_theme
    )

    base_gs: Dict[str, Any] = (
        defaults["globalStyles"]
        if isinstance(defaults.get("globalStyles"), dict)
        else {}
    )
    form_gs = form_definition.get("globalStyles")
    result["globalStyles"] = (
        _deep_merge_ts_style(base_gs, form_gs)
        if form_gs is not None and isinstance(form_gs, dict)
        else base_gs
    )

    base_canvas: Dict[str, Any] = (
        defaults["canvasSettings"]
        if isinstance(defaults.get("canvasSettings"), dict)
        else {}
    )
    form_canvas = form_definition.get("canvasSettings")
    result["canvasSettings"] = (
        _deep_merge_ts_style(base_canvas, form_canvas)
        if form_canvas is not None and isinstance(form_canvas, dict)
        else base_canvas
    )

    return result
