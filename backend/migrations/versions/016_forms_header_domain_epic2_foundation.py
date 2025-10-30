"""Forms Header Domain Epic 2 - Form Header & Access Control Foundation

Revision ID: 016_forms_header_domain_epic2_foundation
Revises: 015_events_domain_epic2_complete
Create Date: 2025-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = '016_forms_epic2'
down_revision = '015_events_domain_epic2_complete'
branch_labels = None
depends_on = None


def upgrade():
    # =====================================================================
    # 1. Create FormStatus Reference Table
    # =====================================================================
    op.create_table('FormStatus',
        sa.Column('FormStatusID', sa.Integer(), nullable=False),
        sa.Column('StatusCode', sa.String(length=20), nullable=False),
        sa.Column('StatusName', sa.String(length=50), nullable=False),
        sa.Column('StatusDescription', sa.String(length=200), nullable=True),
        sa.Column('StatusColor', sa.String(length=7), nullable=True),
        sa.Column('StatusIcon', sa.String(length=50), nullable=True),
        sa.Column('IsActive', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('SortOrder', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('FormStatusID'),
        sa.UniqueConstraint('StatusCode'),
        sa.ForeignKeyConstraint(['CreatedBy'], ['dbo.User.UserID'], name='FK_FormStatus_CreatedBy'),
        sa.ForeignKeyConstraint(['UpdatedBy'], ['dbo.User.UserID'], name='FK_FormStatus_UpdatedBy'),
        sa.ForeignKeyConstraint(['DeletedBy'], ['dbo.User.UserID'], name='FK_FormStatus_DeletedBy'),
        schema='ref'
    )
    
    # Insert FormStatus seed data
    op.execute("""
        INSERT INTO [ref].[FormStatus] (StatusCode, StatusName, StatusDescription, StatusColor, StatusIcon, IsActive, SortOrder, CreatedBy)
        VALUES
            ('DRAFT', 'Draft', 'Form is being created and edited', '#FFA500', 'draft-icon', 1, 1, 1),
            ('REVIEW', 'Under Review', 'Form submitted for approval', '#17A2B8', 'review-icon', 1, 2, 1),
            ('PUBLISHED', 'Published', 'Form is live and accepting submissions', '#28A745', 'published-icon', 1, 3, 1),
            ('PAUSED', 'Paused', 'Form is temporarily paused', '#FFC107', 'paused-icon', 1, 4, 1),
            ('ARCHIVED', 'Archived', 'Form has been archived', '#6C757D', 'archived-icon', 1, 5, 1),
            ('DELETED', 'Deleted', 'Form has been deleted', '#DC3545', 'deleted-icon', 1, 6, 1)
    """)
    
    # =====================================================================
    # 2. Create FormAccessControlAccessType Reference Table
    # =====================================================================
    op.create_table('FormAccessControlAccessType',
        sa.Column('FormAccessControlAccessTypeID', sa.Integer(), nullable=False),
        sa.Column('AccessTypeCode', sa.String(length=20), nullable=False),
        sa.Column('AccessTypeName', sa.String(length=50), nullable=False),
        sa.Column('AccessTypeDescription', sa.String(length=200), nullable=True),
        sa.Column('IsActive', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('SortOrder', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('FormAccessControlAccessTypeID'),
        sa.UniqueConstraint('AccessTypeCode'),
        sa.ForeignKeyConstraint(['CreatedBy'], ['dbo.User.UserID'], name='FK_FormAccessControlAccessType_CreatedBy'),
        sa.ForeignKeyConstraint(['UpdatedBy'], ['dbo.User.UserID'], name='FK_FormAccessControlAccessType_UpdatedBy'),
        sa.ForeignKeyConstraint(['DeletedBy'], ['dbo.User.UserID'], name='FK_FormAccessControlAccessType_DeletedBy'),
        schema='ref'
    )
    
    # Insert FormAccessControlAccessType seed data
    op.execute("""
        INSERT INTO [ref].[FormAccessControlAccessType] (AccessTypeCode, AccessTypeName, AccessTypeDescription, IsActive, SortOrder, CreatedBy)
        VALUES
            ('VIEW', 'View', 'Can view form and basic information', 1, 1, 1),
            ('EDIT', 'Edit', 'Can edit form content and settings', 1, 2, 1),
            ('MANAGE', 'Manage', 'Can manage form settings and access control', 1, 3, 1),
            ('SUBMIT', 'Submit', 'Can submit responses to the form', 1, 4, 1),
            ('ANALYZE', 'Analyze', 'Can view form analytics and responses', 1, 5, 1)
    """)
    
    # =====================================================================
    # 3. Create FormApprovalStatus Reference Table
    # =====================================================================
    op.create_table('FormApprovalStatus',
        sa.Column('FormApprovalStatusID', sa.Integer(), nullable=False),
        sa.Column('ApprovalStatusCode', sa.String(length=20), nullable=False),
        sa.Column('ApprovalStatusName', sa.String(length=50), nullable=False),
        sa.Column('ApprovalStatusDescription', sa.String(length=200), nullable=True),
        sa.Column('IsRequiresApproval', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('IsActive', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('SortOrder', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('FormApprovalStatusID'),
        sa.UniqueConstraint('ApprovalStatusCode'),
        sa.ForeignKeyConstraint(['CreatedBy'], ['dbo.User.UserID'], name='FK_FormApprovalStatus_CreatedBy'),
        sa.ForeignKeyConstraint(['UpdatedBy'], ['dbo.User.UserID'], name='FK_FormApprovalStatus_UpdatedBy'),
        sa.ForeignKeyConstraint(['DeletedBy'], ['dbo.User.UserID'], name='FK_FormApprovalStatus_DeletedBy'),
        schema='ref'
    )
    
    # Insert FormApprovalStatus seed data
    op.execute("""
        INSERT INTO [ref].[FormApprovalStatus] (ApprovalStatusCode, ApprovalStatusName, ApprovalStatusDescription, IsRequiresApproval, IsActive, SortOrder, CreatedBy)
        VALUES
            ('NO_APPROVAL', 'No Approval Required', 'Form does not require approval', 0, 1, 1, 1),
            ('PENDING', 'Pending Approval', 'Form is waiting for approval', 1, 1, 2, 1),
            ('APPROVED', 'Approved', 'Form has been approved', 0, 1, 3, 1),
            ('REJECTED', 'Rejected', 'Form has been rejected', 0, 1, 4, 1),
            ('CANCELLED', 'Cancelled', 'Form approval was cancelled', 0, 1, 5, 1),
            ('EXPIRED', 'Expired', 'Form approval has expired', 0, 1, 6, 1)
    """)
    
    # =====================================================================
    # 4. Create Form Table (Enhanced Form Header)
    # =====================================================================
    op.create_table('Form',
        sa.Column('FormID', sa.BigInteger(), nullable=False),
        sa.Column('FormName', sa.String(length=200), nullable=False),
        sa.Column('FormDescription', sa.Text(), nullable=True),
        sa.Column('CompanyID', sa.BigInteger(), nullable=False),
        sa.Column('EventID', sa.BigInteger(), nullable=True),
        sa.Column('FormStatusID', sa.Integer(), nullable=False),
        sa.Column('FormApprovalStatusID', sa.Integer(), nullable=False),
        sa.Column('IsPublic', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('DeploymentCost', sa.DECIMAL(10,2), nullable=True),
        sa.Column('TotalSubmissions', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('DemoLeadsCollected', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('ProductionLeadsCollected', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('LastSubmissionDate', sa.DateTime(), nullable=True),
        sa.Column('LastActivityDate', sa.DateTime(), nullable=True),
        sa.Column('FormThumbnailURL', sa.String(length=500), nullable=True),
        sa.Column('FormPreviewURL', sa.String(length=500), nullable=True),
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('FormID'),
        sa.ForeignKeyConstraint(['CompanyID'], ['dbo.Company.CompanyID'], name='FK_Form_Company'),
        sa.ForeignKeyConstraint(['EventID'], ['dbo.Event.EventID'], name='FK_Form_Event'),
        sa.ForeignKeyConstraint(['FormStatusID'], ['ref.FormStatus.FormStatusID'], name='FK_Form_FormStatus'),
        sa.ForeignKeyConstraint(['FormApprovalStatusID'], ['ref.FormApprovalStatus.FormApprovalStatusID'], name='FK_Form_FormApprovalStatus'),
        sa.ForeignKeyConstraint(['CreatedBy'], ['dbo.User.UserID'], name='FK_Form_CreatedBy'),
        sa.ForeignKeyConstraint(['UpdatedBy'], ['dbo.User.UserID'], name='FK_Form_UpdatedBy'),
        sa.ForeignKeyConstraint(['DeletedBy'], ['dbo.User.UserID'], name='FK_Form_DeletedBy'),
        sa.CheckConstraint("DeploymentCost IS NULL OR DeploymentCost >= 0", name='CK_Form_DeploymentCost'),
        sa.CheckConstraint("TotalSubmissions >= 0 AND DemoLeadsCollected >= 0 AND ProductionLeadsCollected >= 0", name='CK_Form_SubmissionCounts'),
        schema='dbo'
    )
    
    # =====================================================================
    # 5. Create FormAccessControl Table
    # =====================================================================
    op.create_table('FormAccessControl',
        sa.Column('FormAccessControlID', sa.BigInteger(), nullable=False),
        sa.Column('FormID', sa.BigInteger(), nullable=False),
        sa.Column('UserID', sa.BigInteger(), nullable=False),
        sa.Column('CompanyID', sa.BigInteger(), nullable=False),
        sa.Column('FormAccessControlAccessTypeID', sa.Integer(), nullable=False),
        sa.Column('CompanyRelationshipTypeID', sa.Integer(), nullable=False),
        sa.Column('GrantedBy', sa.BigInteger(), nullable=False),
        sa.Column('GrantedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('ExpiryDate', sa.DateTime(), nullable=True),
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.PrimaryKeyConstraint('FormAccessControlID'),
        sa.ForeignKeyConstraint(['FormID'], ['dbo.Form.FormID'], name='FK_FormAccessControl_Form'),
        sa.ForeignKeyConstraint(['UserID'], ['dbo.User.UserID'], name='FK_FormAccessControl_User'),
        sa.ForeignKeyConstraint(['CompanyID'], ['dbo.Company.CompanyID'], name='FK_FormAccessControl_Company'),
        sa.ForeignKeyConstraint(['FormAccessControlAccessTypeID'], ['ref.FormAccessControlAccessType.FormAccessControlAccessTypeID'], name='FK_FormAccessControl_AccessType'),
        sa.ForeignKeyConstraint(['CompanyRelationshipTypeID'], ['ref.CompanyRelationshipType.CompanyRelationshipTypeID'], name='FK_FormAccessControl_CompanyRelationshipType'),
        sa.ForeignKeyConstraint(['GrantedBy'], ['dbo.User.UserID'], name='FK_FormAccessControl_GrantedBy'),
        sa.ForeignKeyConstraint(['CreatedBy'], ['dbo.User.UserID'], name='FK_FormAccessControl_CreatedBy'),
        sa.ForeignKeyConstraint(['UpdatedBy'], ['dbo.User.UserID'], name='FK_FormAccessControl_UpdatedBy'),
        sa.CheckConstraint("ExpiryDate IS NULL OR ExpiryDate > GrantedDate", name='CK_FormAccessControl_ExpiryDate'),
        schema='dbo'
    )
    
    # =====================================================================
    # 6. Create Indexes for Performance
    # =====================================================================
    # Form table indexes
    op.create_index('IX_Form_Company', 'Form', ['CompanyID', 'IsDeleted'], unique=False, schema='dbo')
    op.create_index('IX_Form_Event', 'Form', ['EventID', 'IsDeleted'], unique=False, schema='dbo')
    op.create_index('IX_Form_Status', 'Form', ['FormStatusID', 'IsDeleted'], unique=False, schema='dbo')
    op.create_index('IX_Form_ApprovalStatus', 'Form', ['FormApprovalStatusID', 'IsDeleted'], unique=False, schema='dbo')
    op.create_index('IX_Form_Activity', 'Form', ['LastActivityDate', 'IsDeleted'], unique=False, schema='dbo')
    op.create_index('IX_Form_Public', 'Form', ['IsPublic', 'IsDeleted'], unique=False, schema='dbo')
    
    # FormAccessControl table indexes
    op.create_index('IX_FormAccessControl_Form', 'FormAccessControl', ['FormID', 'IsDeleted'], unique=False, schema='dbo')
    op.create_index('IX_FormAccessControl_User', 'FormAccessControl', ['UserID', 'IsDeleted'], unique=False, schema='dbo')
    op.create_index('IX_FormAccessControl_Company', 'FormAccessControl', ['CompanyID', 'IsDeleted'], unique=False, schema='dbo')
    op.create_index('IX_FormAccessControl_AccessType', 'FormAccessControl', ['FormAccessControlAccessTypeID', 'IsDeleted'], unique=False, schema='dbo')
    op.create_index('IX_FormAccessControl_Expiry', 'FormAccessControl', ['ExpiryDate', 'IsDeleted'], unique=False, schema='dbo')


def downgrade():
    # =====================================================================
    # 6. Drop Indexes
    # =====================================================================
    op.drop_index('IX_FormAccessControl_Expiry', 'FormAccessControl', schema='dbo')
    op.drop_index('IX_FormAccessControl_AccessType', 'FormAccessControl', schema='dbo')
    op.drop_index('IX_FormAccessControl_Company', 'FormAccessControl', schema='dbo')
    op.drop_index('IX_FormAccessControl_User', 'FormAccessControl', schema='dbo')
    op.drop_index('IX_FormAccessControl_Form', 'FormAccessControl', schema='dbo')
    op.drop_index('IX_Form_Public', 'Form', schema='dbo')
    op.drop_index('IX_Form_Activity', 'Form', schema='dbo')
    op.drop_index('IX_Form_ApprovalStatus', 'Form', schema='dbo')
    op.drop_index('IX_Form_Status', 'Form', schema='dbo')
    op.drop_index('IX_Form_Event', 'Form', schema='dbo')
    op.drop_index('IX_Form_Company', 'Form', schema='dbo')
    
    # =====================================================================
    # 5. Drop FormAccessControl Table
    # =====================================================================
    op.drop_table('FormAccessControl', schema='dbo')
    
    # =====================================================================
    # 4. Drop Form Table
    # =====================================================================
    op.drop_table('Form', schema='dbo')
    
    # =====================================================================
    # 3. Drop FormApprovalStatus Table
    # =====================================================================
    op.drop_table('FormApprovalStatus', schema='ref')
    
    # =====================================================================
    # 2. Drop FormAccessControlAccessType Table
    # =====================================================================
    op.drop_table('FormAccessControlAccessType', schema='ref')
    
    # =====================================================================
    # 1. Drop FormStatus Table
    # =====================================================================
    op.drop_table('FormStatus', schema='ref')
