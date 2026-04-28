from modules.form_ai.service import (
    _CONSENT_GUIDANCE_BLOCK,
    _build_capability_prompt_block,
    _build_initial_messages,
    _filter_runtime_context_to_capability,
)


def _capability_snapshot():
    return {
        "components": [
            {"type": "text", "widthClasses": ["compact", "half", "full"]},
            {"type": "email", "widthClasses": ["half", "full"]},
            {"type": "submit-button", "widthClasses": ["compact", "half"]},
        ]
    }


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

    # The active prompt path keeps the semantic-plan system contract in the
    # system message, not in an orphan static prompt bundle.
    assert "Return FormSemanticPlan only" in simple_messages[0]["content"]
    assert "REQUIRED ROOT KEYS" in simple_messages[0]["content"]


def test_build_initial_messages_returns_two_message_prompt_contract():
    messages = _build_initial_messages(
        prompt="Create a contact form.",
        context_pack="<<context-pack>>",
        runtime_context=None,
    )

    assert [message["role"] for message in messages] == ["system", "user"]
    assert "<<context-pack>>" in messages[0]["content"]
    assert "Create a contact form." in messages[1]["content"]
    assert messages[1]["content"].rstrip().endswith("Return only valid JSON.")


def test_build_capability_prompt_block_renders_allowed_types_and_widths():
    text = _build_capability_prompt_block(_capability_snapshot())

    assert "ALLOWED COMPONENT TYPES" in text
    assert "text (allowed widthIntent hints: compact, half, full)" in text
    assert "email (allowed widthIntent hints: half, full)" in text
    assert "submit-button (allowed widthIntent hints: compact, half)" in text


def test_build_initial_messages_includes_capability_block_when_snapshot_exists():
    messages = _build_initial_messages(
        prompt="Create a contact form.",
        context_pack="<<context-pack>>",
        runtime_context=None,
        capability_snapshot_json=_capability_snapshot(),
    )

    system_prompt = messages[0]["content"]
    assert "ALLOWED COMPONENT TYPES" in system_prompt
    assert "text (allowed widthIntent hints: compact, half, full)" in system_prompt
    assert "submit-button (allowed widthIntent hints: compact, half)" in system_prompt


def test_story_6441_locale_prompt_is_registry_rendered_section():
    messages = _build_initial_messages(
        prompt="Create a contact form.",
        context_pack="<<context-pack>>",
        runtime_context=None,
        audience_locale="AU",
        db_session=None,
    )

    system_prompt = messages[0]["content"]
    assert "## LOCALE AND BRAND POSTURE" in system_prompt
    assert "Audience locale NEUTRAL" in system_prompt
    assert "Brand posture: local" in system_prompt


def test_story_644_h2_consent_guidance_is_compact_decision_table():
    assert len(_CONSENT_GUIDANCE_BLOCK) < 1200
    assert "| User intent | Component | Required guidance |" in _CONSENT_GUIDANCE_BLOCK
    assert "Marketing consent" in _CONSENT_GUIDANCE_BLOCK
    assert "company-managed terms" in _CONSENT_GUIDANCE_BLOCK
    assert "Do not invent legal URLs" in _CONSENT_GUIDANCE_BLOCK
    assert "GDPR, CCPA and the AU Privacy Act" not in _CONSENT_GUIDANCE_BLOCK


def test_story_644_h4_trims_context_pack_operational_notes_from_prompt():
    context_pack = (
        "# Context Pack\n\n"
        "## Component Catalog\nAllowed types stay here.\n\n"
        "## Operational Notes\n"
        "Provider credentials are loaded from local environment only.\n"
        "Never log or return provider secrets.\n"
    )

    messages = _build_initial_messages(
        prompt="Create a contact form.",
        context_pack=context_pack,
        runtime_context=None,
    )

    system_prompt = messages[0]["content"]
    assert "Allowed types stay here." in system_prompt
    assert "## Operational Notes" not in system_prompt
    assert "Provider credentials" not in system_prompt


def test_story_6442_h2_mode_keeps_compact_consent_and_disables_h4(monkeypatch):
    monkeypatch.setenv("FORM_AI_EVAL_PROMPT_SHRINK_MODE", "h2")
    context_pack = (
        "# Context Pack\n\n"
        "## Component Catalog\nAllowed types stay here.\n\n"
        "## Operational Notes\n"
        "Operational notes stay visible when H4 is disabled.\n"
    )

    messages = _build_initial_messages(
        prompt="Create a contact form.",
        context_pack=context_pack,
        runtime_context=None,
    )

    system_prompt = messages[0]["content"]
    assert "| User intent | Component | Required guidance |" in system_prompt
    assert "GDPR, CCPA and the AU Privacy Act" not in system_prompt
    assert "## Operational Notes" in system_prompt
    assert "Operational notes stay visible" in system_prompt


def test_story_6442_h4_mode_restores_legacy_consent_and_trims_operational_notes(monkeypatch):
    monkeypatch.setenv("FORM_AI_EVAL_PROMPT_SHRINK_MODE", "h4")
    context_pack = (
        "# Context Pack\n\n"
        "## Component Catalog\nAllowed types stay here.\n\n"
        "## Operational Notes\n"
        "Operational notes are trimmed when H4 is enabled.\n"
    )

    messages = _build_initial_messages(
        prompt="Create a contact form.",
        context_pack=context_pack,
        runtime_context=None,
    )

    system_prompt = messages[0]["content"]
    assert "GDPR, CCPA and the AU Privacy Act" in system_prompt
    assert "| User intent | Component | Required guidance |" not in system_prompt
    assert "## Operational Notes" not in system_prompt
    assert "Operational notes are trimmed" not in system_prompt


def test_build_capability_prompt_block_missing_snapshot_is_empty_legacy_fallback():
    assert _build_capability_prompt_block(None) == ""
    messages = _build_initial_messages(
        prompt="Create a contact form.",
        context_pack="<<context-pack>>",
        runtime_context=None,
        capability_snapshot_json=None,
    )

    assert "ALLOWED COMPONENT TYPES" not in messages[0]["content"]


def test_filter_runtime_context_to_capability_drops_footprints_outside_snapshot():
    runtime_context = {
        "canvas": {"width": 1920, "height": 1080},
        "componentFootprints": [
            {"componentType": "text", "width": 320, "height": 110},
            {"componentType": "rating", "width": 360, "height": 96},
            {"componentType": "submit-button", "width": 220, "height": 64},
        ],
    }

    filtered = _filter_runtime_context_to_capability(
        runtime_context, _capability_snapshot()
    )

    assert filtered is not runtime_context
    assert filtered["canvas"] == runtime_context["canvas"]
    assert [entry["componentType"] for entry in filtered["componentFootprints"]] == [
        "text",
        "submit-button",
    ]


def test_filter_runtime_context_to_capability_missing_snapshot_is_permissive():
    runtime_context = {
        "componentFootprints": [
            {"componentType": "rating", "width": 360, "height": 96},
        ],
    }

    assert _filter_runtime_context_to_capability(runtime_context, None) is runtime_context
