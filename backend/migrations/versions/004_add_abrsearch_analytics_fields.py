"""add ABRSearch analytics fields

Revision ID: 004_abrsearch_analytics
Revises: 003_add_validation_rule_enhancements
Create Date: 2025-10-18 00:00:00.000000

Story 1.10: Enhanced ABR Search Implementation
AC-1.10.8: Enterprise-Grade Caching (analytics fields)
AC-1.10.11: Success Rate Metrics (analytics fields)

Adds HitCount and LastHitAt fields to cache.ABRSearch table for analytics tracking.

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004_abrsearch_analytics'
down_revision = '003_validation_rule_enhancements'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add analytics fields to cache.ABRSearch table"""
    
    # Add HitCount column
    op.add_column(
        'ABRSearch',
        sa.Column('HitCount', sa.Integer(), nullable=False, server_default='0'),
        schema='cache'
    )
    
    # Add LastHitAt column
    op.add_column(
        'ABRSearch',
        sa.Column('LastHitAt', sa.DateTime(), nullable=True),
        schema='cache'
    )
    
    # Create index for analytics queries (popular searches)
    op.create_index(
        'IX_ABRSearch_Analytics',
        'ABRSearch',
        ['HitCount', 'LastHitAt'],
        schema='cache'
    )


def downgrade() -> None:
    """Remove analytics fields from cache.ABRSearch table"""
    
    # Drop index
    op.drop_index('IX_ABRSearch_Analytics', table_name='ABRSearch', schema='cache')
    
    # Drop columns
    op.drop_column('ABRSearch', 'LastHitAt', schema='cache')
    op.drop_column('ABRSearch', 'HitCount', schema='cache')
