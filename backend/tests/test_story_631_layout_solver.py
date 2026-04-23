"""Story 6.3.1 Phase 2 — row solver invariants.

Pins the behavior of the 3-state per-row solver added to
``modules.form_ai.compiler.flush_row``:

* ``fit``    — the row fits at every component's tier ``target_px``.
* ``shrink`` — the row only fits after proportional shrink toward each
                component's tier ``min_px``.
* ``reflow`` — the row cannot fit even at min widths and the trailing
                components were split off to a new sub-row.

It also pins the diagnostic surface (``compileSummary.rowSolverDecisions`` and
``compileSummary.rowGroupSplits``) so dashboards can rely on them.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from modules.form_ai.compiler import (
    DEFAULT_COLUMN_GAP,
    DEFAULT_MARGIN_X,
    MIN_COLUMN_GAP,
    compile_semantic_plan_to_definition,
)
from modules.form_ai.schemas import FormSemanticPlan


# --- Helpers ----------------------------------------------------------------


def _governance() -> Dict[str, Any]:
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
                {"type": "dropdown", "widthClasses": ["compact", "half", "full"]},
                {"type": "submit-button", "widthClasses": ["compact", "half"]},
            ],
        },
        "validationContracts": [
            {"componentType": "text", "allowedRules": ["required", "maxLength"]},
            {"componentType": "email", "allowedRules": ["required", "email", "maxLength"]},
            {"componentType": "phone", "allowedRules": ["required", "phone", "maxLength"]},
            {"componentType": "dropdown", "allowedRules": ["required"]},
            {"componentType": "submit-button", "allowedRules": []},
            {"componentType": "header", "allowedRules": []},
        ],
    }


def _compile(
    plan_payload: Dict[str, Any], *, canvas_width: int = 1920
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    plan = FormSemanticPlan.model_validate(plan_payload)
    g = _governance()
    return compile_semantic_plan_to_definition(
        plan,
        runtime_context={"canvas": {"width": canvas_width, "height": 980, "gridSize": 8}},
        capability_policy_json=g["capabilityPolicyJson"],
        width_policy_json=g["widthClassPolicyJson"],
        capability_snapshot_json=g["componentCapabilitySnapshotJson"],
        validation_contracts=g["validationContracts"],
    )


def _decisions(summary: Dict[str, Any]) -> List[Dict[str, Any]]:
    decisions = summary.get("rowSolverDecisions")
    assert isinstance(decisions, list), "rowSolverDecisions must be present in compileSummary"
    return decisions


def _splits(summary: Dict[str, Any]) -> List[Dict[str, Any]]:
    splits = summary.get("rowGroupSplits")
    assert isinstance(splits, list), "rowGroupSplits must be present in compileSummary"
    return splits


def _no_overlap(components: List[Dict[str, Any]]) -> None:
    """Pixel-perfect non-overlap assertion for a compiled definition."""
    for i, a in enumerate(components):
        ax1 = a["position"]["x"]
        ay1 = a["position"]["y"]
        ax2 = ax1 + a["style"]["width"]
        ay2 = ay1 + a["style"]["height"]
        for b in components[i + 1:]:
            bx1 = b["position"]["x"]
            by1 = b["position"]["y"]
            bx2 = bx1 + b["style"]["width"]
            by2 = by1 + b["style"]["height"]
            assert not (ax1 < bx2 and bx1 < ax2 and ay1 < by2 and by1 < ay2), (
                f"overlap detected: {a['id']} {a['position']}+{a['style']} "
                f"vs {b['id']} {b['position']}+{b['style']}"
            )


def _within_canvas(
    components: List[Dict[str, Any]], canvas_w: int
) -> None:
    """Right edge must not exceed the editable content area on either side."""
    content_right = canvas_w - DEFAULT_MARGIN_X
    for c in components:
        right = c["position"]["x"] + c["style"]["width"]
        assert c["position"]["x"] >= DEFAULT_MARGIN_X, (
            f"{c['id']} starts left of margin (x={c['position']['x']})"
        )
        assert right <= content_right + 0.5, (
            f"{c['id']} extends beyond content right edge "
            f"(right={right}, max={content_right})"
        )


# --- fit / shrink / reflow --------------------------------------------------


def test_solver_records_fit_when_row_fits_at_target() -> None:
    """A 2-up half/half row at 1920px wide fits at target tier widths
    (320 + 360 = 680 < ~1816 content width). Solver should report ``fit``."""
    plan = {
        "semanticPlanVersion": "1.0",
        "formId": "fit-row",
        "title": "Fit",
        "components": [
            {"componentType": "text",  "label": "First",  "widthIntent": "half", "section": "p", "rowGroup": "g1", "validationIntent": {"required": True, "maxLength": 40}},
            {"componentType": "email", "label": "Email",  "widthIntent": "half", "section": "p", "rowGroup": "g1", "validationIntent": {"required": True, "email": True, "maxLength": 80}},
            {"componentType": "submit-button", "label": "Submit", "widthIntent": "compact", "actionAlignment": "center", "section": "a"},
        ],
    }
    definition, summary = _compile(plan)
    items = definition["pages"][0]["components"]

    decisions = _decisions(summary)
    g1 = [d for d in decisions if d.get("rowGroup") == "g1"]
    assert len(g1) == 1, f"expected 1 sub-row for g1, got {g1}"
    assert g1[0]["decision"] == "fit", g1[0]
    assert len(g1[0]["componentIds"]) == 2
    assert g1[0]["widthSlack"] >= 0
    assert _splits(summary) == []
    _no_overlap(items)
    _within_canvas(items, 1920)


def test_solver_shrinks_when_targets_exceed_canvas() -> None:
    """4 email fields in one rowGroup at email-tier targets (360 each) need
    1512 px + gaps; on a 1280-wide canvas the available content is only
    1152 px so the solver must shrink (or reflow). Either is acceptable;
    ``fit`` is not — that would mean the row overflowed."""
    plan = {
        "semanticPlanVersion": "1.0",
        "formId": "shrink-row",
        "title": "Shrink",
        "components": [
            {"componentType": "email", "label": "Email 1", "widthIntent": "half", "section": "p", "rowGroup": "quad", "validationIntent": {"required": True, "email": True, "maxLength": 80}},
            {"componentType": "email", "label": "Email 2", "widthIntent": "half", "section": "p", "rowGroup": "quad", "validationIntent": {"email": True, "maxLength": 80}},
            {"componentType": "email", "label": "Email 3", "widthIntent": "half", "section": "p", "rowGroup": "quad", "validationIntent": {"email": True, "maxLength": 80}},
            {"componentType": "email", "label": "Email 4", "widthIntent": "half", "section": "p", "rowGroup": "quad", "validationIntent": {"email": True, "maxLength": 80}},
            {"componentType": "submit-button", "label": "Save", "widthIntent": "compact", "actionAlignment": "center", "section": "a"},
        ],
    }
    definition, summary = _compile(plan, canvas_width=1280)
    items = definition["pages"][0]["components"]

    decisions = _decisions(summary)
    quad = [d for d in decisions if d.get("rowGroup") == "quad"]
    assert len(quad) >= 1, f"no decisions recorded for rowGroup=quad: {decisions}"
    # Every recorded decision for this row group must be one of the solver's
    # known states. Critically, shrink or reflow (not fit) is the expected
    # outcome on a 1920-wide canvas with 4 half-tier fields.
    allowed = {"fit", "shrink", "reflow", "force-min"}
    for d in quad:
        assert d["decision"] in allowed, d
    decision_kinds = {d["decision"] for d in quad}
    assert decision_kinds & {"shrink", "reflow"}, (
        f"expected shrink or reflow, got {decision_kinds}"
    )
    _no_overlap(items)
    _within_canvas(items, 1280)


def test_solver_reflows_when_row_cannot_fit_even_after_shrink() -> None:
    """Force a true reflow by squeezing the canvas: 3 ``half`` text fields on
    a narrow canvas will not all fit even at min widths, so the solver must
    split the rowGroup across multiple sub-rows."""
    plan = {
        "semanticPlanVersion": "1.0",
        "formId": "reflow-row",
        "title": "Reflow",
        "components": [
            {"componentType": "text",  "label": "Field A", "widthIntent": "half", "section": "p", "rowGroup": "trio", "validationIntent": {"required": True, "maxLength": 40}},
            {"componentType": "text",  "label": "Field B", "widthIntent": "half", "section": "p", "rowGroup": "trio", "validationIntent": {"required": True, "maxLength": 40}},
            {"componentType": "text",  "label": "Field C", "widthIntent": "half", "section": "p", "rowGroup": "trio", "validationIntent": {"required": True, "maxLength": 40}},
            {"componentType": "submit-button", "label": "Save", "widthIntent": "compact", "actionAlignment": "center", "section": "a"},
        ],
    }
    # Narrow canvas: 720 wide → content_width = 720 - 2*64 = 592.
    # Three text fields at min_px=200 + 2 column gaps = 600+48 = 648 > 592 → reflow.
    definition, summary = _compile(plan, canvas_width=720)
    items = definition["pages"][0]["components"]

    splits = _splits(summary)
    trio_splits = [s for s in splits if s.get("originalRowGroup") == "trio"]
    assert trio_splits, f"expected rowGroup=trio to be split, got {splits}"
    assert trio_splits[0]["splitIntoRows"] >= 2

    decisions = _decisions(summary)
    trio_subrows = [d for d in decisions if d.get("rowGroup") == "trio"]
    assert len(trio_subrows) >= 2, (
        f"reflow should produce 2+ sub-rows for trio: {trio_subrows}"
    )
    _no_overlap(items)
    _within_canvas(items, 720)


# --- Diagnostic surface -----------------------------------------------------


def test_row_solver_decisions_records_one_entry_per_subrow() -> None:
    """The decision count must match the number of physical sub-rows the
    compiler emits (one banner + one rowGroup + one submit = 3)."""
    plan = {
        "semanticPlanVersion": "1.0",
        "formId": "diag-shape",
        "title": "Diag",
        "components": [
            {"componentType": "header", "label": "Welcome", "widthIntent": "full", "section": "intro"},
            {"componentType": "text",   "label": "First",   "widthIntent": "half", "section": "p", "rowGroup": "g1", "validationIntent": {"maxLength": 40}},
            {"componentType": "text",   "label": "Last",    "widthIntent": "half", "section": "p", "rowGroup": "g1", "validationIntent": {"maxLength": 40}},
            {"componentType": "submit-button", "label": "Go", "widthIntent": "compact", "actionAlignment": "center", "section": "a"},
        ],
    }
    _, summary = _compile(plan)
    decisions = _decisions(summary)
    assert len(decisions) == 3, decisions
    # Each entry has the contract dashboards depend on.
    for d in decisions:
        assert "decision" in d and isinstance(d["decision"], str)
        assert "componentIds" in d and isinstance(d["componentIds"], list)
        assert d["componentIds"], f"componentIds must be non-empty: {d}"
        assert "widthSlack" in d
        assert "rowGroup" in d
        assert "subRowIndex" in d
        assert "rowIndex" in d


def test_row_group_splits_empty_when_no_reflow_needed() -> None:
    """Happy-path layouts must not emit phantom split records."""
    plan = {
        "semanticPlanVersion": "1.0",
        "formId": "no-splits",
        "title": "No splits",
        "components": [
            {"componentType": "text",  "label": "First", "widthIntent": "half", "section": "p", "rowGroup": "g1", "validationIntent": {"maxLength": 40}},
            {"componentType": "email", "label": "Email", "widthIntent": "half", "section": "p", "rowGroup": "g1", "validationIntent": {"email": True, "maxLength": 80}},
            {"componentType": "submit-button", "label": "Save", "widthIntent": "compact", "actionAlignment": "center", "section": "a"},
        ],
    }
    _, summary = _compile(plan)
    assert _splits(summary) == []


# --- Banner isolation + section flush ---------------------------------------


def test_full_row_banner_is_always_isolated_even_with_neighbour() -> None:
    """A header (ALWAYS_FULL_WIDTH_TYPES) must own its row even if the next
    component shares the same (None) rowGroup. Pre-fix, the solver would
    proportionally shrink the header next to the email."""
    plan = {
        "semanticPlanVersion": "1.0",
        "formId": "banner-iso",
        "title": "Banner",
        "components": [
            {"componentType": "header", "label": "Welcome", "widthIntent": "full", "section": "intro"},
            {"componentType": "email",  "label": "Email",   "widthIntent": "half", "section": "intro", "validationIntent": {"required": True, "email": True, "maxLength": 80}},
            {"componentType": "submit-button", "label": "Go", "widthIntent": "compact", "actionAlignment": "center", "section": "a"},
        ],
    }
    definition, _ = _compile(plan)
    items = definition["pages"][0]["components"]
    by_label = {c["props"]["label"]: c for c in items}

    welcome = by_label["Welcome"]
    email = by_label["Email"]
    # Welcome must be on its own row (email starts strictly below it).
    assert email["position"]["y"] >= welcome["position"]["y"] + welcome["style"]["height"], (
        f"banner did not isolate: welcome={welcome['position']}, email={email['position']}"
    )
    _no_overlap(items)


def test_section_change_flushes_pending_row() -> None:
    """Two text inputs in different sections (and rowGroup=None) must not
    share a row. The section boundary is a flush trigger."""
    plan = {
        "semanticPlanVersion": "1.0",
        "formId": "section-flush",
        "title": "Section flush",
        "components": [
            {"componentType": "text",  "label": "Name",   "widthIntent": "half", "section": "person",  "validationIntent": {"required": True, "maxLength": 40}},
            {"componentType": "email", "label": "Email",  "widthIntent": "half", "section": "contact", "validationIntent": {"required": True, "email": True, "maxLength": 80}},
            {"componentType": "submit-button", "label": "Go", "widthIntent": "compact", "actionAlignment": "center", "section": "a"},
        ],
    }
    definition, _ = _compile(plan)
    items = definition["pages"][0]["components"]
    by_label = {c["props"]["label"]: c for c in items}

    name = by_label["Name"]
    email = by_label["Email"]
    assert email["position"]["y"] > name["position"]["y"], (
        f"section change did not flush row: name={name['position']}, email={email['position']}"
    )
    # And they should not share a horizontal band that would collide.
    assert email["position"]["y"] >= name["position"]["y"] + name["style"]["height"], (
        f"section flush left rows overlapping vertically: "
        f"name={name['position']}+{name['style']}, email={email['position']}+{email['style']}"
    )


# --- Aligned-grid invariants (UAT round 3) ----------------------------------


def test_multi_row_pins_to_left_margin_and_uses_min_column_gap() -> None:
    """UAT round 3 alignment policy: a multi-row's column-0 left edge sits at
    DEFAULT_MARGIN_X, and the inter-column gap is exactly MIN_COLUMN_GAP.
    Slack falls on the right (consistent with solo-row left-pin).
    """
    plan = {
        "semanticPlanVersion": "1.0",
        "formId": "aligned-grid-multi",
        "title": "Aligned grid multi",
        "components": [
            {"componentType": "email", "label": "A", "widthIntent": "half", "section": "p", "rowGroup": "g1", "validationIntent": {"email": True, "maxLength": 80}},
            {"componentType": "email", "label": "B", "widthIntent": "half", "section": "p", "rowGroup": "g1", "validationIntent": {"email": True, "maxLength": 80}},
            {"componentType": "submit-button", "label": "Go", "widthIntent": "compact", "actionAlignment": "center", "section": "a"},
        ],
    }
    definition, _ = _compile(plan, canvas_width=1920)
    items = definition["pages"][0]["components"]
    by_label = {c["props"]["label"]: c for c in items}

    a = by_label["A"]
    b = by_label["B"]
    assert a["position"]["y"] == b["position"]["y"], "row must be coplanar"

    # Column-0 pinned to left margin.
    assert a["position"]["x"] == DEFAULT_MARGIN_X, (
        f"column-0 should pin to MARGIN_X={DEFAULT_MARGIN_X}, got {a['position']['x']}"
    )
    # Inter-column gap equals MIN_COLUMN_GAP exactly (within rounding).
    interior_gap = b["position"]["x"] - (a["position"]["x"] + a["style"]["width"])
    assert abs(interior_gap - MIN_COLUMN_GAP) <= 1, (interior_gap, MIN_COLUMN_GAP)


def test_solo_rows_share_a_common_left_edge() -> None:
    """Every solo (k=1) row's left edge sits at MARGIN_X, regardless of the
    component's natural width. Each component is given its own rowGroup so
    the compiler treats them as separate rows rather than packing them.
    Submit-button is excluded because its ``actionAlignment`` semantics
    ("center" by default) intentionally override the grid pin.
    """
    plan = {
        "semanticPlanVersion": "1.0",
        "formId": "aligned-grid-solo",
        "title": "Aligned grid solo",
        "components": [
            # Each solo input has a different natural width tier and a
            # distinct rowGroup so it stays on its own row.
            {"componentType": "email", "label": "Solo Email", "rowGroup": "r1"},
            {"componentType": "phone", "label": "Solo Phone", "rowGroup": "r2"},
            {"componentType": "address", "label": "Solo Address", "rowGroup": "r3"},
            {"componentType": "textarea", "label": "Solo Comments", "rowGroup": "r4"},
        ],
    }
    definition, _ = _compile(plan, canvas_width=1920)
    items = definition["pages"][0]["components"]

    for it in items:
        if it["type"] == "submit-button":
            continue
        assert it["position"]["x"] == DEFAULT_MARGIN_X, (
            f"solo row {it['props'].get('label')!r} did not pin to MARGIN_X — "
            f"got x={it['position']['x']}"
        )


def test_multi_rows_with_same_column_count_share_per_column_widths() -> None:
    """Two 2-column rows with different per-row natural widths should end up
    using the SAME column-0 width and the SAME column-1 width — that is the
    grid-alignment guarantee (column-1 of row A lines up under column-1 of
    row B). col_max wins per column position.
    """
    plan = {
        "semanticPlanVersion": "1.0",
        "formId": "aligned-grid-shared",
        "title": "Aligned grid shared",
        "components": [
            # Row 1 has narrower components (phone + first-name).
            {"componentType": "phone", "label": "Phone", "widthIntent": "half", "rowGroup": "r1"},
            {"componentType": "first-name", "label": "First", "widthIntent": "half", "rowGroup": "r1"},
            # Row 2 has wider components (email + url) — these set col_max.
            {"componentType": "email", "label": "Email", "widthIntent": "half", "rowGroup": "r2"},
            {"componentType": "url", "label": "Site", "widthIntent": "half", "rowGroup": "r2"},
        ],
    }
    definition, _ = _compile(plan, canvas_width=1920)
    items = definition["pages"][0]["components"]
    by_label = {c["props"]["label"]: c for c in items}

    # Column 0 of row 1 and row 2 must have the same width and same x.
    assert by_label["Phone"]["style"]["width"] == by_label["Email"]["style"]["width"]
    assert by_label["Phone"]["position"]["x"] == by_label["Email"]["position"]["x"]
    # Column 1 likewise.
    assert by_label["First"]["style"]["width"] == by_label["Site"]["style"]["width"]
    assert by_label["First"]["position"]["x"] == by_label["Site"]["position"]["x"]
    # And column-0 still pinned to MARGIN_X.
    assert by_label["Phone"]["position"]["x"] == DEFAULT_MARGIN_X


# --- Canvas grow (UAT round 3 W3) ------------------------------------------


def test_canvas_height_grows_when_content_exceeds_initial_height() -> None:
    """A form taller than the requested canvas height must grow the canvas to
    fit, with ``compileSummary.canvasHeightGrew=True``. The single-page
    constraint was removed in UAT round 3."""
    plan = {
        "semanticPlanVersion": "1.0",
        "formId": "tall-form",
        "title": "Tall",
        "components": [
            {"componentType": "header",   "label": "Welcome",   "rowGroup": "h"},
            {"componentType": "email",    "label": "Email",     "rowGroup": "r1"},
            {"componentType": "phone",    "label": "Phone",     "rowGroup": "r2"},
            {"componentType": "address",  "label": "Address",   "rowGroup": "r3"},
            {"componentType": "textarea", "label": "Comments 1", "rowGroup": "r4"},
            {"componentType": "textarea", "label": "Comments 2", "rowGroup": "r5"},
            {"componentType": "textarea", "label": "Comments 3", "rowGroup": "r6"},
            {"componentType": "submit-button", "label": "Submit", "actionAlignment": "center"},
        ],
    }
    # Mobile-sized canvas (390x800 simulated). Definitely too small for 3
    # textareas + header + inputs.
    definition, summary = _compile(plan, canvas_width=390)
    canvas = definition["canvasSettings"]
    assert summary["canvasHeightGrew"] is True, summary
    assert canvas["height"] > 800, (
        f"canvas should have grown above initial 800, got {canvas['height']}"
    )
    # Every component still inside the (now taller) canvas vertically.
    items = definition["pages"][0]["components"]
    for it in items:
        bottom = it["position"]["y"] + it["style"]["height"]
        assert bottom <= canvas["height"] + 0.5, (
            f"{it['id']} extends below canvas bottom: bottom={bottom}, canvas={canvas['height']}"
        )
