"""Enhanced Logging System - Epic 2 Foundation

Revision ID: 017
Revises: 016_forms_epic2
Create Date: 2025-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = '017'
down_revision = '016_forms_epic2'
branch_labels = None
depends_on = None


def upgrade():
    """Enhance existing logging tables and create new Epic 2 logging tables"""
    
    # Enhance existing ApiRequest table (only add columns that don't exist)
    op.add_column('ApiRequest', sa.Column('RequestPayload', mssql.NVARCHAR(length='MAX'), nullable=True), schema='log')
    op.add_column('ApiRequest', sa.Column('ResponsePayload', mssql.NVARCHAR(length='MAX'), nullable=True), schema='log')
    op.add_column('ApiRequest', sa.Column('Headers', mssql.NVARCHAR(length='MAX'), nullable=True), schema='log')
    # QueryParams already exists in Epic 1 - skip
    
    # Enhance existing ApplicationError table (only add columns that don't exist)
    # StackTrace already exists in Epic 1 - skip
    op.add_column('ApplicationError', sa.Column('ExceptionType', mssql.NVARCHAR(length=100), nullable=True), schema='log')
    
    # Enhance existing AuthEvent table (only add columns that don't exist)
    # UserAgent already exists in Epic 1 - skip
    op.add_column('AuthEvent', sa.Column('SessionID', mssql.NVARCHAR(length=100), nullable=True), schema='log')
    
    # Enhance existing EmailDelivery table (add missing columns)
    op.add_column('EmailDelivery', sa.Column('ProviderResponse', mssql.NVARCHAR(length='MAX'), nullable=True), schema='log')
    op.add_column('EmailDelivery', sa.Column('RetryCount', sa.Integer(), nullable=False, server_default='0'), schema='log')
    
    # Create new UserAction logging table
    op.create_table('UserAction',
        sa.Column('UserActionID', sa.BigInteger(), nullable=False),
        sa.Column('UserID', sa.BigInteger(), nullable=False),
        sa.Column('Action', mssql.NVARCHAR(length=100), nullable=False),
        sa.Column('Details', mssql.NVARCHAR(length='MAX'), nullable=True),
        sa.Column('Path', mssql.NVARCHAR(length=500), nullable=True),
        sa.Column('RequestID', mssql.NVARCHAR(length=100), nullable=True),
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.ForeignKeyConstraint(['UserID'], ['dbo.User.UserID'], name='FK_UserAction_User_UserID'),
        sa.PrimaryKeyConstraint('UserActionID', name='PK_UserAction'),
        schema='log'
    )
    
    # Create new PerformanceMetric logging table
    op.create_table('PerformanceMetric',
        sa.Column('PerformanceMetricID', sa.BigInteger(), nullable=False),
        sa.Column('MetricType', mssql.NVARCHAR(length=50), nullable=False),
        sa.Column('Endpoint', mssql.NVARCHAR(length=500), nullable=True),
        sa.Column('Value', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('StatusCode', sa.Integer(), nullable=True),
        sa.Column('UserID', sa.BigInteger(), nullable=True),
        sa.Column('Details', mssql.NVARCHAR(length='MAX'), nullable=True),
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.ForeignKeyConstraint(['UserID'], ['dbo.User.UserID'], name='FK_PerformanceMetric_User_UserID'),
        sa.PrimaryKeyConstraint('PerformanceMetricID', name='PK_PerformanceMetric'),
        schema='log'
    )
    
    # Create new IntegrationEvent logging table
    op.create_table('IntegrationEvent',
        sa.Column('IntegrationEventID', sa.BigInteger(), nullable=False),
        sa.Column('EventType', mssql.NVARCHAR(length=100), nullable=False),
        sa.Column('SourceDomain', mssql.NVARCHAR(length=50), nullable=False),
        sa.Column('TargetDomain', mssql.NVARCHAR(length=50), nullable=False),
        sa.Column('EntityID', sa.BigInteger(), nullable=True),
        sa.Column('Details', mssql.NVARCHAR(length='MAX'), nullable=True),
        sa.Column('UserID', sa.BigInteger(), nullable=True),
        sa.Column('RequestID', mssql.NVARCHAR(length=100), nullable=True),
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.ForeignKeyConstraint(['UserID'], ['dbo.User.UserID'], name='FK_IntegrationEvent_User_UserID'),
        sa.PrimaryKeyConstraint('IntegrationEventID', name='PK_IntegrationEvent'),
        schema='log'
    )
    
    # Create indexes for performance
    op.create_index('IX_UserAction_UserID_CreatedDate', 'UserAction', ['UserID', 'CreatedDate'], schema='log')
    op.create_index('IX_UserAction_Action_CreatedDate', 'UserAction', ['Action', 'CreatedDate'], schema='log')
    op.create_index('IX_PerformanceMetric_MetricType_CreatedDate', 'PerformanceMetric', ['MetricType', 'CreatedDate'], schema='log')
    op.create_index('IX_PerformanceMetric_Value_CreatedDate', 'PerformanceMetric', ['Value', 'CreatedDate'], schema='log')
    op.create_index('IX_IntegrationEvent_EventType_CreatedDate', 'IntegrationEvent', ['EventType', 'CreatedDate'], schema='log')
    op.create_index('IX_IntegrationEvent_SourceDomain_CreatedDate', 'IntegrationEvent', ['SourceDomain', 'CreatedDate'], schema='log')
    
    # Create indexes for enhanced existing tables (only for newly added columns)
    # RequestPayload is NVARCHAR(MAX) - cannot be indexed in SQL Server
    # StackTrace index already exists in Epic 1 - skip


def downgrade():
    """Rollback enhanced logging system changes"""
    
    # Drop indexes
    op.drop_index('IX_IntegrationEvent_SourceDomain_CreatedDate', 'IntegrationEvent', schema='log')
    op.drop_index('IX_IntegrationEvent_EventType_CreatedDate', 'IntegrationEvent', schema='log')
    op.drop_index('IX_PerformanceMetric_Value_CreatedDate', 'PerformanceMetric', schema='log')
    op.drop_index('IX_PerformanceMetric_MetricType_CreatedDate', 'PerformanceMetric', schema='log')
    op.drop_index('IX_UserAction_Action_CreatedDate', 'UserAction', schema='log')
    op.drop_index('IX_UserAction_UserID_CreatedDate', 'UserAction', schema='log')
    # RequestPayload index was not created (NVARCHAR(MAX) cannot be indexed)
    # StackTrace index already existed in Epic 1 - don't drop
    
    # Drop new tables
    op.drop_table('IntegrationEvent', schema='log')
    op.drop_table('PerformanceMetric', schema='log')
    op.drop_table('UserAction', schema='log')
    
    # Remove enhanced columns from existing tables (only columns that were added)
    op.drop_column('EmailDelivery', 'RetryCount', schema='log')
    op.drop_column('EmailDelivery', 'ProviderResponse', schema='log')
    op.drop_column('AuthEvent', 'SessionID', schema='log')
    op.drop_column('ApplicationError', 'ExceptionType', schema='log')
    op.drop_column('ApiRequest', 'Headers', schema='log')
    op.drop_column('ApiRequest', 'ResponsePayload', schema='log')
    op.drop_column('ApiRequest', 'RequestPayload', schema='log')
    # QueryParams, UserAgent, StackTrace already existed in Epic 1 - don't drop
