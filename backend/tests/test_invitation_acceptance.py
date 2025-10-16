"""
Integration Tests for Story 1.7: Invitation Acceptance & Multi-Company Support
Tests all acceptance criteria for invitation viewing, acceptance, and company switching
"""
import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from main import app
from common.database import get_db
from models.user import User
from models.company import Company
from models.user_company import UserCompany
from models.user_invitation import UserInvitation
from models.ref.user_status import UserStatus
from models.ref.user_company_status import UserCompanyStatus
from models.ref.user_company_role import UserCompanyRole
from models.ref.user_invitation_status import UserInvitationStatus
from models.ref.joined_via import JoinedVia
from common.security import hash_password
from modules.auth.jwt_service import create_access_token
import secrets


client = TestClient(app)


@pytest.fixture
def db():
    """Get test database session"""
    db_session = next(get_db())
    try:
        yield db_session
    finally:
        db_session.close()


@pytest.fixture
def test_company(db: Session):
    """Create test company"""
    company = Company(
        CompanyName="Test Company Pty Ltd",
        CompanyTradingName="Test Company",
        ABN="53004085616",  # Valid ABN
        IsActive=True,
        CreatedDate=datetime.utcnow(),
        UpdatedDate=datetime.utcnow(),
        IsDeleted=False
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


@pytest.fixture
def test_admin_user(db: Session, test_company):
    """Create test admin user with company relationship"""
    # Get active status
    active_status = db.query(UserStatus).filter(UserStatus.StatusName == "Active").first()
    
    # Create user
    user = User(
        Email="admin@testcompany.com",
        PasswordHash=hash_password("TestP@ssw0rd123"),
        FirstName="Admin",
        LastName="User",
        EmailVerified=True,
        IsActive=True,
        UserStatusID=active_status.UserStatusID if active_status else None,
        CreatedDate=datetime.utcnow(),
        UpdatedDate=datetime.utcnow(),
        IsDeleted=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Get admin role and active status
    admin_role = db.query(UserCompanyRole).filter(
        UserCompanyRole.RoleCode == "company_admin"
    ).first()
    uc_active_status = db.query(UserCompanyStatus).filter(
        UserCompanyStatus.StatusCode == "active"
    ).first()
    joined_via = db.query(JoinedVia).filter(JoinedVia.MethodCode == "signup").first()
    
    # Create UserCompany relationship
    user_company = UserCompany(
        UserID=user.UserID,
        CompanyID=test_company.CompanyID,
        UserCompanyRoleID=admin_role.UserCompanyRoleID if admin_role else None,
        StatusID=uc_active_status.UserCompanyStatusID if uc_active_status else None,
        IsPrimaryCompany=True,
        JoinedDate=datetime.utcnow(),
        JoinedViaID=joined_via.JoinedViaID if joined_via else None,
        CreatedBy=user.UserID,
        CreatedDate=datetime.utcnow(),
        UpdatedBy=user.UserID,
        UpdatedDate=datetime.utcnow(),
        IsDeleted=False
    )
    db.add(user_company)
    db.commit()
    
    return user


@pytest.fixture
def test_invitation(db: Session, test_company, test_admin_user):
    """Create test invitation"""
    # Get pending status and team member role
    pending_status = db.query(UserInvitationStatus).filter(
        UserInvitationStatus.StatusCode == "pending"
    ).first()
    team_role = db.query(UserCompanyRole).filter(
        UserCompanyRole.RoleCode == "company_user"
    ).first()
    
    invitation_token = secrets.token_urlsafe(32)
    
    invitation = UserInvitation(
        CompanyID=test_company.CompanyID,
        Email="newuser@example.com",
        UserCompanyRoleID=team_role.UserCompanyRoleID if team_role else None,
        InvitedBy=test_admin_user.UserID,
        InvitedAt=datetime.utcnow(),
        ExpiresAt=datetime.utcnow() + timedelta(days=7),
        InvitationToken=invitation_token,
        StatusID=pending_status.UserInvitationStatusID if pending_status else None,
        CreatedDate=datetime.utcnow(),
        CreatedBy=test_admin_user.UserID,
        UpdatedDate=datetime.utcnow(),
        UpdatedBy=test_admin_user.UserID,
        IsDeleted=False
    )
    db.add(invitation)
    db.commit()
    db.refresh(invitation)
    return invitation


# ============================================================================
# AC-1.7.1, AC-1.7.2: View Invitation Details (Public Endpoint)
# ============================================================================

def test_view_invitation_details_success(test_invitation):
    """Test viewing valid invitation details"""
    response = client.get(f"/api/invitations/{test_invitation.InvitationToken}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["invitation_id"] == test_invitation.UserInvitationID
    assert data["company_name"] == "Test Company Pty Ltd"
    assert data["role_name"] == "Team Member"  # or whatever the role name is
    assert data["inviter_name"] == "Admin User"
    assert data["invited_email"] == "newuser@example.com"
    assert data["is_expired"] == False
    assert data["status"] == "pending"


def test_view_invitation_not_found():
    """Test viewing non-existent invitation"""
    response = client.get("/api/invitations/invalid_token_123")
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_view_invitation_expired(db: Session, test_invitation):
    """Test viewing expired invitation"""
    # Expire the invitation
    test_invitation.ExpiresAt = datetime.utcnow() - timedelta(days=1)
    db.commit()
    
    response = client.get(f"/api/invitations/{test_invitation.InvitationToken}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["is_expired"] == True


# ============================================================================
# AC-1.7.3, AC-1.7.4, AC-1.7.7, AC-1.7.8: Accept Invitation (Existing User)
# ============================================================================

def test_accept_invitation_existing_user_success(db: Session, test_invitation):
    """Test existing user accepting invitation"""
    # Create existing user (not yet part of company)
    active_status = db.query(UserStatus).filter(UserStatus.StatusName == "Active").first()
    existing_user = User(
        Email="newuser@example.com",  # Matches invitation email
        PasswordHash=hash_password("TestP@ssw0rd123"),
        FirstName="New",
        LastName="User",
        EmailVerified=True,
        IsActive=True,
        UserStatusID=active_status.UserStatusID if active_status else None,
        CreatedDate=datetime.utcnow(),
        UpdatedDate=datetime.utcnow(),
        IsDeleted=False
    )
    db.add(existing_user)
    db.commit()
    db.refresh(existing_user)
    
    # Create JWT for existing user
    access_token = create_access_token(
        user_id=existing_user.UserID,
        email=existing_user.Email,
        role=None,
        company_id=None
    )
    
    # Accept invitation
    response = client.post(
        f"/api/invitations/{test_invitation.InvitationToken}/accept",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["success"] == True
    assert "accepted successfully" in data["message"].lower()
    assert data["company_id"] == test_invitation.CompanyID
    assert data["role"] == "company_user"
    assert "access_token" in data
    assert "refresh_token" in data
    
    # Verify UserCompany relationship created (AC-1.7.4)
    user_company = db.query(UserCompany).filter(
        UserCompany.UserID == existing_user.UserID,
        UserCompany.CompanyID == test_invitation.CompanyID
    ).first()
    
    assert user_company is not None
    assert user_company.IsDeleted == False
    
    # Verify invitation marked as accepted (AC-1.7.7)
    db.refresh(test_invitation)
    inv_status = db.query(UserInvitationStatus).filter(
        UserInvitationStatus.UserInvitationStatusID == test_invitation.StatusID
    ).first()
    assert inv_status.StatusCode == "accepted"
    assert test_invitation.AcceptedAt is not None
    assert test_invitation.AcceptedBy == existing_user.UserID


def test_accept_invitation_email_mismatch(db: Session, test_invitation):
    """Test invitation acceptance fails if email doesn't match"""
    # Create user with different email
    active_status = db.query(UserStatus).filter(UserStatus.StatusName == "Active").first()
    user = User(
        Email="different@example.com",
        PasswordHash=hash_password("TestP@ssw0rd123"),
        FirstName="Different",
        LastName="User",
        EmailVerified=True,
        IsActive=True,
        UserStatusID=active_status.UserStatusID if active_status else None,
        CreatedDate=datetime.utcnow(),
        UpdatedDate=datetime.utcnow(),
        IsDeleted=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create JWT
    access_token = create_access_token(
        user_id=user.UserID,
        email=user.Email,
        role=None,
        company_id=None
    )
    
    # Try to accept invitation
    response = client.post(
        f"/api/invitations/{test_invitation.InvitationToken}/accept",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    assert response.status_code == 400
    assert "email" in response.json()["detail"].lower()


def test_accept_invitation_unauthenticated():
    """Test invitation acceptance requires authentication (AC-1.7.3)"""
    response = client.post("/api/invitations/some_token/accept")
    
    assert response.status_code == 401


def test_accept_invitation_expired(db: Session, test_invitation):
    """Test cannot accept expired invitation"""
    # Create user
    active_status = db.query(UserStatus).filter(UserStatus.StatusName == "Active").first()
    user = User(
        Email="newuser@example.com",
        PasswordHash=hash_password("TestP@ssw0rd123"),
        FirstName="New",
        LastName="User",
        EmailVerified=True,
        IsActive=True,
        UserStatusID=active_status.UserStatusID if active_status else None,
        CreatedDate=datetime.utcnow(),
        UpdatedDate=datetime.utcnow(),
        IsDeleted=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Expire invitation
    test_invitation.ExpiresAt = datetime.utcnow() - timedelta(days=1)
    db.commit()
    
    # Create JWT
    access_token = create_access_token(
        user_id=user.UserID,
        email=user.Email,
        role=None,
        company_id=None
    )
    
    # Try to accept invitation
    response = client.post(
        f"/api/invitations/{test_invitation.InvitationToken}/accept",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    assert response.status_code == 400
    assert "expired" in response.json()["detail"].lower()


# ============================================================================
# AC-1.7.5, AC-1.7.6: New User Signup with Invitation
# ============================================================================

def test_signup_with_invitation_success(test_invitation):
    """Test new user signup with invitation token (AC-1.7.5, AC-1.7.6)"""
    response = client.post(
        "/api/auth/signup",
        json={
            "email": "newuser@example.com",  # Matches invitation
            "password": "SecureP@ssw0rd123",
            "first_name": "New",
            "last_name": "User",
            "invitation_token": test_invitation.InvitationToken
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["success"] == True
    assert "access_token" in data["data"]
    assert "refresh_token" in data["data"]
    assert data["data"]["company_id"] == test_invitation.CompanyID
    assert data["data"]["role"] == "company_user"
    
    # Verify user created
    from common.database import get_db
    db = next(get_db())
    user = db.query(User).filter(User.Email == "newuser@example.com").first()
    
    assert user is not None
    assert user.EmailVerified == True  # Auto-verified for invited users
    assert user.IsActive == True
    assert user.OnboardingComplete == True  # Onboarding skipped
    
    # Verify UserCompany created (AC-1.7.6)
    user_company = db.query(UserCompany).filter(
        UserCompany.UserID == user.UserID,
        UserCompany.CompanyID == test_invitation.CompanyID
    ).first()
    
    assert user_company is not None
    assert user_company.IsPrimaryCompany == True
    
    db.close()


def test_signup_with_invitation_email_mismatch(test_invitation):
    """Test signup fails if email doesn't match invitation"""
    response = client.post(
        "/api/auth/signup",
        json={
            "email": "different@example.com",  # Doesn't match invitation
            "password": "SecureP@ssw0rd123",
            "first_name": "Different",
            "last_name": "User",
            "invitation_token": test_invitation.InvitationToken
        }
    )
    
    assert response.status_code == 400
    assert "email" in response.json()["detail"].lower()


def test_signup_with_invalid_invitation():
    """Test signup fails with invalid invitation token"""
    response = client.post(
        "/api/auth/signup",
        json={
            "email": "test@example.com",
            "password": "SecureP@ssw0rd123",
            "first_name": "Test",
            "last_name": "User",
            "invitation_token": "invalid_token_123"
        }
    )
    
    assert response.status_code == 500  # Or 400 depending on error handling


# ============================================================================
# AC-1.7.9: Multi-Company Support
# ============================================================================

def test_list_user_companies(db: Session, test_admin_user, test_company):
    """Test listing companies user belongs to (AC-1.7.9)"""
    # Create JWT
    access_token = create_access_token(
        user_id=test_admin_user.UserID,
        email=test_admin_user.Email,
        role="company_admin",
        company_id=test_company.CompanyID
    )
    
    # Get companies
    response = client.get(
        "/api/users/me/companies",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    assert response.status_code == 200
    companies = response.json()
    
    assert len(companies) > 0
    assert any(c["company_id"] == test_company.CompanyID for c in companies)
    assert companies[0]["is_primary"] == True


def test_switch_company_success(db: Session, test_admin_user, test_company):
    """Test switching active company (AC-1.7.9)"""
    # Create second company
    company2 = Company(
        CompanyName="Second Company Pty Ltd",
        CompanyTradingName="Second Company",
        ABN="53004085616",
        IsActive=True,
        CreatedDate=datetime.utcnow(),
        UpdatedDate=datetime.utcnow(),
        IsDeleted=False
    )
    db.add(company2)
    db.commit()
    db.refresh(company2)
    
    # Add user to second company
    team_role = db.query(UserCompanyRole).filter(
        UserCompanyRole.RoleCode == "company_user"
    ).first()
    uc_active_status = db.query(UserCompanyStatus).filter(
        UserCompanyStatus.StatusCode == "active"
    ).first()
    joined_via = db.query(JoinedVia).filter(JoinedVia.MethodCode == "signup").first()
    
    user_company2 = UserCompany(
        UserID=test_admin_user.UserID,
        CompanyID=company2.CompanyID,
        UserCompanyRoleID=team_role.UserCompanyRoleID if team_role else None,
        StatusID=uc_active_status.UserCompanyStatusID if uc_active_status else None,
        IsPrimaryCompany=False,
        JoinedDate=datetime.utcnow(),
        JoinedViaID=joined_via.JoinedViaID if joined_via else None,
        CreatedBy=test_admin_user.UserID,
        CreatedDate=datetime.utcnow(),
        UpdatedBy=test_admin_user.UserID,
        UpdatedDate=datetime.utcnow(),
        IsDeleted=False
    )
    db.add(user_company2)
    db.commit()
    
    # Create JWT with first company
    access_token = create_access_token(
        user_id=test_admin_user.UserID,
        email=test_admin_user.Email,
        role="company_admin",
        company_id=test_company.CompanyID
    )
    
    # Switch to second company
    response = client.post(
        "/api/users/me/switch-company",
        json={"company_id": company2.CompanyID},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["success"] == True
    assert data["company_id"] == company2.CompanyID
    assert data["company_name"] == "Second Company Pty Ltd"
    assert data["role"] == "company_user"
    assert "access_token" in data
    assert "refresh_token" in data


def test_switch_company_not_member(db: Session, test_admin_user, test_company):
    """Test cannot switch to company user doesn't belong to"""
    # Create company user doesn't belong to
    company2 = Company(
        CompanyName="Other Company Pty Ltd",
        CompanyTradingName="Other Company",
        ABN="53004085616",
        IsActive=True,
        CreatedDate=datetime.utcnow(),
        UpdatedDate=datetime.utcnow(),
        IsDeleted=False
    )
    db.add(company2)
    db.commit()
    db.refresh(company2)
    
    # Create JWT
    access_token = create_access_token(
        user_id=test_admin_user.UserID,
        email=test_admin_user.Email,
        role="company_admin",
        company_id=test_company.CompanyID
    )
    
    # Try to switch to company user doesn't belong to
    response = client.post(
        "/api/users/me/switch-company",
        json={"company_id": company2.CompanyID},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    assert response.status_code == 400
    assert "belong" in response.json()["detail"].lower()


# ============================================================================
# AC-1.7.10: Audit Logging
# ============================================================================

def test_invitation_acceptance_audit_log(db: Session, test_invitation):
    """Test invitation acceptance logged to audit (AC-1.7.10)"""
    from models.audit.activity_log import ActivityLog
    
    # Create user
    active_status = db.query(UserStatus).filter(UserStatus.StatusName == "Active").first()
    user = User(
        Email="newuser@example.com",
        PasswordHash=hash_password("TestP@ssw0rd123"),
        FirstName="New",
        LastName="User",
        EmailVerified=True,
        IsActive=True,
        UserStatusID=active_status.UserStatusID if active_status else None,
        CreatedDate=datetime.utcnow(),
        UpdatedDate=datetime.utcnow(),
        IsDeleted=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create JWT
    access_token = create_access_token(
        user_id=user.UserID,
        email=user.Email,
        role=None,
        company_id=None
    )
    
    # Accept invitation
    response = client.post(
        f"/api/invitations/{test_invitation.InvitationToken}/accept",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    assert response.status_code == 200
    
    # Check audit log
    audit_log = db.query(ActivityLog).filter(
        ActivityLog.UserID == user.UserID,
        ActivityLog.Action == "INVITATION_ACCEPTED"
    ).first()
    
    assert audit_log is not None
    assert audit_log.CompanyID == test_invitation.CompanyID


def test_company_switch_audit_log(db: Session, test_admin_user, test_company):
    """Test company switch logged to audit (AC-1.7.10)"""
    from models.audit.activity_log import ActivityLog
    
    # Create JWT
    access_token = create_access_token(
        user_id=test_admin_user.UserID,
        email=test_admin_user.Email,
        role="company_admin",
        company_id=test_company.CompanyID
    )
    
    # Switch company (to same company, just for testing)
    response = client.post(
        "/api/users/me/switch-company",
        json={"company_id": test_company.CompanyID},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    assert response.status_code == 200
    
    # Check audit log
    audit_log = db.query(ActivityLog).filter(
        ActivityLog.UserID == test_admin_user.UserID,
        ActivityLog.Action == "COMPANY_SWITCHED"
    ).first()
    
    assert audit_log is not None
    assert audit_log.CompanyID == test_company.CompanyID

