"""Story 6.5b: Extend dbo.GenerationRun for prompt-assembly replayability.

Revision ID: 082
Revises: 081
Create Date: 2026-05-20

Adds two columns to dbo.GenerationRun for full replayability of which
registry rows were used at generation time:

  * PromptAssemblyRegistryVersionID INT NULL
      FK to config.PromptAssemblyRegistryVersion(PromptAssemblyRegistryVersionID).
      Captures which active registry version was resolved for the run.
      Audit-joinable for "show me every run that used FORM_AI_V1 v1".

  * PromptVariantSnapshot NVARCHAR(MAX) NULL
      JSON object of per-block variant IDs:
      `{"A": <id>, "B": <id>, "C": <id>, "G": <id>, "I": <id>}`.
      Sorted-keys serialised by service.py so the column value is a
      stable hash target for diff/replay tooling. NULL on rows persisted
      before this story or when the registry path was bypassed (eval
      fixtures with capability_snapshot_json overrides etc.).

Naming note: the existing column dbo.GenerationRun.PromptAssemblyProfileID
is preserved unchanged. It refers to the legacy 6.3.1 governance step
profile (config.PromptAssemblyProfile), which is a different concept
from the new registry. See migration 078 docstring for full naming
rationale.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql


revision = "082"
down_revision = "081"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "GenerationRun",
        sa.Column("PromptAssemblyRegistryVersionID", sa.BigInteger(), nullable=True),
        schema="dbo",
    )
    op.add_column(
        "GenerationRun",
        sa.Column("PromptVariantSnapshot", mssql.NVARCHAR(length=None), nullable=True),
        schema="dbo",
    )
    op.create_foreign_key(
        "FK_GenerationRun_PromptAssemblyRegistryVersionID",
        source_table="GenerationRun",
        referent_table="PromptAssemblyRegistryVersion",
        local_cols=["PromptAssemblyRegistryVersionID"],
        remote_cols=["PromptAssemblyRegistryVersionID"],
        source_schema="dbo",
        referent_schema="config",
    )
    op.create_index(
        "IX_GenerationRun_PromptAssemblyRegistryVersionID",
        "GenerationRun",
        ["PromptAssemblyRegistryVersionID"],
        unique=False,
        schema="dbo",
    )


def downgrade() -> None:
    op.drop_index(
        "IX_GenerationRun_PromptAssemblyRegistryVersionID",
        table_name="GenerationRun",
        schema="dbo",
    )
    op.drop_constraint(
        "FK_GenerationRun_PromptAssemblyRegistryVersionID",
        "GenerationRun",
        schema="dbo",
        type_="foreignkey",
    )
    op.drop_column("GenerationRun", "PromptVariantSnapshot", schema="dbo")
    op.drop_column("GenerationRun", "PromptAssemblyRegistryVersionID", schema="dbo")
