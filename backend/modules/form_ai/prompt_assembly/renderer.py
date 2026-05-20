"""Renderer for the Story 6.5b Prompt Assembly Registry.

Hydrates a :class:`ResolvedAssembly` into a per-section dict of strings
ready for ``_build_initial_messages`` to splice into the system body.

Only ``DataStructureType = 'Prose'`` is supported in 6.5b. Other
structure types raise :class:`NotImplementedError` so 6.5c / 6.5d
diagnose missing renderer support cleanly.

Block C ``heritage`` variant uses a ``{heritageOrigin}`` placeholder
that the renderer substitutes via ``str.format_map``. A safe-dict shim
keeps unrelated braces in other snippets (e.g. JSON examples in Block
G, ``{label,value}`` in Block I) untouched.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Mapping, Optional

from .resolver import ResolvedAssembly, ResolvedSection


# Sections that are eligible for placeholder substitution. Limiting the
# substitution scope keeps incidental braces in other blocks (Block G
# JSON examples, Block I ``{label,value}``) from triggering format_map
# lookups.
_PLACEHOLDER_SECTIONS = {
    ("C", "heritage"): {"heritageOrigin"},
}


class _SafeFormatDict(dict):
    """``str.format_map`` helper that leaves unknown placeholders untouched.

    e.g. ``"{heritageOrigin} text".format_map(_SafeFormatDict({"heritageOrigin": "AU"}))``
    returns ``"AU text"``; ``"{unrelated}".format_map(...)`` returns
    ``"{unrelated}"`` rather than raising.
    """

    def __missing__(self, key):  # type: ignore[override]
        return "{" + key + "}"


@dataclass(frozen=True)
class RenderedAssembly:
    """Renderer output: per-block hydrated strings + audit IDs."""

    registry_code: str
    registry_version_id: int
    version_number: int
    sections: Dict[str, str]  # SectionCode -> rendered_string
    variant_ids: Dict[str, int]  # SectionCode -> PromptSectionVariantID

    def __getitem__(self, section_code: str) -> str:
        return self.sections[section_code]

    def get(self, section_code: str, default: str = "") -> str:
        return self.sections.get(section_code, default)


def _hydrate_section(
    section: ResolvedSection,
    placeholders: Mapping[str, str],
) -> str:
    if section.data_structure_type != "Prose":
        raise NotImplementedError(
            f"PromptSection.DataStructureType={section.data_structure_type!r} "
            f"is not supported by Story 6.5b's renderer (SectionCode="
            f"{section.section_code!r}). DataStructureTypes other than "
            "'Prose' are reserved for Story 6.5c / 6.5d."
        )

    snippet = section.snippet
    placeholder_keys = _PLACEHOLDER_SECTIONS.get(
        (section.section_code, section.variant_code)
    )
    if not placeholder_keys:
        return snippet

    # Filter placeholders to the keys this section is allowed to read.
    filtered = {
        key: placeholders.get(key, "") for key in placeholder_keys
    }
    return snippet.format_map(_SafeFormatDict(filtered))


def render_prompt_assembly(
    resolved: ResolvedAssembly,
    *,
    placeholders: Optional[Mapping[str, str]] = None,
) -> RenderedAssembly:
    """Hydrate a resolved assembly into a per-block dict of strings.

    Args:
      resolved: Output of :func:`resolve_prompt_assembly`.
      placeholders: Optional mapping of placeholder -> value used by
        sections eligible for placeholder substitution
        (currently Block C ``heritage`` only). Missing keys are
        substituted as the empty string.

    Returns:
      RenderedAssembly with per-section strings keyed by SectionCode.
      Section iteration order follows the resolver's SortOrder; callers
      that need the full assembled string can ``"".join(...)`` over
      ``rendered.sections.values()``.
    """
    effective_placeholders: Mapping[str, str] = placeholders or {}

    # Use insertion-ordered dict so callers iterating sections.values() see
    # SortOrder.
    rendered_map: Dict[str, str] = {}
    variant_ids: Dict[str, int] = {}

    for section in resolved.sections:
        rendered_map[section.section_code] = _hydrate_section(
            section, effective_placeholders
        )
        variant_ids[section.section_code] = section.variant_id

    return RenderedAssembly(
        registry_code=resolved.registry_code,
        registry_version_id=resolved.registry_version_id,
        version_number=resolved.version_number,
        sections=rendered_map,
        variant_ids=variant_ids,
    )
