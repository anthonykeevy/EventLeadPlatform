"""Story 6.5d: ref.FormPurpose + §11.2 seeds.

Revision ID: 090
Revises: 089
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql


revision = "090"
down_revision = "089"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "FormPurpose",
        sa.Column("FormPurposeID", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("Code", mssql.NVARCHAR(length=50), nullable=False),
        sa.Column("DisplayName", mssql.NVARCHAR(length=100), nullable=False),
        sa.Column("PromptHint", mssql.NVARCHAR(length=None), nullable=False),
        sa.Column("SortOrder", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("1")),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.PrimaryKeyConstraint("FormPurposeID", name="PK_FormPurpose"),
        sa.UniqueConstraint("Code", name="UQ_FormPurpose_Code"),
        schema="ref",
    )

    op.execute(
        """
        INSERT INTO [ref].[FormPurpose] ([Code], [DisplayName], [PromptHint], [SortOrder], [IsActive])
        VALUES
        (N'EVENT_REGISTRATION', N'Event Registration',
         N'This is an event registration form. Use warm, welcoming language and minimise friction for first-time attendees. Emphasise clear confirmation and next-step guidance. Respect local privacy expectations.', 10, 1),
        (N'FEEDBACK_SURVEY', N'Feedback Survey',
         N'This is a feedback survey. Keep questions short and balanced. Use a friendly but professional tone. Include an NPS or star-rating question where appropriate.', 20, 1),
        (N'WAIVER_CONSENT', N'Waiver / Consent',
         N'This is a legal waiver or consent form. Use precise, formal language. Include clear liability statements and signature fields. Comply with local consent age rules.', 30, 1),
        (N'LEAD_CAPTURE', N'Lead Capture',
         N'This is a lead-capture form. Minimise friction. Ask only for name, email, company and one qualification question. End with a clear next-step CTA.', 40, 1),
        (N'TRAINING_PROFESSIONAL', N'Training / Workshop',
         N'This is a professional training or workshop registration form. Use clear, instructional language. Collect role, experience level and dietary requirements if relevant.', 50, 1),
        (N'RESEARCH_CONSENT', N'Research / Study Consent',
         N'This is a research consent form. Be precise and neutral. Include purpose of study, data usage, withdrawal rights and contact details for questions.', 60, 1),
        (N'WEBINAR_ONLINE', N'Webinar / Online Event',
         N'This is an online webinar registration form. Emphasise timezone handling, recording access and minimal required fields. Use inclusive, global-friendly language.', 70, 1),
        (N'MEMBER_ONBOARDING', N'Member Onboarding',
         N'This is a member onboarding form. Warm and community-oriented. Collect contact details plus one or two interest/preference questions.', 80, 1),
        (N'CUSTOMER_SUPPORT', N'Support / Service Request',
         N'This is a customer support or service request form. Be empathetic and efficient. Collect issue category, description and urgency level.', 90, 1),
        (N'GENERAL_INQUIRY', N'General Inquiry',
         N'This is a general inquiry or contact form. Keep it simple and friendly. Ask for name, email, subject and message only.', 100, 1);
        """
    )


def downgrade() -> None:
    op.drop_table("FormPurpose", schema="ref")
