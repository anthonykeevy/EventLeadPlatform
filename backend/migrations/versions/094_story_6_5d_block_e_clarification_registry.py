"""Story 6.5d: Block E1/E2/E3 clarification sections in Prompt Assembly Registry.

Revision ID: 094
Revises: 093
"""

from alembic import op
from sqlalchemy import text


revision = "094"
down_revision = "093"
branch_labels = None
depends_on = None


def upgrade() -> None:
    connection = op.get_bind()
    connection.execute(
        text(
            """
            IF EXISTS (
                SELECT 1 FROM sys.check_constraints
                WHERE [name] = N'CK_PromptSection_DataStructureType'
                  AND [parent_object_id] = OBJECT_ID(N'config.PromptSection')
            )
            ALTER TABLE [config].[PromptSection]
            DROP CONSTRAINT [CK_PromptSection_DataStructureType];

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
            ORDER BY prv.[VersionNumber] DESC;

            IF @VersionID IS NULL RETURN;

            DECLARE @Sections TABLE (
                SectionCode NVARCHAR(10),
                DisplayName NVARCHAR(100),
                SortOrder INT,
                Heading NVARCHAR(500)
            );
            INSERT INTO @Sections VALUES
                (N'E1', N'CLARIFICATION_LOCALE', 32, N'Audience Locale'),
                (N'E2', N'CLARIFICATION_PURPOSE', 33, N'Form Purpose'),
                (N'E3', N'CLARIFICATION_RESPONDENT', 34, N'Respondent Type');

            DECLARE @Code NVARCHAR(10);
            DECLARE @Display NVARCHAR(100);
            DECLARE @Sort INT;
            DECLARE @Heading NVARCHAR(500);
            DECLARE @SectionID BIGINT;

            DECLARE section_cursor CURSOR LOCAL FAST_FORWARD FOR
                SELECT SectionCode, DisplayName, SortOrder, Heading FROM @Sections;
            OPEN section_cursor;
            FETCH NEXT FROM section_cursor INTO @Code, @Display, @Sort, @Heading;
            WHILE @@FETCH_STATUS = 0
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM [config].[PromptSection]
                    WHERE [PromptAssemblyRegistryVersionID] = @VersionID
                      AND [SectionCode] = @Code
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
                    VALUES (@VersionID, @Code, @Display, @Sort, 1, N'Refs', @Heading, SYSUTCDATETIME(), 0);
                    SET @SectionID = SCOPE_IDENTITY();
                END
                ELSE
                BEGIN
                    SELECT @SectionID = [PromptSectionID]
                    FROM [config].[PromptSection]
                    WHERE [PromptAssemblyRegistryVersionID] = @VersionID
                      AND [SectionCode] = @Code
                      AND [IsDeleted] = 0;
                END

                IF NOT EXISTS (
                    SELECT 1 FROM [config].[PromptSectionVariant]
                    WHERE [PromptSectionID] = @SectionID
                      AND [VariantCode] = N'DEFAULT'
                      AND [IsDeleted] = 0
                )
                INSERT INTO [config].[PromptSectionVariant]
                (
                    [PromptSectionID],
                    [VariantCode],
                    [DisplayName],
                    [IsDefault],
                    [PromptSnippet],
                    [VariantVersion],
                    [CreatedUtc],
                    [IsDeleted]
                )
                VALUES (
                    @SectionID, N'DEFAULT', N'Default clarification block',
                    1, N'', 1, SYSUTCDATETIME(), 0
                );

                FETCH NEXT FROM section_cursor INTO @Code, @Display, @Sort, @Heading;
            END
            CLOSE section_cursor;
            DEALLOCATE section_cursor;
            """
        )
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

            UPDATE psv SET psv.[IsDeleted] = 1
            FROM [config].[PromptSectionVariant] psv
            INNER JOIN [config].[PromptSection] ps ON ps.[PromptSectionID] = psv.[PromptSectionID]
            WHERE ps.[PromptAssemblyRegistryVersionID] = @VersionID
              AND ps.[SectionCode] IN (N'E1', N'E2', N'E3');

            UPDATE ps SET ps.[IsDeleted] = 1
            FROM [config].[PromptSection] ps
            WHERE ps.[PromptAssemblyRegistryVersionID] = @VersionID
              AND ps.[SectionCode] IN (N'E1', N'E2', N'E3');
            """
        )
    )
