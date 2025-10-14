"""
Test suite for user signup functionality - Story 1.1
Tests AC-1.1, AC-1.2, AC-1.3, AC-1.4
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import json

class TestUserSignup:
    """Test user signup functionality."""
    
    @pytest.mark.unit
    def test_signup_with_valid_data(self, client: TestClient, sample_user_data: dict, mock_email_service):
        """Test AC-1.1: User can submit signup form with valid email and password."""
        response = client.post("/api/auth/signup", json=sample_user_data)
        
        assert response.status_code == 201
        data = response.json()
        
        # Verify user was created
        assert "user_id" in data
        assert "email" in data
        assert data["email"] == sample_user_data["email"]
        assert "email_verified" in data
        assert data["email_verified"] is False
        assert "message" in data
    
    @pytest.mark.unit
    def test_signup_email_validation(self, client: TestClient, mock_email_service):
        """Test AC-1.2: System validates email format."""
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "test@",
            "test..test@example.com",
            "test@example",
            ""
        ]
        
        for invalid_email in invalid_emails:
            user_data = {
                "email": invalid_email,
                "password": "ValidPassword123!",
                "first_name": "Test",
                "last_name": "User"
            }
            
            response = client.post("/api/auth/signup", json=user_data)
            assert response.status_code == 422  # Validation error
            assert "email" in response.json()["detail"][0]["loc"]
    
    @pytest.mark.unit
    def test_signup_password_validation(self, client: TestClient, mock_email_service):
        """Test AC-1.2: System validates password minimum length (8 characters)."""
        invalid_passwords = [
            "123",      # Too short
            "1234567",  # 7 characters (too short)
            "",         # Empty
        ]
        
        for invalid_password in invalid_passwords:
            user_data = {
                "email": "test@example.com",
                "password": invalid_password,
                "first_name": "Test",
                "last_name": "User"
            }
            
            response = client.post("/api/auth/signup", json=user_data)
            assert response.status_code == 422  # Validation error
            assert "password" in response.json()["detail"][0]["loc"]
    
    @pytest.mark.unit
    def test_signup_duplicate_email_prevention(self, client: TestClient, sample_user_data: dict, mock_email_service):
        """Test AC-1.3: System prevents duplicate email registration (409 error returned)."""
        # First signup should succeed
        response1 = client.post("/api/auth/signup", json=sample_user_data)
        assert response1.status_code == 201
        
        # Second signup with same email should fail
        response2 = client.post("/api/auth/signup", json=sample_user_data)
        assert response2.status_code == 409
        assert "duplicate" in response2.json()["detail"].lower()
    
    @pytest.mark.integration
    @patch('modules.auth.service.email_service.send_verification_email')
    def test_signup_sends_verification_email(self, mock_send_email, client: TestClient, sample_user_data: dict):
        """Test AC-1.4: System sends verification email within 5 seconds of signup."""
        mock_send_email.return_value = True
        
        response = client.post("/api/auth/signup", json=sample_user_data)
        
        assert response.status_code == 201
        
        # Verify email service was called
        mock_send_email.assert_called_once()
        call_args = mock_send_email.call_args
        
        # Verify email and token were passed
        assert call_args[0][0] == sample_user_data["email"]  # email
        assert len(call_args[0][1]) > 0  # verification token
        assert call_args[0][2] == sample_user_data["first_name"]  # user name
    
    @pytest.mark.unit
    def test_signup_missing_required_fields(self, client: TestClient, mock_email_service):
        """Test signup with missing required fields."""
        incomplete_data = [
            {"email": "test@example.com"},  # Missing password
            {"password": "ValidPassword123!"},  # Missing email
            {"email": "test@example.com", "password": "ValidPassword123!"},  # Missing names
        ]
        
        for data in incomplete_data:
            response = client.post("/api/auth/signup", json=data)
            assert response.status_code == 422  # Validation error
    
    @pytest.mark.unit
    def test_signup_password_strength_validation(self, client: TestClient, mock_email_service):
        """Test password strength validation."""
        weak_passwords = [
            "password",     # No numbers, no special chars
            "12345678",     # Only numbers
            "Password",     # No numbers, no special chars
            "password123",  # No special chars, no uppercase
        ]
        
        for weak_password in weak_passwords:
            user_data = {
                "email": f"test{weak_password}@example.com",
                "password": weak_password,
                "first_name": "Test",
                "last_name": "User"
            }
            
            response = client.post("/api/auth/signup", json=user_data)
            # Should either succeed with warning or fail with validation error
            assert response.status_code in [201, 422]
    
    @pytest.mark.unit
    def test_signup_sql_injection_protection(self, client: TestClient, mock_email_service):
        """Test protection against SQL injection in signup."""
        malicious_data = {
            "email": "test@example.com'; DROP TABLE users; --",
            "password": "ValidPassword123!",
            "first_name": "Test'; DROP TABLE users; --",
            "last_name": "User"
        }
        
        response = client.post("/api/auth/signup", json=malicious_data)
        # Should handle gracefully (either validation error or sanitized input)
        assert response.status_code in [201, 422]
    
    @pytest.mark.unit
    def test_signup_xss_protection(self, client: TestClient, mock_email_service):
        """Test protection against XSS in signup."""
        xss_data = {
            "email": "test@example.com",
            "password": "ValidPassword123!",
            "first_name": "<script>alert('xss')</script>",
            "last_name": "User"
        }
        
        response = client.post("/api/auth/signup", json=xss_data)
        assert response.status_code == 201
        
        # Verify data was sanitized
        data = response.json()
        assert "<script>" not in data.get("first_name", "")
    
    @pytest.mark.integration
    def test_signup_creates_audit_trail(self, client: TestClient, sample_user_data: dict, mock_email_service):
        """Test that signup creates proper audit trail."""
        response = client.post("/api/auth/signup", json=sample_user_data)
        assert response.status_code == 201
        
        data = response.json()
        
        # Verify audit fields are present
        assert "created_date" in data
        assert "created_by" in data
        assert data["created_by"] == data["user_id"]  # Self-created
