"""Story 6.3.1: Form AI governance and traceability foundation tables.

Revision ID: 053
Revises: 052
Create Date: 2026-04-15
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql


revision = "053"
down_revision = "052"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Prompt registry: template metadata.
    op.create_table(
        "PromptTemplate",
        sa.Column("PromptTemplateID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("TemplateKey", mssql.NVARCHAR(length=120), nullable=False),
        sa.Column("TemplateName", mssql.NVARCHAR(length=200), nullable=False),
        sa.Column("Purpose", mssql.NVARCHAR(length=500), nullable=True),
        sa.Column("Owner", mssql.NVARCHAR(length=200), nullable=True),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("1")),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_PromptTemplate_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_PromptTemplate_UpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_PromptTemplate_DeletedBy"),
        sa.PrimaryKeyConstraint("PromptTemplateID", name="PK_PromptTemplate"),
        schema="config",
    )
    op.create_index(
        "IX_PromptTemplate_TemplateKey",
        "PromptTemplate",
        ["TemplateKey"],
        unique=False,
        schema="config",
    )
    op.execute(
        """
        CREATE UNIQUE NONCLUSTERED INDEX UQ_PromptTemplate_TemplateKey_Active
        ON [config].[PromptTemplate] ([TemplateKey])
        WHERE [IsDeleted] = 0;
        """
    )

    # Prompt registry: immutable template versions.
    op.create_table(
        "PromptTemplateVersion",
        sa.Column("PromptTemplateVersionID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("PromptTemplateID", sa.BigInteger(), nullable=False),
        sa.Column("VersionNumber", sa.Integer(), nullable=False),
        sa.Column("VersionLabel", mssql.NVARCHAR(length=80), nullable=True),
        sa.Column("TemplateBody", mssql.NVARCHAR(length=None), nullable=False),
        sa.Column("ChangeSummary", mssql.NVARCHAR(length=1000), nullable=True),
        sa.Column("ContentHash", mssql.NVARCHAR(length=64), nullable=False),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("ActivatedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("RetiredDate", mssql.DATETIME2(), nullable=True),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(
            ["PromptTemplateID"],
            ["config.PromptTemplate.PromptTemplateID"],
            name="FK_PromptTemplateVersion_PromptTemplateID",
        ),
        sa.ForeignKeyConstraint(
            ["CreatedBy"], ["dbo.User.UserID"], name="FK_PromptTemplateVersion_CreatedBy"
        ),
        sa.ForeignKeyConstraint(
            ["UpdatedBy"], ["dbo.User.UserID"], name="FK_PromptTemplateVersion_UpdatedBy"
        ),
        sa.ForeignKeyConstraint(
            ["DeletedBy"], ["dbo.User.UserID"], name="FK_PromptTemplateVersion_DeletedBy"
        ),
        sa.PrimaryKeyConstraint("PromptTemplateVersionID", name="PK_PromptTemplateVersion"),
        sa.UniqueConstraint(
            "PromptTemplateID",
            "VersionNumber",
            name="UQ_PromptTemplateVersion_Template_Version",
        ),
        schema="config",
    )
    op.create_index(
        "IX_PromptTemplateVersion_Template",
        "PromptTemplateVersion",
        ["PromptTemplateID", "IsActive"],
        unique=False,
        schema="config",
    )
    op.create_index(
        "IX_PromptTemplateVersion_ContentHash",
        "PromptTemplateVersion",
        ["ContentHash"],
        unique=False,
        schema="config",
    )

    # Capability policy governance.
    op.create_table(
        "CapabilityPolicyVersion",
        sa.Column("CapabilityPolicyVersionID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("PolicyKey", mssql.NVARCHAR(length=120), nullable=False),
        sa.Column("VersionNumber", sa.Integer(), nullable=False),
        sa.Column("PolicyJson", mssql.NVARCHAR(length=None), nullable=False),
        sa.Column("PolicyHash", mssql.NVARCHAR(length=64), nullable=False),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("ActivatedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("RetiredDate", mssql.DATETIME2(), nullable=True),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(
            ["CreatedBy"], ["dbo.User.UserID"], name="FK_CapabilityPolicyVersion_CreatedBy"
        ),
        sa.ForeignKeyConstraint(
            ["UpdatedBy"], ["dbo.User.UserID"], name="FK_CapabilityPolicyVersion_UpdatedBy"
        ),
        sa.ForeignKeyConstraint(
            ["DeletedBy"], ["dbo.User.UserID"], name="FK_CapabilityPolicyVersion_DeletedBy"
        ),
        sa.PrimaryKeyConstraint("CapabilityPolicyVersionID", name="PK_CapabilityPolicyVersion"),
        sa.UniqueConstraint(
            "PolicyKey",
            "VersionNumber",
            name="UQ_CapabilityPolicyVersion_Key_Version",
        ),
        schema="config",
    )
    op.create_index(
        "IX_CapabilityPolicyVersion_Active",
        "CapabilityPolicyVersion",
        ["PolicyKey", "IsActive"],
        unique=False,
        schema="config",
    )

    # Framework-derived capability snapshot (versioned manifest).
    op.create_table(
        "ComponentCapabilitySnapshot",
        sa.Column("ComponentCapabilitySnapshotID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("SnapshotVersion", mssql.NVARCHAR(length=80), nullable=False),
        sa.Column("SnapshotJson", mssql.NVARCHAR(length=None), nullable=False),
        sa.Column("SourceManifestHash", mssql.NVARCHAR(length=64), nullable=False),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("GeneratedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(
            ["CreatedBy"], ["dbo.User.UserID"], name="FK_ComponentCapabilitySnapshot_CreatedBy"
        ),
        sa.ForeignKeyConstraint(
            ["UpdatedBy"], ["dbo.User.UserID"], name="FK_ComponentCapabilitySnapshot_UpdatedBy"
        ),
        sa.ForeignKeyConstraint(
            ["DeletedBy"], ["dbo.User.UserID"], name="FK_ComponentCapabilitySnapshot_DeletedBy"
        ),
        sa.PrimaryKeyConstraint(
            "ComponentCapabilitySnapshotID",
            name="PK_ComponentCapabilitySnapshot",
        ),
        sa.UniqueConstraint("SnapshotVersion", name="UQ_ComponentCapabilitySnapshot_SnapshotVersion"),
        schema="config",
    )
    op.create_index(
        "IX_ComponentCapabilitySnapshot_Active",
        "ComponentCapabilitySnapshot",
        ["IsActive", "GeneratedDate"],
        unique=False,
        schema="config",
    )

    # Per-component validation contract.
    op.create_table(
        "ComponentValidationContract",
        sa.Column("ComponentValidationContractID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("ComponentType", mssql.NVARCHAR(length=80), nullable=False),
        sa.Column("ContractVersion", mssql.NVARCHAR(length=80), nullable=False),
        sa.Column("AllowedRulesJson", mssql.NVARCHAR(length=None), nullable=False),
        sa.Column("RuleParameterSchemaJson", mssql.NVARCHAR(length=None), nullable=False),
        sa.Column("RuleCompatibilityJson", mssql.NVARCHAR(length=None), nullable=True),
        sa.Column("MessagePolicyJson", mssql.NVARCHAR(length=None), nullable=True),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("1")),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(
            ["CreatedBy"], ["dbo.User.UserID"], name="FK_ComponentValidationContract_CreatedBy"
        ),
        sa.ForeignKeyConstraint(
            ["UpdatedBy"], ["dbo.User.UserID"], name="FK_ComponentValidationContract_UpdatedBy"
        ),
        sa.ForeignKeyConstraint(
            ["DeletedBy"], ["dbo.User.UserID"], name="FK_ComponentValidationContract_DeletedBy"
        ),
        sa.PrimaryKeyConstraint(
            "ComponentValidationContractID",
            name="PK_ComponentValidationContract",
        ),
        sa.UniqueConstraint(
            "ComponentType",
            "ContractVersion",
            name="UQ_ComponentValidationContract_Component_Version",
        ),
        schema="config",
    )
    op.create_index(
        "IX_ComponentValidationContract_Active",
        "ComponentValidationContract",
        ["ComponentType", "IsActive"],
        unique=False,
        schema="config",
    )

    # Width class policy versioning (compact/half/full resolution governance).
    op.create_table(
        "WidthClassPolicyVersion",
        sa.Column("WidthClassPolicyVersionID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("PolicyKey", mssql.NVARCHAR(length=120), nullable=False),
        sa.Column("VersionNumber", sa.Integer(), nullable=False),
        sa.Column("PolicyJson", mssql.NVARCHAR(length=None), nullable=False),
        sa.Column("PolicyHash", mssql.NVARCHAR(length=64), nullable=False),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("ActivatedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("RetiredDate", mssql.DATETIME2(), nullable=True),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(
            ["CreatedBy"], ["dbo.User.UserID"], name="FK_WidthClassPolicyVersion_CreatedBy"
        ),
        sa.ForeignKeyConstraint(
            ["UpdatedBy"], ["dbo.User.UserID"], name="FK_WidthClassPolicyVersion_UpdatedBy"
        ),
        sa.ForeignKeyConstraint(
            ["DeletedBy"], ["dbo.User.UserID"], name="FK_WidthClassPolicyVersion_DeletedBy"
        ),
        sa.PrimaryKeyConstraint("WidthClassPolicyVersionID", name="PK_WidthClassPolicyVersion"),
        sa.UniqueConstraint(
            "PolicyKey",
            "VersionNumber",
            name="UQ_WidthClassPolicyVersion_Key_Version",
        ),
        schema="config",
    )
    op.create_index(
        "IX_WidthClassPolicyVersion_Active",
        "WidthClassPolicyVersion",
        ["PolicyKey", "IsActive"],
        unique=False,
        schema="config",
    )

    # Prompt assembly profile links template versions and policies used by runtime.
    op.create_table(
        "PromptAssemblyProfile",
        sa.Column("PromptAssemblyProfileID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("ProfileKey", mssql.NVARCHAR(length=120), nullable=False),
        sa.Column("ProfileName", mssql.NVARCHAR(length=200), nullable=False),
        sa.Column("StepName", mssql.NVARCHAR(length=40), nullable=False),
        sa.Column("Description", mssql.NVARCHAR(length=1000), nullable=True),
        sa.Column("PromptTemplateVersionID", sa.BigInteger(), nullable=False),
        sa.Column("CapabilityPolicyVersionID", sa.BigInteger(), nullable=True),
        sa.Column("WidthClassPolicyVersionID", sa.BigInteger(), nullable=True),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("1")),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(
            ["PromptTemplateVersionID"],
            ["config.PromptTemplateVersion.PromptTemplateVersionID"],
            name="FK_PromptAssemblyProfile_PromptTemplateVersionID",
        ),
        sa.ForeignKeyConstraint(
            ["CapabilityPolicyVersionID"],
            ["config.CapabilityPolicyVersion.CapabilityPolicyVersionID"],
            name="FK_PromptAssemblyProfile_CapabilityPolicyVersionID",
        ),
        sa.ForeignKeyConstraint(
            ["WidthClassPolicyVersionID"],
            ["config.WidthClassPolicyVersion.WidthClassPolicyVersionID"],
            name="FK_PromptAssemblyProfile_WidthClassPolicyVersionID",
        ),
        sa.ForeignKeyConstraint(
            ["CreatedBy"], ["dbo.User.UserID"], name="FK_PromptAssemblyProfile_CreatedBy"
        ),
        sa.ForeignKeyConstraint(
            ["UpdatedBy"], ["dbo.User.UserID"], name="FK_PromptAssemblyProfile_UpdatedBy"
        ),
        sa.ForeignKeyConstraint(
            ["DeletedBy"], ["dbo.User.UserID"], name="FK_PromptAssemblyProfile_DeletedBy"
        ),
        sa.PrimaryKeyConstraint("PromptAssemblyProfileID", name="PK_PromptAssemblyProfile"),
        schema="config",
    )
    op.create_index(
        "IX_PromptAssemblyProfile_ProfileKey",
        "PromptAssemblyProfile",
        ["ProfileKey"],
        unique=False,
        schema="config",
    )
    op.execute(
        """
        CREATE UNIQUE NONCLUSTERED INDEX UQ_PromptAssemblyProfile_ProfileKey_Active
        ON [config].[PromptAssemblyProfile] ([ProfileKey], [StepName])
        WHERE [IsDeleted] = 0;
        """
    )

    # Per-request generation run metadata to support replay/audit.
    op.create_table(
        "GenerationRun",
        sa.Column("GenerationRunID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("RequestID", mssql.NVARCHAR(length=100), nullable=False),
        sa.Column("CompanyID", sa.BigInteger(), nullable=True),
        sa.Column("FormID", sa.BigInteger(), nullable=True),
        sa.Column("PromptTemplateVersionID", sa.BigInteger(), nullable=True),
        sa.Column("PromptAssemblyProfileID", sa.BigInteger(), nullable=True),
        sa.Column("CapabilityPolicyVersionID", sa.BigInteger(), nullable=True),
        sa.Column("ComponentCapabilitySnapshotID", sa.BigInteger(), nullable=True),
        sa.Column("WidthClassPolicyVersionID", sa.BigInteger(), nullable=True),
        sa.Column("ValidationContractVersion", mssql.NVARCHAR(length=80), nullable=True),
        sa.Column("PromptHash", mssql.NVARCHAR(length=64), nullable=True),
        sa.Column("RuntimeContextHash", mssql.NVARCHAR(length=64), nullable=True),
        sa.Column("Status", mssql.NVARCHAR(length=32), nullable=False),
        sa.Column("TerminalReason", mssql.NVARCHAR(length=80), nullable=True),
        sa.Column("AttemptCount", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("FirstShotValid", mssql.BIT(), nullable=True),
        sa.Column("IsReplayable", mssql.BIT(), nullable=False, server_default=sa.text("1")),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(["CompanyID"], ["dbo.Company.CompanyID"], name="FK_GenerationRun_CompanyID"),
        sa.ForeignKeyConstraint(["FormID"], ["dbo.Form.FormID"], name="FK_GenerationRun_FormID"),
        sa.ForeignKeyConstraint(
            ["PromptTemplateVersionID"],
            ["config.PromptTemplateVersion.PromptTemplateVersionID"],
            name="FK_GenerationRun_PromptTemplateVersionID",
        ),
        sa.ForeignKeyConstraint(
            ["PromptAssemblyProfileID"],
            ["config.PromptAssemblyProfile.PromptAssemblyProfileID"],
            name="FK_GenerationRun_PromptAssemblyProfileID",
        ),
        sa.ForeignKeyConstraint(
            ["CapabilityPolicyVersionID"],
            ["config.CapabilityPolicyVersion.CapabilityPolicyVersionID"],
            name="FK_GenerationRun_CapabilityPolicyVersionID",
        ),
        sa.ForeignKeyConstraint(
            ["ComponentCapabilitySnapshotID"],
            ["config.ComponentCapabilitySnapshot.ComponentCapabilitySnapshotID"],
            name="FK_GenerationRun_ComponentCapabilitySnapshotID",
        ),
        sa.ForeignKeyConstraint(
            ["WidthClassPolicyVersionID"],
            ["config.WidthClassPolicyVersion.WidthClassPolicyVersionID"],
            name="FK_GenerationRun_WidthClassPolicyVersionID",
        ),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_GenerationRun_CreatedBy"),
        sa.PrimaryKeyConstraint("GenerationRunID", name="PK_GenerationRun"),
        schema="dbo",
    )
    op.create_index(
        "IX_GenerationRun_RequestID",
        "GenerationRun",
        ["RequestID"],
        unique=False,
        schema="dbo",
    )
    op.create_index(
        "IX_GenerationRun_CreatedDate",
        "GenerationRun",
        ["CreatedDate"],
        unique=False,
        schema="dbo",
    )
    op.create_index(
        "IX_GenerationRun_FormID_CreatedDate",
        "GenerationRun",
        ["FormID", "CreatedDate"],
        unique=False,
        schema="dbo",
    )

    # Raw semantic plan, normalized plan, final definition and trace blobs.
    op.create_table(
        "GenerationArtifact",
        sa.Column("GenerationArtifactID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("GenerationRunID", sa.BigInteger(), nullable=False),
        sa.Column("ArtifactType", mssql.NVARCHAR(length=60), nullable=False),
        sa.Column("SequenceNumber", sa.Integer(), nullable=False, server_default=sa.text("1")),
        sa.Column("ArtifactJson", mssql.NVARCHAR(length=None), nullable=False),
        sa.Column("ArtifactHash", mssql.NVARCHAR(length=64), nullable=True),
        sa.Column("IsCompressed", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(
            ["GenerationRunID"],
            ["dbo.GenerationRun.GenerationRunID"],
            name="FK_GenerationArtifact_GenerationRunID",
        ),
        sa.ForeignKeyConstraint(
            ["CreatedBy"], ["dbo.User.UserID"], name="FK_GenerationArtifact_CreatedBy"
        ),
        sa.PrimaryKeyConstraint("GenerationArtifactID", name="PK_GenerationArtifact"),
        sa.UniqueConstraint(
            "GenerationRunID",
            "ArtifactType",
            "SequenceNumber",
            name="UQ_GenerationArtifact_Run_Type_Sequence",
        ),
        schema="dbo",
    )
    op.create_index(
        "IX_GenerationArtifact_GenerationRunID",
        "GenerationArtifact",
        ["GenerationRunID"],
        unique=False,
        schema="dbo",
    )


def downgrade() -> None:
    op.drop_index("IX_GenerationArtifact_GenerationRunID", table_name="GenerationArtifact", schema="dbo")
    op.drop_table("GenerationArtifact", schema="dbo")

    op.drop_index("IX_GenerationRun_FormID_CreatedDate", table_name="GenerationRun", schema="dbo")
    op.drop_index("IX_GenerationRun_CreatedDate", table_name="GenerationRun", schema="dbo")
    op.drop_index("IX_GenerationRun_RequestID", table_name="GenerationRun", schema="dbo")
    op.drop_table("GenerationRun", schema="dbo")

    op.execute(
        """
        IF EXISTS (
            SELECT 1
            FROM sys.indexes
            WHERE name = 'UQ_PromptAssemblyProfile_ProfileKey_Active'
              AND object_id = OBJECT_ID('config.PromptAssemblyProfile')
        )
        DROP INDEX [UQ_PromptAssemblyProfile_ProfileKey_Active] ON [config].[PromptAssemblyProfile];
        """
    )
    op.drop_index("IX_PromptAssemblyProfile_ProfileKey", table_name="PromptAssemblyProfile", schema="config")
    op.drop_table("PromptAssemblyProfile", schema="config")

    op.drop_index("IX_WidthClassPolicyVersion_Active", table_name="WidthClassPolicyVersion", schema="config")
    op.drop_table("WidthClassPolicyVersion", schema="config")

    op.drop_index(
        "IX_ComponentValidationContract_Active",
        table_name="ComponentValidationContract",
        schema="config",
    )
    op.drop_table("ComponentValidationContract", schema="config")

    op.drop_index(
        "IX_ComponentCapabilitySnapshot_Active",
        table_name="ComponentCapabilitySnapshot",
        schema="config",
    )
    op.drop_table("ComponentCapabilitySnapshot", schema="config")

    op.drop_index("IX_CapabilityPolicyVersion_Active", table_name="CapabilityPolicyVersion", schema="config")
    op.drop_table("CapabilityPolicyVersion", schema="config")

    op.drop_index("IX_PromptTemplateVersion_ContentHash", table_name="PromptTemplateVersion", schema="config")
    op.drop_index("IX_PromptTemplateVersion_Template", table_name="PromptTemplateVersion", schema="config")
    op.drop_table("PromptTemplateVersion", schema="config")

    op.execute(
        """
        IF EXISTS (
            SELECT 1
            FROM sys.indexes
            WHERE name = 'UQ_PromptTemplate_TemplateKey_Active'
              AND object_id = OBJECT_ID('config.PromptTemplate')
        )
        DROP INDEX [UQ_PromptTemplate_TemplateKey_Active] ON [config].[PromptTemplate];
        """
    )
    op.drop_index("IX_PromptTemplate_TemplateKey", table_name="PromptTemplate", schema="config")
    op.drop_table("PromptTemplate", schema="config")
