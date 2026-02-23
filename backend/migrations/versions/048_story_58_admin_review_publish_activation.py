"""Story 5.8: Admin Review & Publish + Activation

Revision ID: 048
Revises: 047
Create Date: 2026-02-20

- Add UNPUBLISHED to ref.FormStatus
- Add Form.UnpublishMode (MANUAL | EVENT_END | SCHEDULED)
- Add Form.ScheduledUnpublishDate (nullable)
- Create FormRepublishRequest for re-publish requests from unpublished page
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

revision = "048"
down_revision = "047"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Add UNPUBLISHED to ref.FormStatus (if not exists)
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM [ref].[FormStatus] WHERE StatusCode = N'UNPUBLISHED')
        INSERT INTO [ref].[FormStatus] (StatusCode, StatusName, StatusDescription, StatusColor, StatusIcon, IsActive, SortOrder, CreatedBy)
        VALUES (N'UNPUBLISHED', N'Unpublished', N'Form was published; now taken offline', N'#6C757D', N'unpublish-icon', 1, 4, 1);
    """)

    # 2. Add UnpublishMode to Form
    op.add_column(
        "Form",
        sa.Column("UnpublishMode", mssql.NVARCHAR(length=20), nullable=True),
        schema="dbo",
    )
    # Backfill existing rows before NOT NULL constraint (SQL Server does not auto-backfill on ADD)
    op.execute("UPDATE dbo.[Form] SET UnpublishMode = N'MANUAL' WHERE UnpublishMode IS NULL")
    op.alter_column(
        "Form",
        "UnpublishMode",
        existing_type=mssql.NVARCHAR(length=20),
        nullable=False,
        server_default="MANUAL",
        schema="dbo",
    )

    # 3. Add ScheduledUnpublishDate to Form
    op.add_column(
        "Form",
        sa.Column("ScheduledUnpublishDate", mssql.DATETIME2(), nullable=True),
        schema="dbo",
    )

    # 4. Create FormRepublishRequest (visitor requests re-publish from unpublished page)
    op.create_table(
        "FormRepublishRequest",
        sa.Column("FormRepublishRequestID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("FormID", sa.BigInteger(), nullable=False),
        sa.Column("RequestedAt", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("IPAddress", mssql.NVARCHAR(length=45), nullable=True),
        sa.Column("UserAgent", mssql.NVARCHAR(length=500), nullable=True),
        sa.PrimaryKeyConstraint("FormRepublishRequestID", name="PK_FormRepublishRequest"),
        sa.ForeignKeyConstraint(["FormID"], ["dbo.Form.FormID"], name="FK_FormRepublishRequest_FormID"),
        schema="dbo",
    )
    op.create_index("IX_FormRepublishRequest_FormID", "FormRepublishRequest", ["FormID"], unique=False, schema="dbo")


def downgrade() -> None:
    op.drop_index("IX_FormRepublishRequest_FormID", table_name="FormRepublishRequest", schema="dbo")
    op.drop_table("FormRepublishRequest", schema="dbo")

    op.drop_column("Form", "ScheduledUnpublishDate", schema="dbo")
    op.drop_column("Form", "UnpublishMode", schema="dbo")

    op.execute("""
        DELETE FROM [ref].[FormStatus] WHERE StatusCode = N'UNPUBLISHED';
    """)
