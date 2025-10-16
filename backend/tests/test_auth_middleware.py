"""
Tests for JWT Authentication Middleware and RBAC
Tests AC-1.3.1 through AC-1.3.10
"""
import pytest
from fastapi import FastAPI, Request, Depends
from fastapi.testclient import TestClient
from jose import jwt  # type: ignore
from datetime import datetime, timedelta

from middleware.auth import JWTAuthMiddleware
from modules.auth.dependencies import get_current_user, get_current_user_optional
from modules.auth.models import CurrentUser
from modules.auth.jwt_service import create_access_token, create_refresh_token
from common.rbac import require_role, has_role, is_company_admin, belongs_to_company
from config.jwt import get_secret_key, get_algorithm


# Test app with JWT middleware
@pytest.fixture
def test_app() -> FastAPI:
    """Create test FastAPI app with JWT middleware."""
    app = FastAPI()
    
    # Add JWT middleware
    app.add_middleware(JWTAuthMiddleware)
    
    # Test endpoints
    @app.get("/public")
    async def public_endpoint():
        return {"message": "public"}
    
    @app.get("/protected")
    async def protected_endpoint(
        current_user: CurrentUser = Depends(get_current_user)
    ):
        return {
            "message": "protected",
            "user_id": current_user.user_id,
            "email": current_user.email
        }
    
    @app.get("/admin-only")
    @require_role("company_admin")
    async def admin_endpoint(
        request: Request,
        current_user: CurrentUser = Depends(get_current_user)
    ):
        return {"message": "admin access granted"}
    
    @app.get("/multi-role")
    @require_role(["company_admin", "company_user"])
    async def multi_role_endpoint(
        request: Request,
        current_user: CurrentUser = Depends(get_current_user)
    ):
        return {"message": "access granted"}
    
    @app.get("/optional-auth")
    async def optional_auth_endpoint(
        current_user: CurrentUser | None = Depends(get_current_user_optional)
    ):
        if current_user:
            return {"authenticated": True, "user_id": current_user.user_id}
        return {"authenticated": False}
    
    return app


@pytest.fixture
def test_client(test_app: FastAPI) -> TestClient:
    """Create test client for test app."""
    return TestClient(test_app)


# AC-1.3.1: JWT authentication middleware validates access tokens on protected endpoints
class TestJWTValidation:
    """Test JWT token validation (AC-1.3.1, AC-1.3.6)"""
    
    def test_valid_token_allows_access(self, test_client: TestClient):
        """Test that valid access token allows request to proceed."""
        token = create_access_token(
            user_id=123,
            email="test@example.com",
            role="company_admin",
            company_id=456
        )
        
        response = test_client.get(
            "/protected",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        assert response.json()["user_id"] == 123
        assert response.json()["email"] == "test@example.com"
    
    def test_missing_token_returns_401(self, test_client: TestClient):
        """Test that missing token returns 401 Unauthorized."""
        response = test_client.get("/protected")
        
        assert response.status_code == 401
        assert "Missing authorization header" in response.json()["detail"]
    
    def test_invalid_token_format_returns_401(self, test_client: TestClient):
        """Test that invalid token format returns 401."""
        response = test_client.get(
            "/protected",
            headers={"Authorization": "InvalidFormat token123"}
        )
        
        assert response.status_code == 401
        assert "Invalid authorization header format" in response.json()["detail"]
    
    def test_invalid_token_returns_401(self, test_client: TestClient):
        """Test that invalid token returns 401."""
        response = test_client.get(
            "/protected",
            headers={"Authorization": "Bearer invalid_token_string"}
        )
        
        assert response.status_code == 401
        assert "Invalid token" in response.json()["detail"]
    
    def test_expired_token_returns_401(self, test_client: TestClient):
        """Test that expired token returns 401."""
        # Create expired token (1 second ago)
        past_time = datetime.utcnow() - timedelta(seconds=1)
        payload = {
            "sub": 123,
            "email": "test@example.com",
            "type": "access",
            "exp": past_time,
            "iat": past_time - timedelta(minutes=60)
        }
        
        expired_token = jwt.encode(
            payload,
            get_secret_key(),
            algorithm=get_algorithm()
        )
        
        response = test_client.get(
            "/protected",
            headers={"Authorization": f"Bearer {expired_token}"}
        )
        
        assert response.status_code == 401
        assert "expired" in response.json()["detail"].lower()


# AC-1.3.2: Middleware extracts and validates JWT payload
class TestJWTPayloadExtraction:
    """Test JWT payload extraction (AC-1.3.2)"""
    
    def test_extracts_user_id_from_sub_claim(self, test_client: TestClient):
        """Test that user_id is extracted from 'sub' claim."""
        token = create_access_token(
            user_id=999,
            email="user999@example.com"
        )
        
        response = test_client.get(
            "/protected",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        assert response.json()["user_id"] == 999
    
    def test_extracts_email_claim(self, test_client: TestClient):
        """Test that email is extracted from payload."""
        token = create_access_token(
            user_id=123,
            email="john.doe@example.com"
        )
        
        response = test_client.get(
            "/protected",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        assert response.json()["email"] == "john.doe@example.com"
    
    def test_rejects_refresh_token(self, test_client: TestClient):
        """Test that refresh tokens are rejected (must be access token)."""
        refresh_token = create_refresh_token(user_id=123)
        
        response = test_client.get(
            "/protected",
            headers={"Authorization": f"Bearer {refresh_token}"}
        )
        
        assert response.status_code == 401
        assert "Invalid token type" in response.json()["detail"]


# AC-1.3.3: Current user information injected into request state
class TestCurrentUserInjection:
    """Test current user injection into request.state (AC-1.3.3)"""
    
    def test_user_injected_into_request_state(self, test_client: TestClient):
        """Test that CurrentUser is stored in request.state.user."""
        token = create_access_token(
            user_id=123,
            email="test@example.com",
            role="company_admin",
            company_id=456
        )
        
        response = test_client.get(
            "/protected",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Endpoint successfully accessed current user
        assert response.status_code == 200
        assert response.json()["user_id"] == 123


# AC-1.3.4: Role-based authorization decorator enforces role requirements
class TestRoleBasedAuthorization:
    """Test @require_role decorator (AC-1.3.4)"""
    
    def test_correct_role_allows_access(self, test_client: TestClient):
        """Test that user with correct role can access endpoint."""
        token = create_access_token(
            user_id=123,
            email="admin@example.com",
            role="company_admin",
            company_id=456
        )
        
        response = test_client.get(
            "/admin-only",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        assert response.json()["message"] == "admin access granted"
    
    def test_wrong_role_returns_403(self, test_client: TestClient):
        """Test that user with wrong role gets 403 Forbidden."""
        token = create_access_token(
            user_id=123,
            email="user@example.com",
            role="company_user",
            company_id=456
        )
        
        response = test_client.get(
            "/admin-only",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 403
        assert "Insufficient permissions" in response.json()["detail"]
    
    def test_missing_role_returns_403(self, test_client: TestClient):
        """Test that user with no role gets 403 Forbidden."""
        token = create_access_token(
            user_id=123,
            email="norole@example.com",
            role=None,
            company_id=456
        )
        
        response = test_client.get(
            "/admin-only",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 403
        assert "does not have any role assigned" in response.json()["detail"]
    
    def test_multiple_roles_allowed(self, test_client: TestClient):
        """Test endpoint with multiple allowed roles."""
        # Test company_admin can access
        admin_token = create_access_token(
            user_id=1,
            email="admin@example.com",
            role="company_admin",
            company_id=100
        )
        
        response = test_client.get(
            "/multi-role",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        
        # Test company_user can access
        user_token = create_access_token(
            user_id=2,
            email="user@example.com",
            role="company_user",
            company_id=100
        )
        
        response = test_client.get(
            "/multi-role",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == 200
        
        # Test other role cannot access
        other_token = create_access_token(
            user_id=3,
            email="other@example.com",
            role="other_role",
            company_id=100
        )
        
        response = test_client.get(
            "/multi-role",
            headers={"Authorization": f"Bearer {other_token}"}
        )
        assert response.status_code == 403


# AC-1.3.5: Company context middleware ensures multi-tenant data isolation
class TestCompanyContext:
    """Test company context extraction (AC-1.3.5)"""
    
    def test_company_id_extracted_from_jwt(self, test_client: TestClient):
        """Test that company_id is extracted from JWT."""
        token = create_access_token(
            user_id=123,
            email="test@example.com",
            role="company_admin",
            company_id=789
        )
        
        response = test_client.get(
            "/protected",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Successfully authenticated - company_id should be in request.state.user
        assert response.status_code == 200


# AC-1.3.7: Unauthorized access returns 401 or 403
class TestUnauthorizedAccess:
    """Test error codes for unauthorized access (AC-1.3.7)"""
    
    def test_no_token_returns_401(self, test_client: TestClient):
        """Test that missing token returns 401 Unauthorized."""
        response = test_client.get("/protected")
        assert response.status_code == 401
    
    def test_invalid_token_returns_401(self, test_client: TestClient):
        """Test that invalid token returns 401 Unauthorized."""
        response = test_client.get(
            "/protected",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401
    
    def test_wrong_role_returns_403(self, test_client: TestClient):
        """Test that valid token with wrong role returns 403 Forbidden."""
        token = create_access_token(
            user_id=123,
            email="user@example.com",
            role="company_user",
            company_id=456
        )
        
        response = test_client.get(
            "/admin-only",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 403


# AC-1.3.9: Dependency injection get_current_user() provides user in endpoints
class TestGetCurrentUserDependency:
    """Test get_current_user() dependency (AC-1.3.9)"""
    
    def test_get_current_user_returns_user(self, test_client: TestClient):
        """Test that get_current_user() returns CurrentUser from request.state."""
        token = create_access_token(
            user_id=123,
            email="test@example.com",
            role="company_admin",
            company_id=456
        )
        
        response = test_client.get(
            "/protected",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        assert response.json()["user_id"] == 123
        assert response.json()["email"] == "test@example.com"
    
    def test_get_current_user_raises_401_if_not_authenticated(self, test_client: TestClient):
        """Test that get_current_user() raises 401 if not authenticated."""
        response = test_client.get("/protected")
        assert response.status_code == 401


# AC-1.3.8: Optional authentication
class TestOptionalAuthentication:
    """Test optional authentication endpoints (AC-1.3.8)"""
    
    def test_optional_auth_with_token(self, test_client: TestClient):
        """Test optional auth endpoint with valid token."""
        token = create_access_token(
            user_id=123,
            email="test@example.com"
        )
        
        response = test_client.get(
            "/optional-auth",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        assert response.json()["authenticated"] is True
        assert response.json()["user_id"] == 123
    
    def test_optional_auth_without_token(self, test_client: TestClient):
        """Test optional auth endpoint without token (public access)."""
        response = test_client.get("/optional-auth")
        
        assert response.status_code == 200
        assert response.json()["authenticated"] is False


# Test helper functions
class TestAuthorizationHelpers:
    """Test RBAC helper functions (AC-1.3.4)"""
    
    def test_has_role(self):
        """Test has_role() helper function."""
        user = CurrentUser(
            user_id=123,
            email="test@example.com",
            role="company_admin",
            company_id=456
        )
        
        assert has_role(user, "company_admin") is True
        assert has_role(user, "company_user") is False
    
    def test_is_company_admin(self):
        """Test is_company_admin() helper function."""
        admin = CurrentUser(
            user_id=1,
            email="admin@example.com",
            role="company_admin",
            company_id=100
        )
        
        user = CurrentUser(
            user_id=2,
            email="user@example.com",
            role="company_user",
            company_id=100
        )
        
        assert is_company_admin(admin) is True
        assert is_company_admin(user) is False
    
    def test_belongs_to_company(self):
        """Test belongs_to_company() helper function."""
        user = CurrentUser(
            user_id=123,
            email="test@example.com",
            role="company_admin",
            company_id=456
        )
        
        assert belongs_to_company(user, 456) is True
        assert belongs_to_company(user, 789) is False


# Test public paths
class TestPublicPaths:
    """Test that public paths skip authentication"""
    
    def test_public_auth_endpoints_accessible(self, test_client: TestClient):
        """Test that auth endpoints don't require token."""
        public_endpoints = [
            "/",
            "/docs",
            "/api/health",
        ]
        
        for endpoint in public_endpoints:
            response = test_client.get(endpoint)
            # Should not return 401 (some may return 404, that's fine)
            assert response.status_code != 401

