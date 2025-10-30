"""Logging Configuration Settings - Epic 2 Enhanced Logging

Revision ID: 018_logging_configuration
Revises: 017
Create Date: 2025-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = '018_logging_configuration'
down_revision = '017'
branch_labels = None
depends_on = None


def upgrade():
    """Add logging configuration settings to config.AppSetting"""
    
    # First, add 'logging' category to ref.SettingCategory if it doesn't exist
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [ref].[SettingCategory] WHERE CategoryCode = 'logging')
        BEGIN
            INSERT INTO [ref].[SettingCategory] (CategoryCode, CategoryName, Description, IsActive, SortOrder)
            VALUES ('logging', 'Logging', 'Enhanced logging and diagnostic configuration settings', 1, 50);
        END
    """)
    
    # Add logging configuration settings
    op.execute("""
        INSERT INTO [config].[AppSetting] (
            SettingKey, 
            SettingValue, 
            Description, 
            DefaultValue, 
            SettingCategoryID, 
            SettingTypeID, 
            IsEditable, 
            ValidationRegex, 
            MinValue, 
            MaxValue, 
            IsActive, 
            SortOrder
        )
        SELECT 
            'logging.capture_payloads',
            'false',
            'Enable request/response payload logging for enhanced diagnostics',
            'false',
            (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode = 'logging'),
            (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode = 'boolean'),
            1,
            '^(true|false)$',
            NULL,
            NULL,
            1,
            10
        WHERE NOT EXISTS (SELECT 1 FROM [config].[AppSetting] WHERE SettingKey = 'logging.capture_payloads');
    """)
    
    op.execute("""
        INSERT INTO [config].[AppSetting] (
            SettingKey, 
            SettingValue, 
            Description, 
            DefaultValue, 
            SettingCategoryID, 
            SettingTypeID, 
            IsEditable, 
            ValidationRegex, 
            MinValue, 
            MaxValue, 
            IsActive, 
            SortOrder
        )
        SELECT 
            'logging.max_payload_size_kb',
            '10',
            'Maximum payload size to log in KB (larger payloads will be truncated)',
            '10',
            (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode = 'logging'),
            (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode = 'integer'),
            1,
            '^[0-9]+$',
            1,
            1024,
            1,
            20
        WHERE NOT EXISTS (SELECT 1 FROM [config].[AppSetting] WHERE SettingKey = 'logging.max_payload_size_kb');
    """)
    
    op.execute("""
        INSERT INTO [config].[AppSetting] (
            SettingKey, 
            SettingValue, 
            Description, 
            DefaultValue, 
            SettingCategoryID, 
            SettingTypeID, 
            IsEditable, 
            ValidationRegex, 
            MinValue, 
            MaxValue, 
            IsActive, 
            SortOrder
        )
        SELECT 
            'logging.excluded_endpoints',
            '["/api/health", "/api/test-database"]',
            'Endpoints to exclude from payload logging (JSON array of paths)',
            '["/api/health"]',
            (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode = 'logging'),
            (SELECT SettingTypeID FROM [ref].[SettingType] WHERE TypeCode = 'string'),
            1,
            '^\\[.*\\]$',
            NULL,
            NULL,
            1,
            30
        WHERE NOT EXISTS (SELECT 1 FROM [config].[AppSetting] WHERE SettingKey = 'logging.excluded_endpoints');
    """)


def downgrade():
    """Remove logging configuration settings"""
    
    # Remove logging settings
    op.execute("""
        DELETE FROM [config].[AppSetting] 
        WHERE SettingKey IN (
            'logging.capture_payloads',
            'logging.max_payload_size_kb', 
            'logging.excluded_endpoints'
        );
    """)
    
    # Remove logging category (only if no other settings use it)
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [config].[AppSetting] WHERE SettingCategoryID = (SELECT SettingCategoryID FROM [ref].[SettingCategory] WHERE CategoryCode = 'logging'))
        BEGIN
            DELETE FROM [ref].[SettingCategory] WHERE CategoryCode = 'logging';
        END
    """)
