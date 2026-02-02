"""
Form Public Link Tokens (Story 3.8)

Creates dbo.FormPublicLink to support token-based public renderer URLs:
- Frontend route: /forms/:token
- Public API: GET /api/public/forms/{token}

Revision ID: 032_form_public_link_tokens
Revises: 031_google_fonts_domain
Create Date: 2025-12-14
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '032_form_public_link_tokens'
down_revision = '031_google_fonts_domain'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'FormPublicLink',
        sa.Column('FormPublicLinkID', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('FormID', sa.BigInteger(), nullable=False),
        sa.Column('Token', sa.String(length=255), nullable=False),
        sa.Column('LinkType', sa.String(length=20), nullable=False),  # PREVIEW | PRODUCTION
        sa.Column('IsActive', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('ExpiresAt', sa.DateTime(), nullable=True),
        sa.Column('LastAccessedAt', sa.DateTime(), nullable=True),
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('FormPublicLinkID'),
        sa.ForeignKeyConstraint(['FormID'], ['dbo.Form.FormID'], ),
        sa.ForeignKeyConstraint(['CreatedBy'], ['dbo.User.UserID'], ),
        schema='dbo'
    )

    # Unique token
    op.create_index('IX_FormPublicLink_Token', 'FormPublicLink', ['Token'], unique=True, schema='dbo')
    op.create_index('IX_FormPublicLink_FormID', 'FormPublicLink', ['FormID'], unique=False, schema='dbo')
    op.create_index('IX_FormPublicLink_IsActive', 'FormPublicLink', ['IsActive'], unique=False, schema='dbo')

    # Constraint: LinkType values
    op.execute("""
        ALTER TABLE dbo.FormPublicLink
        ADD CONSTRAINT CK_FormPublicLink_LinkType
        CHECK (LinkType IN ('PREVIEW', 'PRODUCTION'))
    """)


def downgrade() -> None:
    op.execute("ALTER TABLE dbo.FormPublicLink DROP CONSTRAINT CK_FormPublicLink_LinkType")
    op.drop_index('IX_FormPublicLink_IsActive', table_name='FormPublicLink', schema='dbo')
    op.drop_index('IX_FormPublicLink_FormID', table_name='FormPublicLink', schema='dbo')
    op.drop_index('IX_FormPublicLink_Token', table_name='FormPublicLink', schema='dbo')
    op.drop_table('FormPublicLink', schema='dbo')

