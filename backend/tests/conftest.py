"""
Pytest configuration and fixtures for EventLead Platform
"""
import asyncio
import os
import sys
from typing import Generator, Optional

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy import event

# Add backend directory to path for consistent imports
backend_dir = os.path.dirname(os.path.dirname(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Import app and models - this will register all models with Base
from main import app
from common.database import Base, get_db
from modules.users.router import router as users_router
from modules.companies.router import router as companies_router
from modules.auth.router import router as auth_router
# Import other routers as needed for tests...

def create_test_app():
    test_app = FastAPI()
    test_app.include_router(auth_router)
    test_app.include_router(users_router)
    test_app.include_router(companies_router)
    # Add other routers here
    return test_app

# Test database configuration
# For Story 1.13 integration tests, we need SQL Server (not SQLite) 
# due to schema support (config.AppSetting, ref.SettingCategory, etc.)
TEST_DATABASE_URL = os.getenv("DATABASE_URL")  # Use actual database
USE_REAL_DB = TEST_DATABASE_URL and "mssql" in TEST_DATABASE_URL.lower()

@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
def test_db():
    """
    Create a test database for each test function.
    
    For Story 1.13 tests that require SQL Server schemas (config.*, ref.*),
    this will use the actual database connection from DATABASE_URL.
    For other tests, it falls back to in-memory SQLite.
    """
    if USE_REAL_DB:
        # Use actual SQL Server database for schema-dependent tests
        from common.database import engine
        connection = engine.connect()
        transaction = connection.begin()
        from sqlalchemy.orm import Session
        session = Session(bind=connection, join_transaction_mode="create_savepoint")
        try:
            yield session
        finally:
            session.close()
            transaction.rollback()
            connection.close()
    else:
        # Create in-memory SQLite database for testing
        engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            echo=True,  # Enable SQL logging
        )

        # Attach schema-like databases on every new connection (SQLite ATTACH is per-connection)
        @event.listens_for(engine, "connect")
        def _attach_schemas(dbapi_conn, connection_record):
            cursor = dbapi_conn.cursor()
            for schema in ("ref", "dbo", "config", "audit", "log", "cache"):
                cursor.execute(f"ATTACH DATABASE ':memory:' AS \"{schema}\"")
            cursor.close()

        # Create all tables
        Base.metadata.create_all(bind=engine)

        # Seed ref.UserStatus for auth tests (create_user needs "Pending Verification")
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO ref."UserStatus" (StatusCode, StatusName, Description, AllowLogin, IsActive, SortOrder)
                VALUES
                ('pending_verification', 'Pending Verification', 'Awaiting email verification', 0, 1, 0),
                ('active', 'Active', 'Active user', 1, 1, 1)
            """))
            conn.commit()
        
        # Create session
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = TestingSessionLocal()
        
        try:
            yield session
        finally:
            session.close()
            Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(test_db) -> Generator[TestClient, None, None]:
    """Create a test client with database dependency override."""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

@pytest.fixture
def sample_user_data():
    """Sample user data for testing. Uses unique email per test to avoid conflicts with shared DB."""
    import uuid
    unique = str(uuid.uuid4())[:8]
    return {
        "email": f"test-{unique}@example.com",
        "password": "TestPassword123!",
        "first_name": "Test",
        "last_name": "User"
    }

@pytest.fixture
def sample_company_data():
    """Sample company data for testing."""
    return {
        "company_name": "Test Company",
        "abn": "12345678901",
        "industry": "Technology",
        "address": "123 Test Street, Test City, 2000"
    }

@pytest.fixture
def auth_headers(client: TestClient, sample_user_data: dict, test_db):
    """Create authenticated user and return auth headers."""
    # Signup user
    signup_response = client.post("/api/auth/signup", json=sample_user_data)
    assert signup_response.status_code == 201
    
    # Needs to be verified/active for proper login based on test framework changes.
    from models.user import User
    from models.ref.user_status import UserStatus
    active_status = test_db.query(UserStatus).filter_by(StatusCode='active').first()
    user = test_db.query(User).filter_by(Email=sample_user_data["email"]).first()
    if user and active_status:
        user.StatusID = active_status.UserStatusID
        user.IsEmailVerified = True
        test_db.commit()

    # Login user
    login_data = {
        "email": sample_user_data["email"],
        "password": sample_user_data["password"]
    }
    login_response = client.post("/api/auth/login", json=login_data)
    assert login_response.status_code == 200
    
    token_data = login_response.json()
    return {"Authorization": f"Bearer {token_data['access_token']}"}

@pytest.fixture
def user_auth_headers(client: TestClient, test_db):
    """Create authenticated user with company_user role and return auth headers."""
    import uuid
    unique = str(uuid.uuid4())[:8]
    user_data = {
        "email": f"company-user-{unique}@example.com",
        "password": "TestPassword123!",
        "first_name": "Company",
        "last_name": "User"
    }
    
    # Signup user
    signup_response = client.post("/api/auth/signup", json=user_data)
    assert signup_response.status_code == 201
    
    from models.user import User
    from models.ref.user_status import UserStatus
    active_status = test_db.query(UserStatus).filter_by(StatusCode='active').first()
    user = test_db.query(User).filter_by(Email=user_data["email"]).first()
    if user and active_status:
        user.StatusID = active_status.UserStatusID
        user.IsEmailVerified = True
        test_db.commit()

    # Login user
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    login_response = client.post("/api/auth/login", json=login_data)
    assert login_response.status_code == 200
    
    token_data = login_response.json()
    return {"Authorization": f"Bearer {token_data['access_token']}"}

@pytest.fixture
def unverified_user_data():
    """User data for unverified user testing."""
    import uuid
    unique = str(uuid.uuid4())[:8]
    return {
        "email": f"unverified-{unique}@example.com",
        "password": "TestPassword123!",
        "first_name": "Unverified",
        "last_name": "User"
    }

@pytest.fixture
def mock_email_service(monkeypatch):
    """Mock email service to prevent actual emails during testing."""
    from unittest.mock import AsyncMock, MagicMock

    mock_svc = MagicMock()
    mock_svc.send_email = AsyncMock(return_value=True)
    mock_svc.send_verification_email = AsyncMock(return_value=True)
    mock_svc.send_password_reset_email = AsyncMock(return_value=True)
    mock_svc.send_team_invitation_email = AsyncMock(return_value=True)
    mock_svc.send_added_to_company_email = AsyncMock(return_value=True)

    def _get_email_service():
        return mock_svc

    monkeypatch.setattr("services.email_service.get_email_service", _get_email_service)

@pytest.fixture
def mailhog_environment(monkeypatch):
    """Set up environment for MailHog integration testing."""
    monkeypatch.setenv("ENVIRONMENT", "development")
    monkeypatch.setenv("SMTP_SERVER", "localhost")
    monkeypatch.setenv("SMTP_PORT", "1025")
    monkeypatch.setenv("FROM_EMAIL", "noreply@eventlead.com")
    monkeypatch.setenv("FROM_NAME", "EventLead Platform")
    monkeypatch.setenv("FRONTEND_URL", "http://localhost:3000")

@pytest.fixture
def mock_jwt_secret(monkeypatch):
    """Mock JWT secret for consistent testing."""
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret-key-for-testing-only")
    monkeypatch.setenv("JWT_ALGORITHM", "HS256")

@pytest.fixture
def mock_database_url(monkeypatch):
    """Mock database URL for testing."""
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")

# Test data factories
class UserFactory:
    """Factory for creating test users."""
    
    @staticmethod
    def create_user_data(**overrides):
        """Create user data with optional overrides."""
        import uuid
        unique = str(uuid.uuid4())[:8]
        default_data = {
            "email": f"test-{unique}@example.com",
            "password": "TestPassword123!",
            "first_name": "Test",
            "last_name": "User",
            "phone": "+61412345678"
        }
        default_data.update(overrides)
        return default_data
    
    @staticmethod
    def create_verified_user_data(**overrides):
        """Create verified user data."""
        data = UserFactory.create_user_data(**overrides)
        data["email_verified"] = True
        return data

class CompanyFactory:
    """Factory for creating test companies."""
    
    @staticmethod
    def create_company_data(**overrides):
        """Create company data with optional overrides."""
        default_data = {
            "company_name": "Test Company Pty Ltd",
            "abn": "12345678901",
            "industry": "Technology",
            "address": "123 Test Street, Test City, NSW 2000",
            "phone": "+61234567890",
            "website": "https://testcompany.com"
        }
        default_data.update(overrides)
        return default_data

# Utility functions for tests
def assert_user_created(response_data: dict, expected_email: str):
    """Assert that user was created successfully."""
    assert "user_id" in response_data
    assert "email" in response_data
    assert response_data["email"] == expected_email
    assert "message" in response_data

def assert_email_verification_sent(response_data: dict):
    """Assert that email verification was sent."""
    assert "message" in response_data
    assert "email" in response_data

def assert_login_successful(response_data: dict):
    """Assert that login was successful."""
    assert "access_token" in response_data
    assert "refresh_token" in response_data
    assert "token_type" in response_data
    assert response_data["token_type"] == "bearer"

def assert_login_failed(response_data: dict, expected_error: Optional[str] = None):
    """Assert that login failed."""
    assert "detail" in response_data
    if expected_error:
        assert expected_error in response_data["detail"]

# Fixtures for Story 1.11 tests
@pytest.fixture(scope="function")
def db_session(test_db):
    """Alias for test_db to match Story 1.11 test expectations."""
    return test_db

@pytest.fixture
def test_user(test_db):
    """Create a test user for Story 1.11 tests."""
    from models.user import User
    from models.ref.user_status import UserStatus
    from common.security import hash_password
    
    # Get the 'active' StatusID from the database
    active_status = test_db.query(UserStatus).filter_by(StatusCode='active').first()
    if not active_status:
        # If status doesn't exist, create it for testing
        active_status = UserStatus(
            StatusCode='active',
            StatusName='Active',
            Description='User account is active and can log in normally',
            AllowLogin=True,
            IsActive=True,
            SortOrder=1
        )
        test_db.add(active_status)
        test_db.commit()
        test_db.refresh(active_status)
    
    # Check if user already exists
    import uuid
    existing_user = test_db.query(User).filter_by(Email="testuser@example.com").first()
    if existing_user:
        # Normalize legacy fixture state to avoid invalid-password hash panics during login.
        existing_user.PasswordHash = hash_password("TestP@ssw0rd123")
        test_db.commit()
        return existing_user
    
    user = User(
        Email=f"testuser-{uuid.uuid4().hex[:8]}@example.com",
        PasswordHash=hash_password("TestP@ssw0rd123"),
        FirstName="Test",
        LastName="User",
        StatusID=active_status.UserStatusID,
        IsEmailVerified=True
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user

@pytest.fixture
def test_company(test_db, test_user):
    from models.company import Company
    from models.ref.country import Country
    
    # Ensure Country
    country = test_db.query(Country).filter_by(CountryCode="AU").first()
    if not country:
        country = Country(CountryCode="AU", CountryName="Australia", PhonePrefix="+61", CurrencyCode="AUD", CurrencySymbol="$", CurrencyName="Australian Dollar")
        test_db.add(country)
        test_db.commit()
        test_db.refresh(country)
        
    import uuid
    company_name = f"Test Company {uuid.uuid4().hex[:8]}"
    company = test_db.query(Company).filter_by(CompanyName=company_name).first()
    if not company:
        company = Company(CompanyName=company_name, CountryID=country.CountryID, IsActive=True)
        test_db.add(company)
        test_db.commit()
        test_db.refresh(company)
        
    return company

@pytest.fixture
def test_event(test_db, test_company, test_user):
    from models.event import Event
    from models.ref.event_type import EventType
    from datetime import datetime
    
    event_type = test_db.query(EventType).filter_by(TypeCode="CONFERENCE").first()
    if not event_type:
        event_type = EventType(TypeCode="CONFERENCE", TypeName="Conference", CreatedBy=test_user.UserID)
        test_db.add(event_type)
        test_db.commit()
        test_db.refresh(event_type)
        
    event = test_db.query(Event).filter_by(Name="Test Event").first()
    if not event:
        event = Event(Name="Test Event", CompanyID=test_company.CompanyID, CreatedBy=test_user.UserID, StartDateTime=datetime.utcnow(), EventTypeID=event_type.EventTypeID)
        test_db.add(event)
        test_db.commit()
        test_db.refresh(event)
        
    return event

def create_test_token(
    db,
    user_id: int,
    email: str,
    role: Optional[str] = None,
    company_id: Optional[int] = None
) -> str:
    """Create a valid JWT token for testing.
    Uses the real token creation logic from jwt_service."""
    from modules.auth.jwt_service import create_access_token
    return create_access_token(
        db=db,
        user_id=user_id,
        email=email,
        role=role,
        company_id=company_id
    )

@pytest.fixture
def admin_token_headers(test_db, test_user, test_company, client):
    """Get auth headers by actually logging in as the test user"""
    # Create the user and company relationships
    from models.user_company import UserCompany
    from models.ref.user_company_role import UserCompanyRole
    from models.ref.user_company_status import UserCompanyStatus
    from models.ref.joined_via import JoinedVia
    from datetime import datetime

    role = test_db.query(UserCompanyRole).filter(UserCompanyRole.RoleCode == "company_admin").first()
    uc_status = test_db.query(UserCompanyStatus).filter(UserCompanyStatus.StatusCode == "active").first()
    joined_via = test_db.query(JoinedVia).filter(JoinedVia.MethodCode == "signup").first()

    # Check if relationship already exists
    existing_uc = test_db.query(UserCompany).filter_by(UserID=test_user.UserID, CompanyID=test_company.CompanyID).first()
    if not existing_uc:
        user_company = UserCompany(
            UserID=test_user.UserID,
            CompanyID=test_company.CompanyID,
            UserCompanyRoleID=role.UserCompanyRoleID if role else None,
            StatusID=uc_status.UserCompanyStatusID if uc_status else None,
            IsPrimaryCompany=True,
            JoinedDate=datetime.utcnow(),
            JoinedViaID=joined_via.JoinedViaID if joined_via else None,
            CreatedBy=test_user.UserID,
            CreatedDate=datetime.utcnow(),
            UpdatedBy=test_user.UserID,
            UpdatedDate=datetime.utcnow(),
            IsDeleted=False
        )
        test_db.add(user_company)
        test_db.commit()

    # Login to get real token
    response = client.post("/api/auth/login", json={
        "email": test_user.Email,
        "password": "TestP@ssw0rd123"  # Default password from create_test_user
    })
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        return {"Authorization": f"Bearer {token}"}
    
    # Fallback to direct token creation if login fails (e.g. in unit tests)
    token = create_test_token(test_db, user_id=test_user.UserID, email=test_user.Email, role="company_admin", company_id=test_company.CompanyID)
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def user_token_headers(test_db, test_user, test_company, client):
    """Get auth headers by actually logging in as the test user"""
    # Create the user and company relationships
    from models.user_company import UserCompany
    from models.ref.user_company_role import UserCompanyRole
    from models.ref.user_company_status import UserCompanyStatus
    from models.ref.joined_via import JoinedVia
    from datetime import datetime

    role = test_db.query(UserCompanyRole).filter(UserCompanyRole.RoleCode == "company_user").first()
    uc_status = test_db.query(UserCompanyStatus).filter(UserCompanyStatus.StatusCode == "active").first()
    joined_via = test_db.query(JoinedVia).filter(JoinedVia.MethodCode == "signup").first()

    # Check if relationship already exists
    existing_uc = test_db.query(UserCompany).filter_by(UserID=test_user.UserID, CompanyID=test_company.CompanyID).first()
    if not existing_uc:
        user_company = UserCompany(
            UserID=test_user.UserID,
            CompanyID=test_company.CompanyID,
            UserCompanyRoleID=role.UserCompanyRoleID if role else None,
            StatusID=uc_status.UserCompanyStatusID if uc_status else None,
            IsPrimaryCompany=True,
            JoinedDate=datetime.utcnow(),
            JoinedViaID=joined_via.JoinedViaID if joined_via else None,
            CreatedBy=test_user.UserID,
            CreatedDate=datetime.utcnow(),
            UpdatedBy=test_user.UserID,
            UpdatedDate=datetime.utcnow(),
            IsDeleted=False
        )
        test_db.add(user_company)
        test_db.commit()
    else:
        # Update role if needed
        if existing_uc.UserCompanyRoleID != (role.UserCompanyRoleID if role else None):
            existing_uc.UserCompanyRoleID = role.UserCompanyRoleID if role else None
            test_db.commit()

    # Login to get real token
    response = client.post("/api/auth/login", json={
        "email": test_user.Email,
        "password": "TestP@ssw0rd123"  # Default password from create_test_user
    })
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        return {"Authorization": f"Bearer {token}"}
    
    # Fallback to direct token creation if login fails
    token = create_test_token(test_db, user_id=test_user.UserID, email=test_user.Email, role="company_user", company_id=test_company.CompanyID)
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def mock_draft_form(test_db, test_company, test_event, test_user):
    from models.form import Form
    from models.form_version import FormVersion
    from models.ref.form_status import FormStatus
    from models.ref.form_approval_status import FormApprovalStatus
    from models.form_public_link import FormPublicLink
    import secrets
    
    form_status = test_db.query(FormStatus).filter_by(StatusCode="DRAFT").first()
    if not form_status:
        form_status = FormStatus(StatusCode="DRAFT", StatusName="Draft", CreatedBy=test_user.UserID)
        test_db.add(form_status)
        test_db.commit()
        test_db.refresh(form_status)

    approval_status = test_db.query(FormApprovalStatus).filter_by(ApprovalStatusCode="APPROVED").first()
    if not approval_status:
        approval_status = FormApprovalStatus(ApprovalStatusCode="APPROVED", ApprovalStatusName="Approved", CreatedBy=test_user.UserID)
        test_db.add(approval_status)
        test_db.commit()
        test_db.refresh(approval_status)
        
    form = Form(
        FormName="Draft Form",
        CompanyID=test_company.CompanyID,
        EventID=test_event.EventID,
        FormStatusID=form_status.FormStatusID,
        FormApprovalStatusID=approval_status.FormApprovalStatusID,
        CreatedBy=test_user.UserID
    )
    test_db.add(form)
    test_db.commit()
    test_db.refresh(form)
    
    form_version = FormVersion(
        FormID=form.FormID,
        VersionNumber=1,
        DefinitionJSON="{}",
        Status="DRAFT",
        IsActive=True,
        CreatedBy=test_user.UserID
    )
    test_db.add(form_version)
    test_db.commit()

    link = FormPublicLink(
        FormID=form.FormID,
        Token=secrets.token_urlsafe(16),
        LinkType="PREVIEW",
        IsActive=True,
        CreatedBy=test_user.UserID
    )
    test_db.add(link)
    test_db.commit()
    test_db.refresh(link)
    
    return {"form_id": str(form.FormID), "token": link.Token}

@pytest.fixture
def mock_published_form(test_db, test_company, test_event, test_user):
    from models.form import Form
    from models.form_version import FormVersion
    from models.ref.form_status import FormStatus
    from models.ref.form_approval_status import FormApprovalStatus
    from models.form_public_link import FormPublicLink
    import secrets
    
    form_status = test_db.query(FormStatus).filter_by(StatusCode="PUBLISHED").first()
    if not form_status:
        form_status = FormStatus(StatusCode="PUBLISHED", StatusName="Published", CreatedBy=test_user.UserID)
        test_db.add(form_status)
        test_db.commit()
        test_db.refresh(form_status)

    approval_status = test_db.query(FormApprovalStatus).filter_by(ApprovalStatusCode="APPROVED").first()
    if not approval_status:
        approval_status = FormApprovalStatus(ApprovalStatusCode="APPROVED", ApprovalStatusName="Approved", CreatedBy=test_user.UserID)
        test_db.add(approval_status)
        test_db.commit()
        test_db.refresh(approval_status)
        
    form = Form(
        FormName="Published Form",
        CompanyID=test_company.CompanyID,
        EventID=test_event.EventID,
        FormStatusID=form_status.FormStatusID,
        FormApprovalStatusID=approval_status.FormApprovalStatusID,
        CreatedBy=test_user.UserID,
        IsPublic=True
    )
    test_db.add(form)
    test_db.commit()
    test_db.refresh(form)
    
    form_version = FormVersion(
        FormID=form.FormID,
        VersionNumber=1,
        DefinitionJSON="{}",
        Status="PUBLISHED",
        IsActive=True,
        CreatedBy=test_user.UserID
    )
    test_db.add(form_version)
    test_db.commit()

    link = FormPublicLink(
        FormID=form.FormID,
        Token=secrets.token_urlsafe(16),
        LinkType="PRODUCTION",
        IsActive=True,
        CreatedBy=test_user.UserID
    )
    test_db.add(link)
    test_db.commit()
    test_db.refresh(link)
    
    return {"form_id": str(form.FormID), "token": link.Token}

# Test markers for different test types
pytestmark = [
    pytest.mark.asyncio,
]
