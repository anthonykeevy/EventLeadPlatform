"""Story 6.4.4.1: Seed Hofstede 6D country cultural dimensions.

Values are canonical Hofstede 6D country scores as commonly published by
The Culture Factor / Hofstede Insights for the listed markets. DE/JP/FR are
seeded as native-review stubs per story scope.

Revision ID: 068
Revises: 067
Create Date: 2026-04-27
"""

from alembic import op


revision = "068"
down_revision = "067"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.get_bind().exec_driver_sql(
        """
        DECLARE @Now DATETIME2 = GETUTCDATE();

        IF NOT EXISTS (SELECT 1 FROM [ref].[Country] WHERE [CountryCode] = N'DE' AND [IsDeleted] = 0)
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
            (N'DE', N'Germany', N'+49', N'EUR', N'EUR', N'Euro', 0.19, N'VAT', 1, N'VAT Number', NULL, NULL, 1, 70, @Now, 0);
        END;

        IF NOT EXISTS (SELECT 1 FROM [ref].[Country] WHERE [CountryCode] = N'JP' AND [IsDeleted] = 0)
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
            (N'JP', N'Japan', N'+81', N'JPY', N'JPY', N'Japanese Yen', 0.10, N'Consumption Tax', 1, N'Corporate Number', NULL, NULL, 1, 80, @Now, 0);
        END;

        IF NOT EXISTS (SELECT 1 FROM [ref].[Country] WHERE [CountryCode] = N'FR' AND [IsDeleted] = 0)
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
            (N'FR', N'France', N'+33', N'EUR', N'EUR', N'Euro', 0.20, N'VAT', 1, N'VAT Number', NULL, NULL, 1, 90, @Now, 0);
        END;

        ;WITH Dimensions AS (
            SELECT *
            FROM (VALUES
                (N'AU', 38, 51, 90, 61, 21, 71, N'Hofstede 6D 2010', 2010),
                (N'NZ', 22, 49, 79, 58, 33, 75, N'Hofstede 6D 2010', 2010),
                (N'GB', 35, 35, 89, 66, 51, 69, N'Hofstede 6D 2010', 2010),
                (N'US', 40, 46, 91, 62, 26, 68, N'Hofstede 6D 2010', 2010),
                (N'CA', 39, 48, 80, 52, 36, 68, N'Hofstede 6D 2010', 2010),
                (N'IE', 28, 35, 70, 68, 24, 65, N'Hofstede 6D 2010', 2010),
                (N'DE', 35, 65, 67, 66, 83, 40, N'Hofstede 6D 2010, requires native review', 2010),
                (N'JP', 54, 92, 46, 95, 88, 42, N'Hofstede 6D 2010, requires native review', 2010),
                (N'FR', 68, 86, 71, 43, 63, 48, N'Hofstede 6D 2010, requires native review', 2010)
            ) AS rows(
                [CountryCode], [PowerDistanceIndex], [UncertaintyAvoidanceIndex],
                [IndividualismIndex], [MasculinityIndex], [LongTermOrientation],
                [IndulgenceIndex], [Source], [SourceYear]
            )
        ),
        Resolved AS (
            SELECT
                country.[CountryID],
                dimensions.[PowerDistanceIndex],
                dimensions.[UncertaintyAvoidanceIndex],
                dimensions.[IndividualismIndex],
                dimensions.[MasculinityIndex],
                dimensions.[LongTermOrientation],
                dimensions.[IndulgenceIndex],
                dimensions.[Source],
                dimensions.[SourceYear]
            FROM Dimensions dimensions
            INNER JOIN [ref].[Country] country
                ON country.[CountryCode] = dimensions.[CountryCode]
               AND country.[IsDeleted] = 0
        )
        UPDATE existing
        SET
            [PowerDistanceIndex] = resolved.[PowerDistanceIndex],
            [UncertaintyAvoidanceIndex] = resolved.[UncertaintyAvoidanceIndex],
            [IndividualismIndex] = resolved.[IndividualismIndex],
            [MasculinityIndex] = resolved.[MasculinityIndex],
            [LongTermOrientation] = resolved.[LongTermOrientation],
            [IndulgenceIndex] = resolved.[IndulgenceIndex],
            [Source] = resolved.[Source],
            [SourceYear] = resolved.[SourceYear],
            [UpdatedDate] = @Now,
            [IsDeleted] = 0
        FROM [ref].[CountryCulturalDimensions] existing
        INNER JOIN Resolved resolved
            ON resolved.[CountryID] = existing.[CountryID]
        WHERE existing.[IsDeleted] = 0;

        ;WITH Dimensions AS (
            SELECT *
            FROM (VALUES
                (N'AU', 38, 51, 90, 61, 21, 71, N'Hofstede 6D 2010', 2010),
                (N'NZ', 22, 49, 79, 58, 33, 75, N'Hofstede 6D 2010', 2010),
                (N'GB', 35, 35, 89, 66, 51, 69, N'Hofstede 6D 2010', 2010),
                (N'US', 40, 46, 91, 62, 26, 68, N'Hofstede 6D 2010', 2010),
                (N'CA', 39, 48, 80, 52, 36, 68, N'Hofstede 6D 2010', 2010),
                (N'IE', 28, 35, 70, 68, 24, 65, N'Hofstede 6D 2010', 2010),
                (N'DE', 35, 65, 67, 66, 83, 40, N'Hofstede 6D 2010, requires native review', 2010),
                (N'JP', 54, 92, 46, 95, 88, 42, N'Hofstede 6D 2010, requires native review', 2010),
                (N'FR', 68, 86, 71, 43, 63, 48, N'Hofstede 6D 2010, requires native review', 2010)
            ) AS rows(
                [CountryCode], [PowerDistanceIndex], [UncertaintyAvoidanceIndex],
                [IndividualismIndex], [MasculinityIndex], [LongTermOrientation],
                [IndulgenceIndex], [Source], [SourceYear]
            )
        ),
        Resolved AS (
            SELECT
                country.[CountryID],
                dimensions.[PowerDistanceIndex],
                dimensions.[UncertaintyAvoidanceIndex],
                dimensions.[IndividualismIndex],
                dimensions.[MasculinityIndex],
                dimensions.[LongTermOrientation],
                dimensions.[IndulgenceIndex],
                dimensions.[Source],
                dimensions.[SourceYear]
            FROM Dimensions dimensions
            INNER JOIN [ref].[Country] country
                ON country.[CountryCode] = dimensions.[CountryCode]
               AND country.[IsDeleted] = 0
        )
        INSERT INTO [ref].[CountryCulturalDimensions]
        (
            [CountryID], [PowerDistanceIndex], [UncertaintyAvoidanceIndex],
            [IndividualismIndex], [MasculinityIndex], [LongTermOrientation],
            [IndulgenceIndex], [Source], [SourceYear], [CreatedDate], [IsDeleted]
        )
        SELECT
            resolved.[CountryID],
            resolved.[PowerDistanceIndex],
            resolved.[UncertaintyAvoidanceIndex],
            resolved.[IndividualismIndex],
            resolved.[MasculinityIndex],
            resolved.[LongTermOrientation],
            resolved.[IndulgenceIndex],
            resolved.[Source],
            resolved.[SourceYear],
            @Now,
            0
        FROM Resolved resolved
        WHERE NOT EXISTS (
            SELECT 1
            FROM [ref].[CountryCulturalDimensions] existing
            WHERE existing.[CountryID] = resolved.[CountryID]
              AND existing.[IsDeleted] = 0
        );

        IF NOT EXISTS (
            SELECT 1
            FROM [ref].[CountryCulturalDimensions]
            WHERE [CountryID] IS NULL
              AND [IsDeleted] = 0
        )
        BEGIN
            INSERT INTO [ref].[CountryCulturalDimensions]
            (
                [CountryID], [PowerDistanceIndex], [UncertaintyAvoidanceIndex],
                [IndividualismIndex], [MasculinityIndex], [LongTermOrientation],
                [IndulgenceIndex], [Source], [SourceYear], [CreatedDate], [IsDeleted]
            )
            VALUES
            (NULL, 50, 50, 50, 50, 50, 50, N'Neutral midpoint for INTL_ONLINE / NEUTRAL locale', NULL, @Now, 0);
        END;
        """
    )


def downgrade() -> None:
    op.get_bind().exec_driver_sql(
        """
        DELETE dimensions
        FROM [ref].[CountryCulturalDimensions] dimensions
        LEFT JOIN [ref].[Country] country
            ON country.[CountryID] = dimensions.[CountryID]
        WHERE dimensions.[CountryID] IS NULL
           OR country.[CountryCode] IN (N'AU', N'NZ', N'GB', N'US', N'CA', N'IE', N'DE', N'JP', N'FR');
        """
    )
