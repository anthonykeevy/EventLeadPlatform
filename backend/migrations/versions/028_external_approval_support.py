"""External approval support

Revision ID: 028_external_approval_support
Revises: 027_approval_workflow
Create Date: 2025-11-25 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = '028_external_approval_support'
down_revision = '027_approval_workflow'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Add 'EXTERNAL' User Status
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [ref].[UserStatus] WHERE StatusCode = 'EXTERNAL')
        BEGIN
            INSERT INTO [ref].[UserStatus] 
            (StatusCode, StatusName, Description, AllowLogin, IsActive, SortOrder)
            VALUES 
            ('EXTERNAL', 'External User', 'External stakeholder with limited access (e.g., approval only)', 0, 1, 90)
        END
    """)

    # 2. Create FormApprovalToken table
    op.create_table(
        'FormApprovalToken',
        sa.Column('FormApprovalTokenID', sa.BigInteger(), nullable=False),
        sa.Column('FormID', sa.BigInteger(), nullable=False),
        sa.Column('Token', sa.NVARCHAR(length=255), nullable=False),
        sa.Column('Email', sa.NVARCHAR(length=255), nullable=False),
        sa.Column('UserID', sa.BigInteger(), nullable=True),
        sa.Column('ExpiresAt', sa.DateTime(), nullable=False),
        sa.Column('IsUsed', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('UsedAt', sa.DateTime(), nullable=True),
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('FormApprovalTokenID'),
        sa.ForeignKeyConstraint(('FormID',), ['dbo.Form.FormID']),
        sa.ForeignKeyConstraint(('UserID',), ['dbo.User.UserID']),
        sa.ForeignKeyConstraint(('CreatedBy',), ['dbo.User.UserID'])
    )

    # Add index on Token for fast lookups
    op.create_index('IX_FormApprovalToken_Token', 'FormApprovalToken', ['Token'], unique=True)

    # 3. Add 'forms.approval.urgency_threshold_days' setting
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [config].[AppSetting] WHERE SettingKey = 'forms.approval.urgency_threshold_days')
        BEGIN
            DECLARE @CategoryId BIGINT = (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode = 'forms');
            DECLARE @TypeId BIGINT = (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode = 'integer');

            INSERT INTO [config].[AppSetting] 
            (SettingKey, SettingValue, SettingCategoryID, SettingTypeID, DefaultValue, Description, IsEditable, MinValue, MaxValue, IsActive, SortOrder)
            VALUES 
            ('forms.approval.urgency_threshold_days', '3', @CategoryId, @TypeId, '3', 'Days before event start to consider approval urgent', 1, 1, 30, 1, 20)
        END
    """)

    # 4. Add 'forms.approval.allow_internal_domains' setting
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [config].[AppSetting] WHERE SettingKey = 'forms.approval.allow_internal_domains')
        BEGIN
            DECLARE @CategoryId BIGINT = (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode = 'forms');
            DECLARE @TypeId BIGINT = (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode = 'boolean');

            INSERT INTO [config].[AppSetting] 
            (SettingKey, SettingValue, SettingCategoryID, SettingTypeID, DefaultValue, Description, IsEditable, MinValue, MaxValue, IsActive, SortOrder)
            VALUES 
            ('forms.approval.allow_internal_domains', 'false', @CategoryId, @TypeId, 'false', 'Allow approvals from emails on the same domain', 1, 0, 0, 1, 30)
        END
    """)


def downgrade() -> None:
    # Remove settings
    op.execute("DELETE FROM [config].[AppSetting] WHERE SettingKey = 'forms.approval.allow_internal_domains'")
    op.execute("DELETE FROM [config].[AppSetting] WHERE SettingKey = 'forms.approval.urgency_threshold_days'")

    # Drop table
    op.drop_index('IX_FormApprovalToken_Token', table_name='FormApprovalToken')
    op.drop_table('FormApprovalToken')

    # Remove User Status (Optional - usually safe to leave ref data, but deleting if unused)
    op.execute("DELETE FROM [ref].[UserStatus] WHERE StatusCode = 'EXTERNAL' AND NOT EXISTS (SELECT 1 FROM [dbo].[User] WHERE StatusID = (SELECT UserStatusID FROM [ref].[UserStatus] WHERE StatusCode = 'EXTERNAL'))")
