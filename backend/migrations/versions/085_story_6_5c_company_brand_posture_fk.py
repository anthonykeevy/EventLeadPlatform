"""Story 6.5c: Company.BrandPostureID FK to ref.BrandPosture.

Revision ID: 085
Revises: 084
Create Date: 2026-05-20
"""

from alembic import op
import sqlalchemy as sa


revision = "085"
down_revision = "084"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "Company",
        sa.Column("BrandPostureID", sa.Integer(), nullable=True),
        schema="dbo",
    )
    op.create_foreign_key(
        "FK_Company_BrandPosture",
        "Company",
        "BrandPosture",
        ["BrandPostureID"],
        ["BrandPostureID"],
        source_schema="dbo",
        referent_schema="ref",
    )
    op.create_index(
        "IX_Company_BrandPostureID",
        "Company",
        ["BrandPostureID"],
        unique=False,
        schema="dbo",
    )

    op.execute(
        """
        UPDATE c
        SET c.[BrandPostureID] = bp.[BrandPostureID]
        FROM [dbo].[Company] c
        INNER JOIN [ref].[BrandPosture] bp
            ON bp.[Code] = c.[BrandPosture]
           AND bp.[IsActive] = 1
        WHERE c.[BrandPosture] IS NOT NULL;
        """
    )


def downgrade() -> None:
    op.drop_index("IX_Company_BrandPostureID", table_name="Company", schema="dbo")
    op.drop_constraint("FK_Company_BrandPosture", "Company", schema="dbo", type_="foreignkey")
    op.drop_column("Company", "BrandPostureID", schema="dbo")
