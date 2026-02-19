"""Story 5.7: Add Asset display settings for Terms (modal size, rotation)

Revision ID: 045
Revises: 044
Create Date: 2026-02-18

- Add dbo.Asset.DisplayWidthPx, DisplayHeightPx, DisplayRotationDegrees (nullable)
- Used by TERMS assets: preferred modal size and PDF rotation for form users
"""

from alembic import op
import sqlalchemy as sa

revision = "045"
down_revision = "044"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "Asset",
        sa.Column("DisplayWidthPx", sa.Integer, nullable=True),
        schema="dbo",
    )
    op.add_column(
        "Asset",
        sa.Column("DisplayHeightPx", sa.Integer, nullable=True),
        schema="dbo",
    )
    op.add_column(
        "Asset",
        sa.Column("DisplayRotationDegrees", sa.Integer, nullable=True),
        schema="dbo",
    )


def downgrade() -> None:
    op.drop_column("Asset", "DisplayRotationDegrees", schema="dbo")
    op.drop_column("Asset", "DisplayHeightPx", schema="dbo")
    op.drop_column("Asset", "DisplayWidthPx", schema="dbo")
