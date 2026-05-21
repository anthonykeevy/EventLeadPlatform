"""Story 6.5c AC-15: catalog alignment across resolver, init, Block F."""
from __future__ import annotations

from unittest.mock import MagicMock

from modules.form_ai.capability_prompt import build_capability_prompt_block_from_catalog
from modules.form_builder.component_catalog import (
    ResolvedComponent,
    ResolvedComponentCatalog,
    resolve_allowed_components,
)
from modules.form_builder.service import get_allowed_components
from modules.form_ai.semantic_validator import validate_semantic_plan
from modules.form_ai.schemas import FormSemanticPlan, SemanticComponentIntent


def _au_catalog() -> ResolvedComponentCatalog:
    return ResolvedComponentCatalog(
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
            ResolvedComponent(
                component_code="submit-button",
                display_name="Submit",
                category="input",
                sort_order=3,
                properties_schema=None,
                structure=None,
                default_grid_layout_vertical=None,
                default_grid_layout_horizontal=None,
                validation_config=None,
            ),
        ),
    )


def test_catalog_alignment_init_prompt_validator_codes_match(monkeypatch):
    catalog = _au_catalog()
    monkeypatch.setattr(
        "modules.form_builder.service.resolve_allowed_components",
        lambda db, company_id, country_id: catalog,
    )

    init_codes = {
        row["componentCode"]
        for row in get_allowed_components(MagicMock(), company_id=1, country_id=1)
    }
    resolver_codes = set(catalog.component_codes)
    block_f_text = build_capability_prompt_block_from_catalog(catalog)
    prompt_codes = {
        line.split()[1]
        for line in block_f_text.splitlines()
        if line.strip().startswith("- ")
    }
    capability_json = catalog.to_capability_json()
    plan = FormSemanticPlan(
        semanticPlanVersion="1.0",
        formId="contact",
        title="Contact",
        components=[
            SemanticComponentIntent(componentType="text", label="Name"),
            SemanticComponentIntent(componentType="email", label="Email"),
            SemanticComponentIntent(componentType="submit-button", label="Send"),
        ],
    )
    gate = validate_semantic_plan(
        plan,
        capability_snapshot_json=capability_json,
        validation_contracts=None,
    )

    assert init_codes == resolver_codes
    assert prompt_codes == resolver_codes
    assert gate.valid is True


def test_catalog_alignment_rejects_unknown_type_against_same_catalog():
    catalog = _au_catalog()
    plan = FormSemanticPlan(
        semanticPlanVersion="1.0",
        formId="contact",
        title="Contact",
        components=[
            SemanticComponentIntent(componentType="rating", label="Score"),
        ],
    )
    gate = validate_semantic_plan(
        plan,
        capability_snapshot_json=catalog.to_capability_json(),
        validation_contracts=None,
    )
    assert gate.valid is False
    assert gate.violations[0].code == "unknown-component-type"
