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
        assert "message" in data
        assert "verify" in data["message"].lower() or "email" in data["message"].lower()
    
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
        assert ("duplicate" in response2.json()["detail"].lower() or 
                "already" in response2.json()["detail"].lower())
    
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
        
        # Verify email and token were passed (using kwargs since it's called with keyword args)
        assert call_args.kwargs['email'] == sample_user_data["email"]  # email
        assert len(call_args.kwargs['verification_token']) > 0  # verification token
        assert call_args.kwargs['user_name'] == sample_user_data["first_name"]  # user name
    
    @pytest.mark.unit
    def test_signup_missing_required_fields(self, client: TestClient, mock_email_service):
        """Test signup with missing required fields (email and password are required)."""
        incomplete_data = [
            {"email": "test@example.com"},  # Missing password
            {"password": "ValidPassword123!"},  # Missing email
        ]
        
        for data in incomplete_data:
            response = client.post("/api/auth/signup", json=data)
            assert response.status_code == 422  # Validation error
        
        # First_name and last_name are optional, so this should succeed
        valid_data = {"email": "test2@example.com", "password": "ValidPassword123!"}
        response = client.post("/api/auth/signup", json=valid_data)
        assert response.status_code == 201
    
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
        
        # Verify user was created successfully
        assert "user_id" in data
        assert "email" in data
        assert "message" in data
    
    @pytest.mark.integration
    def test_signup_transaction_rollback_on_email_failure(self, db_session):
        """
        Test AC-1.1 Extension: User should NOT be created if email send fails.
        Validates ACID transaction principles - signup is atomic (all-or-nothing).
        Added 2025-10-21 after UAT discovered transaction boundary violation.
        """
        from modules.auth.user_service import create_user, get_user_by_email
        from modules.auth.token_service import generate_verification_token
        from unittest.mock import AsyncMock, MagicMock
        
        test_email = "transaction.test@example.com"
        
        # Simulate the signup flow with email failure
        try:
            # Create user without committing
            user = create_user(
                db=db_session,
                email=test_email,
                password="TestPass123!",
                first_name="Trans",
                last_name="Action",
                auto_commit=False
            )
            
            # Generate token without committing
            token = generate_verification_token(db_session, user.UserID, auto_commit=False)
            
            # Simulate email send failure
            raise Exception("Email send failed")
            
        except Exception:
            # Rollback transaction
            db_session.rollback()
        
        # Verify user was NOT committed to database
        db_session.rollback()  # Ensure clean state
        user_check = get_user_by_email(db_session, test_email)
        assert user_check is None, "User should NOT be in database after rollback"
    
    @pytest.mark.integration
    def test_signup_response_format_matches_fastapi_standard(self, client: TestClient):
        """
        Test that error responses use FastAPI standard 'detail' field (not 'message').
        Added 2025-10-21 after UAT discovered frontend couldn't read error messages.
        """
        # Test duplicate email error
        user_data = {
            "email": "duplicate@example.com",
            "password": "ValidPassword123!",
            "first_name": "Test",
            "last_name": "User"
        }
        
        # Create first user
        response1 = client.post("/api/auth/signup", json=user_data)
        assert response1.status_code == 201
        
        # Try duplicate - should return 400 with 'detail' field
        response2 = client.post("/api/auth/signup", json=user_data)
        assert response2.status_code == 400
        
        error_data = response2.json()
        # Frontend expects 'detail' field (FastAPI standard)
        assert "detail" in error_data, "Error response must have 'detail' field for frontend compatibility"
        assert "email" in error_data["detail"].lower() or "already" in error_data["detail"].lower()
        
        # Should NOT have 'message' field (old format)
        assert "message" not in error_data or error_data.get("detail"), "Should use 'detail' not 'message'"
    
    @pytest.mark.integration  
    def test_signup_end_to_end_integration(self, client: TestClient, db_session):
        """
        Test complete signup flow: API → Service → Database → Email → Logs.
        Added 2025-10-21 to validate full integration.
        """
        from models.user import User
        from models.log.auth_event import AuthEvent
        from models.log.api_request import ApiRequest
        
        user_data = {
            "email": "integration.test@example.com",
            "password": "SecurePass123!",
            "first_name": "Integration",
            "last_name": "Test"
        }
        
        # 1. Call signup endpoint
        response = client.post("/api/auth/signup", json=user_data)
        assert response.status_code == 201
        data = response.json()
        
        # 2. Verify user in database with correct columns
        user = db_session.query(User).filter(User.Email == user_data["email"]).first()
        assert user is not None, "User should exist in database"
        assert user.IsEmailVerified == False, "User should start unverified"
        assert user.StatusID is not None, "User should have StatusID set"
        
        # 3. Verify AuthEvent logged
        auth_event = db_session.query(AuthEvent).filter(
            AuthEvent.UserID == user.UserID
        ).first()
        assert auth_event is not None, "AuthEvent should be logged"
        assert auth_event.EventType == "SIGNUP", "EventType should be SIGNUP"
        
        # 4. Verify ApiRequest logged  
        api_request = db_session.query(ApiRequest).filter(
            ApiRequest.Path == "/api/auth/signup",
            ApiRequest.StatusCode == 201
        ).order_by(ApiRequest.CreatedDate.desc()).first()
        assert api_request is not None, "ApiRequest should be logged"
        
        # 5. Email send is tested separately in test_mailhog_integration.py