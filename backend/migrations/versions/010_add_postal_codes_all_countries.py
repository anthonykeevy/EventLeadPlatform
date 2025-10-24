"""Add postal code validation rules for all countries - Story 1.20

Adds postal code validation for NZ, US, UK, CA to complete international support.

Revision ID: 010
Revises: 009
Create Date: 2025-10-23

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '010'
down_revision = '009'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Add postal code validation rules for all 5 countries.
    Story 1.20: Complete international postal code support.
    """
    
    # ========================================
    # New Zealand Postal Code
    # ========================================
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
    # USA Postal Code (ZIP)
    # ========================================
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
    # UK Postal Code
    # ========================================
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
    # Canada Postal Code
    # ========================================
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [config].[ValidationRule] WHERE RuleKey = 'POSTAL_CODE_CA')
        BEGIN
            INSERT INTO [config].[ValidationRule] (
                RuleKey, RuleTypeID, CountryID, ValidationPattern, ValidationMessage,
                Description, IsActive, SortOrder, MinLength, MaxLength, ExampleValue,
                DisplayFormat, DisplayExample, StripPrefix, SpacingPattern
            )
            VALUES (
                'POSTAL_CODE_CA',
                (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='postal_code'),
                (SELECT CountryID FROM [ref].[Country] WHERE CountryCode='CA'),
                '^[A-Z]\\d[A-Z]\\s?\\d[A-Z]\\d$',
                'Canadian postal code format: A9A 9A9',
                'Canadian postal codes',
                1,
                10,
                6,
                7,
                'M5H 2N2',
                'A9A 9A9',
                'M5H 2N2',
                0,
                'A9A 9A9'
            )
        END
    """)


def downgrade() -> None:
    """Remove postal code rules"""
    op.execute("""
        DELETE FROM [config].[ValidationRule]
        WHERE RuleKey IN ('POSTAL_CODE_NZ', 'POSTAL_CODE_US', 'POSTAL_CODE_UK', 'POSTAL_CODE_CA')
    """)

