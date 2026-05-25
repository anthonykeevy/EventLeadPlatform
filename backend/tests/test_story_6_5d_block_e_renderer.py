"""Story 6.5d: Block E Refs renderer hydration."""
from __future__ import annotations

from modules.form_ai.prompt_assembly.renderer import render_prompt_assembly
from modules.form_ai.prompt_assembly.resolver import ResolvedAssembly, ResolvedSection
from modules.reference.clarification import ResolvedClarificationContext


def test_render_refs_block_e_sections():
    resolved = ResolvedAssembly(
        registry_code="FORM_AI_V1",
        registry_id=1,
        registry_version_id=1,
        version_number=1,
        sections=[
            ResolvedSection(
                section_code="E1",
                section_id=1,
                sort_order=32,
                data_structure_type="Refs",
                heading="Audience Locale",
                variant_id=1,
                variant_code="DEFAULT",
                snippet="",
            ),
            ResolvedSection(
                section_code="E2",
                section_id=2,
                sort_order=33,
                data_structure_type="Refs",
                heading="Form Purpose",
                variant_id=2,
                variant_code="DEFAULT",
                snippet="",
            ),
        ],
    )
    clarification = ResolvedClarificationContext(
        audience_locale_code="AU",
        form_purpose_code="EVENT_REGISTRATION",
        respondent_type_code="ATTENDEE",
        e1_summary="Audience Locale: Australia (AU) – test.",
        e2_hint="Event registration hint.",
        e3_hint="Attendee hint.",
    )
    rendered = render_prompt_assembly(resolved, clarification=clarification)
    assert "Australia (AU)" in rendered["E1"]
    assert "Event registration hint." in rendered["E2"]
