"""Story 6.3.1 Phase 1 — content-aware width tiers + justify-evenly + W2
section-gap rule.

These tests pin the *core invariants* of the layout solver redesign so any
regression that re-introduces the "widthIntent → 908 px first-name" behavior
is caught immediately.
"""

from typing import Any, Dict, List, Tuple

import pytest

from modules.form_ai.compiler import (
    COMPONENT_WIDTH_TIERS,
    DEFAULT_COLUMN_GAP,
    DEFAULT_MARGIN_X,
    DEFAULT_ROW_GAP,
    MIN_COLUMN_GAP,
    SECTION_GAP_MULTIPLIER,
    compile_semantic_plan_to_definition,
)
from modules.form_ai.schemas import FormSemanticPlan


# --- Helpers ----------------------------------------------------------------


def _governance() -> Dict[str, Any]:
    """Minimal governance payload covering every component type referenced in
    these tests. Mirrors the shape of the runtime governance row but keeps
    each list small so the tests stay readable."""
    return {
        "capabilityPolicyJson": {
            "step1": {"allowSemanticOnly": True, "allowGeometry": False},
            "step2": {"gridOnly": True, "allowNonGrid": False},
        },
        "widthClassPolicyJson": {
            "classes": {
                "compact": {"minSpan": 3, "targetSpan": 4, "maxSpan": 5},
                "half": {"minSpan": 5, "targetSpan": 6, "maxSpan": 7},
                "full": {"minSpan": 10, "targetSpan": 12, "maxSpan": 12},
            },
        },
        "componentCapabilitySnapshotJson": {
            "components": [
                {"type": "header", "widthClasses": ["full"]},
                {"type": "text", "widthClasses": ["compact", "half", "full"]},
                {"type": "email", "widthClasses": ["compact", "half", "full"]},
                {"type": "phone", "widthClasses": ["compact", "half", "full"]},
                {"type": "address", "widthClasses": ["full"]},
                {"type": "rating", "widthClasses": ["half", "full"]},
                {"type": "textarea", "widthClasses": ["half", "full"]},
                {"type": "dropdown", "widthClasses": ["compact", "half", "full"]},
                {"type": "submit-button", "widthClasses": ["compact", "half"]},
                {"type": "terms", "widthClasses": ["full"]},
                {"type": "paragraph", "widthClasses": ["full"]},
            ],
        },
        "validationContracts": [
            {"componentType": "text", "allowedRules": ["required", "maxLength"]},
            {"componentType": "email", "allowedRules": ["required", "email", "maxLength"]},
            {"componentType": "phone", "allowedRules": ["required", "phone", "maxLength"]},
            {"componentType": "address", "allowedRules": ["required", "maxLength"]},
            {"componentType": "rating", "allowedRules": ["required", "min", "max"]},
            {"componentType": "textarea", "allowedRules": ["required", "maxLength"]},
            {"componentType": "dropdown", "allowedRules": ["required"]},
            {"componentType": "terms", "allowedRules": ["required"]},
            {"componentType": "submit-button", "allowedRules": []},
            {"componentType": "header", "allowedRules": []},
            {"componentType": "paragraph", "allowedRules": []},
        ],
    }


def _compile(plan_payload: Dict[str, Any], *, canvas_width: int = 1920) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    plan = FormSemanticPlan.model_validate(plan_payload)
    governance = _governance()
    return compile_semantic_plan_to_definition(
        plan,
        runtime_context={"canvas": {"width": canvas_width, "height": 980, "gridSize": 8}},
        capability_policy_json=governance["capabilityPolicyJson"],
        width_policy_json=governance["widthClassPolicyJson"],
        capability_snapshot_json=governance["componentCapabilitySnapshotJson"],
        validation_contracts=governance["validationContracts"],
    )


def _by_label(components: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {c["props"]["label"]: c for c in components}


# --- W1: per-type content-aware width tiers ---------------------------------


@pytest.mark.parametrize(
    ("component_type", "label", "intent", "expected_target"),
    [
        # Generic text — "name"-style label is promoted to the narrower
        # first-name tier (180, 260, 360).
        ("text", "First name", "half", 260),
        ("text", "Last name", "half", 260),
        ("text", "Surname", "half", 260),
        # Generic text with a non-name label sits on the text tier (200, 320, 480).
        ("text", "Job title", "half", 320),
        # Email tier (240, 360, 520) — widthIntent=half does NOT inflate to ~908.
        ("email", "Email", "half", 360),
        # Phone tier (200, 280, 360) — widthIntent=full does NOT inflate to 1840.
        ("phone", "Phone", "full", 280),
        # Dropdown tier (220, 360, 520).
        ("dropdown", "Country", "half", 360),
        # Rating tier (240, 360, 520).
        ("rating", "Stars", "half", 360),
        # Header is always full-width regardless of widthIntent.
        ("header", "Welcome", "compact", 1840),
    ],
)
def test_per_type_tier_target_drives_width_not_widthintent(
    component_type: str, label: str, intent: str, expected_target: int
):
    payload: Dict[str, Any] = {
        "semanticPlanVersion": "1.0",
        "formId": "tier-target",
        "components": [
            {"componentType": component_type, "label": label, "widthIntent": intent},
        ],
    }
    if component_type == "rating":
        payload["components"][0]["validationIntent"] = {"min": 1, "max": 5}
    if component_type == "dropdown":
        payload["components"][0]["options"] = [{"label": "AU", "value": "au"}]

    definition, summary = _compile(payload)
    component = definition["pages"][0]["components"][0]
    assert component["style"]["width"] == expected_target, (
        f"{component_type} '{label}' widthIntent={intent} -> "
        f"expected width {expected_target}, got {component['style']['width']}"
    )

    diag = summary["stageDiagnostics"][0]
    assert diag["widthTargetPx"] == expected_target


def test_widthintent_acts_as_a_cap_not_a_target():
    """The LLM hint is always a cap — it can shrink a field below its tier
    target but never inflate it above. The dropdown tier target (360) >
    compact cap (360-ish) — verified via direct numeric comparison.

    Uses ``email`` (compact is allowed in the snapshot for email) with a long
    enough label/maxLength that the content-cap path doesn't fire — so
    widthSource lands cleanly on intent-cap.
    """
    # email tier (240, 360, 520). Compact cap = 360. They tie, so intent cap
    # is what binds the max — but compact cap shrinks max_px below the tier
    # max of 520. Verify that bound is enforced.
    definition, summary = _compile({
        "semanticPlanVersion": "1.0",
        "formId": "intent-cap",
        "components": [
            # maxLength=80 -> content_hint = 80*9 + 32 = 752 px (above tier
            # target of 360, so content cap does NOT fire — tier_target wins).
            {"componentType": "email", "label": "Email", "widthIntent": "compact",
             "validationIntent": {"required": True, "email": True, "maxLength": 80}},
        ],
    })
    email = definition["pages"][0]["components"][0]
    diag = summary["stageDiagnostics"][0]
    # Tier target (360) and compact cap (360) coincide; verify width respects
    # the intent cap (max_px shrunk from tier_max=520 down to compact cap).
    assert email["style"]["width"] <= 360
    assert diag["widthMaxPx"] <= 360, (
        f"compact intent should cap max_px at ~360, got {diag['widthMaxPx']}"
    )


def test_max_length_below_tier_triggers_content_cap():
    """When ``maxLength`` content target sits below the tier target, the
    compiler emits a content-cap'd width and surfaces ``widthSource``."""
    definition, summary = _compile({
        "semanticPlanVersion": "1.0",
        "formId": "content-cap",
        "components": [
            {"componentType": "text", "label": "State code", "widthIntent": "half",
             "validationIntent": {"required": True, "maxLength": 2}},
        ],
    })
    code = definition["pages"][0]["components"][0]
    # tier text target=320; content_hint = max(label*9, 2*9) + 32. With label
    # "State code" (10 chars) -> max(90, 18) + 32 = 122 px. That's below
    # tier_min=200, so the visual floor clamps target back up to 200.
    assert code["style"]["width"] < 320
    assert code["style"]["width"] >= 200, (
        "tier_min should act as a visual floor when content_hint underflows it"
    )
    diag = summary["stageDiagnostics"][0]
    assert diag["widthSource"] == "content-cap"


def test_known_tier_table_is_complete():
    """Sanity: every tier entry has well-ordered (min <= target <= max).
    Catches accidental swaps when adding new tiers in the future."""
    for component_type, (min_px, target_px, max_px) in COMPONENT_WIDTH_TIERS.items():
        assert min_px > 0, f"{component_type}: min_px must be positive"
        assert min_px <= target_px, f"{component_type}: min_px > target_px"
        assert target_px <= max_px, f"{component_type}: target_px > max_px"


# --- UAT round 3: aligned-grid horizontal placement -------------------------
# (Replaces the previous justify-evenly tests; the compiler no longer spreads
# slack across n+1 slots — solo rows pin to MARGIN_X, multi rows use exactly
# MIN_COLUMN_GAP between columns and let slack fall on the right.)


def test_aligned_grid_pins_solo_row_to_left_margin():
    """A solo (k=1) row's left edge sits at DEFAULT_MARGIN_X regardless of
    component width, so single-component rows line up under each other."""
    canvas_width = 1920
    definition, _ = _compile({
        "semanticPlanVersion": "1.0",
        "formId": "single-row-pin",
        "components": [
            {"componentType": "rating", "label": "Rate us", "widthIntent": "half",
             "validationIntent": {"min": 1, "max": 5}},
        ],
    }, canvas_width=canvas_width)

    rating = definition["pages"][0]["components"][0]
    assert rating["position"]["x"] == DEFAULT_MARGIN_X, (
        f"solo row should pin to MARGIN_X={DEFAULT_MARGIN_X}, "
        f"got x={rating['position']['x']}"
    )


def test_aligned_grid_two_columns_use_min_column_gap_with_left_pin():
    """Two components in the same rowGroup pin to MARGIN_X and use exactly
    MIN_COLUMN_GAP between columns — slack falls on the right (mirrors the
    solo-row left-pin so column-0 lines up under solo rows)."""
    canvas_width = 1920
    content_right = canvas_width - DEFAULT_MARGIN_X
    definition, _ = _compile({
        "semanticPlanVersion": "1.0",
        "formId": "two-col-aligned",
        "components": [
            {"componentType": "text", "label": "First name", "widthIntent": "half",
             "rowGroup": "name", "validationIntent": {"required": True, "maxLength": 40}},
            {"componentType": "text", "label": "Last name", "widthIntent": "half",
             "rowGroup": "name", "validationIntent": {"required": True, "maxLength": 40}},
        ],
    }, canvas_width=canvas_width)

    components = _by_label(definition["pages"][0]["components"])
    first = components["First name"]
    last = components["Last name"]
    # Column 0 pins to MARGIN_X.
    assert first["position"]["x"] == DEFAULT_MARGIN_X, (
        f"col-0 should pin to MARGIN_X, got {first['position']['x']}"
    )
    # Inter-column gap is exactly MIN_COLUMN_GAP (within rounding).
    interior_gap = last["position"]["x"] - (first["position"]["x"] + first["style"]["width"])
    assert abs(interior_gap - MIN_COLUMN_GAP) <= 1, (
        f"interior gap should equal MIN_COLUMN_GAP={MIN_COLUMN_GAP}, got {interior_gap}"
    )
    # Slack is on the right (right_offset > 0 when row is narrower than canvas).
    right_offset = content_right - (last["position"]["x"] + last["style"]["width"])
    assert right_offset >= 0, f"right edge should not exceed canvas, slack={right_offset}"


def test_justify_evenly_does_not_overlap_at_minimum_slack():
    """When the row almost exactly fills content_width the compiler must NOT
    produce overlapping x positions — this is the regression guard against
    the floor-vs-span bug from earlier UAT cycles."""
    # On a tiny canvas where two name fields just barely fit.
    canvas_width = 600  # content_width = 520, two names @ 260 each = 520 exact.
    definition, _ = _compile({
        "semanticPlanVersion": "1.0",
        "formId": "tight-fit",
        "components": [
            {"componentType": "text", "label": "First name", "widthIntent": "half",
             "rowGroup": "name", "validationIntent": {"maxLength": 40}},
            {"componentType": "text", "label": "Last name", "widthIntent": "half",
             "rowGroup": "name", "validationIntent": {"maxLength": 40}},
        ],
    }, canvas_width=canvas_width)

    components = definition["pages"][0]["components"]
    # On a tight canvas the tier target may exceed content_width / 2 - gap; the
    # width-based wrap detection in add_component_row may push the second name
    # to its own row. Either layout is acceptable as long as no overlap.
    rows: Dict[int, List[Dict[str, Any]]] = {}
    for c in components:
        rows.setdefault(c["position"]["y"], []).append(c)
    for items in rows.values():
        items.sort(key=lambda c: c["position"]["x"])
        for i in range(1, len(items)):
            prev_right = items[i - 1]["position"]["x"] + items[i - 1]["style"]["width"]
            assert items[i]["position"]["x"] >= prev_right, (
                f"row at y={items[i]['position']['y']} has overlap: "
                f"{items[i - 1]['id']} right={prev_right} vs "
                f"{items[i]['id']} left={items[i]['position']['x']}"
            )


# --- W2: section-gap multiplier rule ----------------------------------------


def test_section_gap_skipped_when_previous_section_had_one_row():
    """The W2 rule: skip the extra section gap when the previous section had
    fewer than 2 rows. Prevents the LLM-emits-1-row-per-section pattern from
    accumulating vertical sprawl."""
    definition, _ = _compile({
        "semanticPlanVersion": "1.0",
        "formId": "single-row-sections",
        "components": [
            {"componentType": "header", "label": "Welcome", "widthIntent": "full",
             "section": "intro"},
            {"componentType": "text", "label": "Email", "widthIntent": "half",
             "section": "signup", "validationIntent": {"required": True, "maxLength": 80}},
            {"componentType": "submit-button", "label": "Subscribe",
             "widthIntent": "compact", "actionAlignment": "center", "section": "action"},
        ],
    })
    components = _by_label(definition["pages"][0]["components"])
    welcome = components["Welcome"]
    email = components["Email"]
    submit = components["Subscribe"]

    # Each section had 1 row → the multiplier never fires; just base row gaps.
    expected_email_y = welcome["position"]["y"] + welcome["style"]["height"] + DEFAULT_ROW_GAP
    expected_submit_y = email["position"]["y"] + email["style"]["height"] + DEFAULT_ROW_GAP
    assert email["position"]["y"] == expected_email_y
    assert submit["position"]["y"] == expected_submit_y


def test_section_gap_fires_when_previous_section_had_two_rows():
    """The other half of the W2 rule: multi-row previous section DOES trigger
    the SECTION_GAP_MULTIPLIER extra leading gap before the next section."""
    definition, _ = _compile({
        "semanticPlanVersion": "1.0",
        "formId": "multi-row-section",
        "components": [
            # Section 'contact' = 2 rows.
            {"componentType": "text", "label": "First name", "widthIntent": "half",
             "section": "contact", "rowGroup": "name",
             "validationIntent": {"required": True, "maxLength": 40}},
            {"componentType": "text", "label": "Last name", "widthIntent": "half",
             "section": "contact", "rowGroup": "name",
             "validationIntent": {"required": True, "maxLength": 40}},
            {"componentType": "email", "label": "Email", "widthIntent": "half",
             "section": "contact", "rowGroup": "ct",
             "validationIntent": {"required": True, "email": True, "maxLength": 80}},
            {"componentType": "phone", "label": "Phone", "widthIntent": "half",
             "section": "contact", "rowGroup": "ct",
             "validationIntent": {"required": True, "phone": True, "maxLength": 20}},
            # New section 'message' — multi-row previous → extra gap fires.
            {"componentType": "textarea", "label": "Message", "widthIntent": "full",
             "section": "message", "validationIntent": {"maxLength": 2000}},
        ],
    })
    by = _by_label(definition["pages"][0]["components"])
    email_row_bottom = by["Email"]["position"]["y"] + by["Email"]["style"]["height"]
    expected_message_y = (
        email_row_bottom
        + DEFAULT_ROW_GAP
        + int((SECTION_GAP_MULTIPLIER - 1.0) * DEFAULT_ROW_GAP)
    )
    assert by["Message"]["position"]["y"] == expected_message_y


# --- UAT round 4: textarea height + address componentType remap -------------


def test_textarea_default_height_is_200_not_240():
    """The textarea default height was lowered from 240 → 200 in UAT round 4
    so a single Comments box no longer dominates the canvas. 200 also matches
    the runtime DOM chrome (label + body + helper text) and the validator's
    collision-inflation floor, so authored ≈ rendered ≈ inflated."""
    definition, _ = _compile({
        "semanticPlanVersion": "1.0",
        "formId": "textarea-height",
        "components": [
            {"componentType": "textarea", "label": "Comments", "widthIntent": "full",
             "validationIntent": {"maxLength": 2000}},
        ],
    })
    comments = definition["pages"][0]["components"][0]
    assert comments["type"] == "textarea"
    assert comments["style"]["height"] == 200, (
        f"textarea default should be 200, got {comments['style']['height']}"
    )


def test_address_label_remaps_textarea_to_address_component_type():
    """The LLM frequently picks ``componentType: textarea`` for a field labeled
    "Address". The compiler remaps to the ``address`` componentType so the
    field gets the address tier (360/600/900) and single-line text-input height
    instead of the multi-line textarea defaults (320/480/720, height 180)."""
    definition, summary = _compile({
        "semanticPlanVersion": "1.0",
        "formId": "address-remap",
        "components": [
            {"componentType": "textarea", "label": "Address", "widthIntent": "full",
             "validationIntent": {"maxLength": 200}},
        ],
    })
    address = definition["pages"][0]["components"][0]
    assert address["type"] == "address", (
        f"label 'Address' should remap textarea→address, got type={address['type']}"
    )
    # Address tier target = 600. Single-line input default height (~110), not
    # textarea's 200.
    assert address["style"]["width"] == 600
    assert address["style"]["height"] < 200, (
        f"address should use single-line height, got {address['style']['height']}"
    )
    # Remap surfaced in the trace.
    remaps = summary["componentTypeRemaps"]
    assert len(remaps) == 1
    assert remaps[0]["from"] == "textarea"
    assert remaps[0]["to"] == "address"
    assert remaps[0]["reason"] == "label-suggests-address"


def test_textarea_with_non_address_label_keeps_textarea_type():
    """Guard: only the address label list triggers a remap. A 'Comments' or
    'Message' textarea must stay as a textarea so we don't accidentally hide
    multi-line input from prompts that genuinely want it."""
    definition, summary = _compile({
        "semanticPlanVersion": "1.0",
        "formId": "no-remap",
        "components": [
            {"componentType": "textarea", "label": "Comments", "widthIntent": "full",
             "validationIntent": {"maxLength": 2000}},
            {"componentType": "textarea", "label": "Message", "widthIntent": "full",
             "validationIntent": {"maxLength": 2000}},
        ],
    })
    types = {c["props"]["label"]: c["type"] for c in definition["pages"][0]["components"]}
    assert types == {"Comments": "textarea", "Message": "textarea"}
    assert summary["componentTypeRemaps"] == []


# --- UAT round 5: rendered-chrome budget (textarea + submit button) ---------


def test_textarea_followed_by_submit_reserves_chrome_so_no_visual_overlap():
    """UAT round 5 — the renderer paints label + body + validation as separately
    stacked objects; for ``textarea`` the body grows with ``style.height`` and
    chrome is *added* on top, so the JSON bounding box (200 px) understates the
    on-screen footprint by ~80 px. Before the fix, a 200-px-tall Comments box
    placed 24 px above a 72-px Submit button visibly overlapped the rendered
    validation message slot beneath the textarea.

    The compiler now reserves ``style.height + COMPONENT_RENDERED_CHROME_PX``
    of vertical space, so the next row sits low enough that the rendered
    chrome no longer collides. ``style.height`` itself is unchanged (the
    renderer keeps painting a 200 px textarea body and a 72 px submit button)."""
    definition, _ = _compile({
        "semanticPlanVersion": "1.0",
        "formId": "textarea-submit-chrome",
        "components": [
            {"componentType": "textarea", "label": "Comments", "widthIntent": "full",
             "validationIntent": {"maxLength": 2000}},
            {"componentType": "submit-button", "label": "Submit", "widthIntent": "compact"},
        ],
    })
    components = {c["props"]["label"]: c for c in definition["pages"][0]["components"]}
    comments = components["Comments"]
    submit = components["Submit"]

    # style.height is unchanged — renderer paints same as before.
    assert comments["style"]["height"] == 200
    assert submit["style"]["height"] == 72

    # But submit must sit at least textarea_body (200) + textarea_chrome (80)
    # + DEFAULT_ROW_GAP (24) below the textarea's top, otherwise the rendered
    # validation slot below the textarea body will overlap the submit button.
    textarea_top = comments["position"]["y"]
    submit_top = submit["position"]["y"]
    expected_min_gap = 200 + 80 + 24  # body + chrome + row gap
    assert submit_top - textarea_top >= expected_min_gap, (
        f"submit too close to textarea: gap={submit_top - textarea_top}, "
        f"expected >= {expected_min_gap} (body+chrome+row_gap)"
    )


def test_canvas_grows_to_include_textarea_rendered_chrome():
    """The canvas height must include the chrome budget of the *last* row,
    otherwise even a single-textarea form would render with the validation
    message slot dangling off the bottom of the canvas. We verify the canvas
    grew by at least the chrome budget compared to a body-only reservation."""
    definition, _ = _compile({
        "semanticPlanVersion": "1.0",
        "formId": "textarea-canvas-grow",
        "components": [
            {"componentType": "header", "label": "Tell us how we did", "widthIntent": "full"},
            {"componentType": "textarea", "label": "Comments", "widthIntent": "full",
             "validationIntent": {"maxLength": 2000}},
        ],
    })
    components = {c["props"]["label"]: c for c in definition["pages"][0]["components"]}
    comments = components["Comments"]
    canvas_height = definition["canvasSettings"]["height"]

    # Canvas must extend at least body (200) + chrome (80) below the textarea
    # top — otherwise the rendered validation slot is clipped.
    assert canvas_height >= comments["position"]["y"] + 200 + 80, (
        f"canvas height {canvas_height} doesn't accommodate chrome below "
        f"textarea at y={comments['position']['y']}"
    )


def test_submit_button_alone_reserves_validation_slot_below_button():
    """A standalone submit button still has a validation slot rendered below
    it (see ``ComponentRegistry['submit-button'].structure.objects``). The
    compiler must reserve room so the canvas extends past that slot."""
    definition, _ = _compile({
        "semanticPlanVersion": "1.0",
        "formId": "submit-only",
        "components": [
            {"componentType": "header", "label": "Sign up", "widthIntent": "full"},
            {"componentType": "email", "label": "Email", "widthIntent": "full",
             "validationIntent": {"required": True, "email": True}},
            {"componentType": "submit-button", "label": "Submit", "widthIntent": "compact"},
        ],
    })
    components = {c["props"]["label"]: c for c in definition["pages"][0]["components"]}
    submit = components["Submit"]
    canvas_height = definition["canvasSettings"]["height"]

    # Submit button body + chrome (48 = loading slot + validation slot + spacing).
    # Canvas must extend at least to submit_top + 72 (body) + 48 (chrome).
    expected_floor = submit["position"]["y"] + 72 + 48
    assert canvas_height >= expected_floor, (
        f"canvas {canvas_height} doesn't fit submit chrome (need >= {expected_floor})"
    )


def test_text_inputs_have_no_chrome_budget_so_layout_unchanged():
    """Text-style inputs (text, email, phone, etc.) already absorb label +
    input + validation inside their 110 px DEFAULT_COMPONENT_HEIGHTS bounding
    box (the input body is a fixed ~40 px regardless of ``style.height``).
    They have no chrome budget, so the row spacing must be exactly
    DEFAULT_ROW_GAP (24) — proving we didn't accidentally widen *every* row.

    Each component gets its own rowGroup so the row solver doesn't pack them
    into a single multi-column row (which would defeat the per-row spacing
    check)."""
    definition, _ = _compile({
        "semanticPlanVersion": "1.0",
        "formId": "text-no-chrome",
        "components": [
            {"componentType": "first-name", "label": "First", "widthIntent": "full",
             "rowGroup": "row-1"},
            {"componentType": "last-name", "label": "Last", "widthIntent": "full",
             "rowGroup": "row-2"},
            {"componentType": "email", "label": "Email", "widthIntent": "full",
             "rowGroup": "row-3"},
        ],
    })
    components = [c for c in definition["pages"][0]["components"]]
    components.sort(key=lambda c: c["position"]["y"])
    first, last, email = components

    # Each text input reserves exactly style.height (110) + DEFAULT_ROW_GAP (24)
    # of vertical real estate. No chrome surcharge.
    assert last["position"]["y"] - first["position"]["y"] == 110 + 24
    assert email["position"]["y"] - last["position"]["y"] == 110 + 24


# --- UAT round 5 (run 40): uniform inter-row gaps + pre-compile heading drop ---


def test_section_change_does_not_inflate_gap_uniform_rhythm():
    """UAT round 5 (run 40, prompt 1) — user explicitly requested uniform gaps:

      "Based on our calculation method the gap at the top and inbetween should
       be identical?"

    Before this fix ``SECTION_GAP_MULTIPLIER = 2.0`` added an extra
    ``DEFAULT_ROW_GAP`` between Email (last row of section ``contact``) and
    Company (first row of section ``company``) whenever ``contact`` had ≥2
    rows on mobile (where first/last/phone/email all wrap to single-column).
    Result: most gaps were 24 px, the section-change gap was 48 px, and the
    canvas looked visually uneven.

    Setting ``SECTION_GAP_MULTIPLIER = 1.0`` collapses that to 0, so every
    inter-row gap is exactly ``DEFAULT_ROW_GAP``. We replay the exact section
    structure from run 40 here so a regression to ``2.0`` would fail this
    test loudly.
    """
    definition, _ = _compile({
        "semanticPlanVersion": "1.0",
        "formId": "uniform-gaps-run40",
        "components": [
            # contact section — multi-row on mobile (each component its own row).
            {"componentType": "first-name", "label": "First name",
             "widthIntent": "half", "section": "contact", "rowGroup": "name"},
            {"componentType": "last-name", "label": "Last name",
             "widthIntent": "half", "section": "contact", "rowGroup": "name"},
            {"componentType": "phone", "label": "Phone",
             "widthIntent": "half", "section": "contact", "rowGroup": "ct"},
            {"componentType": "email", "label": "Email",
             "widthIntent": "half", "section": "contact", "rowGroup": "ct",
             "validationIntent": {"required": True, "email": True}},
            # company section — section change after a multi-row contact section.
            {"componentType": "text", "label": "Company",
             "widthIntent": "full", "section": "company"},
            # message section — another section change.
            {"componentType": "textarea", "label": "Comments",
             "widthIntent": "full", "section": "message"},
        ],
    }, canvas_width=375)
    by = _by_label(definition["pages"][0]["components"])
    email = by["Email"]
    company = by["Company"]

    # The gap between Email and Company (a section change after a 2+ row section)
    # must equal exactly DEFAULT_ROW_GAP — not 2 * DEFAULT_ROW_GAP.
    email_bottom = email["position"]["y"] + email["style"]["height"]
    gap_email_to_company = company["position"]["y"] - email_bottom
    assert gap_email_to_company == DEFAULT_ROW_GAP, (
        f"section-change gap is {gap_email_to_company}px, expected "
        f"{DEFAULT_ROW_GAP}px (uniform-gap policy)"
    )
    # And SECTION_GAP_MULTIPLIER itself must be 1.0 — guarding against an
    # accidental revert that would silently re-introduce the visual bug.
    assert SECTION_GAP_MULTIPLIER == 1.0, (
        "SECTION_GAP_MULTIPLIER must be 1.0 — any other value re-introduces "
        "non-uniform inter-row gaps that UAT round 5 explicitly flagged"
    )


def test_pre_compile_heading_filter_no_ghost_top_gap():
    """UAT round 5 (run 40, prompt 1) — user observed the live form had ~80 px
    of empty space above First name even though ``DEFAULT_MARGIN_Y = 24``.

    Root cause: the LLM emitted a courtesy ``header`` intent, the compiler
    placed it at y=24 with first-name below at y=24+56+24=104, and the
    *post-compile* heading filter then dropped the rendered header without
    repositioning anything. So the canvas had a ghost 80 px gap at the top.

    Fix: the heading filter now also runs at the *plan* stage (see
    ``_filter_unrequested_headings_from_plan``) so the compiler never reserves
    the vertical real estate in the first place. First name lands at y=24 —
    the same as DEFAULT_MARGIN_Y, the same as every other inter-row gap.

    We exercise the helper directly here because it's pure (no DB / network)
    and the assertion targets exactly the y-coordinate the user complained
    about.
    """
    from modules.form_ai.service import _filter_unrequested_headings_from_plan

    plan = FormSemanticPlan.model_validate({
        "semanticPlanVersion": "1.0",
        "formId": "ghost-gap-repro",
        "components": [
            # Courtesy header the LLM volunteered; user prompt didn't ask for one.
            {"componentType": "header", "label": "Contact form", "widthIntent": "full"},
            {"componentType": "first-name", "label": "First name", "widthIntent": "full"},
            {"componentType": "submit-button", "label": "Submit", "widthIntent": "compact"},
        ],
    })
    # User prompt had none of: header, heading, title, banner, intro.
    user_prompt = "Create a contact form with first name and a submit button."
    filtered_plan, dropped = _filter_unrequested_headings_from_plan(plan, user_prompt)
    assert dropped == 1, "courtesy header should be dropped before compile"
    assert all(c.componentType != "header" for c in filtered_plan.components)

    # Compile the FILTERED plan (mirrors what service.run_form_ai_generation does)
    # and confirm First name now sits at the canvas top margin.
    governance = _governance()
    definition, _ = compile_semantic_plan_to_definition(
        filtered_plan,
        runtime_context={"canvas": {"width": 375, "height": 667, "gridSize": 8}},
        capability_policy_json=governance["capabilityPolicyJson"],
        width_policy_json=governance["widthClassPolicyJson"],
        capability_snapshot_json=governance["componentCapabilitySnapshotJson"],
        validation_contracts=governance["validationContracts"],
    )
    first = _by_label(definition["pages"][0]["components"])["First name"]
    assert first["position"]["y"] == 24, (
        f"First name at y={first['position']['y']}; expected 24 "
        f"(DEFAULT_MARGIN_Y) — ghost gap from dropped header has crept back in"
    )


def test_pre_compile_heading_filter_keeps_requested_heading():
    """The mirror-image of the previous test: when the prompt DOES request a
    header (uses any of header/heading/title/banner/intro), the courtesy
    header survives the pre-compile filter and the compiler lays it out.
    Otherwise we'd silently drop legitimate headers."""
    from modules.form_ai.service import _filter_unrequested_headings_from_plan

    plan = FormSemanticPlan.model_validate({
        "semanticPlanVersion": "1.0",
        "formId": "requested-heading",
        "components": [
            {"componentType": "header", "label": "Welcome", "widthIntent": "full"},
            {"componentType": "first-name", "label": "First name", "widthIntent": "full"},
        ],
    })
    user_prompt = "Build a signup form with a 'Welcome' title at the top."
    filtered_plan, dropped = _filter_unrequested_headings_from_plan(plan, user_prompt)
    assert dropped == 0, "requested header must survive the pre-compile filter"
    assert filtered_plan.components[0].componentType == "header"


def test_pre_compile_heading_filter_drops_placeholder_label_regardless():
    """Headers with placeholder/empty labels are noise and should be dropped
    even when the prompt explicitly asks for a heading. This matches the
    post-compile filter's behaviour (``_is_placeholder_heading_text``)."""
    from modules.form_ai.service import _filter_unrequested_headings_from_plan

    plan = FormSemanticPlan.model_validate({
        "semanticPlanVersion": "1.0",
        "formId": "placeholder-header",
        "components": [
            {"componentType": "header", "label": "-", "widthIntent": "full"},
            {"componentType": "first-name", "label": "First name", "widthIntent": "full"},
        ],
    })
    user_prompt = "Build a form with a heading."  # heading IS requested
    _, dropped = _filter_unrequested_headings_from_plan(plan, user_prompt)
    assert dropped == 1, (
        "placeholder-text header must be dropped even when the prompt asks "
        "for a heading — placeholder text is never a useful heading"
    )


# --- UAT round 5 (run 41): submit-button left-aligned by default ------------


def test_submit_button_defaults_to_left_alignment():
    """UAT round 5 (run 41) — user explicitly requested:

      "Only the submit button is not left aligned like the rest of the
       components"

    Default ``actionAlignment`` for ``submit-button`` was ``center`` so the
    button rendered floating between the canvas's left and right margins while
    every input above it sat flush left at ``DEFAULT_MARGIN_X``. The default
    is now ``left`` so an LLM that omits ``actionAlignment`` produces a form
    that visually "lines up". The LLM can still override with ``center`` /
    ``right`` when a centered call-to-action is genuinely intended.

    Asserts the x-coordinate matches the form's left margin exactly — same
    as every other component above it.
    """
    definition, _ = _compile({
        "semanticPlanVersion": "1.0",
        "formId": "submit-left-default",
        "components": [
            {"componentType": "text", "label": "Email", "widthIntent": "half",
             "validationIntent": {"required": True, "maxLength": 80}},
            # Note: no ``actionAlignment`` field at all — we want the *default*.
            {"componentType": "submit-button", "label": "Submit",
             "widthIntent": "compact"},
        ],
    })
    submit = _by_label(definition["pages"][0]["components"])["Submit"]
    assert submit["position"]["x"] == DEFAULT_MARGIN_X, (
        f"submit-button without explicit actionAlignment must default to "
        f"left (x={DEFAULT_MARGIN_X}); got x={submit['position']['x']}"
    )


def test_submit_button_explicit_center_still_centers():
    """Regression guard: changing the *default* must not break the LLM's
    ability to opt into centered alignment when it really wants one. A form
    with ``actionAlignment: "center"`` should still center the button.
    """
    definition, _ = _compile({
        "semanticPlanVersion": "1.0",
        "formId": "submit-explicit-center",
        "components": [
            {"componentType": "text", "label": "Email", "widthIntent": "half",
             "validationIntent": {"required": True, "maxLength": 80}},
            {"componentType": "submit-button", "label": "Submit",
             "widthIntent": "compact", "actionAlignment": "center"},
        ],
    }, canvas_width=1920)
    submit = _by_label(definition["pages"][0]["components"])["Submit"]
    # On a 1920 px canvas, content_width = 1920 - 2*DEFAULT_MARGIN_X. A
    # ``compact`` submit-button with target width ~280 px should land
    # well to the right of DEFAULT_MARGIN_X — i.e. it MUST not collapse to
    # the left edge just because we changed the default.
    assert submit["position"]["x"] > DEFAULT_MARGIN_X + 200, (
        f"explicit actionAlignment='center' should center the button; got "
        f"x={submit['position']['x']} (too close to left margin)"
    )


# --- UAT round 5 (run 41): rowGroup int -> str coercion ---------------------


def test_rowgroup_integer_is_coerced_to_string():
    """UAT round 5 (run 41 attempt 1 of 3) — wasted because the LLM emitted:

        {"rowGroup": 1, ...}

    The strict ``Optional[str]`` schema rejected the entire plan with seven
    "Input should be a valid string" errors and forced a full correction
    round trip. The role of these fields is purely to *group* components —
    only equality matters — so we now coerce int/float to str, save the
    retry, and surface no behaviour change in downstream consumers.

    Tests both rowGroup AND section since both grouping tokens get the same
    coercion.
    """
    plan = FormSemanticPlan.model_validate({
        "semanticPlanVersion": "1.0",
        "formId": "row-group-int",
        "components": [
            {"componentType": "text", "label": "First", "section": 1, "rowGroup": 1},
            {"componentType": "text", "label": "Last",  "section": 1, "rowGroup": 1},
            # Float rowGroup — also coerced.
            {"componentType": "text", "label": "Phone", "section": 2, "rowGroup": 2.0},
            # String form still works untouched (regression guard).
            {"componentType": "text", "label": "Email", "section": "contact",
             "rowGroup": "ct"},
        ],
    })
    by_label = {c.label: c for c in plan.components}
    assert by_label["First"].rowGroup == "1"
    assert by_label["First"].section == "1"
    assert by_label["Last"].rowGroup == "1"
    # First + Last share rowGroup → equality preserved post-coercion. This is
    # the actual functional invariant the compiler relies on.
    assert by_label["First"].rowGroup == by_label["Last"].rowGroup
    # Float "2.0" coerces to "2.0" (str()), which is distinct from "2" but
    # also distinct from "1" — equality semantics still work for the row
    # solver. The exact stringification is intentionally left to ``str()``;
    # we don't try to canonicalise 2.0 -> "2" because that would be lossy
    # in the rare case the LLM is using floats meaningfully.
    assert by_label["Phone"].rowGroup == "2.0"
    assert by_label["Email"].rowGroup == "ct"


def test_rowgroup_blank_string_collapses_to_none():
    """A blank or whitespace-only ``rowGroup`` carries no grouping signal,
    so the coercer normalises it to ``None`` rather than letting an empty
    string create a phantom row group that's distinct from "no row group".
    """
    plan = FormSemanticPlan.model_validate({
        "semanticPlanVersion": "1.0",
        "formId": "row-group-blank",
        "components": [
            {"componentType": "text", "label": "A", "rowGroup": ""},
            {"componentType": "text", "label": "B", "rowGroup": "   "},
            {"componentType": "text", "label": "C", "rowGroup": None},
        ],
    })
    for component in plan.components:
        assert component.rowGroup is None, (
            f"blank rowGroup must collapse to None; component {component.label} "
            f"got rowGroup={component.rowGroup!r}"
        )


def test_rowgroup_invalid_shape_still_raises():
    """The coercer is intentionally narrow: only int/float/str/None are
    coerced. A list or dict in ``rowGroup`` is a real bug we want to surface,
    not silently turn into a string.

    This guards against a future "lenient" change accidentally swallowing
    structural mistakes the LLM should be told about.
    """
    with pytest.raises(Exception):  # ValidationError; broad to keep import surface small
        FormSemanticPlan.model_validate({
            "semanticPlanVersion": "1.0",
            "formId": "row-group-bad",
            "components": [
                {"componentType": "text", "label": "Bad", "rowGroup": ["a", "b"]},
            ],
        })


def test_rowgroup_boolean_is_not_coerced():
    """``isinstance(True, int)`` is True in Python — we explicitly exclude
    bools from coercion so ``rowGroup: true`` doesn't silently become the
    string ``"True"`` (which is almost certainly not what the LLM meant).
    The schema then raises a ValidationError, which is the right outcome:
    the LLM should get a correction prompt explaining rowGroup is a token,
    not a flag.
    """
    with pytest.raises(Exception):
        FormSemanticPlan.model_validate({
            "semanticPlanVersion": "1.0",
            "formId": "row-group-bool",
            "components": [
                {"componentType": "text", "label": "Bad", "rowGroup": True},
            ],
        })


# --- UAT round 5 (run 42) — trust compiler-emitted widths ------------------
#
# Run 42 was the first run after migrations 055 and 056. Generation succeeded
# but the live system reported "Failed — 1 boundary violation" with the
# ``compiler-validation-failed`` terminal reason. Investigation showed the
# compiled definition itself was clean (every component fit inside the 375 px
# mobile canvas), but ``_collect_visual_boundary_violations`` was inflating
# every component to ``_minimum_render_width`` (460 px — the desktop toolbox
# footprint). On a 375 px mobile canvas, ``40 + 460 = 500`` always overflows.
#
# These tests pin the new "trust the compiler" rule so we don't regress.


def test_visual_boundary_check_trusts_compiler_widths_on_mobile():
    """Mobile canvas (375 px) with realistic compiler widths (~280-295 px).

    Before the fix the check inflated every input to 460 px and reported a
    boundary violation for each. After the fix the stated widths are trusted
    and no violations fire.
    """
    from modules.form_ai.service import _collect_visual_boundary_violations

    definition: Dict[str, Any] = {
        "canvasSettings": {"width": 375, "height": 1328},
        "pages": [
            {
                "id": "page-1",
                "components": [
                    {
                        "id": "first-name-1",
                        "type": "first-name",
                        "position": {"x": 40, "y": 24},
                        "style": {"width": 260, "height": 117},
                        "props": {"label": "First name"},
                    },
                    {
                        "id": "email-1",
                        "type": "email",
                        "position": {"x": 40, "y": 165},
                        "style": {"width": 295, "height": 117},
                        "props": {"label": "Email"},
                    },
                    {
                        "id": "address-1",
                        "type": "address",
                        "position": {"x": 40, "y": 306},
                        "style": {"width": 295, "height": 120},
                        "props": {"label": "Mailing address"},
                    },
                    {
                        "id": "textarea-1",
                        "type": "textarea",
                        "position": {"x": 40, "y": 450},
                        "style": {"width": 295, "height": 200},
                        "props": {"label": "Comments"},
                    },
                    {
                        "id": "submit-1",
                        "type": "submit-button",
                        "position": {"x": 40, "y": 674},
                        "style": {"width": 280, "height": 86},
                        "props": {"label": "Submit"},
                    },
                ],
            }
        ],
    }
    runtime_context = {
        "canvas": {"width": 375, "height": 667, "gridSize": 8},
        "device": "mobile",
    }
    violations = _collect_visual_boundary_violations(definition, runtime_context)
    assert violations == [], (
        "Visual boundary check must trust the deterministic compiler's emitted "
        "widths on narrow canvases instead of inflating to the desktop minimum. "
        f"Got {len(violations)} false-positive violation(s): {violations}"
    )


def test_visual_boundary_check_still_catches_off_canvas_overflow():
    """Regression guard: trusting stated widths must NOT mask real overflows.

    A component with a stated width of 500 px on a 375 px canvas (x=40 →
    right edge 540) still overflows by 165 px and must surface as a boundary
    violation.
    """
    from modules.form_ai.service import _collect_visual_boundary_violations

    definition: Dict[str, Any] = {
        "canvasSettings": {"width": 375, "height": 800},
        "pages": [
            {
                "id": "page-1",
                "components": [
                    {
                        "id": "wide-1",
                        "type": "text",
                        "position": {"x": 40, "y": 24},
                        "style": {"width": 500, "height": 117},  # overflows by 165 px
                        "props": {"label": "Too wide"},
                    },
                ],
            }
        ],
    }
    violations = _collect_visual_boundary_violations(definition, runtime_context=None)
    assert len(violations) == 1, (
        "Real overflow (stated width 500 px on a 375 px canvas) must still "
        f"fire a boundary violation. Got {len(violations)}."
    )
    flags = violations[0].violations
    # ``flags`` is a Pydantic model on the response side — accept either form.
    if hasattr(flags, "model_dump"):
        flags = flags.model_dump()
    assert flags["right"] is True


def test_visual_boundary_check_still_catches_implausible_zero_width():
    """If the stated width is zero / negative / sub-60 px (clear LLM bug),
    the check falls back to ``_minimum_render_width`` so we still detect
    geometry that would render as a degenerate box.
    """
    from modules.form_ai.service import (
        MIN_PLAUSIBLE_RENDER_WIDTH_PX,
        _collect_visual_boundary_violations,
    )

    assert MIN_PLAUSIBLE_RENDER_WIDTH_PX == 60.0, (
        "Plausibility floor changed — review whether the boundary tests "
        "still cover the right band of LLM error widths."
    )

    definition: Dict[str, Any] = {
        # Tiny canvas so the inflated minimum (460 px) is guaranteed to overflow.
        "canvasSettings": {"width": 200, "height": 600},
        "pages": [
            {
                "id": "page-1",
                "components": [
                    {
                        "id": "broken-1",
                        "type": "text",
                        "position": {"x": 10, "y": 10},
                        # Implausibly small — the compiler would never emit this,
                        # so we treat it as "no useful width" and fall back to
                        # the minimum render width for boundary purposes.
                        "style": {"width": 5, "height": 117},
                        "props": {"label": "Broken"},
                    },
                ],
            }
        ],
    }
    violations = _collect_visual_boundary_violations(definition, runtime_context=None)
    assert len(violations) == 1, (
        "Implausibly small stated widths must fall back to the minimum "
        "render width so degenerate LLM output still trips the boundary check."
    )


# --- UAT round 5 (run 42 follow-up) — locale-aware system prompt ----------


def test_locale_block_au_uses_story_644_one_line_directive():
    """Story 6.4.4 shrinks the AU/NZ locale prompt to one directive while
    keeping the same address, phone, date, and spelling intent."""
    from modules.form_ai.service import _build_locale_prompt_block

    block = _build_locale_prompt_block("AU")
    assert block == (
        "Form audience: Australia/New Zealand. Use AU/NZ spelling, address, "
        "phone, date conventions."
    )


def test_locale_block_opt_out_returns_empty_string():
    """``locale_code=None`` and unknown codes return the empty string so
    test fixtures and special tenants can disable locale guidance cleanly
    without bleeding US defaults back in by accident."""
    from modules.form_ai.service import _build_locale_prompt_block

    assert _build_locale_prompt_block(None) == ""
    assert _build_locale_prompt_block("ZZ") == ""
    assert _build_locale_prompt_block("") == ""


def test_initial_messages_default_to_au_locale():
    """Until country plumbing lands, every request gets the compact AU/NZ
    directive by default."""
    from modules.form_ai.service import _build_initial_messages

    messages = _build_initial_messages(
        prompt="Build a contact form",
        context_pack="(context pack stub)",
        runtime_context={"canvas": {"width": 1280, "height": 720}, "device": "desktop"},
    )
    system_msg = messages[0]["content"]
    assert "Form audience: Australia/New Zealand" in system_msg
    assert "AU/NZ spelling, address, phone, date conventions" in system_msg
    # Sanity: still includes the structural rules (locale block was injected,
    # not substituted).
    assert "REQUIRED ROOT KEYS" in system_msg
    assert "FormSemanticPlan" in system_msg


def test_initial_messages_locale_can_be_disabled_per_call():
    """Pass ``locale_code=None`` to opt out for a specific request (e.g. a
    test fixture that wants to assert a regression independent of locale
    copy)."""
    from modules.form_ai.service import _build_initial_messages

    messages = _build_initial_messages(
        prompt="Build a contact form",
        context_pack="(context pack stub)",
        runtime_context=None,
        locale_code=None,
    )
    system_msg = messages[0]["content"]
    assert "Postcode" not in system_msg
    assert "AU/NZ" not in system_msg
    # Structural rules must still be present.
    assert "REQUIRED ROOT KEYS" in system_msg
