"""Story 6.5c: resolve_allowed_components unit tests."""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from modules.form_builder.component_catalog import (
    ResolvedComponent,
    ResolvedComponentCatalog,
    resolve_allowed_components,
    width_classes_for,
)
from modules.form_builder.service import get_allowed_components


class _Row:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def test_width_classes_for_address_lookup_au_is_full():
    assert width_classes_for("address-lookup-au") == ["full"]


def test_resolve_allowed_components_country_scoped_row():
    db = MagicMock()
    db.execute.return_value.fetchall.return_value = [
        _Row(
            ComponentCode="text",
            DisplayName="Text",
            Category="input",
            SortOrder=1,
            PropertiesSchemaJSON=None,
            StructureJSON=None,
            DefaultGridLayoutVerticalJSON=None,
            DefaultGridLayoutHorizontalJSON=None,
            ValidationConfigJSON=None,
        ),
        _Row(
            ComponentCode="address-lookup-au",
            DisplayName="Address Lookup (AU)",
            Category="input",
            SortOrder=99,
            PropertiesSchemaJSON=None,
            StructureJSON=None,
            DefaultGridLayoutVerticalJSON=None,
            DefaultGridLayoutHorizontalJSON=None,
            ValidationConfigJSON=None,
        ),
    ]

    catalog = resolve_allowed_components(db, company_id=1, country_id=1)

    assert catalog.component_codes == ("text", "address-lookup-au")
    capability = catalog.to_capability_json()
    assert capability["resolvedCountryId"] == 1
    assert capability["resolvedCompanyId"] == 1
    assert any(row["type"] == "address-lookup-au" for row in capability["components"])


def test_get_allowed_components_delegates_to_resolver(monkeypatch):
    catalog = ResolvedComponentCatalog(
        company_id=7,
        country_id=2,
        components=(
            ResolvedComponent(
                component_code="email",
                display_name="Email",
                category="input",
                sort_order=1,
                properties_schema=None,
                structure=None,
                default_grid_layout_vertical=None,
                default_grid_layout_horizontal=None,
                validation_config=None,
            ),
        ),
    )
    monkeypatch.setattr(
        "modules.form_builder.service.resolve_allowed_components",
        lambda db, company_id, country_id, **kwargs: catalog,
    )
    db = MagicMock()
    result = get_allowed_components(db, company_id=7, country_id=2)
    assert result == [catalog.components[0].to_init_dict()]
