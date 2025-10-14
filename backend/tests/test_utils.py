"""
Test utilities and helpers for EventLead Platform tests
"""
import pytest
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import json
import hashlib
import secrets

class TestDataFactory:
    """Factory for creating test data."""
    
    @staticmethod
    def create_user_data(**overrides) -> Dict[str, Any]:
        """Create user data with optional overrides."""
        default_data = {
            "email": f"test{secrets.token_hex(4)}@example.com",
            "password": "TestPassword123!",
            "first_name": "Test",
            "last_name": "User",
            "phone": "+61412345678"
        }
        default_data.update(overrides)
        return default_data
    
    @staticmethod
    def create_company_data(**overrides) -> Dict[str, Any]:
        """Create company data with optional overrides."""
        default_data = {
            "company_name": f"Test Company {secrets.token_hex(4)} Pty Ltd",
            "abn": f"{secrets.randbelow(90000000000) + 10000000000}",  # Valid ABN range
            "industry": "Technology",
            "address": "123 Test Street, Test City, NSW 2000",
            "phone": "+61234567890",
            "website": "https://testcompany.com"
        }
        default_data.update(overrides)
        return default_data
    
    @staticmethod
    def create_event_data(**overrides) -> Dict[str, Any]:
        """Create event data with optional overrides."""
        default_data = {
            "event_name": f"Test Event {secrets.token_hex(4)}",
            "description": "Test event description",
            "start_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "end_date": (datetime.now() + timedelta(days=31)).isoformat(),
            "location": "Test Venue, Test City",
            "max_attendees": 100
        }
        default_data.update(overrides)
        return default_data

class TestAssertions:
    """Custom assertions for tests."""
    
    @staticmethod
    def assert_user_created(response_data: Dict[str, Any], expected_email: str):
        """Assert that user was created successfully."""
        assert "user_id" in response_data
        assert "email" in response_data
        assert response_data["email"] == expected_email
        assert "email_verified" in response_data
        assert response_data["email_verified"] is False
        assert "created_date" in response_data
    
    @staticmethod
    def assert_email_verification_sent(response_data: Dict[str, Any]):
        """Assert that email verification was sent."""
        assert "message" in response_data
        assert "verification_sent" in response_data
        assert response_data["verification_sent"] is True
    
    @staticmethod
    def assert_login_successful(response_data: Dict[str, Any]):
        """Assert that login was successful."""
        assert "access_token" in response_data
        assert "refresh_token" in response_data
        assert "token_type" in response_data
        assert response_data["token_type"] == "bearer"
        assert len(response_data["access_token"]) > 0
        assert len(response_data["refresh_token"]) > 0
    
    @staticmethod
    def assert_login_failed(response_data: Dict[str, Any], expected_error: Optional[str] = None):
        """Assert that login failed."""
        assert "detail" in response_data
        if expected_error:
            assert expected_error.lower() in response_data["detail"].lower()
    
    @staticmethod
    def assert_validation_error(response_data: Dict[str, Any], field_name: str):
        """Assert that validation error occurred for specific field."""
        assert "detail" in response_data
        assert isinstance(response_data["detail"], list)
        
        field_errors = [error for error in response_data["detail"] if field_name in error.get("loc", [])]
        assert len(field_errors) > 0
    
    @staticmethod
    def assert_security_headers(headers: Dict[str, str]):
        """Assert that security headers are present."""
        required_headers = [
            "x-content-type-options",
            "x-frame-options",
            "x-xss-protection"
        ]
        
        for header in required_headers:
            assert header in headers, f"Missing security header: {header}"

class TestHelpers:
    """Helper functions for tests."""
    
    @staticmethod
    def generate_test_email(prefix: str = "test") -> str:
        """Generate a unique test email address."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = secrets.token_hex(4)
        return f"{prefix}_{timestamp}_{random_suffix}@example.com"
    
    @staticmethod
    def generate_test_token(length: int = 32) -> str:
        """Generate a test token."""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password for testing."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def create_auth_headers(access_token: str) -> Dict[str, str]:
        """Create authorization headers."""
        return {"Authorization": f"Bearer {access_token}"}
    
    @staticmethod
    def extract_user_id_from_response(response_data: Dict[str, Any]) -> str:
        """Extract user ID from API response."""
        assert "user_id" in response_data
        return response_data["user_id"]
    
    @staticmethod
    def extract_token_from_response(response_data: Dict[str, Any], token_type: str = "access_token") -> str:
        """Extract token from API response."""
        assert token_type in response_data
        return response_data[token_type]

class MockData:
    """Mock data for testing."""
    
    VALID_ABNS = [
        "12345678901",
        "98765432109",
        "11223344556"
    ]
    
    INVALID_ABNS = [
        "1234567890",    # Too short
        "123456789012",  # Too long
        "abcdefghijk",   # Non-numeric
        "00000000000",   # All zeros
        ""               # Empty
    ]
    
    VALID_EMAILS = [
        "test@example.com",
        "user.name@domain.co.uk",
        "test+tag@example.org",
        "123@test.com"
    ]
    
    INVALID_EMAILS = [
        "invalid-email",
        "@example.com",
        "test@",
        "test..test@example.com",
        "test@example",
        ""
    ]
    
    WEAK_PASSWORDS = [
        "123",           # Too short
        "password",      # No numbers, no special chars
        "12345678",      # Only numbers
        "Password",      # No numbers, no special chars
        "password123",   # No special chars, no uppercase
    ]
    
    STRONG_PASSWORDS = [
        "Password123!",
        "MySecure@Pass1",
        "Test123$Password",
        "StrongP@ssw0rd"
    ]
    
    SQL_INJECTION_ATTEMPTS = [
        "'; DROP TABLE users; --",
        "' OR '1'='1",
        "'; INSERT INTO users VALUES ('hacker', 'password'); --",
        "' UNION SELECT * FROM users --"
    ]
    
    XSS_ATTEMPTS = [
        "<script>alert('xss')</script>",
        "javascript:alert('xss')",
        "<img src=x onerror=alert('xss')>",
        "<svg onload=alert('xss')>"
    ]

class TestConstants:
    """Test constants."""
    
    # HTTP Status Codes
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    TOO_MANY_REQUESTS = 429
    INTERNAL_SERVER_ERROR = 500
    
    # Test Timeouts
    DEFAULT_TIMEOUT = 30
    LONG_TIMEOUT = 60
    
    # Test Data Limits
    MAX_EMAIL_LENGTH = 100
    MAX_PASSWORD_LENGTH = 128
    MIN_PASSWORD_LENGTH = 8
    MAX_NAME_LENGTH = 100
    
    # Token Expiration Times
    EMAIL_VERIFICATION_EXPIRY_HOURS = 24
    PASSWORD_RESET_EXPIRY_HOURS = 1
    ACCESS_TOKEN_EXPIRY_MINUTES = 15
    REFRESH_TOKEN_EXPIRY_DAYS = 7
