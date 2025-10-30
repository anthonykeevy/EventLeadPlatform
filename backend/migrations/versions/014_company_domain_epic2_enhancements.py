"""Company Domain Epic 2 Enhancements - Enhanced Billing Relationships & Approval Workflows

Revision ID: 014_company_domain_epic2_enhancements
Revises: 013_enhanced_user_profile
Create Date: 2025-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = '014_company_epic2'
down_revision = '013_enhanced_user_profile'
branch_labels = None
depends_on = None


def upgrade():
    # =====================================================================
    # 1. Extend CompanySwitchRequest Table for Form Deployment
    # =====================================================================
    op.add_column('CompanySwitchRequest', sa.Column('RequestedAmount', sa.DECIMAL(10,2), nullable=True), schema='dbo')
    op.add_column('CompanySwitchRequest', sa.Column('RequestDescription', sa.Text(), nullable=True), schema='dbo')
    op.add_column('CompanySwitchRequest', sa.Column('EventDate', sa.DateTime(), nullable=True), schema='dbo')
    op.add_column('CompanySwitchRequest', sa.Column('UrgencyLevel', sa.String(length=20), nullable=True), schema='dbo')
    
    # =====================================================================
    # 2. Add New Request Types to CompanySwitchRequestType
    # =====================================================================
    op.execute("""
        INSERT INTO [ref].[CompanySwitchRequestType] (TypeName, TypeDescription, IsActive)
        VALUES
            ('FormDeployment', 'Request approval for form deployment costs', 1),
            ('BillingChange', 'Request approval for billing relationship changes', 1),
            ('AccessRequest', 'Request access to company resources', 1),
            ('FormAccess', 'Request access to specific forms', 1)
    """)
    
    # =====================================================================
    # 3. Add New Status Types to CompanySwitchRequestStatus
    # =====================================================================
    op.execute("""
        INSERT INTO [ref].[CompanySwitchRequestStatus] (StatusName, StatusDescription, IsActive)
        VALUES
            ('Escalated', 'Request escalated to higher authority', 1),
            ('UnderReview', 'Request under detailed review', 1),
            ('PendingApprover', 'Waiting for specific approver', 1),
            ('EscalationRequired', 'Escalation needed - approver unavailable', 1)
    """)
    
    # =====================================================================
    # 4. Create ApprovalAuditTrail Table (New Table)
    # =====================================================================
    op.create_table('ApprovalAuditTrail',
        sa.Column('ApprovalAuditTrailID', sa.BigInteger(), nullable=False),
        sa.Column('CompanySwitchRequestID', sa.BigInteger(), nullable=False),
        sa.Column('Action', sa.String(length=50), nullable=False),
        sa.Column('ActionDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('PerformedBy', sa.BigInteger(), nullable=False),
        sa.Column('Comments', sa.Text(), nullable=True),
        sa.Column('PreviousStatus', sa.String(length=20), nullable=True),
        sa.Column('NewStatus', sa.String(length=20), nullable=True),
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint('ApprovalAuditTrailID'),
        sa.ForeignKeyConstraint(['CompanySwitchRequestID'], ['dbo.CompanySwitchRequest.RequestID'], name='FK_ApprovalAuditTrail_Request'),
        sa.ForeignKeyConstraint(['PerformedBy'], ['dbo.User.UserID'], name='FK_ApprovalAuditTrail_PerformedBy'),
        sa.ForeignKeyConstraint(['CreatedBy'], ['dbo.User.UserID'], name='FK_ApprovalAuditTrail_CreatedBy'),
        schema='audit'
    )
    
    # =====================================================================
    # 5. Extend User Table for External Approvers
    # =====================================================================
    op.add_column('User', sa.Column('IsExternalApprover', sa.Boolean(), nullable=False, server_default=sa.text('0')), schema='dbo')
    
    # =====================================================================
    # 6. Add New User Roles
    # =====================================================================
    op.execute("""
        INSERT INTO [ref].[UserRole] (RoleCode, RoleName, Description, RoleLevel, CanManagePlatform, CanManageAllCompanies, CanViewAllData, CanAssignSystemRoles, IsActive, SortOrder)
        VALUES
            ('HEAD_OFFICE_ADMIN', 'Head Office Administrator', 'Manages company relationships and approval workflows', 10, 0, 1, 1, 1, 1, 10),
            ('PARTNER_USER', 'Partner User', 'Form-level access to partner companies', 5, 0, 0, 0, 0, 1, 50),
            ('VENDOR_USER', 'Vendor User', 'Form-level access to vendor relationships', 5, 0, 0, 0, 0, 1, 51),
            ('CLIENT_USER', 'Client User', 'View-only access to assigned forms', 3, 0, 0, 0, 0, 1, 52),
            ('AFFILIATE_USER', 'Affiliate User', 'Form-level access to affiliate relationships', 5, 0, 0, 0, 0, 1, 53),
            ('EXTERNAL_APPROVER', 'External Approver', 'Email-only approver without platform access', 7, 0, 0, 0, 0, 1, 40)
    """)
    
    # =====================================================================
    # 7. Add Indexes for Performance
    # =====================================================================
    op.create_index('IX_CompanySwitchRequest_RequestedAmount', 'CompanySwitchRequest', ['RequestedAmount'], schema='dbo')
    op.create_index('IX_CompanySwitchRequest_EventDate', 'CompanySwitchRequest', ['EventDate'], schema='dbo')
    op.create_index('IX_CompanySwitchRequest_UrgencyLevel', 'CompanySwitchRequest', ['UrgencyLevel'], schema='dbo')
    op.create_index('IX_ApprovalAuditTrail_CompanySwitchRequestID', 'ApprovalAuditTrail', ['CompanySwitchRequestID'], schema='audit')
    op.create_index('IX_ApprovalAuditTrail_ActionDate', 'ApprovalAuditTrail', ['ActionDate'], schema='audit')
    op.create_index('IX_User_IsExternalApprover', 'User', ['IsExternalApprover'], schema='dbo')


def downgrade():
    # =====================================================================
    # 7. Drop Indexes
    # =====================================================================
    op.drop_index('IX_User_IsExternalApprover', 'User', schema='dbo')
    op.drop_index('IX_ApprovalAuditTrail_ActionDate', 'ApprovalAuditTrail', schema='audit')
    op.drop_index('IX_ApprovalAuditTrail_CompanySwitchRequestID', 'ApprovalAuditTrail', schema='audit')
    op.drop_index('IX_CompanySwitchRequest_UrgencyLevel', 'CompanySwitchRequest', schema='dbo')
    op.drop_index('IX_CompanySwitchRequest_EventDate', 'CompanySwitchRequest', schema='dbo')
    op.drop_index('IX_CompanySwitchRequest_RequestedAmount', 'CompanySwitchRequest', schema='dbo')
    
    # =====================================================================
    # 6. Remove New User Roles
    # =====================================================================
    op.execute("""
        DELETE FROM [ref].[UserRole] 
        WHERE RoleCode IN ('HEAD_OFFICE_ADMIN', 'PARTNER_USER', 'VENDOR_USER', 'CLIENT_USER', 'AFFILIATE_USER', 'EXTERNAL_APPROVER')
    """)
    
    # =====================================================================
    # 5. Remove External Approver Field
    # =====================================================================
    op.drop_column('User', 'IsExternalApprover', schema='dbo')
    
    # =====================================================================
    # 4. Drop ApprovalAuditTrail Table
    # =====================================================================
    op.drop_table('ApprovalAuditTrail', schema='audit')
    
    # =====================================================================
    # 3. Remove New Status Types
    # =====================================================================
    op.execute("""
        DELETE FROM [ref].[CompanySwitchRequestStatus] 
        WHERE StatusName IN ('Escalated', 'UnderReview', 'PendingApprover', 'EscalationRequired')
    """)
    
    # =====================================================================
    # 2. Remove New Request Types
    # =====================================================================
    op.execute("""
        DELETE FROM [ref].[CompanySwitchRequestType] 
        WHERE TypeName IN ('FormDeployment', 'BillingChange', 'AccessRequest', 'FormAccess')
    """)
    
    # =====================================================================
    # 1. Remove CompanySwitchRequest Extensions
    # =====================================================================
    op.drop_column('CompanySwitchRequest', 'UrgencyLevel', schema='dbo')
    op.drop_column('CompanySwitchRequest', 'EventDate', schema='dbo')
    op.drop_column('CompanySwitchRequest', 'RequestDescription', schema='dbo')
    op.drop_column('CompanySwitchRequest', 'RequestedAmount', schema='dbo')
