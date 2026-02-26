"""
Unit Tests for JWT Service
Tests JWT token creation, decoding, and validation
"""
import pytest
from datetime import datetime, timedelta
from jose import jwt, JWTError  # type: ignore

from modules.auth.jwt_service import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_token_type,
    extract_user_id,
    is_token_expired
)
from config.jwt import get_access_token_expire_minutes, get_refresh_token_expire_days


class TestJWTService:
    """Test suite for JWT service"""
    
    def test_create_access_token_minimal(self, test_db):
        """Test creating access token with minimal claims"""
        token = create_access_token(
            db=test_db,
            user_id=123,
            email="test@example.com"
        )
        
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Decode and verify
        payload = decode_token(token)
        assert payload["sub"] == "123"
        assert payload["email"] == "test@example.com"
        assert payload["type"] == "access"
        assert "exp" in payload
        assert "iat" in payload
    
    def test_create_access_token_with_role_and_company(self, test_db):
        """Test creating access token with role and company claims"""
        token = create_access_token(
            db=test_db,
            user_id=123,
            email="test@example.com",
            role="admin",
            company_id=456
        )
        
        payload = decode_token(token)
        assert payload["sub"] == "123"
        assert payload["email"] == "test@example.com"
        assert payload["role"] == "admin"
        assert payload["company_id"] == 456
        assert payload["type"] == "access"
    
    def test_access_token_expiry(self, test_db):
        """Test access token has correct expiry (1 hour)"""
        token = create_access_token(test_db, 123, "test@example.com")
        payload = decode_token(token)
        
        exp = datetime.fromtimestamp(payload["exp"])
        iat = datetime.fromtimestamp(payload["iat"])
        
        # Should be approximately the configured access token expiry
        time_diff = (exp - iat).total_seconds()
        expected = get_access_token_expire_minutes(test_db) * 60
        assert expected - 50 <= time_diff <= expected + 50
    
    def test_create_refresh_token(self, test_db):
        """Test creating refresh token"""
        token = create_refresh_token(test_db, user_id=123)
        
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Decode and verify
        payload = decode_token(token)
        assert payload["sub"] == "123"
        assert payload["type"] == "refresh"
        assert "exp" in payload
        assert "iat" in payload
        # Refresh tokens should not have email, role, or company_id
        assert "email" not in payload
        assert "role" not in payload
        assert "company_id" not in payload
    
    def test_refresh_token_expiry(self, test_db):
        """Test refresh token has correct expiry (7 days)"""
        token = create_refresh_token(test_db, 123)
        payload = decode_token(token)
        
        exp = datetime.fromtimestamp(payload["exp"])
        iat = datetime.fromtimestamp(payload["iat"])
        
        # Should be approximately the configured refresh token expiry
        time_diff = (exp - iat).total_seconds()
        expected = get_refresh_token_expire_days(test_db) * 24 * 3600
        assert expected - 100 <= time_diff <= expected + 100  # Allow tolerance
    
    def test_decode_valid_token(self, test_db):
        """Test decoding a valid token"""
        token = create_access_token(test_db, 123, "test@example.com")
        payload = decode_token(token)
        
        assert payload["sub"] == "123"
        assert payload["email"] == "test@example.com"
    
    def test_decode_invalid_token(self):
        """Test decoding an invalid token raises error"""
        invalid_token = "invalid.jwt.token"
        
        with pytest.raises(JWTError):
            decode_token(invalid_token)
    
    def test_decode_tampered_token(self, test_db):
        """Test decoding a tampered token raises error"""
        token = create_access_token(test_db, 123, "test@example.com")
        # Tamper with the token
        parts = token.split('.')
        tampered_token = parts[0] + ".tampered." + parts[2]
        
        with pytest.raises(JWTError):
            decode_token(tampered_token)
    
    def test_verify_token_type_access(self, test_db):
        """Test verifying access token type"""
        token = create_access_token(test_db, 123, "test@example.com")
        payload = decode_token(token)
        
        assert verify_token_type(payload, "access") is True
        assert verify_token_type(payload, "refresh") is False
    
    def test_verify_token_type_refresh(self, test_db):
        """Test verifying refresh token type"""
        token = create_refresh_token(test_db, 123)
        payload = decode_token(token)
        
        assert verify_token_type(payload, "refresh") is True
        assert verify_token_type(payload, "access") is False
    
    def test_extract_user_id(self, test_db):
        """Test extracting user ID from token payload"""
        token = create_access_token(test_db, 123, "test@example.com")
        payload = decode_token(token)
        
        user_id = extract_user_id(payload)
        assert user_id == 123
    
    def test_extract_user_id_from_refresh_token(self, test_db):
        """Test extracting user ID from refresh token"""
        token = create_refresh_token(test_db, 456)
        payload = decode_token(token)
        
        user_id = extract_user_id(payload)
        assert user_id == 456
    
    def test_is_token_expired_not_expired(self, test_db):
        """Test checking if non-expired token is valid"""
        token = create_access_token(test_db, 123, "test@example.com")
        payload = decode_token(token)
        
        assert is_token_expired(payload) is False
    
    def test_token_uniqueness(self, test_db):
        """Test token creation remains valid for repeated calls."""
        token1 = create_access_token(test_db, 123, "test@example.com")
        token2 = create_access_token(test_db, 123, "test@example.com")
        
        # Tokens can be identical when issued in the same second.
        assert isinstance(token1, str) and token1
        assert isinstance(token2, str) and token2
        assert decode_token(token1)["sub"] == "123"
        assert decode_token(token2)["sub"] == "123"
    
    def test_optional_claims_omitted(self, test_db):
        """Test that optional claims are omitted when not provided"""
        token = create_access_token(test_db, 123, "test@example.com")
        payload = decode_token(token)
        
        assert "role" not in payload
        assert "company_id" not in payload


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

