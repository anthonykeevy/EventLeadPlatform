"""Create foundation tables (Country, Language)

Revision ID: 001_foundation_tables
Revises: 
Create Date: 2025-10-13 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = '001_foundation_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Create Country and Language foundation tables"""
    
    # =====================================================================
    # TABLE: Country (ISO 3166-1 Reference Data)
    # =====================================================================
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
    
    # =====================================================================
    # TABLE: Language (ISO 639-1 Reference Data)
    # =====================================================================
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
    # CONSTRAINTS
    # =====================================================================
    
    # Country constraints
    op.create_check_constraint(
        'CK_Country_Code',
        'Country',
        "LEN(CountryCode) = 2 AND CountryCode = UPPER(CountryCode)"
    )
    
    op.create_check_constraint(
        'CK_Country_Currency',
        'Country',
        "LEN(CurrencyCode) = 3 AND CurrencyCode = UPPER(CurrencyCode)"
    )
    
    # Language constraints
    op.create_check_constraint(
        'CK_Language_Code',
        'Language',
        "LEN(LanguageCode) = 2 AND LanguageCode = LOWER(LanguageCode)"
    )
    
    op.create_check_constraint(
        'CK_Language_Direction',
        'Language',
        "Direction IN ('LTR', 'RTL')"
    )
    
    # =====================================================================
    # INDEXES
    # =====================================================================
    
    # Country indexes
    op.create_index('IX_Country_Name', 'Country', ['CountryName', 'IsDeleted'])
    op.create_index('IX_Country_Supported', 'Country', ['IsSupported', 'IsDeleted'])
    
    # Language indexes
    op.create_index('IX_Language_Name', 'Language', ['LanguageName', 'IsDeleted'])
    op.create_index('IX_Language_Supported', 'Language', ['IsSupported', 'IsDeleted'])


def downgrade():
    """Drop foundation tables"""
    
    # Drop indexes
    op.drop_index('IX_Language_Supported', table_name='Language')
    op.drop_index('IX_Language_Name', table_name='Language')
    op.drop_index('IX_Country_Supported', table_name='Country')
    op.drop_index('IX_Country_Name', table_name='Country')
    
    # Drop constraints
    op.drop_constraint('CK_Language_Direction', 'Language', type_='check')
    op.drop_constraint('CK_Language_Code', 'Language', type_='check')
    op.drop_constraint('CK_Country_Currency', 'Country', type_='check')
    op.drop_constraint('CK_Country_Code', 'Country', type_='check')
    
    # Drop tables
    op.drop_table('Language')
    op.drop_table('Country')
