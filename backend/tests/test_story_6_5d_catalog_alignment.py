"""Story 6.5d: offline filter excludes RequiresNetwork components."""
from __future__ import annotations

from unittest.mock import MagicMock

from modules.form_builder.component_catalog import (
    ResolvedComponent,
    ResolvedComponentCatalog,
    resolve_allowed_components,
)


class _Row:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def test_resolve_allowed_components_offline_excludes_network_types(monkeypatch):
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
            ComponentCode="address",
            DisplayName="Address",
            Category="input",
            SortOrder=2,
            PropertiesSchemaJSON=None,
            StructureJSON=None,
            DefaultGridLayoutVerticalJSON=None,
            DefaultGridLayoutHorizontalJSON=None,
            ValidationConfigJSON=None,
        ),
    ]

    catalog = resolve_allowed_components(
        db, company_id=1, country_id=1, requires_offline_capable=True
    )
    assert catalog.component_codes == ("text", "address")
    assert "address-lookup-au" not in catalog.component_codes


def test_catalog_alignment_init_matches_resolver(monkeypatch):
    catalog = ResolvedComponentCatalog(
        company_id=1,
        country_id=1,
        components=(
            ResolvedComponent(
                component_code="text",
                display_name="Text",
                category="input",
                sort_order=1,
                properties_schema=None,
                structure=None,
                default_grid_layout_vertical=None,
                default_grid_layout_horizontal=None,
                validation_config=None,
            ),
            ResolvedComponent(
                component_code="email",
                display_name="Email",
                category="input",
                sort_order=2,
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
        lambda *args, **kwargs: catalog,
    )
    from modules.form_builder.service import get_allowed_components

    init_codes = {
        row["componentCode"]
        for row in get_allowed_components(MagicMock(), company_id=1, country_id=1)
    }
    assert init_codes == set(catalog.component_codes)
