"""Create Company domain tables (Company, CompanyCustomerDetails, CompanyBillingDetails, CompanyOrganizerDetails)

Revision ID: 003_company_domain_tables
Revises: 002_user_domain_tables
Create Date: 2025-10-13 12:02:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = '003_company_domain_tables'
down_revision = '002_user_domain_tables'
branch_labels = None
depends_on = None


def upgrade():
    """Create Company domain tables"""
    
    # =====================================================================
    # CORE TABLE: Company (Universal Company Data)
    # =====================================================================
    op.create_table('Company',
        sa.Column('CompanyID', sa.BigInteger(), nullable=False),
        sa.Column('DisplayName', sa.NVARCHAR(200), nullable=False),
        sa.Column('LegalEntityName', sa.NVARCHAR(200), nullable=False),
        sa.Column('BusinessNames', sa.NVARCHAR(), nullable=True),
        sa.Column('CustomDisplayName', sa.NVARCHAR(200), nullable=True),
        sa.Column('DisplayNameSource', sa.NVARCHAR(20), nullable=False, default='User'),
        sa.Column('Website', sa.NVARCHAR(500), nullable=True),
        sa.Column('Phone', sa.NVARCHAR(20), nullable=True),
        sa.Column('Industry', sa.NVARCHAR(100), nullable=True),
        sa.Column('ParentCompanyID', sa.BigInteger(), nullable=True),
        sa.Column('CompanyType', sa.NVARCHAR(50), nullable=True),
        sa.Column('CompanySize', sa.NVARCHAR(20), nullable=True),
        sa.Column('FoundedYear', sa.Integer(), nullable=True),
        sa.Column('Description', sa.NVARCHAR(1000), nullable=True),
        sa.Column('IsActive', sa.Boolean(), nullable=False, default=True),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('CompanyID')
    )
    
    # =====================================================================
    # EXTENSION TABLE: CompanyCustomerDetails (Multi-Tenant SaaS Context)
    # =====================================================================
    op.create_table('CompanyCustomerDetails',
        sa.Column('CompanyID', sa.BigInteger(), nullable=False),
        sa.Column('SubscriptionPlan', sa.NVARCHAR(50), nullable=False, default='free'),
        sa.Column('SubscriptionStatus', sa.NVARCHAR(20), nullable=False, default='active'),
        sa.Column('BillingCompanyID', sa.BigInteger(), nullable=True),
        sa.Column('TestThreshold', sa.Integer(), nullable=False, default=5),
        sa.Column('AnalyticsOptOut', sa.Boolean(), nullable=False, default=False),
        sa.Column('MaxUsers', sa.Integer(), nullable=True),
        sa.Column('MaxEvents', sa.Integer(), nullable=True),
        sa.Column('MaxSubmissions', sa.Integer(), nullable=True),
        sa.Column('MaxStorageMB', sa.Integer(), nullable=True),
        sa.Column('SubscriptionStartDate', sa.DateTime(), nullable=True),
        sa.Column('SubscriptionEndDate', sa.DateTime(), nullable=True),
        sa.Column('TrialEndDate', sa.DateTime(), nullable=True),
        sa.Column('IsTrialActive', sa.Boolean(), nullable=False, default=False),
        sa.Column('AutoRenew', sa.Boolean(), nullable=False, default=True),
        sa.Column('PaymentMethodID', sa.NVARCHAR(100), nullable=True),
        sa.Column('LastBillingDate', sa.DateTime(), nullable=True),
        sa.Column('NextBillingDate', sa.DateTime(), nullable=True),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('CompanyID')
    )
    
    # =====================================================================
    # EXTENSION TABLE: CompanyBillingDetails (Australian Tax Compliance)
    # =====================================================================
    op.create_table('CompanyBillingDetails',
        sa.Column('CompanyID', sa.BigInteger(), nullable=False),
        sa.Column('ABN', sa.NVARCHAR(11), nullable=False),
        sa.Column('GSTRegistered', sa.Boolean(), nullable=False),
        sa.Column('TaxInvoiceName', sa.NVARCHAR(200), nullable=False),
        sa.Column('BillingEmail', sa.NVARCHAR(100), nullable=False),
        sa.Column('BillingAddress', sa.NVARCHAR(500), nullable=False),
        sa.Column('BillingCity', sa.NVARCHAR(100), nullable=True),
        sa.Column('BillingState', sa.NVARCHAR(50), nullable=True),
        sa.Column('BillingPostalCode', sa.NVARCHAR(20), nullable=True),
        sa.Column('BillingCountry', sa.NVARCHAR(2), nullable=True, default='AU'),
        sa.Column('IsLocked', sa.Boolean(), nullable=False, default=False),
        sa.Column('FirstInvoiceDate', sa.DateTime(), nullable=True),
        sa.Column('ABNLastVerified', sa.DateTime(), nullable=True),
        sa.Column('ABNVerificationStatus', sa.NVARCHAR(20), nullable=True),
        sa.Column('ABNVerificationSource', sa.NVARCHAR(50), nullable=True),
        sa.Column('TaxExemptionReason', sa.NVARCHAR(200), nullable=True),
        sa.Column('TaxExemptionCode', sa.NVARCHAR(20), nullable=True),
        sa.Column('PaymentTerms', sa.Integer(), nullable=True, default=30),
        sa.Column('CreditLimit', sa.DECIMAL(10, 2), nullable=True),
        sa.Column('Currency', sa.NVARCHAR(3), nullable=False, default='AUD'),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('CompanyID'),
        sa.UniqueConstraint('ABN', name='UQ_CompanyBillingDetails_ABN')
    )
    
    # =====================================================================
    # EXTENSION TABLE: CompanyOrganizerDetails (Event Organizer B2B Context)
    # =====================================================================
    op.create_table('CompanyOrganizerDetails',
        sa.Column('CompanyID', sa.BigInteger(), nullable=False),
        sa.Column('PublicProfileName', sa.NVARCHAR(200), nullable=True),
        sa.Column('Description', sa.NVARCHAR(1000), nullable=True),
        sa.Column('LogoUrl', sa.NVARCHAR(500), nullable=True),
        sa.Column('BrandColorPrimary', sa.NVARCHAR(7), nullable=True),
        sa.Column('BrandColorSecondary', sa.NVARCHAR(7), nullable=True),
        sa.Column('ContactEmail', sa.NVARCHAR(100), nullable=True),
        sa.Column('ContactPhone', sa.NVARCHAR(20), nullable=True),
        sa.Column('OrganizerSource', sa.NVARCHAR(50), nullable=True),
        sa.Column('IsPublic', sa.Boolean(), nullable=False, default=True),
        sa.Column('IsVerified', sa.Boolean(), nullable=False, default=False),
        sa.Column('VerificationDate', sa.DateTime(), nullable=True),
        sa.Column('VerificationMethod', sa.NVARCHAR(50), nullable=True),
        sa.Column('SocialMediaLinks', sa.NVARCHAR(), nullable=True),
        sa.Column('EventCategories', sa.NVARCHAR(), nullable=True),
        sa.Column('Specializations', sa.NVARCHAR(500), nullable=True),
        sa.Column('YearsInBusiness', sa.Integer(), nullable=True),
        sa.Column('TotalEventsHosted', sa.Integer(), nullable=False, default=0),
        sa.Column('AverageEventSize', sa.Integer(), nullable=True),
        sa.Column('LargestEventSize', sa.Integer(), nullable=True),
        sa.Column('Rating', sa.DECIMAL(3, 2), nullable=True),
        sa.Column('RatingCount', sa.Integer(), nullable=False, default=0),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('CompanyID')
    )
    
    # =====================================================================
    # FOREIGN KEY CONSTRAINTS
    # =====================================================================
    
    # Company self-reference (Parent-Subsidiary)
    op.create_foreign_key('FK_Company_Parent', 'Company', 'Company', ['ParentCompanyID'], ['CompanyID'])
    
    # Company audit trail
    op.create_foreign_key('FK_Company_CreatedBy', 'Company', 'User', ['CreatedBy'], ['UserID'])
    op.create_foreign_key('FK_Company_UpdatedBy', 'Company', 'User', ['UpdatedBy'], ['UserID'])
    op.create_foreign_key('FK_Company_DeletedBy', 'Company', 'User', ['DeletedBy'], ['UserID'])
    
    # Extension table foreign keys
    op.create_foreign_key('FK_CompanyCustomerDetails_Company', 'CompanyCustomerDetails', 'Company', ['CompanyID'], ['CompanyID'])
    op.create_foreign_key('FK_CompanyCustomerDetails_Billing', 'CompanyCustomerDetails', 'Company', ['BillingCompanyID'], ['CompanyID'])
    op.create_foreign_key('FK_CompanyBillingDetails_Company', 'CompanyBillingDetails', 'Company', ['CompanyID'], ['CompanyID'])
    op.create_foreign_key('FK_CompanyOrganizerDetails_Company', 'CompanyOrganizerDetails', 'Company', ['CompanyID'], ['CompanyID'])
    
    # Extension table audit trails
    op.create_foreign_key('FK_CompanyCustomerDetails_CreatedBy', 'CompanyCustomerDetails', 'User', ['CreatedBy'], ['UserID'])
    op.create_foreign_key('FK_CompanyCustomerDetails_UpdatedBy', 'CompanyCustomerDetails', 'User', ['UpdatedBy'], ['UserID'])
    op.create_foreign_key('FK_CompanyCustomerDetails_DeletedBy', 'CompanyCustomerDetails', 'User', ['DeletedBy'], ['UserID'])
    
    op.create_foreign_key('FK_CompanyBillingDetails_CreatedBy', 'CompanyBillingDetails', 'User', ['CreatedBy'], ['UserID'])
    op.create_foreign_key('FK_CompanyBillingDetails_UpdatedBy', 'CompanyBillingDetails', 'User', ['UpdatedBy'], ['UserID'])
    op.create_foreign_key('FK_CompanyBillingDetails_DeletedBy', 'CompanyBillingDetails', 'User', ['DeletedBy'], ['UserID'])
    
    op.create_foreign_key('FK_CompanyOrganizerDetails_CreatedBy', 'CompanyOrganizerDetails', 'User', ['CreatedBy'], ['UserID'])
    op.create_foreign_key('FK_CompanyOrganizerDetails_UpdatedBy', 'CompanyOrganizerDetails', 'User', ['UpdatedBy'], ['UserID'])
    op.create_foreign_key('FK_CompanyOrganizerDetails_DeletedBy', 'CompanyOrganizerDetails', 'User', ['DeletedBy'], ['UserID'])
    
    # =====================================================================
    # CHECK CONSTRAINTS
    # =====================================================================
    
    # Company constraints
    op.create_check_constraint(
        'CK_Company_DisplayNameSource',
        'Company',
        "DisplayNameSource IN ('Legal', 'Business', 'Custom', 'User')"
    )
    
    # CompanyBillingDetails constraints
    op.create_check_constraint(
        'CK_CompanyBillingDetails_ABN',
        'CompanyBillingDetails',
        "LEN(ABN) = 11 AND ABN LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'"
    )
    
    op.create_check_constraint(
        'CK_CompanyBillingDetails_PaymentTerms',
        'CompanyBillingDetails',
        "PaymentTerms IS NULL OR PaymentTerms > 0"
    )
    
    # CompanyOrganizerDetails constraints
    op.create_check_constraint(
        'CK_CompanyOrganizerDetails_Rating',
        'CompanyOrganizerDetails',
        "Rating IS NULL OR (Rating >= 0.0 AND Rating <= 5.0)"
    )
    
    op.create_check_constraint(
        'CK_CompanyOrganizerDetails_RatingCount',
        'CompanyOrganizerDetails',
        "RatingCount >= 0"
    )
    
    # =====================================================================
    # INDEXES
    # =====================================================================
    
    # Company indexes
    op.create_index('IX_Company_DisplayName', 'Company', ['DisplayName'])
    op.create_index('IX_Company_LegalEntityName', 'Company', ['LegalEntityName'])
    op.create_index('IX_Company_ParentCompanyID', 'Company', ['ParentCompanyID'])
    op.create_index('IX_Company_IsActive', 'Company', ['IsActive'])
    
    # CompanyCustomerDetails indexes
    op.create_index('IX_CompanyCustomerDetails_SubscriptionPlan', 'CompanyCustomerDetails', ['SubscriptionPlan'])
    op.create_index('IX_CompanyCustomerDetails_SubscriptionStatus', 'CompanyCustomerDetails', ['SubscriptionStatus'])
    op.create_index('IX_CompanyCustomerDetails_TrialEndDate', 'CompanyCustomerDetails', ['TrialEndDate'])
    
    # CompanyBillingDetails indexes
    op.create_index('IX_CompanyBillingDetails_ABN', 'CompanyBillingDetails', ['ABN'])
    op.create_index('IX_CompanyBillingDetails_GSTRegistered', 'CompanyBillingDetails', ['GSTRegistered'])
    op.create_index('IX_CompanyBillingDetails_IsLocked', 'CompanyBillingDetails', ['IsLocked'])
    
    # CompanyOrganizerDetails indexes
    op.create_index('IX_CompanyOrganizerDetails_IsPublic', 'CompanyOrganizerDetails', ['IsPublic'])
    op.create_index('IX_CompanyOrganizerDetails_IsVerified', 'CompanyOrganizerDetails', ['IsVerified'])
    op.create_index('IX_CompanyOrganizerDetails_Rating', 'CompanyOrganizerDetails', ['Rating'])


def downgrade():
    """Drop Company domain tables"""
    
    # Drop indexes
    op.drop_index('IX_CompanyOrganizerDetails_Rating', table_name='CompanyOrganizerDetails')
    op.drop_index('IX_CompanyOrganizerDetails_IsVerified', table_name='CompanyOrganizerDetails')
    op.drop_index('IX_CompanyOrganizerDetails_IsPublic', table_name='CompanyOrganizerDetails')
    op.drop_index('IX_CompanyBillingDetails_IsLocked', table_name='CompanyBillingDetails')
    op.drop_index('IX_CompanyBillingDetails_GSTRegistered', table_name='CompanyBillingDetails')
    op.drop_index('IX_CompanyBillingDetails_ABN', table_name='CompanyBillingDetails')
    op.drop_index('IX_CompanyCustomerDetails_TrialEndDate', table_name='CompanyCustomerDetails')
    op.drop_index('IX_CompanyCustomerDetails_SubscriptionStatus', table_name='CompanyCustomerDetails')
    op.drop_index('IX_CompanyCustomerDetails_SubscriptionPlan', table_name='CompanyCustomerDetails')
    op.drop_index('IX_Company_IsActive', table_name='Company')
    op.drop_index('IX_Company_ParentCompanyID', table_name='Company')
    op.drop_index('IX_Company_LegalEntityName', table_name='Company')
    op.drop_index('IX_Company_DisplayName', table_name='Company')
    
    # Drop check constraints
    op.drop_constraint('CK_CompanyOrganizerDetails_RatingCount', 'CompanyOrganizerDetails', type_='check')
    op.drop_constraint('CK_CompanyOrganizerDetails_Rating', 'CompanyOrganizerDetails', type_='check')
    op.drop_constraint('CK_CompanyBillingDetails_PaymentTerms', 'CompanyBillingDetails', type_='check')
    op.drop_constraint('CK_CompanyBillingDetails_ABN', 'CompanyBillingDetails', type_='check')
    op.drop_constraint('CK_Company_DisplayNameSource', 'Company', type_='check')
    
    # Drop foreign key constraints
    op.drop_constraint('FK_CompanyOrganizerDetails_DeletedBy', 'CompanyOrganizerDetails', type_='foreignkey')
    op.drop_constraint('FK_CompanyOrganizerDetails_UpdatedBy', 'CompanyOrganizerDetails', type_='foreignkey')
    op.drop_constraint('FK_CompanyOrganizerDetails_CreatedBy', 'CompanyOrganizerDetails', type_='foreignkey')
    op.drop_constraint('FK_CompanyBillingDetails_DeletedBy', 'CompanyBillingDetails', type_='foreignkey')
    op.drop_constraint('FK_CompanyBillingDetails_UpdatedBy', 'CompanyBillingDetails', type_='foreignkey')
    op.drop_constraint('FK_CompanyBillingDetails_CreatedBy', 'CompanyBillingDetails', type_='foreignkey')
    op.drop_constraint('FK_CompanyCustomerDetails_DeletedBy', 'CompanyCustomerDetails', type_='foreignkey')
    op.drop_constraint('FK_CompanyCustomerDetails_UpdatedBy', 'CompanyCustomerDetails', type_='foreignkey')
    op.drop_constraint('FK_CompanyCustomerDetails_CreatedBy', 'CompanyCustomerDetails', type_='foreignkey')
    op.drop_constraint('FK_CompanyOrganizerDetails_Company', 'CompanyOrganizerDetails', type_='foreignkey')
    op.drop_constraint('FK_CompanyBillingDetails_Company', 'CompanyBillingDetails', type_='foreignkey')
    op.drop_constraint('FK_CompanyCustomerDetails_Billing', 'CompanyCustomerDetails', type_='foreignkey')
    op.drop_constraint('FK_CompanyCustomerDetails_Company', 'CompanyCustomerDetails', type_='foreignkey')
    op.drop_constraint('FK_Company_DeletedBy', 'Company', type_='foreignkey')
    op.drop_constraint('FK_Company_UpdatedBy', 'Company', type_='foreignkey')
    op.drop_constraint('FK_Company_CreatedBy', 'Company', type_='foreignkey')
    op.drop_constraint('FK_Company_Parent', 'Company', type_='foreignkey')
    
    # Drop tables
    op.drop_table('CompanyOrganizerDetails')
    op.drop_table('CompanyBillingDetails')
    op.drop_table('CompanyCustomerDetails')
    op.drop_table('Company')
