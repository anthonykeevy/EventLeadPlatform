"""Add Asset metadata tables (AssetType + Asset)

Revision ID: 036
Revises: 035
Create Date: 2026-02-09

Story: 5.1 - Background Asset Management
Task: T02 - DB Migration — Asset Metadata Tables
Purpose:
- Create reference table `ref.AssetType` (seed: IMAGE)
- Create metadata table `dbo.Asset` with:
  - AssetTypeID FK → ref.AssetType
  - hash-based dedup support (unique filtered index on CompanyID + AssetTypeID + Sha256 where IsDeleted = 0)
  - soft-delete support
  - display name + original filename support
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql


# revision identifiers, used by Alembic.
revision = "036"
down_revision = "035"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Ensure ref schema exists (safe even if already present)
    op.execute("IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'ref') EXEC('CREATE SCHEMA [ref]')")

    # ---------------------------------------------------------------------
    # ref.AssetType (reference/enum table)
    # ---------------------------------------------------------------------
    op.create_table(
        "AssetType",
        sa.Column("AssetTypeID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("TypeCode", mssql.NVARCHAR(length=20), nullable=False),
        sa.Column("TypeName", mssql.NVARCHAR(length=50), nullable=False),
        sa.Column("Description", mssql.NVARCHAR(length=500), nullable=True),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("1")),
        sa.Column("SortOrder", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column(
            "CreatedDate",
            mssql.DATETIME2(),
            nullable=False,
            server_default=sa.func.getutcdate(),
        ),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("AssetTypeID", name="PK_AssetType_AssetTypeID"),
        sa.UniqueConstraint("TypeCode", name="UQ_AssetType_TypeCode"),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_AssetType_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_AssetType_UpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_AssetType_DeletedBy"),
        schema="ref",
    )

    # Seed required AssetType values (minimum: IMAGE)
    # Use UserID=1 if it exists; otherwise leave CreatedBy NULL.
    op.execute(
        """
        DECLARE @SystemUserID BIGINT;
        SELECT @SystemUserID = UserID FROM [dbo].[User] WHERE UserID = 1;
        IF @SystemUserID IS NULL
        BEGIN
            SET @SystemUserID = NULL;
        END

        IF NOT EXISTS (
            SELECT 1
            FROM [ref].[AssetType]
            WHERE TypeCode = 'IMAGE' AND IsDeleted = 0
        )
        BEGIN
            INSERT INTO [ref].[AssetType] (TypeCode, TypeName, Description, IsActive, SortOrder, CreatedBy)
            VALUES ('IMAGE', 'Image', 'Image asset type (backgrounds and related images).', 1, 1, @SystemUserID);
        END
        """
    )

    # ---------------------------------------------------------------------
    # dbo.Asset (tenant-scoped asset metadata)
    # ---------------------------------------------------------------------
    op.create_table(
        "Asset",
        sa.Column("AssetID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("CompanyID", sa.BigInteger(), nullable=False),
        sa.Column("AssetTypeID", sa.BigInteger(), nullable=False),
        sa.Column("Sha256", mssql.NVARCHAR(length=64), nullable=False),
        sa.Column("MimeType", mssql.NVARCHAR(length=100), nullable=False),
        sa.Column("SizeBytes", sa.BigInteger(), nullable=False),
        sa.Column("WidthPx", sa.Integer(), nullable=False),
        sa.Column("HeightPx", sa.Integer(), nullable=False),
        sa.Column("StorageProvider", mssql.NVARCHAR(length=50), nullable=False),
        sa.Column("StorageKey", mssql.NVARCHAR(length=500), nullable=False),
        sa.Column("OriginalFileName", mssql.NVARCHAR(length=255), nullable=True),
        sa.Column("DisplayName", mssql.NVARCHAR(length=255), nullable=True),
        sa.Column(
            "CreatedDate",
            mssql.DATETIME2(),
            nullable=False,
            server_default=sa.func.getutcdate(),
        ),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("AssetID", name="PK_Asset_AssetID"),
        sa.ForeignKeyConstraint(["CompanyID"], ["dbo.Company.CompanyID"], name="FK_Asset_CompanyID"),
        sa.ForeignKeyConstraint(["AssetTypeID"], ["ref.AssetType.AssetTypeID"], name="FK_Asset_AssetTypeID"),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_Asset_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_Asset_UpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_Asset_DeletedBy"),
        schema="dbo",
    )

    # Query-friendly indexes (soft-delete aware)
    op.create_index(
        "IX_Asset_CompanyID_IsDeleted",
        "Asset",
        ["CompanyID", "IsDeleted"],
        unique=False,
        schema="dbo",
    )
    op.create_index(
        "IX_Asset_AssetTypeID_IsDeleted",
        "Asset",
        ["AssetTypeID", "IsDeleted"],
        unique=False,
        schema="dbo",
    )

    # Hash-based deduplication (scoped to Company + AssetType, excluding soft-deleted rows)
    op.create_index(
        "UQ_Asset_CompanyID_AssetTypeID_Sha256",
        "Asset",
        ["CompanyID", "AssetTypeID", "Sha256"],
        unique=True,
        schema="dbo",
        mssql_where="IsDeleted = 0",
    )


def downgrade() -> None:
    # Drop indexes first (SQL Server safe + explicit)
    op.drop_index(
        "UQ_Asset_CompanyID_AssetTypeID_Sha256",
        table_name="Asset",
        schema="dbo",
    )
    op.drop_index(
        "IX_Asset_AssetTypeID_IsDeleted",
        table_name="Asset",
        schema="dbo",
    )
    op.drop_index(
        "IX_Asset_CompanyID_IsDeleted",
        table_name="Asset",
        schema="dbo",
    )

    # Drop tables in dependency order
    op.drop_table("Asset", schema="dbo")
    op.drop_table("AssetType", schema="ref")

