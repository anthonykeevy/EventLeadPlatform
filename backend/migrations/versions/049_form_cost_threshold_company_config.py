"""Add FormCostThreshold to CompanyFormTestConfig (unified approval gates)

Revision ID: 049
Revises: 048
Create Date: 2026-02-20

- Add FormCostThreshold (nullable, dollars) to CompanyFormTestConfig
- When set: forms with deployment cost > threshold require approval (future: unified flow)
- Backfill 100 for backward compatibility with hardcoded threshold
"""

from alembic import op
import sqlalchemy as sa

revision = "049"
down_revision = "048"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "CompanyFormTestConfig",
        sa.Column("FormCostThreshold", sa.Numeric(10, 2), nullable=True),
        schema="dbo",
    )
    op.execute("UPDATE dbo.CompanyFormTestConfig SET FormCostThreshold = 100 WHERE FormCostThreshold IS NULL")


def downgrade() -> None:
    op.drop_column("CompanyFormTestConfig", "FormCostThreshold", schema="dbo")
