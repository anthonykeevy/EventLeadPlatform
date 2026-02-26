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
from sqlalchemy import select
from datetime import datetime, timedelta
import uuid

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


@pytest.fixture(autouse=True)
def mock_email_delivery(monkeypatch):
    """Prevent real SMTP calls so invitation tests remain deterministic."""
    from unittest.mock import AsyncMock, MagicMock
    import importlib

    mock_svc = MagicMock()
    mock_svc.send_team_invitation_email = AsyncMock(return_value=True)
    mock_svc.send_added_to_company_email = AsyncMock(return_value=True)

    def _get_email_service():
        return mock_svc

    companies_router_module = importlib.import_module("modules.companies.router")
    monkeypatch.setattr(companies_router_module, "get_email_service", _get_email_service)
    return mock_svc


def seed_reference_data(db):
    """Load required reference rows for invitation tests."""
    refs = {
        "active_status": db.execute(select(UserStatus).where(UserStatus.StatusCode == "active")).scalar_one_or_none(),
        "company_admin_role": db.execute(
            select(UserCompanyRole).where(UserCompanyRole.RoleCode == "company_admin")
        ).scalar_one_or_none(),
        "company_user_role": db.execute(
            select(UserCompanyRole).where(UserCompanyRole.RoleCode == "company_user")
        ).scalar_one_or_none(),
        "active_membership_status": db.execute(
            select(UserCompanyStatus).where(UserCompanyStatus.StatusCode == "active")
        ).scalar_one_or_none(),
        "signup_method": db.execute(select(JoinedVia).where(JoinedVia.MethodCode == "signup")).scalar_one_or_none(),
        "pending_invite_status": db.execute(
            select(UserInvitationStatus).where(UserInvitationStatus.StatusCode == "pending")
        ).scalar_one_or_none(),
        "country_au": db.execute(select(Country).where(Country.CountryCode == "AU")).scalar_one_or_none(),
    }

    missing = [name for name, value in refs.items() if value is None]
    if missing:
        raise RuntimeError(f"Missing required reference data for invitation tests: {', '.join(missing)}")

    return refs


def unique_email(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}@example.com"


def create_test_company_admin(db):
    """Helper to create a company admin user"""
    refs = seed_reference_data(db)
    suffix = uuid.uuid4().hex[:8]

    # Create user
    user = User(
        Email=f"admin-{suffix}@example.com",
        PasswordHash=hash_password("TestPassword123!"),
        FirstName="Admin",
        LastName="User",
        StatusID=refs["active_status"].UserStatusID,
        IsEmailVerified=True,
        EmailVerifiedAt=datetime.utcnow(),
        TimezoneIdentifier="Australia/Sydney"
    )
    db.add(user)
    db.flush()
    
    # Create company
    company = Company(
        CompanyName=f"Test Company {suffix}",
        CountryID=refs["country_au"].CountryID,
        IsActive=True,
        CreatedBy=user.UserID
    )
    db.add(company)
    db.flush()
    
    # Create UserCompany relationship
    user_company = UserCompany(
        UserID=user.UserID,
        CompanyID=company.CompanyID,
        UserCompanyRoleID=refs["company_admin_role"].UserCompanyRoleID,
        StatusID=refs["active_membership_status"].UserCompanyStatusID,
        IsPrimaryCompany=True,
        JoinedViaID=refs["signup_method"].JoinedViaID,
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

def test_send_invitation_requires_auth(client, db_session):
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


def test_send_invitation_requires_company_admin(client, db_session):
    """Test that only company_admin can send invitations"""
    admin, company = create_test_company_admin(db_session)
    refs = seed_reference_data(db_session)
    user_email = unique_email("user")

    # Create regular user (not admin)
    user = User(
        Email=user_email,
        PasswordHash=hash_password("TestPassword123!"),
        FirstName="Regular",
        LastName="User",
        StatusID=refs["active_status"].UserStatusID,
        IsEmailVerified=True,
        TimezoneIdentifier="Australia/Sydney"
    )
    db_session.add(user)
    db_session.commit()
    
    # Generate token without role or with company_user role
    token = create_access_token(
        db=db_session,
        user_id=user.UserID,
        email=user.Email,
        role="company_user",
        company_id=company.CompanyID,
    )
    
    response = client.post(
        f"/api/companies/{company.CompanyID}/invite",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": unique_email("invite"),
            "first_name": "Test",
            "last_name": "User",
            "role": "company_user"
        }
    )
    
    assert response.status_code == 403


# ============================================================================
# Test AC-1.6.2, AC-1.6.3, AC-1.6.4: Send invitation with token and email
# ============================================================================

def test_send_invitation_success(client, db_session):
    """Test successful invitation sending (AC-1.6.2, AC-1.6.3, AC-1.6.4)"""
    admin, company = create_test_company_admin(db_session)
    invite_email = unique_email("newmember")
    token = create_access_token(
        db=db_session,
        user_id=admin.UserID,
        email=admin.Email,
        role="company_admin",
        company_id=company.CompanyID,
    )
    
    response = client.post(
        f"/api/companies/{company.CompanyID}/invite",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": invite_email,
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
        select(UserInvitation).where(UserInvitation.Email == invite_email)
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

def test_cannot_invite_existing_member(client, db_session):
    """Test that existing company member cannot be invited (AC-1.6.5)"""
    admin, company = create_test_company_admin(db_session)
    token = create_access_token(
        db=db_session,
        user_id=admin.UserID,
        email=admin.Email,
        role="company_admin",
        company_id=company.CompanyID,
    )
    
    # Try to invite the admin (who is already a member)
    response = client.post(
        f"/api/companies/{company.CompanyID}/invite",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": admin.Email,
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

def test_invitation_with_different_roles(client, db_session):
    """Test invitations can be sent with different roles (AC-1.6.6)"""
    admin, company = create_test_company_admin(db_session)
    invite_email = unique_email("admin2")
    token = create_access_token(
        db=db_session,
        user_id=admin.UserID,
        email=admin.Email,
        role="company_admin",
        company_id=company.CompanyID,
    )
    
    # Send invitation with company_admin role
    response = client.post(
        f"/api/companies/{company.CompanyID}/invite",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": invite_email,
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
        .where(UserInvitation.Email == invite_email)
    ).scalar_one()
    
    role = db_session.execute(
        select(UserCompanyRole).where(UserCompanyRole.UserCompanyRoleID == invitation.UserCompanyRoleID)
    ).scalar_one()
    
    assert role.RoleCode == "company_admin"


# ============================================================================
# Test AC-1.6.7: Resend invitation
# ============================================================================

def test_resend_invitation_success(client, db_session):
    """Test resending invitation (AC-1.6.7)"""
    admin, company = create_test_company_admin(db_session)
    invite_email = unique_email("resend")
    token = create_access_token(
        db=db_session,
        user_id=admin.UserID,
        email=admin.Email,
        role="company_admin",
        company_id=company.CompanyID,
    )
    
    # Send initial invitation
    response = client.post(
        f"/api/companies/{company.CompanyID}/invite",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": invite_email,
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

def test_cancel_invitation_success(client, db_session):
    """Test cancelling invitation (AC-1.6.8)"""
    admin, company = create_test_company_admin(db_session)
    invite_email = unique_email("cancel")
    token = create_access_token(
        db=db_session,
        user_id=admin.UserID,
        email=admin.Email,
        role="company_admin",
        company_id=company.CompanyID,
    )
    
    # Send invitation
    response = client.post(
        f"/api/companies/{company.CompanyID}/invite",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": invite_email,
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

def test_list_invitations(client, db_session):
    """Test listing company invitations (AC-1.6.9)"""
    admin, company = create_test_company_admin(db_session)
    token = create_access_token(
        db=db_session,
        user_id=admin.UserID,
        email=admin.Email,
        role="company_admin",
        company_id=company.CompanyID,
    )
    
    # Send multiple invitations
    suffix = uuid.uuid4().hex[:6]
    for i in range(3):
        client.post(
            f"/api/companies/{company.CompanyID}/invite",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "email": f"member{i}-{suffix}@example.com",
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

def test_invitation_audit_logging(client, db_session):
    """Test that invitation events are logged to audit table (AC-1.6.10)"""
    admin, company = create_test_company_admin(db_session)
    invite_email = unique_email("audit")
    token = create_access_token(
        db=db_session,
        user_id=admin.UserID,
        email=admin.Email,
        role="company_admin",
        company_id=company.CompanyID,
    )
    
    # Send invitation
    response = client.post(
        f"/api/companies/{company.CompanyID}/invite",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": invite_email,
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
    assert invite_email in audit_log.NewValue
    
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

def test_admin_cannot_invite_to_different_company(client, db_session):
    """Test that admin cannot invite users to a different company"""
    admin, company = create_test_company_admin(db_session)
    token = create_access_token(
        db=db_session,
        user_id=admin.UserID,
        email=admin.Email,
        role="company_admin",
        company_id=company.CompanyID,
    )
    
    # Try to invite to a different company
    response = client.post(
        "/api/companies/999/invite",  # Different company ID
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": unique_email("wrong-company"),
            "first_name": "Test",
            "last_name": "User",
            "role": "company_user"
        }
    )
    
    assert response.status_code == 403


def test_cannot_invite_with_invalid_role(client, db_session):
    """Test that invalid role is rejected"""
    admin, company = create_test_company_admin(db_session)
    token = create_access_token(
        db=db_session,
        user_id=admin.UserID,
        email=admin.Email,
        role="company_admin",
        company_id=company.CompanyID,
    )
    
    response = client.post(
        f"/api/companies/{company.CompanyID}/invite",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": unique_email("invalid-role"),
            "first_name": "Test",
            "last_name": "User",
            "role": "super_admin"  # Invalid role
        }
    )
    
    assert response.status_code == 400


def test_cannot_resend_cancelled_invitation(client, db_session):
    """Test that cancelled invitations cannot be resent"""
    admin, company = create_test_company_admin(db_session)
    invite_email = unique_email("resend-cancelled")
    token = create_access_token(
        db=db_session,
        user_id=admin.UserID,
        email=admin.Email,
        role="company_admin",
        company_id=company.CompanyID,
    )
    
    # Send and cancel invitation
    response = client.post(
        f"/api/companies/{company.CompanyID}/invite",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": invite_email,
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

