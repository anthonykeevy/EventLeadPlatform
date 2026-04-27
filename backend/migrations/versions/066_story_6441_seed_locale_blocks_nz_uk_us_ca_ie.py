"""Story 6.4.4.1: Seed NZ, UK, US, CA, and IE locale prompt blocks.

Revision ID: 066
Revises: 065
Create Date: 2026-04-27
"""

from alembic import op


revision = "066"
down_revision = "065"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.get_bind().exec_driver_sql(
        """
        DECLARE @Now DATETIME2 = GETUTCDATE();

        IF NOT EXISTS (SELECT 1 FROM [ref].[Country] WHERE [CountryCode] = N'IE' AND [IsDeleted] = 0)
        BEGIN
            INSERT INTO [ref].[Country]
            (
                [CountryCode], [CountryName], [PhonePrefix],
                [CurrencyCode], [CurrencySymbol], [CurrencyName],
                [TaxRate], [TaxName], [TaxInclusive], [TaxNumberLabel],
                [CompanyValidationProvider], [AddressValidationProvider],
                [IsActive], [SortOrder], [CreatedDate], [IsDeleted]
            )
            VALUES
            (
                N'IE', N'Ireland', N'+353',
                N'EUR', N'EUR', N'Euro',
                0.23, N'VAT', 1, N'VAT Number',
                NULL, NULL,
                1, 60, @Now, 0
            );
        END;

        DECLARE @PromptTemplateID BIGINT = (
            SELECT TOP 1 [PromptTemplateID]
            FROM [config].[PromptTemplate]
            WHERE [TemplateKey] = N'FORM_AI_STEP1_BASE'
              AND [IsDeleted] = 0
            ORDER BY [PromptTemplateID] DESC
        );

        IF @PromptTemplateID IS NULL
            THROW 6441061, 'FORM_AI_STEP1_BASE PromptTemplate is required before seeding locale blocks.', 1;

        ;WITH Blocks AS (
            SELECT *
            FROM (VALUES
                (N'NZ', N'format', N'Audience locale NZ. Prefer DD/MM/YYYY dates, local NZ phone guidance with +64 only when needed, NZ address labels such as Suburb / City / Postcode, NZD currency, and plain First name / Last name labels.'),
                (N'NZ', N'policy', N'For New Zealand forms, consent and privacy copy should reference the Privacy Act 2020 where personal information is collected. Keep opt-ins specific, plain-English, and separate marketing consent from service communications.'),
                (N'NZ', N'tone', N'New Zealand tone defaults to understated, practical, friendly copy. Avoid over-selling, excessive formality, and Australian-specific phrasing.'),

                (N'GB', N'format', N'Audience locale UK. Prefer DD/MM/YYYY dates, +44 phone help text only when international context matters, Town / County / Postcode address labels, GBP currency, and First name / Surname labels.'),
                (N'GB', N'policy', N'For UK forms, privacy copy should reference UK GDPR and the Data Protection Act 2018 where personal data is collected. Use clear consent wording and avoid implying EU-only processing rules.'),
                (N'GB', N'tone', N'UK tone defaults to clear, courteous, slightly reserved copy. Use British spelling, avoid hype, and keep required-field language firm but not heavy-handed.'),

                (N'US', N'format', N'Audience locale US. Prefer MM/DD/YYYY dates, +1 phone examples when useful, City / State / ZIP address labels, USD currency, and First name / Last name labels.'),
                (N'US', N'policy', N'For US forms, avoid inventing sensitive identifiers such as SSN or TIN unless explicitly requested and justified. Use state-neutral privacy language; mention CCPA/CPRA only for California-specific collection.'),
                (N'US', N'tone', N'US tone can be more direct and benefit-led than AU/UK. Keep copy concise, action-oriented, and customer-friendly without legal overreach.'),

                (N'CA', N'format', N'Audience locale CA. Prefer YYYY-MM-DD or DD/MM/YYYY only when context requires, +1 phone guidance, City / Province / Postal code labels, CAD currency, and First name / Last name labels.'),
                (N'CA', N'policy', N'For Canadian forms, privacy copy should reference PIPEDA for personal information collection unless a province-specific rule is requested. Keep marketing opt-in language explicit and separate.'),
                (N'CA', N'tone', N'Canadian tone defaults to polite, practical, and inclusive copy. Avoid US-only labels such as ZIP unless the audience locale is US.'),

                (N'IE', N'format', N'Audience locale IE. Prefer DD/MM/YYYY dates, +353 phone guidance only when international context matters, Town / County / Eircode address labels, EUR currency, and First name / Surname labels.'),
                (N'IE', N'policy', N'For Irish forms, privacy copy should reference GDPR and the Data Protection Act 2018 where personal data is collected. Use explicit consent for marketing and clear purpose-specific wording.'),
                (N'IE', N'tone', N'Irish tone defaults to warm, clear, and lightly informal copy. Use Irish/British spelling conventions and avoid US-specific field labels.')
            ) AS rows([CountryCode], [BlockType], [BlockBody])
        ),
        ResolvedBlocks AS (
            SELECT
                country.[CountryID],
                blocks.[BlockType],
                blocks.[BlockBody]
            FROM Blocks blocks
            INNER JOIN [ref].[Country] country
                ON country.[CountryCode] = blocks.[CountryCode]
               AND country.[IsDeleted] = 0
        )
        UPDATE existing
        SET
            [BlockBody] = resolved.[BlockBody],
            [ContentHash] = CONVERT(NVARCHAR(64), HASHBYTES('SHA2_256', CONVERT(NVARCHAR(MAX), resolved.[BlockBody])), 2),
            [IsActive] = 1,
            [UpdatedDate] = @Now,
            [IsDeleted] = 0
        FROM [config].[PromptTemplateLocaleBlock] existing
        INNER JOIN ResolvedBlocks resolved
            ON resolved.[CountryID] = existing.[CountryID]
           AND resolved.[BlockType] = existing.[BlockType]
        WHERE existing.[PromptTemplateID] = @PromptTemplateID
          AND existing.[IsDeleted] = 0;

        ;WITH Blocks AS (
            SELECT *
            FROM (VALUES
                (N'NZ', N'format', N'Audience locale NZ. Prefer DD/MM/YYYY dates, local NZ phone guidance with +64 only when needed, NZ address labels such as Suburb / City / Postcode, NZD currency, and plain First name / Last name labels.'),
                (N'NZ', N'policy', N'For New Zealand forms, consent and privacy copy should reference the Privacy Act 2020 where personal information is collected. Keep opt-ins specific, plain-English, and separate marketing consent from service communications.'),
                (N'NZ', N'tone', N'New Zealand tone defaults to understated, practical, friendly copy. Avoid over-selling, excessive formality, and Australian-specific phrasing.'),
                (N'GB', N'format', N'Audience locale UK. Prefer DD/MM/YYYY dates, +44 phone help text only when international context matters, Town / County / Postcode address labels, GBP currency, and First name / Surname labels.'),
                (N'GB', N'policy', N'For UK forms, privacy copy should reference UK GDPR and the Data Protection Act 2018 where personal data is collected. Use clear consent wording and avoid implying EU-only processing rules.'),
                (N'GB', N'tone', N'UK tone defaults to clear, courteous, slightly reserved copy. Use British spelling, avoid hype, and keep required-field language firm but not heavy-handed.'),
                (N'US', N'format', N'Audience locale US. Prefer MM/DD/YYYY dates, +1 phone examples when useful, City / State / ZIP address labels, USD currency, and First name / Last name labels.'),
                (N'US', N'policy', N'For US forms, avoid inventing sensitive identifiers such as SSN or TIN unless explicitly requested and justified. Use state-neutral privacy language; mention CCPA/CPRA only for California-specific collection.'),
                (N'US', N'tone', N'US tone can be more direct and benefit-led than AU/UK. Keep copy concise, action-oriented, and customer-friendly without legal overreach.'),
                (N'CA', N'format', N'Audience locale CA. Prefer YYYY-MM-DD or DD/MM/YYYY only when context requires, +1 phone guidance, City / Province / Postal code labels, CAD currency, and First name / Last name labels.'),
                (N'CA', N'policy', N'For Canadian forms, privacy copy should reference PIPEDA for personal information collection unless a province-specific rule is requested. Keep marketing opt-in language explicit and separate.'),
                (N'CA', N'tone', N'Canadian tone defaults to polite, practical, and inclusive copy. Avoid US-only labels such as ZIP unless the audience locale is US.'),
                (N'IE', N'format', N'Audience locale IE. Prefer DD/MM/YYYY dates, +353 phone guidance only when international context matters, Town / County / Eircode address labels, EUR currency, and First name / Surname labels.'),
                (N'IE', N'policy', N'For Irish forms, privacy copy should reference GDPR and the Data Protection Act 2018 where personal data is collected. Use explicit consent for marketing and clear purpose-specific wording.'),
                (N'IE', N'tone', N'Irish tone defaults to warm, clear, and lightly informal copy. Use Irish/British spelling conventions and avoid US-specific field labels.')
            ) AS rows([CountryCode], [BlockType], [BlockBody])
        ),
        ResolvedBlocks AS (
            SELECT country.[CountryID], blocks.[BlockType], blocks.[BlockBody]
            FROM Blocks blocks
            INNER JOIN [ref].[Country] country
                ON country.[CountryCode] = blocks.[CountryCode]
               AND country.[IsDeleted] = 0
        )
        INSERT INTO [config].[PromptTemplateLocaleBlock]
        (
            [PromptTemplateID], [CountryID], [BlockType], [BlockBody], [ContentHash],
            [IsActive], [CreatedDate], [IsDeleted]
        )
        SELECT
            @PromptTemplateID,
            resolved.[CountryID],
            resolved.[BlockType],
            resolved.[BlockBody],
            CONVERT(NVARCHAR(64), HASHBYTES('SHA2_256', CONVERT(NVARCHAR(MAX), resolved.[BlockBody])), 2),
            1,
            @Now,
            0
        FROM ResolvedBlocks resolved
        WHERE NOT EXISTS (
            SELECT 1
            FROM [config].[PromptTemplateLocaleBlock] existing
            WHERE existing.[PromptTemplateID] = @PromptTemplateID
              AND existing.[CountryID] = resolved.[CountryID]
              AND existing.[BlockType] = resolved.[BlockType]
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
          AND country.[CountryCode] IN (N'NZ', N'GB', N'US', N'CA', N'IE')
          AND blocks.[BlockType] IN (N'format', N'policy', N'tone');
        """
    )
