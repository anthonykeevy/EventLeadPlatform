"""Story 6.4.4.1: Seed Form AI locale default AppSettings.

Revision ID: 071
Revises: 070
Create Date: 2026-04-27
"""

from alembic import op


revision = "071"
down_revision = "070"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.get_bind().exec_driver_sql(
        """
        DECLARE @Now DATETIME2 = GETUTCDATE();

        DECLARE @StringTypeID BIGINT = (
            SELECT TOP 1 [SettingTypeID] FROM [ref].[SettingType]
            WHERE [TypeCode] = N'string' AND [IsActive] = 1
        );

        DECLARE @FormsCategoryID BIGINT = (
            SELECT TOP 1 [SettingCategoryID] FROM [ref].[SettingCategory]
            WHERE [CategoryCode] = N'forms' AND [IsActive] = 1
        );

        IF @StringTypeID IS NULL
            THROW 6441711, 'ref.SettingType string row is required before seeding Form AI locale settings.', 1;
        IF @FormsCategoryID IS NULL
            THROW 6441712, 'ref.SettingCategory forms row is required before seeding Form AI locale settings.', 1;

        ;WITH Settings AS (
            SELECT *
            FROM (VALUES
                (
                    N'form_ai.default_audience_locale',
                    N'AU',
                    N'Default audience locale for Form AI generation when request, event, company, and user do not supply one.',
                    N'AU',
                    N'^(AU|NZ|UK|US|CA|IE|DE|INTL_ONLINE|APAC|EU|NEUTRAL)$',
                    110
                ),
                (
                    N'form_ai.default_brand_posture',
                    N'local',
                    N'Default brand posture for Form AI generation when request and company do not supply one.',
                    N'local',
                    N'^(local|heritage|neutral|transcreate)$',
                    111
                ),
                (
                    N'form_ai.locale_block_render_strategy',
                    N'registry',
                    N'Locale prompt block rendering strategy for Form AI. registry uses config.PromptTemplateLocaleBlock.',
                    N'registry',
                    N'^(registry)$',
                    112
                )
            ) AS rows([SettingKey], [SettingValue], [Description], [DefaultValue], [ValidationRegex], [SortOrder])
        )
        UPDATE existing
        SET
            [SettingValue] = settings.[SettingValue],
            [Description] = settings.[Description],
            [DefaultValue] = settings.[DefaultValue],
            [SettingCategoryID] = @FormsCategoryID,
            [SettingTypeID] = @StringTypeID,
            [IsEditable] = 1,
            [ValidationRegex] = settings.[ValidationRegex],
            [MinValue] = NULL,
            [MaxValue] = NULL,
            [IsActive] = 1,
            [SortOrder] = settings.[SortOrder],
            [UpdatedDate] = @Now,
            [IsDeleted] = 0
        FROM [config].[AppSetting] existing
        INNER JOIN Settings settings
            ON settings.[SettingKey] = existing.[SettingKey]
        WHERE existing.[IsDeleted] = 0;

        ;WITH Settings AS (
            SELECT *
            FROM (VALUES
                (
                    N'form_ai.default_audience_locale',
                    N'AU',
                    N'Default audience locale for Form AI generation when request, event, company, and user do not supply one.',
                    N'AU',
                    N'^(AU|NZ|UK|US|CA|IE|DE|INTL_ONLINE|APAC|EU|NEUTRAL)$',
                    110
                ),
                (
                    N'form_ai.default_brand_posture',
                    N'local',
                    N'Default brand posture for Form AI generation when request and company do not supply one.',
                    N'local',
                    N'^(local|heritage|neutral|transcreate)$',
                    111
                ),
                (
                    N'form_ai.locale_block_render_strategy',
                    N'registry',
                    N'Locale prompt block rendering strategy for Form AI. registry uses config.PromptTemplateLocaleBlock.',
                    N'registry',
                    N'^(registry)$',
                    112
                )
            ) AS rows([SettingKey], [SettingValue], [Description], [DefaultValue], [ValidationRegex], [SortOrder])
        )
        INSERT INTO [config].[AppSetting]
        (
            [SettingKey], [SettingValue], [Description], [DefaultValue],
            [SettingCategoryID], [SettingTypeID],
            [IsEditable], [ValidationRegex], [MinValue], [MaxValue],
            [IsActive], [SortOrder], [CreatedDate], [IsDeleted]
        )
        SELECT
            settings.[SettingKey],
            settings.[SettingValue],
            settings.[Description],
            settings.[DefaultValue],
            @FormsCategoryID,
            @StringTypeID,
            1,
            settings.[ValidationRegex],
            NULL,
            NULL,
            1,
            settings.[SortOrder],
            @Now,
            0
        FROM Settings settings
        WHERE NOT EXISTS (
            SELECT 1
            FROM [config].[AppSetting] existing
            WHERE existing.[SettingKey] = settings.[SettingKey]
              AND existing.[IsDeleted] = 0
        );
        """
    )


def downgrade() -> None:
    op.get_bind().exec_driver_sql(
        """
        DELETE FROM [config].[AppSetting]
        WHERE [SettingKey] IN (
            N'form_ai.default_audience_locale',
            N'form_ai.default_brand_posture',
            N'form_ai.locale_block_render_strategy'
        );
        """
    )
