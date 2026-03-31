"""Story 6.2.2: SubmissionAttachment for public file uploads

Revision ID: 051
Revises: 050
Create Date: 2026-03-31

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql


revision = "051"
down_revision = "050"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "SubmissionAttachment",
        sa.Column("SubmissionAttachmentID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("FormPublicLinkID", sa.BigInteger(), nullable=False),
        sa.Column("FormSubmissionID", sa.BigInteger(), nullable=True),
        sa.Column("PublicAttachmentId", mssql.NVARCHAR(length=36), nullable=False),
        sa.Column("OriginalFileName", mssql.NVARCHAR(length=510), nullable=False),
        sa.Column("ContentType", mssql.NVARCHAR(length=255), nullable=False),
        sa.Column("SizeBytes", sa.BigInteger(), nullable=False),
        sa.Column("Sha256", mssql.NVARCHAR(length=64), nullable=False),
        sa.Column("StorageProvider", mssql.NVARCHAR(length=32), nullable=False),
        sa.Column("StorageKey", mssql.NVARCHAR(length=1024), nullable=False),
        sa.Column("ClientUploadSessionKey", mssql.NVARCHAR(length=128), nullable=True),
        sa.Column("CreatedAt", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("ExpiresAt", mssql.DATETIME2(), nullable=True),
        sa.ForeignKeyConstraint(
            ["FormPublicLinkID"],
            ["dbo.FormPublicLink.FormPublicLinkID"],
            name="FK_SubmissionAttachment_FormPublicLinkID",
        ),
        sa.ForeignKeyConstraint(
            ["FormSubmissionID"],
            ["dbo.FormSubmission.FormSubmissionID"],
            name="FK_SubmissionAttachment_FormSubmissionID",
        ),
        sa.PrimaryKeyConstraint("SubmissionAttachmentID", name="PK_SubmissionAttachment_SubmissionAttachmentID"),
        sa.UniqueConstraint("PublicAttachmentId", name="UQ_SubmissionAttachment_PublicAttachmentId"),
        schema="dbo",
    )
    op.create_index(
        "IX_SubmissionAttachment_FormPublicLinkID",
        "SubmissionAttachment",
        ["FormPublicLinkID"],
        unique=False,
        schema="dbo",
    )
    op.create_index(
        "IX_SubmissionAttachment_FormSubmissionID",
        "SubmissionAttachment",
        ["FormSubmissionID"],
        unique=False,
        schema="dbo",
    )
    op.create_index(
        "IX_SubmissionAttachment_Sha256",
        "SubmissionAttachment",
        ["Sha256"],
        unique=False,
        schema="dbo",
    )
    op.execute(
        """
        CREATE NONCLUSTERED INDEX IX_SubmissionAttachment_DedupePending
        ON [dbo].[SubmissionAttachment] ([FormPublicLinkID], [ClientUploadSessionKey], [Sha256])
        WHERE [FormSubmissionID] IS NULL;
        """
    )


def downgrade() -> None:
    op.execute(
        """
        IF EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_SubmissionAttachment_DedupePending' AND object_id = OBJECT_ID('dbo.SubmissionAttachment'))
        DROP INDEX [IX_SubmissionAttachment_DedupePending] ON [dbo].[SubmissionAttachment];
        """
    )
    op.drop_index("IX_SubmissionAttachment_Sha256", table_name="SubmissionAttachment", schema="dbo")
    op.drop_index("IX_SubmissionAttachment_FormSubmissionID", table_name="SubmissionAttachment", schema="dbo")
    op.drop_index("IX_SubmissionAttachment_FormPublicLinkID", table_name="SubmissionAttachment", schema="dbo")
    op.drop_constraint("FK_SubmissionAttachment_FormSubmissionID", "SubmissionAttachment", schema="dbo", type_="foreignkey")
    op.drop_constraint("FK_SubmissionAttachment_FormPublicLinkID", "SubmissionAttachment", schema="dbo", type_="foreignkey")
    op.drop_table("SubmissionAttachment", schema="dbo")
