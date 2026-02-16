"""Story 5.5: Preview/Production Governance Foundations

Revision ID: 041
Revises: 040
Create Date: 2026-02-16

- Add IsPreview to FormSubmission (preview vs production flag)
- Create CompanyFormTestConfig (per-company test threshold)
- Create FormTestRun (explicit 'Record test run' audit)
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

revision = "041"
down_revision = "040"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Add IsPreview to FormSubmission
    op.add_column(
        "FormSubmission",
        sa.Column("IsPreview", mssql.BIT(), nullable=True, server_default=sa.text("0")),
        schema="dbo",
    )
    # Backfill: IsPreview=1 where LinkType='PREVIEW'
    op.execute(
        """
        UPDATE [dbo].[FormSubmission]
        SET [IsPreview] = 1
        WHERE [LinkType] = N'PREVIEW';
        """
    )
    op.alter_column(
        "FormSubmission",
        "IsPreview",
        existing_type=mssql.BIT(),
        nullable=False,
        server_default=sa.text("0"),
        schema="dbo",
    )

    # 2. Create CompanyFormTestConfig
    op.create_table(
        "CompanyFormTestConfig",
        sa.Column("CompanyFormTestConfigID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("CompanyID", sa.BigInteger(), nullable=False),
        sa.Column("TestThresholdEnabled", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("TestThresholdValue", sa.Integer(), nullable=False, server_default=sa.text("3")),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("CompanyFormTestConfigID", name="PK_CompanyFormTestConfig"),
        sa.ForeignKeyConstraint(["CompanyID"], ["dbo.Company.CompanyID"], name="FK_CompanyFormTestConfig_CompanyID"),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_CompanyFormTestConfig_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_CompanyFormTestConfig_UpdatedBy"),
        sa.UniqueConstraint("CompanyID", name="UQ_CompanyFormTestConfig_CompanyID"),
        schema="dbo",
    )
    op.create_index("IX_CompanyFormTestConfig_CompanyID", "CompanyFormTestConfig", ["CompanyID"], unique=True, schema="dbo")

    # 3. Create FormTestRun
    op.create_table(
        "FormTestRun",
        sa.Column("FormTestRunID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("FormID", sa.BigInteger(), nullable=False),
        sa.Column("FormVersionID", sa.BigInteger(), nullable=False),
        sa.Column("CompanyID", sa.BigInteger(), nullable=False),
        sa.Column("RecordedBy", sa.BigInteger(), nullable=False),
        sa.Column("RecordedAt", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.PrimaryKeyConstraint("FormTestRunID", name="PK_FormTestRun"),
        sa.ForeignKeyConstraint(["FormID"], ["dbo.Form.FormID"], name="FK_FormTestRun_FormID"),
        sa.ForeignKeyConstraint(["FormVersionID"], ["dbo.FormVersion.FormVersionID"], name="FK_FormTestRun_FormVersionID"),
        sa.ForeignKeyConstraint(["CompanyID"], ["dbo.Company.CompanyID"], name="FK_FormTestRun_CompanyID"),
        sa.ForeignKeyConstraint(["RecordedBy"], ["dbo.User.UserID"], name="FK_FormTestRun_RecordedBy"),
        schema="dbo",
    )
    op.create_index("IX_FormTestRun_FormID", "FormTestRun", ["FormID"], unique=False, schema="dbo")
    op.create_index("IX_FormTestRun_RecordedAt", "FormTestRun", ["RecordedAt"], unique=False, schema="dbo")


def downgrade() -> None:
    op.drop_index("IX_FormTestRun_RecordedAt", table_name="FormTestRun", schema="dbo")
    op.drop_index("IX_FormTestRun_FormID", table_name="FormTestRun", schema="dbo")
    op.drop_table("FormTestRun", schema="dbo")

    op.drop_index("IX_CompanyFormTestConfig_CompanyID", table_name="CompanyFormTestConfig", schema="dbo")
    op.drop_table("CompanyFormTestConfig", schema="dbo")

    op.drop_column("FormSubmission", "IsPreview", schema="dbo")
