"""Story 5.7: Add TERMS, DOCUMENT, VIDEO asset types; Asset.WidthPx/HeightPx nullable

Revision ID: 043
Revises: 042
Create Date: 2026-02-18

- Add ref.AssetType: TERMS, DOCUMENT, VIDEO (IMAGE already exists)
- Make dbo.Asset.WidthPx and HeightPx nullable (non-image assets don't have dimensions)
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

revision = "043"
down_revision = "042"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Insert TERMS, DOCUMENT, VIDEO into ref.AssetType (skip if exists)
    op.execute("""
        DECLARE @SystemUserID BIGINT;
        SELECT @SystemUserID = UserID FROM [dbo].[User] WHERE UserID = 1;

        IF NOT EXISTS (SELECT 1 FROM [ref].[AssetType] WHERE TypeCode = N'TERMS' AND IsDeleted = 0)
        INSERT INTO [ref].[AssetType] (TypeCode, TypeName, Description, IsActive, SortOrder, CreatedBy)
        VALUES (N'TERMS', N'Terms of Agreement', N'Terms of Service, Privacy Policy, consent documents.', 1, 2, @SystemUserID);

        IF NOT EXISTS (SELECT 1 FROM [ref].[AssetType] WHERE TypeCode = N'DOCUMENT' AND IsDeleted = 0)
        INSERT INTO [ref].[AssetType] (TypeCode, TypeName, Description, IsActive, SortOrder, CreatedBy)
        VALUES (N'DOCUMENT', N'Document', N'General document assets (PDF, Word, etc.).', 1, 3, @SystemUserID);

        IF NOT EXISTS (SELECT 1 FROM [ref].[AssetType] WHERE TypeCode = N'VIDEO' AND IsDeleted = 0)
        INSERT INTO [ref].[AssetType] (TypeCode, TypeName, Description, IsActive, SortOrder, CreatedBy)
        VALUES (N'VIDEO', N'Video', N'Video assets.', 1, 4, @SystemUserID);
    """)

    # 2. Make Asset.WidthPx and HeightPx nullable
    op.alter_column(
        "Asset",
        "WidthPx",
        existing_type=sa.Integer(),
        nullable=True,
        schema="dbo",
    )
    op.alter_column(
        "Asset",
        "HeightPx",
        existing_type=sa.Integer(),
        nullable=True,
        schema="dbo",
    )


def downgrade() -> None:
    # Restore NOT NULL for WidthPx/HeightPx - set NULLs to 0 for existing rows
    op.execute("""
        UPDATE [dbo].[Asset] SET WidthPx = 0 WHERE WidthPx IS NULL;
        UPDATE [dbo].[Asset] SET HeightPx = 0 WHERE HeightPx IS NULL;
    """)
    op.alter_column(
        "Asset",
        "WidthPx",
        existing_type=sa.Integer(),
        nullable=False,
        schema="dbo",
    )
    op.alter_column(
        "Asset",
        "HeightPx",
        existing_type=sa.Integer(),
        nullable=False,
        schema="dbo",
    )
    # Soft-delete TERMS, DOCUMENT, VIDEO (or leave - no hard delete for ref data)
    op.execute("""
        UPDATE [ref].[AssetType] SET IsDeleted = 1, DeletedDate = SYSUTCDATETIME()
        WHERE TypeCode IN (N'TERMS', N'DOCUMENT', N'VIDEO');
    """)
