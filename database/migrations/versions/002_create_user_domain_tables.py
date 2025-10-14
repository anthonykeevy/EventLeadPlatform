"""Create User domain tables (UserStatus, InvitationStatus, User, UserCompany, Invitation)

Revision ID: 002_user_domain_tables
Revises: 001_foundation_tables
Create Date: 2025-10-13 12:01:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = '002_user_domain_tables'
down_revision = '001_foundation_tables'
branch_labels = None
depends_on = None


def upgrade():
    """Create User domain tables"""
    
    # =====================================================================
    # LOOKUP TABLE: UserStatus
    # =====================================================================
    op.create_table('UserStatus',
        sa.Column('StatusCode', sa.NVARCHAR(20), nullable=False),
        sa.Column('DisplayName', sa.NVARCHAR(50), nullable=False),
        sa.Column('Description', sa.NVARCHAR(500), nullable=False),
        sa.Column('AllowLogin', sa.Boolean(), nullable=False),
        sa.Column('IsSystemStatus', sa.Boolean(), nullable=False, default=True),
        sa.Column('SortOrder', sa.Integer(), nullable=False),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=True),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('StatusCode')
    )
    
    # =====================================================================
    # LOOKUP TABLE: InvitationStatus
    # =====================================================================
    op.create_table('InvitationStatus',
        sa.Column('StatusCode', sa.NVARCHAR(20), nullable=False),
        sa.Column('DisplayName', sa.NVARCHAR(50), nullable=False),
        sa.Column('Description', sa.NVARCHAR(500), nullable=False),
        sa.Column('CanResend', sa.Boolean(), nullable=False),
        sa.Column('CanCancel', sa.Boolean(), nullable=False),
        sa.Column('IsFinalState', sa.Boolean(), nullable=False),
        sa.Column('IsSystemStatus', sa.Boolean(), nullable=False, default=True),
        sa.Column('SortOrder', sa.Integer(), nullable=False),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=True),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('StatusCode')
    )
    
    # =====================================================================
    # CORE TABLE: User
    # =====================================================================
    op.create_table('User',
        sa.Column('UserID', sa.BigInteger(), nullable=False),
        sa.Column('Email', sa.NVARCHAR(100), nullable=False),
        sa.Column('PasswordHash', sa.NVARCHAR(255), nullable=False),
        sa.Column('FirstName', sa.NVARCHAR(100), nullable=False),
        sa.Column('LastName', sa.NVARCHAR(100), nullable=False),
        sa.Column('Status', sa.NVARCHAR(20), nullable=False),
        sa.Column('OnboardingComplete', sa.Boolean(), nullable=False, default=False),
        sa.Column('EmailVerificationToken', sa.NVARCHAR(255), nullable=True),
        sa.Column('PasswordResetToken', sa.NVARCHAR(255), nullable=True),
        sa.Column('SessionToken', sa.NVARCHAR(255), nullable=True),
        sa.Column('AccessTokenVersion', sa.Integer(), nullable=False, default=1),
        sa.Column('RefreshTokenVersion', sa.Integer(), nullable=False, default=1),
        sa.Column('FailedLoginCount', sa.Integer(), nullable=False, default=0),
        sa.Column('LockedUntil', sa.DateTime(), nullable=True),
        sa.Column('LastLoginDate', sa.DateTime(), nullable=True),
        sa.Column('LastLoginIP', sa.NVARCHAR(45), nullable=True),
        sa.Column('Timezone', sa.NVARCHAR(50), nullable=True, default='UTC'),
        sa.Column('LanguagePreference', sa.NVARCHAR(2), nullable=True, default='en'),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=True),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('UserID'),
        sa.UniqueConstraint('Email', name='UQ_User_Email')
    )
    
    # =====================================================================
    # CORE TABLE: UserCompany (Multi-Company Access)
    # =====================================================================
    op.create_table('UserCompany',
        sa.Column('UserCompanyID', sa.BigInteger(), nullable=False),
        sa.Column('UserID', sa.BigInteger(), nullable=False),
        sa.Column('CompanyID', sa.BigInteger(), nullable=False),
        sa.Column('Role', sa.NVARCHAR(20), nullable=False, default='company_user'),
        sa.Column('Status', sa.NVARCHAR(20), nullable=False, default='active'),
        sa.Column('IsDefaultCompany', sa.Boolean(), nullable=False, default=False),
        sa.Column('JoinedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('JoinedVia', sa.NVARCHAR(20), nullable=False),
        sa.Column('InvitedByUserID', sa.BigInteger(), nullable=True),
        sa.Column('InvitationID', sa.BigInteger(), nullable=True),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=True),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('UserCompanyID'),
        sa.UniqueConstraint('UserID', 'CompanyID', name='UQ_UserCompany_User_Company')
    )
    
    # =====================================================================
    # CORE TABLE: Invitation
    # =====================================================================
    op.create_table('Invitation',
        sa.Column('InvitationID', sa.BigInteger(), nullable=False),
        sa.Column('CompanyID', sa.BigInteger(), nullable=False),
        sa.Column('InvitedByUserID', sa.BigInteger(), nullable=False),
        sa.Column('InvitedEmail', sa.NVARCHAR(100), nullable=False),
        sa.Column('InvitedFirstName', sa.NVARCHAR(100), nullable=True),
        sa.Column('InvitedLastName', sa.NVARCHAR(100), nullable=True),
        sa.Column('AssignedRole', sa.NVARCHAR(20), nullable=False, default='company_user'),
        sa.Column('InvitationToken', sa.NVARCHAR(255), nullable=False),
        sa.Column('Status', sa.NVARCHAR(20), nullable=False, default='pending'),
        sa.Column('ExpiresAt', sa.DateTime(), nullable=False),
        sa.Column('AcceptedAt', sa.DateTime(), nullable=True),
        sa.Column('AcceptedByUserID', sa.BigInteger(), nullable=True),
        sa.Column('CancelledAt', sa.DateTime(), nullable=True),
        sa.Column('CancelledByUserID', sa.BigInteger(), nullable=True),
        sa.Column('ResentCount', sa.Integer(), nullable=False, default=0),
        sa.Column('LastResentAt', sa.DateTime(), nullable=True),
        sa.Column('RelationshipContext', sa.NVARCHAR(200), nullable=True),
        # Audit Trail
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=True),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('InvitationID'),
        sa.UniqueConstraint('InvitationToken', name='UQ_Invitation_Token')
    )
    
    # =====================================================================
    # FOREIGN KEY CONSTRAINTS
    # =====================================================================
    
    # User foreign keys
    op.create_foreign_key('FK_User_Status', 'User', 'UserStatus', ['Status'], ['StatusCode'])
    
    # UserCompany foreign keys
    op.create_foreign_key('FK_UserCompany_User', 'UserCompany', 'User', ['UserID'], ['UserID'])
    op.create_foreign_key('FK_UserCompany_InvitedBy', 'UserCompany', 'User', ['InvitedByUserID'], ['UserID'])
    
    # Invitation foreign keys
    op.create_foreign_key('FK_Invitation_InvitedBy', 'Invitation', 'User', ['InvitedByUserID'], ['UserID'])
    op.create_foreign_key('FK_Invitation_AcceptedBy', 'Invitation', 'User', ['AcceptedByUserID'], ['UserID'])
    op.create_foreign_key('FK_Invitation_CancelledBy', 'Invitation', 'User', ['CancelledByUserID'], ['UserID'])
    op.create_foreign_key('FK_Invitation_Status', 'Invitation', 'InvitationStatus', ['Status'], ['StatusCode'])
    
    # =====================================================================
    # INDEXES
    # =====================================================================
    
    # User indexes
    op.create_index('IX_User_Email', 'User', ['Email'])
    op.create_index('IX_User_Status', 'User', ['Status'])
    op.create_index('IX_User_OnboardingComplete', 'User', ['OnboardingComplete'])
    
    # UserCompany indexes
    op.create_index('IX_UserCompany_UserID', 'UserCompany', ['UserID'])
    op.create_index('IX_UserCompany_CompanyID', 'UserCompany', ['CompanyID'])
    op.create_index('IX_UserCompany_Default', 'UserCompany', ['UserID', 'IsDefaultCompany'])
    
    # Invitation indexes
    op.create_index('IX_Invitation_CompanyID', 'Invitation', ['CompanyID'])
    op.create_index('IX_Invitation_Email', 'Invitation', ['InvitedEmail'])
    op.create_index('IX_Invitation_Status', 'Invitation', ['Status'])
    op.create_index('IX_Invitation_ExpiresAt', 'Invitation', ['ExpiresAt'])
    
    # =====================================================================
    # SEED DATA: Lookup Tables
    # =====================================================================
    
    # UserStatus seed data
    op.execute("""
        INSERT INTO [UserStatus] (StatusCode, DisplayName, Description, AllowLogin, IsSystemStatus, SortOrder)
        VALUES
            ('active', 'Active', 'User account is active and can log in normally', 1, 1, 1),
            ('unverified', 'Unverified Email', 'User signed up but has not verified email address yet', 0, 1, 2),
            ('suspended', 'Suspended', 'User account suspended by admin (temporary - billing issue, policy violation)', 0, 1, 3),
            ('locked', 'Locked (Brute Force)', 'Account temporarily locked due to failed login attempts (auto-unlocks after 15 min)', 0, 1, 4),
            ('deleted', 'Deleted', 'User account soft-deleted (retain data for audit trail)', 0, 1, 5)
    """)
    
    # InvitationStatus seed data
    op.execute("""
        INSERT INTO [InvitationStatus] (StatusCode, DisplayName, Description, CanResend, CanCancel, IsFinalState, IsSystemStatus, SortOrder)
        VALUES
            ('pending', 'Pending', 'Invitation sent but not yet accepted', 1, 1, 0, 1, 1),
            ('accepted', 'Accepted', 'Invitation accepted - user joined company', 0, 0, 1, 1, 2),
            ('expired', 'Expired', 'Invitation expired without acceptance', 1, 0, 1, 1, 3),
            ('cancelled', 'Cancelled', 'Invitation cancelled by admin', 0, 0, 1, 1, 4),
            ('declined', 'Declined', 'Invitation declined by invitee', 0, 0, 1, 1, 5)
    """)


def downgrade():
    """Drop User domain tables"""
    
    # Drop indexes
    op.drop_index('IX_Invitation_ExpiresAt', table_name='Invitation')
    op.drop_index('IX_Invitation_Status', table_name='Invitation')
    op.drop_index('IX_Invitation_Email', table_name='Invitation')
    op.drop_index('IX_Invitation_CompanyID', table_name='Invitation')
    op.drop_index('IX_UserCompany_Default', table_name='UserCompany')
    op.drop_index('IX_UserCompany_CompanyID', table_name='UserCompany')
    op.drop_index('IX_UserCompany_UserID', table_name='UserCompany')
    op.drop_index('IX_User_OnboardingComplete', table_name='User')
    op.drop_index('IX_User_Status', table_name='User')
    op.drop_index('IX_User_Email', table_name='User')
    
    # Drop foreign key constraints
    op.drop_constraint('FK_Invitation_Status', 'Invitation', type_='foreignkey')
    op.drop_constraint('FK_Invitation_CancelledBy', 'Invitation', type_='foreignkey')
    op.drop_constraint('FK_Invitation_AcceptedBy', 'Invitation', type_='foreignkey')
    op.drop_constraint('FK_Invitation_InvitedBy', 'Invitation', type_='foreignkey')
    op.drop_constraint('FK_UserCompany_InvitedBy', 'UserCompany', type_='foreignkey')
    op.drop_constraint('FK_UserCompany_User', 'UserCompany', type_='foreignkey')
    op.drop_constraint('FK_User_Status', 'User', type_='foreignkey')
    
    # Drop tables
    op.drop_table('Invitation')
    op.drop_table('UserCompany')
    op.drop_table('User')
    op.drop_table('InvitationStatus')
    op.drop_table('UserStatus')
