"""Knowledge Base (kb schema) - Ideas, Aspects, Relations, and Kaizen Review Queue

Revision ID: 036
Revises: 035
Create Date: 2026-02-08

Purpose:
- Add kb schema for an SQL-authoritative knowledge base:
  - Aspects (durable dossiers)
  - Ideas (incubation before GitHub work items)
  - Typed relationships (avoid context blowouts)
  - Session notes (capture decision context from chats)
  - Doc refs (section-level references via stable anchors + optional commit SHA)
  - Review queue + stored proc for Kaizen-style impact reviews
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql


# revision identifiers, used by Alembic.
revision = "036"
down_revision = "035"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # -------------------------------------------------------------------------
    # Schema
    # -------------------------------------------------------------------------
    op.execute(
        "IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'kb') EXEC('CREATE SCHEMA [kb]')"
    )

    # -------------------------------------------------------------------------
    # Reference tables
    # -------------------------------------------------------------------------
    op.create_table(
        "MaturityLevel",
        sa.Column("MaturityLevelID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("LevelCode", mssql.NVARCHAR(length=10), nullable=False),
        sa.Column("LevelName", mssql.NVARCHAR(length=100), nullable=False),
        sa.Column("Description", mssql.NVARCHAR(length=500), nullable=True),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("1")),
        sa.Column("SortOrder", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("MaturityLevelID", name="PK_MaturityLevel_MaturityLevelID"),
        sa.UniqueConstraint("LevelCode", name="UQ_MaturityLevel_LevelCode"),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_MaturityLevel_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_MaturityLevel_UpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_MaturityLevel_DeletedBy"),
        schema="kb",
    )
    op.create_index("IX_MaturityLevel_SortOrder", "MaturityLevel", ["SortOrder"], unique=False, schema="kb")

    op.create_table(
        "AspectState",
        sa.Column("AspectStateID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("StateCode", mssql.NVARCHAR(length=50), nullable=False),
        sa.Column("StateName", mssql.NVARCHAR(length=100), nullable=False),
        sa.Column("Description", mssql.NVARCHAR(length=500), nullable=True),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("1")),
        sa.Column("SortOrder", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("AspectStateID", name="PK_AspectState_AspectStateID"),
        sa.UniqueConstraint("StateCode", name="UQ_AspectState_StateCode"),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_AspectState_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_AspectState_UpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_AspectState_DeletedBy"),
        schema="kb",
    )

    op.create_table(
        "IdeaStatus",
        sa.Column("IdeaStatusID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("StatusCode", mssql.NVARCHAR(length=50), nullable=False),
        sa.Column("StatusName", mssql.NVARCHAR(length=100), nullable=False),
        sa.Column("Description", mssql.NVARCHAR(length=500), nullable=True),
        sa.Column("IsTerminal", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("1")),
        sa.Column("SortOrder", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("IdeaStatusID", name="PK_IdeaStatus_IdeaStatusID"),
        sa.UniqueConstraint("StatusCode", name="UQ_IdeaStatus_StatusCode"),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_IdeaStatus_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_IdeaStatus_UpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_IdeaStatus_DeletedBy"),
        schema="kb",
    )

    op.create_table(
        "RelationType",
        sa.Column("RelationTypeID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("TypeCode", mssql.NVARCHAR(length=50), nullable=False),
        sa.Column("TypeName", mssql.NVARCHAR(length=100), nullable=False),
        sa.Column("Description", mssql.NVARCHAR(length=500), nullable=True),
        sa.Column("IsSymmetric", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("1")),
        sa.Column("SortOrder", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("RelationTypeID", name="PK_RelationType_RelationTypeID"),
        sa.UniqueConstraint("TypeCode", name="UQ_RelationType_TypeCode"),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_RelationType_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_RelationType_UpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_RelationType_DeletedBy"),
        schema="kb",
    )

    op.create_table(
        "WorkItemType",
        sa.Column("WorkItemTypeID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("TypeCode", mssql.NVARCHAR(length=50), nullable=False),
        sa.Column("TypeName", mssql.NVARCHAR(length=100), nullable=False),
        sa.Column("Description", mssql.NVARCHAR(length=500), nullable=True),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("1")),
        sa.Column("SortOrder", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("WorkItemTypeID", name="PK_WorkItemType_WorkItemTypeID"),
        sa.UniqueConstraint("TypeCode", name="UQ_WorkItemType_TypeCode"),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_WorkItemType_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_WorkItemType_UpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_WorkItemType_DeletedBy"),
        schema="kb",
    )

    op.create_table(
        "ReviewTaskStatus",
        sa.Column("ReviewTaskStatusID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("StatusCode", mssql.NVARCHAR(length=50), nullable=False),
        sa.Column("StatusName", mssql.NVARCHAR(length=100), nullable=False),
        sa.Column("Description", mssql.NVARCHAR(length=500), nullable=True),
        sa.Column("IsTerminal", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("1")),
        sa.Column("SortOrder", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("ReviewTaskStatusID", name="PK_ReviewTaskStatus_ReviewTaskStatusID"),
        sa.UniqueConstraint("StatusCode", name="UQ_ReviewTaskStatus_StatusCode"),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_ReviewTaskStatus_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_ReviewTaskStatus_UpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_ReviewTaskStatus_DeletedBy"),
        schema="kb",
    )

    # -------------------------------------------------------------------------
    # Entity tables
    # -------------------------------------------------------------------------
    op.create_table(
        "Aspect",
        sa.Column("AspectID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("AspectKey", mssql.NVARCHAR(length=200), nullable=False),
        sa.Column("Title", mssql.NVARCHAR(length=200), nullable=False),
        sa.Column("Summary", mssql.NVARCHAR(length=None), nullable=True),  # NVARCHAR(MAX)
        sa.Column("MaturityLevelID", sa.BigInteger(), nullable=False),
        sa.Column("AspectStateID", sa.BigInteger(), nullable=False),
        sa.Column("Owner", mssql.NVARCHAR(length=200), nullable=True),
        sa.Column("LastReviewedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("NextReviewDate", mssql.DATETIME2(), nullable=True),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("AspectID", name="PK_Aspect_AspectID"),
        sa.UniqueConstraint("AspectKey", name="UQ_Aspect_AspectKey"),
        sa.ForeignKeyConstraint(
            ["MaturityLevelID"], ["kb.MaturityLevel.MaturityLevelID"], name="FK_Aspect_MaturityLevelID"
        ),
        sa.ForeignKeyConstraint(
            ["AspectStateID"], ["kb.AspectState.AspectStateID"], name="FK_Aspect_AspectStateID"
        ),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_Aspect_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_Aspect_UpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_Aspect_DeletedBy"),
        schema="kb",
    )
    op.create_index("IX_Aspect_AspectKey", "Aspect", ["AspectKey"], unique=True, schema="kb")
    op.create_index("IX_Aspect_AspectStateID", "Aspect", ["AspectStateID"], unique=False, schema="kb")
    op.create_index("IX_Aspect_MaturityLevelID", "Aspect", ["MaturityLevelID"], unique=False, schema="kb")

    op.create_table(
        "Idea",
        sa.Column("IdeaID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("Title", mssql.NVARCHAR(length=200), nullable=False),
        sa.Column("ProblemStatement", mssql.NVARCHAR(length=None), nullable=True),  # NVARCHAR(MAX)
        sa.Column("Hypothesis", mssql.NVARCHAR(length=None), nullable=True),  # NVARCHAR(MAX)
        sa.Column("ImpactNotes", mssql.NVARCHAR(length=None), nullable=True),  # NVARCHAR(MAX)
        sa.Column("Risks", mssql.NVARCHAR(length=None), nullable=True),  # NVARCHAR(MAX)
        sa.Column("NextStep", mssql.NVARCHAR(length=None), nullable=True),  # NVARCHAR(MAX)
        sa.Column("DecisionSummary", mssql.NVARCHAR(length=None), nullable=True),  # NVARCHAR(MAX)
        sa.Column("IdeaStatusID", sa.BigInteger(), nullable=False),
        sa.Column("ApprovedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("IdeaID", name="PK_Idea_IdeaID"),
        sa.ForeignKeyConstraint(["IdeaStatusID"], ["kb.IdeaStatus.IdeaStatusID"], name="FK_Idea_IdeaStatusID"),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_Idea_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_Idea_UpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_Idea_DeletedBy"),
        schema="kb",
    )
    op.create_index("IX_Idea_IdeaStatusID", "Idea", ["IdeaStatusID"], unique=False, schema="kb")
    op.create_index("IX_Idea_CreatedDate", "Idea", ["CreatedDate"], unique=False, schema="kb")

    op.create_table(
        "AspectRelation",
        sa.Column("AspectRelationID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("FromAspectID", sa.BigInteger(), nullable=False),
        sa.Column("ToAspectID", sa.BigInteger(), nullable=False),
        sa.Column("RelationTypeID", sa.BigInteger(), nullable=False),
        sa.Column("Notes", mssql.NVARCHAR(length=None), nullable=True),  # NVARCHAR(MAX)
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("AspectRelationID", name="PK_AspectRelation_AspectRelationID"),
        sa.UniqueConstraint(
            "FromAspectID",
            "ToAspectID",
            "RelationTypeID",
            name="UQ_AspectRelation_FromAspectID_ToAspectID_RelationTypeID",
        ),
        sa.CheckConstraint("FromAspectID <> ToAspectID", name="CK_AspectRelation_NoSelf"),
        sa.ForeignKeyConstraint(["FromAspectID"], ["kb.Aspect.AspectID"], name="FK_AspectRelation_FromAspectID"),
        sa.ForeignKeyConstraint(["ToAspectID"], ["kb.Aspect.AspectID"], name="FK_AspectRelation_ToAspectID"),
        sa.ForeignKeyConstraint(
            ["RelationTypeID"], ["kb.RelationType.RelationTypeID"], name="FK_AspectRelation_RelationTypeID"
        ),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_AspectRelation_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_AspectRelation_UpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_AspectRelation_DeletedBy"),
        schema="kb",
    )
    op.create_index("IX_AspectRelation_FromAspectID", "AspectRelation", ["FromAspectID"], unique=False, schema="kb")
    op.create_index("IX_AspectRelation_ToAspectID", "AspectRelation", ["ToAspectID"], unique=False, schema="kb")
    op.create_index(
        "IX_AspectRelation_RelationTypeID", "AspectRelation", ["RelationTypeID"], unique=False, schema="kb"
    )

    op.create_table(
        "IdeaAspect",
        sa.Column("IdeaAspectID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("IdeaID", sa.BigInteger(), nullable=False),
        sa.Column("AspectID", sa.BigInteger(), nullable=False),
        sa.Column("Notes", mssql.NVARCHAR(length=None), nullable=True),  # NVARCHAR(MAX)
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("IdeaAspectID", name="PK_IdeaAspect_IdeaAspectID"),
        sa.UniqueConstraint("IdeaID", "AspectID", name="UQ_IdeaAspect_IdeaID_AspectID"),
        sa.ForeignKeyConstraint(["IdeaID"], ["kb.Idea.IdeaID"], name="FK_IdeaAspect_IdeaID"),
        sa.ForeignKeyConstraint(["AspectID"], ["kb.Aspect.AspectID"], name="FK_IdeaAspect_AspectID"),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_IdeaAspect_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_IdeaAspect_UpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_IdeaAspect_DeletedBy"),
        schema="kb",
    )
    op.create_index("IX_IdeaAspect_IdeaID", "IdeaAspect", ["IdeaID"], unique=False, schema="kb")
    op.create_index("IX_IdeaAspect_AspectID", "IdeaAspect", ["AspectID"], unique=False, schema="kb")

    op.create_table(
        "WorkItem",
        sa.Column("WorkItemID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("WorkItemTypeID", sa.BigInteger(), nullable=False),
        sa.Column("ExternalSystem", mssql.NVARCHAR(length=100), nullable=True),
        sa.Column("ExternalKey", mssql.NVARCHAR(length=200), nullable=True),
        sa.Column("Url", mssql.NVARCHAR(length=1000), nullable=True),
        sa.Column("Status", mssql.NVARCHAR(length=50), nullable=True),
        sa.Column("Title", mssql.NVARCHAR(length=200), nullable=True),
        sa.Column("Description", mssql.NVARCHAR(length=None), nullable=True),  # NVARCHAR(MAX)
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("WorkItemID", name="PK_WorkItem_WorkItemID"),
        sa.ForeignKeyConstraint(
            ["WorkItemTypeID"], ["kb.WorkItemType.WorkItemTypeID"], name="FK_WorkItem_WorkItemTypeID"
        ),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_WorkItem_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_WorkItem_UpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_WorkItem_DeletedBy"),
        schema="kb",
    )
    op.create_index("IX_WorkItem_WorkItemTypeID", "WorkItem", ["WorkItemTypeID"], unique=False, schema="kb")
    op.create_index("IX_WorkItem_ExternalKey", "WorkItem", ["ExternalKey"], unique=False, schema="kb")

    op.create_table(
        "IdeaWorkItem",
        sa.Column("IdeaWorkItemID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("IdeaID", sa.BigInteger(), nullable=False),
        sa.Column("WorkItemID", sa.BigInteger(), nullable=False),
        sa.Column("Notes", mssql.NVARCHAR(length=None), nullable=True),  # NVARCHAR(MAX)
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("IdeaWorkItemID", name="PK_IdeaWorkItem_IdeaWorkItemID"),
        sa.UniqueConstraint("IdeaID", "WorkItemID", name="UQ_IdeaWorkItem_IdeaID_WorkItemID"),
        sa.ForeignKeyConstraint(["IdeaID"], ["kb.Idea.IdeaID"], name="FK_IdeaWorkItem_IdeaID"),
        sa.ForeignKeyConstraint(["WorkItemID"], ["kb.WorkItem.WorkItemID"], name="FK_IdeaWorkItem_WorkItemID"),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_IdeaWorkItem_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_IdeaWorkItem_UpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_IdeaWorkItem_DeletedBy"),
        schema="kb",
    )
    op.create_index("IX_IdeaWorkItem_IdeaID", "IdeaWorkItem", ["IdeaID"], unique=False, schema="kb")
    op.create_index("IX_IdeaWorkItem_WorkItemID", "IdeaWorkItem", ["WorkItemID"], unique=False, schema="kb")

    op.create_table(
        "AspectWorkItem",
        sa.Column("AspectWorkItemID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("AspectID", sa.BigInteger(), nullable=False),
        sa.Column("WorkItemID", sa.BigInteger(), nullable=False),
        sa.Column("Notes", mssql.NVARCHAR(length=None), nullable=True),  # NVARCHAR(MAX)
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("AspectWorkItemID", name="PK_AspectWorkItem_AspectWorkItemID"),
        sa.UniqueConstraint("AspectID", "WorkItemID", name="UQ_AspectWorkItem_AspectID_WorkItemID"),
        sa.ForeignKeyConstraint(["AspectID"], ["kb.Aspect.AspectID"], name="FK_AspectWorkItem_AspectID"),
        sa.ForeignKeyConstraint(["WorkItemID"], ["kb.WorkItem.WorkItemID"], name="FK_AspectWorkItem_WorkItemID"),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_AspectWorkItem_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_AspectWorkItem_UpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_AspectWorkItem_DeletedBy"),
        schema="kb",
    )
    op.create_index("IX_AspectWorkItem_AspectID", "AspectWorkItem", ["AspectID"], unique=False, schema="kb")
    op.create_index("IX_AspectWorkItem_WorkItemID", "AspectWorkItem", ["WorkItemID"], unique=False, schema="kb")

    op.create_table(
        "SessionNote",
        sa.Column("SessionNoteID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("Title", mssql.NVARCHAR(length=200), nullable=False),
        sa.Column("Summary", mssql.NVARCHAR(length=None), nullable=True),  # NVARCHAR(MAX)
        sa.Column("Decisions", mssql.NVARCHAR(length=None), nullable=True),  # NVARCHAR(MAX)
        sa.Column("SourceType", mssql.NVARCHAR(length=50), nullable=True),
        sa.Column("SourceRef", mssql.NVARCHAR(length=200), nullable=True),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("SessionNoteID", name="PK_SessionNote_SessionNoteID"),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_SessionNote_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_SessionNote_UpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_SessionNote_DeletedBy"),
        schema="kb",
    )
    op.create_index("IX_SessionNote_CreatedDate", "SessionNote", ["CreatedDate"], unique=False, schema="kb")

    op.create_table(
        "SessionNoteIdea",
        sa.Column("SessionNoteIdeaID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("SessionNoteID", sa.BigInteger(), nullable=False),
        sa.Column("IdeaID", sa.BigInteger(), nullable=False),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("SessionNoteIdeaID", name="PK_SessionNoteIdea_SessionNoteIdeaID"),
        sa.UniqueConstraint("SessionNoteID", "IdeaID", name="UQ_SessionNoteIdea_SessionNoteID_IdeaID"),
        sa.ForeignKeyConstraint(["SessionNoteID"], ["kb.SessionNote.SessionNoteID"], name="FK_SessionNoteIdea_SessionNoteID"),
        sa.ForeignKeyConstraint(["IdeaID"], ["kb.Idea.IdeaID"], name="FK_SessionNoteIdea_IdeaID"),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_SessionNoteIdea_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_SessionNoteIdea_UpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_SessionNoteIdea_DeletedBy"),
        schema="kb",
    )
    op.create_index("IX_SessionNoteIdea_SessionNoteID", "SessionNoteIdea", ["SessionNoteID"], unique=False, schema="kb")
    op.create_index("IX_SessionNoteIdea_IdeaID", "SessionNoteIdea", ["IdeaID"], unique=False, schema="kb")

    op.create_table(
        "SessionNoteAspect",
        sa.Column("SessionNoteAspectID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("SessionNoteID", sa.BigInteger(), nullable=False),
        sa.Column("AspectID", sa.BigInteger(), nullable=False),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("SessionNoteAspectID", name="PK_SessionNoteAspect_SessionNoteAspectID"),
        sa.UniqueConstraint("SessionNoteID", "AspectID", name="UQ_SessionNoteAspect_SessionNoteID_AspectID"),
        sa.ForeignKeyConstraint(
            ["SessionNoteID"], ["kb.SessionNote.SessionNoteID"], name="FK_SessionNoteAspect_SessionNoteID"
        ),
        sa.ForeignKeyConstraint(["AspectID"], ["kb.Aspect.AspectID"], name="FK_SessionNoteAspect_AspectID"),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_SessionNoteAspect_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_SessionNoteAspect_UpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_SessionNoteAspect_DeletedBy"),
        schema="kb",
    )
    op.create_index(
        "IX_SessionNoteAspect_SessionNoteID", "SessionNoteAspect", ["SessionNoteID"], unique=False, schema="kb"
    )
    op.create_index("IX_SessionNoteAspect_AspectID", "SessionNoteAspect", ["AspectID"], unique=False, schema="kb")

    op.create_table(
        "DocRef",
        sa.Column("DocRefID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("DocPath", mssql.NVARCHAR(length=400), nullable=False),
        sa.Column("AnchorID", mssql.NVARCHAR(length=200), nullable=True),
        sa.Column("SnapshotCommitSHA", mssql.NVARCHAR(length=64), nullable=True),
        sa.Column("ContextNote", mssql.NVARCHAR(length=None), nullable=True),  # NVARCHAR(MAX)
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("DocRefID", name="PK_DocRef_DocRefID"),
        sa.UniqueConstraint(
            "DocPath", "AnchorID", "SnapshotCommitSHA", name="UQ_DocRef_DocPath_AnchorID_SnapshotCommitSHA"
        ),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_DocRef_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_DocRef_UpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_DocRef_DeletedBy"),
        schema="kb",
    )
    op.create_index("IX_DocRef_DocPath", "DocRef", ["DocPath"], unique=False, schema="kb")

    op.create_table(
        "AspectDocRef",
        sa.Column("AspectDocRefID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("AspectID", sa.BigInteger(), nullable=False),
        sa.Column("DocRefID", sa.BigInteger(), nullable=False),
        sa.Column("Notes", mssql.NVARCHAR(length=None), nullable=True),  # NVARCHAR(MAX)
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("AspectDocRefID", name="PK_AspectDocRef_AspectDocRefID"),
        sa.UniqueConstraint("AspectID", "DocRefID", name="UQ_AspectDocRef_AspectID_DocRefID"),
        sa.ForeignKeyConstraint(["AspectID"], ["kb.Aspect.AspectID"], name="FK_AspectDocRef_AspectID"),
        sa.ForeignKeyConstraint(["DocRefID"], ["kb.DocRef.DocRefID"], name="FK_AspectDocRef_DocRefID"),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_AspectDocRef_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_AspectDocRef_UpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_AspectDocRef_DeletedBy"),
        schema="kb",
    )
    op.create_index("IX_AspectDocRef_AspectID", "AspectDocRef", ["AspectID"], unique=False, schema="kb")
    op.create_index("IX_AspectDocRef_DocRefID", "AspectDocRef", ["DocRefID"], unique=False, schema="kb")

    op.create_table(
        "IdeaDocRef",
        sa.Column("IdeaDocRefID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("IdeaID", sa.BigInteger(), nullable=False),
        sa.Column("DocRefID", sa.BigInteger(), nullable=False),
        sa.Column("Notes", mssql.NVARCHAR(length=None), nullable=True),  # NVARCHAR(MAX)
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("IdeaDocRefID", name="PK_IdeaDocRef_IdeaDocRefID"),
        sa.UniqueConstraint("IdeaID", "DocRefID", name="UQ_IdeaDocRef_IdeaID_DocRefID"),
        sa.ForeignKeyConstraint(["IdeaID"], ["kb.Idea.IdeaID"], name="FK_IdeaDocRef_IdeaID"),
        sa.ForeignKeyConstraint(["DocRefID"], ["kb.DocRef.DocRefID"], name="FK_IdeaDocRef_DocRefID"),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_IdeaDocRef_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_IdeaDocRef_UpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_IdeaDocRef_DeletedBy"),
        schema="kb",
    )
    op.create_index("IX_IdeaDocRef_IdeaID", "IdeaDocRef", ["IdeaID"], unique=False, schema="kb")
    op.create_index("IX_IdeaDocRef_DocRefID", "IdeaDocRef", ["DocRefID"], unique=False, schema="kb")

    op.create_table(
        "ReviewTask",
        sa.Column("ReviewTaskID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("AspectID", sa.BigInteger(), nullable=False),
        sa.Column("TriggeredByAspectID", sa.BigInteger(), nullable=True),
        sa.Column("Reason", mssql.NVARCHAR(length=500), nullable=False),
        sa.Column("ReviewTaskStatusID", sa.BigInteger(), nullable=False),
        sa.Column("DueDate", mssql.DATETIME2(), nullable=True),
        sa.Column("CompletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("Notes", mssql.NVARCHAR(length=None), nullable=True),  # NVARCHAR(MAX)
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("ReviewTaskID", name="PK_ReviewTask_ReviewTaskID"),
        sa.ForeignKeyConstraint(["AspectID"], ["kb.Aspect.AspectID"], name="FK_ReviewTask_AspectID"),
        sa.ForeignKeyConstraint(
            ["TriggeredByAspectID"], ["kb.Aspect.AspectID"], name="FK_ReviewTask_TriggeredByAspectID"
        ),
        sa.ForeignKeyConstraint(
            ["ReviewTaskStatusID"],
            ["kb.ReviewTaskStatus.ReviewTaskStatusID"],
            name="FK_ReviewTask_ReviewTaskStatusID",
        ),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_ReviewTask_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_ReviewTask_UpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_ReviewTask_DeletedBy"),
        schema="kb",
    )
    op.create_index("IX_ReviewTask_AspectID", "ReviewTask", ["AspectID"], unique=False, schema="kb")
    op.create_index(
        "IX_ReviewTask_TriggeredByAspectID", "ReviewTask", ["TriggeredByAspectID"], unique=False, schema="kb"
    )
    op.create_index(
        "IX_ReviewTask_ReviewTaskStatusID", "ReviewTask", ["ReviewTaskStatusID"], unique=False, schema="kb"
    )

    # -------------------------------------------------------------------------
    # Seed reference data
    # -------------------------------------------------------------------------
    op.execute(
        """
        IF NOT EXISTS (SELECT 1 FROM [kb].[MaturityLevel] WHERE LevelCode = 'M0')
        BEGIN
            INSERT INTO [kb].[MaturityLevel] (LevelCode, LevelName, Description, SortOrder, IsActive)
            VALUES
                ('M0', 'Captured', 'Idea captured; minimal context recorded.', 0, 1),
                ('M1', 'Explored', 'Initial exploration performed; opportunities and constraints identified.', 1, 1),
                ('M2', 'Synthesized', 'Options compared; recommendation criteria documented.', 2, 1),
                ('M3', 'Decided', 'Decision recorded; delivery path chosen (RFC/Story/etc.).', 3, 1),
                ('M4', 'Implemented', 'Implementation merged; knowledge updated.', 4, 1),
                ('M5', 'Validated', 'Value validated (feedback/metrics) and maintenance cadence defined.', 5, 1);
        END
        """
    )
    op.execute(
        """
        IF NOT EXISTS (SELECT 1 FROM [kb].[AspectState] WHERE StateCode = 'active')
        BEGIN
            INSERT INTO [kb].[AspectState] (StateCode, StateName, Description, SortOrder, IsActive)
            VALUES
                ('active', 'Active', 'Actively being explored or maintained.', 0, 1),
                ('parked', 'Parked', 'Paused but intentionally kept for later.', 1, 1),
                ('deprecated', 'Deprecated', 'No longer relevant; kept only for history.', 2, 1);
        END
        """
    )
    op.execute(
        """
        IF NOT EXISTS (SELECT 1 FROM [kb].[IdeaStatus] WHERE StatusCode = 'captured')
        BEGIN
            INSERT INTO [kb].[IdeaStatus] (StatusCode, StatusName, Description, SortOrder, IsTerminal, IsActive)
            VALUES
                ('captured', 'Captured', 'Idea captured; not yet evaluated.', 0, 0, 1),
                ('exploring', 'Exploring', 'Being explored (options/impact/research).', 1, 0, 1),
                ('parked', 'Parked', 'Parked until a trigger or scheduled review.', 2, 0, 1),
                ('rejected', 'Rejected', 'Rejected with rationale; can be revisited if assumptions change.', 3, 1, 1),
                ('approved_to_build', 'ApprovedToBuild', 'Approved for delivery work (may create GitHub work items).', 4, 0, 1),
                ('implemented', 'Implemented', 'Implemented and linked to delivery artifacts.', 5, 0, 1),
                ('validated', 'Validated', 'Validated; outcome achieved and maintained.', 6, 1, 1);
        END
        """
    )
    op.execute(
        """
        IF NOT EXISTS (SELECT 1 FROM [kb].[RelationType] WHERE TypeCode = 'depends_on')
        BEGIN
            INSERT INTO [kb].[RelationType] (TypeCode, TypeName, Description, SortOrder, IsSymmetric, IsActive)
            VALUES
                ('depends_on', 'DependsOn', 'This aspect depends on another aspect.', 0, 0, 1),
                ('impacts', 'Impacts', 'This aspect impacts another aspect.', 1, 0, 1),
                ('blocks', 'Blocks', 'This aspect blocks progress on another aspect.', 2, 0, 1),
                ('similar_to', 'SimilarTo', 'These aspects are similar (symmetric).', 3, 1, 1),
                ('supersedes', 'Supersedes', 'This aspect supersedes another aspect.', 4, 0, 1);
        END
        """
    )
    op.execute(
        """
        IF NOT EXISTS (SELECT 1 FROM [kb].[WorkItemType] WHERE TypeCode = 'github_issue')
        BEGIN
            INSERT INTO [kb].[WorkItemType] (TypeCode, TypeName, Description, SortOrder, IsActive)
            VALUES
                ('github_issue', 'GitHubIssue', 'GitHub issue (delivery tracking).', 0, 1),
                ('github_pr', 'GitHubPR', 'GitHub pull request.', 1, 1),
                ('story', 'Story', 'BMAD story document (docs/stories).', 2, 1),
                ('task', 'Task', 'BMAD task spec/completion (docs/tasks).', 3, 1),
                ('bug_session', 'BugSession', 'Bug-session journal/artifacts (docs/bug-session).', 4, 1),
                ('doc', 'Doc', 'Documentation artifact.', 5, 1);
        END
        """
    )
    op.execute(
        """
        IF NOT EXISTS (SELECT 1 FROM [kb].[ReviewTaskStatus] WHERE StatusCode = 'pending')
        BEGIN
            INSERT INTO [kb].[ReviewTaskStatus] (StatusCode, StatusName, Description, SortOrder, IsTerminal, IsActive)
            VALUES
                ('pending', 'Pending', 'Queued for review.', 0, 0, 1),
                ('in_progress', 'InProgress', 'Review is in progress.', 1, 0, 1),
                ('completed', 'Completed', 'Review completed.', 2, 1, 1),
                ('cancelled', 'Cancelled', 'Review cancelled.', 3, 1, 1);
        END
        """
    )

    # -------------------------------------------------------------------------
    # Stored procedure: enqueue review tasks for directly related aspects
    # -------------------------------------------------------------------------
    op.execute(
        """
        CREATE OR ALTER PROCEDURE [kb].[EnqueueRelatedAspectReviews]
            @AspectID BIGINT,
            @Reason NVARCHAR(500),
            @CreatedBy BIGINT = NULL
        AS
        BEGIN
            SET NOCOUNT ON;

            DECLARE @PendingStatusID BIGINT;
            SELECT @PendingStatusID = ReviewTaskStatusID
            FROM [kb].[ReviewTaskStatus]
            WHERE StatusCode = 'pending' AND IsDeleted = 0;

            IF @PendingStatusID IS NULL
            BEGIN
                RAISERROR('kb.ReviewTaskStatus missing pending status', 16, 1);
                RETURN;
            END

            ;WITH Related AS (
                SELECT DISTINCT
                    CASE
                        WHEN ar.FromAspectID = @AspectID THEN ar.ToAspectID
                        ELSE ar.FromAspectID
                    END AS RelatedAspectID
                FROM [kb].[AspectRelation] ar
                WHERE ar.IsDeleted = 0
                  AND (ar.FromAspectID = @AspectID OR ar.ToAspectID = @AspectID)
            )
            INSERT INTO [kb].[ReviewTask] (
                AspectID,
                TriggeredByAspectID,
                Reason,
                ReviewTaskStatusID,
                CreatedBy
            )
            SELECT
                r.RelatedAspectID,
                @AspectID,
                @Reason,
                @PendingStatusID,
                @CreatedBy
            FROM Related r
            WHERE r.RelatedAspectID IS NOT NULL
              AND r.RelatedAspectID <> @AspectID
              AND NOT EXISTS (
                  SELECT 1
                  FROM [kb].[ReviewTask] rt
                  WHERE rt.IsDeleted = 0
                    AND rt.AspectID = r.RelatedAspectID
                    AND rt.TriggeredByAspectID = @AspectID
                    AND rt.ReviewTaskStatusID = @PendingStatusID
                    AND rt.CompletedDate IS NULL
              );
        END
        """
    )

    # -------------------------------------------------------------------------
    # Triggers (minimal): keep UpdatedDate in sync on updates
    # -------------------------------------------------------------------------
    op.execute(
        """
        CREATE OR ALTER TRIGGER [kb].[TR_Aspect_SetUpdatedDate]
        ON [kb].[Aspect]
        AFTER UPDATE
        AS
        BEGIN
            SET NOCOUNT ON;
            -- Guard against recursion/nesting
            IF TRIGGER_NESTLEVEL() > 1 RETURN;

            UPDATE a
            SET UpdatedDate = GETUTCDATE()
            FROM [kb].[Aspect] a
            INNER JOIN inserted i ON a.AspectID = i.AspectID;
        END
        """
    )
    op.execute(
        """
        CREATE OR ALTER TRIGGER [kb].[TR_Idea_SetUpdatedDate]
        ON [kb].[Idea]
        AFTER UPDATE
        AS
        BEGIN
            SET NOCOUNT ON;
            -- Guard against recursion/nesting
            IF TRIGGER_NESTLEVEL() > 1 RETURN;

            UPDATE d
            SET UpdatedDate = GETUTCDATE()
            FROM [kb].[Idea] d
            INNER JOIN inserted i ON d.IdeaID = i.IdeaID;
        END
        """
    )

    # -------------------------------------------------------------------------
    # Seed: capture this workflow-design conversation as a durable SessionNote
    # -------------------------------------------------------------------------
    op.execute(
        """
        DECLARE @AspectID BIGINT;
        DECLARE @IdeaID BIGINT;
        DECLARE @SessionNoteID BIGINT;

        -- Aspect: Knowledge management + ideation workflow
        SELECT @AspectID = AspectID
        FROM [kb].[Aspect]
        WHERE AspectKey = 'process.knowledge-management' AND IsDeleted = 0;

        IF @AspectID IS NULL
        BEGIN
            INSERT INTO [kb].[Aspect] (
                AspectKey,
                Title,
                Summary,
                MaturityLevelID,
                AspectStateID,
                Owner
            )
            VALUES (
                'process.knowledge-management',
                'Process: Knowledge management + ideation workflow',
                'SQL-authoritative KB + Kaizen ideation workflow for capturing, parking, and evaluating ideas without context blowouts.',
                (SELECT MaturityLevelID FROM [kb].[MaturityLevel] WHERE LevelCode = 'M1' AND IsDeleted = 0),
                (SELECT AspectStateID FROM [kb].[AspectState] WHERE StateCode = 'active' AND IsDeleted = 0),
                'Anthony'
            );

            SET @AspectID = CAST(SCOPE_IDENTITY() AS BIGINT);
        END

        -- Idea: Dolt evaluation (rejected)
        SELECT @IdeaID = IdeaID
        FROM [kb].[Idea]
        WHERE Title = 'Evaluate Dolt for workflow efficiency' AND IsDeleted = 0;

        IF @IdeaID IS NULL
        BEGIN
            INSERT INTO [kb].[Idea] (
                Title,
                ProblemStatement,
                DecisionSummary,
                IdeaStatusID
            )
            VALUES (
                'Evaluate Dolt for workflow efficiency',
                'Assess whether Dolt (git-for-data) would make agents more efficient at managing git/workflow and improving delivery quality.',
                'Rejected: Dolt versions tables/data (not code) and adopting it would be a large platform change. Chosen path: implement higher-ROI workflow improvements via an SQL-authoritative KB + Kaizen-style review loop.',
                (SELECT IdeaStatusID FROM [kb].[IdeaStatus] WHERE StatusCode = 'rejected' AND IsDeleted = 0)
            );

            SET @IdeaID = CAST(SCOPE_IDENTITY() AS BIGINT);
        END

        -- Link idea -> aspect
        IF NOT EXISTS (
            SELECT 1 FROM [kb].[IdeaAspect]
            WHERE IdeaID = @IdeaID AND AspectID = @AspectID AND IsDeleted = 0
        )
        BEGIN
            INSERT INTO [kb].[IdeaAspect] (IdeaID, AspectID, Notes)
            VALUES (@IdeaID, @AspectID, 'This conversation: Dolt evaluation pivoted into KB + Kaizen ideation workflow design.');
        END

        -- Session note: capture the pivot
        SELECT @SessionNoteID = SessionNoteID
        FROM [kb].[SessionNote]
        WHERE Title = 'Dolt evaluation → KB + Kaizen ideation pivot (2026-02-08)' AND IsDeleted = 0;

        IF @SessionNoteID IS NULL
        BEGIN
            INSERT INTO [kb].[SessionNote] (
                Title,
                Summary,
                Decisions,
                SourceType,
                SourceRef
            )
            VALUES (
                'Dolt evaluation → KB + Kaizen ideation pivot (2026-02-08)',
                'Started by evaluating Dolt for workflow efficiency; concluded it is not a good fit for git/PR discipline. Pivoted to designing an SQL-authoritative knowledge base + Kaizen ideation workflow to capture/park/revisit ideas with strong cross-linking.',
                '- Decision: Do not adopt Dolt now (too large, wrong problem).\\n- Decision: Implement SQL Server KB (schema kb) with aspects, ideas, relationships, session notes, and a Kaizen review queue.\\n- Rule: Only create GitHub delivery work items once an idea is approved_to_build.',
                'cursor_chat',
                '2026-02-08'
            );

            SET @SessionNoteID = CAST(SCOPE_IDENTITY() AS BIGINT);
        END

        -- Link session note -> idea
        IF NOT EXISTS (
            SELECT 1 FROM [kb].[SessionNoteIdea]
            WHERE SessionNoteID = @SessionNoteID AND IdeaID = @IdeaID AND IsDeleted = 0
        )
        BEGIN
            INSERT INTO [kb].[SessionNoteIdea] (SessionNoteID, IdeaID)
            VALUES (@SessionNoteID, @IdeaID);
        END

        -- Link session note -> aspect
        IF NOT EXISTS (
            SELECT 1 FROM [kb].[SessionNoteAspect]
            WHERE SessionNoteID = @SessionNoteID AND AspectID = @AspectID AND IsDeleted = 0
        )
        BEGIN
            INSERT INTO [kb].[SessionNoteAspect] (SessionNoteID, AspectID)
            VALUES (@SessionNoteID, @AspectID);
        END
        """
    )


def downgrade() -> None:
    # Triggers
    op.execute(
        """
        IF OBJECT_ID('[kb].[TR_Idea_SetUpdatedDate]', 'TR') IS NOT NULL
        DROP TRIGGER [kb].[TR_Idea_SetUpdatedDate];
        """
    )
    op.execute(
        """
        IF OBJECT_ID('[kb].[TR_Aspect_SetUpdatedDate]', 'TR') IS NOT NULL
        DROP TRIGGER [kb].[TR_Aspect_SetUpdatedDate];
        """
    )

    # Stored proc
    op.execute(
        """
        IF OBJECT_ID('[kb].[EnqueueRelatedAspectReviews]', 'P') IS NOT NULL
        DROP PROCEDURE [kb].[EnqueueRelatedAspectReviews];
        """
    )

    # Drop tables in dependency order
    op.drop_table("ReviewTask", schema="kb")

    op.drop_table("IdeaDocRef", schema="kb")
    op.drop_table("AspectDocRef", schema="kb")
    op.drop_table("DocRef", schema="kb")

    op.drop_table("SessionNoteAspect", schema="kb")
    op.drop_table("SessionNoteIdea", schema="kb")
    op.drop_table("SessionNote", schema="kb")

    op.drop_table("AspectWorkItem", schema="kb")
    op.drop_table("IdeaWorkItem", schema="kb")
    op.drop_table("WorkItem", schema="kb")

    op.drop_table("IdeaAspect", schema="kb")
    op.drop_table("AspectRelation", schema="kb")
    op.drop_table("Idea", schema="kb")
    op.drop_table("Aspect", schema="kb")

    op.drop_table("ReviewTaskStatus", schema="kb")
    op.drop_table("WorkItemType", schema="kb")
    op.drop_table("RelationType", schema="kb")
    op.drop_table("IdeaStatus", schema="kb")
    op.drop_table("AspectState", schema="kb")
    op.drop_table("MaturityLevel", schema="kb")

    # Drop schema (best effort)
    op.execute("IF EXISTS (SELECT * FROM sys.schemas WHERE name = 'kb') EXEC('DROP SCHEMA [kb]')")

