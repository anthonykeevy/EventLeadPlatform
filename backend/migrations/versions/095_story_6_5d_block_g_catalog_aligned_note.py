"""Story 6.5d: Block G prose note — catalog-resident types only (no ghost types).

Revision ID: 095
Revises: 094
"""

from alembic import op
from sqlalchemy import text


revision = "095"
down_revision = "094"
branch_labels = None
depends_on = None

CATALOG_NOTE = (
    "\n\n## Catalog alignment (Story 6.5d)\n"
    "Emit only component types returned by the COMPONENT_CAPABILITY block above. "
    "Do not invent types such as last-name that are not in the allowed list. "
    "For AU online forms use address-lookup-au or company-lookup-abr only when "
    "they appear in the allowed list; otherwise use address or text fallbacks.\n"
)


def upgrade() -> None:
    connection = op.get_bind()
    connection.execute(
        text(
            """
            DECLARE @VersionID BIGINT;
            SELECT TOP 1 @VersionID = prv.[PromptAssemblyRegistryVersionID]
            FROM [config].[PromptAssemblyRegistryVersion] prv
            INNER JOIN [config].[PromptAssemblyRegistry] pr
                ON pr.[PromptAssemblyRegistryID] = prv.[PromptAssemblyRegistryID]
            WHERE pr.[Code] = N'FORM_AI_V1'
              AND prv.[IsActive] = 1
              AND prv.[IsDeleted] = 0
            ORDER BY prv.[VersionNumber] DESC;

            IF @VersionID IS NULL RETURN;

            DECLARE @SectionID BIGINT;
            SELECT @SectionID = [PromptSectionID]
            FROM [config].[PromptSection]
            WHERE [PromptAssemblyRegistryVersionID] = @VersionID
              AND [SectionCode] = N'G'
              AND [IsDeleted] = 0;

            IF @SectionID IS NULL RETURN;

            UPDATE psv
            SET [PromptSnippet] = [PromptSnippet] + :note
            FROM [config].[PromptSectionVariant] psv
            WHERE psv.[PromptSectionID] = @SectionID
              AND psv.[VariantCode] = N'DEFAULT'
              AND psv.[IsDeleted] = 0
              AND psv.[PromptSnippet] NOT LIKE N'%Catalog alignment (Story 6.5d)%';
            """
        ),
        {"note": CATALOG_NOTE},
    )


def downgrade() -> None:
    connection = op.get_bind()
    connection.execute(
        text(
            """
            DECLARE @VersionID BIGINT;
            SELECT TOP 1 @VersionID = prv.[PromptAssemblyRegistryVersionID]
            FROM [config].[PromptAssemblyRegistryVersion] prv
            INNER JOIN [config].[PromptAssemblyRegistry] pr
                ON pr.[PromptAssemblyRegistryID] = prv.[PromptAssemblyRegistryID]
            WHERE pr.[Code] = N'FORM_AI_V1'
              AND prv.[IsActive] = 1
              AND prv.[IsDeleted] = 0
            ORDER BY prv.[VersionNumber] DESC;

            IF @VersionID IS NULL RETURN;

            DECLARE @SectionID BIGINT;
            SELECT @SectionID = [PromptSectionID]
            FROM [config].[PromptSection]
            WHERE [PromptAssemblyRegistryVersionID] = @VersionID
              AND [SectionCode] = N'G'
              AND [IsDeleted] = 0;

            IF @SectionID IS NULL RETURN;

            UPDATE psv
            SET [PromptSnippet] = REPLACE(
                [PromptSnippet],
                :note,
                N''
            )
            FROM [config].[PromptSectionVariant] psv
            WHERE psv.[PromptSectionID] = @SectionID
              AND psv.[VariantCode] = N'DEFAULT'
              AND psv.[IsDeleted] = 0;
            """
        ),
        {"note": CATALOG_NOTE},
    )
