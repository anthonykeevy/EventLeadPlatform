"""Prompt Assembly Registry resolver + renderer for Story 6.5b.

This package wraps the database-backed prompt assembly registry behind a
small Python API used by ``backend/modules/form_ai/service.py``:

  * :func:`resolve_prompt_assembly` - active version + winning variant
    selection for the in-scope sections (A/B/C/G/I in 6.5b).
  * :func:`render_prompt_assembly` - hydrate the resolved sections into a
    ``{SectionCode -> rendered_string}`` mapping ready for the
    ``_build_initial_messages`` glue path.

Story 6.5b only exercises ``DataStructureType = 'Prose'``. Other
DataStructureTypes (``Json``, ``Snapshot``, ``Refs``) are reserved for
6.5c / 6.5d and the renderer raises ``NotImplementedError`` if asked to
hydrate them.

Why a dict-by-SectionCode rather than a single concatenated string:
the current ``_build_initial_messages`` interleaves out-of-scope blocks
(Block D locale, Block F capability, Block H user prompt, layout-mode
nudge, runtime-context block, instruction addendum) between the
in-scope blocks. Returning per-block snippets lets the existing
assembly glue stay byte-identical while the source of each in-scope
snippet shifts from Python literal -> registry. The final assembly
order will be cleaned up in 6.5c when Block F migrates into the
registry and the renderer becomes the authoritative orchestrator.
"""

from .resolver import (
    REGISTRY_CODE_FORM_AI_V1,
    ResolvedSection,
    ResolvedAssembly,
    resolve_prompt_assembly,
)
from .renderer import RenderedAssembly, render_prompt_assembly

__all__ = [
    "REGISTRY_CODE_FORM_AI_V1",
    "ResolvedSection",
    "ResolvedAssembly",
    "RenderedAssembly",
    "resolve_prompt_assembly",
    "render_prompt_assembly",
]
