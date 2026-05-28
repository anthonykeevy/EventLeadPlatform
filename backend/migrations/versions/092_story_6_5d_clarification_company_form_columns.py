"""Story 6.5d: Company + Form clarification default/persist columns.

Revision ID: 092
Revises: 091
"""

from alembic import op
import sqlalchemy as sa


revision = "092"
down_revision = "091"
branch_labels = None
depends_on = None


def upgrade() -> None:
    for table, columns in (
        ("Company", ("DefaultAudienceLocaleCode", "DefaultFormPurposeCode", "DefaultRespondentTypeCode")),
        ("Form", ("AudienceLocaleCode", "FormPurposeCode", "RespondentTypeCode")),
    ):
        for col in columns:
            op.execute(
                f"""
                IF COL_LENGTH('dbo.{table}', '{col}') IS NULL
                ALTER TABLE [dbo].[{table}] ADD [{col}] VARCHAR(50) NULL;
                """
            )


def downgrade() -> None:
    for table, columns in (
        ("Form", ("RespondentTypeCode", "FormPurposeCode", "AudienceLocaleCode")),
        ("Company", ("DefaultRespondentTypeCode", "DefaultFormPurposeCode", "DefaultAudienceLocaleCode")),
    ):
        for col in columns:
            op.execute(
                f"""
                IF COL_LENGTH('dbo.{table}', '{col}') IS NOT NULL
                ALTER TABLE [dbo].[{table}] DROP COLUMN [{col}];
                """
            )
