"""
Story 5.4: Parity tests — backend vs frontend defaults resolution.
Compares resolve_definition_for_render_from_defaults (Python) with a Python simulation
of frontend resolveDefinitionForRender. Uses shared fixtures.
"""
import json
import pytest
from pathlib import Path

from modules.form_defaults.service import resolve_definition_for_render_from_defaults
from tests.parity_resolver_sim import resolve_definition_for_render_frontend_equiv


FIXTURES_PATH = Path(__file__).resolve().parent / "fixtures" / "parity_fixtures.json"


def _load_fixtures():
    with open(FIXTURES_PATH, encoding="utf-8") as f:
        return json.load(f)


def _build_form_definition(overrides: dict) -> dict:
    """Build a minimal form definition with theme, globalStyles, canvasSettings overrides."""
    return {
        "schemaVersion": 1,
        "pages": [],
        "theme": overrides.get("theme"),
        "globalStyles": overrides.get("globalStyles"),
        "canvasSettings": overrides.get("canvasSettings"),
    }


def _extract_resolved_fields(d: dict) -> dict:
    """Extract theme, globalStyles, canvasSettings for comparison."""
    return {
        "theme": d.get("theme"),
        "globalStyles": d.get("globalStyles"),
        "canvasSettings": d.get("canvasSettings"),
    }


class TestResolverParity:
    """Parity tests: backend and frontend merge logic produce identical output."""

    def test_parity_merged_defaults_and_form_overrides(self):
        """DC1: Backend and frontend produce identical theme, globalStyles, canvasSettings."""
        fixtures = _load_fixtures()
        merged = fixtures["merged_defaults_1"]
        overrides = fixtures["form_overrides_1"]
        form_def = _build_form_definition(overrides)

        backend_result = resolve_definition_for_render_from_defaults(merged, form_def)
        frontend_result = resolve_definition_for_render_frontend_equiv(merged, form_def)

        backend_fields = _extract_resolved_fields(backend_result)
        frontend_fields = _extract_resolved_fields(frontend_result)

        assert backend_fields == frontend_fields, (
            f"Parity mismatch:\nBackend:  {backend_fields}\nFrontend: {frontend_fields}"
        )

    def test_parity_second_fixture_set(self):
        """Parity with different fixture: partial overrides."""
        fixtures = _load_fixtures()
        merged = fixtures["merged_defaults_2"]
        overrides = fixtures["form_overrides_2"]
        form_def = _build_form_definition(overrides)

        backend_result = resolve_definition_for_render_from_defaults(merged, form_def)
        frontend_result = resolve_definition_for_render_frontend_equiv(merged, form_def)

        assert _extract_resolved_fields(backend_result) == _extract_resolved_fields(
            frontend_result
        )

    def test_parity_no_form_overrides(self):
        """Parity when form has no theme/globalStyles/canvasSettings overrides."""
        fixtures = _load_fixtures()
        merged = fixtures["merged_defaults_1"]
        form_def = _build_form_definition(fixtures["form_overrides_empty"])

        backend_result = resolve_definition_for_render_from_defaults(merged, form_def)
        frontend_result = resolve_definition_for_render_frontend_equiv(merged, form_def)

        assert _extract_resolved_fields(backend_result) == _extract_resolved_fields(
            frontend_result
        )

    def test_parity_null_form_theme_and_canvas(self):
        """Parity when form explicitly has null theme/canvasSettings (use defaults)."""
        fixtures = _load_fixtures()
        merged = fixtures["merged_defaults_1"]
        form_def = _build_form_definition(fixtures["form_overrides_null_theme"])

        backend_result = resolve_definition_for_render_from_defaults(merged, form_def)
        frontend_result = resolve_definition_for_render_frontend_equiv(merged, form_def)

        # Backend: form_theme is None -> use merged theme. form_canvas is None -> use merged canvasSettings.
        # Frontend: formTheme is null/undefined -> baseTheme. formCanvas null -> baseCanvas.
        assert _extract_resolved_fields(backend_result) == _extract_resolved_fields(
            frontend_result
        )

    def test_parity_empty_defaults(self):
        """Parity when merged defaults have empty theme/globalStyles/canvasSettings."""
        merged = {"theme": {}, "globalStyles": {}, "canvasSettings": {}}
        form_def = _build_form_definition(
            {"theme": {"primaryColor": "#123"}, "globalStyles": {}, "canvasSettings": {}}
        )

        backend_result = resolve_definition_for_render_from_defaults(merged, form_def)
        frontend_result = resolve_definition_for_render_frontend_equiv(merged, form_def)

        assert _extract_resolved_fields(backend_result) == _extract_resolved_fields(
            frontend_result
        )

    def test_parity_deep_merge_nested(self):
        """Parity for deeply nested structures (e.g. defaultGridLayoutsByComponent)."""
        merged = {
            "theme": {},
            "globalStyles": {
                "defaultGridLayoutsByComponent": {
                    "text": {"vertical": {"rows": 1}, "horizontal": {"rows": 2}},
                }
            },
            "canvasSettings": {},
        }
        form_def = _build_form_definition(
            {
                "theme": {},
                "globalStyles": {
                    "defaultGridLayoutsByComponent": {
                        "text": {"vertical": {"rows": 5}},
                    }
                },
                "canvasSettings": {},
            }
        )

        backend_result = resolve_definition_for_render_from_defaults(merged, form_def)
        frontend_result = resolve_definition_for_render_frontend_equiv(merged, form_def)

        assert _extract_resolved_fields(backend_result) == _extract_resolved_fields(
            frontend_result
        )
        # Verify partial override: text.vertical.rows=5, text.horizontal.rows=2 preserved
        dgl = backend_result.get("globalStyles", {}).get(
            "defaultGridLayoutsByComponent", {}
        )
        assert dgl.get("text", {}).get("vertical", {}).get("rows") == 5
        assert dgl.get("text", {}).get("horizontal", {}).get("rows") == 2


class TestParityFixturesExist:
    """DC2: Parity tests use shared fixtures."""

    def test_fixtures_file_exists(self):
        assert FIXTURES_PATH.exists(), f"Fixture file missing: {FIXTURES_PATH}"

    def test_fixtures_have_required_keys(self):
        fixtures = _load_fixtures()
        assert "merged_defaults_1" in fixtures
        assert "form_overrides_1" in fixtures
