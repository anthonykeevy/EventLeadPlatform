"""Canonical Block A/B/C/G/I literals for the Story 6.5b registry seed.

These constants are the single source of truth (in code) for the prose
that lives in the registry tables after Story 6.5b's migrations run.
They are duplicated as Python literals in
``backend/migrations/versions/080_story_6_5b_seed_variants_a_b_c_i.py``
and ``081_story_6_5b_seed_block_g_context_pack.py`` (because migrations
must be self-contained); the equivalence test
``backend/tests/test_story_6_5b_equivalence.py`` asserts the migration
copies match these constants byte-for-byte.

Two consumers:
  1. ``service.py::_build_initial_messages`` falls back to these
     constants when called without a DB session (legacy tests that
     pre-date the registry path).
  2. ``backend/scripts/story_6_5b_prompt_equivalence_diff.py`` rebuilds
     the OLD pre-6.5b prompt path for the AC-19 sign-off diff.

Block C heritage placeholder note:
  ``BLOCK_C_HERITAGE`` uses the registry-side ``{heritageOrigin}``
  placeholder, substituted at render time by
  ``prompt_assembly.renderer.render_prompt_assembly``. The fallback
  helper ``render_canonical_brand_posture_block`` mirrors the legacy
  ``service.py::_render_brand_posture_block`` semantics:
    * ``heritage`` posture without an ``origin`` collapses to ``local``
      (matches existing fallback behaviour - critical for AC-19
      byte-equivalence).
    * Any unrecognised posture string also collapses to ``local``.
"""

from __future__ import annotations

from typing import Dict, Optional


BLOCK_A_DEFAULT = (
    "You generate an EventLead semantic form plan for Story 6.3.1.\n"
    "Output a single JSON object only. No markdown or prose.\n"
    "Return FormSemanticPlan only; do not output any coordinates, "
    "pixel widths, x/y positions, style blocks, or final DefinitionJSON.\n"
)


BLOCK_B_DEFAULT = (
    "## CONSENT & LEGAL ACKNOWLEDGEMENTS\n"
    "| User intent | Component | Required guidance |\n"
    "|---|---|---|\n"
    "| Marketing consent, terms acceptance, privacy acknowledgement, "
    "data/cookie consent, waiver, release, code-of-conduct or indemnity "
    "acknowledgement | ``terms`` | Set ``validationIntent.required = true`` "
    "unless explicitly optional. Use company-managed terms when runtime "
    "context provides them. |\n"
    "| Consent text but no company-managed terms | ``terms`` | Keep the "
    "acknowledgement sentence in ``label`` or ``props.termsContent``. Do "
    "not invent legal URLs or policy content. |\n"
    "| Interests, preferences, dietary choices, availability, feature "
    "toggles or other non-legal multi-select | ``checkbox`` | Treat as "
    "ordinary choices, not legal acknowledgement. |\n"
)


BLOCK_I_DEFAULT = (
    "REQUIRED ROOT KEYS (exact, case-sensitive):\n"
    '  - semanticPlanVersion: must be the string "1.0" (do NOT use the story number).\n'
    "  - formId: short slug or id (string).\n"
    "  - title: form title (string).\n"
    "  - components: array of component intents (see below).\n"
    "Do NOT add any other root keys.\n"
    "\n"
    "EACH COMPONENT (object):\n"
    "  - componentType (required), label, placeholder, helpText, section, rowGroup,\n"
    '  - widthIntent: one of "compact" | "half" | "full".\n'
    "    This is a HINT, not a final width. The deterministic compiler picks\n"
    "    the actual pixel width from a per-type tier table and may shrink the\n"
    "    component further (or wrap it onto its own row) so the layout fits\n"
    '    the canvas. Treat widthIntent as a maximum cap: use "compact" when\n'
    '    the field\'s content is short (e.g. zip, age, state code), "full"\n'
    "    only when you genuinely want the field to span the row.\n"
    "    Use rowGroup to indicate which fields you'd like packed side-by-side;\n"
    "    the compiler decides whether they actually fit.\n"
    "  - options: array of {label,value} for dropdown/radio,\n"
    "  - validationIntent: an OBJECT (not an array) with any of these boolean/number keys:\n"
    "      required, email, phone, url, minLength, maxLength, min, max, pattern.\n"
    '    Example: "validationIntent": { "required": true, "email": true }.\n'
    '    NEVER emit validationIntent as a list of strings (e.g. ["required","email"]).\n'
    "\n"
    "Use only Story 6.2/6.3.1 supported component catalog and single-page constraints.\n\n"
)


BLOCK_C_LOCAL = (
    "Brand posture: local. Match copy voice to the resolved audience locale."
)


BLOCK_C_HERITAGE = (
    "Brand posture: heritage. Audience locale still controls field shape "
    "and compliance; copy voice may lightly reflect {heritageOrigin} brand heritage."
)


BLOCK_C_NEUTRAL = (
    "Brand posture: neutral. Use market-neutral voice; audience locale "
    "still controls field shape and compliance."
)


BLOCK_C_TRANSCREATE = (
    "Brand posture: transcreate. Adapt copy idiomatically for the audience "
    "locale while preserving the user's intent."
)


_BLOCK_C_VARIANTS: Dict[str, str] = {
    "local": BLOCK_C_LOCAL,
    "heritage": BLOCK_C_HERITAGE,
    "neutral": BLOCK_C_NEUTRAL,
    "transcreate": BLOCK_C_TRANSCREATE,
}


def render_canonical_brand_posture_block(
    posture: Optional[str],
    origin: Optional[str],
) -> str:
    """Mirror of legacy ``service.py::_render_brand_posture_block``.

    Selects the variant by posture; collapses heritage-without-origin and
    any unrecognised posture to ``local`` (matches existing fallback
    behaviour - required for AC-19 byte-equivalence).
    """
    normalised = (posture or "").strip().lower() or None
    origin_clean = (origin or "").strip()
    if normalised == "heritage" and origin_clean:
        return BLOCK_C_HERITAGE.format(heritageOrigin=origin_clean)
    if normalised in {"neutral", "transcreate"}:
        return _BLOCK_C_VARIANTS[normalised]
    return BLOCK_C_LOCAL


__all__ = [
    "BLOCK_A_DEFAULT",
    "BLOCK_B_DEFAULT",
    "BLOCK_I_DEFAULT",
    "BLOCK_C_LOCAL",
    "BLOCK_C_HERITAGE",
    "BLOCK_C_NEUTRAL",
    "BLOCK_C_TRANSCREATE",
    "render_canonical_brand_posture_block",
]
