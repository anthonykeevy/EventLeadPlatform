"""Enhanced User Profile for Epic 2

Revision ID: 013_enhanced_user_profile
Revises: 012_unique_abn_constraint
Create Date: 2025-10-26 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = '013_enhanced_user_profile'
down_revision = '012'
branch_labels = None
depends_on = None


def upgrade():
    # =====================================================================
    # 1. Create ThemePreference Reference Table
    # =====================================================================
    op.create_table('ThemePreference',
        sa.Column('ThemePreferenceID', sa.BigInteger(), nullable=False),
        sa.Column('ThemeCode', sa.String(length=20), nullable=False),
        sa.Column('ThemeName', sa.String(length=50), nullable=False),
        sa.Column('Description', sa.String(length=200), nullable=False),
        sa.Column('CSSClass', sa.String(length=50), nullable=False),
        sa.Column('IsActive', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('SortOrder', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=True),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('ThemePreferenceID'),
        sa.UniqueConstraint('ThemeCode'),
        schema='ref'
    )

    # Insert theme options
    op.execute("""
        INSERT INTO [ref].[ThemePreference] (ThemeCode, ThemeName, Description, CSSClass, SortOrder)
        VALUES
            ('light', 'Light Theme', 'Clean, bright interface with light backgrounds', 'theme-light', 1),
            ('dark', 'Dark Theme', 'Dark interface with dark backgrounds for low-light environments', 'theme-dark', 2),
            ('high-contrast', 'High Contrast', 'High contrast theme for accessibility and vision-impaired users', 'theme-high-contrast', 3),
            ('system', 'System Default', 'Follows the user''s operating system theme preference', 'theme-system', 4)
    """)

    # =====================================================================
    # 2. Create LayoutDensity Reference Table
    # =====================================================================
    op.create_table('LayoutDensity',
        sa.Column('LayoutDensityID', sa.BigInteger(), nullable=False),
        sa.Column('DensityCode', sa.String(length=20), nullable=False),
        sa.Column('DensityName', sa.String(length=50), nullable=False),
        sa.Column('Description', sa.String(length=200), nullable=False),
        sa.Column('CSSClass', sa.String(length=50), nullable=False),
        sa.Column('IsActive', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('SortOrder', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=True),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('LayoutDensityID'),
        sa.UniqueConstraint('DensityCode'),
        schema='ref'
    )

    # Insert layout density options
    op.execute("""
        INSERT INTO [ref].[LayoutDensity] (DensityCode, DensityName, Description, CSSClass, SortOrder)
        VALUES
            ('compact', 'Compact', 'Tight spacing for power users and small screens', 'layout-compact', 1),
            ('comfortable', 'Comfortable', 'Balanced spacing for optimal readability and usability', 'layout-comfortable', 2),
            ('spacious', 'Spacious', 'Generous spacing for accessibility and large screens', 'layout-spacious', 3)
    """)

    # =====================================================================
    # 3. Create FontSize Reference Table
    # =====================================================================
    op.create_table('FontSize',
        sa.Column('FontSizeID', sa.BigInteger(), nullable=False),
        sa.Column('SizeCode', sa.String(length=20), nullable=False),
        sa.Column('SizeName', sa.String(length=50), nullable=False),
        sa.Column('Description', sa.String(length=200), nullable=False),
        sa.Column('CSSClass', sa.String(length=50), nullable=False),
        sa.Column('BaseFontSize', sa.String(length=10), nullable=False),
        sa.Column('IsActive', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('SortOrder', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=True),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('FontSizeID'),
        sa.UniqueConstraint('SizeCode'),
        schema='ref'
    )

    # Insert font size options
    op.execute("""
        INSERT INTO [ref].[FontSize] (SizeCode, SizeName, Description, CSSClass, BaseFontSize, SortOrder)
        VALUES
            ('small', 'Small', 'Smaller text for compact interfaces and power users', 'font-small', '14px', 1),
            ('medium', 'Medium', 'Standard text size for optimal readability', 'font-medium', '16px', 2),
            ('large', 'Large', 'Larger text for accessibility and easy reading', 'font-large', '18px', 3)
    """)

    # =====================================================================
    # 4. Add fields to User table
    # =====================================================================
    op.add_column('User', sa.Column('Bio', sa.String(length=500), nullable=True), schema='dbo')
    op.add_column('User', sa.Column('ThemePreferenceID', sa.BigInteger(), nullable=True), schema='dbo')
    op.add_column('User', sa.Column('LayoutDensityID', sa.BigInteger(), nullable=True), schema='dbo')
    op.add_column('User', sa.Column('FontSizeID', sa.BigInteger(), nullable=True), schema='dbo')

    # =====================================================================
    # 5. Add Foreign Key Constraints
    # =====================================================================
    op.create_foreign_key('FK_User_ThemePreference', 'User', 'ThemePreference', ['ThemePreferenceID'], ['ThemePreferenceID'], source_schema='dbo', referent_schema='ref')
    op.create_foreign_key('FK_User_LayoutDensity', 'User', 'LayoutDensity', ['LayoutDensityID'], ['LayoutDensityID'], source_schema='dbo', referent_schema='ref')
    op.create_foreign_key('FK_User_FontSize', 'User', 'FontSize', ['FontSizeID'], ['FontSizeID'], source_schema='dbo', referent_schema='ref')

    # =====================================================================
    # 6. Create UserIndustry junction table
    # =====================================================================
    op.create_table('UserIndustry',
        sa.Column('UserIndustryID', sa.BigInteger(), nullable=False),
        sa.Column('UserID', sa.BigInteger(), nullable=False),
        sa.Column('IndustryID', sa.BigInteger(), nullable=False),
        sa.Column('IsPrimary', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('SortOrder', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=True),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('UserIndustryID'),
        sa.ForeignKeyConstraint(['UserID'], ['dbo.User.UserID'], name='FK_UserIndustry_User'),
        sa.ForeignKeyConstraint(['IndustryID'], ['ref.Industry.IndustryID'], name='FK_UserIndustry_Industry'),
        sa.ForeignKeyConstraint(['CreatedBy'], ['dbo.User.UserID'], name='FK_UserIndustry_CreatedBy'),
        sa.ForeignKeyConstraint(['UpdatedBy'], ['dbo.User.UserID'], name='FK_UserIndustry_UpdatedBy'),
        sa.ForeignKeyConstraint(['DeletedBy'], ['dbo.User.UserID'], name='FK_UserIndustry_DeletedBy'),
        sa.UniqueConstraint('UserID', 'IndustryID', name='UX_UserIndustry_User_Industry'),
        sa.CheckConstraint('(IsPrimary = 1 AND SortOrder = 0) OR (IsPrimary = 0 AND SortOrder > 0)', name='CK_UserIndustry_Primary'),
        schema='dbo'
    )

    # =====================================================================
    # 7. Create Indexes for Performance
    # =====================================================================
    # Note: SQL Server doesn't support filtered indexes with WHERE clause in Alembic the same way as PostgreSQL
    # We'll create regular indexes instead
    op.create_index('IX_User_ThemePreferenceID', 'User', ['ThemePreferenceID'], unique=False, schema='dbo')
    op.create_index('IX_User_LayoutDensityID', 'User', ['LayoutDensityID'], unique=False, schema='dbo')
    op.create_index('IX_User_FontSizeID', 'User', ['FontSizeID'], unique=False, schema='dbo')
    
    op.create_index('IX_UserIndustry_UserID', 'UserIndustry', ['UserID', 'IsDeleted'], unique=False, schema='dbo')
    op.create_index('IX_UserIndustry_IndustryID', 'UserIndustry', ['IndustryID', 'IsDeleted'], unique=False, schema='dbo')
    op.create_index('IX_UserIndustry_IsPrimary', 'UserIndustry', ['UserID', 'IsPrimary'], unique=False, schema='dbo')


def downgrade():
    # =====================================================================
    # Rollback in reverse order
    # =====================================================================
    
    # Drop indexes
    op.drop_index('IX_UserIndustry_IsPrimary', table_name='UserIndustry', schema='dbo')
    op.drop_index('IX_UserIndustry_IndustryID', table_name='UserIndustry', schema='dbo')
    op.drop_index('IX_UserIndustry_UserID', table_name='UserIndustry', schema='dbo')
    op.drop_index('IX_User_FontSizeID', table_name='User', schema='dbo')
    op.drop_index('IX_User_LayoutDensityID', table_name='User', schema='dbo')
    op.drop_index('IX_User_ThemePreferenceID', table_name='User', schema='dbo')
    
    # Drop UserIndustry table
    op.drop_table('UserIndustry', schema='dbo')
    
    # Drop foreign key constraints
    op.drop_constraint('FK_User_FontSize', 'User', type_='foreignkey', schema='dbo')
    op.drop_constraint('FK_User_LayoutDensity', 'User', type_='foreignkey', schema='dbo')
    op.drop_constraint('FK_User_ThemePreference', 'User', type_='foreignkey', schema='dbo')
    
    # Drop columns from User table
    op.drop_column('User', 'FontSizeID', schema='dbo')
    op.drop_column('User', 'LayoutDensityID', schema='dbo')
    op.drop_column('User', 'ThemePreferenceID', schema='dbo')
    op.drop_column('User', 'Bio', schema='dbo')
    
    # Drop reference tables
    op.drop_table('FontSize', schema='ref')
    op.drop_table('LayoutDensity', schema='ref')
    op.drop_table('ThemePreference', schema='ref')
