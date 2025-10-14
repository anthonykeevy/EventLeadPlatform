"""Create enhanced features tables (ABRSearchCache, CompanyRelationship, CompanySwitchRequest, CountryWebProperties, ValidationRule)

Revision ID: 004_enhanced_features_tables
Revises: 003_company_domain_tables
Create Date: 2025-10-13 12:03:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = '004_enhanced_features_tables'
down_revision = '003_company_domain_tables'
branch_labels = None
depends_on = None


def upgrade():
    """Create enhanced features tables"""
    
    # =====================================================================
    # TABLE: ABRSearchCache (Enhanced ABR Search Caching)
    # =====================================================================
    op.create_table('ABRSearchCache',
        sa.Column('SearchType', sa.NVARCHAR(20), nullable=False),
        sa.Column('SearchKey', sa.NVARCHAR(200), nullable=False),
        sa.Column('ResultIndex', sa.Integer(), nullable=False),
        sa.Column('SearchResult', sa.JSON(), nullable=False),
        sa.Column('CreatedAt', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('ExpiresAt', sa.DateTime(), nullable=False),
        sa.Column('HitCount', sa.Integer(), nullable=False, default=0),
        sa.Column('LastHitAt', sa.DateTime(), nullable=True),
        sa.Column('SearchMetadata', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('SearchType', 'SearchKey', 'ResultIndex')
    )
    
    # =====================================================================
    # TABLE: CompanyRelationship (Branch Company Scenarios)
    # =====================================================================
    op.create_table('CompanyRelationship',
        sa.Column('RelationshipID', sa.BigInteger(), nullable=False),
        sa.Column('ParentCompanyID', sa.BigInteger(), nullable=False),
        sa.Column('ChildCompanyID', sa.BigInteger(), nullable=False),
        sa.Column('RelationshipType', sa.NVARCHAR(50), nullable=False),
        sa.Column('Status', sa.NVARCHAR(20), nullable=False, default='active'),
        sa.Column('EstablishedBy', sa.BigInteger(), nullable=False),
        sa.Column('EstablishedAt', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('ApprovedBy', sa.BigInteger(), nullable=True),
        sa.Column('ApprovedAt', sa.DateTime(), nullable=True),
        sa.Column('Description', sa.NVARCHAR(500), nullable=True),
        sa.Column('IsActive', sa.Boolean(), nullable=False, default=True),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('RelationshipID'),
        sa.UniqueConstraint('ParentCompanyID', 'ChildCompanyID', name='UQ_CompanyRelationship_Parent_Child')
    )
    
    # =====================================================================
    # TABLE: CompanySwitchRequest (Company Switching Management)
    # =====================================================================
    op.create_table('CompanySwitchRequest',
        sa.Column('RequestID', sa.BigInteger(), nullable=False),
        sa.Column('UserID', sa.BigInteger(), nullable=False),
        sa.Column('FromCompanyID', sa.BigInteger(), nullable=False),
        sa.Column('ToCompanyID', sa.BigInteger(), nullable=False),
        sa.Column('RequestType', sa.NVARCHAR(50), nullable=False),
        sa.Column('Status', sa.NVARCHAR(20), nullable=False, default='pending'),
        sa.Column('RequestedBy', sa.BigInteger(), nullable=False),
        sa.Column('RequestedAt', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('ApprovedBy', sa.BigInteger(), nullable=True),
        sa.Column('ApprovedAt', sa.DateTime(), nullable=True),
        sa.Column('RejectedBy', sa.BigInteger(), nullable=True),
        sa.Column('RejectedAt', sa.DateTime(), nullable=True),
        sa.Column('RejectionReason', sa.NVARCHAR(500), nullable=True),
        sa.Column('ExpiresAt', sa.DateTime(), nullable=True),
        sa.Column('Notes', sa.NVARCHAR(500), nullable=True),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('RequestID')
    )
    
    # =====================================================================
    # TABLE: CountryWebProperties (International Foundation)
    # =====================================================================
    op.create_table('CountryWebProperties',
        sa.Column('CountryID', sa.BigInteger(), nullable=False),
        sa.Column('SortOrder', sa.Integer(), nullable=False, default=999),
        sa.Column('DisplayColor', sa.NVARCHAR(7), nullable=True),
        sa.Column('IsActive', sa.Boolean(), nullable=False, default=True),
        sa.Column('LaunchPriority', sa.Integer(), nullable=True),
        sa.Column('MarketingName', sa.NVARCHAR(100), nullable=True),
        sa.Column('SupportEmail', sa.NVARCHAR(100), nullable=True),
        sa.Column('LegalJurisdiction', sa.NVARCHAR(100), nullable=True),
        sa.Column('TimezoneOffset', sa.NVARCHAR(10), nullable=True),
        sa.Column('DateFormat', sa.NVARCHAR(20), nullable=True, default='DD/MM/YYYY'),
        sa.Column('CurrencySymbol', sa.NVARCHAR(5), nullable=True, default='$'),
        sa.Column('CurrencyPosition', sa.NVARCHAR(10), nullable=True, default='before'),
        sa.Column('IsDefaultCountry', sa.Boolean(), nullable=False, default=False),
        sa.Column('MaintenanceMode', sa.Boolean(), nullable=False, default=False),
        sa.Column('BetaAccess', sa.Boolean(), nullable=False, default=False),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('CountryID')
    )
    
    # =====================================================================
    # TABLE: ValidationRule (Country-Specific Validation Rules)
    # =====================================================================
    op.create_table('ValidationRule',
        sa.Column('RuleID', sa.BigInteger(), nullable=False),
        sa.Column('CountryID', sa.BigInteger(), nullable=False),
        sa.Column('RuleType', sa.NVARCHAR(50), nullable=False),
        sa.Column('RuleName', sa.NVARCHAR(100), nullable=False),
        sa.Column('ValidationPattern', sa.NVARCHAR(500), nullable=False),
        sa.Column('ErrorMessage', sa.NVARCHAR(200), nullable=False),
        sa.Column('IsActive', sa.Boolean(), nullable=False, default=True),
        sa.Column('SortOrder', sa.Integer(), nullable=False, default=999),
        sa.Column('MinLength', sa.Integer(), nullable=True),
        sa.Column('MaxLength', sa.Integer(), nullable=True),
        sa.Column('ExampleValue', sa.NVARCHAR(100), nullable=True),
        sa.Column('Description', sa.NVARCHAR(500), nullable=True),
        sa.Column('IsRequired', sa.Boolean(), nullable=False, default=True),
        sa.Column('FieldType', sa.NVARCHAR(50), nullable=True),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('RuleID')
    )
    
    # =====================================================================
    # TABLE: LookupTableWebProperties (Lookup Table UI Properties)
    # =====================================================================
    op.create_table('LookupTableWebProperties',
        sa.Column('TableName', sa.NVARCHAR(100), nullable=False),
        sa.Column('DisplayName', sa.NVARCHAR(100), nullable=False),
        sa.Column('SortOrder', sa.Integer(), nullable=False, default=999),
        sa.Column('DisplayColor', sa.NVARCHAR(7), nullable=True),
        sa.Column('IsActive', sa.Boolean(), nullable=False, default=True),
        sa.Column('IconClass', sa.NVARCHAR(50), nullable=True),
        sa.Column('Description', sa.NVARCHAR(500), nullable=True),
        sa.Column('Category', sa.NVARCHAR(50), nullable=True),
        sa.Column('IsSystemTable', sa.Boolean(), nullable=False, default=False),
        sa.Column('AllowCustomValues', sa.Boolean(), nullable=False, default=False),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('TableName')
    )
    
    # =====================================================================
    # TABLE: LookupValueWebProperties (Lookup Value UI Properties)
    # =====================================================================
    op.create_table('LookupValueWebProperties',
        sa.Column('TableName', sa.NVARCHAR(100), nullable=False),
        sa.Column('ValueCode', sa.NVARCHAR(50), nullable=False),
        sa.Column('SortOrder', sa.Integer(), nullable=False, default=999),
        sa.Column('DisplayColor', sa.NVARCHAR(7), nullable=True),
        sa.Column('IconClass', sa.NVARCHAR(50), nullable=True),
        sa.Column('TooltipText', sa.NVARCHAR(200), nullable=True),
        sa.Column('IsDefault', sa.Boolean(), nullable=False, default=False),
        sa.Column('IsActive', sa.Boolean(), nullable=False, default=True),
        sa.Column('IsSystemValue', sa.Boolean(), nullable=False, default=False),
        sa.Column('CustomDisplayName', sa.NVARCHAR(100), nullable=True),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('TableName', 'ValueCode')
    )
    
    # =====================================================================
    # FOREIGN KEY CONSTRAINTS
    # =====================================================================
    
    # CompanyRelationship foreign keys
    op.create_foreign_key('FK_CompanyRelationship_Parent', 'CompanyRelationship', 'Company', ['ParentCompanyID'], ['CompanyID'])
    op.create_foreign_key('FK_CompanyRelationship_Child', 'CompanyRelationship', 'Company', ['ChildCompanyID'], ['CompanyID'])
    op.create_foreign_key('FK_CompanyRelationship_EstablishedBy', 'CompanyRelationship', 'User', ['EstablishedBy'], ['UserID'])
    op.create_foreign_key('FK_CompanyRelationship_ApprovedBy', 'CompanyRelationship', 'User', ['ApprovedBy'], ['UserID'])
    
    # CompanySwitchRequest foreign keys
    op.create_foreign_key('FK_CompanySwitchRequest_User', 'CompanySwitchRequest', 'User', ['UserID'], ['UserID'])
    op.create_foreign_key('FK_CompanySwitchRequest_FromCompany', 'CompanySwitchRequest', 'Company', ['FromCompanyID'], ['CompanyID'])
    op.create_foreign_key('FK_CompanySwitchRequest_ToCompany', 'CompanySwitchRequest', 'Company', ['ToCompanyID'], ['CompanyID'])
    op.create_foreign_key('FK_CompanySwitchRequest_RequestedBy', 'CompanySwitchRequest', 'User', ['RequestedBy'], ['UserID'])
    op.create_foreign_key('FK_CompanySwitchRequest_ApprovedBy', 'CompanySwitchRequest', 'User', ['ApprovedBy'], ['UserID'])
    op.create_foreign_key('FK_CompanySwitchRequest_RejectedBy', 'CompanySwitchRequest', 'User', ['RejectedBy'], ['UserID'])
    
    # CountryWebProperties foreign keys
    op.create_foreign_key('FK_CountryWebProperties_Country', 'CountryWebProperties', 'Country', ['CountryID'], ['CountryID'])
    
    # ValidationRule foreign keys
    op.create_foreign_key('FK_ValidationRule_Country', 'ValidationRule', 'Country', ['CountryID'], ['CountryID'])
    
    # Audit trail foreign keys
    op.create_foreign_key('FK_CompanyRelationship_CreatedBy', 'CompanyRelationship', 'User', ['CreatedBy'], ['UserID'])
    op.create_foreign_key('FK_CompanyRelationship_UpdatedBy', 'CompanyRelationship', 'User', ['UpdatedBy'], ['UserID'])
    op.create_foreign_key('FK_CompanyRelationship_DeletedBy', 'CompanyRelationship', 'User', ['DeletedBy'], ['UserID'])
    
    op.create_foreign_key('FK_CompanySwitchRequest_CreatedBy', 'CompanySwitchRequest', 'User', ['CreatedBy'], ['UserID'])
    op.create_foreign_key('FK_CompanySwitchRequest_UpdatedBy', 'CompanySwitchRequest', 'User', ['UpdatedBy'], ['UserID'])
    op.create_foreign_key('FK_CompanySwitchRequest_DeletedBy', 'CompanySwitchRequest', 'User', ['DeletedBy'], ['UserID'])
    
    op.create_foreign_key('FK_CountryWebProperties_CreatedBy', 'CountryWebProperties', 'User', ['CreatedBy'], ['UserID'])
    op.create_foreign_key('FK_CountryWebProperties_UpdatedBy', 'CountryWebProperties', 'User', ['UpdatedBy'], ['UserID'])
    op.create_foreign_key('FK_CountryWebProperties_DeletedBy', 'CountryWebProperties', 'User', ['DeletedBy'], ['UserID'])
    
    op.create_foreign_key('FK_ValidationRule_CreatedBy', 'ValidationRule', 'User', ['CreatedBy'], ['UserID'])
    op.create_foreign_key('FK_ValidationRule_UpdatedBy', 'ValidationRule', 'User', ['UpdatedBy'], ['UserID'])
    op.create_foreign_key('FK_ValidationRule_DeletedBy', 'ValidationRule', 'User', ['DeletedBy'], ['UserID'])
    
    op.create_foreign_key('FK_LookupTableWebProperties_CreatedBy', 'LookupTableWebProperties', 'User', ['CreatedBy'], ['UserID'])
    op.create_foreign_key('FK_LookupTableWebProperties_UpdatedBy', 'LookupTableWebProperties', 'User', ['UpdatedBy'], ['UserID'])
    op.create_foreign_key('FK_LookupTableWebProperties_DeletedBy', 'LookupTableWebProperties', 'User', ['DeletedBy'], ['UserID'])
    
    op.create_foreign_key('FK_LookupValueWebProperties_CreatedBy', 'LookupValueWebProperties', 'User', ['CreatedBy'], ['UserID'])
    op.create_foreign_key('FK_LookupValueWebProperties_UpdatedBy', 'LookupValueWebProperties', 'User', ['UpdatedBy'], ['UserID'])
    op.create_foreign_key('FK_LookupValueWebProperties_DeletedBy', 'LookupValueWebProperties', 'User', ['DeletedBy'], ['UserID'])
    
    # =====================================================================
    # CHECK CONSTRAINTS
    # =====================================================================
    
    # ABRSearchCache constraints
    op.create_check_constraint(
        'CK_ABRSearchCache_SearchType',
        'ABRSearchCache',
        "SearchType IN ('ABN', 'ACN', 'Name')"
    )
    
    op.create_check_constraint(
        'CK_ABRSearchCache_ResultIndex',
        'ABRSearchCache',
        "ResultIndex >= 0"
    )
    
    # CompanyRelationship constraints
    op.create_check_constraint(
        'CK_CompanyRelationship_Type',
        'CompanyRelationship',
        "RelationshipType IN ('branch', 'subsidiary', 'partner', 'affiliate', 'division')"
    )
    
    op.create_check_constraint(
        'CK_CompanyRelationship_Status',
        'CompanyRelationship',
        "Status IN ('active', 'suspended', 'terminated', 'pending')"
    )
    
    op.create_check_constraint(
        'CK_CompanyRelationship_NotSelf',
        'CompanyRelationship',
        "ParentCompanyID != ChildCompanyID"
    )
    
    # CompanySwitchRequest constraints
    op.create_check_constraint(
        'CK_CompanySwitchRequest_Type',
        'CompanySwitchRequest',
        "RequestType IN ('invitation_accepted', 'company_switch', 'relationship_join', 'access_request')"
    )
    
    op.create_check_constraint(
        'CK_CompanySwitchRequest_Status',
        'CompanySwitchRequest',
        "Status IN ('pending', 'approved', 'rejected', 'expired', 'cancelled')"
    )
    
    # ValidationRule constraints
    op.create_check_constraint(
        'CK_ValidationRule_Type',
        'ValidationRule',
        "RuleType IN ('phone', 'postal_code', 'tax_id', 'address', 'email', 'url', 'date', 'number')"
    )
    
    op.create_check_constraint(
        'CK_ValidationRule_SortOrder',
        'ValidationRule',
        "SortOrder > 0"
    )
    
    # =====================================================================
    # INDEXES
    # =====================================================================
    
    # ABRSearchCache indexes
    op.create_index('IX_ABRSearchCache_ExpiresAt', 'ABRSearchCache', ['ExpiresAt'])
    op.create_index('IX_ABRSearchCache_HitCount', 'ABRSearchCache', ['HitCount'])
    
    # CompanyRelationship indexes
    op.create_index('IX_CompanyRelationship_Parent', 'CompanyRelationship', ['ParentCompanyID'])
    op.create_index('IX_CompanyRelationship_Child', 'CompanyRelationship', ['ChildCompanyID'])
    op.create_index('IX_CompanyRelationship_Type', 'CompanyRelationship', ['RelationshipType'])
    op.create_index('IX_CompanyRelationship_Status', 'CompanyRelationship', ['Status'])
    
    # CompanySwitchRequest indexes
    op.create_index('IX_CompanySwitchRequest_User', 'CompanySwitchRequest', ['UserID'])
    op.create_index('IX_CompanySwitchRequest_Status', 'CompanySwitchRequest', ['Status'])
    op.create_index('IX_CompanySwitchRequest_ExpiresAt', 'CompanySwitchRequest', ['ExpiresAt'])
    
    # ValidationRule indexes
    op.create_index('IX_ValidationRule_Country', 'ValidationRule', ['CountryID'])
    op.create_index('IX_ValidationRule_Type', 'ValidationRule', ['RuleType'])
    op.create_index('IX_ValidationRule_Active', 'ValidationRule', ['IsActive'])
    
    # LookupValueWebProperties indexes
    op.create_index('IX_LookupValueWebProperties_Table', 'LookupValueWebProperties', ['TableName'])
    op.create_index('IX_LookupValueWebProperties_Active', 'LookupValueWebProperties', ['IsActive'])


def downgrade():
    """Drop enhanced features tables"""
    
    # Drop indexes
    op.drop_index('IX_LookupValueWebProperties_Active', table_name='LookupValueWebProperties')
    op.drop_index('IX_LookupValueWebProperties_Table', table_name='LookupValueWebProperties')
    op.drop_index('IX_ValidationRule_Active', table_name='ValidationRule')
    op.drop_index('IX_ValidationRule_Type', table_name='ValidationRule')
    op.drop_index('IX_ValidationRule_Country', table_name='ValidationRule')
    op.drop_index('IX_CompanySwitchRequest_ExpiresAt', table_name='CompanySwitchRequest')
    op.drop_index('IX_CompanySwitchRequest_Status', table_name='CompanySwitchRequest')
    op.drop_index('IX_CompanySwitchRequest_User', table_name='CompanySwitchRequest')
    op.drop_index('IX_CompanyRelationship_Status', table_name='CompanyRelationship')
    op.drop_index('IX_CompanyRelationship_Type', table_name='CompanyRelationship')
    op.drop_index('IX_CompanyRelationship_Child', table_name='CompanyRelationship')
    op.drop_index('IX_CompanyRelationship_Parent', table_name='CompanyRelationship')
    op.drop_index('IX_ABRSearchCache_HitCount', table_name='ABRSearchCache')
    op.drop_index('IX_ABRSearchCache_ExpiresAt', table_name='ABRSearchCache')
    
    # Drop check constraints
    op.drop_constraint('CK_ValidationRule_SortOrder', 'ValidationRule', type_='check')
    op.drop_constraint('CK_ValidationRule_Type', 'ValidationRule', type_='check')
    op.drop_constraint('CK_CompanySwitchRequest_Status', 'CompanySwitchRequest', type_='check')
    op.drop_constraint('CK_CompanySwitchRequest_Type', 'CompanySwitchRequest', type_='check')
    op.drop_constraint('CK_CompanyRelationship_NotSelf', 'CompanyRelationship', type_='check')
    op.drop_constraint('CK_CompanyRelationship_Status', 'CompanyRelationship', type_='check')
    op.drop_constraint('CK_CompanyRelationship_Type', 'CompanyRelationship', type_='check')
    op.drop_constraint('CK_ABRSearchCache_ResultIndex', 'ABRSearchCache', type_='check')
    op.drop_constraint('CK_ABRSearchCache_SearchType', 'ABRSearchCache', type_='check')
    
    # Drop foreign key constraints
    op.drop_constraint('FK_LookupValueWebProperties_DeletedBy', 'LookupValueWebProperties', type_='foreignkey')
    op.drop_constraint('FK_LookupValueWebProperties_UpdatedBy', 'LookupValueWebProperties', type_='foreignkey')
    op.drop_constraint('FK_LookupValueWebProperties_CreatedBy', 'LookupValueWebProperties', type_='foreignkey')
    op.drop_constraint('FK_LookupTableWebProperties_DeletedBy', 'LookupTableWebProperties', type_='foreignkey')
    op.drop_constraint('FK_LookupTableWebProperties_UpdatedBy', 'LookupTableWebProperties', type_='foreignkey')
    op.drop_constraint('FK_LookupTableWebProperties_CreatedBy', 'LookupTableWebProperties', type_='foreignkey')
    op.drop_constraint('FK_ValidationRule_DeletedBy', 'ValidationRule', type_='foreignkey')
    op.drop_constraint('FK_ValidationRule_UpdatedBy', 'ValidationRule', type_='foreignkey')
    op.drop_constraint('FK_ValidationRule_CreatedBy', 'ValidationRule', type_='foreignkey')
    op.drop_constraint('FK_CountryWebProperties_DeletedBy', 'CountryWebProperties', type_='foreignkey')
    op.drop_constraint('FK_CountryWebProperties_UpdatedBy', 'CountryWebProperties', type_='foreignkey')
    op.drop_constraint('FK_CountryWebProperties_CreatedBy', 'CountryWebProperties', type_='foreignkey')
    op.drop_constraint('FK_CompanySwitchRequest_DeletedBy', 'CompanySwitchRequest', type_='foreignkey')
    op.drop_constraint('FK_CompanySwitchRequest_UpdatedBy', 'CompanySwitchRequest', type_='foreignkey')
    op.drop_constraint('FK_CompanySwitchRequest_CreatedBy', 'CompanySwitchRequest', type_='foreignkey')
    op.drop_constraint('FK_CompanyRelationship_DeletedBy', 'CompanyRelationship', type_='foreignkey')
    op.drop_constraint('FK_CompanyRelationship_UpdatedBy', 'CompanyRelationship', type_='foreignkey')
    op.drop_constraint('FK_CompanyRelationship_CreatedBy', 'CompanyRelationship', type_='foreignkey')
    op.drop_constraint('FK_ValidationRule_Country', 'ValidationRule', type_='foreignkey')
    op.drop_constraint('FK_CountryWebProperties_Country', 'CountryWebProperties', type_='foreignkey')
    op.drop_constraint('FK_CompanySwitchRequest_RejectedBy', 'CompanySwitchRequest', type_='foreignkey')
    op.drop_constraint('FK_CompanySwitchRequest_ApprovedBy', 'CompanySwitchRequest', type_='foreignkey')
    op.drop_constraint('FK_CompanySwitchRequest_RequestedBy', 'CompanySwitchRequest', type_='foreignkey')
    op.drop_constraint('FK_CompanySwitchRequest_ToCompany', 'CompanySwitchRequest', type_='foreignkey')
    op.drop_constraint('FK_CompanySwitchRequest_FromCompany', 'CompanySwitchRequest', type_='foreignkey')
    op.drop_constraint('FK_CompanySwitchRequest_User', 'CompanySwitchRequest', type_='foreignkey')
    op.drop_constraint('FK_CompanyRelationship_ApprovedBy', 'CompanyRelationship', type_='foreignkey')
    op.drop_constraint('FK_CompanyRelationship_EstablishedBy', 'CompanyRelationship', type_='foreignkey')
    op.drop_constraint('FK_CompanyRelationship_Child', 'CompanyRelationship', type_='foreignkey')
    op.drop_constraint('FK_CompanyRelationship_Parent', 'CompanyRelationship', type_='foreignkey')
    
    # Drop tables
    op.drop_table('LookupValueWebProperties')
    op.drop_table('LookupTableWebProperties')
    op.drop_table('ValidationRule')
    op.drop_table('CountryWebProperties')
    op.drop_table('CompanySwitchRequest')
    op.drop_table('CompanyRelationship')
    op.drop_table('ABRSearchCache')
