"""Story 6.4.4.1: Country cultural dimensions sidecar.

Revision ID: 064
Revises: 063
Create Date: 2026-04-27
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql


revision = "064"
down_revision = "063"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "CountryCulturalDimensions",
        sa.Column("CountryCulturalDimensionsID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("CountryID", sa.BigInteger(), nullable=True),
        sa.Column("PowerDistanceIndex", sa.Integer(), nullable=True),
        sa.Column("UncertaintyAvoidanceIndex", sa.Integer(), nullable=True),
        sa.Column("IndividualismIndex", sa.Integer(), nullable=True),
        sa.Column("MasculinityIndex", sa.Integer(), nullable=True),
        sa.Column("LongTermOrientation", sa.Integer(), nullable=True),
        sa.Column("IndulgenceIndex", sa.Integer(), nullable=True),
        sa.Column("Source", mssql.NVARCHAR(length=200), nullable=False),
        sa.Column("SourceYear", sa.Integer(), nullable=True),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(
            ["CountryID"],
            ["ref.Country.CountryID"],
            name="FK_CountryCulturalDimensions_CountryID",
        ),
        sa.ForeignKeyConstraint(
            ["CreatedBy"], ["dbo.User.UserID"], name="FK_CountryCulturalDimensions_CreatedBy"
        ),
        sa.ForeignKeyConstraint(
            ["UpdatedBy"], ["dbo.User.UserID"], name="FK_CountryCulturalDimensions_UpdatedBy"
        ),
        sa.ForeignKeyConstraint(
            ["DeletedBy"], ["dbo.User.UserID"], name="FK_CountryCulturalDimensions_DeletedBy"
        ),
        sa.PrimaryKeyConstraint("CountryCulturalDimensionsID", name="PK_CountryCulturalDimensions"),
        schema="ref",
    )
    op.execute(
        """
        CREATE UNIQUE NONCLUSTERED INDEX UQ_CountryCulturalDimensions_CountryID_Active
        ON [ref].[CountryCulturalDimensions] ([CountryID])
        WHERE [IsDeleted] = 0;
        """
    )


def downgrade() -> None:
    op.execute(
        """
        IF EXISTS (
            SELECT 1
            FROM sys.indexes
            WHERE name = 'UQ_CountryCulturalDimensions_CountryID_Active'
              AND object_id = OBJECT_ID('ref.CountryCulturalDimensions')
        )
        DROP INDEX [UQ_CountryCulturalDimensions_CountryID_Active]
        ON [ref].[CountryCulturalDimensions];
        """
    )
    op.drop_table("CountryCulturalDimensions", schema="ref")
