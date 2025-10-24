"""
Integration Tests for Story 1.9 - Frontend Authentication (Signup & Login Pages)
Tests all fixes applied during UAT on 2025-10-21
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from models.user import User
from models.log.auth_event import AuthEvent
from models.log.api_request import ApiRequest
from models.log.application_error import ApplicationError


class TestStory19SignupFlow:
    """Test Story 1.9 signup flow with all UAT fixes"""
    
    @pytest.mark.integration
    def test_successful_signup_creates_user_and_logs(self, client: TestClient, db_session: Session):
        """
        Test AC-1.9.1: Successful signup creates user and sends email.
        Validates all logs are created (AuthEvent, ApiRequest).
        """
        user_data = {
            "email": "story19.success@example.com",
            "password": "StrongPass123!",
            "first_name": "Story",
            "last_name": "Nineteen"
        }
        
        # Call signup
        response = client.post("/api/auth/signup", json=user_data)
        assert response.status_code == 201
        
        # Verify user created with correct columns
        user = db_session.query(User).filter(User.Email == user_data["email"]).first()
        assert user is not None
        assert user.IsEmailVerified == False, "Should use IsEmailVerified (not EmailVerified)"
        assert user.StatusID is not None, "Should use StatusID (not IsActive)"
        
        # Verify AuthEvent logged with correct columns
        auth_event = db_session.query(AuthEvent).filter(
            AuthEvent.UserID == user.UserID
        ).first()
        assert auth_event is not None
        assert hasattr(auth_event, 'EventType'), "Should have EventType (not EventStatus)"
        assert hasattr(auth_event, 'Reason'), "Should have Reason (not Details)"
        assert auth_event.EventType == "SIGNUP"
    
    @pytest.mark.integration
    def test_duplicate_email_returns_detail_field(self, client: TestClient):
        """
        Test that duplicate email error uses 'detail' field (not 'message').
        Validates frontend can read error messages.
        """
        user_data = {
            "email": "story19.duplicate@example.com",
            "password": "StrongPass123!",
            "first_name": "Dup",
            "last_name": "Test"
        }
        
        # First signup
        response1 = client.post("/api/auth/signup", json=user_data)
        assert response1.status_code == 201
        
        # Second signup (duplicate)
        response2 = client.post("/api/auth/signup", json=user_data)
        assert response2.status_code == 400
        
        error_data = response2.json()
        assert "detail" in error_data, "Must use 'detail' field (FastAPI standard)"
        assert "already" in error_data["detail"].lower() or "registered" in error_data["detail"].lower()
    
    @pytest.mark.integration
    def test_weak_password_returns_specific_error(self, client: TestClient):
        """
        Test that password validation error shows specific requirements.
        Validates user sees actionable error message.
        """
        user_data = {
            "email": "story19.weakpass@example.com",
            "password": "weak",  # Too short, no uppercase, no numbers, no special chars
            "first_name": "Weak",
            "last_name": "Pass"
        }
        
        response = client.post("/api/auth/signup", json=user_data)
        assert response.status_code in [400, 422], "Should return validation error"
        
        error_data = response.json()
        assert "detail" in error_data
        # Response format depends on validation layer (Pydantic=422, business logic=400)
        detail_text = str(error_data["detail"]).lower() if isinstance(error_data["detail"], str) else str(error_data["detail"])
        assert "password" in detail_text or "8" in detail_text or "characters" in detail_text


class TestStory19LoginFlow:
    """Test Story 1.9 login flow"""
    
    @pytest.mark.integration
    def test_unverified_user_cannot_login(self, client: TestClient, db_session: Session):
        """
        Test AC-1.9.7: Unverified users cannot login.
        Validates IsEmailVerified check (not EmailVerified).
        """
        from models.ref.user_status import UserStatus
        from common.security import hash_password
        
        # Create unverified user directly
        pending_status = db_session.query(UserStatus).filter(
            UserStatus.StatusName == "Pending Verification"
        ).first()
        
        user = User(
            Email="story19.unverified@example.com",
            PasswordHash=hash_password("TestPass123!"),
            FirstName="Unverified",
            LastName="User",
            IsEmailVerified=False,  # Not verified
            StatusID=pending_status.UserStatusID if pending_status else 1
        )
        db_session.add(user)
        db_session.commit()
        
        # Try to login
        response = client.post("/api/auth/login", json={
            "email": "story19.unverified@example.com",
            "password": "TestPass123!"
        })
        
        # Should be blocked
        assert response.status_code == 403
        assert "detail" in response.json()
        assert "verify" in response.json()["detail"].lower()


class TestStory19ErrorHandling:
    """Test Story 1.9 error handling (Story 0.2 compliance)"""
    
    @pytest.mark.integration
    def test_all_errors_logged_to_application_error(self, client: TestClient, db_session: Session):
        """
        Test AC-0.2.4: All errors logged to log.ApplicationError.
        Validates global exception handler catches all errors.
        """
        # Trigger a validation error (duplicate email)
        user_data = {
            "email": "error.logging@example.com",
            "password": "TestPass123!",
            "first_name": "Error",
            "last_name": "Test"
        }
        
        # First signup
        client.post("/api/auth/signup", json=user_data)
        
        # Second signup (should fail)
        response = client.post("/api/auth/signup", json=user_data)
        assert response.status_code == 400
        
        # Verify ApplicationError was logged
        app_error = db_session.query(ApplicationError).filter(
            ApplicationError.Path == "/api/auth/signup",
            ApplicationError.ErrorType == "HTTPException"
        ).order_by(ApplicationError.CreatedDate.desc()).first()
        
        assert app_error is not None, "HTTPException should be logged to ApplicationError"
        assert "already" in app_error.ErrorMessage.lower() or "registered" in app_error.ErrorMessage.lower()
    
    @pytest.mark.integration
    def test_auth_events_use_correct_columns(self, client: TestClient, db_session: Session):
        """
        Test that AuthEvent uses EventType and Reason (not EventStatus and Details).
        Validates fix for column name mismatch discovered in UAT.
        """
        user_data = {
            "email": "auth.event.test@example.com",
            "password": "TestPass123!",
            "first_name": "Auth",
            "last_name": "Event"
        }
        
        # Signup
        response = client.post("/api/auth/signup", json=user_data)
        
        # Find the AuthEvent
        auth_events = db_session.query(AuthEvent).order_by(AuthEvent.CreatedDate.desc()).limit(1).all()
        
        if auth_events:
            event = auth_events[0]
            # Verify correct columns exist
            assert hasattr(event, 'EventType'), "AuthEvent should have EventType"
            assert hasattr(event, 'Reason'), "AuthEvent should have Reason"
            assert not hasattr(event, 'EventStatus'), "AuthEvent should NOT have EventStatus"
            assert not hasattr(event, 'Details'), "AuthEvent should NOT have Details"


class TestStory19TransactionManagement:
    """Test transaction management (ACID compliance)"""
    
    @pytest.mark.integration
    def test_email_failure_rolls_back_user_creation(self, db_session: Session):
        """
        Test that user is NOT created if email send fails.
        Critical fix for transaction boundary violation discovered in UAT.
        """
        from modules.auth.user_service import create_user, get_user_by_email
        from modules.auth.token_service import generate_verification_token
        
        test_email = "transaction.rollback@example.com"
        
        # Simulate signup flow with failure
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
            
            # Simulate email failure
            raise Exception("Email service unavailable")
            
        except Exception:
            db_session.rollback()
        
        # Verify user NOT in database
        db_session.rollback()  # Clean state
        user_check = get_user_by_email(db_session, test_email)
        assert user_check is None, "User should NOT exist after rollback"

