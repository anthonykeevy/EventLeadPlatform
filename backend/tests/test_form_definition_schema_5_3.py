"""
Story 5.3: Form Definition Schema Compatibility Tests
Validates DefinitionJSON structure; regression protection for builder output.
"""
import pytest
from pydantic import ValidationError

from schemas.form_definition import FormDefinition, FormPage, FormComponent, FormTheme, FormLogic


# Valid DefinitionJSON fixture (builder-like output)
VALID_DEFINITION = {
    "schemaVersion": "1.0",
    "formId": "form-123",
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
        "objectRowGapPx": 0,
        "objectColumnGapPx": 8,
        "dividerBorderColor": "#E5E7EB",
        "dividerBorderWidth": 1,
        "dividerWidth": "380px",
    },
    "canvasSettings": {
        "width": 1920,
        "height": 980,
        "gridSize": 8,
        "backgroundColor": "#f0f0f0",
    },
    "pages": [
        {
            "id": "page-1",
            "title": "Page 1",
            "components": [
                {
                    "id": "comp-1",
                    "type": "text",
                    "props": {"label": "Name", "placeholder": "Enter name"},
                },
                {
                    "id": "comp-2",
                    "type": "email",
                    "props": {"label": "Email", "required": True},
                },
            ],
            "background": {
                "type": "color",
                "value": "#FFFFFF",
            },
        },
    ],
    "desktopPages": [
        {
            "id": "page-1",
            "title": "Page 1",
            "components": [
                {"id": "comp-1", "type": "text", "props": {}},
                {"id": "comp-2", "type": "email", "props": {}},
            ],
        },
    ],
    "logic": {
        "rules": [
            {
                "id": "rule-1",
                "enabled": True,
                "when": {"sourceComponentId": "comp-1", "operator": "equals", "value": "yes"},
                "then": {"targetComponentId": "comp-2", "action": "show"},
            },
        ],
    },
}


class TestDefinitionJSONValid:
    """DC1: Valid DefinitionJSON passes validation."""

    def test_valid_full_structure_passes(self):
        result = FormDefinition.model_validate(VALID_DEFINITION)
        assert result.formId == "form-123"
        assert result.theme.primaryColor == "#0055FF"
        assert result.globalStyles is not None
        assert result.canvasSettings.width == 1920
        assert len(result.pages) == 1
        assert len(result.desktopPages) == 1
        assert result.pages[0].background is not None
        assert result.pages[0].background.type == "color"

    def test_valid_minimal_passes(self):
        minimal = {
            "schemaVersion": "1.0",
            "formId": "f1",
            "theme": {"primaryColor": "#000", "backgroundColor": "#fff", "fontFamily": "Arial"},
            "pages": [
                {"id": "p1", "title": "Page", "components": [{"id": "c1", "type": "text", "props": {}}]},
            ],
        }
        result = FormDefinition.model_validate(minimal)
        assert result.formId == "f1"
        assert len(result.pages[0].components) == 1


class TestDefinitionJSONInvalid:
    """DC1: Invalid structures rejected."""

    def test_missing_form_id_raises(self):
        bad = {**VALID_DEFINITION, "formId": ""}
        with pytest.raises(ValidationError) as exc_info:
            FormDefinition.model_validate(bad)
        err = str(exc_info.value).lower()
        assert "formid" in err or "min_length" in err or "at least 1" in err

    def test_missing_form_id_key_raises(self):
        bad = {k: v for k, v in VALID_DEFINITION.items() if k != "formId"}
        with pytest.raises(ValidationError):
            FormDefinition.model_validate(bad)

    def test_unknown_top_level_key_rejected(self):
        bad = {**VALID_DEFINITION, "unknownKey": "x"}
        with pytest.raises(ValidationError):
            FormDefinition.model_validate(bad)


class TestDuplicateComponentIds:
    """DC4: Duplicate component IDs rejected."""

    def test_duplicate_ids_same_page_rejected(self):
        dup = {
            **VALID_DEFINITION,
            "pages": [
                {
                    "id": "p1",
                    "title": "Page",
                    "components": [
                        {"id": "dup-id", "type": "text", "props": {}},
                        {"id": "dup-id", "type": "email", "props": {}},
                    ],
                },
            ],
            "desktopPages": None,
            "tabletPages": None,
            "mobilePages": None,
            "logic": None,
        }
        with pytest.raises(ValidationError) as exc_info:
            FormDefinition.model_validate(dup)
        assert "Duplicate" in str(exc_info.value)

    def test_duplicate_ids_across_pages_rejected(self):
        dup = {
            **VALID_DEFINITION,
            "pages": [
                {"id": "p1", "title": "P1", "components": [{"id": "c1", "type": "text", "props": {}}]},
                {"id": "p2", "title": "P2", "components": [{"id": "c1", "type": "text", "props": {}}]},
            ],
            "desktopPages": None,
            "tabletPages": None,
            "mobilePages": None,
            "logic": None,
        }
        with pytest.raises(ValidationError) as exc_info:
            FormDefinition.model_validate(dup)
        assert "Duplicate" in str(exc_info.value)


class TestLogicRuleIntegrity:
    """DC4: Logic rule sourceComponentId != targetComponentId."""

    def test_source_equals_target_rejected(self):
        # Use unique component IDs to avoid duplicate-id check; only logic rule fails
        bad_logic = {
            "schemaVersion": "1.0",
            "formId": "f1",
            "theme": {"primaryColor": "#000", "backgroundColor": "#fff", "fontFamily": "Arial"},
            "pages": [
                {
                    "id": "p1",
                    "title": "P",
                    "components": [
                        {"id": "c1", "type": "text", "props": {}},
                        {"id": "c2", "type": "email", "props": {}},
                    ],
                },
            ],
            "logic": {
                "rules": [
                    {
                        "id": "r1",
                        "enabled": True,
                        "when": {"sourceComponentId": "c1", "operator": "equals", "value": "x"},
                        "then": {"targetComponentId": "c1", "action": "show"},  # source === target
                    },
                ],
                },
        }
        with pytest.raises(ValidationError) as exc_info:
            FormDefinition.model_validate(bad_logic)
        err = str(exc_info.value).lower()
        assert "sourcecomponentid" in err or "target" in err or "cannot equal" in err


class TestSchemaVersion:
    """DC2: schemaVersion validated."""

    def test_schema_version_1_0_accepted(self):
        minimal = {
            "schemaVersion": "1.0",
            "formId": "f1",
            "theme": {"primaryColor": "#000", "backgroundColor": "#fff", "fontFamily": "Arial"},
            "pages": [{"id": "p1", "title": "P", "components": [{"id": "c1", "type": "text", "props": {}}]}],
        }
        result = FormDefinition.model_validate(minimal)
        assert result.schemaVersion == "1.0"

    def test_schema_version_invalid_rejected(self):
        bad = {**VALID_DEFINITION, "schemaVersion": "2.0"}
        with pytest.raises(ValidationError):
            FormDefinition.model_validate(bad)


class TestRegressionProtection:
    """DC3: Regression protection - builder output must pass."""

    def test_builder_representative_fixture_passes(self):
        """Representative builder output structure validates."""
        FormDefinition.model_validate(VALID_DEFINITION)


