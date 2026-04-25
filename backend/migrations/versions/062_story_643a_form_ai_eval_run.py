"""Story 6.4.3a: Create log.FormAiEvalRun.

Stores repeatable Form AI evaluation harness metrics separately from
log.ApiRequest. GenerationRunID references the current replay/audit table
dbo.GenerationRun introduced by Story 6.3.1.

Revision ID: 062
Revises: 061
Create Date: 2026-04-25
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql


revision = "062"
down_revision = "061"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "FormAiEvalRun",
        sa.Column("EvalRunID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("BenchmarkSetVersion", mssql.NVARCHAR(length=20), nullable=False),
        sa.Column("HypothesisCode", mssql.NVARCHAR(length=20), nullable=False),
        sa.Column("VariantLabel", mssql.NVARCHAR(length=100), nullable=False),
        sa.Column("PromptID", mssql.NVARCHAR(length=80), nullable=False),
        sa.Column("RepetitionIndex", sa.Integer(), nullable=False),
        sa.Column("GenerationRunID", sa.BigInteger(), nullable=True),
        sa.Column("MetricsJSON", mssql.NVARCHAR(length=None), nullable=False),
        sa.Column("JudgeRubricVersion", mssql.NVARCHAR(length=20), nullable=True),
        sa.Column("JudgeAgreementScore", sa.Numeric(precision=5, scale=3), nullable=True),
        sa.Column("BiasDeltaJSON", mssql.NVARCHAR(length=None), nullable=True),
        sa.Column("BaselineExpiresAt", mssql.DATETIME2(), nullable=True),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.ForeignKeyConstraint(
            ["GenerationRunID"],
            ["dbo.GenerationRun.GenerationRunID"],
            name="FK_FormAiEvalRun_GenerationRunID",
        ),
        sa.PrimaryKeyConstraint("EvalRunID", name="PK_FormAiEvalRun"),
        schema="log",
    )
    op.create_index(
        "IX_FormAiEvalRun_Hypothesis_Variant_Prompt",
        "FormAiEvalRun",
        ["HypothesisCode", "VariantLabel", "PromptID"],
        unique=False,
        schema="log",
    )


def downgrade() -> None:
    op.drop_index(
        "IX_FormAiEvalRun_Hypothesis_Variant_Prompt",
        table_name="FormAiEvalRun",
        schema="log",
    )
    op.drop_table("FormAiEvalRun", schema="log")
