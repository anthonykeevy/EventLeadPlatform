"""Story 6.4.8: Update AU PromptTemplateLocaleBlock with AU-005 behaviour + AU-006 lint-clean wording.

Revision ID: 072
Revises: 071
Create Date: 2026-05-07
"""

from alembic import op


revision = "072"
down_revision = "071"
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
            THROW 6441051, 'FORM_AI_STEP1_BASE PromptTemplate is required before updating AU locale blocks.', 1;
        IF @CountryID IS NULL
            THROW 6441052, 'AU Country row is required before updating AU locale blocks.', 1;

        ;WITH Blocks AS (
            SELECT *
            FROM (VALUES
                (
                    N'format',
                    N'Audience locale AU is authoritative for all generated form copy and component configuration. Use Australian English and AU conventions for phone (local mobile help text including country code if overseas), dates (DD/MM/YYYY), address labels (Suburb / State / Postcode), currency (AUD), privacy, marketing-message consent, waivers, terms, and acknowledgements. When a user prompt includes foreign-market cues that conflict with AU, generate the Australian equivalent unless the form is explicitly collecting an external destination or source-market value. Avoid generated timezone options or labels that introduce foreign phone-code-like strings or overseas region names unless the form is explicitly collecting an external value. Preserve publish-ready ordering: identity and contact fields first, form-specific choices next, operational notes and preferences after that, consent and terms near the end. Include every material field group requested by the user. Make required or optional intent explicit through validationIntent. Choose the most specific supported component type. Prefer checkbox or terms acknowledgement patterns over typed signatures unless a signature is explicitly requested. Do not add address, organisation, role, or extra context fields unless requested or clearly necessary.'
                ),
                (
                    N'policy',
                    N'For Australian forms, consent and privacy copy must cite the Privacy Act 1988 when personal information is collected and the Spam Act 2003 for marketing opt-ins. Keep consent plain-English, specific to the collection purpose, and reference AU Privacy Principles where appropriate. Do not substitute generic GDPR wording.'
                ),
                (
                    N'tone',
                    N'Australian tone defaults to practical, plain-English, low-formality copy. Be friendly and direct; avoid excessive honorifics, legalese, or over-mandatory language unless the user asks. Describe categories of conflicting cues and substitution behaviour positively rather than listing forbidden examples. Preserve AU-005 field coverage, validation intent accuracy, component specificity, and copy quality.'
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
                    N'Audience locale AU is authoritative for all generated form copy and component configuration. Use Australian English and AU conventions for phone (local mobile help text including country code if overseas), dates (DD/MM/YYYY), address labels (Suburb / State / Postcode), currency (AUD), privacy, marketing-message consent, waivers, terms, and acknowledgements. When a user prompt includes foreign-market cues that conflict with AU, generate the Australian equivalent unless the form is explicitly collecting an external destination or source-market value. Avoid generated timezone options or labels that introduce foreign phone-code-like strings or overseas region names unless the form is explicitly collecting an external value. Preserve publish-ready ordering: identity and contact fields first, form-specific choices next, operational notes and preferences after that, consent and terms near the end. Include every material field group requested by the user. Make required or optional intent explicit through validationIntent. Choose the most specific supported component type. Prefer checkbox or terms acknowledgement patterns over typed signatures unless a signature is explicitly requested. Do not add address, organisation, role, or extra context fields unless requested or clearly necessary.'
                ),
                (
                    N'policy',
                    N'For Australian forms, consent and privacy copy must cite the Privacy Act 1988 when personal information is collected and the Spam Act 2003 for marketing opt-ins. Keep consent plain-English, specific to the collection purpose, and reference AU Privacy Principles where appropriate. Do not substitute generic GDPR wording.'
                ),
                (
                    N'tone',
                    N'Australian tone defaults to practical, plain-English, low-formality copy. Be friendly and direct; avoid excessive honorifics, legalese, or over-mandatory language unless the user asks. Describe categories of conflicting cues and substitution behaviour positively rather than listing forbidden examples. Preserve AU-005 field coverage, validation intent accuracy, component specificity, and copy quality.'
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
    # Downgrade restores previous block bodies from Story 6.4.4.1 seed (065).
    # Exact prior text is preserved in migration 065; no data loss on downgrade path.
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

        IF @PromptTemplateID IS NULL OR @CountryID IS NULL
            RETURN;

        ;WITH PriorBlocks AS (
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
            [BlockBody] = p.[BlockBody],
            [ContentHash] = CONVERT(NVARCHAR(64), HASHBYTES('SHA2_256', CONVERT(NVARCHAR(MAX), p.[BlockBody])), 2),
            [UpdatedDate] = @Now
        FROM [config].[PromptTemplateLocaleBlock] existing
        INNER JOIN PriorBlocks p
            ON p.[BlockType] = existing.[BlockType]
        WHERE existing.[PromptTemplateID] = @PromptTemplateID
          AND existing.[CountryID] = @CountryID
          AND existing.[IsDeleted] = 0;
        """
    )
