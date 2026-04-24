"""Story 6.4: Seed config.AppSetting row for form_ai.default_retries.

Adds a new AppSetting that controls the default number of system correction
attempts for AI form generation. The frontend no longer sends
maxSystemCorrectionAttempts on the request payload; instead the backend reads
this setting (cached on startup) to determine the retry budget.

  SettingKey:   form_ai.default_retries
  DefaultValue: 2
  SettingType:  Integer
  Category:     Forms (existing ref.SettingCategory row)
  Min: 0 / Max: 10

Revision ID: 061
Revises: 060
Create Date: 2026-04-24
"""

from alembic import op


revision = "061"
down_revision = "060"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.get_bind().exec_driver_sql(
        """
        DECLARE @Now DATETIME2 = GETUTCDATE();

        DECLARE @IntegerTypeID BIGINT = (
            SELECT TOP 1 [SettingTypeID] FROM [ref].[SettingType]
            WHERE [TypeCode] = N'integer' AND [IsActive] = 1
        );

        DECLARE @FormsCategoryID BIGINT = (
            SELECT TOP 1 [SettingCategoryID] FROM [ref].[SettingCategory]
            WHERE [CategoryCode] = N'forms' AND [IsActive] = 1
        );

        IF NOT EXISTS (
            SELECT 1 FROM [config].[AppSetting]
            WHERE [SettingKey] = N'form_ai.default_retries'
              AND [IsDeleted] = 0
        )
        BEGIN
            INSERT INTO [config].[AppSetting]
            (
                [SettingKey], [SettingValue], [Description], [DefaultValue],
                [SettingCategoryID], [SettingTypeID],
                [IsEditable], [ValidationRegex], [MinValue], [MaxValue],
                [IsActive], [SortOrder],
                [CreatedDate], [IsDeleted]
            )
            VALUES
            (
                N'form_ai.default_retries',
                N'2',
                N'Default number of system correction attempts for AI form generation. Frontend no longer sends this value; the backend reads it from this setting (cached on startup). Range: 0-10.',
                N'2',
                @FormsCategoryID,
                @IntegerTypeID,
                1,      -- IsEditable
                NULL,   -- ValidationRegex
                0,      -- MinValue
                10,     -- MaxValue
                1,      -- IsActive
                100,    -- SortOrder
                @Now,
                0
            );
        END
        """
    )


def downgrade() -> None:
    op.get_bind().exec_driver_sql(
        """
        DELETE FROM [config].[AppSetting]
        WHERE [SettingKey] = N'form_ai.default_retries';
        """
    )
