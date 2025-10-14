"""Complete foreign key references and finalize schema

Revision ID: 007_complete_foreign_key_references
Revises: 006_seed_foundation_data
Create Date: 2025-10-13 12:06:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '007_complete_foreign_key_references'
down_revision = '006_seed_foundation_data'
branch_labels = None
depends_on = None


def upgrade():
    """Complete foreign key references and finalize schema"""
    
    # =====================================================================
    # ADD MISSING FOREIGN KEY CONSTRAINTS
    # =====================================================================
    
    # Country foreign keys (to Language)
    op.create_foreign_key('FK_Country_DefaultLanguage', 'Country', 'Language', ['DefaultLanguageCode'], ['LanguageCode'])
    
    # User foreign keys (to Language for language preference)
    op.create_foreign_key('FK_User_LanguagePreference', 'User', 'Language', ['LanguagePreference'], ['LanguageCode'])
    
    # CompanyBillingDetails foreign keys (to Country)
    op.create_foreign_key('FK_CompanyBillingDetails_BillingCountry', 'CompanyBillingDetails', 'Country', ['BillingCountry'], ['CountryCode'])
    
    # =====================================================================
    # ADD MISSING CHECK CONSTRAINTS
    # =====================================================================
    
    # User constraints
    op.create_check_constraint(
        'CK_User_AccessTokenVersion',
        'User',
        "AccessTokenVersion > 0"
    )
    
    op.create_check_constraint(
        'CK_User_RefreshTokenVersion',
        'User',
        "RefreshTokenVersion > 0"
    )
    
    op.create_check_constraint(
        'CK_User_FailedLoginCount',
        'User',
        "FailedLoginCount >= 0"
    )
    
    # UserCompany constraints
    op.create_check_constraint(
        'CK_UserCompany_Role',
        'UserCompany',
        "Role IN ('company_admin', 'company_user', 'company_viewer')"
    )
    
    op.create_check_constraint(
        'CK_UserCompany_Status',
        'UserCompany',
        "Status IN ('active', 'suspended', 'pending', 'inactive')"
    )
    
    op.create_check_constraint(
        'CK_UserCompany_JoinedVia',
        'UserCompany',
        "JoinedVia IN ('signup', 'invitation', 'admin_add', 'import')"
    )
    
    # Company constraints
    op.create_check_constraint(
        'CK_Company_CompanyType',
        'Company',
        "CompanyType IN ('sole_trader', 'partnership', 'company', 'trust', 'association', 'government')"
    )
    
    op.create_check_constraint(
        'CK_Company_CompanySize',
        'Company',
        "CompanySize IN ('micro', 'small', 'medium', 'large', 'enterprise')"
    )
    
    op.create_check_constraint(
        'CK_Company_FoundedYear',
        'Company',
        "FoundedYear IS NULL OR (FoundedYear >= 1800 AND FoundedYear <= YEAR(GETUTCDATE()))"
    )
    
    # CompanyCustomerDetails constraints
    op.create_check_constraint(
        'CK_CompanyCustomerDetails_SubscriptionPlan',
        'CompanyCustomerDetails',
        "SubscriptionPlan IN ('free', 'basic', 'professional', 'enterprise', 'custom')"
    )
    
    op.create_check_constraint(
        'CK_CompanyCustomerDetails_SubscriptionStatus',
        'CompanyCustomerDetails',
        "SubscriptionStatus IN ('active', 'trial', 'cancelled', 'suspended', 'expired')"
    )
    
    op.create_check_constraint(
        'CK_CompanyCustomerDetails_TestThreshold',
        'CompanyCustomerDetails',
        "TestThreshold > 0"
    )
    
    op.create_check_constraint(
        'CK_CompanyCustomerDetails_MaxUsers',
        'CompanyCustomerDetails',
        "MaxUsers IS NULL OR MaxUsers > 0"
    )
    
    op.create_check_constraint(
        'CK_CompanyCustomerDetails_MaxEvents',
        'CompanyCustomerDetails',
        "MaxEvents IS NULL OR MaxEvents > 0"
    )
    
    op.create_check_constraint(
        'CK_CompanyCustomerDetails_MaxSubmissions',
        'CompanyCustomerDetails',
        "MaxSubmissions IS NULL OR MaxSubmissions > 0"
    )
    
    op.create_check_constraint(
        'CK_CompanyCustomerDetails_MaxStorageMB',
        'CompanyCustomerDetails',
        "MaxStorageMB IS NULL OR MaxStorageMB > 0"
    )
    
    # CompanyOrganizerDetails constraints
    op.create_check_constraint(
        'CK_CompanyOrganizerDetails_OrganizerSource',
        'CompanyOrganizerDetails',
        "OrganizerSource IN ('direct', 'referral', 'google', 'facebook', 'linkedin', 'eventbrite', 'other')"
    )
    
    op.create_check_constraint(
        'CK_CompanyOrganizerDetails_VerificationMethod',
        'CompanyOrganizerDetails',
        "VerificationMethod IN ('email', 'phone', 'document', 'manual', 'api')"
    )
    
    op.create_check_constraint(
        'CK_CompanyOrganizerDetails_YearsInBusiness',
        'CompanyOrganizerDetails',
        "YearsInBusiness IS NULL OR YearsInBusiness >= 0"
    )
    
    op.create_check_constraint(
        'CK_CompanyOrganizerDetails_TotalEventsHosted',
        'CompanyOrganizerDetails',
        "TotalEventsHosted >= 0"
    )
    
    op.create_check_constraint(
        'CK_CompanyOrganizerDetails_AverageEventSize',
        'CompanyOrganizerDetails',
        "AverageEventSize IS NULL OR AverageEventSize > 0"
    )
    
    op.create_check_constraint(
        'CK_CompanyOrganizerDetails_LargestEventSize',
        'CompanyOrganizerDetails',
        "LargestEventSize IS NULL OR LargestEventSize > 0"
    )
    
    op.create_check_constraint(
        'CK_CompanyOrganizerDetails_Rating',
        'CompanyOrganizerDetails',
        "Rating IS NULL OR (Rating >= 0.0 AND Rating <= 5.0)"
    )
    
    op.create_check_constraint(
        'CK_CompanyOrganizerDetails_RatingCount',
        'CompanyOrganizerDetails',
        "RatingCount >= 0"
    )
    
    # =====================================================================
    # ADD ADDITIONAL INDEXES FOR PERFORMANCE
    # =====================================================================
    
    # User indexes
    op.create_index('IX_User_LastLoginDate', 'User', ['LastLoginDate'])
    op.create_index('IX_User_FailedLoginCount', 'User', ['FailedLoginCount'])
    op.create_index('IX_User_LockedUntil', 'User', ['LockedUntil'])
    
    # Company indexes
    op.create_index('IX_Company_CompanyType', 'Company', ['CompanyType'])
    op.create_index('IX_Company_CompanySize', 'Company', ['CompanySize'])
    op.create_index('IX_Company_Industry', 'Company', ['Industry'])
    
    # CompanyBillingDetails indexes
    op.create_index('IX_CompanyBillingDetails_Currency', 'CompanyBillingDetails', ['Currency'])
    op.create_index('IX_CompanyBillingDetails_BillingCountry', 'CompanyBillingDetails', ['BillingCountry'])
    
    # CompanyOrganizerDetails indexes
    op.create_index('IX_CompanyOrganizerDetails_OrganizerSource', 'CompanyOrganizerDetails', ['OrganizerSource'])
    op.create_index('IX_CompanyOrganizerDetails_TotalEventsHosted', 'CompanyOrganizerDetails', ['TotalEventsHosted'])
    
    # Invitation indexes
    op.create_index('IX_Invitation_InvitedByUserID', 'Invitation', ['InvitedByUserID'])
    op.create_index('IX_Invitation_AcceptedByUserID', 'Invitation', ['AcceptedByUserID'])
    
    # =====================================================================
    # ADD ROW-LEVEL SECURITY (RLS) SUPPORT
    # =====================================================================
    
    # Enable RLS on tenant tables (multi-tenant isolation)
    op.execute("ALTER TABLE [UserCompany] ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE [Company] ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE [CompanyCustomerDetails] ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE [CompanyBillingDetails] ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE [CompanyOrganizerDetails] ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE [Invitation] ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE [CompanyRelationship] ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE [CompanySwitchRequest] ENABLE ROW LEVEL SECURITY")
    
    # Create RLS policies (basic - will be enhanced in application layer)
    op.execute("""
        CREATE POLICY [CompanyIsolationPolicy] ON [Company]
        FOR ALL TO [application_role]
        USING (CompanyID IN (
            SELECT CompanyID FROM UserCompany 
            WHERE UserID = CAST(SESSION_CONTEXT(N'user_id') AS BIGINT)
        ))
    """)
    
    op.execute("""
        CREATE POLICY [UserCompanyIsolationPolicy] ON [UserCompany]
        FOR ALL TO [application_role]
        USING (UserID = CAST(SESSION_CONTEXT(N'user_id') AS BIGINT))
    """)
    
    # =====================================================================
    # CREATE HELPFUL VIEWS
    # =====================================================================
    
    # Active users with company information
    op.execute("""
        CREATE VIEW [vw_ActiveUsersWithCompanies] AS
        SELECT 
            u.UserID,
            u.Email,
            u.FirstName,
            u.LastName,
            u.Status,
            u.OnboardingComplete,
            u.LastLoginDate,
            uc.CompanyID,
            c.DisplayName AS CompanyName,
            uc.Role AS CompanyRole,
            uc.JoinedDate,
            uc.IsDefaultCompany
        FROM [User] u
        INNER JOIN [UserCompany] uc ON u.UserID = uc.UserID
        INNER JOIN [Company] c ON uc.CompanyID = c.CompanyID
        WHERE u.IsDeleted = 0 
          AND uc.IsDeleted = 0 
          AND c.IsDeleted = 0
          AND u.Status = 'active'
    """)
    
    # Company details with all contexts
    op.execute("""
        CREATE VIEW [vw_CompanyFullDetails] AS
        SELECT 
            c.CompanyID,
            c.DisplayName,
            c.LegalEntityName,
            c.Industry,
            c.IsActive,
            -- Customer details
            cd.SubscriptionPlan,
            cd.SubscriptionStatus,
            cd.MaxUsers,
            cd.MaxEvents,
            cd.TrialEndDate,
            cd.IsTrialActive,
            -- Billing details
            bd.ABN,
            bd.GSTRegistered,
            bd.BillingEmail,
            bd.Currency,
            -- Organizer details
            od.IsPublic,
            od.IsVerified,
            od.TotalEventsHosted,
            od.Rating,
            od.RatingCount
        FROM [Company] c
        LEFT JOIN [CompanyCustomerDetails] cd ON c.CompanyID = cd.CompanyID
        LEFT JOIN [CompanyBillingDetails] bd ON c.CompanyID = bd.CompanyID
        LEFT JOIN [CompanyOrganizerDetails] od ON c.CompanyID = od.CompanyID
        WHERE c.IsDeleted = 0
    """)
    
    # Pending invitations with company context
    op.execute("""
        CREATE VIEW [vw_PendingInvitations] AS
        SELECT 
            i.InvitationID,
            i.InvitedEmail,
            i.InvitedFirstName,
            i.InvitedLastName,
            i.AssignedRole,
            i.ExpiresAt,
            i.CreatedDate,
            c.DisplayName AS CompanyName,
            c.Industry AS CompanyIndustry,
            u.FirstName + ' ' + u.LastName AS InvitedByUser
        FROM [Invitation] i
        INNER JOIN [Company] c ON i.CompanyID = c.CompanyID
        INNER JOIN [User] u ON i.InvitedByUserID = u.UserID
        WHERE i.Status = 'pending'
          AND i.ExpiresAt > GETUTCDATE()
          AND i.IsDeleted = 0
          AND c.IsDeleted = 0
          AND u.IsDeleted = 0
    """)


def downgrade():
    """Remove foreign key references and views"""
    
    # Drop views
    op.execute("DROP VIEW [vw_PendingInvitations]")
    op.execute("DROP VIEW [vw_CompanyFullDetails]")
    op.execute("DROP VIEW [vw_ActiveUsersWithCompanies]")
    
    # Drop RLS policies and disable RLS
    op.execute("DROP POLICY [UserCompanyIsolationPolicy] ON [UserCompany]")
    op.execute("DROP POLICY [CompanyIsolationPolicy] ON [Company]")
    op.execute("ALTER TABLE [CompanySwitchRequest] DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE [CompanyRelationship] DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE [Invitation] DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE [CompanyOrganizerDetails] DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE [CompanyBillingDetails] DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE [CompanyCustomerDetails] DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE [Company] DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE [UserCompany] DISABLE ROW LEVEL SECURITY")
    
    # Drop additional indexes
    op.drop_index('IX_Invitation_AcceptedByUserID', table_name='Invitation')
    op.drop_index('IX_Invitation_InvitedByUserID', table_name='Invitation')
    op.drop_index('IX_CompanyOrganizerDetails_TotalEventsHosted', table_name='CompanyOrganizerDetails')
    op.drop_index('IX_CompanyOrganizerDetails_OrganizerSource', table_name='CompanyOrganizerDetails')
    op.drop_index('IX_CompanyBillingDetails_BillingCountry', table_name='CompanyBillingDetails')
    op.drop_index('IX_CompanyBillingDetails_Currency', table_name='CompanyBillingDetails')
    op.drop_index('IX_Company_Industry', table_name='Company')
    op.drop_index('IX_Company_CompanySize', table_name='Company')
    op.drop_index('IX_Company_CompanyType', table_name='Company')
    op.drop_index('IX_User_LockedUntil', table_name='User')
    op.drop_index('IX_User_FailedLoginCount', table_name='User')
    op.drop_index('IX_User_LastLoginDate', table_name='User')
    
    # Drop check constraints
    op.drop_constraint('CK_CompanyOrganizerDetails_RatingCount', 'CompanyOrganizerDetails', type_='check')
    op.drop_constraint('CK_CompanyOrganizerDetails_Rating', 'CompanyOrganizerDetails', type_='check')
    op.drop_constraint('CK_CompanyOrganizerDetails_LargestEventSize', 'CompanyOrganizerDetails', type_='check')
    op.drop_constraint('CK_CompanyOrganizerDetails_AverageEventSize', 'CompanyOrganizerDetails', type_='check')
    op.drop_constraint('CK_CompanyOrganizerDetails_TotalEventsHosted', 'CompanyOrganizerDetails', type_='check')
    op.drop_constraint('CK_CompanyOrganizerDetails_YearsInBusiness', 'CompanyOrganizerDetails', type_='check')
    op.drop_constraint('CK_CompanyOrganizerDetails_VerificationMethod', 'CompanyOrganizerDetails', type_='check')
    op.drop_constraint('CK_CompanyOrganizerDetails_OrganizerSource', 'CompanyOrganizerDetails', type_='check')
    op.drop_constraint('CK_CompanyCustomerDetails_MaxStorageMB', 'CompanyCustomerDetails', type_='check')
    op.drop_constraint('CK_CompanyCustomerDetails_MaxSubmissions', 'CompanyCustomerDetails', type_='check')
    op.drop_constraint('CK_CompanyCustomerDetails_MaxEvents', 'CompanyCustomerDetails', type_='check')
    op.drop_constraint('CK_CompanyCustomerDetails_MaxUsers', 'CompanyCustomerDetails', type_='check')
    op.drop_constraint('CK_CompanyCustomerDetails_TestThreshold', 'CompanyCustomerDetails', type_='check')
    op.drop_constraint('CK_CompanyCustomerDetails_SubscriptionStatus', 'CompanyCustomerDetails', type_='check')
    op.drop_constraint('CK_CompanyCustomerDetails_SubscriptionPlan', 'CompanyCustomerDetails', type_='check')
    op.drop_constraint('CK_Company_FoundedYear', 'Company', type_='check')
    op.drop_constraint('CK_Company_CompanySize', 'Company', type_='check')
    op.drop_constraint('CK_Company_CompanyType', 'Company', type_='check')
    op.drop_constraint('CK_UserCompany_JoinedVia', 'UserCompany', type_='check')
    op.drop_constraint('CK_UserCompany_Status', 'UserCompany', type_='check')
    op.drop_constraint('CK_UserCompany_Role', 'UserCompany', type_='check')
    op.drop_constraint('CK_User_FailedLoginCount', 'User', type_='check')
    op.drop_constraint('CK_User_RefreshTokenVersion', 'User', type_='check')
    op.drop_constraint('CK_User_AccessTokenVersion', 'User', type_='check')
    
    # Drop foreign key constraints
    op.drop_constraint('FK_CompanyBillingDetails_BillingCountry', 'CompanyBillingDetails', type_='foreignkey')
    op.drop_constraint('FK_User_LanguagePreference', 'User', type_='foreignkey')
    op.drop_constraint('FK_Country_DefaultLanguage', 'Country', type_='foreignkey')
