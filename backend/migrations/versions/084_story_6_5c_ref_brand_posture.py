"""Story 6.5c: ref.BrandPosture table + seed.

Revision ID: 084
Revises: 083
Create Date: 2026-05-20
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql


revision = "084"
down_revision = "083"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "BrandPosture",
        sa.Column("BrandPostureID", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("Code", mssql.NVARCHAR(length=40), nullable=False),
        sa.Column("DisplayName", mssql.NVARCHAR(length=100), nullable=False),
        sa.Column("SortOrder", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("1")),
        sa.PrimaryKeyConstraint("BrandPostureID", name="PK_BrandPosture_BrandPostureID"),
        sa.UniqueConstraint("Code", name="UQ_BrandPosture_Code"),
        schema="ref",
    )

    op.execute(
        """
        INSERT INTO [ref].[BrandPosture] ([Code], [DisplayName], [SortOrder], [IsActive])
        VALUES
            (N'local', N'Local', 10, 1),
            (N'heritage', N'Heritage', 20, 1),
            (N'neutral', N'Neutral', 30, 1),
            (N'transcreate', N'Transcreate', 40, 1);
        """
    )


def downgrade() -> None:
    op.drop_table("BrandPosture", schema="ref")
