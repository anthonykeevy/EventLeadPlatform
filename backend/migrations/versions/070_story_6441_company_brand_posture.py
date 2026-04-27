"""Story 6.4.4.1: Add company brand posture defaults.

Revision ID: 070
Revises: 069
Create Date: 2026-04-27
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql


revision = "070"
down_revision = "069"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("Company", sa.Column("BrandPosture", mssql.NVARCHAR(length=40), nullable=True), schema="dbo")
    op.add_column(
        "Company",
        sa.Column("BrandHeritageOrigin", mssql.NVARCHAR(length=5), nullable=True),
        schema="dbo",
    )
    op.execute(
        """
        ALTER TABLE [dbo].[Company]
        ADD CONSTRAINT [CK_Company_BrandPosture]
        CHECK (
            [BrandPosture] IS NULL
            OR [BrandPosture] IN (N'local', N'heritage', N'neutral', N'transcreate')
        );
        """
    )


def downgrade() -> None:
    op.execute(
        """
        IF EXISTS (
            SELECT 1 FROM sys.check_constraints
            WHERE [name] = N'CK_Company_BrandPosture'
              AND [parent_object_id] = OBJECT_ID(N'dbo.Company')
        )
        ALTER TABLE [dbo].[Company]
        DROP CONSTRAINT [CK_Company_BrandPosture];
        """
    )
    op.drop_column("Company", "BrandHeritageOrigin", schema="dbo")
    op.drop_column("Company", "BrandPosture", schema="dbo")
