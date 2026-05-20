"""Story 6.5b: Trim Block A ROLE_CONTRACT — remove Story 6.3.1 preamble line.

Revision ID: 083
Revises: 082
Create Date: 2026-05-20

UAT feedback: the first line of Block A
"You generate an EventLead semantic form plan for Story 6.3.1."
is internal story metadata, not LLM-facing contract prose. This migration
updates the seeded DEFAULT variant for section A on the active FORM_AI_V1
registry version.

Canonical source: ``backend/modules/form_ai/prompt_assembly/canonical_seeds.py::BLOCK_A_DEFAULT``.
Fresh installs that already ran the updated migration 080 literal get the
same text; this migration is required for databases that upgraded before
080 was amended.
"""

from alembic import op
from sqlalchemy import text


revision = "083"
down_revision = "082"
branch_labels = None
depends_on = None

_BLOCK_A_DEFAULT = (
    "Output a single JSON object only. No markdown or prose.\n"
    "Return FormSemanticPlan only; do not output any coordinates, "
    "pixel widths, x/y positions, style blocks, or final DefinitionJSON.\n"
)

_BLOCK_A_LEGACY = (
    "You generate an EventLead semantic form plan for Story 6.3.1.\n"
    "Output a single JSON object only. No markdown or prose.\n"
    "Return FormSemanticPlan only; do not output any coordinates, "
    "pixel widths, x/y positions, style blocks, or final DefinitionJSON.\n"
)


def upgrade() -> None:
    connection = op.get_bind()
    connection.execute(
        text(
            """
            UPDATE v
            SET
                v.[PromptSnippet] = :snippet,
                v.[ChangeReason] = N'Story 6.5b UAT: remove internal Story 6.3.1 preamble from Block A ROLE_CONTRACT',
                v.[LastUpdatedUtc] = SYSUTCDATETIME()
            FROM [config].[PromptSectionVariant] v
            INNER JOIN [config].[PromptSection] s
                ON s.[PromptSectionID] = v.[PromptSectionID]
            INNER JOIN [config].[PromptAssemblyRegistryVersion] prv
                ON prv.[PromptAssemblyRegistryVersionID] = s.[PromptAssemblyRegistryVersionID]
            INNER JOIN [config].[PromptAssemblyRegistry] pr
                ON pr.[PromptAssemblyRegistryID] = prv.[PromptAssemblyRegistryID]
            WHERE pr.[Code] = N'FORM_AI_V1'
              AND prv.[IsActive] = 1
              AND prv.[IsDeleted] = 0
              AND s.[SectionCode] = N'A'
              AND v.[VariantCode] = N'DEFAULT'
              AND v.[IsDeleted] = 0
            """
        ),
        {"snippet": _BLOCK_A_DEFAULT},
    )


def downgrade() -> None:
    connection = op.get_bind()
    connection.execute(
        text(
            """
            UPDATE v
            SET
                v.[PromptSnippet] = :snippet,
                v.[ChangeReason] = N'Revert 083: restore Block A with Story 6.3.1 preamble',
                v.[LastUpdatedUtc] = SYSUTCDATETIME()
            FROM [config].[PromptSectionVariant] v
            INNER JOIN [config].[PromptSection] s
                ON s.[PromptSectionID] = v.[PromptSectionID]
            INNER JOIN [config].[PromptAssemblyRegistryVersion] prv
                ON prv.[PromptAssemblyRegistryVersionID] = s.[PromptAssemblyRegistryVersionID]
            INNER JOIN [config].[PromptAssemblyRegistry] pr
                ON pr.[PromptAssemblyRegistryID] = prv.[PromptAssemblyRegistryID]
            WHERE pr.[Code] = N'FORM_AI_V1'
              AND prv.[IsActive] = 1
              AND prv.[IsDeleted] = 0
              AND s.[SectionCode] = N'A'
              AND v.[VariantCode] = N'DEFAULT'
              AND v.[IsDeleted] = 0
            """
        ),
        {"snippet": _BLOCK_A_LEGACY},
    )
