"""Story 6.5d: GenerationRun clarification audit columns.

Revision ID: 093
Revises: 092
"""

from alembic import op


revision = "093"
down_revision = "092"
branch_labels = None
depends_on = None


def upgrade() -> None:
    for col in (
        "AudienceLocaleCode",
        "FormPurposeCode",
        "RespondentTypeCode",
    ):
        op.execute(
            f"""
            IF COL_LENGTH('dbo.GenerationRun', '{col}') IS NULL
            ALTER TABLE [dbo].[GenerationRun] ADD [{col}] VARCHAR(50) NULL;
            """
        )


def downgrade() -> None:
    for col in ("RespondentTypeCode", "FormPurposeCode", "AudienceLocaleCode"):
        op.execute(
            f"""
            IF COL_LENGTH('dbo.GenerationRun', '{col}') IS NOT NULL
            ALTER TABLE [dbo].[GenerationRun] DROP COLUMN [{col}];
            """
        )
