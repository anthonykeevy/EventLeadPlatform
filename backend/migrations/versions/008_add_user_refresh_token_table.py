"""add UserRefreshToken table for JWT refresh token storage

Revision ID: 008
Revises: 007
Create Date: 2025-10-20 14:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '008'
down_revision = '007'
branch_labels = None
depends_on = None


def upgrade():
    """
    Create dbo.UserRefreshToken table for JWT refresh token storage.
    
    This table supports the hybrid JWT approach:
    - Stores refresh tokens in database for revocation capability
    - Enables "logout from one device" feature
    - Tracks token usage and expiry
    - Provides security audit trail
    
    Related to Story 1.2: Login & JWT Tokens
    """
    op.create_table(
        'UserRefreshToken',
        sa.Column('UserRefreshTokenID', sa.BigInteger(), sa.Identity(always=False, start=1, increment=1), nullable=False),
        sa.Column('UserID', sa.BigInteger(), nullable=False),
        sa.Column('Token', sa.String(length=500), nullable=False),
        sa.Column('ExpiresAt', sa.DateTime(), nullable=False),
        sa.Column('IsUsed', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('UsedAt', sa.DateTime(), nullable=True),
        sa.Column('IsRevoked', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('RevokedAt', sa.DateTime(), nullable=True),
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.PrimaryKeyConstraint('UserRefreshTokenID', name='PK_UserRefreshToken'),
        sa.ForeignKeyConstraint(['UserID'], ['dbo.User.UserID'], name='FK_UserRefreshToken_User'),
        schema='dbo'
    )
    
    # Create indexes for performance
    op.create_index('IX_UserRefreshToken_UserID', 'UserRefreshToken', ['UserID'], unique=False, schema='dbo')
    op.create_index('IX_UserRefreshToken_Token', 'UserRefreshToken', ['Token'], unique=True, schema='dbo')
    op.create_index('IX_UserRefreshToken_ExpiresAt', 'UserRefreshToken', ['ExpiresAt'], unique=False, schema='dbo')


def downgrade():
    """
    Drop UserRefreshToken table and all associated indexes.
    """
    op.drop_index('IX_UserRefreshToken_ExpiresAt', table_name='UserRefreshToken', schema='dbo')
    op.drop_index('IX_UserRefreshToken_Token', table_name='UserRefreshToken', schema='dbo')
    op.drop_index('IX_UserRefreshToken_UserID', table_name='UserRefreshToken', schema='dbo')
    op.drop_table('UserRefreshToken', schema='dbo')



