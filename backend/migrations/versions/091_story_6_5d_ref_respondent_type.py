"""Story 6.5d: ref.RespondentType + §11.3 seeds.

Revision ID: 091
Revises: 090
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql


revision = "091"
down_revision = "090"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "RespondentType",
        sa.Column("RespondentTypeID", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("Code", mssql.NVARCHAR(length=50), nullable=False),
        sa.Column("DisplayName", mssql.NVARCHAR(length=100), nullable=False),
        sa.Column("PromptHint", mssql.NVARCHAR(length=None), nullable=False),
        sa.Column("SortOrder", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("1")),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.PrimaryKeyConstraint("RespondentTypeID", name="PK_RespondentType"),
        sa.UniqueConstraint("Code", name="UQ_RespondentType_Code"),
        schema="ref",
    )

    op.execute(
        """
        INSERT INTO [ref].[RespondentType] ([Code], [DisplayName], [PromptHint], [SortOrder], [IsActive])
        VALUES
        (N'ATTENDEE', N'Attendee / Visitor',
         N'The primary respondent is an event attendee or first-time visitor. Assume limited prior knowledge. Provide clear directions and reassurance.', 10, 1),
        (N'MEMBER', N'Member / Subscriber',
         N'The respondent is an existing or prospective member. Use warm, community language and reference membership benefits.', 20, 1),
        (N'PARENT_GUARDIAN', N'Parent / Guardian',
         N'The respondent is a parent or guardian acting on behalf of a child. Use reassuring, family-friendly language and include consent/medical fields where appropriate.', 30, 1),
        (N'EMPLOYEE', N'Employee / Staff',
         N'The respondent is an employee. Use professional, concise language. Reference company policy or compliance where relevant.', 40, 1),
        (N'DONOR', N'Donor / Supporter',
         N'The respondent is a donor or supporter. Use appreciative, mission-driven language. Minimise friction for gift or pledge details.', 50, 1),
        (N'PARTICIPANT', N'Participant / Subject',
         N'The respondent is a research or study participant. Use neutral, respectful language and emphasise voluntary nature and data privacy.', 60, 1),
        (N'CUSTOMER', N'Customer / Client',
         N'The respondent is a customer or client. Use helpful, solution-oriented language and focus on their needs.', 70, 1),
        (N'STUDENT', N'Student / Learner',
         N'The respondent is a student or learner. Use encouraging, accessible language and avoid corporate jargon.', 80, 1),
        (N'PROFESSIONAL', N'Professional / Executive',
         N'The respondent is a busy professional or decision-maker. Keep questions short, respect time, and highlight business value.', 90, 1);
        """
    )


def downgrade() -> None:
    op.drop_table("RespondentType", schema="ref")
