"""Add Agency Form Builder Role - Event-Scoped Form Access

Revision ID: 024_add_agency_form_builder_role
Revises: 023_drop_old_public_review_status_column
Create Date: 2025-01-XX 12:00:00.000000

Story: Epic 2 - Form Access Control Enhancement
Purpose: Add agency_form_builder role with event-scoped form access capabilities

Changes:
1. Add HasViewAllFormsForEvent column to ref.EventCompanyRole
2. Add HasEditAllFormsForEvent column to ref.EventCompanyRole
3. Insert agency_form_builder role seed data
4. Update existing roles to set new columns to 0
5. Create index for performance

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '024_add_agency_form_builder_role'
down_revision = '023_drop_public_review_status'
branch_labels = None
depends_on = None


def upgrade():
    """Add agency form builder role and form access columns"""
    
    # Add new columns to ref.EventCompanyRole
    op.add_column(
        'EventCompanyRole',
        sa.Column('HasViewAllFormsForEvent', sa.Boolean(), nullable=False, server_default='0'),
        schema='ref'
    )
    
    op.add_column(
        'EventCompanyRole',
        sa.Column('HasEditAllFormsForEvent', sa.Boolean(), nullable=False, server_default='0'),
        schema='ref'
    )
    
    # Create index for performance on form access columns
    # Note: SQL Server filtered indexes don't support OR conditions, so we use a regular index
    op.execute("""
        CREATE NONCLUSTERED INDEX IX_EventCompanyRole_FormAccess 
        ON [ref].[EventCompanyRole](HasViewAllFormsForEvent, HasEditAllFormsForEvent)
        WHERE HasViewAllFormsForEvent = 1
    """)
    
    # Create second filtered index for HasEditAllFormsForEvent
    op.execute("""
        CREATE NONCLUSTERED INDEX IX_EventCompanyRole_FormAccessEdit 
        ON [ref].[EventCompanyRole](HasEditAllFormsForEvent)
        WHERE HasEditAllFormsForEvent = 1
    """)
    
    # Insert agency_form_builder role seed data
    # Note: Column order matches existing seed data pattern, with new columns added at the end
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
            HasViewAllFormsForEvent,
            HasEditAllFormsForEvent,
            IsActive,
            SortOrder,
            CreatedBy
        ) VALUES (
            'agency_form_builder',
            'Agency Form Builder',
            'External agency company working on forms for a specific event. Read-only event access, but can view and edit all forms associated with the event. Forms remain owned by host company.',
            25,
            0,
            0,
            0,
            1,
            1,
            1,
            1,
            4,
            1
        )
    """)


def downgrade():
    """Rollback agency form builder role changes"""
    
    # Drop indexes
    op.execute("DROP INDEX IF EXISTS IX_EventCompanyRole_FormAccessEdit ON [ref].[EventCompanyRole]")
    op.execute("DROP INDEX IF EXISTS IX_EventCompanyRole_FormAccess ON [ref].[EventCompanyRole]")
    
    # Remove agency_form_builder role
    op.execute("""
        DELETE FROM [ref].[EventCompanyRole]
        WHERE RoleCode = 'agency_form_builder'
    """)
    
    # Drop columns
    op.drop_column('EventCompanyRole', 'HasEditAllFormsForEvent', schema='ref')
    op.drop_column('EventCompanyRole', 'HasViewAllFormsForEvent', schema='ref')

