"""Create Application Specification system tables (ApplicationSpecification, CountryApplicationSpecification, EnvironmentApplicationSpecification)

Revision ID: 005_application_specification_tables
Revises: 004_enhanced_features_tables
Create Date: 2025-10-13 12:04:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = '005_application_specification_tables'
down_revision = '004_enhanced_features_tables'
branch_labels = None
depends_on = None


def upgrade():
    """Create Application Specification system tables"""
    
    # =====================================================================
    # TABLE: ApplicationSpecification (Global Parameters)
    # =====================================================================
    op.create_table('ApplicationSpecification',
        sa.Column('SpecificationID', sa.BigInteger(), nullable=False),
        sa.Column('Category', sa.NVARCHAR(100), nullable=False),
        sa.Column('ParameterName', sa.NVARCHAR(200), nullable=False),
        sa.Column('ParameterValue', sa.NVARCHAR(), nullable=False),
        sa.Column('DataType', sa.NVARCHAR(50), nullable=False),
        sa.Column('Description', sa.NVARCHAR(500), nullable=False),
        sa.Column('IsActive', sa.Boolean(), nullable=False, default=True),
        sa.Column('SortOrder', sa.Integer(), nullable=False, default=999),
        sa.Column('DefaultValue', sa.NVARCHAR(), nullable=True),
        sa.Column('MinValue', sa.NVARCHAR(50), nullable=True),
        sa.Column('MaxValue', sa.NVARCHAR(50), nullable=True),
        sa.Column('AllowedValues', sa.NVARCHAR(), nullable=True),
        sa.Column('ValidationRegex', sa.NVARCHAR(500), nullable=True),
        sa.Column('HelpText', sa.NVARCHAR(1000), nullable=True),
        sa.Column('IsSystemParameter', sa.Boolean(), nullable=False, default=False),
        sa.Column('RequiresRestart', sa.Boolean(), nullable=False, default=False),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('SpecificationID'),
        sa.UniqueConstraint('Category', 'ParameterName', name='UQ_ApplicationSpecification_Category_Parameter')
    )
    
    # =====================================================================
    # TABLE: CountryApplicationSpecification (Country-Specific Overrides)
    # =====================================================================
    op.create_table('CountryApplicationSpecification',
        sa.Column('CountrySpecificationID', sa.BigInteger(), nullable=False),
        sa.Column('CountryID', sa.BigInteger(), nullable=False),
        sa.Column('Category', sa.NVARCHAR(100), nullable=False),
        sa.Column('ParameterName', sa.NVARCHAR(200), nullable=False),
        sa.Column('ParameterValue', sa.NVARCHAR(), nullable=False),
        sa.Column('DataType', sa.NVARCHAR(50), nullable=False),
        sa.Column('Description', sa.NVARCHAR(500), nullable=True),
        sa.Column('IsActive', sa.Boolean(), nullable=False, default=True),
        sa.Column('SortOrder', sa.Integer(), nullable=False, default=999),
        sa.Column('OverrideReason', sa.NVARCHAR(200), nullable=True),
        sa.Column('EffectiveDate', sa.DateTime(), nullable=True),
        sa.Column('ExpiryDate', sa.DateTime(), nullable=True),
        sa.Column('IsTemporary', sa.Boolean(), nullable=False, default=False),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('CountrySpecificationID'),
        sa.UniqueConstraint('CountryID', 'Category', 'ParameterName', name='UQ_CountryApplicationSpecification_Country_Category_Parameter')
    )
    
    # =====================================================================
    # TABLE: EnvironmentApplicationSpecification (Environment-Specific Overrides)
    # =====================================================================
    op.create_table('EnvironmentApplicationSpecification',
        sa.Column('EnvironmentSpecificationID', sa.BigInteger(), nullable=False),
        sa.Column('EnvironmentName', sa.NVARCHAR(50), nullable=False),
        sa.Column('CountryID', sa.BigInteger(), nullable=True),
        sa.Column('Category', sa.NVARCHAR(100), nullable=False),
        sa.Column('ParameterName', sa.NVARCHAR(200), nullable=False),
        sa.Column('ParameterValue', sa.NVARCHAR(), nullable=False),
        sa.Column('DataType', sa.NVARCHAR(50), nullable=False),
        sa.Column('Description', sa.NVARCHAR(500), nullable=True),
        sa.Column('IsActive', sa.Boolean(), nullable=False, default=True),
        sa.Column('SortOrder', sa.Integer(), nullable=False, default=999),
        sa.Column('OverrideReason', sa.NVARCHAR(200), nullable=True),
        sa.Column('EffectiveDate', sa.DateTime(), nullable=True),
        sa.Column('ExpiryDate', sa.DateTime(), nullable=True),
        sa.Column('IsTemporary', sa.Boolean(), nullable=False, default=False),
        sa.Column('RequiresApproval', sa.Boolean(), nullable=False, default=False),
        sa.Column('ApprovedBy', sa.BigInteger(), nullable=True),
        sa.Column('ApprovedAt', sa.DateTime(), nullable=True),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('EnvironmentSpecificationID'),
        sa.UniqueConstraint('EnvironmentName', 'CountryID', 'Category', 'ParameterName', name='UQ_EnvironmentApplicationSpecification_Environment_Country_Category_Parameter')
    )
    
    # =====================================================================
    # FOREIGN KEY CONSTRAINTS
    # =====================================================================
    
    # CountryApplicationSpecification foreign keys
    op.create_foreign_key('FK_CountryApplicationSpecification_Country', 'CountryApplicationSpecification', 'Country', ['CountryID'], ['CountryID'])
    
    # EnvironmentApplicationSpecification foreign keys
    op.create_foreign_key('FK_EnvironmentApplicationSpecification_Country', 'EnvironmentApplicationSpecification', 'Country', ['CountryID'], ['CountryID'])
    op.create_foreign_key('FK_EnvironmentApplicationSpecification_ApprovedBy', 'EnvironmentApplicationSpecification', 'User', ['ApprovedBy'], ['UserID'])
    
    # Audit trail foreign keys
    op.create_foreign_key('FK_ApplicationSpecification_CreatedBy', 'ApplicationSpecification', 'User', ['CreatedBy'], ['UserID'])
    op.create_foreign_key('FK_ApplicationSpecification_UpdatedBy', 'ApplicationSpecification', 'User', ['UpdatedBy'], ['UserID'])
    op.create_foreign_key('FK_ApplicationSpecification_DeletedBy', 'ApplicationSpecification', 'User', ['DeletedBy'], ['UserID'])
    
    op.create_foreign_key('FK_CountryApplicationSpecification_CreatedBy', 'CountryApplicationSpecification', 'User', ['CreatedBy'], ['UserID'])
    op.create_foreign_key('FK_CountryApplicationSpecification_UpdatedBy', 'CountryApplicationSpecification', 'User', ['UpdatedBy'], ['UserID'])
    op.create_foreign_key('FK_CountryApplicationSpecification_DeletedBy', 'CountryApplicationSpecification', 'User', ['DeletedBy'], ['UserID'])
    
    op.create_foreign_key('FK_EnvironmentApplicationSpecification_CreatedBy', 'EnvironmentApplicationSpecification', 'User', ['CreatedBy'], ['UserID'])
    op.create_foreign_key('FK_EnvironmentApplicationSpecification_UpdatedBy', 'EnvironmentApplicationSpecification', 'User', ['UpdatedBy'], ['UserID'])
    op.create_foreign_key('FK_EnvironmentApplicationSpecification_DeletedBy', 'EnvironmentApplicationSpecification', 'User', ['DeletedBy'], ['UserID'])
    
    # =====================================================================
    # CHECK CONSTRAINTS
    # =====================================================================
    
    # ApplicationSpecification constraints
    op.create_check_constraint(
        'CK_ApplicationSpecification_Category',
        'ApplicationSpecification',
        "Category IN ('authentication', 'validation', 'business_rules', 'ui', 'performance', 'security', 'integration', 'monitoring')"
    )
    
    op.create_check_constraint(
        'CK_ApplicationSpecification_DataType',
        'ApplicationSpecification',
        "DataType IN ('string', 'integer', 'boolean', 'json', 'decimal', 'datetime', 'url', 'email')"
    )
    
    op.create_check_constraint(
        'CK_ApplicationSpecification_SortOrder',
        'ApplicationSpecification',
        "SortOrder > 0"
    )
    
    # CountryApplicationSpecification constraints
    op.create_check_constraint(
        'CK_CountryApplicationSpecification_Category',
        'CountryApplicationSpecification',
        "Category IN ('authentication', 'validation', 'business_rules', 'ui', 'performance', 'security', 'integration', 'monitoring')"
    )
    
    op.create_check_constraint(
        'CK_CountryApplicationSpecification_DataType',
        'CountryApplicationSpecification',
        "DataType IN ('string', 'integer', 'boolean', 'json', 'decimal', 'datetime', 'url', 'email')"
    )
    
    # EnvironmentApplicationSpecification constraints
    op.create_check_constraint(
        'CK_EnvironmentApplicationSpecification_Environment',
        'EnvironmentApplicationSpecification',
        "EnvironmentName IN ('development', 'staging', 'production', 'testing')"
    )
    
    op.create_check_constraint(
        'CK_EnvironmentApplicationSpecification_Category',
        'EnvironmentApplicationSpecification',
        "Category IN ('authentication', 'validation', 'business_rules', 'ui', 'performance', 'security', 'integration', 'monitoring')"
    )
    
    op.create_check_constraint(
        'CK_EnvironmentApplicationSpecification_DataType',
        'EnvironmentApplicationSpecification',
        "DataType IN ('string', 'integer', 'boolean', 'json', 'decimal', 'datetime', 'url', 'email')"
    )
    
    # =====================================================================
    # INDEXES
    # =====================================================================
    
    # ApplicationSpecification indexes
    op.create_index('IX_ApplicationSpecification_Category', 'ApplicationSpecification', ['Category'])
    op.create_index('IX_ApplicationSpecification_Active', 'ApplicationSpecification', ['IsActive'])
    op.create_index('IX_ApplicationSpecification_System', 'ApplicationSpecification', ['IsSystemParameter'])
    
    # CountryApplicationSpecification indexes
    op.create_index('IX_CountryApplicationSpecification_Country', 'CountryApplicationSpecification', ['CountryID'])
    op.create_index('IX_CountryApplicationSpecification_Category', 'CountryApplicationSpecification', ['Category'])
    op.create_index('IX_CountryApplicationSpecification_Active', 'CountryApplicationSpecification', ['IsActive'])
    
    # EnvironmentApplicationSpecification indexes
    op.create_index('IX_EnvironmentApplicationSpecification_Environment', 'EnvironmentApplicationSpecification', ['EnvironmentName'])
    op.create_index('IX_EnvironmentApplicationSpecification_Country', 'EnvironmentApplicationSpecification', ['CountryID'])
    op.create_index('IX_EnvironmentApplicationSpecification_Category', 'EnvironmentApplicationSpecification', ['Category'])
    op.create_index('IX_EnvironmentApplicationSpecification_Active', 'EnvironmentApplicationSpecification', ['IsActive'])
    
    # =====================================================================
    # SEED DATA: Global Application Parameters
    # =====================================================================
    
    # Authentication parameters
    op.execute("""
        INSERT INTO [ApplicationSpecification] (Category, ParameterName, ParameterValue, DataType, Description, IsActive, SortOrder, IsSystemParameter, CreatedBy)
        VALUES
            ('authentication', 'password_min_length', '8', 'integer', 'Minimum password length', 1, 1, 1, 1),
            ('authentication', 'password_require_special_chars', 'true', 'boolean', 'Require special characters in password', 1, 2, 1, 1),
            ('authentication', 'jwt_access_token_expiry_minutes', '15', 'integer', 'JWT access token expiry in minutes', 1, 3, 1, 1),
            ('authentication', 'jwt_refresh_token_expiry_days', '7', 'integer', 'JWT refresh token expiry in days', 1, 4, 1, 1),
            ('authentication', 'max_failed_login_attempts', '5', 'integer', 'Max failed login attempts before lockout', 1, 5, 1, 1),
            ('authentication', 'account_lockout_minutes', '15', 'integer', 'Account lockout duration in minutes', 1, 6, 1, 1)
    """)
    
    # Validation parameters
    op.execute("""
        INSERT INTO [ApplicationSpecification] (Category, ParameterName, ParameterValue, DataType, Description, IsActive, SortOrder, IsSystemParameter, CreatedBy)
        VALUES
            ('validation', 'email_verification_expiry_hours', '24', 'integer', 'Email verification token expiry in hours', 1, 1, 1, 1),
            ('validation', 'password_reset_expiry_hours', '1', 'integer', 'Password reset token expiry in hours', 1, 2, 1, 1),
            ('validation', 'invitation_expiry_days', '7', 'integer', 'Team invitation expiry in days', 1, 3, 1, 1),
            ('validation', 'company_name_min_length', '2', 'integer', 'Minimum company name length', 1, 4, 1, 1),
            ('validation', 'company_name_max_length', '200', 'integer', 'Maximum company name length', 1, 5, 1, 1)
    """)
    
    # Business rules parameters
    op.execute("""
        INSERT INTO [ApplicationSpecification] (Category, ParameterName, ParameterValue, DataType, Description, IsActive, SortOrder, IsSystemParameter, CreatedBy)
        VALUES
            ('business_rules', 'default_test_threshold', '5', 'integer', 'Default preview tests required before publish', 1, 1, 1, 1),
            ('business_rules', 'free_tier_max_events', '10', 'integer', 'Maximum events for free tier', 1, 2, 1, 1),
            ('business_rules', 'free_tier_max_users', '5', 'integer', 'Maximum users for free tier', 1, 3, 1, 1),
            ('business_rules', 'abn_cache_ttl_days', '30', 'integer', 'ABN lookup cache TTL in days', 1, 4, 1, 1),
            ('business_rules', 'max_invitations_per_day', '50', 'integer', 'Maximum invitations per company per day', 1, 5, 1, 1)
    """)


def downgrade():
    """Drop Application Specification system tables"""
    
    # Drop indexes
    op.drop_index('IX_EnvironmentApplicationSpecification_Active', table_name='EnvironmentApplicationSpecification')
    op.drop_index('IX_EnvironmentApplicationSpecification_Category', table_name='EnvironmentApplicationSpecification')
    op.drop_index('IX_EnvironmentApplicationSpecification_Country', table_name='EnvironmentApplicationSpecification')
    op.drop_index('IX_EnvironmentApplicationSpecification_Environment', table_name='EnvironmentApplicationSpecification')
    op.drop_index('IX_CountryApplicationSpecification_Active', table_name='CountryApplicationSpecification')
    op.drop_index('IX_CountryApplicationSpecification_Category', table_name='CountryApplicationSpecification')
    op.drop_index('IX_CountryApplicationSpecification_Country', table_name='CountryApplicationSpecification')
    op.drop_index('IX_ApplicationSpecification_System', table_name='ApplicationSpecification')
    op.drop_index('IX_ApplicationSpecification_Active', table_name='ApplicationSpecification')
    op.drop_index('IX_ApplicationSpecification_Category', table_name='ApplicationSpecification')
    
    # Drop check constraints
    op.drop_constraint('CK_EnvironmentApplicationSpecification_DataType', 'EnvironmentApplicationSpecification', type_='check')
    op.drop_constraint('CK_EnvironmentApplicationSpecification_Category', 'EnvironmentApplicationSpecification', type_='check')
    op.drop_constraint('CK_EnvironmentApplicationSpecification_Environment', 'EnvironmentApplicationSpecification', type_='check')
    op.drop_constraint('CK_CountryApplicationSpecification_DataType', 'CountryApplicationSpecification', type_='check')
    op.drop_constraint('CK_CountryApplicationSpecification_Category', 'CountryApplicationSpecification', type_='check')
    op.drop_constraint('CK_ApplicationSpecification_SortOrder', 'ApplicationSpecification', type_='check')
    op.drop_constraint('CK_ApplicationSpecification_DataType', 'ApplicationSpecification', type_='check')
    op.drop_constraint('CK_ApplicationSpecification_Category', 'ApplicationSpecification', type_='check')
    
    # Drop foreign key constraints
    op.drop_constraint('FK_EnvironmentApplicationSpecification_DeletedBy', 'EnvironmentApplicationSpecification', type_='foreignkey')
    op.drop_constraint('FK_EnvironmentApplicationSpecification_UpdatedBy', 'EnvironmentApplicationSpecification', type_='foreignkey')
    op.drop_constraint('FK_EnvironmentApplicationSpecification_CreatedBy', 'EnvironmentApplicationSpecification', type_='foreignkey')
    op.drop_constraint('FK_CountryApplicationSpecification_DeletedBy', 'CountryApplicationSpecification', type_='foreignkey')
    op.drop_constraint('FK_CountryApplicationSpecification_UpdatedBy', 'CountryApplicationSpecification', type_='foreignkey')
    op.drop_constraint('FK_CountryApplicationSpecification_CreatedBy', 'CountryApplicationSpecification', type_='foreignkey')
    op.drop_constraint('FK_ApplicationSpecification_DeletedBy', 'ApplicationSpecification', type_='foreignkey')
    op.drop_constraint('FK_ApplicationSpecification_UpdatedBy', 'ApplicationSpecification', type_='foreignkey')
    op.drop_constraint('FK_ApplicationSpecification_CreatedBy', 'ApplicationSpecification', type_='foreignkey')
    op.drop_constraint('FK_EnvironmentApplicationSpecification_ApprovedBy', 'EnvironmentApplicationSpecification', type_='foreignkey')
    op.drop_constraint('FK_EnvironmentApplicationSpecification_Country', 'EnvironmentApplicationSpecification', type_='foreignkey')
    op.drop_constraint('FK_CountryApplicationSpecification_Country', 'CountryApplicationSpecification', type_='foreignkey')
    
    # Drop tables
    op.drop_table('EnvironmentApplicationSpecification')
    op.drop_table('CountryApplicationSpecification')
    op.drop_table('ApplicationSpecification')
