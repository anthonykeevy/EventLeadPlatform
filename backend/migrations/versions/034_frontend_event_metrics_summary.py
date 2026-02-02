"""Add metrics summary columns to log.FrontendEvent

Revision ID: 034
Revises: 033_frontend_logging
Create Date: 2026-01-20 00:00:00.000000

Adds structured metrics storage and summary columns to improve agent diagnostics.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = '034'
down_revision = '033'
branch_labels = None
depends_on = None


def upgrade():
    """Add metrics columns to FrontendEvent"""
    op.add_column(
        'FrontendEvent',
        sa.Column('MetricsJson', mssql.NVARCHAR(length='MAX'), nullable=True),
        schema='log'
    )
    op.add_column(
        'FrontendEvent',
        sa.Column('LayoutType', mssql.NVARCHAR(length=50), nullable=True),
        schema='log'
    )
    op.add_column(
        'FrontendEvent',
        sa.Column('ObjectCount', sa.Integer(), nullable=True),
        schema='log'
    )
    op.add_column(
        'FrontendEvent',
        sa.Column('ContainerWidth', sa.Integer(), nullable=True),
        schema='log'
    )
    op.add_column(
        'FrontendEvent',
        sa.Column('ContainerHeight', sa.Integer(), nullable=True),
        schema='log'
    )
    op.add_column(
        'FrontendEvent',
        sa.Column('GridColumns', sa.Integer(), nullable=True),
        schema='log'
    )
    op.add_column(
        'FrontendEvent',
        sa.Column('GridRows', sa.Integer(), nullable=True),
        schema='log'
    )
    op.add_column(
        'FrontendEvent',
        sa.Column('HasValidationObject', sa.Boolean(), nullable=True),
        schema='log'
    )

    op.execute("UPDATE [log].[FrontendEvent] SET HasValidationObject = 0 WHERE HasValidationObject IS NULL")
    op.execute(
        "ALTER TABLE [log].[FrontendEvent] "
        "ADD CONSTRAINT DF_FrontendEvent_HasValidationObject DEFAULT 0 FOR HasValidationObject"
    )
    op.alter_column(
        'FrontendEvent',
        'HasValidationObject',
        nullable=False,
        existing_type=mssql.BIT(),
        schema='log'
    )


def downgrade():
    """Remove metrics columns from FrontendEvent"""
    op.execute(
        "ALTER TABLE [log].[FrontendEvent] "
        "DROP CONSTRAINT DF_FrontendEvent_HasValidationObject"
    )
    op.drop_column('FrontendEvent', 'HasValidationObject', schema='log')
    op.drop_column('FrontendEvent', 'GridRows', schema='log')
    op.drop_column('FrontendEvent', 'GridColumns', schema='log')
    op.drop_column('FrontendEvent', 'ContainerHeight', schema='log')
    op.drop_column('FrontendEvent', 'ContainerWidth', schema='log')
    op.drop_column('FrontendEvent', 'ObjectCount', schema='log')
    op.drop_column('FrontendEvent', 'LayoutType', schema='log')
    op.drop_column('FrontendEvent', 'MetricsJson', schema='log')
