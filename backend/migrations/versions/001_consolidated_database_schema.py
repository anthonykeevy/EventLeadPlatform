"""Consolidated database schema - Complete EventLead Platform database

Revision ID: 001_consolidated_database_schema
Revises: 
Create Date: 2025-10-14 20:11:30.944631

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = '001_consolidated_database_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create complete EventLead Platform database schema"""
    
    # =====================================================================
    # STEP 1: FOUNDATION TABLES (No dependencies)
    # =====================================================================
    
    # Country table (ISO 3166-1 Reference Data)
    op.create_table('Country',
        sa.Column('CountryID', sa.BigInteger(), nullable=False),
        sa.Column('CountryCode', sa.NVARCHAR(2), nullable=False),
        sa.Column('CountryName', sa.NVARCHAR(100), nullable=False),
        sa.Column('CountryNameLocal', sa.NVARCHAR(100), nullable=True),
        sa.Column('Region', sa.NVARCHAR(50), nullable=True),
        sa.Column('Continent', sa.NVARCHAR(20), nullable=True),
        sa.Column('CurrencyCode', sa.NVARCHAR(3), nullable=False),
        sa.Column('CurrencyName', sa.NVARCHAR(50), nullable=False),
        sa.Column('CurrencySymbol', sa.NVARCHAR(5), nullable=True),
        sa.Column('TaxIDType', sa.NVARCHAR(20), nullable=True),
        sa.Column('TaxIDLabel', sa.NVARCHAR(50), nullable=True),
        sa.Column('TaxIDFormat', sa.NVARCHAR(100), nullable=True),
        sa.Column('TaxIDValidationAPI', sa.NVARCHAR(200), nullable=True),
        sa.Column('ConsumptionTaxName', sa.NVARCHAR(50), nullable=True),
        sa.Column('ConsumptionTaxRate', sa.DECIMAL(5, 2), nullable=True),
        sa.Column('ConsumptionTaxVariable', sa.Boolean(), nullable=False, default=False),
        sa.Column('AddressFormat', sa.NVARCHAR(500), nullable=True),
        sa.Column('RequiresStateProvince', sa.Boolean(), nullable=False, default=False),
        sa.Column('PostalCodeLabel', sa.NVARCHAR(50), nullable=True),
        sa.Column('PostalCodeFormat', sa.NVARCHAR(100), nullable=True),
        sa.Column('PhoneCountryCode', sa.NVARCHAR(5), nullable=True),
        sa.Column('PhoneLandlineRegex', sa.NVARCHAR(500), nullable=True),
        sa.Column('PhoneMobileRegex', sa.NVARCHAR(500), nullable=True),
        sa.Column('PhoneFreeCallRegex', sa.NVARCHAR(500), nullable=True),
        sa.Column('PhoneSpecialRegex', sa.NVARCHAR(500), nullable=True),
        sa.Column('PhoneFormatExample', sa.NVARCHAR(200), nullable=True),
        sa.Column('IsSupported', sa.Boolean(), nullable=False, default=False),
        sa.Column('LaunchDate', sa.DateTime(), nullable=True),
        sa.Column('SupportPriority', sa.Integer(), nullable=True),
        sa.Column('DefaultLanguageCode', sa.NVARCHAR(2), nullable=True),
        sa.Column('Locale', sa.NVARCHAR(10), nullable=True),
        sa.Column('DateFormat', sa.NVARCHAR(20), nullable=True),
        sa.Column('TimeFormat', sa.NVARCHAR(20), nullable=True),
        sa.Column('Notes', sa.NVARCHAR(), nullable=True),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('CountryID'),
        sa.UniqueConstraint('CountryCode', name='UQ_Country_Code')
    )
    
    # Language table (ISO 639-1 Reference Data)
    op.create_table('Language',
        sa.Column('LanguageID', sa.BigInteger(), nullable=False),
        sa.Column('LanguageCode', sa.NVARCHAR(2), nullable=False),
        sa.Column('LanguageName', sa.NVARCHAR(100), nullable=False),
        sa.Column('LanguageNameLocal', sa.NVARCHAR(100), nullable=True),
        sa.Column('LanguageFamily', sa.NVARCHAR(50), nullable=True),
        sa.Column('Direction', sa.NVARCHAR(3), nullable=False, default='LTR'),
        sa.Column('IsSupported', sa.Boolean(), nullable=False, default=False),
        sa.Column('TranslationCompleteness', sa.Integer(), nullable=True),
        sa.Column('LaunchDate', sa.DateTime(), nullable=True),
        sa.Column('SupportPriority', sa.Integer(), nullable=True),
        sa.Column('PluralRules', sa.NVARCHAR(500), nullable=True),
        sa.Column('DateFormatExample', sa.NVARCHAR(50), nullable=True),
        sa.Column('NumberFormat', sa.NVARCHAR(50), nullable=True),
        sa.Column('Notes', sa.NVARCHAR(), nullable=True),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('LanguageID'),
        sa.UniqueConstraint('LanguageCode', name='UQ_Language_Code')
    )
    
    # =====================================================================
    # STEP 2: LOOKUP TABLES (No dependencies)
    # =====================================================================
    
    # UserStatus lookup table
    op.create_table('UserStatus',
        sa.Column('StatusCode', sa.NVARCHAR(20), nullable=False),
        sa.Column('DisplayName', sa.NVARCHAR(50), nullable=False),
        sa.Column('Description', sa.NVARCHAR(500), nullable=False),
        sa.Column('AllowLogin', sa.Boolean(), nullable=False),
        sa.Column('IsSystemStatus', sa.Boolean(), nullable=False, default=True),
        sa.Column('SortOrder', sa.Integer(), nullable=False),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=True),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('StatusCode')
    )
    
    # InvitationStatus lookup table
    op.create_table('InvitationStatus',
        sa.Column('StatusCode', sa.NVARCHAR(20), nullable=False),
        sa.Column('DisplayName', sa.NVARCHAR(50), nullable=False),
        sa.Column('Description', sa.NVARCHAR(500), nullable=False),
        sa.Column('CanResend', sa.Boolean(), nullable=False),
        sa.Column('CanCancel', sa.Boolean(), nullable=False),
        sa.Column('IsFinalState', sa.Boolean(), nullable=False),
        sa.Column('IsSystemStatus', sa.Boolean(), nullable=False, default=True),
        sa.Column('SortOrder', sa.Integer(), nullable=False),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=True),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('StatusCode')
    )
    
    # =====================================================================
    # STEP 3: COMPANY TABLES (Depends on Country)
    # =====================================================================
    
    # Company table
    op.create_table('Company',
        sa.Column('CompanyID', sa.BigInteger(), nullable=False),
        sa.Column('CompanyName', sa.NVARCHAR(200), nullable=False),
        sa.Column('CompanyNameShort', sa.NVARCHAR(50), nullable=True),
        sa.Column('ABN', sa.NVARCHAR(11), nullable=True),
        sa.Column('ACN', sa.NVARCHAR(9), nullable=True),
        sa.Column('CompanyType', sa.NVARCHAR(50), nullable=True),
        sa.Column('Industry', sa.NVARCHAR(100), nullable=True),
        sa.Column('Website', sa.NVARCHAR(200), nullable=True),
        sa.Column('Phone', sa.NVARCHAR(50), nullable=True),
        sa.Column('Email', sa.NVARCHAR(100), nullable=True),
        sa.Column('Country', sa.NVARCHAR(2), nullable=False),
        sa.Column('IsActive', sa.Boolean(), nullable=False, default=True),
        sa.Column('IsVerified', sa.Boolean(), nullable=False, default=False),
        sa.Column('VerificationDate', sa.DateTime(), nullable=True),
        sa.Column('VerificationMethod', sa.NVARCHAR(50), nullable=True),
        sa.Column('VerificationNotes', sa.NVARCHAR(500), nullable=True),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('CompanyID'),
        sa.UniqueConstraint('ABN', name='UQ_Company_ABN'),
        sa.UniqueConstraint('ACN', name='UQ_Company_ACN')
    )
    
    # CompanyCustomerDetails table
    op.create_table('CompanyCustomerDetails',
        sa.Column('CompanyID', sa.BigInteger(), nullable=False),
        sa.Column('CustomerSince', sa.DateTime(), nullable=True),
        sa.Column('SubscriptionTier', sa.NVARCHAR(50), nullable=True),
        sa.Column('SubscriptionStatus', sa.NVARCHAR(20), nullable=True),
        sa.Column('SubscriptionStartDate', sa.DateTime(), nullable=True),
        sa.Column('SubscriptionEndDate', sa.DateTime(), nullable=True),
        sa.Column('PaymentMethod', sa.NVARCHAR(50), nullable=True),
        sa.Column('BillingCycle', sa.NVARCHAR(20), nullable=True),
        sa.Column('LastPaymentDate', sa.DateTime(), nullable=True),
        sa.Column('NextPaymentDate', sa.DateTime(), nullable=True),
        sa.Column('TotalSpent', sa.DECIMAL(10, 2), nullable=True),
        sa.Column('Notes', sa.NVARCHAR(), nullable=True),
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
    
    # CompanyBillingDetails table
    op.create_table('CompanyBillingDetails',
        sa.Column('CompanyID', sa.BigInteger(), nullable=False),
        sa.Column('BillingCompanyName', sa.NVARCHAR(200), nullable=True),
        sa.Column('BillingAddress', sa.NVARCHAR(500), nullable=True),
        sa.Column('BillingCity', sa.NVARCHAR(100), nullable=True),
        sa.Column('BillingStateProvince', sa.NVARCHAR(100), nullable=True),
        sa.Column('BillingPostalCode', sa.NVARCHAR(20), nullable=True),
        sa.Column('BillingCountry', sa.NVARCHAR(2), nullable=True),
        sa.Column('BillingContactName', sa.NVARCHAR(100), nullable=True),
        sa.Column('BillingContactEmail', sa.NVARCHAR(100), nullable=True),
        sa.Column('BillingContactPhone', sa.NVARCHAR(50), nullable=True),
        sa.Column('TaxID', sa.NVARCHAR(50), nullable=True),
        sa.Column('TaxIDType', sa.NVARCHAR(20), nullable=True),
        sa.Column('PaymentTerms', sa.NVARCHAR(50), nullable=True),
        sa.Column('Currency', sa.NVARCHAR(3), nullable=True),
        sa.Column('Notes', sa.NVARCHAR(), nullable=True),
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
    
    # CompanyOrganizerDetails table
    op.create_table('CompanyOrganizerDetails',
        sa.Column('CompanyID', sa.BigInteger(), nullable=False),
        sa.Column('PrimaryContactName', sa.NVARCHAR(100), nullable=True),
        sa.Column('PrimaryContactEmail', sa.NVARCHAR(100), nullable=True),
        sa.Column('PrimaryContactPhone', sa.NVARCHAR(50), nullable=True),
        sa.Column('SecondaryContactName', sa.NVARCHAR(100), nullable=True),
        sa.Column('SecondaryContactEmail', sa.NVARCHAR(100), nullable=True),
        sa.Column('SecondaryContactPhone', sa.NVARCHAR(50), nullable=True),
        sa.Column('EventTypes', sa.NVARCHAR(), nullable=True),
        sa.Column('AverageEventSize', sa.Integer(), nullable=True),
        sa.Column('EventsPerYear', sa.Integer(), nullable=True),
        sa.Column('PreferredVenueTypes', sa.NVARCHAR(), nullable=True),
        sa.Column('BudgetRange', sa.NVARCHAR(50), nullable=True),
        sa.Column('SpecialRequirements', sa.NVARCHAR(), nullable=True),
        sa.Column('MarketingPreferences', sa.NVARCHAR(), nullable=True),
        sa.Column('Notes', sa.NVARCHAR(), nullable=True),
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
    # STEP 4: USER TABLES (Depends on Company, UserStatus, InvitationStatus)
    # =====================================================================
    
    # User table
    op.create_table('User',
        sa.Column('UserID', sa.BigInteger(), nullable=False),
        sa.Column('Email', sa.NVARCHAR(100), nullable=False),
        sa.Column('PasswordHash', sa.NVARCHAR(255), nullable=False),
        sa.Column('FirstName', sa.NVARCHAR(100), nullable=False),
        sa.Column('LastName', sa.NVARCHAR(100), nullable=False),
        sa.Column('Phone', sa.NVARCHAR(50), nullable=True),
        sa.Column('Status', sa.NVARCHAR(20), nullable=False, default='active'),
        sa.Column('EmailVerified', sa.Boolean(), nullable=False, default=False),
        sa.Column('EmailVerificationToken', sa.NVARCHAR(255), nullable=True),
        sa.Column('EmailVerificationExpires', sa.DateTime(), nullable=True),
        sa.Column('PasswordResetToken', sa.NVARCHAR(255), nullable=True),
        sa.Column('PasswordResetExpires', sa.DateTime(), nullable=True),
        sa.Column('LastLoginDate', sa.DateTime(), nullable=True),
        sa.Column('LastLoginIP', sa.NVARCHAR(45), nullable=True),
        sa.Column('LoginAttempts', sa.Integer(), nullable=False, default=0),
        sa.Column('LockedUntil', sa.DateTime(), nullable=True),
        sa.Column('TwoFactorEnabled', sa.Boolean(), nullable=False, default=False),
        sa.Column('TwoFactorSecret', sa.NVARCHAR(255), nullable=True),
        sa.Column('BackupCodes', sa.NVARCHAR(), nullable=True),
        sa.Column('LanguagePreference', sa.NVARCHAR(2), nullable=True),
        sa.Column('Timezone', sa.NVARCHAR(50), nullable=True),
        sa.Column('ProfilePicture', sa.NVARCHAR(500), nullable=True),
        sa.Column('OnboardingComplete', sa.Boolean(), nullable=False, default=False),
        sa.Column('OnboardingStep', sa.NVARCHAR(50), nullable=True),
        sa.Column('AccessTokenVersion', sa.Integer(), nullable=False, default=1),
        sa.Column('RefreshTokenVersion', sa.Integer(), nullable=False, default=1),
        sa.Column('Notes', sa.NVARCHAR(), nullable=True),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('UserID'),
        sa.UniqueConstraint('Email', name='UQ_User_Email')
    )
    
    # UserCompany table (Multi-Company Access)
    op.create_table('UserCompany',
        sa.Column('UserCompanyID', sa.BigInteger(), nullable=False),
        sa.Column('UserID', sa.BigInteger(), nullable=False),
        sa.Column('CompanyID', sa.BigInteger(), nullable=False),
        sa.Column('Role', sa.NVARCHAR(20), nullable=False, default='company_user'),
        sa.Column('Status', sa.NVARCHAR(20), nullable=False, default='active'),
        sa.Column('IsDefaultCompany', sa.Boolean(), nullable=False, default=False),
        sa.Column('JoinedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('JoinedVia', sa.NVARCHAR(20), nullable=False),
        sa.Column('InvitedByUserID', sa.BigInteger(), nullable=True),
        sa.Column('InvitationID', sa.BigInteger(), nullable=True),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('UserCompanyID'),
        sa.UniqueConstraint('UserID', 'CompanyID', name='UQ_UserCompany_User_Company')
    )
    
    # Invitation table
    op.create_table('Invitation',
        sa.Column('InvitationID', sa.BigInteger(), nullable=False),
        sa.Column('CompanyID', sa.BigInteger(), nullable=False),
        sa.Column('InvitedByUserID', sa.BigInteger(), nullable=False),
        sa.Column('InvitedEmail', sa.NVARCHAR(100), nullable=False),
        sa.Column('Role', sa.NVARCHAR(20), nullable=False),
        sa.Column('Status', sa.NVARCHAR(20), nullable=False, default='pending'),
        sa.Column('Token', sa.NVARCHAR(255), nullable=False),
        sa.Column('ExpiresAt', sa.DateTime(), nullable=False),
        sa.Column('AcceptedByUserID', sa.BigInteger(), nullable=True),
        sa.Column('AcceptedAt', sa.DateTime(), nullable=True),
        sa.Column('CancelledByUserID', sa.BigInteger(), nullable=True),
        sa.Column('CancelledAt', sa.DateTime(), nullable=True),
        sa.Column('CancellationReason', sa.NVARCHAR(500), nullable=True),
        sa.Column('Message', sa.NVARCHAR(1000), nullable=True),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('InvitationID'),
        sa.UniqueConstraint('Token', name='UQ_Invitation_Token')
    )
    
    # =====================================================================
    # STEP 5: ENHANCED FEATURES TABLES (Depends on User, Company)
    # =====================================================================
    
    # ABRSearchCache table
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
    
    # CompanyRelationship table
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
    
    # CompanySwitchRequest table
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
    
    # CountryWebProperties table
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
    
    # ValidationRule table
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
    
    # LookupTableWebProperties table
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
    
    # LookupValueWebProperties table
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
    # STEP 6: APPLICATION SPECIFICATION TABLES (Depends on Company, Country)
    # =====================================================================
    
    # ApplicationSpecification table
    op.create_table('ApplicationSpecification',
        sa.Column('SpecificationID', sa.BigInteger(), nullable=False),
        sa.Column('SpecificationName', sa.NVARCHAR(100), nullable=False),
        sa.Column('SpecificationVersion', sa.NVARCHAR(20), nullable=False),
        sa.Column('Description', sa.NVARCHAR(1000), nullable=True),
        sa.Column('Configuration', sa.JSON(), nullable=True),
        sa.Column('IsActive', sa.Boolean(), nullable=False, default=True),
        sa.Column('IsDefault', sa.Boolean(), nullable=False, default=False),
        sa.Column('SortOrder', sa.Integer(), nullable=False, default=999),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('SpecificationID')
    )
    
    # CountryApplicationSpecification table
    op.create_table('CountryApplicationSpecification',
        sa.Column('CountryID', sa.BigInteger(), nullable=False),
        sa.Column('SpecificationID', sa.BigInteger(), nullable=False),
        sa.Column('IsActive', sa.Boolean(), nullable=False, default=True),
        sa.Column('Configuration', sa.JSON(), nullable=True),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('CountryID', 'SpecificationID')
    )
    
    # EnvironmentApplicationSpecification table
    op.create_table('EnvironmentApplicationSpecification',
        sa.Column('EnvironmentID', sa.BigInteger(), nullable=False),
        sa.Column('SpecificationID', sa.BigInteger(), nullable=False),
        sa.Column('EnvironmentName', sa.NVARCHAR(50), nullable=False),
        sa.Column('IsActive', sa.Boolean(), nullable=False, default=True),
        sa.Column('Configuration', sa.JSON(), nullable=True),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('EnvironmentID', 'SpecificationID')
    )
    
    # =====================================================================
    # STEP 7: CHECK CONSTRAINTS
    # =====================================================================
    
    # Country constraints
    op.create_check_constraint('CK_Country_Code', 'Country', "LEN(CountryCode) = 2 AND CountryCode = UPPER(CountryCode)")
    op.create_check_constraint('CK_Country_Currency', 'Country', "LEN(CurrencyCode) = 3 AND CurrencyCode = UPPER(CurrencyCode)")
    
    # Language constraints
    op.create_check_constraint('CK_Language_Code', 'Language', "LEN(LanguageCode) = 2 AND LanguageCode = LOWER(LanguageCode)")
    op.create_check_constraint('CK_Language_Direction', 'Language', "Direction IN ('LTR', 'RTL')")
    
    # User constraints
    op.create_check_constraint('CK_User_AccessTokenVersion', 'User', "AccessTokenVersion > 0")
    op.create_check_constraint('CK_User_RefreshTokenVersion', 'User', "RefreshTokenVersion > 0")
    
    # UserCompany constraints
    op.create_check_constraint('CK_UserCompany_Role', 'UserCompany', "Role IN ('admin', 'manager', 'company_user', 'viewer')")
    op.create_check_constraint('CK_UserCompany_Status', 'UserCompany', "Status IN ('active', 'suspended', 'inactive')")
    op.create_check_constraint('CK_UserCompany_JoinedVia', 'UserCompany', "JoinedVia IN ('invitation', 'direct_add', 'self_join')")
    
    # ABRSearchCache constraints
    op.create_check_constraint('CK_ABRSearchCache_SearchType', 'ABRSearchCache', "SearchType IN ('ABN', 'ACN', 'Name')")
    op.create_check_constraint('CK_ABRSearchCache_ResultIndex', 'ABRSearchCache', "ResultIndex >= 0")
    
    # CompanyRelationship constraints
    op.create_check_constraint('CK_CompanyRelationship_Type', 'CompanyRelationship', "RelationshipType IN ('branch', 'subsidiary', 'partner', 'affiliate', 'division')")
    op.create_check_constraint('CK_CompanyRelationship_Status', 'CompanyRelationship', "Status IN ('active', 'suspended', 'terminated', 'pending')")
    op.create_check_constraint('CK_CompanyRelationship_NotSelf', 'CompanyRelationship', "ParentCompanyID != ChildCompanyID")
    
    # CompanySwitchRequest constraints
    op.create_check_constraint('CK_CompanySwitchRequest_Type', 'CompanySwitchRequest', "RequestType IN ('invitation_accepted', 'company_switch', 'relationship_join', 'access_request')")
    op.create_check_constraint('CK_CompanySwitchRequest_Status', 'CompanySwitchRequest', "Status IN ('pending', 'approved', 'rejected', 'expired', 'cancelled')")
    
    # ValidationRule constraints
    op.create_check_constraint('CK_ValidationRule_Type', 'ValidationRule', "RuleType IN ('phone', 'postal_code', 'tax_id', 'address', 'email', 'url', 'date', 'number')")
    op.create_check_constraint('CK_ValidationRule_SortOrder', 'ValidationRule', "SortOrder > 0")
    
    # =====================================================================
    # STEP 8: FOREIGN KEY CONSTRAINTS (All tables now exist)
    # =====================================================================
    
    # Country foreign keys
    op.create_foreign_key('FK_Country_DefaultLanguage', 'Country', 'Language', ['DefaultLanguageCode'], ['LanguageCode'])
    
    # User foreign keys
    op.create_foreign_key('FK_User_Status', 'User', 'UserStatus', ['Status'], ['StatusCode'])
    op.create_foreign_key('FK_User_LanguagePreference', 'User', 'Language', ['LanguagePreference'], ['LanguageCode'])
    
    # UserCompany foreign keys
    op.create_foreign_key('FK_UserCompany_User', 'UserCompany', 'User', ['UserID'], ['UserID'])
    op.create_foreign_key('FK_UserCompany_Company', 'UserCompany', 'Company', ['CompanyID'], ['CompanyID'])
    op.create_foreign_key('FK_UserCompany_InvitedBy', 'UserCompany', 'User', ['InvitedByUserID'], ['UserID'])
    
    # Invitation foreign keys
    op.create_foreign_key('FK_Invitation_Company', 'Invitation', 'Company', ['CompanyID'], ['CompanyID'])
    op.create_foreign_key('FK_Invitation_InvitedBy', 'Invitation', 'User', ['InvitedByUserID'], ['UserID'])
    op.create_foreign_key('FK_Invitation_AcceptedBy', 'Invitation', 'User', ['AcceptedByUserID'], ['UserID'])
    op.create_foreign_key('FK_Invitation_CancelledBy', 'Invitation', 'User', ['CancelledByUserID'], ['UserID'])
    op.create_foreign_key('FK_Invitation_Status', 'Invitation', 'InvitationStatus', ['Status'], ['StatusCode'])
    
    # CompanyBillingDetails foreign keys
    op.create_foreign_key('FK_CompanyBillingDetails_Company', 'CompanyBillingDetails', 'Company', ['CompanyID'], ['CompanyID'])
    op.create_foreign_key('FK_CompanyBillingDetails_BillingCountry', 'CompanyBillingDetails', 'Country', ['BillingCountry'], ['CountryCode'])
    
    # CompanyCustomerDetails foreign keys
    op.create_foreign_key('FK_CompanyCustomerDetails_Company', 'CompanyCustomerDetails', 'Company', ['CompanyID'], ['CompanyID'])
    
    # CompanyOrganizerDetails foreign keys
    op.create_foreign_key('FK_CompanyOrganizerDetails_Company', 'CompanyOrganizerDetails', 'Company', ['CompanyID'], ['CompanyID'])
    
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
    
    # ApplicationSpecification foreign keys
    op.create_foreign_key('FK_CountryApplicationSpecification_Country', 'CountryApplicationSpecification', 'Country', ['CountryID'], ['CountryID'])
    op.create_foreign_key('FK_CountryApplicationSpecification_Specification', 'CountryApplicationSpecification', 'ApplicationSpecification', ['SpecificationID'], ['SpecificationID'])
    
    # EnvironmentApplicationSpecification foreign keys
    op.create_foreign_key('FK_EnvironmentApplicationSpecification_Specification', 'EnvironmentApplicationSpecification', 'ApplicationSpecification', ['SpecificationID'], ['SpecificationID'])
    
    # =====================================================================
    # STEP 9: INDEXES
    # =====================================================================
    
    # Country indexes
    op.create_index('IX_Country_Name', 'Country', ['CountryName', 'IsDeleted'])
    op.create_index('IX_Country_Supported', 'Country', ['IsSupported', 'IsDeleted'])
    
    # Language indexes
    op.create_index('IX_Language_Name', 'Language', ['LanguageName', 'IsDeleted'])
    op.create_index('IX_Language_Supported', 'Language', ['IsSupported', 'IsDeleted'])
    
    # User indexes
    op.create_index('IX_User_Email', 'User', ['Email'])
    op.create_index('IX_User_Status', 'User', ['Status'])
    op.create_index('IX_User_OnboardingComplete', 'User', ['OnboardingComplete'])
    
    # UserCompany indexes
    op.create_index('IX_UserCompany_UserID', 'UserCompany', ['UserID'])
    op.create_index('IX_UserCompany_CompanyID', 'UserCompany', ['CompanyID'])
    op.create_index('IX_UserCompany_Default', 'UserCompany', ['UserID', 'IsDefaultCompany'])
    
    # Invitation indexes
    op.create_index('IX_Invitation_CompanyID', 'Invitation', ['CompanyID'])
    op.create_index('IX_Invitation_Email', 'Invitation', ['InvitedEmail'])
    op.create_index('IX_Invitation_Status', 'Invitation', ['Status'])
    op.create_index('IX_Invitation_ExpiresAt', 'Invitation', ['ExpiresAt'])
    
    # Company indexes
    op.create_index('IX_Company_Name', 'Company', ['CompanyName', 'IsDeleted'])
    op.create_index('IX_Company_ABN', 'Company', ['ABN'])
    op.create_index('IX_Company_ACN', 'Company', ['ACN'])
    op.create_index('IX_Company_Country', 'Company', ['Country'])
    op.create_index('IX_Company_Active', 'Company', ['IsActive', 'IsDeleted'])
    
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


def downgrade() -> None:
    """Drop complete EventLead Platform database schema"""
    
    # Drop indexes (in reverse order)
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
    op.drop_index('IX_Company_Active', table_name='Company')
    op.drop_index('IX_Company_Country', table_name='Company')
    op.drop_index('IX_Company_ACN', table_name='Company')
    op.drop_index('IX_Company_ABN', table_name='Company')
    op.drop_index('IX_Company_Name', table_name='Company')
    op.drop_index('IX_Invitation_ExpiresAt', table_name='Invitation')
    op.drop_index('IX_Invitation_Status', table_name='Invitation')
    op.drop_index('IX_Invitation_Email', table_name='Invitation')
    op.drop_index('IX_Invitation_CompanyID', table_name='Invitation')
    op.drop_index('IX_UserCompany_Default', table_name='UserCompany')
    op.drop_index('IX_UserCompany_CompanyID', table_name='UserCompany')
    op.drop_index('IX_UserCompany_UserID', table_name='UserCompany')
    op.drop_index('IX_User_OnboardingComplete', table_name='User')
    op.drop_index('IX_User_Status', table_name='User')
    op.drop_index('IX_User_Email', table_name='User')
    op.drop_index('IX_Language_Supported', table_name='Language')
    op.drop_index('IX_Language_Name', table_name='Language')
    op.drop_index('IX_Country_Supported', table_name='Country')
    op.drop_index('IX_Country_Name', table_name='Country')
    
    # Drop foreign key constraints (in reverse order)
    op.drop_constraint('FK_EnvironmentApplicationSpecification_Specification', 'EnvironmentApplicationSpecification', type_='foreignkey')
    op.drop_constraint('FK_CountryApplicationSpecification_Specification', 'CountryApplicationSpecification', type_='foreignkey')
    op.drop_constraint('FK_CountryApplicationSpecification_Country', 'CountryApplicationSpecification', type_='foreignkey')
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
    op.drop_constraint('FK_CompanyOrganizerDetails_Company', 'CompanyOrganizerDetails', type_='foreignkey')
    op.drop_constraint('FK_CompanyCustomerDetails_Company', 'CompanyCustomerDetails', type_='foreignkey')
    op.drop_constraint('FK_CompanyBillingDetails_BillingCountry', 'CompanyBillingDetails', type_='foreignkey')
    op.drop_constraint('FK_CompanyBillingDetails_Company', 'CompanyBillingDetails', type_='foreignkey')
    op.drop_constraint('FK_Invitation_Status', 'Invitation', type_='foreignkey')
    op.drop_constraint('FK_Invitation_CancelledBy', 'Invitation', type_='foreignkey')
    op.drop_constraint('FK_Invitation_AcceptedBy', 'Invitation', type_='foreignkey')
    op.drop_constraint('FK_Invitation_InvitedBy', 'Invitation', type_='foreignkey')
    op.drop_constraint('FK_Invitation_Company', 'Invitation', type_='foreignkey')
    op.drop_constraint('FK_UserCompany_InvitedBy', 'UserCompany', type_='foreignkey')
    op.drop_constraint('FK_UserCompany_Company', 'UserCompany', type_='foreignkey')
    op.drop_constraint('FK_UserCompany_User', 'UserCompany', type_='foreignkey')
    op.drop_constraint('FK_User_LanguagePreference', 'User', type_='foreignkey')
    op.drop_constraint('FK_User_Status', 'User', type_='foreignkey')
    op.drop_constraint('FK_Country_DefaultLanguage', 'Country', type_='foreignkey')
    
    # Drop check constraints (in reverse order)
    op.drop_constraint('CK_ValidationRule_SortOrder', 'ValidationRule', type_='check')
    op.drop_constraint('CK_ValidationRule_Type', 'ValidationRule', type_='check')
    op.drop_constraint('CK_CompanySwitchRequest_Status', 'CompanySwitchRequest', type_='check')
    op.drop_constraint('CK_CompanySwitchRequest_Type', 'CompanySwitchRequest', type_='check')
    op.drop_constraint('CK_CompanyRelationship_NotSelf', 'CompanyRelationship', type_='check')
    op.drop_constraint('CK_CompanyRelationship_Status', 'CompanyRelationship', type_='check')
    op.drop_constraint('CK_CompanyRelationship_Type', 'CompanyRelationship', type_='check')
    op.drop_constraint('CK_ABRSearchCache_ResultIndex', 'ABRSearchCache', type_='check')
    op.drop_constraint('CK_ABRSearchCache_SearchType', 'ABRSearchCache', type_='check')
    op.drop_constraint('CK_UserCompany_JoinedVia', 'UserCompany', type_='check')
    op.drop_constraint('CK_UserCompany_Status', 'UserCompany', type_='check')
    op.drop_constraint('CK_UserCompany_Role', 'UserCompany', type_='check')
    op.drop_constraint('CK_User_RefreshTokenVersion', 'User', type_='check')
    op.drop_constraint('CK_User_AccessTokenVersion', 'User', type_='check')
    op.drop_constraint('CK_Language_Direction', 'Language', type_='check')
    op.drop_constraint('CK_Language_Code', 'Language', type_='check')
    op.drop_constraint('CK_Country_Currency', 'Country', type_='check')
    op.drop_constraint('CK_Country_Code', 'Country', type_='check')
    
    # Drop tables (in reverse order)
    op.drop_table('EnvironmentApplicationSpecification')
    op.drop_table('CountryApplicationSpecification')
    op.drop_table('ApplicationSpecification')
    op.drop_table('LookupValueWebProperties')
    op.drop_table('LookupTableWebProperties')
    op.drop_table('ValidationRule')
    op.drop_table('CountryWebProperties')
    op.drop_table('CompanySwitchRequest')
    op.drop_table('CompanyRelationship')
    op.drop_table('ABRSearchCache')
    op.drop_table('CompanyOrganizerDetails')
    op.drop_table('CompanyBillingDetails')
    op.drop_table('CompanyCustomerDetails')
    op.drop_table('Company')
    op.drop_table('Invitation')
    op.drop_table('UserCompany')
    op.drop_table('User')
    op.drop_table('InvitationStatus')
    op.drop_table('UserStatus')
    op.drop_table('Language')
    op.drop_table('Country')