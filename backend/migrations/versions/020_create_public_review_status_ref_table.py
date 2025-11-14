"""Create PublicReviewStatus reference table

Revision ID: 020_public_review_status_ref
Revises: 019_event_company_relationships
Create Date: 2025-01-XX 12:00:00.000000

Story: 2.6 - Admin Public Event Review Workflow
Purpose: Create reference table for public event review status (PENDING, APPROVED, REJECTED)
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = '020_public_review_status_ref'
down_revision = '019_event_company_relationships'
branch_labels = None
depends_on = None


def upgrade():
    """Create ref.PublicReviewStatus reference table with seed data"""
    
    # Ensure ref schema exists (should already exist, but safe to check)
    op.execute("IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'ref') EXEC('CREATE SCHEMA [ref]')")
    
    # =====================================================================
    # CREATE PublicReviewStatus REFERENCE TABLE
    # =====================================================================
    op.create_table(
        'PublicReviewStatus',
        sa.Column('PublicReviewStatusID', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('StatusCode', mssql.NVARCHAR(20), nullable=False),
        sa.Column('StatusName', mssql.NVARCHAR(50), nullable=False),
        sa.Column('StatusDescription', mssql.NVARCHAR(200), nullable=True),
        sa.Column('StatusColor', mssql.NVARCHAR(7), nullable=True),
        sa.Column('StatusIcon', mssql.NVARCHAR(50), nullable=True),
        sa.Column('IsActive', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('SortOrder', sa.Integer(), nullable=False, server_default='0'),
        # Using DATETIME2 explicitly for precision (Solomon's recommendation)
        sa.Column('CreatedDate', mssql.DATETIME2(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=True),
        sa.Column('UpdatedDate', mssql.DATETIME2(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('DeletedDate', mssql.DATETIME2(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('PublicReviewStatusID', name='PK_PublicReviewStatus_PublicReviewStatusID'),
        sa.UniqueConstraint('StatusCode', name='UQ_PublicReviewStatus_StatusCode'),
        schema='ref'
    )
    
    # Create foreign key constraints
    op.create_foreign_key(
        'FK_PublicReviewStatus_CreatedBy',
        'PublicReviewStatus',
        'User',
        ['CreatedBy'],
        ['UserID'],
        source_schema='ref',
        referent_schema='dbo'
    )
    
    op.create_foreign_key(
        'FK_PublicReviewStatus_UpdatedBy',
        'PublicReviewStatus',
        'User',
        ['UpdatedBy'],
        ['UserID'],
        source_schema='ref',
        referent_schema='dbo'
    )
    
    op.create_foreign_key(
        'FK_PublicReviewStatus_DeletedBy',
        'PublicReviewStatus',
        'User',
        ['DeletedBy'],
        ['UserID'],
        source_schema='ref',
        referent_schema='dbo'
    )
    
    # =====================================================================
    # INSERT SEED DATA (with UserID validation)
    # =====================================================================
    # Validate that UserID=1 exists before inserting seed data (Solomon's recommendation)
    op.execute("""
        -- Validate UserID=1 exists (for seed data CreatedBy)
        DECLARE @SystemUserID BIGINT;
        SELECT @SystemUserID = UserID FROM [dbo].[User] WHERE UserID = 1;
        
        IF @SystemUserID IS NULL
        BEGIN
            -- If UserID=1 doesn't exist, use NULL for system-created records
            SET @SystemUserID = NULL;
        END
        
        INSERT INTO [ref].[PublicReviewStatus] (
            StatusCode, 
            StatusName, 
            StatusDescription, 
            StatusColor, 
            StatusIcon, 
            IsActive, 
            SortOrder, 
            CreatedBy
        ) VALUES
        -- PENDING: Event is in admin review queue
        ('PENDING', 'Pending Review', 
            'Event is awaiting admin review for platform-wide visibility. Admin will review content quality before approving.', 
            '#FFC107', 'clock-icon', 1, 1, @SystemUserID),
        
        -- APPROVED: Admin approved, but user controls publication
        ('APPROVED', 'Approved', 
            'Event has been approved by admin for platform-wide visibility. Event will be publicly visible when user publishes it (EventStatus = PUBLISHED).', 
            '#28A745', 'check-circle-icon', 1, 2, @SystemUserID),
        
        -- REJECTED: Admin rejected, but can be resubmitted
        ('REJECTED', 'Rejected', 
            'Event has been rejected by admin and cannot be shared with platform-wide search. Event remains visible to company network only. User can edit and resubmit for review.', 
            '#DC3545', 'x-circle-icon', 1, 3, @SystemUserID);
    """)


def downgrade():
    """Drop ref.PublicReviewStatus reference table"""
    
    # Drop foreign keys first
    op.drop_constraint('FK_PublicReviewStatus_DeletedBy', 'PublicReviewStatus', schema='ref', type_='foreignkey')
    op.drop_constraint('FK_PublicReviewStatus_UpdatedBy', 'PublicReviewStatus', schema='ref', type_='foreignkey')
    op.drop_constraint('FK_PublicReviewStatus_CreatedBy', 'PublicReviewStatus', schema='ref', type_='foreignkey')
    
    # Drop table
    op.drop_table('PublicReviewStatus', schema='ref')

