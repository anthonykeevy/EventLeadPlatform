"""Add APPROVED_FOR_PUBLISH + deactivate unused statuses (Story 5.8)

Revision ID: 050
Revises: 049
Create Date: 2026-02-20

- Add APPROVED_FOR_PUBLISH to ref.FormStatus (Approved for Publish; after Approve only)
- Set IsActive=0 for unused statuses: REVIEW, PAUSED, ARCHIVED, DELETED (FormStatus)
  and CANCELLED, EXPIRED (FormApprovalStatus)
"""

from alembic import op

revision = "050"
down_revision = "049"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Add APPROVED_FOR_PUBLISH to ref.FormStatus (if not exists)
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [ref].[FormStatus] WHERE StatusCode = N'APPROVED_FOR_PUBLISH')
        INSERT INTO [ref].[FormStatus] (StatusCode, StatusName, StatusDescription, StatusColor, StatusIcon, IsActive, SortOrder, CreatedBy)
        VALUES (N'APPROVED_FOR_PUBLISH', N'Approved for Publish', N'Form approved; Admin can publish with one click', N'#059669', N'review-icon', 1, 3, 1);
    """)

    # 2. Deactivate unused FormStatus: REVIEW, PAUSED, ARCHIVED, DELETED
    op.execute("""
        UPDATE [ref].[FormStatus] SET IsActive = 0 WHERE StatusCode IN (N'REVIEW', N'PAUSED', N'ARCHIVED', N'DELETED');
    """)

    # 3. Deactivate unused FormApprovalStatus: CANCELLED, EXPIRED
    op.execute("""
        UPDATE [ref].[FormApprovalStatus] SET IsActive = 0 WHERE ApprovalStatusCode IN (N'CANCELLED', N'EXPIRED');
    """)


def downgrade() -> None:
    # Reactivate statuses
    op.execute("""
        UPDATE [ref].[FormStatus] SET IsActive = 1 WHERE StatusCode IN (N'REVIEW', N'PAUSED', N'ARCHIVED', N'DELETED');
    """)
    op.execute("""
        UPDATE [ref].[FormApprovalStatus] SET IsActive = 1 WHERE ApprovalStatusCode IN (N'CANCELLED', N'EXPIRED');
    """)

    # Remove APPROVED_FOR_PUBLISH (only if no forms reference it)
    op.execute("""
        DELETE FROM [ref].[FormStatus] WHERE StatusCode = N'APPROVED_FOR_PUBLISH';
    """)
