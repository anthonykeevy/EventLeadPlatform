"""Capability model and prompt text generation for Form AI."""

from __future__ import annotations

from typing import Literal, TypedDict

SupportLevel = Literal["strong", "moderate", "limited"]


class FormBuilderCapabilities(TypedDict):
    headers: SupportLevel
    paragraphs: SupportLevel
    dividers: SupportLevel
    style_overrides: SupportLevel
    mixed_object_layout: SupportLevel
    multi_column_layout: SupportLevel
    label_emphasis: SupportLevel
    help_text_emphasis: SupportLevel
    input_height_override: SupportLevel
    submit_alignment_and_width: SupportLevel
    section_visual_emphasis: SupportLevel


DEFAULT_FORM_BUILDER_CAPABILITIES: FormBuilderCapabilities = {
    "headers": "moderate",
    "paragraphs": "moderate",
    "dividers": "moderate",
    "style_overrides": "moderate",
    "mixed_object_layout": "limited",
    "multi_column_layout": "strong",
    "label_emphasis": "moderate",
    "help_text_emphasis": "limited",
    "input_height_override": "limited",
    "submit_alignment_and_width": "strong",
    "section_visual_emphasis": "limited",
}


_CAPABILITY_REASONING: dict[str, dict[SupportLevel, str]] = {
    "headers": {
        "strong": "Use headers when sections are genuinely distinct and they improve scanability.",
        "moderate": "Use at most one to two headers for major section boundaries.",
        "limited": "Do not rely on decorative headers; prefer spacing and grouping.",
    },
    "paragraphs": {
        "strong": "Use concise paragraphs for intent-setting and instructions.",
        "moderate": "Use short instructional paragraphs only when they reduce user confusion.",
        "limited": "Avoid paragraph-heavy designs; keep text minimal.",
    },
    "dividers": {
        "strong": "Use dividers to separate large semantic sections.",
        "moderate": "Use sparingly; no more than one per major transition.",
        "limited": "Avoid decorative divider use; spacing is preferred.",
    },
    "style_overrides": {
        "strong": "Apply purposeful, restrained overrides for emphasis on key fields.",
        "moderate": "Use minimal overrides; prioritize structural clarity over styling.",
        "limited": "Avoid reliance on style overrides for hierarchy.",
    },
    "mixed_object_layout": {
        "strong": "Use mixed layouts when they clearly improve density without harming readability.",
        "moderate": "Use mixed layout only for specific fields with a clear space benefit.",
        "limited": "Prefer standard vertical layout; avoid mixed layout in general generation.",
    },
    "multi_column_layout": {
        "strong": "Use two-column rows for related short fields where width permits.",
        "moderate": "Use multi-column only on stable rows with clear grouping.",
        "limited": "Prefer single-column flow unless a row is obviously safe.",
    },
    "label_emphasis": {
        "strong": "Use subtle label weight/size differences for critical fields.",
        "moderate": "Use very restrained label emphasis and only for key fields.",
        "limited": "Keep label styling mostly uniform.",
    },
    "help_text_emphasis": {
        "strong": "Use emphasized help text for high-risk inputs.",
        "moderate": "Use concise help text with minimal emphasis.",
        "limited": "Do not depend on help text styling for hierarchy.",
    },
    "input_height_override": {
        "strong": "Use height overrides for select key controls when it improves usability.",
        "moderate": "Use input height overrides rarely and only for clear purpose.",
        "limited": "Avoid input height overrides except where absolutely needed.",
    },
    "submit_alignment_and_width": {
        "strong": "Use submit alignment/width options to create a clear final action area.",
        "moderate": "Use standard aligned submit placement with conservative width choices.",
        "limited": "Keep submit placement simple and predictable.",
    },
    "section_visual_emphasis": {
        "strong": "Create section emphasis with restrained combinations of structure and typography.",
        "moderate": "Rely mainly on grouping and spacing; use visual emphasis lightly.",
        "limited": "Do not attempt decorative hierarchy; use clean structural grouping only.",
    },
}


def build_capability_boundary_section(
    capabilities: FormBuilderCapabilities = DEFAULT_FORM_BUILDER_CAPABILITIES,
) -> str:
    lines = [
        "## Capability Boundaries",
        "",
        "Design only within verified renderer capabilities. Do not invent visual effects.",
        "When capability is limited, prefer clean grouping, spacing, and ordering over decoration.",
        "",
        f"- Headers: {capabilities['headers']}. {_CAPABILITY_REASONING['headers'][capabilities['headers']]}",
        f"- Paragraphs: {capabilities['paragraphs']}. {_CAPABILITY_REASONING['paragraphs'][capabilities['paragraphs']]}",
        f"- Dividers: {capabilities['dividers']}. {_CAPABILITY_REASONING['dividers'][capabilities['dividers']]}",
        f"- Style overrides: {capabilities['style_overrides']}. {_CAPABILITY_REASONING['style_overrides'][capabilities['style_overrides']]}",
        f"- Mixed object layouts: {capabilities['mixed_object_layout']}. {_CAPABILITY_REASONING['mixed_object_layout'][capabilities['mixed_object_layout']]}",
        f"- Multi-column layouts: {capabilities['multi_column_layout']}. {_CAPABILITY_REASONING['multi_column_layout'][capabilities['multi_column_layout']]}",
        f"- Label emphasis: {capabilities['label_emphasis']}. {_CAPABILITY_REASONING['label_emphasis'][capabilities['label_emphasis']]}",
        f"- Help text emphasis: {capabilities['help_text_emphasis']}. {_CAPABILITY_REASONING['help_text_emphasis'][capabilities['help_text_emphasis']]}",
        f"- Input height overrides: {capabilities['input_height_override']}. {_CAPABILITY_REASONING['input_height_override'][capabilities['input_height_override']]}",
        f"- Submit alignment and width: {capabilities['submit_alignment_and_width']}. {_CAPABILITY_REASONING['submit_alignment_and_width'][capabilities['submit_alignment_and_width']]}",
        f"- Section-level visual emphasis: {capabilities['section_visual_emphasis']}. {_CAPABILITY_REASONING['section_visual_emphasis'][capabilities['section_visual_emphasis']]}",
        "",
        "### Graceful Fallback Rules",
        "- When section emphasis is weak, rely on grouping and spacing rather than decorative headers.",
        "- When style overrides are limited, prefer clean structure over forced emphasis.",
        "- When multi-column layout is risky, use single-column grouping.",
        "- When components do not visually differentiate well, avoid excessive sections.",
        "- Do not create decorative hierarchy that renders flat.",
        "- Use the simplest professional layout that fits platform strengths.",
    ]
    return "\n".join(lines)

