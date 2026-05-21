"""Story 6.5c: DynamicComponentCatalog renderer tests."""
from modules.form_ai.prompt_assembly.renderer import render_prompt_assembly
from modules.form_ai.prompt_assembly.resolver import ResolvedAssembly, ResolvedSection
from modules.form_builder.component_catalog import (
    ResolvedComponent,
    ResolvedComponentCatalog,
)


def _catalog() -> ResolvedComponentCatalog:
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
        ),
    )


def test_renderer_hydrates_block_f_and_appends_allowed_types_to_block_a():
    resolved = ResolvedAssembly(
        registry_code="FORM_AI_V1",
        registry_id=1,
        registry_version_id=1,
        version_number=1,
        sections=[
            ResolvedSection(
                section_code="A",
                section_id=1,
                sort_order=10,
                data_structure_type="Prose",
                heading=None,
                variant_id=1,
                variant_code="DEFAULT",
                snippet="Block A prose.",
            ),
            ResolvedSection(
                section_code="F",
                section_id=2,
                sort_order=35,
                data_structure_type="DynamicComponentCatalog",
                heading=None,
                variant_id=2,
                variant_code="DEFAULT",
                snippet="Shell reminder text.",
            ),
        ],
    )

    rendered = render_prompt_assembly(resolved, component_catalog=_catalog())

    assert "ALLOWED COMPONENT TYPES" in rendered["F"]
    assert "text (allowed widthIntent hints:" in rendered["F"]
    assert "Shell reminder text." in rendered["F"]
    assert "ALLOWED componentType values" in rendered["A"]
    assert "text" in rendered["A"]
