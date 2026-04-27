"""Story 6.4.4.1: Seed AU locale prompt blocks.

Revision ID: 065
Revises: 064
Create Date: 2026-04-27
"""

from alembic import op


revision = "065"
down_revision = "064"
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
        DECLARE @CountryID BIGINT = (
            SELECT TOP 1 [CountryID]
            FROM [ref].[Country]
            WHERE [CountryCode] = N'AU'
              AND [IsDeleted] = 0
        );

        IF @PromptTemplateID IS NULL
            THROW 6441051, 'FORM_AI_STEP1_BASE PromptTemplate is required before seeding AU locale blocks.', 1;
        IF @CountryID IS NULL
            THROW 6441052, 'AU Country row is required before seeding AU locale blocks.', 1;

        ;WITH Blocks AS (
            SELECT *
            FROM (VALUES
                (
                    N'format',
                    N'Audience locale AU. Prefer DD/MM/YYYY dates, local Australian mobile help text ("Include country code if overseas"), Suburb / State / Postcode address labels, AUD currency, and First name / Last name or Given name / Surname.'
                ),
                (
                    N'policy',
                    N'For Australian forms, consent and privacy copy should cite the Privacy Act 1988 when personal information is collected and the Spam Act 2003 for marketing opt-ins. Keep consent plain-English, specific to the collection purpose, and do not substitute generic GDPR wording.'
                ),
                (
                    N'tone',
                    N'Australian tone defaults to practical, plain-English, low-formality copy. Be friendly and direct; avoid excessive honorifics, legalese, or over-mandatory language unless the user asks.'
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
          AND existing.[CountryID] = @CountryID
          AND existing.[IsDeleted] = 0;

        ;WITH Blocks AS (
            SELECT *
            FROM (VALUES
                (
                    N'format',
                    N'Audience locale AU. Prefer DD/MM/YYYY dates, local Australian mobile help text ("Include country code if overseas"), Suburb / State / Postcode address labels, AUD currency, and First name / Last name or Given name / Surname.'
                ),
                (
                    N'policy',
                    N'For Australian forms, consent and privacy copy should cite the Privacy Act 1988 when personal information is collected and the Spam Act 2003 for marketing opt-ins. Keep consent plain-English, specific to the collection purpose, and do not substitute generic GDPR wording.'
                ),
                (
                    N'tone',
                    N'Australian tone defaults to practical, plain-English, low-formality copy. Be friendly and direct; avoid excessive honorifics, legalese, or over-mandatory language unless the user asks.'
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
            @CountryID,
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
              AND existing.[CountryID] = @CountryID
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
        INNER JOIN [ref].[Country] country
            ON country.[CountryID] = blocks.[CountryID]
        WHERE template.[TemplateKey] = N'FORM_AI_STEP1_BASE'
          AND country.[CountryCode] = N'AU'
          AND blocks.[BlockType] IN (N'format', N'policy', N'tone');
        """
    )
