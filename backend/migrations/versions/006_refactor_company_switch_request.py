"""refactor company switch request table

Revision ID: 006
Revises: 005
Create Date: 2025-10-18 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None


def upgrade():
    # ### Create and seed ref tables ###
    op.create_table('CompanySwitchRequestType',
        sa.Column('CompanySwitchRequestTypeID', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('TypeName', sa.String(length=50), nullable=False),
        sa.Column('TypeDescription', sa.String(length=255), nullable=True),
        sa.Column('IsActive', sa.Boolean(), server_default='1', nullable=False),
        # Audit columns...
        sa.PrimaryKeyConstraint('CompanySwitchRequestTypeID'),
        sa.UniqueConstraint('TypeName'),
        schema='ref'
    )
    op.execute("INSERT INTO ref.CompanySwitchRequestType (TypeName) VALUES ('access_request'), ('invitation_accepted'), ('relationship_join');")

    op.create_table('CompanySwitchRequestStatus',
        sa.Column('CompanySwitchRequestStatusID', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('StatusName', sa.String(length=50), nullable=False),
        sa.Column('StatusDescription', sa.String(length=255), nullable=True),
        sa.Column('IsActive', sa.Boolean(), server_default='1', nullable=False),
        # Audit columns...
        sa.PrimaryKeyConstraint('CompanySwitchRequestStatusID'),
        sa.UniqueConstraint('StatusName'),
        schema='ref'
    )
    op.execute("INSERT INTO ref.CompanySwitchRequestStatus (StatusName) VALUES ('pending'), ('approved'), ('rejected');")

    # ### Alter dbo.CompanySwitchRequest table ###
    op.add_column('CompanySwitchRequest', sa.Column('RequestTypeID', sa.Integer(), nullable=True), schema='dbo')
    op.add_column('CompanySwitchRequest', sa.Column('StatusID', sa.Integer(), nullable=True), schema='dbo')

    op.create_foreign_key(
        'FK_CompanySwitchRequest_RequestType', 'CompanySwitchRequest', 'CompanySwitchRequestType',
        ['RequestTypeID'], ['CompanySwitchRequestTypeID'], source_schema='dbo', referent_schema='ref'
    )
    op.create_foreign_key(
        'FK_CompanySwitchRequest_Status', 'CompanySwitchRequest', 'CompanySwitchRequestStatus',
        ['StatusID'], ['CompanySwitchRequestStatusID'], source_schema='dbo', referent_schema='ref'
    )

    # ### Data migration ###
    op.execute("""
        UPDATE dbo.CompanySwitchRequest
        SET RequestTypeID = rt.CompanySwitchRequestTypeID
        FROM dbo.CompanySwitchRequest csr
        JOIN ref.CompanySwitchRequestType rt ON csr.RequestType = rt.TypeName;
    """)
    op.execute("""
        UPDATE dbo.CompanySwitchRequest
        SET StatusID = rs.CompanySwitchRequestStatusID
        FROM dbo.CompanySwitchRequest csr
        JOIN ref.CompanySwitchRequestStatus rs ON csr.Status = rs.StatusName;
    """)

    # ### Final schema changes ###
    op.alter_column('CompanySwitchRequest', 'RequestTypeID', existing_type=sa.Integer(), nullable=False, schema='dbo')
    op.alter_column('CompanySwitchRequest', 'StatusID', existing_type=sa.Integer(), nullable=False, schema='dbo')
    op.drop_column('CompanySwitchRequest', 'RequestType', schema='dbo')
    op.drop_column('CompanySwitchRequest', 'Status', schema='dbo')
    
    # Renaming PK is complex; for this migration, we'll accept the model `name` override.
    # A manual script would be `sp_rename`


def downgrade():
    op.add_column('CompanySwitchRequest', sa.Column('RequestType', sa.String(length=50), nullable=True), schema='dbo')
    op.add_column('CompanySwitchRequest', sa.Column('Status', sa.String(length=20), nullable=True), schema='dbo')
    
    op.execute("""
        UPDATE dbo.CompanySwitchRequest
        SET RequestType = rt.TypeName
        FROM dbo.CompanySwitchRequest csr
        JOIN ref.CompanySwitchRequestType rt ON csr.RequestTypeID = rt.CompanySwitchRequestTypeID;
    """)
    op.execute("""
        UPDATE dbo.CompanySwitchRequest
        SET Status = rs.StatusName
        FROM dbo.CompanySwitchRequest csr
        JOIN ref.CompanySwitchRequestStatus rs ON csr.StatusID = rs.CompanySwitchRequestStatusID;
    """)
    
    op.alter_column('CompanySwitchRequest', 'RequestType', existing_type=sa.String(length=50), nullable=False, schema='dbo')
    op.alter_column('CompanySwitchRequest', 'Status', existing_type=sa.String(length=20), nullable=False, schema='dbo')
    
    op.drop_constraint('FK_CompanySwitchRequest_RequestType', 'CompanySwitchRequest', schema='dbo', type_='foreignkey')
    op.drop_constraint('FK_CompanySwitchRequest_Status', 'CompanySwitchRequest', schema='dbo', type_='foreignkey')
    
    op.drop_column('CompanySwitchRequest', 'RequestTypeID', schema='dbo')
    op.drop_column('CompanySwitchRequest', 'StatusID', schema='dbo')

    op.drop_table('CompanySwitchRequestType', schema='ref')
    op.drop_table('CompanySwitchRequestStatus', schema='ref')
