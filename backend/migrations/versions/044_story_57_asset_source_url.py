"""Story 5.7: Add Asset.SourceURL for URL-based Terms

Revision ID: 044
Revises: 043
Create Date: 2026-02-18

- Add dbo.Asset.SourceURL nullable (URL-based Terms; when set, StorageKey is url:{hash})
"""

from alembic import op
import sqlalchemy as sa

revision = "044"
down_revision = "043"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "Asset",
        sa.Column("SourceURL", sa.NVARCHAR(2048), nullable=True),
        schema="dbo",
    )


def downgrade() -> None:
    op.drop_column("Asset", "SourceURL", schema="dbo")
