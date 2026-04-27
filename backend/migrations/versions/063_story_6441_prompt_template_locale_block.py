"""Story 6.4.4.1: Prompt template locale block registry.

Revision ID: 063
Revises: 062
Create Date: 2026-04-27
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql


revision = "063"
down_revision = "062"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "PromptTemplateLocaleBlock",
        sa.Column("PromptTemplateLocaleBlockID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("PromptTemplateID", sa.BigInteger(), nullable=False),
        sa.Column("CountryID", sa.BigInteger(), nullable=True),
        sa.Column("BlockType", mssql.NVARCHAR(length=20), nullable=False),
        sa.Column("BlockBody", mssql.NVARCHAR(length=None), nullable=False),
        sa.Column("ContentHash", mssql.NVARCHAR(length=64), nullable=False),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("1")),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.CheckConstraint(
            "BlockType IN (N'format', N'policy', N'tone')",
            name="CK_PromptTemplateLocaleBlock_BlockType",
        ),
        sa.ForeignKeyConstraint(
            ["PromptTemplateID"],
            ["config.PromptTemplate.PromptTemplateID"],
            name="FK_PromptTemplateLocaleBlock_PromptTemplateID",
        ),
        sa.ForeignKeyConstraint(
            ["CountryID"],
            ["ref.Country.CountryID"],
            name="FK_PromptTemplateLocaleBlock_CountryID",
        ),
        sa.ForeignKeyConstraint(
            ["CreatedBy"], ["dbo.User.UserID"], name="FK_PromptTemplateLocaleBlock_CreatedBy"
        ),
        sa.ForeignKeyConstraint(
            ["UpdatedBy"], ["dbo.User.UserID"], name="FK_PromptTemplateLocaleBlock_UpdatedBy"
        ),
        sa.ForeignKeyConstraint(
            ["DeletedBy"], ["dbo.User.UserID"], name="FK_PromptTemplateLocaleBlock_DeletedBy"
        ),
        sa.PrimaryKeyConstraint("PromptTemplateLocaleBlockID", name="PK_PromptTemplateLocaleBlock"),
        schema="config",
    )
    op.create_index(
        "IX_PromptTemplateLocaleBlock_Template_Country",
        "PromptTemplateLocaleBlock",
        ["PromptTemplateID", "CountryID"],
        unique=False,
        schema="config",
    )
    op.execute(
        """
        CREATE UNIQUE NONCLUSTERED INDEX UQ_PromptTemplateLocaleBlock_Active
        ON [config].[PromptTemplateLocaleBlock] ([PromptTemplateID], [CountryID], [BlockType])
        WHERE [IsActive] = 1 AND [IsDeleted] = 0;
        """
    )


def downgrade() -> None:
    op.execute(
        """
        IF EXISTS (
            SELECT 1
            FROM sys.indexes
            WHERE name = 'UQ_PromptTemplateLocaleBlock_Active'
              AND object_id = OBJECT_ID('config.PromptTemplateLocaleBlock')
        )
        DROP INDEX [UQ_PromptTemplateLocaleBlock_Active]
        ON [config].[PromptTemplateLocaleBlock];
        """
    )
    op.drop_index(
        "IX_PromptTemplateLocaleBlock_Template_Country",
        table_name="PromptTemplateLocaleBlock",
        schema="config",
    )
    op.drop_table("PromptTemplateLocaleBlock", schema="config")
