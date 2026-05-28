"""Renderer for the Story 6.5b+ Prompt Assembly Registry.

Hydrates a :class:`ResolvedAssembly` into a per-section dict of strings
ready for ``_build_initial_messages`` to splice into the system body.

Story 6.5b: ``DataStructureType = 'Prose'`` only.
Story 6.5c: ``DynamicComponentCatalog`` for Block F (prose shell + injected
catalog list) and allowed-type fragments appended to Blocks A / I.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Mapping, Optional

from modules.form_builder.component_catalog import ResolvedComponentCatalog
from modules.form_ai.capability_prompt import build_capability_prompt_block_from_catalog
from modules.reference.clarification import ResolvedClarificationContext

from .resolver import ResolvedAssembly, ResolvedSection


_PLACEHOLDER_SECTIONS = {
    ("C", "heritage"): {"heritageOrigin"},
}

_SECTIONS_WITH_ALLOWED_TYPES_FRAGMENT = frozenset({"A", "I"})


class _SafeFormatDict(dict):
    """``str.format_map`` helper that leaves unknown placeholders untouched."""

    def __missing__(self, key):  # type: ignore[override]
        return "{" + key + "}"


@dataclass(frozen=True)
class RenderedAssembly:
    """Renderer output: per-block hydrated strings + audit IDs."""

    registry_code: str
    registry_version_id: int
    version_number: int
    sections: Dict[str, str]
    variant_ids: Dict[str, int]

    def __getitem__(self, section_code: str) -> str:
        return self.sections[section_code]

    def get(self, section_code: str, default: str = "") -> str:
        return self.sections.get(section_code, default)


def _hydrate_dynamic_component_catalog(
    section: ResolvedSection,
    catalog: ResolvedComponentCatalog,
) -> str:
    dynamic_list = build_capability_prompt_block_from_catalog(catalog)
    shell = section.snippet.strip()
    if not shell:
        return dynamic_list
    if not dynamic_list:
        return shell
    return f"{dynamic_list}\n\n{shell}"


def _hydrate_refs_section(
    section: ResolvedSection,
    clarification: ResolvedClarificationContext,
) -> str:
    heading = (section.heading or "").strip()
    if section.section_code == "E1":
        body = clarification.e1_summary
    elif section.section_code == "E2":
        body = clarification.e2_hint
    elif section.section_code == "E3":
        body = clarification.e3_hint
    else:
        body = section.snippet.strip()
    if heading and body:
        return f"## {heading}\n{body}"
    if body:
        return body
    return heading


def _hydrate_section(
    section: ResolvedSection,
    placeholders: Mapping[str, str],
    *,
    component_catalog: Optional[ResolvedComponentCatalog] = None,
    clarification: Optional[ResolvedClarificationContext] = None,
) -> str:
    if section.data_structure_type == "Refs":
        if clarification is None:
            raise RuntimeError(
                f"PromptSection {section.section_code!r} requires Refs hydration "
                "but no clarification context was supplied."
            )
        return _hydrate_refs_section(section, clarification)

    if section.data_structure_type == "DynamicComponentCatalog":
        if component_catalog is None:
            raise RuntimeError(
                f"PromptSection {section.section_code!r} requires "
                "DynamicComponentCatalog hydration but no component_catalog "
                "was supplied."
            )
        return _hydrate_dynamic_component_catalog(section, component_catalog)

    if section.data_structure_type != "Prose":
        raise NotImplementedError(
            f"PromptSection.DataStructureType={section.data_structure_type!r} "
            f"is not supported (SectionCode={section.section_code!r})."
        )

    snippet = section.snippet
    placeholder_keys = _PLACEHOLDER_SECTIONS.get(
        (section.section_code, section.variant_code)
    )
    if placeholder_keys:
        filtered = {
            key: placeholders.get(key, "") for key in placeholder_keys
        }
        snippet = snippet.format_map(_SafeFormatDict(filtered))

    if (
        component_catalog is not None
        and section.section_code in _SECTIONS_WITH_ALLOWED_TYPES_FRAGMENT
        and component_catalog.components
    ):
        snippet = snippet.rstrip() + "\n\n" + component_catalog.format_allowed_types_fragment()

    return snippet


def render_prompt_assembly(
    resolved: ResolvedAssembly,
    *,
    placeholders: Optional[Mapping[str, str]] = None,
    component_catalog: Optional[ResolvedComponentCatalog] = None,
    clarification: Optional[ResolvedClarificationContext] = None,
) -> RenderedAssembly:
    """Hydrate a resolved assembly into a per-block dict of strings."""
    effective_placeholders: Mapping[str, str] = placeholders or {}

    rendered_map: Dict[str, str] = {}
    variant_ids: Dict[str, int] = {}

    for section in resolved.sections:
        rendered_map[section.section_code] = _hydrate_section(
            section,
            effective_placeholders,
            component_catalog=component_catalog,
            clarification=clarification,
        )
        variant_ids[section.section_code] = section.variant_id

    return RenderedAssembly(
        registry_code=resolved.registry_code,
        registry_version_id=resolved.registry_version_id,
        version_number=resolved.version_number,
        sections=rendered_map,
        variant_ids=variant_ids,
    )
