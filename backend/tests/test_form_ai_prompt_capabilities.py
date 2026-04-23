from modules.form_ai.prompt_capabilities import (
    DEFAULT_FORM_BUILDER_CAPABILITIES,
    build_capability_boundary_section,
)
from modules.form_ai.service import _build_initial_messages
from modules.form_ai.system_prompt_sections_1_6 import SYSTEM_PROMPT_SECTIONS_1_TO_6


def test_system_prompt_orders_persona_before_schema_and_contract():
    persona_idx = SYSTEM_PROMPT_SECTIONS_1_TO_6.index("## Persona")
    priorities_idx = SYSTEM_PROMPT_SECTIONS_1_TO_6.index("## Design Priorities")
    capability_idx = SYSTEM_PROMPT_SECTIONS_1_TO_6.index("## Capability Boundaries")
    output_idx = SYSTEM_PROMPT_SECTIONS_1_TO_6.index("## Output Contract")
    schema_idx = SYSTEM_PROMPT_SECTIONS_1_TO_6.index("## Output Schema")
    assert persona_idx < priorities_idx < capability_idx < output_idx < schema_idx


def test_capability_section_strong_layout_scenario():
    caps = dict(DEFAULT_FORM_BUILDER_CAPABILITIES)
    caps["multi_column_layout"] = "strong"
    caps["mixed_object_layout"] = "moderate"
    text = build_capability_boundary_section(caps)  # type: ignore[arg-type]
    assert "Multi-column layouts: strong." in text
    assert "Mixed object layouts: moderate." in text


def test_capability_section_weak_section_emphasis_and_limited_overrides():
    caps = dict(DEFAULT_FORM_BUILDER_CAPABILITIES)
    caps["section_visual_emphasis"] = "limited"
    caps["style_overrides"] = "limited"
    text = build_capability_boundary_section(caps)  # type: ignore[arg-type]
    assert "Section-level visual emphasis: limited." in text
    assert "Style overrides: limited." in text
    assert "prefer clean structure over forced emphasis" in text


def test_system_prompt_includes_locked_global_styles_rule():
    assert "## Global Styles Lock/Unlock Rules" in SYSTEM_PROMPT_SECTIONS_1_TO_6
    assert "Copy runtime globalStyles exactly" in SYSTEM_PROMPT_SECTIONS_1_TO_6


def test_user_message_supports_simple_and_complex_prompts_without_hardcoding():
    """Story 6.3.1 (UAT round 2) — the legacy ``_build_user_message`` helper
    was inlined into ``_build_initial_messages`` when the deterministic
    compiler took over. The contract that survives is: the user-facing prompt
    appears verbatim in the user-role message, with no hidden hardcoded
    template fields, and the system message keeps the persona/contract.
    """
    simple_prompt = "Create a short contact form with name and email."
    complex_prompt = "Create a multi-section job application form with grouped fields."

    simple_messages = _build_initial_messages(
        prompt=simple_prompt,
        context_pack="<<context-pack>>",
        runtime_context=None,
    )
    complex_messages = _build_initial_messages(
        prompt=complex_prompt,
        context_pack="<<context-pack>>",
        runtime_context=None,
    )

    # Both flows produce a system + user message pair.
    assert len(simple_messages) == 2 and len(complex_messages) == 2
    assert simple_messages[0]["role"] == "system"
    assert simple_messages[1]["role"] == "user"

    # User-facing prompt text is carried into the user-role message verbatim.
    assert simple_prompt in simple_messages[1]["content"]
    assert complex_prompt in complex_messages[1]["content"]
    assert simple_messages[1]["content"].rstrip().endswith("Return only valid JSON.")
    assert complex_messages[1]["content"].rstrip().endswith("Return only valid JSON.")

    # The system body still references the design-priority cue from the
    # static section bundle, even though the bundle is no longer pasted
    # verbatim — keeps a regression alarm if someone removes the cue.
    assert "Which fields belong together" in SYSTEM_PROMPT_SECTIONS_1_TO_6
