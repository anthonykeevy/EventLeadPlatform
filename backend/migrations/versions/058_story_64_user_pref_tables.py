"""Story 6.4: Create User Preferences architecture tables.

Creates three new tables that mirror the existing config.AppSetting pattern:
  - ref.UserPreferenceCategory: catalogue of preference categories
  - ref.UserPreferenceKey: catalogue of available preferences (reuses ref.SettingType)
  - dbo.UserPreference: per-user preference values (one row per user × key)

Revision ID: 058
Revises: 057
Create Date: 2026-04-24
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql


revision = "058"
down_revision = "057"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ─────────────────────────────────────────────────────────────────────────
    # 1. ref.UserPreferenceCategory
    # ─────────────────────────────────────────────────────────────────────────
    op.create_table(
        "UserPreferenceCategory",
        sa.Column("UserPreferenceCategoryID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("CategoryName", mssql.NVARCHAR(length=100), nullable=False),
        sa.Column("Description", mssql.NVARCHAR(length=500), nullable=False, server_default=sa.text("N''")),
        sa.Column("DisplayOrder", sa.Integer(), nullable=False, server_default=sa.text("999")),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("1")),
        # Audit columns — minimal for reference tables (match ref.SettingCategory pattern)
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("UserPreferenceCategoryID", name="PK_UserPreferenceCategory"),
        sa.UniqueConstraint("CategoryName", name="UQ_UserPreferenceCategory_CategoryName"),
        schema="ref",
    )

    # ─────────────────────────────────────────────────────────────────────────
    # 2. ref.UserPreferenceKey
    # ─────────────────────────────────────────────────────────────────────────
    op.create_table(
        "UserPreferenceKey",
        sa.Column("UserPreferenceKeyID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("PreferenceKey", mssql.NVARCHAR(length=150), nullable=False),
        sa.Column("PreferenceCategoryID", sa.BigInteger(), nullable=False),
        sa.Column("SettingTypeID", sa.BigInteger(), nullable=False),
        sa.Column("DisplayName", mssql.NVARCHAR(length=200), nullable=False),
        sa.Column("Description", mssql.NVARCHAR(length=500), nullable=False, server_default=sa.text("N''")),
        sa.Column("DefaultValue", mssql.NVARCHAR(length=None), nullable=False),
        sa.Column("IsEditable", mssql.BIT(), nullable=False, server_default=sa.text("1")),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("1")),
        sa.Column("SortOrder", sa.Integer(), nullable=False, server_default=sa.text("999")),
        # Audit columns — minimal for reference tables
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("UserPreferenceKeyID", name="PK_UserPreferenceKey"),
        sa.UniqueConstraint("PreferenceKey", name="UQ_UserPreferenceKey_PreferenceKey"),
        sa.ForeignKeyConstraint(
            ["PreferenceCategoryID"],
            ["ref.UserPreferenceCategory.UserPreferenceCategoryID"],
            name="FK_UserPreferenceKey_PreferenceCategoryID",
        ),
        sa.ForeignKeyConstraint(
            ["SettingTypeID"],
            ["ref.SettingType.SettingTypeID"],
            name="FK_UserPreferenceKey_SettingTypeID",
        ),
        schema="ref",
    )
    op.create_index(
        "IX_UserPreferenceKey_PreferenceCategoryID",
        "UserPreferenceKey",
        ["PreferenceCategoryID"],
        schema="ref",
    )
    op.create_index(
        "IX_UserPreferenceKey_SettingTypeID",
        "UserPreferenceKey",
        ["SettingTypeID"],
        schema="ref",
    )

    # ─────────────────────────────────────────────────────────────────────────
    # 3. dbo.UserPreference
    # ─────────────────────────────────────────────────────────────────────────
    op.create_table(
        "UserPreference",
        sa.Column("UserPreferenceID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("UserID", sa.BigInteger(), nullable=False),
        sa.Column("PreferenceKeyID", sa.BigInteger(), nullable=False),
        sa.Column("PreferenceValue", mssql.NVARCHAR(length=None), nullable=False),
        # Full audit columns — matches dbo.User / config.AppSetting pattern
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("UserPreferenceID", name="PK_UserPreference"),
        sa.UniqueConstraint("UserID", "PreferenceKeyID", name="UQ_UserPreference_UserID_PreferenceKeyID"),
        sa.ForeignKeyConstraint(
            ["UserID"],
            ["dbo.User.UserID"],
            name="FK_UserPreference_UserID",
        ),
        sa.ForeignKeyConstraint(
            ["PreferenceKeyID"],
            ["ref.UserPreferenceKey.UserPreferenceKeyID"],
            name="FK_UserPreference_PreferenceKeyID",
        ),
        schema="dbo",
    )
    op.create_index(
        "IX_UserPreference_UserID",
        "UserPreference",
        ["UserID"],
        schema="dbo",
    )
    op.create_index(
        "IX_UserPreference_PreferenceKeyID",
        "UserPreference",
        ["PreferenceKeyID"],
        schema="dbo",
    )


def downgrade() -> None:
    op.drop_table("UserPreference", schema="dbo")
    op.drop_index("IX_UserPreferenceKey_SettingTypeID", table_name="UserPreferenceKey", schema="ref")
    op.drop_index("IX_UserPreferenceKey_PreferenceCategoryID", table_name="UserPreferenceKey", schema="ref")
    op.drop_table("UserPreferenceKey", schema="ref")
    op.drop_table("UserPreferenceCategory", schema="ref")
