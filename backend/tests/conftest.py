"""
Pytest configuration and fixtures for EventLead Platform
"""
import pytest
import asyncio
from typing import AsyncGenerator, Generator, Optional
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
import tempfile
from datetime import datetime, timedelta

# Import your FastAPI app and database models
import sys
from fastapi import FastAPI

# Add backend directory to path for consistent imports
backend_dir = os.path.dirname(os.path.dirname(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Import app and models - this will register all models with Base
from main import app
from common.database import Base, get_db
# Import models module to ensure all models are registered
import models
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
        from common.database import engine as prod_engine, SessionLocal
        session = SessionLocal()
        try:
            yield session
        finally:
            session.close()
    else:
        # Create in-memory SQLite database for testing
        engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # Create session
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = TestingSessionLocal()
        
        try:
            yield session
        finally:
            session.close()
            Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(test_db) -> TestClient:
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
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
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
def auth_headers(client: TestClient, sample_user_data: dict):
    """Create authenticated user and return auth headers."""
    # Signup user
    signup_response = client.post("/api/auth/signup", json=sample_user_data)
    assert signup_response.status_code == 201
    
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
def unverified_user_data():
    """User data for unverified user testing."""
    return {
        "email": "unverified@example.com",
        "password": "TestPassword123!",
        "first_name": "Unverified",
        "last_name": "User"
    }

@pytest.fixture
def mock_email_service(monkeypatch):
    """Mock email service to prevent actual emails during testing."""
    async def mock_send_verification_email(email: str, token: str, user_name: Optional[str] = None):
        return True
    
    async def mock_send_password_reset_email(email: str, token: str, user_name: Optional[str] = None):
        return True
    
    # Mock the email service methods
    monkeypatch.setattr("modules.auth.service.email_service.send_verification_email", mock_send_verification_email)
    monkeypatch.setattr("modules.auth.service.email_service.send_password_reset_email", mock_send_password_reset_email)

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
        default_data = {
            "email": "test@example.com",
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
    existing_user = test_db.query(User).filter_by(Email="testuser@example.com").first()
    if existing_user:
        # Clean up existing user's companies to ensure clean state
        from models.user_company import UserCompany
        test_db.query(UserCompany).filter_by(UserID=existing_user.UserID).delete()
        test_db.commit()
        return existing_user
    
    user = User(
        Email="testuser@example.com",
        PasswordHash="$2b$12$dummyhash",
        FirstName="Test",
        LastName="User",
        StatusID=active_status.UserStatusID,
        IsEmailVerified=True
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user

# Test markers for different test types
pytestmark = [
    pytest.mark.asyncio,
]
