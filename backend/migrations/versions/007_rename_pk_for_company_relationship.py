"""rename PK for CompanyRelationship

Revision ID: 007
Revises: 006
Create Date: 2025-10-18 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '007'
down_revision = '006'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'CompanyRelationship',
        'RelationshipID',
        new_column_name='CompanyRelationshipID',
        existing_type=sa.BigInteger(),
        schema='dbo'
    )


def downgrade():
    op.alter_column(
        'CompanyRelationship',
        'CompanyRelationshipID',
        new_column_name='RelationshipID',
        existing_type=sa.BigInteger(),
        schema='dbo'
    )
