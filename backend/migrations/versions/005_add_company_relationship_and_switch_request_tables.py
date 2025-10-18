"""add company relationship, type, and switch request tables

Revision ID: 005
Revises: 004
Create Date: 2025-10-18 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '005'
down_revision = '004_abrsearch_analytics'
branch_labels = None
depends_on = None


def upgrade():
    # ### Create ref.CompanyRelationshipType table ###
    company_relationship_type_table = op.create_table('CompanyRelationshipType',
    sa.Column('CompanyRelationshipTypeID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('TypeName', sa.String(length=50), nullable=False),
    sa.Column('TypeDescription', sa.String(length=255), nullable=True),
    sa.Column('IsActive', sa.Boolean(), nullable=False),
    sa.Column('CreatedDate', sa.DateTime(), server_default=sa.text('getutcdate()'), nullable=False),
    sa.Column('CreatedBy', sa.BigInteger(), nullable=True),
    sa.Column('UpdatedDate', sa.DateTime(), server_default=sa.text('getutcdate()'), nullable=False),
    sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
    sa.Column('IsDeleted', sa.Boolean(), nullable=False),
    sa.Column('DeletedDate', sa.DateTime(), nullable=True),
    sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['CreatedBy'], ['dbo.User.UserID'], ),
    sa.ForeignKeyConstraint(['DeletedBy'], ['dbo.User.UserID'], ),
    sa.ForeignKeyConstraint(['UpdatedBy'], ['dbo.User.UserID'], ),
    sa.PrimaryKeyConstraint('CompanyRelationshipTypeID'),
    sa.UniqueConstraint('TypeName'),
    schema='ref'
    )

    # ### Seed ref.CompanyRelationshipType table ###
    op.bulk_insert(company_relationship_type_table,
        [
            {'CompanyRelationshipTypeID': 1, 'TypeName': 'branch', 'TypeDescription': 'A child company operating as a branch of a parent company (e.g., Head Office -> Melbourne Branch).', 'IsActive': True, 'IsDeleted': False},
            {'CompanyRelationshipTypeID': 2, 'TypeName': 'subsidiary', 'TypeDescription': 'A child company owned or controlled by a parent or holding company.', 'IsActive': True, 'IsDeleted': False},
            {'CompanyRelationshipTypeID': 3, 'TypeName': 'partner', 'TypeDescription': 'A relationship between two companies of equal standing for collaboration (e.g., Event Organizer ↔ Venue Partner).', 'IsActive': True, 'IsDeleted': False}
        ]
    )

    # ### Create dbo.CompanyRelationship table ###
    op.create_table('CompanyRelationship',
    sa.Column('RelationshipID', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('ParentCompanyID', sa.BigInteger(), nullable=False),
    sa.Column('ChildCompanyID', sa.BigInteger(), nullable=False),
    sa.Column('RelationshipTypeID', sa.Integer(), nullable=False),
    sa.Column('Status', sa.String(length=20), nullable=False),
    sa.Column('EstablishedBy', sa.BigInteger(), nullable=False),
    sa.Column('EstablishedAt', sa.DateTime(), server_default=sa.text('getutcdate()'), nullable=False),
    sa.Column('CreatedDate', sa.DateTime(), server_default=sa.text('getutcdate()'), nullable=False),
    sa.Column('CreatedBy', sa.BigInteger(), nullable=True),
    sa.Column('UpdatedDate', sa.DateTime(), server_default=sa.text('getutcdate()'), nullable=False),
    sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
    sa.Column('IsDeleted', sa.Boolean(), nullable=False),
    sa.Column('DeletedDate', sa.DateTime(), nullable=True),
    sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
    sa.CheckConstraint('ParentCompanyID <> ChildCompanyID', name='CK_CompanyRelationship_NotSelf'),
    sa.ForeignKeyConstraint(['ChildCompanyID'], ['dbo.Company.CompanyID'], ),
    sa.ForeignKeyConstraint(['CreatedBy'], ['dbo.User.UserID'], ),
    sa.ForeignKeyConstraint(['DeletedBy'], ['dbo.User.UserID'], ),
    sa.ForeignKeyConstraint(['EstablishedBy'], ['dbo.User.UserID'], ),
    sa.ForeignKeyConstraint(['ParentCompanyID'], ['dbo.Company.CompanyID'], ),
    sa.ForeignKeyConstraint(['RelationshipTypeID'], ['ref.CompanyRelationshipType.CompanyRelationshipTypeID'], ),
    sa.ForeignKeyConstraint(['UpdatedBy'], ['dbo.User.UserID'], ),
    sa.PrimaryKeyConstraint('RelationshipID'),
    sa.UniqueConstraint('ParentCompanyID', 'ChildCompanyID', name='UQ_CompanyRelationship'),
    schema='dbo'
    )
    op.create_index(op.f('ix_dbo_CompanyRelationship_ChildCompanyID'), 'CompanyRelationship', ['ChildCompanyID'], unique=False, schema='dbo')
    op.create_index(op.f('ix_dbo_CompanyRelationship_ParentCompanyID'), 'CompanyRelationship', ['ParentCompanyID'], unique=False, schema='dbo')
    op.create_index(op.f('ix_dbo_CompanyRelationship_RelationshipTypeID'), 'CompanyRelationship', ['RelationshipTypeID'], unique=False, schema='dbo')

    # ### Create dbo.CompanySwitchRequest table ###
    op.create_table('CompanySwitchRequest',
    sa.Column('RequestID', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('UserID', sa.BigInteger(), nullable=False),
    sa.Column('FromCompanyID', sa.BigInteger(), nullable=True),
    sa.Column('ToCompanyID', sa.BigInteger(), nullable=False),
    sa.Column('RequestType', sa.String(length=50), nullable=False),
    sa.Column('Status', sa.String(length=20), nullable=False),
    sa.Column('RequestedBy', sa.BigInteger(), nullable=False),
    sa.Column('RequestedAt', sa.DateTime(), server_default=sa.text('getutcdate()'), nullable=False),
    sa.Column('Reason', sa.String(length=500), nullable=True),
    sa.Column('ApprovedBy', sa.BigInteger(), nullable=True),
    sa.Column('ApprovedAt', sa.DateTime(), nullable=True),
    sa.Column('RejectedBy', sa.BigInteger(), nullable=True),
    sa.Column('RejectedAt', sa.DateTime(), nullable=True),
    sa.Column('RejectionReason', sa.String(length=500), nullable=True),
    sa.Column('CreatedDate', sa.DateTime(), server_default=sa.text('getutcdate()'), nullable=False),
    sa.Column('CreatedBy', sa.BigInteger(), nullable=True),
    sa.Column('UpdatedDate', sa.DateTime(), server_default=sa.text('getutcdate()'), nullable=False),
    sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
    sa.Column('IsDeleted', sa.Boolean(), nullable=False),
    sa.Column('DeletedDate', sa.DateTime(), nullable=True),
    sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['ApprovedBy'], ['dbo.User.UserID'], ),
    sa.ForeignKeyConstraint(['CreatedBy'], ['dbo.User.UserID'], ),
    sa.ForeignKeyConstraint(['DeletedBy'], ['dbo.User.UserID'], ),
    sa.ForeignKeyConstraint(['FromCompanyID'], ['dbo.Company.CompanyID'], ),
    sa.ForeignKeyConstraint(['RejectedBy'], ['dbo.User.UserID'], ),
    sa.ForeignKeyConstraint(['RequestedBy'], ['dbo.User.UserID'], ),
    sa.ForeignKeyConstraint(['ToCompanyID'], ['dbo.Company.CompanyID'], ),
    sa.ForeignKeyConstraint(['UpdatedBy'], ['dbo.User.UserID'], ),
    sa.ForeignKeyConstraint(['UserID'], ['dbo.User.UserID'], ),
    sa.PrimaryKeyConstraint('RequestID'),
    schema='dbo'
    )
    op.create_index(op.f('ix_dbo_CompanySwitchRequest_ToCompanyID'), 'CompanySwitchRequest', ['ToCompanyID'], unique=False, schema='dbo')
    op.create_index(op.f('ix_dbo_CompanySwitchRequest_UserID'), 'CompanySwitchRequest', ['UserID'], unique=False, schema='dbo')


def downgrade():
    # ### Drop tables in reverse order of creation ###
    op.drop_index(op.f('ix_dbo_CompanySwitchRequest_UserID'), table_name='CompanySwitchRequest', schema='dbo')
    op.drop_index(op.f('ix_dbo_CompanySwitchRequest_ToCompanyID'), table_name='CompanySwitchRequest', schema='dbo')
    op.drop_table('CompanySwitchRequest', schema='dbo')

    op.drop_index(op.f('ix_dbo_CompanyRelationship_RelationshipTypeID'), table_name='CompanyRelationship', schema='dbo')
    op.drop_index(op.f('ix_dbo_CompanyRelationship_ParentCompanyID'), table_name='CompanyRelationship', schema='dbo')
    op.drop_index(op.f('ix_dbo_CompanyRelationship_ChildCompanyID'), table_name='CompanyRelationship', schema='dbo')
    op.drop_table('CompanyRelationship', schema='dbo')

    op.drop_table('CompanyRelationshipType', schema='ref')
