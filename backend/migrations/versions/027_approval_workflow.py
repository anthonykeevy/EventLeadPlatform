"""Add approval workflow settings

Revision ID: 027_add_approval_workflow_settings
Revises: 026_add_form_access_function
Create Date: 2025-11-24 12:00:00.000000

"""
from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = '027_approval_workflow'
down_revision = 'fix_agency_access_join_issue'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Add 'forms' setting category
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [ref].[SettingCategory] WHERE CategoryCode = 'forms')
        BEGIN
            INSERT INTO [ref].[SettingCategory] 
            (CategoryCode, CategoryName, Description, IsActive, SortOrder)
            VALUES 
            ('forms', 'Forms', 'Form builder and workflow settings', 1, 50)
        END
    """)

    # 2. Add default approval cost threshold setting
    # Key: forms.approval.default_cost_threshold
    # Value: 100.00
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [config].[AppSetting] WHERE SettingKey = 'forms.approval.default_cost_threshold')
        BEGIN
            DECLARE @CategoryId BIGINT = (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode = 'forms');
            DECLARE @TypeId BIGINT = (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode = 'decimal');

            INSERT INTO [config].[AppSetting] 
            (SettingKey, SettingValue, SettingCategoryID, SettingTypeID, DefaultValue, Description, IsEditable, MinValue, MaxValue, IsActive, SortOrder)
            VALUES 
            ('forms.approval.default_cost_threshold', '100.00', @CategoryId, @TypeId, '100.00', 'Default deployment cost threshold for form approval workflow', 1, 0.00, 999999.99, 1, 10)
        END
    """)


def downgrade() -> None:
    # Delete the setting
    op.execute("DELETE FROM [config].[AppSetting] WHERE SettingKey = 'forms.approval.default_cost_threshold'")
    
    # Note: We typically don't delete the category in downgrade as other settings might depend on it in future,
    # but for this specific migration reversibility, we can check if it's empty.
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [config].[AppSetting] WHERE SettingCategoryID = (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode = 'forms'))
        BEGIN
            DELETE FROM [ref].[SettingCategory] WHERE CategoryCode = 'forms'
        END
    """)

