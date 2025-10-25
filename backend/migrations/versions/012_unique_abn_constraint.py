"""Add unique constraint on Company.ABN (where ABN is not NULL)

Revision ID: 012
Revises: 011
Create Date: 2025-10-25

Story 1.19: Prevent duplicate companies with same ABN

Business Rule:
- Companies WITH ABN: Must be unique (one company per ABN)
- Companies WITHOUT ABN: Can have duplicates (sole traders, manual entries)

Technical Implementation:
- Filtered unique index: UNIQUE WHERE ABN IS NOT NULL
- Allows multiple NULL ABNs (SQL Server treats NULLs as distinct)
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '012'
down_revision = '011'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Add unique constraint on Company.ABN (excluding NULL values)
    
    SQL Server filtered index allows:
    - Only ONE company with ABN '53102443916'
    - Multiple companies with ABN = NULL (sole traders, etc.)
    """
    # Create filtered unique index on ABN
    op.execute("""
        CREATE UNIQUE NONCLUSTERED INDEX UQ_Company_ABN
        ON dbo.Company(ABN)
        WHERE ABN IS NOT NULL AND IsDeleted = 0;
    """)
    
    # Add helpful comment
    op.execute("""
        EXEC sys.sp_addextendedproperty 
            @name = N'MS_Description',
            @value = N'Prevents duplicate companies with same ABN. Allows multiple NULL ABNs for sole traders.',
            @level0type = N'SCHEMA', @level0name = N'dbo',
            @level1type = N'TABLE', @level1name = N'Company',
            @level2type = N'INDEX', @level2name = N'UQ_Company_ABN';
    """)


def downgrade() -> None:
    """Remove unique constraint on ABN"""
    op.execute("DROP INDEX UQ_Company_ABN ON dbo.Company;")

