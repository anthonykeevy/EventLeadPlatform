"""
Integration Tests for Story 1.6: Team Invitation System

Tests the complete team invitation flow including:
- Sending invitations with role-based auth
- Resending invitations
- Cancelling invitations
- Listing invitations
- Email delivery
- Audit logging
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from main import app
from common.database import Base, get_db
from models.user import User
from models.company import Company
from models.user_company import UserCompany
from models.user_invitation import UserInvitation
from models.ref.user_status import UserStatus
from models.ref.country import Country
from models.ref.user_company_role import UserCompanyRole
from models.ref.user_company_status import UserCompanyStatus
from models.ref.user_invitation_status import UserInvitationStatus
from models.ref.joined_via import JoinedVia
from models.audit.activity_log import ActivityLog
from modules.auth.jwt_service import create_access_token
from common.security import hash_password


# Test database setup
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """Override database dependency for testing"""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(scope="function")
def db_session():
    """Create test database and session for each test"""
    Base.metadata.create_all(bind=test_engine)
    db = TestSessionLocal()
    
    # Seed reference data
    seed_reference_data(db)
    
    yield db
    
    db.close()
    Base.metadata.drop_all(bind=test_engine)


def seed_reference_data(db):
    """Seed minimal reference data for testing"""
    # User status
    active_status = UserStatus(
        UserStatusID=1,
        StatusCode="active",
        StatusName="Active",
        Description="Active user"
    )
    db.add(active_status)
    
    # Country
    australia = Country(
        CountryID=1,
        CountryCode="AU",
        CountryName="Australia",
        ISO2Code="AU",
        ISO3Code="AUS"
    )
    db.add(australia)
    
    # UserCompanyRole
    admin_role = UserCompanyRole(
        UserCompanyRoleID=1,
        RoleCode="company_admin",
        RoleName="Company Administrator",
        Description="Full admin access",
        RoleLevel=100
    )
    user_role = UserCompanyRole(
        UserCompanyRoleID=2,
        RoleCode="company_user",
        RoleName="Team Member",
        Description="Regular team member",
        RoleLevel=10
    )
    db.add_all([admin_role, user_role])
    
    # UserCompanyStatus
    active_company_status = UserCompanyStatus(
        UserCompanyStatusID=1,
        StatusCode="active",
        StatusName="Active",
        Description="Active membership"
    )
    db.add(active_company_status)
    
    # JoinedVia
    signup_via = JoinedVia(
        JoinedViaID=1,
        MethodCode="signup",
        MethodName="Sign Up",
        Description="Joined via signup"
    )
    db.add(signup_via)
    
    # UserInvitationStatus
    pending_status = UserInvitationStatus(
        UserInvitationStatusID=1,
        StatusCode="pending",
        StatusName="Pending",
        Description="Invitation sent, awaiting response",
        CanResend=True,
        CanCancel=True,
        IsFinalState=False
    )
    accepted_status = UserInvitationStatus(
        UserInvitationStatusID=2,
        StatusCode="accepted",
        StatusName="Accepted",
        Description="Invitation accepted",
        CanResend=False,
        CanCancel=False,
        IsFinalState=True
    )
    cancelled_status = UserInvitationStatus(
        UserInvitationStatusID=3,
        StatusCode="cancelled",
        StatusName="Cancelled",
        Description="Invitation cancelled",
        CanResend=False,
        CanCancel=False,
        IsFinalState=True
    )
    db.add_all([pending_status, accepted_status, cancelled_status])
    
    db.commit()


def create_test_company_admin(db):
    """Helper to create a company admin user"""
    # Create user
    user = User(
        Email="admin@example.com",
        PasswordHash=hash_password("TestPassword123!"),
        FirstName="Admin",
        LastName="User",
        StatusID=1,
        IsEmailVerified=True,
        EmailVerifiedAt=datetime.utcnow(),
        TimezoneIdentifier="Australia/Sydney"
    )
    db.add(user)
    db.flush()
    
    # Create company
    company = Company(
        CompanyName="Test Company",
        CountryID=1,
        IsActive=True,
        CreatedBy=user.UserID
    )
    db.add(company)
    db.flush()
    
    # Create UserCompany relationship
    user_company = UserCompany(
        UserID=user.UserID,
        CompanyID=company.CompanyID,
        UserCompanyRoleID=1,  # company_admin
        StatusID=1,  # active
        IsPrimaryCompany=True,
        JoinedViaID=1,
        CreatedBy=user.UserID
    )
    db.add(user_company)
    db.commit()
    db.refresh(user)
    db.refresh(company)
    
    return user, company


# ============================================================================
# Test AC-1.6.1: Protected endpoint requires company_admin role
# ============================================================================

def test_send_invitation_requires_auth(db_session):
    """Test that sending invitation requires authentication"""
    response = client.post(
        "/api/companies/1/invite",
        json={
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "role": "company_user"
        }
    )
    
    assert response.status_code == 401


def test_send_invitation_requires_company_admin(db_session):
    """Test that only company_admin can send invitations"""
    # Create regular user (not admin)
    user = User(
        Email="user@example.com",
        PasswordHash=hash_password("TestPassword123!"),
        FirstName="Regular",
        LastName="User",
        StatusID=1,
        IsEmailVerified=True,
        TimezoneIdentifier="Australia/Sydney"
    )
    db_session.add(user)
    db_session.commit()
    
    # Generate token without role or with company_user role
    token = create_access_token(user.UserID, user.Email, role="company_user", company_id=1)
    
    response = client.post(
        "/api/companies/1/invite",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "role": "company_user"
        }
    )
    
    assert response.status_code == 403


# ============================================================================
# Test AC-1.6.2, AC-1.6.3, AC-1.6.4: Send invitation with token and email
# ============================================================================

def test_send_invitation_success(db_session):
    """Test successful invitation sending (AC-1.6.2, AC-1.6.3, AC-1.6.4)"""
    admin, company = create_test_company_admin(db_session)
    token = create_access_token(admin.UserID, admin.Email, role="company_admin", company_id=company.CompanyID)
    
    response = client.post(
        f"/api/companies/{company.CompanyID}/invite",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": "newmember@example.com",
            "first_name": "New",
            "last_name": "Member",
            "role": "company_user"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["invitation_id"] > 0
    assert "expires_at" in data
    
    # Verify invitation created in database
    invitation = db_session.execute(
        select(UserInvitation).where(UserInvitation.Email == "newmember@example.com")
    ).scalar_one()
    
    assert invitation.FirstName == "New"
    assert invitation.LastName == "Member"
    assert invitation.CompanyID == company.CompanyID
    assert invitation.InvitedBy == admin.UserID
    assert invitation.InvitationToken is not None
    assert len(invitation.InvitationToken) > 40  # Secure token
    assert invitation.ExpiresAt > datetime.utcnow()
    assert invitation.ExpiresAt < datetime.utcnow() + timedelta(days=8)


# ============================================================================
# Test AC-1.6.5: Cannot invite existing member
# ============================================================================

def test_cannot_invite_existing_member(db_session):
    """Test that existing company member cannot be invited (AC-1.6.5)"""
    admin, company = create_test_company_admin(db_session)
    token = create_access_token(admin.UserID, admin.Email, role="company_admin", company_id=company.CompanyID)
    
    # Try to invite the admin (who is already a member)
    response = client.post(
        f"/api/companies/{company.CompanyID}/invite",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": "admin@example.com",  # Admin's email
            "first_name": "Admin",
            "last_name": "User",
            "role": "company_user"
        }
    )
    
    assert response.status_code == 400
    assert "already belongs" in response.json()["detail"].lower()


# ============================================================================
# Test AC-1.6.6: Admin can specify role
# ============================================================================

def test_invitation_with_different_roles(db_session):
    """Test invitations can be sent with different roles (AC-1.6.6)"""
    admin, company = create_test_company_admin(db_session)
    token = create_access_token(admin.UserID, admin.Email, role="company_admin", company_id=company.CompanyID)
    
    # Send invitation with company_admin role
    response = client.post(
        f"/api/companies/{company.CompanyID}/invite",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": "admin2@example.com",
            "first_name": "Second",
            "last_name": "Admin",
            "role": "company_admin"
        }
    )
    
    assert response.status_code == 201
    
    # Verify role in database
    invitation = db_session.execute(
        select(UserInvitation)
        .join(UserCompanyRole)
        .where(UserInvitation.Email == "admin2@example.com")
    ).scalar_one()
    
    role = db_session.execute(
        select(UserCompanyRole).where(UserCompanyRole.UserCompanyRoleID == invitation.UserCompanyRoleID)
    ).scalar_one()
    
    assert role.RoleCode == "company_admin"


# ============================================================================
# Test AC-1.6.7: Resend invitation
# ============================================================================

def test_resend_invitation_success(db_session):
    """Test resending invitation (AC-1.6.7)"""
    admin, company = create_test_company_admin(db_session)
    token = create_access_token(admin.UserID, admin.Email, role="company_admin", company_id=company.CompanyID)
    
    # Send initial invitation
    response = client.post(
        f"/api/companies/{company.CompanyID}/invite",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": "resend@example.com",
            "first_name": "Resend",
            "last_name": "Test",
            "role": "company_user"
        }
    )
    
    invitation_id = response.json()["invitation_id"]
    
    # Resend invitation
    response = client.post(
        f"/api/companies/{company.CompanyID}/invitations/{invitation_id}/resend",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["resend_count"] == 1
    assert "new_expires_at" in data
    
    # Verify resend count in database
    invitation = db_session.execute(
        select(UserInvitation).where(UserInvitation.UserInvitationID == invitation_id)
    ).scalar_one()
    
    assert invitation.ResendCount == 1
    assert invitation.LastResentAt is not None


# ============================================================================
# Test AC-1.6.8: Cancel invitation
# ============================================================================

def test_cancel_invitation_success(db_session):
    """Test cancelling invitation (AC-1.6.8)"""
    admin, company = create_test_company_admin(db_session)
    token = create_access_token(admin.UserID, admin.Email, role="company_admin", company_id=company.CompanyID)
    
    # Send invitation
    response = client.post(
        f"/api/companies/{company.CompanyID}/invite",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": "cancel@example.com",
            "first_name": "Cancel",
            "last_name": "Test",
            "role": "company_user"
        }
    )
    
    invitation_id = response.json()["invitation_id"]
    
    # Cancel invitation
    response = client.delete(
        f"/api/companies/{company.CompanyID}/invitations/{invitation_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    
    # Verify status in database
    invitation = db_session.execute(
        select(UserInvitation)
        .join(UserInvitationStatus)
        .where(UserInvitation.UserInvitationID == invitation_id)
    ).scalar_one()
    
    status = db_session.execute(
        select(UserInvitationStatus).where(
            UserInvitationStatus.UserInvitationStatusID == invitation.StatusID
        )
    ).scalar_one()
    
    assert status.StatusCode == "cancelled"
    assert invitation.CancelledAt is not None
    assert invitation.CancelledBy == admin.UserID


# ============================================================================
# Test AC-1.6.9: List invitations with filtering
# ============================================================================

def test_list_invitations(db_session):
    """Test listing company invitations (AC-1.6.9)"""
    admin, company = create_test_company_admin(db_session)
    token = create_access_token(admin.UserID, admin.Email, role="company_admin", company_id=company.CompanyID)
    
    # Send multiple invitations
    for i in range(3):
        client.post(
            f"/api/companies/{company.CompanyID}/invite",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "email": f"member{i}@example.com",
                "first_name": f"Member{i}",
                "last_name": "Test",
                "role": "company_user"
            }
        )
    
    # List all invitations
    response = client.get(
        f"/api/companies/{company.CompanyID}/invitations",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["invitations"]) == 3
    assert data["page"] == 1
    
    # Test filtering by status
    response = client.get(
        f"/api/companies/{company.CompanyID}/invitations?status_filter=pending",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert all(inv["status"] == "pending" for inv in data["invitations"])


# ============================================================================
# Test AC-1.6.10: Audit logging
# ============================================================================

def test_invitation_audit_logging(db_session):
    """Test that invitation events are logged to audit table (AC-1.6.10)"""
    admin, company = create_test_company_admin(db_session)
    token = create_access_token(admin.UserID, admin.Email, role="company_admin", company_id=company.CompanyID)
    
    # Send invitation
    response = client.post(
        f"/api/companies/{company.CompanyID}/invite",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": "audit@example.com",
            "first_name": "Audit",
            "last_name": "Test",
            "role": "company_user"
        }
    )
    
    invitation_id = response.json()["invitation_id"]
    
    # Check audit log for INVITATION_SENT
    audit_log = db_session.execute(
        select(ActivityLog).where(
            ActivityLog.Action == "INVITATION_SENT",
            ActivityLog.EntityID == invitation_id
        )
    ).scalar_one_or_none()
    
    assert audit_log is not None
    assert audit_log.UserID == admin.UserID
    assert audit_log.CompanyID == company.CompanyID
    assert audit_log.EntityType == "UserInvitation"
    assert "audit@example.com" in audit_log.NewValue
    
    # Resend invitation
    client.post(
        f"/api/companies/{company.CompanyID}/invitations/{invitation_id}/resend",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Check audit log for INVITATION_RESENT
    audit_log = db_session.execute(
        select(ActivityLog).where(
            ActivityLog.Action == "INVITATION_RESENT",
            ActivityLog.EntityID == invitation_id
        )
    ).scalar_one_or_none()
    
    assert audit_log is not None
    
    # Cancel invitation
    client.delete(
        f"/api/companies/{company.CompanyID}/invitations/{invitation_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Check audit log for INVITATION_CANCELLED
    audit_log = db_session.execute(
        select(ActivityLog).where(
            ActivityLog.Action == "INVITATION_CANCELLED",
            ActivityLog.EntityID == invitation_id
        )
    ).scalar_one_or_none()
    
    assert audit_log is not None
    assert "cancelled" in audit_log.NewValue.lower()


# ============================================================================
# Test Security & Edge Cases
# ============================================================================

def test_admin_cannot_invite_to_different_company(db_session):
    """Test that admin cannot invite users to a different company"""
    admin, company = create_test_company_admin(db_session)
    token = create_access_token(admin.UserID, admin.Email, role="company_admin", company_id=company.CompanyID)
    
    # Try to invite to a different company
    response = client.post(
        "/api/companies/999/invite",  # Different company ID
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "role": "company_user"
        }
    )
    
    assert response.status_code == 403


def test_cannot_invite_with_invalid_role(db_session):
    """Test that invalid role is rejected"""
    admin, company = create_test_company_admin(db_session)
    token = create_access_token(admin.UserID, admin.Email, role="company_admin", company_id=company.CompanyID)
    
    response = client.post(
        f"/api/companies/{company.CompanyID}/invite",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "role": "super_admin"  # Invalid role
        }
    )
    
    assert response.status_code == 400


def test_cannot_resend_cancelled_invitation(db_session):
    """Test that cancelled invitations cannot be resent"""
    admin, company = create_test_company_admin(db_session)
    token = create_access_token(admin.UserID, admin.Email, role="company_admin", company_id=company.CompanyID)
    
    # Send and cancel invitation
    response = client.post(
        f"/api/companies/{company.CompanyID}/invite",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "role": "company_user"
        }
    )
    
    invitation_id = response.json()["invitation_id"]
    
    client.delete(
        f"/api/companies/{company.CompanyID}/invitations/{invitation_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Try to resend
    response = client.post(
        f"/api/companies/{company.CompanyID}/invitations/{invitation_id}/resend",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 400

