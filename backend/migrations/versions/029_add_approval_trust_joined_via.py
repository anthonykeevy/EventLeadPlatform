"""add_approval_trust_joined_via

Revision ID: 029
Revises: 028_external_approval_support
Create Date: 2025-11-26 06:20:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '029'
down_revision = '028_external_approval_support'
branch_labels = None
depends_on = None

def upgrade():
    # Create ad-hoc table for insert
    joined_via = table('JoinedVia',
        column('MethodCode', sa.String),
        column('MethodName', sa.String),
        column('Description', sa.String),
        column('IsActive', sa.Boolean),
        column('SortOrder', sa.Integer),
        column('CreatedDate', sa.DateTime),
        schema='ref'
    )

    op.bulk_insert(joined_via,
        [
            {
                'MethodCode': 'approval_trust',
                'MethodName': 'Approval Trust',
                'Description': 'Joined existing company based on prior trusted approval history',
                'IsActive': True,
                'SortOrder': 50,
                'CreatedDate': datetime.utcnow()
            }
        ]
    )

def downgrade():
    op.execute("DELETE FROM ref.JoinedVia WHERE MethodCode = 'approval_trust'")

