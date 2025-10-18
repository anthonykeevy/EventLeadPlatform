"""Add MinLength, MaxLength, ExampleValue to ValidationRule table

Revision ID: 003
Revises: 002_epic1_complete_schema
Create Date: 2025-10-18 (Story 1.12 implementation)

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '003_validation_rule_enhancements'
down_revision = '002_epic1_complete_schema'
branch_labels = None
depends_on = None


def upgrade():
    """Add missing validation rule fields for Story 1.12"""
    
    # Add MinLength, MaxLength, ExampleValue columns to ValidationRule table
    op.add_column('ValidationRule', sa.Column('MinLength', sa.Integer(), nullable=True), schema='config')
    op.add_column('ValidationRule', sa.Column('MaxLength', sa.Integer(), nullable=True), schema='config')
    op.add_column('ValidationRule', sa.Column('ExampleValue', sa.String(100), nullable=True), schema='config')
    
    # Add check constraints for validation
    op.execute("""
        ALTER TABLE [config].[ValidationRule] 
        ADD CONSTRAINT CK_ValidationRule_MinLength 
        CHECK (MinLength IS NULL OR MinLength > 0)
    """)
    
    op.execute("""
        ALTER TABLE [config].[ValidationRule] 
        ADD CONSTRAINT CK_ValidationRule_MaxLength 
        CHECK (MaxLength IS NULL OR MaxLength > 0)
    """)
    
    op.execute("""
        ALTER TABLE [config].[ValidationRule] 
        ADD CONSTRAINT CK_ValidationRule_LengthRange 
        CHECK (MinLength IS NULL OR MaxLength IS NULL OR MinLength <= MaxLength)
    """)
    
    # Update existing Australia validation rules with new fields and international formats
    # Enhanced phone formats with international +61 prefix
    op.execute(r"""
        UPDATE [config].[ValidationRule] 
        SET ValidationPattern = '^\\+61[4-5][0-9]{8}$',
            ValidationMessage = 'Mobile phone must be +61 followed by 4 or 5 and 8 digits',
            MinLength = 12, MaxLength = 13, ExampleValue = '+61412345678'
        WHERE RuleKey = 'PHONE_MOBILE_FORMAT'
    """)
    
    op.execute(r"""
        UPDATE [config].[ValidationRule] 
        SET ValidationPattern = '^\\+61[2-8][0-9]{8}$',
            ValidationMessage = 'Landline must be +61 followed by area code (2-8) and 8 digits',
            MinLength = 12, MaxLength = 13, ExampleValue = '+61298765432'
        WHERE RuleKey = 'PHONE_LANDLINE_FORMAT'
    """)
    
    op.execute("""
        UPDATE [config].[ValidationRule] 
        SET MinLength = 4, MaxLength = 4, ExampleValue = '2000'
        WHERE RuleKey = 'POSTAL_CODE_FORMAT'
    """)
    
    # Enhanced ABN format with checksum requirement  
    op.execute("""
        UPDATE [config].[ValidationRule] 
        SET ValidationPattern = '^[0-9]{11}$',
            ValidationMessage = 'ABN must be 11 digits with valid checksum',
            MinLength = 11, MaxLength = 11, ExampleValue = '53004085616'
        WHERE RuleKey = 'TAX_ID_FORMAT' AND RuleTypeID = (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='tax_id')
    """)
    
    # Add ACN validation rule if not exists
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [config].[ValidationRule] WHERE RuleKey = 'ACN_FORMAT')
        BEGIN
            INSERT INTO [config].[ValidationRule] 
            (RuleKey, RuleTypeID, CountryID, ValidationPattern, ValidationMessage, Description, MinLength, MaxLength, ExampleValue, IsActive, Priority)
            VALUES 
            ('ACN_FORMAT', 
             (SELECT RuleTypeID FROM [ref].[RuleType] WHERE TypeCode='tax_id'), 
             (SELECT CountryID FROM [ref].[Country] WHERE CountryCode='AU'), 
             '^[0-9]{9}$', 
             'ACN must be 9 digits with valid checksum', 
             'Australian Company Number (ACN) format validation', 
             9, 9, '123456789', 1, 50)
        END
    """)


def downgrade():
    """Remove validation rule enhancements"""
    
    # Remove check constraints
    op.execute("ALTER TABLE [config].[ValidationRule] DROP CONSTRAINT CK_ValidationRule_MinLength")
    op.execute("ALTER TABLE [config].[ValidationRule] DROP CONSTRAINT CK_ValidationRule_MaxLength") 
    op.execute("ALTER TABLE [config].[ValidationRule] DROP CONSTRAINT CK_ValidationRule_LengthRange")
    
    # Remove columns
    op.drop_column('ValidationRule', 'MinLength', schema='config')
    op.drop_column('ValidationRule', 'MaxLength', schema='config')
    op.drop_column('ValidationRule', 'ExampleValue', schema='config')
