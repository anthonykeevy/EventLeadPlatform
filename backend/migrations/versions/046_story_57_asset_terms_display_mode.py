"""Story 5.7: Add Asset.TermsDisplayMode for pop-up vs new tab

Revision ID: 046
Revises: 045
Create Date: 2026-02-18

- Add dbo.Asset.TermsDisplayMode (NVARCHAR(20), nullable): 'popup' | 'new_tab'
- URL-based Terms: popup = display in iframe; new_tab = link opens in new tab
- PDF assets: null (always popup)
"""

from alembic import op
import sqlalchemy as sa

revision = "046"
down_revision = "045"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "Asset",
        sa.Column("TermsDisplayMode", sa.String(20), nullable=True),
        schema="dbo",
    )


def downgrade() -> None:
    op.drop_column("Asset", "TermsDisplayMode", schema="dbo")
