"""Migrate PublicReviewStatus from VARCHAR to Foreign Key

Revision ID: 022_public_review_status_fk
Revises: 021_is_shared_with_platform
Create Date: 2025-01-XX 12:02:00.000000

Story: 2.6 - Admin Public Event Review Workflow
Purpose: Convert PublicReviewStatus VARCHAR(20) to PublicReviewStatusID BIGINT FK to ref.PublicReviewStatus

IMPORTANT: This migration performs data migration from VARCHAR to FK.
The old PublicReviewStatus column will be dropped in a subsequent migration
after verifying data migration was successful.
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '022_public_review_status_fk'
down_revision = '021_is_shared_with_platform'
branch_labels = None
depends_on = None


def upgrade():
    """Migrate PublicReviewStatus VARCHAR to PublicReviewStatusID FK"""
    
    # =====================================================================
    # STEP 1: Add new PublicReviewStatusID column (nullable initially)
    # =====================================================================
    op.add_column(
        'Event',
        sa.Column('PublicReviewStatusID', sa.BigInteger(), nullable=True),
        schema='dbo'
    )
    
    # =====================================================================
    # STEP 2: Migrate existing data from VARCHAR to FK
    # =====================================================================
    # Map existing PublicReviewStatus values to new PublicReviewStatusID
    op.execute("""
        UPDATE e
        SET e.PublicReviewStatusID = prs.PublicReviewStatusID
        FROM [dbo].[Event] e
        INNER JOIN [ref].[PublicReviewStatus] prs 
            ON e.PublicReviewStatus = prs.StatusCode
        WHERE e.PublicReviewStatus IS NOT NULL;
    """)
    
    # =====================================================================
    # STEP 3: Add foreign key constraint
    # =====================================================================
    op.create_foreign_key(
        'FK_Event_PublicReviewStatus',
        'Event',
        'PublicReviewStatus',
        ['PublicReviewStatusID'],
        ['PublicReviewStatusID'],
        source_schema='dbo',
        referent_schema='ref'
    )
    
    # =====================================================================
    # STEP 4: Create index for performance
    # =====================================================================
    op.create_index(
        'IX_Event_PublicReviewStatus',
        'Event',
        ['PublicReviewStatusID', 'IsDeleted'],
        schema='dbo'
    )
    
    # =====================================================================
    # STEP 5: Update existing index to include PublicReviewStatusID
    # =====================================================================
    # Drop old index if it exists
    op.execute("""
        IF EXISTS (SELECT 1 FROM sys.indexes 
                   WHERE name = 'IX_Event_PublicReview' 
                   AND object_id = OBJECT_ID('dbo.Event'))
        BEGIN
            DROP INDEX IX_Event_PublicReview ON [dbo].[Event];
        END
    """)
    
    # Create new composite index for review queries
    # Note: IsDeleted first for better filtering (Solomon's recommendation on index ordering)
    op.create_index(
        'IX_Event_PublicReview',
        'Event',
        ['IsDeleted', 'IsPublic', 'IsSharedWithPlatform', 'PublicReviewStatusID'],
        schema='dbo'
    )
    
    # =====================================================================
    # STEP 6: Drop old CHECK constraint (if exists)
    # =====================================================================
    op.execute("""
        IF EXISTS (
            SELECT 1 
            FROM sys.check_constraints 
            WHERE name = 'CK_Event_PublicReviewStatus'
            AND parent_object_id = OBJECT_ID('dbo.Event')
        )
        BEGIN
            ALTER TABLE [dbo].[Event]
            DROP CONSTRAINT CK_Event_PublicReviewStatus;
        END
    """)


def downgrade():
    """Revert PublicReviewStatusID FK back to PublicReviewStatus VARCHAR"""
    
    # Drop index
    op.drop_index('IX_Event_PublicReview', table_name='Event', schema='dbo')
    op.drop_index('IX_Event_PublicReviewStatus', table_name='Event', schema='dbo')
    
    # Drop foreign key
    op.drop_constraint('FK_Event_PublicReviewStatus', 'Event', schema='dbo', type_='foreignkey')
    
    # Migrate data back from FK to VARCHAR (if PublicReviewStatusID exists)
    op.execute("""
        -- Add PublicReviewStatus column back if it doesn't exist
        IF NOT EXISTS (
            SELECT 1 FROM sys.columns 
            WHERE object_id = OBJECT_ID('dbo.Event') 
            AND name = 'PublicReviewStatus'
        )
        BEGIN
            ALTER TABLE [dbo].[Event]
            ADD PublicReviewStatus NVARCHAR(20) NULL;
        END
        
        -- Migrate data back
        UPDATE e
        SET e.PublicReviewStatus = prs.StatusCode
        FROM [dbo].[Event] e
        INNER JOIN [ref].[PublicReviewStatus] prs 
            ON e.PublicReviewStatusID = prs.PublicReviewStatusID
        WHERE e.PublicReviewStatusID IS NOT NULL;
    """)
    
    # Drop PublicReviewStatusID column
    op.drop_column('Event', 'PublicReviewStatusID', schema='dbo')
    
    # Recreate CHECK constraint
    op.create_check_constraint(
        'CK_Event_PublicReviewStatus',
        'Event',
        "PublicReviewStatus IS NULL OR PublicReviewStatus IN ('PENDING', 'APPROVED', 'REJECTED')",
        schema='dbo'
    )

