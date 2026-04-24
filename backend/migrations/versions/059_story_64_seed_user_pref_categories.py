"""Story 6.4: Seed ref.UserPreferenceCategory initial rows.

Seeds the four category placeholders (Notifications, Theme, Account, AI Agent).
Notifications is the active consumer for Story 6.4; the others are scaffolding
so future stories can add preferences without a category migration.

Revision ID: 059
Revises: 058
Create Date: 2026-04-24
"""

from alembic import op


revision = "059"
down_revision = "058"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.get_bind().exec_driver_sql(
        """
        DECLARE @Now DATETIME2 = GETUTCDATE();

        -- Notifications (first consumer for Story 6.4 — AI panel suppress-warning preference)
        IF NOT EXISTS (
            SELECT 1 FROM [ref].[UserPreferenceCategory]
            WHERE [CategoryName] = N'Notifications' AND [IsDeleted] = 0
        )
        BEGIN
            INSERT INTO [ref].[UserPreferenceCategory]
                ([CategoryName], [Description], [DisplayOrder], [IsActive], [CreatedDate], [IsDeleted])
            VALUES
                (N'Notifications', N'Control which in-product notifications and warnings are shown.', 10, 1, @Now, 0);
        END

        -- Theme (placeholder for future unification with ThemePreferenceID)
        IF NOT EXISTS (
            SELECT 1 FROM [ref].[UserPreferenceCategory]
            WHERE [CategoryName] = N'Theme' AND [IsDeleted] = 0
        )
        BEGIN
            INSERT INTO [ref].[UserPreferenceCategory]
                ([CategoryName], [Description], [DisplayOrder], [IsActive], [CreatedDate], [IsDeleted])
            VALUES
                (N'Theme', N'Appearance and display preferences.', 20, 1, @Now, 0);
        END

        -- Account (placeholder for future account-level preferences)
        IF NOT EXISTS (
            SELECT 1 FROM [ref].[UserPreferenceCategory]
            WHERE [CategoryName] = N'Account' AND [IsDeleted] = 0
        )
        BEGIN
            INSERT INTO [ref].[UserPreferenceCategory]
                ([CategoryName], [Description], [DisplayOrder], [IsActive], [CreatedDate], [IsDeleted])
            VALUES
                (N'Account', N'Account-level preferences and defaults.', 30, 1, @Now, 0);
        END

        -- AI Agent (placeholder for future AI generation preferences)
        IF NOT EXISTS (
            SELECT 1 FROM [ref].[UserPreferenceCategory]
            WHERE [CategoryName] = N'AI Agent' AND [IsDeleted] = 0
        )
        BEGIN
            INSERT INTO [ref].[UserPreferenceCategory]
                ([CategoryName], [Description], [DisplayOrder], [IsActive], [CreatedDate], [IsDeleted])
            VALUES
                (N'AI Agent', N'Preferences for AI form generation behaviour.', 40, 1, @Now, 0);
        END
        """
    )


def downgrade() -> None:
    op.get_bind().exec_driver_sql(
        """
        DELETE FROM [ref].[UserPreferenceCategory]
        WHERE [CategoryName] IN (N'Notifications', N'Theme', N'Account', N'AI Agent');
        """
    )
