"""
Multi-Tenancy Data Isolation Tests (Story 1.8)
Tests AC-1.8.1, AC-1.8.2, AC-1.8.3, AC-1.8.4, AC-1.8.6
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from common.database import get_db
from tests.test_utils import (
    MultiTenantTestScenario,
    create_test_company,
    create_test_user,
    create_test_token,
    create_test_invitation,
    get_auth_headers
)
from common.multi_tenant import (
    filter_by_company,
    verify_company_access,
    require_company_context,
    verify_path_company_matches_user
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
# AC-1.8.1: All company-scoped queries filter by company_id from JWT
# ============================================================================

def test_filter_by_company_helper_requires_company_id(db: Session):
    """Test filter_by_company raises exception if no company_id"""
    from models.company import Company
    
    query = db.query(Company)
    
    with pytest.raises(Exception) as exc_info:
        filter_by_company(query, None)
    
    assert exc_info.value.status_code == 403
    assert "no company context" in str(exc_info.value.detail).lower()


def test_filter_by_company_helper_filters_correctly(db: Session, test_scenario):
    """Test filter_by_company applies correct filter"""
    from models.company import Company
    
    query = db.query(Company)
    filtered_query = filter_by_company(query, test_scenario.company_a.CompanyID)
    
    # Should only return Company A
    companies = filtered_query.all()
    assert len(companies) == 1
    assert companies[0].CompanyID == test_scenario.company_a.CompanyID


def test_require_company_context_raises_if_none():
    """Test require_company_context raises exception if None"""
    with pytest.raises(Exception) as exc_info:
        require_company_context(None)
    
    assert exc_info.value.status_code == 403


def test_require_company_context_returns_valid_id():
    """Test require_company_context returns valid company_id"""
    company_id = require_company_context(123)
    assert company_id == 123


# ============================================================================
# AC-1.8.2: Users cannot access other companies' data
# ============================================================================

def test_user_cannot_access_other_company_invitations(test_scenario):
    """Test user from Company A cannot view Company B's invitations"""
    # Admin B sends invitation
    response = client.post(
        f"/api/companies/{test_scenario.company_b.CompanyID}/invite",
        headers=get_auth_headers(test_scenario.token_admin_b),
        json={
            "email": "newuser@company-b.com",
            "role": "company_user",
            "message": "Join our team"
        }
    )
    assert response.status_code == 201
    
    # Admin A tries to view Company B's invitations
    response = client.get(
        f"/api/companies/{test_scenario.company_b.CompanyID}/invitations",
        headers=get_auth_headers(test_scenario.token_admin_a)
    )
    assert response.status_code == 403
    assert "different company" in response.json()["detail"].lower()


def test_user_cannot_invite_to_other_company(test_scenario):
    """Test user from Company A cannot send invitation to Company B"""
    # Admin A tries to send invitation to Company B
    response = client.post(
        f"/api/companies/{test_scenario.company_b.CompanyID}/invite",
        headers=get_auth_headers(test_scenario.token_admin_a),
        json={
            "email": "newuser@company-b.com",
            "role": "company_user",
            "message": "Join our team"
        }
    )
    assert response.status_code == 403
    assert "different company" in response.json()["detail"].lower()


def test_user_cannot_access_other_company_data_via_company_switch(test_scenario):
    """Test user cannot switch to company they don't belong to"""
    # User A tries to switch to Company B
    response = client.post(
        "/api/users/me/switch-company",
        headers=get_auth_headers(test_scenario.token_user_a),
        json={"company_id": int(test_scenario.company_b.CompanyID)}  # type: ignore
    )
    assert response.status_code == 400
    assert "belong" in response.json()["detail"].lower()


def test_verify_company_access_blocks_cross_company_access(test_scenario):
    """Test verify_company_access helper blocks cross-company access"""
    with pytest.raises(Exception) as exc_info:
        verify_company_access(
            resource_company_id=int(test_scenario.company_b.CompanyID),  # type: ignore
            user_company_id=int(test_scenario.company_a.CompanyID),  # type: ignore
            resource_type="Event"
        )
    
    assert exc_info.value.status_code == 403
    assert "different company" in str(exc_info.value.detail).lower()


def test_verify_path_company_matches_user_blocks_mismatch(test_scenario):
    """Test verify_path_company_matches_user blocks company_id manipulation"""
    with pytest.raises(Exception) as exc_info:
        verify_path_company_matches_user(
            path_company_id=int(test_scenario.company_b.CompanyID),  # type: ignore
            user_company_id=int(test_scenario.company_a.CompanyID)  # type: ignore
        )
    
    assert exc_info.value.status_code == 403
    assert "cannot access different company" in str(exc_info.value.detail).lower()


# ============================================================================
# AC-1.8.3: Company admins can only manage their own company
# ============================================================================

def test_company_admin_can_invite_to_own_company(test_scenario):
    """Test company admin can send invitations to their own company"""
    response = client.post(
        f"/api/companies/{test_scenario.company_a.CompanyID}/invite",
        headers=get_auth_headers(test_scenario.token_admin_a),
        json={
            "email": "newuser@company-a.com",
            "role": "company_user",
            "message": "Join our team"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] == True


def test_company_admin_cannot_invite_to_other_company(test_scenario):
    """Test company admin cannot send invitations to other company"""
    # Admin A tries to invite to Company B
    response = client.post(
        f"/api/companies/{test_scenario.company_b.CompanyID}/invite",
        headers=get_auth_headers(test_scenario.token_admin_a),
        json={
            "email": "newuser@company-b.com",
            "role": "company_user",
            "message": "Join our team"
        }
    )
    assert response.status_code == 403


def test_company_admin_can_view_own_company_invitations(test_scenario):
    """Test company admin can view their own company's invitations"""
    # Send invitation first
    client.post(
        f"/api/companies/{test_scenario.company_a.CompanyID}/invite",
        headers=get_auth_headers(test_scenario.token_admin_a),
        json={
            "email": "newuser@company-a.com",
            "role": "company_user",
            "message": "Join our team"
        }
    )
    
    # View invitations
    response = client.get(
        f"/api/companies/{test_scenario.company_a.CompanyID}/invitations",
        headers=get_auth_headers(test_scenario.token_admin_a)
    )
    assert response.status_code == 200
    invitations = response.json()
    assert len(invitations) > 0
    # All invitations should belong to Company A
    for inv in invitations:
        assert inv["company_id"] == test_scenario.company_a.CompanyID


def test_company_admin_cannot_view_other_company_invitations(test_scenario):
    """Test company admin cannot view other company's invitations"""
    response = client.get(
        f"/api/companies/{test_scenario.company_b.CompanyID}/invitations",
        headers=get_auth_headers(test_scenario.token_admin_a)
    )
    assert response.status_code == 403


# ============================================================================
# AC-1.8.4: Company users can only view their own company's data
# ============================================================================

def test_company_user_can_view_own_companies(test_scenario):
    """Test company user can view companies they belong to"""
    response = client.get(
        "/api/users/me/companies",
        headers=get_auth_headers(test_scenario.token_user_a)
    )
    assert response.status_code == 200
    companies = response.json()
    assert len(companies) > 0
    # Should only see Company A
    assert all(c["company_id"] == test_scenario.company_a.CompanyID for c in companies)


def test_company_user_cannot_invite_team_members(test_scenario):
    """Test company user cannot send invitations (admin-only action)"""
    response = client.post(
        f"/api/companies/{test_scenario.company_a.CompanyID}/invite",
        headers=get_auth_headers(test_scenario.token_user_a),
        json={
            "email": "newuser@company-a.com",
            "role": "company_user",
            "message": "Join our team"
        }
    )
    assert response.status_code == 403
    assert "admin" in response.json()["detail"].lower()


def test_company_user_cannot_view_invitations(test_scenario):
    """Test company user cannot view invitations (admin-only action)"""
    response = client.get(
        f"/api/companies/{test_scenario.company_a.CompanyID}/invitations",
        headers=get_auth_headers(test_scenario.token_user_a)
    )
    # Should be 403 because user is not admin
    assert response.status_code == 403


def test_company_user_cannot_cancel_invitations(test_scenario):
    """Test company user cannot cancel invitations (admin-only action)"""
    # Admin A creates invitation
    invite_response = client.post(
        f"/api/companies/{test_scenario.company_a.CompanyID}/invite",
        headers=get_auth_headers(test_scenario.token_admin_a),
        json={
            "email": "newuser@company-a.com",
            "role": "company_user",
            "message": "Join our team"
        }
    )
    assert invite_response.status_code == 201
    invitation_id = invite_response.json()["invitation_id"]
    
    # User A tries to cancel invitation
    response = client.delete(
        f"/api/companies/{test_scenario.company_a.CompanyID}/invitations/{invitation_id}",
        headers=get_auth_headers(test_scenario.token_user_a)
    )
    assert response.status_code == 403


# ============================================================================
# AC-1.8.6: Comprehensive test suite validates data isolation
# ============================================================================

def test_multi_company_user_sees_correct_data(db: Session):
    """Test user belonging to multiple companies sees correct data per company"""
    # Create two companies
    company_a = create_test_company(db, "Multi Company A")
    company_b = create_test_company(db, "Multi Company B")
    
    # Create user belonging to both companies
    user = create_test_user(
        db,
        "multi@test.com",
        company_id=company_a.CompanyID,
        role_code="company_admin",
        onboarding_complete=True
    )
    
    # Add user to Company B
    from models.user_company import UserCompany
    from models.ref.user_company_role import UserCompanyRole
    from models.ref.user_company_status import UserCompanyStatus
    from models.ref.joined_via import JoinedVia
    from datetime import datetime
    
    role = db.query(UserCompanyRole).filter(
        UserCompanyRole.RoleCode == "company_user"
    ).first()
    uc_status = db.query(UserCompanyStatus).filter(
        UserCompanyStatus.StatusCode == "active"
    ).first()
    joined_via = db.query(JoinedVia).filter(
        JoinedVia.MethodCode == "invitation"
    ).first()
    
    user_company_b = UserCompany(
        UserID=user.UserID,
        CompanyID=company_b.CompanyID,
        UserCompanyRoleID=role.UserCompanyRoleID if role else None,
        StatusID=uc_status.UserCompanyStatusID if uc_status else None,
        IsPrimaryCompany=False,
        JoinedDate=datetime.utcnow(),
        JoinedViaID=joined_via.JoinedViaID if joined_via else None,
        CreatedBy=user.UserID,
        CreatedDate=datetime.utcnow(),
        UpdatedBy=user.UserID,
        UpdatedDate=datetime.utcnow(),
        IsDeleted=False
    )
    db.add(user_company_b)
    db.commit()
    
    # Create tokens for each company context
    token_a = create_test_token(
        int(user.UserID),  # type: ignore
        str(user.Email),  # type: ignore
        "company_admin",
        int(company_a.CompanyID)  # type: ignore
    )
    token_b = create_test_token(
        int(user.UserID),  # type: ignore
        str(user.Email),  # type: ignore
        "company_user",
        int(company_b.CompanyID)  # type: ignore
    )
    
    # User should be able to list companies
    response = client.get(
        "/api/users/me/companies",
        headers=get_auth_headers(token_a)
    )
    assert response.status_code == 200
    companies = response.json()
    assert len(companies) == 2
    company_ids = [c["company_id"] for c in companies]
    assert company_a.CompanyID in company_ids
    assert company_b.CompanyID in company_ids
    
    # When using Company A token, can only access Company A
    response = client.post(
        f"/api/companies/{company_a.CompanyID}/invite",
        headers=get_auth_headers(token_a),
        json={
            "email": "test@test.com",
            "role": "company_user",
            "message": "Join us"
        }
    )
    assert response.status_code == 201
    
    # Cannot access Company B with Company A token
    response = client.post(
        f"/api/companies/{company_b.CompanyID}/invite",
        headers=get_auth_headers(token_a),
        json={
            "email": "test2@test.com",
            "role": "company_user",
            "message": "Join us"
        }
    )
    assert response.status_code == 403


def test_data_isolation_across_all_protected_endpoints(test_scenario):
    """
    Comprehensive test: Verify data isolation across all company-scoped endpoints.
    
    Tests that User A (Company A) cannot access any of Company B's resources.
    """
    # List of endpoints to test (company-scoped)
    test_cases = [
        # Invitations
        ("GET", f"/api/companies/{test_scenario.company_b.CompanyID}/invitations", None),
        ("POST", f"/api/companies/{test_scenario.company_b.CompanyID}/invite", {
            "email": "test@test.com",
            "role": "company_user",
            "message": "Join us"
        }),
    ]
    
    for method, endpoint, body in test_cases:
        if method == "GET":
            response = client.get(
                endpoint,
                headers=get_auth_headers(test_scenario.token_admin_a)
            )
        elif method == "POST":
            response = client.post(
                endpoint,
                headers=get_auth_headers(test_scenario.token_admin_a),
                json=body
            )
        elif method == "DELETE":
            response = client.delete(
                endpoint,
                headers=get_auth_headers(test_scenario.token_admin_a)
            )
        
        # All should be 403 (Forbidden) - cannot access other company's data
        assert response.status_code == 403, f"Failed for {method} {endpoint}: got {response.status_code}"


# ============================================================================
# Additional Data Isolation Tests
# ============================================================================

def test_unauthenticated_user_cannot_access_protected_endpoints():
    """Test that unauthenticated requests are rejected"""
    response = client.get("/api/users/me/companies")
    assert response.status_code == 401


def test_invalid_jwt_rejected():
    """Test that invalid JWT tokens are rejected"""
    response = client.get(
        "/api/users/me/companies",
        headers={"Authorization": "Bearer invalid_token_123"}
    )
    assert response.status_code == 401


def test_jwt_without_company_context_limited_access(db: Session):
    """Test user without company context has limited access"""
    # Create user without company
    user = create_test_user(
        db,
        "nocompany@test.com",
        company_id=None,
        onboarding_complete=False
    )
    
    token = create_test_token(
        int(user.UserID),  # type: ignore
        str(user.Email),  # type: ignore
        role=None,
        company_id=None
    )
    
    # Can access user profile
    response = client.get(
        "/api/users/me",
        headers=get_auth_headers(token)
    )
    assert response.status_code == 200
    
    # Cannot access company-scoped endpoints
    response = client.get(
        "/api/users/me/companies",
        headers=get_auth_headers(token)
    )
    # Should return empty list (user belongs to no companies)
    assert response.status_code == 200
    assert response.json() == []

