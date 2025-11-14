"""Drop old PublicReviewStatus VARCHAR column

Revision ID: 023_drop_public_review_status
Revises: 022_public_review_status_fk
Create Date: 2025-01-XX 12:03:00.000000

Story: 2.6 - Admin Public Event Review Workflow
Purpose: Remove old PublicReviewStatus VARCHAR(20) column after successful migration to FK

IMPORTANT: Only run this migration after verifying that:
1. All data has been successfully migrated from PublicReviewStatus to PublicReviewStatusID
2. Application code has been updated to use PublicReviewStatusID
3. No queries still reference the old PublicReviewStatus column
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '023_drop_public_review_status'
down_revision = '022_public_review_status_fk'
branch_labels = None
depends_on = None


def upgrade():
    """Drop old PublicReviewStatus VARCHAR column"""
    
    # Verify migration was successful before dropping
    op.execute("""
        -- Validation: Check if any records have PublicReviewStatus but no PublicReviewStatusID
        DECLARE @UnmigratedCount INT;
        SELECT @UnmigratedCount = COUNT(*)
        FROM [dbo].[Event]
        WHERE PublicReviewStatus IS NOT NULL 
            AND PublicReviewStatusID IS NULL;
        
        IF @UnmigratedCount > 0
        BEGIN
            RAISERROR('Migration validation failed: %d records have PublicReviewStatus but no PublicReviewStatusID. Cannot drop column.', 16, 1, @UnmigratedCount);
        END
    """)
    
    # Drop the old VARCHAR column
    op.drop_column('Event', 'PublicReviewStatus', schema='dbo')


def downgrade():
    """Recreate PublicReviewStatus VARCHAR column (for rollback)"""
    
    # Re-add the column
    op.add_column(
        'Event',
        sa.Column('PublicReviewStatus', sa.NVARCHAR(20), nullable=True),
        schema='dbo'
    )
    
    # Migrate data back from FK to VARCHAR
    op.execute("""
        UPDATE e
        SET e.PublicReviewStatus = prs.StatusCode
        FROM [dbo].[Event] e
        INNER JOIN [ref].[PublicReviewStatus] prs 
            ON e.PublicReviewStatusID = prs.PublicReviewStatusID
        WHERE e.PublicReviewStatusID IS NOT NULL;
    """)
    
    # Recreate CHECK constraint
    op.create_check_constraint(
        'CK_Event_PublicReviewStatus',
        'Event',
        "PublicReviewStatus IS NULL OR PublicReviewStatus IN ('PENDING', 'APPROVED', 'REJECTED')",
        schema='dbo'
    )

