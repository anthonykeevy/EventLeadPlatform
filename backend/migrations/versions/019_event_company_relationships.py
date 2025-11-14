"""EventCompany Relationships - Track Company Participation in Events

Revision ID: 019_event_company_relationships
Revises: 018_logging_configuration
Create Date: 2025-01-15 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = '019_event_company_relationships'
down_revision = '018_logging_configuration'
branch_labels = None
depends_on = None


def upgrade():
    """Create EventCompany relationships and EventCompanyRole reference table"""
    
    # Create EventCompanyRole reference table
    op.create_table('EventCompanyRole',
        sa.Column('EventCompanyRoleID', sa.BigInteger(), nullable=False),
        sa.Column('RoleCode', mssql.NVARCHAR(length=50), nullable=False),
        sa.Column('RoleName', mssql.NVARCHAR(length=100), nullable=False),
        sa.Column('Description', mssql.NVARCHAR(length=500), nullable=False),
        sa.Column('RoleLevel', sa.Integer(), nullable=False),
        sa.Column('HasEditEvent', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('HasDeleteEvent', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('HasManageParticipants', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('HasViewEvent', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('IsActive', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('SortOrder', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=True),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(['CreatedBy'], ['dbo.User.UserID'], name='FK_EventCompanyRole_CreatedBy'),
        sa.ForeignKeyConstraint(['UpdatedBy'], ['dbo.User.UserID'], name='FK_EventCompanyRole_UpdatedBy'),
        sa.PrimaryKeyConstraint('EventCompanyRoleID', name='PK_EventCompanyRole'),
        sa.UniqueConstraint('RoleCode', name='UQ_EventCompanyRole_RoleCode'),
        schema='ref'
    )
    
    # Create EventCompany junction table
    op.create_table('EventCompany',
        sa.Column('EventCompanyID', sa.BigInteger(), nullable=False),
        sa.Column('EventID', sa.BigInteger(), nullable=False),
        sa.Column('CompanyID', sa.BigInteger(), nullable=False),
        sa.Column('EventCompanyRoleID', sa.BigInteger(), nullable=False),
        sa.Column('FormsCreated', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('FirstUsedDate', sa.DateTime(), nullable=True),
        sa.Column('LastUsedDate', sa.DateTime(), nullable=True),
        sa.Column('IsActive', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('DisassociatedDate', sa.DateTime(), nullable=True),
        sa.Column('DisassociatedBy', sa.BigInteger(), nullable=True),
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(['EventID'], ['dbo.Event.EventID'], name='FK_EventCompany_Event'),
        sa.ForeignKeyConstraint(['CompanyID'], ['dbo.Company.CompanyID'], name='FK_EventCompany_Company'),
        sa.ForeignKeyConstraint(['EventCompanyRoleID'], ['ref.EventCompanyRole.EventCompanyRoleID'], name='FK_EventCompany_EventCompanyRole'),
        sa.ForeignKeyConstraint(['CreatedBy'], ['dbo.User.UserID'], name='FK_EventCompany_CreatedBy'),
        sa.ForeignKeyConstraint(['UpdatedBy'], ['dbo.User.UserID'], name='FK_EventCompany_UpdatedBy'),
        sa.ForeignKeyConstraint(['DisassociatedBy'], ['dbo.User.UserID'], name='FK_EventCompany_DisassociatedBy'),
        sa.ForeignKeyConstraint(['DeletedBy'], ['dbo.User.UserID'], name='FK_EventCompany_DeletedBy'),
        sa.PrimaryKeyConstraint('EventCompanyID', name='PK_EventCompany'),
        schema='dbo'
    )
    
    # Create unique constraint for active EventCompany relationships
    # Only one active relationship per Event+Company combination
    op.execute("""
        CREATE UNIQUE NONCLUSTERED INDEX UQ_EventCompany_Event_Company_Active
        ON dbo.EventCompany (EventID, CompanyID, IsActive)
        WHERE IsActive = 1
    """)
    
    # Create indexes for EventCompany table
    op.create_index('IX_EventCompany_Event', 'EventCompany', ['EventID', 'IsActive', 'IsDeleted'], schema='dbo')
    op.create_index('IX_EventCompany_Company', 'EventCompany', ['CompanyID', 'IsActive', 'IsDeleted'], schema='dbo')
    op.create_index('IX_EventCompany_EventCompanyRole', 'EventCompany', ['EventCompanyRoleID', 'IsActive'], schema='dbo')
    op.create_index('IX_EventCompany_Active', 'EventCompany', ['IsActive', 'IsDeleted'], schema='dbo')
    
    # Seed reference data for EventCompanyRole
    op.execute("""
        INSERT INTO ref.EventCompanyRole (
            RoleCode, 
            RoleName, 
            Description, 
            RoleLevel, 
            HasEditEvent, 
            HasDeleteEvent, 
            HasManageParticipants, 
            HasViewEvent, 
            IsActive, 
            SortOrder, 
            CreatedBy
        ) VALUES
        ('event_owner', 'Event Owner', 'Company that created the event. Full control over event details, can edit all fields, delete event, and manage participants.', 100, 1, 1, 1, 1, 1, 1, 1),
        ('event_organizer', 'Event Organizer', 'Company organizing the event (if different from owner). Can edit extended fields (description, tags, organizer details), cannot edit core fields (name, dates, location) unless granted, cannot delete event.', 50, 1, 0, 0, 1, 1, 2, 1),
        ('event_participant', 'Event Participant', 'Company using public event for forms. Read-only access (can view event details), can disassociate from event, cannot edit event.', 10, 0, 0, 0, 1, 1, 3, 1)
    """)


def downgrade():
    """Rollback EventCompany relationships changes"""
    
    # Drop indexes
    op.drop_index('IX_EventCompany_Active', 'EventCompany', schema='dbo')
    op.drop_index('IX_EventCompany_EventCompanyRole', 'EventCompany', schema='dbo')
    op.drop_index('IX_EventCompany_Company', 'EventCompany', schema='dbo')
    op.drop_index('IX_EventCompany_Event', 'EventCompany', schema='dbo')
    
    # Drop unique constraint
    op.execute("DROP INDEX UQ_EventCompany_Event_Company_Active ON dbo.EventCompany")
    
    # Drop tables
    op.drop_table('EventCompany', schema='dbo')
    op.drop_table('EventCompanyRole', schema='ref')

