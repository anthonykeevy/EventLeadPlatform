"""
Integration Tests for Story 1.5: First-Time User Onboarding

Tests the complete onboarding flow:
1. User updates profile details
2. User creates first company
3. JWT refreshed with role and company_id
4. ABN/ACN validation
5. Audit logging
6. Security constraints
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from main import app
from common.database import Base, get_db
from models.user import User
from models.company import Company
from models.user_company import UserCompany
from models.ref.user_status import UserStatus
from models.ref.country import Country
from models.ref.industry import Industry
from models.ref.timezone import Timezone
from models.ref.user_company_role import UserCompanyRole
from models.ref.user_company_status import UserCompanyStatus
from models.ref.joined_via import JoinedVia
from models.audit.user_audit import UserAudit
from models.audit.company_audit import CompanyAudit
from modules.auth.jwt_service import create_access_token, decode_token
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
    
    # Industry
    events = Industry(
        IndustryID=1,
        IndustryCode="events",
        IndustryName="Events & Conferences"
    )
    db.add(events)
    
    # Timezone
    sydney_tz = Timezone(
        TimezoneID=1,
        TimezoneIdentifier="Australia/Sydney",
        DisplayName="Sydney (AEDT/AEST)",
        OffsetMinutes=660
    )
    melbourne_tz = Timezone(
        TimezoneID=2,
        TimezoneIdentifier="Australia/Melbourne",
        DisplayName="Melbourne (AEDT/AEST)",
        OffsetMinutes=660
    )
    db.add_all([sydney_tz, melbourne_tz])
    
    # UserCompanyRole
    admin_role = UserCompanyRole(
        UserCompanyRoleID=1,
        RoleCode="company_admin",
        RoleName="Company Administrator",
        Description="Full admin access",
        RoleLevel=100,
        CanManageCompany=True,
        CanManageUsers=True,
        CanManageEvents=True,
        CanManageForms=True,
        CanExportData=True,
        CanViewReports=True
    )
    db.add(admin_role)
    
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
    
    db.commit()


def create_test_user(db, email="test@example.com"):
    """Helper to create a test user"""
    user = User(
        Email=email,
        PasswordHash=hash_password("TestPassword123!"),
        FirstName="Test",
        LastName="User",
        StatusID=1,
        IsEmailVerified=True,
        EmailVerifiedAt=datetime.utcnow(),
        TimezoneIdentifier="Australia/Sydney",
        OnboardingComplete=False,
        OnboardingStep=1
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ============================================================================
# Test AC-1.5.1: Protected endpoint for user details
# ============================================================================

def test_update_user_details_requires_auth(db_session):
    """Test that updating user details requires authentication"""
    response = client.post(
        "/api/users/me/details",
        json={
            "phone": "+61412345678",
            "timezone_identifier": "Australia/Sydney",
            "role_title": "Marketing Manager"
        }
    )
    
    assert response.status_code == 401


def test_update_user_details_with_auth(db_session):
    """Test successful user details update (AC-1.5.1, AC-1.5.2)"""
    # Create test user
    user = create_test_user(db_session)
    
    # Generate access token
    token = create_access_token(user.UserID, user.Email)
    
    # Update user details
    response = client.post(
        "/api/users/me/details",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "phone": "+61412345678",
            "timezone_identifier": "Australia/Melbourne",
            "role_title": "Event Manager"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["user_id"] == user.UserID
    
    # Verify database update
    db_session.refresh(user)
    assert user.Phone == "+61412345678"
    assert user.TimezoneIdentifier == "Australia/Melbourne"
    assert user.RoleTitle == "Event Manager"


# ============================================================================
# Test AC-1.5.10: Timezone validation
# ============================================================================

def test_invalid_timezone_rejected(db_session):
    """Test that invalid timezone is rejected (AC-1.5.10)"""
    user = create_test_user(db_session)
    token = create_access_token(user.UserID, user.Email)
    
    response = client.post(
        "/api/users/me/details",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "phone": "+61412345678",
            "timezone_identifier": "Invalid/Timezone",
            "role_title": "Manager"
        }
    )
    
    assert response.status_code == 400
    assert "timezone" in response.json()["detail"].lower()


# ============================================================================
# Test AC-1.5.3, AC-1.5.4: Company creation
# ============================================================================

def test_create_company_requires_auth(db_session):
    """Test that creating company requires authentication (AC-1.5.3)"""
    response = client.post(
        "/api/companies",
        json={
            "company_name": "Test Company",
            "country_id": 1
        }
    )
    
    assert response.status_code == 401


def test_create_company_success(db_session):
    """Test successful company creation (AC-1.5.3, AC-1.5.4, AC-1.5.5, AC-1.5.6)"""
    user = create_test_user(db_session)
    token = create_access_token(user.UserID, user.Email)
    
    response = client.post(
        "/api/companies",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "company_name": "Acme Events Pty Ltd",
            "abn": "51824753556",
            "acn": "123456782",
            "phone": "+61298765432",
            "email": "info@acme.com",
            "website": "https://acme.com",
            "country_id": 1,
            "industry_id": 1
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    
    # Verify response structure
    assert data["success"] is True
    assert data["company_id"] > 0
    assert data["user_company_id"] > 0
    assert data["role"] == "company_admin"
    assert "access_token" in data
    assert "refresh_token" in data
    
    # Verify company created in database
    company = db_session.execute(
        select(Company).where(Company.CompanyID == data["company_id"])
    ).scalar_one()
    
    assert company.CompanyName == "Acme Events Pty Ltd"
    assert company.ABN == "51824753556"
    assert company.ACN == "123456782"
    
    # Verify UserCompany relationship (AC-1.5.5)
    user_company = db_session.execute(
        select(UserCompany).where(UserCompany.UserCompanyID == data["user_company_id"])
    ).scalar_one()
    
    assert user_company.UserID == user.UserID
    assert user_company.CompanyID == company.CompanyID
    assert user_company.IsPrimaryCompany is True
    
    # Verify role is company_admin
    role = db_session.execute(
        select(UserCompanyRole).where(
            UserCompanyRole.UserCompanyRoleID == user_company.UserCompanyRoleID
        )
    ).scalar_one()
    
    assert role.RoleCode == "company_admin"
    
    # Verify JWT contains role and company_id (AC-1.5.6)
    payload = decode_token(data["access_token"])
    assert payload["role"] == "company_admin"
    assert payload["company_id"] == company.CompanyID
    assert payload["sub"] == user.UserID


# ============================================================================
# Test AC-1.5.7: Audit logging
# ============================================================================

def test_user_update_audit_logged(db_session):
    """Test that user updates are logged to audit table (AC-1.5.7)"""
    user = create_test_user(db_session)
    token = create_access_token(user.UserID, user.Email)
    
    # Update user details
    client.post(
        "/api/users/me/details",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "phone": "+61412345678",
            "timezone_identifier": "Australia/Melbourne",
            "role_title": "Manager"
        }
    )
    
    # Check audit log
    audit_entry = db_session.execute(
        select(UserAudit)
        .where(UserAudit.UserID == user.UserID)
        .where(UserAudit.Action == "UPDATE_PROFILE")
    ).scalar_one_or_none()
    
    assert audit_entry is not None
    assert audit_entry.ChangedBy == user.UserID


def test_company_creation_audit_logged(db_session):
    """Test that company creation is logged to audit table (AC-1.5.7)"""
    user = create_test_user(db_session)
    token = create_access_token(user.UserID, user.Email)
    
    # Create company
    response = client.post(
        "/api/companies",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "company_name": "Test Company",
            "country_id": 1
        }
    )
    
    company_id = response.json()["company_id"]
    
    # Check audit log
    audit_entry = db_session.execute(
        select(CompanyAudit)
        .where(CompanyAudit.CompanyID == company_id)
        .where(CompanyAudit.Action == "CREATE")
    ).scalar_one_or_none()
    
    assert audit_entry is not None
    assert audit_entry.ChangedBy == user.UserID


# ============================================================================
# Test AC-1.5.8: User cannot create duplicate company
# ============================================================================

def test_user_cannot_create_second_company(db_session):
    """Test that user cannot create company if already has one (AC-1.5.8)"""
    user = create_test_user(db_session)
    token = create_access_token(user.UserID, user.Email)
    
    # Create first company
    response1 = client.post(
        "/api/companies",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "company_name": "First Company",
            "country_id": 1
        }
    )
    
    assert response1.status_code == 201
    
    # Try to create second company
    response2 = client.post(
        "/api/companies",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "company_name": "Second Company",
            "country_id": 1
        }
    )
    
    assert response2.status_code == 400
    assert "already has" in response2.json()["detail"].lower()


# ============================================================================
# Test AC-1.5.9: ABN/ACN validation
# ============================================================================

def test_valid_abn_accepted(db_session):
    """Test that valid ABN is accepted (AC-1.5.9)"""
    user = create_test_user(db_session)
    token = create_access_token(user.UserID, user.Email)
    
    # Valid ABN: 51 824 753 556
    response = client.post(
        "/api/companies",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "company_name": "Test Company",
            "abn": "51824753556",
            "country_id": 1
        }
    )
    
    assert response.status_code == 201


def test_invalid_abn_rejected(db_session):
    """Test that invalid ABN is rejected (AC-1.5.9)"""
    user = create_test_user(db_session)
    token = create_access_token(user.UserID, user.Email)
    
    # Invalid ABN (bad checksum)
    response = client.post(
        "/api/companies",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "company_name": "Test Company",
            "abn": "12345678901",  # Invalid checksum
            "country_id": 1
        }
    )
    
    assert response.status_code == 400
    assert "abn" in response.json()["detail"].lower()


def test_valid_acn_accepted(db_session):
    """Test that valid ACN is accepted (AC-1.5.9)"""
    user = create_test_user(db_session)
    token = create_access_token(user.UserID, user.Email)
    
    # Valid ACN: 123 456 782
    response = client.post(
        "/api/companies",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "company_name": "Test Company",
            "acn": "123456782",
            "country_id": 1
        }
    )
    
    assert response.status_code == 201


def test_invalid_acn_rejected(db_session):
    """Test that invalid ACN is rejected (AC-1.5.9)"""
    user = create_test_user(db_session)
    token = create_access_token(user.UserID, user.Email)
    
    # Invalid ACN (bad checksum)
    response = client.post(
        "/api/companies",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "company_name": "Test Company",
            "acn": "123456789",  # Invalid checksum
            "country_id": 1
        }
    )
    
    assert response.status_code == 400
    assert "acn" in response.json()["detail"].lower()


def test_abn_with_spaces_accepted(db_session):
    """Test that ABN with spaces is normalized and accepted"""
    user = create_test_user(db_session)
    token = create_access_token(user.UserID, user.Email)
    
    # Valid ABN with spaces
    response = client.post(
        "/api/companies",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "company_name": "Test Company",
            "abn": "51 824 753 556",
            "country_id": 1
        }
    )
    
    assert response.status_code == 201


# ============================================================================
# Test Complete Onboarding Flow
# ============================================================================

def test_complete_onboarding_flow(db_session):
    """Test the complete onboarding flow from start to finish"""
    # Step 1: User signs up and is verified (Story 1.1)
    user = create_test_user(db_session, email="newuser@example.com")
    
    # Step 2: User logs in (Story 1.2) - gets JWT without role/company
    token = create_access_token(user.UserID, user.Email)
    payload = decode_token(token)
    assert "role" not in payload
    assert "company_id" not in payload
    
    # Step 3: User updates profile details
    response = client.post(
        "/api/users/me/details",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "phone": "+61412345678",
            "timezone_identifier": "Australia/Sydney",
            "role_title": "Event Manager"
        }
    )
    
    assert response.status_code == 200
    
    # Step 4: User creates company
    response = client.post(
        "/api/companies",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "company_name": "New Events Co",
            "abn": "51824753556",
            "country_id": 1
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    
    # Step 5: Verify UserCompany created with company_admin role
    user_company = db_session.execute(
        select(UserCompany).where(UserCompany.UserID == user.UserID)
    ).scalar_one()
    
    assert user_company is not None
    
    # Step 6: Verify new JWT has role and company_id
    new_token = data["access_token"]
    new_payload = decode_token(new_token)
    assert new_payload["role"] == "company_admin"
    assert new_payload["company_id"] == data["company_id"]
    
    # Step 7: User can now access protected company endpoints
    # (This would be tested in future stories)
    
    # Verify onboarding marked complete
    db_session.refresh(user)
    assert user.OnboardingComplete is True
    assert user.OnboardingStep == 5

