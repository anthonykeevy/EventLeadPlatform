"""Story 6.4.4.1: Add brand posture audit fields to GenerationRun.

Revision ID: 069
Revises: 068
Create Date: 2026-04-27
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql


revision = "069"
down_revision = "068"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("GenerationRun", sa.Column("BrandPosture", mssql.NVARCHAR(length=40), nullable=True), schema="dbo")
    op.add_column(
        "GenerationRun",
        sa.Column("BrandHeritageOrigin", mssql.NVARCHAR(length=5), nullable=True),
        schema="dbo",
    )
    op.execute(
        """
        ALTER TABLE [dbo].[GenerationRun]
        ADD CONSTRAINT [CK_GenerationRun_BrandPosture]
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
            WHERE [name] = N'CK_GenerationRun_BrandPosture'
              AND [parent_object_id] = OBJECT_ID(N'dbo.GenerationRun')
        )
        ALTER TABLE [dbo].[GenerationRun]
        DROP CONSTRAINT [CK_GenerationRun_BrandPosture];
        """
    )
    op.drop_column("GenerationRun", "BrandHeritageOrigin", schema="dbo")
    op.drop_column("GenerationRun", "BrandPosture", schema="dbo")
