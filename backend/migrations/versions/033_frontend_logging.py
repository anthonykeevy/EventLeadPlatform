"""Frontend Logging - Builder Events Integration

Revision ID: 033
Revises: 032_form_public_link_tokens
Create Date: 2025-12-21 15:00:00.000000

Creates log.FrontendEvent table for storing frontend builder events
(SmartBorder, drag, resize, collision detection, etc.) for unified
debugging through enhanced_diagnostic_logs.py.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = '033'
down_revision = '032_form_public_link_tokens'
branch_labels = None
depends_on = None


def upgrade():
    """Create FrontendEvent table for frontend logging integration"""
    
    # Create FrontendEvent table
    op.create_table('FrontendEvent',
        sa.Column('FrontendEventID', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('EventType', mssql.NVARCHAR(length=200), nullable=False),
        sa.Column('Level', mssql.NVARCHAR(length=20), nullable=False),
        sa.Column('ComponentID', mssql.NVARCHAR(length=100), nullable=True),
        sa.Column('ComponentType', mssql.NVARCHAR(length=100), nullable=True),
        sa.Column('Payload', mssql.NVARCHAR(length='MAX'), nullable=True),
        sa.Column('SessionID', mssql.NVARCHAR(length=100), nullable=True),
        sa.Column('UserID', sa.BigInteger(), nullable=True),
        sa.Column('RequestID', mssql.NVARCHAR(length=100), nullable=True),
        sa.Column('BrowserInfo', mssql.NVARCHAR(length=500), nullable=True),
        sa.Column('PageURL', mssql.NVARCHAR(length=1000), nullable=True),
        sa.Column('ClientTimestamp', sa.BigInteger(), nullable=True),
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.ForeignKeyConstraint(['UserID'], ['dbo.User.UserID'], name='FK_FrontendEvent_User_UserID'),
        sa.PrimaryKeyConstraint('FrontendEventID', name='PK_FrontendEvent'),
        schema='log'
    )
    
    # Create indexes for common query patterns
    op.create_index('IX_FrontendEvent_EventType', 'FrontendEvent', ['EventType'], schema='log')
    op.create_index('IX_FrontendEvent_Level', 'FrontendEvent', ['Level'], schema='log')
    op.create_index('IX_FrontendEvent_ComponentID', 'FrontendEvent', ['ComponentID'], schema='log')
    op.create_index('IX_FrontendEvent_ComponentType', 'FrontendEvent', ['ComponentType'], schema='log')
    op.create_index('IX_FrontendEvent_SessionID', 'FrontendEvent', ['SessionID'], schema='log')
    op.create_index('IX_FrontendEvent_CreatedDate', 'FrontendEvent', ['CreatedDate'], schema='log')


def downgrade():
    """Remove FrontendEvent table"""
    op.drop_index('IX_FrontendEvent_CreatedDate', table_name='FrontendEvent', schema='log')
    op.drop_index('IX_FrontendEvent_SessionID', table_name='FrontendEvent', schema='log')
    op.drop_index('IX_FrontendEvent_ComponentType', table_name='FrontendEvent', schema='log')
    op.drop_index('IX_FrontendEvent_ComponentID', table_name='FrontendEvent', schema='log')
    op.drop_index('IX_FrontendEvent_Level', table_name='FrontendEvent', schema='log')
    op.drop_index('IX_FrontendEvent_EventType', table_name='FrontendEvent', schema='log')
    op.drop_table('FrontendEvent', schema='log')











