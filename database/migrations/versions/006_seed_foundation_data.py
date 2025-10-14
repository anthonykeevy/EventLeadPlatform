"""Seed foundation data (Country, Language, Lookup tables, Application Specification)

Revision ID: 006_seed_foundation_data
Revises: 005_application_specification_tables
Create Date: 2025-10-13 12:05:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '006_seed_foundation_data'
down_revision = '005_application_specification_tables'
branch_labels = None
depends_on = None


def upgrade():
    """Seed foundation data"""
    
    # =====================================================================
    # SEED DATA: Country (Australia - MVP)
    # =====================================================================
    op.execute("""
        INSERT INTO [Country] (
            CountryCode, CountryName, Region, Continent,
            CurrencyCode, CurrencyName, CurrencySymbol,
            TaxIDType, TaxIDLabel, TaxIDFormat, TaxIDValidationAPI,
            ConsumptionTaxName, ConsumptionTaxRate, ConsumptionTaxVariable,
            AddressFormat, RequiresStateProvince, PostalCodeLabel, PostalCodeFormat,
            PhoneCountryCode, PhoneLandlineRegex, PhoneMobileRegex, PhoneFreeCallRegex, PhoneSpecialRegex, PhoneFormatExample,
            IsSupported, LaunchDate, SupportPriority,
            DefaultLanguageCode, Locale, DateFormat, TimeFormat,
            Notes,
            CreatedBy
        ) VALUES (
            'AU', 'Australia', 'Asia-Pacific', 'Oceania',
            'AUD', 'Australian Dollar', '$',
            'ABN', 'ABN (Australian Business Number)', '11 digits', 'https://abr.business.gov.au/abrxmlsearch',
            'GST', 10.00, 0,
            '[AddressLine1], [City] [StateProvince] [PostalCode]', 1, 'Postcode', '4 digits',
            '+61', 
            '^\+61\s?[2378]\s?\d{4}\s?\d{4}$',
            '^\+61\s?4\d{2}\s?\d{3}\s?\d{3}$',
            '^(1800|1300)\s?\d{3}\s?\d{3}$',
            '^(13\s?\d{4}|1900\s?\d{6})$',
            'Landline: +61 2 9215 7100 | Mobile: +61 400 123 456 | Free call: 1800 123 456 | Special: 13 1234',
            1, '2025-10-01', 1,
            'en', 'en-AU', 'DD/MM/YYYY', '24-hour',
            'MVP launch market. ABN validation via ABR API (FREE). GST compliance required for invoices.',
            1
        )
    """)
    
    # =====================================================================
    # SEED DATA: Language (English - MVP)
    # =====================================================================
    op.execute("""
        INSERT INTO [Language] (
            LanguageCode, LanguageName, LanguageNameLocal, LanguageFamily, Direction,
            IsSupported, TranslationCompleteness, LaunchDate, SupportPriority,
            PluralRules, DateFormatExample, NumberFormat,
            Notes,
            CreatedBy
        ) VALUES (
            'en', 'English', 'English', 'Germanic', 'LTR',
            1, 100, '2025-10-01', 1,
            '{"one": "1 item", "other": "{n} items"}', '13/10/2025', '1,234.56',
            'Primary platform language. Australian English dialect (en-AU) for MVP.',
            1
        )
    """)
    
    # =====================================================================
    # SEED DATA: CountryWebProperties (Australia)
    # =====================================================================
    op.execute("""
        INSERT INTO [CountryWebProperties] (
            CountryID, SortOrder, DisplayColor, IsActive, LaunchPriority,
            MarketingName, SupportEmail, LegalJurisdiction, TimezoneOffset,
            DateFormat, CurrencySymbol, CurrencyPosition, IsDefaultCountry,
            CreatedBy
        ) VALUES (
            1, 1, '#0066CC', 1, 1,
            'Australia', 'support@eventleadplatform.com.au', 'Australia', '+10:00',
            'DD/MM/YYYY', '$', 'before', 1,
            1
        )
    """)
    
    # =====================================================================
    # SEED DATA: ValidationRule (Australia-specific validation rules)
    # =====================================================================
    op.execute("""
        INSERT INTO [ValidationRule] (
            CountryID, RuleType, RuleName, ValidationPattern, ErrorMessage,
            IsActive, SortOrder, MinLength, MaxLength, ExampleValue, Description,
            IsRequired, FieldType,
            CreatedBy
        ) VALUES
            -- Phone validation rules
            (1, 'phone', 'Australian Landline', '^\+61\s?[2378]\s?\d{4}\s?\d{4}$', 'Please enter a valid Australian landline number (e.g., +61 2 9215 7100)', 1, 1, 14, 18, '+61 2 9215 7100', 'Australian landline phone validation', 0, 'phone', 1),
            (1, 'phone', 'Australian Mobile', '^\+61\s?4\d{2}\s?\d{3}\s?\d{3}$', 'Please enter a valid Australian mobile number (e.g., +61 400 123 456)', 1, 2, 14, 18, '+61 400 123 456', 'Australian mobile phone validation', 0, 'phone', 1),
            (1, 'phone', 'Australian Free Call', '^(1800|1300)\s?\d{3}\s?\d{3}$', 'Please enter a valid Australian free call number (e.g., 1800 123 456)', 1, 3, 10, 14, '1800 123 456', 'Australian free call number validation', 0, 'phone', 1),
            
            -- Postal code validation rules
            (1, 'postal_code', 'Australian Postcode', '^\d{4}$', 'Please enter a valid Australian postcode (4 digits)', 1, 1, 4, 4, '2000', 'Australian postal code validation', 0, 'text', 1),
            
            -- Tax ID validation rules
            (1, 'tax_id', 'Australian ABN', '^\d{11}$', 'Please enter a valid 11-digit ABN', 1, 1, 11, 11, '12345678901', 'Australian Business Number validation', 0, 'text', 1),
            
            -- Address validation rules
            (1, 'address', 'Australian Address Format', '^.{10,200}$', 'Please enter a valid Australian address (10-200 characters)', 1, 1, 10, 200, '123 George Street, Sydney NSW 2000', 'Australian address format validation', 0, 'text', 1)
    """)
    
    # =====================================================================
    # SEED DATA: LookupTableWebProperties (Lookup table UI properties)
    # =====================================================================
    op.execute("""
        INSERT INTO [LookupTableWebProperties] (
            TableName, DisplayName, SortOrder, DisplayColor, IsActive,
            IconClass, Description, Category, IsSystemTable, AllowCustomValues,
            CreatedBy
        ) VALUES
            ('UserStatus', 'User Status', 1, '#28a745', 1, 'fas fa-user-check', 'User account status definitions', 'User Management', 1, 0, 1),
            ('InvitationStatus', 'Invitation Status', 2, '#17a2b8', 1, 'fas fa-envelope', 'Team invitation status definitions', 'Team Management', 1, 0, 1),
            ('CompanyType', 'Company Type', 3, '#6f42c1', 1, 'fas fa-building', 'Company type classifications', 'Company Management', 0, 1, 1),
            ('Industry', 'Industry', 4, '#fd7e14', 1, 'fas fa-industry', 'Industry classifications', 'Company Management', 0, 1, 1),
            ('SubscriptionPlan', 'Subscription Plan', 5, '#20c997', 1, 'fas fa-crown', 'Subscription plan types', 'Billing', 1, 0, 1),
            ('SubscriptionStatus', 'Subscription Status', 6, '#6c757d', 1, 'fas fa-credit-card', 'Subscription status definitions', 'Billing', 1, 0, 1)
    """)
    
    # =====================================================================
    # SEED DATA: LookupValueWebProperties (Lookup value UI properties)
    # =====================================================================
    op.execute("""
        INSERT INTO [LookupValueWebProperties] (
            TableName, ValueCode, SortOrder, DisplayColor, IconClass, TooltipText,
            IsDefault, IsActive, IsSystemValue, CustomDisplayName,
            CreatedBy
        ) VALUES
            -- UserStatus values
            ('UserStatus', 'active', 1, '#28a745', 'fas fa-user-check', 'User can log in and use the platform', 1, 1, 1, NULL, 1),
            ('UserStatus', 'unverified', 2, '#ffc107', 'fas fa-user-clock', 'User needs to verify their email address', 0, 1, 1, NULL, 1),
            ('UserStatus', 'suspended', 3, '#dc3545', 'fas fa-user-slash', 'User account is temporarily suspended', 0, 1, 1, NULL, 1),
            ('UserStatus', 'locked', 4, '#6c757d', 'fas fa-lock', 'User account is locked due to failed login attempts', 0, 1, 1, NULL, 1),
            ('UserStatus', 'deleted', 5, '#343a40', 'fas fa-user-times', 'User account has been deleted', 0, 1, 1, NULL, 1),
            
            -- InvitationStatus values
            ('InvitationStatus', 'pending', 1, '#17a2b8', 'fas fa-envelope', 'Invitation sent but not yet accepted', 1, 1, 1, NULL, 1),
            ('InvitationStatus', 'accepted', 2, '#28a745', 'fas fa-check-circle', 'Invitation accepted - user joined company', 0, 1, 1, NULL, 1),
            ('InvitationStatus', 'expired', 3, '#ffc107', 'fas fa-clock', 'Invitation expired without acceptance', 0, 1, 1, NULL, 1),
            ('InvitationStatus', 'cancelled', 4, '#6c757d', 'fas fa-times-circle', 'Invitation cancelled by admin', 0, 1, 1, NULL, 1),
            ('InvitationStatus', 'declined', 5, '#dc3545', 'fas fa-ban', 'Invitation declined by invitee', 0, 1, 1, NULL, 1),
            
            -- SubscriptionPlan values
            ('SubscriptionPlan', 'free', 1, '#6c757d', 'fas fa-gift', 'Free tier with basic features', 1, 1, 1, 'Free', 1),
            ('SubscriptionPlan', 'basic', 2, '#17a2b8', 'fas fa-star', 'Basic plan with enhanced features', 0, 1, 1, 'Basic', 1),
            ('SubscriptionPlan', 'professional', 3, '#6f42c1', 'fas fa-crown', 'Professional plan with advanced features', 0, 1, 1, 'Professional', 1),
            ('SubscriptionPlan', 'enterprise', 4, '#fd7e14', 'fas fa-building', 'Enterprise plan with custom features', 0, 1, 1, 'Enterprise', 1),
            
            -- SubscriptionStatus values
            ('SubscriptionStatus', 'active', 1, '#28a745', 'fas fa-check-circle', 'Subscription is active and billing', 1, 1, 1, NULL, 1),
            ('SubscriptionStatus', 'trial', 2, '#17a2b8', 'fas fa-clock', 'Trial period active', 0, 1, 1, NULL, 1),
            ('SubscriptionStatus', 'cancelled', 3, '#dc3545', 'fas fa-times-circle', 'Subscription cancelled', 0, 1, 1, NULL, 1),
            ('SubscriptionStatus', 'suspended', 4, '#ffc107', 'fas fa-pause-circle', 'Subscription suspended', 0, 1, 1, NULL, 1),
            ('SubscriptionStatus', 'expired', 5, '#6c757d', 'fas fa-hourglass-end', 'Subscription expired', 0, 1, 1, NULL, 1)
    """)
    
    # =====================================================================
    # SEED DATA: CountryApplicationSpecification (Australia-specific overrides)
    # =====================================================================
    op.execute("""
        INSERT INTO [CountryApplicationSpecification] (
            CountryID, Category, ParameterName, ParameterValue, DataType,
            Description, IsActive, SortOrder, OverrideReason,
            CreatedBy
        ) VALUES
            (1, 'validation', 'company_name_min_length', '3', 'integer', 'Australia requires longer company names', 1, 1, 'Australian business registration requirements', 1),
            (1, 'business_rules', 'abn_cache_ttl_days', '30', 'integer', 'ABR API allows 30-day caching for Australia', 1, 1, 'ABR API caching policy', 1),
            (1, 'validation', 'phone_country_code', '+61', 'string', 'Australian international dialing code', 1, 1, 'Country-specific phone format', 1),
            (1, 'validation', 'postal_code_format', '^\\d{4}$', 'string', 'Australian postcode format (4 digits)', 1, 1, 'Australian postal system', 1),
            (1, 'business_rules', 'default_currency', 'AUD', 'string', 'Australian Dollar as default currency', 1, 1, 'Australian market', 1),
            (1, 'business_rules', 'consumption_tax_rate', '10.00', 'decimal', 'Australian GST rate', 1, 1, 'Australian tax law', 1),
            (1, 'validation', 'tax_id_label', 'ABN', 'string', 'Australian Business Number label', 1, 1, 'Australian tax terminology', 1)
    """)


def downgrade():
    """Remove foundation seed data"""
    
    # Remove seed data in reverse order (due to foreign key constraints)
    op.execute("DELETE FROM [CountryApplicationSpecification] WHERE CountryID = 1")
    op.execute("DELETE FROM [LookupValueWebProperties] WHERE TableName IN ('UserStatus', 'InvitationStatus', 'SubscriptionPlan', 'SubscriptionStatus')")
    op.execute("DELETE FROM [LookupTableWebProperties] WHERE TableName IN ('UserStatus', 'InvitationStatus', 'CompanyType', 'Industry', 'SubscriptionPlan', 'SubscriptionStatus')")
    op.execute("DELETE FROM [ValidationRule] WHERE CountryID = 1")
    op.execute("DELETE FROM [CountryWebProperties] WHERE CountryID = 1")
    op.execute("DELETE FROM [Language] WHERE LanguageCode = 'en'")
    op.execute("DELETE FROM [Country] WHERE CountryCode = 'AU'")
