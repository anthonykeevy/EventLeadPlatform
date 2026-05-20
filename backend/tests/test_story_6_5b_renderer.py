"""Story 6.5b - renderer behaviour tests.

Renderer is pure (no DB). Tests build ``ResolvedAssembly`` /
``ResolvedSection`` instances directly and exercise:

  * Verbatim ``Prose`` hydration (Block A / G with no placeholders).
  * ``{heritageOrigin}`` substitution for Block C heritage variant only.
  * Unrelated braces in other sections (e.g. Block I ``{label,value}``)
    are left untouched.
  * Unknown ``DataStructureType`` raises ``NotImplementedError``.
  * ``RenderedAssembly.variant_ids`` mirrors the resolved variants.
"""

from __future__ import annotations

import pytest

from modules.form_ai.prompt_assembly.renderer import (
    RenderedAssembly,
    render_prompt_assembly,
)
from modules.form_ai.prompt_assembly.resolver import (
    REGISTRY_CODE_FORM_AI_V1,
    ResolvedAssembly,
    ResolvedSection,
)


def _make_resolved(*sections: ResolvedSection) -> ResolvedAssembly:
    return ResolvedAssembly(
        registry_code=REGISTRY_CODE_FORM_AI_V1,
        registry_id=1,
        registry_version_id=42,
        version_number=1,
        sections=list(sections),
    )


def _section(
    code: str,
    *,
    sort_order: int,
    snippet: str,
    variant_code: str = "DEFAULT",
    variant_id: int = 100,
    data_structure_type: str = "Prose",
) -> ResolvedSection:
    return ResolvedSection(
        section_code=code,
        section_id=10,
        sort_order=sort_order,
        data_structure_type=data_structure_type,
        heading=None,
        variant_id=variant_id,
        variant_code=variant_code,
        snippet=snippet,
    )


def test_renderer_hydrates_prose_verbatim_when_no_placeholders():
    snippet = "Block A literal\nwith multiple lines\n"
    resolved = _make_resolved(_section("A", sort_order=10, snippet=snippet))

    rendered = render_prompt_assembly(resolved)

    assert rendered["A"] == snippet
    assert rendered.sections == {"A": snippet}


def test_renderer_substitutes_heritage_origin_in_block_c_heritage_variant():
    snippet = (
        "Brand posture: heritage. Audience locale still controls field shape "
        "and compliance; copy voice may lightly reflect {heritageOrigin} brand heritage."
    )
    resolved = _make_resolved(
        _section(
            "C",
            sort_order=50,
            snippet=snippet,
            variant_code="heritage",
            variant_id=222,
        )
    )

    rendered = render_prompt_assembly(
        resolved,
        placeholders={"heritageOrigin": "Australia"},
    )

    assert "{heritageOrigin}" not in rendered["C"]
    assert "Australia brand heritage" in rendered["C"]


def test_renderer_does_not_substitute_block_c_local_variant():
    """Block C local variant has no placeholder; the placeholder dict
    must not bleed into other variants even when keys collide."""
    snippet = "Brand posture: local. Match copy voice to the resolved audience locale."
    resolved = _make_resolved(
        _section(
            "C",
            sort_order=50,
            snippet=snippet,
            variant_code="local",
            variant_id=111,
        )
    )

    rendered = render_prompt_assembly(
        resolved,
        placeholders={"heritageOrigin": "ShouldNotAppear"},
    )

    assert rendered["C"] == snippet


def test_renderer_leaves_unrelated_braces_untouched_in_other_sections():
    """Block I and Block G contain JSON examples and ``{label,value}``
    fragments that must not be format_map'd. The renderer narrows
    placeholder substitution to specific (section, variant) pairs."""
    block_i_snippet = (
        '  - options: array of {label,value} for dropdown/radio,\n'
        '    Example: "validationIntent": { "required": true }.\n'
    )
    block_g_snippet = '{"componentType": "text"}'
    resolved = _make_resolved(
        _section("I", sort_order=30, snippet=block_i_snippet),
        _section("G", sort_order=40, snippet=block_g_snippet),
    )

    rendered = render_prompt_assembly(
        resolved,
        placeholders={"heritageOrigin": "AU"},
    )

    assert rendered["I"] == block_i_snippet
    assert rendered["G"] == block_g_snippet


def test_renderer_preserves_section_order_from_resolver():
    resolved = _make_resolved(
        _section("A", sort_order=10, snippet="A"),
        _section("B", sort_order=20, snippet="B"),
        _section("I", sort_order=30, snippet="I"),
        _section("G", sort_order=40, snippet="G"),
        _section("C", sort_order=50, snippet="C"),
    )

    rendered = render_prompt_assembly(resolved)

    assert list(rendered.sections.keys()) == ["A", "B", "I", "G", "C"]


def test_renderer_records_variant_ids_for_audit():
    resolved = _make_resolved(
        _section("A", sort_order=10, snippet="A", variant_id=11),
        _section("C", sort_order=50, snippet="C", variant_code="local", variant_id=22),
    )

    rendered = render_prompt_assembly(resolved)

    assert rendered.variant_ids == {"A": 11, "C": 22}
    assert rendered.registry_version_id == 42
    assert rendered.version_number == 1


def test_renderer_raises_for_unsupported_data_structure_type():
    """``Json`` / ``Snapshot`` / ``Refs`` are reserved for 6.5c / 6.5d."""
    resolved = _make_resolved(
        _section(
            "F",
            sort_order=25,
            snippet="ignored",
            data_structure_type="Snapshot",
        )
    )

    with pytest.raises(NotImplementedError):
        render_prompt_assembly(resolved)


def test_renderer_returns_rendered_assembly_dataclass():
    resolved = _make_resolved(_section("A", sort_order=10, snippet="A-text"))

    rendered = render_prompt_assembly(resolved)

    assert isinstance(rendered, RenderedAssembly)
    assert rendered.get("A") == "A-text"
    assert rendered.get("does-not-exist", "fallback") == "fallback"
