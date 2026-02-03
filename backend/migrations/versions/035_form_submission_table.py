"""Create FormSubmission table for public submissions

Revision ID: 035
Revises: 034
Create Date: 2026-02-03

Story: 3.11 - Dynamic Submission (Outbox)
Purpose: Add dbo.FormSubmission for public submissions + idempotency
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql


# revision identifiers, used by Alembic.
revision = '035'
down_revision = '034'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'FormSubmission',
        sa.Column('FormSubmissionID', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('FormID', sa.BigInteger(), nullable=False),
        sa.Column('FormVersionID', sa.BigInteger(), nullable=False),
        sa.Column('FormPublicLinkID', sa.BigInteger(), nullable=False),
        sa.Column('LinkType', mssql.NVARCHAR(length=20), nullable=False),
        sa.Column('IdempotencyKey', mssql.NVARCHAR(length=255), nullable=False),
        sa.Column('SubmittedAtClient', mssql.DATETIME2(), nullable=False),
        sa.Column(
            'ReceivedAtServer',
            mssql.DATETIME2(),
            nullable=False,
            server_default=sa.func.getutcdate(),
        ),
        sa.Column('AnswersJSON', mssql.NVARCHAR(length=None), nullable=False),  # NVARCHAR(MAX)
        sa.Column('ContextJSON', mssql.NVARCHAR(length=None), nullable=True),  # NVARCHAR(MAX)
        sa.Column(
            'CreatedDate',
            mssql.DATETIME2(),
            nullable=False,
            server_default=sa.func.getutcdate(),
        ),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', mssql.BIT(), nullable=False, server_default=sa.text('0')),
        sa.Column('DeletedDate', mssql.DATETIME2(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('FormSubmissionID', name='PK_FormSubmission_FormSubmissionID'),
        sa.ForeignKeyConstraint(['FormID'], ['dbo.Form.FormID'], name='FK_FormSubmission_FormID'),
        sa.ForeignKeyConstraint(
            ['FormVersionID'],
            ['dbo.FormVersion.FormVersionID'],
            name='FK_FormSubmission_FormVersionID',
        ),
        sa.ForeignKeyConstraint(
            ['FormPublicLinkID'],
            ['dbo.FormPublicLink.FormPublicLinkID'],
            name='FK_FormSubmission_FormPublicLinkID',
        ),
        sa.ForeignKeyConstraint(['CreatedBy'], ['dbo.User.UserID'], name='FK_FormSubmission_CreatedBy'),
        sa.ForeignKeyConstraint(['DeletedBy'], ['dbo.User.UserID'], name='FK_FormSubmission_DeletedBy'),
        sa.UniqueConstraint(
            'FormPublicLinkID',
            'IdempotencyKey',
            name='UQ_FormSubmission_FormPublicLinkID_IdempotencyKey',
        ),
        schema='dbo',
    )
    op.create_index('IX_FormSubmission_FormID', 'FormSubmission', ['FormID'], unique=False, schema='dbo')
    op.create_index(
        'IX_FormSubmission_FormVersionID',
        'FormSubmission',
        ['FormVersionID'],
        unique=False,
        schema='dbo',
    )
    op.create_index(
        'IX_FormSubmission_FormPublicLinkID',
        'FormSubmission',
        ['FormPublicLinkID'],
        unique=False,
        schema='dbo',
    )


def downgrade() -> None:
    op.drop_index('IX_FormSubmission_FormPublicLinkID', table_name='FormSubmission', schema='dbo')
    op.drop_index('IX_FormSubmission_FormVersionID', table_name='FormSubmission', schema='dbo')
    op.drop_index('IX_FormSubmission_FormID', table_name='FormSubmission', schema='dbo')
    op.execute(
        """
        IF EXISTS (
            SELECT 1
            FROM sys.objects
            WHERE name = 'UQ_FormSubmission_FormPublicLinkID_IdempotencyKey' AND type = 'UQ'
        )
        ALTER TABLE [dbo].[FormSubmission]
        DROP CONSTRAINT [UQ_FormSubmission_FormPublicLinkID_IdempotencyKey];
        IF EXISTS (
            SELECT 1
            FROM sys.objects
            WHERE name = 'UQ_FormSubmission_IdempotencyKey' AND type = 'UQ'
        )
        ALTER TABLE [dbo].[FormSubmission]
        DROP CONSTRAINT [UQ_FormSubmission_IdempotencyKey];
        """
    )
    op.drop_constraint(
        'FK_FormSubmission_DeletedBy',
        'FormSubmission',
        schema='dbo',
        type_='foreignkey',
    )
    op.drop_constraint(
        'FK_FormSubmission_CreatedBy',
        'FormSubmission',
        schema='dbo',
        type_='foreignkey',
    )
    op.drop_constraint(
        'FK_FormSubmission_FormPublicLinkID',
        'FormSubmission',
        schema='dbo',
        type_='foreignkey',
    )
    op.drop_constraint(
        'FK_FormSubmission_FormVersionID',
        'FormSubmission',
        schema='dbo',
        type_='foreignkey',
    )
    op.drop_constraint(
        'FK_FormSubmission_FormID',
        'FormSubmission',
        schema='dbo',
        type_='foreignkey',
    )
    op.drop_table('FormSubmission', schema='dbo')
