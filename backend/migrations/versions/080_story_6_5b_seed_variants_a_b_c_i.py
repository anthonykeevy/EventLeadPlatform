"""Story 6.5b: Seed PromptSectionVariant rows for Blocks A, B, I, C (4 variants).

Revision ID: 080
Revises: 079
Create Date: 2026-05-20

Seeds the variant prose for Blocks A, B, I, and C (4 brand-posture variants).
Block G (FEW_SHOT context pack) is seeded separately by migration 081 since
it's the R6 fix migration.

Snippet sources (verbatim from backend/modules/form_ai/service.py
*before* the renderer wires in - see git blame at base commit cb339ed):
  * Block A: lines 1879-1881 of service.py (role + JSON-only contract).
  * Block B: _CONSENT_GUIDANCE_BLOCK (the production default returned by
    _active_consent_guidance_block() when FORM_AI_EVAL_PROMPT_SHRINK_MODE
    is unset or 'h2-h4'). Eval-only modes 'baseline' and 'h4' would use
    _LEGACY_CONSENT_GUIDANCE_BLOCK; that path is not part of the production
    default and is out of scope for AC-19's pre-merge sign-off.
  * Block I: lines 1886-1910 of service.py (REQUIRED ROOT KEYS through
    'Use only Story 6.2/6.3.1 supported component catalog ...'). Seed
    snippet INCLUDES the trailing '\\n\\n' that lives in the literal so
    that _build_initial_messages can concatenate it directly with the
    capability_block / context_pack that follow it.
  * Block C: 4 variants matching _render_brand_posture_block() return
    values, one per brandPosture enum value. The 'heritage' variant uses
    `{heritageOrigin}` placeholder (renderer substitutes via
    str.format_map at render time when origin is non-empty).

IsDefault selection for Block C:
  - 'local' is the runtime fallback in the existing code
    (_render_brand_posture_block returns the local string when posture is
    None / unrecognised / heritage-without-origin), so IsDefault=1 is on
    'local'. The dev prompt's suggestion of 'neutral' as default would
    deviate from the current fallback and break byte-equivalence on
    AC-19; deferred to 6.5c if Tony wants a different default after the
    `ref.BrandPosture` cutover.

Block C variant `heritage` placeholder semantics:
  - Source code uses `{origin}` in an f-string at render time.
  - Registry variant uses literal `{heritageOrigin}` token; renderer
    substitutes via str.format_map only on Block C variant `heritage`.
"""

from alembic import op
from sqlalchemy import text


revision = "080"
down_revision = "079"
branch_labels = None
depends_on = None


# ---------------------------------------------------------------------------
# Canonical snippets - copied verbatim from service.py at base cb339ed.
# Tests in test_story_6_5b_equivalence.py compare these against the
# constants in service.py to guard against drift.
# ---------------------------------------------------------------------------

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


def _resolve_section_id(connection, registry_code: str, section_code: str) -> int:
    row = connection.execute(
        text(
            """
            SELECT TOP 1 ps.[PromptSectionID]
            FROM [config].[PromptSection] ps
            INNER JOIN [config].[PromptAssemblyRegistryVersion] prv
                ON prv.[PromptAssemblyRegistryVersionID] = ps.[PromptAssemblyRegistryVersionID]
            INNER JOIN [config].[PromptAssemblyRegistry] pr
                ON pr.[PromptAssemblyRegistryID] = prv.[PromptAssemblyRegistryID]
            WHERE pr.[Code] = :registry_code
              AND prv.[IsActive] = 1
              AND prv.[IsDeleted] = 0
              AND ps.[SectionCode] = :section_code
              AND ps.[IsDeleted] = 0
            """
        ),
        {"registry_code": registry_code, "section_code": section_code},
    ).scalar_one_or_none()
    if row is None:
        raise RuntimeError(
            f"Story 6.5b migration 080 cannot resolve PromptSectionID for "
            f"registry={registry_code!r}, section={section_code!r}. "
            f"Ensure migration 079 has run first."
        )
    return int(row)


def _insert_variant(
    connection,
    *,
    section_id: int,
    variant_code: str,
    display_name: str,
    description: str,
    is_default: bool,
    snippet: str,
    change_reason: str,
) -> None:
    existing = connection.execute(
        text(
            """
            SELECT TOP 1 [PromptSectionVariantID]
            FROM [config].[PromptSectionVariant]
            WHERE [PromptSectionID] = :section_id
              AND [VariantCode] = :variant_code
              AND [IsDeleted] = 0
            """
        ),
        {"section_id": section_id, "variant_code": variant_code},
    ).scalar_one_or_none()
    if existing is not None:
        return  # idempotent

    connection.execute(
        text(
            """
            INSERT INTO [config].[PromptSectionVariant]
            (
                [PromptSectionID],
                [VariantCode],
                [DisplayName],
                [Description],
                [IsDefault],
                [PromptSnippet],
                [VariantVersion],
                [IsLockedForEdits],
                [ActivatedUtc],
                [ChangeReason],
                [CreatedUtc],
                [IsDeleted]
            )
            VALUES
            (
                :section_id,
                :variant_code,
                :display_name,
                :description,
                :is_default,
                :snippet,
                1,
                0,
                GETUTCDATE(),
                :change_reason,
                GETUTCDATE(),
                0
            )
            """
        ),
        {
            "section_id": section_id,
            "variant_code": variant_code,
            "display_name": display_name,
            "description": description,
            "is_default": 1 if is_default else 0,
            "snippet": snippet,
            "change_reason": change_reason,
        },
    )


def upgrade() -> None:
    connection = op.get_bind()

    section_a = _resolve_section_id(connection, "FORM_AI_V1", "A")
    section_b = _resolve_section_id(connection, "FORM_AI_V1", "B")
    section_i = _resolve_section_id(connection, "FORM_AI_V1", "I")
    section_c = _resolve_section_id(connection, "FORM_AI_V1", "C")

    _insert_variant(
        connection,
        section_id=section_a,
        variant_code="DEFAULT",
        display_name="Default role + output contract",
        description=(
            "System role + JSON-only contract prose. Migrated from Python "
            "literals in service.py::_build_initial_messages by Story 6.5b."
        ),
        is_default=True,
        snippet=BLOCK_A_DEFAULT,
        change_reason="Initial migration of Block A from code literal to registry (Story 6.5b).",
    )

    _insert_variant(
        connection,
        section_id=section_b,
        variant_code="DEFAULT",
        display_name="Consent & legal acknowledgements guidance",
        description=(
            "Consent / legal-acknowledgement component-selection guidance "
            "(production default). Migrated from _CONSENT_GUIDANCE_BLOCK in "
            "service.py by Story 6.5b. Future stories may layer proper "
            "PII / brand-safety prose as a new variant version."
        ),
        is_default=True,
        snippet=BLOCK_B_DEFAULT,
        change_reason="Initial migration of Block B from code literal to registry (Story 6.5b).",
    )

    _insert_variant(
        connection,
        section_id=section_i,
        variant_code="DEFAULT",
        display_name="JSON output contract (FormSemanticPlan tail)",
        description=(
            "REQUIRED ROOT KEYS + EACH COMPONENT contract instructions "
            "(FormSemanticPlan tail). Migrated from Python literals in "
            "service.py by Story 6.5b. Snippet includes the trailing "
            "double-newline so the assembler can concatenate it directly "
            "with the capability_block / context_pack that follow it."
        ),
        is_default=True,
        snippet=BLOCK_I_DEFAULT,
        change_reason="Initial migration of Block I from code literal to registry (Story 6.5b).",
    )

    _insert_variant(
        connection,
        section_id=section_c,
        variant_code="local",
        display_name="Brand posture - local",
        description="Match copy voice to the resolved audience locale.",
        is_default=True,  # Default fallback per existing _render_brand_posture_block.
        snippet=BLOCK_C_LOCAL,
        change_reason="Initial migration of Block C local variant (Story 6.5b).",
    )

    _insert_variant(
        connection,
        section_id=section_c,
        variant_code="heritage",
        display_name="Brand posture - heritage",
        description=(
            "Lightly reflects brand heritage origin via {heritageOrigin} "
            "placeholder substituted by the renderer at request time."
        ),
        is_default=False,
        snippet=BLOCK_C_HERITAGE,
        change_reason="Initial migration of Block C heritage variant (Story 6.5b).",
    )

    _insert_variant(
        connection,
        section_id=section_c,
        variant_code="neutral",
        display_name="Brand posture - neutral",
        description="Market-neutral voice; locale still controls field shape and compliance.",
        is_default=False,
        snippet=BLOCK_C_NEUTRAL,
        change_reason="Initial migration of Block C neutral variant (Story 6.5b).",
    )

    _insert_variant(
        connection,
        section_id=section_c,
        variant_code="transcreate",
        display_name="Brand posture - transcreate",
        description="Adapt copy idiomatically while preserving user intent.",
        is_default=False,
        snippet=BLOCK_C_TRANSCREATE,
        change_reason="Initial migration of Block C transcreate variant (Story 6.5b).",
    )


def downgrade() -> None:
    op.get_bind().exec_driver_sql(
        """
        DECLARE @VersionID BIGINT = (
            SELECT TOP 1 prv.[PromptAssemblyRegistryVersionID]
            FROM [config].[PromptAssemblyRegistryVersion] prv
            INNER JOIN [config].[PromptAssemblyRegistry] pr
                ON pr.[PromptAssemblyRegistryID] = prv.[PromptAssemblyRegistryID]
            WHERE pr.[Code] = N'FORM_AI_V1'
              AND prv.[IsActive] = 1
              AND prv.[IsDeleted] = 0
        );

        IF @VersionID IS NULL RETURN;

        DELETE psv
        FROM [config].[PromptSectionVariant] psv
        INNER JOIN [config].[PromptSection] ps
            ON ps.[PromptSectionID] = psv.[PromptSectionID]
        WHERE ps.[PromptAssemblyRegistryVersionID] = @VersionID
          AND ps.[SectionCode] IN (N'A', N'B', N'C', N'I')
          AND psv.[VariantCode] IN (N'DEFAULT', N'local', N'heritage', N'neutral', N'transcreate');
        """
    )
