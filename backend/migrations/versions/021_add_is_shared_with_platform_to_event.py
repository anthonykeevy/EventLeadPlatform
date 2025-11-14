"""Add IsSharedWithPlatform field to Event table

Revision ID: 021_is_shared_with_platform
Revises: 020_public_review_status_ref
Create Date: 2025-01-XX 12:01:00.000000

Story: 2.6 - Admin Public Event Review Workflow
Purpose: Add IsSharedWithPlatform field to support "Company Network Only" vs "Share with Platform" visibility options
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '021_is_shared_with_platform'
down_revision = '020_public_review_status_ref'
branch_labels = None
depends_on = None


def upgrade():
    """Add IsSharedWithPlatform column to dbo.Event table"""
    
    # Add IsSharedWithPlatform column
    op.add_column(
        'Event',
        sa.Column('IsSharedWithPlatform', sa.Boolean(), nullable=False, server_default='0'),
        schema='dbo'
    )
    
    # Add column description (SQL Server extended property)
    op.execute("""
        EXEC sp_addextendedproperty 
            @name = N'MS_Description',
            @value = N'User''s choice to share event with platform-wide search (beyond company network). 0 = Company network only (no review needed), 1 = Share with platform (requires admin review)',
            @level0type = N'SCHEMA', @level0name = N'dbo',
            @level1type = N'TABLE', @level1name = N'Event',
            @level2type = N'COLUMN', @level2name = N'IsSharedWithPlatform';
    """)
    
    # Update existing events: If IsPublic = True and PublicReviewStatus is not NULL,
    # assume they want platform sharing (for backward compatibility)
    op.execute("""
        UPDATE [dbo].[Event]
        SET IsSharedWithPlatform = 1
        WHERE IsPublic = 1 
            AND (PublicReviewStatus IS NOT NULL OR IsPublicReviewRequired = 1);
    """)


def downgrade():
    """Remove IsSharedWithPlatform column from dbo.Event table"""
    
    # Drop extended property
    op.execute("""
        EXEC sp_dropextendedproperty 
            @name = N'MS_Description',
            @level0type = N'SCHEMA', @level0name = N'dbo',
            @level1type = N'TABLE', @level1name = N'Event',
            @level2type = N'COLUMN', @level2name = N'IsSharedWithPlatform';
    """)
    
    # Drop column
    op.drop_column('Event', 'IsSharedWithPlatform', schema='dbo')

