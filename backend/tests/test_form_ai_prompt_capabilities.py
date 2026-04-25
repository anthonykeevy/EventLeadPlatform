from modules.form_ai.service import (
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
