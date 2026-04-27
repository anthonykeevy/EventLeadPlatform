"""Story 6.4.4.1: Seed INTL_ONLINE / NEUTRAL locale prompt blocks.

Revision ID: 067
Revises: 066
Create Date: 2026-04-27
"""

from alembic import op


revision = "067"
down_revision = "066"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.get_bind().exec_driver_sql(
        """
        DECLARE @Now DATETIME2 = GETUTCDATE();
        DECLARE @PromptTemplateID BIGINT = (
            SELECT TOP 1 [PromptTemplateID]
            FROM [config].[PromptTemplate]
            WHERE [TemplateKey] = N'FORM_AI_STEP1_BASE'
              AND [IsDeleted] = 0
            ORDER BY [PromptTemplateID] DESC
        );

        IF @PromptTemplateID IS NULL
            THROW 6441071, 'FORM_AI_STEP1_BASE PromptTemplate is required before seeding INTL_ONLINE locale blocks.', 1;

        ;WITH Blocks AS (
            SELECT *
            FROM (VALUES
                (
                    N'format',
                    N'Audience locale INTL_ONLINE / NEUTRAL. Prefer ISO 8601 dates (YYYY-MM-DD), E.164 phone help text, single-line address with Country required, English-neutral spelling, and avoid region-specific labels unless the prompt names a market.'
                ),
                (
                    N'policy',
                    N'For international online forms, use jurisdiction-neutral privacy wording: state what personal data is collected, why it is collected, how it will be used, and require explicit marketing opt-in. Do not cite a country-specific law unless requested.'
                ),
                (
                    N'tone',
                    N'International online tone should be clear, neutral, and low-idiom. Avoid local slang, country-specific compliance claims, and assumptions about formality.'
                )
            ) AS rows([BlockType], [BlockBody])
        )
        UPDATE existing
        SET
            [BlockBody] = b.[BlockBody],
            [ContentHash] = CONVERT(NVARCHAR(64), HASHBYTES('SHA2_256', CONVERT(NVARCHAR(MAX), b.[BlockBody])), 2),
            [IsActive] = 1,
            [UpdatedDate] = @Now,
            [IsDeleted] = 0
        FROM [config].[PromptTemplateLocaleBlock] existing
        INNER JOIN Blocks b
            ON b.[BlockType] = existing.[BlockType]
        WHERE existing.[PromptTemplateID] = @PromptTemplateID
          AND existing.[CountryID] IS NULL
          AND existing.[IsDeleted] = 0;

        ;WITH Blocks AS (
            SELECT *
            FROM (VALUES
                (
                    N'format',
                    N'Audience locale INTL_ONLINE / NEUTRAL. Prefer ISO 8601 dates (YYYY-MM-DD), E.164 phone help text, single-line address with Country required, English-neutral spelling, and avoid region-specific labels unless the prompt names a market.'
                ),
                (
                    N'policy',
                    N'For international online forms, use jurisdiction-neutral privacy wording: state what personal data is collected, why it is collected, how it will be used, and require explicit marketing opt-in. Do not cite a country-specific law unless requested.'
                ),
                (
                    N'tone',
                    N'International online tone should be clear, neutral, and low-idiom. Avoid local slang, country-specific compliance claims, and assumptions about formality.'
                )
            ) AS rows([BlockType], [BlockBody])
        )
        INSERT INTO [config].[PromptTemplateLocaleBlock]
        (
            [PromptTemplateID], [CountryID], [BlockType], [BlockBody], [ContentHash],
            [IsActive], [CreatedDate], [IsDeleted]
        )
        SELECT
            @PromptTemplateID,
            NULL,
            b.[BlockType],
            b.[BlockBody],
            CONVERT(NVARCHAR(64), HASHBYTES('SHA2_256', CONVERT(NVARCHAR(MAX), b.[BlockBody])), 2),
            1,
            @Now,
            0
        FROM Blocks b
        WHERE NOT EXISTS (
            SELECT 1
            FROM [config].[PromptTemplateLocaleBlock] existing
            WHERE existing.[PromptTemplateID] = @PromptTemplateID
              AND existing.[CountryID] IS NULL
              AND existing.[BlockType] = b.[BlockType]
              AND existing.[IsDeleted] = 0
        );
        """
    )


def downgrade() -> None:
    op.get_bind().exec_driver_sql(
        """
        DELETE blocks
        FROM [config].[PromptTemplateLocaleBlock] blocks
        INNER JOIN [config].[PromptTemplate] template
            ON template.[PromptTemplateID] = blocks.[PromptTemplateID]
        WHERE template.[TemplateKey] = N'FORM_AI_STEP1_BASE'
          AND blocks.[CountryID] IS NULL
          AND blocks.[BlockType] IN (N'format', N'policy', N'tone');
        """
    )
