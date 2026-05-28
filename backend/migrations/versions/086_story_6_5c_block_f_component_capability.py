"""Story 6.5c: Block F COMPONENT_CAPABILITY registry section + prose shell.

Revision ID: 086
Revises: 085
Create Date: 2026-05-20

Adds PromptSection F (COMPONENT_CAPABILITY, DynamicComponentCatalog) on the
active FORM_AI_V1 registry version. SortOrder=35 places Block F between I (30)
and G (40), matching legacy ``_build_initial_messages`` emission order.
"""

from alembic import op
from sqlalchemy import text


revision = "086"
down_revision = "085"
branch_labels = None
depends_on = None

BLOCK_F_SHELL = (
    "WidthIntent vocabulary reminder: use only the widthIntent hints listed "
    "per component type above. The deterministic compiler maps hints to pixel "
    "widths and may shrink fields further to fit the canvas."
)


def upgrade() -> None:
    connection = op.get_bind()

    # DynamicComponentCatalog (22 chars) exceeds the 6.5b NVARCHAR(20) column
    # and was not in the original CHECK constraint enum.
    connection.execute(
        text(
            """
            IF EXISTS (
                SELECT 1
                FROM sys.check_constraints
                WHERE [name] = N'CK_PromptSection_DataStructureType'
                  AND [parent_object_id] = OBJECT_ID(N'config.PromptSection')
            )
            ALTER TABLE [config].[PromptSection]
            DROP CONSTRAINT [CK_PromptSection_DataStructureType];

            ALTER TABLE [config].[PromptSection]
            ALTER COLUMN [DataStructureType] NVARCHAR(30) NOT NULL;

            ALTER TABLE [config].[PromptSection]
            ADD CONSTRAINT [CK_PromptSection_DataStructureType]
            CHECK (
                [DataStructureType] IN (
                    N'Prose',
                    N'Json',
                    N'Snapshot',
                    N'Refs',
                    N'DynamicComponentCatalog'
                )
            );
            """
        )
    )

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
            ORDER BY prv.[VersionNumber] DESC, prv.[PromptAssemblyRegistryVersionID] DESC;

            IF @VersionID IS NULL RETURN;

            DECLARE @SectionID BIGINT;

            IF NOT EXISTS (
                SELECT 1
                FROM [config].[PromptSection]
                WHERE [PromptAssemblyRegistryVersionID] = @VersionID
                  AND [SectionCode] = N'F'
                  AND [IsDeleted] = 0
            )
            BEGIN
                INSERT INTO [config].[PromptSection]
                (
                    [PromptAssemblyRegistryVersionID],
                    [SectionCode],
                    [DisplayName],
                    [SortOrder],
                    [IsRequired],
                    [DataStructureType],
                    [Heading],
                    [CreatedUtc],
                    [IsDeleted]
                )
                VALUES
                (
                    @VersionID,
                    N'F',
                    N'COMPONENT_CAPABILITY',
                    35,
                    1,
                    N'DynamicComponentCatalog',
                    NULL,
                    SYSUTCDATETIME(),
                    0
                );
                SET @SectionID = SCOPE_IDENTITY();
            END
            ELSE
            BEGIN
                SELECT @SectionID = [PromptSectionID]
                FROM [config].[PromptSection]
                WHERE [PromptAssemblyRegistryVersionID] = @VersionID
                  AND [SectionCode] = N'F'
                  AND [IsDeleted] = 0;
            END

            IF NOT EXISTS (
                SELECT 1
                FROM [config].[PromptSectionVariant]
                WHERE [PromptSectionID] = @SectionID
                  AND [VariantCode] = N'DEFAULT'
                  AND [IsDeleted] = 0
            )
            BEGIN
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
                    @SectionID,
                    N'DEFAULT',
                    N'Component capability prose shell',
                    N'Story 6.5c Block F DynamicComponentCatalog shell',
                    1,
                    :snippet,
                    1,
                    0,
                    GETUTCDATE(),
                    N'Story 6.5c: seed Block F COMPONENT_CAPABILITY',
                    GETUTCDATE(),
                    0
                );
            END
            """
        ),
        {"snippet": BLOCK_F_SHELL},
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
            ORDER BY prv.[VersionNumber] DESC, prv.[PromptAssemblyRegistryVersionID] DESC;

            IF @VersionID IS NULL RETURN;

            DECLARE @SectionID BIGINT;
            SELECT @SectionID = [PromptSectionID]
            FROM [config].[PromptSection]
            WHERE [PromptAssemblyRegistryVersionID] = @VersionID
              AND [SectionCode] = N'F'
              AND [IsDeleted] = 0;

            IF @SectionID IS NULL RETURN;

            DELETE FROM [config].[PromptSectionVariant]
            WHERE [PromptSectionID] = @SectionID;

            DELETE FROM [config].[PromptSection]
            WHERE [PromptSectionID] = @SectionID;
            """
        )
    )

    connection.execute(
        text(
            """
            IF EXISTS (
                SELECT 1
                FROM sys.check_constraints
                WHERE [name] = N'CK_PromptSection_DataStructureType'
                  AND [parent_object_id] = OBJECT_ID(N'config.PromptSection')
            )
            ALTER TABLE [config].[PromptSection]
            DROP CONSTRAINT [CK_PromptSection_DataStructureType];

            ALTER TABLE [config].[PromptSection]
            ALTER COLUMN [DataStructureType] NVARCHAR(20) NOT NULL;

            ALTER TABLE [config].[PromptSection]
            ADD CONSTRAINT [CK_PromptSection_DataStructureType]
            CHECK (
                [DataStructureType] IN (
                    N'Prose',
                    N'Json',
                    N'Snapshot',
                    N'Refs'
                )
            );
            """
        )
    )
