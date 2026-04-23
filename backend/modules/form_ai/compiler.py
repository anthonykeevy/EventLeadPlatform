import math
from typing import Any, Dict, List, Optional, Tuple

from .schemas import FormSemanticPlan, SemanticComponentIntent

DEFAULT_CANVAS_WIDTH = 1920
DEFAULT_CANVAS_HEIGHT = 980
DEFAULT_GRID_SIZE = 8
DEFAULT_GRID_COLUMNS = 12
DEFAULT_MARGIN_X = 40
DEFAULT_MARGIN_Y = 24
DEFAULT_ROW_GAP = 24
DEFAULT_COLUMN_GAP = 24
MIN_COLUMN_GAP = 24

# Story 6.3.1 grouping: extra spacing inserted before a row that begins a new
# semantic section (semantic.section change). Multiplier is applied on top of
# the base DEFAULT_ROW_GAP so the visual rhythm stays grid-snapped.
#
# UAT round 5 feedback (run 40): user observed the gap between Email (last row
# of "contact" section) and Company (first row of "company" section) was 48 px
# while every other inter-row gap was 24 px, and explicitly requested
# uniform gaps:
#
#   "Based on our calculation method the gap at the top and inbetween should
#    be identical?"
#
# Setting the multiplier to 1.0 collapses the section-leading gap to 0 (see
# ``leading_section_gap = (SECTION_GAP_MULTIPLIER - 1.0) * DEFAULT_ROW_GAP`` in
# ``flush_row``) so every inter-row gap is exactly ``DEFAULT_ROW_GAP``. The
# section-tracking diagnostic (``rowSolverDecisions[i].leadingSectionGap``)
# stays in place for future debugging — we just no longer add a visual rhythm
# gap. If we want a softer-than-2.0 multiplier in the future, the only place
# that needs to change is this constant.
SECTION_GAP_MULTIPLIER = 1.0

# Story 6.3.1 Phase 1 W1 — content-aware width tiers, per component type.
# Each entry is ``(min_px, target_px, max_px)`` describing the natural visual
# range for an input of that type. The compiler picks the tier's ``target_px``
# as the default width and may shrink toward ``min_px`` when the row needs to
# fit horizontally (Phase 2 solver). The LLM-supplied ``widthIntent`` is treated
# as a *cap* on ``max_px``, not a target — so the compiler owns layout and the
# LLM can only narrow a field, never widen one beyond its natural range.
#
# Numbers err on the generous side because real glyph width depends on the
# font; the goal is "no more 908 px first-name fields", not pixel-perfect
# typesetting. ``9999`` is shorthand for "unbounded — let the row solver use
# the full content width".
COMPONENT_WIDTH_TIERS: Dict[str, Tuple[float, float, float]] = {
    "text": (200.0, 320.0, 480.0),
    "first-name": (180.0, 260.0, 360.0),
    "last-name": (180.0, 260.0, 360.0),
    "email": (240.0, 360.0, 520.0),
    "phone": (200.0, 280.0, 360.0),
    "url": (240.0, 420.0, 600.0),
    "number": (160.0, 220.0, 320.0),
    "date": (160.0, 220.0, 320.0),
    "time": (160.0, 200.0, 280.0),
    # ``address`` is rendered as a single-line input in this app, so it never
    # needs the full row. UAT round 2 showed full-row addresses crowding the
    # canvas and leaving textarea / submit nowhere to go.
    "address": (360.0, 600.0, 900.0),
    "dropdown": (220.0, 360.0, 520.0),
    "select": (220.0, 360.0, 520.0),
    # ``textarea`` capped at 720 (was unbounded → content_width). On a 1920 px
    # canvas the previous max meant a single Comments box could eat 1816 px,
    # leaving the rest of the form starved. The renderer scrolls vertically,
    # so 720 is plenty of typing area.
    "textarea": (320.0, 480.0, 720.0),
    "checkbox": (220.0, 360.0, 9999.0),
    "radio": (220.0, 360.0, 9999.0),
    "rating": (240.0, 360.0, 520.0),
    "file-upload": (320.0, 480.0, 9999.0),
    "submit-button": (180.0, 280.0, 360.0),
    # Full-row banner-style components.
    "header": (320.0, 9999.0, 9999.0),
    "paragraph": (320.0, 9999.0, 9999.0),
    "divider": (320.0, 9999.0, 9999.0),
    "terms": (320.0, 9999.0, 9999.0),
}

# Generic catch-all when the LLM emits a componentType not in the tier table.
# Same shape as a generic text input so we never pick a degenerate width.
DEFAULT_WIDTH_TIER: Tuple[float, float, float] = (200.0, 320.0, 480.0)

# Labels that strongly suggest a "name" field even when the LLM uses a generic
# ``text`` componentType. Used to nudge generic text fields onto the narrower
# name tier so a "First name" field doesn't render as a 320 px input next to a
# 360 px email — visually unbalanced.
NAME_FIELD_LABELS = {
    "first name", "given name", "preferred name",
    "last name", "surname", "family name",
    "middle name", "middle initial",
    "full name", "name",
}

# Story 6.3.1 UAT round 4 — labels that strongly suggest a postal address even
# when the LLM picks ``componentType: textarea`` for them. Address is rendered
# as a single-line input in this app, so a 240 px tall multi-line textarea for
# "Address" both wastes vertical space and is semantically wrong (validation,
# autofill, and the address widget all assume single-line). When the label
# matches one of these phrases the compiler remaps to ``address`` early so the
# whole pipeline (tier widths, default heights, validation) uses the right type.
ADDRESS_FIELD_LABELS = {
    "address",
    "street", "street address",
    "mailing address", "postal address",
    "shipping address", "billing address",
    "home address", "work address",
    "delivery address",
}

# Story 6.3.1: components that must always span the full content width
# regardless of widthIntent (banners, dividers, terms blocks). The LLM emitting
# ``compact`` for a header is a category error — the compiler ignores it.
ALWAYS_FULL_WIDTH_TYPES = {"header", "paragraph", "divider", "terms"}

# Per-class width caps a widthIntent hint applies. Computed lazily from
# content_width inside ``_widthIntent_pixel_cap`` because the cap depends on
# the canvas.
WIDTHINTENT_COMPACT_CAP_PX = 360.0

# Glyph-width estimate used to shrink a field when ``validationIntent.maxLength``
# is small (e.g. a 2-char state code). Errs on the generous side — see comment
# above on COMPONENT_WIDTH_TIERS.
AVG_CHAR_PX = 9.0
LABEL_PADDING_PX = 32.0

# Story 6.3.1 (UAT round 7) — Fix E item 1: tighter padding used ONLY for the
# horizontal-stacked label band. The general ``LABEL_PADDING_PX = 32`` was too
# generous in horizontal mode — it added ~2 chars of right-side breathing room
# beyond the longest label, which on a typical form (longest label ≈ 25 chars)
# pushed the input column ~32 px to the right of the label text and felt like
# "the label-input gap is too wide". 16 px = ~1 char of breathing room, which
# matches the visual gap a designer would draw between a label and its input.
# The vertical-mode ``LABEL_PADDING_PX`` is left at 32 because labels there sit
# on their own line and the extra breathing room reads as comfortable margin
# rather than dead space.
HORIZONTAL_LABEL_BAND_PADDING_PX = 16.0

# Story 6.3.1 (UAT round 6) — Fix D: per-type "comfortable character count"
# table for horizontal-stacked input sizing.
#
# In horizontal-stacked grid mode every component renders as
# ``[ Label ][ Input ][ Validation ]`` on its own row. Without a per-type
# input-band size the input column either shrink-wraps to the browser default
# (~150 px <input> intrinsic — too narrow, what the user reported in UAT) or
# stretches to ``1fr`` (eats the entire leftover row — too wide and visually
# unbalanced). The fix is to give each input a content-aware target width
# derived from how many characters the field is realistically expected to
# hold.
#
# Each entry is ``(comfortable_chars, hard_max_chars)`` where:
#   * ``comfortable_chars`` is the P95-ish content length for that field
#     based on form-UX studies (Baymard Institute "Form Field Usability",
#     Nielsen Norman Group "Form Design Guidelines", and the GOV.UK Service
#     Manual field-length guidance). Numbers err slightly wide so a typical
#     value never touches the right edge of the input.
#   * ``hard_max_chars`` caps the rendered width even when the LLM-supplied
#     ``validationIntent.maxLength`` is silly-large (RFC 5321 lets emails be
#     254 chars long; rendering an email input that wide would dominate the
#     row and confuse the user — 80 chars covers the longest email anyone
#     has ever typed in real-world usage).
#
# Resolution per component:
#   * if ``validationIntent.maxLength`` provided:
#       ``chars = min(maxLength, hard_max)``
#   * else:
#       ``chars = comfortable``
#   ``input_band_px = ceil(chars * AVG_CHAR_PX + INPUT_BAND_PADDING_PX)``
#   ``input_band_px = clamp(input_band_px, tier.min, tier.max)``
#
# Examples (email tier = (240, 360, 520), comfortable = 32, hard_max = 80):
#   * email, no maxLength → 32 chars → 312 px (typical desktop email field)
#   * email, maxLength=254 → capped to 80 chars → 744 → tier-clamped to 520 px
#   * email, maxLength=50  → 50 chars → 474 px (LLM hint honoured, in tier)
#   * email, maxLength=20  → 20 chars → 204 → tier-clamped UP to 240 px
#
# Components not in this table fall back to the existing tier ``target_px``
# unchanged — that's the "no opinion, use the tier" path.
INPUT_COMFORTABLE_CHARS: Dict[str, Tuple[int, int]] = {
    # Names — Baymard P95 personal name ≈ 20 chars (longest legal names go to
    # ~30, hyphenated compounds ~25). 22/35 covers virtually every customer.
    "first-name": (22, 35),
    "last-name": (22, 35),
    # Generic text — the catch-all "Name", "Title", "Reference" etc. Errs
    # slightly wide so a free-text label never feels cramped.
    "text": (28, 50),
    # Email — RFC 5321 max is 254 but Baymard's analysis of real submissions
    # shows P95 ≈ 30 chars and P99 ≈ 50. 80 covers the longest emails seen
    # in production ("first.last@really.long.subdomain.example.com.au").
    "email": (32, 80),
    # Phone — international format with separators: "+61 4XX XXX XXX" or
    # "+1 (XXX) XXX-XXXX" ≈ 15-18 chars. 22 leaves room for extension.
    "phone": (18, 22),
    # URL — average shareable URL ≈ 30 chars; cap at 80 because any longer
    # URL is almost certainly being pasted, not typed, and the customer can
    # scroll within the input.
    "url": (40, 80),
    # Number — most numeric fields (age, quantity, count, amount) are <8
    # digits; 12 leaves room for currency formatting / thousands separators.
    "number": (12, 18),
    # Date / time — typed format is "DD/MM/YYYY" (10 chars) or "HH:MM" (5).
    # 12 / 14 lets a picker badge / icon sit comfortably alongside.
    "date": (12, 14),
    "time": (12, 14),
    # Address (single-line, this app) — typical street address line goes
    # ~30 chars ("123 Australia Avenue, Sydney"); 35/60 covers ParcelLocker
    # destinations and long suburb names.
    "address": (35, 60),
    # Dropdowns / selects — width is driven by the longest option label, not
    # by maxLength. We still record a default chars value so a dropdown with
    # no options yet (during AI generation) gets a sensible fallback width.
    # When ``options`` are provided in the semantic plan, the placement loop
    # passes ``options_max_chars`` to the estimator and that value wins
    # (capped at ``hard_max``) so a "Company size: 201-500 / 501-1000 /
    # Enterprise" dropdown ends up just wide enough for "Enterprise" rather
    # than the generic 22-char default (Fix E item 3).
    "dropdown": (22, 50),
    "select": (22, 50),
    # Rating — the input renders as a fixed row of icons (default 5 stars,
    # NPS-style scales go to 10/11). Each star is roughly ``RATING_ICON_PX``
    # wide, so the band is computed as
    #   ``rating_count * RATING_ICON_PX + INPUT_BAND_PADDING_PX``
    # in the placement loop using ``validationIntent.max`` as the icon count
    # when the LLM provides it. This chars entry is the fallback for the
    # case where no scale is supplied — covers a default 5-star widget
    # (5 * ~24 px ≈ 120 px which is just under what 12 chars resolves to).
    # ``hard_max = 24`` caps the band at ~240 px so an 11-point NPS scale
    # never balloons past two-and-a-half tier-min widths even if the LLM
    # forgot to set a maxLength hint (Fix E item 4).
    "rating": (12, 24),
    # Terms — a checkbox input. The "input" object is just the checkbox
    # control (~24 px wide); the visible width of the COMPONENT comes from
    # the consent text (which lives in the LABEL object, not here). 4 chars
    # leaves room for the checkbox + 1 char of focus-ring breathing room;
    # ``hard_max = 6`` is a paranoia cap so the checkbox never balloons.
    # Bounding-box width for terms is computed in a dedicated branch (Fix E
    # item 5) using the consent-text length for the label band.
    "terms": (4, 6),
}

# Story 6.3.1 (UAT round 7) — Fix E item 4: pixel width per icon for the
# rating component. Matches the default ``ratingIconSize`` (24 px) plus the
# 4 px gap the rating runtime renders between icons. Used together with
# ``validationIntent.max`` (or ``rating_count`` from the plan) to size the
# input band exactly to the visible row of icons.
RATING_ICON_PX = 28.0

# Story 6.3.1 (UAT round 7) — Fix E item 5: pixel width reserved for the
# terms checkbox itself (the "input" object). The checkbox glyph is ~16 px
# but the runtime renders it inside a focus-ring container that needs ~32 px
# to look balanced next to the consent text.
TERMS_CHECKBOX_BAND_PX = 32

# Padding inside the input band (left + right), accounts for the input's
# inner ``inputPaddingX`` plus the focus-ring breathing room. 24 px = 12 each
# side, which matches the default ``inputPaddingX = 12`` in the global
# styles. Keeping this in sync with the global style means the rendered
# input matches the band the compiler computes.
INPUT_BAND_PADDING_PX = 24.0

# Story 6.3.1 (UAT round 6) — Fix D: form-wide density preset multipliers
# for horizontal-stacked input bands. The renderer / form designer can pick
# one of these via ``globalStyles.horizontalInputBandPreset`` to scale all
# inputs at once without overriding individual per-type comfortable widths.
#
# Multipliers chosen so:
#   * "compact"  - dense form, e.g. internal data-entry, ~2/3 width chars
#   * "standard" - default, matches the Baymard P95-ish chars table
#   * "spacious" - marketing / lead-gen forms with breathing room
INPUT_BAND_PRESET_MULTIPLIERS: Dict[str, float] = {
    "compact": 0.80,
    "standard": 1.0,
    "spacious": 1.25,
}
DEFAULT_INPUT_BAND_PRESET = "standard"


def _resolve_input_band_preset_multiplier(
    runtime_context: Optional[Dict[str, Any]],
) -> float:
    """Pull ``globalStyles.horizontalInputBandPreset`` from the runtime
    context's locked globals (set on the form definition by the user) and
    map it to a chars-multiplier. Falls back to the standard 1.0 multiplier
    for unknown / missing presets so a typo in the form JSON degrades
    gracefully rather than producing degenerate widths.
    """
    if not isinstance(runtime_context, dict):
        return 1.0
    locked = runtime_context.get("lockedGlobals")
    if not isinstance(locked, dict):
        return 1.0
    global_styles = locked.get("globalStyles")
    if not isinstance(global_styles, dict):
        return 1.0
    preset = global_styles.get("horizontalInputBandPreset")
    if not isinstance(preset, str):
        return 1.0
    return INPUT_BAND_PRESET_MULTIPLIERS.get(preset, 1.0)


def _estimate_horizontal_input_band_px(
    component_type: str,
    max_length: Optional[int],
    tier: Tuple[float, float, float],
    chars_multiplier: float = 1.0,
    options_max_chars: Optional[int] = None,
    rating_count: Optional[int] = None,
) -> int:
    """Return a content-aware input-band width (px) for horizontal-stacked
    grid mode.

    Resolution:
      1. Special-case the rating component (Fix E item 4): when a rating
         count is provided (from ``validationIntent.max`` or the rating
         scale), size the band to ``rating_count * RATING_ICON_PX +
         INPUT_BAND_PADDING_PX``. This is a fixed-icon control so the
         comfortable-chars table doesn't apply and tier clamps are skipped
         (the icon row is the natural width by definition).
      2. Look up ``INPUT_COMFORTABLE_CHARS[type] = (comfortable, hard_max)``.
      3. For dropdown/select with ``options_max_chars`` (Fix E item 3): use
         the longest option label length (capped at ``hard_max``) as the
         chars count instead of the generic ``comfortable`` default. This
         makes a "201-500" dropdown render at ~7 chars wide instead of the
         22-char default.
      4. Otherwise pick ``chars = min(max_length, hard_max)`` if max_length
         supplied, else ``comfortable``.
      5. Convert to pixels: ``ceil(chars * AVG_CHAR_PX + INPUT_BAND_PADDING_PX)``.
      6. Clamp to ``[tier.min, tier.max]`` so the band still respects the
         component-type's natural visual range (e.g. a 2-char state-code
         input never collapses below ~160 px because the input control itself
         needs that much chrome to be usable).

    Components not in the chars table fall back to ``tier.target`` so the
    function is safe to call for every component type (returns the existing
    behaviour for unknown types without forcing the caller to branch).
    """
    # Fix E item 4: rating uses a fixed-icon row, NOT a chars-driven width.
    # When the LLM supplies a scale (5-star, 10-point NPS, etc.) we size to
    # the icon row directly. We still clamp to a sane minimum so a 1-star
    # rating doesn't render as a 28-px tile that's hard to click; the tier
    # max cap is also honoured so an 11-point NPS doesn't balloon past the
    # input column the user expected.
    if component_type == "rating" and isinstance(rating_count, int) and rating_count > 0:
        # Apply the density preset to the icon count too — "compact" forms
        # use slightly smaller icons; "spacious" forms get more breathing
        # room around each star.
        effective_count = rating_count
        if chars_multiplier != 1.0 and chars_multiplier > 0:
            effective_count = max(1, int(round(rating_count * chars_multiplier)))
        band_px = float(effective_count) * RATING_ICON_PX + INPUT_BAND_PADDING_PX
        # Floor only — a rating component is naturally narrow and should not
        # be inflated up to ``tier.min`` (which is the text-input minimum,
        # ~220 px, and would force wasted whitespace around 5 stars).
        # Clamp to tier max so an 11-pt scale still fits the column.
        clamped = min(band_px, tier[2])
        return int(round(clamped))

    chars_entry = INPUT_COMFORTABLE_CHARS.get(component_type)
    if chars_entry is None:
        # Unknown / non-text component — defer to the tier's natural target.
        return int(round(tier[1]))

    comfortable, hard_max = chars_entry
    # Resolution rule (precedence — first match wins):
    #   * Dropdown/select with options: use the longest option label length,
    #     capped at ``hard_max``. This is the dominant signal for select
    #     widgets — the value is text the user reads, so the input must fit
    #     the option, not some abstract maxLength.
    #   * If the LLM supplied ``validationIntent.maxLength``, use it but cap
    #     at ``hard_max`` so a silly-large maxLength (e.g. RFC 5321's 254-
    #     char email upper bound) doesn't explode the input width.
    #   * Otherwise use ``comfortable`` — the per-type default.
    # Either way the result is then pixel-converted and tier-clamped, so a
    # tiny maxLength can't shrink an input below the tier min (the input
    # control needs a minimum amount of chrome to remain usable).
    options_driven_dropdown = (
        component_type in ("dropdown", "select")
        and isinstance(options_max_chars, int)
        and options_max_chars > 0
    )
    if options_driven_dropdown:
        chars = min(options_max_chars, hard_max)
    elif max_length is not None and max_length > 0:
        chars = min(int(max_length), hard_max)
    else:
        chars = comfortable
    chars = max(1, chars)

    # Apply the form-wide density preset (Fix D, item 4). Multiplier is
    # applied to the chars count BEFORE the px conversion + tier clamp so a
    # "compact" preset can shrink an email below its tier target (down to
    # tier.min) and a "spacious" preset can stretch it up to tier.max.
    if chars_multiplier != 1.0 and chars_multiplier > 0:
        chars = max(1, int(round(chars * chars_multiplier)))

    band_px = float(chars) * AVG_CHAR_PX + INPUT_BAND_PADDING_PX
    # Story 6.3.1 (UAT round 8) — Fix F item 1: options-driven dropdowns skip
    # the ``tier[0]`` floor and use a narrow chrome floor instead. The user
    # asked in UAT round 7 (item 4): "the Dropdown input object normally
    # automatically resizes based on the longest option in the Dropdown" —
    # ``COMPONENT_WIDTH_TIERS["dropdown"][0] = 220`` was the *vertical-mode*
    # input minimum (where the dropdown sits on its own row), not the
    # horizontal-mode minimum (where every column is sized to its content).
    # Pinning to 220 px would render a "201-500" company-size dropdown at
    # the same width as a "1001-5000-chars" textarea, defeating the UAT
    # round 7 ask. The narrow floor (= the natural chrome of a closed
    # dropdown — border + arrow + 1 char of padding) is just enough that
    # the arrow stays visible even on the shortest option.
    if options_driven_dropdown:
        narrow_floor_px = AVG_CHAR_PX + INPUT_BAND_PADDING_PX  # ~33 px
        clamped = max(narrow_floor_px, min(band_px, tier[2]))
    else:
        clamped = max(tier[0], min(band_px, tier[2]))
    return int(round(clamped))


def _longest_option_chars(options: Optional[List[Any]]) -> Optional[int]:
    """Return the length (in chars) of the longest option label in
    ``options`` or ``None`` if the list is empty/missing.

    Each option is expected to be a dict with ``label`` and/or ``value``
    keys (the LLM emits ``[{"label": "201-500", "value": "201-500"}, ...]``)
    but plain strings are accepted too as a robustness measure — the LLM
    occasionally drops the dict wrapper for short option lists. ``label``
    wins over ``value`` when both are present because ``label`` is what the
    user reads in the dropdown.
    """
    if not isinstance(options, list) or len(options) == 0:
        return None
    longest = 0
    for option in options:
        text: Optional[str] = None
        if isinstance(option, dict):
            for key in ("label", "value", "text"):
                candidate = option.get(key)
                if isinstance(candidate, str) and candidate.strip():
                    text = candidate.strip()
                    break
            if text is None:
                # Last-ditch: stringify any non-empty value so a malformed
                # option (e.g. ``{"id": 1}``) still contributes a width.
                for candidate in option.values():
                    if candidate is None:
                        continue
                    text = str(candidate).strip()
                    if text:
                        break
        elif isinstance(option, str):
            text = option.strip()
        elif option is not None:
            text = str(option).strip()
        if text:
            longest = max(longest, len(text))
    return longest if longest > 0 else None


def _resolve_rating_count(intent: SemanticComponentIntent) -> Optional[int]:
    """Return the rating-scale count for ``intent`` or ``None`` if it can't
    be determined.

    Resolution order (first match wins):
      1. ``validationIntent.max`` — the canonical schema field for "the
         largest legal value", which for a rating is the top of the scale.
      2. Free-form attributes the LLM commonly emits (``maxRating``,
         ``ratingScale``, ``scale``, ``maxValue``) — the schema's
         ``extra="allow"`` lets these flow through, so we accept them as
         a robustness measure rather than forcing a re-prompt.
      3. ``len(options)`` — labelled scales (``[{label:"Not likely"}, ...]``)
         encode the scale length in the option list itself.

    Returns an int in ``[1, 11]`` or ``None`` (the ``11`` upper bound covers
    the standard NPS 0–10 scale; anything larger is almost certainly an LLM
    confusion between rating and a different control type).
    """
    candidate: Optional[int] = None
    if intent.validationIntent is not None and intent.validationIntent.max is not None:
        try:
            candidate = int(intent.validationIntent.max)
        except (TypeError, ValueError):
            candidate = None

    if candidate is None:
        extras = intent.model_extra or {}
        for key in ("maxRating", "ratingScale", "scale", "maxValue"):
            raw = extras.get(key)
            if raw is None:
                continue
            try:
                candidate = int(raw)
                break
            except (TypeError, ValueError):
                continue

    if candidate is None and isinstance(intent.options, list) and intent.options:
        candidate = len(intent.options)

    # Story 6.3.1 (UAT round 8) — Fix F item 1b: default to 5 stars when the
    # LLM emits a bare ``rating`` component with no scale info. The renderer's
    # default rating control is a 5-star scale, so 5 matches what the user
    # actually sees in the canvas. Without this default, ``_estimate_horizontal
    # _input_band_px`` would fall through to the chars-table path
    # (12 comfortable chars → 132 px → tier-clamped to ~240 px) and the input
    # band would no longer be the icon-tight width the user requested in
    # UAT round 7 ("the Rating component automatically resizes the Input to
    # house the icons"). Returning ``None`` here would re-introduce the
    # "rating is the same width as everything else" symptom from UAT round 8.
    if candidate is None:
        candidate = 5
    # Out-of-range values almost always mean the LLM confused ``rating`` with
    # a different control (e.g. emitted ``max: 100`` for a numeric input
    # mislabelled as ``rating``). Snap back to the renderer-default 5-star
    # scale so the icon-sized band is still applied.
    if candidate < 1 or candidate > 11:
        candidate = 5
    return candidate


COMPONENT_TYPES_WIDTH_AWARE = {
    "text",
    "first-name",
    "last-name",
    "email",
    "phone",
    "url",
    "number",
    "date",
    "time",
    "address",
    "dropdown",
    "select",
}


def _estimate_validation_band_px(
    component_props: Dict[str, Any],
    *,
    min_px: float,
    max_px: float,
) -> int:
    """Story 6.3.1 (UAT round 8) — Fix F item 2: content-aware validation
    column width.

    Returns the natural width (in CSS px) the validation column needs to
    render the longest validator message for ``component_props`` on a single
    line, clamped to ``[min_px, max_px]``.

    Resolution:
      1. If ``props.validation.rules`` is a structured list (rare — mostly
         hand-authored DefinitionJSON) walk every rule and pick the longest
         ``message`` string verbatim.
      2. Otherwise treat ``props.validation`` as the flat normalized intent
         the compiler emits (``{"required": True, "maxLength": 50, ...}``)
         and synthesize the message text the runtime ``validationEngine``
         would render for each active rule (see
         ``frontend/.../validationEngine.ts``). The longest synthesized
         message is the binding constraint because the renderer shows them
         one at a time.
      3. If the component has no validation rules at all, fall back to
         ``DEFAULT_VALIDATION_PLACEHOLDER_CHARS`` so the column still has
         room for the renderer's "Validation error message" placeholder
         shown in builder mode.
      4. Convert chars → px: ``chars * AVG_CHAR_PX + INPUT_BAND_PADDING_PX``.
      5. Clamp to ``[min_px, max_px]``. The caller passes the available
         remaining content_width as ``max_px`` so the column can never push
         the bounding box past the canvas edge — the surrounding placement
         loop handles drop-below when the clamped value is still too wide.

    Why this matters: Fix E item 2 (UAT round 7) pinned this column at a
    fixed 200 px to stop validation messages from wrapping on inputs with
    short rules ("Required"), but UAT round 8 showed that real validators
    (e.g. ``maxLength`` with the default message "Must be no more than 50
    characters") emit ~32-char messages that still wrapped at 200 px. The
    user explicitly asked for auto-grow with collision-aware fallback in
    UAT round 8 (item 3): "allow the validation object to auto grow to
    support the longest validation message. If the growth of the validation
    object causes the component to collide with other components or the
    canvas border then it should be reduced in width to avoid collisions".
    """
    longest_chars = 0
    validation_block = component_props.get("validation")
    if isinstance(validation_block, dict):
        rules = validation_block.get("rules")
        if isinstance(rules, list) and rules:
            # Path 1: structured rules with explicit messages.
            for rule in rules:
                if not isinstance(rule, dict):
                    continue
                message = rule.get("message")
                if isinstance(message, str) and message.strip():
                    longest_chars = max(longest_chars, len(message.strip()))
        else:
            # Path 2: flat normalized intent from
            # ``_normalize_validation_intent``. Synthesize the runtime
            # message for each active rule.
            for rule_chars in _synthesize_validation_message_chars(
                validation_block
            ):
                longest_chars = max(longest_chars, rule_chars)

    if longest_chars <= 0:
        longest_chars = DEFAULT_VALIDATION_PLACEHOLDER_CHARS

    band_px = float(longest_chars) * AVG_CHAR_PX + INPUT_BAND_PADDING_PX
    clamped = max(min_px, min(band_px, max_px))
    return int(round(clamped))


def _synthesize_validation_message_chars(
    flat_validation: Dict[str, Any],
) -> List[int]:
    """Return the rendered char-length of every active rule in
    ``flat_validation`` (the compiler-emitted normalized intent), using the
    same default messages the runtime ``validationEngine.ts`` would render.

    Kept in lockstep with ``frontend/src/features/builder/utils/validationEngine.ts``
    — when a new rule message is added/changed there, mirror the char count
    here. We track CHAR COUNTS rather than the literal strings because (a)
    the compiler doesn't render text and (b) the only thing the band sizing
    cares about is the longest single-line width.
    """
    chars: List[int] = []

    # ``required`` → "This field is required" (22 chars). Common short
    # message — included to keep the floor sane on rule-free required
    # inputs (along with the placeholder default).
    if flat_validation.get("required") is True:
        chars.append(len("This field is required"))

    # ``minLength`` → "Must be at least N characters"
    min_length = flat_validation.get("minLength")
    if isinstance(min_length, int) and min_length > 0:
        chars.append(len(f"Must be at least {min_length} characters"))

    # ``maxLength`` → "Must be no more than N characters"
    max_length = flat_validation.get("maxLength")
    if isinstance(max_length, int) and max_length > 0:
        chars.append(len(f"Must be no more than {max_length} characters"))

    # ``min`` / ``max`` numeric ranges (rating, number) → "Must be at
    # least N" / "Must be no more than N"
    min_val = flat_validation.get("min")
    if isinstance(min_val, (int, float)):
        chars.append(len(f"Must be at least {min_val}"))
    max_val = flat_validation.get("max")
    if isinstance(max_val, (int, float)):
        chars.append(len(f"Must be no more than {max_val}"))

    # ``pattern`` → "Please match the requested format" (33 chars).
    if flat_validation.get("pattern"):
        chars.append(len("Please match the requested format"))

    # Catch-all: any boolean rule we don't have an explicit synthesizer for
    # (alpha, alphanumeric, ...) gets a generic 30-char placeholder so the
    # band still grows above the floor when those rules are active.
    GENERIC_RULE_CHARS = 30
    for key, value in flat_validation.items():
        if key in {"required", "minLength", "maxLength", "min", "max", "pattern"}:
            continue
        if value is True or (isinstance(value, str) and value.strip()):
            chars.append(GENERIC_RULE_CHARS)

    return chars

DEFAULT_THEME = {
    "primaryColor": "#0055FF",
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
}

# Story 6.3.1 Phase 1 W3 — default rendered heights aligned to actual runtime
# footprints. Toolbox-tile footprints (sourced from runtime ``componentFootprints``)
# only measure the closed control box; the rendered runtime adds label +
# validation chrome on top, and the form_validate collision check inflates short
# textareas to ~200. Picking a default that matches the rendered footprint
# avoids the "compiler thinks it's 109, validator inflates it to 200, layout
# overlaps" failure mode.
# Story 6.3.1 (UAT round 9) — Fix G item 4a: layout-mode-aware row heights.
#
# Background: ``DEFAULT_COMPONENT_HEIGHTS`` was tuned for VERTICAL layout
# where each component stacks ``[label] / [input] / [validation]`` inside
# its bounding box (~110 px for a typical text input). In horizontal-stacked
# mode those three objects share one row so the actual rendered footprint
# is closer to ~50 px. Reusing the vertical estimate as the horizontal
# row reservation produces ``9 components × (110 + 24 row gap) ≈ 1206 px``
# of vertical space when the rendered content only needs ``9 × ~74 ≈ 666 px``,
# which is exactly the "lots of space between all the components" + "canvas
# automatically increased the height" the user reported in UAT round 9.
#
# This separate horizontal table holds the per-type rendered height when
# label/input/validation share one row. ``_component_height`` consults the
# right table based on ``layout_mode``. Components whose intrinsic height
# is unchanged by horizontal mode (textarea body, file-upload drop zone,
# header/paragraph banners that are full-row regardless) keep the vertical
# value. The resulting tighter row reservations let the canvas grow only
# as much as the form actually needs, and the second-pass DOM measurements
# (``measured_heights``, render-then-measure pipeline) refine further.
DEFAULT_COMPONENT_HEIGHTS_HORIZONTAL = {
    "header": 56,
    "paragraph": 48,
    "divider": 20,
    "first-name": 52,
    "last-name": 52,
    "text": 52,
    "number": 52,
    "email": 52,
    "url": 52,
    "phone": 52,
    "date": 52,
    "address": 52,
    "dropdown": 52,
    "select": 52,
    "checkbox": 52,
    "radio": 52,
    "rating": 52,
    # Textarea body still grows vertically — it intentionally takes more
    # space for multi-line input. Keep the vertical default so the body
    # is tall enough to type into.
    "textarea": 200,
    # Submit button row stays compact in horizontal mode just like the
    # other inputs.
    "submit-button": 52,
    # Terms in horizontal mode is a single row of [checkbox][label][
    # validation]; keep height in line with other inputs even though
    # the consent text may wrap on narrow canvases.
    "terms": 52,
    # File-upload drop-zone is a meaningful vertical drop target —
    # keep the larger footprint.
    "file-upload": 132,
}


DEFAULT_COMPONENT_HEIGHTS = {
    "header": 56,
    "paragraph": 48,
    "divider": 20,
    # UAT round 4: 240 → 200. 240 was too tall for a single-purpose comments
    # box (user feedback: "comments dominates the canvas"). 180 was tried first
    # but the runtime DOM renders larger than that — label + textarea body +
    # validation chrome lands around 200 in practice — so the submit button
    # below the textarea ended up touching it visually. 200 matches the
    # validator's collision-inflation floor so authored ≈ rendered ≈ inflated.
    #
    # NOTE: This is the *input body* height for textarea — the renderer (see
    # ``StandardInput.tsx``) reads ``style.height`` and applies it directly to
    # the ``<textarea>`` element. Label and validation chrome are *added* on
    # top, so the on-screen component is taller than this value. The compiler
    # accounts for that via ``COMPONENT_RENDERED_CHROME_PX`` below.
    "textarea": 200,
    "checkbox": 120,
    "radio": 120,
    "rating": 88,
    # Submit button: ``style.height`` is the button-body height only. The
    # renderer wraps the button with a ``loading`` status slot and a
    # ``validation`` placeholder slot below, both of which add visible pixels.
    # We keep 72 here (so the rendered button looks the same as before) and
    # account for the chrome via ``COMPONENT_RENDERED_CHROME_PX``.
    "submit-button": 72,
    "terms": 120,
    "file-upload": 132,
}


# Story 6.3.1 UAT round 5 — rendered-chrome budget per component type.
#
# Background: the compiler's ``style.height`` for most components is the *whole
# rendered component height* (label + input + validation chrome already baked
# in). For a ``text`` input, the input body is a fixed ~40 px regardless of
# ``style.height``, so the heuristic 110 absorbs label (~32) + body (~40) +
# validation slot (~32) inside the bounding box and the next row sits cleanly
# 24 px below.
#
# A few component types break that assumption — their renderer interprets
# ``style.height`` as the *input body only* and stacks label + body + validation
# vertically. For these the on-screen component is taller than the JSON
# bounding box, so the next row visually overlaps even though the JSON math
# says there's a 24 px gap. Concretely:
#
#   * ``textarea``   — body grows with ``style.height``; label (~32) and
#                      validation slot (~32) plus inter-object spacing (~16)
#                      add ~80 px of chrome below/above the bounding box.
#   * ``submit-button`` — body is the button. Renderer adds a ``loading`` status
#                      slot (~16) and a ``validation`` slot (~32) below the
#                      button, plus inter-object spacing — ~48 px of chrome.
#   * ``file-upload`` — drop-zone is the body. Validation placeholder below
#                      adds ~32 px.
#
# The compiler uses this map *only* for vertical layout reservations
# (``row_height`` in ``flush_row``-time placement and ``max_bottom`` for canvas
# grow-to). The emitted ``style.height`` in the JSON is unchanged, so the
# renderer keeps painting the same input body height — the chrome simply
# occupies space that used to become collision.
COMPONENT_RENDERED_CHROME_PX: Dict[str, float] = {
    "textarea": 80.0,
    "submit-button": 48.0,
    "file-upload": 32.0,
}


def _row_chrome(component_type: str, *, layout_mode: str = "vertical-packed") -> float:
    """Return the rendered-chrome overhead (px) for ``component_type``.

    Returns 0 for component types whose ``style.height`` already represents
    the whole rendered footprint (text/email/phone/dropdown/etc. — see the
    ``COMPONENT_RENDERED_CHROME_PX`` docstring for the rationale).

    Story 6.3.1 (UAT round 9) — Fix G4a: in horizontal-stacked mode the
    label and validation render INLINE with the input (left/right
    columns), so the vertical chrome stack (label-above + validation-
    below) doesn't apply. Returns 0 in that mode for every component
    type — the bounding ``style.height`` already represents the rendered
    row height. Without this carve-out, horizontal forms over-reserve
    vertical space (e.g. ``textarea`` adds 80 px of phantom label +
    validation chrome that doesn't exist in horizontal mode), which is
    the "huge gaps between components" symptom from UAT round 9.
    """
    if layout_mode == LAYOUT_MODE_HORIZONTAL_STACKED:
        return 0.0
    return COMPONENT_RENDERED_CHROME_PX.get(component_type, 0.0)


def _reserved_height(item: Dict[str, Any], *, layout_mode: str = "vertical-packed") -> float:
    """Vertical space the layout solver must reserve for ``item``.

    Equals ``style.height`` plus the per-type rendered-chrome budget. Used
    everywhere ``row_height`` was previously computed straight from
    ``style.height`` so chrome no longer overflows into the next row.

    Story 6.3.1 (UAT round 9) — Fix G4a: ``layout_mode`` is propagated
    so horizontal mode skips the (vertical-only) chrome budget.
    """
    style_height = float(item["style"]["height"])
    return style_height + _row_chrome(
        str(item.get("type", "")).strip(),
        layout_mode=layout_mode,
    )


def _parse_positive_number(value: Any, fallback: float) -> float:
    if isinstance(value, (int, float)):
        number = float(value)
        return number if number > 0 else fallback
    if isinstance(value, str):
        candidate = value.strip().lower()
        if candidate.endswith("px"):
            candidate = candidate[:-2]
        try:
            parsed = float(candidate)
            return parsed if parsed > 0 else fallback
        except ValueError:
            return fallback
    return fallback


# Story 6.3.1 (UAT round 6) — layout-mode constants.
#
# Two placement strategies live side-by-side in the compiler. Which one
# runs is decided by ``resolve_layout_mode`` from the runtime context's
# ``defaultObjectLayout`` Global Style:
#
#   * ``vertical-packed`` (default): each input renders as
#     label-above-input and the aligned-grid row solver packs them by
#     ``rowGroup``. This is the original layout introduced in Story 6.3.1
#     Phase 2 and is the path every existing canvas form takes.
#
#   * ``horizontal-stacked``: each input renders as
#     ``[ Label ][ Input ][ Validation ]`` on its own row. The compiler
#     gives every component a full-width bounding box and the renderer's
#     CSS column split produces canvas-scaled label / input / validation
#     columns. ``rowGroup`` is ignored in this mode (single-column layout
#     by definition).
#
# A pre-flight downgrade in the AI panel + renderer keeps horizontal mode
# off canvases narrower than ``HORIZONTAL_LAYOUT_MIN_WIDTH_PX = 600`` so
# we never try to fit ``[ Label ][ Input ][ Validation ]`` into a 375 px
# mobile preview.
LAYOUT_MODE_VERTICAL_PACKED = "vertical-packed"
LAYOUT_MODE_HORIZONTAL_STACKED = "horizontal-stacked"


# ---------------------------------------------------------------------------
# Story 6.3.1 (UAT round 6) — Phase 2 *completion*: horizontal-stacked geometry
# ---------------------------------------------------------------------------
#
# In horizontal-stacked mode the renderer (``UniversalFieldShell.tsx`` →
# ``groupObjectsForLayout`` with ``layout === 'horizontal'``) puts every
# sub-object of a component (label, input, validation) into ONE row and
# lets CSS split them across the component's bounding box. So the
# compiler's job is simply to:
#
#   1. give each input component its OWN row (no horizontal packing —
#      the LLM nudge already says "do not use rowGroup" but we enforce
#      it here too so a stray rowGroup doesn't break the layout);
#
#   2. set ``style.width = content_width`` (the full row band) so the
#      renderer's column split has plenty of pixels to work with — that
#      auto-satisfies the user's "generous on wide, tighter on narrow"
#      label-band policy without us inventing a new sizing model;
#
#   3. detect when the row is too narrow to fit ``[ Label ][ Input ][
#      Validation ]`` inline, and reserve extra height so the renderer
#      can wrap the validation message below the input without the next
#      row colliding (this is the "drop below" branch the user asked
#      for in UAT round 6).
#
# Everything else (banner full-rows, submit-button alignment) inherits
# the vertical-mode policy.

# Per-row split assumption used ONLY for the inline-validation detection
# below. Conservatively assumes the renderer's default split allocates ~1/3
# of the bounding box to the label column. If the renderer ever ships a
# different default we widen this constant — never narrow it — because the
# detection prefers a false negative (validation drops below earlier than
# strictly necessary) over a false positive (validation crashes into the
# input). Not used for layout placement itself, only for the drop-below
# decision.
HORIZONTAL_LABEL_BAND_FRACTION = 1.0 / 3.0

# Visual gap between label / input / validation columns. Mirrors the
# renderer's default object-column gap so the detection uses the same
# arithmetic the browser will use.
HORIZONTAL_INTRA_GAP_PX = 16.0

# Minimum width (CSS px) the validation copy needs to render on one line
# without wrapping. ``"This field is required"`` is roughly 180 px at the
# default font; we give it 200 px of headroom.
HORIZONTAL_VALIDATION_MIN_PX = 200.0

# Story 6.3.1 (UAT round 8) — Fix F item 2: hard ceiling for the auto-grown
# validation column. Even when a validator emits a paragraph-length message
# (rare but legal), we don't let the validation column dominate the row —
# beyond ~480 px the message should wrap, not stretch every other column to
# the right. Picked to match the widest realistic single-line validation
# message in the seed validator catalog ("Please enter a valid Australian
# postcode (4 digits)" ≈ 56 chars at the default font).
HORIZONTAL_VALIDATION_MAX_PX = 480.0

# Story 6.3.1 (UAT round 8) — Fix F item 2: assumed validation length used
# only when the component has no validation rules at all. The runtime always
# reserves a slot for a possible "Validation error message" placeholder of
# ~24 chars, so the column needs at least that much room even on a
# rule-free input.
DEFAULT_VALIDATION_PLACEHOLDER_CHARS = 24

# Extra reserved height (CSS px) added to a component when the validation
# message has to wrap below the input instead of sitting next to it. Just
# enough for one validation line + 8 px breathing room.
HORIZONTAL_VALIDATION_DROP_HEIGHT_PX = 24

# Story 6.3.1 (UAT round 7) — Fix E item 5: full-row banner types in
# horizontal-stacked mode. ``terms`` was previously included here (it sits
# in ``ALWAYS_FULL_WIDTH_TYPES`` for vertical mode where the consent
# paragraph naturally fills the row), but in horizontal mode the renderer
# spreads its 3 sub-objects (checkbox + consent label + validation) across
# the full-row bounding box and leaves ~700 px of dead space between the
# checkbox and the text. The fix is to give terms its own tight bounding
# box in horizontal mode (handled by ``_compile_terms_horizontal_box``)
# and reserve this set strictly for banners that genuinely want a full row.
HORIZONTAL_MODE_BANNER_TYPES = {"header", "paragraph", "divider"}

# Story 6.3.1 (UAT round 6) — Fix C: form-wide horizontal label band.
#
# In horizontal-stacked grid mode every component renders as
# ``[ Label ][ Input ][ Validation ]`` on its own row. The renderer's CSS grid
# splits the bounding box across those three columns; without an explicit
# label-column width every label shrink-wraps to its own intrinsic glyph width
# and the input column starts at a different x for each component (visually
# ragged left-edge for the inputs). The fix is to compute a single label-band
# width once per form, derived from the longest label in the semantic plan
# (estimated via ``AVG_CHAR_PX``) and clamped to a canvas-aware band, and
# stamp it on ``globalStyles.horizontalLabelBandPx``. The renderer
# (``UniversalFieldShell.gridContent`` → ``resolveColumnTrack``) consumes that
# value as the label-column track width so every component lines up at the
# same input left-edge.
#
# Bounds rationale:
#   * ``MIN``: even a 1-char label needs room for the colon and visual breath
#     so the input doesn't kiss it. ~120 px is two short words at the default
#     font (e.g. "Email *").
#   * ``MAX``: prevents a single very-long label (e.g. "Are you currently
#     employed full-time, part-time, or seeking work?") from eating the input
#     column. ~280 px is roughly 25 chars at the default font — past that the
#     label will wrap to two lines inside the band, which is still readable
#     and lets the input keep enough width to be useful.
#   * ``CANVAS_FRACTION_CAP``: never let the label band exceed a third of the
#     usable canvas. On a 600 px mobile canvas this caps the band at 200 px;
#     on 1920 px desktop it's a soft 640 px cap that the absolute MAX already
#     subsumes.
HORIZONTAL_LABEL_BAND_MIN_PX = 120.0
HORIZONTAL_LABEL_BAND_MAX_PX = 280.0
HORIZONTAL_LABEL_BAND_CANVAS_FRACTION = 1.0 / 3.0


def _estimate_horizontal_label_band_px(
    semantic_plan: FormSemanticPlan,
    content_width: float,
) -> int:
    """Return a clamped pixel value for ``globalStyles.horizontalLabelBandPx``.

    Walks every component intent in ``semantic_plan`` and picks the maximum
    estimated label width (``len(label) * AVG_CHAR_PX +
    HORIZONTAL_LABEL_BAND_PADDING_PX``), then clamps to the bounds documented
    above. Returns an int because the value is consumed as a CSS pixel literal
    — sub-pixel precision adds noise without value.

    The padding constant is intentionally TIGHTER than the general
    ``LABEL_PADDING_PX`` (16 px vs. 32 px) — Fix E item 1, UAT round 7. In
    horizontal mode the gap between the label and the input is the entire
    "white space" the user perceives, and the previous 32 px padding made
    the label band feel ~1 char wider than the longest label. 16 px gives
    ~1 char of breathing room at the right edge of the band, which matches
    how a designer would draw the alignment by hand. The Layer-2 ``labelGap``
    style still adds the configured inter-column gap between this band and
    the input column on top of this padding.

    The ``"*"`` glyph is added to the chars count when ``required = True``
    on the intent's ``validationIntent`` because the renderer paints a
    required-marker after the label text — without this the band looked
    fine in tests (no required fields) but cropped the asterisk in real
    forms (every field required).

    Components without a label (display-only) are skipped. If no labels are
    present at all (extreme edge case, all-display form) we still return a
    sensible MIN-band fallback so the renderer never sees ``0``.
    """
    longest_label_chars = 0
    for intent in semantic_plan.components:
        # Story 6.3.1 (UAT round 8) — Fix F item 3: exclude ``terms`` from
        # the form-wide band. Terms uses its own per-row
        # ``labelWidthOverride`` (Fix E item 5) sized to the consent
        # paragraph, which is structurally much longer than other labels.
        # If we let the consent text dominate the form-wide band, every
        # other row gets pushed N px to the right of where it actually
        # needs to be, and the user perceives the input column as
        # "starting too far right" — exactly the "label-input gap is too
        # wide" symptom reported in UAT round 8 (issue 2). The terms row
        # itself is unaffected because its ``labelWidthOverride`` wins
        # over the form-wide band per the Fix B precedence chain.
        if intent.componentType == "terms":
            continue
        label = (intent.label or "").strip()
        if not label:
            continue
        # Required-marker contribution: the renderer appends " *" to required
        # labels, so count those 2 chars when sizing the band — otherwise the
        # band crops the asterisk on the longest required label.
        required_marker_chars = 0
        if intent.validationIntent is not None and intent.validationIntent.required:
            required_marker_chars = 2
        longest_label_chars = max(
            longest_label_chars, len(label) + required_marker_chars
        )

    estimated_label_width = (
        longest_label_chars * AVG_CHAR_PX + HORIZONTAL_LABEL_BAND_PADDING_PX
        if longest_label_chars > 0
        else HORIZONTAL_LABEL_BAND_MIN_PX
    )

    canvas_cap = max(
        HORIZONTAL_LABEL_BAND_MIN_PX,
        content_width * HORIZONTAL_LABEL_BAND_CANVAS_FRACTION,
    )

    clamped = max(
        HORIZONTAL_LABEL_BAND_MIN_PX,
        min(
            estimated_label_width,
            HORIZONTAL_LABEL_BAND_MAX_PX,
            canvas_cap,
        ),
    )
    return int(round(clamped))


def resolve_layout_mode(
    runtime_context: Optional[Dict[str, Any]],
) -> str:
    """Return the canonical layout mode for this generation.

    Looks at ``runtime_context.lockedGlobals.globalStyles.defaultObjectLayout``
    and maps the only "horizontal-ish" value the form builder produces today
    (the literal string ``"horizontal"``) to ``LAYOUT_MODE_HORIZONTAL_STACKED``.
    Everything else — ``"vertical"``, ``"mixed"``, missing, ``None``, an
    unknown future token — is treated as the default vertical mode so a typo
    in stored config can never accidentally route to an unimplemented branch.

    The frontend's Phase 1 pre-flight downgrade (``buildRuntimeContext`` in
    ``AIAgentPanel.tsx``) is responsible for *changing* horizontal→vertical
    when the canvas is too narrow; this function only *reads* whatever the
    request shipped with.
    """
    if not isinstance(runtime_context, dict):
        return LAYOUT_MODE_VERTICAL_PACKED
    locked_globals = runtime_context.get("lockedGlobals")
    if not isinstance(locked_globals, dict):
        return LAYOUT_MODE_VERTICAL_PACKED
    global_styles = locked_globals.get("globalStyles")
    if not isinstance(global_styles, dict):
        return LAYOUT_MODE_VERTICAL_PACKED
    raw = global_styles.get("defaultObjectLayout")
    if isinstance(raw, str) and raw.strip().lower() == "horizontal":
        return LAYOUT_MODE_HORIZONTAL_STACKED
    return LAYOUT_MODE_VERTICAL_PACKED


def _runtime_footprint_map(
    runtime_context: Optional[Dict[str, Any]],
) -> Dict[str, Dict[str, float]]:
    if not isinstance(runtime_context, dict):
        return {}
    footprints = runtime_context.get("componentFootprints")
    if not isinstance(footprints, list):
        return {}
    mapped: Dict[str, Dict[str, float]] = {}
    for row in footprints:
        if not isinstance(row, dict):
            continue
        component_type = str(row.get("componentType", "")).strip()
        if not component_type:
            continue
        width = _parse_positive_number(row.get("width"), 0.0)
        height = _parse_positive_number(row.get("height"), 0.0)
        gap = _parse_positive_number(row.get("recommendedGapAfter"), 0.0)
        if width <= 0 or height <= 0:
            continue
        mapped[component_type] = {
            "width": width,
            "height": height,
            "recommendedGapAfter": gap,
        }
    return mapped


def _allowed_width_intents(
    component_type: str, snapshot_json: Optional[Dict[str, Any]]
) -> List[str]:
    default = ["compact", "half", "full"]
    if not isinstance(snapshot_json, dict):
        return default
    components = snapshot_json.get("components")
    if not isinstance(components, list):
        return default
    for row in components:
        if not isinstance(row, dict):
            continue
        if str(row.get("type", "")).strip() != component_type:
            continue
        width_classes = row.get("widthClasses")
        if isinstance(width_classes, list):
            normalized = [str(item).strip() for item in width_classes if str(item).strip()]
            return normalized or default
    return default


def _normalize_width_intent(
    requested: Optional[str],
    component_type: str,
    canvas_width: float,
    width_policy_json: Optional[Dict[str, Any]],
    snapshot_json: Optional[Dict[str, Any]],
) -> str:
    """Resolve the canonical widthIntent the compiler should *report* for a
    component (used for diagnostics and as the cap source). Layout itself is
    driven by ``COMPONENT_WIDTH_TIERS`` — this function only governs the cap
    chosen and the value surfaced in stageDiagnostics.
    """
    allowed = _allowed_width_intents(component_type, snapshot_json)
    width_intent = requested if isinstance(requested, str) else None
    if width_intent not in {"compact", "half", "full"}:
        width_intent = "full" if component_type in ALWAYS_FULL_WIDTH_TYPES else "half"
    if width_intent not in allowed:
        # deterministic fallback preference from widest to narrowest
        for candidate in ("full", "half", "compact"):
            if candidate in allowed:
                width_intent = candidate
                break

    downgrade_rules: List[Dict[str, Any]] = []
    if isinstance(width_policy_json, dict):
        rules = width_policy_json.get("downgradeRules")
        if isinstance(rules, list):
            downgrade_rules = [row for row in rules if isinstance(row, dict)]

    for rule in downgrade_rules:
        rule_if = str(rule.get("if", "")).replace(" ", "")
        from_width = str(rule.get("from", "")).strip()
        to_width = str(rule.get("to", "")).strip()
        if from_width != width_intent or not to_width:
            continue
        if rule_if.startswith("canvasWidth<"):
            threshold_raw = rule_if.split("<", 1)[1]
            try:
                threshold = float(threshold_raw)
            except ValueError:
                continue
            if canvas_width < threshold and to_width in allowed:
                width_intent = to_width
    return width_intent


def _widthIntent_pixel_cap(intent: str, content_width: float) -> float:
    """Convert a widthIntent label to its pixel cap. The compiler uses this as
    a *max*, not a target — so widthIntent="half" doesn't force a 908 px name
    field on a wide canvas, it just promises the field will not exceed half the
    content area. Phase 2 of the layout solver may shrink further to fit a row.
    """
    if intent == "compact":
        return WIDTHINTENT_COMPACT_CAP_PX
    if intent == "half":
        # Two halves + one inter-column gap must fit content_width.
        return max(WIDTHINTENT_COMPACT_CAP_PX, (content_width - MIN_COLUMN_GAP) / 2.0)
    # "full" or unknown: no narrower cap than content_width itself.
    return content_width


def _content_width_target_px(semantic: SemanticComponentIntent) -> Optional[float]:
    """Compute a content-derived width target (px) for narrow input components.

    Returns ``None`` when the component is not in the width-aware set, when no
    ``maxLength`` is supplied, or when the LLM left validationIntent empty.
    Caller treats ``None`` as "no opinion, use the tier's natural target".
    """
    if semantic.componentType not in COMPONENT_TYPES_WIDTH_AWARE:
        return None
    validation = semantic.validationIntent
    if validation is None:
        return None
    max_length = validation.maxLength
    if max_length is None or max_length <= 0:
        return None
    label_chars = len(semantic.label or "")
    label_px = float(label_chars) * AVG_CHAR_PX
    value_px = float(max_length) * AVG_CHAR_PX
    return max(label_px, value_px) + LABEL_PADDING_PX


def _resolve_component_widths(
    semantic: SemanticComponentIntent,
    *,
    content_width: float,
    footprint_map: Dict[str, Dict[str, float]],
    width_intent_resolved: str,
) -> Tuple[float, float, float, str]:
    """Return ``(min_px, target_px, max_px, source)`` for a single component.

    Width policy:
      1. Look up the component's tier (or a generic catch-all). Tier defines
         natural ``(min, target, max)`` widths for the type.
      2. ``ALWAYS_FULL_WIDTH_TYPES`` (header/paragraph/divider/terms) force
         ``target = max = content_width`` regardless of the LLM widthIntent.
      3. ``widthIntent`` shrinks ``max_px`` to its pixel cap (compact/half/full).
         The LLM hint is a *cap*, never a target.
      4. ``validationIntent.maxLength`` (when present and small) further shrinks
         ``target_px`` toward content size — handles "2-char state code" cases.
      5. Runtime footprint width acts as a hard floor (never narrower than the
         actual rendered DOM control reports).
      6. Final clamp: ``min_px <= target_px <= max_px`` and all <= content_width.
    """
    component_type = semantic.componentType
    label_lc = (semantic.label or "").strip().lower()

    tier = COMPONENT_WIDTH_TIERS.get(component_type)
    if tier is None:
        tier = DEFAULT_WIDTH_TIER
    # Promote generic-text fields onto the narrower name tier when the label
    # clearly identifies a name. Avoids "First name" rendering at 320 px.
    if (
        component_type in {"text"}
        and label_lc in NAME_FIELD_LABELS
        and label_lc != "name"  # generic "Name" stays on the wider text tier
    ):
        tier = COMPONENT_WIDTH_TIERS["first-name"]

    tier_min, tier_target, tier_max = tier

    if component_type in ALWAYS_FULL_WIDTH_TYPES:
        tier_target = content_width
        tier_max = content_width
        # Banner-style components don't shrink below their tier_min, but the
        # tier_min clamp below already handles that.

    intent_cap = _widthIntent_pixel_cap(width_intent_resolved, content_width)

    # Effective max: tier max, intent cap, and content_width all bind.
    max_px = min(tier_max, intent_cap, content_width)

    content_hint = _content_width_target_px(semantic)
    if content_hint is not None:
        target_candidate = min(tier_target, content_hint)
    else:
        target_candidate = tier_target
    target_px = min(target_candidate, max_px)

    # tier_min is a *visual minimum* — even when the content hint says a 2-char
    # state code only needs 122 px, the rendered control must stay readable.
    # Clamp target up to tier_min, but never above max_px (max_px caps everything).
    floor_px = min(tier_min, max_px)

    # Footprint floor — runtime DOM reports an actual minimum width for this
    # type. Use it as a *stronger* floor than tier_min when the rendered DOM
    # would otherwise clip content. Capped by max_px so we never invert the
    # constraint.
    if component_type in footprint_map:
        floor_px = max(floor_px, min(footprint_map[component_type]["width"], max_px))

    if target_px < floor_px:
        target_px = floor_px
    min_px = floor_px

    # Source classification — useful for diagnostics & ops triage.
    if component_type in ALWAYS_FULL_WIDTH_TYPES:
        source = "always-full"
    elif content_hint is not None and content_hint < tier[1]:
        source = "content-cap"
    elif intent_cap < tier[1]:
        source = "intent-cap"
    elif target_px < tier[1]:
        # Bound by content_width on a narrow canvas.
        source = "canvas-cap"
    else:
        source = "tier-target"

    return min_px, target_px, max_px, source


def _component_height(
    component_type: str,
    footprint_map: Dict[str, Dict[str, float]],
    *,
    layout_mode: str = "vertical-packed",
) -> float:
    """Authored height the compiler should reserve for ``component_type``.

    Runtime ``componentFootprints`` are sourced from the toolbox tile DOM, which
    only measures the closed control box (e.g. ~109px for textarea). The
    rendered runtime adds label + validation chrome on top, and the form
    validator inflates short heights to ~200px when checking collisions
    (see ``form_validate.service._inflate_height_for_collision``). To prevent
    the compiler from underestimating vertical space and producing layouts that
    overlap once rendered, take ``max(footprint, default)`` so the floor is
    always at least the documented rendered footprint for the type.

    Story 6.3.1 (UAT round 9) — Fix G item 4a: horizontal-stacked mode uses
    a separate (tighter) per-type table because label/input/validation share
    one row at runtime. See the ``DEFAULT_COMPONENT_HEIGHTS_HORIZONTAL``
    docstring for the full rationale.

    NOTE: in horizontal mode we intentionally do NOT take ``max`` with the
    runtime footprint, because the toolbox tile footprint reflects the
    component as it is laid out in vertical-packed form (label-above-input)
    which is *always* taller than the horizontal row. Trusting the
    horizontal table directly is what unlocks the tighter canvas reservation.
    """
    if layout_mode == LAYOUT_MODE_HORIZONTAL_STACKED:
        return float(
            DEFAULT_COMPONENT_HEIGHTS_HORIZONTAL.get(
                component_type,
                DEFAULT_COMPONENT_HEIGHTS.get(component_type, 56),
            )
        )
    default_height = float(DEFAULT_COMPONENT_HEIGHTS.get(component_type, 110))
    if component_type in footprint_map:
        return max(footprint_map[component_type]["height"], default_height)
    return default_height


def _component_props_from_semantic(
    semantic: SemanticComponentIntent,
    normalized_validation: Dict[str, Any],
    width_px: int,
    height_px: int,
) -> Dict[str, Any]:
    props: Dict[str, Any] = {}
    if isinstance(semantic.label, str) and semantic.label.strip():
        props["label"] = semantic.label.strip()
    if isinstance(semantic.placeholder, str) and semantic.placeholder.strip():
        props["placeholder"] = semantic.placeholder.strip()
    if isinstance(semantic.helpText, str) and semantic.helpText.strip():
        props["helpText"] = semantic.helpText.strip()
    if isinstance(semantic.options, list):
        props["options"] = semantic.options
    if "required" in normalized_validation:
        props["required"] = bool(normalized_validation.get("required"))
    if normalized_validation:
        props["validation"] = normalized_validation
    props["width"] = f"{width_px}px"
    props["height"] = height_px
    return props


def _normalize_validation_intent(
    semantic: SemanticComponentIntent,
    allowed_rules_by_component: Dict[str, List[str]],
) -> Dict[str, Any]:
    component_type = semantic.componentType
    allowed = set(allowed_rules_by_component.get(component_type, []))
    raw = semantic.validationIntent.model_dump(exclude_none=True) if semantic.validationIntent else {}
    normalized: Dict[str, Any] = {}
    for key, value in raw.items():
        if key in allowed:
            normalized[key] = value
    if semantic.validationIntent and semantic.validationIntent.required is True and "required" in allowed:
        normalized["required"] = True
    return normalized


def _build_allowed_rules(
    validation_contracts: Optional[List[Dict[str, Any]]],
) -> Dict[str, List[str]]:
    if not isinstance(validation_contracts, list):
        return {}
    mapped: Dict[str, List[str]] = {}
    for row in validation_contracts:
        if not isinstance(row, dict):
            continue
        component_type = str(row.get("componentType", "")).strip()
        if not component_type:
            continue
        rules = row.get("allowedRules")
        if isinstance(rules, list):
            mapped[component_type] = [str(item).strip() for item in rules if str(item).strip()]
    return mapped


def compile_semantic_plan_to_definition(
    semantic_plan: FormSemanticPlan,
    *,
    runtime_context: Optional[Dict[str, Any]],
    capability_policy_json: Optional[Dict[str, Any]],
    width_policy_json: Optional[Dict[str, Any]],
    capability_snapshot_json: Optional[Dict[str, Any]],
    validation_contracts: Optional[List[Dict[str, Any]]],
    measured_heights: Optional[Dict[str, float]] = None,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Compile a semantic plan into a deterministic ``DefinitionJSON``.

    ``measured_heights`` (Story 6.3.1 UAT round 5 — render-then-measure):
        Optional ``{componentId: rendered_height_px}`` map. When present, the
        height the compiler reserves for each listed component is forced to
        ``ceil(rendered_height_px)`` instead of the per-type estimate from
        ``_component_height``. This is the second pass of the render-then-
        measure flow:

          1. ``/generate`` runs without measurements and emits an estimated
             layout (``estimated`` heights, ``compileSummary.heightsSource =
             "estimated"``).
          2. The frontend renders that layout off-screen, measures each
             rendered component's height from the DOM, and POSTs the
             measurements to ``/remeasure``.
          3. ``/remeasure`` calls this function again with the same semantic
             plan + ``measured_heights`` so the layout solver places rows
             using ground-truth heights — no more "compiler said 131 px,
             validator inflated to 220 px, collision fired" mismatches.

        Components missing from the dict (or with non-positive values) fall
        back to ``_component_height`` exactly as before, so a partial
        measurement payload still works.
    """
    runtime_canvas_raw = runtime_context.get("canvas") if isinstance(runtime_context, dict) else None
    runtime_canvas: Dict[str, Any] = runtime_canvas_raw if isinstance(runtime_canvas_raw, dict) else {}
    canvas_width = int(
        _parse_positive_number(runtime_canvas.get("width"), DEFAULT_CANVAS_WIDTH)
    )
    canvas_height = int(
        _parse_positive_number(runtime_canvas.get("height"), DEFAULT_CANVAS_HEIGHT)
    )
    grid_size = int(_parse_positive_number(runtime_canvas.get("gridSize"), DEFAULT_GRID_SIZE))

    locked_globals = runtime_context.get("lockedGlobals") if isinstance(runtime_context, dict) else {}

    # Story 6.3.1 (UAT round 6) — layout-mode resolution. Decides which of
    # the two placement strategies (vertical-packed vs horizontal-stacked)
    # this compile run uses; both branches live below the row-solver loop.
    layout_mode = resolve_layout_mode(runtime_context)

    theme = DEFAULT_THEME
    if isinstance(locked_globals, dict):
        maybe_theme = locked_globals.get("theme")
        if isinstance(maybe_theme, dict):
            theme = {
                "primaryColor": str(maybe_theme.get("primaryColor", DEFAULT_THEME["primaryColor"])),
                "backgroundColor": str(
                    maybe_theme.get("backgroundColor", DEFAULT_THEME["backgroundColor"])
                ),
                "fontFamily": str(maybe_theme.get("fontFamily", DEFAULT_THEME["fontFamily"])),
            }

    footprint_map = _runtime_footprint_map(runtime_context)
    allowed_rules_by_component = _build_allowed_rules(validation_contracts)

    components: List[Dict[str, Any]] = []
    diagnostics: List[Dict[str, Any]] = []
    # Phase 2 S4 trace: per sub-row solver decision.
    row_solver_decisions: List[Dict[str, Any]] = []
    # Phase 2 S4 trace: rowGroups that the solver had to split across multiple
    # rows because they couldn't fit horizontally even at min widths.
    row_group_splits: List[Dict[str, Any]] = []
    dropped_components = 0
    # Story 6.3.1 (failure-mode separation): every drop now records WHY in a
    # parallel reasons list. The service treats any post-gate drop as a
    # compiler-fault and surfaces this list for triage.
    dropped_component_reasons: List[Dict[str, Any]] = []
    # Story 6.3.1 UAT round 4: deterministic remaps applied to the LLM's
    # ``componentType``. Currently only label-driven (e.g. textarea→address for
    # a field labeled "Address"). Surface them so prompt regressions are easy
    # to spot in the trace.
    component_type_remaps: List[Dict[str, Any]] = []
    fallback_count = 0
    submit_button_clamped = False
    section_keys_seen: set = set()
    row_group_keys_seen: set = set()

    content_width = float(canvas_width - (DEFAULT_MARGIN_X * 2))

    pending_row: List[Dict[str, Any]] = []
    pending_row_group: Optional[str] = None
    pending_section: Optional[str] = None
    pending_action_alignments: List[Optional[str]] = []
    last_flushed_section: Optional[str] = None
    rows_in_last_section: int = 0
    y_cursor = float(DEFAULT_MARGIN_Y)

    # Story 6.3.1 UAT round 3 — aligned grid layout.
    # Pass 1 (the for-loop below) only DECIDES per-row widths and queues
    # sub-rows into ``placed_subrows``. Pass 2 (``_apply_grid_alignment``)
    # computes the per-column width grid (max of every column position across
    # all sub-rows that share a column count ``k``) and writes final x/y/width
    # so that:
    #   - every solo row's left edge sits at MARGIN_X (so single-component
    #     rows line up under each other);
    #   - every multi-row of column count k uses the same per-column widths
    #     and inter-column gap (so column-1 and column-2 line up under each
    #     other across rows of the same arity).
    # This replaces the previous justify-evenly-per-row policy which made
    # rows visually drift left/right based on individual component widths.
    placed_subrows: List[Dict[str, Any]] = []

    def _solve_row(items: List[Dict[str, Any]]) -> Tuple[Optional[List[float]], str, float]:
        """Phase 2 S1 row solver. Returns ``(widths_per_item, decision, slack)``.

        ``decision`` is one of:
          - ``"fit"``        — every item gets its tier target width.
          - ``"shrink"``     — items are scaled proportionally toward their
                               min_px; row consumed all available width.
          - ``"reflow"``     — even at min widths the row exceeds content_width
                               (caller must pop trailing items into a sub-row).
        """
        n = len(items)
        if n == 0:
            return [], "empty", 0.0
        targets = [float(it["_solverTarget"]) for it in items]
        mins = [float(it["_solverMin"]) for it in items]
        base_gaps = (n - 1) * MIN_COLUMN_GAP

        # Stage 1: every item at its tier target.
        target_total = sum(targets)
        if target_total + base_gaps <= content_width:
            return targets, "fit", content_width - target_total - base_gaps

        # Stage 2: proportional shrink toward tier min.
        available = content_width - base_gaps
        if available <= 0.0 or target_total <= 0.0:
            return None, "reflow", 0.0
        scale = available / target_total
        shrunk = [max(mins[i], targets[i] * scale) for i in range(n)]
        # Items pinned to their min may push the proportionally-scaled total
        # over `available`. Iterate one more time, redistributing the remaining
        # slack across items that aren't yet pinned. Keeps the final widths
        # within (min, target) without exceeding `available`.
        for _ in range(8):  # bounded refinement loop, in practice converges in <=3
            slack = available - sum(shrunk)
            if slack >= -0.5:
                break
            # Identify items that can still shrink (above their min).
            shrinkable_idx = [i for i in range(n) if shrunk[i] > mins[i] + 0.5]
            if not shrinkable_idx:
                break
            # How much room above-min do we have to give back?
            shrinkable_slack = sum(shrunk[i] - mins[i] for i in shrinkable_idx)
            # We need to absorb |slack| pixels from shrinkable items.
            need = -slack
            if need > shrinkable_slack:
                # Even pulling all shrinkables to min won't be enough → reflow.
                for i in shrinkable_idx:
                    shrunk[i] = mins[i]
                break
            scale_back = need / shrinkable_slack
            for i in shrinkable_idx:
                shrunk[i] = max(mins[i], shrunk[i] - (shrunk[i] - mins[i]) * scale_back)

        if sum(shrunk) <= available + 0.5:
            return shrunk, "shrink", max(0.0, available - sum(shrunk))

        # Stage 3: caller must reflow.
        return None, "reflow", 0.0

    def _collect_subrow(
        items: List[Dict[str, Any]],
        widths: List[float],
        align_overrides: List[Optional[str]],
        *,
        sub_row_index: int,
        decision: str,
        rowgroup: Optional[str],
        leading_section_gap: float,
    ) -> None:
        """Phase 1 of the aligned-grid layout: queue a placed sub-row for
        deferred placement. Width is the per-row solver's preferred width for
        each item (``items[i]._solverTarget`` after fit/shrink). Final pixel
        positions and any column-grid widening / shrinking are decided in
        ``_apply_grid_alignment`` once every sub-row has been collected.
        """
        # Stamp the per-row preferred width onto the item now so the solver
        # decision is preserved if alignment doesn't widen further.
        for i, it in enumerate(items):
            it["style"]["width"] = int(round(widths[i]))
        placed_subrows.append({
            "items": items,
            "widths": [float(w) for w in widths],
            "alignments": list(align_overrides),
            "decision": decision,
            "rowgroup": rowgroup,
            "subRowIndex": sub_row_index,
            "leadingSectionGap": float(leading_section_gap),
        })

    def flush_row() -> None:
        """Run the 3-state solver against ``pending_row`` and queue each
        resulting sub-row into ``placed_subrows`` for deferred placement.

        Solver behaviour is unchanged from Phase 2 S1: fit-at-target → shrink
        proportionally → reflow trailing items. The ONLY difference from the
        previous implementation is that we no longer write x/y/widths here —
        ``_apply_grid_alignment`` does that after the column grid is known.
        """
        nonlocal last_flushed_section, pending_row_group, pending_section
        nonlocal rows_in_last_section
        if not pending_row:
            return

        leading_section_gap = 0.0
        if (
            pending_section is not None
            and pending_section != last_flushed_section
            and last_flushed_section is not None
            and rows_in_last_section >= 2
        ):
            leading_section_gap = (SECTION_GAP_MULTIPLIER - 1.0) * DEFAULT_ROW_GAP

        queue: List[Dict[str, Any]] = list(pending_row)
        aligns: List[Optional[str]] = list(pending_action_alignments)
        section = pending_section
        rowgroup = pending_row_group
        pending_row.clear()
        pending_action_alignments.clear()
        pending_row_group = None
        pending_section = None

        sub_rows_placed = 0
        rowgroup_was_split = False

        while queue:
            head = list(queue)
            head_aligns = list(aligns)
            spillover: List[Dict[str, Any]] = []
            spillover_aligns: List[Optional[str]] = []

            widths, decision, _slack = _solve_row(head)
            while decision == "reflow" and len(head) > 1:
                spillover.insert(0, head.pop())
                spillover_aligns.insert(0, head_aligns.pop())
                widths, decision, _slack = _solve_row(head)
                rowgroup_was_split = True

            if decision == "reflow":
                # Single item that can't fit alone — clamp to min. (Unreachable
                # for a sane canvas because min_px <= max_px <= content_width
                # by construction; safe fallback.)
                widths = [float(head[0]["_solverMin"])]
                decision = "force-min"

            _collect_subrow(
                head,
                widths if widths is not None else [float(it["_solverTarget"]) for it in head],
                head_aligns,
                sub_row_index=sub_rows_placed,
                decision=decision,
                rowgroup=rowgroup,
                # Only the first sub-row of a flush carries the section gap.
                leading_section_gap=leading_section_gap if sub_rows_placed == 0 else 0.0,
            )
            sub_rows_placed += 1

            queue = spillover
            aligns = spillover_aligns

        if rowgroup_was_split:
            row_group_splits.append({
                "originalRowGroup": rowgroup,
                "splitIntoRows": sub_rows_placed,
            })

        if section == last_flushed_section:
            rows_in_last_section += sub_rows_placed
        else:
            rows_in_last_section = sub_rows_placed
        last_flushed_section = section

    def add_component_row(
        item: Dict[str, Any],
        *,
        row_group: Optional[str],
        section: Optional[str],
        force_isolated: bool,
        action_alignment: Optional[str],
    ) -> None:
        nonlocal pending_row_group, pending_section
        if force_isolated:
            if pending_row:
                flush_row()
            pending_row_group = row_group
            pending_section = section
            pending_row.append(item)
            pending_action_alignments.append(action_alignment)
            flush_row()
            return
        if not pending_row:
            pending_row_group = row_group
            pending_section = section
            pending_row.append(item)
            pending_action_alignments.append(action_alignment)
            return
        # rowGroup boundary: a different rowGroup is intentional grouping, not
        # overflow, so the solver doesn't need a chance to combine. A section
        # boundary is an even stronger signal — sections are visual zones that
        # should never share a row, even if their rowGroups happen to both be
        # None.
        if row_group != pending_row_group or section != pending_section:
            flush_row()
            pending_row_group = row_group
            pending_section = section
            pending_row.append(item)
            pending_action_alignments.append(action_alignment)
            return
        # The Phase 2 solver handles row-too-wide via shrink + reflow inside
        # flush_row(), so we eagerly queue items belonging to the same rowGroup
        # without an upfront wrap check.
        pending_row.append(item)
        pending_action_alignments.append(action_alignment)

    for index, semantic in enumerate(semantic_plan.components, start=1):
        component_type = semantic.componentType.strip()
        if not component_type:
            dropped_components += 1
            dropped_component_reasons.append(
                {
                    "componentIndex": index - 1,
                    "componentType": semantic.componentType,
                    "reason": "empty-component-type",
                }
            )
            continue

        # Story 6.3.1 UAT round 4 — label-driven type remap. The LLM frequently
        # picks ``componentType: textarea`` for a field labeled "Address" (free
        # text + multi-line is the easy match). The address componentType is
        # rendered as a single-line input here, so remapping fixes width tier
        # (480→600 target), height (240→110), validation, and autofill in one
        # step. We only remap when the label clearly identifies an address —
        # never on the rowGroup alone, because a rowGroup of "address" can also
        # legitimately group multiple text fields (street + city + zip).
        original_component_type = component_type
        label_lc = (semantic.label or "").strip().lower()
        if component_type == "textarea" and label_lc in ADDRESS_FIELD_LABELS:
            component_type = "address"
            # Replace ``semantic.componentType`` everywhere downstream — width
            # resolver, validation normaliser, and props builder all read it
            # directly off the model. ``model_copy(update=...)`` returns a new
            # SemanticComponentIntent without mutating the original (which is
            # logged for trace auditing).
            semantic = semantic.model_copy(update={"componentType": component_type})
            component_type_remaps.append({
                "componentIndex": index - 1,
                "componentId": semantic.componentId,
                "from": original_component_type,
                "to": component_type,
                "reason": "label-suggests-address",
                "label": semantic.label,
            })

        section_value = semantic.section.strip() if isinstance(semantic.section, str) else None
        if section_value == "":
            section_value = None
        row_group_value = (
            semantic.rowGroup.strip() if isinstance(semantic.rowGroup, str) else None
        )
        if row_group_value == "":
            row_group_value = None
        if section_value is not None:
            section_keys_seen.add(section_value)
        if row_group_value is not None:
            row_group_keys_seen.add(row_group_value)

        width_intent = _normalize_width_intent(
            semantic.widthIntent,
            component_type,
            float(canvas_width),
            width_policy_json,
            capability_snapshot_json,
        )
        # Phase 1 W1: the tier-based resolver replaces the old span→pixel math.
        min_px, target_px, max_px, width_source = _resolve_component_widths(
            semantic,
            content_width=content_width,
            footprint_map=footprint_map,
            width_intent_resolved=width_intent,
        )
        # For Phase 1 we use the tier target as the placement width. Phase 2's
        # solver will swap this out per-row to honor (min, target, max) under a
        # row-level fit constraint.
        width_px = int(round(target_px))
        # Hard floor so we don't emit a ridiculously narrow control on a tiny
        # canvas. min_px is always <= target_px by construction, so this only
        # fires when target_px got squeezed below the tier minimum by the
        # canvas cap (very narrow canvases, e.g. 250 px).
        if width_px < int(round(min_px)):
            width_px = int(round(min_px))
        # Submit-button skips the content_width cap so the constraint pass below
        # can detect overflow on a narrow canvas and emit submitButtonClamped.
        if component_type != "submit-button":
            width_px = min(width_px, int(round(content_width)))
        # Compute the candidate component_id early so we can look up a
        # render-pass measurement for it. Final id assignment is unchanged
        # (still ``semantic.componentId`` or the synthesised fallback).
        candidate_component_id = semantic.componentId or f"{component_type}-{index}"
        # Story 6.3.1 UAT round 5 — render-then-measure path: when the
        # frontend has already rendered an estimated layout and posted the
        # actual DOM heights back to ``/remeasure``, we trust the
        # measurement instead of the per-type estimate. This eliminates
        # compiler-vs-validator disagreements (e.g. checkbox with 8 options
        # estimated at 131 px but rendered at 220 px → collision) without
        # us having to predict every renderer quirk in pure Python.
        measured_height_value: Optional[float] = None
        if measured_heights:
            raw_measured = measured_heights.get(candidate_component_id)
            if isinstance(raw_measured, (int, float)) and float(raw_measured) > 0:
                measured_height_value = float(raw_measured)
        if measured_height_value is not None:
            height_px = int(math.ceil(measured_height_value))
            height_source = "measured"
        else:
            height_px = int(round(_component_height(
                component_type, footprint_map, layout_mode=layout_mode,
            )))
            height_source = "estimated"

        normalized_validation = _normalize_validation_intent(semantic, allowed_rules_by_component)
        props = _component_props_from_semantic(semantic, normalized_validation, width_px, height_px)

        # UAT round 5 (run 41) — submit-button default alignment changed from
        # "center" to "left" so it lines up with the rest of the form's left
        # margin (DEFAULT_MARGIN_X). User feedback:
        #
        #   "Only the submit button is not left aligned like the rest of the
        #    components"
        #
        # The LLM can still override via ``actionAlignment: "center"|"right"``
        # for forms that genuinely want a centered call-to-action, but in 99%
        # of contact / signup / feedback forms the natural place is flush left
        # with the inputs above it.
        action_alignment = semantic.actionAlignment or (
            "left" if component_type == "submit-button" else None
        )
        is_submit = component_type == "submit-button"
        # Banner-style components (header/paragraph/divider/terms) are always
        # isolated to their own row so the solver doesn't pack a 1840-wide
        # header next to a 360-wide email and proportionally shrink them both.
        # The semantic intent is "this is a section break / contextual block",
        # not "share a row with adjacent inputs".
        is_full_row_banner = component_type in ALWAYS_FULL_WIDTH_TYPES

        component_id = candidate_component_id
        # ``_solverMin/Target/Max`` are private metadata consumed by the Phase 2
        # row solver in flush_row(); they are stripped before the definition
        # leaves the compiler so downstream consumers never see them.
        item = {
            "id": component_id,
            "type": component_type,
            "props": props,
            "position": {"x": 0, "y": 0},  # filled in by flush_row / solver
            "style": {"width": width_px, "height": height_px},
            "widthIntentResolved": width_intent,
            "_heightSource": height_source,
            "_solverMin": int(round(min_px)),
            "_solverTarget": int(round(target_px)),
            "_solverMax": int(round(max_px)),
        }
        add_component_row(
            item,
            row_group=row_group_value,
            section=section_value,
            force_isolated=is_submit or is_full_row_banner,
            action_alignment=action_alignment,
        )

        # Diagnostics: report final pixel widths (post-tier, post-cap) plus the
        # source classification for ops triage. ``span`` is no longer the source
        # of truth, but we surface a derived span (ceil(width / col_unit)) for
        # backward-compat consumers.
        col_unit_px = (content_width + MIN_COLUMN_GAP) / float(DEFAULT_GRID_COLUMNS)
        derived_span = max(1, int(math.ceil(width_px / col_unit_px))) if col_unit_px > 0 else 1
        diagnostics.append(
            {
                "componentId": component_id,
                "componentType": component_type,
                "widthIntentResolved": width_intent,
                "widthSource": width_source,
                "maxLengthHint": (
                    semantic.validationIntent.maxLength
                    if semantic.validationIntent is not None
                    else None
                ),
                "section": section_value,
                "rowGroup": row_group_value,
                "span": derived_span,
                "widthPx": width_px,
                "widthMinPx": int(round(min_px)),
                "widthTargetPx": int(round(target_px)),
                "widthMaxPx": int(round(max_px)),
                "heightPx": height_px,
            }
        )

    flush_row()

    # ---------- Story 6.3.1 (UAT round 6) — Phase 2 *completion* ----------
    # Horizontal-stacked layout placement.
    #
    # When the form is configured for horizontal label layout AND the canvas
    # is wide enough to keep that mode (the AI panel + renderer apply a
    # ``HORIZONTAL_LAYOUT_MIN_WIDTH_PX = 600`` mobile downgrade upstream, so
    # by the time we reach this branch we know the canvas is at least 600 px
    # wide), we produce a single-column layout with one component per row.
    # Each component's bounding box spans the whole content row, and the
    # renderer's CSS splits that box into label / input / validation
    # columns. This satisfies the user's UAT round 6 directive:
    #
    #   * Label width = "same logic as vertical mode, scaled by available
    #     canvas width — generous on wide, less on narrow." Achieved
    #     implicitly by handing the renderer a full-row bounding box and
    #     letting its default column split scale with canvas width.
    #
    #   * Input width = "same widthIntent → tier logic, with validation
    #     dropping below if there isn't enough room inline." We keep the
    #     tier table for the drop-below detection (using ``_solverMin``
    #     as the input column floor), but the bounding box itself becomes
    #     the full row so the renderer has room to split.
    #
    # The vertical-packed path below is unchanged — banner full-rows and
    # submit-button alignment are handled identically in both modes by
    # branching on component type. A regression test pins down that
    # vertical-mode geometry stays byte-identical (Phase 2 detection-only
    # invariant from UAT round 6 still holds).
    if layout_mode == LAYOUT_MODE_HORIZONTAL_STACKED:
        # Re-flatten ``placed_subrows`` back to a 1-D list. ``flush_row``
        # may have packed multiple inputs into the same sub-row when the
        # LLM emitted a ``rowGroup`` — in horizontal mode we ignore that
        # grouping (each component is its own row) so we walk every item.
        horizontal_items: List[Tuple[Dict[str, Any], Optional[str]]] = []
        for sr in placed_subrows:
            sr_items = sr["items"]
            sr_aligns = sr["alignments"] or [None] * len(sr_items)
            for idx, sr_item in enumerate(sr_items):
                alignment = sr_aligns[idx] if idx < len(sr_aligns) else None
                horizontal_items.append((sr_item, alignment))

        max_bottom = float(DEFAULT_MARGIN_Y)

        # Story 6.3.1 (UAT round 6) — Fix D: build a per-component lookup of
        # the LLM-supplied ``validationIntent.maxLength`` so the input-band
        # estimator can honour it. Mirrors the synthesis rule used to pick
        # ``candidate_component_id`` further up so ``item["id"]`` matches
        # the key here even when the LLM didn't supply ``componentId``.
        # Story 6.3.1 (UAT round 7) — Fix E items 3/4: also keep the full
        # intent so the placement loop can read ``options`` (dropdown sizing)
        # and the rating-scale extras (rating sizing) without re-walking the
        # plan.
        max_length_by_component_id: Dict[str, Optional[int]] = {}
        intent_by_component_id: Dict[str, SemanticComponentIntent] = {}
        # IMPORTANT: enumerate ``start=1`` to mirror the synthesis rule used
        # by the main compile loop (search for ``enumerate(...,start=1)``);
        # otherwise the lookup keys are off by one and the compiled item
        # ``"rating-1"`` would silently miss the map entry ``"rating-0"``.
        for s_index, s_intent in enumerate(semantic_plan.components, start=1):
            s_component_id = s_intent.componentId or f"{s_intent.componentType}-{s_index}"
            s_max_length: Optional[int] = None
            if s_intent.validationIntent is not None:
                raw_max = s_intent.validationIntent.maxLength
                if isinstance(raw_max, int) and raw_max > 0:
                    s_max_length = raw_max
            max_length_by_component_id[s_component_id] = s_max_length
            intent_by_component_id[s_component_id] = s_intent

        # Story 6.3.1 (UAT round 6) — Fix C/D: use the SAME label band the
        # form-wide ``globalStyles.horizontalLabelBandPx`` is going to ship
        # with so the compiler's box-width math agrees with what the
        # renderer paints. The legacy ``HORIZONTAL_LABEL_BAND_FRACTION``
        # heuristic stays as the conservative fallback for the inline-vs-
        # below detection further down.
        label_band_estimate = float(
            _estimate_horizontal_label_band_px(semantic_plan, content_width)
        )

        # Story 6.3.1 (UAT round 6) — Fix D: assumed validation natural
        # width used ONLY when computing the "just-wide-enough" component
        # bounding box. The actual validation column track in the renderer
        # is ``auto`` (Fix B leaves it untouched) so the message stretches
        # to its real content; this estimate just lets us decide how wide
        # to make ``style.width`` so a typical validation message fits
        # inline without forcing the grid to overflow.
        #
        # Picked to match the existing ``HORIZONTAL_VALIDATION_MIN_PX``
        # floor (= ~22 chars at the default font, e.g. "Please enter your
        # email address"). Validation messages longer than this will cause
        # the grid's auto track to grow and the inline-grid will visually
        # extend past ``style.width`` — which is fine because the canvas
        # has empty space to the right (Fix D bounding-box policy).
        assumed_validation_band_px = HORIZONTAL_VALIDATION_MIN_PX

        # Story 6.3.1 (UAT round 6) — Fix D item 4: form-wide density
        # preset. Multiplier resolved once per compile so every standard
        # input on the page agrees on which density they're using.
        chars_multiplier = _resolve_input_band_preset_multiplier(runtime_context)

        for entry_idx, (item, alignment) in enumerate(horizontal_items):
            item_type = str(item.get("type", "")).strip()

            if item_type in HORIZONTAL_MODE_BANNER_TYPES:
                # Banners (header / paragraph / divider) genuinely want a
                # full-row band — they're typographic display objects and
                # the natural reading flow is "title left, span the page".
                # ``terms`` is intentionally NOT in this set anymore (Fix E
                # item 5) — see the dedicated branch below.
                item["style"]["width"] = int(round(content_width))
                item["position"]["x"] = int(round(DEFAULT_MARGIN_X))
                item["position"]["y"] = int(round(y_cursor))
                row_height = _reserved_height(item, layout_mode=layout_mode)
                row_decision = "horizontal-banner"
                validation_dropped_below = False
            elif item_type == "terms":
                # Story 6.3.1 (UAT round 7) — Fix E item 5: terms tight box.
                #
                # Terms has its own 3-object internal layout
                # ``[checkbox(input)] [consent text(label)] [validation]``.
                # In UAT round 6 we routed terms through the full-row banner
                # branch which gave it ``style.width = content_width`` and
                # the renderer's auto-tracked grid then spread the checkbox
                # to the far left of the canvas, the consent text to the
                # far right, and the validation message even further right
                # — visually the consent looked like 3 unrelated controls
                # spread across 1000+ px.
                #
                # Resolution per terms component:
                #   1. ``input_band_px = TERMS_CHECKBOX_BAND_PX`` (~32 px)
                #      — pinned via ``inputWidthOverride`` so the renderer
                #      doesn't stretch the checkbox column to fill 1fr.
                #   2. ``terms_label_band_px`` = consent-text width
                #      (``len(label) + len(termsLinkText) + 2`` chars at
                #      ``AVG_CHAR_PX`` plus tight padding). Pinned via
                #      ``labelWidthOverride`` — this *overrides* the form-
                #      wide ``horizontalLabelBandPx`` for the terms row only
                #      (per-component override wins per Fix B precedence),
                #      because the consent text is naturally longer than
                #      the form's other labels and forcing it into the form-
                #      wide band would wrap it onto multiple lines.
                #   3. ``box_width = checkbox + gap + label + gap + validation``
                #      — the full inline-grid width. Validation drop-below
                #      and helpWidthOverride pinning follow the same policy
                #      as standard inputs so the terms component looks
                #      consistent with the rest of the form.
                terms_props = item.get("props") if isinstance(item.get("props"), dict) else {}
                terms_label_text = str(terms_props.get("label") or "I agree to the").strip()
                terms_link_text = str(terms_props.get("termsLinkText") or "Terms").strip()
                # ``+ 3`` chars covers the space between label/link, the
                # required-marker " *" the renderer appends, and a half
                # char of breathing room after the link.
                consent_chars = max(1, len(terms_label_text) + len(terms_link_text) + 3)
                terms_label_band_px = float(consent_chars) * AVG_CHAR_PX + HORIZONTAL_LABEL_BAND_PADDING_PX
                # Don't let the consent label itself dominate the canvas —
                # if the LLM emitted a very long consent paragraph (rare
                # but possible) clamp to two-thirds of the content width
                # so the checkbox + validation still fit comfortably.
                terms_label_band_px = min(
                    terms_label_band_px,
                    max(HORIZONTAL_LABEL_BAND_MAX_PX, content_width * (2.0 / 3.0)),
                )
                terms_input_band_px = float(TERMS_CHECKBOX_BAND_PX)

                # Story 6.3.1 (UAT round 9) — Fix G item 3: revert Fix F4.
                #
                # Fix F4 always dropped the terms validation onto a second
                # row by adding ``HORIZONTAL_VALIDATION_DROP_HEIGHT_PX`` to
                # ``style.height`` — but the compiler never actually
                # mutates ``gridLayout.cellAssignments``, so the renderer
                # kept placing validation in the existing
                # ``[checkbox][label][validation]`` row. With a tight
                # bounding box (checkbox + label only) the validation
                # column was squeezed into ~150 px of leftover slack and
                # wrapped to 3 lines (UAT round 9 screenshot 2).
                #
                # Resolution: keep validation INLINE next to the consent
                # link, expand the bounding box to budget for the
                # validation column, and let the renderer's own
                # ``max-content`` auto track grow the column to fit the
                # actual message at runtime. No ``helpWidthOverride`` is
                # stamped — that matches every other component under
                # framework-first (Fix G item 1) so users can later
                # adjust via the standard Properties Panel.
                #
                # ``inputWidthOverride`` and ``labelWidthOverride`` ARE
                # still stamped here because they are *structural* for
                # terms, not sizing pins:
                #   * Without ``inputWidthOverride: 32`` the renderer's
                #     ``flexColumnSet`` treats the checkbox column as
                #     ``minmax(0, 1fr)`` and stretches the 16 px checkbox
                #     across the full row, putting the consent label
                #     hundreds of pixels to the right.
                #   * Without ``labelWidthOverride`` the consent label
                #     would be forced into the form-wide
                #     ``horizontalLabelBandPx`` (~241 px), wrapping the
                #     "I consent to receiving marketing communications"
                #     copy onto multiple lines.
                terms_validation_band_px = float(_estimate_validation_band_px(
                    terms_props,
                    min_px=HORIZONTAL_VALIDATION_MIN_PX,
                    max_px=HORIZONTAL_VALIDATION_MAX_PX,
                ))
                terms_box_width = (
                    terms_input_band_px
                    + HORIZONTAL_INTRA_GAP_PX
                    + terms_label_band_px
                    + HORIZONTAL_INTRA_GAP_PX
                    + terms_validation_band_px
                )
                if terms_box_width > content_width:
                    # Canvas too narrow for inline validation — drop
                    # validation column from the box and reserve a
                    # second-row chrome budget. Height bump matches the
                    # standard-input drop-below path. NOTE: gridLayout
                    # cellAssignments still place validation on row 0
                    # which means the renderer will continue to render
                    # inline; the +24 px buffer is for the wrap, not a
                    # true drop-below. This compromise is acceptable for
                    # narrow canvases (rare in practice) and a future
                    # iteration can mutate gridLayout for true drop-
                    # below behaviour.
                    terms_box_width = (
                        terms_input_band_px
                        + HORIZONTAL_INTRA_GAP_PX
                        + terms_label_band_px
                    )
                    terms_box_width = min(terms_box_width, content_width)
                    terms_base_h = float(item["style"]["height"])
                    item["style"]["height"] = int(
                        round(terms_base_h + HORIZONTAL_VALIDATION_DROP_HEIGHT_PX)
                    )
                    row_decision = "horizontal-terms-validation-wrapped"
                    terms_validation_dropped = True
                else:
                    row_decision = "horizontal-terms-inline-validation"
                    terms_validation_dropped = False

                item["style"]["width"] = int(round(terms_box_width))
                item["position"]["x"] = int(round(DEFAULT_MARGIN_X))
                item["position"]["y"] = int(round(y_cursor))

                terms_item_props = item.get("props")
                if not isinstance(terms_item_props, dict):
                    terms_item_props = {}
                    item["props"] = terms_item_props
                # Sync ``props.width`` to the tight bounding box so the
                # renderer's ``hasExplicitWidth`` branch lays out the
                # inline-grid at the correct wrapper width (otherwise it
                # would inherit ``content_width`` from
                # ``_resolve_component_widths`` because terms is in
                # ``ALWAYS_FULL_WIDTH_TYPES``).
                terms_item_props["width"] = f"{int(round(terms_box_width))}px"
                terms_item_props["inputWidthOverride"] = int(round(terms_input_band_px))
                terms_item_props["labelWidthOverride"] = int(round(terms_label_band_px))
                # No ``helpWidthOverride`` — validation column is auto.

                row_height = _reserved_height(item, layout_mode=layout_mode)
                validation_dropped_below = terms_validation_dropped
            elif item_type == "submit-button":
                # Submit-button keeps its tier width and alignment policy —
                # in both layout modes the call-to-action is a focal point
                # that benefits from a tighter, action-shaped box rather
                # than a full-row band. ``actionAlignment`` defaults to
                # "left" upstream (UAT round 5) so it lines up with the
                # other inputs.
                it_w = float(item["style"]["width"])
                if it_w > content_width:
                    item["style"]["width"] = int(round(content_width))
                    it_w = float(item["style"]["width"])
                    submit_button_clamped = True
                if alignment == "left":
                    btn_x = float(DEFAULT_MARGIN_X)
                elif alignment == "right":
                    btn_x = float(DEFAULT_MARGIN_X) + max(
                        0.0, content_width - it_w
                    )
                else:
                    btn_x = float(DEFAULT_MARGIN_X) + max(
                        0.0, (content_width - it_w) / 2.0
                    )
                item["position"]["x"] = int(round(btn_x))
                item["position"]["y"] = int(round(y_cursor))
                row_height = _reserved_height(item, layout_mode=layout_mode)
                row_decision = "horizontal-submit"
                validation_dropped_below = False
            else:
                # Story 6.3.1 (UAT round 6) — Fix D: standard inputs now get
                # a content-aware "just-wide-enough" bounding box.
                #
                # Resolution per component:
                #   1. Compute ``input_band_px`` from the chars table, the
                #      LLM's ``validationIntent.maxLength`` hint, and the
                #      tier bounds. This is the width the renderer will pin
                #      the input column to via Fix B's
                #      ``props.inputWidthOverride`` plumbing.
                #   2. Compute the desired bounding box width:
                #          label_band + intra_gap + input_band + intra_gap
                #          + assumed_validation_band
                #      The label and validation columns are auto-tracked in
                #      the renderer (label = form-wide band via Fix C,
                #      validation = ``auto``), so the inline-grid will
                #      naturally fit inside this width when the validation
                #      message is at typical length.
                #   3. If the ideal box exceeds ``content_width`` (e.g. a
                #      narrow tablet canvas + a wide email tier), drop
                #      validation below the input — recompute the box
                #      without the validation column and reserve the extra
                #      height. The user's UAT round 6 instruction was
                #      explicit: "If there is not enough space to fit in
                #      the validation object then drop it below."
                # Story 6.3.1 (UAT round 8) — Fix F item 1: use the ORIGINAL
                # tier (``COMPONENT_WIDTH_TIERS[item_type]``) instead of the
                # footprint-inflated ``_solverMin/Target/Max`` left on ``item``
                # by ``_resolve_component_widths``.
                #
                # Why: ``_resolve_component_widths`` floors ``min_px`` to the
                # runtime ``componentFootprints`` width (line ~1042). The
                # frontend currently emits a UNIFORM ``width = 359`` for every
                # component type because the toolbox tile container is fixed-
                # width regardless of the control inside it (a "first-name"
                # tile is the same physical size as a "dropdown" tile in the
                # palette UI). Feeding that into the horizontal-stacked
                # estimator clamps every chars-driven calculation back up to
                # 359 px, so first-name (target 222), email (312), phone (200),
                # text (276), and dropdown (longest-option) all collapse to
                # 359 — exactly the "all inputs are the same width" regression
                # the user reported in UAT round 8.
                #
                # The toolbox-tile footprint is the right floor for the
                # full-component vertical-mode width (where label sits above
                # the input and the wrapper width has to fit a bunch of UI
                # chrome), but it is NOT a meaningful floor for just the
                # horizontal-mode input column — that column only has to fit
                # the input control itself, and ``COMPONENT_WIDTH_TIERS``
                # already encodes a sensible per-type visual minimum
                # (e.g. 220 px for text inputs). Bypass the footprint here.
                fallback_tier = COMPONENT_WIDTH_TIERS["first-name"]
                original_tier = COMPONENT_WIDTH_TIERS.get(item_type, fallback_tier)
                tier_tuple: Tuple[float, float, float] = original_tier
                tier_min_input = float(tier_tuple[0])
                tier_target_input = float(tier_tuple[1])
                tier_max_input = float(tier_tuple[2])

                component_id_for_lookup = str(item.get("id", "")).strip()
                max_length_hint = max_length_by_component_id.get(component_id_for_lookup)
                # Story 6.3.1 (UAT round 7) — Fix E items 3/4: extra
                # estimator inputs derived from the semantic intent.
                #   * options_max_chars  — for dropdown/select, the longest
                #     option label drives the input width (a "Company size"
                #     dropdown with options "201-500", "501-1000",
                #     "Enterprise" sizes itself to "Enterprise" ≈ 10 chars
                #     instead of the generic 22-char default).
                #   * rating_count       — for rating, ``validationIntent.max``
                #     (or LLM extras like ``maxRating``/``scale``, or
                #     ``len(options)``) determines the icon row width.
                lookup_intent = intent_by_component_id.get(component_id_for_lookup)
                options_max_chars: Optional[int] = None
                rating_count: Optional[int] = None
                if lookup_intent is not None:
                    if item_type in ("dropdown", "select"):
                        options_max_chars = _longest_option_chars(lookup_intent.options)
                    if item_type == "rating":
                        rating_count = _resolve_rating_count(lookup_intent)
                input_band_px = _estimate_horizontal_input_band_px(
                    item_type,
                    max_length_hint,
                    tier_tuple,
                    chars_multiplier=chars_multiplier,
                    options_max_chars=options_max_chars,
                    rating_count=rating_count,
                )

                # Story 6.3.1 (UAT round 8) — Fix F item 2: validation column
                # auto-grow. Replaces the fixed ``HORIZONTAL_VALIDATION_MIN_PX``
                # pin from Fix E item 2 with a per-component natural width
                # derived from the actual longest validator message. The clamp
                # uses the remaining content_width budget as ``max_px`` so the
                # column never exceeds what physically fits next to the input.
                # When the natural width is wider than that budget, the
                # drop-below path below kicks in just like it does for an
                # over-wide input.
                remaining_after_input = (
                    content_width
                    - label_band_estimate
                    - HORIZONTAL_INTRA_GAP_PX
                    - float(input_band_px)
                    - HORIZONTAL_INTRA_GAP_PX
                )
                # Floor at MIN so a tiny remaining budget still sees a
                # passable validation column; the drop-below path will
                # detect overflow and re-route.
                validation_max_budget = max(
                    HORIZONTAL_VALIDATION_MIN_PX,
                    min(remaining_after_input, HORIZONTAL_VALIDATION_MAX_PX),
                )
                item_props_for_validation = item.get("props")
                if not isinstance(item_props_for_validation, dict):
                    item_props_for_validation = {}
                validation_band_px = float(_estimate_validation_band_px(
                    item_props_for_validation,
                    min_px=HORIZONTAL_VALIDATION_MIN_PX,
                    max_px=validation_max_budget,
                ))

                ideal_box_width = (
                    label_band_estimate
                    + HORIZONTAL_INTRA_GAP_PX
                    + float(input_band_px)
                    + HORIZONTAL_INTRA_GAP_PX
                    + validation_band_px
                )

                if ideal_box_width > content_width:
                    # Not enough room to keep validation inline at the
                    # comfortable input band. Per UAT round 6 policy, drop
                    # validation below before shrinking the input — a
                    # readable input matters more than a single-line
                    # validation message.
                    validation_dropped_below = True
                    box_width_no_validation = (
                        label_band_estimate
                        + HORIZONTAL_INTRA_GAP_PX
                        + float(input_band_px)
                    )
                    if box_width_no_validation > content_width:
                        # Even without validation the input is too wide for
                        # this canvas — shrink the input toward its tier
                        # min so it still fits. ``input_band_px`` is now
                        # the floor width the renderer will use.
                        max_input_band = (
                            content_width - label_band_estimate - HORIZONTAL_INTRA_GAP_PX
                        )
                        input_band_px = int(round(max(
                            tier_min_input or fallback_tier[0],
                            min(float(input_band_px), max_input_band),
                        )))
                        box_width_no_validation = (
                            label_band_estimate
                            + HORIZONTAL_INTRA_GAP_PX
                            + float(input_band_px)
                        )
                    box_width = box_width_no_validation
                    base_h = float(item["style"]["height"])
                    item["style"]["height"] = int(
                        round(base_h + HORIZONTAL_VALIDATION_DROP_HEIGHT_PX)
                    )
                    row_decision = "horizontal-validation-below"
                else:
                    validation_dropped_below = False
                    box_width = ideal_box_width
                    row_decision = "horizontal-inline-validation"

                # Story 6.3.1 (UAT round 9) — Fix G "framework-first":
                # the compiler now stamps the *bounding box* only and lets
                # the framework's natural CSS Grid resolve the inner
                # column tracks. Per ``COMPONENT-FRAMEWORK-REFERENCE.md``
                # ("Width Calculation per Object Category") the input
                # absorbs flex while label and validation stay content-
                # sized — exactly the behaviour the builder uses for hand-
                # authored components. Earlier passes (Fix D/E/F) stamped
                # ``inputWidthOverride`` and ``helpWidthOverride`` as
                # absolute pixel pins, which:
                #
                #   * locked dropdown/rating widths so adding an option /
                #     extra star wrapped instead of growing
                #   * locked the validation column at compile time so
                #     longer runtime messages wrapped instead of growing
                #   * left no Properties Panel affordance to undo the pin,
                #     defeating the goal that AI generation seeds a form
                #     the user then customises with the rest of the
                #     builder tools
                #
                # Bounding-box width still uses the same width budgets
                # (``input_band_px`` + ``validation_band_px``) so that
                # collision math, canvas grow-to, and submit/textarea
                # placement all stay accurate; we just no longer pin the
                # individual object columns. Components are left-aligned
                # at ``DEFAULT_MARGIN_X`` (Fix D bounding-box policy).
                item["style"]["width"] = int(round(box_width))
                item["position"]["x"] = int(round(DEFAULT_MARGIN_X))
                item["position"]["y"] = int(round(y_cursor))

                # Story 6.3.1 (UAT round 9) — Fix G2: sync ``props.width``
                # to the new bounding ``style.width``. The frontend canvas
                # wrapper (``SortableComponent.displayWidth``) reads
                # ``component.props.width`` to size the absolutely-
                # positioned shell; if it stays at the earlier tier-based
                # value (e.g. "359px") the universal grid renders inside
                # a 359-px wrapper even though the compiler reserved
                # ``box_width`` (e.g. 735 px) for the collision footprint.
                # Pre-Fix-G the older ``inputWidthOverride`` pin used to
                # expand ``displayWidth`` to match — now that the override
                # is gone, the props.width sync is what keeps the wrapper
                # in step with the bounding box.
                item_props_for_width = item.get("props")
                if not isinstance(item_props_for_width, dict):
                    item_props_for_width = {}
                    item["props"] = item_props_for_width
                item_props_for_width["width"] = f"{int(round(box_width))}px"

                # No per-object width-override stamping. The frontend
                # ``UniversalFieldShell.resolveColumnTrack`` will:
                #   * label column → ``globalStyles.horizontalLabelBandPx``
                #     (form-wide band, matches "all labels start where the
                #     longest label ends" UAT-round-9 ask)
                #   * input column → ``minmax(0, 1fr)`` (absorbs slack)
                #   * validation column → ``minmax(0, max-content)``
                #     (auto-grows to whatever message the runtime emits)

                row_height = _reserved_height(item, layout_mode=layout_mode)

            components.append(item)
            row_solver_decisions.append({
                "rowIndex": entry_idx,
                "decision": row_decision,
                "componentIds": [item["id"]],
                "rowGroup": None,  # ignored in horizontal mode
                "subRowIndex": 0,
                "widthSlack": 0,
                # Horizontal-mode-specific extras for trace consumers.
                "validationDroppedBelow": validation_dropped_below,
                "layoutMode": LAYOUT_MODE_HORIZONTAL_STACKED,
            })

            bottom = y_cursor + row_height
            if bottom > max_bottom:
                max_bottom = bottom
            y_cursor += row_height + DEFAULT_ROW_GAP

        # Refresh the per-component widthPx in stageDiagnostics so the trace
        # shows the *bounding box* the renderer actually receives (= content
        # width) rather than the tier target the loop above stamped before
        # we knew which mode would win. Heights are unchanged for the most
        # part — only when validation drops below do we bump them, and we
        # reflect that here too so the diagnostic matches what shipped.
        components_by_id = {c["id"]: c for c in components}
        for diag in diagnostics:
            placed = components_by_id.get(diag["componentId"])
            if placed is None:
                continue
            diag["widthPx"] = int(placed["style"]["width"])
            diag["heightPx"] = int(placed["style"]["height"])

    # ---------- Phase 2: aligned-grid placement (vertical-packed) ----------
    # Group every queued sub-row by its column count k. For each k >= 2, the
    # column grid uses ``col_max[c] = max(item.width across all k-col rows)``
    # so column 1 lines up under column 1, column 2 under column 2, etc. If
    # the column grid doesn't fit content_width, shrink it proportionally
    # toward the per-column ``col_min`` (mirrors the per-row solver math).
    # Solo rows (k=1) pin x = MARGIN_X so single-column rows share a left edge
    # with each other AND with column-0 of the multi-rows.
    #
    # Skipped entirely when the horizontal-stacked branch above has already
    # placed every component — the two branches are mutually exclusive
    # placement strategies.
    elif layout_mode == LAYOUT_MODE_VERTICAL_PACKED:
        col_max_by_k: Dict[int, List[float]] = {}
        col_min_by_k: Dict[int, List[float]] = {}
        for sr in placed_subrows:
            k = len(sr["items"])
            if k < 2:
                continue
            if k not in col_max_by_k:
                col_max_by_k[k] = [0.0] * k
                col_min_by_k[k] = [0.0] * k
            for c in range(k):
                col_max_by_k[k][c] = max(col_max_by_k[k][c], sr["widths"][c])
                col_min_by_k[k][c] = max(
                    col_min_by_k[k][c], float(sr["items"][c]["_solverMin"])
                )

        grid_widths_by_k: Dict[int, List[float]] = {}
        for k, col_max in col_max_by_k.items():
            gaps_total = (k - 1) * MIN_COLUMN_GAP
            target_total = sum(col_max)
            if target_total + gaps_total <= content_width + 0.5:
                grid_widths_by_k[k] = list(col_max)
                continue
            col_min = col_min_by_k[k]
            available = content_width - gaps_total
            shrinkable_slack = sum(col_max[c] - col_min[c] for c in range(k))
            need = target_total - available
            if shrinkable_slack <= 0.5 or need >= shrinkable_slack:
                grid_widths_by_k[k] = list(col_min)
            else:
                scale = need / shrinkable_slack
                grid_widths_by_k[k] = [
                    max(col_min[c], col_max[c] - (col_max[c] - col_min[c]) * scale)
                    for c in range(k)
                ]

        # Place every sub-row in queue order.
        max_bottom = float(DEFAULT_MARGIN_Y)
        for sr in placed_subrows:
            items = sr["items"]
            k = len(items)
            if sr["leadingSectionGap"] > 0.0:
                y_cursor += sr["leadingSectionGap"]

            if k >= 2:
                widths = grid_widths_by_k[k]
                x_cursor = float(DEFAULT_MARGIN_X)
                # UAT round 5 — reserve style.height + per-type rendered chrome so
                # textarea/submit/file-upload stop overlapping the next row. The
                # rendered DOM places label + input + validation as separately
                # stacked objects (see ``UniversalFieldShell``); for most types
                # the chrome budget is 0 because their renderer already fits
                # everything inside ``style.height``.
                row_height = max(_reserved_height(it) for it in items)
                for c, item in enumerate(items):
                    item["style"]["width"] = int(round(widths[c]))
                    item["position"]["x"] = int(round(x_cursor))
                    item["position"]["y"] = int(round(y_cursor))
                    components.append(item)
                    x_cursor += widths[c] + MIN_COLUMN_GAP
                actual_slack = max(
                    0.0, content_width - sum(widths) - (k - 1) * MIN_COLUMN_GAP
                )
            else:
                it = items[0]
                it_type = str(it.get("type", "")).strip()
                align = sr["alignments"][0] if sr["alignments"] else None
                it_w = float(it["style"]["width"])

                if it_type in ALWAYS_FULL_WIDTH_TYPES:
                    # Banners/dividers/terms always span the full content row.
                    it["style"]["width"] = int(round(content_width))
                    it_w = float(it["style"]["width"])
                    x_cursor = float(DEFAULT_MARGIN_X)
                elif it_type == "submit-button":
                    # Submit-button keeps its actionAlignment semantics (LLM owns
                    # this hint). Default = center; left/right pin to that edge.
                    # Width is also clamped to content_width here so we no longer
                    # need a separate constraint pass.
                    if it_w > content_width:
                        it["style"]["width"] = int(round(content_width))
                        it_w = float(it["style"]["width"])
                        submit_button_clamped = True
                    if align == "left":
                        x_cursor = float(DEFAULT_MARGIN_X)
                    elif align == "right":
                        x_cursor = float(DEFAULT_MARGIN_X) + max(
                            0.0, content_width - it_w
                        )
                    else:
                        x_cursor = float(DEFAULT_MARGIN_X) + max(
                            0.0, (content_width - it_w) / 2.0
                        )
                else:
                    # Every other solo input pins to the common left edge so
                    # single-component rows line up under each other and under
                    # the column-0 of any multi-rows.
                    x_cursor = float(DEFAULT_MARGIN_X)

                it["position"]["x"] = int(round(x_cursor))
                it["position"]["y"] = int(round(y_cursor))
                components.append(it)
                # UAT round 5 — same chrome reservation as the multi-column branch.
                row_height = _reserved_height(it)
                actual_slack = max(0.0, content_width - it_w)

            # Record the FINAL solver decision (with grid-aligned widths) so the
            # rowSolverDecisions diagnostic reflects what shipped.
            row_solver_decisions.append({
                "rowIndex": len(row_solver_decisions),
                "decision": sr["decision"],
                "componentIds": [it["id"] for it in items],
                "rowGroup": sr["rowgroup"],
                "subRowIndex": sr["subRowIndex"],
                "widthSlack": int(round(actual_slack)),
            })

            bottom = y_cursor + row_height
            if bottom > max_bottom:
                max_bottom = bottom
            y_cursor += row_height + DEFAULT_ROW_GAP

    # UAT round 3 — canvas grows vertically as needed. The single-page constraint
    # was removed because forms with rating/textarea/file-upload simply cannot
    # fit on a 980 px mobile canvas; the renderer scrolls.
    desired_height = int(math.ceil(max_bottom + DEFAULT_MARGIN_Y))
    if desired_height > canvas_height:
        canvas_height = desired_height
    canvas_height_grew = desired_height > int(
        _parse_positive_number(runtime_canvas.get("height"), DEFAULT_CANVAS_HEIGHT)
    )

    # Final normalization: deterministic tab order from geometry.
    ordered: List[Dict[str, Any]] = sorted(
        components,
        key=lambda item: (
            float(item["position"]["y"]),
            float(item["position"]["x"]),
            item["id"],
        ),
    )
    for tab_index, raw_item in enumerate(ordered, start=1):
        item = raw_item
        props = item.get("props")
        if not isinstance(props, dict):
            props = {}
            item["props"] = props
        props["tabOrder"] = tab_index

    for item in components:
        item.pop("widthIntentResolved", None)
        item.pop("_solverMin", None)
        item.pop("_solverTarget", None)
        item.pop("_solverMax", None)

    # Story 6.3.1 (UAT round 6) — Fix C: stamp the form-wide horizontal label
    # band on the AI-emitted definition. The frontend's
    # ``applyValidatedDefinition`` reducer reads ``definition.globalStyles
    # .horizontalLabelBandPx`` and merges it into the preserved global styles
    # (only that one knob is allowed through — see the reducer comment for
    # why). For vertical-packed forms we emit ``None`` to make it explicit
    # that the compiler intentionally skipped the band; the frontend reducer
    # only patches when it sees a finite number, so vertical-mode generations
    # don't accidentally clobber a previously-stamped value.
    horizontal_label_band_px = (
        _estimate_horizontal_label_band_px(semantic_plan, content_width)
        if layout_mode == LAYOUT_MODE_HORIZONTAL_STACKED
        else None
    )

    global_styles_payload: Dict[str, Any] = {}
    if horizontal_label_band_px is not None:
        global_styles_payload["horizontalLabelBandPx"] = horizontal_label_band_px

    final_definition: Dict[str, Any] = {
        "schemaVersion": "1.0",
        "formId": semantic_plan.formId or "ai-generated-form",
        "theme": theme,
        "canvasSettings": {
            "width": canvas_width,
            "height": canvas_height,
            "gridSize": grid_size,
        },
        "pages": [
            {
                "id": "page-1",
                "title": semantic_plan.title or "Page 1",
                "components": ordered,
            }
        ],
    }
    if global_styles_payload:
        final_definition["globalStyles"] = global_styles_payload

    # Story 6.3.1 UAT round 5 — render-then-measure: how many components in
    # this pass had ground-truth measured heights vs per-type estimates. This
    # lets us distinguish a fresh ``/generate`` (everything estimated) from
    # the second ``/remeasure`` pass (everything measured) in the trace.
    measured_components = sum(
        1 for c in ordered if c.get("_heightSource") == "measured"
    )
    estimated_components = len(ordered) - measured_components
    if measured_components > 0 and estimated_components == 0:
        heights_source_label = "measured"
    elif measured_components == 0:
        heights_source_label = "estimated"
    else:
        heights_source_label = "mixed"

    # Strip the ``_heightSource`` debug marker before emitting components —
    # downstream consumers (renderer, validator, persistence) only ever see
    # the public schema. The marker is summarised in compileSummary instead.
    for component in ordered:
        component.pop("_heightSource", None)

    compile_summary = {
        "compilerMode": "deterministic-grid",
        # Story 6.3.1 (UAT round 6) — Phase 2 layout-mode resolution.
        # ``"vertical-packed"`` is the default: each input renders as
        # label-above-input and the row solver packs them by rowGroup.
        # ``"horizontal-stacked"`` means the form is configured for
        # ``[ Label ][ Input ][ Validation ]`` rows — every component gets
        # its own row at full content width and the renderer's column split
        # produces canvas-scaled label / input / validation columns. Per-row
        # ``rowSolverDecisions[i].validationDroppedBelow`` records whether
        # the validation message had to wrap below the input on that row.
        "layoutMode": layout_mode,
        # Story 6.3.1 (UAT round 6) — Fix C trace field. ``None`` for vertical
        # mode (the compiler doesn't author this knob outside horizontal-
        # stacked geometry); a positive int when the compiler stamped a
        # form-wide label band on ``definition.globalStyles
        # .horizontalLabelBandPx``. Lets us answer "did the AI think this form
        # needed a 240 px or a 160 px label band?" in the trace without
        # having to inspect the emitted definition.
        "horizontalLabelBandPx": horizontal_label_band_px,
        "inputComponentCount": len(semantic_plan.components),
        "outputComponentCount": len(ordered),
        "droppedComponentCount": dropped_components,
        "droppedComponentReasons": dropped_component_reasons,
        "fallbackCount": fallback_count,
        "submitButtonClamped": submit_button_clamped,
        "sectionCount": len(section_keys_seen),
        "rowGroupCount": len(row_group_keys_seen),
        "canvasHeightGrew": canvas_height_grew,
        # Story 6.3.1 UAT round 5 — render-then-measure trace fields.
        # ``heightsSource`` is one of "estimated" (no measurements provided —
        # this is a fresh ``/generate`` first pass), "measured" (every
        # component was sized from a frontend-supplied DOM measurement, the
        # second-pass ``/remeasure`` happy path), or "mixed" (partial
        # measurements — usually means a few components were missing from
        # the frontend payload, e.g. dynamically-rendered slots).
        "heightsSource": heights_source_label,
        "measuredComponentCount": measured_components,
        "estimatedComponentCount": estimated_components,
        # Story 6.3.1 UAT round 4 — list of label-driven componentType remaps
        # (e.g. textarea→address). Empty when the LLM picked the right type.
        "componentTypeRemaps": component_type_remaps,
        "stageDiagnostics": diagnostics,
        # Phase 2 S4 trace fields. ``rowSolverDecisions`` records every placed
        # sub-row with its solver decision (fit/shrink/reflow/force-min) and
        # leftover horizontal slack. ``rowGroupSplits`` lists rowGroups whose
        # items the solver had to split across multiple sub-rows because they
        # couldn't fit horizontally even after proportional shrink. Both are
        # additive — older consumers ignore the keys.
        "rowSolverDecisions": row_solver_decisions,
        "rowGroupSplits": row_group_splits,
        "policyFlags": {
            "semanticOnly": bool(
                isinstance(capability_policy_json, dict)
                and isinstance(capability_policy_json.get("step1"), dict)
                and capability_policy_json.get("step1", {}).get("allowSemanticOnly") is True
            ),
            "gridOnly": bool(
                isinstance(capability_policy_json, dict)
                and isinstance(capability_policy_json.get("step2"), dict)
                and capability_policy_json.get("step2", {}).get("gridOnly") is True
            ),
        },
    }
    return final_definition, compile_summary
