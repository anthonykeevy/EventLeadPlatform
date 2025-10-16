"""
Tests for Password Reset Flow (Story 1.4)
Tests AC-1.4.1 through AC-1.4.10
"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from datetime import datetime, timedelta

from modules.auth.schemas import PasswordResetRequestSchema, PasswordResetConfirmSchema
from modules.auth.token_service import (
    generate_password_reset_token,
    validate_password_reset_token,
    mark_password_reset_token_used
)


class TestPasswordResetRequest:
    """Test password reset request endpoint (AC-1.4.1, AC-1.4.2, AC-1.4.4)"""
    
    def test_password_reset_request_existing_email(self, client: TestClient, sample_user_data: dict):
        """Test password reset request for existing email"""
        # Create user first
        signup_response = client.post("/api/auth/signup", json=sample_user_data)
        assert signup_response.status_code == 201
        
        # Request password reset
        response = client.post(
            "/api/auth/password-reset/request",
            json={"email": sample_user_data["email"]}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "reset link has been sent" in data["message"]
    
    def test_password_reset_request_non_existing_email(self, client: TestClient):
        """Test AC-1.4.4: Same response for non-existing email (security)"""
        response = client.post(
            "/api/auth/password-reset/request",
            json={"email": "nonexistent@example.com"}
        )
        
        # Should return same success message (don't leak email existence)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "reset link has been sent" in data["message"]
    
    def test_password_reset_token_generated(self, test_db, sample_user_data: dict):
        """Test AC-1.4.2: Password reset token generated with 1-hour expiry"""
        from models.user import User
        
        # Create user
        user = User(
            Email=sample_user_data["email"],
            PasswordHash="hashed",
            FirstName=sample_user_data["first_name"],
            LastName=sample_user_data["last_name"]
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        # Generate password reset token
        token = generate_password_reset_token(test_db, user.UserID)
        
        assert token is not None
        assert len(token) > 30  # Crypto-secure token should be long
        
        # Validate token was stored
        token_record = validate_password_reset_token(test_db, token)
        assert token_record is not None
        assert token_record.UserID == user.UserID
        assert token_record.IsUsed is False
        
        # Check expiry is ~1 hour
        expiry_delta = token_record.ExpiresAt - datetime.utcnow()
        assert 55 < expiry_delta.total_seconds() / 60 < 65  # ~60 minutes


class TestPasswordResetConfirm:
    """Test password reset confirmation endpoint (AC-1.4.5, AC-1.4.6, AC-1.4.7, AC-1.4.8)"""
    
    def test_password_reset_confirm_valid_token(self, client: TestClient, test_db, sample_user_data: dict):
        """Test AC-1.4.5, AC-1.4.7: Valid token resets password"""
        from models.user import User
        from common.security import hash_password, verify_password
        
        # Create user
        old_password = sample_user_data["password"]
        user = User(
            Email=sample_user_data["email"],
            PasswordHash=hash_password(old_password),
            FirstName=sample_user_data["first_name"],
            LastName=sample_user_data["last_name"],
            EmailVerified=True
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        # Generate token
        token = generate_password_reset_token(test_db, user.UserID)
        
        # Reset password
        new_password = "NewSecureP@ss123"
        response = client.post(
            "/api/auth/password-reset/confirm",
            json={
                "token": token,
                "new_password": new_password
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "reset successfully" in data["message"]
        
        # Verify password was updated
        test_db.refresh(user)
        assert verify_password(new_password, user.PasswordHash)
        assert not verify_password(old_password, user.PasswordHash)
    
    def test_password_reset_confirm_invalid_token(self, client: TestClient):
        """Test AC-1.4.5: Invalid token returns error"""
        response = client.post(
            "/api/auth/password-reset/confirm",
            json={
                "token": "invalid_token_123",
                "new_password": "NewSecureP@ss123"
            }
        )
        
        assert response.status_code == 400
        assert "Invalid or expired" in response.json()["detail"]
    
    def test_password_reset_confirm_weak_password(self, client: TestClient, test_db, sample_user_data: dict):
        """Test AC-1.4.6: Weak password rejected"""
        from models.user import User
        from common.security import hash_password
        
        # Create user
        user = User(
            Email=sample_user_data["email"],
            PasswordHash=hash_password(sample_user_data["password"]),
            FirstName=sample_user_data["first_name"],
            LastName=sample_user_data["last_name"]
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        # Generate token
        token = generate_password_reset_token(test_db, user.UserID)
        
        # Try to reset with weak password
        response = client.post(
            "/api/auth/password-reset/confirm",
            json={
                "token": token,
                "new_password": "weak"  # Too short, no uppercase, no special char
            }
        )
        
        assert response.status_code == 400
        assert "security requirements" in response.json()["detail"]
    
    def test_password_reset_token_marked_used(self, client: TestClient, test_db, sample_user_data: dict):
        """Test AC-1.4.8: Token marked as used after successful reset"""
        from models.user import User
        from common.security import hash_password
        
        # Create user
        user = User(
            Email=sample_user_data["email"],
            PasswordHash=hash_password(sample_user_data["password"]),
            FirstName=sample_user_data["first_name"],
            LastName=sample_user_data["last_name"]
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        # Generate token
        token = generate_password_reset_token(test_db, user.UserID)
        
        # Reset password
        client.post(
            "/api/auth/password-reset/confirm",
            json={
                "token": token,
                "new_password": "NewSecureP@ss123"
            }
        )
        
        # Try to use token again - should fail
        response = client.post(
            "/api/auth/password-reset/confirm",
            json={
                "token": token,
                "new_password": "AnotherP@ss456"
            }
        )
        
        assert response.status_code == 400
        assert "Invalid or expired" in response.json()["detail"]


class TestPasswordResetTokenExpiry:
    """Test AC-1.4.10: Token can only be used once within 1-hour window"""
    
    def test_expired_token_rejected(self, test_db, sample_user_data: dict):
        """Test that expired token (>1 hour) is rejected"""
        from models.user import User
        from models.user_password_reset_token import UserPasswordResetToken
        import secrets
        
        # Create user
        user = User(
            Email=sample_user_data["email"],
            PasswordHash="hashed",
            FirstName=sample_user_data["first_name"],
            LastName=sample_user_data["last_name"]
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        # Create expired token (2 hours ago)
        expired_token = secrets.token_urlsafe(32)
        token_record = UserPasswordResetToken(
            UserID=user.UserID,
            Token=expired_token,
            ExpiresAt=datetime.utcnow() - timedelta(hours=1, minutes=1),  # Expired
            IsUsed=False,
            CreatedDate=datetime.utcnow() - timedelta(hours=2)
        )
        test_db.add(token_record)
        test_db.commit()
        
        # Try to validate expired token
        validated = validate_password_reset_token(test_db, expired_token)
        assert validated is None  # Should be rejected


class TestPasswordResetSecurity:
    """Test security aspects (AC-1.4.4, AC-1.4.9, AC-1.4.10)"""
    
    def test_no_information_leakage(self, client: TestClient):
        """Test AC-1.4.4: No information leakage about email existence"""
        # Request reset for existing email (if any)
        response1 = client.post(
            "/api/auth/password-reset/request",
            json={"email": "existing@example.com"}
        )
        
        # Request reset for non-existing email
        response2 = client.post(
            "/api/auth/password-reset/request",
            json={"email": "nonexist@example.com"}
        )
        
        # Both should return identical responses
        assert response1.status_code == response2.status_code == 200
        assert response1.json()["message"] == response2.json()["message"]
        assert response1.json()["success"] == response2.json()["success"] == True


# Mark all tests with Story 1.4 marker
pytestmark = pytest.mark.story_1_4

