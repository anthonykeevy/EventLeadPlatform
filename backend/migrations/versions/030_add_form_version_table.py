"""add_form_version_table

Revision ID: e842a3b901c4
Revises: 1d6fd98cc9ea
Create Date: 2025-11-28 12:00:00.000000

Story: Story 3.1 - Form Versioning Architecture
Purpose: Create FormVersion table to store form schema history

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '030'
down_revision = '029'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'FormVersion',
        sa.Column('FormVersionID', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('FormID', sa.BigInteger(), nullable=False),
        sa.Column('VersionNumber', sa.Integer(), nullable=False),
        sa.Column('DefinitionJSON', sa.String(length=None), nullable=False), # NVARCHAR(MAX)
        sa.Column('VersionComment', sa.String(length=500), nullable=True),
        sa.Column('Status', sa.String(length=20), nullable=False, server_default='DRAFT'),
        sa.Column('IsActive', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('CreatedDate', sa.DateTime(), server_default=sa.func.getutcdate(), nullable=False),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=True),
        sa.Column('PublishedDate', sa.DateTime(), nullable=True),
        sa.Column('PublishedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('FormVersionID'),
        sa.ForeignKeyConstraint(['FormID'], ['dbo.Form.FormID'], ),
        sa.ForeignKeyConstraint(['CreatedBy'], ['dbo.User.UserID'], ),
        sa.ForeignKeyConstraint(['PublishedBy'], ['dbo.User.UserID'], ),
        schema='dbo'
    )
    op.create_index(op.f('ix_dbo_FormVersion_FormID'), 'FormVersion', ['FormID'], unique=False, schema='dbo')


def downgrade() -> None:
    op.drop_index(op.f('ix_dbo_FormVersion_FormID'), table_name='FormVersion', schema='dbo')
    op.drop_table('FormVersion', schema='dbo')

