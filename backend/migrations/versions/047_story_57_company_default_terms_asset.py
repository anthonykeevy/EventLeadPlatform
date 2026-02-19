"""Story 5.7: Add Company.DefaultTermsAssetID for preferred Terms

Revision ID: 047
Revises: 046
Create Date: 2026-02-18

- Add dbo.Company.DefaultTermsAssetID (BIGINT, nullable FK to Asset)
- When multiple Terms assets exist, company selects which to use in forms
"""

from alembic import op
import sqlalchemy as sa

revision = "047"
down_revision = "046"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "Company",
        sa.Column("DefaultTermsAssetID", sa.BigInteger(), nullable=True),
        schema="dbo",
    )
    op.create_foreign_key(
        "FK_Company_DefaultTermsAsset_Asset",
        "Company",
        "Asset",
        ["DefaultTermsAssetID"],
        ["AssetID"],
        source_schema="dbo",
        referent_schema="dbo",
    )


def downgrade() -> None:
    op.drop_constraint(
        "FK_Company_DefaultTermsAsset_Asset",
        "Company",
        schema="dbo",
        type_="foreignkey",
    )
    op.drop_column("Company", "DefaultTermsAssetID", schema="dbo")
