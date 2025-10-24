"""Company-level validation architecture - Story 1.20

Comprehensive phone validation with company-level configuration.
Adds support for AU, NZ, US, UK, CA with telco-specific rules.
Seeds EventLeads company validation configuration.

Revision ID: 009
Revises: 008
Create Date: 2025-10-23

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '009'
down_revision = '008'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Story 1.20: Company-Level Phone Validation Architecture
    
    Features:
    1. CompanyValidationRule table (company-specific rule configuration)
    2. Comprehensive phone rules for AU, NZ, US, UK, CA
    3. EventLeads company seed data with validation configuration
    4. Soft delete support for validation rules
    5. Validation message stacking capability
    
    Architecture:
    - Country → ValidationRule (base rules, IsActive controls country-level availability)
    - Company → CompanyValidationRule → ValidationRule (company enables/disables)
    - Rule is usable IF: ValidationRule.IsActive = 1 AND CompanyValidationRule.IsEnabled = 1
    - Companies without config inherit all active country rules (backward compatible)
    """
    
    # ========================================
    # STEP 1: Add SortOrder Column to ValidationRule
    # ========================================
    
    # Add SortOrder column (standardize from Priority)
    op.execute("""
        IF NOT EXISTS (
            SELECT 1 FROM sys.columns 
            WHERE object_id = OBJECT_ID('[config].[ValidationRule]') 
            AND name = 'SortOrder'
        )
        BEGIN
            ALTER TABLE [config].[ValidationRule]
            ADD SortOrder INT NULL;
        END
    """)
    
    # Copy Priority to SortOrder using dynamic SQL
    op.execute("""
        IF EXISTS (
            SELECT 1 FROM sys.columns 
            WHERE object_id = OBJECT_ID('[config].[ValidationRule]') 
            AND name = 'SortOrder'
            AND is_nullable = 1
        )
        BEGIN
            EXEC('UPDATE [config].[ValidationRule] SET SortOrder = ISNULL(Priority, 999)');
            ALTER TABLE [config].[ValidationRule] ALTER COLUMN SortOrder INT NOT NULL;
        END
    """)
    
    # Add display formatting columns for local number display (Story 1.20)
    op.execute("""
        IF NOT EXISTS (
            SELECT 1 FROM sys.columns 
            WHERE object_id = OBJECT_ID('[config].[ValidationRule]') 
            AND name = 'DisplayFormat'
        )
        BEGIN
            ALTER TABLE [config].[ValidationRule]
            ADD DisplayFormat NVARCHAR(100) NULL,
                DisplayExample NVARCHAR(100) NULL,
                StripPrefix BIT NOT NULL DEFAULT 0,
                SpacingPattern NVARCHAR(50) NULL;  -- e.g., '04XX XXX XXX' for formatting
        END
    """)
    
    op.execute("""
        -- Add constraint for display format
        IF NOT EXISTS (SELECT 1 FROM sys.check_constraints WHERE name = 'CK_ValidationRule_DisplayFormat')
        BEGIN
            ALTER TABLE [config].[ValidationRule]
            ADD CONSTRAINT CK_ValidationRule_DisplayFormat
            CHECK (DisplayFormat IS NULL OR LEN(DisplayFormat) > 0);
        END
    """)
    
    # Set display formats for existing postal code rule
    op.execute("""
        UPDATE [config].[ValidationRule]
        SET 
            DisplayFormat = 'XXXX',
            DisplayExample = '2000',
            StripPrefix = 0,
            SpacingPattern = 'XXXX'
        WHERE RuleKey = 'POSTAL_CODE_FORMAT'
    """)
    
    # ========================================
    # STEP 2: Create CompanyValidationRule Table
    # ========================================
    
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'CompanyValidationRule' AND schema_id = SCHEMA_ID('config'))
        BEGIN
            CREATE TABLE [config].[CompanyValidationRule] (
                CompanyValidationRuleID BIGINT IDENTITY(1,1) NOT NULL,
                
                -- Links
                CompanyID BIGINT NOT NULL,
                ValidationRuleID BIGINT NOT NULL,
                
                -- Configuration
                IsEnabled BIT NOT NULL DEFAULT 1,
                SortOrderOverride INT NULL,  -- Optional: Company can reorder rules
                
                -- Audit trail
                CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
                CreatedBy BIGINT NULL,
                UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
                UpdatedBy BIGINT NULL,
                
                -- Soft delete
                IsDeleted BIT NOT NULL DEFAULT 0,
                DeletedDate DATETIME2 NULL,
                DeletedBy BIGINT NULL,
                
                -- Primary key
                CONSTRAINT PK_CompanyValidationRule 
                    PRIMARY KEY (CompanyValidationRuleID),
                
                -- Foreign keys
                CONSTRAINT FK_CompanyValidationRule_Company 
                    FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID),
                CONSTRAINT FK_CompanyValidationRule_ValidationRule 
                    FOREIGN KEY (ValidationRuleID) REFERENCES [config].[ValidationRule](ValidationRuleID),
                CONSTRAINT FK_CompanyValidationRule_CreatedBy 
                    FOREIGN KEY (CreatedBy) REFERENCES [dbo].[User](UserID),
                CONSTRAINT FK_CompanyValidationRule_UpdatedBy 
                    FOREIGN KEY (UpdatedBy) REFERENCES [dbo].[User](UserID),
                CONSTRAINT FK_CompanyValidationRule_DeletedBy 
                    FOREIGN KEY (DeletedBy) REFERENCES [dbo].[User](UserID),
                
                -- Unique constraint
                CONSTRAINT UQ_CompanyValidationRule_Company_Rule 
                    UNIQUE (CompanyID, ValidationRuleID)
            );
            
            -- Indexes
            CREATE INDEX IX_CompanyValidationRule_Company 
                ON [config].[CompanyValidationRule](CompanyID) 
                WHERE IsEnabled = 1 AND IsDeleted = 0;
                
            CREATE INDEX IX_CompanyValidationRule_ValidationRule 
                ON [config].[CompanyValidationRule](ValidationRuleID) 
                WHERE IsEnabled = 1 AND IsDeleted = 0;
        END
    """)
    
    # ========================================
    # STEP 3: Add Countries (NZ, US, UK, CA)
    # ========================================
    
    op.execute("""
        -- New Zealand
        IF NOT EXISTS (SELECT 1 FROM [ref].[Country] WHERE CountryCode = 'NZ')
        BEGIN
            INSERT INTO [ref].[Country] (
                CountryCode, CountryName, PhonePrefix,
                CurrencyCode, CurrencySymbol, CurrencyName,
                TaxRate, TaxName, TaxInclusive, TaxNumberLabel,
                CompanyValidationProvider, AddressValidationProvider,
                IsActive, SortOrder
            )
            VALUES (
                'NZ', 'New Zealand', '+64',
                'NZD', '$', 'New Zealand Dollar',
                0.15, 'GST', 1, 'NZBN',
                NULL, NULL,
                1, 20
            );
        END
        
        -- United States
        IF NOT EXISTS (SELECT 1 FROM [ref].[Country] WHERE CountryCode = 'US')
        BEGIN
            INSERT INTO [ref].[Country] (
                CountryCode, CountryName, PhonePrefix,
                CurrencyCode, CurrencySymbol, CurrencyName,
                TaxRate, TaxName, TaxInclusive, TaxNumberLabel,
                CompanyValidationProvider, AddressValidationProvider,
                IsActive, SortOrder
            )
            VALUES (
                'US', 'United States', '+1',
                'USD', '$', 'United States Dollar',
                NULL, 'Sales Tax', 0, 'EIN',
                NULL, NULL,
                1, 30
            );
        END
        
        -- United Kingdom
        IF NOT EXISTS (SELECT 1 FROM [ref].[Country] WHERE CountryCode = 'GB')
        BEGIN
            INSERT INTO [ref].[Country] (
                CountryCode, CountryName, PhonePrefix,
                CurrencyCode, CurrencySymbol, CurrencyName,
                TaxRate, TaxName, TaxInclusive, TaxNumberLabel,
                CompanyValidationProvider, AddressValidationProvider,
                IsActive, SortOrder
            )
            VALUES (
                'GB', 'United Kingdom', '+44',
                'GBP', '£', 'Pound Sterling',
                0.20, 'VAT', 1, 'VAT Number',
                NULL, NULL,
                1, 40
            );
        END
        
        -- Canada
        IF NOT EXISTS (SELECT 1 FROM [ref].[Country] WHERE CountryCode = 'CA')
        BEGIN
            INSERT INTO [ref].[Country] (
                CountryCode, CountryName, PhonePrefix,
                CurrencyCode, CurrencySymbol, CurrencyName,
                TaxRate, TaxName, TaxInclusive, TaxNumberLabel,
                CompanyValidationProvider, AddressValidationProvider,
                IsActive, SortOrder
            )
            VALUES (
                'CA', 'Canada', '+1',
                'CAD', '$', 'Canadian Dollar',
                0.05, 'GST', 0, 'BN',
                NULL, NULL,
                1, 50
            );
        END
    """)
    
    # ========================================
    # STEP 4: Australian Phone Rules (Comprehensive)
    # ========================================
    
    # Mobile - Local format (04XX XXX XXX)
    op.execute("""
        UPDATE [config].[ValidationRule]
        SET 
            ValidationPattern = '^0[4-5]\\d{8}$',
            ValidationMessage = 'Mobile must be 04 or 05 followed by 8 digits (10 total)',
            MinLength = 10,
            MaxLength = 10,
            ExampleValue = '0412345678',
            SortOrder = 10,
            IsActive = 1,
            DisplayFormat = '04XX XXX XXX',
            DisplayExample = '0412 345 678',
            StripPrefix = 1,
            SpacingPattern = 'XXXX XXX XXX'
        WHERE RuleKey = 'PHONE_MOBILE_FORMAT'
    """)
    
    # Mobile - International format (+61 4XX XXX XXX)
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [config].[ValidationRule] WHERE RuleKey = 'PHONE_AU_MOBILE_INTL')
        BEGIN
            INSERT INTO [config].[ValidationRule] (
                RuleKey, RuleTypeID, CountryID, ValidationPattern, ValidationMessage, 
                Description, IsActive, SortOrder, MinLength, MaxLength, ExampleValue,
                DisplayFormat, DisplayExample, StripPrefix, SpacingPattern
            )
            VALUES (
                'PHONE_AU_MOBILE_INTL',
                (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='phone'),
                (SELECT CountryID FROM [ref].[Country] WHERE CountryCode='AU'),
                '^\\+61[4-5]\\d{8}$',
                'International mobile: +61 4 or 5 followed by 8 digits',
                'Australian mobile international format',
                1,
                11,
                12,
                12,
                '+61412345678',
                '04XX XXX XXX',
                '0412 345 678',
                1,
                'XXXX XXX XXX'
            )
        END
    """)
    
    # Landline - Local format (02/03/07/08 XXXX XXXX)
    op.execute("""
        UPDATE [config].[ValidationRule]
        SET 
            ValidationPattern = '^0[2-3,7-8]\\d{8}$',
            ValidationMessage = 'Landline must be 02, 03, 07, or 08 followed by 8 digits',
            MinLength = 10,
            MaxLength = 10,
            ExampleValue = '0298765432',
            SortOrder = 20,
            IsActive = 1,
            DisplayFormat = '0X XXXX XXXX',
            DisplayExample = '02 9876 5432',
            StripPrefix = 1,
            SpacingPattern = 'XX XXXX XXXX'
        WHERE RuleKey = 'PHONE_LANDLINE_FORMAT'
    """)
    
    # Landline - International format
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [config].[ValidationRule] WHERE RuleKey = 'PHONE_AU_LANDLINE_INTL')
        BEGIN
            INSERT INTO [config].[ValidationRule] (
                RuleKey, RuleTypeID, CountryID, ValidationPattern, ValidationMessage,
                Description, IsActive, SortOrder, MinLength, MaxLength, ExampleValue
            )
            VALUES (
                'PHONE_AU_LANDLINE_INTL',
                (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='phone'),
                (SELECT CountryID FROM [ref].[Country] WHERE CountryCode='AU'),
                '^\\+61[2-3,7-8]\\d{8}$',
                'International landline: +61 2, 3, 7, or 8 followed by 8 digits',
                'Australian landline international',
                1,
                21,
                12,
                12,
                '+61298765432'
            )
        END
    """)
    
    # Satellite phones (014X XXXXXX) - EventLeads accepts
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [config].[ValidationRule] WHERE RuleKey = 'PHONE_AU_SATELLITE')
        BEGIN
            INSERT INTO [config].[ValidationRule] (
                RuleKey, RuleTypeID, CountryID, ValidationPattern, ValidationMessage,
                Description, IsActive, SortOrder, MinLength, MaxLength, ExampleValue
            )
            VALUES (
                'PHONE_AU_SATELLITE',
                (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='phone'),
                (SELECT CountryID FROM [ref].[Country] WHERE CountryCode='AU'),
                '^014[0-9]\\d{6}$',
                'Satellite phone must start with 014 followed by 7 digits',
                'Australian satellite phones (Telstra/Optus)',
                1,
                25,
                10,
                10,
                '0147123456'
            )
        END
    """)
    
    # Location-independent (018X XXXXXX) - EventLeads accepts
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [config].[ValidationRule] WHERE RuleKey = 'PHONE_AU_LOCATION_INDEP')
        BEGIN
            INSERT INTO [config].[ValidationRule] (
                RuleKey, RuleTypeID, CountryID, ValidationPattern, ValidationMessage,
                Description, IsActive, SortOrder, MinLength, MaxLength, ExampleValue
            )
            VALUES (
                'PHONE_AU_LOCATION_INDEP',
                (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='phone'),
                (SELECT CountryID FROM [ref].[Country] WHERE CountryCode='AU'),
                '^018\\d{7}$',
                'Location-independent must start with 018 followed by 7 digits',
                'Australian location-independent numbers',
                1,
                26,
                10,
                10,
                '0181234567'
            )
        END
    """)
    
    # Toll-free (1800) - Disabled at country level (companies can enable)
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [config].[ValidationRule] WHERE RuleKey = 'PHONE_AU_TOLLFREE')
        BEGIN
            INSERT INTO [config].[ValidationRule] (
                RuleKey, RuleTypeID, CountryID, ValidationPattern, ValidationMessage,
                Description, IsActive, SortOrder, MinLength, MaxLength, ExampleValue
            )
            VALUES (
                'PHONE_AU_TOLLFREE',
                (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='phone'),
                (SELECT CountryID FROM [ref].[Country] WHERE CountryCode='AU'),
                '^1800\\d{6}$',
                'Toll-free (FreeCall) must be 1800 followed by 6 digits',
                'Australian toll-free numbers',
                0,  -- Disabled (EventLeads rejects)
                30,
                10,
                10,
                '1800123456'
            )
        END
    """)
    
    # Local rate (1300/13XX) - Disabled at country level
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [config].[ValidationRule] WHERE RuleKey = 'PHONE_AU_LOCALRATE')
        BEGIN
            INSERT INTO [config].[ValidationRule] (
                RuleKey, RuleTypeID, CountryID, ValidationPattern, ValidationMessage,
                Description, IsActive, SortOrder, MinLength, MaxLength, ExampleValue
            )
            VALUES (
                'PHONE_AU_LOCALRATE',
                (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='phone'),
                (SELECT CountryID FROM [ref].[Country] WHERE CountryCode='AU'),
                '^13(00|11|22|33)\\d{6}$',
                'Local rate must be 1300, 1311, 1322, or 1333 followed by 6 digits',
                'Australian local rate numbers',
                0,  -- Disabled (EventLeads rejects)
                31,
                10,
                10,
                '1300123456'
            )
        END
    """)
    
    # Premium rate (19XX) - Disabled at country level
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [config].[ValidationRule] WHERE RuleKey = 'PHONE_AU_PREMIUM')
        BEGIN
            INSERT INTO [config].[ValidationRule] (
                RuleKey, RuleTypeID, CountryID, ValidationPattern, ValidationMessage,
                Description, IsActive, SortOrder, MinLength, MaxLength, ExampleValue
            )
            VALUES (
                'PHONE_AU_PREMIUM',
                (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='phone'),
                (SELECT CountryID FROM [ref].[Country] WHERE CountryCode='AU'),
                '^19\\d{8}$',
                'Premium rate must start with 19 followed by 8 digits',
                'Australian premium rate numbers',
                0,  -- Disabled (EventLeads rejects)
                32,
                10,
                10,
                '1900123456'
            )
        END
    """)
    
    # ========================================
    # STEP 5: New Zealand Phone Rules
    # ========================================
    
    # NZ Mobile (021, 022, 027, 028, 029) - Vodafone, 2degrees, Spark
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [config].[ValidationRule] WHERE RuleKey = 'PHONE_NZ_MOBILE')
        BEGIN
            INSERT INTO [config].[ValidationRule] (
                RuleKey, RuleTypeID, CountryID, ValidationPattern, ValidationMessage,
                Description, IsActive, SortOrder, MinLength, MaxLength, ExampleValue
            )
            VALUES (
                'PHONE_NZ_MOBILE',
                (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='phone'),
                (SELECT CountryID FROM [ref].[Country] WHERE CountryCode='NZ'),
                '^0(21|22|27|28|29)\\d{6,8}$',
                'NZ mobile must start with 021, 022, 027, 028, or 029',
                'New Zealand mobile phones (Vodafone, 2degrees, Spark)',
                1,
                10,
                9,
                11,
                '0212345678'
            )
        END
    """)
    
    # NZ Landline - Geographic (03, 04, 06, 07, 09)
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [config].[ValidationRule] WHERE RuleKey = 'PHONE_NZ_LANDLINE')
        BEGIN
            INSERT INTO [config].[ValidationRule] (
                RuleKey, RuleTypeID, CountryID, ValidationPattern, ValidationMessage,
                Description, IsActive, SortOrder, MinLength, MaxLength, ExampleValue
            )
            VALUES (
                'PHONE_NZ_LANDLINE',
                (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='phone'),
                (SELECT CountryID FROM [ref].[Country] WHERE CountryCode='NZ'),
                '^0[3-4,6-7,9]\\d{7,8}$',
                'NZ landline must start with 03, 04, 06, 07, or 09',
                'New Zealand landlines (geographic)',
                1,
                20,
                8,
                10,
                '0312345678'
            )
        END
    """)
    
    # NZ Toll-free (0800, 0508)
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [config].[ValidationRule] WHERE RuleKey = 'PHONE_NZ_TOLLFREE')
        BEGIN
            INSERT INTO [config].[ValidationRule] (
                RuleKey, RuleTypeID, CountryID, ValidationPattern, ValidationMessage,
                Description, IsActive, SortOrder, MinLength, MaxLength, ExampleValue
            )
            VALUES (
                'PHONE_NZ_TOLLFREE',
                (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='phone'),
                (SELECT CountryID FROM [ref].[Country] WHERE CountryCode='NZ'),
                '^0(800|508)\\d{6,7}$',
                'NZ toll-free must be 0800 or 0508',
                'New Zealand toll-free numbers',
                0,  -- Disabled by default
                30,
                10,
                11,
                '0800123456'
            )
        END
    """)
    
    # NZ Postal Code
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [config].[ValidationRule] WHERE RuleKey = 'POSTAL_CODE_NZ')
        BEGIN
            INSERT INTO [config].[ValidationRule] (
                RuleKey, RuleTypeID, CountryID, ValidationPattern, ValidationMessage,
                Description, IsActive, SortOrder, MinLength, MaxLength, ExampleValue,
                DisplayFormat, DisplayExample, StripPrefix, SpacingPattern
            )
            VALUES (
                'POSTAL_CODE_NZ',
                (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='postal_code'),
                (SELECT CountryID FROM [ref].[Country] WHERE CountryCode='NZ'),
                '^\\d{4}$',
                'NZ postcode must be 4 digits',
                'New Zealand postal codes',
                1,
                10,
                4,
                4,
                '1010',
                'XXXX',
                '1010',
                0,
                'XXXX'
            )
        END
    """)
    
    # ========================================
    # STEP 6: USA Phone Rules (NANP)
    # ========================================
    
    # USA/Canada use North American Numbering Plan (NANP)
    # Format: +1 NXX NXX XXXX (N = 2-9, X = 0-9)
    
    # USA Local format (XXX) XXX-XXXX
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [config].[ValidationRule] WHERE RuleKey = 'PHONE_US_LOCAL')
        BEGIN
            INSERT INTO [config].[ValidationRule] (
                RuleKey, RuleTypeID, CountryID, ValidationPattern, ValidationMessage,
                Description, IsActive, SortOrder, MinLength, MaxLength, ExampleValue
            )
            VALUES (
                'PHONE_US_LOCAL',
                (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='phone'),
                (SELECT CountryID FROM [ref].[Country] WHERE CountryCode='US'),
                '^[2-9]\\d{2}[2-9]\\d{6}$',
                'US phone must be 10 digits: area code (2-9XX) + 7 digits',
                'USA local format (no +1 prefix)',
                1,
                10,
                10,
                10,
                '4155551234'
            )
        END
    """)
    
    # USA International format +1 XXX XXX XXXX
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [config].[ValidationRule] WHERE RuleKey = 'PHONE_US_INTL')
        BEGIN
            INSERT INTO [config].[ValidationRule] (
                RuleKey, RuleTypeID, CountryID, ValidationPattern, ValidationMessage,
                Description, IsActive, SortOrder, MinLength, MaxLength, ExampleValue
            )
            VALUES (
                'PHONE_US_INTL',
                (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='phone'),
                (SELECT CountryID FROM [ref].[Country] WHERE CountryCode='US'),
                '^\\+1[2-9]\\d{9}$',
                'International format: +1 followed by 10 digits',
                'USA international format',
                1,
                11,
                12,
                12,
                '+14155551234'
            )
        END
    """)
    
    # USA Toll-free (800, 888, 877, 866, 855, 844, 833)
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [config].[ValidationRule] WHERE RuleKey = 'PHONE_US_TOLLFREE')
        BEGIN
            INSERT INTO [config].[ValidationRule] (
                RuleKey, RuleTypeID, CountryID, ValidationPattern, ValidationMessage,
                Description, IsActive, SortOrder, MinLength, MaxLength, ExampleValue
            )
            VALUES (
                'PHONE_US_TOLLFREE',
                (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='phone'),
                (SELECT CountryID FROM [ref].[Country] WHERE CountryCode='US'),
                '^1(800|888|877|866|855|844|833)\\d{7}$',
                'Toll-free must be 1-800, 1-888, 1-877, 1-866, 1-855, 1-844, or 1-833',
                'USA toll-free numbers',
                0,  -- Disabled by default
                30,
                11,
                11,
                '18005551234'
            )
        END
    """)
    
    # USA Postal Code (ZIP)
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [config].[ValidationRule] WHERE RuleKey = 'POSTAL_CODE_US')
        BEGIN
            INSERT INTO [config].[ValidationRule] (
                RuleKey, RuleTypeID, CountryID, ValidationPattern, ValidationMessage,
                Description, IsActive, SortOrder, MinLength, MaxLength, ExampleValue,
                DisplayFormat, DisplayExample, StripPrefix, SpacingPattern
            )
            VALUES (
                'POSTAL_CODE_US',
                (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='postal_code'),
                (SELECT CountryID FROM [ref].[Country] WHERE CountryCode='US'),
                '^\\d{5}(-\\d{4})?$',
                'ZIP code must be 5 digits or 5+4 format',
                'USA ZIP codes',
                1,
                10,
                5,
                10,
                '94102',
                'XXXXX',
                '94102',
                0,
                'XXXXX'
            )
        END
    """)
    
    # ========================================
    # STEP 7: UK Phone Rules (Ofcom)
    # ========================================
    
    # UK Mobile (07XXX XXXXXX)
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [config].[ValidationRule] WHERE RuleKey = 'PHONE_UK_MOBILE')
        BEGIN
            INSERT INTO [config].[ValidationRule] (
                RuleKey, RuleTypeID, CountryID, ValidationPattern, ValidationMessage,
                Description, IsActive, SortOrder, MinLength, MaxLength, ExampleValue
            )
            VALUES (
                'PHONE_UK_MOBILE',
                (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='phone'),
                (SELECT CountryID FROM [ref].[Country] WHERE CountryCode='GB'),
                '^07\\d{9}$',
                'UK mobile must start with 07 followed by 9 digits (11 total)',
                'UK mobile phones (EE, Vodafone, O2, Three)',
                1,
                10,
                11,
                11,
                '07912345678'
            )
        END
    """)
    
    # UK Landline (01XXX/02X/03XX)
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [config].[ValidationRule] WHERE RuleKey = 'PHONE_UK_LANDLINE')
        BEGIN
            INSERT INTO [config].[ValidationRule] (
                RuleKey, RuleTypeID, CountryID, ValidationPattern, ValidationMessage,
                Description, IsActive, SortOrder, MinLength, MaxLength, ExampleValue
            )
            VALUES (
                'PHONE_UK_LANDLINE',
                (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='phone'),
                (SELECT CountryID FROM [ref].[Country] WHERE CountryCode='GB'),
                '^0[1-2]\\d{9}$',
                'UK landline must start with 01 or 02 followed by 9 digits',
                'UK geographic landlines',
                1,
                20,
                11,
                11,
                '02012345678'
            )
        END
    """)
    
    # UK Toll-free (0800)
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [config].[ValidationRule] WHERE RuleKey = 'PHONE_UK_TOLLFREE')
        BEGIN
            INSERT INTO [config].[ValidationRule] (
                RuleKey, RuleTypeID, CountryID, ValidationPattern, ValidationMessage,
                Description, IsActive, SortOrder, MinLength, MaxLength, ExampleValue
            )
            VALUES (
                'PHONE_UK_TOLLFREE',
                (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='phone'),
                (SELECT CountryID FROM [ref].[Country] WHERE CountryCode='GB'),
                '^0800\\d{6,7}$',
                'UK freephone must start with 0800',
                'UK freephone numbers',
                0,  -- Disabled by default
                30,
                10,
                11,
                '08001234567'
            )
        END
    """)
    
    # UK Postal Code
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [config].[ValidationRule] WHERE RuleKey = 'POSTAL_CODE_UK')
        BEGIN
            INSERT INTO [config].[ValidationRule] (
                RuleKey, RuleTypeID, CountryID, ValidationPattern, ValidationMessage,
                Description, IsActive, SortOrder, MinLength, MaxLength, ExampleValue,
                DisplayFormat, DisplayExample, StripPrefix, SpacingPattern
            )
            VALUES (
                'POSTAL_CODE_UK',
                (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='postal_code'),
                (SELECT CountryID FROM [ref].[Country] WHERE CountryCode='GB'),
                '^[A-Z]{1,2}\\d{1,2}[A-Z]?\\s?\\d[A-Z]{2}$',
                'UK postcode format: AA9A 9AA',
                'UK postal codes',
                1,
                10,
                5,
                8,
                'SW1A 1AA',
                'AA9A 9AA',
                'SW1A 1AA',
                0,
                'AA9A 9AA'
            )
        END
    """)
    
    # ========================================
    # STEP 8: Canada Phone Rules (Same as USA - NANP)
    # ========================================
    
    # Canada Local format (same as USA)
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [config].[ValidationRule] WHERE RuleKey = 'PHONE_CA_LOCAL')
        BEGIN
            INSERT INTO [config].[ValidationRule] (
                RuleKey, RuleTypeID, CountryID, ValidationPattern, ValidationMessage,
                Description, IsActive, SortOrder, MinLength, MaxLength, ExampleValue
            )
            VALUES (
                'PHONE_CA_LOCAL',
                (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='phone'),
                (SELECT CountryID FROM [ref].[Country] WHERE CountryCode='CA'),
                '^[2-9]\\d{2}[2-9]\\d{6}$',
                'Canadian phone must be 10 digits: area code (2-9XX) + 7 digits',
                'Canadian local format (no +1 prefix)',
                1,
                10,
                10,
                10,
                '4165551234'
            )
        END
    """)
    
    # Canada International format
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [config].[ValidationRule] WHERE RuleKey = 'PHONE_CA_INTL')
        BEGIN
            INSERT INTO [config].[ValidationRule] (
                RuleKey, RuleTypeID, CountryID, ValidationPattern, ValidationMessage,
                Description, IsActive, SortOrder, MinLength, MaxLength, ExampleValue
            )
            VALUES (
                'PHONE_CA_INTL',
                (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='phone'),
                (SELECT CountryID FROM [ref].[Country] WHERE CountryCode='CA'),
                '^\\+1[2-9]\\d{9}$',
                'International format: +1 followed by 10 digits',
                'Canadian international format',
                1,
                11,
                12,
                12,
                '+14165551234'
            )
        END
    """)
    
    # ========================================
    # STEP 9: EventLeads Company Seed Data
    # ========================================
    
    op.execute("""
        -- EventLeads company setup - handles both dev (existing data) and production (fresh DB)
        
        DECLARE @EventLeadsExists BIT = 0;
        DECLARE @CompanyIDOne BIT = 0;
        
        -- Check if EventLeads company already exists
        IF EXISTS (SELECT 1 FROM [dbo].[Company] WHERE CompanyName = 'EventLeads')
            SET @EventLeadsExists = 1;
        
        -- Check if CompanyID = 1 exists  
        IF EXISTS (SELECT 1 FROM [dbo].[Company] WHERE CompanyID = 1)
            SET @CompanyIDOne = 1;
        
        -- Scenario 1: Fresh production database - INSERT EventLeads as CompanyID = 1
        IF @EventLeadsExists = 0 AND @CompanyIDOne = 0
        BEGIN
            SET IDENTITY_INSERT [dbo].[Company] ON;
            
            INSERT INTO [dbo].[Company] (
                CompanyID,
                CompanyName,
                LegalEntityName,
                DisplayNameSource,
                ABN,
                GSTRegistered,
                Phone,
                Email,
                CountryID,
                ParentCompanyID,
                IsActive
            )
            VALUES (
                1,
                'EventLeads',
                'EventLeads Pty Ltd',
                'Legal',
                '00000000000',  -- Placeholder ABN
                0,
                NULL,
                'info@eventlead.com',
                (SELECT CountryID FROM [ref].[Country] WHERE CountryCode = 'AU'),
                NULL,
                1
            );
            
            SET IDENTITY_INSERT [dbo].[Company] OFF;
        END
        
        -- Scenario 2: Dev database with test data - UPDATE existing CompanyID = 1 to EventLeads
        IF @EventLeadsExists = 0 AND @CompanyIDOne = 1
        BEGIN
            UPDATE [dbo].[Company]
            SET 
                CompanyName = 'EventLeads',
                LegalEntityName = 'EventLeads Pty Ltd',
                UpdatedDate = GETUTCDATE()
            WHERE CompanyID = 1;
        END
        
        -- Scenario 3: EventLeads exists but not as CompanyID = 1 - Leave as-is
        -- (Admin can manually configure validation for the correct company)
    """)
    
    # ========================================
    # STEP 9: EventLeads Validation Configuration
    # ========================================
    
    op.execute("""
        -- Configure EventLeads phone validation rules
        -- ACCEPT: Mobile, Landline, Satellite, Location-independent
        -- REJECT: Toll-free, Local rate, Premium
        
        DECLARE @EventLeadsID BIGINT = 1;  -- EventLeads CompanyID
        
        -- Get rule IDs for Australian phone types
        DECLARE @MobileLoc BIGINT = (SELECT ValidationRuleID FROM [config].[ValidationRule] WHERE RuleKey = 'PHONE_MOBILE_FORMAT');
        DECLARE @MobileIntl BIGINT = (SELECT ValidationRuleID FROM [config].[ValidationRule] WHERE RuleKey = 'PHONE_AU_MOBILE_INTL');
        DECLARE @LandlineLoc BIGINT = (SELECT ValidationRuleID FROM [config].[ValidationRule] WHERE RuleKey = 'PHONE_LANDLINE_FORMAT');
        DECLARE @LandlineIntl BIGINT = (SELECT ValidationRuleID FROM [config].[ValidationRule] WHERE RuleKey = 'PHONE_AU_LANDLINE_INTL');
        DECLARE @Satellite BIGINT = (SELECT ValidationRuleID FROM [config].[ValidationRule] WHERE RuleKey = 'PHONE_AU_SATELLITE');
        DECLARE @LocationIndep BIGINT = (SELECT ValidationRuleID FROM [config].[ValidationRule] WHERE RuleKey = 'PHONE_AU_LOCATION_INDEP');
        
        -- Insert EventLeads configuration (only if rules found)
        IF @MobileLoc IS NOT NULL
        BEGIN
            INSERT INTO [config].[CompanyValidationRule] (CompanyID, ValidationRuleID, IsEnabled, SortOrderOverride)
            VALUES
                (@EventLeadsID, @MobileLoc, 1, 10),        -- Mobile local (highest priority)
                (@EventLeadsID, @MobileIntl, 1, 11),       -- Mobile international
                (@EventLeadsID, @LandlineLoc, 1, 20),      -- Landline local
                (@EventLeadsID, @LandlineIntl, 1, 21);     -- Landline international
                
            -- Add satellite and location-independent if they exist
            IF @Satellite IS NOT NULL
                INSERT INTO [config].[CompanyValidationRule] (CompanyID, ValidationRuleID, IsEnabled, SortOrderOverride)
                VALUES (@EventLeadsID, @Satellite, 1, 25);
                
            IF @LocationIndep IS NOT NULL
                INSERT INTO [config].[CompanyValidationRule] (CompanyID, ValidationRuleID, IsEnabled, SortOrderOverride)
                VALUES (@EventLeadsID, @LocationIndep, 1, 26);
        END
        
        -- NOTE: Toll-free, Local rate, and Premium are NOT inserted
        -- Therefore EventLeads rejects these number types
    """)
    
    # ========================================
    # STEP 10: Set Display Formats for All Phone Rules (All Countries)
    # ========================================
    
    # Batch update display formats for all phone rules
    # This ensures users see LOCAL formats, not international (+61, +64, etc.)
    op.execute("""
        -- Australia - All phone rules strip +61 prefix for display
        UPDATE [config].[ValidationRule]
        SET DisplayFormat = '04XX XXX XXX', DisplayExample = '0412 345 678', 
            StripPrefix = 1, SpacingPattern = 'XXXX XXX XXX'
        WHERE RuleKey IN ('PHONE_AU_MOBILE_INTL', 'PHONE_AU_MOBILE_INTL');
        
        UPDATE [config].[ValidationRule]
        SET DisplayFormat = '0X XXXX XXXX', DisplayExample = '02 9876 5432', 
            StripPrefix = 1, SpacingPattern = 'XX XXXX XXXX'
        WHERE RuleKey = 'PHONE_AU_LANDLINE_INTL';
        
        UPDATE [config].[ValidationRule]
        SET DisplayFormat = '014X XXXXXX', DisplayExample = '0147 123456', 
            StripPrefix = 1, SpacingPattern = 'XXXX XXXXXX'
        WHERE RuleKey = 'PHONE_AU_SATELLITE';
        
        UPDATE [config].[ValidationRule]
        SET DisplayFormat = '018X XXXXXX', DisplayExample = '0181 234567', 
            StripPrefix = 1, SpacingPattern = 'XXXX XXXXXX'
        WHERE RuleKey = 'PHONE_AU_LOCATION_INDEP';
        
        -- New Zealand - Strip +64 prefix
        UPDATE [config].[ValidationRule]
        SET DisplayFormat = '02X XXX XXXX', DisplayExample = '021 234 5678', 
            StripPrefix = 1, SpacingPattern = 'XXX XXX XXXX'
        WHERE RuleKey = 'PHONE_NZ_MOBILE';
        
        UPDATE [config].[ValidationRule]
        SET DisplayFormat = '0X XXX XXXX', DisplayExample = '03 123 4567', 
            StripPrefix = 1, SpacingPattern = 'XX XXX XXXX'
        WHERE RuleKey = 'PHONE_NZ_LANDLINE';
        
        -- USA - Strip +1 prefix
        UPDATE [config].[ValidationRule]
        SET DisplayFormat = '(XXX) XXX-XXXX', DisplayExample = '(415) 555-1234', 
            StripPrefix = 1, SpacingPattern = '(XXX) XXX-XXXX'
        WHERE RuleKey IN ('PHONE_US_LOCAL', 'PHONE_US_INTL');
        
        -- UK - NO prefix to strip (07 and 01/02 are local formats)
        UPDATE [config].[ValidationRule]
        SET DisplayFormat = '07XXX XXXXXX', DisplayExample = '07912 345678', 
            StripPrefix = 0, SpacingPattern = 'XXXXX XXXXXX'
        WHERE RuleKey = 'PHONE_UK_MOBILE';
        
        UPDATE [config].[ValidationRule]
        SET DisplayFormat = '0XX XXXX XXXX', DisplayExample = '020 1234 5678', 
            StripPrefix = 0, SpacingPattern = 'XXX XXXX XXXX'
        WHERE RuleKey = 'PHONE_UK_LANDLINE';
        
        -- Canada - Strip +1 prefix (same as USA)
        UPDATE [config].[ValidationRule]
        SET DisplayFormat = '(XXX) XXX-XXXX', DisplayExample = '(416) 555-1234', 
            StripPrefix = 1, SpacingPattern = '(XXX) XXX-XXXX'
        WHERE RuleKey IN ('PHONE_CA_LOCAL', 'PHONE_CA_INTL');
    """)


def downgrade() -> None:
    """Remove company validation architecture - CORRECT ORDER"""
    
    # STEP 1: Remove CompanyValidationRule records FIRST (before dropping table or company)
    op.execute("DELETE FROM [config].[CompanyValidationRule] WHERE CompanyID = 1")
    
    # STEP 2: Drop CompanyValidationRule table
    op.execute("DROP TABLE IF EXISTS [config].[CompanyValidationRule]")
    
    # STEP 3: NOW safe to delete EventLeads company (no FK references)
    op.execute("DELETE FROM [dbo].[Company] WHERE CompanyID = 1 AND CompanyName = 'EventLeads'")
    
    # STEP 4: Remove display format columns from ValidationRule
    op.execute("""
        ALTER TABLE [config].[ValidationRule] DROP CONSTRAINT IF EXISTS CK_ValidationRule_DisplayFormat;
        ALTER TABLE [config].[ValidationRule] DROP COLUMN IF EXISTS DisplayFormat;
        ALTER TABLE [config].[ValidationRule] DROP COLUMN IF EXISTS DisplayExample;
        ALTER TABLE [config].[ValidationRule] DROP COLUMN IF EXISTS StripPrefix;
        ALTER TABLE [config].[ValidationRule] DROP COLUMN IF EXISTS SpacingPattern;
        ALTER TABLE [config].[ValidationRule] DROP COLUMN IF EXISTS SortOrder;
    """)
    
    # STEP 5: Remove new validation rules (keep original mobile/landline)
    op.execute("""
        DELETE FROM [config].[ValidationRule] 
        WHERE RuleKey IN (
            'PHONE_AU_MOBILE_INTL', 'PHONE_AU_LANDLINE_INTL', 'PHONE_AU_SATELLITE',
            'PHONE_AU_LOCATION_INDEP', 'PHONE_AU_TOLLFREE', 'PHONE_AU_LOCALRATE', 'PHONE_AU_PREMIUM',
            'PHONE_NZ_MOBILE', 'PHONE_NZ_LANDLINE', 'PHONE_NZ_TOLLFREE',
            'PHONE_US_LOCAL', 'PHONE_US_INTL', 'PHONE_US_TOLLFREE',
            'PHONE_UK_MOBILE', 'PHONE_UK_LANDLINE', 'PHONE_UK_TOLLFREE',
            'PHONE_CA_LOCAL', 'PHONE_CA_INTL'
        )
    """)
    
    # STEP 6: Remove new countries
    op.execute("DELETE FROM [ref].[Country] WHERE CountryCode IN ('NZ', 'US', 'GB', 'CA')")

