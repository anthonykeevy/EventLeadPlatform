"""Fix UK phone display format - Story 1.20

UK phones should strip +44 prefix for local display.

Revision ID: 011
Revises: 010
Create Date: 2025-10-23

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '011'
down_revision = '010'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Fix UK phone display settings.
    UK phones normalize to +44... but should display as 07... (local format).
    """
    
    op.execute("""
        UPDATE [config].[ValidationRule]
        SET StripPrefix = 1  -- Strip +44 for display
        WHERE RuleKey IN ('PHONE_UK_MOBILE', 'PHONE_UK_LANDLINE')
    """)


def downgrade() -> None:
    """Revert to not stripping UK prefix"""
    op.execute("""
        UPDATE [config].[ValidationRule]
        SET StripPrefix = 0
        WHERE RuleKey IN ('PHONE_UK_MOBILE', 'PHONE_UK_LANDLINE')
    """)

