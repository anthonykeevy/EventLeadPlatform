"""Story 5.6: Publish Request Workflow

Revision ID: 042
Revises: 041
Create Date: 2026-02-16

- Add RequirePublishApproval to CompanyFormTestConfig
- Create FormPublishRequest table
- Add PENDING_REVIEW to ref.FormStatus
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

revision = "042"
down_revision = "041"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Add RequirePublishApproval to CompanyFormTestConfig
    op.add_column(
        "CompanyFormTestConfig",
        sa.Column("RequirePublishApproval", mssql.BIT(), nullable=True, server_default=sa.text("0")),
        schema="dbo",
    )
    op.alter_column(
        "CompanyFormTestConfig",
        "RequirePublishApproval",
        existing_type=mssql.BIT(),
        nullable=False,
        schema="dbo",
    )

    # 2. Add PENDING_REVIEW to ref.FormStatus (if not exists)
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [ref].[FormStatus] WHERE StatusCode = N'PENDING_REVIEW')
        INSERT INTO [ref].[FormStatus] (StatusCode, StatusName, StatusDescription, StatusColor, StatusIcon, IsActive, SortOrder, CreatedBy)
        VALUES (N'PENDING_REVIEW', N'Pending Admin Review', N'Form requested for publish; awaiting admin review', N'#17A2B8', N'review-icon', 1, 2, 1);
    """)

    # 3. Create FormPublishRequest table
    op.create_table(
        "FormPublishRequest",
        sa.Column("FormPublishRequestID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("FormID", sa.BigInteger(), nullable=False),
        sa.Column("RequestedBy", sa.BigInteger(), nullable=False),
        sa.Column("RequestedAt", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("Message", mssql.NVARCHAR(length=1000), nullable=True),
        sa.Column("Status", mssql.NVARCHAR(length=20), nullable=False, server_default="pending"),
        sa.Column("CompanyID", sa.BigInteger(), nullable=False),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("FormPublishRequestID", name="PK_FormPublishRequest"),
        sa.ForeignKeyConstraint(["FormID"], ["dbo.Form.FormID"], name="FK_FormPublishRequest_FormID"),
        sa.ForeignKeyConstraint(["RequestedBy"], ["dbo.User.UserID"], name="FK_FormPublishRequest_RequestedBy"),
        sa.ForeignKeyConstraint(["CompanyID"], ["dbo.Company.CompanyID"], name="FK_FormPublishRequest_CompanyID"),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_FormPublishRequest_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_FormPublishRequest_UpdatedBy"),
        schema="dbo",
    )
    op.create_index("IX_FormPublishRequest_FormID", "FormPublishRequest", ["FormID"], unique=False, schema="dbo")
    op.create_index("IX_FormPublishRequest_CompanyID_Status", "FormPublishRequest", ["CompanyID", "Status"], unique=False, schema="dbo")
    op.create_index("IX_FormPublishRequest_RequestedAt", "FormPublishRequest", ["RequestedAt"], unique=False, schema="dbo")


def downgrade() -> None:
    op.drop_index("IX_FormPublishRequest_RequestedAt", table_name="FormPublishRequest", schema="dbo")
    op.drop_index("IX_FormPublishRequest_CompanyID_Status", table_name="FormPublishRequest", schema="dbo")
    op.drop_index("IX_FormPublishRequest_FormID", table_name="FormPublishRequest", schema="dbo")
    op.drop_table("FormPublishRequest", schema="dbo")

    op.execute("""
        DELETE FROM [ref].[FormStatus] WHERE StatusCode = N'PENDING_REVIEW';
    """)

    op.drop_column("CompanyFormTestConfig", "RequirePublishApproval", schema="dbo")
