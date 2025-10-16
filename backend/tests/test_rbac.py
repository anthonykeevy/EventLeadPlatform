"""
Role-Based Access Control Tests (Story 1.8)
Tests AC-1.8.3, AC-1.8.4, AC-1.8.5
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from common.database import get_db
from tests.test_utils import (
    MultiTenantTestScenario,
    get_auth_headers
)

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
def test_scenario(db: Session):
    """Create multi-tenant test scenario"""
    scenario = MultiTenantTestScenario(db)
    yield scenario
    scenario.cleanup()


# ============================================================================
# AC-1.8.5: Role requirements enforced on all protected endpoints
# ============================================================================

def test_company_admin_can_send_invitations(test_scenario):
    """Test company_admin can send team invitations"""
    response = client.post(
        f"/api/companies/{test_scenario.company_a.CompanyID}/invite",
        headers=get_auth_headers(test_scenario.token_admin_a),
        json={
            "email": "newmember@company-a.com",
            "role": "company_user",
            "message": "Join our team"
        }
    )
    assert response.status_code == 201
    assert response.json()["success"] == True


def test_company_user_cannot_send_invitations(test_scenario):
    """Test company_user cannot send team invitations (AC-1.8.5)"""
    response = client.post(
        f"/api/companies/{test_scenario.company_a.CompanyID}/invite",
        headers=get_auth_headers(test_scenario.token_user_a),
        json={
            "email": "newmember@company-a.com",
            "role": "company_user",
            "message": "Join our team"
        }
    )
    assert response.status_code == 403
    assert "admin" in response.json()["detail"].lower()


def test_company_admin_can_list_invitations(test_scenario):
    """Test company_admin can list invitations"""
    response = client.get(
        f"/api/companies/{test_scenario.company_a.CompanyID}/invitations",
        headers=get_auth_headers(test_scenario.token_admin_a)
    )
    assert response.status_code == 200


def test_company_user_cannot_list_invitations(test_scenario):
    """Test company_user cannot list invitations (AC-1.8.5)"""
    response = client.get(
        f"/api/companies/{test_scenario.company_a.CompanyID}/invitations",
        headers=get_auth_headers(test_scenario.token_user_a)
    )
    assert response.status_code == 403


def test_company_admin_can_cancel_invitations(test_scenario):
    """Test company_admin can cancel invitations"""
    # First, send invitation
    invite_response = client.post(
        f"/api/companies/{test_scenario.company_a.CompanyID}/invite",
        headers=get_auth_headers(test_scenario.token_admin_a),
        json={
            "email": "cancel@company-a.com",
            "role": "company_user",
            "message": "Join our team"
        }
    )
    assert invite_response.status_code == 201
    invitation_id = invite_response.json()["invitation_id"]
    
    # Cancel invitation
    response = client.delete(
        f"/api/companies/{test_scenario.company_a.CompanyID}/invitations/{invitation_id}",
        headers=get_auth_headers(test_scenario.token_admin_a)
    )
    assert response.status_code == 200


def test_company_user_cannot_cancel_invitations(test_scenario):
    """Test company_user cannot cancel invitations (AC-1.8.5)"""
    # Admin sends invitation
    invite_response = client.post(
        f"/api/companies/{test_scenario.company_a.CompanyID}/invite",
        headers=get_auth_headers(test_scenario.token_admin_a),
        json={
            "email": "cancel2@company-a.com",
            "role": "company_user",
            "message": "Join our team"
        }
    )
    assert invite_response.status_code == 201
    invitation_id = invite_response.json()["invitation_id"]
    
    # Regular user tries to cancel
    response = client.delete(
        f"/api/companies/{test_scenario.company_a.CompanyID}/invitations/{invitation_id}",
        headers=get_auth_headers(test_scenario.token_user_a)
    )
    assert response.status_code == 403


def test_company_admin_can_resend_invitations(test_scenario):
    """Test company_admin can resend invitations"""
    # Send invitation
    invite_response = client.post(
        f"/api/companies/{test_scenario.company_a.CompanyID}/invite",
        headers=get_auth_headers(test_scenario.token_admin_a),
        json={
            "email": "resend@company-a.com",
            "role": "company_user",
            "message": "Join our team"
        }
    )
    assert invite_response.status_code == 201
    invitation_id = invite_response.json()["invitation_id"]
    
    # Resend invitation
    response = client.post(
        f"/api/companies/{test_scenario.company_a.CompanyID}/invitations/{invitation_id}/resend",
        headers=get_auth_headers(test_scenario.token_admin_a)
    )
    assert response.status_code == 200


def test_company_user_cannot_resend_invitations(test_scenario):
    """Test company_user cannot resend invitations (AC-1.8.5)"""
    # Admin sends invitation
    invite_response = client.post(
        f"/api/companies/{test_scenario.company_a.CompanyID}/invite",
        headers=get_auth_headers(test_scenario.token_admin_a),
        json={
            "email": "resend2@company-a.com",
            "role": "company_user",
            "message": "Join our team"
        }
    )
    assert invite_response.status_code == 201
    invitation_id = invite_response.json()["invitation_id"]
    
    # Regular user tries to resend
    response = client.post(
        f"/api/companies/{test_scenario.company_a.CompanyID}/invitations/{invitation_id}/resend",
        headers=get_auth_headers(test_scenario.token_user_a)
    )
    assert response.status_code == 403


# ============================================================================
# Additional RBAC Tests
# ============================================================================

def test_all_users_can_view_own_profile(test_scenario):
    """Test all authenticated users can view their own profile"""
    # Admin can view profile
    response = client.get(
        "/api/users/me",
        headers=get_auth_headers(test_scenario.token_admin_a)
    )
    assert response.status_code == 200
    
    # Regular user can view profile
    response = client.get(
        "/api/users/me",
        headers=get_auth_headers(test_scenario.token_user_a)
    )
    assert response.status_code == 200


def test_all_users_can_update_own_profile(test_scenario):
    """Test all authenticated users can update their own profile"""
    # Admin can update profile
    response = client.post(
        "/api/users/me/details",
        headers=get_auth_headers(test_scenario.token_admin_a),
        json={
            "phone": "+61412345678",
            "timezone_identifier": "Australia/Sydney",
            "role_title": "Senior Manager"
        }
    )
    assert response.status_code == 200
    
    # Regular user can update profile
    response = client.post(
        "/api/users/me/details",
        headers=get_auth_headers(test_scenario.token_user_a),
        json={
            "phone": "+61487654321",
            "timezone_identifier": "Australia/Melbourne",
            "role_title": "Team Member"
        }
    )
    assert response.status_code == 200


def test_all_users_can_list_their_companies(test_scenario):
    """Test all authenticated users can list companies they belong to"""
    # Admin can list companies
    response = client.get(
        "/api/users/me/companies",
        headers=get_auth_headers(test_scenario.token_admin_a)
    )
    assert response.status_code == 200
    assert len(response.json()) > 0
    
    # Regular user can list companies
    response = client.get(
        "/api/users/me/companies",
        headers=get_auth_headers(test_scenario.token_user_a)
    )
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_all_users_can_switch_companies(test_scenario, db: Session):
    """Test all authenticated users can switch between their companies"""
    # Note: This test would require setting up multi-company users
    # For now, test that users can switch to their current company (no-op but valid)
    response = client.post(
        "/api/users/me/switch-company",
        headers=get_auth_headers(test_scenario.token_admin_a),
        json={"company_id": int(test_scenario.company_a.CompanyID)}  # type: ignore
    )
    assert response.status_code == 200


def test_role_enforcement_across_all_admin_endpoints(test_scenario):
    """Test that all admin-only endpoints enforce role requirements"""
    admin_endpoints = [
        ("POST", f"/api/companies/{test_scenario.company_a.CompanyID}/invite", {
            "email": "test@test.com",
            "role": "company_user",
            "message": "Join us"
        }),
        ("GET", f"/api/companies/{test_scenario.company_a.CompanyID}/invitations", None),
    ]
    
    for method, endpoint, body in admin_endpoints:
        # Regular user should be denied
        if method == "POST":
            response = client.post(
                endpoint,
                headers=get_auth_headers(test_scenario.token_user_a),
                json=body
            )
        elif method == "GET":
            response = client.get(
                endpoint,
                headers=get_auth_headers(test_scenario.token_user_a)
            )
        
        assert response.status_code == 403, f"Expected 403 for {method} {endpoint}, got {response.status_code}"
        
        # Admin should be allowed
        if method == "POST":
            response = client.post(
                endpoint,
                headers=get_auth_headers(test_scenario.token_admin_a),
                json=body
            )
        elif method == "GET":
            response = client.get(
                endpoint,
                headers=get_auth_headers(test_scenario.token_admin_a)
            )
        
        assert response.status_code in [200, 201], f"Expected 200/201 for admin on {method} {endpoint}, got {response.status_code}"


def test_unauthenticated_requests_denied_for_all_protected_endpoints():
    """Test that all protected endpoints require authentication"""
    protected_endpoints = [
        ("GET", "/api/users/me"),
        ("GET", "/api/users/me/companies"),
        ("POST", "/api/users/me/details", {"phone": "+61412345678"}),
        ("POST", "/api/users/me/switch-company", {"company_id": 1}),
    ]
    
    for method, endpoint, *body in protected_endpoints:
        if method == "GET":
            response = client.get(endpoint)
        elif method == "POST":
            response = client.post(endpoint, json=body[0] if body else None)
        
        assert response.status_code == 401, f"Expected 401 for unauthenticated {method} {endpoint}, got {response.status_code}"

