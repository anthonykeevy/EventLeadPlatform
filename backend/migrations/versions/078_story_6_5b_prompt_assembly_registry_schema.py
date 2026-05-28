"""Story 6.5b: Prompt Assembly Registry schema (foundation tables for A/B/C/G/I migration).

Revision ID: 078
Revises: 074
Create Date: 2026-05-20

Creates the foundation registry tables required by Story 6.5b:
  * config.PromptAssemblyRegistry            - top-level named profile (e.g. FORM_AI_V1)
  * config.PromptAssemblyRegistryVersion     - versioned activation (one IsActive per registry)
  * config.PromptSection                     - ordered sections (per blocks A/B/C/G/I in 6.5b)
  * config.PromptSectionVariant              - variants per section (variant-level versioning)
  * config.PromptSectionData                 - structured side-data per variant (optional)

Naming note: the architecture document refers to these tables as
  config.PromptAssemblyProfile / PromptAssemblyProfileVersion / ...
The legacy table config.PromptAssemblyProfile already exists from Story 6.3.1
(migration 053) as a runtime governance step profile FK'd from
dbo.GenerationRun.PromptAssemblyProfileID. To avoid colliding with that
table (and the live FK lineage), this story uses the
'PromptAssemblyRegistry' prefix for the new registry tables. The
architecture doc and ERD will be reconciled to the implementation name
in Story 6.5c (carry-forward backlog item).

Per Story 6.5b §2.1 + arch §3 + §8.1 (variant-level versioning columns:
VariantVersion, IsLockedForEdits, ActivatedUtc, optional ExperimentFlag,
RolloutPercent). All audit columns mirror the rest of the codebase.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql


revision = "078"
down_revision = "074"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ------------------------------------------------------------------
    # config.PromptAssemblyRegistry
    # Top-level named profile (e.g. FORM_AI_V1).
    # ------------------------------------------------------------------
    op.create_table(
        "PromptAssemblyRegistry",
        sa.Column("PromptAssemblyRegistryID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("Code", mssql.NVARCHAR(length=120), nullable=False),
        sa.Column("Description", mssql.NVARCHAR(length=1000), nullable=True),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("1")),
        sa.Column("CreatedUtc", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("LastUpdatedUtc", mssql.DATETIME2(), nullable=True),
        sa.Column("LastUpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_PromptAssemblyRegistry_CreatedBy"),
        sa.ForeignKeyConstraint(["LastUpdatedBy"], ["dbo.User.UserID"], name="FK_PromptAssemblyRegistry_LastUpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_PromptAssemblyRegistry_DeletedBy"),
        sa.PrimaryKeyConstraint("PromptAssemblyRegistryID", name="PK_PromptAssemblyRegistry"),
        schema="config",
    )
    op.execute(
        """
        CREATE UNIQUE NONCLUSTERED INDEX UQ_PromptAssemblyRegistry_Code_Active
        ON [config].[PromptAssemblyRegistry] ([Code])
        WHERE [IsDeleted] = 0;
        """
    )

    # ------------------------------------------------------------------
    # config.PromptAssemblyRegistryVersion
    # Versioned activation. Only one IsActive per registry (partial unique).
    # ------------------------------------------------------------------
    op.create_table(
        "PromptAssemblyRegistryVersion",
        sa.Column("PromptAssemblyRegistryVersionID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("PromptAssemblyRegistryID", sa.BigInteger(), nullable=False),
        sa.Column("VersionNumber", sa.Integer(), nullable=False),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("IsLockedForEdits", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("ReleaseNotes", mssql.NVARCHAR(length=2000), nullable=True),
        sa.Column("ActivatedUtc", mssql.DATETIME2(), nullable=True),
        sa.Column("CreatedUtc", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("LastUpdatedUtc", mssql.DATETIME2(), nullable=True),
        sa.Column("LastUpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(
            ["PromptAssemblyRegistryID"],
            ["config.PromptAssemblyRegistry.PromptAssemblyRegistryID"],
            name="FK_PromptAssemblyRegistryVersion_Registry",
        ),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_PromptAssemblyRegistryVersion_CreatedBy"),
        sa.ForeignKeyConstraint(["LastUpdatedBy"], ["dbo.User.UserID"], name="FK_PromptAssemblyRegistryVersion_LastUpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_PromptAssemblyRegistryVersion_DeletedBy"),
        sa.PrimaryKeyConstraint("PromptAssemblyRegistryVersionID", name="PK_PromptAssemblyRegistryVersion"),
        sa.UniqueConstraint(
            "PromptAssemblyRegistryID",
            "VersionNumber",
            name="UQ_PromptAssemblyRegistryVersion_Registry_VersionNumber",
        ),
        schema="config",
    )
    # Only one active version per registry.
    op.execute(
        """
        CREATE UNIQUE NONCLUSTERED INDEX UQ_PromptAssemblyRegistryVersion_Active
        ON [config].[PromptAssemblyRegistryVersion] ([PromptAssemblyRegistryID])
        WHERE [IsActive] = 1 AND [IsDeleted] = 0;
        """
    )

    # ------------------------------------------------------------------
    # config.PromptSection
    # Ordered sections within a registry version.
    # ------------------------------------------------------------------
    op.create_table(
        "PromptSection",
        sa.Column("PromptSectionID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("PromptAssemblyRegistryVersionID", sa.BigInteger(), nullable=False),
        sa.Column("SectionCode", mssql.NVARCHAR(length=10), nullable=False),
        sa.Column("DisplayName", mssql.NVARCHAR(length=200), nullable=False),
        sa.Column("SortOrder", sa.Integer(), nullable=False),
        sa.Column("IsRequired", mssql.BIT(), nullable=False, server_default=sa.text("1")),
        sa.Column("DataStructureType", mssql.NVARCHAR(length=20), nullable=False),
        sa.Column("Heading", mssql.NVARCHAR(length=200), nullable=True),
        sa.Column("CreatedUtc", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("LastUpdatedUtc", mssql.DATETIME2(), nullable=True),
        sa.Column("LastUpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(
            ["PromptAssemblyRegistryVersionID"],
            ["config.PromptAssemblyRegistryVersion.PromptAssemblyRegistryVersionID"],
            name="FK_PromptSection_RegistryVersion",
        ),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_PromptSection_CreatedBy"),
        sa.ForeignKeyConstraint(["LastUpdatedBy"], ["dbo.User.UserID"], name="FK_PromptSection_LastUpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_PromptSection_DeletedBy"),
        sa.CheckConstraint(
            "[DataStructureType] IN (N'Prose', N'Json', N'Snapshot', N'Refs')",
            name="CK_PromptSection_DataStructureType",
        ),
        sa.PrimaryKeyConstraint("PromptSectionID", name="PK_PromptSection"),
        sa.UniqueConstraint(
            "PromptAssemblyRegistryVersionID",
            "SectionCode",
            name="UQ_PromptSection_Version_SectionCode",
        ),
        schema="config",
    )
    op.create_index(
        "IX_PromptSection_Version_SortOrder",
        "PromptSection",
        ["PromptAssemblyRegistryVersionID", "SortOrder"],
        unique=False,
        schema="config",
    )

    # ------------------------------------------------------------------
    # config.PromptSectionVariant
    # Variants per section. Variant-level versioning per arch §8.1.
    # ------------------------------------------------------------------
    op.create_table(
        "PromptSectionVariant",
        sa.Column("PromptSectionVariantID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("PromptSectionID", sa.BigInteger(), nullable=False),
        sa.Column("VariantCode", mssql.NVARCHAR(length=50), nullable=False),
        sa.Column("DisplayName", mssql.NVARCHAR(length=200), nullable=True),
        sa.Column("Description", mssql.NVARCHAR(length=1000), nullable=True),
        sa.Column("IsDefault", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("PromptSnippet", mssql.NVARCHAR(length=None), nullable=False),  # NVARCHAR(MAX)
        sa.Column("SchemaJson", mssql.NVARCHAR(length=None), nullable=True),
        sa.Column("VariantVersion", sa.Integer(), nullable=False, server_default=sa.text("1")),
        sa.Column("IsLockedForEdits", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("ActivatedUtc", mssql.DATETIME2(), nullable=True),
        sa.Column("ExperimentFlag", mssql.NVARCHAR(length=80), nullable=True),
        sa.Column("RolloutPercent", sa.SmallInteger(), nullable=True),
        sa.Column("ChangeReason", mssql.NVARCHAR(length=500), nullable=True),
        sa.Column("CreatedUtc", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("LastUpdatedUtc", mssql.DATETIME2(), nullable=True),
        sa.Column("LastUpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(
            ["PromptSectionID"],
            ["config.PromptSection.PromptSectionID"],
            name="FK_PromptSectionVariant_Section",
        ),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_PromptSectionVariant_CreatedBy"),
        sa.ForeignKeyConstraint(["LastUpdatedBy"], ["dbo.User.UserID"], name="FK_PromptSectionVariant_LastUpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_PromptSectionVariant_DeletedBy"),
        sa.PrimaryKeyConstraint("PromptSectionVariantID", name="PK_PromptSectionVariant"),
        schema="config",
    )
    # VariantCode is unique within a section per active version (one row per VariantCode while not soft-deleted).
    op.execute(
        """
        CREATE UNIQUE NONCLUSTERED INDEX UQ_PromptSectionVariant_Section_VariantCode
        ON [config].[PromptSectionVariant] ([PromptSectionID], [VariantCode])
        WHERE [IsDeleted] = 0;
        """
    )
    # Only one IsDefault=1 per section.
    op.execute(
        """
        CREATE UNIQUE NONCLUSTERED INDEX UQ_PromptSectionVariant_DefaultPerSection
        ON [config].[PromptSectionVariant] ([PromptSectionID])
        WHERE [IsDefault] = 1 AND [IsDeleted] = 0;
        """
    )

    # ------------------------------------------------------------------
    # config.PromptSectionData
    # Structured side-data per variant (e.g. PROHIBITED_TOPICS, ALLOWED_COMPONENTS).
    # Optional in 6.5b; added to schema so 6.5c/6.5d can use it without another migration.
    # ------------------------------------------------------------------
    op.create_table(
        "PromptSectionData",
        sa.Column("PromptSectionDataID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("PromptSectionVariantID", sa.BigInteger(), nullable=False),
        sa.Column("DataKey", mssql.NVARCHAR(length=120), nullable=False),
        sa.Column("DataValue", mssql.NVARCHAR(length=None), nullable=False),  # NVARCHAR(MAX)
        sa.Column("DataType", mssql.NVARCHAR(length=30), nullable=False),
        sa.Column("SortOrder", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("CreatedUtc", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("LastUpdatedUtc", mssql.DATETIME2(), nullable=True),
        sa.Column("LastUpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(
            ["PromptSectionVariantID"],
            ["config.PromptSectionVariant.PromptSectionVariantID"],
            name="FK_PromptSectionData_Variant",
        ),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_PromptSectionData_CreatedBy"),
        sa.ForeignKeyConstraint(["LastUpdatedBy"], ["dbo.User.UserID"], name="FK_PromptSectionData_LastUpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_PromptSectionData_DeletedBy"),
        sa.CheckConstraint(
            "[DataType] IN (N'Json', N'Csv', N'Text', N'Reference')",
            name="CK_PromptSectionData_DataType",
        ),
        sa.PrimaryKeyConstraint("PromptSectionDataID", name="PK_PromptSectionData"),
        sa.UniqueConstraint(
            "PromptSectionVariantID",
            "DataKey",
            name="UQ_PromptSectionData_Variant_DataKey",
        ),
        schema="config",
    )


def downgrade() -> None:
    # Drop in reverse FK order so children go before parents.
    op.drop_table("PromptSectionData", schema="config")

    # Drop the partial UQs/indexes we created with raw SQL before dropping
    # the variant table (Alembic will not infer them).
    op.execute(
        """
        IF EXISTS (
            SELECT 1
            FROM sys.indexes
            WHERE name = 'UQ_PromptSectionVariant_DefaultPerSection'
              AND object_id = OBJECT_ID('config.PromptSectionVariant')
        )
        DROP INDEX [UQ_PromptSectionVariant_DefaultPerSection] ON [config].[PromptSectionVariant];
        """
    )
    op.execute(
        """
        IF EXISTS (
            SELECT 1
            FROM sys.indexes
            WHERE name = 'UQ_PromptSectionVariant_Section_VariantCode'
              AND object_id = OBJECT_ID('config.PromptSectionVariant')
        )
        DROP INDEX [UQ_PromptSectionVariant_Section_VariantCode] ON [config].[PromptSectionVariant];
        """
    )
    op.drop_table("PromptSectionVariant", schema="config")

    op.drop_index(
        "IX_PromptSection_Version_SortOrder",
        table_name="PromptSection",
        schema="config",
    )
    op.drop_table("PromptSection", schema="config")

    op.execute(
        """
        IF EXISTS (
            SELECT 1
            FROM sys.indexes
            WHERE name = 'UQ_PromptAssemblyRegistryVersion_Active'
              AND object_id = OBJECT_ID('config.PromptAssemblyRegistryVersion')
        )
        DROP INDEX [UQ_PromptAssemblyRegistryVersion_Active] ON [config].[PromptAssemblyRegistryVersion];
        """
    )
    op.drop_table("PromptAssemblyRegistryVersion", schema="config")

    op.execute(
        """
        IF EXISTS (
            SELECT 1
            FROM sys.indexes
            WHERE name = 'UQ_PromptAssemblyRegistry_Code_Active'
              AND object_id = OBJECT_ID('config.PromptAssemblyRegistry')
        )
        DROP INDEX [UQ_PromptAssemblyRegistry_Code_Active] ON [config].[PromptAssemblyRegistry];
        """
    )
    op.drop_table("PromptAssemblyRegistry", schema="config")
