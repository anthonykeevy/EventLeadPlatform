"""Story 6.4: Seed ref.UserPreferenceKey rows.

Seeds two preference keys in the Notifications category:

1. notifications.ai_agent.suppress_replace_warning (Boolean, default "false")
   - Active consumer: AIAgentPanel replace-form warning (ACs 2, 3, 13, 14)
   - Written when user checks "don't show again" and confirms generation

2. notifications.ai_agent.show_compile_summary (Boolean, default "true")
   - AC-15 demo: proves the architecture scales by rendering automatically
     in the Notifications UI without any frontend code change.
   - Not wired to any feature code in Story 6.4 — ref-seed only.
   - May be removed in a future cleanup story or promoted to a real feature.

Both look up SettingTypeID by TypeCode ('boolean') to avoid hardcoded IDs.

Revision ID: 060
Revises: 059
Create Date: 2026-04-24
"""

from alembic import op


revision = "060"
down_revision = "059"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.get_bind().exec_driver_sql(
        """
        DECLARE @Now DATETIME2 = GETUTCDATE();

        DECLARE @BooleanTypeID BIGINT = (
            SELECT TOP 1 [SettingTypeID] FROM [ref].[SettingType]
            WHERE [TypeCode] = N'boolean' AND [IsActive] = 1
        );

        DECLARE @NotificationsCategoryID BIGINT = (
            SELECT TOP 1 [UserPreferenceCategoryID] FROM [ref].[UserPreferenceCategory]
            WHERE [CategoryName] = N'Notifications' AND [IsDeleted] = 0
        );

        -- Preference key 1: suppress replace-warning (first real consumer — Story 6.4)
        IF NOT EXISTS (
            SELECT 1 FROM [ref].[UserPreferenceKey]
            WHERE [PreferenceKey] = N'notifications.ai_agent.suppress_replace_warning'
              AND [IsDeleted] = 0
        )
        BEGIN
            INSERT INTO [ref].[UserPreferenceKey]
            (
                [PreferenceKey], [PreferenceCategoryID], [SettingTypeID],
                [DisplayName], [Description], [DefaultValue],
                [IsEditable], [IsActive], [SortOrder], [CreatedDate], [IsDeleted]
            )
            VALUES
            (
                N'notifications.ai_agent.suppress_replace_warning',
                @NotificationsCategoryID,
                @BooleanTypeID,
                N'AI panel: suppress replace-form warning',
                N'When enabled, generating a new form over an existing canvas skips the confirmation dialog. Use Ctrl/Cmd+Z to undo.',
                N'false',
                1, 1, 10, @Now, 0
            );
        END

        -- Preference key 2: show compile summary (AC-15 demo — proves architecture scales)
        IF NOT EXISTS (
            SELECT 1 FROM [ref].[UserPreferenceKey]
            WHERE [PreferenceKey] = N'notifications.ai_agent.show_compile_summary'
              AND [IsDeleted] = 0
        )
        BEGIN
            INSERT INTO [ref].[UserPreferenceKey]
            (
                [PreferenceKey], [PreferenceCategoryID], [SettingTypeID],
                [DisplayName], [Description], [DefaultValue],
                [IsEditable], [IsActive], [SortOrder], [CreatedDate], [IsDeleted]
            )
            VALUES
            (
                N'notifications.ai_agent.show_compile_summary',
                @NotificationsCategoryID,
                @BooleanTypeID,
                N'AI panel: show compile summary',
                N'Demo preference (Story 6.4 AC-15). Seeded to prove the Notifications UI renders controls dynamically from the API without frontend code changes.',
                N'true',
                1, 1, 20, @Now, 0
            );
        END
        """
    )


def downgrade() -> None:
    op.get_bind().exec_driver_sql(
        """
        DELETE FROM [ref].[UserPreferenceKey]
        WHERE [PreferenceKey] IN (
            N'notifications.ai_agent.suppress_replace_warning',
            N'notifications.ai_agent.show_compile_summary'
        );
        """
    )
